import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_services.news_report_generation_pipeline_service import NewsReportGenerationPipelineService


def test_report_generation_pipeline():
    """
    Tests the complete report generation pipeline.
    """
    print("=" * 80)
    print("Testing Report Generation Pipeline")
    print("=" * 80)
    
    try:
        # Initialize pipeline
        pipeline = NewsReportGenerationPipelineService()
        
        # Run report generation
        print("\nRunning report generation pipeline...")
        stats = pipeline.process_report_generation()
        
        print("\n" + "=" * 80)
        print("REPORT GENERATION RESULTS")
        print("=" * 80)
        print(f"Clusters processed: {stats['clusters_processed']}")
        print(f"Reports generated: {stats['reports_generated']}")
        print(f"News marked as processed: {stats['news_marked_processed']}")
        print("=" * 80)
        
        if stats['reports_generated'] > 0:
            print("\n✅ Report generation pipeline completed successfully!")
        else:
            print("\n⚠️ No reports were generated (no clusters found or all failed)")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_report_generation_pipeline()
