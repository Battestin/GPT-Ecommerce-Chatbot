from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import encode_image

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4-vision-preview"  # Use the vision model for image analysis

def analyze_image(image_path):
    prompt = """
        Assume you are a chatbot assistant and the user is likely sending a photo of a product.
        Analyze the product, and if it is defective, provide an assessment. Assume you have processed
        an image with Vision and your response should follow the output format below.

        # RESPONSE FORMAT

        My analysis of the image consists of: Assessment with indications of the defect or product description (if there is no defect)

        ## Describe the image
        put the description here
    """

    image_base64 = encode_image(image_path)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

print(analyze_image("Python\GPT Pytho chatbot\\data\\new_mug.png"))