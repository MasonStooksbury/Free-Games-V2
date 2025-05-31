from dotenv import load_dotenv
from subprocess import Popen
from pathlib import Path
from PIL import ImageGrab
from os import getenv
from time import sleep
import pyautogui as pag
import numpy as np
import cv2


# Utility to grab the screen and convert to OpenCV BGR format
def capture_screenshot():
    return cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)


def search_with_timeout(template_name, timeout=5):
    template_path = Path("OCVTemplates") / template_name
    for _ in range(timeout):
        screenshot = capture_screenshot()
        match, coords = find_best_match(screenshot, str(template_path))
        if match is not None:
            sleep(1)
            return match, coords
        sleep(1)
    return None, None


def find_best_match(screenshot, template_path, threshold=0.7):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    h, w = template.shape

    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
        return screenshot, center
    return None, None


def find_all_matches(screenshot, template_path, threshold=0.7):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    h, w = template.shape

    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    centers = [(pt[0] + w // 2, pt[1] + h // 2) for pt in zip(*locations[::-1])]
    return (screenshot, centers) if centers else (None, [])


def login(email, password):
    screenshot = capture_screenshot()
    match, coords = find_best_match(
        screenshot, str(Path("OCVTemplates") / "login_email_box.png")
    )
    if match is None:
        print("Failed to find email input box")
        return

    pag.click(coords[0], coords[1] + 30)
    sleep(1)
    for _ in range(len(email) + 10):
        pag.press("backspace")
        pag.press("delete")

    pag.write(email)
    pag.press("tab")
    sleep(1)
    pag.write(password)
    pag.press("enter")
    sleep(7)


def grab_free_game(skip=0, max_scrolls=15):
    pag.scroll(100000)  # Scroll to top
    scroll_count = 0

    while scroll_count < max_scrolls:
        screenshot = capture_screenshot()
        match, matches = find_all_matches(
            screenshot, str(Path("OCVTemplates") / "free_game_button.png")
        )

        if len(matches) > skip:
            coords = matches[skip]
            pag.click(*coords)
            break

        skip -= len(matches)
        pag.scroll(-750)
        scroll_count += 1
        sleep(1)
    else:
        return True  # Reached end of scroll attempts

    print("Free game found.")

    # Mature content warning
    print("Awaiting Mature Content Warning screen.")
    match, coords = search_with_timeout("continue_button.png")
    if match is not None:
        pag.click(*coords)
    else:
        print("No Mature Content Warning screen.")

    # Check if already in library
    screenshot = capture_screenshot()
    match, coords = find_best_match(
        screenshot, str(Path("OCVTemplates") / "in_library.png")
    )
    if match is not None:
        print("Game is already in library.")
        return

    # Click 'Get' button
    match, coords = search_with_timeout("get_game_button.png", 7)
    if match is not None:
        pag.click(*coords)
    else:
        print("Couldn't find 'Get' button. Skipping.")
        return

    sleep(1)

    # Accept 'Refund and Right of Withdrawal'
    match, coords = search_with_timeout("eula_accept_button.png")
    if match is not None:
        pag.click(*coords)

    # Click 'Place Order'
    match, coords = search_with_timeout("place_order_button.png")
    if match is not None:
        pag.click(*coords)
    else:
        print("Couldn't find 'Place Order' button")
        return

    # Accept EULA
    match, coords = search_with_timeout("eula_accept_button.png")
    if match is not None:
        pag.click(*coords)
    else:
        print("No EULA")


def main():
    load_dotenv()
    email = getenv("EPIC_EMAIL")
    password = getenv("EPIC_PASSWORD")
    launcher_path = getenv("LAUNCHER_PATH")

    Popen(rf"{launcher_path}")

    match, coords = search_with_timeout("store_button.png", timeout=10)

    if match is None:
        login(email, password)
    else:
        pag.click(*coords)
        sleep(2)

    for skip in range(10):
        reached_max_scrolls = grab_free_game(skip, max_scrolls=20)
        if reached_max_scrolls:
            print("Reached the end of search.")
            break

        match, coords = search_with_timeout("store_button.png", 10)
        if match is not None:
            pag.click(*coords)
            sleep(2)

    print("Finished.")


if __name__ == "__main__":
    main()
