class VitaminName:
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
