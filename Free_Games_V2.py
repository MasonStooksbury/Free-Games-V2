from subprocess import Popen
from PIL import ImageGrab
from pathlib import Path
import pyautogui as pag
from time import sleep
import numpy as np
import cv2

##############################################################################################################
#################################         REPLACE THESE           ############################################
##############################################################################################################
# Replace this with the path to your EpicGamesLauncher executable path
launcher_exe_path = r'E:\Programs\Epic Games\Launcher\Engine\Binaries\Win64\EpicGamesLauncher.exe'
email = 'flump'
password = 'doople'
##############################################################################################################
##############################################################################################################
##############################################################################################################



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

    # Check for a strong enough match (e.g., 80%)
    if max_val > 0.8:
        top_left = max_loc
        bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

        # Calculate the center coordinates
        center_x = top_left[0] + template_w // 2
        center_y = top_left[1] + template_h // 2

        # Draw a green rectangle around the matched area
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

        return screenshot, (center_x, center_y)
    else:
        return None, None



def login():
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
    found = False
    coords = ''
    # Search for, then click the 'Free Now' button on the game
    while not found:
        pag.scroll(-750)
        matched_image, center_coordinates = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('free_game_button.png')))
        sleep(1)
        if matched_image is not None:
            found = True
            coords = center_coordinates
            break
        
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



# Open the Epic Games Desktop App
Popen(launcher_exe_path)

# Give the app a second to startup
sleep(6)

# Check to see if we're already logged in or not by looking for the "Store" link on the left side of the app
matched_image, coords = findTemplateInScreenshot(captureScreenshot(), str(Path('OCVTemplates').joinpath('store_button.png')))

# If we aren't logged in, login
if matched_image is None:
    login()
    sleep(5)
# Otherwise, make sure the window is focused, then get our free game
else:
    pag.click(x=coords[0], y=coords[1])
    sleep(2)

grabFreeGame()
