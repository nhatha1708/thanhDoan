from facebook_scraper import get_posts, _scraper
import json
import facebook_scraper as fs
import pandas as pd
import time

# Page 1: hoi sinh vien da nang
with open('./mbasicHeaders.json', 'r') as file:
    _scraper.mbasic_headers = json.load(file)

# Read the cookies from the file
with open('mbasic.facebook.com_cookies.txt', 'r') as f:
    cookies = {}
    for line in f:
        if not line.startswith('#') and not line.isspace():
            key, value = line.strip().split('\t')[5:7]
            cookies[key] = value

index = 0
post_urls = [None]*40
date = [None]*40
list_content = [None]*40
for post in get_posts('hoisinhviendanang', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/hoisinhviendanang?v=timeline&lst=100025055373500%3A100064556115412%3A1715361298&eav=AfYEcgIK-dATP-jj-eqtrax6PwWy0KrhYBJBGjLoZCfhO1yp8I0tBQKO5bKZmEzGdZA&paipv=0", pages=10, cookies=cookies):
        time.sleep(200)
        content = [None]
        print(index)
        date[index] = post['time']
        post_urls[index] = post['post_url']
        if 'full_text' in post:
                content = content + [post['full_text']]
                list_content[index] = content
        else:
                list_content[index] = "None found"
        index = index + 1
        if index == 10:
                break

# Page 2: thieu nhi thanh pho da nang
with open('./hoithieunhiHeaders.json', 'r') as file:
    _scraper.mbasic_headers = json.load(file)

for post in get_posts('Thieunhithanhphodanang', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/Thieunhithanhphodanang?v=timeline&lst=100025055373500%3A100050942934157%3A1715368776&eav=AfZ4xlSOtfhRJiHfIctWakILlqxgIa7iRafrtGEr5_fkfUAngRHNlEzXht_n6pEjb0g&paipv=0", pages=10, cookies=cookies):
        time.sleep(200)
        content = [None]
        print(index)
        date[index] = post['time']
        post_urls[index] = post['post_url']
        if 'full_text' in post:
                content = content + [post['full_text']]
                list_content[index] = content
        else:
                list_content[index] = "None found"
        index = index + 1
        if index == 20:
                break
# Page 3: tuoi tre da nang
with open('./tuoitrednHeaders.json', 'r') as file:
    _scraper.mbasic_headers = json.load(file)

for post in get_posts('tuoitredanangdn', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/tuoitredanangdn?v=timeline&lst=100025055373500%3A100064539736066%3A1715408567&eav=AfbS6dJYEfoiU84j16b7t-qAKEBfyRdKzWO3Tgi-saPQcL9S7S-GCSBjtnrXz1FL954&paipv=0", pages=10, cookies=cookies):
        time.sleep(200)
        content = [None]
        print(index)
        date[index] = post['time']
        post_urls[index] = post['post_url']
        if 'full_text' in post:
                content = content + [post['full_text']]
                list_content[index] = content
        else:
                list_content[index] = "None found"
        index = index + 1
        if index == 30:
                break

# Page 4: Viec lam thanh nien da nang
with open('./vieclamtndnHeaders.json', 'r') as file:
    _scraper.mbasic_headers = json.load(file)

for post in get_posts('vieclamthanhniendanang', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/vieclamthanhniendanang?v=timeline&lst=100025055373500%3A100090460894592%3A1715408837&eav=AfbOHuRS5YCENXUPK3BKWFm4rXRcZiAoKIDEGmRYnsKRDovr8-tg0u4E__ujxGfuzfE&paipv=0", pages=10, cookies=cookies):
        time.sleep(300)
        content = [None]
        print(index)
        date[index] = post['time']
        post_urls[index] = post['post_url']
        if 'full_text' in post:
                content = content + [post['full_text']]
                list_content[index] = content
        else:
                list_content[index] = "None found"
        index = index + 1
        if index == 40:
                break

# Tao df va xuat csv
df = pd.DataFrame({
            'link': post_urls,
            'date': date,
            'content': list_content})
df['Index'] = range(1, len(df) + 1)
column_order = ['Index'] + [col for col in df if col != 'Index']
df = df[column_order]

df.to_csv('dataframe.csv', index=False)