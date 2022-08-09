from __future__ import annotations
import tkinter.ttk as ttk
import check_fields
import error
from current_user import CurrentUser


class personalTab():
    def __init__(self, current_user: CurrentUser):
        self.current_user = current_user

    def create_personal_tab(self, edit_personal_data_frame: ttk.Frame):
        """ create the change personal data frame
        Args:
            edit_personal_data_frame - the frame of the edit personal data tab
        """
        edit_personal_data_frame.grid_propagate(False)

        personal_change_frame = ttk.Labelframe(
            edit_personal_data_frame, width=100, height=2000)
        personal_change_frame.grid(ipady=10, ipadx=10, sticky='ew')
        ttk.Label(personal_change_frame, text="Edit Your Profile").grid(
            row=1, column=1, pady=10, padx=30)

        self.username_change_frame = ttk.Labelframe(
            edit_personal_data_frame, width=100, height=2000)
        self.username_change_frame.grid(row=2, ipady=10, ipadx=10, sticky='ew')
        ttk.Label(self.username_change_frame, text="User Name :").grid(
            row=2, column=1, pady=10)
        username_entry = ttk.Entry(self.username_change_frame, width=15)
        username_entry.grid(row=2, column=2)
        ttk.Button(self.username_change_frame, text="Ok", command=lambda: self.change_username(
            username_entry.get())).grid(row=3, column=2, pady=10)

        password_change_frame = ttk.Labelframe(
            edit_personal_data_frame, width=100, height=2000)
        password_change_frame.grid(row=3, ipady=10, ipadx=10, sticky='ew')
        ttk.Label(password_change_frame, text="Old Password :").grid(
            row=3, column=1, pady=10)
        old_pass_entry = ttk.Entry(password_change_frame, width=15, show="*")
        old_pass_entry.grid(row=3, column=2)
        ttk.Label(password_change_frame, text="New Password :").grid(
            row=4, column=1, pady=10)
        new_pass_entry = ttk.Entry(password_change_frame, width=15, show="*")
        new_pass_entry.grid(row=4, column=2)
        ttk.Label(password_change_frame, text="Reapet New Password :").grid(
            row=5, column=1, pady=10)
        new_reapet_pass_entry = ttk.Entry(
            password_change_frame, width=15, show="*")
        new_reapet_pass_entry.grid(row=5, column=2)
        ttk.Button(password_change_frame, text="Ok", command=lambda: self.change_password(old_pass_entry.get(
        ), new_pass_entry.get(), new_reapet_pass_entry.get(), password_change_frame)).grid(row=7, column=2, pady=10)

    def change_password(self, old_password: str, new_password: str, repeat_password: str, password_change_frame: ttk.Frame):
        """change the old password to a new one, but first check:
            1. a valid new and old password
            2. the old password is the same as the user password
            3. repeated password is the same as new password
        Args:
            old_password -  the old password the user enter
            new_password - the new password the user want 
            repeat_password - the user repeat the new password fo verification
            password_change_frame - current frame
        """

        try:
            check_fields.check_changed_password(
                new_password, old_password, repeat_password, self.current_user.get_password())
        except error.ValidationError as exception:
            self.label_change(str(exception))
            return

        self.current_user.update_password(new_password)
        self.label_change("Password changed")

    def change_username(self, new_username: str):
        """change the username 
        Args:
            new_username - the new username the user want
            username_change_frame - current frame
        """
        # check if username already exist for other user
        try:
            check_fields.check_changed_username(
                new_username, self.current_user.get_name())
        except error.ValidationError as exception:
            self.label_change(str(exception))
            return

        self.current_user.update_username()
        self.label_change("Username changed")

    def label_change(self, label_txt: str):
        ttk.Label(self.username_change_frame, text=label_txt,
                  style="error.login.TLabel").grid(row=9, column=2, sticky="ew")
