"""
Membase Authentication Setup
Handles real Membase credentials and authentication
"""

import os
from typing import Optional, Dict
from pathlib import Path


class MembaseAuth:
    """Manage Membase authentication and credentials"""
    
    @staticmethod
    def get_credentials() -> Dict[str, Optional[str]]:
        """Get Membase credentials from environment"""
        return {
            "membase_id": os.getenv("MEMBASE_ID"),
            "membase_account": os.getenv("MEMBASE_ACCOUNT"),
            "membase_secret_key": os.getenv("MEMBASE_SECRET_KEY")
        }
    
    @staticmethod
    def validate_credentials() -> bool:
        """Validate that all required credentials are set"""
        creds = MembaseAuth.get_credentials()
        
        required = ["membase_id", "membase_account", "membase_secret_key"]
        missing = [k for k in required if not creds[k]]
        
        if missing:
            print(f"❌ Missing Membase credentials: {', '.join(missing)}")
            print("\nSet environment variables:")
            print("  export MEMBASE_ID='eternalgov_delegate'")
            print("  export MEMBASE_ACCOUNT='0x...'")
            print("  export MEMBASE_SECRET_KEY='your_private_key'")
            return False
        
        return True
    
    @staticmethod
    def load_from_env_file(env_path: str = ".env") -> bool:
        """Load credentials from .env file"""
        env_file = Path(env_path)
        
        if not env_file.exists():
            print(f"ℹ️ No {env_path} file found. Using environment variables.")
            return False
        
        try:
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip().strip('"\'')
            
            print(f"✅ Loaded credentials from {env_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to load {env_path}: {str(e)}")
            return False
    
    @staticmethod
    def print_credentials_status():
        """Print credential status (without revealing secrets)"""
        creds = MembaseAuth.get_credentials()
        
        print("\n" + "=" * 70)
        print("MEMBASE AUTHENTICATION STATUS")
        print("=" * 70)
        
        print(f"\n✅ MEMBASE_ID: {creds['membase_id']}")
        print(f"✅ MEMBASE_ACCOUNT: {creds['membase_account'][:10]}...") if creds['membase_account'] else print("❌ MEMBASE_ACCOUNT: Not set")
        print(f"{'✅' if creds['membase_secret_key'] else '❌'} MEMBASE_SECRET_KEY: {'*' * 20}")
        
        is_valid = MembaseAuth.validate_credentials()
        print(f"\n{'✅ All credentials set' if is_valid else '❌ Missing credentials'}")
        print("=" * 70 + "\n")
        
        return is_valid


def setup_membase_auth():
    """Setup Membase authentication for the application"""
    
    print("\n🔐 Membase Authentication Setup")
    print("=" * 70)
    
    # Try to load from .env
    MembaseAuth.load_from_env_file()
    
    # Check credentials
    if MembaseAuth.validate_credentials():
        print("✅ Membase credentials are properly configured!")
        MembaseAuth.print_credentials_status()
        return True
    else:
        print("\n⚠️ Membase SDK will run in fallback mode with placeholder data")
        print("   Real data will NOT be synced to Membase Hub")
        print("\n   To enable real Membase:")
        print("   1. Install SDK: pip install git+https://github.com/unibaseio/membase.git")
        print("   2. Set environment variables or create .env file")
        print("   3. Re-run the application")
        return False


if __name__ == "__main__":
    setup_membase_auth()


# Convenience functions (for easier importing)
def get_credentials() -> Dict[str, Optional[str]]:
    """Get Membase credentials from environment or .env file"""
    MembaseAuth.load_from_env_file()
    return MembaseAuth.get_credentials()


def validate_credentials(creds: Optional[Dict] = None) -> bool:
    """Validate Membase credentials"""
    if creds is None:
        return MembaseAuth.validate_credentials()
    
    required = ["membase_id", "membase_account", "membase_secret_key"]
    return all(creds.get(k) for k in required)

