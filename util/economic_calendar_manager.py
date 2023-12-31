from playwright.sync_api import sync_playwright
import pandas as pd
import tkinter as tk
from tkinter import messagebox

class EconomicCalendarManager:
    def __init__(self, selected_countries=[]):
        self.selected_countries = selected_countries
        self.events_df = pd.DataFrame()
        self.browser = None
        self.page = None

        
    def show_message(self):
        root = tk.Tk()
        root.withdraw()  # 루트 창을 숨깁니다.
        root.attributes('-topmost', True)  # 창을 항상 최상위에 띄웁니다.
        messagebox.showinfo("No Events", "오늘, 내일 중에 일어나는 이벤트가 없습니다.")
        root.attributes('-topmost', False)  
        root.destroy()  # 루트 창을 파괴하여 메모리를 해제합니다.
        
    # def check_countries(self, selected_countries):
    #     # 혹시 모를 문자 차이에 대비해 selected_countries 요소를 전부 소문자로 변경함.
    #     selected_countries_lowercase_list = [item.lower() for item in selected_countries]
        
    #     country_region_tab_selector = '.dfx-calendarTopBar__filterFull > .dfx-calendarTopBar__multipleCheckboxesWithIconFilterCheckboxes'
    #     self.page.wait_for_selector(selector=country_region_tab_selector, state='attached')
    #     print('찾았네염')
    #     # 일단 컨트리/리전 탭 셀렉터를 통해 페이지에서 컨트리/리전 탭을 선택하여 변수에 할당함.
    #     country_region_tab = self.page.query_selector(country_region_tab_selector)
    #     self.page.get_by_role
        
    #     # data-country 속성을 가진 모든 요소를 찾습니다.
    #     country_checkbox_elements = country_region_tab.query_selector_all('[data-country]')
        
    #     for element in country_checkbox_elements:
    #         # 각 요소의 data-country 속성 값을 소문자로 가져옵니다.
    #         country = element.get_attribute("data-country").lower()

    #         if country in selected_countries_lowercase_list:
    #             # 나라 리스트에 포함되면 체크합니다.
    #             element.get_by_role()
    #         else:
    #             # 나라 리스트에 포함되지 않으면 언체크합니다.
    #             if element.is_checked():
    #                 element.uncheck()
    
    def check_countries(self, selected_countries):
        # 혹시 모를 문자 차이에 대비해 selected_countries 요소를 전부 소문자로 변경함.
        selected_countries_lowercase_list = [item.lower() for item in selected_countries]
        
        country_region_tab_selector = '.dfx-calendarTopBar__filterFull > .dfx-calendarTopBar__multipleCheckboxesWithIconFilterCheckboxes'
        self.page.wait_for_selector(selector=country_region_tab_selector, state='attached')
        print('찾았네염')
        # 일단 컨트리/리전 탭 셀렉터를 통해 페이지에서 컨트리/리전 탭을 선택하여 변수에 할당함.
        country_region_tab = self.page.locator(country_region_tab_selector)
        self.page.get_by_role
        
        # data-country 속성을 가진 모든 요소를 찾습니다.
        country_checkbox_elements = country_region_tab.query_selector_all('[data-country]')
        
        for element in country_checkbox_elements:
            # 각 요소의 data-country 속성 값을 소문자로 가져옵니다.
            country = element.get_attribute("data-country").lower()

            if country in selected_countries_lowercase_list:
                # 나라 리스트에 포함되면 체크합니다.
                element.get_by_role()
            else:
                # 나라 리스트에 포함되지 않으면 언체크합니다.
                if element.is_checked():
                    element.uncheck()

    def get_scraped_data(self):
        # 셀렉터를 기반으로 요소가 로드될 때까지 기다림
        container_selector = '#dfx-tabs > div.dfx-tabs__content > div.dfx-tabs__tabContent.dfx-tabs__tabContent--active'
        self.page.wait_for_selector(container_selector)

        # 셀렉터 내의 모든 필요한 요소들을 추출 (예: 각 이벤트의 세부 정보)
        container = self.page.query_selector(container_selector)
        
        # 일단 스케줄이 없으면 지나친다.
        if self.schedule_existence_check(container):
            #스크랩한 데이터를 기존 리스트에 낑겨넣는다.
            return self.scrape_container(container)
        return []

    def schedule_existence_check(self, container):
        no_schedule_selector = 'h2.text-center'
        no_schedule_screen = container.query_selector(no_schedule_selector)
        if no_schedule_screen and 'There are no events scheduled' in no_schedule_screen.inner_text():
            return False # 추후에 맞게 바꿔야함.
        return True

    def scrape_container(self, container):
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
                        'event title' : title,
                        'importance' : importance,
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

    def scrape_economic_calendar(self, selected_countries):
        with sync_playwright() as p:
            # self.browser = p.chromium.launch()
            self.browser = p.chromium.launch(headless=False)
            self.page = self.browser.new_page()
            
            today_tomorrow_event_list = []
            #page today
            self.page.goto('https://www.dailyfx.com/economic-calendar#today')
            #물론 체크는 처음만 해주면 되겠지
            self.check_countries(selected_countries)
            #그냥 새로 고침을 하면 웨이팅을 이미 했는지 안했는지 애매하지 않지.
            self.page.reload()
            
            today_tomorrow_event_list.extend(self.get_scraped_data())
                
            #page tomorrow
            self.page.goto('https://www.dailyfx.com/economic-calendar#tomorrow')

            today_tomorrow_event_list.extend(self.get_scraped_data())
            
            
            # 추출된 데이터를 출력합니다.

            # self.browser.close()

            # 추출된 데이터를 DataFrame으로 변환
            df = pd.DataFrame(today_tomorrow_event_list)
            self.events_df = df

        

    # 스크래핑 함수 실행
    
    
