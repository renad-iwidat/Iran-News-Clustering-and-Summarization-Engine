import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.news_key_points_extraction_service import NewsKeyPointsExtractionService
from llm_services.news_clustering_service import NewsClusteringService
from llm_services.openai_client_manager import OpenAIClientManager
from database.news_clustering_repository import NewsClusteringRepository
from database.postgresql_connection_manager import PostgreSQLConnectionManager
from config.database_connection_config import DatabaseConnectionConfig
from config.openai_api_keys_config import OpenAIAPIKeysConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsClusteringPipelineService:
    """
    Main service that orchestrates the clustering pipeline.
    Extracts key points, clusters similar news, and saves to database.
    """
    
    def __init__(self):
        """
        Initialize the clustering pipeline service.
        """
        # Initialize database connection
        db_config = DatabaseConnectionConfig()
        self.connection_manager = PostgreSQLConnectionManager(db_config)
        
        # Initialize OpenAI client
        openai_config = OpenAIAPIKeysConfig()
        self.client_manager = OpenAIClientManager(openai_config)
        
        # Initialize services
        self.key_points_extractor = NewsKeyPointsExtractionService(self.client_manager)
        self.clustering_service = NewsClusteringService(self.client_manager)
        self.repository = NewsClusteringRepository(self.connection_manager)
    
    def process_clustering(self, batch_size: int = 20):
        """
        Processes news clustering pipeline.
        
        Args:
            batch_size: Number of articles to process
            
        Returns:
            dict: Statistics about the processing
        """
        logger.info(f"Starting clustering pipeline (batch size: {batch_size})")
        
        # Step 1: Fetch translated news
        news_articles = self.repository.get_news_for_clustering(limit=batch_size)
        
        if not news_articles:
            logger.info("No news articles found for clustering")
            return {
                'processed': 0,
                'clusters_created': 0
            }
        
        logger.info(f"Found {len(news_articles)} news articles for clustering")
        
        # Step 2: Extract key points from each article
        logger.info("Extracting key points from articles...")
        news_with_key_points = self.key_points_extractor.extract_key_points_batch(news_articles)
        
        # Step 3: Cluster based on key points
        logger.info("Clustering articles based on key points...")
        clusters = self.clustering_service.cluster_news_by_key_points(news_with_key_points)
        
        # Step 4: Save clusters to database
        logger.info("Saving clusters to database...")
        clusters_created = 0
        clustered_news_ids = set()
        
        for cluster in clusters:
            topic = cluster.get("topic", "Unknown Topic")
            news_ids = cluster.get("news_ids", [])
            
            if len(news_ids) < 1:
                logger.warning(f"Skipping empty cluster '{topic}'")
                continue
            
            # Use first news source_id as cluster source_id
            first_news_id = news_ids[0]
            source_id = self._get_source_id_for_news(first_news_id)
            
            # Create cluster
            cluster_id = self.repository.create_cluster(topic, source_id)
            
            # Add news to cluster
            self.repository.add_news_to_cluster(cluster_id, news_ids)
            
            # Track clustered news
            clustered_news_ids.update(news_ids)
            
            clusters_created += 1
            
            if len(news_ids) == 1:
                logger.info(f"Created standalone cluster for news {news_ids[0]}: '{topic}'")
        
        # Step 5: Handle standalone news (not in any cluster)
        all_news_ids = [news_id for news_id, _, _ in news_articles]
        standalone_news_ids = [nid for nid in all_news_ids if nid not in clustered_news_ids]
        
        if standalone_news_ids:
            logger.info(f"Found {len(standalone_news_ids)} standalone news articles")
            standalone_clusters_created = self._create_standalone_clusters(standalone_news_ids, news_with_key_points)
            clusters_created += standalone_clusters_created
        
        stats = {
            'processed': len(news_articles),
            'clusters_created': clusters_created,
            'standalone_clusters': len(standalone_news_ids)
        }
        
        logger.info(f"Clustering pipeline completed: {stats}")
        return stats
    
    def _get_source_id_for_news(self, news_id: int) -> int:
        """
        Gets the source_id for a news article.
        
        Args:
            news_id: ID of the news article
            
        Returns:
            int: source_id
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("SELECT source_id FROM raw_data WHERE id = %s;", (news_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result else 1
            
        except Exception as e:
            logger.error(f"Failed to get source_id for news {news_id}: {str(e)}")
            return 1
        finally:
            if connection:
                connection.close()
    
    def _create_standalone_clusters(self, standalone_news_ids: list, news_with_key_points: dict) -> int:
        """
        Creates individual clusters for standalone news articles.
        
        Args:
            standalone_news_ids: List of news IDs that are not in any cluster
            news_with_key_points: Dictionary mapping news_id to key points
            
        Returns:
            int: Number of standalone clusters created
        """
        standalone_clusters_created = 0
        
        for news_id in standalone_news_ids:
            try:
                # Get key points for this news
                news_data = news_with_key_points.get(news_id, {})
                key_points = news_data.get("key_points", [])
                
                if not key_points:
                    logger.warning(f"No key points found for standalone news {news_id}, skipping")
                    continue
                
                # Use first key point as topic (or combine first 2)
                if len(key_points) >= 2:
                    topic = f"{key_points[0][:50]}... {key_points[1][:30]}..."
                else:
                    topic = key_points[0][:80] + "..." if len(key_points[0]) > 80 else key_points[0]
                
                # Get source_id
                source_id = self._get_source_id_for_news(news_id)
                
                # Create standalone cluster
                cluster_id = self.repository.create_cluster(topic, source_id)
                
                # Add news to cluster
                self.repository.add_news_to_cluster(cluster_id, [news_id])
                
                standalone_clusters_created += 1
                logger.info(f"Created standalone cluster {cluster_id} for news {news_id}")
                
            except Exception as e:
                logger.error(f"Failed to create standalone cluster for news {news_id}: {str(e)}")
                continue
        
        return standalone_clusters_created
    
    def get_statistics(self):
        """
        Gets clustering statistics from the database.
        
        Returns:
            dict: Clustering statistics
        """
        return self.repository.get_cluster_statistics()
