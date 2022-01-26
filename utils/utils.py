import warnings
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def print_channel_vids(channel: str, driver_path: str) -> None:
    driver = webdriver.Chrome(driver_path)
    wait = WebDriverWait(driver, 3)
    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located

    URL = 'https://www.youtube.com/c/{}/videos?view=0&sort=p&flow=grid'

    # Navigate to the YouTube channel
    driver.get(URL.format(channel))

    renderers = driver.find_elements_by_tag_name('ytd-grid-video-renderer')
    for renderer in renderers:
        try:
            title = renderer.find_element_by_id('video-title').text
            cc = renderer.find_element_by_class_name('badge-style-type-simple').text
            vid_url = renderer.find_element_by_id('thumbnail').get_attribute('href')
            views = renderer.find_element_by_class_name('ytd-grid-video-renderer')
        except NoSuchElementException as exp:
            print(f'{title}')
            pass
        else:
            print(f'{title} ({cc})')
            pass
        finally:
            print(vid_url, views.text)
            print('='*30)
    