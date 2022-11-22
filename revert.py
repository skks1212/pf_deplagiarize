import json
import os
import time
from selenium.webdriver.common.by import By
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Edge(r"msedgedriver.exe")
pf_link = "https://pupilfirst.school"
pf_session = config("SESSION_KEY")
driver.get(pf_link)
driver.add_cookie({"name": "_pupilfirst_session", "value": pf_session})

with open("verdicts.json") as f:
    data = json.load(f)
    c = 0
    for i in reversed(list(data.keys())):
        
        sub = data[i]
        if sub["verdict"]:
            driver.get(i)
            time.sleep(2)
            try:
                driver.find_element(By.XPATH, '//*[@id="app-router"]/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div/button').click()
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
            except:
                pass
            c += 1

    print(c)