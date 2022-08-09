import json
from datetime import datetime, date
import bcrypt
import error


def is_empty(my_str: str) -> bool:
    """check if string is empty, return True if it is ,otherwise False"""
    if not my_str.strip():
        return True
    return False


def calculate_age(born: datetime) -> int:
    """given a date (DD/MM/YYYY) return an age"""
    born_datetime = born.date()
    today = date.today()
    year_gep = today.year - born_datetime.year
    return year_gep - ((today.month, today.day) < (born_datetime.month, born_datetime.day))


def to_dict(obj: object) -> json:
    """return a json object from object"""
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def verfiay_password(password: str, db_password: str):
    """check if password is the same as user_doc's password"""

    encoded_password = password.encode('utf-8')
    # verify the password with the collection
    if not bcrypt.checkpw(encoded_password, db_password):
        raise error.ValidationError()


def make_hashed_password(new_password: str) -> str:
    encoded_password = new_password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


def convert_datetime(birthday: str) -> datetime:
    return datetime.strptime(birthday,  '%d/%m/%Y')
