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

TARGET = 'https://orgsync.com/412/community/calendar?view=upcoming'

print('Setting up user agent...')
#################################
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = USER_AGENT

print('Setting up Phantom JS webdriver...')
###########################################
browser = webdriver.PhantomJS(desired_capabilities=dcap)

print('Fetching - ', TARGET)
############################
browser.get('https://orgsync.com/412/community/calendar?view=upcoming')

print('Waiting for JS to load...')
##################################
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'osw-events-list-date')))
events_module = browser.find_element_by_class_name('osw-events-index-main')
print('Found events module')

# Constants specific to Orgsync DOM
DATE_CLASS = 'osw-events-list-date'
EVENT_CLASS = 'osw-events-list-item-content'
TITLE_CLASS = 'osw-events-list-date-header'
NAME_CLASS = 'osw-events-list-item-title'
TIME_CLASS = 'osw-events-list-item-time'
ORG_CLASS = 'osw-events-list-item-portal-name'

# Parse remaining with BS4
html = events_module.get_attribute('outerHTML')
soup = BeautifulSoup(html, 'html.parser')
dates = soup.find_all('div', attrs={'class': DATE_CLASS})
calendar = []
for item in dates: # <class 'bs4.element.Tag'>
    title = item.find('div', attrs={'class', TITLE_CLASS})
    events = item.findAll('a', attrs={'class': EVENT_CLASS})
    event_list = EventList(title.text, [])
    for entry in events: # Events in November 18th, 2016 <- example
        name = entry.find('div', attrs={'class': NAME_CLASS}).text
        time = entry.find('span', attrs={'class': TIME_CLASS}).text
        organization = entry.find('span', attrs={'class': ORG_CLASS}).text
        img = ''
        try: # Some events don't have images
            img = entry.find('img')['src']
        except Exception:
            event_list.errors.append('Missing image for event: {}'.format(name))
        event = Event(name, time, organization, img)
        event_list.events.append(event)
    print(json.dumps({'results': event_list.to_json()}, indent=4, sort_keys=True))

browser.close()



