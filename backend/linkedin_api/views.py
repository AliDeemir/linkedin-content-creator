from rest_framework.response import Response
from rest_framework.views import APIView
from .utils.openai_helper import generate_linkedin_content, analyze_cv, generate_content_ideas, get_openai_client, search_news, analyze_industry_trends, generate_content_calendar
from rest_framework.parsers import MultiPartParser, FormParser
import PyPDF2
import io
from rest_framework.decorators import api_view
from openai import OpenAI
from django.http import JsonResponse

class GeneratePostsView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def format_response_data(self, cv_analysis, content_ideas, posts, industry_trends, content_calendar, news_results):
        """Format response data in a consistent structure"""
        try:
            # Format posts data
            formatted_posts = []
            for post in posts:
                formatted_post = {
                    'type': post['type'],
                    'content': post['content'],
                    'status': post['status'],
                }
                if post['status'] == 'success':
                    # Keep engagement_suggestions as string for frontend rendering
                    formatted_post.update({
                        'engagement_suggestions': post.get('engagement_suggestions', ''),
                        'industry_trends': post.get('industry_trends', ''),
                        'skills_analysis': post.get('skills_analysis', {}),
                        'related_news': post.get('related_news', []),
                    })
                formatted_posts.append(formatted_post)

            # Format CV analysis to match frontend expectations
            formatted_cv_analysis = {
                'key_areas_of_expertise': cv_analysis.get('key_areas_of_expertise', []),
                'industry_focus': cv_analysis.get('industry_focus', ''),
                'notable_achievements': cv_analysis.get('notable_achievements', ''),  # Keep as string
                'technical_skills': cv_analysis.get('technical_skills', []),
                'soft_skills': cv_analysis.get('soft_skills', []),
                'career_level': cv_analysis.get('career_level', ''),
                'content_topics': cv_analysis.get('content_topics', [])
            }

            # Format content ideas as object with numbered keys
            formatted_content_ideas = {}
            if isinstance(content_ideas, dict):
                for key, idea in content_ideas.items():
                    formatted_content_ideas[key] = {
                        'title': idea.get('title', ''),
                        'angle': idea.get('angle', ''),
                        'key_points': idea.get('key_points', [])
                    }

            # Keep industry_trends as string for frontend rendering
            formatted_industry_trends = industry_trends if isinstance(industry_trends, str) else ''

            # Format news to match frontend display
            formatted_news = []
            for news_item in news_results:
                formatted_news.append({
                    'title': news_item.get('title', ''),
                    'link': news_item.get('link', ''),
                    'published': news_item.get('published', '')
                })

            # Direct response structure to match frontend expectations
            return {
                'status': 'success',
                'cv_analysis': formatted_cv_analysis,
                'content_ideas': formatted_content_ideas,
                'posts': formatted_posts,
                'industry_trends': formatted_industry_trends,
                'content_calendar': content_calendar,
                'news': formatted_news,
                'skills_analysis': posts[0].get('skills_analysis', {}) if posts else {}
            }

        except Exception as e:
            print(f"Error formatting response data: {str(e)}")
            import traceback
            print("Traceback:", traceback.format_exc())
            return {
                'status': 'error',
                'error': 'Failed to format response data',
                'details': str(e)
            }

    def post(self, request):
        try:
            print("=== Starting GeneratePostsView.post ===")
            
            # Get API key from request
            api_key = request.POST.get('api_key')
            print(f"API Key received: {api_key[:10]}..." if api_key else "No API key received")
            
            if not api_key:
                return Response({'error': 'API key is required'}, status=400)
            
            cv_file = request.FILES.get('cv')
            if not cv_file:
                print("Error: No CV file provided")
                return Response({'error': 'No CV file provided'}, status=400)

            print(f"Processing CV file: {cv_file.name}")

            # Read PDF content
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(cv_file.read()))
                cv_text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    cv_text += page.extract_text()
                print(f"Successfully extracted text from {len(pdf_reader.pages)} pages")
            except Exception as e:
                print(f"Error reading PDF: {str(e)}")
                return Response({'error': f'Failed to read PDF: {str(e)}'}, status=400)

            # First, analyze the CV
            print("Analyzing CV...")
            cv_analysis = analyze_cv(cv_text, api_key=api_key)
            if not cv_analysis:
                print("Error: CV analysis failed")
                return Response({'error': 'Failed to analyze CV'}, status=400)

            # Generate content ideas
            print("Generating content ideas...")
            content_ideas = generate_content_ideas(cv_analysis, api_key=api_key)
            if not content_ideas:
                print("Error: Content ideas generation failed")
                return Response({'error': 'Failed to generate content ideas'}, status=400)

            # Get industry trends
            print("Analyzing industry trends...")
            industry_trends = analyze_industry_trends(
                cv_analysis.get('industry_focus', ''),
                ', '.join(cv_analysis.get('key_areas_of_expertise', [])),
                api_key=api_key
            )

            # Generate content calendar
            print("Generating content calendar...")
            content_calendar = generate_content_calendar(cv_analysis, api_key=api_key)

            # Generate different types of posts
            print("Generating posts...")
            posts = []
            post_types = [
                {'type': 'achievement', 'tone': 'professional'},
                {'type': 'skill_highlight', 'tone': 'confident'},
                {'type': 'career_journey', 'tone': 'storytelling'},
                {'type': 'industry_insight', 'tone': 'thought_leadership'},
            ]

            for post_type in post_types:
                print(f"Generating {post_type['type']} post...")
                post_data = generate_linkedin_content(
                    cv_text,
                    post_type['type'],
                    post_type['tone'],
                    api_key=api_key
                )
                
                if isinstance(post_data, str):  # Error case
                    posts.append({
                        'type': post_type['type'],
                        'content': post_data,
                        'status': 'error'
                    })
                else:
                    posts.append({
                        'type': post_type['type'],
                        'content': post_data['content'],
                        'engagement_suggestions': post_data.get('engagement_suggestions'),
                        'industry_trends': post_data.get('industry_trends'),
                        'skills_analysis': post_data.get('skills_analysis'),
                        'related_news': post_data.get('related_news'),
                        'status': 'success'
                    })

            # Get news for the industry and expertise
            print("Fetching relevant news...")
            news_results = search_news(
                f"{cv_analysis.get('industry_focus', '')} {' '.join(cv_analysis.get('key_areas_of_expertise', []))}"
            )

            # Format and return response
            response_data = self.format_response_data(
                cv_analysis=cv_analysis,
                content_ideas=content_ideas,
                posts=posts,
                industry_trends=industry_trends,
                content_calendar=content_calendar,
                news_results=news_results
            )
            
            if response_data['status'] == 'error':
                return Response(response_data, status=500)
                
            return Response(response_data)

        except Exception as e:
            print(f"=== Error in GeneratePostsView.post: {str(e)} ===")
            return Response({
                'status': 'error',
                'error': str(e),
                'details': 'An unexpected error occurred'
            }, status=500)

@api_view(['POST'])
def verify_api_key(request):
    # Try different ways to get the API key
    api_key = (
        request.POST.get('api_key') or  # Try form data first
        request.data.get('api_key') or  # Try JSON data next
        request.FILES.get('api_key')    # Try file upload data last
    )
    
    print(f"Received request data: {request.data}")
    print(f"Received POST data: {request.POST}")
    print(f"API Key received: {api_key[:10]}..." if api_key else "No API key received")
    
    if not api_key:
        return Response({'error': 'API key is required'}, status=400)
    
    if not api_key.startswith('sk-'):
        return Response({'error': 'Invalid API key format. Key should start with "sk-"'}, status=400)
    
    try:
        # Try to create a client with the provided API key
        client = get_openai_client(api_key)
        
        # Make a simple API call to verify the key
        try:
            models = client.models.list()
            # Check if we can access the models data
            if hasattr(models, 'data'):
                print(f"API Key verification successful: {len(models.data)} models available")
            else:
                print("API Key verification successful: Models list retrieved")
            return Response({'status': 'valid'})
        except Exception as api_error:
            print(f"API call failed: {str(api_error)}")
            return Response({
                'error': 'API key validation failed',
                'details': str(api_error)
            }, status=401)
            
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return Response({'error': str(ve)}, status=400)
    except Exception as e:
        print(f"Unexpected error during API key verification: {str(e)}")
        return Response({
            'error': 'Invalid API key',
            'details': str(e)
        }, status=401)

@api_view(['POST'])
def generate_posts(request):
    api_key = request.data.get('api_key')
    if not api_key:
        return Response({'error': 'API key is required'}, status=400)

    try:
        cv_file = request.FILES.get('cv')
        if not cv_file:
            return Response({'error': 'No CV file provided'}, status=400)

        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(cv_file.read()))
        cv_text = ""
        for page in pdf_reader.pages:
            cv_text += page.extract_text()

        # Analyze CV with provided API key
        cv_analysis = analyze_cv(cv_text, api_key=api_key)
        if not cv_analysis:
            return Response({'error': 'Failed to analyze CV'}, status=400)

        # Generate content ideas with provided API key
        content_ideas = generate_content_ideas(cv_analysis, api_key=api_key)
        if not content_ideas:
            return Response({'error': 'Failed to generate content ideas'}, status=400)

        # Generate different types of posts
        print("Generating posts...")
        posts = []
        post_types = [
            {'type': 'achievement', 'tone': 'professional'},
            {'type': 'skill_highlight', 'tone': 'confident'},
            {'type': 'career_journey', 'tone': 'storytelling'},
            {'type': 'industry_insight', 'tone': 'thought_leadership'},
        ]

        for post_type in post_types:
            print(f"Generating {post_type['type']} post...")
            post_data = generate_linkedin_content(
                cv_text,
                post_type['type'],
                post_type['tone'],
                api_key=api_key
            )
            
            if isinstance(post_data, str):  # Error case
                posts.append({
                    'type': post_type['type'],
                    'content': post_data,
                    'status': 'error'
                })
            else:
                posts.append({
                    'type': post_type['type'],
                    'content': post_data['content'],
                    'engagement_suggestions': post_data.get('engagement_suggestions'),
                    'industry_trends': post_data.get('industry_trends'),
                    'skills_analysis': post_data.get('skills_analysis'),
                    'related_news': post_data.get('related_news'),
                    'status': 'success'
                })

        response_data = {
            'status': 'success',
            'cv_analysis': cv_analysis,
            'content_ideas': content_ideas,
            'posts': posts,
            'industry_trends': posts[0].get('industry_trends'),
            'skills_analysis': posts[0].get('skills_analysis'),
            'news': posts[0].get('related_news', [])
        }
        
        return Response(response_data)

    except Exception as e:
        print(f"=== Error in GeneratePostsView.post: {str(e)} ===")
        return Response({'error': str(e)}, status=500) 