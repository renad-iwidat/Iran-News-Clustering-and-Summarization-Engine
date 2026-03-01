import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConnectionConfig:
    """
    Configuration class for PostgreSQL database connection on Render.
    Loads credentials from environment variables for security.
    """
    database_name: str = os.getenv("DATABASE_NAME", "iran_news_pipeline")
    host: str = os.getenv("DATABASE_HOST", "dpg-d6hl9v7gi27c73ftat10-a.oregon-postgres.render.com")
    username: str = os.getenv("DATABASE_USERNAME", "iran_news_pipeline_user")
    password: str = os.getenv("DATABASE_PASSWORD", "")
    port: int = int(os.getenv("DATABASE_PORT", "5432"))
    
    def get_connection_string(self) -> str:
        """
        Returns the PostgreSQL connection string for SQLAlchemy.
        
        Returns:
            str: Database connection URL
        """
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"
    
    def get_connection_dict(self) -> dict:
        """
        Returns connection parameters as a dictionary for psycopg2.
        
        Returns:
            dict: Connection parameters
        """
        return {
            "dbname": self.database_name,
            "user": self.username,
            "password": self.password,
            "host": self.host,
            "port": self.port
        }
