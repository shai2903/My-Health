import json
import requests
from consts import key_from_USDA
from errors import USDAConnectionError
from vitamin_data.optimal_values import OptimalData
from vitamin_data.vitamin_names import VitaminName
from requests.auth import HTTPBasicAuth

def get_all_options_USDA(food_name: str) -> list:
    """ Get all the food option from searching food_name in USDA.
        Args:
           food_name - the food name we search
    """

    json_result = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key_from_USDA}&query={food_name}&dataType=SR Legacy', auth=HTTPBasicAuth('mars_test_343343', None))

    try:
        res_foods=json_result.json()["foods"]
    except KeyError:
        raise USDAConnectionError
    return res_foods


def get_serving_option(food_id: str) -> list:
    """Get all the serving option from searching food_id in USDA.
        Args:
           food_id - the food id we search
    """
    api_response = json.loads(requests.get(
        f'https://api.nal.usda.gov/fdc/v1/food/{food_id}?api_key={key_from_USDA}', auth=HTTPBasicAuth('mars_test_343343', None)).text)
    
    try:
        api_serving = api_response['foodPortions']
    except KeyError:
        raise USDAConnectionError

    serving_options = []

    for serving_info in api_serving:
        if 'modifier' in serving_info and 'gramWeight' in serving_info:
            serving = serving_info['modifier']
            serving_in_gram = str(serving_info['gramWeight'])
            serving_options.append(f"{serving} ({serving_in_gram} gr)")

    return serving_options


def get_food_nutrient(food_id: str) -> dict:
    """Get all food nutrient from searching food_id in USDA.
        Args:
           food_id - the food id we search
    """
    vitamins_nutrient = dict.fromkeys(VitaminName.vitamin_name, 0)
    api_response = json.loads(requests.get(
        f'https://api.nal.usda.gov/fdc/v1/food/{food_id}?api_key={key_from_USDA}', auth=HTTPBasicAuth('mars_test_343343', None)).text)

    try:
        api_nutrients = api_response['foodNutrients']
    except KeyError:
        raise USDAConnectionError
        
    for nutrients in api_nutrients:
        if 'nutrient' in nutrients and 'name' in nutrients['nutrient']:
            index = is_in_selected_vitamins(
                nutrients['nutrient']['name'].lower())
            if index >= 0 and 'amount' in nutrients:
                official_name = VitaminName.vitamin_name[index]
                vitamins_nutrient[official_name] += round(
                    float(nutrients['amount']), 2)

    return vitamins_nutrient


def is_in_selected_vitamins(vitamin_name: str) -> int:
    """Check if vitamin_name in vitamin_name_united and return it's index,
    if vitamin isn't in vitamin_name_united return -1.
    Args:
        vitamin_name - the vitamin name we search in vitamin_name_united
    """
    index = 0
    for vitamins in VitaminName.vitamin_name_united:
        if isinstance(vitamins, tuple):
            for sub_vitamin in vitamins:
                if sub_vitamin.lower() == vitamin_name:
                    return index
        elif vitamin_name == vitamins.lower():
            return index
        index += 1

    return -1


def get_amount_vitamin(age: float, gender: bool, df_vitamin) -> str:
    """Get the optimal value according to age and gender from df_vitamins.
    Args:
        age - the age of user
        gender - the gender of user (1= Female , 0= Man)
        df_vitamin - dataFrame with the optimal intake of vitamin (for all age and gender)
    """
    return (df_vitamin[df_vitamin.loc[:, 'Age'] > age].head(1).loc[:, gender]).values[0]


def get_amount(age: float, gender: bool) -> dict:
    """Get the optimal value according to age and gender for each vitamin.
    Args:
        age - the age of user
        gender - the gender of user(1= Female , 0= Man)
    """
    gender_name = "Female" if gender == 1 else "Male"
    optimal_value = dict.fromkeys(VitaminName.vitamin_name, 0)
    for vit in VitaminName.vitamin_name:
        if vit == "Sodium":
            optimal_value["Sodium"] = '2300'
            continue
        elif vit == "Caffeine":
            if age > 18:
                optimal_value["Caffeine"] = '400'
            else:
                optimal_value["Caffeine"] = '0'
            continue
        optimal_value[vit] = get_amount_vitamin(
            age, gender_name, getattr(OptimalData, vit))
    return optimal_value
