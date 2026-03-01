import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.news_translation_pipeline_service import NewsTranslationPipelineService


def test_translation_pipeline():
    """
    Tests the complete translation pipeline on sample data.
    """
    print("\n")
    print("=" * 60)
    print("TRANSLATION PIPELINE TEST")
    print("=" * 60)
    print("\n")
    
    # Initialize the translation service
    print("Initializing translation service...")
    translation_service = NewsTranslationPipelineService()
    
    # Get initial statistics
    print("\n" + "-" * 60)
    print("Initial Statistics:")
    print("-" * 60)
    initial_stats = translation_service.get_statistics()
    for key, value in initial_stats.items():
        print(f"  {key}: {value}")
    
    # Process a batch of news articles
    print("\n" + "-" * 60)
    print("Processing News Articles...")
    print("-" * 60)
    
    batch_stats = translation_service.process_batch(batch_size=20)
    
    print("\n" + "-" * 60)
    print("Batch Processing Results:")
    print("-" * 60)
    for key, value in batch_stats.items():
        print(f"  {key}: {value}")
    
    # Get final statistics
    print("\n" + "-" * 60)
    print("Final Statistics:")
    print("-" * 60)
    final_stats = translation_service.get_statistics()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TRANSLATION TEST COMPLETED")
    print("=" * 60)
    
    if batch_stats['succeeded'] > 0:
        print("\nSUCCESS: Translation pipeline is working!")
        print(f"  - Translated {batch_stats['succeeded']} articles")
        if batch_stats['failed'] > 0:
            print(f"  - Failed: {batch_stats['failed']} articles")
    else:
        print("\nWARNING: No articles were successfully translated")
    
    print("\n")


if __name__ == "__main__":
    test_translation_pipeline()
