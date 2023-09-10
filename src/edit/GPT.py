#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name : ok.py
# Description : Script de test de l'API OpenAI
# Author : MasterLaplace

import openai
import os
import re

openai.api_key = "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" # os.getenv("OPENAI_API_KEY")

class LaplaceAPI:
    @staticmethod
    def create_file(name: str = "", content: str = ""):
      '''
      Create a file
      :param name: Name of the file
      :param content: Content of the file
      '''
      with open(name, 'w') as file:
        file.write(content)
        os.system("echo [LOG] " + name + " created >> log.txt")

    @staticmethod
    def edit_file(name: str = "", content: str = ""):
      '''
      Édite un fichier
      :param name: Name of the file
      :param content: Content of the file
      '''
      os.system("echo " + content + " > " + name)
      os.system("echo [LOG] " + name + " edited >> log.txt")

    @staticmethod
    def get_file(name: str = "") -> str:
      '''
      Return the content of a file
      :param name: Name of the file
      :return: Content of the file
      '''
      os.system("echo [LOG] Get file " + name + " >> log.txt")
      return open(name, "r").read()

    @staticmethod
    def create_folder(name: str = ""):
      '''
      Create a folder
      :param name: Name of the folder
      '''
      os.makedirs(name, exist_ok=True)
      os.system("echo [LOG] " + name + " created >> log.txt")

    @staticmethod
    def get_tree() -> list:
      '''
      Return the list of files
      :return: List of files
      '''
      os.system("echo [LOG] Get tree >> log.txt")
      return os.listdir()

    @staticmethod
    def move_file(name: str = "", path: str = ""):
      '''
      Move a file
      :param name: Name of the file
      :param path: Path of the file
      '''
      os.system("mv " + name + " " + path)
      os.system("echo [LOG] " + name + " moved to " + path + " >> log.txt")

INTERACT_FUNC = {
    "create_file": LaplaceAPI.create_file,
    "edit_file": LaplaceAPI.edit_file,
    "get_file": LaplaceAPI.get_file,
    "create_folder": LaplaceAPI.create_folder,
    "get_tree": LaplaceAPI.get_tree,
    "move_file": LaplaceAPI.move_file
}

PROMPT="""You can use the following functions:
- "- create_file(name="", content="")"
- "- edit_file(name="", content="")"
- "- get_file(name="")" -> I give you the content of the file
- "- create_folder(name="")"
- "- get_tree()" -> I give you the list of files
- "- move_file(name="", path="")"

Example: if I want to create a file named "test.txt" in a folder named "tmp" with the content "Hello World!", just answer:
```
- create_folder("tmp")
- create_file("tmp/test.txt", "Hello World!")
```
"""

# task = input(PROMPT + "Task: ") # I want to have a python script named "Hollo" that say hello world.
task = "I want to have a python script named \"Hollo\" that say hello world."

# response = openai.ChatCompletion.create(
#   model = 'gpt-3.5-turbo',
#   messages=[
#     {"role": "system", "content": PROMPT},
#     {"role": "user", "content": task}
#   ]
# )

# print(response['choices'][0]['message']['content'])

class GPT:
    def __init__(self, model='gpt-3.5-turbo', temperature=0.7):
        self.model = model
        self.temperature = temperature

    def submit_request(self, task):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
              {"role": "system", "content": PROMPT},
              {"role": "user", "content": task}
            ],
            temperature=self.temperature,
        )
        return response

    def get_top_reply(self, prompt):
        response = self.submit_request(prompt)
        return response['choices'][0]['message']['content']

response = """Alright! I can help you with that. Let's create a new file named "Hollo.py" and write the code for it. Here are the steps:

1. Create a file named "Hollo.py":
```
- create_file("Hollo.py")
```

2. Edit the file to add the Python code that prints "Hello World!":
```
- edit_file("Hollo.py", 'print("Hello World!")')
```

That's it! Now you have a Python script named "Hollo.py" that says "Hello World!" when executed.
"""

# function_calls = re.findall(r"^- ([a-zA-Z_]+)\((.*?)\)$", response['choices'][0]['message']['content'], re.MULTILINE)
function_calls = re.findall(r"^- ([a-zA-Z_]+)\((.*?)\)", response, re.MULTILINE)

formatted_calls = [(func_name, tuple(map(str.strip, args.split(',')))) for func_name, args in function_calls]

for call in formatted_calls:
    function_name = call[0]
    print("Function name: ", function_name, end=", ")
    if function_name in INTERACT_FUNC:
        print("Executing", function_name, "with args", call[1])
        INTERACT_FUNC[function_name](*call[1])
