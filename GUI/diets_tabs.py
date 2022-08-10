import tkinter.ttk as ttk
from tkinter import ANCHOR, END
import tkinter as tk
import ttkbootstrap
from ttkbootstrap.tableview import Tableview
from current_user import CurrentUser
from vitamin_data import VitaminNameData
from USDA_handler import *
import add_diet
import reset_fields
import show
import delete
import update
import analysis_chart
from diet import Diet

lst_of_meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]


class DietsTab():
    def __init__(self, current_user: CurrentUser):
        self.current_user = current_user

    def create_new_diet_tab(self, new_diet_frame: ttk.Frame):
        """create the new diet tab
        Args:
            new_diet_frame - the parent frame of all the tabs"""

        self.create_search_frame(new_diet_frame, False, "")
        self.create_meals_frame(new_diet_frame, False, "")
        self.create_vitamin_frame(new_diet_frame, False)

    def create_vitamin_frame(self, new_diet_frame: ttk.Frame, is_edit: bool, chosen_diet: str = ""):
        """create the parent frame of all the vitamin related data (i.e: optimal value and user consumption)
        Args:
            new_diet_frame - the frame of the Add_new_edit tab
            is_edit - true if in edit mode
            chosen_diet - the diet the user choose in edit mode
        """
        vitamin_frame = ttk.LabelFrame(new_diet_frame, width=930, height=900)
        vitamin_frame.grid(row=0, column=4)
        vitamin_frame.grid_propagate(False)

        self.create_vitamin_consumption_frame(
            vitamin_frame, is_edit, chosen_diet)
        self.create_percentage_frame(vitamin_frame, is_edit, chosen_diet)
        self.create_optimal_frame(vitamin_frame)

    def create_vitamin_consumption_frame(self, vitamin_frame: ttk.LabelFrame, is_edit: bool, chosen_diet: str):
        """create the user consumption vitamin frame(i.e how much vitamin he consume from the food in is diet)
        Args:
            vitamin_frame - parent of the consumption frame
            is_edit - true if in edit mode, in edit mode we set the value accordingly to the chosen_diet foods
            chosen_diet - the diet the user choose in edit mode
        """
        consumption_frame = ttk.Frame(vitamin_frame, width=150, height=200)
        consumption_frame.grid(row=0, column=4)
        ttk.Label(consumption_frame, text="Your consumption").grid(
            row=0, column=4, pady=5)

        for vitamin_count in range(len(VitaminNameData.vitamin_name)):
            self.create_consumption_label(
                VitaminNameData.vitamin_name[vitamin_count], vitamin_count+1, consumption_frame, is_edit, chosen_diet)

    def create_meals_frame(self, new_diet_frame: ttk.Frame, is_edit: bool, chosen_diet: str):
        """create the meals frame (i.e the tableview with the chosen food for each meal)
        Args:
            new_diet_frame - the frame of the Add_new_edit tab
            is_edit - true if in edit mode
            chosen_diet - the diet the user choose in edit mode
        """
        meals_frame = ttk.LabelFrame(new_diet_frame, width=450, height=920)
        meals_frame.grid(row=0, column=3, sticky="nw", pady=10, padx=10)
        meals_frame.grid_propagate(False)

        for i in range(len(lst_of_meals)):
            self.create_meal_tableview(
                lst_of_meals[i], i, meals_frame, is_edit, chosen_diet)

        del_button = ttk.Button(meals_frame, text="Delete", command=lambda: delete.delete_item_from_list_box(self, self.tableview_Lunch.view.selection(
        ), self.tableview_Breakfast.view.selection(), self.tableview_Snacks.view.selection(), self.tableview_Dinner.view.selection()))
        del_button.grid(row=4, column=2, sticky='n')

    def create_search_frame(self, new_diet_frame: ttk.Frame, is_edit: bool, chosen_diet: str):
        """ create the search frame from add_new_diet tab
        if in edit mode replace the "add new diet" button to "Done" button
        Args:
            new_diet_frame - the parent frame 
            is_edit - true if in edit mode
            chosen_diet - the diet the user choose in edit mode
        """
        search_frame = ttk.LabelFrame(new_diet_frame, width=450, height=900)
        search_frame.grid(row=0, column=0, pady=10,
                          sticky='n', ipadx=10, padx=10)

        ttk.Label(search_frame, text="Add new food").grid(
            row=1, column=0, pady=10)
        ttk.Label(search_frame, text="Food name :").grid(
            row=2, column=0, pady=5)
        self.food_name_entry = ttk.Entry(search_frame, width=40)
        self.food_name_entry.grid(row=2, column=1, sticky='w')

        self.food_options_combobox = ttk.Combobox(search_frame, width=50)
        self.food_options_combobox.grid(row=3, column=1, pady=5)
        ttk.Button(search_frame, text="Search", command=lambda: show.show_food_options(self,
                                                                                       self.food_name_entry.get(), self.food_options_combobox)).grid(row=2, column=1, pady=5, sticky='e')

        ttk.Label(search_frame, text="Serving").grid(row=5, column=0, pady=5)
        self.serving_combobox = ttk.Combobox(search_frame, width=50)
        self.serving_combobox.grid(row=5, column=1, pady=5)

        ttk.Label(search_frame, text="Amount").grid(row=7, column=0, pady=5)
        self.amount_entry = ttk.Entry(search_frame, width=12)
        self.amount_entry.grid(row=7, column=1)

        ttk.Label(search_frame, text="Meal").grid(row=8, column=0, pady=5)
        meal = tk.StringVar()
        self.meal_combobox = ttk.Combobox(
            search_frame, width=10, textvariable=meal)
        self.meal_combobox['values'] = ('Dinner',
                                        'Lunch',
                                        'Breakfast',
                                        'Snacks',
                                        )
        self.meal_combobox.grid(row=8, column=1, pady=5)

        ttk.Button(search_frame, text="Selcet", command=lambda: show.show_serving(self,
                                                                                  self.food_options_combobox.get(), self.serving_combobox)).grid(row=4, column=1, pady=5)
        ttk.Button(search_frame, text="Add food", command=lambda: update.add_food(self, self.meal_combobox.get(), self.food_options_combobox.get(
        ), self.serving_combobox.get(), self.amount_entry.get())).grid(row=9, column=1, pady=5, sticky="s")

        self.done_new_diet = ttk.Labelframe(new_diet_frame)
        self.done_new_diet.grid(row=0, column=0, padx=10)
        ttk.Label(self.done_new_diet, text="Diet name: ").grid(row=0, column=0)

        self.diet_name_entry = ttk.Entry(self.done_new_diet, width=30)
        self.diet_name_entry.insert(END, chosen_diet)
        self.diet_name_entry.grid(row=0, column=1, pady=5, padx=10)

        error_label = ttk.Label(self.done_new_diet, text="")
        error_label.grid(row=2, column=1)

        if not is_edit:
            ttk.Button(self.done_new_diet, text="Add new diet", command=lambda: add_diet.add_new_diet(self, error_label
                                                                                                      )).grid(row=1, column=1, pady=5, sticky="s")
        else:
            ttk.Button(self.done_new_diet, text="Done", command=lambda: self.back_to_diets(
                new_diet_frame, False)).grid(row=1, column=1, pady=5, sticky="s")

    def create_optimal_frame(self, vitamin_frame: ttk.LabelFrame):
        """create the frame of the optimal value, include: label of the optimal value
        Args:
            vitamin_frame - parent of the optimal value frame
        """
        optimal_values_frame = ttk.Frame(vitamin_frame, width=150, height=200)
        optimal_values_frame.grid(row=0, column=6, sticky='w')
        ttk.Label(optimal_values_frame, text="Optimal value").grid(
            row=1, column=6, pady=5)

        row_count = 2
        for vitamin in VitaminNameData.vitamin_name:
            if vitamin == "Sodium":
                ttk.Label(optimal_values_frame, text="less than 2300 mg ").grid(
                    row=row_count, column=6, pady=6.5)

            elif vitamin == "Caffeine" and self.current_user.age > 18:
                ttk.Label(optimal_values_frame, text="less than 400 mg").grid(
                    row=row_count, column=6, pady=6.5)
            elif vitamin == "Caffeine" and self.current_user.age <= 18:
                ttk.Label(optimal_values_frame, text="0 mg").grid(
                    row=row_count, column=6, pady=6.5)
            else:
                ttk.Label(optimal_values_frame,
                          text=self.current_user.custom_recommended_values[vitamin]).grid(row=row_count, column=6, pady=6)
            row_count += 1

    def create_percentage_frame(self, vitamin_frame: ttk.LabelFrame, is_edit: bool, chosen_diet: str = ""):
        """ create the frame of progress bar for all vitamins 
        Args:
            vitamin_frame - parent of percentage frame
            is_edit - True if we on edit mode 
            chosen_diet - the current diet (passed only if is_edit=True)
        """
        percentage_frame = ttk.Frame(vitamin_frame, width=270, height=850)
        percentage_frame.grid(row=0, column=5)
        ttk.Label(percentage_frame, text="progress bar").grid(
            row=0, column=5, padx=50, pady=16)
        percentage_frame.grid_propagate(False)

        row_count = 1
        for vitamin in VitaminNameData.vitamin_name:
            optimal_quantity = self.current_user.get_number_from_recommended(
                vitamin)
            setattr(self, vitamin+"_pbar", ttkbootstrap.Floodgauge(percentage_frame, length=100,
                                                                   style='secondary.Horizontal.TFloodgauge', maximum=optimal_quantity))
            setattr(self, vitamin+"_label_pbar",
                    ttk.Label(percentage_frame, foreground="#42f5b6"))

            getattr(self, vitamin+"_pbar").grid(row=row_count,
                                                column=5, pady=7.4, ipady=1)
            getattr(self, vitamin+"_label_pbar").grid(row=row_count, column=6)
            row_count += 1

        if is_edit:
            dict_consumption = self.current_user.get_all_vitamin_values_from_diet(
                chosen_diet)
        else:
            dict_consumption = dict.fromkeys(VitaminNameData.vitamin_name, 0)
        update.set_consumption_widgets(self, dict_consumption)

    def create_meal_tableview(self, meal: str, grid_row_start: int, meals_frame: ttk.LabelFrame, is_edit: bool, chosen_diet: str):
        """create the frame and tableview of meal data in add_new_frame and edit-diets, 
        if in edit mode set all the foods from chosen_diet otherwise it's empty
        Args:
            meal - current meal
            grid_row_start - the first row of this meal frame
            meals_frame - frame of all the meals
            is_edit - True if we on edit mode 
            chosen_diet - the current diet (passed only if is_edit=True)
        """

        current_meal_frame = ttk.Frame(meals_frame, width=400, height=200)
        current_meal_frame.grid(row=grid_row_start, column=2, pady=7, padx=10)

        ttk.Label(current_meal_frame, text=meal).grid(
            row=grid_row_start, column=2)

        coldata = [
            {"text": "Name", "width": 250},
            {"text": "Serving", "width": 70},
            {"text": "Amount", "width": 70},
        ]

        setattr(self, "tableview_"+meal,  Tableview(
            master=current_meal_frame,
            coldata=coldata,

            paginated=True,
            height=5,

        ))

        current_meal_tableview = getattr(self, "tableview_"+meal)
        current_meal_tableview.grid(row=1+grid_row_start, column=2, sticky='e')
        current_meal_frame.grid_propagate(False)

        if is_edit:  # in edit mode add all foods from chosen_diet to current_meal_listbox
            foods_in_diet_meal = self.current_user.get_foods_from_meal_diet(
                chosen_diet, meal)

            for food in foods_in_diet_meal:
                current_meal_tableview.insert_row(
                    'end', [food.name, food.serving, food.amount])
        current_meal_tableview.load_table_data()

    def create_consumption_label(self, vitamin: str, row_count: int, consumption_frame: ttk.Frame, is_edit: bool, chosen_diet: str):
        """set labels of vitamin consumption to 0 ot the saved value
        Args:
            vitamin - the vitamin we create it's label
            row_count - the row of current label
            consumption_frame - the frame of all labels
            is_edit - True if we on edit mode 
            chosen_diet - the current diet (passed only if is_edit=True)
        """
        ttk.Label(consumption_frame, text=vitamin +
                  " :").grid(row=row_count, column=4)

        if not is_edit:
            setattr(self, vitamin+"_consumption_label",
                    ttk.Label(consumption_frame, text="0 "+VitaminNameData.units[vitamin]))
        else:  # in edit mode get the saved value
            value = self.current_user.get_vitamin_value_from_diet(
                chosen_diet, vitamin)
            print(vitamin)
            setattr(self, vitamin+"_consumption_label",
                    ttk.Label(consumption_frame, text=str(round(value, 2))+" "+VitaminNameData.units[vitamin]))

        getattr(self, vitamin+"_consumption_label").grid(row=row_count,
                                                         column=5, pady=6.49)

    def create_all_diets_tab(self, all_diet_frame: ttk.Frame):
        """ create all the diets tab (diets listbox and all the button)
        Args:
            all_diet_frame - current frame
        """
        self.diets_frame = ttk.Labelframe(
            all_diet_frame, width=2000, height=900)
        self.diets_frame.grid(row=0, column=0, padx=15, sticky='ns')
        ttk.Label(self.diets_frame, text="All your Diets").grid(
            row=1, column=1, pady=10, padx=30, sticky='ns')

        self.all_diets_listbox = tk.Listbox(self.diets_frame)
        self.all_diets_listbox.grid(row=2, column=1)
        self.all_diets_listbox.configure(
            background="skyblue4", foreground="black", font=('Aerial 13'))

        diets: list = self.current_user.get_diets_name()
        row = 2

        for diet_name in diets:
            add_diet.add_diet_to_all_diets_list(self, diet_name)
            row += 1

        buttons_diets_frame = ttk.Labelframe(
            all_diet_frame, width=2000, height=200)
        buttons_diets_frame.grid(row=0, column=2, padx=30)

        ttk.Button(buttons_diets_frame, text="Edit", command=lambda: self.edit_diet(
            self.all_diets_listbox.get(ANCHOR), all_diet_frame)).grid(row=1, column=2, padx=10, pady=10)
        ttk.Button(buttons_diets_frame, text="Analysis", command=lambda: self.create_analysis_diet(
            self.all_diets_listbox.get(ANCHOR), all_diet_frame)).grid(row=1, column=3, padx=10, pady=10)
        ttk.Button(buttons_diets_frame, text="Delete", command=lambda: delete.delete_diet(
            self)).grid(row=1, column=4, padx=10, pady=10)

    def edit_diet(self, chosen_diet: str, all_diet_frame: ttk.Frame):
        """ show the edit diet frame, which identical to the add_new_diet but all the diet data is  shown
        Args:
            chosen_diet -  the diet the user wanted to edit
            all_diet_frame - the current frame 
        """
        reset_fields.reset_frame(all_diet_frame)

        self.current_user.current_diet = self.current_user.user.diets[chosen_diet]

        self.create_search_frame(all_diet_frame, True, chosen_diet)
        self.create_meals_frame(all_diet_frame, True, chosen_diet)
        self.create_vitamin_frame(all_diet_frame, True, chosen_diet)

    def back_to_diets(self, new_diet_frame: ttk.Frame, is_analysis: bool):
        """ function used after editing an existing diet or analysis of a diet
        return to all diet tab
        Args:
            new_diet_frame - the current frame
            is_analysis - true if we go back from analysis frame
        """

        if not is_analysis:
            add_diet.add_diet_to_diets(self, True)

        reset_fields.reset_frame(new_diet_frame)

        self.create_all_diets_tab(new_diet_frame)

    def create_analysis_diet(self, chosen_diet: str, all_diet_frame: ttk.Frame):
        """show the analysis of the chosen_diet
        Args:
            chosen_diet -  the diet the user wanted to show
            all_diet_frame - current frame
        """

        reset_fields.reset_frame(all_diet_frame)

        self.analysis_diet_frame = ttk.Labelframe(all_diet_frame, width=2000)
        self.analysis_diet_frame.grid(row=0, column=0, padx=15, sticky='ns')

        ttk.Label(self.analysis_diet_frame, text="Analysis " +
                  chosen_diet).grid(row=1, column=0, pady=10, padx=30, sticky='ns')
        ttk.Label(self.analysis_diet_frame, text="choose your vitamin").grid(
            row=2, column=0, pady=10, padx=30, sticky='ns')

        list_box_analysis = tk.Listbox(
            self.analysis_diet_frame, width=50, height=35)
        list_box_analysis.grid(row=3, columns=1)

        for vitamin in VitaminNameData.vitamin_name:
            list_box_analysis.insert(END, vitamin)

        self.analysis_vitamin_pei = ttk.Labelframe(
            all_diet_frame, width=2000, height=50)
        self.analysis_vitamin_pei.grid(row=0, column=2, padx=15)

        ttk.Label(self.analysis_vitamin_pei,
                  text="Your Analysis data ").grid(row=0, column=2)

        self.analysis_vitamin_meal = ttk.Frame(
            all_diet_frame, width=2000, height=50)
        self.analysis_vitamin_meal.grid(row=0, column=3, padx=15)

        ttk.Button(all_diet_frame, text="Ok", command=lambda: analysis_chart.show_analysis_vitamin(
            self, chosen_diet, list_box_analysis.get(ANCHOR))).grid(row=4, column=0, padx=30, pady=10)
        ttk.Button(all_diet_frame, text="Back", command=lambda: self.back_to_diets(
            all_diet_frame, True)).grid(row=5, column=0, padx=30, pady=10)

    def get_current_diet(self) -> Diet:
        return self.current_user.get_current_diet()

    def get_entry(self, entry_name) -> str:
        return getattr(self, entry_name+"_entry").get()
