from selenium import webdriver
from time import sleep

browser = webdriver.Firefox()
sleep(1)
browser.get('http://localhost:8000')

assert 'Django' in browser.title