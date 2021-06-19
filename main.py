#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
from os import access, R_OK
from os.path import isfile
import logging

parser = argparse.ArgumentParser(description="Send slack invitations")
parser.add_argument("emails", type=str, help="A file that contains one email per line")
parser.add_argument("--workspace", type=str, help="A url to your Slack workspace", required=True)
parser.add_argument("--email", type=str, help="Your Slack workspace email", required=True)
parser.add_argument("--passwd", type=str, help="Your Slack workspace password", required=True)
parser.add_argument("--verbose", default=False, action='store_true', help="Verbose mode")
parser.add_argument("--screenshot", default=False, action='store_true', help="Screenshot after every invite")
args = parser.parse_args()

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG if args.verbose else logging.INFO)

url = args.workspace + "/?redir=%2Fadmin%2Finvites"
file = args.emails

if not isfile(file) or not access(file, R_OK):
    logging.fatal("Can't open emails file, make sure it is readable")
    exit(1)

opts = webdriver.FirefoxOptions()
opts.add_argument("--headless")
logging.info("Starting the Firefox webdriver")
driver = webdriver.Firefox(options=opts)

logging.debug("Trying to sign in")
# Login to workspace
driver.get(args.workspace)
if "Slack" not in driver.title or "Sign in to" not in driver.page_source:
    logging.fatal("Couldn't get to the sign in form")
    exit(1)

logging.debug("Got the sign in form, entering credentials")

emailInput = driver.find_element_by_name("email")
emailInput.clear()
emailInput.send_keys(args.email)

passInput = driver.find_element_by_name("password")
passInput.clear()
passInput.send_keys(args.passwd)

loginBtn = driver.find_element_by_id("signin_btn")
loginBtn.click()

logging.debug("Submitted sign in form")

if "you entered an incorrect email address or password" in driver.page_source:
    logging.fatal("Invalid credentials, make sure you entered the correct email and password")
    exit(1)

logging.info("Signed in successfully, going to the invitations page")
driver.get(url)

logging.debug("Waiting 5 seconds for page to load")
driver.implicitly_wait(5)

logging.debug("Opening the invitation modal")
inviteButton = driver.find_element_by_xpath('//button[text()="Invite People"]')
inviteButton.click()
with open(file, "r") as emailsFile:
    for line in emailsFile:
        cleanEmail = line.strip()
        logging.info("Inviting %s", cleanEmail)

        logging.debug("Filling the email into the form")
        emailsInput = driver.find_element_by_id("invite_modal_select")
        emailsInput.send_keys(cleanEmail)
        emailsInput.send_keys(Keys.TAB)
        sendBtn = driver.find_element_by_xpath('//button[@data-qa="invite-to-workspace-modal-invite-form-send-button"]')
        driver.execute_script("document.querySelector('.c-popover').style.display = 'none'")
        sendBtn.click()

        logging.debug("Clicked on send, waiting 30 seconds")
        driver.implicitly_wait(30)

        if args.screenshot:
            logging.debug("Saving a screenshot of the page")
            if not driver.save_screenshot("./screenshots/aft-"+cleanEmail+".png"):
                logging.warning("Couldn't save screenshot")

        if "This person is already in your workspace." in driver.page_source:
            logging.warning("%s is already invited to your workspace", cleanEmail)

        logging.debug("Reloading the invitation modal")
        inviteMore = driver.find_element_by_xpath('//button[text()="Invite More People"]')
        inviteMore.click()

logging.info("Finished all emails")
driver.close()