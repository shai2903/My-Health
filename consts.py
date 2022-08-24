from enum import Enum
import re


class SuperEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Meals(SuperEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACKS = "snacks"

    def cap(self):
        return self.value.capitalize()




# Email
SMTP_SERVER = ""
SENDER_PASSWORD = ""
SENDER_MAIL = ""

# Colors
GREEN_PIE = '#5cb85c'
BLUE_PIE = '#5bc0de'
ORANGE_PIE = "#f0ad4e"
RED_PIE = "#d9534f"
RED_PERCENTAGE = '#f55142'
GREEN_PERCENTAGE = "#42f5b6"
DARK_BLUE_STYLE = '#2B3E50'


# Regex
REGEX_FIND_GR = re.compile("\(\d*\.\d*\s[g][gr]\)")
REGEX_FIND_FLOAT = re.compile("\d+\.\d+|\d+|\d*\,\d+|\d*\,\d*\.\d+|\d*\.\d+")

# Errors
# Username and password errors
ERROR_EMPTY_USERPASS = "Enter username and password"
ERROR_EMPTY_PASS_REPEATED = "Enter password and Repeated password"
ERROR_EMPTY_PASS = "Enter password"
ERROR_EMPTY_USER = "Enter username"
ERROR_WRONG_OLD_PASS = "Wrong old password"
ERROR_WRONG_PASS = "Wrong password"
ERROR_MATCH_PASS = "Repeated password doesn't match password"
ERROR_SAME_USER = "That your username"
ERROR_USED_USER = "Username already exist"
ERROR_USER_NOT_FOUND = "Username doesn't exist"

# Mail errors
ERROR_SAME_MAIL = "That your mail"
ERROR_USED_MAIL = "Mail already exist"
ERROR_WRONG_MAIL = "Is it you'r mail?"
ERROR_VALID_MAIL = "Enter valid mail"
ERROR_SEND_MAIL = "Couldn't send mail"

# Gender error
ERROR_EMPTY_GENDER = "Enter gender"

# Birthday error
ERROR_VALID_BIRTHDAY = "Enter valid birthday"

# Diet errors
ERROR_EMPTY_DIET = "Enter diet name"
ERROR_UNIQUE_DIET = "Enter unique diet name"


# Notes to user
PASSWORD_SENT = "New password sent to your mail"

# USDA KEY
key_from_USDA = "Idd4pw784uoM2XfIhNmIyxsfwKv6xLdUBnIUz99m"
