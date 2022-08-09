from pymongo import MongoClient
from diet import Diet
import helper 
from user import User
import bson 
import error


connection = MongoClient()
collection = connection.Main_Database.Users


def search_user_collection(username: str, password: str) -> User:
    """search the user in collection to check it's an existing user, if exist import to self.user
    Args:
        username - the username the user enter
        password - the password the user enter
    """
    user_doc = collection.find_one({"user": username})
    if not user_doc : #user doesn't exist
        raise error.ValidationError("Username doesn't exist")
    
    try:
        helper.verfiay_password(password, user_doc["password"])
    except error.ValidationError:
        raise error.ValidationError("Wrong password")

    user = User(user_doc["user"], user_doc["mail"], user_doc["password"],
                        user_doc["gender"], user_doc["birthday"], user_doc["num_of_diets"])
    user.set_diets_json(user_doc["diets"])

    return user

def add_to_DB(user: User):
    """add the user data to collection"""
    item = {
        "_id": bson.objectid.ObjectId(),
        "user": user.username,
        "mail": user.mail,
        "password": user.password,
        "gender": user.gender,
        "birthday": user.birthday,
        "diets": {},
        "num_of_diets": user.num_of_diets
    }
    collection.insert_many([item])

def is_username_exists(username: str) -> bool:
    """check if username exists in collection, return True if it is ,otherwise False"""
    my_doc = collection.find_one({"user": username})

    # username already exist
    if my_doc:
        return True
    return False

    
def get_user(username: str):
    """return user from collection"""
    return collection.find_one({"user": username})

def delete_from_db(user_collection: dict,diet_name: str):
    """delete diet from collection"""
    collection.update_many({"_id": user_collection["_id"]}, {
                               "$unset": {"diets."+diet_name: ""}})
    collection.update_many({"_id": user_collection["_id"]}, {
                               "$inc": {"num_of_diets": -1}})

def update_username(user_collection: dict,new_username: str):
    """update username in collection"""
    collection.update_many({"_id": user_collection["_id"]}, {
                               "$set": {"user": new_username}})                         

def update_password(user_collection: dict,new_password: str):
    """update password in collection"""
    collection.update_many({"_id": user_collection["_id"]}, {
                               "$set": {"password": new_password}}) 


def update_diets(user_collection: dict,diet_name: str,is_edit: bool,current_diet: Diet):
    """add diet to saved diets in collection (in edit mode we don't increase the counter of diets 
    because we changed an existing diet"""
    print("hey 2")
    print(current_diet.vitamins)
    json_diet = helper.to_dict(current_diet)
    print(current_diet.vitamins)
    print(json_diet)
    collection.update_many({"_id": user_collection["_id"]}, {
                              "$set": {"diets."+diet_name: json_diet}})
    
    if not is_edit:
        collection.update_many({"_id": user_collection["_id"]}, {

                                   "$inc": {"num_of_diets": 1}})