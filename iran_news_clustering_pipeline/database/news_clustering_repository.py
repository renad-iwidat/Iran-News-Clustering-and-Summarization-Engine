import sys
import os
from datetime import datetime
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.postgresql_connection_manager import PostgreSQLConnectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsClusteringRepository:
    """
    Handles database operations for news clustering.
    Manages clusters and cluster_members tables.
    """
    
    def __init__(self, connection_manager: PostgreSQLConnectionManager):
        """
        Initialize the repository.
        
        Args:
            connection_manager: PostgreSQLConnectionManager instance
        """
        self.connection_manager = connection_manager
    
    def create_cluster(self, topic: str, source_id: int) -> int:
        """
        Creates a new cluster in the database.
        
        Args:
            topic: The topic/theme of the cluster
            source_id: ID of the primary source
            
        Returns:
            int: The ID of the created cluster
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                INSERT INTO clusters (topic, source_id, created_at)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (topic, source_id, datetime.now()))
            
            cluster_id = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
            
            logger.info(f"Created cluster ID {cluster_id}: '{topic}'")
            return cluster_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Failed to create cluster: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def add_news_to_cluster(self, cluster_id: int, news_ids: list):
        """
        Adds news articles to a cluster.
        
        Args:
            cluster_id: ID of the cluster
            news_ids: List of news article IDs to add
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            for news_id in news_ids:
                cursor.execute("""
                    INSERT INTO cluster_members (cluster_id, raw_id, created_at)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (cluster_id, raw_id) DO NOTHING;
                """, (cluster_id, news_id, datetime.now()))
            
            connection.commit()
            cursor.close()
            
            logger.info(f"Added {len(news_ids)} news articles to cluster {cluster_id}")
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Failed to add news to cluster {cluster_id}: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def get_news_for_clustering(self, limit: int = 20):
        """
        Fetches translated news articles that are ready for clustering.
        Reads from the new translations table.
        
        Args:
            limit: Maximum number of articles to fetch
            
        Returns:
            list: List of tuples (id, arabic_content, source_url)
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT rd.id, t.translated_content, s.url
                FROM raw_data rd
                JOIN translations t ON rd.id = t.raw_data_id AND t.target_language = 'ar'
                JOIN sources s ON rd.source_id = s.id
                WHERE rd.is_processed = false
                AND t.translation_status IN ('completed', 'not_required')
                AND t.translated_content IS NOT NULL
                ORDER BY rd.id DESC
                LIMIT %s;
            """, (limit,))
            
            results = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Fetched {len(results)} news articles for clustering")
            return results
            
        except Exception as e:
            logger.error(f"Failed to fetch news for clustering: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def get_cluster_statistics(self):
        """
        Gets statistics about clusters.
        
        Returns:
            dict: Statistics about clusters
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT c.id) as total_clusters,
                    COUNT(cm.raw_id) as total_news_in_clusters,
                    AVG(cluster_size.size) as avg_cluster_size
                FROM clusters c
                LEFT JOIN cluster_members cm ON c.id = cm.cluster_id
                LEFT JOIN (
                    SELECT cluster_id, COUNT(*) as size
                    FROM cluster_members
                    GROUP BY cluster_id
                ) cluster_size ON c.id = cluster_size.cluster_id;
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            stats = {
                'total_clusters': result[0] or 0,
                'total_news_in_clusters': result[1] or 0,
                'avg_cluster_size': float(result[2]) if result[2] else 0
            }
            
            logger.info(f"Cluster statistics: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get cluster statistics: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
