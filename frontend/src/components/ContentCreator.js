import React, { useState, useRef } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  Paper,
  Typography,
  Card,
  CardContent,
  IconButton,
  Divider,
  Chip,
  Link,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  ContentCopy,
  Upload,
  ExpandMore,
  Lightbulb,
  Analytics,
  Article,
  TrendingUp,
} from '@mui/icons-material';
import ApiKeyInput from './ApiKeyInput';
import DownloadPdfButton from './DownloadPdfButton';

const ContentCreator = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [posts, setPosts] = useState([]);
  const [cvAnalysis, setCvAnalysis] = useState(null);
  const [contentIdeas, setContentIdeas] = useState(null);
  const [news, setNews] = useState([]);
  const [error, setError] = useState(null);
  const [industryTrends, setIndustryTrends] = useState(null);
  const [engagementSuggestions, setEngagementSuggestions] = useState({});
  const [apiKey, setApiKey] = useState('');
  const [isApiKeyVerified, setIsApiKeyVerified] = useState(false);
  const [apiKeyError, setApiKeyError] = useState(null);
  const contentRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please upload a PDF file');
      setFile(null);
    }
  };

  const handleCopyToClipboard = (content) => {
    navigator.clipboard.writeText(content);
  };

  const verifyApiKey = async () => {
    setApiKeyError(null);
    setLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/verify-api-key`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ api_key: apiKey }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Invalid API key');
      }

      setIsApiKeyVerified(true);
    } catch (err) {
      setApiKeyError(err.message);
      setIsApiKeyVerified(false);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('cv', file);
    formData.append('api_key', apiKey);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/generate-posts`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate posts');
      }

      setPosts(data.posts);
      setCvAnalysis(data.cv_analysis);
      setContentIdeas(data.content_ideas);
      setIndustryTrends(data.industry_trends);
      setNews(data.news);

      // Create engagement suggestions map
      const suggestions = {};
      data.posts.forEach(post => {
        if (post.engagement_suggestions) {
          suggestions[post.type] = post.engagement_suggestions;
        }
      });
      setEngagementSuggestions(suggestions);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderIndustryTrends = () => {
    if (!industryTrends) return null;

    return (
      <Accordion defaultExpanded sx={{ mt: 2 }}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <TrendingUp />
            <Typography variant="h6">Industry Trends</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body1" component="div" sx={{ whiteSpace: 'pre-wrap' }}>
            {industryTrends}
          </Typography>
        </AccordionDetails>
      </Accordion>
    );
  };

  const renderPost = (post, index) => (
    <Card key={index} sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="h6" color="primary">
            {post.type.replace('_', ' ').toUpperCase()}
          </Typography>
          <IconButton
            onClick={() => handleCopyToClipboard(post.content)}
            size="small"
          >
            <ContentCopy />
          </IconButton>
        </Box>
        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
          {post.content}
        </Typography>
        
        {engagementSuggestions[post.type] && (
          <Box sx={{ mt: 2 }}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle2" color="primary" gutterBottom>
              Engagement Suggestions
            </Typography>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
              {engagementSuggestions[post.type]}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ p: 3 }}>
      {!isApiKeyVerified ? (
        <ApiKeyInput
          apiKey={apiKey}
          setApiKey={setApiKey}
          onSubmit={verifyApiKey}
          error={apiKeyError}
        />
      ) : (
        <>
          <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h4">
                LinkedIn Content Generator
              </Typography>
              {(posts.length > 0 || contentIdeas || industryTrends) && (
                <DownloadPdfButton 
                  targetRef={contentRef}
                  fileName={`linkedin-content-${new Date().toISOString().split('T')[0]}.pdf`}
                />
              )}
            </Box>

            <Typography color="text.secondary" paragraph>
              Upload your CV (PDF) and we'll analyze it to generate personalized LinkedIn content ideas and posts.
            </Typography>

            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
              <Button
                variant="contained"
                component="label"
                startIcon={<Upload />}
              >
                Upload CV
                <input
                  type="file"
                  hidden
                  accept="application/pdf"
                  onChange={handleFileChange}
                />
              </Button>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
                disabled={!file || loading}
              >
                Generate Content
              </Button>
            </Box>

            {file && (
              <Typography variant="body2" color="text.secondary">
                Selected file: {file.name}
              </Typography>
            )}

            {error && (
              <Typography color="error" sx={{ mt: 2 }}>
                {error}
              </Typography>
            )}

            {loading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <CircularProgress />
              </Box>
            )}

            {cvAnalysis && (
              <Accordion defaultExpanded sx={{ mt: 4 }}>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Analytics />
                    <Typography variant="h6">CV Analysis</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle1" color="primary" gutterBottom>
                        Expertise & Skills
                      </Typography>
                      <Box sx={{ mb: 2 }}>
                        {Array.isArray(cvAnalysis.technical_skills) && cvAnalysis.technical_skills.map((skill, index) => (
                          <Chip key={index} label={skill} sx={{ m: 0.5 }} />
                        ))}
                      </Box>
                      {Array.isArray(cvAnalysis.soft_skills) && cvAnalysis.soft_skills.length > 0 && (
                        <>
                          <Typography variant="subtitle2" color="primary" gutterBottom>
                            Soft Skills
                          </Typography>
                          <Box sx={{ mb: 2 }}>
                            {cvAnalysis.soft_skills.map((skill, index) => (
                              <Chip 
                                key={index} 
                                label={skill} 
                                sx={{ m: 0.5 }}
                                variant="outlined"
                              />
                            ))}
                          </Box>
                        </>
                      )}
                      {Array.isArray(cvAnalysis.content_topics) && cvAnalysis.content_topics.length > 0 && (
                        <>
                          <Typography variant="subtitle2" color="primary" gutterBottom>
                            Content Topics
                          </Typography>
                          <Box sx={{ mb: 2 }}>
                            {cvAnalysis.content_topics.map((topic, index) => (
                              <Chip 
                                key={index} 
                                label={topic} 
                                sx={{ m: 0.5 }}
                                variant="outlined"
                                color="secondary"
                              />
                            ))}
                          </Box>
                        </>
                      )}
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle1" color="primary" gutterBottom>
                        Industry & Level
                      </Typography>
                      <Typography variant="body1" paragraph>
                        {cvAnalysis.industry_focus} • {cvAnalysis.career_level}
                      </Typography>
                      {cvAnalysis.notable_achievements && (
                        <>
                          <Typography variant="subtitle2" color="primary" gutterBottom sx={{ mt: 2 }}>
                            Key Achievements
                          </Typography>
                          <Typography variant="body2" component="div">
                            {cvAnalysis.notable_achievements.split('\n').map((achievement, index) => (
                              <Box key={index} sx={{ mb: 1 }}>• {achievement}</Box>
                            ))}
                          </Typography>
                        </>
                      )}
                    </Grid>
                  </Grid>
                </AccordionDetails>
              </Accordion>
            )}

            {contentIdeas && (
              <Accordion defaultExpanded sx={{ mt: 2 }}>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Lightbulb />
                    <Typography variant="h6">Content Ideas</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    {Object.entries(contentIdeas).map(([key, idea], index) => (
                      <Grid item xs={12} md={6} key={index}>
                        <Card variant="outlined">
                          <CardContent>
                            <Typography variant="h6" gutterBottom>
                              {idea.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" paragraph>
                              {idea.angle}
                            </Typography>
                            <Box>
                              {idea.key_points.map((point, i) => (
                                <Typography key={i} variant="body2" sx={{ mb: 0.5 }}>
                                  • {point}
                                </Typography>
                              ))}
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </AccordionDetails>
              </Accordion>
            )}

            {news.length > 0 && (
              <Accordion defaultExpanded sx={{ mt: 2 }}>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Article />
                    <Typography variant="h6">Related Industry News</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  {news.map((item, index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                      <Link href={item.link} target="_blank" rel="noopener noreferrer">
                        <Typography variant="subtitle1">{item.title}</Typography>
                      </Link>
                      <Typography variant="caption" color="text.secondary">
                        Published: {new Date(item.published).toLocaleDateString()}
                      </Typography>
                    </Box>
                  ))}
                </AccordionDetails>
              </Accordion>
            )}

            {renderIndustryTrends()}

            {posts.length > 0 && (
              <Box sx={{ mt: 4 }}>
                <Typography variant="h5" gutterBottom>
                  Generated Posts
                </Typography>
                {posts.map((post, index) => renderPost(post, index))}
              </Box>
            )}
          </Paper>
        </>
      )}
    </Box>
  );
};

export default ContentCreator; 