__author__ = 'Anonymous'

from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path='C:\\Python27\\chromedriver.exe')
#driver.set_window_size(600, 600)
driver.get("http://gis.nyc.gov/doitt/nycitymap/")
driver.find_element_by_xpath('//*[@id="wm_widget_ZoomSlider_0"]/div[2]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="wm_widget_ZoomSlider_0"]/div[2]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="wm_widget_ZoomSlider_0"]/div[2]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="wm_widget_ZoomSlider_0"]/div[2]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="wm_widget_ZoomSlider_0"]/div[2]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="wm_widget_ZoomSlider_0"]/div[2]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="dijit_form_CheckBox_3"]').click()
time.sleep(10)
driver.quit()