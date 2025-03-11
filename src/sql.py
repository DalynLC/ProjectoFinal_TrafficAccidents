import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

# load the .env file variables
load_dotenv()

# 1) Connect to the database here using the SQLAlchemy's create_engine function

connection_string = f"postgresql://{os.getenv('gitpod')}:{os.getenv('postgres')}@{os.getenv('localhost')}/{os.getenv('sample-db')}"
engine = create_engine(connection_string).execution_options(autocommit=True)
engine.connect()