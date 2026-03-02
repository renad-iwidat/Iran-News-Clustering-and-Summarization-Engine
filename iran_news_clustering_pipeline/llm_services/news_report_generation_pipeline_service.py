import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.news_key_points_extraction_service import NewsKeyPointsExtractionService
from llm_services.news_report_generation_service import NewsReportGenerationService
from llm_services.openai_client_manager import OpenAIClientManager
from database.news_report_repository import NewsReportRepository
from database.postgresql_connection_manager import PostgreSQLConnectionManager
from config.database_connection_config import DatabaseConnectionConfig
from config.openai_api_keys_config import OpenAIAPIKeysConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsReportGenerationPipelineService:
    """
    Main service that orchestrates the report generation pipeline.
    Extracts key points from clustered news, generates reports, and marks news as processed.
    """
    
    def __init__(self):
        """
        Initialize the report generation pipeline service.
        """
        # Initialize database connection
        db_config = DatabaseConnectionConfig()
        self.connection_manager = PostgreSQLConnectionManager(db_config)
        
        # Initialize OpenAI clients
        openai_config = OpenAIAPIKeysConfig()
        self.client_manager = OpenAIClientManager(openai_config)
        
        # Initialize services
        self.key_points_extractor = NewsKeyPointsExtractionService(self.client_manager)
        self.report_generator = NewsReportGenerationService(self.client_manager)
        self.repository = NewsReportRepository(self.connection_manager)
    
    def process_report_generation(self):
        """
        Processes report generation pipeline for all clusters needing reports.
        
        Returns:
            dict: Statistics about the processing
        """
        logger.info("Starting report generation pipeline")
        
        # Step 1: Get clusters that need reports
        clusters = self.repository.get_clusters_for_report_generation()
        
        if not clusters:
            logger.info("No clusters found needing report generation")
            return {
                'clusters_processed': 0,
                'reports_generated': 0,
                'news_marked_processed': 0
            }
        
        logger.info(f"Found {len(clusters)} clusters needing reports")
        
        reports_generated = 0
        total_news_processed = 0
        
        # Step 2: Process each cluster
        for cluster_id, topic, news_ids in clusters:
            try:
                logger.info(f"Processing cluster {cluster_id}: '{topic}' ({len(news_ids)} articles)")
                
                # Step 3: Get news details
                news_details = self.repository.get_news_details_for_cluster(news_ids)
                
                # Step 4: Extract key points from each article
                logger.info(f"Extracting key points from {len(news_details)} articles...")
                news_articles_data = []
                
                for news_id, arabic_content, source_url in news_details:
                    try:
                        key_points_data = self.key_points_extractor.extract_key_points(arabic_content, news_id)
                        
                        # Extract source name from URL
                        source_name = self._extract_source_name_from_url(source_url)
                        
                        # Use ALL points (current + historical) for report generation
                        # This preserves historical context in the final report
                        all_points_text = []
                        if isinstance(key_points_data, dict):
                            # New format with temporal classification
                            for point in key_points_data.get("all_points", []):
                                all_points_text.append(point.get("text", ""))
                        else:
                            # Old format (backward compatibility)
                            all_points_text = key_points_data if isinstance(key_points_data, list) else []
                        
                        news_articles_data.append({
                            "news_id": news_id,
                            "key_points": all_points_text,  # Use all points for report
                            "source": source_name,
                            "source_url": source_url
                        })
                        
                    except Exception as e:
                        logger.error(f"Failed to extract key points for news {news_id}: {str(e)}")
                        continue
                
                if not news_articles_data:
                    logger.warning(f"No key points extracted for cluster {cluster_id}, skipping")
                    continue
                
                # Step 5: Generate report from key points
                logger.info(f"Generating report for cluster {cluster_id}...")
                cluster_data = {
                    "cluster_topic": topic,
                    "news_articles": news_articles_data
                }
                
                report_result = self.report_generator.generate_report_from_cluster(cluster_data)
                
                # Step 6: Save report to database
                report_id = self.repository.save_report(
                    cluster_id=cluster_id,
                    report_title=report_result["title"],
                    report_text=report_result["report"],
                    content_type_name=report_result["content_type"]
                )
                
                logger.info(f"Saved report {report_id} for cluster {cluster_id}")
                
                # Step 7: Mark news as processed
                processed_news_ids = [article["news_id"] for article in news_articles_data]
                self.repository.mark_news_as_processed(processed_news_ids)
                
                reports_generated += 1
                total_news_processed += len(processed_news_ids)
                
                logger.info(f"Cluster {cluster_id} completed: report generated, {len(processed_news_ids)} news marked as processed")
                
            except Exception as e:
                logger.error(f"Failed to process cluster {cluster_id}: {str(e)}")
                continue
        
        stats = {
            'clusters_processed': len(clusters),
            'reports_generated': reports_generated,
            'news_marked_processed': total_news_processed
        }
        
        logger.info(f"Report generation pipeline completed: {stats}")
        return stats
    
    def _extract_source_name_from_url(self, url: str) -> str:
        """
        Extracts source name from URL.
        
        Args:
            url: Source URL
            
        Returns:
            str: Source name
        """
        if not url:
            return "Unknown"
        
        # Extract domain name
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Extract main name
            parts = domain.split('.')
            if len(parts) >= 2:
                return parts[0].capitalize()
            
            return domain
            
        except Exception:
            return "Unknown"
