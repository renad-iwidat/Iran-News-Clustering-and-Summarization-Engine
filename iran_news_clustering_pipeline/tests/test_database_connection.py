import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database_connection_config import DatabaseConnectionConfig
from database.postgresql_connection_manager import PostgreSQLConnectionManager


def test_connection_configuration():
    """
    Test 1: Verify that configuration is loaded correctly.
    """
    print("=" * 60)
    print("Test 1: Testing Configuration Loading")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    
    print(f"Database Name: {config.database_name}")
    print(f"Host: {config.host}")
    print(f"Username: {config.username}")
    print(f"Port: {config.port}")
    print(f"Connection String: {config.get_connection_string()}")
    print()


def test_database_connection():
    """
    Test 2: Test actual database connection.
    """
    print("=" * 60)
    print("Test 2: Testing Database Connection")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    is_connected = connection_manager.test_database_connection()
    
    if is_connected:
        print("\nConnection Status: SUCCESS")
        print("Database is reachable and ready for operations")
    else:
        print("\nConnection Status: FAILED")
        print("Please check your credentials and network connection")
    
    print()
    return is_connected


def test_connection_pool():
    """
    Test 3: Test connection pool creation and usage.
    """
    print("=" * 60)
    print("Test 3: Testing Connection Pool")
    print("=" * 60)
    
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    try:
        connection_manager.create_connection_pool(min_connections=1, max_connections=5)
        print("Connection pool created successfully")
        
        connection = connection_manager.get_connection()
        print("Connection retrieved from pool")
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test_value;")
        result = cursor.fetchone()
        print(f"Test query result: {result[0]}")
        cursor.close()
        
        connection_manager.return_connection(connection)
        print("Connection returned to pool")
        
        connection_manager.close_all_connections()
        print("All connections closed")
        
        print("\nConnection Pool Status: SUCCESS")
        return True
        
    except Exception as e:
        print(f"\nConnection Pool Status: FAILED")
        print(f"Error: {str(e)}")
        return False
    finally:
        print()


def run_all_tests():
    """
    Runs all database connection tests.
    """
    print("\n")
    print("*" * 60)
    print("IRAN NEWS PIPELINE - DATABASE CONNECTION TESTS")
    print("*" * 60)
    print("\n")
    
    test_connection_configuration()
    
    connection_success = test_database_connection()
    
    if connection_success:
        test_connection_pool()
    else:
        print("Skipping connection pool test due to connection failure")
    
    print("*" * 60)
    print("ALL TESTS COMPLETED")
    print("*" * 60)
    print("\n")


if __name__ == "__main__":
    run_all_tests()
