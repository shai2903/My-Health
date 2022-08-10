import json
import bcrypt
from diet import Diet
from datetime import datetime
salt = bcrypt.gensalt()


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
        """constructor for User object"""
        self.username: str = username
        self.mail: str = mail
        self.password: str = password
        self.gender: bool = gender
        self.birthday: datetime = birthday
        self.diets: dict = {}
        self.num_of_diets: int = num_of_diets

    def get_foods_from_meal_diet(self, chosen_diet: str, meal: str) -> list:
        """return list of all the foods from chosen_diet and chosen_meal"""
        return (self.diets[chosen_diet]).get_foods_from_meals(meal)

    def add_new_diet(self, diet: Diet, diet_name: str, is_edit: bool):
        """add new diet to self.diets dict
        Args:
            diet - the diet we want to add
            diet_name - the diet name
            is_edit - in edit mode we dont increase num_of_diets
        """
        self.diets[diet_name] = diet

        if not is_edit:
            self.num_of_diets += 1

    def set_diets_json(self, json_diets: json):
        """set the diet dict from a json"""
        if json_diets:
            for diet_name, diet_obj in json_diets.items():
                diet_to_obj = Diet(diet_obj, True)
                self.diets[diet_name] = diet_to_obj

    def get_diet(self, diet_name: str) -> Diet:
        """return the diet object of diet_name from self.diets"""
        return self.diets[diet_name]

    def delete_diet(self, diet_name: str):
        """delete diet from diets"""
        self.num_of_diets -= 1
        del self.diets[diet_name]

    def set_username(self, new_username: str):
        self.username = new_username

    def set_mail(self, new_mail: str):
        self.mail = new_mail

    def get_password(self):
        return self.password

    def set_password(self, new_password: str):
        self.password = new_password

    def get_diets_name(self) -> list:
        return self.diets.keys()

    def get_vitamin_value_from_meal(self, chosen_diet: str, meal: str, vitamin: str) -> float:
        """get vitamin intake value from meal in chosen_diet"""
        return self.diets[chosen_diet].get_vitamin_value_from_meal(meal, vitamin)

    def get_vitamin_value_from_diet(self, chosen_diet: str, vitamin: str) -> float:
        """return the vitamin consumption from chosen_diet"""
        return self.diets[chosen_diet].get_vitamin_value(vitamin)

    def get_all_vitamin_values_from_diet(self, chosen_diet: str):
        """return all vitamins consumption from chosen_diet"""
        self.diets[chosen_diet].get_vitamins()
