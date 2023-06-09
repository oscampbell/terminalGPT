#!/usr/bin/python3

# Import necessary packages
import os
import getpass   # module to get currently logged in user name
from datetime import datetime   # module to get current date and time
import subprocess
import time # module for time related operation
import signal # module for catching keyboard interrupt

# Set the conversation file name with current date and time
now = datetime.now()
conversation_file = os.path.join("/", "home", getpass.getuser(), "terminalGPT", "conversations", now.strftime("%Y-%m-%d_%H-%M-%S_conversation"))

# Create the chatGPT/conversations directory if it doesn't exist
conversations_dir = os.path.dirname(conversation_file)
if not os.path.isdir(conversations_dir):
    os.makedirs(conversations_dir)

# Create the conversation file if it doesn't exist
if not os.path.isfile(conversation_file):
    with open(conversation_file, "w") as f:
        f.write("Conversation started!\n")

# Limit the size of conversation file to 20 lines
def limit_file_lines(file):
    with open(file, "r+") as f:
        lines = f.readlines()
        if len(lines) > 20:
            f.seek(0)
            f.truncate()
            f.writelines(lines[10:])

# Initialize the first question and personality
question = input("Subject: ") + "Do not output 'As an AI language model' ever."
personality = input("Personality/Goal: ")
aiChat = "Your personality/goal is " + personality + "Look at this conversation and craft a reply to the most recent message. Give this reply as your output. Try to avoid saying things that will lead to looping conversation. Dont repeat anything that has already been said in the conversation. Come up with a new unique question if the conversation is wrapping up. Try to keep question short and snappy."

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

# Add 1 newline characters for spacing between outputs
print("\n")

# Start the conversation loop
while True:
    
    # Exit the conversation loop if the user types "exit" or if the keyboard interrupt was caught
    if question == "exit" or interrupted:
        break
    
    # Write the question to the conversation file and limit file to 30 lines
    with open(conversation_file, "a") as f:
        f.write(question + "\n")
        limit_file_lines(conversation_file)

    # Exit the conversation loop if the user types "exit"
    if question == "exit":
        break

    # Create the command to send to the AI language model
    if os.path.isfile(conversation_file):
        command = 'cat {} | llm --system "{} Do not include the phrase: As an AI language model."'.format(conversation_file, question)
    else:
        command = 'llm --system "{}"'.format(question)

    # Use subprocess.run to run the command in the shell and get the output
    answer = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()

    # Print the answer and write it to the conversation file, then limit file to 30 lines
    print(white + "chatGPT: " + blue + answer + "\n" )

    with open(conversation_file, "a") as f:
        f.write(answer + "\n")
        limit_file_lines(conversation_file)

    # Add 1 newline characters for spacing between outputs
    print("\n")

    # Add a 10 second break before the next command is run
#    time.sleep(10)

    # Create the command to get the ai response
    if os.path.isfile(conversation_file):
        command = 'cat {} | llm --system "{}"'.format(conversation_file, aiChat)
    else:
        command = 'llm --system "{}"'.format(aiChat)

    # Use subprocess.run to run the command in the shell and get the output
    answer = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()

    # Print the answer and write it to the conversation file, then limit file to 30 lines
    print(white + "terminalGPT: " + cyan + answer + "\n" )

    # Add 1 newline characters for spacing between outputs
    print("\n")

    # Add a 10 second break before the next command is run
#    time.sleep(10)

    # Set the next question
    question = answer

    # Exit the conversation loop if the AI model suggests to do so, but don't include this in the conversation file
    if "bye" in answer.lower():
        # Ask for confirmation
        confirmation = input(red + "The AI suggests to exit the conversation. Are you sure you want to exit (y/n)? ")
        # If confirmed, break the loop
        if confirmation.lower() == "y":
            break
        # If not confirmed, continue the loop
        else:
            continue

# Generate the new file name using the specific command
name_generation_command = 'cat {} | llm --system "describe what was discussed here in 3 words. the output must be 3 words only."'.format(conversation_file)
generated_name = subprocess.run(name_generation_command, shell=True, capture_output=True, text=True).stdout.strip()
generated_name = generated_name.replace(" ", "-") 
generated_name = generated_name.replace(",", "-") 
generated_name = generated_name.replace(".", "") 

# Rename the conversation file with the generated name
new_file_name = os.path.join(conversations_dir, generated_name)
os.rename(conversation_file, new_file_name)
print(white + "Conversation ended. File saved as:", new_file_name + "\n")
