"""
Run the pipeline once (for Render Cron Job).
This script runs the full pipeline and exits.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main_pipeline_service import MainPipelineService
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Run the pipeline once and exit.
    """
    try:
        logger.info("Starting pipeline execution (Cron Job)")
        
        pipeline = MainPipelineService()
        stats = pipeline.run_full_pipeline(batch_size=15)
        
        logger.info(f"Pipeline completed successfully: {stats}")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
