import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.news_clustering_pipeline_service import NewsClusteringPipelineService


def test_clustering_pipeline():
    """
    Tests the complete clustering pipeline on translated news.
    """
    print("\n")
    print("=" * 60)
    print("CLUSTERING PIPELINE TEST")
    print("=" * 60)
    print("\n")
    
    # Initialize the clustering service
    print("Initializing clustering service...")
    clustering_service = NewsClusteringPipelineService()
    
    # Get initial statistics
    print("\n" + "-" * 60)
    print("Initial Statistics:")
    print("-" * 60)
    initial_stats = clustering_service.get_statistics()
    for key, value in initial_stats.items():
        print(f"  {key}: {value}")
    
    # Process clustering
    print("\n" + "-" * 60)
    print("Processing Clustering...")
    print("-" * 60)
    
    batch_stats = clustering_service.process_clustering(batch_size=20)
    
    print("\n" + "-" * 60)
    print("Clustering Results:")
    print("-" * 60)
    for key, value in batch_stats.items():
        print(f"  {key}: {value}")
    
    # Get final statistics
    print("\n" + "-" * 60)
    print("Final Statistics:")
    print("-" * 60)
    final_stats = clustering_service.get_statistics()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    # Summary
    print("\n" + "=" * 60)
    print("CLUSTERING TEST COMPLETED")
    print("=" * 60)
    
    if batch_stats['clusters_created'] > 0:
        print("\nSUCCESS: Clustering pipeline is working!")
        print(f"  - Created {batch_stats['clusters_created']} clusters")
        print(f"  - Processed {batch_stats['processed']} articles")
    else:
        print("\nWARNING: No clusters were created")
    
    print("\n")


if __name__ == "__main__":
    test_clustering_pipeline()
