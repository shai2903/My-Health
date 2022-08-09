from vitamin_data import VitaminNameData
from meal import Meal


class Diet:
    """Diet class represent a diet of user.

    Attributes:
        meals - dict with key as the lunch\breakfast\dinner\snacks and value is a meal object  
        vitamins - dict with all the vitamins data for all meals in diet     
    """

    def __init__(self, dict_diet: dict, is_dict_json):
        """constructor for diet object"""
        if not is_dict_json:
            self.meals: dict = dict_diet
            self.vitamins: dict = dict.fromkeys(
                VitaminNameData.vitamin_name, 0)
        else:
            if dict_diet:
                for key, value in dict_diet.items():
                    if key == "meals":
                        self.meals = {}
                        for meal_name, meal_dict in value.items():
                            self.meals[meal_name] = Meal(meal_dict)
                    else:
                        setattr(self, key, value)

    def get_foods_from_meals(self, meal: str) -> list:
        """return list_of_foods from meal"""
        return self.meals[meal].get_foods()

    def get_meal(self, meal: str) -> Meal:
        """return Meal object of meal"""
        return self.meals[meal]

    def get_vitamins(self) -> dict:
        return self.vitamins

