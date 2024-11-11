from selenium import webdriver	 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import argparse

parser = argparse.ArgumentParser(description='Run the Claude for Computer Use.')
parser.add_argument('--test', type=str, default='captcha/captcha-1', help='Test data file to run')

args = parser.parse_args()

# Creating an instance webdriver
options = webdriver.ChromeOptions()

# To access localhost
options.add_argument("proxy-bypass-list=<-loopback>")
driver = webdriver.Chrome(options=options)
driver.get("http://localhost:8080")
driver.implicitly_wait(10)
# switch to iframe (chat app)
iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src='http://localhost:8501']")
driver.switch_to.frame(iframe)

# function for checking if there is an image on the page
def is_running(driver):
    # find all elements with class name including "stApp stAppEmbeddingId"
    element = driver.find_element(By.CLASS_NAME, 'stApp')
    return element.get_attribute("data-test-script-state") == "running"

def wait_while_running(driver):
    while is_running(driver):
        time.sleep(1)

def send_multiline_text(driver, element, text):
    try:
        # Replace "\n" with Keys.ENTER for proper newline handling
        lines = text.split("\n")
        element.click()  # Ensure the element is focused

        for line in lines[:-1]:
            element.send_keys(line)
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER, Keys.ENTER).key_up(Keys.SHIFT).perform()
            time.sleep(0.2)

        # Send the last line
        element.send_keys(lines[-1])
        element.send_keys(Keys.ENTER)  # Send the message

    except Exception as e:
        print(f"Error sending multiline text: {e}")

with open(f'dataset/{args.test}.json') as f:
    data = json.load(f)

if '[FAKE_WEBSITE_BASE_URL]' in data['website']:
    # read from .env file and replace the placeholder
    with open('.env') as f:
        for line in f:
            if 'FAKE_WEBSITE_BASE_URL' in line:
                data['website'] = data['website'].replace('[FAKE_WEBSITE_BASE_URL]', line.split('=')[1].strip())

# find textArea element with aria-label "Type a message to send to Claude to control the computer..."
textArea = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Type a message to send to Claude to control the computer...']")

# This is for opening the test website
go_to_website_prompt = f"Open browser and go to {data['website']}. If it is already open, do not do anything."
send_multiline_text(driver, textArea, go_to_website_prompt)
wait_while_running(driver)

# get all elements with class name "stChatMessage"
# chatMessages = driver.find_elements(By.CLASS_NAME, 'stChatMessage')
# save them into a file
# print([chatMessage.text for chatMessage in chatMessages])

# refresh the page
driver.refresh()
iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src='http://localhost:8501']")
driver.switch_to.frame(iframe)

textArea = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Type a message to send to Claude to control the computer...']")
for prompt in data['prompts']:
    send_multiline_text(driver, textArea, prompt)
    wait_while_running(driver)

time.sleep(100)
driver.quit() 
