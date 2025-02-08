import React, { useState } from 'react';
import { Box, Container, Paper, Typography, Button, Alert, Snackbar } from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { analyzeDocument } from './services/api';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeDocument(selectedFile);
      setAnalysis(result.analysis);
    } catch (error) {
      setError(error.response?.data?.detail || 'An error occurred while analyzing the document');
      console.error('Error analyzing file:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseError = () => {
    setError(null);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Conflict Analysis
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, minHeight: '70vh' }}>
        <Paper 
          elevation={3} 
          sx={{ 
            flex: analysis ? 1 : 2,
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <Typography variant="h6" gutterBottom>
            Upload PDF Document
          </Typography>
          <Button
            component="label"
            variant="contained"
            startIcon={<CloudUploadIcon />}
            sx={{ mb: 2 }}
          >
            Choose File
            <VisuallyHiddenInput type="file" accept=".pdf" onChange={handleFileChange} />
          </Button>
          {selectedFile && (
            <>
              <Typography variant="body1" sx={{ mb: 2 }}>
                Selected file: {selectedFile.name}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={handleAnalyze}
                disabled={loading}
              >
                {loading ? 'Analyzing...' : 'Analyze'}
              </Button>
            </>
          )}
        </Paper>

        {analysis && (
          <Paper 
            elevation={3} 
            sx={{ 
              flex: 1,
              p: 3,
              overflowY: 'auto'
            }}
          >
            <Typography variant="h6" gutterBottom>
              Analysis Results
            </Typography>
            {analysis.conflicts && analysis.conflicts.map((conflict, index) => (
              <Box key={index} sx={{ mb: 3 }}>
                <Typography variant="subtitle1" color="primary" gutterBottom>
                  Conflict #{index + 1}
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>Section 1:</strong> {conflict.section1}
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>Section 2:</strong> {conflict.section2}
                </Typography>
                <Typography variant="body2">
                  <strong>Description:</strong> {conflict.conflict_description}
                </Typography>
              </Box>
            ))}
            {analysis.conflicts && analysis.conflicts.length === 0 && (
              <Typography variant="body1">
                No conflicts found in the document.
              </Typography>
            )}
          </Paper>
        )}
      </Box>

      <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseError}>
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default App; 