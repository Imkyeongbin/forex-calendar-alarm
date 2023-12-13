from playwright.sync_api import sync_playwright
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from data.countries import regions

def show_message():
    root = tk.Tk()
    root.withdraw()  # 루트 창을 숨깁니다.
    root.attributes('-topmost', True)  # 창을 항상 최상위에 띄웁니다.
    messagebox.showinfo("No Events", "오늘, 내일 중에 일어나는 이벤트가 없습니다.")
    root.attributes('-topmost', False)  
    root.destroy()  # 루트 창을 파괴하여 메모리를 해제합니다.

def get_scraped_data(page):
    # 셀렉터를 기반으로 요소가 로드될 때까지 기다림
    container_selector = '#dfx-tabs > div.dfx-tabs__content > div.dfx-tabs__tabContent.dfx-tabs__tabContent--active'
    page.wait_for_selector(container_selector)

    # 셀렉터 내의 모든 필요한 요소들을 추출 (예: 각 이벤트의 세부 정보)
    container = page.query_selector(container_selector)
    
    # 일단 스케줄이 없으면 지나친다.
    if schedule_existence_check(container):
        #스크랩한 데이터를 기존 리스트에 낑겨넣는다.
        return scrape_container(container)
    return []

def schedule_existence_check(container):
    no_schedule_selector = 'h2.text-center'
    no_schedule_screen = container.query_selector(no_schedule_selector)
    if no_schedule_screen and 'There are no events scheduled' in no_schedule_screen.inner_text():
        return False # 추후에 맞게 바꿔야함.
    return True

def scrape_container(container):
    div_table = container.query_selector('div>div')
    # div_table은 이미 선택된 div 요소
    hourBlock_selector = ".dfx-expandableTable__hourBlock"  
    event_times = div_table.query_selector_all(hourBlock_selector)
        
    event_data = []
    for event_element in event_times:
        # 이벤트 시간 추출
        # 이미 선택된 요소 내에서 특정 span 요소를 찾습니다.
        time_element = event_element.query_selector('span.dfx-economicCalendarRow__time')

        # 해당 span 요소에서 'data-time' 속성을 추출합니다.
        data_time = time_element.get_attribute('data-time') if time_element else "No data-time"

        # 추출한 'data-time' 값을 출력합니다.
        print(data_time)

        
        country_group_selector = 'div.dfx-economicCalendarRow__CountryGroup'
        country_groups = event_element.query_selector_all(country_group_selector)
        country_data = []
        for country_group in country_groups:
            country_name_selector = 'span.dfx-economicCalendarRow__country'
            country_name_element = country_group.query_selector(country_name_selector)
            country_name = country_name_element.inner_text() if time_element else "No Country"
            
            rows_selector = 'div.dfx-expandableTable__row'
            rows = country_group.query_selector_all(rows_selector)
            row_data = []
            for row in rows:
                # 이벤트 제목 추출
                title_element = row.query_selector('.jsdfx-economicCalendarRow__title')
                title = title_element.inner_text() if title_element else "No title"
            
                # 이벤트 중요도 추출
                importance_element = row.query_selector('.dfx-importance')
                importance = importance_element.inner_text() if importance_element else "No importance"
            
                # # 실제 값 추출
                # actual_element = event_element.query_selector('.jsdfx-economicCalendarRow__actual')
                # actual = actual_element.inner_text() if actual_element else "No actual"
                
                # # 이전 값 추출
                # previous_element = event_element.query_selector('.jsdfx-economicCalendarRow__previous')
                # previous = previous_element.inner_text() if previous_element else "No previous"
                
                row_data.append({
                    'event title' : title_element,
                    'importance' : importance_element,
                })
            
            # 추출한 데이터를 딕셔너리로 저장하여 리스트에 추가합니다.
            country_data.append({
                'country name' : country_name,
                'event list' : row_data
            })

        event_data.append({
            'event time' : data_time,
            'country groups' : country_data
        })
        
    return event_data

def scrape_economic_calendar():
    with sync_playwright() as p:
        # browser = p.chromium.launch()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        today_tomorrow_event_list = []
        #page today
        page.goto('https://www.dailyfx.com/economic-calendar#today')
        
        today_tomorrow_event_list.extend(get_scraped_data(page))
            
        #page tomorrow
        page.goto('https://www.dailyfx.com/economic-calendar#tomorrow')

        today_tomorrow_event_list.extend(get_scraped_data(page))
        
        
        # 추출된 데이터를 출력합니다.

        # browser.close()

        # 추출된 데이터를 DataFrame으로 변환
        df = pd.DataFrame(today_tomorrow_event_list)
        return df

    

# 스크래핑 함수 실행

economic_calendar_df = scrape_economic_calendar()
show_message()
print(economic_calendar_df)
