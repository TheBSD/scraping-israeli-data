from typing import List
import json
import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options

firefox_options = Options()
firefox_options.add_argument("-headless")

# TODO Abdullah: Create factory to get driver for firefox, chrome ... etc browsers based on the given arg.
driver = webdriver.Firefox(
    service=Service(executable_path = "./geckodriver"),
    options=firefox_options,
)

def data_from_person(person: WebElement):
    name = person.find_element(By.CLASS_NAME, "person-name").text
    title = person.find_element(By.CLASS_NAME, "person-title").text
    profile_link = person.find_element(By.CLASS_NAME, "person-padding").get_attribute("href")
    image = person.find_element(By.CLASS_NAME, "person-img").get_attribute("src") or "No Profile Photo"
    location = person.find_element(By.CSS_SELECTOR, '[fs-cmsfilter-field="location"]').text
    company_name = person.find_element(By.CSS_SELECTOR, '[fs-cmsfilter-field="company"]').text
    company_logo = person.find_element(By.CLASS_NAME, "person-logo").get_attribute("src") or "No Company Logo"
    company_url = person.find_element(By.CLASS_NAME, "person-company-link").get_attribute("href")
    return {
        "name": name,
        "title": title,
        "profile_link": profile_link,
        "image": image,
        "location": location,
        "company_name": company_name,
        "company_logo": company_logo,
        "company_url": company_url,
    }

def download_image(url: str, file_name: str):
    if os.path.exists(f"images/{file_name}") or url in ("No Profile Photo", "No Company Logo"):
        return
    
    response = requests.get(url)
    if response.status_code == 200:
        image_content = response.content
        with open(f"images/{file_name}", "wb") as file:
            file.write(image_content)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def dump_to_json(array: List[dict], file_name: str):
    with open(f"{file_name}.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(array, indent=4))

if not os.path.exists("images"):
    os.makedirs("images")
