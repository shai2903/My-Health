from __future__ import annotations
import tkinter.ttk as ttk
import tkinter as tk
from ttkbootstrap.tableview import Tableview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import diets_tabs
import reset_fields
from vitamin_data.vitamin_names import VitaminName
import helper
import consts



def show_analysis_vitamin(diet_tab: diets_tabs.DietsTab, chosen_diet: str, vitamin: str):
    """Show the pie chart of the chosen vitamin.
    Args:
        diet_tab - diets_tabs object from GUI
        chosen_diet - the diet the user wanted to show
        vitamin - the vitamin the user choose
    """
    reset_fields.reset_frame(diet_tab.analysis_vitamin_pie_frame)
    reset_fields.reset_frame(diet_tab.analysis_vitamin_meal_frame)

    ttk.Label(diet_tab.analysis_vitamin_pie_frame, text=vitamin).grid(
        row=0, column=2, sticky='n')

    show_pie(diet_tab, chosen_diet, vitamin)


def show_pie(diet_tab: diets_tabs.DietsTab, chosen_diet: str, vitamin: str):
    """Calculate the intake of the vitamin for each meal"""
    chart_frame = tk.Frame(diet_tab.analysis_vitamin_pie_frame)
    chart_frame.grid(row=1, column=2)

    is_all_zero = True
    vitamin_values = []

    for enum_meal in consts.Meals:
        meal=enum_meal.value
        to_add = diet_tab.current_user.get_vitamin_value_from_meal(
            chosen_diet, meal, vitamin)
        if to_add:
            is_all_zero = False
        vitamin_values += [to_add]

    if not is_all_zero:
        build_pie(diet_tab, vitamin_values, chart_frame, vitamin, chosen_diet)
    else:  # no intake of this vitamin
        ttk.Label(chart_frame, text="No intake at all").grid(
            row=2, column=2, pady=10, padx=30, sticky='ns')


def build_pie(diet_tab: diets_tabs.DietsTab, vitamin_values: list, chart_frame: tk.Frame, vitamin: str, chosen_diet: str):
    """Build the pie of vitamin
    Args:
        diet_tab - diets_tabs object from GUI
        vitamin_values - the value of vitamin intake in each meal
        chart_frame - the pie's frame
        chosen_diet - the diet the user wanted to show
        vitamin - the vitamin the user choose
    """
    colors = [consts.GREEN_PIE, consts.BLUE_PIE, consts.ORANGE_PIE, consts.RED_PIE]
    pie_figure = Figure()
    pie_figure.patch.set_facecolor(consts.DARK_BLUE_STYLE)

    ax_pie_figure = pie_figure.add_subplot(111)
    ax_pie_figure.pie(vitamin_values, autopct='%1.1f%%', colors=colors)
    ax_pie_figure.legend(labels=consts.Meals.list(),
               title="Meals",
               loc="center left",
               bbox_to_anchor=(0.85, 0.5))              
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax_pie_figure.axis('equal')

    chart = FigureCanvasTkAgg(pie_figure, chart_frame)
    chart.get_tk_widget().grid()

    meals_legend_frame = ttk.Frame(chart_frame)
    meals_legend_frame.grid(row=3, padx=10, column=0, sticky='we')

    breakfast_text_button=consts.Meals.BREAKFAST
    lunch_text_button=consts.Meals.LUNCH
    dinner_text_button=consts.Meals.DINNER
    snacks_text_button=consts.Meals.SNACKS

    ttk.Button(meals_legend_frame, text=breakfast_text_button.capitalize(), bootstyle="success", command=lambda: show_meal_analysis_frame(
        breakfast_text_button, vitamin, chosen_diet, diet_tab)).grid(row=3, column=0, padx=20, pady=10)
    ttk.Button(meals_legend_frame, text=lunch_text_button.capitalize(), bootstyle="info", command=lambda: show_meal_analysis_frame(
        lunch_text_button, vitamin, chosen_diet, diet_tab)).grid(row=3, column=1, padx=20, pady=10)
    ttk.Button(meals_legend_frame, text=dinner_text_button.capitalize(), bootstyle="warning", command=lambda: show_meal_analysis_frame(
        dinner_text_button, vitamin, chosen_diet, diet_tab)).grid(row=3, column=2, padx=20, pady=10)
    ttk.Button(meals_legend_frame, text=snacks_text_button.capitalize(), bootstyle="danger", command=lambda: show_meal_analysis_frame(
        snacks_text_button, vitamin, chosen_diet, diet_tab)).grid(row=3, column=3, padx=20, pady=10,)


def show_meal_analysis_frame(meal: str, vitamin: str, chosen_diet: str, diet_tab: diets_tabs.DietsTab):
    """Build data-table of all foods in meal"""
    reset_fields.reset_frame(diet_tab.analysis_vitamin_meal_frame)

    meal_analysis_frame = ttk.LabelFrame(diet_tab.analysis_vitamin_meal_frame)
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
        consumption_food_str = f'{str(round(consumption_food, 2))} {VitaminName.units[vitamin]}'
        consumption_total_user = diet_tab.current_user.user.get_diet(
            chosen_diet).get_vitamins()[vitamin]
        proportional_str = f'{str(round((float(consumption_food/consumption_total_user))*100, 2))} %'

        meal_tableview.insert_row('end', [
                                  food.get_name(), food.get_amount(), food.get_serving(), consumption_food_str, proportional_str])
    meal_tableview.load_table_data()
    meal_tableview.grid()
