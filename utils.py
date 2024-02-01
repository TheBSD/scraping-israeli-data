from typing import List
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Firefox(service=Service(executable_path = "./geckodriver"))
driver.fullscreen_window()

def data_from_person(person: WebElement):
    image = person.find_element(By.CLASS_NAME, "person-img").get_attribute("src")
    company_logo = person.find_element(By.CLASS_NAME, "person-logo").get_attribute("src")
    profile_link = person.find_element(By.CLASS_NAME, "person-padding").get_attribute("href")
    name = person.find_element(By.CLASS_NAME, "person-name").text
    title = person.find_element(By.CLASS_NAME, "person-title").text
    location = person.find_element(By.CSS_SELECTOR, '[fs-cmsfilter-field="location"]').text
    company_name = person.find_element(By.CSS_SELECTOR, '[fs-cmsfilter-field="company"]').text
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

def dump_to_json(array: List[dict], file_name: str):
    with open(f"{file_name}.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(array, indent=4))
