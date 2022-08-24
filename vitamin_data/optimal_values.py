import pandas as pd
import os


class OptimalData:
    """Class contain dataframe for each vitamin with optimal intake values
    (according to age and gender)"""
    #path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    path_optimal=os.path.abspath(os.path.join(os.path.dirname(__file__),'optimal_values_USDA.xlsx'))
   
    Vitamin_A = pd.read_excel(
        path_optimal, sheet_name='vitamin_A')
    Vitamin_C = pd.read_excel(
        path_optimal, sheet_name='vitamin_C')
    Vitamin_D = pd.read_excel(
        path_optimal, sheet_name='vitamin_D')
    Vitamin_B6 = pd.read_excel(
        path_optimal, sheet_name='vitamin_B6')
    Vitamin_E = pd.read_excel(
        path_optimal, sheet_name='vitamin_E')
    Vitamin_K = pd.read_excel(
        path_optimal, sheet_name='vitamin_K')
    Thiamin = pd.read_excel(
        path_optimal, sheet_name='Thiamin')
    Vitamin_B12 = pd.read_excel(
        path_optimal, sheet_name='vitamin_B12')
    Riboflavin = pd.read_excel(
        path_optimal, sheet_name='Riboflavin')
    Folate = pd.read_excel(
        path_optimal, sheet_name='Folate')
    Choline = pd.read_excel(
        path_optimal, sheet_name='Choline')
    Pantothenic_acid = pd.read_excel(
        path_optimal, sheet_name='pantothenic')
    Niacin = pd.read_excel(
        path_optimal, sheet_name='Niacin')
    Iron = pd.read_excel(
        path_optimal, sheet_name='Iron')
    Zinc = pd.read_excel(
        path_optimal, sheet_name='Zink')
    Folid_acid = pd.read_excel(
        path_optimal, sheet_name='Folic_acid')
    Selenium = pd.read_excel(
        path_optimal, sheet_name='Selenium')
    Calcium = pd.read_excel(
        path_optimal, sheet_name='Calcium')
    Copper = pd.read_excel(
        path_optimal, sheet_name='Copper')
    Manganese = pd.read_excel(
        path_optimal, sheet_name='Manganese')
    Magnesium = pd.read_excel(
        path_optimal, sheet_name='magnesium')
    Phosphorus = pd.read_excel(
        path_optimal, sheet_name='Phosphorus')
    Potassium = pd.read_excel(
        path_optimal, sheet_name='Potassium')
