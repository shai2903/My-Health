from __future__ import annotations
import handler_USDA 
import reset_fields
import helper
import diets_tabs
from consts import GREEN_PERCENTAGE,RED_PERCENTAGE
from errors import USDAConnectionError
from tkinter import messagebox
from vitamin_data.vitamin_names import VitaminName


def add_food(diet_tab: diets_tabs.DietsTab):
    """Add chosen food to Meal object and to tableview
    Args:
        diet_tab - diets_tabs object from GUI
    """
    meal=diet_tab.meal_combobox.get() # the meal the user choose
    food=diet_tab.food_options_combobox.get() #the food the user choose to add to meal
    serving=diet_tab.serving_combobox.get() #the serving of food
    amount=diet_tab.amount_entry.get() # the amount of serving from food
    food_id = diet_tab.from_description_to_fcdif[food]
    
    try:
        current_food_nutrient = handler_USDA.get_food_nutrient(str(food_id))
    except USDAConnectionError:
        messagebox.showerror("showerror", "USDA bad connection")
        return

    current_meal_tableview = getattr(diet_tab, "tableview_"+meal)
    current_meal_tableview.insert_row(
        'end', [food, serving, amount])
    current_meal_tableview.load_table_data()

    vitamin_intake = calculate_intake(diet_tab, current_food_nutrient,
                                           serving, amount, False)
    set_intake_widgets(diet_tab, vitamin_intake)

    diet_tab.current_user.update_meal(
        meal, food_id, food, serving, amount, current_food_nutrient)

    reset_fields.reset_search_frame(diet_tab, True)


def calculate_intake(diet_tab: diets_tabs.DietsTab, current_food_nutrient: dict, sreving: str, amount: str, is_delete: bool) -> dict:
    """Calculate the intake of user after adding\deleting food """
    ratio = helper.get_ratio(sreving)
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


def set_intake_widgets(diet_tab: diets_tabs.DietsTab, intake_dict: dict):
    """Set all widget with update intake_dict values """
    # update all vitamin's progressbar , label and current_meal dict
    for vitamin, intake_value in intake_dict.items():

        optimal_quantity = diet_tab.current_user.get_number_from_recommended(
            vitamin)
        rounded_val = round(intake_value, 2)

        getattr(diet_tab, vitamin+"_intake_label").config(
            text=str(rounded_val)+" "+VitaminName.units[vitamin])

        color = GREEN_PERCENTAGE
        if optimal_quantity:
            if intake_value > optimal_quantity:
                color = RED_PERCENTAGE
            getattr(diet_tab, vitamin +
                    "_pbar").configure(value=intake_value)
            getattr(diet_tab, vitamin+"pbar_label")['text'] = str(
                round((float(intake_value/optimal_quantity))*100, 2))+"%"
            getattr(diet_tab, vitamin+"pbar_label").configure(foreground=color)
        else:
            getattr(diet_tab, vitamin+"_pbar").configure(value=0)
            getattr(diet_tab, vitamin+"pbar_label")['text'] = "*"
