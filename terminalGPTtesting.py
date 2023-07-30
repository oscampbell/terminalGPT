#!/usr/bin/python3

import os
import getpass
from datetime import datetime
import subprocess
import signal

red = '\033[91m'
green = '\033[92m'
blue = '\033[94m'
cyan = '\033[96m'
white = '\033[97m'
yellow = '\033[93m'
magenta = '\033[95m'
grey = '\033[90m'
black = '\033[90m'
default = '\033[99m'

def keyboard_interrupt_handler(signal, frame):
    print(red + "\nKeyboard Interrupt detected! Exiting chat loop, but the program will continue to generate a filename.")
    global question
    question = "exit"
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, keyboard_interrupt_handler)
interrupted = False

def print_banner():
    banner = blue + "+-------------------------------------------+\n" + \
                    "|                                           |\n" + \
                    "|        " + white + "Welcome to terminalGPT!" + blue + "            |\n" + \
                    "|                                           |\n" + \
                    "|    " + white + "Use chatGPT directly in the terminal!" + blue + "  |\n" + \
                    "|          " + white + "Type 'exit' to end session." + blue + "      |\n" + \
                    "|                                           |\n" + \
                    "+-------------------------------------------+\n" + default
    print(banner)

def check_python_dependencies():
    dep_line = '\n--------------------------------------------------------\n'
    # Check for Python3
    if not os.path.exists('/usr/bin/python3'):
        install = input('It seems like Python3 is not installed on your system.\nDo you want to install it now (y/n)? ')
        if install.lower() == 'y':
            print("{}Installing Python3...{}".format(dep_line, dep_line))
            os.system('sudo apt install python3')
        else:
            print('{}Cannot start without Python3. Exiting...{}'.format(dep_line, dep_line))
            exit()

    # Check for pip
    if not os.path.exists('/usr/bin/pip'):
        install = input('It seems like pip is not installed on your system.\nDo you want to install it now (y/n)? ')
        if install.lower() == 'y':
            print("{}Installing pip...{}".format(dep_line, dep_line))
            os.system('sudo apt install pip')
        else:
            print('{}Cannot start without pip. Exiting...{}'.format(dep_line, dep_line))
            exit()

def check_llm_dependency():
    dep_line = '\n--------------------------------------------------------\n'
    # Check for LLM
    if not os.path.exists('/home/{}/.local/bin/llm'.format(getpass.getuser())):
        install = input('It seems like LLM is not installed on your system.\nDo you want to install it now (y/n)? ')
        if install.lower() == 'y':
            print("{}Installing LLM (https://github.com/simonw/llm.git)...{}".format(dep_line, dep_line))
            os.system('pip install llm')
        else:
            print('{}Cannot start without LLM. Exiting...{}'.format(dep_line, dep_line))
            exit()
    
def check_internet_connection():
    dep_line = '\n--------------------------------------------------------\n'
    try:
        host = subprocess.run(['host', 'google.com'], capture_output=True)
    except Exception as e:
        print(red + '\n{}Cannot check internet connection.{}'.format(dep_line, dep_line) + default)
        return

    if host.returncode != 0:
        print(red + '\n{}No internet connection detected.{}'.format(dep_line, dep_line) + default)
        exit()

def check_dependancies():
    print(white+'Checking internet connection...', end=' \n')
    check_internet_connection()
    print(white + 'Checking dependancies...', end=' \n')
    check_python_dependencies()
    check_llm_dependency()

    print(green + 'OK\n' + default)

def ask_user_for_choice(chats_dir, chat_files):
    print(blue + "+--------+------------------------------------------------------+")
    print(blue + "| " + white + "Index " + blue + " | " + white + "Chat Name (Auto-generated)   " + blue + "                        |")
    print(blue + "+--------+------------------------------------------------------+")
    for i, file in enumerate(chat_files):
        print(blue + "+--------+------------------------------------------------------+")
        print(blue + "|   {0:<2}   |  {1:<52}|".format(i+1, file))
    print(blue + "+--------+------------------------------------------------------+\n")

    choice = input(white + "Press enter to start a new conversation or enter chat index to resume chat ('exit' to quit): ")

    if choice == "":
        now = datetime.now()
        chat_file = os.path.join(chats_dir, now.strftime("%Y-%m-%d_%H-%M-%S_chat"))
        now = datetime.now()
        with open(chat_file, "w") as f:
            f.write("Chat started on " + now.strftime("%Y-%m-%d %H:%M:%S") + "!\n")
    else:
        if choice == 'exit' or interrupted:
            print(red + "Exiting...")
            exit()
        try:
            file_index = int(choice) - 1
            chat_file = os.path.join(chats_dir, chat_files[file_index])
            with open(chat_file, "r") as f:
                print(f.read())
        except ValueError:
            print(red + 'Invalid input. Exiting...' + default)
            exit()

    return chat_file

def run_chat_loop(chat_file):
    while True:
        question = input(white + getpass.getuser() + ": ")
        with open(chat_file, "a") as f:
            f.write("Question: " + question + "\n")

        if question == "exit" or interrupted:
            confirmation = input(red + "Are you sure you want to exit the chat (y/n)? ")
            if confirmation.lower() == "y":
                break
            else:
                continue

        if question.lower() == 'new':
            confirmation = input(red + "Are you sure you want start a new chat (y/n)? ")
            if confirmation.lower() == "y":
                generate_chat_file_name(chats_dir, chat_file)
                main()
            else:
                continue           

        if os.path.isfile(chat_file):
            command = 'cat {} | llm --system "{}" -s'.format(chat_file, question)
        else:
            command = 'llm --system "{}" -s'.format(question)

        answer = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()

        print("\n")

        print(white + "terminalGPT: " + cyan + answer + default)
        with open(chat_file, "a") as f:
            f.write("Answer: " + answer + "\n")

        print("\n")

def generate_chat_file_name(chats_dir, chat_file):
    name_generation_command = 'cat {} | llm --system "describe what was discussed here in 3 words. the output must be 3 words only."'.format(chat_file)
    generated_name = subprocess.run(name_generation_command, shell=True, capture_output=True, text=True).stdout.strip()
    generated_name = generated_name.replace(" ", "-") 
    generated_name = generated_name.replace(",", "-") 
    generated_name = generated_name.replace(".", "") 

    new_file_name = os.path.join(chats_dir, generated_name)
    os.rename(chat_file, new_file_name)
    print(white + "chat ended. File saved as:", new_file_name + "\n")

def main():
    global chats_dir
    print_banner()

    chats_dir = os.path.join("/", "home", getpass.getuser(), "terminalGPT", "chats")
    if not os.path.isdir(chats_dir):
        os.makedirs(chats_dir)

    chat_files = os.listdir(chats_dir)

    check_dependancies()

    chat_file = ask_user_for_choice(chats_dir, chat_files)

    run_chat_loop(chat_file)

    generate_chat_file_name(chats_dir, chat_file)

main()