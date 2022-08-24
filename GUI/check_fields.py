from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import helper
from errors import GenderValidationError, BirthdayValidationError, MailValidationError, UserPassValidationError, DietValidationError
import consts
import handler_mongoDB

def check_empty_fields(username: str, password: str):
    """Check the fields the user filled aren't empty
    Args:
            username - the username the user enter
            password - the password the user enter
    """
    if helper.is_empty(username) or helper.is_empty(password):
        raise UserPassValidationError(consts.ERROR_EMPTY_USERPASS)


def check_gender(gender: str):
    """Check if the user enter a valid gender
    Args:
        gender - the gender the user enter
    """
    if helper.is_empty(gender):
        raise GenderValidationError(consts.ERROR_EMPTY_GENDER)


def check_birthday(birthday: str):
    """Check if the user enter a valid birthday
    Args:
        birthday - the birthday the user enter
    """
    try:
        date = datetime.strptime(birthday,  '%d/%m/%Y')
    except ValueError as exc:
        raise BirthdayValidationError(consts.ERROR_VALID_BIRTHDAY) from exc

    if date.year < 1920:
        raise BirthdayValidationError(consts.ERROR_VALID_BIRTHDAY)


def check_mail(mail: str):
    """Check if the user enter a valid mail
    Args:
        mail - the mail the user enter
    """
    if handler_mongoDB.is_mail_exists(mail):
        raise MailValidationError(consts.ERROR_USED_MAIL)

    # This is a proof-of-concept program do I don’t perform full email validation
    if mail.find('@') == -1:
        raise MailValidationError(consts.ERROR_VALID_MAIL)


def check_username(username: str):
    """Check if the user enter a valid username
    Args:
        username - the username the user enter
    """
    #username is empty
    if helper.is_empty(username):
        raise UserPassValidationError(consts.ERROR_EMPTY_USER)

    if handler_mongoDB.is_username_exists(username):
        raise UserPassValidationError(consts.ERROR_USED_USER)


def check_mail_user(username: str, mail: str):
    """Check if the mail match the username's mail"""
    if handler_mongoDB.get_mail(username) != mail:
        raise MailValidationError(consts.ERROR_WRONG_MAIL)


def check_changed_username(username_new: str, username_user: str):
    """Check that username_new is valid"""
    if username_new == username_user:
        raise UserPassValidationError(consts.ERROR_SAME_USER)
    if handler_mongoDB.is_username_exists(username_new):
        raise UserPassValidationError(consts.ERROR_USED_USER)


def check_changed_mail(mail_new: str, mail_user: str):
    """Check that mail_new is valid and unique"""
    try:
        check_mail(mail_new)
    except MailValidationError as exc:
        raise exc

    if mail_new == mail_user:
        raise MailValidationError(consts.ERROR_SAME_MAIL)
    if handler_mongoDB.is_mail_exists(mail_new):
        raise MailValidationError(consts.ERROR_USED_MAIL)


def check_password(password: str, password_repeat: str):
    """Check if the user enter a valid password
    Args:
        password - the password the user enter
        password_repeat - the password_repeat the user enter
    """
    if helper.is_empty(password) or helper.is_empty(password_repeat):
        raise UserPassValidationError(consts.ERROR_EMPTY_PASS)

    if password != password_repeat:
        raise UserPassValidationError(consts.ERROR_MATCH_PASS)


def check_changed_password(password_new: str, password_old: str, password_repeat: str, password_real: str):
    """Check that the passwords the user enter are valid"""
    if helper.is_empty(password_old) or helper.is_empty(password_new) or helper.is_empty(password_repeat):
        raise UserPassValidationError(consts.ERROR_EMPTY_PASS)

    try:
        helper.verify_password(password_old, password_real)
    except ValueError as exc:
        raise UserPassValidationError(consts.ERROR_WRONG_OLD_PASS) from exc

    if password_new != password_repeat:
        raise UserPassValidationError(consts.ERROR_MATCH_PASS)


def check_diet_name(diet_name: str, all_diets_names: list):
    """Check the diet name is valid and unique"""
    if helper.is_empty(diet_name):
        raise DietValidationError(consts.ERROR_EMPTY_DIET)

    if diet_name in all_diets_names:
        raise DietValidationError(consts.ERROR_UNIQUE_DIET)
