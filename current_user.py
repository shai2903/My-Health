from ast import Str
from user import User
from diet import Diet
from meal import Meal
from food import Food
import helper
import handler_USDA
import handler_mongoDB
from consts import Meals, REGEX_FIND_FLOAT


class CurrentUser:
    """Class that represent the user that use the app now.

    Attributes:
        user - user object of the user
        custom_recommended_values - the user optimal values for all vitamin 
        current_diet - diet object of the current diet the user edit now
        user_collection - user data from collection
        age - the age of user (calculated from his birthday)
    """

    def __init__(self, user: User):

        self.user: User = user
        self.age: int = helper.calculate_age(self.user.birthday)
        self.custom_recommended_values: dict = handler_USDA.get_amount(
            int(self.age), self.user.gender)  # Recommend vitamin value according to USDA
        self.current_diet: Diet = self.reset_diet()
        self.user_collection = handler_mongoDB.get_user(self.user.username)

    def reset_diet(self) -> Diet:
        """Create new diet object and return it"""
        self.breakfast_foods: Meal = Meal()
        self.dinner_foods: Meal = Meal()
        self.lunch_foods: Meal = Meal()
        self.snacks_foods: Meal = Meal()
        meals_dct: dict = {}

        for enum_meal in Meals:
            meal = enum_meal.value
            meals_dct[meal] = getattr(self, meal+"_foods")
        return Diet(meals_dct, False)

    def get_name(self) -> str:
        """Get the name of user"""
        return self.user.username

    def get_mail(self) -> str:
        """Get the mail of user"""
        return self.user.mail

    def get_vitamin_value_from_meal(self, chosen_diet: str, meal: str, vitamin: str):
        """Get vitamin intake value from meal in chosen_diet"""
        return self.user.get_vitamin_value_from_meal(chosen_diet, meal, vitamin)

    def get_vitamin_value_from_diet(self, chosen_diet: str, vitamin: str) -> float:
        """Return the vitamin intake from chosen_diet"""
        return self.user.get_vitamin_value_from_diet(chosen_diet, vitamin)

    def get_all_vitamin_values_from_diet(self, chosen_diet: Str) -> dict:
        """Return all vitamins intake from chosen_diet"""
        return self.user.get_all_vitamin_values_from_diet(chosen_diet)

    def get_diet(self, diet_name: str) -> Diet:
        """Return diet object of diet_name"""
        return self.user.get_diet(diet_name)

    def delete_diet(self, diet_name: str):
        """Delete diet in collection and in user object"""
        handler_mongoDB.delete_from_collection(self.user_collection, diet_name)
        self.user.delete_diet(diet_name)

    def update_username(self, username_new: str):
        """Update username"""
        handler_mongoDB.update_username(self.user_collection, username_new)
        self.user.set_username(username_new)

    def update_mail(self, mail_new: str):
        """Update mail"""
        handler_mongoDB.update_mail(self.user_collection, mail_new)
        self.user.set_mail(mail_new)

    def get_password(self) -> str:
        """Return user's password"""
        return self.user.get_password()

    def update_password(self, password_new: str):
        """Update password to password_new"""
        password_hashed_new = helper.make_password_hashed(password_new)
        self.user.set_password(password_hashed_new)
        handler_mongoDB.update_password(
            self.user_collection, password_hashed_new)

    def update_diets(self, current_diet: Diet, diet_name: str, is_edit: bool):
        """Add diet to diets"""
        self.user.add_new_diet(current_diet, diet_name, is_edit)
        handler_mongoDB.update_diets(self.user_collection,
                                     diet_name, is_edit, current_diet)

    def get_number_from_recommended(self, vitamin: str) -> float:
        """Return the optimal amount of vitamin"""
        return float(REGEX_FIND_FLOAT.findall(self.custom_recommended_values[vitamin])[0].replace(',', ''))

    def get_foods_from_meal_diet(self, chosen_diet: str, meal: str) -> list:
        """Get list of foods from meal in chosen_diet"""
        return self.user.get_foods_from_meal_diet(
            chosen_diet, meal)

    def update_meal(self, meal: str, food_id: str, food_name: str, serving: str, amount: str, current_food_nutrient: dict):
        """Update meal with new food data"""
        current_meal = self.current_diet.get_meal(meal)
        new_food = Food(food_id, food_name, serving,
                        amount, current_food_nutrient)

        current_meal.add_food(new_food)

    def get_current_diet_vitamins(self) -> dict:
        """Get vitamin intake from current_diet"""
        return self.current_diet.get_vitamins()

    def get_current_diet(self) -> Diet:
        """Return current diet object"""
        return self.current_diet

    def get_diets_name(self) -> list:
        """Return list of all diets name"""
        return self.user.get_diets_name()

    def get_meal(self, meal: str) -> Meal:
        """Return Meal object of meal"""
        return self.current_diet.get_meal(meal)

    def set_current_diet(self, chosen_diet: str):
        """Set current diet to chosen_diet"""
        self.current_diet = self.user.get_diet(chosen_diet)
