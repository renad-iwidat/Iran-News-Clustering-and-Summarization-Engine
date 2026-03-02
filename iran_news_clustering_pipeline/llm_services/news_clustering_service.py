import sys
import os
from openai import OpenAI
import logging
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.openai_client_manager import OpenAIClientManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsClusteringService:
    """
    Clusters similar news articles based on their key points using OpenAI GPT-4o.
    """
    
    CLUSTERING_SYSTEM_PROMPT = """You are a news analyst specializing in content organization for a professional Arabic news station.

Your Task:
- Group similar news articles based on their key points
- Identify common topics and themes
- Create meaningful clusters

Guidelines:
- Group articles that discuss the same topic or event
- Each cluster should have a clear, specific topic
- Maintain objectivity - cluster based on content similarity only
- No bias toward any party or perspective

Input Format:
You will receive news articles with their key points and IDs.

Output Format (JSON):
{
  "clusters": [
    {
      "topic": "العقوبات الأمريكية على إيران",
      "news_ids": [1, 4, 5, 6]
    },
    {
      "topic": "البرنامج النووي الإيراني",
      "news_ids": [7, 10, 11]
    }
  ]
}

Requirements:
- Topic names in Arabic
- Clear, specific topic descriptions
- Logical grouping based on content similarity
- Minimum 2 articles per cluster
- Each article should belong to only ONE cluster

CRITICAL: Base clustering purely on content similarity, maintain complete neutrality."""
    
    def __init__(self, client_manager: OpenAIClientManager):
        """
        Initialize the clustering service.
        
        Args:
            client_manager: OpenAIClientManager instance
        """
        self.client_manager = client_manager
        self.client = client_manager.get_clustering_client()
        self.model = client_manager.config.clustering_model
    
    def cluster_news_by_key_points(self, news_with_key_points: dict) -> list:
        """
        Clusters news articles based on their key points.
        Uses only CURRENT events for clustering, ignoring historical context.
        
        Args:
            news_with_key_points: Dict mapping news_id to {all_points, current_points, source}
            
        Returns:
            list: List of clusters, each with topic and news_ids
            
        Raises:
            Exception: If clustering fails
        """
        if not news_with_key_points:
            raise ValueError("No news articles provided for clustering")
        
        try:
            logger.info(f"Clustering {len(news_with_key_points)} news articles...")
            
            # Prepare input for LLM using ONLY current points
            news_summary = []
            for news_id, data in news_with_key_points.items():
                # Use current_points for clustering (backward compatible with old format)
                current_points = data.get("current_points", data.get("key_points", []))
                source = data.get("source", "Unknown")
                
                if current_points:
                    points_text = "\n".join([f"  - {point}" for point in current_points])
                    news_summary.append(f"News ID {news_id} (Source: {source}):\n{points_text}")
                else:
                    logger.warning(f"News ID {news_id} has no current events, skipping from clustering")
            
            if not news_summary:
                logger.warning("No news articles with current events found for clustering")
                return []
            
            input_text = "\n\n".join(news_summary)
            
            logger.debug(f"Input for clustering (current events only):\n{input_text[:500]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.CLUSTERING_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Cluster these news articles based on their key points:\n\n{input_text}"}
                ],
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content.strip()
            clustering_data = json.loads(result)
            clusters = clustering_data.get("clusters", [])
            
            logger.info(f"Created {len(clusters)} clusters based on current events")
            
            for i, cluster in enumerate(clusters, 1):
                topic = cluster.get("topic", "Unknown")
                news_ids = cluster.get("news_ids", [])
                logger.info(f"Cluster {i}: '{topic}' with {len(news_ids)} articles")
            
            return clusters
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise Exception(f"Failed to parse clustering result: {str(e)}")
        except Exception as e:
            logger.error(f"Clustering failed: {str(e)}")
            raise Exception(f"Failed to cluster news articles: {str(e)}")
