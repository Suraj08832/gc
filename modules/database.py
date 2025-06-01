from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# Load environment variables
load_dotenv()
MONGODB_URI = os.getenv('MONGO_DB_URI', 'mongodb://localhost:27017/')

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client['telegram_bot']
            
            # Collections
            self.users = self.db['users']
            self.chats = self.db['chats']
            self.warnings = self.db['warnings']
            self.mutes = self.db['mutes']
            self.settings = self.db['settings']
            self.sticker_approvals = self.db['sticker_approvals']
            
            # Create indexes
            self._create_indexes()
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        # Create indexes for faster queries
        self.users.create_index('user_id', unique=True)
        self.chats.create_index('chat_id', unique=True)
        self.warnings.create_index([('user_id', 1), ('chat_id', 1)])
        self.mutes.create_index([('user_id', 1), ('chat_id', 1)])
        self.settings.create_index('chat_id', unique=True)
        self.sticker_approvals.create_index([('chat_id', 1), ('sticker_id', 1)], unique=True)
    
    # Sticker approval operations
    def add_sticker_approval(self, chat_id: int, sticker_id: str, approved_by: int):
        self.sticker_approvals.update_one(
            {'chat_id': chat_id, 'sticker_id': sticker_id},
            {
                '$set': {
                    'approved_by': approved_by,
                    'approved_at': self.get_current_timestamp()
                }
            },
            upsert=True
        )
    
    def is_sticker_approved(self, chat_id: int, sticker_id: str) -> bool:
        """Check if a sticker is approved in a chat"""
        try:
            result = self.sticker_approvals.find_one({
                'chat_id': chat_id,
                'sticker_id': sticker_id,
                'approved': True
            })
            return bool(result)
        except Exception as e:
            logger.error(f"Error checking sticker approval: {e}")
            return False
    
    def approve_sticker(self, chat_id: int, sticker_id: str) -> bool:
        """Approve a sticker in a chat"""
        try:
            self.sticker_approvals.update_one(
                {
                    'chat_id': chat_id,
                    'sticker_id': sticker_id
                },
                {
                    '$set': {
                        'approved': True,
                        'approved_at': datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error approving sticker: {e}")
            return False
    
    def remove_sticker_approval(self, chat_id: int, sticker_id: str):
        self.sticker_approvals.delete_one({
            'chat_id': chat_id,
            'sticker_id': sticker_id
        })
    
    # User operations
    def add_user(self, user_id: int, username: str = None, first_name: str = None):
        self.users.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'username': username,
                    'first_name': first_name,
                    'is_banned': False
                }
            },
            upsert=True
        )
    
    def get_user(self, user_id: int):
        return self.users.find_one({'user_id': user_id})
    
    # Chat operations
    def add_chat(self, chat_id: int, title: str = None):
        self.chats.update_one(
            {'chat_id': chat_id},
            {
                '$set': {
                    'title': title,
                    'welcome_enabled': True,
                    'copyright_protection': True
                }
            },
            upsert=True
        )
    
    def get_chat(self, chat_id: int):
        return self.chats.find_one({'chat_id': chat_id})
    
    # Warning operations
    def add_warning(self, user_id: int, chat_id: int, reason: str):
        warning = {
            'user_id': user_id,
            'chat_id': chat_id,
            'reason': reason,
            'timestamp': self.get_current_timestamp()
        }
        self.warnings.insert_one(warning)
        return self.get_warning_count(user_id, chat_id)
    
    def get_warning_count(self, user_id: int, chat_id: int):
        return self.warnings.count_documents({
            'user_id': user_id,
            'chat_id': chat_id
        })
    
    def reset_warnings(self, user_id: int, chat_id: int):
        self.warnings.delete_many({
            'user_id': user_id,
            'chat_id': chat_id
        })
    
    # Mute operations
    def add_mute(self, user_id: int, chat_id: int, duration: int, reason: str):
        mute = {
            'user_id': user_id,
            'chat_id': chat_id,
            'duration': duration,
            'reason': reason,
            'timestamp': self.get_current_timestamp(),
            'expires_at': self.get_current_timestamp() + duration * 3600
        }
        self.mutes.insert_one(mute)
    
    def get_mute(self, user_id: int, chat_id: int):
        return self.mutes.find_one({
            'user_id': user_id,
            'chat_id': chat_id,
            'expires_at': {'$gt': self.get_current_timestamp()}
        })
    
    def remove_mute(self, user_id: int, chat_id: int):
        self.mutes.delete_many({
            'user_id': user_id,
            'chat_id': chat_id
        })
    
    # Settings operations
    def update_chat_settings(self, chat_id: int, settings: dict):
        self.settings.update_one(
            {'chat_id': chat_id},
            {'$set': settings},
            upsert=True
        )
    
    def get_chat_settings(self, chat_id: int):
        return self.settings.find_one({'chat_id': chat_id})
    
    @staticmethod
    def get_current_timestamp():
        return datetime.utcnow().timestamp()

# Create a global database instance
db = Database()