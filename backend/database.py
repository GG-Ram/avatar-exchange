"""MongoDB database connection and configuration"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    """Singleton database connection manager"""
    
    _instance: Optional['Database'] = None
    _client: Optional[MongoClient] = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Establish connection to MongoDB"""
        # Get MongoDB URI from environment variable or use default
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb+srv://rf9301793_db_user:ayU2smZsBUQdWhtH@avatar-exchange.tqjbhzt.mongodb.net/')
        database_name = os.getenv('MONGODB_DB_NAME', 'avatar_exchange')
        
        try:
            self._client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self._client.admin.command('ping')
            self._db = self._client[database_name]
            print(f"Successfully connected to MongoDB database: {database_name}")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    @property
    def db(self):
        """Get the database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    @property
    def users(self):
        """Get users collection"""
        return self.db.users
    
    @property
    def stocks(self):
        """Get stocks collection (for caching stock data if needed)"""
        return self.db.stocks
    
    def close(self):
        """Close the database connection"""
        if self._client:
            self._client.close()
            print("MongoDB connection closed")

# Global database instance
db = Database()

