import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from driver import close_driver
from driver import get_url
from driver import get_webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import df_output
from utils import get_current_time
from utils import launcher_path
from utils import parse_url
from utils import selectors

current_time = get_current_time()


def navigate_to_category(link, search_query, browser_arg, headless_arg):
    city_name = parse_url(link)
    driver = get_webdriver(browser_arg, headless_arg)
    wait = WebDriverWait(driver, 60)
    get_url(driver, link)

    print(f"Fetching {search_query}s from {city_name.capitalize()} Craigslist...")

    for_sale = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, selectors["selectors"]["links"]["for_sale"]["all"])
        )
    )
    for_sale.click()
    search_field = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, selectors["selectors"]["for_sale"]["search"])
        )
    )

    if search_query:
        search_field.clear()
        search_field.send_keys(search_query)
        search_field.send_keys(Keys.ENTER)
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, selectors["selectors"]["for_sale"]["results"])
        )
    )

    # result_options = wait.until(EC.visibility_of_element_located((By.XPATH, selectors['selectors']['result_options']['box_button'])))
    # result_options.click()

    # result_list = wait.until(EC.visibility_of_element_located((By.XPATH, selectors['selectors']['result_options']['list'])))
    # result_list.click()
    # wait.until(EC.visibility_of_element_located((By.XPATH, selectors['selectors']['for_sale']['results'])))

    return driver


def get_listing_data(driver):
    posts_data = []
    scraped_img_tag_src = set()
    to_stop = False
    current_page = 0
    total_items = 0

    scroll_pause_time = 1.4  # find a method to wait for images to load
    scroll_offset = 1000
    actions = ActionChains(driver)

    while not to_stop:  # write custom actions for Preview
        while True:
            prev_url = driver.current_url
            prev_gallery = prev_url.split("#")[1] if "#" in prev_url else None
            actions.scroll_by_amount(0, scroll_offset).perform()
            time.sleep(scroll_pause_time)
            current_url = driver.current_url
            current_gallery = current_url.split("#")[1] if "#" in current_url else None
            if current_gallery == prev_gallery:
                break
        search_results = driver.find_element(
            By.XPATH, selectors["selectors"]["for_sale"]["results"]
        )
        soup = BeautifulSoup(search_results.get_attribute("innerHTML"), "html.parser")
        for div in soup.find_all("li", {"class": "cl-search-result"}):
            img_tag = div.find("img")
            if img_tag:
                img_tag_src = img_tag.get("src")
                if img_tag_src not in scraped_img_tag_src:
                    posts_data.extend(div)
                    scraped_img_tag_src.add(img_tag_src)
            else:
                post_url = div.find("a", {"class": "posting-title"})
                if post_url:
                    img_tag_src = post_url.get("href")
                    if img_tag_src not in scraped_img_tag_src:
                        posts_data.extend(div)
                        scraped_img_tag_src.add(img_tag_src)

        page_num = driver.find_element(By.CLASS_NAME, "cl-page-number").text
        pattern = r"([\d,]+)\s*of\s*([\d,]+)"
        match = re.search(pattern, page_num)
        if match:
            current_page = int(match.group(1).replace(",", ""))
            total_items = int(match.group(2).replace(",", ""))
        if posts_data == []:
            driver.close()
            raise NoSuchElementException(
                "No listings found on the page. Check if the page loaded properly."
            )

        try:
            driver.execute_script("window.scrollTo(0, 0)")
            button_next = driver.find_element(
                By.XPATH, selectors["selectors"]["for_sale"]["next"]
            )
            button_next.click()
            time.sleep(1)
            if current_page == total_items:
                to_stop = True
            else:
                to_stop = False

        except ElementNotInteractableException:
            to_stop = True

        except NoSuchElementException as e:
            print(f"Error: {e}")
            break

    print("Collected {0} listings".format(len(posts_data)))
    close_driver(driver)

    return posts_data


def write_the_data_frames(link, craigslist_posts, make_images, output_arg):
    city_name = parse_url(link)
    sheets = f"{launcher_path}/sheets"
    source_name = f"craigslist_{city_name}"

    if not os.path.exists(sheets):
        os.makedirs(sheets)

    df = pd.DataFrame([x.as_dict() for x in craigslist_posts])
    df.insert(0, "time_added", current_time)
    df.insert(0, "is_new", "1")
    df.insert(0, "source", f"{source_name}")
    df.dropna(inplace=True)
    df_output(df, city_name, output_arg)
