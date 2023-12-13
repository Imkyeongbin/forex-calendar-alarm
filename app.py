# app.py

import tkinter as tk
from gui import CountryChecklistApp
from data.countries import regions
import yaml

def load_default_countries(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data['default_selected_countries']

def confirm_selection():
    selected_countries = [country for country, var in app.vars.items() if var.get()]
    print("Selected countries:", selected_countries)
    # 여기에서 스크래핑 로직을 호출하거나 기타 필요한 작업을 수행할 수 있습니다.

# 메인 윈도우 생성
root = tk.Tk()
default_selected_countries = load_default_countries('settings.yaml')
app = CountryChecklistApp(root, regions, default_selected_countries, confirm_selection)
root.mainloop()
