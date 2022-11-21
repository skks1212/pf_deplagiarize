from selenium import webdriver
from selenium.webdriver.common.by import By
from review import review
from decouple import config
import time
from playsound import playsound
import os
l4_review_link = "https://www.pupilfirst.school/courses/1804/review?sortCriterion=SubmittedAt&levelId=4438&tab=Pending"

pf_link = "https://pupilfirst.school"
pf_session = config("SESSION_KEY")

driver = webdriver.Edge(r"msedgedriver.exe")

driver.get(pf_link)
driver.add_cookie({"name": "_pupilfirst_session", "value": pf_session})
driver.get(l4_review_link)

def start(index = 0):
    try:
        for i in range(index):
            driver.find_element(By.XPATH, '//*[@id="app-router"]/div/div[3]/div[2]/div[3]/div/div/div[2]/button').click()
            time.sleep(2)
        time.sleep(2)
        submissions_wrapper = driver.find_element(By.ID, "submissions")
        submissions = submissions_wrapper.find_elements(By.TAG_NAME, "a")
        for i in range((index * 20), len(submissions)):
            submission = submissions[i]
            print("Reviewing submission " + submission.get_attribute("href"))
            review(driver, submission)
        start(index + 1)
    except:
        audio_file = os.path.dirname(__file__) + "/buzzer.wav"
        playsound(audio_file)

start()

driver.quit()