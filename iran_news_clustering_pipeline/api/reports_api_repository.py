import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.postgresql_connection_manager import PostgreSQLConnectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportsAPIRepository:
    """
    Repository for API endpoints to fetch reports data.
    """
    
    def __init__(self, connection_manager: PostgreSQLConnectionManager):
        """
        Initialize the repository.
        
        Args:
            connection_manager: PostgreSQLConnectionManager instance
        """
        self.connection_manager = connection_manager
    
    def get_all_reports_with_pagination(self, page: int = 1, limit: int = 20):
        """
        Gets all reports with pagination.
        
        Args:
            page: Page number (starts from 1)
            limit: Number of reports per page
            
        Returns:
            tuple: (total_count, reports_list)
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM output_content;")
            total_count = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * limit
            
            # Get reports with pagination
            cursor.execute("""
                SELECT 
                    oc.id,
                    oc.title,
                    oc.content,
                    ct.name as content_type_name,
                    c.topic as cluster_topic,
                    oc.cluster_id,
                    oc.created_at
                FROM output_content oc
                JOIN content_type ct ON oc.content_type_id = ct.id
                JOIN clusters c ON oc.cluster_id = c.id
                ORDER BY oc.created_at DESC
                LIMIT %s OFFSET %s;
            """, (limit, offset))
            
            reports = cursor.fetchall()
            cursor.close()
            
            return total_count, reports
            
        except Exception as e:
            logger.error(f"Failed to get reports: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def get_report_by_id_with_sources(self, report_id: int):
        """
        Gets a single report by ID with all its sources.
        
        Args:
            report_id: ID of the report
            
        Returns:
            dict: Report data with sources, or None if not found
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            # Get report details
            cursor.execute("""
                SELECT 
                    oc.id,
                    oc.title,
                    oc.content,
                    ct.name as content_type_name,
                    c.topic as cluster_topic,
                    c.id as cluster_id,
                    oc.created_at
                FROM output_content oc
                JOIN content_type ct ON oc.content_type_id = ct.id
                JOIN clusters c ON oc.cluster_id = c.id
                WHERE oc.id = %s;
            """, (report_id,))
            
            report = cursor.fetchone()
            
            if not report:
                cursor.close()
                return None
            
            # Get sources (original news URLs) for this cluster
            cluster_id = report[5]
            cursor.execute("""
                SELECT DISTINCT rd.url, s.url as source_url
                FROM cluster_members cm
                JOIN raw_data rd ON cm.raw_id = rd.id
                JOIN sources s ON rd.source_id = s.id
                WHERE cm.cluster_id = %s
                ORDER BY rd.url;
            """, (cluster_id,))
            
            results = cursor.fetchall()
            
            # Extract source names from URLs
            sources = []
            for news_url, source_url in results:
                # Skip manual text sources
                if source_url == 'text' or news_url.startswith('manual_text'):
                    sources.append(("Manual Text", "manual"))
                else:
                    source_name = self._extract_source_name_from_url(news_url)
                    sources.append((source_name, news_url))
            cursor.close()
            
            return {
                'report': report,
                'sources': sources
            }
            
        except Exception as e:
            logger.error(f"Failed to get report {report_id}: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def get_sources_for_cluster(self, cluster_id: int):
        """
        Gets all sources (original news URLs) for a specific cluster.
        
        Args:
            cluster_id: ID of the cluster
            
        Returns:
            list: List of tuples (source_name, source_url) where source_name is extracted from URL
        """
        connection = None
        try:
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT DISTINCT rd.url, s.url as source_url
                FROM cluster_members cm
                JOIN raw_data rd ON cm.raw_id = rd.id
                JOIN sources s ON rd.source_id = s.id
                WHERE cm.cluster_id = %s
                ORDER BY rd.url;
            """, (cluster_id,))
            
            results = cursor.fetchall()
            cursor.close()
            
            # Extract source name from URL
            sources = []
            for news_url, source_url in results:
                # Skip manual text sources
                if source_url == 'text' or news_url.startswith('manual_text'):
                    sources.append(("Manual Text", "manual"))
                else:
                    source_name = self._extract_source_name_from_url(news_url)
                    sources.append((source_name, news_url))
            
            return sources
            
        except Exception as e:
            logger.error(f"Failed to get sources for cluster {cluster_id}: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
    
    def _extract_source_name_from_url(self, url: str) -> str:
        """
        Extracts a readable source name from URL.
        
        Args:
            url: Source URL
            
        Returns:
            str: Source name (e.g., "Ynet", "Maariv", "Walla")
        """
        if not url:
            return "Unknown"
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Extract main name and capitalize
            parts = domain.split('.')
            if len(parts) >= 2:
                name = parts[0].capitalize()
                
                # Special handling for known sources
                name_mapping = {
                    'Ynet': 'Ynet',
                    'Maariv': 'Maariv',
                    'Walla': 'Walla',
                    'Aljazeera': 'Al Jazeera',
                    'Alarabiya': 'Al Arabiya',
                    'Almayadeen': 'Al Mayadeen',
                    'Channel12': 'Channel 12',
                    'T': 'Telegram'  # for t.me
                }
                
                return name_mapping.get(name, name)
            
            return domain
            
        except Exception:
            return "Unknown"
    
    def _extract_source_name_from_url(self, url: str) -> str:
        """
        Extracts a readable source name from URL.
        
        Args:
            url: Source URL
            
        Returns:
            str: Source name (e.g., "Ynet", "Maariv", "Walla")
        """
        if not url:
            return "Unknown"
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Extract main name and capitalize
            parts = domain.split('.')
            if len(parts) >= 2:
                name = parts[0].capitalize()
                
                # Special handling for known sources
                name_mapping = {
                    'Ynet': 'Ynet',
                    'Maariv': 'Maariv',
                    'Walla': 'Walla',
                    'Aljazeera': 'Al Jazeera',
                    'Alarabiya': 'Al Arabiya',
                    'Almayadeen': 'Al Mayadeen',
                    'Channel12': 'Channel 12',
                    'T': 'Telegram'  # for t.me
                }
                
                return name_mapping.get(name, name)
            
            return domain
            
        except Exception:
            return "Unknown"
    
    def count_words_in_content(self, content: str) -> int:
        """
        Counts words in Arabic content.
        
        Args:
            content: The content text
            
        Returns:
            int: Word count
        """
        if not content:
            return 0
        
        # Simple word count (split by spaces)
        words = content.split()
        return len(words)
