

from __future__ import annotations
from USDA_handler import *
import reset_fields
import re
import diets_tabs


def add_food(diet_tab: diets_tabs.DietsTab, meal: str, food: str, serving: str, amount: str):
    """add chosen food to Meal object and to listbox
    Args:
        diet_tab - diets_tabs object from GUI
        meal - the meal the user choose
        food - the food the user choose to add to meal
        serving - the serving of food
        amount - the amount of serving from food
    """
    food_id = diet_tab.from_description_to_fcdif[food]
    current_food_nutrient = get_food_nutrient(str(food_id))

    num_of_foods = diet_tab.current_user.get_num_of_foods_from(meal)
    current_meal_listbox = getattr(diet_tab, "listbox_"+meal)
    current_meal_listbox.insert(
        num_of_foods, food+" | "+serving+" | amount: "+amount)

    vitamin_intake = calculate_consumption(diet_tab, current_food_nutrient,
                                           serving, amount, False)
    set_consumption_widgets(diet_tab, vitamin_intake)

    diet_tab.current_user.update_meal(
        meal, food_id, food, serving, amount, current_food_nutrient, vitamin_intake)

    reset_fields.reset_search_frame(diet_tab, True)


def calculate_consumption(diet_tab: diets_tabs.DietsTab, current_food_nutrient: dict, sreving: str, amount: str, is_delete: bool):
    """calculate the consumption of user after adding\deleting food """
    sreving_in_grams = float(re.findall("\(\d*\.\d*\s[g][gr]\)", sreving)[0].split(
        "(")[1].split(' ')[0])  # get serving in grams (example: 1 cup is x gram)
    ratio = sreving_in_grams/100
    vitamin_intake = diet_tab.current_user.get_current_diet_vitamins()

    # update all vitamin's progressbar , label and current_meal dict
    for vitamin, nutritional_value in current_food_nutrient.items():
        if not is_delete:
            vitamin_intake[vitamin] += (float(nutritional_value)
                                        * ratio)*float(amount)
        else:
            vitamin_intake[vitamin] -= (float(nutritional_value)
                                        * ratio)*float(amount)
    return vitamin_intake


def set_consumption_widgets(diet_tab: diets_tabs.DietsTab, consumption_dict):
    """set all widget with update consumption_dict values """
    # update all vitamin's progressbar , label and current_meal dict
    for vitamin, consumption_value in consumption_dict.items():

        optimal_quantity = diet_tab.current_user.get_number_from_recommended(
            vitamin)
        rounded_val = round(consumption_value, 2)

        getattr(diet_tab, vitamin+"_consumption_label").config(
            text=str(rounded_val)+" "+VitaminNameData.units[vitamin])

        color = "#42f5b6"
        if optimal_quantity:
            if (consumption_value > optimal_quantity):
                color = "#f55142"
            getattr(diet_tab, vitamin +
                    "_pbar").configure(value=consumption_value)
            getattr(diet_tab, vitamin+"_label_pbar")['text'] = str(
                round((float(consumption_value/optimal_quantity))*100, 2))+"%"
            getattr(diet_tab, vitamin+"_label_pbar").configure(foreground=color)
        else:
            getattr(diet_tab, vitamin+"_pbar").configure(value=0)
            getattr(diet_tab, vitamin+"_label_pbar")['text'] = "*"
