import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database_connection_config import DatabaseConnectionConfig
from database.postgresql_connection_manager import PostgreSQLConnectionManager


def inspect_content_type_table():
    """
    Inspects the content_type table to see what types are defined.
    """
    print("=" * 60)
    print("Inspecting content_type Table")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    connection = None
    try:
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id, name FROM content_type ORDER BY id;")
        rows = cursor.fetchall()
        
        if rows:
            print(f"\nFound {len(rows)} content types:")
            print("-" * 60)
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}")
        else:
            print("\nNo content types found. Table is empty.")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if connection:
            connection.close()
    
    print("=" * 60)
    print()


def inspect_output_content_table():
    """
    Inspects the output_content table to see if there's any data.
    """
    print("=" * 60)
    print("Inspecting output_content Table")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    connection = None
    try:
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM output_content;")
        count = cursor.fetchone()[0]
        
        print(f"\nTotal records in output_content: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT oc.id, oc.cluster_id, ct.name as content_type, 
                       LEFT(oc.content, 100) as content_preview
                FROM output_content oc
                LEFT JOIN content_type ct ON oc.content_type_id = ct.id
                LIMIT 5;
            """)
            rows = cursor.fetchall()
            
            print("\nSample records:")
            print("-" * 60)
            for row in rows:
                print(f"ID: {row[0]}, Cluster: {row[1]}, Type: {row[2]}")
                print(f"Preview: {row[3]}...")
                print("-" * 60)
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if connection:
            connection.close()
    
    print("=" * 60)
    print()


def inspect_raw_data_sample():
    """
    Inspects raw_data table to understand the data structure.
    """
    print("=" * 60)
    print("Inspecting raw_data Table")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    connection = None
    try:
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM raw_data;")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM raw_data WHERE is_processed = false;")
        unprocessed_count = cursor.fetchone()[0]
        
        print(f"\nTotal news articles: {total_count}")
        print(f"Unprocessed articles: {unprocessed_count}")
        print(f"Processed articles: {total_count - unprocessed_count}")
        
        cursor.execute("""
            SELECT id, LEFT(content, 100) as content_preview, 
                   published_at, is_processed
            FROM raw_data
            LIMIT 3;
        """)
        rows = cursor.fetchall()
        
        if rows:
            print("\nSample records:")
            print("-" * 60)
            for row in rows:
                print(f"ID: {row[0]}")
                print(f"Content: {row[1]}...")
                print(f"Published: {row[2]}")
                print(f"Processed: {row[3]}")
                print("-" * 60)
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if connection:
            connection.close()
    
    print("=" * 60)
    print()


if __name__ == "__main__":
    print("\n")
    print("*" * 60)
    print("DATABASE SCHEMA INSPECTION")
    print("*" * 60)
    print("\n")
    
    inspect_content_type_table()
    inspect_output_content_table()
    inspect_raw_data_sample()
    
    print("*" * 60)
    print("INSPECTION COMPLETED")
    print("*" * 60)
    print("\n")
