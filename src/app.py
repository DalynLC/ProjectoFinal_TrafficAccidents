import streamlit as st
from streamlit_lottie import st_lottie
import datetime as dt
import numpy as np
from pickle import load

#carga el modelo
model = load(open("../src/model_classifier.sav", "rb"))

page_bg_img = '''
<style>
body {
background-image: url("../src/bg2.jpg");
background-size: cover;
}
</style>
'''
st.set_page_config(page_title="Predictor de Accidentes de Tráfico", page_icon=":oncoming_automobile:", layout="wide")
st.markdown(page_bg_img, unsafe_allow_html=True)

with st.container():
    st.title(":blue_car: Predictor de Lesiones en Accidentes de Tráfico :car:")
    st.write("Esta aplicación permite predecir la gravedad de las heridas en un accidente de tráfico.")

with st.container():
    st.write("Fecha: ")
    st.write("Hora: ")
    st.subheader("🔍 Ingresa las condiciones del accidente")
    col1, col2 = st.columns(2)
    with col1:
        traffic_control_device = st.selectbox('Select Traffic Device',['TRAFFIC SIGNAL','STOP SIGN/FLASHER','NO CONTROLS','UNKNOW','OTHER'])
        weather_condition = st.selectbox('Select weather',['CLEAR','RAIN','CLOUDY/OVERCAST','SNOW','UNKNOWN'])
        alignment = st.selectbox('Select alignment',['STRAIGHT AND LEVEL','STRAIGHT ON GRADE','CURVE, LEVEL','STRAIGHT ON HILLCREST','CURVE ON GRADE'])
        roadway_surface_cond = st.selectbox('Roadway Surface Condition',['DRY','WET','UNKNOWN','SNOW OR SLUSH','ICE'])
        road_defect = st.selectbox('Roadway Defect',['NO DEFECTS','UNKNOWN','WORN SURFACE','OTHER','RUT, HOLES'])

    with col2:
        crash_type = st.selectbox('Crash Type',['NO INJURY / DRIVE AWAY','INJURY AND / OR TOW DUE TO CRASH'])
        intersection_related_i = st.selectbox('Intersection related',['TRUE','FALSE'])
        prim_contributory_cause = st.selectbox('Primary Contributory Cause',['UNABLE TO DETERMINE','FAILING TO YIELD RIGHT-OF-WAY','FOLLOWING TOO CLOSELY','DISREGARDING TRAFFIC SIGNALS','IMPROPER TURNING/NO SIGNAL'])
        num_units = st.slider("Number Units",1,11)
        total_fatal_injuries = st.slider('Fatal Injuries',0,10)
        total_non_fatal_injuries= st.slider('Non Fatal Injuries',0,21)

with st.container():
    st.markdown("---")
    if st.button("✨ Predict Most Severe Injury"):
        input_data = np.array([[traffic_control_device,weather_condition,alignment,roadway_surface_cond,crash_type,intersection_related_i,prim_contributory_cause,num_units,total_fatal_injuries,total_non_fatal_injuries]])
        prediction = model.predict(input_data)[0]

        #st.success(f"🏡 El precio predicho de la casa es: **${prediction * 1000:.2f} USD**")


