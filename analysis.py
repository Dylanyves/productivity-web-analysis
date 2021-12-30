import plotly.express as px
from streamlit.elements.arrow import Data
from data import Database

class Visualization:
    def __init__ (self, df):
        self.df = df

    def check(self):
        return self.df

    def line_study(self):
        mod_df = self.df.copy()
        mod_df['Study_total'] = mod_df['Study(hr)'] + (mod_df['Study(min)'] / 60)
        fig = px.line(mod_df, x='Day', y='Study_total', markers=True, color='Month', title='Study Chart', 
            labels={
                'Study_total':'Study (Hour)',
                'index':'Day'
            }
        )
        fig.update_layout(
            font_color='blue'
        )
        return fig

    def line_workout(self):
        fig = px.line(self.df, x='Day', y='Workout(min)', markers=True, color='Month', title='Workout Chart', 
            labels={
                'Workout(min)': 'Workout (Minute)',
                'index':'Day'
            }
        )
        fig.update_layout(
            font_color='blue'
        )
        return fig

    def line_satisfaction(self):
        fig = px.line(self.df, x='Day', y='Satisfaction', markers=True, color='Month', title='Satisfaction Chart',
            labels={
                'Satisfaction':'Satisfaction (0-10)',
                'index':'Day'
            }
        )
        fig.update_layout(
            font_color='blue'
        )
        return fig

    def bar_chart(self, y):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_dict = {int(i):month for month, i in zip(months, range(1,13))}
        avg = self.df.groupby('Month')[y].mean()
        y_axes = list()
        for key in month_dict.keys():
            if key in avg.index.tolist():
                y_axes.append(avg[key])
            else:
                y_axes.append(0)
        fig = px.bar(x=months, y=y_axes, labels={'y':y+' (Average)'})
        fig.update_layout(
            font_color='blue'
        )
        return fig