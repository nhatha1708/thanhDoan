import numpy as np
from selenium import webdriver
from time import sleep
import random 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import pandas as pd
import os
from datetime import datetime



def clean_text(text):
            my_string = ", ".join(text)
            index = my_string.find('\nBÀI VIẾT LIÊN QUAN')
            my_string = my_string[:index]
            # Split the text into lines
            lines = my_string.split('\n')
            
            # Remove unwanted lines and phrases
            cleaned_lines = [line for line in lines]
            
            # Join the cleaned lines back into a single string
            cleaned_text = '\n'.join(cleaned_lines)
            return cleaned_text

def convert_to_datetime(date_str):
        # Tạo từ điển ánh xạ tên tháng tiếng Việt sang tiếng Anh
        month_mapping = {
            'Tháng Một,': 'January',
            'Tháng Hai,': 'February',
            'Tháng Ba,': 'March',
            'Tháng Tư,': 'April',
            'Tháng Năm,': 'May',
            'Tháng Sáu,': 'June',
            'Tháng Bảy,': 'July',
            'Tháng Tám,': 'August',
            'Tháng Chín,': 'September',
            'Tháng Mười,': 'October',
            'Tháng Mười Một,': 'November',
            'Tháng Mười Hai,': 'December'
        }
        
        # Thay thế tên tháng tiếng Việt bằng tên tháng tiếng Anh tương ứng
        for viet_month, eng_month in month_mapping.items():
            if viet_month in date_str:
                date_str = date_str.replace(viet_month, eng_month)
                break
        
        # Chuyển chuỗi ngày tháng sang đối tượng datetime
        return datetime.strptime(date_str, "'%d %B %Y'")

class ThanhDoan(webdriver.Chrome):
# luu tru nhung duong dan cua driver
    def __init__(self, driver_path=r"C:\Users\admin\OneDrive\Tài liệu\Python Scripts\thanhDoan",
                 teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(ThanhDoan, self).__init__()
        self.implicitly_wait(150)
        self.maximize_window()

    def __exit__(self,  exc_type, exc_value, exc_tb):
        if self.teardown:
            self.quit()
        pass

    def land_first_page(self):
        self.get('http://thanhdoandanang.org.vn/')
        self.implicitly_wait(15)

    
    def get_data(self):

        # get title and link href
        titles, links = [],[]
        title = self.find_elements(By.CSS_SELECTOR, ".tab-content, .entry-title [href]" )# Extract text and href attributes
        titles = [t.get_attribute('title') for t in title]
        links = [t.get_attribute('href') for t in title]


        list1 = [None]  * len(links)
        list2 = [None]  * len(links)
        for i in range(len(links)):
            try:
                self.get(links[i])
                self.implicitly_wait(15)
                date_list = self.find_elements(By.CSS_SELECTOR, ".posted-on ,.entry-date published")
                d1 = [date.text for date in date_list]
                list1[i] = d1

                content_list = self.find_elements(By.ID, "content")
                d2 = [content.text for content in content_list]
                cleaned_text = clean_text(d2)
                list2[i] = cleaned_text
                pass
            except Exception as e:
                print(f"index {i}: " + e.message)
                pass


        df = []
        df = pd.DataFrame({
                'title': titles,
                'link': links,
                'date': list1,
                'content': list2})
        

        df = df.dropna()
        df['date'] = df['date'].astype(str)
        df['date'] = [d.replace('[', '').replace(']', '') for d in df['date']]
        df['date'] = df['date'].apply(convert_to_datetime)
        df.sort_values(by='date', inplace=True, ascending = False) 

        df['Index'] = range(1,len(df)+1)
        comlumn_order = ['Index']+[col for col in df if col != 'Index']
        df = df[comlumn_order]

        return df

    def to_csv(df):  
        df.to_csv('dataframe.csv', index=False)
        

