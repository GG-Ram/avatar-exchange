"""MongoDB User model and database operations"""

from bson import ObjectId
from typing import Optional, Dict, List, Any
from database import db
import bcrypt
from datetime import datetime

class UserModel:
    """MongoDB User model with database operations"""
    
    @staticmethod
    def create_user(username: str, email: str, password: str, balance: float = 500.0) -> Dict[str, Any]:
        """Create a new user in MongoDB"""
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_doc = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "balance": balance,
            "positions": [],  # List of stock positions
            "inventory": [],  # List of purchased items
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db.users.insert_one(user_doc)
        user_doc["_id"] = str(result.inserted_id)
        # Don't return password
        user_doc.pop("password", None)
        return user_doc
    
    @staticmethod
    def find_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Find user by MongoDB _id"""
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
                return user
            return None
        except Exception:
            return None
    
    @staticmethod
    def find_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Find user by username"""
        user = db.users.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None
    
    @staticmethod
    def find_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        user = db.users.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None
    
    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        """Verify a password against a hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def update_user(user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user document"""
        try:
            updates["updated_at"] = datetime.utcnow()
            # Convert string _id back to ObjectId
            result = db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    @staticmethod
    def update_balance(user_id: str, new_balance: float) -> bool:
        """Update user balance"""
        return UserModel.update_user(user_id, {"balance": round(new_balance, 2)})
    
    @staticmethod
    def add_position(user_id: str, position: Dict[str, Any]) -> bool:
        """Add or update a stock position"""
        try:
            # Check if position already exists
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return False
            
            positions = user.get("positions", [])
            # Find existing position with same symbol
            existing_index = None
            for i, pos in enumerate(positions):
                if pos.get("symbol") == position.get("symbol"):
                    existing_index = i
                    break
            
            if existing_index is not None:
                # Update existing position
                existing = positions[existing_index]
                total_shares = existing["shares"] + position["shares"]
                # Calculate weighted average buy price
                existing["buyPrice"] = (
                    (existing["buyPrice"] * existing["shares"] + position["buyPrice"] * position["shares"])
                    / total_shares
                )
                existing["shares"] = total_shares
                positions[existing_index] = existing
            else:
                # Add new position
                positions.append(position)
            
            return UserModel.update_user(user_id, {"positions": positions})
        except Exception as e:
            print(f"Error adding position: {e}")
            return False
    
    @staticmethod
    def update_position(user_id: str, symbol: str, shares: int, buy_price: float = None) -> bool:
        """Update a stock position (for selling, shares should be negative or reduced)"""
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return False
            
            positions = user.get("positions", [])
            for i, pos in enumerate(positions):
                if pos.get("symbol") == symbol:
                    if buy_price is not None:
                        pos["buyPrice"] = buy_price
                    pos["shares"] = shares
                    if shares <= 0:
                        positions.pop(i)
                    else:
                        positions[i] = pos
                    return UserModel.update_user(user_id, {"positions": positions})
            return False
        except Exception as e:
            print(f"Error updating position: {e}")
            return False
    
    @staticmethod
    def add_to_inventory(user_id: str, item: Dict[str, Any]) -> bool:
        """Add item to user inventory"""
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return False
            
            inventory = user.get("inventory", [])
            inventory.append(item)
            return UserModel.update_user(user_id, {"inventory": inventory})
        except Exception as e:
            print(f"Error adding to inventory: {e}")
            return False
    
    @staticmethod
    def get_user_data(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data in the format expected by the frontend"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return None
        
        # Format positions for frontend
        positions = []
        for pos in user.get("positions", []):
            positions.append({
                "shares": pos.get("shares", 0),
                "symbol": pos.get("symbol", ""),
                "name": pos.get("name", ""),
                "buyPrice": pos.get("buyPrice", 0),
                # Note: price and other calculated fields will be added by the User class
            })
        
        return {
            "_id": user.get("_id"),
            "balance": user.get("balance", 500),
            "positions": positions,
            "inventory": user.get("inventory", [])
        }

