from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from select_document import *
from select_persona import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4-1106-preview" # gpt-4 or lower does not allow sending files and receiving files as a response

my_tools = [
    {"type": "retrieval" },
    {"type": "function",
        "function": {
            "name": "validate_promotional_code",
            "description": "Validate a promotional code based on the company's Discounts and Promotions guidelines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The promotional code, in the format COUPON_XX. For example: COUPON_ECO.",
                    },
                    "validity": {
                        "type": "string",
                        "description": "The validity of the coupon, if it is valid and associated with the policies. In the format DD/MM/YYYY.",
                    },
                },
                "required": ["code", "validity"],
            }
        }
    }
]

def validate_promotional_code(arguments):
    code = arguments.get("code")
    validity = arguments.get("validity")

    return f"""
        
        # Response Format
        
        {code} with validity: {validity}.
        Also, tell the user whether it is valid or not.

        """

my_functions = {
    "validate_promotional_code": validate_promotional_code,
}

