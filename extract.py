from openai import OpenAI
from tools import string_to_dict
from extract_tools import retrieve_from_model, generate_prompt
from dotenv import load_dotenv
from prompt_info import FIELD_DESCRIPTIONS, EXTRACTION_SPEC
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")
CURRENT_MODEL=os.getenv("CURRENT_MODEL")

# Initiate the openai client
client = OpenAI(
    api_key = API_KEY
)

# Define the function for running the test
# Takes raw text (from a CESIR), returns model output
def get_cost_info(text):
    
    # Prepare the prompt
    prompt = generate_prompt(text, EXTRACTION_SPEC, additional_info=FIELD_DESCRIPTIONS) 

    response = retrieve_from_model(prompt = prompt, model = CURRENT_MODEL)

    print("Model Response:", response)

    return string_to_dict(response)

