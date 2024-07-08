# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from PyPDF2 import PdfReader
# import re
# import json

# app = Flask(__name__)
# CORS(app, supports_credentials=True)  # Enable CORS for all origins

# def extract_information(extracted_text):
#     name = ''
#     email = ''
#     highest_qualification = ''
#     phone_number = ''
#     permanent_address = ''
#     date_of_birth = ''
#     research_publications_count = 0
#     workshop_attended_count = 0  # Initialize count for workshops attended
#     work_experience_count = 0  # Initialize count for work experience
    
#     # Define regular expressions
#     name_pattern = re.compile(r'^[A-Z][a-z]+(?: [A-Z][a-z]+)+')  # Assumes name starts with capital letters
#     email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
#     phone_pattern = re.compile(r'\b\d{10}\b')
#     dob_pattern = re.compile(r'Date of Birth\s*([^\n]+)')
#     address_pattern = re.compile(r'Permanent Address\s*([^\n]+)')
#     education_keywords = ['PhD', 'ph.d', 'Doctorate', 'masters', "B.E", "B.Tech", 'MBA','bachelors']
    
#     # Count occurrences of "Presented" and research publication keywords
#     presented_count = 0
#     research_keywords = ['Published', 'ISSN','Publishers','Publishing','Journal']
    
#     for page in extracted_text:
#         text = page['text']
#         # Extract name, email, phone number, date of birth, permanent address, and highest qualification
#         if not name:
#             match = name_pattern.search(text)
#             if match:
#                 name = match.group()
        
#         if not email:
#             match = email_pattern.search(text)
#             if match:
#                 email = match.group()
        
#         if not phone_number:
#             match = phone_pattern.search(text)
#             if match:
#                 phone_number = match.group()
        
#         if not date_of_birth:
#             match = dob_pattern.search(text)
#             if match:
#                 date_of_birth = match.group(1).strip()
        
#         if not permanent_address:
#             match = address_pattern.search(text)
#             if match:
#                 permanent_address = match.group(1).strip()
        
#         if not highest_qualification:
#             for keyword in education_keywords:
#                 if keyword.lower() in text.lower():
#                     highest_qualification = keyword
#                     break
        
#         # Count occurrences of "Presented"
#         presented_count += text.count("Presented")
        
#         # Count occurrences of research publication keywords (case insensitive)
#         for keyword in research_keywords:
#             research_publications_count += text.lower().count(keyword.lower())
        
#         # Count occurrences of workshop attended keywords (case insensitive)
#         workshop_attended_count += text.lower().count("workshop")
#         workshop_attended_count += text.lower().count("online faculty development programme on")
        
#         # Count occurrences of work experience keywords (case insensitive)
#         work_experience_count += len(re.findall(r'Worked', text, re.IGNORECASE))
#         work_experience_count += len(re.findall(r'Working', text, re.IGNORECASE))
    
#     return {
#         'name': name,
#         'email': email,
#         'phone_number': phone_number,
#         'date_of_birth': date_of_birth,
#         'permanent_address': permanent_address,
#         'highest_qualification': highest_qualification,
#         'presented_count': presented_count,
#         'research_publications_count': research_publications_count,
#         'workshop_attended_count': workshop_attended_count,  # Include workshop attended count
#         'work_experience_count': work_experience_count  # Include work experience count
#     }

# @app.route('/api/upload-resume', methods=['POST'])
# def upload_resume():
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     resume_file = request.files['resume']
#     reader = PdfReader(resume_file) 
    
#     extracted_text = []
#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]
#         text = page.extract_text() 
#         # Structure the extracted text into a dictionary
#         extracted_text.append({'page_number': page_num + 1, 'text': text})
    
#     # Extract specific information
#     extracted_info = extract_information(extracted_text)
    
#     # Store the extracted text and information in a JSON file
#     with open('extracted_resume.json', 'w') as json_file:
#         json.dump({'pages': extracted_text, 'extracted_info': extracted_info}, json_file)
    
#     return jsonify({'message': 'Resume uploaded successfully', 'extracted_info': extracted_info}), 200

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from PyPDF2 import PdfReader
# import re
# import json

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all origins

# def extract_education_details(extracted_text):
#     education_titles = [
#         "Education", "Academic Background", "Qualifications", "Educational Background", 
#         "Academic Qualifications", "Professional Qualification", "Academic History", 
#         "Scholastic Background", "Background", "Educational Background", 
#         "Education and Training", "Academic Training", "Professional Education", 
#         "Education History", "Academic Achievements", "Scholastic Achievements", 
#         "Formal Education", "Educational Qualifications", "Professional Background"
#     ]
    
#     stop_titles = [
#         "Project", "Projects", "Achievement", "Achievements", "Research Work", 
#         "Research", "Experience", "Work Experience", "Professional Experience", 
#         "Skills", "Certifications", "Publications", "Professional Activities", 
#         "Career Summary", "Career Objective", "Objective", "Personal Information", 
#         "Personal Details", "Professional Experience", "Work History", "Employment History", 
#         "Volunteer Experience", "Internship Experience", "Technical Skills", "Technical Proficiencies", 
#         "Awards", "Honors", "Languages", "References", "Interests", "Hobbies", "Extracurricular Activities",
#         "Teaching Experience", "Academic Appointments", "Teaching Interests", "Course Development",
#         "Courses Taught", "Workshops Conducted", "Seminars", "Grants and Funding", "Fellowships",
#         "Awards and Honors", "Conference Presentations", "Thesis Supervision", "Dissertation Supervision",
#         "Academic Service", "Committee Membership", "Administrative Experience", "Community Service",
#         "Outreach Activities", "Professional Memberships", "Faculty Development Program", "Research Publication",
#         "Research Experience", "Research Paper Presented", "Paper Presented", "Conferences Attended",
#         "Symposiums", "Training Programs", "Consultancy", "Collaborations", "Projects Guided",
#         "Invited Talks", "Guest Lectures", "Panel Discussions", "Keynote Addresses",
#         "Advisory Roles", "Editorial Boards", "Review Boards", "Research Grants",
#         "Patents", "Intellectual Property", "Book Chapters", "Books Published",
#         "Journals Edited", "Professional Development", "Workshops Attended",
#         "Faculty Workshops", "Academic Projects", "Capstone Projects", "Thesis Evaluation",
#         "Doctoral Committee", "M.Phil Committee", "Ph.D. Committee", "External Examiner",
#         "Industry Experience", "Academic Collaborations", "Exchange Programs",
#         "Visiting Faculty", "Professional Engagements", "Seminars Conducted",
#         "Symposiums Conducted", "Conference Organization", "Academic Workshops",
#         "Research Conferences", "Seminar Participation", "Academic Publications",
#         "Teaching Innovations", "Pedagogical Innovations", "Curriculum Development",
#         "Curriculum Design", "Syllabus Design", "Course Coordination", "Course Leadership",
#         "Course Moderation", "Education Leadership", "Educational Administration",
#         "Conferences Attended", "Books Published", "Academic Presentations", "Journal Publications",
#         "Book Publications", "Research Projects", "Grants Received", "Honors and Awards",
#         "Theses Supervised", "Dissertations Supervised", "Academic Research", "Scholarships",
#         "Professional Development Courses", "Training Attended", "Professional Certifications",
#         "Educational Certifications", "Academic Honors", "Research Fellowships", "Study Abroad Programs",
#         "Educational Trips", "Pedagogical Training", "Educational Workshops", "Faculty Training Programs",
#         "Academic Qualifications", "Graduate Studies", "Postgraduate Studies", "Doctoral Studies",
#         "Undergraduate Studies", "Research Assignments", "Research Collaboration", "Academic Conferences",
#         "Educational Seminars", "Symposium Attendance", "Fellowship Programs", "Teaching Fellowships",
#         "Research Fellowships", "Scholar Programs", "Advanced Training Programs", "Research Mentorship",
#         "Mentorship Programs", "Educational Mentorship", "Academic Awards", "Research Awards",
#         "Position of Authority", "Leadership Experience", "Management Experience", "Administrative Experience"
#     ]
    
    
#     education_titles_lower = [title.lower() for title in education_titles]
#     stop_titles_lower = [title.lower() for title in stop_titles]
    
#     education_section = []
#     capturing = False

#     for page in extracted_text:
#         lines = page['text'].split('\n')
#         for line in lines:
#             if any(title in line.lower() for title in education_titles_lower):
#                 capturing = True
#                 continue  # Skip the heading line itself
#             elif capturing and any(title in line.lower() for title in stop_titles_lower):
#                 capturing = False
#                 break  # Stop capturing on encountering a stop title

#             if capturing:
#                 education_section.append(line)

#     return "\n".join(education_section).strip() if education_section else "Education details not found"

# def extract_information(extracted_text):
#     name = ''
#     email = ''
#     highest_qualification = ''
#     phone_number = ''
#     permanent_address = ''
#     date_of_birth = ''
#     research_publications_count = 0
#     workshop_attended_count = 0  # Initialize count for workshops attended
#     work_experience_count = 0  # Initialize count for work experience
    
#     # Define regular expressions
#     name_pattern = re.compile(r'^[A-Z][a-z]+(?: [A-Z][a-z]+)+')  # Assumes name starts with capital letters
#     email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
#     phone_pattern = re.compile(r'\b\d{10}\b')
#     dob_pattern = re.compile(r'Date of Birth\s*([^\n]+)')
#     address_pattern = re.compile(r'Permanent Address\s*([^\n]+)')
#     education_keywords = [
#         'Post-doctoral Fellowship', 'pdf', 'postdoctoral', 'Postdoctoral Fellow'
#         ,'PhD', 'Ph.D', 'Doctorate', 'DPhil', 'Doctor of Philosophy', 'Doctor of Science', 'Sc.D', 'Ed.D', 'D.M.A', 'J.S.D', 'LL.D', 'D.Litt', 'D.Sc', 'D.B.A', 'Doctorate of Business Administration',
#         'Masters', 'M.Sc', 'M.A', 'M.Com', 'MBA', 'LLM', 'MD', 'MPhil', 'Master of Science', 'Master of Arts', 'Master of Commerce', 'Master of Business Administration', 'Master of Laws', 'Master of Philosophy', 'M.Ed', 'M.Tech', 'M.Eng', 'MFA', 'Master of Fine Arts', 'MPA', 'Master of Public Administration', 'MSW', 'Master of Social Work',
#         'Bachelors', 'B.Sc', 'B.A', 'B.Com', 'BBA', 'LLB', 'MBBS', 'B.E', 'B.Tech', 'Bachelor of Science', 'Bachelor of Arts', 'Bachelor of Commerce', 'Bachelor of Business Administration', 'Bachelor of Laws', 'Bachelor of Medicine, Bachelor of Surgery', 'Bachelor of Engineering', 'Bachelor of Technology', 'Undergraduate',
#         'Diploma', 'Certificate', 'Associate Degree', 'Advanced Diploma', 'Postgraduate Diploma', 'Graduate Diploma', 'Diploma of Higher Education', 'Foundation Degree', 'Higher National Diploma', 'HND'
#     ]
    
#     # Count occurrences of "Presented" and research publication keywords
#     presented_count = 0
#     research_keywords = ['Published', 'ISSN','Publishers','Publishing','Journal']
    
#     for page in extracted_text:
#         text = page['text']
#         # Extract name, email, phone number, date of birth, permanent address, and highest qualification
#         if not name:
#             match = name_pattern.search(text)
#             if match:
#                 name = match.group()
        
#         if not email:
#             match = email_pattern.search(text)
#             if match:
#                 email = match.group()
        
#         if not phone_number:
#             match = phone_pattern.search(text)
#             if match:
#                 phone_number = match.group()
        
#         if not date_of_birth:
#             match = dob_pattern.search(text)
#             if match:
#                 date_of_birth = match.group(1).strip()
        
#         if not permanent_address:
#             match = address_pattern.search(text)
#             if match:
#                 permanent_address = match.group(1).strip()
        
#         if not highest_qualification:
#             for keyword in education_keywords:
#                 if keyword.lower() in text.lower():
#                     highest_qualification = keyword
#                     break
        
#         # Count occurrences of "Presented"
#         presented_count += text.count("Presented")
        
#         # Count occurrences of research publication keywords (case insensitive)
#         for keyword in research_keywords:
#             research_publications_count += text.lower().count(keyword.lower())
        
#         # Count occurrences of workshop attended keywords (case insensitive)
#         workshop_attended_count += text.lower().count("workshop")
#         workshop_attended_count += text.lower().count("online faculty development programme on")
        
#         # Count occurrences of work experience keywords (case insensitive)
#         work_experience_count += len(re.findall(r'Worked', text, re.IGNORECASE))
#         work_experience_count += len(re.findall(r'Working', text, re.IGNORECASE))
    
#     # Extract education details
#     education_details = extract_education_details(extracted_text)
    
#     return {
#         'name': name,
#         'email': email,
#         'phone_number': phone_number,
#         'date_of_birth': date_of_birth,
#         'permanent_address': permanent_address,
#         'highest_qualification': highest_qualification,
#         'presented_count': presented_count,
#         'research_publications_count': research_publications_count,
#         'workshop_attended_count': workshop_attended_count,  # Include workshop attended count
#         'work_experience_count': work_experience_count,  # Include work experience count
#         'education_details': education_details  # Include education details
#     }

# @app.route('/api/upload-resume', methods=['POST'])
# def upload_resume():
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     resume_file = request.files['resume']
#     reader = PdfReader(resume_file) 
    
#     extracted_text = []
#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]
#         text = page.extract_text() 
#         # Structure the extracted text into a dictionary
#         extracted_text.append({'page_number': page_num + 1, 'text': text})
    
#     # Extract specific information
#     extracted_info = extract_information(extracted_text)
    
#     # Store the extracted text and information in a JSON file
#     with open('extracted_resume.json', 'w') as json_file:
#         json.dump({'pages': extracted_text, 'extracted_info': extracted_info}, json_file)
    
#     return jsonify({'message': 'Resume uploaded successfully', 'extracted_info': extracted_info}), 200

# if __name__ == '__main__':
#     app.run(debug=True)




























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
