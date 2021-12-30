import numpy as np
import streamlit as st
from streamlit import cursor
from streamlit.elements.arrow import Data
from data import *
from analysis import Visualization
import sqlite3

st.set_page_config(
    page_title='Productivity Tracker',
    page_icon=':book:',
)

class Sidebar:
    def input_data():
        with st.form(key='input_form', clear_on_submit=True):
            with st.sidebar:
                st.header('Study Input')
                input_date = st.date_input('Date')
                input_hr = st.number_input('Study (Hr)', min_value=0, max_value=24)
                input_min = st.number_input('Study (Min)', min_value=0, max_value=60)
                input_workout = st.number_input('Minute Workout', min_value=0, max_value=720)
                input_description = st.text_input('Study Description')
                input_satisfaction = st.number_input('Satisfaction scale (0-10)', min_value=0.0, max_value=10.0, step=0.5)
                submit_button = st.form_submit_button('Submit')

                # Group data into a dictionary
                data = {
                    'date':str(input_date),
                    'study_hr':int(input_hr),
                    'study_min':int(input_min),
                    'workout':int(input_workout),
                    'description':str(input_description),
                    'satisfaction':float(input_satisfaction)
                }

                # Input to database
                if submit_button:
                    # Insert to database
                    db = Database
                    db.insert_data(data)

                    # Succes message
                    st.success('Data added!')

                # Line separator
                st.write('---')
    
    def delete_data():
        with st.form(key='delete_form'):
            with st.sidebar:
                st.header('Delete data')
                id_input = st.number_input('Row ID', min_value=0)
                delete_data_button = st.form_submit_button('Delete')

                if delete_data_button:
                    db = Database
                    data = db.get_data()
                    ids = [i[0] for i in data]

                    if id_input in ids:
                        db.delete_data(id_input)
                        st.success('Row deleted!')
                    else:
                        st.error('Invalid ID')


                # Line separator
                st.write('---')
    
    def delete_table():
        with st.form(key='delete_table', clear_on_submit=True):
            with st.sidebar:
                st.header('Remove all data')
                confirm_input = st.text_input('Type "CONFIRM"')
                check_input = st.checkbox('I agree')
                delete_table_btn = st.form_submit_button('Remove')

                if delete_table_btn:
                    if (confirm_input == 'CONFIRM') & check_input:
                        try:
                            db = Database
                            db.delete_table()
                            st.write('Table deleted!')
                        except:
                            st.error('There is no table to be deleted')
                    else:
                        st.error('Inavlid Input') 


sidebar = Sidebar
sidebar.input_data()
sidebar.delete_data()
sidebar.delete_table()

class Content:
    def main_table():
        try:
            st.title(':book: Productivity Data')

            database = Database
            df = database.feature_engineering()
            df = df[['ID', 'Date', 'Study(hr)', 'Study(min)', 'Workout(min)', 'Description', 'Satisfaction']].reset_index(drop=True)
            st.write(df)

            st.text(f'Table dimension: {df.shape}')
            st.write('---')
        except:
            st.warning('There is no data to be displayed. Go input some data!')

    def line_charts():
        try:
            st.title(':bar_chart: Data Analysis')

            database = Database
            df = database.feature_engineering()

            # Filter year
            years = list(map(int, df.Year.unique()))
            year_input = st.selectbox('Year', years, index=0)
            
            # Filter month
            months_num = [i for i in range(1,13)]
            months_str = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            month_input = st.multiselect('Month', months_str, default=months_str)
            selected_months = [x for x,y in zip(months_num, months_str) if y in month_input]
        
            # Filtering Data
            filtered_df = df[(df.Year == year_input) & (df.Month.isin(selected_months))]
            filtered_df.reset_index(drop=True, inplace=True)
            filtered_df.sort_values('Date', inplace=True)

            # Visualization object
            vis = Visualization(filtered_df)

            # Line study
            fig = vis.line_study()
            st.plotly_chart(fig, use_container_width=True)

            # Line workout
            fig = vis.line_workout()
            st.plotly_chart(fig, use_container_width=True)

            # Line satisfaction
            fig = vis.line_satisfaction()
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('---')

        except:
            st.warning('There is no data to be displayed. Go input some data!')


    def bar_chart():
        try:
            # Bar chart
            database = Database
            df = database.feature_engineering()
            df['Study_total'] = df['Study(hr)'] + (df['Study(min)'] / 60)

            st.subheader('Average Analysis')

            col1, col2 = st.columns(2)
            with col1:
                year_input = st.selectbox('Select Year', df.Year.unique())
            with col2:
                y_input = st.selectbox('Select data', ['Study_total', 'Workout(min)', 'Satisfaction'])
            
            filtered_df = df[df.Year == year_input]
            vis = Visualization(filtered_df)
            fig = vis.bar_chart(y_input)
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass

content = Content
content.main_table()
content.line_charts()
content.bar_chart()