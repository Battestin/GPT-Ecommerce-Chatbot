from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from select_persona import *
from select_document import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"

app = Flask(__name__)
app.secret_key = 'alura'

def chatbot(prompt):
    max_attempts = 1
    attempts = 0
    personality = persona[select_persona(prompt)]
    context = select_document(prompt)
    select_document = select_context(context)

    while True:
        try:
            system_prompt = f"""
            You are a customer service chatbot for an e-commerce platform.
            You should not answer questions that are not related to the provided e-commerce data!

            You might generate the responses based on the context below:
            You should adopt the personality described below to respond to the user.


            #Context
            {context}

            #Persona
            {personality}
            """
            response = cliente.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=300,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=modelo)
            return response
        except Exception as error:
            attempts += 1
            if attempts >= max_attempts:
                return "GPT Error: %s" % error
            print('Communication error with OpenAI:', error)
            sleep(1)

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    response = chatbot(prompt)
    response_text = response.choices[0].message.content
    return response_text
    
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
