import helper


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
        """Constructor for Food object"""
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
        """Calculate intake for serving and amount"""
        ratio = helper.get_ratio(self.serving)
        intake_food = (
            float(self.vitamins[vitamin]) * ratio)*float(self.amount)

        return intake_food

    def get_vitamins(self):
        return self.vitamins

    def get_amount(self):
        return self.amount

    def get_serving(self):
        return self.serving

    def get_name(self):
        return self.name
