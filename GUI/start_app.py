from __future__ import annotations
from tkinter import FLAT
from ttkbootstrap import Style
import welcome_page
import tab_creator
import tkinter as tk


class StartApp(tk.Tk):
    """StartApp class set the container af the app and it's style and other setting of window"""

    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        self.title("Check your Vitamins")
        self.iconbitmap("additional_files\Icon.ico")  # set the icon of window

        container.grid()

        self.set_style()

        self.frames = {}
        frame = welcome_page.WelcomePage(container, self)
        self.frames[welcome_page.WelcomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_WelcomePage()

    def set_style(self):
        """set the style of window"""
        self.style = Style(theme='superhero')
        self.style.configure(
            "secondary.Horizontal.TFloodgauge", thickness=5, relief=FLAT)
        self.style.configure("TLabel", font="Aharoni 12")
        self.style.configure("Welcome.TLabel", font="Aharoni 24")
        self.style.configure("TLabelframe", font="Aharoni 12")
        self.style.configure("error.login.TLabel", font="Calibri 12")

    def show_WelcomePage(self):
        """show the frame of WelcomePage"""
        # self.state('zoomed')
        self.geometry("1000x700")
        self.state('normal')
        self.resizable(0, 0)  # can't resize window
        frame = self.frames[welcome_page.WelcomePage]
        frame.tkraise()

    def show_tab_creator(self):
        """show the frame of TabPage"""
        self.state('zoomed')
        self.resizable(1, 1)  # can resize window
        frame = self.frames[tab_creator.TabPage]
        frame.tkraise()

    def switch_frames(self, parent_frame: tk.Frame, frame_name: str, welcome_obj: welcome_page.WelcomePage = None):
        """ switch the frames to frame_name
        Args:
            parent_frame - the parent frame of the new app
            welcome_obj - need to pass it to TabPage to get access for user data
        """
        if frame_name == "TabCreator":
            frame = tab_creator.TabPage(parent_frame, welcome_obj, self)
            self.frames[tab_creator.TabPage] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_tab_creator()
        else:
            frame = welcome_page.WelcomePage(parent_frame, self)
            self.frames[welcome_page.WelcomePage] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_WelcomePage()


if __name__ == '__main__':
    my_gui = StartApp()
    my_gui.mainloop()
