import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database_connection_config import DatabaseConnectionConfig
from database.postgresql_connection_manager import PostgreSQLConnectionManager


class DatabaseMigrationRunner:
    """
    Runs SQL migration scripts against the database.
    Executes migration files in order to update database schema.
    """
    
    def __init__(self, connection_manager: PostgreSQLConnectionManager):
        self.connection_manager = connection_manager
        self.migrations_directory = Path(__file__).parent / "migrations"
    
    def get_all_migration_files(self):
        """
        Gets all SQL migration files sorted by filename.
        
        Returns:
            List of Path objects for migration files
        """
        if not self.migrations_directory.exists():
            print(f"Migrations directory not found: {self.migrations_directory}")
            return []
        
        migration_files = sorted(self.migrations_directory.glob("*.sql"))
        return migration_files
    
    def run_migration_file(self, migration_file_path: Path):
        """
        Executes a single migration file.
        
        Args:
            migration_file_path: Path to the SQL migration file
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\nRunning migration: {migration_file_path.name}")
        print("-" * 60)
        
        connection = None
        try:
            with open(migration_file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            connection = self.connection_manager.get_connection_without_pool()
            cursor = connection.cursor()
            
            cursor.execute(sql_content)
            connection.commit()
            
            cursor.close()
            
            print(f"SUCCESS: {migration_file_path.name} executed successfully")
            return True
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"ERROR: Failed to execute {migration_file_path.name}")
            print(f"Error message: {str(e)}")
            return False
            
        finally:
            if connection:
                connection.close()
    
    def run_all_migrations(self):
        """
        Runs all migration files in the migrations directory.
        """
        print("\n")
        print("=" * 60)
        print("DATABASE MIGRATION RUNNER")
        print("=" * 60)
        
        migration_files = self.get_all_migration_files()
        
        if not migration_files:
            print("\nNo migration files found.")
            return
        
        print(f"\nFound {len(migration_files)} migration file(s)")
        print("=" * 60)
        
        successful_migrations = 0
        failed_migrations = 0
        
        for migration_file in migration_files:
            success = self.run_migration_file(migration_file)
            if success:
                successful_migrations += 1
            else:
                failed_migrations += 1
        
        print("\n")
        print("=" * 60)
        print("MIGRATION SUMMARY")
        print("=" * 60)
        print(f"Total migrations: {len(migration_files)}")
        print(f"Successful: {successful_migrations}")
        print(f"Failed: {failed_migrations}")
        print("=" * 60)
        print("\n")


def run_database_migrations():
    """
    Main function to run all database migrations.
    """
    config = DatabaseConnectionConfig()
    connection_manager = PostgreSQLConnectionManager(config)
    
    migration_runner = DatabaseMigrationRunner(connection_manager)
    migration_runner.run_all_migrations()


if __name__ == "__main__":
    run_database_migrations()
