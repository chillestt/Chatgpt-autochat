import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
# from extract_examples import Extract_Examples
from webdriver_manager.chrome import ChromeDriverManager


prompts = pd.read_csv("writing_task2_prompts.csv")

op = webdriver.ChromeOptions()
op.add_argument(f"user-agent={UserAgent.random}")
op.add_argument("user-data-dir=./")
op.add_experimental_option("detach", True)
op.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = uc.Chrome(chrome_options=op)

MAIL = "-------------------------"
PASSWORD = "-------------------------------"
PATH = "/home/imnitin/code_snippets/tweets_scrapping/chromedriver"

# get to the web
driver.get('https://chat.openai.com/auth/login')
sleep(3)

inputElements = driver.find_elements(By.TAG_NAME, "button")
inputElements[0].click()
sleep(3)

# input email
mail = driver.find_elements(By.TAG_NAME,"input")[1]
mail.send_keys(MAIL)
btn=driver.find_elements(By.TAG_NAME,"button")[0]
btn.click()

# input password
password= driver.find_elements(By.TAG_NAME,"input")[2]
password.send_keys(PASSWORD)
sleep(3)

# wait until the login button active
wait = WebDriverWait(driver, 10)
btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_button-login-password")))
btn.click()
sleep(10)

# find element with specific text
# href = /c/3f08462d-89c4-4748-a71e-19bd7d1ffff6
# element = driver.find_elements("xpath", "//[contains(text(), 'Evaluate writing essays: IELTS')]")
try:
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, "Evaluate writing essays: IELTS"))
    )
    link[0].click()
except:
    driver.quit()


def send_prompt(prompt):
   inputElements = driver.find_elements(By.TAG_NAME, "textarea")
   inputElements[0].send_keys(prompt)
   wait = WebDriverWait(driver, 10)
   btn = wait.until(EC.element_to_be_clickable(inputElements[0]))
   btn.send_keys(Keys.ENTER)
   # inputElements[0].send_keys(Keys.ENTER)
   sleep(10)
   inputElements = driver.find_elements(By.TAG_NAME, "p")
   content = inputElements[0]
   sleep(5)
   return content


result = []
for i in range(3):
   content = send_prompt(prompts["prompt"][i])
   result.append([prompt, content])