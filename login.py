#coding:utf-8
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized");
chrome_options.add_argument("--window-position=1367,0");
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
#if mobile_emulation:
#   chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome("/Users/zhtian/Downloads/chromedriver", 
                                  chrome_options = chrome_options)

driver.get('http://qzone.qq.com')
driver.switch_to_frame('login_frame')
driver.find_element_by_id('switcher_plogin').click()
driver.find_element_by_id('u').clear()
driver.find_element_by_id('u').send_keys('747674262')
driver.find_element_by_id('p').clear()
driver.find_element_by_id('p').send_keys('xxxxxx')
driver.find_element_by_id('login_button').click()

# driver.quit()