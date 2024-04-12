import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly

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


ui.page_opts(title="Filling layout", fillable=True)
with ui.layout_columns():

    @render_plotly
    def plot1():
        return px.histogram(px.data.tips(), y="tip")

    @render_plotly
    def plot2():
        return px.histogram(px.data.tips(), y="total_bill")
