import sys
import os
from openai import OpenAI
from typing import Optional
import logging
import certifi

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.openai_api_keys_config import OpenAIAPIKeysConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['SSL_CERT_FILE'] = certifi.where()


class OpenAIClientManager:
    """
    Manages OpenAI API clients for different services.
    Provides separate clients for translation, clustering, and report generation.
    """
    
    def __init__(self, config: OpenAIAPIKeysConfig):
        """
        Initialize the OpenAI client manager with API keys configuration.
        
        Args:
            config: OpenAIAPIKeysConfig instance with API keys
        """
        self.config = config
        self.translation_client: Optional[OpenAI] = None
        self.clustering_client: Optional[OpenAI] = None
        self.report_generation_client: Optional[OpenAI] = None
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """
        Initializes OpenAI clients for each service.
        """
        try:
            if self.config.translation_api_key:
                self.translation_client = OpenAI(
                    api_key=self.config.translation_api_key,
                    timeout=120.0
                )
                logger.info("Translation client initialized successfully")
            
            if self.config.clustering_api_key:
                self.clustering_client = OpenAI(
                    api_key=self.config.clustering_api_key,
                    timeout=60.0
                )
                logger.info("Clustering client initialized successfully")
            
            if self.config.report_generation_api_key:
                self.report_generation_client = OpenAI(
                    api_key=self.config.report_generation_api_key,
                    timeout=60.0
                )
                logger.info("Report generation client initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI clients: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise
    
    def get_translation_client(self) -> OpenAI:
        """
        Returns the OpenAI client for translation service.
        
        Returns:
            OpenAI: Client instance for translation
        """
        if not self.translation_client:
            raise Exception("Translation client not initialized. Check API key.")
        return self.translation_client
    
    def get_clustering_client(self) -> OpenAI:
        """
        Returns the OpenAI client for clustering service.
        
        Returns:
            OpenAI: Client instance for clustering
        """
        if not self.clustering_client:
            raise Exception("Clustering client not initialized. Check API key.")
        return self.clustering_client
    
    def get_report_generation_client(self) -> OpenAI:
        """
        Returns the OpenAI client for report generation service.
        
        Returns:
            OpenAI: Client instance for report generation
        """
        if not self.report_generation_client:
            raise Exception("Report generation client not initialized. Check API key.")
        return self.report_generation_client
    
    def test_translation_client(self) -> bool:
        """
        Tests the translation client with a simple API call.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Testing translation client...")
            client = self.get_translation_client()
            
            response = client.chat.completions.create(
                model=self.config.translation_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Translation client is working'"}
                ],
                max_tokens=20
            )
            
            result = response.choices[0].message.content
            logger.info(f"Translation client test result: {result}")
            return True
            
        except Exception as e:
            logger.error(f"Translation client test failed: {str(e)}")
            return False
    
    def test_clustering_client(self) -> bool:
        """
        Tests the clustering client with a simple API call.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Testing clustering client...")
            client = self.get_clustering_client()
            
            response = client.chat.completions.create(
                model=self.config.clustering_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Clustering client is working'"}
                ],
                max_tokens=20
            )
            
            result = response.choices[0].message.content
            logger.info(f"Clustering client test result: {result}")
            return True
            
        except Exception as e:
            logger.error(f"Clustering client test failed: {str(e)}")
            return False
    
    def test_report_generation_client(self) -> bool:
        """
        Tests the report generation client with a simple API call.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Testing report generation client...")
            client = self.get_report_generation_client()
            
            response = client.chat.completions.create(
                model=self.config.report_generation_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Report generation client is working'"}
                ],
                max_tokens=20
            )
            
            result = response.choices[0].message.content
            logger.info(f"Report generation client test result: {result}")
            return True
            
        except Exception as e:
            logger.error(f"Report generation client test failed: {str(e)}")
            return False
    
    def test_all_clients(self) -> dict:
        """
        Tests all OpenAI clients.
        
        Returns:
            dict: Test results for each client
        """
        results = {
            "translation": self.test_translation_client(),
            "clustering": self.test_clustering_client(),
            "report_generation": self.test_report_generation_client()
        }
        return results
