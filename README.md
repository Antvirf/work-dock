# Workdock - Add / remove 'work apps' from your MacOS dock
Simple command line tool to add or remove certain defined 'work apps' from the macOS dock. For example, every morning you can easily add the required apps to the dock, and once you're done with your day/week or go on leave, remove the apps you don't need to touch with a single command.
Default 'work' apps are MS Outlook, MS Teams

## Usage (without alias)
    python dock.py work # Adds work apps
    python dock.py chill # Removes work apps

## Usage (with alias configured)
    workdock work # Adds work apps
    workdock chill # Removes work apps


## Installation
In a directory of your choice, clone the repo

    git clone https://github.com/Antvirf/work-dock

Define your work applications in the dock.py file, update the work_apps list on line 8. For example, you can do this in vim:

    vim dock.py

The defaults are as below. To add an app, provide the complete path to it, including ".app" at the end.

    work_apps = [
    "/Applications/Microsoft Outlook.app",
    "/Applications/Microsoft Teams.app"
    ]

### Optional: add workdock alias to your terminal
If you prefer, you can add workdock to your terminal profile (assuming zsh by default):

    sudo python dock.py add-alias

