import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import Optional
import logging

from config.database_connection_config import DatabaseConnectionConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgreSQLConnectionManager:
    """
    Manages PostgreSQL database connections with connection pooling.
    Handles connection creation, testing, and resource cleanup.
    """
    
    def __init__(self, config: DatabaseConnectionConfig):
        """
        Initialize the connection manager with database configuration.
        
        Args:
            config: DatabaseConnectionConfig instance with connection details
        """
        self.config = config
        self.connection_pool: Optional[pool.SimpleConnectionPool] = None
        
    def create_connection_pool(self, min_connections: int = 1, max_connections: int = 10):
        """
        Creates a connection pool for efficient database connection management.
        
        Args:
            min_connections: Minimum number of connections to maintain
            max_connections: Maximum number of connections allowed
        """
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                min_connections,
                max_connections,
                **self.config.get_connection_dict()
            )
            logger.info("Connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create connection pool: {str(e)}")
            raise
    
    def get_connection(self):
        """
        Gets a connection from the pool.
        
        Returns:
            psycopg2 connection object
        """
        if self.connection_pool is None:
            raise Exception("Connection pool not initialized. Call create_connection_pool first.")
        return self.connection_pool.getconn()
    
    def return_connection(self, connection):
        """
        Returns a connection back to the pool.
        
        Args:
            connection: psycopg2 connection object to return
        """
        if self.connection_pool:
            self.connection_pool.putconn(connection)
    
    def close_all_connections(self):
        """
        Closes all connections in the pool.
        """
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("All connections closed")
    
    def get_connection_without_pool(self):
        """
        Gets a direct connection without using the pool.
        Useful for one-time operations or testing.
        
        Returns:
            psycopg2 connection object
        """
        return psycopg2.connect(**self.config.get_connection_dict())
    
    def test_database_connection(self) -> bool:
        """
        Tests the database connection and returns connection status.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        connection = None
        try:
            logger.info("Testing database connection...")
            connection = psycopg2.connect(**self.config.get_connection_dict())
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                db_version = cursor.fetchone()
                logger.info(f"Successfully connected to PostgreSQL")
                logger.info(f"Database version: {db_version[0]}")
                
                cursor.execute("SELECT current_database();")
                current_db = cursor.fetchone()
                logger.info(f"Connected to database: {current_db[0]}")
                
            return True
            
        except psycopg2.OperationalError as e:
            logger.error(f"Operational error during connection: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {str(e)}")
            return False
        finally:
            if connection:
                connection.close()
                logger.info("Test connection closed")
