from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import json
import os
from waitress import serve

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['resume']
    
    try:
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        extracted_info = {
            'number_of_pages': number_of_pages,
            'text': text
        }

        # Save extracted information to a JSON file
        with open('extracted_info.json', 'w') as json_file:
            json.dump(extracted_info, json_file)

        return jsonify({
            'extracted_info': extracted_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the app with waitress
    serve(app, host='0.0.0.0', port=5000)
