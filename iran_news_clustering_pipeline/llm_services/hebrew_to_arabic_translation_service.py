import sys
import os
from openai import OpenAI
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.openai_client_manager import OpenAIClientManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HebrewToArabicTranslationService:
    """
    Translates Hebrew text to Arabic using OpenAI GPT-4o.
    Specialized for news articles about Iran.
    """
    
    TRANSLATION_SYSTEM_PROMPT = """You are a professional translator specializing in Hebrew to Arabic translation for a leading Arabic news station focused on economics and politics.

Your Role:
- Translate Hebrew news articles to Modern Standard Arabic
- Maintain the highest level of professionalism
- Preserve accuracy and journalistic tone

Target Audience:
- Specialized, professional audience
- Experts in politics, security, and economics

Coverage Focus:
- Israeli internal affairs
- News, security, and economic developments
- Iran-related news

MANDATORY Terminology Rules (CRITICAL):
- Replace "צבא ההגנה" (Army of Defense) with "الجيش الإسرائيلي" (Israeli Army)
- Replace "מחבל" (terrorist/saboteur) with "مسلح" (armed person)
- Replace "כוחות הכיבוש" (Occupation Forces) with "الجيش الإسرائيلي" (Israeli Army)
- Maintain complete neutrality - no bias toward any party

Translation Guidelines:
- Use professional journalistic Arabic
- Preserve proper nouns (names, places, organizations)
- Maintain factual accuracy
- Keep the original meaning and context
- Output ONLY the Arabic translation, no explanations

IMPORTANT: The translation must be completely neutral and unbiased."""
    
    def __init__(self, client_manager: OpenAIClientManager):
        """
        Initialize the translation service.
        
        Args:
            client_manager: OpenAIClientManager instance
        """
        self.client_manager = client_manager
        self.client = client_manager.get_translation_client()
        self.model = client_manager.config.translation_model
    
    def translate_hebrew_to_arabic(self, hebrew_text: str) -> str:
        """
        Translates Hebrew text to Arabic.
        
        Args:
            hebrew_text: The Hebrew text to translate
            
        Returns:
            str: The Arabic translation
            
        Raises:
            Exception: If translation fails
        """
        if not hebrew_text or not hebrew_text.strip():
            raise ValueError("Hebrew text cannot be empty")
        
        try:
            logger.info(f"Translating Hebrew text ({len(hebrew_text)} characters)...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.TRANSLATION_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Translate this Hebrew news article to Arabic:\n\n{hebrew_text}"}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            arabic_translation = response.choices[0].message.content.strip()
            
            logger.info(f"Translation completed ({len(arabic_translation)} characters)")
            logger.debug(f"Original: {hebrew_text[:100]}...")
            logger.debug(f"Translation: {arabic_translation[:100]}...")
            
            return arabic_translation
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise Exception(f"Failed to translate Hebrew to Arabic: {str(e)}")
    
    def translate_batch(self, hebrew_texts: list) -> list:
        """
        Translates multiple Hebrew texts to Arabic.
        
        Args:
            hebrew_texts: List of Hebrew texts to translate
            
        Returns:
            list: List of Arabic translations
        """
        translations = []
        
        for i, text in enumerate(hebrew_texts, 1):
            try:
                logger.info(f"Translating text {i}/{len(hebrew_texts)}")
                translation = self.translate_hebrew_to_arabic(text)
                translations.append(translation)
            except Exception as e:
                logger.error(f"Failed to translate text {i}: {str(e)}")
                translations.append(None)
        
        return translations
