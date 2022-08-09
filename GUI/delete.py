from __future__ import annotations
import tkinter as tk
import update
import diets_tabs
from meal import Meal
from food import Food


def delete_item_from_list_box(diet_tab: diets_tabs.DietsTab, item_lunch: str, item_breakfast: str, item_snacks: str, item_dinner: str):
    """delete item from meal, choose the right meal to delete from (delete only from one)
    Args:
        diet_tab - the diet tab object of GUI
        item_lunch - the item we want to delete from lunch
        item_breakfast - the item we want to delete from breakfast
        item_snacks - the item we want to delete from snacks
        item_dinner - the item we want to delete from dinner
        chosen_diet - the diet the user choose in edit mode
    """
    print(item_lunch)
    # for meal in lst_of_meals:
    if item_lunch:
        delete_from_meal(diet_tab, item_lunch, "Lunch")
        return
    if item_breakfast:
        delete_from_meal(diet_tab, item_breakfast, "Breakfast")
        return
    if item_snacks:
        delete_from_meal(diet_tab, item_snacks, "Snacks")
        return
    if item_dinner:
        delete_from_meal(diet_tab, item_dinner, "Dinner")
        return


def delete_from_meal(diet_tab: diets_tabs.DietsTab, item_to_del: str, meal: str):
    """delete an item from specific tableview and the user meal object
    Args:
        diet_tab -the diet tab object of GUI
        item_to_del - the chosen food to delete
        meal - the meal we wand to delete from
    """
    # delete from tableview
    meal_tableview = getattr(diet_tab, "tableview_"+meal)
    food_name= meal_tableview.iidmap.get(item_to_del[0]).values[0]
    meal_tableview.delete_row(iid=item_to_del[0])
    meal_tableview.load_table_data()

    # delete from user object
    meal_obj: Meal = diet_tab.current_user.current_diet.get_meal(meal)
    food_obj: Food = meal_obj.delete_food(food_name)

    # update vitamin frame
    vitamin_intake = update.calculate_consumption(diet_tab, food_obj.vitamins,
                                                  food_obj.serving, food_obj.amount, True)
    update.set_consumption_widgets(diet_tab, vitamin_intake)


def delete_diet(diet_tab: diets_tabs.DietsTab):
    """delete diet name from all diets listbox, collection and local user"""
    diet_name = diet_tab.all_diets_listbox.get(tk.ANCHOR)
    diet_tab.current_user.delete_diet(diet_name)

    idx = diet_tab.all_diets_listbox.get(0, tk.END).index(diet_name)
    diet_tab.all_diets_listbox.delete(idx)
