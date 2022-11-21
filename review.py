from selenium.webdriver.common.by import By
from decouple import config
import time
from verdict import get_verdict
import json
l4_review_link = "https://www.pupilfirst.school/courses/1804/review?sortCriterion=SubmittedAt&levelId=4438&tab=Pending"
form_link = "https://forms.gle/QktPeSaQB1b9eSku5"
name = config("NAME")

plagiarism_message = '''
**This code looks very similar to existing solutions we've reviewed.**

I noticed that there is code in this submission that is likely to have been taken from another source. **If you're certain that this isn't the case**, then please ignore the next paragraphs.

To make the best out of the course, you have to write the code yourselves fully. Unfortunately, there is no shortcut to getting good at programming other than writing thousands of lines of code, making mistakes and struggling. We're happy to help if you have any questions in the process, but only you can put in the necessary effort. As always, if you have any doubts regarding how to complete this task, please reach out to us on the Web Development community, here on Pupilfirst School, or on the Discord server.

We also make a note of all submissions where plagiarism is suspected and report to the respective institution. Your submission for the Capstone project will undergo stricter review under such circumstances. If plagiarism is confirmed, no course completion certificate will be issued. 

We encourage you to go through the lessons in this level, work on your *own solution* for this assignment and submit again.

---
'''

def review(driver, submission):
    submission_link = submission.get_attribute("href")

    with open("verdicts.json", "r") as f:
        data = json.load(f)
        if submission_link in data.keys():
            print("Already reviewed")
            return

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(submission_link)
    time.sleep(2)

    check_if_button_present = driver.find_elements(By.XPATH, "//button[contains(text(), 'Yes, Assign Me')]")
    if len(check_if_button_present) > 0:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return

    github_link = driver.find_element(By.CSS_SELECTOR, "a.border-blue-400").get_attribute("href")

    verdict = get_verdict(github_link)

    print(verdict)

    if verdict["verdict"]:
        student_link = driver.find_element(By.XPATH, '//span[text()="Submitted by "]').find_element(By.XPATH, "..").find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[2])
        driver.get(student_link)
        time.sleep(2)
        student_id = driver.find_element(By.CSS_SELECTOR, ".text-sm.underline").text
        student_id = student_id.split("#")[1]
        driver.get(form_link)
        time.sleep(5)
        values = [
            name,
            student_id,
            submission_link,
            "4"
        ]
        for i in range(1, len(values) + 1):
            xpath = f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[{i}]/div/div/div[2]/div/div[1]/div/div[1]/input'
            driver.find_element(By.XPATH, xpath).send_keys(values[i - 1])
            print(i)
        
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/textarea').send_keys(
            verdict["message"] + " (" + str(verdict["percent"]) + "% match)"
        )
        
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()

        driver.close()
        driver.switch_to.window(driver.window_handles[1])

        try:
            driver.find_element(By.XPATH, '//button[text()="Start Review"]').click()
        except:
            pass
        
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Markdown editor"]').send_keys(plagiarism_message)
        driver.find_element(By.XPATH, '//*[@id="app-router"]/div/div/div[2]/div[2]/div/div[4]/div[2]/div/div[1]/div/div/div[2]/button[4]').click()
        driver.find_element(By.XPATH, '//*[@id="app-router"]/div/div/div[2]/div[2]/div/div[5]/button').click()

    with open("verdicts.json", "r") as f:
        data = json.load(f)
        data[submission_link] = verdict
        with open("verdicts.json", "w") as f:
            json.dump(data, f)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])