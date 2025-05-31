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


def search_timeout(img, timeout=5):
    for _ in range(timeout):
        matched_image, coords = findBestMatchInScreenshot(
            captureScreenshot(), str(Path("OCVTemplates").joinpath(img))
        )
        if matched_image is not None:
            sleep(1)
            return matched_image, coords
        sleep(1)

    return None, None


def findBestMatchInScreenshot(screenshot, template_path, threshold=0.7):
    # Read the template image
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    # Convert screenshot to grayscale for template matching
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Check for a strong enough match (e.g., >=70%)
    if max_val >= threshold:
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


def findAllMatchesInScreenshot(screenshot, template_path, threshold=0.7):
    # Read the template image in grayscale
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    # Convert screenshot to grayscale
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Find all locations where matching result exceeds threshold
    locations = np.where(result >= threshold)
    match_centers = []

    for pt in zip(*locations[::-1]):  # (x, y) format
        center_x = pt[0] + template_w // 2
        center_y = pt[1] + template_h // 2
        match_centers.append((center_x, center_y))

        # Optional: draw rectangles around matches
        # bottom_right = (pt[0] + template_w, pt[1] + template_h)
        # cv2.rectangle(screenshot, pt, bottom_right, (0, 255, 0), 2)

    if match_centers:
        return screenshot, match_centers
    else:
        return None, []


def login(email, password):
    # Email box
    matched_image, coords = findBestMatchInScreenshot(
        captureScreenshot(), str(Path("OCVTemplates").joinpath("login_email_box.png"))
    )

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1] + 30)
        sleep(1)
        for i in range(len(email) + 10):
            pag.press("backspace")
            pag.press("delete")
    else:
        print("failed email box")
        return None

    # Write email into box
    pag.write(email)

    # Hit Enter to continue
    pag.press("tab")
    sleep(1)
    # Password box
    pag.write(password)

    # Hit Enter to continue
    pag.press("enter")

    # Wait a while
    sleep(7)


# Grab the free game
def grabFreeGame(skip: int, max_scrolls=15):
    end_search = False
    scrolls = 0
    # Make sure we are scrolled to the very top. Since we don't know how far down we are, let's pick some astronomical number to be sure
    pag.scroll(100000)
    found = False
    coords = ""
    # Search for, then click the 'Free Now' button on the game
    while not found:
        matched_image, matches = findAllMatchesInScreenshot(
            captureScreenshot(), str(Path("OCVTemplates") / "free_game_button.png")
        )

        # Skip initial matches (supposedly already checked free games)
        if len(matches) > skip:
            found = True
            coords = matches[skip]
            break
        skip -= len(matches)

        if scrolls >= max_scrolls:
            end_search = True
            break
        scrolls += 1

        pag.scroll(-750)
        sleep(1)

    if found:
        pag.click(x=coords[0], y=coords[1])
    else:
        return end_search

    # Navigate Mature Content Warning screen
    matched_image, coords = search_timeout("continue_button.png")

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
    else:
        print("No Mature Content Warning screen")

    # Find and click 'Get'
    matched_image, coords = search_timeout("get_game_button.png", 7)

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])

    else:
        print("Couldn't find 'Get' button checking for in library")
        matched_image, coords = findBestMatchInScreenshot(
            captureScreenshot(), str(Path("OCVTemplates").joinpath("in_library.png"))
        )

        if matched_image is not None:
            print("Found game in library")

        return None

    sleep(1)

    # Accept 'Refund and Right of Withdrawal'
    matched_image, coords = search_timeout("eula_accept_button.png")

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])

    # Find and click 'Place Order'
    matched_image, coords = search_timeout("place_order_button.png")

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
    else:
        print("Couldn't find 'Place Order' button")
        return None

    # Accept EULA
    matched_image, coords = search_timeout("eula_accept_button.png")

    if matched_image is not None:
        pag.click(x=coords[0], y=coords[1])
    else:
        print("No EULA")


if __name__ == "__main__":
    # Load credentials from .env file
    load_dotenv()

    # Grab credentials from file and put them into an array to unpack later (doing it this way allows for future improvements like multiple-accounts)
    credentials = [getenv("EPIC_EMAIL"), getenv("EPIC_PASSWORD")]

    # Open the Epic Games Desktop App
    Popen(rf'{getenv("LAUNCHER_PATH")}')

    matched_image, coords = search_timeout("store_button.png", 10)

    # If we aren't logged in, login
    if matched_image is None:
        login(*credentials)
    # Otherwise, make sure the window is focused, then get our free game
    else:
        pag.click(x=coords[0], y=coords[1])
        sleep(2)

    # Try to get 10 different free games
    for i in range(10):
        end_search = grabFreeGame(skip=i)
        if end_search:
            print("Reached the end with no more results.")
            break

        # Return to store page
        matched_image, coords = search_timeout("store_button.png", 10)
        if matched_image is not None:
            pag.click(x=coords[0], y=coords[1])
            sleep(2)

    print("Finished.")
