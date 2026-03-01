import sys
import os
import logging
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from llm_services.news_translation_pipeline_service import NewsTranslationPipelineService
from llm_services.news_clustering_pipeline_service import NewsClusteringPipelineService
from llm_services.news_report_generation_pipeline_service import NewsReportGenerationPipelineService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MainPipelineService:
    """
    Main service that orchestrates the complete news processing pipeline.
    Runs: Translation -> Clustering -> Report Generation
    """
    
    def __init__(self):
        """
        Initialize all pipeline services.
        """
        logger.info("Initializing Main Pipeline Service...")
        self.translation_pipeline = NewsTranslationPipelineService()
        self.clustering_pipeline = NewsClusteringPipelineService()
        self.report_pipeline = NewsReportGenerationPipelineService()
        logger.info("Main Pipeline Service initialized successfully")
    
    def run_full_pipeline(self, batch_size: int = 10):
        """
        Runs the complete pipeline: Translation -> Clustering -> Report Generation.
        
        Args:
            batch_size: Number of news articles to process (default: 10)
            
        Returns:
            dict: Complete statistics from all pipeline stages
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info(f"Starting Full Pipeline Execution (batch size: {batch_size})")
        logger.info("=" * 80)
        
        try:
            # Stage 1: Translation
            logger.info("\n[STAGE 1/3] Running Translation Pipeline...")
            translation_stats = self.translation_pipeline.process_batch(batch_size=batch_size)
            logger.info(f"Translation completed: {translation_stats}")
            
            # Stage 2: Clustering
            logger.info("\n[STAGE 2/3] Running Clustering Pipeline...")
            clustering_stats = self.clustering_pipeline.process_clustering(batch_size=batch_size)
            logger.info(f"Clustering completed: {clustering_stats}")
            
            # Stage 3: Report Generation
            logger.info("\n[STAGE 3/3] Running Report Generation Pipeline...")
            report_stats = self.report_pipeline.process_report_generation()
            logger.info(f"Report Generation completed: {report_stats}")
            
            # Calculate total execution time
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Compile complete statistics
            complete_stats = {
                'execution_time_seconds': execution_time,
                'translation': translation_stats,
                'clustering': clustering_stats,
                'report_generation': report_stats,
                'timestamp': start_time.isoformat()
            }
            
            logger.info("\n" + "=" * 80)
            logger.info("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            logger.info(f"Total execution time: {execution_time:.2f} seconds")
            logger.info(f"News translated: {translation_stats.get('succeeded', 0)}")
            logger.info(f"Clusters created: {clustering_stats.get('clusters_created', 0)}")
            logger.info(f"Reports generated: {report_stats.get('reports_generated', 0)}")
            logger.info(f"News processed: {report_stats.get('news_marked_processed', 0)}")
            logger.info("=" * 80)
            
            return complete_stats
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
