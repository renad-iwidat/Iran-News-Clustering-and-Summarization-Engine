import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LanguageDetectionService:
    """
    Detects the language of text content.
    Supports Hebrew and Arabic detection.
    """
    
    # Hebrew Unicode range
    HEBREW_PATTERN = re.compile(r'[\u0590-\u05FF]')
    
    # Arabic Unicode range
    ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
    
    def detect_language(self, text: str) -> str:
        """
        Detects if text is Hebrew or Arabic.
        
        Args:
            text: The text content to analyze
            
        Returns:
            str: 'he' for Hebrew, 'ar' for Arabic, 'unknown' if cannot determine
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for language detection")
            return 'unknown'
        
        # Count Hebrew and Arabic characters
        hebrew_chars = len(self.HEBREW_PATTERN.findall(text))
        arabic_chars = len(self.ARABIC_PATTERN.findall(text))
        
        logger.debug(f"Hebrew characters: {hebrew_chars}, Arabic characters: {arabic_chars}")
        
        # Determine language based on character count
        if hebrew_chars > arabic_chars and hebrew_chars > 10:
            logger.info("Detected language: Hebrew")
            return 'he'
        elif arabic_chars > hebrew_chars and arabic_chars > 10:
            logger.info("Detected language: Arabic")
            return 'ar'
        else:
            logger.warning(f"Could not determine language. Hebrew: {hebrew_chars}, Arabic: {arabic_chars}")
            return 'unknown'
    
    def is_hebrew(self, text: str) -> bool:
        """
        Checks if text is Hebrew.
        
        Args:
            text: The text content to check
            
        Returns:
            bool: True if Hebrew, False otherwise
        """
        return self.detect_language(text) == 'he'
    
    def is_arabic(self, text: str) -> bool:
        """
        Checks if text is Arabic.
        
        Args:
            text: The text content to check
            
        Returns:
            bool: True if Arabic, False otherwise
        """
        return self.detect_language(text) == 'ar'
