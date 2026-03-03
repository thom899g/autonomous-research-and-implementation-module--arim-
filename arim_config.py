"""
ARIM Configuration Module
Centralized configuration management for the Autonomous Research and Implementation Module
"""
import os
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Firebase configuration
FIREBASE_CONFIG = {
    "type": os.getenv("FIREBASE_TYPE", "service_account"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
}

@dataclass
class ARIMConfig:
    """Configuration dataclass for ARIM system"""
    
    # Monitoring settings
    monitoring_interval: int = 300  # 5 minutes
    performance_threshold: float = 0.8  # 80% performance threshold
    error_rate_threshold: float = 0.05  # 5% error rate threshold
    
    # Research settings
    max_research_time: int = 3600  # 1 hour max research time
    min_data_points: int = 100  # Minimum data points for analysis
    confidence_threshold: float = 0.85  # 85% confidence threshold
    
    # Implementation settings
    dry_run: bool = True  # Test mode - set to False for production
    rollback_enabled: bool = True  # Automatic rollback on failure
    max_implementation_time: int = 7200  # 2 hours max
    
    # Firebase settings
    firebase_collection: str = "arim_state"
    firebase_backup_collection: str = "arim_backup"
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str = "arim_system.log"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ARIMConfig":
        """Create config from dictionary"""
        return cls(**data)

def load_config(config_path: Optional[str] = None) -> ARIMConfig:
    """
    Load configuration from file or environment
    
    Args:
        config_path: Optional path to JSON config file
        
    Returns:
        ARIMConfig instance
    """
    try:
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return ARIMConfig.from_dict(config_data)
        
        # Load from environment variables
        return ARIMConfig(
            monitoring_interval=int(os.getenv("ARIM_MONITORING_INTERVAL", "300")),
            performance_threshold=float(os.getenv("ARIM_PERFORMANCE_THRESHOLD", "0.8")),
            error_rate_threshold=float(os.getenv("ARIM_ERROR_RATE_THRESHOLD", "0.05")),
            max_research_time=int(os.getenv("ARIM_MAX_RESEARCH_TIME", "3600")),
            min_data_points=int(os.getenv("ARIM_MIN_DATA_POINTS", "100")),
            confidence_threshold=float(os.getenv("ARIM_CONFIDENCE_THRESHOLD", "0.85")),
            dry_run=os.getenv("ARIM_DRY_RUN", "True").lower() == "true",
            rollback_enabled=os.getenv("ARIM_ROLLBACK_ENABLED", "True").lower() == "true",
            max_implementation_time=int(os.getenv("ARIM_MAX_IMPLEMENTATION_TIME", "7200")),
            firebase_collection=os.getenv("ARIM_FIREBASE_COLLECTION", "arim_state"),
            firebase_backup_collection=os.getenv("ARIM_FIREBASE_BACKUP_COLLECTION", "arim_backup"),
            log_level=os.getenv("ARIM_LOG_LEVEL", "INFO"),
            log_file=os.getenv("ARIM_LOG_FILE", "arim_system.log")
        )
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        # Return default config
        return ARIMConfig()

# Global configuration instance
CONFIG = load_config()