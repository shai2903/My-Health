from __future__ import annotations
import tkinter.ttk as ttk
import check_fields
from errors import MailValidationError, UserPassValidationError
from current_user import CurrentUser


class PersonalTab():
    """Class creating the change-personal information tab
    Attributes:
        current_user - the current user object
    """

    def __init__(self, current_user: CurrentUser):
        self.current_user = current_user

    def create_personal_tab(self, edit_personal_data_frame: ttk.Frame):
        """Create the change personal data frame
        Args:
            edit_personal_data_frame - the frame of the edit personal data tab
        """
        edit_personal_data_frame.grid_propagate(False)

        personal_change_frame = ttk.Labelframe(edit_personal_data_frame)
        personal_change_frame.grid(ipady=10, ipadx=10, sticky='ew')
        ttk.Label(personal_change_frame, text="Edit Your Profile").grid(
            row=1, column=1, pady=10, padx=30)

        mail_change_frame = ttk.Labelframe(edit_personal_data_frame)
        mail_change_frame.grid(row=2, ipady=10, ipadx=10, sticky='ew')
        ttk.Label(mail_change_frame, text="New mail :").grid(
            row=2, column=1, pady=10)
        mail_entry = ttk.Entry(mail_change_frame, width=30)
        mail_entry.grid(row=2, column=2)
        ttk.Button(mail_change_frame, text="Ok", command=lambda: self.change_mail(mail_change_frame,
                                                                                  mail_entry.get())).grid(row=3, column=2, pady=10)

        password_change_frame = ttk.Labelframe(edit_personal_data_frame)
        password_change_frame.grid(row=3, ipady=10, ipadx=10, sticky='ew')
        ttk.Label(password_change_frame, text="Old Password :").grid(
            row=3, column=1, pady=10)
        old_password_entry = ttk.Entry(
            password_change_frame, width=15, show="*")
        old_password_entry.grid(row=3, column=2)
        ttk.Label(password_change_frame, text="New Password :").grid(
            row=4, column=1, pady=10)
        new_password_entry = ttk.Entry(
            password_change_frame, width=15, show="*")
        new_password_entry.grid(row=4, column=2)
        ttk.Label(password_change_frame, text="Repeat New Password :").grid(
            row=5, column=1, pady=10)
        new_repeat_password_entry = ttk.Entry(
            password_change_frame, width=15, show="*")
        new_repeat_password_entry.grid(row=5, column=2)
        ttk.Button(password_change_frame, text="Ok", command=lambda: self.change_password(old_password_entry.get(
        ), new_password_entry.get(), new_repeat_password_entry.get(), password_change_frame)).grid(row=7, column=2, pady=10)

    def change_password(self, password_old: str, password_new: str, password_repeat: str, password_change_frame: ttk.Frame):
        """Change the old password to a new one, but first check:
            1. a valid new and old password
            2. the old password is the same as the user password
            3. repeated password is the same as new password
        Args:
            password_old -  the old password the user enter
            password_new - the new password the user want
            password_repeat - the user repeat the new password fo verification
            password_change_frame - current frame
        """

        try:
            check_fields.check_changed_password(
                password_new, password_old, password_repeat, self.current_user.get_password())
        except UserPassValidationError as exception:
            self.label_change(password_change_frame, str(exception))
            return

        self.current_user.update_password(password_new)
        self.label_change(password_change_frame, "Password changed")

    def change_mail(self, mail_frame: ttk.Frame, mail_new: str):
        """Change the mail
        Args:
            mail_new - the new mail the user want
            mail_frame - current frame"""

        # check if mail already exist for other user
        try:
            check_fields.check_changed_mail(
                mail_new, self.current_user.get_mail())
        except MailValidationError as exception:
            self.label_change(mail_frame, str(exception))
            return

        self.current_user.update_mail(mail_new)
        self.label_change(mail_frame, "Mail changed")

    def label_change(self, frame: ttk.Frame, label_txt: str):
        """Change the note label (mail notes or password notes)"""
        ttk.Label(frame, text=label_txt,
                  style="error.login.TLabel").grid(row=9, column=2, sticky="ew")
