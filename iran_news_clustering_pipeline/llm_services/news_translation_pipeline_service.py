import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.language_detection_service import LanguageDetectionService
from llm_services.hebrew_to_arabic_translation_service import HebrewToArabicTranslationService
from llm_services.openai_client_manager import OpenAIClientManager
from database.news_translation_repository import NewsTranslationRepository
from database.postgresql_connection_manager import PostgreSQLConnectionManager
from config.database_connection_config import DatabaseConnectionConfig
from config.openai_api_keys_config import OpenAIAPIKeysConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsTranslationPipelineService:
    """
    Main service that orchestrates the translation pipeline.
    Detects language, translates if needed, and updates database.
    """
    
    def __init__(self):
        """
        Initialize the translation pipeline service.
        """
        # Initialize database connection
        db_config = DatabaseConnectionConfig()
        self.connection_manager = PostgreSQLConnectionManager(db_config)
        
        # Initialize OpenAI client
        openai_config = OpenAIAPIKeysConfig()
        self.client_manager = OpenAIClientManager(openai_config)
        
        # Initialize services
        self.language_detector = LanguageDetectionService()
        self.translator = HebrewToArabicTranslationService(self.client_manager)
        self.repository = NewsTranslationRepository(self.connection_manager)
    
    def process_single_news(self, news_id: int, content: str):
        """
        Processes a single news article for translation.
        
        Args:
            news_id: ID of the news article
            content: Content of the news article
        """
        try:
            logger.info(f"Processing news ID {news_id}")
            
            # Step 1: Detect language
            detected_language = self.language_detector.detect_language(content)
            logger.info(f"Detected language: {detected_language}")
            
            if detected_language == 'unknown':
                logger.warning(f"Could not detect language for news ID {news_id}")
                self.repository.update_translation_info(
                    news_id=news_id,
                    original_language='unknown',
                    arabic_content=content,
                    translation_status='failed',
                    error_message='Could not detect language'
                )
                return
            
            # Step 2: Handle based on language
            if detected_language == 'ar':
                # Arabic - no translation needed
                logger.info(f"News ID {news_id} is already in Arabic")
                self.repository.update_translation_info(
                    news_id=news_id,
                    original_language='ar',
                    arabic_content=content,
                    translation_status='not_required'
                )
            
            elif detected_language == 'he':
                # Hebrew - translate to Arabic
                logger.info(f"News ID {news_id} is in Hebrew, translating...")
                try:
                    arabic_translation = self.translator.translate_hebrew_to_arabic(content)
                    
                    self.repository.update_translation_info(
                        news_id=news_id,
                        original_language='he',
                        arabic_content=arabic_translation,
                        translation_status='completed'
                    )
                    
                    logger.info(f"Successfully translated news ID {news_id}")
                    
                except Exception as translation_error:
                    logger.error(f"Translation failed for news ID {news_id}: {str(translation_error)}")
                    self.repository.update_translation_info(
                        news_id=news_id,
                        original_language='he',
                        arabic_content=None,
                        translation_status='failed',
                        error_message=str(translation_error)
                    )
        
        except Exception as e:
            logger.error(f"Failed to process news ID {news_id}: {str(e)}")
            raise
    
    def process_batch(self, batch_size: int = 10):
        """
        Processes a batch of unprocessed news articles.
        
        Args:
            batch_size: Number of articles to process
            
        Returns:
            dict: Statistics about the processing
        """
        logger.info(f"Starting translation batch processing (batch size: {batch_size})")
        
        # Fetch unprocessed news
        unprocessed_news = self.repository.get_unprocessed_news(limit=batch_size)
        
        if not unprocessed_news:
            logger.info("No unprocessed news found")
            return {
                'processed': 0,
                'succeeded': 0,
                'failed': 0
            }
        
        logger.info(f"Found {len(unprocessed_news)} unprocessed news articles")
        
        succeeded = 0
        failed = 0
        
        for news_id, content in unprocessed_news:
            try:
                self.process_single_news(news_id, content)
                succeeded += 1
            except Exception as e:
                logger.error(f"Failed to process news ID {news_id}: {str(e)}")
                failed += 1
        
        stats = {
            'processed': len(unprocessed_news),
            'succeeded': succeeded,
            'failed': failed
        }
        
        logger.info(f"Batch processing completed: {stats}")
        return stats
    
    def get_statistics(self):
        """
        Gets translation statistics from the database.
        
        Returns:
            dict: Translation statistics
        """
        return self.repository.get_translation_statistics()
