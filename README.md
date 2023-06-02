# Chatbot scripts

This repository contains two Python scripts that can be used to interact with AI language models through the terminal and have text-based conversations. These scripts require Python 3 and the llm package (requires an OpenAI API key), which is used to interface with the AI model.

## `terminalGPT.py`

This script allows the user to have a text-based conversation with an AI language model. The script keeps track of the conversation, and saves it to a file in the `conversations` directory. The user can choose an existing conversation file to continue the conversation, or start a new file. 

### How to use 

1. Clone the repository.
2. In the terminal, navigate to the directory where the repository was cloned.
3. Type `python3 terminalGPT.py` and press Enter. 
4. Follow the prompts to start or choose a conversation file, and enter your questions.
5. Type "exit" to end the conversation.

### Dependencies

This script requires Python 3 and the llm package, which can be installed using pip.

## `loopGPT.py`

This script is designed for two AI language models to have a conversation with each other. The script generates a conversation file in the `conversations` directory, and saves the conversation to the file as it progresses.

### How to use

1. Clone the repository.
2. In the terminal, navigate to the directory where the repository was cloned.
3. Type `python3 loopGPT.py` and press Enter.
4. Follow the prompts to specify the subject and initial prompt for the conversation.
5. The script will generate AI responses to each other, and the conversation will be saved to a file named with 3 descriptive words in the `conversations` directory.
6. Type "exit" to end the conversation.

### Dependencies

This script requires Python 3 and the llm package, which can be installed using pip.

## Authors

os.campbell@proton.me
