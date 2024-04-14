from shiny import App, render, ui, reactive, req
from shiny.express import input, ui, render
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()
import pandas as pd
import seaborn as sns
from faicons import icon_svg

ui.page_opts(title="Sarah's Penguin Databoard", fillable=True,)

with ui.sidebar(title="Palmer Penguins Dashboard", style="background-color: #7FFFD4;"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    ui.hr()
    ui.a(
        "GitHub Source",
        href="https://github.com/sapapesh/cintel-06-custom",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/sapapesh/cintel-06-custom/blob/main/app.py",
    )

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)



@reactive.calc
def filtered_df():
    filt_df = penguins_df[penguins_df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df

#define a reactive calc to fake new data points and/or filter a data frame
#define the Shiny Express UI
#The overall page options
#A sidebar
#The main section with ui cards, value boxes, and space for grids and charts
