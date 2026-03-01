"""
Run the Iran News Reports API server.

Usage:
    python run_api.py

The API will be available at:
    - http://localhost:8000
    - API Documentation: http://localhost:8000/docs
    - Alternative Documentation: http://localhost:8000/redoc
"""

import uvicorn

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         Iran News Reports API - Starting Server           ║
    ╚════════════════════════════════════════════════════════════╝
    
    API Server Configuration:
    • Host: 0.0.0.0 (accessible from all network interfaces)
    • Port: 8000
    • Auto-reload: Enabled (for development)
    
    Available Endpoints:
    • GET  /api/reports          - Get all reports (with pagination)
    • GET  /api/reports/{id}     - Get specific report by ID
    • GET  /api/reports/latest   - Get latest reports
    • GET  /health               - Health check
    
    Documentation:
    • Swagger UI:  http://localhost:8000/docs
    • ReDoc:       http://localhost:8000/redoc
    
    Press Ctrl+C to stop the server
    
    ════════════════════════════════════════════════════════════
    """)
    
    uvicorn.run(
        "api.iran_news_reports_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (disable in production)
        log_level="info"
    )
