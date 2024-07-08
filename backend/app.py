# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from PyPDF2 import PdfReader
# import json
# import requests

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5174", "http://127.0.0.1:5174"]}})

# LLAMA_API_URL = "https://llama3-endpoint.ishavverma.workers.dev/"

# def send_data_to_api(extracted_text):
#     try:
#         # Combine all extracted text into a single string
#         combined_text = "\n".join([page['text'] for page in extracted_text])
        
#         # Prepare the JSON payload for the external API
#         payload = {
#             "messages": [
#                 {"role": "system", "content": "convert the data into structured format"},
#                 {"role": "user", "content": combined_text}
#             ]
#         }
        
#         # Send POST request to the external API
#         response = requests.post(LLAMA_API_URL, json=payload)
        
#         if response.status_code == 200:
#             return True
#         else:
#             return False
#     except Exception as e:
#         print(f"Error sending data to API: {str(e)}")
#         return False

# @app.route('/api/upload-resume', methods=['POST'])
# def upload_resume():
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     resume_file = request.files['resume']
    
#     if resume_file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if not resume_file.filename.lower().endswith('.pdf'):
#         return jsonify({'error': 'Only PDF files are supported'}), 400

#     try:
#         reader = PdfReader(resume_file) 
        
#         extracted_text = []
#         for page_num in range(len(reader.pages)):
#             page = reader.pages[page_num]
#             text = page.extract_text() 
#             extracted_text.append({'page_number': page_num + 1, 'text': text})
        
#         # Store the extracted text in a JSON file (optional)
#         with open('extracted_resume.json', 'w') as json_file:
#             json.dump({'pages': extracted_text}, json_file)
        
#         # Send extracted text to external API
#         out = send_data_to_api(extracted_text)
#         print(out)
#         if out:
#             return jsonify({'message': 'Resume uploaded successfully', 'extracted_text': out}), 200
#         else:
#             return jsonify({'error': 'Failed to send data to external API'}), 500
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'healthy'}), 200

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)














# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from PyPDF2 import PdfReader
# import json
# import requests

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5174", "http://127.0.0.1:5174"]}})

# LLAMA_API_URL = "https://llama3-endpoint.ishavverma.workers.dev/"

# def send_data_to_api(extracted_text):
#     try:
#         combined_text = "\n".join([page['text'] for page in extracted_text])
#         payload = {
#             "messages": [
#                 {"role": "system", "content": "convert the data into structured format"},
#                 {"role": "user", "content": combined_text}
#             ]
#         }
#         response = requests.post(LLAMA_API_URL, json=payload)
#         return response.status_code == 200
#     except Exception as e:
#         print(f"Error sending data to API: {str(e)}")
#         return False

# @app.route('/api/upload-resume', methods=['POST'])
# def upload_resume():
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     resume_file = request.files['resume']
    
#     if resume_file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if not resume_file.filename.lower().endswith('.pdf'):
#         return jsonify({'error': 'Only PDF files are supported'}), 400

#     try:
#         reader = PdfReader(resume_file)
#         extracted_text = []
#         for page_num in range(len(reader.pages)):
#             page = reader.pages[page_num]
#             text = page.extract_text()
#             extracted_text.append({'page_number': page_num + 1, 'text': text})
        
#         with open('extracted_resume.json', 'w') as json_file:
#             json.dump({'pages': extracted_text}, json_file)
        
#         out = send_data_to_api(extracted_text)

#         if out:
#             return jsonify({'message': 'Resume uploaded successfully', 'extracted_text': out}), 200
#         else:
#             return jsonify({'error': 'Failed to send data to external API'}), 500
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'healthy'}), 200

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)









from flask import Flask, request, jsonify
import pdfplumber
import io
import requests
import logging
from flask_cors import CORS
import os
import json
import tempfile
import traceback

app = Flask(__name__)
CORS(app, origins='*')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        if not text:
            logging.warning("Extracted text is empty.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        logging.error(traceback.format_exc())
        return None

@app.route('/api/upload-resume', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension != '.pdf':
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Save the file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        # Extract text from the saved file
        extracted_text = extract_text_from_pdf(temp_path)
        
        # Remove the temporary file
        os.remove(temp_path)
        
        if extracted_text is None:
            return jsonify({'error': 'Failed to extract text from PDF'}), 500
        
        logging.debug(f"Extracted text: {extracted_text[:500]}...")  # Log first 500 characters
        if len(extracted_text)>4800:
            extracted_text = extracted_text[:4500]
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "consider this data provided and convert it into a structured format if data is not provided return None. Return the data as a dictionary, use variables such as name, mail, UG_Institute, is_pg, PG_Institute, count_years_of_experience, is_PHD, #_workshops, #_papers, #_books, #_achievements, skills, school."
                },
                {
                    "role": "user",
                    "content": extracted_text
                }
            ]
        }
        
        try:
            logging.debug(f"Sending request to API with data: {json.dumps(data)[:500]}...")  # Log first 500 characters
            response = requests.post('https://llama3-endpoint.ishavverma.workers.dev/', json=data)
            logging.debug(f"API Response: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                # Save the response to a JSON file
                with open('response.json', 'w') as json_file:
                    json.dump(response_data, json_file)
                return jsonify(response_data)
            else:
                logging.error(f"API request failed with status code {response.status_code}: {response.text}")
                # Save the error response to a JSON file
                with open('error_response.json', 'w') as json_file:
                    json.dump(response.json(), json_file)
                return jsonify({'error': 'Failed to process the request to the API'}), response.status_code
        except Exception as e:
            logging.error(f"Error making API request: {e}")
            logging.error(traceback.format_exc())
            return jsonify({'error': 'Failed to process the request to the API'}), 500
    
    return jsonify({'error': 'Failed to process the file'}), 500

if __name__ == '__main__':
    app.run(debug=True)
















# from flask import Flask, request, jsonify
# import pdfplumber
# import io
# import requests
# import logging
# from flask_cors import CORS
# import os
# import json
# import tempfile
# import traceback
# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, origins='*')

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# # Load the dataset and similarity matrix
# employee_data_path = '/Users/smarty/Desktop/uploader/backend/employee_data_numeric.csv'
# cosine_sim_matrix_path = '/Users/smarty/Desktop/uploader/backend/cosine_sim_matrix.csv'

# employee_data = pd.read_csv(employee_data_path)
# cosine_sim_matrix = pd.read_csv(cosine_sim_matrix_path).values

# def extract_text_from_pdf(file_path):
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             text = ""
#             for page in pdf.pages:
#                 text += page.extract_text() or ""
#         if not text:
#             logging.warning("Extracted text is empty.")
#         return text
#     except Exception as e:
#         logging.error(f"Error extracting text from PDF: {e}")
#         logging.error(traceback.format_exc())
#         return None

# def map_response_to_features(response_data):
#     feature_mapping = {
#         "UG_Institute": "UG_Institute",
#         "PG_Institute": "PG_Institute",
#         "PhD_Institute": "PhD_Institute",
#         "TotalPapers": "TotalPapers",
#         "TotalPatents": "TotalPatents",
#         "Achievements": "Achievements",
#         "Workshops": "Workshops",
#         "Trainings": "Trainings",
#         "Longevity": "Longevity",
#         "Books_Chapters": "Books_Chapters",
#         "Student_Projects": "Student_Projects",
#         "Committee_Chair": "Committee_Chair",
#         "Memberships": "Memberships",
#         "Languages_Known": "Languages_Known",
#         "Awards": "Awards",
#         "Grant_Details": "Grant_Details",
#         "Courses_Taught": "Courses_Taught",
#         "Certifications": "Certifications",
#         "Additional_Roles": "Additional_Roles",
#         "Proficiency": "Proficiency",
#         "Number_of_Departments": "Number_of_Departments",
#         "Number_of_Institutes": "Number_of_Institutes",
#         "Number_of_Projects": "Number_of_Projects",
#         "Salary": "Salary",
#         "Department_Admin": "Department_Admin",
#         "Post_UG": "Post_UG",
#         "Post_PG": "Post_PG",
#         "Post_PHD": "Post_PHD",
#         "Role_Head": "Role_Head",
#         "Department_Faculty": "Department_Faculty",
#         "Post_Admin": "Post_Admin",
#         "Role_Other": "Role_Other",
#         "City_1": "City_1",
#         "State_1": "State_1",
#         "Total_Experience": "Total_Experience",
#         "Number_of_Jobs": "Number_of_Jobs",
#         "Number_of_Unique_Designations": "Number_of_Unique_Designations",
#         "Sector_Academia/Education": "Sector_Academia/Education",
#         "Sector_Defense": "Sector_Defense",
#         "Sector_Government": "Sector_Government",
#         "Sector_Industry": "Sector_Industry"
#     }
    
#     mapped_features = {feature: 0 for feature in feature_mapping.values()}
    
#     for key, value in response_data.items():
#         if key in feature_mapping and value:
#             mapped_features[feature_mapping[key]] = 1
#             logging.debug(f"Feature {feature_mapping[key]} is set to 1")

#     logging.debug(f"Mapped features: {mapped_features}")
    
#     return mapped_features

# @app.route('/api/upload-resume', methods=['POST'])
# def upload_file():
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['resume']
    
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if file:
#         file_extension = os.path.splitext(file.filename)[1].lower()
#         if file_extension != '.pdf':
#             return jsonify({'error': 'Unsupported file type'}), 400
        
#         # Save the file temporarily
#         temp_dir = tempfile.gettempdir()
#         temp_path = os.path.join(temp_dir, file.filename)
#         file.save(temp_path)
        
#         # Extract text from the saved file
#         extracted_text = extract_text_from_pdf(temp_path)
        
#         # Remove the temporary file
#         os.remove(temp_path)
        
#         if extracted_text is None:
#             return jsonify({'error': 'Failed to extract text from PDF'}), 500
        
#         logging.debug(f"Extracted text: {extracted_text[:500]}...")  # Log first 500 characters
        
#         # Prepare the data for the external API
#         data = {
#             "messages": [
#                 {
#                     "role": "system",
#                     "content": "consider this data provided and convert it into a structured format if data is not provided return None. Return the data as a dictionary, use variables such as UG_Institute, PG_Institute, PhD_Institute, TotalPapers, TotalPatents, Achievements, Books, Total_Experience, Number_of_Jobs, Number_of_Unique_Designations, Sector_Academia/Education, Sector_Defense, Sector_Government, Sector_Industry."
#                 },
#                 {
#                     "role": "user",
#                     "content": extracted_text
#                 }
#             ]
#         }
        
#         try:
#             logging.debug(f"Sending request to API with data: {json.dumps(data)[:500]}...")  # Log first 500 characters
#             response = requests.post('https://llama3-endpoint.ishavverma.workers.dev/', json=data)
#             logging.debug(f"API Response: {response.text}")
            
#             if response.status_code == 200:
#                 response_data = response.json()
#                 # Log the API response
#                 logging.debug(f"API response data: {response_data}")

#                 # Save the response to a JSON file
#                 with open('response.json', 'w') as json_file:
#                     json.dump(response_data, json_file)
                
#                 # Map the response to features
#                 mapped_features = map_response_to_features(response_data)
#                 user_data_df = pd.DataFrame([mapped_features])
                
#                 # Ensure the columns match the employee data
#                 user_data_df = user_data_df.reindex(columns=employee_data.columns, fill_value=0)
                
#                 # Log the user data frame
#                 logging.debug(f"User data frame: \n{user_data_df}")
                
#                 # Calculate the cosine similarity
#                 user_vector = user_data_df.values
#                 similarity_scores = cosine_similarity(user_vector, employee_data.values).flatten()
                
#                 # Log the similarity scores
#                 logging.debug(f"Similarity scores: {similarity_scores}")
                
#                 # Print each parameter
#                 logging.debug(f"User vector: {user_vector}")
#                 for idx, employee_vector in enumerate(employee_data.values):
#                     logging.debug(f"Employee {idx} vector: {employee_vector}")
#                     logging.debug(f"Similarity with Employee {idx}: {similarity_scores[idx]}")
                
#                 # Find the most similar employee
#                 most_similar_index = np.argmax(similarity_scores)
#                 most_similar_score = similarity_scores[most_similar_index]
                
#                 return jsonify({
#                     'most_similar_employee_index': int(most_similar_index),
#                     'similarity_score': float(most_similar_score)
#                 })
#             else:
#                 logging.error(f"API request failed with status code {response.status_code}: {response.text}")
#                 # Save the error response to a JSON file
#                 with open('error_response.json', 'w') as json_file:
#                     json.dump(response.json(), json_file)
#                 return jsonify({'error': 'Failed to process the request to the API'}), response.status_code
#         except Exception as e:
#             logging.error(f"Error making API request: {e}")
#             logging.error(traceback.format_exc())
#             return jsonify({'error': 'Failed to process the request to the API'}), 500
    
#     return jsonify({'error': 'Failed to process the file'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)




















# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import json
# import tempfile
# import traceback
# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# import pdfplumber
# import requests
# import logging

# app = Flask(__name__)
# CORS(app, origins='*')

# logging.basicConfig(level=logging.DEBUG)

# employee_data_path = '/Users/smarty/Desktop/uploader/backend/employee_data_numeric.csv'
# cosine_sim_matrix_path = '/Users/smarty/Desktop/uploader/backend/cosine_sim_matrix.csv'

# employee_data = pd.read_csv(employee_data_path)
# cosine_sim_matrix = pd.read_csv(cosine_sim_matrix_path).values

# def extract_text_from_pdf(file_path):
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             text = "".join([page.extract_text() or "" for page in pdf.pages])
#         if not text:
#             logging.warning("Extracted text is empty.")
#         return text
#     except Exception as e:
#         logging.error(f"Error extracting text from PDF: {e}")
#         logging.error(traceback.format_exc())
#         return None

# def map_response_to_features(response_data):
#     feature_mapping = {
#         "UG_Institute": "UG_Institute",
#         "PG_Institute": "PG_Institute",
#         "PhD_Institute": "PhD_Institute",
#         "TotalPapers": "TotalPapers",
#         "TotalPatents": "TotalPatents",
#         "Achievements": "Achievements",
#         "Books": "Books_Chapters",
#         "Total_Experience": "Total_Experience",
#         "Number_of_Jobs": "Number_of_Jobs",
#         "Number_of_Unique_Designations": "Number_of_Unique_Designations",
#         "Sector_Academia/Education": "Sector_Academia/Education",
#         "Sector_Defense": "Sector_Defense",
#         "Sector_Government": "Sector_Government",
#         "Sector_Industry": "Sector_Industry"
#     }
    
#     mapped_features = {feature: 0 for feature in feature_mapping.values()}
    
#     for key, value in response_data.items():
#         if key in feature_mapping and value:
#             mapped_features[feature_mapping[key]] = 1
#             logging.debug(f"Feature {feature_mapping[key]} is set to 1")

#     logging.debug(f"Mapped features: {mapped_features}")
    
#     return mapped_features

# @app.route('/api/upload-resume', methods=['POST'])
# def upload_file():
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['resume']
    
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if file:
#         file_extension = os.path.splitext(file.filename)[1].lower()
#         if file_extension != '.pdf':
#             return jsonify({'error': 'Unsupported file type'}), 400
        
#         temp_dir = tempfile.gettempdir()
#         temp_path = os.path.join(temp_dir, file.filename)
#         file.save(temp_path)
        
#         extracted_text = extract_text_from_pdf(temp_path)
        
#         os.remove(temp_path)
        
#         if extracted_text is None:
#             return jsonify({'error': 'Failed to extract text from PDF'}), 500
        
#         logging.debug(f"Extracted text: {extracted_text[:500]}...")
#         if len(extracted_text)>4500:
#             extracted_text = extracted_text[:4500]
#         data = {
#             "messages": [
#                 {"role": "system", "content": "consider this data provided and convert it into a structured format if data is not provided return None. Return the data as a dictionary, use variables such as UG_Institute, PG_Institute, PhD_Institute, TotalPapers, TotalPatents, Achievements, Books, Total_Experience, Number_of_Jobs, Number_of_Unique_Designations, Sector_Academia/Education, Sector_Defense, Sector_Government, Sector_Industry."},
#                 {"role": "user", "content": extracted_text}
#             ]
#         }
        
#         try:
#             logging.debug(f"Sending request to API with data: {json.dumps(data)[:500]}...")
#             response = requests.post('https://llama3-endpoint.ishavverma.workers.dev/', json=data)
#             logging.debug(f"API Response: {response.text}")
            
#             if response.status_code == 200:
#                 response_data = response.json()
#                 logging.debug(f"API response data: {response_data}")

#                 mapped_features = map_response_to_features(response_data)
#                 user_data_df = pd.DataFrame([mapped_features])
                
#                 user_data_df = user_data_df.reindex(columns=employee_data.columns, fill_value=0)
                
#                 logging.debug(f"User data frame: \n{user_data_df}")
                
#                 user_vector = user_data_df.values
#                 similarity_scores = cosine_similarity(user_vector, employee_data.values).flatten()
                
#                 logging.debug(f"Similarity scores: {similarity_scores}")
                
#                 logging.debug(f"User vector: {user_vector}")
#                 for idx, employee_vector in enumerate(employee_data.values):
#                     logging.debug(f"Employee {idx} vector: {employee_vector}")
#                     logging.debug(f"Similarity with Employee {idx}: {similarity_scores[idx]}")
                
#                 most_similar_index = np.argmax(similarity_scores)
#                 most_similar_score = similarity_scores[most_similar_index]
                
#                 return jsonify({
#                     'most_similar_employee_index': int(most_similar_index),
#                     'similarity_score': float(most_similar_score),
#                     'AI_response': response_data
#                 })
#             else:
#                 logging.error(f"API request failed with status code {response.status_code}: {response.text}")
#                 with open('error_response.json', 'w') as json_file:
#                     json.dump(response.json(), json_file)
#                 return jsonify({'error': 'Failed to process the request to the API'}), response.status_code
#         except Exception as e:
#             logging.error(f"Error making API request: {e}")
#             logging.error(traceback.format_exc())
#             return jsonify({'error': 'Failed to process the request to the API'}), 500
    
#     return jsonify({'error': 'Failed to process the file'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)