"""
Test script for the scheduler - runs once without scheduling.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main_pipeline_service import MainPipelineService


def test_single_run():
    """
    Test a single pipeline run without scheduling.
    """
    print("=" * 80)
    print("Testing Pipeline - Single Run")
    print("=" * 80)
    
    try:
        pipeline = MainPipelineService()
        
        print("\nRunning full pipeline (batch size: 10)...")
        stats = pipeline.run_full_pipeline(batch_size=10)
        
        print("\n" + "=" * 80)
        print("TEST COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print(f"\nExecution time: {stats['execution_time_seconds']:.2f} seconds")
        print(f"\nTranslation Stats:")
        print(f"  - Succeeded: {stats['translation'].get('succeeded', 0)}")
        print(f"  - Failed: {stats['translation'].get('failed', 0)}")
        
        print(f"\nClustering Stats:")
        print(f"  - Clusters created: {stats['clustering'].get('clusters_created', 0)}")
        print(f"  - Standalone clusters: {stats['clustering'].get('standalone_clusters', 0)}")
        
        print(f"\nReport Generation Stats:")
        print(f"  - Reports generated: {stats['report_generation'].get('reports_generated', 0)}")
        print(f"  - News processed: {stats['report_generation'].get('news_marked_processed', 0)}")
        
        print("\n" + "=" * 80)
        print("✅ Pipeline is ready for scheduling!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_single_run()
