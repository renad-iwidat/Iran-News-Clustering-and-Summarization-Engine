import sys
import os
from datetime import datetime
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.postgresql_connection_manager import PostgreSQLConnectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsTranslationRepository:
    """
    Handles database operations for news translation.
    Updates raw_data table with translation information.
    """
    
    def __init__(self, connection_manager: PostgreSQLConnectionManager):
        """
        Initialize the repository.
        
        Args:
            connection_manager: PostgreSQLConnectionManager instance
        """
        self.connection_manager = connection_manager
    
    def get_unprocessed_news(self, limit: int = 10):
        """
        Fetches unprocessed news articles from the database.
        
        Args:
            limit: Maximum number of articles to fetch
            
        Returns:
            list: List of tuples (id, content)
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT id, content
                FROM raw_data
                WHERE is_processed = false
                AND (translation_status = 'pending' OR translation_status IS NULL)
                ORDER BY published_at DESC
                LIMIT %s;
            """, (limit,))
            
            results = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Fetched {len(results)} unprocessed news articles")
            return results
            
        except Exception as e:
            logger.error(f"Failed to fetch unprocessed news: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def update_translation_info(self, news_id: int, original_language: str, 
                                arabic_content: str, translation_status: str,
                                error_message: str = None):
        """
        Updates translation information for a news article.
        
        Args:
            news_id: ID of the news article
            original_language: Detected language ('ar' or 'he')
            arabic_content: Arabic version of the content
            translation_status: Status of translation
            error_message: Error message if translation failed
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                UPDATE raw_data
                SET original_language = %s,
                    arabic_content = %s,
                    translation_status = %s,
                    translated_at = %s,
                    translation_error_message = %s
                WHERE id = %s;
            """, (
                original_language,
                arabic_content,
                translation_status,
                datetime.now() if translation_status in ['completed', 'not_required'] else None,
                error_message,
                news_id
            ))
            
            connection.commit()
            cursor.close()
            
            logger.info(f"Updated translation info for news ID {news_id}: {translation_status}")
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Failed to update translation info for news ID {news_id}: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def get_translation_statistics(self):
        """
        Gets statistics about translation status.
        
        Returns:
            dict: Statistics about translations
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN translation_status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN translation_status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN translation_status = 'not_required' THEN 1 ELSE 0 END) as not_required,
                    SUM(CASE WHEN translation_status = 'failed' THEN 1 ELSE 0 END) as failed
                FROM raw_data;
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            stats = {
                'total': result[0],
                'pending': result[1],
                'completed': result[2],
                'not_required': result[3],
                'failed': result[4]
            }
            
            logger.info(f"Translation statistics: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get translation statistics: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
