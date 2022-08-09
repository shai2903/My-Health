import json
import requests
from vitamin_data import OptimalData
from vitamin_data import VitaminNameData

key_from_USDA = "Idd4pw784uoM2XfIhNmIyxsfwKv6xLdUBnIUz99m"

def get_all_options_USDA(food_name: str) -> list:
    """ get all the food option from searching food_name in USDA
        Args:
           food_name - the food name we search
    """
    json_result = requests.get(
        'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={}&query={}&dataType=SR Legacy'.format(key_from_USDA, food_name))
    return json_result.json()["foods"]


def get_serving_option(food_id: str) -> list:
    """ get all the serving option from searching food_id in USDA
        Args:
           food_id - the food id we search
    """
    api_response = json.loads(requests.get(
        'https://api.nal.usda.gov/fdc/v1/food/' + food_id + '?api_key=' + key_from_USDA).text)
    api_serving = api_response['foodPortions']
    serving = []

    for serving_info in api_serving:
        if 'modifier' in serving_info and 'gramWeight' in serving_info :
            serving.append(serving_info['modifier']+" " +
                           "("+str(serving_info['gramWeight']) + " gr"+")")

    return serving


def get_food_nutrient(food_id: str) -> dict:
    """ get all food nutrient from searching food_id in USDA
        Args:
           food_id - the food id we search
    """
    vitamins_nutrient = dict.fromkeys(VitaminNameData.vitamin_name, 0)
    api_response = json.loads(requests.get(
        'https://api.nal.usda.gov/fdc/v1/food/' + food_id + '?api_key=' + key_from_USDA).text)

    api_nutrients = api_response['foodNutrients']

    for nutrients in api_nutrients:
        if 'nutrient' in nutrients:
            if 'name' in nutrients['nutrient']:
                index = is_in_selected_vitamins(
                    nutrients['nutrient']['name'].lower())
                if index >= 0:
                    if 'amount' in nutrients:
                        offical_name = VitaminNameData.vitamin_name[index]
                        vitamins_nutrient[offical_name] += round(
                            float(nutrients['amount']), 2)

    return vitamins_nutrient


def is_in_selected_vitamins(vitamin_name: str) ->int:
    """check if vitamin in vitamin_name_united and return it's index, if vitamin isn't in vitamin_name_united return -1"""
    index = 0
    for item in VitaminNameData.vitamin_name_united:
        if isinstance(item, tuple):
            for vitamin in item:

                if vitamin.lower() == vitamin_name:

                    return index
        else:

            if vitamin_name == item.lower():
                return index
        index += 1

    return -1


def get_amount_vitamin(age: float, gender: bool, df_vitamin) -> str:
    """ get the optimal value according to age and gender from df_vitamins.
    Args:
        age - the age of user
        gender - the gender of user (1= Female , 0= Man)
        df_vitamin - dataFrame with the optimal intake of vitamin (for all age and gender)
    """
    return (df_vitamin[df_vitamin.loc[:, 'Age'] > age].head(1).loc[:, gender]).values[0]


def get_amount(age: float, gender: bool) -> dict:
    """ get the optimal value according to age and gender for each vitamin
    Args:
        age - the age of user
        gender - the gender of user(1= Female , 0= Man)
    """
    gender_name= "Female" if gender==1 else "Male"
    optimal_value = dict.fromkeys(VitaminNameData.vitamin_name, 0)
    for vit in VitaminNameData.vitamin_name:
        if vit == "Sodium":
            optimal_value["Sodium"] = 2300
            continue
        else:
            if vit == "Caffeine":
                if age > 18:
                    optimal_value["Caffeine"] = 400
                else:
                    optimal_value["Caffeine"] = 0
                continue
        optimal_value[vit] = get_amount_vitamin(
            age, gender_name, getattr(OptimalData, vit))
    return optimal_value
