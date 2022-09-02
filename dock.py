#!/usr/bin/env python
import os
import re
import sys
import time

# Define work apps
work_apps = [
    "/Applications/Microsoft Outlook.app",
    "/Applications/Microsoft Teams.app"
]

# Defines desired alias
alias_name = 'workdock'
alias_string = """alias {}="python {}\"""".format(
    alias_name, os.path.realpath(__file__))
terminal_rc = '.zshrc'

# Some issue with system preferences?
# Dock addition source https://stackoverflow.com/questions/59614341/add-terminal-to-dock-persistent-apps-with-default-write-with-foreign-language-ma/59637792#59637792
# Bash alias addition based on https://stackoverflow.com/questions/37842862/creating-command-line-alias-with-python

# Default: Finder / Edge / Safari / Outlook / VSCode / Teams / Settings / Trash


def append_to_bash_rc(alias):
    homefolder = os.path.expanduser('~')
    bashrc = os.path.abspath('{}/{}'.format(homefolder, terminal_rc))

    pattern = re.compile(alias)
    if os.path.isfile(bashrc):
        with open(bashrc, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if pattern.match(line):
                    return
            out = open(bashrc, 'a')
            out.write('\n{}'.format(alias))
            out.close()
    else:
        with open(bashrc, 'w') as f:
            f.write('\n{}'.format(alias))


def get_dock_contents():
    settings = os.popen("defaults read com.apple.dock").read()
    file_labels = [x.strip().split("=")[1][1:-1].replace('"', "")
                   for x in settings.split('\n') if 'file-label' in x]

    output_list = []
    # Resolve the paths - try /Applications/ first, then try /System/Applications
    for app in file_labels:
        if os.path.isdir('/Applications/' + app + '.app'):
            output_list.append('/Applications/' + app + '.app')
        elif os.path.isdir('/System/Applications/' + app + '.app'):
            output_list.append('/System/Applications/' + app + '.app')
        else:
            print('Failed to resolve path for', app)
    return output_list


def send_to_dock(inp, append=True, print_output=False):
    command = """<dict><key>tile-data</key><dict><key>file-data</key><dict><key>_CFURLString</key><string>{}</string><key>_CFURLStringType</key><integer>0</integer></dict></dict></dict>""".format(
        inp)
    if append:
        output = "defaults write com.apple.dock persistent-apps -array-add '{}'".format(
            command)
    else:
        os.system("defaults write com.apple.dock persistent-apps ''")
        output = "defaults write com.apple.dock persistent-apps -array '{}'".format(
            command)
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

    # Parse arguments
    if first_arg == 'work':
        print("Working - adding work apps to the dock...")
        dock_app_list = get_dock_contents()

        for app in work_apps:
            # print("\t", app)
            if app not in dock_app_list:
                send_to_dock(app)
        reset_dock()

    elif first_arg == 'chill':
        print("Chilling - removing work apps from the dock...")
        dock_app_list = get_dock_contents()
        # Deleting some icons - Exclude outlook, teams
        app_list = [x for x in dock_app_list if x not in work_apps]

        for app in app_list:
            if app == app_list[0]:
                send_to_dock(app, append=False)
            else:
                send_to_dock(app, append=True)
        reset_dock()

    elif first_arg == 'add-alias':
        try:
            append_to_bash_rc(alias_string)
            print("Alias added succesfully, you can now run 'workdock <command>'. See 'workdock help' for available commands.")
            print(
                "Please restart your terminal or do 'source ~/.bash_profile' for changes to take effect.")
        except IOError:
            print('Permission denied; try editing your .bash_profile manually or run this command again with sudo.')

    elif first_arg == 'help':
        print("\nWorkDock - simple command line util to add/delete working apps from the macOS dock.")
        print("Usage: 'python dock.py <command>', or '{} <command> if alias is set.".format(
            alias_name))
        print("Available commands:")
        print(
            """
    work \t Adds defined working apps to the dock.
    chill \t Removes the defined working apps from the dock.
    add-alias \t Adds 'workdock' alias to your terminal for easier usage.

    help \t Prints out this commmands help screen.
            """
        )
    else:
        print("\nInvalid arguments. Usage: dock <command>")
        print("To see help text for available commands, you can run:\n\tdock help")
        quit()
