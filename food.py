import re


class Food:
    """Food class represent a food object.

    Attributes:
        food_id - the food id from USDA
        name - food name from USDA
        serving - the serving the user chose
        amount - the amount of serving the user choose
        vitamins - dict of vitamin data from food,(taken from USDA)
    """

    def __init__(self, food_id: str = "", name: str = "", serving: str = "", amount: str = "", vitamins: dict = "", dict_food=None):
        """constructor for Food object"""
        if not dict_food:
            self.food_id: str = food_id
            self.name: str = name
            self.serving: str = serving
            self.amount: str = amount
            self.vitamins: dict = vitamins  # vitamin for 100 gr of food
        else:
            if dict_food:
                for key, value in dict_food.items():
                    setattr(self, key, value)

    def calculate_for_serving(self, vitamin):
        sreving_in_grams = float(re.findall("\(\d*\.\d*\s[g][gr]\)", self.serving)[0].split(
            "(")[1].split(' ')[0])  # get serving in grams (example: 1 cup is x gram)

        ratio = sreving_in_grams/100
        consumption_food = (
            float(self.vitamins[vitamin]) * ratio)*float(self.amount)

        return consumption_food
