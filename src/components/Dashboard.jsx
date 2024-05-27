import React, { useState } from 'react';
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Container,
  Grid,
  TextField
} from '@mui/material';
import { getDocument } from 'pdfjs-dist';

const extractTextFromPDF = async (file) => {
  const arrayBuffer = await file.arrayBuffer();
  const pdf = await getDocument(new Uint8Array(arrayBuffer)).promise;
  const page = await pdf.getPage(1);
  const textContent = await page.getTextContent();
  return textContent.items.map((item) => item.str).join('\n');
};

// Resume Upload Component
const ResumeUpload = ({ onResumeUpload }) => {
  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    const text = await extractTextFromPDF(file);
    onResumeUpload(file, text);
  };

  return (
    <Card>
      <CardHeader title="Upload Resume" />
      <CardContent>
        <input
          accept=".pdf,.doc,.docx"
          style={{ display: 'none' }}
          id="resume-upload"
          type="file"
          onChange={handleResumeUpload}
        />
        <label htmlFor="resume-upload">
          <Button variant="contained" component="span">
            Upload Resume
          </Button>
        </label>
      </CardContent>
    </Card>
  );
};

// Dataset Selection Component
const DatasetSelection = ({ datasetFilePath, onDatasetFilePathChange }) => {
  return (
    <Card>
      <CardHeader title="Dataset Selection" />
      <CardContent>
        <TextField
          fullWidth
          label="Enter dataset file path"
          value={datasetFilePath}
          onChange={onDatasetFilePathChange}
        />
      </CardContent>
    </Card>
  );
};

// Custom Dataset Upload Component
const CustomDatasetUpload = ({ onAddDataset }) => {
  const [customDataset, setCustomDataset] = useState(null);

  const handleCustomDatasetUpload = (e) => {
    const file = e.target.files[0];
    setCustomDataset(file);
  };

  const handleAddDataset = () => {
    if (customDataset) {
      onAddDataset(customDataset);
      setCustomDataset(null);
    }
  };

  return (
    <Card>
      <CardHeader title="Upload Custom Dataset" />
      <CardContent>
        <input
          style={{ display: 'none' }}
          id="custom-dataset-upload"
          type="file"
          onChange={handleCustomDatasetUpload}
        />
        <label htmlFor="custom-dataset-upload">
          <Button variant="contained" component="span">
            Choose File
          </Button>
        </label>
        {customDataset && (
          <Button
            variant="contained"
            color="primary"
            onClick={handleAddDataset}
            style={{ marginLeft: '10px' }}
          >
            Add Dataset
          </Button>
        )}
      </CardContent>
    </Card>
  );
};

// Dashboard Component
const Dashboard = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [datasetFilePath, setDatasetFilePath] = useState('');
  const [datasets, setDatasets] = useState([]);

  const handleResumeUpload = (file, text) => {
    setResumeFile(file);
    setResumeText(text);
  };

  const handleDatasetFilePathChange = (e) => {
    setDatasetFilePath(e.target.value);
  };

  const handleAddDataset = (dataset) => {
    setDatasets([...datasets, dataset]);
  };

  const handleAnalyze = () => {
    // Perform analysis logic here
    console.log('Analyzing resume:', resumeFile);
    console.log('Resume text:', resumeText);
    console.log('Dataset file path:', datasetFilePath);
    console.log('Custom datasets:', datasets);
  };

  return (
    <Container>
      <h2>Dashboard</h2>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <ResumeUpload onResumeUpload={handleResumeUpload} />
        </Grid>
        <Grid item xs={12}>
          <DatasetSelection
            datasetFilePath={datasetFilePath}
            onDatasetFilePathChange={handleDatasetFilePathChange}
          />
        </Grid>
        <Grid item xs={12}>
          <CustomDatasetUpload onAddDataset={handleAddDataset} />
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleAnalyze}
          >
            Analyze
          </Button>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
