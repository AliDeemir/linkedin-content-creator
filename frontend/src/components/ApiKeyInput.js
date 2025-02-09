import React from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Alert,
} from '@mui/material';
import { Key } from '@mui/icons-material';

const ApiKeyInput = ({ apiKey, setApiKey, onSubmit, error }) => {
  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Key />
        Enter Your OpenAI API Key
      </Typography>
      
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Your API key is required to generate content. It will only be used for your current session.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TextField
        fullWidth
        label="OpenAI API Key"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        type="password"
        placeholder="sk-..."
        sx={{ mb: 2 }}
      />

      <Button
        variant="contained"
        onClick={onSubmit}
        disabled={!apiKey}
        fullWidth
      >
        Verify API Key
      </Button>
    </Box>
  );
};

export default ApiKeyInput; 