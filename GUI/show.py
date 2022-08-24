from __future__ import annotations
import handler_USDA
import diets_tabs
from tkinter import messagebox
from errors import USDAConnectionError

def show_serving(diet_tab: diets_tabs.DietsTab):
    """Show all the serving option after food search
    Args:
        diet_tab - diets_tabs object from GUI
    """
    # get the of the chosen food
    food=diet_tab.food_options_combobox.get() #the food we search
    serving_combobox=diet_tab.serving_combobox
    food_id = diet_tab.from_description_to_fcdif[food]
    try:
        optional_serving_list: list = handler_USDA.get_serving_option(str(food_id))
    except USDAConnectionError:
        messagebox.showerror("showerror", "USDA bad connection")
        return

    values_to_add = tuple(optional_serving_list)
    serving_combobox['values'] = values_to_add


def show_food_options(diet_tab: diets_tabs.DietsTab):
    """Show in combobox all the food option from the food search
    Args:
        diet_tab - diets_tabs object from GUI
    """
    food=diet_tab.food_name_entry.get() #the food we want to search
    food_options_combobox=diet_tab.food_options_combobox

    all_food_options = get_list_of_foods_options(diet_tab, food)

    # add the description of each food to combobox
    values_to_add = tuple(all_food_options)
    food_options_combobox['values'] = values_to_add


def get_list_of_foods_options(diet_tab: diets_tabs.DietsTab, food: str) -> list:
    """Return all the food option from the USDA search of food
    Args:
        diet_tab - diets_tabs object from GUI
        food - the food we want to search
    return : list of food's description (string)
    """
    foods_from_USDA = handler_USDA.get_all_options_USDA(food)

    list_of_description = []
    diet_tab.from_description_to_fcdif = {}
    for item in foods_from_USDA:
        diet_tab.from_description_to_fcdif[item['description']] = item['fdcId']
        list_of_description.append(item['description'])

    return list_of_description
