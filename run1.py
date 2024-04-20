import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


# Define a function to clean the text by removing unwanted lines and phrases
def clean_text(text):
    #
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


# Instantiate a Chrome driver object
driver = webdriver.Chrome()

# Use the get method to navigate to the page
driver.get("http://thanhdoandanang.org.vn/")
driver.implicitly_wait(15)
driver.maximize_window()


titles, links = [],[]
title = driver.find_elements(By.CSS_SELECTOR, ".tab-content, .entry-title [href]" )# Extract text and href attributes
titles = [t.get_attribute('title') for t in title]
links = [t.get_attribute('href') for t in title]



list1 = [None]  * len(links)
list2 = [None]  * len(links)
for i in range(len(links)):
    try:
        driver.get(links[i])
        driver.implicitly_wait(15)
        date_list = driver.find_elements(By.CSS_SELECTOR, ".posted-on ,.entry-date published")
        d1 = [date.text for date in date_list]
        list1[i] = d1

        content_list = driver.find_elements(By.ID, "content")
        d2 = [content.text for content in content_list]
        cleaned_text = clean_text(d2)
        list2[i] = cleaned_text
        pass
    except Exception as e:
        print(f"index {i}")
        pass


df = []
df = pd.DataFrame({
        'title': titles,
        'link': links,
        'date': list1,
        'content': list2})
df['Index'] = range(1,len(df)+1)
comlumn_order = ['Index']+[col for col in df if col != 'Index']
df = df[comlumn_order]

df.sort_values(by='date', inplace=True, ascending = False)

print(df.shape)
print(df.head(5))

# # # Giả sử 'df' là DataFrame của bạn
df.to_csv('dataframe.csv', index=False)

# Close the browser
driver.quit()

