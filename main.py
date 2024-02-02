from datetime import datetime
from utils import List, driver, By, data_from_person, dump_to_json, download_image

url = "https://www.techaviv.com"
start_time = datetime.now()
driver.get(f"{url}/members")

club_members: List[dict] = []
try:
    while load_more_button := driver.find_element(by=By.LINK_TEXT, value="Load More"):
        load_more_button.click()
except:
    persons = driver.find_elements(By.CLASS_NAME, value="person-item")
    for person in persons:
        club_members.append(data_from_person(person))
        _person = club_members[-1]
        download_image(
            url=_person.get("image"), 
            file_name=f"{_person.get('name')}.{_person.get('image').split('.')[-1]}"
        )
        download_image(
            url=_person.get("company_logo"),
            file_name=f"{_person.get('name')}'s company ({_person.get('company_name')}) logo.{_person.get('company_logo').split('.')[-1]}"
        )

driver.quit()

dump_to_json(array=club_members, file_name="club_members")

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
