from __future__ import annotations
import tkinter as tk
import tkinter.ttk as ttk
import start_app
from current_user import CurrentUser
from diets_tabs import DietsTab
from personal_tab import PersonalTab
from user import User

class TabPage(tk.Frame):

    def __init__(self, parent_frame: tk.Frame, user: User, controller: start_app.StartApp):
        """Class for the user app GUI with all the features to analysis and calculate your vitamin intake daily.
        Args:
            parent_frame - the current frame
            user - the current user that used the app
            controller - startapp object
        """
        tk.Frame.__init__(self, parent_frame)
        self.controller = controller
        self.parent_frame = parent_frame

        self.current_user = CurrentUser(user)

        self.create_tabs()

    def create_tabs(self):
        """Create all the tabs and their frames"""
        control_tab = ttk.Notebook(
            self, style='lefttab.TNoteboOk', width=2000, height=2000)

        tab_new_diet_frame = ttk.Frame(control_tab, width=2000, height=2000)
        tab_new_diet_frame.grid(row=1, column=0)
        diets_obj = DietsTab(self.current_user)
        diets_obj.create_new_diet_tab(tab_new_diet_frame)

        tab_edit_personal_data_frame = ttk.Frame(
            control_tab, width=900, height=2000)
        tab_edit_personal_data_frame.grid(row=0, column=0)
        personal_obj = PersonalTab(self.current_user)
        personal_obj.create_personal_tab(tab_edit_personal_data_frame)

        tab_all_diets_frame = ttk.Frame(control_tab, width=900, height=2000)
        tab_all_diets_frame.grid(row=2, column=0)
        diets_obj.create_all_diets_tab(tab_all_diets_frame)

        control_tab.add(tab_new_diet_frame, text='Add new diet')
        control_tab.add(tab_all_diets_frame, text='Diets')
        control_tab.add(tab_edit_personal_data_frame,
                        text='Change Personal Data')
        control_tab.grid(row=1, column=0)

        ttk.Label(self, text="Hello  " +
                  self.current_user.get_name()).grid(row=0, column=0, sticky='w')
        ttk.Button(self, text="Log-out ",
                   command=self.logout).grid(row=0, column=0)

    def logout(self):
        """Logout from current user and go back to WelcomePage"""
        self.controller.switch_frames(self.parent_frame, "WelcomePage")
