from os import curdir
import sqlite3
from types import new_class
import pandas as pd
from streamlit.elements.arrow import Data
from datetime import datetime

class Database:
    def insert_data(data):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS study(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date text,
                study_hr integer,
                study_min integer,
                minute_workout integer,
                description text,
                satisfaction integer
        )""")

        cursor.execute(""" INSERT INTO study 
                (date, study_hr, study_min, minute_workout, description, satisfaction)
                VALUES (?, ?, ?, ?, ?, ?)
         """,   (data['date'], data['study_hr'], data['study_min'], data['workout'], data['description'], data['satisfaction']))

        conn.commit()
        conn.close()

    def get_data():
        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            all_data = cursor.execute("SELECT * FROM study").fetchall()

            conn.commit()
            conn.close()
            return all_data
        except:
            return 'error'

    def delete_table():
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute("DROP TABLE study")

        conn.commit()
        conn.close()

    def delete_data(data_id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
    
        cursor.execute("DELETE FROM study WHERE id =?", (data_id,))
        conn.commit()
        conn.close()


    def feature_engineering():
        conn = sqlite3.connect('data.db')
        df = pd.read_sql_query('SELECT * from study', conn)
        df.columns = ['ID', 'Date' ,'Study(hr)', 'Study(min)', 'Workout(min)', 'Description', 'Satisfaction']

        # Convert to datetime object
        df.Date = pd.to_datetime(df.Date)

        # Add year, month, and day columns
        new_columns = ['Year', 'Month', 'Day']
        for column in new_columns:
            if column == 'Year':
                df[column] = df.Date.apply(lambda x: int(x.year))
            elif column == 'Month':
                df[column] = df.Date.apply(lambda x: int(x.month))
            else:
                df[column] = df.Date.apply(lambda x: int(x.day))

        df.Date = df.Date.astype(str)

        conn.close()
        return df