from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath('../diet proj'))
import helper
import handler_collection
import error



def check_empty_fields(username: str, password: str):
    """check the fields the user filled aren't empty
    Args:
            username - the username the user enter
            password - the password the user enter
    """
    if helper.is_empty(username) or helper.is_empty(password):
        raise error.ValidationError("Please enter username and password")


def check_gender(gender: str):
    """check if the user enter a valid gender
    Args:
        gender - the gender the user enter
    """
    if helper.is_empty(gender):
        raise error.ValidationError("Enter gender")


def check_birthday(birthday: str):
    """check if the user enter a valid birthday
    Args:
        birthday - the birthday the user enter
    """
    try:
        date = datetime.strptime(birthday,  '%d/%m/%Y')
    except ValueError as exc:
        raise error.ValidationError("Enter valid birthday") from exc

    if date.year < 1920:
        raise error.ValidationError("Enter valid birthday")


def check_mail(mail: str):
    """check if the user enter a valid mail
    Args:
        mail - the mail the user enter
    """
    if handler_collection.is_mail_exists(mail):
        raise error.ValidationError("Mail already exist")
    if mail.find('@') == -1:
        raise error.ValidationError("Enter valid mail")


def check_username(username: str):
    """check if the user enter a valid username
    Args:
        username - the username the user enter
    """
    #username is empty
    if helper.is_empty(username):
        raise error.ValidationError("Enter username")

    if handler_collection.is_username_exists(username):
        raise error.ValidationError("Username already exist")


def check_mail_user(username: str, mail: str):
    """ check if the mail match the username's mail"""
    if handler_collection.get_mail(username) != mail:
        raise error.ValidationError("invalid email")


def check_changed_username(username_new: str, username_user: str):
    """check that username_new is valid"""
    if username_new == username_user:
        raise error.ValidationError("That your username")
    if handler_collection.is_username_exists(username_new):
        raise error.ValidationError("Username already exist")


def check_changed_mail(mail_new: str, mail_user: str):
    """check that mail_new is valid and unique"""
    try:
        check_mail(mail_new)
    except error.ValidationError as exception:
        raise error.ValidationError(str(exception))
    if mail_new == mail_user:
        raise error.ValidationError("That your mail")
    if handler_collection.is_mail_exists(mail_new):
        raise error.ValidationError("Mail already exist")


def check_password(password: str, password_repeat: str):
    """check if the user enter a valid password
    Args:
        password - the password the user enter
        password_repeat - the password_repeat the user enter
    """
    if helper.is_empty(password) or helper.is_empty(password_repeat):
        raise error.ValidationError("Enter password or Repeated password")

    if password != password_repeat:
        raise error.ValidationError("Repeated password doesn't match password")


def check_changed_password(password_new: str, password_old: str, password_repeat: str, password_real: str):
    """check that the passwords the user enter are valid"""
    if helper.is_empty(password_old) or helper.is_empty(password_new) or helper.is_empty(password_repeat):
        raise error.ValidationError("Please enter password")

    try:
        helper.verify_password(password_old, password_real)
    except  ValueError as exc:
        raise error.ValidationError("Wrong old password") from exc

    if password_new != password_repeat:
        raise error.ValidationError("Repeated password doesn't match password")


def check_diet_name(diet_name: str, all_diets_names: list):
    """check the diet name is valid and unique"""
    if helper.is_empty(diet_name):
        raise error.ValidationError("Enter a diet name")

    if diet_name in all_diets_names:
        raise error.ValidationError("Enter unique diet name")
