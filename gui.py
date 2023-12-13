# gui.py

import tkinter as tk
from tkinter import ttk

class CountryChecklistApp:
    def __init__(self, root, regions, default_selected_countries, confirm_callback):
        self.root = root
        self.root.title("Country Checklist")
        self.regions = regions
        self.default_selected_countries = default_selected_countries
        self.confirm_callback = confirm_callback
        self.checkboxes = {}
        self.vars = {}
        self.create_widgets()

    def create_widgets(self):
        self.create_checkboxes()
        self.create_confirm_button()

    def create_checkboxes(self):
        for region, countries in self.regions.items():
            region_frame = ttk.Frame(self.root)
            region_frame.pack(side='top', fill='x', expand=True, padx=10, pady=5)
            label = ttk.Label(region_frame, text=region, anchor='w')
            label.pack(side='left', padx=5)
            countries_frame = ttk.Frame(region_frame)
            countries_frame.pack(side='left', fill='x', expand=True, padx=5)
            for country in countries:
                var = tk.BooleanVar(value=country in self.default_selected_countries)
                cb = ttk.Checkbutton(countries_frame, text=country, variable=var)
                cb.pack(side='left', padx=2, pady=2)
                self.checkboxes[country] = cb
                self.vars[country] = var

    def create_confirm_button(self):
        confirm_button = ttk.Button(self.root, text="Confirm", command=self.confirm_callback)
        confirm_button.pack(side='bottom', pady=10)
