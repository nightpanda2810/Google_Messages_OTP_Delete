## Introduction
This is my first public Python project. It is a simple script that uses Playwright to log into Google Messages app and delete messages based on the names you specify in the config file.

### Why?
I got tired of deleting OTPs, and other types of notification texts that I really only want to see once. I wanted to be able to just check a list and have it delete them for me. My phone is not rootable, so this was the best option I could think of, and a good way for me to practice Python. Automatic OTP deletion option in Messages app only works for some of them.

## How to use
1. To set up, on line 12, you first must change gotta_log_in to True.
1. In line 39, change headless to be false. Change value of slow_mo to 1000, or whatever you are comfortable with for testing.
1. Then, add your username and password to the config.yaml file. Example file provided.
1. Add a list of names that you want to check for text messages.
1. Add a description for each name in the list. 
1. Setup your virtual environment, or simply run pip install -r requirements.txt
1. Run playwright install firefox. This does NOT work with chromium or webkit.
1. Create empty "userdata" folder in the same directory as app.py
1. Have your phone ready to go, then run app.py
1. The login process will begin, you will need to confirm the connection with your phone just like you would manually.
1. The script will check for any messages that match the names in the list and delete them if they are older than an hour.
1. If you want to keep a message longer than an hour, put a 1 in the "keep" column of the name's row in the config file. This will keep the message for 2 days.
1. Watch the script work. It will NOT delete messages yet. 
1. Once you are satisfied that it is working as expected, change gotta_log_in to False and run again. The script will run without logging in and do the same as previously, without deleting messages. To begin deleting messages, in line 89 and 104, change "Cancel" to "Delete". Case sensitive.
1. You are all set! You can change debug to False in config.yaml if you no longer want to see the print statements in your terminal.

## Known issues or limitations
- If you have multiple conversations with the same name, those conversations *may* be skipped. *Test what happens if this is the case for you.*
- Does not work with archived messages. I won't be including this.
- Automation on Windows or MacOS unknown.

## Automation

If you want this to run automatically, you can use a cron job, windows task manager, or something similar. If you're going to automate it on another machine, copying the userdata folder you previously created is important. It will save your login session and allow you to log in without having to go through the confirmation process again.

I personally set this up in a Linux virtual machine to run hourly during the times I'm normally awake (in order to see the messages that came in while I was sleeping), and it works great for me. I wanted to keep all messages available for me to see when I wake up in order to see if any OTPs or other notifications came in before they get deleted. I'm not sure how well it will work on Windows or MacOS, when automated, but I coded and tested in Windows before moving it over to Linux.