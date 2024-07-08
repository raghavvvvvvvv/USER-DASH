import React, { useState } from 'react';
import axios from 'axios';

function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState([]);
  const [similarityScores, setSimilarityScores] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/upload-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setExtractedText(response.data.structured_data || []);
      setSimilarityScores(response.data.similarity_scores || []);
    } catch (error) {
      console.error('Error uploading file:', error.response ? error.response.data : error.message);
      alert('An error occurred while uploading the file.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept=".pdf" />
      <button onClick={handleUpload} disabled={isLoading}>
        {isLoading ? 'Extracting...' : 'Upload and Extract'}
      </button>
      {/* {extractedText && (
        <div>
          <h2>Extracted Text:</h2>
          <pre>{JSON.stringify(extractedText, null, 2)}</pre>
        </div>
      )}
      {similarityScores.length > 0 && (
        <div>
          <h2>Cosine Similarity Scores:</h2>
          <ul>
            {similarityScores.map((score, index) => (
              <li key={index}>Score {index + 1}: {score}</li>
            ))}
          </ul>
        </div>
      )} */}
    </div>
  );
}

export default ResumeUploader;
