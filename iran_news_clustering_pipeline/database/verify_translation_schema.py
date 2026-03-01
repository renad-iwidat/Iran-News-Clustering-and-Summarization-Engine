import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database_connection_config import DatabaseConnectionConfig
from database.postgresql_connection_manager import PostgreSQLConnectionManager


def verify_raw_data_translation_columns():
    """
    Verifies that translation columns were added to raw_data table.
    """
    print("=" * 60)
    print("Verifying raw_data Translation Columns")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    connection = None
    try:
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT column_name, data_type, column_default, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'raw_data'
            AND column_name IN (
                'original_language', 
                'arabic_content', 
                'translation_status', 
                'translated_at',
                'translation_error_message'
            )
            ORDER BY column_name;
        """)
        
        columns = cursor.fetchall()
        
        if columns:
            print(f"\nFound {len(columns)} translation-related columns:")
            print("-" * 60)
            for col in columns:
                print(f"Column: {col[0]}")
                print(f"  Type: {col[1]}")
                print(f"  Default: {col[2]}")
                print(f"  Nullable: {col[3]}")
                print("-" * 60)
        else:
            print("\nWARNING: No translation columns found!")
            print("Please run the migration script first.")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if connection:
            connection.close()
    
    print()


def verify_raw_data_indexes():
    """
    Verifies that indexes were created for translation columns.
    """
    print("=" * 60)
    print("Verifying raw_data Indexes")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    connection = None
    try:
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'raw_data'
            AND indexname LIKE '%translation%'
            ORDER BY indexname;
        """)
        
        indexes = cursor.fetchall()
        
        if indexes:
            print(f"\nFound {len(indexes)} translation-related indexes:")
            print("-" * 60)
            for idx in indexes:
                print(f"Index: {idx[0]}")
                print(f"Definition: {idx[1]}")
                print("-" * 60)
        else:
            print("\nWARNING: No translation indexes found!")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if connection:
            connection.close()
    
    print()


def verify_content_type_data():
    """
    Verifies that content_type table has the required types.
    """
    print("=" * 60)
    print("Verifying content_type Table Data")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    connection = None
    try:
        connection = connection_manager.get_connection_without_pool()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id, name FROM content_type ORDER BY id;")
        content_types = cursor.fetchall()
        
        expected_types = ['short_news', 'medium_news', 'long_news', 'explanation', 'analysis']
        
        if content_types:
            print(f"\nFound {len(content_types)} content types:")
            print("-" * 60)
            for ct in content_types:
                status = "✓" if ct[1] in expected_types else "?"
                print(f"{status} ID: {ct[0]}, Name: {ct[1]}")
            print("-" * 60)
            
            found_names = [ct[1] for ct in content_types]
            missing_types = [t for t in expected_types if t not in found_names]
            
            if missing_types:
                print(f"\nWARNING: Missing content types: {', '.join(missing_types)}")
            else:
                print("\nSUCCESS: All expected content types are present")
        else:
            print("\nWARNING: content_type table is empty!")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if connection:
            connection.close()
    
    print()


def verify_complete_schema():
    """
    Runs all verification checks.
    """
    print("\n")
    print("*" * 60)
    print("DATABASE SCHEMA VERIFICATION")
    print("*" * 60)
    print("\n")
    
    verify_raw_data_translation_columns()
    verify_raw_data_indexes()
    verify_content_type_data()
    
    print("*" * 60)
    print("VERIFICATION COMPLETED")
    print("*" * 60)
    print("\n")


if __name__ == "__main__":
    verify_complete_schema()
