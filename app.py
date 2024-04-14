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
print(df[['age', 'sex', 'bmi', 'bp', 's2', 's3', 's4', 's5', 's6', 'target']].head())

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

with ui.sidebar(open="open", style="font-family: 'Comic Sans MS'"):
    ui.h2("Diabetes Contributing Factors", class_="text-center")
    icon_svg("bomb")
    ui.p(
        "A demonstration of how various factors impact diabetes.",
        class_="text-center",
    )

    ui.hr()

    ui.input_checkbox_group(  
    "checkbox_group",  
        "Checkbox group",  
        {  
        "age":"Age",  
        "sex": "Sex",  
        "bmi": "Body Mass Index",
        "s2": "LDL",
        "s3": "HDL",
        "s4": "Total Cholesterol",
        "s6": "Blood Glucose Level"},)

    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://https://https://github.com/sapapesh/cintel-06-custom",
        target="_blank",
    )

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("arrow-right"),
        style="background-color: gray; font-family: 'Comic Sans MS'",
    ):
        "A1C"
        
        @render.text
        def display_A1C():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['A1C']}"

        "Time Stamp"
        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

with ui.card(full_screen=True):
    ui.card_header("Current Readings", style="background-color: yellow; color: black",)

    @render.data_frame
    def display_df():
        """Get the latest reading and return a dataframe with current readings"""
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        pd.set_option('display.width', None)        # Use maximum width
        return render.DataGrid( df,width="100%")

ui.hr()

with ui.layout_columns(col_widths=(4, 8)):
    with ui.card(full_screen=True):
        "Diabetes Stats"

    @render.data_frame
    def diabetes_datatable():
        return render.DataTable(filtered_data())

with ui.card():
    ui.card_header("Chart with Current Trend", style="background-color: lightgray; width: 100%,")

    @render_plotly
    def display_plot():
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        if not df.empty:
           df["target"] = pd.to_datetime(df["target"]) 
        
        fig = px.scatter(df,
            x="sex",
            y="smoker",
            title="Factors of sex and smoking",
            labels={"sex": "Sex", "smoker": "Smoker"},
            color_discrete_sequence=["blue"] )

        sequence = range(len(df))
        x_vals = list(sequence)
        y_vals = df["target"]

        slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
        df['best_fit_line'] = [slope * x + intercept for x in x_vals]

        fig.add_scatter(x=df["target"], y=df['best_fit_line'], mode='lines', name='Regression Line')
        fig.update_layout(xaxis_title="Sex",yaxis_title="Smoker", yaxis_range=[])
        fig.update_layout(font_color="black")
        return fig

@reactive.calc
def filtered_data():
    return diabetes.data[diabetes.data["sex"].isin(input_checkbox_group())]
    
with ui.layout_columns(col_widths=(4, 8)):
    with ui.card(full_screen=True): "Plotly Scatterplot"

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(filtered_data(),
            x="sex",
            y="bmi",
            color="blood glucose",
            title="Diabetes Factors",
            labels={
                "sex": "Sex",
                "bmi": "Body Mass Index",
            },
            size_max=8, 
        )

@render_plotly
def plot1():
        return px.histogram(px.data.tips(), y="sex")

@render_plotly
    
def plot2():
        return px.histogram(px.data.tips(), y="smoker")

#define a reactive calc to fake new data points and/or filter a data frame
#define the Shiny Express UI
#The overall page options
#A sidebar
#The main section with ui cards, value boxes, and space for grids and charts

