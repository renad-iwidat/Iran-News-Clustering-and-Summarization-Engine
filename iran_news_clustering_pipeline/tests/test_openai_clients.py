import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.openai_api_keys_config import OpenAIAPIKeysConfig
from llm_services.openai_client_manager import OpenAIClientManager


def test_api_keys_configuration():
    """
    Test 1: Verify that API keys are loaded correctly from .env file.
    """
    print("=" * 60)
    print("Test 1: Testing API Keys Configuration")
    print("=" * 60)
    
    config = OpenAIAPIKeysConfig()
    
    print(f"\nTranslation Model: {config.translation_model}")
    print(f"Clustering Model: {config.clustering_model}")
    print(f"Report Generation Model: {config.report_generation_model}")
    
    print(f"\nTranslation API Key: {'*' * 20}{config.translation_api_key[-10:] if config.translation_api_key else 'NOT SET'}")
    print(f"Clustering API Key: {'*' * 20}{config.clustering_api_key[-10:] if config.clustering_api_key else 'NOT SET'}")
    print(f"Report Generation API Key: {'*' * 20}{config.report_generation_api_key[-10:] if config.report_generation_api_key else 'NOT SET'}")
    
    validation = config.validate_keys()
    print(f"\nValidation Results:")
    for key_name, is_valid in validation.items():
        status = "✓ VALID" if is_valid else "✗ MISSING"
        print(f"  {key_name}: {status}")
    
    print()


def test_openai_client_initialization():
    """
    Test 2: Test OpenAI client initialization.
    """
    print("=" * 60)
    print("Test 2: Testing OpenAI Client Initialization")
    print("=" * 60)
    
    config = OpenAIAPIKeysConfig()
    
    try:
        client_manager = OpenAIClientManager(config)
        print("\n✓ OpenAI Client Manager initialized successfully")
        
        print("\nClient Status:")
        print(f"  Translation Client: {'✓ Ready' if client_manager.translation_client else '✗ Not Ready'}")
        print(f"  Clustering Client: {'✓ Ready' if client_manager.clustering_client else '✗ Not Ready'}")
        print(f"  Report Generation Client: {'✓ Ready' if client_manager.report_generation_client else '✗ Not Ready'}")
        
        return client_manager
        
    except Exception as e:
        print(f"\n✗ Failed to initialize OpenAI Client Manager")
        print(f"Error: {str(e)}")
        return None
    finally:
        print()


def test_openai_api_connections(client_manager: OpenAIClientManager):
    """
    Test 3: Test actual API connections with OpenAI.
    """
    if not client_manager:
        print("Skipping API connection tests due to initialization failure")
        return
    
    print("=" * 60)
    print("Test 3: Testing OpenAI API Connections")
    print("=" * 60)
    print("\nThis will make actual API calls to OpenAI...")
    print()
    
    results = client_manager.test_all_clients()
    
    print("\n" + "=" * 60)
    print("API Connection Test Results")
    print("=" * 60)
    
    for service, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{service.capitalize()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All OpenAI clients are working correctly!")
    else:
        print("\n✗ Some clients failed. Please check your API keys and credits.")
    
    print()


def run_all_tests():
    """
    Runs all OpenAI client tests.
    """
    print("\n")
    print("*" * 60)
    print("OPENAI CLIENT TESTS - IRAN NEWS PIPELINE")
    print("*" * 60)
    print("\n")
    
    test_api_keys_configuration()
    
    client_manager = test_openai_client_initialization()
    
    if client_manager:
        test_openai_api_connections(client_manager)
    
    print("*" * 60)
    print("ALL TESTS COMPLETED")
    print("*" * 60)
    print("\n")


if __name__ == "__main__":
    run_all_tests()
