from dotenv import load_dotenv
from subprocess import Popen
from PIL import ImageGrab
from pathlib import Path
import pyautogui as pag
from time import sleep
from os import getenv
import numpy as np
import cv2



# Function to easily capture screenshots
def captureScreenshot():
    # Capture the entire screen, convert to a numpy array, then convert to OpenCV format
    return cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)



def findTemplateInScreenshot(screenshot, template_path):
    # Read the template image
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    # Convert screenshot to grayscale for template matching
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Check for a strong enough match (e.g., >=70%)
    if max_val >= 0.7:
        top_left = max_loc
        # bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

        # Calculate the center coordinates
        center_x = top_left[0] + template_w // 2
        center_y = top_left[1] + template_h // 2

        # Draw a green rectangle around the matched area
        # cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

        return screenshot, (center_x, center_y)
    else:
        return None, None



def login(email, password):
    # Email box
    matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('login_email_box.png')))

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
        sleep(1)
    else:
        print('failed email box')
        return None

    # Write email into box
    pag.write(email)

    # Hit Enter to continue
    pag.press('enter')

    # Wait a bit
    sleep(5)

    # Password box
    matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('login_password_box.png')))

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
        sleep(1)
    else:
        print('failed password')
        return None

    # Write password into box
    pag.write(password)

    # Hit Enter to continue
    pag.press('enter')

    # Wait a while
    sleep(5)



# Grab the free game
def grabFreeGame():
    # Make sure we are scrolled to the very top. Since we don't know how far down we are, let's pick some astronomical number to be sure
    pag.scroll(10000)
    found = False
    coords = ''
    # Search for, then click the 'Free Now' button on the game
    while not found:
        matched_image, center_coordinates = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('free_game_button.png')))
        sleep(1.5)
        if matched_image is not None:
            found = True
            coords = center_coordinates
            break
        pag.scroll(-750)
        
    if found:
        pag.click(x=coords[0], y=coords[1])
        sleep(5)
    else:
        return None
    

    # Navigate Mature Content Warning screen
    matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('continue_button.png')))

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
        sleep(5)
    else:
        print("No Mature Content Warning screen")


    # Find and click 'Get'
    matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('get_game_button.png')))

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
        sleep(5)
    else:
        print("Couldn't find 'Get' button")
        return None


    # Fill out EULA if available
    matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('eula_checkbox.png')))

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
        sleep(2)
        matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('eula_accept_button.png')))
        if matched_image is not None:
            pag.click(x=coords[0], y=coords[1])
            sleep(5)
    else:
        print("No EULA")


    # Find and click 'Place Order'
    matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('place_order_button.png')))

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
        sleep(5)
    else:
        print("Couldn't find 'Place Order' button")
        return None





# Load credentials from .env file
load_dotenv()

# Grab credentials from file and put them into an array to unpack later (doing it this way allows for future improvements like multiple-accounts)
credentials = [getenv("EPIC_EMAIL"), getenv("EPIC_PASSWORD")]

# Open the Epic Games Desktop App
Popen(rf'{getenv("LAUNCHER_PATH")}')

# Give the app a second to startup
sleep(10)

# Check to see if we're already logged in or not by looking for the "Store" link on the left side of the app
matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('store_button.png')))

# If we aren't logged in, login
if matched_image is None:
    login(*credentials)
    sleep(5)
# Otherwise, make sure the window is focused, then get our free game
else:
    pag.click(x=coords[0], y=coords[1])
    sleep(2)

grabFreeGame()
