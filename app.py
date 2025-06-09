import numpy as np
import pandas as pd
import logging
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly

# Constants

diastatic_malt_percentage = 0.5

# User Interface

ui.panel_title("Dough Calculator"),
ui.input_slider("hydration_percentage", "Hydration", 50, 100, 70),
ui.input_slider("salt_percentage", "Salt", 0, 5, 2),
ui.input_slider("yeast_percentage", "Yeast", 0, 5, 2),
ui.input_slider("oil_percentage", "Oil", 0, 10, 0),
ui.input_slider("sugar_percentage", "Sugar", 0, 20, 0),
ui.input_numeric("starter", "Starter", 80, min=0, max=500)
ui.input_slider("wheat_percentage", "Whole Wheat", 0, 50, 0),
ui.input_checkbox("include_malt",f"Diastatic Malt ({diastatic_malt_percentage}%)", False),
"Dough Recipe:"
ui.input_numeric("flour", "Flour Target", 400, min=0, max=1000)


@render.data_frame  
def text():
    flour_target = input.flour()
    starter_total = input.starter()
    starter_hydration = 0.5
    starter_flour = starter_total*(1-starter_hydration)
    starter_water = starter_total*(starter_hydration)
    salt_fraction = input.salt_percentage()/100
    yeast_fraction = input.yeast_percentage()/100
    sugar_fraction = input.sugar_percentage()/100
    wheat_fraction = input.wheat_percentage()/100


    hydration = input.hydration_percentage()/100
    
    water_target = flour_target * hydration
    water_added = water_target - starter_water



    wheat_flour = flour_target*wheat_fraction
    base_flour = flour_target - starter_flour - wheat_flour

    diastatic_malt = diastatic_malt_percentage/100*flour_target if input.include_malt() else 0
    
    ingredients = {}
    ingredients['base flour'] = base_flour
    ingredients['wheat flour'] = wheat_flour
    ingredients["starter"] = starter_total
    ingredients["salt"] = flour_target * (salt_fraction)
    ingredients["sugar"] = flour_target * (sugar_fraction)
    ingredients["yeast"] = flour_target * (yeast_fraction)
    ingredients["water"] = water_added
    ingredients['diastatic malt'] = diastatic_malt
    ingredients_dataframe = pd.DataFrame(ingredients.items(), columns=['Ingredient', 'Amount (g)'])
    filtered_ingredients = ingredients_dataframe[ingredients_dataframe["Amount (g)"]!=0]
    return filtered_ingredients
    