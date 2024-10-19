import mysql.connector
import MySQLdb
from sqlalchemy import create_engine
import my_constant as constant
import pandas as pd


def establish_connection():
    try:
        # The database URL must be in a specific format
        db_url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}/{DBNAME}"
        # DB username, password, host and database name
        db_url = db_url.format(
                 USER = constant.USER,
                 PWD = constant.PASSWORD,
                 HOST = constant.HOST,
                 DBNAME = constant.DATA_BASE_NAME
                )
        # Create the DB engine instance. We'll use
        # this engine to connect to the database
        engine = create_engine(db_url, echo=False)
        print("Connection established")
        return engine
    except mysql.connector.Error as err:
           print("An error occurred:", err)

def create_table():
    metadata_obj = create_engine.MetaData()             

def insert_into_db(tablename, data):
    engine = establish_connection()
    with engine.begin() as conn:
        # Invoke DataFrame method to_sql() to
        # create the table 'largest_cities' and
        # insert all the DataFrame rows into it
         data.to_sql(
                    name=tablename, # database table
                    con=engine, # database connection
                    if_exists='append',
                    index=False # Don't save index
                )    
    print("record inserted inside DB")          

def read_data(query):
    engine = establish_connection()      
    data = pd.read_sql(query,con=engine)
    return data