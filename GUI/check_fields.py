import sys
import os
sys.path.append(os.path.abspath('../diet proj'))
from datetime import datetime
import helper
import handle_db
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
    except ValueError:
        raise error.ValidationError("Enter valid birthday")

    if date.year < 1920:
        raise error.ValidationError("Enter valid birthday")


def check_mail(mail: str):
    """check if the user enter a valid mail
    Args:
        mail - the mail the user enter
    """
    if handle_db.is_mail_exists(mail):
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

    if handle_db.is_username_exists(username):
        raise error.ValidationError("Username already exist")


def check_mail_user(username: str, mail: str):
    """ check if the mail match the username's mail"""
    if handle_db.get_mail(username) != mail:
        raise error.ValidationError("invalid email")


def check_changed_username(new_username: str, username_user: str):
    """check that new_username is valid"""
    if new_username == username_user:
        raise error.ValidationError("That your username")
    if handle_db.is_username_exists(new_username):
        raise error.ValidationError("Username already exist")


def check_changed_mail(new_mail: str, mail_user: str):
    """check that new_mail is valid and unique"""
    try:
        check_mail(new_mail)
    except error.ValidationError as exception:
        raise error.ValidationError(str(exception))
    if new_mail == mail_user:
        raise error.ValidationError("That your mail")
    if handle_db.is_mail_exists(new_mail):
        raise error.ValidationError("Mail already exist")


def check_password(password: str, repeat_password: str):
    """check if the user enter a valid password
    Args:
        password - the password the user enter
        repeat_password - the repeat_password the user enter
    """
    if helper.is_empty(password) or helper.is_empty(repeat_password):
        raise error.ValidationError("Enter password or Repeated password")

    if password != repeat_password:
        raise error.ValidationError("Repeated password doesn't match password")


def check_changed_password(new_password: str, old_password: str, repeat_password: str, real_password: str):
    """check that the passwords the user enter are valid"""
    if helper.is_empty(old_password) or helper.is_empty(new_password) or helper.is_empty(repeat_password):
        raise error.ValidationError("Please enter password")

    try:
        helper.verify_password(old_password, real_password)
    except:
        raise error.ValidationError("Wrong old password")

    if new_password != repeat_password:
        raise error.ValidationError("Repeated password doesn't match password")


def check_diet_name(diet_name: str, all_diets_name: list):
    """check the diet name is valid and unique"""
    if helper.is_empty(diet_name):
        raise error.ValidationError("Enter a diet name")

    if diet_name in all_diets_name:
        raise error.ValidationError("Enter unique diet name")
