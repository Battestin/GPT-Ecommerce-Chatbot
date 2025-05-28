from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

ecomart_policy = load_file('Python\GPT Pytho chatbot\\data\\ecomart_policy.txt')
ecomart_data = load_file('Python\GPT Pytho chatbot\\data\\ecomart_data.txt')
ecomart_products = load_file('Python\GPT Pytho chatbot\\data\\ecomart_products.txt')

def select_document(openai_response):
    if "politicas" in openai_response:
        return ecomart_data + "\n" + ecomart_policy
    elif "produtos" in openai_response:
        return ecomart_data + "\n" + ecomart_products
    else:
        return ecomart_data

def select_context(user_message):
    system_prompt = f"""
    The company EcoMart has three main documents detailing different aspects of the business:

    #Document 1 "\n {ecomart_data} "\n"
    #Document 2 "\n" {ecomart_policy} "\n"
    #Document 3 "\n" {ecomart_products} "\n"

    Analyze the user's prompt and return the most appropriate document to be used as context for the answer. Return 'dados' for Document 1, 'politicas' for Document 2, and 'produtos' for Document 3.
    """

    response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=1,
        )

    context = response.choices[0].message.content.lower()

    return context