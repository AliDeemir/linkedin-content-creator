# LinkedIn Content Creator

An AI-powered application that helps professionals create engaging LinkedIn content based on their CV and industry trends. The application uses OpenAI's GPT models to analyze CVs and generate personalized content suggestions.

## Prerequisites

### Docker Installation

1. **Install Docker Desktop**
   - Windows & Mac: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Linux: [Docker Engine Installation](https://docs.docker.com/engine/install/)

2. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

3. **System Requirements**
   - Windows: Windows 10/11 Pro, Enterprise, or Education (with WSL 2)
   - Mac: macOS 10.15 or newer
   - Linux: Any modern distribution with kernel version 3.10 or higher

4. **Resource Recommendations**
   - 8GB RAM minimum
   - 2 CPU cores minimum
   - 10GB available disk space

## Features

- 📄 CV Analysis & Content Generation
  - Upload and analyze PDF CVs
  - Extract key skills and expertise
  - Generate personalized content ideas
  - Create engaging LinkedIn posts

- 🤖 AI-Powered Features
  - Skill categorization and analysis
  - Industry trend insights
  - Engagement suggestions
  - Content topic recommendations

- 💼 Professional Tools
  - Multiple post types (achievements, skills, career journey)
  - PDF export functionality
  - Copy-to-clipboard feature
  - Related industry news integration

## Tech Stack

### Frontend
- React.js with Material-UI
- React Router for navigation
- React-to-PDF for document export

### Backend
- Django with REST Framework
- OpenAI API integration
- PyPDF2 for PDF processing

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose
- OpenAI API key

### Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/linkedin-content-creator.git
cd linkedin-content-creator
```

2. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-openai-api-key
DJANGO_SECRET_KEY=your-django-secret-key
```

3. Start the application:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Usage

1. Open http://localhost:3000 in your browser
2. Enter your OpenAI API key when prompted
3. Upload your CV in PDF format
4. Click "Generate Content" to analyze your CV
5. View and interact with generated content:
   - CV Analysis
   - Content Ideas
   - Industry Trends
   - Generated Posts
6. Use the download button to export content as PDF
7. Copy individual posts using the copy button

## Docker Services

### Frontend Container
- Node.js 18 environment
- Live reload enabled
- Volume mounted for development
- Exposed on port 3000

### Backend Container
- Python 3.11 environment
- Django development server
- Volume mounted for development
- Exposed on port 8000

## Project Structure
```
linkedin-content-creator/
├── docker-compose.yml          # Docker services configuration
├── backend/
│   ├── Dockerfile.dev         # Backend container configuration
│   ├── requirements.txt       # Python dependencies
│   └── linkedin_api/         # Django application
├── frontend/
│   ├── Dockerfile.dev        # Frontend container configuration
│   ├── package.json         # Node.js dependencies
│   └── src/                # React application
└── .env                    # Environment variables
```

## Development with Docker

### Viewing Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs frontend
docker-compose logs backend
```

### Rebuilding Services
```bash
# Rebuild specific service
docker-compose up -d --build frontend

# Rebuild all services
docker-compose up -d --build
```

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## API Endpoints

- `POST /api/verify-api-key`: Verify OpenAI API key
- `POST /api/generate-posts`: Generate content from CV

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   If you see "address already in use" error:
   ```bash
   # Kill processes using the ports
   sudo lsof -i :3000 -t | xargs kill -9
   sudo lsof -i :8000 -t | xargs kill -9
   
   # Then restart Docker containers
   docker-compose down
   docker-compose up --build
   ```

2. **Container Access**
   ```bash
   # Check container status
   docker-compose ps
   
   # View container logs
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. **Clean Start**
   ```bash
   # Remove all containers and volumes
   docker-compose down -v
   docker system prune -f
   docker-compose up --build
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for GPT API
- Material-UI for React components
- Django community for the robust backend framework 