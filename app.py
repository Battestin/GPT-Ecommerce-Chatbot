from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from select_persona import *
from select_document import *
from ecomart_assistant import *
import uuid
from vision_ecomart import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo" #on production use "gpt-4-1106-preview"

app = Flask(__name__)
app.secret_key = 'alura'

assistant = take_json()
thread_id = assistant["thread_id"]
assistant_id = assistant["assistant_id"]
files_id = assistant["files_id"]

STATUS_COMPLETED = "completed"
STATUS_REQUIRES_ACTION = "requires_action"

sent_image_path = None
UPLOAD_FOLDER = "data"

def chatbot(prompt):
    global sent_image_path
    max_attempts = 1
    repetition = 0

    while True:
        try:
            personality = persona[select_persona(prompt)]

            client.beta.threads.messages.create(
                thread_id = thread_id,
                role = "user",
                content = f"""
                Assuma, de agora em diante, a personalidade abaixo.
                Ignore as personalidades anteriores.

                #Persona
                {personality}
                """,
                files_id = files_id
            )

            vision_response = ""
            if sent_image_path is not None:
                vision_response = analyze_image(sent_image_path)
                vision_response += ". In the end of the response, show details about the image."
                os.remove(sent_image_path)
                sent_image_path = None

            client.beta.threads.messages.create(
                thread_id = thread_id,
                role = "user",
                content = vision_response+prompt,
                files_id = files_id
            )

            run = client.beta.threads.runs.create(
                thread_id = thread_id,
                assistant_id = assistant_id
            )

            while run.status != STATUS_COMPLETED:
                run = client.beta.threads.runs.retrieve(
                    thread_id = thread_id,
                    run_id = run.id
                )
                print(f"Status: {run.status}")

                if run.status == STATUS_REQUIRES_ACTION:
                    triggered_tools = run.required_action.submit_tool_outputs.tool_calls
                    triggered_tools_responses = []

                    for tool in triggered_tools:
                        function_name = tool.function.name
                        chosen_function = my_functions[function_name]
                        arguments = json.loads(tool.function.arguments)
                        print(arguments)
                        function_response = chosen_function(arguments)

                        triggered_tools_responses.append({
                            "tool_call_id": tool.id,
                            "output": function_response
                        })

                    run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id = thread_id,
                        run_id = run.id,
                        tool_outputs = triggered_tools_responses
                    )

            history = list(client.beta.threads.messages.list(thread_id = thread_id).data)
            response = history[0]
            return response

        except Exception as error:
            repetition += 1
            if repetition >= max_attempts:
                return "GPT Error: %s" % error
            print('Communication error with OpenAI:', error)
            sleep(1)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    global sent_image_path
    if 'image' in request.files:
        sent_image = request.files['image']
        
        file_name = str(uuid.uuid4()) + os.path.splitext(sent_image.filename)[1]
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        sent_image.save(file_path)
        sent_image_path = file_path
        
        return 'Umage uploaded successfully', 200
    return 'No image uploaded', 400

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    response = chatbot(prompt)
    response_text = response.content[0].text.value
    return response_text
    
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
