# Iran News Clustering and Summarization Engine

Automated pipeline for processing, clustering, and generating professional reports from Iran-related news articles in Hebrew and Arabic.

## Overview

This system automatically:
1. Translates Hebrew news to Arabic
2. Extracts key points from articles
3. Clusters similar news together
4. Generates professional reports with source citations
5. Provides REST API for frontend access

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- PostgreSQL database (Render or other)
- OpenAI API keys

### Setup

1. Clone the repository:
```bash
git clone https://github.com/renad-iwidat/Iran-News-Clustering-and-Summarization-Engine.git
cd Iran-News-Clustering-and-Summarization-Engine/iran_news_clustering_pipeline
```

2. Create `.env` file from example:
```bash
cp .env.example .env
```

3. Edit `.env` with your credentials:
```env
DATABASE_HOST=your-database-host.render.com
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password

OPENAI_API_KEY_IRAN_NEWS_TRANSLATION_HEBREW_ARABIC=sk-proj-...
OPENAI_API_KEY_IRAN_NEWS_CLUSTERING_ANALYSIS=sk-proj-...
OPENAI_API_KEY_IRAN_NEWS_REPORT_SUMMARIZATION=sk-proj-...
```

4. Run with Docker Compose:
```bash
docker-compose up -d
```

### Services

- **API Service**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Scheduler**: Runs every 15 minutes automatically

## API Endpoints

- `GET /api/reports` - Get all reports (with pagination)
- `GET /api/reports/{id}` - Get specific report
- `GET /api/reports/latest` - Get latest reports
- `GET /health` - Health check

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for details.

## Pipeline Workflow

1. **Translation Stage**: Hebrew articles → Arabic (with language detection)
2. **Clustering Stage**: Extract key points → Group similar news
3. **Report Generation**: Create professional reports with titles and clickable sources
4. **Scheduling**: Runs every 15 minutes, processes last 10 unprocessed articles

## Deployment on Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect to GitHub repository
4. Select "Docker" as environment
5. Set Dockerfile path: `iran_news_clustering_pipeline/Dockerfile.api` (for API)
6. Add environment variables from `.env`
7. Deploy

For scheduler, create another Web Service with `Dockerfile.scheduler`.

## Monitoring

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f scheduler

# Check status
docker-compose ps
```

## Development

```bash
# Rebuild after code changes
docker-compose up -d --build

# Restart services
docker-compose restart api
docker-compose restart scheduler

# Stop everything
docker-compose down
```

## Project Structure

```
iran_news_clustering_pipeline/
├── api/                    # REST API
├── config/                 # Database and OpenAI configuration
├── database/              # Database repositories and migrations
├── llm_services/          # LLM services (translation, clustering, reports)
├── tests/                 # Test files
├── docker-compose.yml     # Docker orchestration
├── Dockerfile.api         # API service Docker image
├── Dockerfile.scheduler   # Scheduler service Docker image
└── requirements.txt       # Python dependencies
```

## License

Private project
