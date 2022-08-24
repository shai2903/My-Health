import tkinter.ttk as ttk
from tkinter import ANCHOR, END
import tkinter as tk
import ttkbootstrap
from ttkbootstrap.tableview import Tableview
import add_diet
import reset_fields
import show
import delete
import update
import analysis_chart
from vitamin_data.vitamin_names import VitaminName
from current_user import CurrentUser
from diet import Diet
from consts import Meals,GREEN_PERCENTAGE



class DietsTab():
    """Class creating the tabs frame.
    Attributes:
        current_user - current user object
        food_name_entry - the entry of food the user choose
        food_options_combobox - all the food options from USDA
        amount_entry - the entry of the amount the user choose
        meal_combobox - the entry of the meal the user choose (lunch\breakfast\snacks\dinner)
        analysis_vitamin_meal_frame - frame for the meal analysis the user choose
        analysis_vitamin_pie_frame - frame for analysis-pie
        all_diets_listbox - list box of all diets
        serving_combobox - combobox of all the options serving options from USDA
        diet_name_entry - the entry of the diet name the user choose
    """

    def __init__(self, current_user: CurrentUser):
        self.current_user = current_user
        self.food_name_entry = None
        self.food_options_combobox = None
        self.amount_entry = None
        self.meal_combobox = None
        self.analysis_vitamin_meal_frame = None
        self.analysis_vitamin_pie_frame = None
        self.all_diets_listbox = None
        self.serving_combobox = None
        self.diet_name_entry = None

    def create_new_diet_tab(self, new_diet_frame: ttk.Frame):
        """Create the new diet tab
        Args:
            new_diet_frame - the parent frame of all the tabs"""

        self.create_search_frame(new_diet_frame, False, "")
        self.create_meals_frame(new_diet_frame, False, "")
        self.create_vitamin_frame(new_diet_frame, False)

    def create_vitamin_frame(self, new_diet_frame: ttk.Frame, is_edit: bool, chosen_diet: str = ""):
        """Create the parent frame of all the vitamin related data
        (i.e: optimal value and user intake)
        Args:
            new_diet_frame - the frame of the Add_new_edit tab
            is_edit - true if in edit mode
            chosen_diet - the diet the user choose in edit mode
        """
        vitamin_frame = ttk.LabelFrame(new_diet_frame, width=930, height=900)
        vitamin_frame.grid(row=0, column=4)
        vitamin_frame.grid_propagate(False)

        self.create_vitamin_intake_frame(
            vitamin_frame, is_edit, chosen_diet)
        self.create_percentage_frame(vitamin_frame, is_edit, chosen_diet)
        self.create_optimal_frame(vitamin_frame)

    def create_vitamin_intake_frame(self, vitamin_frame: ttk.LabelFrame, is_edit: bool, chosen_diet: str):
        """Create the user intake vitamin frame
        (i.e how much vitamin he consume from the food in is diet)
        Args:
            vitamin_frame - parent of the intake frame
            is_edit - true if in edit mode, in edit mode we set the value accordingly to the chosen_diet foods
            chosen_diet - the diet the user choose in edit mode
        """
        intake_frame = ttk.Frame(vitamin_frame, width=150, height=200)
        intake_frame.grid(row=0, column=4)
        ttk.Label(intake_frame, text="Your intake").grid(
            row=0, column=4, pady=5)

        for index, vitamin in enumerate(VitaminName.vitamin_name):
            self.create_intake_label(
                vitamin, index+1, intake_frame, is_edit, chosen_diet)

    def create_meals_frame(self, new_diet_frame: ttk.Frame, is_edit: bool, chosen_diet: str):
        """Create the meals frame (i.e the tableview with the chosen food for each meal)
        Args:
            new_diet_frame - the frame of the Add_new_edit tab
            is_edit - true if in edit mode
            chosen_diet - the diet the user choose in edit mode
        """
        meals_frame = ttk.LabelFrame(new_diet_frame)
        meals_frame.grid(row=0, column=3, sticky="nw", pady=10, padx=10)

        for index, meal in enumerate(Meals):
            self.create_meal_tableview(
                meal.value, index, meals_frame, is_edit, chosen_diet)

        delete_button = ttk.Button(
            meals_frame, text="Delete", command=lambda: delete.delete_item_from_list_box(self))
        delete_button.grid(row=4, column=2, sticky='n', pady=10)

    def create_search_frame(self, new_diet_frame: ttk.Frame, is_edit: bool, chosen_diet: str):
        """Create the search frame from add_new_diet tab
        if in edit mode replace the "add new diet" button to "Done" button
        Args:
            new_diet_frame - the parent frame
            is_edit - true if in edit mode
            chosen_diet - the diet the user choose in edit mode
        """
        search_frame = ttk.LabelFrame(new_diet_frame)
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
        search_button = ttk.Button(
            search_frame, text="Search", command=lambda: show.show_food_options(self))
        search_button.grid(row=2, column=1, pady=5, sticky='e')

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
        self.meal_combobox['values'] = ('dinner',
                                        'lunch',
                                        'breakfast',
                                        'snacks',
                                        )
        self.meal_combobox.grid(row=8, column=1, pady=5)

        ttk.Button(search_frame, text="Select", command=lambda: show.show_serving(
            self)).grid(row=4, column=1, pady=5)
        ttk.Button(search_frame, text="Add food", command=lambda: update.add_food(
            self)).grid(row=9, column=1, pady=5, sticky="s")

        done_new_diet_frame = ttk.Labelframe(new_diet_frame)
        done_new_diet_frame.grid(row=0, column=0, padx=10)
        ttk.Label(done_new_diet_frame, text="Diet name: ").grid(
            row=0, column=0)

        self.diet_name_entry = ttk.Entry(done_new_diet_frame, width=30)
        self.diet_name_entry.insert(END, chosen_diet)
        self.diet_name_entry.grid(row=0, column=1, pady=5, padx=10)

        error_label = ttk.Label(done_new_diet_frame, text="")
        error_label.grid(row=2, column=1)

        if not is_edit:
            ttk.Button(done_new_diet_frame, text="Add new diet", command=lambda: add_diet.add_new_diet(self, error_label
                                                                                                       )).grid(row=1, column=1, pady=5, sticky="s")
        else:
            ttk.Button(done_new_diet_frame, text="Done", command=lambda: self.back_to_diets(
                new_diet_frame, False)).grid(row=1, column=1, pady=5, sticky="s")

    def create_optimal_frame(self, vitamin_frame: ttk.LabelFrame):
        """Create the frame of the optimal value, include: label of the optimal value
        Args:
            vitamin_frame - parent of the optimal value frame
        """
        optimal_values_frame = ttk.Frame(vitamin_frame)
        optimal_values_frame.grid(row=0, column=6, sticky='w')
        ttk.Label(optimal_values_frame, text="Optimal value").grid(
            row=1, column=6, pady=5)

        row_count = 2
        for vitamin in VitaminName.vitamin_name:
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
        """Create the frame of progress bar for all vitamins
        Args:
            vitamin_frame - parent of percentage frame
            is_edit - True if we on edit mode
            chosen_diet - the current diet (passed only if is_edit=True)
        """
        percentage_frame = ttk.Frame(vitamin_frame)
        percentage_frame.grid(row=0, column=5)
        ttk.Label(percentage_frame, text="progress bar").grid(
            row=0, column=5, padx=50, pady=16)

        row_count = 1
        for vitamin in VitaminName.vitamin_name:
            optimal_quantity = self.current_user.get_number_from_recommended(
                vitamin)
            setattr(self, vitamin+"_pbar", ttkbootstrap.Floodgauge(percentage_frame, length=100,
                                                                   style='secondary.Horizontal.TFloodgauge', maximum=optimal_quantity))
            setattr(self, vitamin+"pbar_label",
                    ttk.Label(percentage_frame, foreground=GREEN_PERCENTAGE))

            getattr(self, vitamin+"_pbar").grid(row=row_count,
                                                column=5, pady=7.4, ipady=1)
            getattr(self, vitamin+"pbar_label").grid(row=row_count, column=6)
            row_count += 1

        if is_edit:
            dict_intake = self.current_user.get_all_vitamin_values_from_diet(
                chosen_diet)
        else:
            dict_intake = dict.fromkeys(VitaminName.vitamin_name, 0)
        update.set_intake_widgets(self, dict_intake)

    def create_meal_tableview(self, meal: str, grid_row_start: int, meals_frame: ttk.LabelFrame, is_edit: bool, chosen_diet: str):
        """Create the frame and tableview of meal data in add_new_frame and edit-diets, 
        if in edit mode set all the foods from chosen_diet otherwise it's empty
        Args:
            meal - current meal
            grid_row_start - the first row of this meal frame
            meals_frame - frame of all the meals
            is_edit - True if we on edit mode 
            chosen_diet - the current diet (not empty only if is_edit=True)
        """

        current_meal_frame = ttk.Frame(meals_frame)
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

        if is_edit:  # in edit mode add all foods from chosen_diet to current_meal_listbox
            foods_in_diet_meal = self.current_user.get_foods_from_meal_diet(
                chosen_diet, meal)

            for food in foods_in_diet_meal:
                current_meal_tableview.insert_row(
                    'end', [food.name, food.serving, food.amount])
        current_meal_tableview.load_table_data()

    def create_intake_label(self, vitamin: str, row_count: int, intake_frame: ttk.Frame, is_edit: bool, chosen_diet: str):
        """Set labels of vitamin intake to 0 ot the saved value
        Args:
            vitamin - the vitamin we create it's label
            row_count - the row of current label
            intake_frame - the frame of all labels
            is_edit - True if we on edit mode
            chosen_diet - the current diet (passed only if is_edit=True)
        """
        ttk.Label(intake_frame, text=vitamin +
                  " :").grid(row=row_count, column=4)

        if not is_edit:
            setattr(self, vitamin+"_intake_label",
                    ttk.Label(intake_frame, text="0 "+VitaminName.units[vitamin]))
        else:  # in edit mode get the saved value
            value = self.current_user.get_vitamin_value_from_diet(
                chosen_diet, vitamin)
            setattr(self, vitamin+"_intake_label",
                    ttk.Label(intake_frame, text=str(round(value, 2))+" "+VitaminName.units[vitamin]))

        getattr(self, vitamin+"_intake_label").grid(row=row_count,
                                                    column=5, pady=6.49)

    def create_all_diets_tab(self, all_diet_frame: ttk.Frame):
        """Create all the diets tab (diets listbox and all the button)
        Args:
            all_diet_frame - current frame
        """
        diets_frame = ttk.Labelframe(all_diet_frame)
        diets_frame.grid(row=0, column=0, padx=15, sticky='ns')
        ttk.Label(diets_frame, text="All your Diets").grid(
            row=1, column=1, pady=10, padx=30, sticky='ns')

        self.all_diets_listbox = tk.Listbox(diets_frame)
        self.all_diets_listbox.grid(row=2, column=1)
        self.all_diets_listbox.configure(
            background="skyblue4", foreground="black", font=('Aerial 13'))

        diets: list = self.current_user.get_diets_name()
        row = 2

        for diet_name in diets:
            add_diet.add_diet_to_all_diets_list(self, diet_name)
            row += 1

        buttons_diets_frame = ttk.Labelframe(all_diet_frame)
        buttons_diets_frame.grid(row=0, column=2, padx=30)

        ttk.Button(buttons_diets_frame, text="Edit", command=lambda: self.edit_diet(
            self.all_diets_listbox.get(ANCHOR), all_diet_frame)).grid(row=1, column=2, padx=10, pady=10)
        ttk.Button(buttons_diets_frame, text="Analysis", command=lambda: self.create_analysis_diet(
            self.all_diets_listbox.get(ANCHOR), all_diet_frame)).grid(row=1, column=3, padx=10, pady=10)
        ttk.Button(buttons_diets_frame, text="Delete", command=lambda: delete.delete_diet(
            self)).grid(row=1, column=4, padx=10, pady=10)

    def edit_diet(self, chosen_diet: str, all_diet_frame: ttk.Frame):
        """Show the edit diet frame, which identical to the add_new_diet but all the diet data is  shown
        Args:
            chosen_diet -  the diet the user wanted to edit
            all_diet_frame - the current frame
        """
        reset_fields.reset_frame(all_diet_frame)

        self.current_user.set_current_diet(chosen_diet)

        self.create_search_frame(all_diet_frame, True, chosen_diet)
        self.create_meals_frame(all_diet_frame, True, chosen_diet)
        self.create_vitamin_frame(all_diet_frame, True, chosen_diet)

    def back_to_diets(self, new_diet_frame: ttk.Frame, is_analysis: bool):
        """Function used after editing an existing diet or analysis of a diet
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
        """Show the analysis of the chosen_diet
        Args:
            chosen_diet -  the diet the user wanted to show
            all_diet_frame - current frame
        """

        reset_fields.reset_frame(all_diet_frame)

        analysis_diet_frame = ttk.Labelframe(all_diet_frame, width=2000)
        analysis_diet_frame.grid(row=0, column=0, padx=15, sticky='ns')

        ttk.Label(analysis_diet_frame, text="Analysis " +
                  chosen_diet).grid(row=1, column=0, pady=10, padx=30, sticky='ns')
        ttk.Label(analysis_diet_frame, text="Choose your vitamin").grid(
            row=2, column=0, pady=10, padx=30, sticky='ns')

        analysis_listbox = tk.Listbox(
            analysis_diet_frame, width=50, height=35)
        analysis_listbox.grid(row=3, columns=1)

        for vitamin in VitaminName.vitamin_name:
            analysis_listbox.insert(END, vitamin)

        self.analysis_vitamin_pie_frame = ttk.Labelframe(
            all_diet_frame, width=2000, height=50)
        self.analysis_vitamin_pie_frame.grid(row=0, column=2, padx=15)

        ttk.Label(self.analysis_vitamin_pie_frame,
                  text="Your Analysis data ").grid(row=0, column=2)

        self.analysis_vitamin_meal_frame = ttk.Frame(
            all_diet_frame, width=2000, height=50)
        self.analysis_vitamin_meal_frame.grid(row=0, column=3, padx=15)

        ttk.Button(all_diet_frame, text="Ok", command=lambda: analysis_chart.show_analysis_vitamin(
            self, chosen_diet, analysis_listbox.get(ANCHOR))).grid(row=4, column=0, padx=30, pady=10)
        ttk.Button(all_diet_frame, text="Back", command=lambda: self.back_to_diets(
            all_diet_frame, True)).grid(row=5, column=0, padx=30, pady=10)

    def get_current_diet(self) -> Diet:
        return self.current_user.get_current_diet()

    def get_entry(self, entry_name) -> str:
        return getattr(self, entry_name+"_entry").get()
