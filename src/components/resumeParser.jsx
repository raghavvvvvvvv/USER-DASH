const axios = require('axios');
const fs = require('fs');

// Your API key
const apiKey = 'sgvKuS4u5PBghDDSSqvvd5t58N6xY1AT';

// URL for the API Layer endpoint
const url = 'https://api.apilayer.com/resume_parser';

// Path to the resume file you want to parse
const resumeFilePath = 'path/to/your/resume.pdf';

// Read the resume file
fs.readFile(resumeFilePath, (err, resumeContent) => {
    if (err) {
        console.error('Error reading the resume file:', err);
        return;
    }

    // Make the API request
    axios.post(url, resumeContent, {
        headers: {
            'apikey': apiKey,
            'Content-Type': 'application/pdf'  // Adjust content type based on the file type
        }
    })
    .then(response => {
        // Check if the request was successful
        if (response.status === 200) {
            // Extract the data from the response
            const resumeData = response.data;

            // Path to the JSON file where data will be saved
            const outputJsonPath = 'parsed_resume.json';

            // Save the extracted data to a JSON file
            fs.writeFile(outputJsonPath, JSON.stringify(resumeData, null, 4), err => {
                if (err) {
                    console.error('Error writing to JSON file:', err);
                } else {
                    console.log(`Resume data successfully extracted and saved to ${outputJsonPath}`);
                }
            });
        } else {
            console.error(`Failed to extract resume data. Status code: ${response.status}`);
            console.error(response.data);
        }
    })
    .catch(error => {
        console.error('Error making the API request:', error);
    });
});
