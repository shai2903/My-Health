from __future__ import annotations
import tkinter.ttk as ttk
import tkinter as tk
from ttkbootstrap.tableview import Tableview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import diets_tabs
import reset_fields
from vitamin_data import VitaminNameData
import helper



lst_of_meals = ["breakfast", "lunch", "dinner", "snacks"]


def show_analysis_vitamin(diet_tab: diets_tabs.DietsTab, chosen_diet: str, vitamin: str):
    """ show the pei chart of the chosen vitamin.
    Args:
        diet_tab - diets_tabs object from GUI
        chosen_diet - the diet the user wanted to show
        vitamin - the vitamin the user choose
    """
    reset_fields.reset_frame(diet_tab.analysis_vitamin_pei_frame)
    reset_fields.reset_frame(diet_tab.analysis_vitamin_meal_frame)

    ttk.Label(diet_tab.analysis_vitamin_pei_frame, text=vitamin).grid(
        row=0, column=2, sticky='n')

    show_pei(diet_tab, chosen_diet, vitamin)


def show_pei(diet_tab: diets_tabs.DietsTab, chosen_diet: str, vitamin: str):
    """calculate the intake of the vitamin for each meal"""
    chart_frame = tk.Frame(diet_tab.analysis_vitamin_pei_frame)
    chart_frame.grid(row=1, column=2)

    is_all_zero = True
    vitamin_values = []

    for meal in lst_of_meals:

        to_add = diet_tab.current_user.get_vitamin_value_from_meal(
            chosen_diet, meal, vitamin)
        if to_add:
            is_all_zero = False
        vitamin_values += [to_add]

    if not is_all_zero:
        build_pei(diet_tab, vitamin_values, chart_frame, vitamin, chosen_diet)
    else:  # no intake of this vitamin
        ttk.Label(chart_frame, text="No intake at all").grid(
            row=2, column=2, pady=10, padx=30, sticky='ns')


def build_pei(diet_tab: diets_tabs.DietsTab, vitamin_values: list, chart_frame: tk.Frame, vitamin: str, chosen_diet: str):
    """build the pei of vitamin
    Args:
        diet_tab - diets_tabs object from GUI
        vitamin_values - the value of vitamin intake in each meal
        chart_frame - the pei's frame
        chosen_diet - the diet the user wanted to show
        vitamin - the vitamin the user choose
    """
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
    chart1 = FigureCanvasTkAgg(fig1, chart_frame)
    chart1.get_tk_widget().grid()

    meals_legend_frame = ttk.Frame(chart_frame)
    meals_legend_frame.grid(row=3, padx=10, column=0, sticky='we')

    ttk.Button(meals_legend_frame, text="breakfast", bootstyle="success", command=lambda: show_meal_analysis_frame(
        "breakfast", vitamin, chosen_diet, diet_tab)).grid(row=3, column=0, padx=20, pady=10)
    ttk.Button(meals_legend_frame, text="lunch", bootstyle="info", command=lambda: show_meal_analysis_frame(
        "lunch", vitamin, chosen_diet, diet_tab)).grid(row=3, column=1, padx=20, pady=10)
    ttk.Button(meals_legend_frame, text="dinner", bootstyle="warning", command=lambda: show_meal_analysis_frame(
        "dinner", vitamin, chosen_diet, diet_tab)).grid(row=3, column=2, padx=20, pady=10)
    ttk.Button(meals_legend_frame, text="snacks", bootstyle="danger", command=lambda: show_meal_analysis_frame(
        "snacks", vitamin, chosen_diet, diet_tab)).grid(row=3, column=3, padx=20, pady=10,)


def show_meal_analysis_frame(meal: str, vitamin: str, chosen_diet: str, diet_tab: diets_tabs.DietsTab):
    """build data-table of all foods in meal"""
    reset_fields.reset_frame(diet_tab.analysis_vitamin_meal_frame)

    meal_analysis_frame = ttk.LabelFrame(diet_tab.analysis_vitamin_meal_frame, width=400)
    meal_analysis_frame.grid(column=4, row=0)

    ttk.Label(meal_analysis_frame, text=meal).grid(sticky="ew")

    food_list = diet_tab.current_user.get_foods_from_meal_diet(
        chosen_diet, meal)

    coldata = [
        {"text": "Name", "width": 300},
        {"text": "Amount", "width": 70},
        {"text": "Serving", "width": 200},
        {"text": "Intake", "width": 100},
        {"text": "%", "width": 60}
    ]

    meal_tableview = Tableview(
        master=meal_analysis_frame,
        coldata=coldata,
        paginated=True,
        searchable=True
    )

    for food in food_list:

        ratio = helper.get_ratio(food.serving)
        consumption_food = (
            float(food.vitamins[vitamin]) * ratio)*float(food.amount)
        consumption_food_str = str(
            round(consumption_food, 2)) + " "+VitaminNameData.units[vitamin]
        consumption_total_user = diet_tab.current_user.user.get_diet(
            chosen_diet).get_vitamins()[vitamin]
        proportional_str = str(
            round((float(consumption_food/consumption_total_user))*100, 2))+" %"

        meal_tableview.insert_row('end', [
                                  food.get_name(), food.get_amount(), food.get_serving(), consumption_food_str, proportional_str])
    meal_tableview.load_table_data()
    meal_tableview.grid()
