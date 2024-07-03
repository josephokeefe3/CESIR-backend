from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")

print(API_KEY)

# Set your OpenAI API key
client = OpenAI(
    api_key=API_KEY
    )

def generate_prompt(text, fields, additional_info):
    """
    Generates a prompt based on the provided text, fields, and additional information.

    Args:
        text (str): The raw text to extract information from.
        fields (dict): A dictionary specifying the fields to extract.
        additional_info (dict): A dictionary providing additional information for each field.

    Returns:
        str: The constructed prompt.
    """
    fields_prompt = "\n".join([f"- {field}: {additional_info.get(field, '')}" for field in fields.keys()])
    
    prompt = f"""
    Extract the following information from the text:
    {fields_prompt}
    
    You many find it useful to first identify the "Utility" and then find the information, as different utilities format there documents differently.

    Text:
    {text}

    Provide the extracted information in the following JSON format:
    {{
    {", ".join([f'"{key}": "<{key.replace(" ", "_")}>"' for key in fields.keys()])}
    }}
    """
    return prompt


def retrieve_from_model(prompt, model):
    """
    Sends the prompt to the OpenAI API and retrieves the response.

    Args:
        prompt (str): The constructed prompt.

    Returns:
        dict: The response from the OpenAI API as a JSON object.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response from the completion
    info = completion.choices[0].message.content

    return info