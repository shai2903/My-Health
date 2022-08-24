from __future__ import annotations
import tkinter as tk
import diets_tabs
from vitamin_data.vitamin_names import VitaminName
from consts import GREEN_PERCENTAGE,Meals



def reset_add_new_diet_frame(diet_tab: diets_tabs.DietsTab):
    """Reset all frames to default values after add new diet"""
    diet_tab.diet_name_entry.delete(0, 'end')
    reset_search_frame(diet_tab, False)
    reset_meals_frame(diet_tab)
    reset_vitamin_frame(diet_tab)


def reset_vitamin_frame(diet_tab: diets_tabs.DietsTab):
    """Reset the vitamin frame after add new diet"""
    color = GREEN_PERCENTAGE
    for vitamin in VitaminName.vitamin_name:
        getattr(diet_tab, vitamin+"_intake_label")['text'] = '0'
        getattr(diet_tab, vitamin+"_pbar")['value'] = 0
        getattr(diet_tab, vitamin+"pbar_label")['text'] = '0%'
        getattr(diet_tab, vitamin+"pbar_label").configure(foreground=color)


def reset_meals_frame(diet_tab: diets_tabs.DietsTab):
    """Reset the meal frame after we add new diet to empty values"""
    for enum_meal in Meals:
        meal=enum_meal.value
        getattr(diet_tab, "tableview_"+meal).delete_rows()
        setattr(diet_tab, meal+"_foods", None)


def reset_search_frame(diet_tab: diets_tabs.DietsTab, is_new_food: bool):
    """Reset search frame after we add new food
    if new food is added we don't delete the food_name_entry,
    otherwise we add new diet and we delete this entry as well
    Args:
        diet_tab - diets_tabs object from GUI
        is_new_food- true if we add_new_food in add_food
    """
    if not is_new_food:
        diet_tab.food_name_entry.delete(0, 'end')
    diet_tab.food_options_combobox.set('')
    diet_tab.serving_combobox.set('')
    diet_tab.amount_entry.delete(0, 'end')
    diet_tab.meal_combobox.set('')


def reset_frame(frame: tk.Frame):
    """Delete all widget from frame"""
    for widget in frame.winfo_children():
        widget.destroy()
