import streamlit as st
from streamlit_lottie import st_lottie
import datetime as dt
import numpy as np
from pickle import load
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import pandas as pd


#scaler = MinMaxScaler()
scaler = StandardScaler()
#carga el modelo
model = load(open("../src/model_classifier.sav", "rb"))

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://www.mapfre.com.mx/media/545x257_087_autoTurista_noticias_carrilRapido.jpg");
  background-size: cover;
}
.my-container {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 5px;
}
</style>
"""
st.set_page_config(page_title="Predictor de Accidentes de Tráfico", page_icon=":oncoming_automobile:", layout="wide")
st.markdown(page_element, unsafe_allow_html=True)

with st.container():
    st.title(":blue_car: Predictor de Lesiones en Accidentes de Tráfico :car:",)
    
    st.write("Esta aplicación permite predecir la gravedad de las heridas en un accidente de tráfico.")


with st.container():
    col1, col2 = st.columns(2)

days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] 
month = ["January","February","March","April","May","June","July","August","September","October","November","December"]
tcd = ['TRAFFIC SIGNAL', 'NO CONTROLS', 'STOP SIGN/FLASHER', 'UNKNOWN', 'OTHER', 'PEDESTRIAN CROSSING SIGN', 'OTHER WARNING SIGN', 'YIELD', 'FLASHING CONTROL SIGNAL', 'LANE USE MARKING', 'OTHER REG. SIGN', 'DELINEATORS', 'SCHOOL ZONE', 'POLICE/FLAGMAN', 'NO PASSING', 'RR CROSSING SIGN', 'RAILROAD CROSSING GATE', 'BICYCLE CROSSING SIGN', 'OTHER RAILROAD CROSSING']
wc = ['CLEAR', 'RAIN', 'SNOW', 'CLOUDY/OVERCAST', 'UNKNOWN', 'FOG/SMOKE/HAZE', 'BLOWING SNOW', 'FREEZING RAIN/DRIZZLE', 'OTHER', 'SLEET/HAIL', 'SEVERE CROSS WIND GATE', 'BLOWING SAND, SOIL, DIRT']
fct = ['TURNING', 'REAR END', 'ANGLE', 'FIXED OBJECT', 'REAR TO FRONT', 'SIDESWIPE SAME DIRECTION', 'SIDESWIPE OPPOSITE DIRECTION', 'PEDALCYCLIST', 'PEDESTRIAN', 'HEAD ON', 'PARKED MOTOR VEHICLE', 'OTHER NONCOLLISION', 'OVERTURNED', 'OTHER OBJECT', 'REAR TO SIDE', 'ANIMAL', 'TRAIN', 'REAR TO REAR']
rsc = ['UNKNOWN', 'DRY', 'WET', 'SNOW OR SLUSH', 'ICE', 'OTHER', 'SAND, MUD, DIRT']
rd = ['UNKNOWN', 'NO DEFECTS', 'OTHER', 'SHOULDER DEFECT', 'WORN SURFACE', 'DEBRIS ON ROADWAY', 'RUT, HOLES']
ir = ['TRUE','FALSE']


fecha = dt.date.today()
dDay = days[fecha.weekday()] 
dMonth = month[fecha.month-1]
dDayN = str(fecha.day)
dYear = str(fecha.year)

with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1: 
        #st.write("Date: ", dDay, " ", dDayN, " ", dMonth," ", dYear)
        crash_day = st.selectbox('Day',["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"])
    with col2:    
        crash_month = st.selectbox('Month',["January","February","March","April","May","June","July","August","September","October","November","December"])
    with col3:
        crash_hour = st.selectbox('Time',[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])

with st.container(border=True):
    st.subheader("🔍 Ingresa las condiciones del accidente")
    col1, col2 = st.columns(2)
    with col1:
        traffic_control_device = st.selectbox('Select Traffic Device',tcd)
        weather_condition = st.selectbox('Select weather',wc)
        first_crash_type = st.selectbox('Select first crash type',fct)
        roadway_surface_cond = st.selectbox('Roadway Surface Condition',rsc)
        
    with col2:
        road_defect = st.selectbox('Roadway Defect',rd)
        intersection_related_i = st.selectbox('Intersection related',ir)
        num_units = st.slider("Number Units",1,11)
        total_non_fatal_injuries= st.slider('Non Fatal Injuries',0,21)

with st.container(border=True):
    if st.button("Predict Most Severe Injury"):
        input_data = np.array([[tcd.index(traffic_control_device),wc.index(weather_condition),fct.index(first_crash_type),rsc.index(roadway_surface_cond),rd.index(road_defect),ir.index(intersection_related_i),num_units,crash_hour,days.index(crash_day),month.index(crash_month),total_non_fatal_injuries]])
        input_data = pd.DataFrame(input_data, columns=['traffic_control_device', 'weather_condition', 'first_crash_type',
       'roadway_surface_cond', 'road_defect', 'intersection_related_i',
       'num_units', 'crash_hour', 'crash_day_of_week', 'crash_month',
       'total_non_fatal_injuries'])
        array_escalado = scaler.fit_transform(input_data)

        #st.write("x",input_data)
        prediction = model.predict(input_data)[0]
        pred = ''
        
        if prediction == 0:
            pred = 'NO INDICATION OF INJURY'
        elif prediction == 1:
            pred = 'NONINCAPACITATING INJURY'
        elif prediction == 2:
            pred = 'INCAPACITATING INJURY'
        elif prediction == 3:
            pred = 'REPORTED, NOT EVIDENT'

        st.success(f"🏡 La herida más grave en este accidente será {pred}")


