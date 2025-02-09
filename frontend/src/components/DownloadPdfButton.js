import React from 'react';
import { Button } from '@mui/material';
import { PictureAsPdf } from '@mui/icons-material';
import { usePDF } from 'react-to-pdf';

const DownloadPdfButton = ({ targetRef, fileName = 'linkedin-content.pdf' }) => {
  const { toPDF } = usePDF({
    filename: fileName,
    targetRef: targetRef,
    options: {
      page: {
        margin: 20,
        format: 'A4',
      },
      html2canvas: {
        scale: 2,
        useCORS: true,
      },
    },
  });

  return (
    <Button
      variant="contained"
      color="primary"
      startIcon={<PictureAsPdf />}
      onClick={() => toPDF()}
      sx={{ ml: 2 }}
    >
      Download PDF
    </Button>
  );
};

export default DownloadPdfButton; 