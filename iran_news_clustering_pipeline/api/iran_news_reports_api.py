import sys
import os
from typing import List, Optional
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.reports_api_repository import ReportsAPIRepository
from database.postgresql_connection_manager import PostgreSQLConnectionManager
from config.database_connection_config import DatabaseConnectionConfig

# Initialize FastAPI app
app = FastAPI(
    title="Iran News Reports API",
    description="API for accessing Iran news reports with clustering and intelligent analysis",
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection and repository
database_config = DatabaseConnectionConfig()
database_connection_manager = PostgreSQLConnectionManager(database_config)
reports_repository = ReportsAPIRepository(database_connection_manager)


# Pydantic models for API responses
class NewsSourceModel(BaseModel):
    """Model for a news source."""
    name: str
    url: str


class NewsReportSummaryModel(BaseModel):
    """Model for a report summary in list view."""
    id: int
    title: str
    content: str
    content_type: str
    word_count: int
    cluster_topic: str
    sources: List[NewsSourceModel]
    created_at: datetime


class NewsReportDetailModel(BaseModel):
    """Model for a detailed report view."""
    id: int
    title: str
    content: str
    content_type: str
    word_count: int
    cluster_topic: str
    sources: List[NewsSourceModel]
    created_at: datetime


class PaginatedReportsResponseModel(BaseModel):
    """Model for paginated reports response."""
    success: bool
    total: int
    page: int
    limit: int
    reports: List[NewsReportSummaryModel]


class SingleReportResponseModel(BaseModel):
    """Model for single report response."""
    success: bool
    report: NewsReportDetailModel


class LatestReportsResponseModel(BaseModel):
    """Model for latest reports response."""
    success: bool
    count: int
    reports: List[NewsReportSummaryModel]


class ErrorResponseModel(BaseModel):
    """Model for error response."""
    success: bool
    error: str
    code: int



# Helper function to format report data
def format_report_data_for_response(report_tuple, sources_list):
    """
    Formats raw database data into API response format.
    
    Args:
        report_tuple: Tuple from database (id, title, content, content_type, cluster_topic, cluster_id, created_at)
        sources_list: List of tuples (source_name, source_url)
        
    Returns:
        dict: Formatted report data
    """
    report_id, title, content, content_type, cluster_topic, cluster_id, created_at = report_tuple[:7]
    
    # Count words in content
    word_count = reports_repository.count_words_in_content(content)
    
    # Format sources
    formatted_sources = [
        {"name": source_name, "url": source_url}
        for source_name, source_url in sources_list
    ]
    
    return {
        "id": report_id,
        "title": title,
        "content": content,
        "content_type": content_type,
        "word_count": word_count,
        "cluster_topic": cluster_topic,
        "sources": formatted_sources,
        "created_at": created_at
    }


# API Endpoints

@app.get("/", tags=["Root"])
async def read_root_endpoint():
    """
    Root endpoint - API information.
    """
    return {
        "message": "Iran News Reports API",
        "version": "1.0.0",
        "endpoints": {
            "get_all_reports": "/api/reports",
            "get_report_by_id": "/api/reports/{id}",
            "get_latest_reports": "/api/reports/latest"
        }
    }


@app.get("/api/reports", response_model=PaginatedReportsResponseModel, tags=["Reports"])
async def get_all_reports_endpoint(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(20, ge=1, le=100, description="Number of reports per page (max 100)")
):
    """
    Get all reports with pagination.
    
    Parameters:
    - page: Page number (default: 1)
    - limit: Number of reports per page (default: 20, max: 100)
    
    Returns:
    - List of reports with pagination info
    """
    try:
        total_count, reports_data = reports_repository.get_all_reports_with_pagination(page, limit)
        
        formatted_reports = []
        for report in reports_data:
            # report structure: (id, title, content, content_type, cluster_topic, cluster_id, created_at)
            cluster_id = report[5]  # cluster_id is at index 5
            sources = reports_repository.get_sources_for_cluster(cluster_id) if cluster_id else []
            formatted_report = format_report_data_for_response(report, sources)
            formatted_reports.append(formatted_report)
        
        return {
            "success": True,
            "total": total_count,
            "page": page,
            "limit": limit,
            "reports": formatted_reports
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/reports/latest", response_model=LatestReportsResponseModel, tags=["Reports"])
async def get_latest_reports_endpoint(
    limit: int = Query(10, ge=1, le=50, description="Number of latest reports (max 50)")
):
    """
    Get the latest reports.
    
    Parameters:
    - limit: Number of reports to return (default: 10, max: 50)
    
    Returns:
    - List of latest reports
    """
    try:
        # Use page 1 with the specified limit
        total_count, reports_data = reports_repository.get_all_reports_with_pagination(1, limit)
        
        formatted_reports = []
        for report in reports_data:
            # report structure: (id, title, content, content_type, cluster_topic, cluster_id, created_at)
            cluster_id = report[5]  # cluster_id is at index 5
            sources = reports_repository.get_sources_for_cluster(cluster_id) if cluster_id else []
            formatted_report = format_report_data_for_response(report, sources)
            formatted_reports.append(formatted_report)
        
        return {
            "success": True,
            "count": len(formatted_reports),
            "reports": formatted_reports
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/reports/{report_id}", response_model=SingleReportResponseModel, tags=["Reports"])
async def get_report_by_id_endpoint(report_id: int):
    """
    Get a single report by ID with all details and sources.
    
    Parameters:
    - report_id: ID of the report
    
    Returns:
    - Detailed report information
    """
    try:
        result = reports_repository.get_report_by_id_with_sources(report_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Report not found")
        
        report_data = result['report']
        sources_data = result['sources']
        
        formatted_report = format_report_data_for_response(report_data, sources_data)
        
        return {
            "success": True,
            "report": formatted_report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health", tags=["Health"])
async def health_check_endpoint():
    """
    Health check endpoint.
    
    Returns:
    - API health status
    """
    try:
        # Test database connection
        connection = database_connection_manager.get_connection_without_pool()
        connection.close()
        database_status = "connected"
    except:
        database_status = "disconnected"
    
    return {
        "status": "healthy" if database_status == "connected" else "unhealthy",
        "database": database_status,
        "version": "1.0.0"
    }


# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
