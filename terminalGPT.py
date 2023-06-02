#!/usr/bin/python3

# This is a Python script for a Chatbot that runs on top of an AI language model.

import os # Module for OS operations
import getpass # Module for retrieving currently logged in user name
from datetime import datetime # Module for getting current date and time
import subprocess # Module for running subprocesses
import signal # module for catching keyboard interrupt

# Set color codes for terminal outputs
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

# Function to handle keyboard interrupt (ctrl + c)
def keyboard_interrupt_handler(signal, frame):
    print(red + "\nKeyboard Interrupt detected! Exiting conversation loop, but the program will continue to generate a filename.")
    global question
    question = "exit"
    global interrupted
    interrupted = True

# Assign the keyboard_interrupt_handler to SIGINT (ctrl + c)
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

# Set the interrupted flag to False initially
interrupted = False

# This function prints a banner containing information about the chatbot.
def print_banner():
    banner= blue + "+-------------------------------------------+\n" + \
            "|                                           |\n" + \
            "|            Welcome to terminalGPT!        |\n" + \
            "|                                           |\n" + \
            "|    Let's chat with an AI language model.  |\n" + \
            "|          Type 'exit' to end session.      |\n" + \
            "|                                           |\n" + \
            "+-------------------------------------------+\n" + default
    print(banner)

# Print the Welcome Banner
print_banner()

#Function to check the required dependencies for running the Chatbot, like Python3 and LLM.
def check_dependancies():
    print(white + 'Checking dependancies...', end=' ')
    dep_line='\n--------------------------------------------------------\n'
    # Check if program llm exists.
    # llm is a Python package that interfaces with an AI language model
    if os.path.exists('/home/{}/.local/bin/llm'.format(getpass.getuser())):
        print(green + 'OK' + default)

    # If python3 is not installed, prompt the user to install it
    if not os.path.exists('/usr/bin/python3'):
        install = input('It seems like Python3 is not installed on your system.\nDo you want to install it now (y/n)? ')
        if install.lower()=='y':
            print("{}Installing Python3...{}".format(dep_line, dep_line))
            os.system('sudo apt install python3') # Install python3
        else:
            print('{}Cannot start without Python3. Exiting...{}'.format(dep_line, dep_line))
            exit()

    ## If pip is not installed, prompt the user to install it
    if not os.path.exists('/usr/bin/pip'):
        install = input('It seems like pip is not installed on your system.\nDo you want to install it now (y/n)? ')
        if install.lower()=='y':
            print("{}Installing pip...{}".format(dep_line, dep_line))
            os.system('sudo apt install pip') # Install pip
        else:
            print('{}Cannot start without pip. Exiting...{}'.format(dep_line, dep_line))
            exit()

    ## If llm package is not installed, prompt the user to install it
    if not os.path.exists('/home/{}/.local/bin/llm'.format(getpass.getuser())):
        install = input('It seems like LLM is not installed on your system.\nDo you want to install it now (y/n)? ')
        if install.lower()=='y':
            print("{}Installing LLM (https://github.com/simonw/llm.git)...{}".format(dep_line, dep_line))
            os.system('pip install llm') # Install llm package
        else:
            print('{}Cannot start without LLM. Exiting...{}'.format(dep_line, dep_line))
            exit()

    ## Check internet connection
    print(white+'Checking internet connection...', end=' ')
    try:
        host = subprocess.run(['host', 'google.com'], capture_output=True)
    except Exception as e:
        print(red + '\n{}Cannot check internet connection.{}'.format(dep_line, dep_line) + default)
        return
    # Exit Program if you cannot detect a valid host
    if host.returncode != 0:
        print(red + '\n{}No internet connection detected.{}'.format(dep_line, dep_line) + default)
        exit()
    print(green + 'OK\n' + default)

# Call the function to check the dependencies
check_dependancies()

# create the conversaion directory
conversations_dir = os.path.join("/", "home", getpass.getuser(), "terminalGPT", "conversations")
if not os.path.isdir(conversations_dir):
    os.makedirs(conversations_dir)

# list default/new conversation files in directory
conversation_files = os.listdir(conversations_dir)

# print available conversations
print(blue + "+--------+----------------------------------+" + default)
print(blue + "| Index  | Conversation from                |" + default)
print(blue + "+--------+----------------------------------+" + default)
print(blue + "|   0    | Start a new conversation         |" + default)
for i, file in enumerate(conversation_files):
    print(blue + "+--------+----------------------------------+" + default)
    print(blue + "|   {0:<2}   | {1:<32} |".format(i+1, file) + default)
print(blue + "+--------+----------------------------------+\n" + default)

# get the chosen conversation
choice = input(white + "Enter conversation index or 'exit': ")

# If they want to start a new conversation, save their conversation and get the name
if choice == "0":
    now = datetime.now()
    conversation_file = os.path.join(conversations_dir, now.strftime("%Y-%m-%d_%H-%M-%S_conversation"))

    # save the conversation to the file
    now = datetime.now()
    with open(conversation_file, "w") as f:
        f.write("Conversation started on " + now.strftime("%Y-%m-%d %H:%M:%S") + "!\n")
else:
    # if they're attempting to exit, exit gracefully
    if choice == 'exit' or interrupted:
        print(red + "Exiting...")
        exit()
    try:
        # Grab the conversation file
        file_index = int(choice) - 1
        conversation_file = os.path.join(conversations_dir, conversation_files[file_index])

        # Display full conversation so far
        with open(conversation_file, "r") as f:
            print(f.read())
    except ValueError:
        print(red + 'Invalid input. Exiting...' + default)
        exit()

while True:
    # get user input question
    question = input(white + getpass.getuser() + ": ")

    # write the question to the conversation file
    with open(conversation_file, "a") as f:
        f.write(white + "Question: " + question + "\n")

    # Exit chatbot loop if user enters "exit"
    if question == "exit" or interrupted:
        confirmation = input(red + "Are you sure you want to exit the conversation (y/n)? ")
        if confirmation.lower() == "y":
            break
        # Return the control back to the while loop if the user wants to keep chatting
        else:
            continue

    # create the command to send to the AI language model
    if os.path.isfile(conversation_file):
        command = 'cat {} | llm --system "{}"'.format(conversation_file, question)
    else:
        command = 'llm --system "{}"'.format(question)

    # use subprocess.run to run the command in the shell and get the output
    answer = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()

    # Add 1 newline characters for spacing between outputs
    print("\n")

    # print the answer and write it to the conversation file
    print(white + "terminalGPT: " + cyan + answer)
    with open(conversation_file, "a") as f:
        f.write("Answer: " + answer + "\n")

    # Add 1 newline characters for spacing between outputs
    print("\n")

    # Exit chatbot loop if the AI model suggests to do so
    if "exit" in answer.lower():
        # confirm with the user if they want to exit
        confirmation = input(red + "The AI suggests to exit the conversation. Are you sure you want to exit (y/n)? ")
        if confirmation.lower() == "y":
            break
        else:
            continue

# generate the name for the new file using the subject of the chat
name_generation_command = 'cat {} | llm --system "describe the subject of conversation in 3 words only."'.format(conversation_file)
generated_name = subprocess.run(name_generation_command, shell=True, capture_output=True, text=True).stdout.strip()

# obtain the filename which includes only 3 capitalized words.
new_file_name = generated_name.replace(".", "").replace(",", "").replace("-", "")
new_file_name = " ".join(word.capitalize() for word in new_file_name.split()[:3])
new_file_name = os.path.join(conversations_dir, new_file_name)

# Rename Conversation file as generated_filename
os.rename(conversation_file, new_file_name)
print(white + "\nConversation ended. File saved as:", new_file_name)
