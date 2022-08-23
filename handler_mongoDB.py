from pymongo import MongoClient
import bson
import helper
import error_validate
import consts
from user import User
from diet import Diet

connection = MongoClient()
collection = connection.Main_Database.Users


def search_user_collection(username: str, password: str) -> User:
    """Search the user in collection to check it's an existing user, if exist import to self.user
    Args:
        username - the username the user enter
        password - the password the user enter
    """
    user_doc = collection.find_one({"user": username})
    if not user_doc:  # user doesn't exist
        raise error_validate.UserPassValidationError(consts.ERROR_USER_NOT_FOUND)

    try:
        helper.verify_password(password, user_doc["password"])
    except error_validate.UserPassValidationError as exc:
        exc.str=consts.ERROR_WRONG_PASS
        raise exc

    user = User(user_doc["user"], user_doc["mail"], user_doc["password"],
                user_doc["gender"], user_doc["birthday"], user_doc["num_of_diets"])
    user.set_diets_json(user_doc["diets"])

    return user


def add_to_collection(user: User):
    """Add the user data to collection"""
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
    """Check if username exists in collection, return True if it is ,otherwise False"""
    user_doc = collection.find_one({"user": username})

    # username already exist
    if user_doc:
        return True
    return False


def is_mail_exists(mail: str) -> bool:
    """Check if mail exists in collection, return True if it is ,otherwise False"""
    user_doc = collection.find_one({"mail": mail})

    # mail already exist
    if user_doc:
        return True
    return False


def get_user(username: str):
    """Return user from collection"""
    return collection.find_one({"user": username})


def get_mail(username: str):
    """Return username's mail from collection"""
    user_doc = collection.find_one({"user": username})
    return user_doc["mail"]


def delete_from_collection(user_collection: dict, diet_name: str):
    """Delete diet from collection"""
    collection.update_many({"_id": user_collection["_id"]}, {
        "$unset": {"diets."+diet_name: ""}})
    collection.update_many({"_id": user_collection["_id"]}, {
        "$inc": {"num_of_diets": -1}})


def update_username(user_collection: dict, username_new: str):
    """Update username in collection"""
    collection.update_many({"_id": user_collection["_id"]}, {
        "$set": {"user": username_new}})


def update_password(user_collection: dict, password_new: str):
    """Update password in collection"""
    collection.update_many({"_id": user_collection["_id"]}, {
        "$set": {"password": password_new}})


def update_mail(user_collection: dict, mail_new: str):
    """Update mail in collection"""
    collection.update_many({"_id": user_collection["_id"]}, {
        "$set": {"mail": mail_new}})


def update_diets(user_collection: dict, diet_name: str, is_edit: bool, current_diet: Diet):
    """Add diet to saved diets in collection (in edit mode we don't increase the counter of diets 
    because we changed an existing diet"""

    json_diet = helper.to_dict(current_diet)

    collection.update_many({"_id": user_collection["_id"]}, {
        "$set": {"diets."+diet_name: json_diet}})

    if not is_edit:
        collection.update_many({"_id": user_collection["_id"]}, {

            "$inc": {"num_of_diets": 1}})
