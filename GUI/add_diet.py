from __future__ import annotations
from tkinter import END
import tkinter as tk
import reset_fields
import diets_tabs
import check_fields
from error_validate import DietValidationError


def add_new_diet(diet_tab: diets_tabs.DietsTab, error_label: tk.Label):
    """Add new diet to collection and update self.user with new diet,
    reset all fields in new_diet tab"""
    try:
        check_fields.check_diet_name(diet_tab.get_entry(
            "diet_name"), diet_tab.current_user.get_diets_name())
        error_label['text'] = ""
    except DietValidationError as exception:
        error_label['text'] = str(exception)
        return

    add_diet_to_diets(diet_tab, False)
    reset_fields.reset_add_new_diet_frame(diet_tab)


def add_diet_to_all_diets_list(diet_tab: diets_tabs.DietsTab, diet_name: str):
    """Add diet_name to all diets names listbox"""
    diet_tab.all_diets_listbox.insert(END, diet_name)


def add_diet_to_diets(diet_tab: diets_tabs.DietsTab, is_edit: bool):
    """Add new diet to all diets or if is_edit=True add edited diet to diets
    update the collection and the local user args
    Args:
        is_edit - true if in edit mode
        diet_tab - tab page object
    """

    diet_tab.current_user.update_diets(
        diet_tab.get_current_diet(), diet_tab.get_entry("diet_name"), is_edit)
    if not is_edit:
        add_diet_to_all_diets_list(diet_tab, diet_tab.diet_name_entry.get())
