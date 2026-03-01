import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database_connection_config import DatabaseConnectionConfig
from database.postgresql_connection_manager import PostgreSQLConnectionManager


def insert_sample_data():
    """
    Inserts sample data into the database for testing purposes.
    """
    print("\n")
    print("=" * 60)
    print("INSERTING SAMPLE DATA")
    print("=" * 60)
    print("\n")
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    sample_data_file = Path(__file__).parent / "sample_data" / "insert_sample_data.sql"
    
    if not sample_data_file.exists():
        print(f"ERROR: Sample data file not found: {sample_data_file}")
        return False
    
    connection = None
    try:
        print(f"Reading sample data from: {sample_data_file.name}")
        with open(sample_data_file, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        print("Connecting to database...")
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        print("Executing SQL statements...")
        cursor.execute(sql_content)
        connection.commit()
        
        print("\n" + "=" * 60)
        print("SAMPLE DATA INSERTED SUCCESSFULLY")
        print("=" * 60)
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM raw_data;")
        total_news = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sources;")
        total_sources = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM source_type;")
        total_source_types = cursor.fetchone()[0]
        
        print(f"\nStatistics:")
        print(f"  Source Types: {total_source_types}")
        print(f"  Sources: {total_sources}")
        print(f"  News Articles: {total_news}")
        
        # Show sample of inserted data
        cursor.execute("""
            SELECT rd.id, s.url, LEFT(rd.content, 50) as preview, rd.published_at
            FROM raw_data rd
            JOIN sources s ON rd.source_id = s.id
            ORDER BY rd.published_at DESC
            LIMIT 5;
        """)
        
        samples = cursor.fetchall()
        
        print(f"\nSample of inserted news (latest 5):")
        print("-" * 60)
        for sample in samples:
            print(f"ID: {sample[0]}")
            print(f"Source: {sample[1]}")
            print(f"Preview: {sample[2]}...")
            print(f"Published: {sample[3]}")
            print("-" * 60)
        
        cursor.close()
        
        print("\n" + "=" * 60)
        print("READY FOR TESTING")
        print("=" * 60)
        print("\n")
        
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"\nERROR: Failed to insert sample data")
        print(f"Error message: {str(e)}")
        return False
        
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    success = insert_sample_data()
    if not success:
        sys.exit(1)
