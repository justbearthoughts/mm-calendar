from io import BytesIO
import math
from PIL import Image
import discord
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import FirefoxOptions
from time import sleep
from datetime import datetime

HOOK_ID = 1234
HOOK_SECRET = 'abcd'

try:
    options = FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.maximize_window()
    browser.get('https://www.investing.com/economic-calendar/')
    sleep(2)
    btn = browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
    btn.click()
    sleep(1)
    element = browser.find_element('xpath', '//*[@id="economicCalendarData"]')
    location = element.location
    size = element.size
    total_height = element.size["height"]+1000
    browser.set_window_size(1920, total_height)
    sleep(1)
    png = browser.get_screenshot_as_png()
    browser.quit()
    img = Image.open(BytesIO(png))
    arr = BytesIO()

    left = location['x'] + 270
    top = location['y']
    right = location['x'] + 290 + size['width']
    bottom = location['y'] + 50 + size['height']

    img = img.crop((math.floor(left), math.floor(top), math.ceil(right), math.ceil(bottom)))

    img.save(arr, format='PNG')
    arr.seek(0)
    picture = discord.File(arr, 'calendar.png')
    webhook = discord.Webhook.partial(HOOK_ID, HOOK_SECRET, adapter=discord.RequestsWebhookAdapter())

    webhook.send(F'**Financial Calender for {datetime.now().date().strftime("%Y/%m/%d")}**', username='Financial Calender', file=picture)
except NoSuchElementException:
    picture = None