import { createTheme } from '@mui/material/styles';
import { pdfStyles } from '../styles/pdfStyles';

const theme = createTheme({
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        ...pdfStyles,
      },
    },
  },
  // ... rest of your theme configuration
});

export default theme; 