import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from faicons import icon_svg
from scipy import stats
from shiny import reactive, render

import random
from datetime import datetime
from collections import deque

#import the dataset and pands
from sklearn import datasets
import pandas as pd

#Load the diabetes dataset and create a dataframe
diabetes = datasets.load_diabetes()
df = pd.DataFrame(diabetes.data,columns=diabetes.feature_names)

#Add the target variable to the dataframe
df['target'] = diabetes.target

#Print the first 5 rows of some variables
print(df[['age', 'sex', 'bmi','target']].head())

#Correlation Analysis of dataset
corr = df[['age', 'sex', 'bmi', 'target']].corr()
print(corr)

#Create A1C readings
UPDATE_INTERVAL_SECS: int = 60

DEQUE_SIZE: int = 1
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    A1C = round(random.uniform(4, 15), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"A1C": A1C, "timestamp": timestamp}
    reactive_value_wrapper.get().append(new_dictionary_entry)
    deque_snapshot = reactive_value_wrapper.get()
    df = pd.DataFrame(deque_snapshot)
    latest_dictionary_entry = new_dictionary_entry
    return deque_snapshot, df, latest_dictionary_entry

ui.page_opts(title="Diabetes Awareness Statistics", fillable=True)


with ui.layout_columns():

    @render_plotly
    def plot1():
        return px.histogram(px.data.tips(), y="tip")

    @render_plotly
    
    def plot2():
        return px.histogram(px.data.tips(), y="total_bill")

#define a reactive calc to fake new data points and/or filter a data frame
#define the Shiny Express UI
#The overall page options
#A sidebar
#The main section with ui cards, value boxes, and space for grids and charts
