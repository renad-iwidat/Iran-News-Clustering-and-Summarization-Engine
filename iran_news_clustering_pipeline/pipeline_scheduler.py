import sys
import os
import schedule
import time
import logging
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main_pipeline_service import MainPipelineService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PipelineScheduler:
    """
    Scheduler that runs the news processing pipeline at regular intervals.
    Default: Every 15 minutes, processes last 10 unprocessed news articles.
    """
    
    def __init__(self, batch_size: int = 10, interval_minutes: int = 15):
        """
        Initialize the scheduler.
        
        Args:
            batch_size: Number of news articles to process per run (default: 10)
            interval_minutes: Interval between runs in minutes (default: 15)
        """
        self.batch_size = batch_size
        self.interval_minutes = interval_minutes
        self.pipeline = MainPipelineService()
        self.run_count = 0
        
        logger.info("=" * 80)
        logger.info("PIPELINE SCHEDULER INITIALIZED")
        logger.info("=" * 80)
        logger.info(f"Batch size: {self.batch_size} news articles")
        logger.info(f"Interval: Every {self.interval_minutes} minutes")
        logger.info("=" * 80)
    
    def run_pipeline_job(self):
        """
        Job function that runs the pipeline.
        """
        self.run_count += 1
        
        logger.info("\n" + "=" * 80)
        logger.info(f"SCHEDULED RUN #{self.run_count}")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        try:
            stats = self.pipeline.run_full_pipeline(batch_size=self.batch_size)
            
            logger.info(f"\n✅ Run #{self.run_count} completed successfully")
            logger.info(f"Next run in {self.interval_minutes} minutes")
            
        except Exception as e:
            logger.error(f"\n❌ Run #{self.run_count} failed: {str(e)}")
            logger.error(f"Will retry in {self.interval_minutes} minutes")
    
    def start(self):
        """
        Start the scheduler.
        """
        # Schedule the job
        schedule.every(self.interval_minutes).minutes.do(self.run_pipeline_job)
        
        logger.info("\n🚀 Scheduler started!")
        logger.info(f"Pipeline will run every {self.interval_minutes} minutes")
        logger.info("Press Ctrl+C to stop\n")
        
        # Run immediately on start
        logger.info("Running initial pipeline execution...")
        self.run_pipeline_job()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n\n🛑 Scheduler stopped by user")
            logger.info(f"Total runs completed: {self.run_count}")
            logger.info("=" * 80)


def main():
    """
    Main entry point for the scheduler.
    """
    # You can customize these values
    BATCH_SIZE = 10  # Process last 10 unprocessed news
    INTERVAL_MINUTES = 15  # Run every 15 minutes
    
    scheduler = PipelineScheduler(
        batch_size=BATCH_SIZE,
        interval_minutes=INTERVAL_MINUTES
    )
    
    scheduler.start()


if __name__ == "__main__":
    main()
