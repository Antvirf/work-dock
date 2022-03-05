import sys
import os
import time

# Define work apps
work_apps = [
    "/Applications/Microsoft Outlook.app",
    "/Applications/Microsoft Teams.app"
]

# Some issue with system preferences?

# Dock addition source https://stackoverflow.com/questions/59614341/add-terminal-to-dock-persistent-apps-with-default-write-with-foreign-language-ma/59637792#59637792
# Default: Finder / Edge / Safari / Outlook / VSCode / Teams / Settings / Trash

def get_dock_contents():
    settings = os.popen("defaults read com.apple.dock").read()
    # bundle_identifier = [x.strip().split("=")[1] for x in settings.split('\n') if 'bundle-identifier' in x]
    file_labels = [x.strip().split("=")[1][1:-1].replace('"', "") for x in settings.split('\n') if 'file-label' in x]
    # urlstring = [x.strip().split("=")[1] for x in settings.split('\n') if 'CFURLString' in x]

    return ['/Applications/' + x + '.app' for x in file_labels]


def send_to_dock(inp, append=True, print_output=False):
    command = """<dict><key>tile-data</key><dict><key>file-data</key><dict><key>_CFURLString</key><string>{}</string><key>_CFURLStringType</key><integer>0</integer></dict></dict></dict>""".format(inp)
    if append:
        output = "defaults write com.apple.dock persistent-apps -array-add '{}'".format(command)
    else:
        output = "defaults write com.apple.dock persistent-apps -array '{}'".format(command)
    if print_output:
        print(output)
    time.sleep(0.75)
    os.system(output)


def reset_dock():
    time.sleep(1.5)
    os.system("killall Dock")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect usage, enter either 'work' or 'chill' as argument... Quitting.")
        quit()

    first_arg = sys.argv[1]

    # Get dock info
    dock_app_list = get_dock_contents()

    # Parse arguments
    if first_arg == 'work':
        print("Working")

        for app in work_apps:
            if app not in dock_app_list:
                send_to_dock(app)
        reset_dock()

    elif first_arg == 'chill':
        print("Chilling")

        # Deleting some icons - Exclude outlook, teams
        app_list = [x for x in dock_app_list if x not in work_apps]

        for app in app_list:
            if app == app_list[0]:
                send_to_dock(app, append=False)
            else:
                send_to_dock(app, append=True)

        reset_dock()
    else:
        print("Incorrect usage, enter either 'work' or 'chill' as argument... Quitting.")
        quit()
