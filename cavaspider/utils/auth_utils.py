import os
from dotenv import load_dotenv

load_dotenv()

def get_credentials():
    """Get credentials from environment variables"""
    return {
        'username': os.getenv('CAVA_USERNAME'),
        'password': os.getenv('CAVA_PASSWORD')
    }

def is_logged_in(response):
    """Check if current session is logged in"""
    if "login" in response.url or "login" in response.text or "Invalid credentials" in response.text:
        return False
    return True