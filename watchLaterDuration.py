#! python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep


def getLogin():
    """
    Gets user's YouTube login, allowing user to test different accounts without
    manually updating the constants.py file.
    """

    email = input('Email: ')
    password = input('Password: ')

    # Overwrite constants.py file with YouTube credentials provided by user,
    # or creates the file if not already available.
    with open('constants.py', 'w') as file:
        file.write("EMAIL = '" + email + "'\n")
        file.write("PASSWORD = '" + password + "'\n")


def useExistingLogin():
    """
    Asks user whether they want to use the current credentials or input a new
    login. If 'yes', the program runs; if 'no', getLogin() is called.
    """

    use_existing_login = input(
        "Do you want to use the login credentials for " +
        constants.EMAIL + "? (y/n) ")
    if use_existing_login.lower() == 'y' or \
            use_existing_login.lower() == 'yes':
        pass
    else:
        getLogin()


# Import constants file, if available
# If file isn't found (ImportError), call getLogin() to get user credentials
try:
    import constants
    useExistingLogin()
except ImportError:
    print("Login file not detected. Please enter your information below.")
    getLogin()
    import constants


def getWatchLaterTime():
    """
    Main function for calculating the Watch Later Duration. Uses Selenium to
    automate the task.
    """

    active = True
    while active:
        print('Testing...')

        # Establish Selenium connection
        binary = FirefoxBinary(
            r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
        browser = webdriver.Firefox(firefox_binary=binary)
        browser.get('https://www.youtube.com/feed/subscriptions')

        # Sign in to Google account
        emailElem = browser.find_element_by_id('Email')
        emailElem.send_keys(constants.EMAIL)
        emailElem.submit()
        passElem = WebDriverWait(browser, 2).until(
            EC.element_to_be_clickable((By.ID, 'Passwd'))
        )
        passElem.send_keys(constants.PASSWORD)
        passElem.submit()
        sleep(1)

        # Go to Watch Later playlist
        browser.get('https://www.youtube.com/playlist?list=WL')

        # Import time of all videos in watch later playlist using timestamps
        timeElem = browser.find_elements_by_class_name('timestamp')
        splitTimes = []

        # Split time into individual ints
        splitTimes += [elems.text.split(':') for elems in timeElem]

        # Convert each sub-time to int
        splitTimes = [[int(x) for x in row] for row in splitTimes]

        # Convert hours and minutes to seconds
        secondsList = []
        for row in splitTimes:
            if len(row) == 3:
                row[0] = row[0] * 3600
                row[1] = row[1] * 60
                secondsList += [sum(row)]
            elif len(row) == 2:
                row[0] = row[0] * 60
                secondsList += [sum(row)]

        # Get total number of seconds from secondsList
        totalSeconds = 0
        for seconds in secondsList:
            totalSeconds += seconds

        # Convert and display total time
        m, s = divmod(totalSeconds, 60)
        h, m = divmod(m, 60)
        print('Total videos: %s' % (len(splitTimes)))
        print('Total Watch Later time: %d:%02d:%02d' % (h, m, s))

        # Asks user whether they want to continue testing. If 'yes',
        # useExistingLogin() is called to see if a different account should be
        # tested. If 'no', program quits.
        closeProgram = input('Do you test again? (y/n) ')
        if closeProgram.lower() == 'y' or closeProgram.lower() == 'yes':
            useExistingLogin()
            browser.quit()
            active = True
        else:
            print('Testing complete.')
            browser.quit()
            active = False


if __name__ == '__main__':
    getWatchLaterTime()
