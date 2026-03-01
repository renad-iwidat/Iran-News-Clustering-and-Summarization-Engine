"""
Reset all data and process all news articles.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.database_connection_config import DatabaseConnectionConfig
from database.postgresql_connection_manager import PostgreSQLConnectionManager
from main_pipeline_service import MainPipelineService
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def reset_all_data():
    """Reset all processing flags and delete generated data."""
    logger.info("=" * 80)
    logger.info("RESETTING ALL DATA")
    logger.info("=" * 80)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    connection = None
    
    try:
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        # 1. Delete all reports
        cursor.execute("DELETE FROM output_content;")
        logger.info("✓ Deleted all reports from output_content")
        
        # 2. Delete all clusters
        cursor.execute("DELETE FROM cluster_members;")
        cursor.execute("DELETE FROM clusters;")
        logger.info("✓ Deleted all clusters and cluster_members")
        
        # 3. Delete all translations
        cursor.execute("DELETE FROM translations;")
        logger.info("✓ Deleted all translations")
        
        # 4. Reset is_processed flag
        cursor.execute("UPDATE raw_data SET is_processed = false, processed_at = NULL;")
        logger.info("✓ Reset is_processed flag for all news")
        
        # Get count of news to process
        cursor.execute("SELECT COUNT(*) FROM raw_data;")
        total_news = cursor.fetchone()[0]
        
        connection.commit()
        cursor.close()
        
        logger.info("=" * 80)
        logger.info(f"RESET COMPLETED - Ready to process {total_news} news articles")
        logger.info("=" * 80)
        
        return total_news
        
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Failed to reset data: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()


def process_all_news(total_news):
    """Process all news in batches."""
    logger.info("\n" + "=" * 80)
    logger.info("STARTING FULL PROCESSING")
    logger.info("=" * 80)
    
    pipeline = MainPipelineService()
    
    # Calculate number of runs needed (15 news per batch)
    batch_size = 15
    num_runs = (total_news + batch_size - 1) // batch_size  # Round up
    
    logger.info(f"Total news: {total_news}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Estimated runs: {num_runs}")
    logger.info("=" * 80)
    
    total_translated = 0
    total_clusters = 0
    total_reports = 0
    
    for run in range(1, num_runs + 1):
        logger.info(f"\n{'=' * 80}")
        logger.info(f"RUN {run}/{num_runs}")
        logger.info(f"{'=' * 80}")
        
        try:
            stats = pipeline.run_full_pipeline(batch_size=batch_size)
            
            total_translated += stats['translation']['succeeded']
            total_clusters += stats['clustering']['clusters_created']
            total_reports += stats['report_generation']['reports_generated']
            
            logger.info(f"\n✓ Run {run} completed successfully")
            logger.info(f"  Translated: {stats['translation']['succeeded']}")
            logger.info(f"  Clusters: {stats['clustering']['clusters_created']}")
            logger.info(f"  Reports: {stats['report_generation']['reports_generated']}")
            
            # Check if we're done
            if stats['translation']['processed'] == 0:
                logger.info("\n✓ All news processed!")
                break
                
        except Exception as e:
            logger.error(f"\n✗ Run {run} failed: {str(e)}")
            continue
    
    logger.info("\n" + "=" * 80)
    logger.info("PROCESSING COMPLETED")
    logger.info("=" * 80)
    logger.info(f"Total news translated: {total_translated}")
    logger.info(f"Total clusters created: {total_clusters}")
    logger.info(f"Total reports generated: {total_reports}")
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        # Step 1: Reset all data
        total_news = reset_all_data()
        
        # Step 2: Process all news
        process_all_news(total_news)
        
        logger.info("\n✓ ALL DONE! Check the API for results.")
        
    except Exception as e:
        logger.error(f"\n✗ Process failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
