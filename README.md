# Chatbot scripts

This repository contains 3 Python scripts that can be used to interact with AI language models through the terminal and have text-based conversations. These scripts require Python 3 and the llm package (requires an OpenAI API key), which is used to interface with the AI model. Credit to simonw for creating llm (https://github.com/simonw/llm). 

### To-Do

Modify terminalGPT menu to give options for new convo, show old convos or use built in hardcoded prompts for games etc.

Implement dependancy checking on looper. Implement API Key checking on both.

Implement ability to move the cursor around within the prompts without it doing the weird characters. 

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

This script requires Python 3 and the llm package, which can be installed using pip. Also an OpenAI API key must be present in either the OPENAI_API_KEY environment variable, or saved in a plain text file called ~/.openai-api-key.txt in your home directory.

![Screenshot 2023-06-02 105540](https://github.com/oscampbell/terminalGPT/assets/113595058/6efad3a4-7ed0-44c3-a651-f9b90d4326ed)

## `loopGPTcode.py`

This script uses loopGPT but with the built in instruction specifically to look for possible improvements in the outputted code and ask for improvements, while always outputting the full modified code. With this you can watch an AI write a simple program and then iterate on it indefinitely.

### How to use

1. Clone the repository.
2. In the terminal, navigate to the directory where the repository was cloned.
3. Type `python3 loopGPTcode.py` and press Enter.
4. Follow the prompts to specify the coding goal.

### Dependencies

This script requires Python 3 and the llm package, which can be installed using pip. Also an OpenAI API key must be present in either the OPENAI_API_KEY environment variable, or saved in a plain text file called ~/.openai-api-key.txt in your home directory.

## `terminalGPT.py`

This script allows the user to have a text-based conversation with an AI language model. I made it after using llm and finding that it did not allow you to ask follow up questions, as the AI did not have the history of the conversation. The script keeps track of the conversation, and saves it to a file in the `conversations` directory, and feeds that to the ai as well as the next question each time you make a request. The user can choose an existing conversation file to continue the conversation, or start a new file. 

### How to use 

1. Clone the repository.
2. In the terminal, navigate to the directory where the repository was cloned.
3. Type `python3 terminalGPT.py` and press Enter. 
4. Follow the prompts to start or choose a conversation file, and enter your questions.
5. Type "exit" to end the conversation.

### Dependencies

As above.

![Screenshot 2023-06-02 110021](https://github.com/oscampbell/terminalGPT/assets/113595058/db73d0a7-3847-46c7-9f25-e8edbe6d22bd)

## Authors

os.campbell@proton.me

simonw - https://github.com/simonw/llm
