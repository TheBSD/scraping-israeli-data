import os
import requests
from utils import write_json
from bs4 import BeautifulSoup

results_dir = "../results"


def get_soup_object(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")


def scrap_management_page():
    page_url = "https://startupnationcentral.org/management"
    soup = get_soup_object(page_url)

    members = []
    section_title = soup.find("h2", {"class": "section_title"}).get_text()
    team_members = soup.select("div.team_member_col")

    for item in team_members:
        members.append({
            "name": item.find("h3", {"class": "team_member_name"}).get_text().strip(),
            "position": item.find("p", {"class": "team_member_position"}).get_text().strip(),
            "img_src": item.find("div", {"class": "team_member_image"}).img["src"].strip()
        })

    return {"section_title": section_title, "page_url": page_url, "members": members}


if __name__ == '__main__':
    # crawl & save /management
    management_results = scrap_management_page()
    full_file_path = os.path.join(results_dir, "management.json")
    write_json(management_results, full_file_path)
