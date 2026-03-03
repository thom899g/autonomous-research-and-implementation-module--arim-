"""
ARIM State Manager
Firebase-based state management for ARIM system with atomic operations and recovery
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from typing import Dict, Any, Optional, List, Union
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, is_dataclass
import hashlib
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Initialize Firebase
def initialize_firebase():
    """Initialize Firebase app with error handling"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            from arim_config import FIREBASE_CONFIG
            cred_dict = {k: v for k, v in FIREBASE_CONFIG.items() if v}
            
            if not cred_dict.get("private_key