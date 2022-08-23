import json
from diet import Diet
from datetime import datetime



class User:
    """User class represent a user.

    Attributes:
        username - the username of user
        mail - user's mail
        password - user's password
        gender - user's gender (1= Female , 0= Man)
        birthday - user's birthday
        diets - dict with all user's diet (key is string-diet name, value is a diet obj)
        num_of_diets - number of diets
    """

    def __init__(self, username: str, mail: str, password: str, gender: bool, birthday: datetime, num_of_diets: int = 0):
        """Constructor for User object"""
        self.username: str = username
        self.mail: str = mail
        self.password: str = password
        self.gender: bool = gender
        self.birthday: datetime = birthday
        self.diets: dict = {}
        self.num_of_diets: int = num_of_diets

    def get_foods_from_meal_diet(self, chosen_diet: str, meal: str) -> list:
        """Return list of all the foods from chosen_diet and chosen_meal"""
        return (self.diets[chosen_diet]).get_foods_from_meals(meal)

    def add_new_diet(self, diet: Diet, diet_name: str, is_edit: bool):
        """Add new diet to self.diets dict
        Args:
            diet - the diet we want to add
            diet_name - the diet name
            is_edit - in edit mode we dont increase num_of_diets
        """
        self.diets[diet_name] = diet

        if not is_edit:
            self.num_of_diets += 1

    def set_diets_json(self, json_diets: json):
        """Set the diet dict from a json"""
        if json_diets:
            for diet_name, diet_obj in json_diets.items():
                diet_to_obj = Diet(diet_obj, True)
                self.diets[diet_name] = diet_to_obj

    def get_diet(self, diet_name: str) -> Diet:
        """Return the diet object of diet_name from self.diets"""
        return self.diets[diet_name]

    def delete_diet(self, diet_name: str):
        """Delete diet from diets"""
        self.num_of_diets -= 1
        del self.diets[diet_name]

    def set_username(self, username_new: str):
        self.username = username_new

    def set_mail(self, mail_new: str):
        self.mail = mail_new

    def get_password(self):
        return self.password

    def set_password(self, password_new: str):
        self.password = password_new

    def get_diets_name(self) -> list:
        return self.diets.keys()

    def get_vitamin_value_from_meal(self, chosen_diet: str, meal: str, vitamin: str) -> float:
        """Get vitamin intake value from meal in chosen_diet"""
        return self.diets[chosen_diet].get_vitamin_value_from_meal(meal, vitamin)

    def get_vitamin_value_from_diet(self, chosen_diet: str, vitamin: str) -> float:
        """Return the vitamin intake from chosen_diet"""
        return self.diets[chosen_diet].get_vitamin_value(vitamin)

    def get_all_vitamin_values_from_diet(self, chosen_diet: str):
        """Return all vitamins intake from chosen_diet"""
        return self.diets[chosen_diet].get_vitamins()
