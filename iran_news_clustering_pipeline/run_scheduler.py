"""
Quick start script for the pipeline scheduler.

Usage:
    python run_scheduler.py

Configuration:
    - Batch size: 10 news articles per run
    - Interval: Every 15 minutes
    
To customize, edit the values in pipeline_scheduler.py
"""

from pipeline_scheduler import main

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   Iran News Clustering Pipeline - Automated Scheduler     ║
    ╚════════════════════════════════════════════════════════════╝
    
    Configuration:
    • Batch Size: 15 news articles
    • Interval: Every 15 minutes
    • Stages: Translation → Clustering → Report Generation
    
    The scheduler will:
    1. Check for unprocessed news every 15 minutes
    2. Process the oldest 15 unprocessed articles (FIFO)
    3. Generate reports with titles and clickable sources
    
    Press Ctrl+C to stop the scheduler
    
    ════════════════════════════════════════════════════════════
    """)
    
    main()
