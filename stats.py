import os
from re import I
from tkinter import Button
from jmespath import search
from matplotlib.pyplot import text

import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import datetime

x = datetime.datetime.now()
print(x)

import time
import numpy as np

from selenium import webdriver

#URL:str  = "https://dak.gg/valorant/en/profile/DSP%20KimGyuTae-1111"
#URL:str  = r"https://dak.gg/valorant/en/profile/walle-cotta"
#URL:str  = r"https://dak.gg/valorant/en/profile/ilsoto-beth3"
URL:str  = r"https://dak.gg/valorant/en/profile/tabwesley-saya"

#URL:str  = r"https://dak.gg/valorant/en"

Path_chrome_driver:str = r"C:\Users\Cesar\Dropbox\PC\Desktop\chromedriver.exe"

XPATH_button:str = '//*[@id="__next"]/main/div[4]/ul[2]/li[2]/button'
XPATH_name:str = '//*[@id="__next"]/main/div[4]/header/div/div/h2/span[1]'
XPATH_table:str = '//*[@id="__next"]/main/div[4]/div[2]/table'

XPATH_write_name:str = '//*[@id="__next"]/main/section/div/form/input'
XPATH_write_name_button:str = '//*[@id="__next"]/main/section/div/form/button/svg'

Maps:str = 'Maps'
Agents:str = 'Agents'

#Cotta_user_name:str = 'aAa cutefatb0y#fat'

def extract_info_tables_valorant(URL, Path_chrome_driver, XPATH_name, XPATH_button, XPATH_table, Table_chosen):
    
    Player_name:str = ''
    Time_wait_value:int = 1
    Header_list:list = []
    
    Driver = webdriver.Chrome(Path_chrome_driver)
    Driver.get(URL)

    Driver.implicitly_wait(Time_wait_value)

    """
    Agent_name = Driver.find_element(By.TAG_NAME, 'input')
    Agent_name_click = Driver.find_element(By.NAME, XPATH_write_agent_button)

    Agent_name.send_keys(Agent_name_player)
    Agent_name_click.click()
    """
   
    Player_name = Driver.find_element(By.XPATH, XPATH_name).text

    if Table_chosen is Maps:

        Button_click_map = Driver.find_element(By.XPATH, XPATH_button)
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

extract_info_tables_valorant(URL, Path_chrome_driver, XPATH_name, XPATH_button, XPATH_table, Agents)
extract_info_tables_valorant(URL, Path_chrome_driver, XPATH_name, XPATH_button, XPATH_table, Maps)


@Utilities.time_func
    def extract_info_agents_valorant(self):

        # *
        XPATH_button_update = '//*[@id="__next"]/main/div[4]/header/div/div/div[1]/button[1]'
        XPATH_player_name = '//*[@id="__next"]/main/div[4]/header/div/div/h2/span[1]'
        XPATH_stats_table = '//*[@id="__next"]/main/div[4]/div[2]/table'

        # * Webdriver chrome activate
        Driver = webdriver.Chrome(self.Path_chrome_driver)
        Driver.get(self.URL)

        # * Waiting time
        Driver.implicitly_wait(self.Time_wait_value)
        
        # *
        Button_click_update = Driver.find_element(By.XPATH, XPATH_button_update)
        Button_click_update.click()

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

        # * Save dataframe in the folder given
        self.save_figure(self.Save_dataframe, Dataframe_table_complete, XPATH_player_name, Header_row_agent, self.Folder_path)

        Driver.quit()