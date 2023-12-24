# app.py

import tkinter as tk
from util.settings_manager import SettingsManager
from util.economic_calendar_manager import EconomicCalendarManager
from data.countries import regions
import pandas as pd
import yaml

def load_default_countries(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data['default_selected_countries']

# economic_calendar_manager 객체 먼저 생성
economic_calendar_manager = EconomicCalendarManager()

# confirm_selection 함수 정의
def confirm_selection():
    selected_countries = [country for country, var in settings_manager.vars.items() if var.get()]
    print("Selected countries:", selected_countries)
    
    pd.set_option('display.max_columns', None)
    # economic_calendar_manager의 스크래핑 메소드 호출
    economic_calendar_manager.scrape_economic_calendar(selected_countries)
    # print(economic_calendar_manager.events_df)
    
    economic_calendar_manager.events_df.to_csv('test.csv')
    
    
    economic_calendar_manager.show_message()

# 메인 윈도우 생성 및 settings_manager 객체 실행
root = tk.Tk()
default_selected_countries = load_default_countries('settings.yaml')
#gui 띄우고 컨펌시 설정 반영해서 스크래핑까지
settings_manager = SettingsManager(root, regions, default_selected_countries, confirm_selection)

# 이벤트 데이터 프레임도 가져왔다. 그러면 이제 알람 설정해야지
# economic_calendar_manager.events_df

root.mainloop()
