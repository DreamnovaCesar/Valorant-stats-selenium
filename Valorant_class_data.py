import os
import string
import numpy as np
import pandas as pd

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

#URL:str  = "https://dak.gg/valorant/en/profile/DSP%20KimGyuTae-1111"
#URL:str  = r"https://dak.gg/valorant/en/profile/walle-cotta"
#URL:str  = r"https://dak.gg/valorant/en/profile/ilsoto-beth3"
URL:str  = r"https://dak.gg/valorant/en/profile/tabwesley-saya"

#Cotta_user_name:str = 'aAa cutefatb0y#fat'

class ValorantWebScrapping:

    def __init__(self, **kwargs) -> None:

        # * Instance attributes
        self.URL = kwargs.get('url', None)
        self.Path_chrome_driver = r"C:\Users\Cesar\Dropbox\PC\Desktop\chromedriver.exe"

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
    
    def extract_info_agents_valorant(self):

        XPATH_button_update = '//*[@id="__next"]/main/div[4]/header/div/div/div[1]/button[1]'

    def extract_info_tables_valorant(self):

        # * General parameters
        Agents = 'Agents'
        Maps = 'Maps'

        # *
        Time_wait_value = 1
        Header_list = []

        # *
        Tables_info = (Agents, Maps)

        XPATH_button_update = '//*[@id="__next"]/main/div[4]/header/div/div/div[1]/button[1]'
        XPATH_button_maps = '//*[@id="__next"]/main/div[4]/ul[2]/li[2]/button'

        XPATH_name = '//*[@id="__next"]/main/div[4]/header/div/div/h2/span[1]'
        XPATH_table = '//*[@id="__next"]/main/div[4]/div[1]/table'
        XPATH_table_competitive = '//*[@id="__next"]/main/div[4]/dl/div[1]'

        #XPATH_write_name:str = '//*[@id="__next"]/main/section/div/form/input'
        #XPATH_write_name_button:str = '//*[@id="__next"]/main/section/div/form/button/svg'
        
        # * Webdriver chrome activate
        Driver = webdriver.Chrome(Path_chrome_driver)
        Driver.get(self.URL)

        # * Waiting time
        Driver.implicitly_wait(Time_wait_value)
        
        Button_click_update = Driver.find_element(By.XPATH, XPATH_button_update)
        Button_click_update.click()
        
        time.sleep(4)

        # * Find name
        Player_name = Driver.find_element(By.XPATH, XPATH_name).text
        
        # * Table competitive
        Table_competitive = Driver.find_element(By.XPATH, XPATH_table_competitive)
        Table_competitive_header_ranking = Table_competitive.find_element(By.TAG_NAME, 'div')
        Table_competitive_scores = Table_competitive.find_element(By.TAG_NAME, 'dd')

        Table_competitive_header_mode = Table_competitive_header_ranking.find_elements(By.TAG_NAME, 'strong')
        Table_competitive_header_score = Table_competitive_header_ranking.find_elements(By.TAG_NAME, 'p')

        Table_competitive_scores_cells = Table_competitive_scores.find_elements(By.TAG_NAME, 'div')

        for Index, Row in enumerate(Table_competitive_scores_cells):

            Columns = Table_competitive_scores_cells[Index].find_elements(By.TAG_NAME, 'dt')
            Columns = Table_competitive_scores_cells[Index].find_elements(By.TAG_NAME, 'span')

        if Table_chosen is Maps:

            Button_click_map = Driver.find_element(By.XPATH, XPATH_button_maps)
            Button_click_map.click()

        Table_search = Driver.find_element(By.XPATH, XPATH_table)
        Header_row = Table_search.find_element(By.TAG_NAME, 'tr')

        Header_row_agent = Header_row.find_element(By.TAG_NAME, 'th').text
        Header_get_column = Header_row.find_elements(By.TAG_NAME, 'th')

        #print(Header_row_agent)
        Header_list.append(Header_row_agent)

        for i, Row in enumerate(Header_get_column):

            Columns = Header_get_column[i].find_elements(By.TAG_NAME, 'span')

            for k, Column in enumerate(Columns):

                #print('[' + str(k) + ']' + ' ////// ' + str(Column.text))
                Header_list.append(Column.text)

        Table_search_body = Table_search.find_element(By.TAG_NAME, 'tbody')
        Table_search_body_rows = Table_search_body.find_elements(By.TAG_NAME, 'tr')

        for i, Row in enumerate(Table_search_body_rows):

            Table_columns = Table_search_body_rows[i].find_elements(By.TAG_NAME, 'td')

        Table_info = np.full([len(Table_search_body_rows), len(Table_columns)], None)

        for i, Row in enumerate(Table_search_body_rows):

            Columns = Table_search_body_rows[i].find_elements(By.TAG_NAME, 'td')

            for j, Column in enumerate(Columns):

                #print('[' + str(i) + ']' + '[' + str(j) + ']' + ' ////// ' + str(Column.text))
                Table_info[i][j] = Column.text

        Header_list_filtered = list(filter(None, Header_list))

        #print(Header_list_filtered)

        Dataframe_table_header = pd.DataFrame(columns = Header_list_filtered)
        Dataframe_table_info = pd.DataFrame(Table_info)

        Dataframe_table_info.columns = Dataframe_table_header.columns
        Dataframe_table_header_info = pd.concat([Dataframe_table_header, Dataframe_table_info], ignore_index = True, sort = False)

        # * Save dataframe in the folder given
        #Dataframe_save_mias_name = 'Biclass_' + 'Dataframe_' + 'CNN_' + str(Technique) + '_' + str(Model_name_letters) + '.csv'
        Dataframe_save = 'Dataframe_' + str(Header_row_agent) + '_' + str(Player_name) + '.csv'
        Dataframe_save_folder = os.path.join(r'C:\Users\Cesar\Desktop\Python software\Web scraping', Dataframe_save)

        Dataframe_table_header_info.to_csv(Dataframe_save_folder)

        Driver.quit()

        