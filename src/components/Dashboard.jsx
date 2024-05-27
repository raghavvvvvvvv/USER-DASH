import React, { useState } from 'react';
import { 
  Button, 
  Card, 
  CardContent, 
  CardHeader, 
  Container, 
  Grid, 
  Radio, 
  RadioGroup, 
  FormControlLabel, 
  FormControl, 
  FormLabel, 
  Typography 
} from '@mui/material';

// Resume Upload Component
const ResumeUpload = ({ onResumeUpload, resumeName }) => {
  const handleResumeUpload = (e) => {
    const file = e.target.files[0];
    onResumeUpload(file);
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
        {resumeName && <Typography variant="body2">{`Uploaded: ${resumeName}`}</Typography>}
      </CardContent>
    </Card>
  );
};

// Custom Dataset Upload Component
const CustomDatasetUpload = ({ onAddDataset, datasetName }) => {
  const [customDataset, setCustomDataset] = useState(null);

  const handleCustomDatasetUpload = (e) => {
    const file = e.target.files[0];
    setCustomDataset(file);
    onAddDataset(file);
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
        {datasetName && <Typography variant="body2">{`Uploaded: ${datasetName}`}</Typography>}
      </CardContent>
    </Card>
  );
};

// Dataset Selection Component
const DatasetSelection = ({ selectedDataset, onDatasetChange }) => {
  return (
    <Card>
      <CardHeader title="Select Dataset" />
      <CardContent>
        <FormControl component="fieldset">
          <FormLabel component="legend">Dataset Option</FormLabel>
          <RadioGroup
            aria-label="dataset"
            name="dataset"
            value={selectedDataset}
            onChange={onDatasetChange}
          >
            <FormControlLabel value="default" control={<Radio />} label="Use Default Dataset" />
            <FormControlLabel value="custom" control={<Radio />} label="Upload Custom Dataset" />
          </RadioGroup>
        </FormControl>
      </CardContent>
    </Card>
  );
};

// Dashboard Component
const Dashboard = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [selectedDataset, setSelectedDataset] = useState('default');
  const [customDatasets, setCustomDatasets] = useState([]);
  const [resumeName, setResumeName] = useState('');
  const [datasetName, setDatasetName] = useState('');

  // Predefined dataset file path set in the backend
  const predefinedDatasetFilePath = "/path/to/predefined/dataset";

  const handleResumeUpload = (file) => {
    setResumeFile(file);
    setResumeName(file.name);
  };

  const handleDatasetChange = (e) => {
    setSelectedDataset(e.target.value);
    setDatasetName('');
  };

  const handleAddDataset = (dataset) => {
    setCustomDatasets([...customDatasets, dataset]);
    setDatasetName(dataset.name);
  };

  const handleAnalyze = () => {
    const datasetToUse = selectedDataset === 'default' 
      ? predefinedDatasetFilePath 
      : customDatasets;

    // Perform analysis logic here
    console.log('Analyzing resume:', resumeFile);
    console.log('Dataset(s) in use:', datasetToUse);
  };

  return (
    <Container>
      <h2>Dashboard</h2>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <ResumeUpload 
            onResumeUpload={handleResumeUpload} 
            resumeName={resumeName} 
          />
        </Grid>
        <Grid item xs={12}>
          <DatasetSelection
            selectedDataset={selectedDataset}
            onDatasetChange={handleDatasetChange}
          />
        </Grid>
        {selectedDataset === 'custom' && (
          <Grid item xs={12}>
            <CustomDatasetUpload
              onAddDataset={handleAddDataset}
              datasetName={datasetName}
            />
          </Grid>
        )}
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
