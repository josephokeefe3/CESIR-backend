### PDF TO TEXT FUNCTIONALITY ###

import pdfplumber

# Takes file path, returns list of the pdf pages (text contents)
def get_pages(path):
    pages = []

    with pdfplumber.open(path) as pdf: # opens and plumbs pdf

        for page in range(len(pdf.pages)): # indexes through pages
            pages.append(pdf.pages[page].extract_text()) # adds text contents of each page to list
    
    return pages

# Joins list of stsrings into one giant string (used to combine a list of pages into one string)
def join_lines(lines):
    return "\n".join(lines)

# Converts a pdf (provided by a file path) and converts it to a single string
def pdf_to_text(pdf_path):
    pages = get_pages(pdf_path)
    text = join_lines(pages)

    return text

import json

def read_json_from_file(file_path):
    """
    Reads a JSON object from a text file and returns it as a Python dictionary.
    
    Args:
        file_path (str): The path to the text file containing the JSON object.
        
    Returns:
        dict: The JSON object as a Python dictionary.
    """
    with open(file_path, 'r') as file:
        json_object = json.load(file)
    return json_object


### END OF PDF TO TEXT FUNCTIONALITY ###


def string_to_dict(json_str):
    try:
        # Load the JSON string into a Python dictionary
        result_dict = json.loads(json_str)
        return result_dict
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None