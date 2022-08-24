import json
import bcrypt
from consts import REGEX_FIND_GR,REGEX_FIND_FLOAT
from errors import UserPassValidationError
from datetime import datetime, date

def is_empty(my_str: str) -> bool:
    """Check if string is empty, return True if it is ,otherwise False"""
    if not my_str.strip():
        return True
    return False


def calculate_age(born: datetime) -> int:
    """Given a date (DD/MM/YYYY) return an age"""
    born_datetime = born.date()
    today = date.today()
    year_gep = today.year - born_datetime.year
    return year_gep - ((today.month, today.day) < (born_datetime.month, born_datetime.day))


def to_dict(obj: object) -> json:
    """Return a json object from object"""
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def verify_password(password: str, collection_password: str):
    """Check if password is the same as user_doc's password"""
    password_encoded = password.encode('utf-8')
    # verify the password with the collection
    if not bcrypt.checkpw(password_encoded, collection_password):
        raise UserPassValidationError()


def make_password_hashed(password: str) -> str:
    """Return an hashed password from password"""
    password_encoded = password.encode('utf-8')
    password_hashed = bcrypt.hashpw(password_encoded, bcrypt.gensalt())
    return password_hashed


def convert_datetime(birthday: str) -> datetime:
    """Convert birthday to datetime format"""
    return datetime.strptime(birthday,  '%d/%m/%Y')


def get_ratio(serving: str) -> float:
    """Get the serving in gram from the serving str and calculate the ratio from 100"""
    
    serving_in_grams= REGEX_FIND_GR.findall(serving)
    serving_in_grams_num=float(REGEX_FIND_FLOAT.findall(serving_in_grams[0])[0]) # get serving in grams (example: 1 cup is x gram)

    return serving_in_grams_num/100

