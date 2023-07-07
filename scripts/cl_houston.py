from bs4 import BeautifulSoup
from collections import namedtuple
import datetime
import os
import pandas as pd
import re
import requests
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0'
firefox_driver_path = os.path.join(os.getcwd(), 'drivers', 'geckodriver')
firefox_service = Service(firefox_driver_path, log_path=os.path.devnull)
firefox_option = Options()
firefox_option.set_preference('general.useragent.override', user_agent)
driver = webdriver.Firefox(service=firefox_service, options=firefox_option)
driver.implicitly_wait(9)

url = 'https://houston.craigslist.org/'
source_name = f"cl_{url.split('.')[0].split('//')[-1]}"
city_name = source_name.split("_")[1].capitalize()
driver.get(url)

search_query = 'record player'
search_field = driver.find_element(By.XPATH, '/html/body/div[2]/section/div[2]/div[1]/div/input')
search_field.clear()
search_field.send_keys(search_query)
search_field.send_keys(Keys.ENTER)
time.sleep(11)  # If you start getting "ValueError:" "Expected axis has 0 elements" increase time.sleep

posts_html = []
to_stop = False
current_page = 0
total_items = 0

scroll_pause_time = .7  # if current_gallery == prev_gallery before it reaches the end of the page increase this
scroll_offset = 1200
actions = ActionChains(driver)

while not to_stop:
    while True:
        prev_url = driver.current_url
        prev_gallery = prev_url.split('#')[1] if '#' in prev_url else None
        actions.scroll_by_amount(0, scroll_offset).perform()
        time.sleep(scroll_pause_time)
        current_url = driver.current_url
        current_gallery = current_url.split('#')[1] if '#' in current_url else None
        if current_gallery == prev_gallery:
            break
    search_results = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[4]/ol')
    soup = BeautifulSoup(search_results.get_attribute('innerHTML'), 'html.parser')
    posts_html.extend(soup.find_all('li', {'class': 'cl-search-result'}))
    page_num = driver.find_element(By.CLASS_NAME, 'cl-page-number').text
    pattern = r'([\d,]+)\s*of\s*([\d,]+)'
    match = re.search(pattern, page_num)
    if match:
        current_page = int(match.group(1).replace(',', ''))
        total_items = int(match.group(2).replace(',', ''))

    try:
        driver.execute_script('window.scrollTo(0, 0)')
        button_next = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div[2]/button[3]')
        button_next.click()
        time.sleep(1)
        if current_page == total_items:
            to_stop = True
        else:
            to_stop = False
    except ElementNotInteractableException:
        to_stop = True

print('Collected {0} listings'.format(len(posts_html)))

CraigslistPost = namedtuple('CraigslistPost',
                            ['title', 'price', 'post_timestamp', 'location', 'post_url', 'image_url', 'data_pid'])
craigslist_posts = []
image_paths = []
default_image_path = "images/no_image.png"
for posts_html in posts_html:
    title = getattr(posts_html.find('a', 'posting-title'), 'text', None)
    price_element = posts_html.find('span', 'priceinfo')
    price = price_element.text.strip() if price_element is not None else 'Price not given'
    meta_div = posts_html.find('div', class_='meta')
    if meta_div:
        meta_info = meta_div.get_text(strip=True)
        separator = meta_div.find('span', class_='separator')
        if separator:
            post_timestamp = meta_info.split(separator.text)[0]
            location = meta_info.split(separator.text)[1]
            if location.strip() == '':
                location = f'{city_name} area'
    post_url = posts_html.find('a', 'posting-title').get('href') if posts_html.find('a', 'posting-title') else ''
    if not os.path.exists(f"images/{source_name}"):
        os.makedirs(f"images/{source_name}")
    image_url = posts_html.find('img').get('src') if posts_html.find('img') else ''
    file_path = ""
    if image_url:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_file_name = image_url.split("/")[-1]
            file_path = os.path.join(f"images/{source_name}", image_file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
                print(f"Image downloaded: {file_path}")
    else:
        file_path = f'{default_image_path}'
    image_paths.append(file_path)
    if image_url.strip() == '': # sometimes this errors out if the scroll_pause_time is too low
        image_url = 'No image'
    data_pid = posts_html.get('data-pid')
    craigslist_posts.append(CraigslistPost(title, price, post_timestamp, location, post_url, image_url, data_pid))

df = pd.DataFrame(craigslist_posts)
current_time = datetime.datetime.now().strftime("%m/%d %H:%M:%S")
df.insert(0, 'time_added', current_time)
df.insert(0, 'source', f"{source_name}")
df['image_path'] = image_paths
df.dropna(inplace=True)
df.to_excel(f'sheets/{source_name}.xlsx', index=False)
driver.close()