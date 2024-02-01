from datetime import datetime
from utils import List, driver, By, data_from_person, dump_to_json

url = "https://www.techaviv.com"
start_time = datetime.now()
driver.get(f"{url}/members")

club_members: List[dict] = []
try:
    while load_more_button := driver.find_element(by=By.LINK_TEXT, value="Load More"):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more_button.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(3)
except:
    persons = driver.find_elements(By.CLASS_NAME, value="person-item")
    for person in persons:
        # TODO Abdullah: save/download the member's photo and company's photo
        club_members.append(data_from_person(person))

driver.quit()

dump_to_json(array=club_members, file_name="club_members")

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
