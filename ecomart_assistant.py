from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from select_persona import *
import json
from tools_ecomart import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4-1106-preview"  # gpt-4 or lower does not allow sending files and receiving files as a response
context = load_file("Python\GPT Pytho chatbot\\data\\ecomart.txt")

def create_ids_list(): 
    files_id_list = []

    data_file = client.files.create(
        file = open("Python/GPT Pytho chatbot/data/ecomart_data.txt", "rb"),
        purpose = "assistants"
    )
    files_id_list.append(data_file.id)

    policy_file = client.files.create(
        file = open("Python/GPT Pytho chatbot/data/ecomart_policy.txt", "rb"),
        purpose = "assistants"
    )
    files_id_list.append(policy_file.id)

    
    products_file = client.files.create(
        file = open("Python/GPT Pytho chatbot/data/ecomart_products.txt", "rb"),
        purpose = "assistants"
    )
    files_id_list.append(products_file.id)

    # Note: the assistant can access up to 20 files at a time

def take_json():
    filename = "assistants.json"

    if not os.path.exists(filename):
        thread_id = create_thread()
        file_id_list = create_ids_list()
        assistant_id = create_assistant(file_id_list)
        data = {
            "thread_id": thread_id.id,
            "assistant_id": assistant_id.id,
            "files_id": file_id_list
        }
        with open(filename, "w", encoding = "utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"{filename} file created successfully.")

    try:
        with open(filename, "r", encoding = "utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")


def create_thread():
    return client.beta.threads.create()

def create_assistant(files_id = []):
    assistant = client.beta.assistants.create(
        name="EcoMart Assistant",
        instructions = f"""
            You are a customer service chatbot for an e-commerce store.
            You must not answer questions that are not related to the provided e-commerce data!
            Also, access the files associated with you and the thread to answer the questions.
        """,
        model = model,
        tools = my_tools,
        files_id = files_id
    )
    return assistant

# ##print(assistant.id) # Uncomment this line to print the assistant ID

# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "List the products"
#         }
#     ]
# )

# client.beta.threads.messages.create(
#     thread_id = thread.id,
#     role = "user",
#     content = " from the sustainable fashion category"
# )

# ## Create a run for the thread with the assistant
# run = client.beta.threads.runs.create(
#     thread_id = thread.id,
#     assistant_id = assistant.id
# )

# ## Wait for the run to complete
# while run.status != "completed":
#     run = client.beta.threads.runs.retrieve(
#         thread_id = thread.id,
#         run_id = run.id
#     )

# # Print the response from the assistant
# history = client.beta.threads.messages.list(thread_id=thread.id).data

# ## Print the messages in reverse order to show the conversation flow
# for message in reversed(history):
#     print(f"\nRole: {message.role}\n content: {message.content[0].text.value}\n")