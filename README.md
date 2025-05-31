[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)

# Free Games V2

New and improved games grabber for Epic Games that utilizes the Desktop Application rather than the webapp. Designed to run on Windows, but this should also work on Mac and Linux.

If you have an improvement or bug fix, please feel free to make a pull request and I'll try to get to it as soon as I can
<br><br>

## Logs in for you

![](https://github.com/MasonStooksbury/Free-Games-V2/blob/main/GIFs/login.gif)

<br>

## And grabs the free game! (sorry for the terrible quality. I had to compress it to make GitHub happy)

![](https://github.com/MasonStooksbury/Free-Games-V2/blob/main/GIFs/grabbing_game.gif)

<br><br>

# Installation and Setup

- Install Python [from their website](https://www.python.org/downloads/)
  - Be sure to install PIP if it asks
  - Check any boxes related to PATH (this will make execution by any scheduling tool much easier)
- Clone this repository or download a ZIP using the green `Code` button on GitHub
- In a terminal or command prompt run this command to install the required dependencies:
  - `pip install -r requirements.txt`
  - (If that doesn't work, try `pip3` instead of `pip`)
- Open the `.env-sample` file in a text editor (Notepad, VSCode, Sublime, whatever you have)
- Modify these values to what they should be
  - `LAUNCHER_PATH`: This is absolute filepath leading to the executable that launches the EpicGamesLauncher on your computer (on Windows this is a `.exe` file and on Mac I think this is `.app`). It will probably be named `EpicGamesLauncher` (at least, that's what it's called on Windows. If you have a Mac, please confirm this and post an Issue on this repo. Thank you :)). Make sure that there are quotes around the path like in the example
  - `EPIC_EMAIL`: This is the email you use to login with
  - `EPIC_PASSWORD`: This is the password you use to login with
- Rename the `.env-sample` file to just `.env`
- Once everything is modified and saved, go ahead and run the `Free_Games_V2.py` file
  - For Windows: Open a command prompt, navigate to the folder housing the `Free_Games_V2.py` file and run it with `.\Free_Games_V2.py`. You can also just open the folder in the File Explorer and double-click on it
  - For Mac: Open a terminal, navigate to the folder housing the `Free_Games_V2.py` file, and run it with `python3 ./Free_Games_V2.py`.

<br>

# Schedule to run automatically

TODO, but basically, just use `Windows Task Scheduler` or a `CRON` job to run that script whenever you need to (I forget when Epic drops games now, but once a week should do it)

<br><br>

## Edge cases

### Can pass the EULA screen

![](https://github.com/MasonStooksbury/Free-Games-V2/blob/main/GIFs/passing_eula.gif)

<br><br>

## TODO

- Test/Trim sleep times in between actions to make it faster
- Have the script close Epic Games app when finished (for some reason .terminate() and .kill() do not want to work)

# Pyinstaller how-to

Run `pyinstaller Free_Games_V2.spec` to build a new release.

(Make sure pyinstaller is installed. It is part of requirements.txt).

Remember to copy the `.env-sample` file into the release folder before shipping it.
