import plotly.express as px
from shiny import App, render, ui
from shiny.express import input, ui, render
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req
from faicons import icon_svg

ui.page_opts(title="Sarah's Penguin Databoard", fillable=True,)

with ui.sidebar(title="Palmer Penguins Dashboard", style="background-color: #7FFFD4;"):
    ui.input_select("var", "Select variable", choices=["bill_length_mm", "body_mass_g"])
    ui.input_switch("species", "Group by species", value=True)
    ui.input_switch("show_rug", "Show Rug", value=True)

    ui.hr()
    ui.a(
        "GitHub Source",
        href="https://github.com/sapapesh/cintel-06-custom",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/sapapesh/cintel-06-custom/blob/main/app.py",
    )

with ui.card(full_screen=True):
        "Comparison of Penguins by Bill Length or by Body Mass"
@render.plot
def hist():
    hue = "species" if input.species() else None
    sns.kdeplot(penguins_df, x=input.var(), hue=hue)
    if input.show_rug():
        sns.rugplot(penguins_df, x=input.var(), hue=hue, color="black", alpha=0.25)



#define a reactive calc to fake new data points and/or filter a data frame
#define the Shiny Express UI
#The overall page options
#A sidebar
#The main section with ui cards, value boxes, and space for grids and charts


#define a reactive calc to fake new data points and/or filter a data frame
#define the Shiny Express UI
#The overall page options
#A sidebar
#The main section with ui cards, value boxes, and space for grids and charts

