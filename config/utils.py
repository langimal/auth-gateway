import logging
import os
from typing import Dict, List, Tuple

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_environment_variables() -> Dict[str, str]:
    try:
        env_vars = {
            'AUTH_GW_HOST': os.environ['AUTH_GW_HOST'],
            'AUTH_GW_PORT': os.environ['AUTH_GW_PORT'],
            'AUTH_GW_CLIENT_ID': os.environ['AUTH_GW_CLIENT_ID'],
            'AUTH_GW_CLIENT_SECRET': os.environ['AUTH_GW_CLIENT_SECRET']
        }
        return env_vars
    except KeyError as e:
        logger.error(f"Missing environment variable: {e}")
        raise

def validate_config(config: Dict[str, str]) -> bool:
    required_keys = ['AUTH_GW_HOST', 'AUTH_GW_PORT', 'AUTH_GW_CLIENT_ID', 'AUTH_GW_CLIENT_SECRET']
    for key in required_keys:
        if key not in config:
            logger.error(f"Missing configuration key: {key}")
            return False
    return True

def parse_auth_response(response: Dict[str, str]) -> Tuple[str, str]:
    try:
        access_token = response['access_token']
        token_type = response['token_type']
        return access_token, token_type
    except KeyError as e:
        logger.error(f"Invalid auth response: {e}")
        raise

def get_auth_headers(access_token: str, token_type: str) -> Dict[str, str]:
    return {
        'Authorization': f"{token_type} {access_token}",
        'Content-Type': 'application/json'
    }