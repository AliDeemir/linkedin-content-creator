from openai import OpenAI
from django.conf import settings
import requests
from bs4 import BeautifulSoup
import json

def get_openai_client(api_key=None):
    """Create and return an OpenAI client instance"""
    print(f"Attempting to create OpenAI client with key: {api_key[:10]}..." if api_key else "No API key provided")
    
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    if not isinstance(api_key, str):
        raise ValueError("API key must be a string")
    
    if not api_key.startswith('sk-'):
        raise ValueError("Invalid API key format. Key should start with 'sk-'")
    
    try:
        # Initialize with base configuration
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1",  # Explicitly set base URL
            timeout=30.0,  # Set reasonable timeout
            max_retries=2  # Set retry limit
        )
        print("Successfully created OpenAI client")
        return client
    except Exception as e:
        print(f"Error creating OpenAI client: {str(e)}")
        raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")

def search_news(query, num_results=5):
    """Search for relevant news articles using Google News"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = f'https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en'
        response = requests.get(url, headers=headers)
        
        # Explicitly use lxml parser
        soup = BeautifulSoup(response.text, 'lxml-xml')
        
        # Fallback to html parser if lxml fails
        if not soup.find_all('item'):
            soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.find_all('item', limit=num_results)
        
        results = []
        for item in items:
            try:
                results.append({
                    'title': item.title.text if item.title else '',
                    'link': item.link.text if item.link else '',
                    'published': item.pubDate.text if item.pubDate else ''
                })
            except AttributeError as e:
                print(f"Error parsing news item: {str(e)}")
                continue
                
        return results
    except Exception as e:
        print(f"Error searching news: {str(e)}")
        print("Returning empty news list")
        return []

def analyze_cv(cv_text, api_key=None):
    """Analyze CV to extract key information and specialties"""
    client = get_openai_client(api_key)
    
    print("=== Starting CV Analysis ===")
    
    analysis_prompt = """Analyze this CV and extract the following information in a clear, structured format:
    1. Key Areas of Expertise: List the main areas of professional expertise (comma-separated)
    2. Industry Focus: The primary industry or sector
    3. Notable Achievements: Focus on factual, measurable results (one per line, start each with a dash)
    4. Technical Skills: List all technical skills (comma-separated)
    5. Soft Skills: List all soft skills (comma-separated)
    6. Career Level: Specify one of: junior, mid-level, senior, executive
    7. Content Topics: Topics this person could write about (comma-separated)
    
    Format your response with these exact headings followed by a colon, then the details.
    For lists, use commas to separate items.
    Example:
    Key Areas of Expertise: skill1, skill2, skill3
    Industry Focus: specific industry
    Technical Skills: tech1, tech2, tech3
    etc."""

    try:
        print("Sending request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are an expert CV analyzer focused on extracting factual information."},
                {"role": "user", "content": f"{analysis_prompt}\n\nCV Content:\n{cv_text}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        print("Parsing OpenAI response...")
        content = response.choices[0].message.content
        print("Raw OpenAI response:", content)
        
        result = {}
        current_key = None
        current_value = []
        
        # Define expected keys and their dictionary versions
        key_mapping = {
            'Key Areas of Expertise': 'key_areas_of_expertise',
            'Industry Focus': 'industry_focus',
            'Notable Achievements': 'notable_achievements',
            'Technical Skills': 'technical_skills',
            'Soft Skills': 'soft_skills',
            'Career Level': 'career_level',
            'Content Topics': 'content_topics'
        }
        
        # Define which fields should be arrays
        array_fields = {
            'key_areas_of_expertise',
            'technical_skills',
            'soft_skills',
            'content_topics'
        }
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check if this line starts with any of our expected keys
            found_key = None
            for expected_key in key_mapping.keys():
                if line.startswith(expected_key + ':'):
                    found_key = expected_key
                    break
            
            if found_key:
                # Save previous key's data if it exists
                if current_key and current_value:
                    dict_key = key_mapping[current_key]
                    joined_value = '\n'.join(current_value)
                    
                    # Convert comma-separated strings to arrays for specific fields
                    if dict_key in array_fields:
                        result[dict_key] = [item.strip() for item in joined_value.split(',') if item.strip()]
                    else:
                        result[dict_key] = joined_value
                
                # Start new key
                current_key = found_key
                value = line[len(found_key) + 1:].strip()  # +1 for the colon
                current_value = [value] if value else []
            else:
                if current_key:
                    current_value.append(line)
        
        # Save the last key's data
        if current_key and current_value:
            dict_key = key_mapping[current_key]
            joined_value = '\n'.join(current_value)
            
            # Convert comma-separated strings to arrays for specific fields
            if dict_key in array_fields:
                result[dict_key] = [item.strip() for item in joined_value.split(',') if item.strip()]
            else:
                result[dict_key] = joined_value
        
        # Ensure all array fields exist, even if empty
        for field in array_fields:
            if field not in result:
                result[field] = []
        
        print("Parsed result:", result)
        print("=== CV Analysis Complete ===")
        return result
        
    except Exception as e:
        print(f"Error in analyze_cv: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return None

def analyze_cv_skills(cv_text, api_key=None):

    client = get_openai_client(api_key)

    """Analyze CV skills with detailed categorization"""
    skills_prompt = """Analyze the CV and categorize skills into:
    1. Technical Skills (with proficiency levels: Expert, Advanced, Intermediate, Beginner)
    2. Soft Skills (with strength indicators: Strong, Moderate, Developing)
    3. Domain Knowledge (with experience levels: Deep, Moderate, Basic)
    4. Tools & Technologies (with expertise: Expert, Proficient, Familiar)
    5. Certifications & Training (with status: Active, Expired, In Progress)
    
    Format as JSON with categories and subcategories."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are a skilled HR analyst specializing in technical skill assessment."},
                {"role": "user", "content": f"{skills_prompt}\n\nCV Content:\n{cv_text}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in skill analysis: {str(e)}")
        return None

def generate_content_ideas(cv_analysis, api_key=None):
    """Generate content ideas based on CV analysis"""
    client = get_openai_client(api_key)

    ideas_prompt = f"""Based on this professional's profile:
    - Expertise: {', '.join(cv_analysis.get('key_areas_of_expertise', []))}
    - Industry: {cv_analysis.get('industry_focus', '')}
    - Level: {cv_analysis.get('career_level', '')}
    - Topics: {', '.join(cv_analysis.get('content_topics', []))}

    Generate 5 specific content ideas for LinkedIn posts. Format each idea exactly as follows:

    1. Title: [title here]
    Angle: [angle here]
    Key Points:
    - [point 1]
    - [point 2]
    - [point 3]

    2. Title: [title here]
    Angle: [angle here]
    Key Points:
    - [point 1]
    - [point 2]
    - [point 3]

    [and so on for all 5 ideas]

    Make each idea:
    1. Share helpful insights from their experience
    2. Provide practical value to their network
    3. Contribute meaningfully to industry discussions
    4. Connect with current industry trends
    5. Foster constructive engagement

    Keep the tone professional, helpful, and humble. Focus on sharing knowledge rather than self-promotion."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are a content strategist who focuses on helpful, value-driven content."},
                {"role": "user", "content": ideas_prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )
        
        print("Raw content ideas response:", response.choices[0].message.content)
        
        # Parse the response into a structured format
        content = response.choices[0].message.content
        ideas = {}
        current_idea = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check for new idea starting with number
            if line[0].isdigit() and line[1] == '.':
                current_idea = f"idea_{len(ideas) + 1}"
                ideas[current_idea] = {'title': '', 'angle': '', 'key_points': []}
                continue
                
            if line.lower().startswith('title:'):
                if current_idea:
                    ideas[current_idea]['title'] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('angle:'):
                if current_idea:
                    ideas[current_idea]['angle'] = line.split(':', 1)[1].strip()
            elif line.startswith('-') and current_idea:
                point = line[1:].strip()
                if point:
                    ideas[current_idea]['key_points'].append(point)
        
        print("Parsed content ideas:", ideas)
        return ideas
    except Exception as e:
        print(f"Error generating ideas: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return None

def generate_linkedin_content(cv_text, post_type, tone, api_key=None):
    """Generate LinkedIn content based on CV analysis and current trends"""
    client = get_openai_client(api_key)
    try:
        # First, analyze the CV and skills
        cv_analysis = analyze_cv(cv_text, api_key)
        if not cv_analysis:
            raise Exception("Failed to analyze CV")
        
        skills_analysis = analyze_cv_skills(cv_text, api_key)
        if not skills_analysis:
            print("Warning: Detailed skills analysis failed, continuing with basic analysis")

        # Generate content ideas and analyze industry trends
        content_ideas = generate_content_ideas(cv_analysis, api_key)
        industry_trends = analyze_industry_trends(
            cv_analysis.get('industry_focus', ''),
            ', '.join(cv_analysis.get('key_areas_of_expertise', [])),
            api_key
        )

        # Search for relevant news
        news_results = search_news(
            f"{cv_analysis.get('industry_focus', '')} {' '.join(cv_analysis.get('key_areas_of_expertise', []))}"
        )

        # Define base prompt based on post type
        prompts = {
            'achievement': f"""Create a LinkedIn post sharing a learning experience or achievement in {cv_analysis.get('key_areas_of_expertise', '')}.
                             Focus on the lessons learned and how they might help others. Include specific examples but maintain humility.
                             
                             Skills Context:
                             {skills_analysis}
                             
                             Industry Trends:
                             {industry_trends}""",
            
            'skill_highlight': f"""Create a LinkedIn post discussing expertise in {cv_analysis.get('technical_skills', '')}.
                                 Focus on how these skills can help solve common challenges. Share practical insights rather than self-promotion.
                                 
                                 Detailed Skills Analysis:
                                 {skills_analysis}""",
            
            'career_journey': f"""Create a reflective LinkedIn post about experiences in {cv_analysis.get('industry_focus', '')}.
                                Share honest insights about challenges faced and lessons learned. Keep the tone authentic and humble.
                                
                                Career Context:
                                {cv_analysis.get('notable_achievements', '')}""",
            
            'industry_insight': f"""Create a thoughtful post about trends in {cv_analysis.get('industry_focus', '')}.
                                  Share observations and insights while encouraging discussion and different perspectives.
                                  
                                  Industry Analysis:
                                  {industry_trends}
                                  
                                  Current Industry News:
                                  {json.dumps(news_results, indent=2)}"""
        }

        system_prompt = f"""You are a professional LinkedIn content creator writing as a {cv_analysis.get('career_level', '')} professional in {cv_analysis.get('industry_focus', '')}.
        Your task is to create an engaging post in a {tone} tone that shares valuable insights from your experience in {', '.join(cv_analysis.get('key_areas_of_expertise', []))}.
        
        Writing Guidelines:
        - Write in first person
        - Keep the post between 150-300 words
        - Include 3-5 relevant hashtags
        - Be authentic and humble
        - Focus on helping others
        - Encourage discussion
        - Share practical insights
        - Acknowledge learning is continuous
        - Avoid self-promotion or boasting
        - Reference industry trends where relevant
        
        Content Ideas for Reference:
        {json.dumps(content_ideas, indent=2)}"""

        # Generate base content
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompts[post_type]}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        base_content = response.choices[0].message.content.strip()

        # Enhance the content based on post type
        enhancement_mapping = {
            'achievement': 'storytelling',
            'skill_highlight': 'problem_solution',
            'career_journey': 'storytelling',
            'industry_insight': 'thought_leadership'
        }
        
        enhanced_content = enhance_post_content(base_content, enhancement_mapping[post_type], api_key)
        if not enhanced_content:
            enhanced_content = base_content

        # Generate engagement prompts
        engagement_content = generate_engagement_prompts(enhanced_content, api_key)

        return {
            'content': enhanced_content,
            'engagement_suggestions': engagement_content,
            'industry_trends': industry_trends,
            'skills_analysis': skills_analysis,
            'related_news': news_results
        }

    except Exception as e:
        print(f"Error generating content: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return f"Error generating {post_type} post. Please try again."

def analyze_industry_trends(industry, expertise, api_key=None):

    client = get_openai_client(api_key)

    """Generate industry trend analysis and recommendations"""
    trend_prompt = f"""Analyze current trends in {industry} focusing on:
    1. Emerging Technologies
    2. Market Challenges
    3. Growth Opportunities
    4. Skills in Demand
    5. Industry Predictions
    
    Consider the expertise in: {expertise}
    Provide actionable insights for content creation."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are an industry analyst specializing in market trends and professional development."},
                {"role": "user", "content": trend_prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in trend analysis: {str(e)}")
        return None

def generate_content_calendar(cv_analysis, timeframe=30, api_key=None):
    """Generate a content calendar with post ideas"""

    client = get_openai_client(api_key)
    calendar_prompt = f"""Create a {timeframe}-day LinkedIn content calendar based on:
    - Expertise: {cv_analysis.get('key_areas_of_expertise', [])}
    - Industry: {cv_analysis.get('industry_focus', '')}
    - Career Level: {cv_analysis.get('career_level', '')}

    For each week, provide:
    1. Theme of the Week
    2. 3-4 Post Ideas
    3. Best Posting Times
    4. Engagement Strategies
    5. Relevant Hashtags

    Format as structured JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are a social media strategist specializing in professional content planning."},
                {"role": "user", "content": calendar_prompt}
            ],
            temperature=0.8,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating calendar: {str(e)}")
        return None

def generate_engagement_prompts(post_content, api_key=None):
    """Generate engagement prompts and conversation starters"""
    client = get_openai_client(api_key)
    prompt = f"""For this LinkedIn post:
    {post_content}

    Generate:
    1. 3 Conversation-Starting Questions
    2. 2 Call-to-Action Ideas
    3. 3 Follow-up Comment Templates
    4. Relevant Industry Statistics
    5. Engagement Hook Ideas

    Focus on fostering meaningful professional discussions."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are a social media engagement specialist focusing on professional networking."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating engagement prompts: {str(e)}")
        return None

def enhance_post_content(content, enhancement_type, api_key=None):
    """Enhance post content with specific improvements"""
    client = get_openai_client(api_key)
    enhancement_prompts = {
        'storytelling': "Transform this content into a compelling professional story with a clear narrative arc.",
        'data_driven': "Enhance this content with relevant industry statistics and data points.",
        'thought_leadership': "Elevate this content to establish thought leadership with expert insights.",
        'problem_solution': "Restructure this content into a clear problem-solution format.",
        'case_study': "Transform this content into a mini case study format."
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are a professional content editor specializing in LinkedIn posts."},
                {"role": "user", "content": f"{enhancement_prompts[enhancement_type]}\n\nContent:\n{content}"}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error enhancing content: {str(e)}")
        return None