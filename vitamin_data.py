import sys
import os
import pandas as pd
sys.path.append(os.path.abspath('../diet proj'))


class OptimalData:
    """Class contain dataframe for each vitamin with optimal intake values
    (according to age and gender)"""
    Vitamin_A = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='vitamin_A')
    Vitamin_C = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='vitamin_C')
    Vitamin_D = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='vitamin_D')
    Vitamin_B6 = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='vitamin_B6')
    Vitamin_E = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='vitamin_E')
    Vitamin_K = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='vitamin_K')
    Thiamin = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Thiamin')
    Vitamin_B12 = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='vitamin_B12')
    Riboflavin = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Riboflavin')
    Folate = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Folate')
    Choline = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Choline')
    Pantothenic_acid = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='pantothenic')
    Niacin = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Niacin')
    Iron = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Iron')
    Zinc = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Zink')
    Folid_acid = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Folic_acid')
    Selenium = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Selenium')
    Calcium = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Calcium')
    Copper = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Copper')
    Manganese = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Manganese')
    Magnesium = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='magnesium')
    Phosphorus = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Phosphorus')
    Potassium = pd.read_excel(
        'additional_files/Data_vitamin.xlsx', sheet_name='Potassium')


class VitaminNameData:
    """set of the correct name of vitamins
    vitamin_name_united - since some vitamin have more than one name we keep a set with all the possible names
    vitamin_name - the vitamin name as we used it in this app
    """

    vitamin_name_united = ('Iron, Fe', 'Zinc, Zn', 'Vitamin C, total ascorbic acid', 'Folate, total', ('Vitamin B-12', 'Vitamin B-12, added'), 'Vitamin A, RAE',
                           ('Vitamin E (alpha-tocopherol)', 'Vitamin E, added'),('Vitamin K (Dihydrophylloquinone)', 'Vitamin K (phylloquinone)'),
                           'Vitamin D (D2 + D3), International Units', 'Niacin', 'Vitamin B-6', 'Pantothenic acid', 'Choline, total', 'Riboflavin', 'Thiamin',
                           'Selenium, Se', 'Calcium, Ca', 'Sodium, Na', 'Copper, Cu', 'Manganese, Mn',
                           'Magnesium, Mg', 'Phosphorus, P', 'Potassium, K', 'Caffeine')
    
    units={"Iron":"mg","Zinc":"mg","Vitamin_C":"mg","Folid_acid":"mcg","Vitamin_B12":"mcg","Vitamin_A":"mcg RAE","Vitamin_E":"mg",
        "Vitamin_K":"mcg","Vitamin_D":"IU","Niacin":"mg","Vitamin_B6":"mg","Pantothenic_acid":"mg",
        "Choline":"mg","Riboflavin":"mg","Thiamin":"mg","Selenium":"mcg","Calcium":"mg","Sodium":"mg","Copper":"mg",
        "Manganese":"mg","Magnesium":"mg","Phosphorus":"mg","Potassium":"mg","Caffeine":"mg"}

    vitamin_name = ["Iron", "Zinc", "Vitamin_C", "Folid_acid", "Vitamin_B12", "Vitamin_A", "Vitamin_E", "Vitamin_K",
                    "Vitamin_D", "Niacin", "Vitamin_B6", "Pantothenic_acid", "Choline", "Riboflavin",
                    "Thiamin", "Selenium", "Calcium", "Sodium", "Copper", "Manganese", "Magnesium", "Phosphorus", "Potassium", "Caffeine"]
