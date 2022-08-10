from ast import Str
from user import User
from diet import Diet
from meal import Meal
from food import Food
import helper
import USDA_handler
import handle_db
import re


class CurrentUser:
    """ class that represent the user that use the app now.

    Attributes:
    user - user object of the user
    custom_recommended_values - the user optimal values for all vitamin 
    current_diet - diet object of the current diet the user edit now
    user_collection - user data from collection
    age - the age of user (calculated from his birthday)
    """

    def __init__(self, user: User):

        self.user = user
        self.age: int = helper.calculate_age(self.user.birthday)
        self.custom_recommended_values: dict = USDA_handler.get_amount(
            int(self.age), self.user.gender)  # recommend vitamin value according to USDA
        self.current_diet = self.reset_diet()
        self.user_collection = handle_db.get_user(self.user.username)

    def reset_diet(self) -> Diet:
        """create new diet object and return it"""
        self.Breakfast_foods: Meal = Meal()
        self.Dinner_foods: Meal = Meal()
        self.Lunch_foods: Meal = Meal()
        self.Snacks_foods: Meal = Meal()
        meals_dct = {}
        lst_of_meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        for meal in lst_of_meals:
            meals_dct[meal] = getattr(self, meal+"_foods")
        return Diet(meals_dct, False)

    def get_name(self) -> str:
        """get the name of user"""
        return self.user.username

    def get_mail(self) -> str:
        """get the mail of user"""
        return self.user.mail

    def get_diets_name(self):
        """return the names of all the diets"""
        return self.user.diets.keys()

    def get_vitamin_value_from_meal(self, chosen_diet: str, meal: str, vitamin: str):
        """get vitamin intake value from meal in chosen_diet"""
        return self.user.get_vitamin_value_from_meal(chosen_diet, meal, vitamin)

    def get_vitamin_value_from_diet(self, chosen_diet: str, vitamin: str) -> float:
        """return the vitamin consumption from chosen_diet"""
        return self.user.get_vitamin_value_from_diet(chosen_diet, vitamin)

    def get_all_vitamin_values_from_diet(self, chosen_diet: Str) -> dict:
        """return all vitamins consumption from chosen_diet"""
        return self.user.get_all_vitamin_values_from_diet(chosen_diet)

    def get_diet(self, diet_name: str) -> Diet:
        """return diet object of diet_name"""
        return self.user.get_diet(diet_name)

    def delete_diet(self, diet_name: str):
        """delete diet in db and in user object"""
        handle_db.delete_from_db(self.user_collection, diet_name)
        self.user.delete_diet(diet_name)

    def update_username(self, new_username: str):
        """update username"""
        handle_db.update_username(self.user_collection, new_username)
        self.user.set_username(new_username)

    def update_mail(self, new_mail: str):
        """update mail"""
        handle_db.update_mail(self.user_collection, new_mail)
        self.user.set_mail(new_mail)

    def get_password(self) -> str:
        """return user's password"""
        return self.user.get_password()

    def update_password(self, new_password: str):
        """update password to new_password"""
        hashed_new_password = helper.make_hashed_password(new_password)
        self.user.set_password(hashed_new_password)
        handle_db.update_password(self.user_collection, hashed_new_password)

    def update_diets(self, current_diet: Diet, diet_name: str, is_edit: bool):
        """add diet to diets"""
        self.user.add_new_diet(current_diet, diet_name, is_edit)
        handle_db.update_diets(self.user_collection,
                               diet_name, is_edit, current_diet)

    def get_number_from_recommended(self, vitamin: str) -> float:
        """return the optimal amount of vitamin"""
        return float(re.findall("[-+]?(?:\d*\,\d*\.\d+|\d*\.\d+|\d*\,\d+|\d+)", str(
            self.custom_recommended_values[vitamin]))[0].replace(',', ''))

    def get_foods_from_meal_diet(self, chosen_diet: str, meal: str) -> list:
        """get list of foods from meal in chosen_diet"""
        return self.user.get_foods_from_meal_diet(
            chosen_diet, meal)

    def update_meal(self, meal: str, food_id: str, food_name: str, serving: str, amount: str, current_food_nutrient: dict):
        """update meal with new food data"""
        current_meal = self.current_diet.get_meal(meal)
        new_food = Food(food_id, food_name, serving,
                        amount, current_food_nutrient)

        current_meal.add_food(new_food)

    def get_current_diet_vitamins(self) -> dict:
        """get vitamin intake from current_diet"""
        return self.current_diet.get_vitamins()

    def get_current_diet(self) -> Diet:
        """return current diet object"""
        return self.current_diet

    def get_diets_name(self) -> list:
        """return list of all diets name"""
        return self.user.get_diets_name()

    def get_meal(self, meal: str) -> Meal:
        """return Meal object of meal"""
        return self.current_diet.get_meal(meal)
