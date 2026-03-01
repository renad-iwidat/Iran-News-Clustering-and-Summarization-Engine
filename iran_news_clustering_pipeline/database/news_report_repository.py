import sys
import os
from datetime import datetime
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.postgresql_connection_manager import PostgreSQLConnectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsReportRepository:
    """
    Handles database operations for news reports.
    Manages output_content table and marks news as processed.
    """
    
    def __init__(self, connection_manager: PostgreSQLConnectionManager):
        """
        Initialize the repository.
        
        Args:
            connection_manager: PostgreSQLConnectionManager instance
        """
        self.connection_manager = connection_manager
    
    def save_report(self, cluster_id: int, report_title: str, report_text: str, content_type_name: str) -> int:
        """
        Saves a generated report to the database.
        
        Args:
            cluster_id: ID of the cluster
            report_title: The generated report title/headline
            report_text: The generated report text
            content_type_name: Type of content (short_news, medium_news, etc.)
            
        Returns:
            int: The ID of the created report
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            # Get content_type_id
            cursor.execute("SELECT id FROM content_type WHERE name = %s;", (content_type_name,))
            result = cursor.fetchone()
            
            if not result:
                logger.warning(f"Content type '{content_type_name}' not found, using default")
                content_type_id = 2  # medium_news as default
            else:
                content_type_id = result[0]
            
            # Insert report
            cursor.execute("""
                INSERT INTO output_content (cluster_id, content_type_id, title, content, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (cluster_id, content_type_id, report_title, report_text, datetime.now()))
            
            report_id = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
            
            logger.info(f"Saved report ID {report_id} for cluster {cluster_id} (title: {report_title[:50]}..., type: {content_type_name})")
            return report_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Failed to save report for cluster {cluster_id}: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def mark_news_as_processed(self, news_ids: list):
        """
        Marks news articles as processed.
        
        Args:
            news_ids: List of news article IDs
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            for news_id in news_ids:
                cursor.execute("""
                    UPDATE raw_data
                    SET is_processed = true, processed_at = %s
                    WHERE id = %s;
                """, (datetime.now(), news_id))
            
            connection.commit()
            cursor.close()
            
            logger.info(f"Marked {len(news_ids)} news articles as processed")
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Failed to mark news as processed: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def get_clusters_for_report_generation(self):
        """
        Gets clusters that need report generation.
        
        Returns:
            list: List of tuples (cluster_id, topic, news_ids)
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT c.id, c.topic, ARRAY_AGG(cm.raw_id) as news_ids
                FROM clusters c
                JOIN cluster_members cm ON c.id = cm.cluster_id
                LEFT JOIN output_content oc ON c.id = oc.cluster_id
                WHERE oc.id IS NULL
                GROUP BY c.id, c.topic;
            """)
            
            results = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Found {len(results)} clusters needing report generation")
            return results
            
        except Exception as e:
            logger.error(f"Failed to get clusters for report generation: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def get_news_details_for_cluster(self, news_ids: list):
        """
        Gets news details for a cluster from translations table.
        
        Args:
            news_ids: List of news IDs
            
        Returns:
            list: List of tuples (news_id, arabic_content, news_article_url)
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            placeholders = ','.join(['%s'] * len(news_ids))
            cursor.execute(f"""
                SELECT rd.id, t.translated_content, rd.url
                FROM raw_data rd
                JOIN translations t ON rd.id = t.raw_data_id AND t.target_language = 'ar'
                WHERE rd.id IN ({placeholders});
            """, news_ids)
            
            results = cursor.fetchall()
            cursor.close()
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to get news details: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
