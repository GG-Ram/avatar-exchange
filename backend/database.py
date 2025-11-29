"""MongoDB database connection and configuration"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
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
    _connected = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Don't connect immediately - make it lazy
        pass
    
    def connect(self):
        """Establish connection to MongoDB"""
        if self._connected and self._client is not None:
            return
        
        # Get MongoDB URI from environment variable or use default
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb+srv://rf9301793_db_user:ayU2smZsBUQdWhtH@avatar-exchange.tqjbhzt.mongodb.net/')
        database_name = os.getenv('MONGODB_DB_NAME', 'avatar_exchange')
        
        try:
            self._client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self._client.admin.command('ping')
            self._db = self._client[database_name]
            self._connected = True
            print(f"Successfully connected to MongoDB database: {database_name}")
        except (ConnectionFailure, OperationFailure) as e:
            print(f"Failed to connect to MongoDB: {e}")
            print(f"   Please check your MONGODB_URI in .env file")
            self._client = None
            self._db = None
            self._connected = False
            raise
        except Exception as e:
            print(f"Unexpected error connecting to MongoDB: {e}")
            self._client = None
            self._db = None
            self._connected = False
            raise
    
    @property
    def db(self):
        """Get the database instance"""
        if self._db is None or not self._connected:
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
            self._connected = False
            print("MongoDB connection closed")

# Global database instance (lazy connection - won't connect until first use)
db = Database()

