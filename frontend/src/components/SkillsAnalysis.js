import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Pagination,
  Card,
  CardContent,
  IconButton,
  Collapse,
} from '@mui/material';
import {
  Analytics,
  ExpandMore,
  KeyboardArrowDown,
  KeyboardArrowUp,
} from '@mui/icons-material';

const SkillCategory = ({ category, skills }) => {
  const [expanded, setExpanded] = useState(false);
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  const displayedSkills = Array.isArray(skills) 
    ? skills.slice((page - 1) * itemsPerPage, page * itemsPerPage)
    : [];

  const totalPages = Math.ceil(skills.length / itemsPerPage);

  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="subtitle1" color="primary">
            {category}
          </Typography>
          <IconButton 
            onClick={() => setExpanded(!expanded)}
            size="small"
          >
            {expanded ? <KeyboardArrowUp /> : <KeyboardArrowDown />}
          </IconButton>
        </Box>
        
        <Collapse in={expanded}>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
            {displayedSkills.map((skill, idx) => (
              <Chip
                key={idx}
                label={skill}
                variant="outlined"
                sx={{ m: 0.5 }}
              />
            ))}
          </Box>
          
          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                size="small"
                color="primary"
              />
            </Box>
          )}
        </Collapse>
      </CardContent>
    </Card>
  );
};

const SkillsAnalysis = ({ skillsAnalysis }) => {
  if (!skillsAnalysis) return null;

  // Group skills into categories
  const groupedSkills = Object.entries(skillsAnalysis).reduce((acc, [category, skills]) => {
    const groupKey = category.includes('Technical') ? 'Technical Skills' :
                    category.includes('Soft') ? 'Soft Skills' :
                    category.includes('Domain') ? 'Domain Knowledge' : 'Other Skills';
    
    if (!acc[groupKey]) acc[groupKey] = {};
    acc[groupKey][category] = skills;
    return acc;
  }, {});

  return (
    <Accordion defaultExpanded sx={{ mt: 2 }}>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Analytics />
          <Typography variant="h6">Skills Analysis</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={2}>
          {Object.entries(groupedSkills).map(([group, categories], index) => (
            <Grid item xs={12} key={index}>
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                {group}
              </Typography>
              {Object.entries(categories).map(([category, skills], idx) => (
                <SkillCategory
                  key={idx}
                  category={category}
                  skills={skills}
                />
              ))}
            </Grid>
          ))}
        </Grid>
      </AccordionDetails>
    </Accordion>
  );
};

export default SkillsAnalysis; 