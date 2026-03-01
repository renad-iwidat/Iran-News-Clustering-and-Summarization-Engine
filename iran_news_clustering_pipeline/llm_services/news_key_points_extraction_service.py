import sys
import os
from openai import OpenAI
import logging
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.openai_client_manager import OpenAIClientManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsKeyPointsExtractionService:
    """
    Extracts key points from news articles using OpenAI GPT-4o.
    Specialized for professional Arabic news coverage.
    """
    
    KEY_POINTS_EXTRACTION_SYSTEM_PROMPT = """You are a professional journalist working for a leading Arabic news station specialized in economics and politics.

Your Role:
- Extract key points from news articles
- Focus on accurate information, context, and implications

Target Audience:
- Specialized, professional, expert audience
- Professionals in politics, security, and economics

Coverage Focus:
- Israeli internal affairs
- News, security, and economic developments
- Iran-related news

Task:
- Extract 3-5 key points from each news article
- Each point should be one clear, concise sentence
- Focus on facts, not opinions
- Maintain complete neutrality

MANDATORY Terminology Rules:
- Use "الجيش الإسرائيلي" (Israeli Army) consistently
- Use "مسلح" (armed person) instead of biased terms
- Maintain professional, neutral language

Output Format:
- Provide key points in Arabic only
- Return as JSON array
- Be concise and factual

Example Output:
{
  "key_points": [
    "فرضت الولايات المتحدة عقوبات جديدة على إيران",
    "العقوبات تستهدف قطاع النفط الإيراني",
    "الهدف الحد من قدرة طهران على تمويل برنامجها النووي"
  ]
}

CRITICAL: Maintain complete neutrality and objectivity."""
    
    def __init__(self, client_manager: OpenAIClientManager):
        """
        Initialize the key points extraction service.
        
        Args:
            client_manager: OpenAIClientManager instance
        """
        self.client_manager = client_manager
        self.client = client_manager.get_clustering_client()
        self.model = client_manager.config.clustering_model
    
    def extract_key_points(self, news_content: str, news_id: int = None) -> list:
        """
        Extracts key points from a news article.
        
        Args:
            news_content: The Arabic news content
            news_id: Optional news ID for logging
            
        Returns:
            list: List of key points (strings)
            
        Raises:
            Exception: If extraction fails
        """
        if not news_content or not news_content.strip():
            raise ValueError("News content cannot be empty")
        
        try:
            log_prefix = f"News ID {news_id}: " if news_id else ""
            logger.info(f"{log_prefix}Extracting key points from article ({len(news_content)} characters)...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.KEY_POINTS_EXTRACTION_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Extract key points from this news article:\n\n{news_content}"}
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content.strip()
            key_points_data = json.loads(result)
            key_points = key_points_data.get("key_points", [])
            
            logger.info(f"{log_prefix}Extracted {len(key_points)} key points")
            
            return key_points
            
        except json.JSONDecodeError as e:
            logger.error(f"{log_prefix}Failed to parse JSON response: {str(e)}")
            raise Exception(f"Failed to parse key points: {str(e)}")
        except Exception as e:
            logger.error(f"{log_prefix}Key points extraction failed: {str(e)}")
            raise Exception(f"Failed to extract key points: {str(e)}")
    
    def extract_key_points_batch(self, news_articles: list) -> dict:
        """
        Extracts key points from multiple news articles.
        
        Args:
            news_articles: List of tuples (news_id, content, source_name)
            
        Returns:
            dict: Dictionary mapping news_id to key points
        """
        results = {}
        
        for news_id, content, source_name in news_articles:
            try:
                logger.info(f"Processing news ID {news_id} from {source_name}")
                key_points = self.extract_key_points(content, news_id)
                results[news_id] = {
                    "key_points": key_points,
                    "source": source_name
                }
            except Exception as e:
                logger.error(f"Failed to extract key points for news ID {news_id}: {str(e)}")
                results[news_id] = {
                    "key_points": [],
                    "source": source_name,
                    "error": str(e)
                }
        
        return results
