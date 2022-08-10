from food import Food
from vitamin_data import VitaminNameData


class Meal:
    """Meal class represent a meal from a diet.

    Attributes:
        vitamins - dict of vitamin data of all foods from meal
        list_of_foods - list of foods in meal
        num_of_foods - num of foods in meal
    """

    def __init__(self, dict_meal: dict = None):
        """constructor for Meal object
        Args:
            dict_meal - if not none, the dict is meal in dict format
        """
        if not dict_meal:
            self.vitamins = dict.fromkeys(VitaminNameData.vitamin_name, 0)
            self.list_of_foods: list[Food] = []
            self.num_of_foods = 0
        else:  # creating Meal object from dict
            if dict_meal is not None:
                for key, value in dict_meal.items():
                    if key == "list_of_foods":
                        setattr(self, key, [])
                        # create food object for each food and add it to list
                        for food_value in value:
                            food = Food(dict_food=food_value)
                            self.list_of_foods.append(food)
                    else:
                        setattr(self, key, value)

    def get_foods(self) -> list:
        """return list_of_foods"""
        return self.list_of_foods

    def get_num_of_foods(self) -> int:
        """return num_of_foods"""
        return self.num_of_foods

    def add_food(self, food: Food):
        """add food to list and update num_of_foods"""
        self.num_of_foods += 1
        self.list_of_foods.append(food)
        for vitamin in food.get_vitamins().keys():
            to_add = food.calculate_for_serving(vitamin)
            self.add_to_vitamin(vitamin, to_add)

    def add_to_vitamin(self, vitamin: str, to_add: float):
        """add to_add to to specific vitamin in dict """
        self.vitamins[vitamin] += to_add

    def delete_food(self, food_name: str) -> Food:
        """delete food_name from list of foods and update vitamins, return the deleted food"""
        to_return = None

        for food in self.list_of_foods:
            if food.name == food_name:
                to_return = food
                self.num_of_foods -= 1
                self.list_of_foods.remove(food)
                break
        if to_return:
            for vitamin in VitaminNameData.vitamin_name:
                to_add = to_return.calculate_for_serving(vitamin)
                self.add_to_vitamin(vitamin, (-1)*to_add)
            return to_return

    def get_vitamin(self, vitamin: str) -> float:
        return self.vitamins[vitamin]
