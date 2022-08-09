

from __future__ import annotations
import tkinter.ttk as ttk
import tkinter as tk
from vitamin_data import VitaminNameData
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import diets_tabs
import reset_fields
import re

lst_of_meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]


def show_analysis_vitamin(diet_tab: diets_tabs.DietsTab, chosen_diet: str, vitamin: str):
    """ show the analysis pei chart of the chosen vitamin.
    Args:
        diet_tab - diets_tabs object from GUI
        chosen_diet - the diet the user wanted to show
        vitamin - the vitamin the user choose
    """
    reset_fields.reset_frame(diet_tab.analysis_vitamin_pei)
    reset_fields.reset_frame(diet_tab.analysis_vitamin_meal)

    ttk.Label(diet_tab.analysis_vitamin_pei, text=vitamin).grid(
        row=0, column=2, sticky='n')

    show_pei(diet_tab, chosen_diet, vitamin)


def show_pei(diet_tab: diets_tabs.DietsTab, chosen_diet: str, vitamin: str):
    """create and show the pei of the chosen vitamin from chosen_diet"""
    frame_chart = tk.Frame(diet_tab.analysis_vitamin_pei)
    frame_chart.grid(row=1, column=2)

    is_all_zero = True
    vitamin_values = []

    for meal in lst_of_meals:

        to_add = diet_tab.current_user.get_vitamin_value(
            chosen_diet, meal, vitamin)
        if to_add:
            is_all_zero = False
        vitamin_values += [to_add]

    if not is_all_zero:
        build_pei(diet_tab, vitamin_values, frame_chart, vitamin, chosen_diet)
    else:
        ttk.Label(frame_chart, text="No intake at all").grid(
            row=2, column=2, pady=10, padx=30, sticky='ns')


def build_pei(diet_tab: diets_tabs.DietsTab, vitamin_values: list, frame_chart: tk.Frame, vitamin: str, chosen_diet: str):
    """build the pei of vitamin"""
    fig1 = Figure()
    fig1.patch.set_facecolor('#2B3E50')
    ax1 = fig1.add_subplot(111)
    colors = ['#5cb85c', '#5bc0de', '#f0ad4e', '#d9534f']
    ax1.pie(vitamin_values, autopct='%1.1f%%', colors=colors)
    ax1.legend(labels=lst_of_meals,
               title="Meals",
               loc="center left",
               bbox_to_anchor=(0.85, 0.5))
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    chart1 = FigureCanvasTkAgg(fig1, frame_chart)
    chart1.get_tk_widget().grid()

    meals_frame_legend = ttk.Frame(frame_chart)
    meals_frame_legend.grid(row=3, padx=10, column=0, sticky='we')

    ttk.Button(meals_frame_legend, text="Breakfast", bootstyle="success", command=lambda: show_meal_analysis(
        "Breakfast", vitamin, chosen_diet, diet_tab)).grid(row=3, column=0, padx=20, pady=10)
    ttk.Button(meals_frame_legend, text="Lunch", bootstyle="info", command=lambda: show_meal_analysis(
        "Lunch", vitamin, chosen_diet, diet_tab)).grid(row=3, column=1, padx=20, pady=10)
    ttk.Button(meals_frame_legend, text="Dinner", bootstyle="warning", command=lambda: show_meal_analysis(
        "Dinner", vitamin, chosen_diet, diet_tab)).grid(row=3, column=2, padx=20, pady=10)
    ttk.Button(meals_frame_legend, text="Snacks", bootstyle="danger", command=lambda: show_meal_analysis(
        "Snacks", vitamin, chosen_diet, diet_tab)).grid(row=3, column=3, padx=20, pady=10,)


def show_meal_analysis(meal: str, vitamin: str, chosen_diet: str, diet_tab: diets_tabs.DietsTab):
    """build datatable of all foods in meal"""
    reset_fields.reset_frame(diet_tab.analysis_vitamin_meal)

    meal_analysis = ttk.LabelFrame(diet_tab.analysis_vitamin_meal, width=400)
    meal_analysis.grid(column=4, row=0)

    ttk.Label(meal_analysis, text=meal).grid(sticky="ew")

    food_lst = diet_tab.current_user.user.get_foods_from_meal_diet(
        chosen_diet, meal)

    coldata = [
        {"text": "Name", "width": 300},
        {"text": "Amount", "width": 70},
        {"text": "Serving", "width": 200},
        {"text": "Intake", "width": 100},
        {"text": "%", "width": 60}
    ]

    meal_datatable = Tableview(
        master=meal_analysis,
        coldata=coldata,
        paginated=True,
        searchable=True
    )

    for food in food_lst:
        sreving_in_grams = float(re.findall("\(\d*\.\d*\s[g][gr]\)", food.serving)[0].split(
            "(")[1].split(' ')[0])  # get serving in grams (example: 1 cup is x gram)
        ratio = sreving_in_grams/100
        consumption_food = (
            float(food.vitamins[vitamin]) * ratio)*float(food.amount)
        consumption_food_str = str(
            round(consumption_food, 2)) + " "+VitaminNameData.units[vitamin]
        consumption_user = diet_tab.current_user.user.get_diet(
            chosen_diet).get_vitamins()[vitamin]
        proportional_str = str(
            round((float(consumption_food/consumption_user))*100, 2))+"%"

        meal_datatable.insert_row('end', [
                                  food.name, food.amount, food.serving, consumption_food_str, proportional_str])

    meal_datatable.grid()
