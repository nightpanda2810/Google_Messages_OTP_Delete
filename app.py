# Base application structure

from pandalibs.yaml_importer import get_configuration_data
from pandalibs.pprint_nosort import pp  # noqa: F401
from playwright.sync_api import Playwright, sync_playwright
import datetime
import time
import re

gotta_log_in = None
config = get_configuration_data()
today = datetime.date.today()
today_abbreviation = today.strftime("%a").lower()
days_of_week = [
    "sun",
    "mon",
    "tue",
    "wed",
    "thu",
    "fri",
    "sat",
]
today_index = days_of_week.index(today_abbreviation)
valid_abbreviations = []
for i in range(2, 7):  # Check for 2, 3, 4, 5, and 6 days ago
    index = (today_index - i) % 7
    valid_abbreviations.append(days_of_week[index])


def run(playwright: Playwright) -> None:
    browser_type = playwright.firefox  # Or playwright.chromium, playwright.webkit
    user_data_dir = "./userdata"
    browser = browser_type.launch_persistent_context(headless=True, user_data_dir=user_data_dir)
    page = browser.new_page()
    page.goto(config["login_url"])
    if gotta_log_in:
        page.locator("mw-sign-in-banner").get_by_role("button", name="Sign in").click()
        page.get_by_label("Email or phone").fill(config["username"])
        page.get_by_label("Email or phone").press("Enter")
        page.get_by_label("Enter your password").fill(config["password"])
        page.get_by_label("Enter your password").press("Enter")

    names_to_check = {}
    for item in config["text_names"]:
        try:
            if config["DEBUG"]:
                print(f"Checking if the {item['name']} conversation is in the list.")
            text_name = str(item["name"])
            checked_name = page.get_by_role("option", name=text_name).text_content(timeout=10000)
            names_to_check[text_name] = {
                "desc": item["desc"],
                "checked_name": checked_name,
                "days_keep": item["keep"],
            }
        except Exception as e:
            if config["DEBUG"]:
                print(f"{text_name} not found. BEGIN EXCEPTION:\n\n{e}\nEND EXCEPTION\n")
            else:
                pass
    if config["DEBUG"]:
        print("\nThese are the names to check:\n")
        pp(names_to_check)
        print("")
    if names_to_check:
        try:
            for name in names_to_check:
                value = names_to_check[name]
                # print(f"VALUE: {value}")
                # print(f"VALUE: {value['days_keep']}")
                if config["DEBUG"]:
                    print(f"Checking if conversation: {name}, {value['desc']} exists.")
                if re.findall(config["day_pattern"][1:], value["checked_name"]) and value["days_keep"] == 1:
                    last_three_chars = value["checked_name"][-3:].lower()
                    if last_three_chars in valid_abbreviations:
                        label = f"Options for {name}"
                        if config["DEBUG"]:
                            print(f"Deleting the {value['desc']} conversation.")
                        page.get_by_role("option", name=name).hover()
                        page.get_by_label(label).click()
                        page.get_by_role("menuitem", name="Delete").click()
                        page.get_by_role("button", name="Cancel").click()
                        pass
                    else:
                        if config["DEBUG"]:
                            print(f"{value['desc']} is being kept some time.")
                elif re.findall(config["time_pattern"][1:], value["checked_name"]) or re.findall(config["day_pattern"][1:], value["checked_name"]):
                    if value["days_keep"] == 0:
                        label = f"Options for {name}"
                        if config["DEBUG"]:
                            print(f"Deleting the {value['desc']} conversation.")
                        page.get_by_role("option", name=name).hover()
                        page.get_by_label(label).click()
                        page.get_by_role("menuitem", name="Delete").click()
                        page.get_by_role("button", name="Cancel").click()
                    else:
                        if config["DEBUG"]:
                            print(f"{value['desc']} is being kept some time.")
                else:
                    if config["DEBUG"]:
                        print(f"The {name} conversation is not at least an hour old.")
                pass
        except Exception as e:
            if config["DEBUG"]:
                print(f"There was an error processing names_to_check:\n{e}END ERROR\n")
    else:
        print("No names found.")
        pass
    if config["DEBUG"]:
        print("Completed cleaning up text messages.")

    # KEEP SESSION OPEN (Comment out when you're ready to close)
    time.sleep(1)
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
