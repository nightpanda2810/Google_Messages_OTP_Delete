# Base application structure

from pandalibs.yaml_importer import get_configuration_data
from playwright.sync_api import Playwright, sync_playwright
import time
import re

config = get_configuration_data()
# time_pattern = r"\d{1,2}:\d{2}\s*(AM|PM)"
# print(time_pattern)
# print(config["time_pattern"][1:])


def run(playwright: Playwright) -> None:
    browser_type = playwright.firefox  # Or playwright.chromium, playwright.webkit
    user_data_dir = "./userdata"
    browser = browser_type.launch_persistent_context(headless=False, user_data_dir=user_data_dir)
    page = browser.new_page()
    page.goto(config["login_url"])
    # page.locator("mw-sign-in-banner").get_by_role("button", name="Sign in").click()
    # page.get_by_label("Email or phone").fill(config["username"])
    # page.get_by_label("Email or phone").press("Enter")
    # page.get_by_label("Enter your password").fill(config["password"])
    # page.get_by_label("Enter your password").press("Enter")

    names_to_check = {}
    for text_name in config["text_names"]:
        try:
            checked_name = page.get_by_role("option", name=text_name).text_content(timeout=2500)
            # print(checked_name)
            names_to_check[text_name] = checked_name
            # pp(names_to_check)
        except Exception as e:
            print(f"{text_name} not found. ERROR:\n{e}END ERROR")
            pass

    if names_to_check:
        for name in names_to_check:
            value = names_to_check[name]
            if re.findall(config["time_pattern"][1:], value):
                label = f"Options for {name}"
                print(f"Deleting the {name} conversation.")
                page.get_by_role("option", name=name).hover()
                page.get_by_label(label).click()
                page.get_by_role("menuitem", name="Delete").click()
                page.get_by_role("button", name="Cancel").click()
            else:
                print(f"The {name} conversation is not at least an hour old.")
            pass
    else:
        print("No names found.")
        pass
    print("Completed cleaning up text messages.")

    # KEEP SESSION OPEN (Comment out when you're ready to close)
    time.sleep(1)
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
