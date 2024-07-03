from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
from extract import get_cost_info
from tools import pdf_to_text

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check for allowed file extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from the PDF
        text = ''
        with open(file_path, 'rb') as pdf_file:
            text = pdf_to_text(pdf_file)
        
        # Extract info from the text
        extracted_info = get_cost_info(text)

        jsonOb = jsonify({"text": text, "extracted_info": extracted_info})
        return jsonOb
    return jsonify({"error": "File not allowed"}), 400

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    original_text = data['text']
    extracted_info = data['extracted_info']
    
    # Save the data to a JSON Lines file
    data_entry = {
        "original_text": original_text,
        "extracted_info": extracted_info
    }
    with open('database.jsonl', 'a') as db_file:
        json.dump(data_entry, db_file)
        db_file.write('\n')  # Ensure the next record is on a new line
    
    return jsonify({"message": "Data saved successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
