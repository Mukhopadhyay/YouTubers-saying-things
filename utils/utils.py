import numpy as np
import pandas as pd
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

URL: str = 'https://www.youtube.com/c/{}/videos?view=0&sort=p&flow=grid'
dataframe_cols: list = ['Title', 'CC', 'URL', 'Released', 'Views']

def get_channel_info(channel: str, driver_path: str, verbose: Optional[bool] = False) -> pd.DataFrame:
    # Chrome driver
    driver = webdriver.Chrome(driver_path)

    # List to store the video details
    data = []

    # Navigate to the YouTube channel
    driver.get(URL.format(channel))

    channel_name = driver.find_element_by_xpath('//yt-formatted-string[@class="style-scope ytd-channel-name"]')
    subscribers = driver.find_element_by_xpath('//yt-formatted-string[@id="subscriber-count"]')

    print("Channel Name: {}".format(channel_name.text))
    print("Subscribers: {}".format(subscribers.text))

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
            data.append(
                [
                    title.text, cc, vid_url,
                    released[0] if len(released) != 0 else np.nan,
                    views[0] if len(views) != 0 else np.nan,
                ]
            )
    # Close chrome
    driver.close()
    # Generate & return the dataframe
    return pd.DataFrame(
        data, columns=dataframe_cols
    )
