
from __future__ import annotations
from USDA_handler import *
import tkinter.ttk as ttk
import diets_tabs


def show_serving(diet_tab: diets_tabs.DietsTab, food: str, combobox_serving: ttk.Combobox):
    """show all the serving option after food search 
    Args:
        diet_tab - diets_tabs object from GUI
        food - the food we search
        combobox_serving - the combobox we want to add the option to 
    """
    # get the of the chosen food
    food_id = diet_tab.from_description_to_fcdif[food]
    optional_serving_list: list = get_serving_option(str(food_id))

    values_to_add = tuple(optional_serving_list)
    combobox_serving['values'] = values_to_add


def show_food_options(diet_tab: diets_tabs.DietsTab, food: str, combobox_food_options: ttk.Combobox):
    """ show in combobox all the food option from the food search
    Args:
        diet_tab - diets_tabs object from GUI
        food - the foos we want to search
        combobox_serving - the combobox we want to add the option to 
    """
    all_food_options = get_list_of_foods_options(diet_tab, food)

    # add the description of each food to combobox
    values_to_add = tuple(all_food_options)
    combobox_food_options['values'] = values_to_add


def get_list_of_foods_options(diet_tab: diets_tabs.DietsTab, food: str) -> list:
    """ return all the food option from the USDA search of food
    Args:
        diet_tab - diets_tabs object from GUI
        food - the food we want to search
    return : list of food's description (string)
    """
    foods_from_USDA = get_all_options_USDA(food)

    lst_of_description = []
    diet_tab.from_description_to_fcdif = {}
    for item in foods_from_USDA:
        diet_tab.from_description_to_fcdif[item['description']] = item['fdcId']
        lst_of_description.append(item['description'])

    return lst_of_description
