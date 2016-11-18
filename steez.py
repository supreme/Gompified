#!/usr/bin/env python3

"""Pulls WPI's daily campus events from orgsync."""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
from modules.Event import Event
from modules.EventList import EventList

target = 'https://orgsync.com/412/community/calendar?view=upcoming'

print('Setting up user agent...')
#################################
user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent

print('Setting up Phantom JS webdriver...')
###########################################
browser = webdriver.PhantomJS(desired_capabilities=dcap)

print('Fetching - ', target)
############################
browser.get('https://orgsync.com/412/community/calendar?view=upcoming')

print('Waiting for JS to load...')
##################################
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'osw-events-list-date')))
events_module = browser.find_element_by_class_name('osw-events-index-main')
print('Found events module')

# Constants specific to Orgsync DOM
find_date = {'name': 'div', 'attrs': {'class': 'osw-events-list-date'}}
find_events = {'name': 'a', 'attrs': {'class': 'osw-events-list-item-content'}}
title_class = 'osw-events-list-date-header'
name_attr = {'name': 'div', 'attrs': {'class': 'osw-events-list-date'}}
date_attr = {'name': 'div', 'attrs': {'class': 'osw-events-list-date'}}

def find(tag, attr_type, attr_name, attr_val):
    return tag.find_all(attr_type, attrs=dict([(attr_name, attr_val)]))

# Parse remaining with BS4
html = events_module.get_attribute('outerHTML')
soup = BeautifulSoup(html, 'html.parser')
dates = soup.find_all('div', attrs={'class': 'osw-events-list-date'})
calendar = []
for item in dates: # <class 'bs4.element.Tag'>
    title = item.find('div', attrs={'class', title_class})
    events = item.findAll('a', attrs={'class': 'osw-events-list-item-content'})
    event_list = EventList(title.text, [])
    for entry in events: # Events in November 18th, 2016 <- example
        name = entry.find('div', attrs={'class': 'osw-events-list-item-title'}).text
        time = entry.find('span', attrs={'class': 'osw-events-list-item-time'}).text
        organization = entry.find('span', attrs={'class': 'osw-events-list-item-portal-name'}).text
        img = ''
        try: # Some events don't have images
            img = entry.find('img')['src']
        except Exception:
            event_list.errors.append('Missing image for event: {}'.format(name))
        event = Event(name, time, organization, img)
        event_list.events.append(event)
    print(json.dumps(event_list.to_json(), indent=4, sort_keys=True))

browser.close()



