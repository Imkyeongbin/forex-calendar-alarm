# gui.py

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import sys
import yaml

class SettingsManager:
    def __init__(self, root, regions, default_selected_countries, confirm_callback):
        self.root = root
        self.root.title("Country Checklist")
        self.regions = regions
        self.default_selected_countries = default_selected_countries
        self.confirm_callback = confirm_callback
        self.checkboxes = {}
        self.vars = {}
        self.create_widgets()
    
    def get_selected_countries(self):
        return [country for country, var in self.vars.items() if var.get()]

    def create_widgets(self):
        self.create_checkboxes()
        self.create_confirm_and_cancel_buttons()
        self.create_save_button()  # save 버튼 생성 함수 추가

    def create_checkboxes(self):
        # 가장 긴 region 문자열의 길이를 찾습니다.
        max_length = max(len(region) for region in self.regions)

        # 볼드체 글꼴을 설정합니다.
        bold_font = tkFont.Font(weight="bold")

        for region, countries in self.regions.items():
            region_frame = ttk.Frame(self.root)
            region_frame.pack(side='top', fill='x', expand=True, padx=10, pady=5)

            # 레이블에 볼드체 글꼴을 적용합니다.
            label = ttk.Label(region_frame, text=region, anchor='w', font=bold_font, width=max_length)
            label.pack(side='left', padx=5)

            countries_frame = ttk.Frame(region_frame)
            countries_frame.pack(side='left', fill='x', expand=True, padx=5)

            for country in countries:
                country_value = country.split(sep=" ")[1]
                var = tk.BooleanVar(value=country_value in self.default_selected_countries)
                cb = ttk.Checkbutton(countries_frame, text=country, variable=var)
                cb.pack(side='left', padx=2, pady=2)
                self.checkboxes[country_value] = cb
                self.vars[country_value] = var


    def create_confirm_and_cancel_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side='bottom', pady=10)

        confirm_button = ttk.Button(button_frame, text="Confirm", command=self.confirm_callback)
        confirm_button.pack(side='left', padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.exit_app)
        cancel_button.pack(side='left', padx=5)
        
    def confirm_callback(self):
        selected_countries = [country for country, var in self.vars.items() if var.get()]
        print("Confirmed countries:", selected_countries)
        self.root.destroy()
    
    def exit_app(self):
        self.root.destroy()
        sys.exit()  # 프로그램을 완전히 종료


    def create_save_button(self):
        save_button = ttk.Button(self.root, text="Save", command=self.save_settings)
        save_button.pack(side='bottom', pady=10)
        # 색상 지정을 위한 스타일 설정 (예시: 파란색 배경, 흰색 글씨)
        style = ttk.Style()
        style.configure("Save.TButton", background="blue", foreground="white")
        save_button.configure(style="Save.TButton")

    def save_settings(self):
        selected_countries = [country for country, var in self.vars.items() if var.get()]
        settings = {'default_selected_countries': selected_countries}
        with open('settings.yaml', 'w') as file:
            yaml.dump(settings, file)