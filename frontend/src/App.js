import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import Welcome from './components/Welcome';
import ContentCreator from './components/ContentCreator';

const theme = createTheme({
  palette: {
    primary: {
      main: '#0A66C2', // LinkedIn blue
    },
    secondary: {
      main: '#057642', // Professional green
    },
    background: {
      default: '#f3f2ef', // LinkedIn background color
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      'Segoe UI',
      'Roboto',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/content/create" element={<ContentCreator />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App; 