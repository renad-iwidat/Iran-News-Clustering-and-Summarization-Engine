import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class OpenAIAPIKeysConfig:
    """
    Configuration class for OpenAI API keys.
    Loads different keys for different services from environment variables.
    """
    
    translation_api_key: str = os.getenv("OPENAI_API_KEY_IRAN_NEWS_TRANSLATION_HEBREW_ARABIC", "")
    clustering_api_key: str = os.getenv("OPENAI_API_KEY_IRAN_NEWS_CLUSTERING_ANALYSIS", "")
    report_generation_api_key: str = os.getenv("OPENAI_API_KEY_IRAN_NEWS_REPORT_SUMMARIZATION", "")
    
    translation_model: str = os.getenv("OPENAI_MODEL_FOR_TRANSLATION", "gpt-4o")
    clustering_model: str = os.getenv("OPENAI_MODEL_FOR_CLUSTERING", "gpt-4o")
    report_generation_model: str = os.getenv("OPENAI_MODEL_FOR_REPORT_GENERATION", "gpt-4o")
    
    def validate_keys(self) -> dict:
        """
        Validates that all API keys are present.
        
        Returns:
            dict: Validation results for each key
        """
        validation_results = {
            "translation_key": bool(self.translation_api_key),
            "clustering_key": bool(self.clustering_api_key),
            "report_generation_key": bool(self.report_generation_api_key)
        }
        return validation_results
    
    def get_all_keys(self) -> dict:
        """
        Returns all API keys as a dictionary.
        
        Returns:
            dict: All API keys with their purposes
        """
        return {
            "translation": self.translation_api_key,
            "clustering": self.clustering_api_key,
            "report_generation": self.report_generation_api_key
        }
