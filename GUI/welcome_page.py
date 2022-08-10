from __future__ import annotations
import tkinter as tk
import tkinter.ttk as ttk
import ttkbootstrap
import check_fields as check_fields
import error
import handle_db
from user import User
import start_app
import helper
import mail_handler


class WelcomePage(tk.Frame):
    """ WelcomePage class, create the welcome page with login and signup options for user to 
    enter their account or sign up.

    Attributes:
        parent_frame - the parent frame of this app
        controller - the start_app object of this GUI
    """

    def __init__(self, parent_frame: tk.Frame, controller: start_app):
        tk.Frame.__init__(self, parent_frame)

        self.parent_frame = parent_frame
        self.controller = controller

        padding_left_frame = ttk.Frame(self, width=50, height=200)
        padding_left_frame.grid(row=0, column=0)
        ttk.Label(self, text="Welcome", style="Welcome.TLabel").grid(
            row=0, column=2, pady=5)

        # create the login frame and the sign-up frame
        self.create_login_frame()
        self.create_signup_frame()
        self.create_forgot_password_frame()

    def create_forgot_password_frame(self):
        """create the forgor password frame"""

        self.forgot_password_frame = ttk.Labelframe(self, width=300)
        self.forgot_password_frame.grid(row=1, column=1, padx=10, sticky='s')
        ttk.Label(self.forgot_password_frame, text="Forgot password", style="login.TLabel").grid(
            row=1, column=1)

        ttk.Label(self.forgot_password_frame, text="Username : ").grid(
            row=2, column=1, padx=5)
        username_entry = ttk.Entry(self.forgot_password_frame, width=30)
        username_entry.grid(row=2, column=2, padx=15, pady=5)

        ttk.Label(self.forgot_password_frame, text="Mail : ").grid(
            row=3, column=1, padx=5)
        mail_entry = ttk.Entry(self.forgot_password_frame, width=30)
        mail_entry.grid(row=3, column=2, padx=15, pady=5)

        error_label = ttk.Label(
            self.forgot_password_frame, text="", style="error.login.TLabel")
        error_label.grid(row=4, column=2, padx=5)

        ttk.Button(self.forgot_password_frame, command=lambda: self.send_reset_password(
            mail_entry.get(), username_entry.get(), error_label), text="Ok").grid(row=4, column=1, pady=10)

    def send_reset_password(self, mail: str, username: str, label: tk.Label):
        """create the frame of 'forgot password'"""
        if not handle_db.is_username_exists(username):
            label['text'] = "Username doesn't exist"
            return

        try:
            check_fields.check_mail_user(username, mail)
        except error.ValidationError as exception:

            label['text'] = str(exception)
            return

        try:
            password = mail_handler.send_mail_reset(mail, username)
            hashed_new_password = helper.make_hashed_password(password)
            handle_db.update_password(
                handle_db.get_user(username), hashed_new_password)

        except Exception as exception:
            label['text'] = "couldn't send mail"
            return

        label['text'] = "New password sent to your mail"

    def create_login_frame(self):
        """create the login frame"""

        self.login_frame = ttk.Labelframe(self, width=300)
        self.login_frame.grid(row=1, column=1, padx=10, sticky='n')

        ttk.Label(self.login_frame, text="Login", style="login.TLabel").grid(
            row=1, column=1, pady=5)

        ttk.Label(self.login_frame, text="User name : ").grid(
            row=2, column=1, padx=5)
        login_username_entry = ttk.Entry(self.login_frame, width=20)
        login_username_entry.grid(row=2, column=2, padx=15, pady=5)

        ttk.Label(self.login_frame, text="Password : ").grid(row=3, column=1)
        login_password_entry = ttk.Entry(self.login_frame, width=20, show="*")
        login_password_entry.grid(row=3, column=2, padx=15)

        ttk.Button(self.login_frame, text="Ok", command=lambda: self.from_login_to_tab_creator(
            login_username_entry.get(), login_password_entry.get())).grid(row=4, column=2, pady=10)

    def from_login_to_tab_creator(self, username: str, password: str):
        """show the user's app if the username and password are valid
        Args:
            username - the username the user enter
            password - the password the user enter
        """
        try:
            check_fields.check_empty_fields(username, password)
            self.user = handle_db.search_user_collection(username, password)

        except error.ValidationError as exception:
            self.label_error(self.login_frame, 5, 2, str(exception))
            return

        # if user exists show tab_creator
        self.show_tab_creator()

    def create_signup_frame(self):
        """create the signup frame"""
        self.signup_frame = ttk.Labelframe(self, width=300, height=200)
        self.signup_frame.grid(row=1, column=3)
        ttk.Label(self.signup_frame, text="Sign up ").grid(
            row=1, column=3, pady=20)

        ttk.Label(self.signup_frame, text="User name :").grid(row=2, column=3)
        signup_username_entry = ttk.Entry(self.signup_frame, width=20)
        signup_username_entry.grid(row=2, column=4, padx=15, pady=5)

        ttk.Label(self.signup_frame, text="Password : ").grid(row=3, column=3)
        signup_pass_entry = ttk.Entry(self.signup_frame, width=20, show="*")
        signup_pass_entry.grid(row=3, column=4, padx=15, pady=5)

        ttk.Label(self.signup_frame, text="Repeat password :").grid(
            row=4, column=3)
        signup_rep_password_entry = ttk.Entry(
            self.signup_frame, width=20, show="*")
        signup_rep_password_entry.grid(row=4, column=4, padx=15, pady=5)

        ttk.Label(self.signup_frame, text="Mail :").grid(row=5, column=3)
        signup_mail_entry = ttk.Entry(self.signup_frame, width=30)
        signup_mail_entry.grid(row=5, column=4, padx=15, pady=5)

        ttk.Label(self.signup_frame, text="Birthday :").grid(row=6, column=3)
        signup_date_entry = ttkbootstrap.DateEntry(self.signup_frame, width=20)
        signup_date_entry.grid(row=6, column=4, padx=15, pady=5)

        ttk.Label(self.signup_frame, text="Gender :").grid(row=7, column=3)
        n = tk.StringVar()
        gender_combobox = ttk.Combobox(self.signup_frame, width=10,
                                       textvariable=n)
        gender_combobox['values'] = ('Female', 'Male',)
        gender_combobox.grid(row=7, column=4)

        ttk.Button(self.signup_frame, text="Ok", command=lambda: self.from_signup_to_tab_creator(signup_username_entry.get(), signup_pass_entry.get(
        ), signup_rep_password_entry.get(), signup_mail_entry.get(), signup_date_entry.entry.get(), gender_combobox.get())).grid(row=8, column=4, pady=25)

    def from_signup_to_tab_creator(self, username: str, password: str, rep_password: str, mail: str, birthday: str, gender: str):
        """from signup to tab_creator, adding the new user data to collection and create a local user
        Args:
            username - the username the user enter
            password - the password the user enter
            repeat_password -  the repeat password the user enter
            mail - the mail the user enter
            birthday - the birthday the user enter
            gender - the gender the user enter
        """
        try:
            self.validation_details_signup(
                username, password, rep_password, mail, gender, birthday)
        except error.ValidationError as exception:
            self.label_error(self.signup_frame, 9, 4, str(exception))
            return

        gender_bool = 1 if gender == "Female" else 0
        hashed_password = helper.make_hashed_password(password)
        birthday_datetime = helper.convert_datetime(birthday)
        self.user = User(username, mail, hashed_password,
                         gender_bool, birthday_datetime)
        handle_db.add_to_DB(self.user)
        self.show_tab_creator()

    def validation_details_signup(self, username: str, password: str, repeat_password: str, mail: str, gender: str, birthday: str):
        """validation all the fields the user enter
        Args:
            username - the username the user enter
            password - the password the user enter
            repeat_password - repeat_password username the user enter
            mail - the mail the user enter
            gender - the gender the user enter
            birthday - the birthday the user enter
        """
        try:
            check_fields.check_username(username)
            check_fields.check_password(password, repeat_password)
            check_fields.check_mail(mail)
            check_fields.check_birthday(birthday)
            check_fields.check_gender(gender)

        except error.ValidationError as exception:
            raise error.ValidationError(str(exception))

    def label_error(self, frame: tk.Frame, row: int, column: int, error_str: str):
        """ make a label for the error in login\signup
        Args:
            frame - the frame of the label
            row - row of the label
            column - column of the label
            error_str - the text for the error label
        """
        ttk.Label(frame, text=error_str,
                  style="error.login.TLabel").grid(row=row, column=column, sticky="ew")

    def show_tab_creator(self):
        """show the TabCreator frame"""
        self.controller.switch_frames(self.parent_frame, "TabCreator", self)
