import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Grid,
  Paper,
  Container,
} from '@mui/material';
import {
  PostAdd,
  Analytics,
  Schedule,
} from '@mui/icons-material';

const FeatureCard = ({ icon, title, description }) => (
  <Paper
    elevation={3}
    sx={{
      p: 3,
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      textAlign: 'center',
    }}
  >
    {icon}
    <Typography variant="h6" sx={{ my: 2 }}>
      {title}
    </Typography>
    <Typography color="text.secondary">{description}</Typography>
  </Paper>
);

const Welcome = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <PostAdd sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'AI-Powered Content Creation',
      description:
        'Generate engaging LinkedIn posts with our advanced AI technology. Get content suggestions tailored to your professional profile.',
    },
    {
      icon: <Analytics sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Performance Analytics',
      description:
        'Track your content performance with detailed analytics. Understand what works best for your audience.',
    },
    {
      icon: <Schedule sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Smart Scheduling',
      description:
        'Schedule your posts for optimal engagement times. Our system analyzes the best posting times for your audience.',
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 8 }}>
        {/* Hero Section */}
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography variant="h3" component="h1" gutterBottom>
            LinkedIn Content Creator
          </Typography>
          <Typography
            variant="h5"
            color="text.secondary"
            sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}
          >
            Create engaging LinkedIn content with AI-powered suggestions and smart scheduling
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/content/create')}
            startIcon={<PostAdd />}
          >
            Create Content
          </Button>
        </Box>

        {/* Features Section */}
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <FeatureCard {...feature} />
            </Grid>
          ))}
        </Grid>

        {/* How It Works Section */}
        <Box sx={{ mt: 8, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>
            How It Works
          </Typography>
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                1. Upload CV
              </Typography>
              <Typography color="text.secondary">
                Upload your CV to get started with personalized content
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                2. Generate Content
              </Typography>
              <Typography color="text.secondary">
                Get AI-powered content suggestions based on your profile
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                3. Review and Post
              </Typography>
              <Typography color="text.secondary">
                Review, edit, and schedule your content for optimal engagement
              </Typography>
            </Grid>
          </Grid>
        </Box>

        {/* Call to Action */}
        <Box sx={{ mt: 8, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            Ready to create engaging LinkedIn content?
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/content/create')}
            sx={{ mt: 2 }}
          >
            Start Creating
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Welcome; 