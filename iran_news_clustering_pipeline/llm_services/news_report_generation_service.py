import sys
import os
from openai import OpenAI
import logging
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.openai_client_manager import OpenAIClientManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsReportGenerationService:
    """
    Generates comprehensive news reports from clustered articles using OpenAI GPT-4o.
    Includes source citations and determines content type.
    """
    
    REPORT_GENERATION_SYSTEM_PROMPT = """You are a professional journalist working for a leading Arabic news station specialized in economics and politics.

Your Role:
- Write comprehensive news reports from multiple sources
- Focus on accurate information, context, and implications
- Serve a specialized, professional, expert audience

Coverage Focus:
- Israeli internal affairs
- News, security, and economic developments
- Iran-related news

MANDATORY Writing Rules:

1. Neutrality (CRITICAL):
   - Complete neutrality - absolutely no bias toward any party
   - Present facts objectively
   - Avoid loaded language or emotional terms

2. Terminology (MANDATORY):
   - Use "الجيش الإسرائيلي" (Israeli Army) consistently
   - Never use "جيش الدفاع" or "جيش الاحتلال"
   - Use "مسلح" (armed person) instead of "إرهابي" or "مخرب"

3. Source Attribution (REQUIRED):
   - Cite sources at the end of each paragraph using Markdown hyperlinks
   - Format: [اسم المصدر](URL) [اسم المصدر2](URL2)
   - Example: [الجزيرة](https://www.aljazeera.net/news/article) [العربية](https://www.alarabiya.net/article)
   - Each source name must be a clickable link to the original article
   - DO NOT wrap sources with "المصدر:" or any other text
   - Just add the links directly in Markdown format

4. Content Quality:
   - Extract information from original texts
   - Rewrite in professional journalistic style
   - Maintain factual accuracy
   - Provide context and implications
   - Use clear, professional Arabic

Title Requirements:
- Create an attractive, professional headline (5-10 words)
- Capture the main story in Arabic
- Use active voice and strong verbs
- Be specific and informative
- Example: "واشنطن تشدد العقوبات على صناعة النفط الإيرانية"

Report Structure (CRITICAL):
- Start with CURRENT events and developments (what's happening NOW)
- Integrate historical context naturally within the narrative (not as separate section)
- Use historical events to provide background and understanding
- Maintain focus on current developments while enriching with context
- Logical flow: Present → Context → Present → Analysis
- Source citations after each paragraph
- Professional conclusion if needed

Historical Context Integration:
- Weave historical events naturally into the narrative
- Use phrases like: "تأتي هذه التطورات بعد..." or "في سياق..." or "منذ..."
- Historical context should SUPPORT the current story, not overshadow it
- Keep historical references concise but informative
- Example: "بدأت العملية الحالية... [current]. تأتي بعد سلسلة عمليات بدأت في يناير 2024... [context]. اليوم، تواصل القوات... [back to current]"

Content Type Classification:
After writing, classify the report as ONE of:
- short_news: Brief news (50-150 words), focuses on main facts
- medium_news: Standard news (150-300 words), includes context
- long_news: Detailed news (300-500 words), comprehensive coverage
- explanation: Explains background, context, and implications
- analysis: In-depth analysis with causes, effects, and predictions

Output Format (JSON):
{
  "title": "عنوان جذاب ومختصر للتقرير",
  "report": "التقرير الكامل بالعربية مع المصادر...",
  "content_type": "medium_news",
  "word_count": 250,
  "sources_used": ["الجزيرة", "العربية", "الميادين"]
}

CRITICAL REQUIREMENTS:
- Write ONLY in Arabic
- Maintain complete neutrality
- Follow terminology rules strictly
- Cite sources properly
- Professional journalistic style"""
    
    def __init__(self, client_manager: OpenAIClientManager):
        """
        Initialize the report generation service.
        
        Args:
            client_manager: OpenAIClientManager instance
        """
        self.client_manager = client_manager
        self.client = client_manager.get_report_generation_client()
        self.model = client_manager.config.report_generation_model
    
    def generate_report_from_cluster(self, cluster_data: dict) -> dict:
        """
        Generates a comprehensive report from a cluster of news articles.
        
        Args:
            cluster_data: Dict with cluster_topic, news_articles (list of dicts with key_points and source)
            
        Returns:
            dict: Report data with report text, content_type, word_count, sources
            
        Raises:
            Exception: If report generation fails
        """
        cluster_topic = cluster_data.get("cluster_topic", "Unknown Topic")
        news_articles = cluster_data.get("news_articles", [])
        
        if not news_articles:
            raise ValueError("No news articles provided for report generation")
        
        try:
            logger.info(f"Generating report for cluster: '{cluster_topic}' ({len(news_articles)} articles)")
            
            # Prepare input for LLM
            articles_summary = []
            for article in news_articles:
                source = article.get("source", "Unknown")
                source_url = article.get("source_url", "")
                key_points = article.get("key_points", [])
                
                if key_points:
                    points_text = "\n".join([f"  - {point}" for point in key_points])
                    articles_summary.append(f"من [{source}]({source_url}):\n{points_text}")
            
            input_text = f"الموضوع: {cluster_topic}\n\nالنقاط الرئيسية من المصادر:\n\n" + "\n\n".join(articles_summary)
            
            logger.debug(f"Input for report generation:\n{input_text[:500]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.REPORT_GENERATION_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Write a comprehensive news report based on these key points from multiple sources:\n\n{input_text}"}
                ],
                temperature=0.4,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content.strip()
            report_data = json.loads(result)
            
            title = report_data.get("title", "")
            report_text = report_data.get("report", "")
            content_type = report_data.get("content_type", "medium_news")
            word_count = report_data.get("word_count", 0)
            sources_used = report_data.get("sources_used", [])
            
            logger.info(f"Report generated: {word_count} words, type: {content_type}")
            logger.info(f"Title: {title}")
            logger.info(f"Sources used: {', '.join(sources_used)}")
            
            return {
                "title": title,
                "report": report_text,
                "content_type": content_type,
                "word_count": word_count,
                "sources_used": sources_used
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise Exception(f"Failed to parse report generation result: {str(e)}")
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            raise Exception(f"Failed to generate report: {str(e)}")
