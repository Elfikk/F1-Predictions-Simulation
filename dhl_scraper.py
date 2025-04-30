import bs4
import requests

# Selenium
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dhl_site = "https://inmotion.dhl/en/formula-1/fastest-pit-stop-award"

visited = set()
all_visited = False

driver = webdriver.Firefox()
driver.get(dhl_site)
try:
    print("hi")
    consent_buttons = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.TAG_NAME, "button")) #This is a dummy element
    )
    print(consent_buttons)
    for button in consent_buttons:
        print(button.text)
        if button.text == "Accept All":
            button.click()

    # consent_buttons.click()



    choose_event_button = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".button.button--secondary")) #This is a dummy element
    )
    choose_event_button.click()

    radio_buttons = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".form-element")) #This is a dummy element
    )

    print(radio_buttons)


finally:
    driver.quit()



# html_content = requests.get(dhl_site).text
# da_soup = bs4.BeautifulSoup(html_content, "html.parser")

# # topic_navigation = da_soup.find_all("table")
# # for tag in topic_navigation:
# #     print(tag)

# with open("scraped.html", "w", encoding="utf-8") as f:
#     f.write(html_content)
#     f.close()