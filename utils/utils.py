import numpy as np
import pandas as pd
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=1')

# Download Chrome driver from this link: https://chromedriver.chromium.org/downloads

URL: str = 'https://www.youtube.com/c/{}/videos?view=0&sort=p&flow=grid'
dataframe_cols: list = ['Id', 'Channel', 'Subscribers', 'Title', 'CC', 'URL', 'Released', 'Views']

def get_channel_info(channel: dict, driver_path: str, verbose: Optional[bool] = False) -> pd.DataFrame:
    # Chrome driver
    driver = webdriver.Chrome(driver_path, options=chrome_options)

    # List to store the video details
    data = []

    # Navigate to the YouTube channel
    url = channel.get('url', URL.format(channel.get('channel')))
    if not url.endswith('=grid'):
        url += '?view=0&sort=p&flow=grid'
    driver.get(url)

    try:
        ch = driver.find_element_by_xpath('//yt-formatted-string[@class="style-scope ytd-channel-name"]')
        subs = driver.find_element_by_xpath('//yt-formatted-string[@id="subscriber-count"]')
    except Exception:
        print(f'[EXCEPTION] Channel not found ({channel})!\nPlease check this URL: {url}\n')
        # Exit the program
        return
    else:
        string = 'Channel: {}\nSubscribers: {}\n{}'.format(ch.text, subs.text, '-'*30)
        print(string)

    renderers = driver.find_elements_by_tag_name('ytd-grid-video-renderer')
    for renderer in renderers:
        try:
            title = renderer.find_element_by_id('video-title')
            vid_url = renderer.find_element_by_id('thumbnail').get_attribute('href')
            views = renderer.find_element_by_class_name('ytd-grid-video-renderer')
            cc = renderer.find_element_by_class_name('badge-style-type-simple').text
        except NoSuchElementException as _:
            if verbose:
                print('NoSuchElementException occurred!')
            cc = np.nan
        else:
            pass
        finally:
            # Parse the details
            views = views.text.split('\n')
            released = [x for x in views if x.endswith('s ago')]
            views = [x for x in views if x.endswith(' views')]
            # Append this video's details to the list
            data.append([
                vid_url.split('v=')[1],
                ch.text,
                subs.text,
                title.text, cc, vid_url,
                released[0] if len(released) != 0 else np.nan,
                views[0] if len(views) != 0 else np.nan,
            ])

    # Close chrome
    driver.close()
    # Generate & return the dataframe
    return pd.DataFrame(data, columns=dataframe_cols)
