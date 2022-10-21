import os
import string
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import time
import datetime

from tkinter import Button
from jmespath import search
from matplotlib.pyplot import text

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functools import wraps

#URL  = r"https://dak.gg/valorant/en/profile/DSP%20KimGyuTae-1111"
#URL  = r"https://dak.gg/valorant/en/profile/walle-cotta"
URL  = r"https://dak.gg/valorant/en/profile/ilsoto-beth3"
#URL = r"https://dak.gg/valorant/en/profile/tabwesley-saya"

#Cotta_user_name:str = 'aAa cutefatb0y#fat'

class Utilities(object):

    @staticmethod  # no default first argument in logger function
    def time_func(func):  # accepts a function
        @wraps(func)  # good practice https://docs.python.org/2/library/functools.html#functools.wraps
        def wrapper(self, *args, **kwargs):  # explicit self, which means this decorator better be used inside classes only

            t1 = time.time()
            result = func(self, *args, **kwargs)
            t2 = time.time()
            #print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
            print("\n")
            print("*" * 60)

            print('Function {} executed in {:.4f}'.format(func.__name__, t2 - t1))

            print("*" * 60)
            print("\n")

            return result
        return wrapper

    @staticmethod  # no default first argument in logger function
    def chrome_window_settings(func):  # accepts a function
        @wraps(func)  # good practice https://docs.python.org/2/library/functools.html#functools.wraps
        def wrapper(self, *args, **kwargs):  # explicit self, which means this decorator better be used inside classes only
            
            # *
            Agents = 'Agents'
            Weapon = 'Weapon'
            Maps = 'Maps'

            # *
            XPATH_button_update = '//*[@id="__next"]/main/div[4]/header/div/div/div[1]/button[1]'
            XPATH_button_maps = '//*[@id="__next"]/main/div[4]/ul[2]/li[2]/button'
            XPATH_button_Act_1 = '//*[@id="__next"]/main/div[4]/header/dl/div[2]/dd[1]/a'

            # * Webdriver chrome activate
            Driver = webdriver.Chrome(self.Path_chrome_driver)
            Driver.get(self.URL)

            # * Waiting time
            Driver.implicitly_wait(self.Time_wait_value)

            # *
            Button_click_Act_1 = Driver.find_element(By.XPATH, XPATH_button_Act_1)
            Button_click_Act_1.click()

            # *
            Button_click_update = Driver.find_element(By.XPATH, XPATH_button_update)
            Button_click_update.click()

            # *
            if(self.Table_chosen is Maps):

                Button_click_map = Driver.find_element(By.XPATH, XPATH_button_maps)
                Button_click_map.click()

            result = func(self, Driver)

            Driver.quit()

            return result
        return wrapper

class ValorantWebScrapping(object):

    def __init__(self, **kwargs) -> None:

        # * Instance attributes
        self.URL = kwargs.get('url', None)
        self.Folder_path = kwargs.get('folder', None)
        self.Save_dataframe = kwargs.get('SD', None)
        self.Table_chosen = kwargs.get('table', None)
        
        # *
        self.Path_chrome_driver = r"C:\Users\Cesar\Dropbox\PC\Desktop\New folder\chromedriver.exe"
        self.Time_wait_value = 6
        self.Header_list = []

        # * Folder attribute (ValueError, TypeError)
        if self.URL == None:
            raise ValueError("url does not exist") #! Alert

    def __repr__(self):

        kwargs_info = "{}".format(self.URL)

        return kwargs_info

    def __str__(self):
        pass
    
    # * URL attribute
    @property
    def URL_property(self):
        return self.URL

    @URL_property.setter
    def URL_property(self, New_value):
        if not isinstance(New_value, str):
            raise TypeError("URL must be a string") #! Alert
        self.URL = New_value
    
    @URL_property.deleter
    def URL_property(self):
        print("Deleting URL...")
        del self.URL
    
    # * Path_chrome_driver attribute
    @property
    def Path_chrome_driver_property(self):
        return self.Path_chrome_driver

    @Path_chrome_driver_property.setter
    def Path_chrome_driver_property(self, New_value):
        self.Path_chrome_driver = New_value

    # ? Decorator
    @staticmethod
    def save_figure(Save_figure: bool, Dataframe: pd.DataFrame, XPATH_player_name: str, Name_header: str, Folder_path: str) -> None:

        if(Save_figure == True):
            
            Dataframe_save = 'Dataframe_{}_{}.csv'.format(Name_header, XPATH_player_name)
            Dataframe_save_folder = os.path.join(Folder_path, Dataframe_save)
            Dataframe.to_csv(Dataframe_save_folder)

        else:
            pass
    

    @Utilities.time_func
    @Utilities.chrome_window_settings
    def extract_info_table_valorant(self, Driver):
        
        # *
        XPATH_stats_table = '//*[@id="__next"]/main/div[4]/div[2]/table'
        XPATH_player_name = '//*[@id="__next"]/main/div[4]/header/div/div/h2/span[1]'

        # *
        Player_name = Driver.find_element(By.XPATH, XPATH_player_name).text

        # *
        Table_search = Driver.find_element(By.XPATH, XPATH_stats_table)
        Header_row = Table_search.find_element(By.TAG_NAME, 'tr')

        # *
        Header_row_agent = Header_row.find_element(By.TAG_NAME, 'th').text
        Header_get_column = Header_row.find_elements(By.TAG_NAME, 'th')
        
        # *
        self.Header_list.append(Header_row_agent)

        # *
        for i, Row in enumerate(Header_get_column):

            Columns = Header_get_column[i].find_elements(By.TAG_NAME, 'span')

            for k, Column in enumerate(Columns):

                #print('[' + str(k) + ']' + ' ////// ' + str(Column.text))
                self.Header_list.append(Column.text)

        # *
        Table_search_body = Table_search.find_element(By.TAG_NAME, 'tbody')
        Table_search_body_rows = Table_search_body.find_elements(By.TAG_NAME, 'tr')

        # * Get the data from each row
        for i, Row in enumerate(Table_search_body_rows):

            Table_columns = Table_search_body_rows[i].find_elements(By.TAG_NAME, 'td')

        # * Create a table full of None
        Table_info = np.full([len(Table_search_body_rows), len(Table_columns)], None)

        # * Data search of the body table and save the values inside the Table_info
        for i, Row in enumerate(Table_search_body_rows):

            Columns = Table_search_body_rows[i].find_elements(By.TAG_NAME, 'td')

            for j, Column in enumerate(Columns):
                #print('[' + str(i) + ']' + '[' + str(j) + ']' + ' ////// ' + str(Column.text))
                Table_info[i][j] = Column.text

        # * Filter the header list
        Header_list_filtered = list(filter(None, self.Header_list))

        # * Create a dataframe with the header we got early.
        Dataframe_table_header = pd.DataFrame(columns = Header_list_filtered)
        Dataframe_table_info = pd.DataFrame(Table_info)

        # * Concat table body with headers
        Dataframe_table_info.columns = Dataframe_table_header.columns
        Dataframe_table_complete = pd.concat([Dataframe_table_header, Dataframe_table_info], ignore_index = True, sort = False)
        print(Dataframe_table_complete)

        # * Save dataframe in the folder given
        self.save_figure(self.Save_dataframe, Dataframe_table_complete, Player_name, Header_row_agent, self.Folder_path)


f = ValorantWebScrapping(url = URL, folder = r'C:\Users\Cesar\Desktop\Python software\Web scraping', SD = True, table = 'Maps')

f.extract_info_table_valorant()
#f.extract_info_agents_valorant()