import React, { useState } from 'react';
import { TextField, TextareaAutosize, Select, MenuItem, Button, Grid, Typography, FormControl, InputLabel, FormHelperText } from '@mui/material';

const SimpleForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    date_of_birth: '',
    phone_number: '',
    permanent_address: '',
    highest_qualification: '',
    work_experience_count: '',
    research_publications_count: '',
    presented_count: '',
    workshop_attended_count: ''
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Form submitted:', formData);
  };

  const generateOptions = (maxValue) => {
    const options = [];
    for (let i = 0; i <= maxValue; i++) {
      options.push(<MenuItem key={i} value={i}>{i}</MenuItem>);
    }
    return options;
  };

  return (
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h5" component="h2" gutterBottom>
            Personal Information
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <TextField
            id="name"
            label="Name"
            variant="outlined"
            name="name"
            fullWidth
            value={formData.name}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            id="email"
            label="Email"
            variant="outlined"
            type="email"
            name="email"
            fullWidth
            value={formData.email}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            id="dob"
            label="Date of Birth"
            variant="outlined"
            name="date_of_birth"
            fullWidth
            value={formData.date_of_birth}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            id="mobilenumber"
            label="Mobile Number"
            variant="outlined"
            name="phone_number"
            fullWidth
            value={formData.phone_number}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={12}>
          <TextareaAutosize
            id="permanentaddress"
            aria-label="Permanent Address"
            placeholder="Permanent Address"
            name="permanent_address"
            minRows={3}
            style={{ width: '100%' }}
            value={formData.permanent_address}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h5" component="h2" gutterBottom>
            Qualifications & Experience
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <TextField
            id="education"
            label="Highest Qualification"
            variant="outlined"
            name="highest_qualification"
            fullWidth
            value={formData.highest_qualification}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={6}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel id="work-experience-label">Work Experience Count</InputLabel>
            <Select
              id="workExperience"
              labelId="work-experience-label"
              name="work_experience_count"
              value={formData.work_experience_count}
              onChange={handleChange}
              label="Work Experience Count"
            >
              {generateOptions(100)}
            </Select>
            <FormHelperText>Select your work experience count</FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={6}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel id="research-experience-label">Research Publications Count</InputLabel>
            <Select
              id="researchExperience"
              labelId="research-experience-label"
              name="research_publications_count"
              value={formData.research_publications_count}
              onChange={handleChange}
              label="Research Publications Count"
            >
              {generateOptions(100)}
            </Select>
            <FormHelperText>Select your research publications count</FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={6}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel id="research-presented-label">Research Papers Presented Count</InputLabel>
            <Select
              id="researchPresented"
              labelId="research-presented-label"
              name="presented_count"
              value={formData.presented_count}
              onChange={handleChange}
              label="Research Papers Presented Count"
            >
              {generateOptions(100)}
            </Select>
            <FormHelperText>Select your research papers presented count</FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={6}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel id="training-workshops-label">Workshops Attended Count</InputLabel>
            <Select
              id="trainingWorkshops"
              labelId="training-workshops-label"
              name="workshop_attended_count"
              value={formData.workshop_attended_count}
              onChange={handleChange}
              label="Workshops Attended Count"
            >
              {generateOptions(100)}
            </Select>
            <FormHelperText>Select your workshops attended count</FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Submit
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default SimpleForm;
