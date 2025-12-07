#!/usr/bin/env python3
"""
Test script to verify Membase integration and real SDK installation
Run this to check if your system is ready for real Membase sync
"""

import os
import sys
from pathlib import Path

def print_status(label, status):
    """Pretty print status"""
    icon = "✅" if status else "❌"
    print(f"{icon} {label}")

def check_environment():
    """Check environment variables"""
    print("\n📋 **Environment Variables Check**")
    print("-" * 50)
    
    # First try loading from .env
    try:
        from membase_auth import MembaseAuth
        MembaseAuth.load_from_env_file()
    except:
        pass
    
    membase_id = os.getenv("MEMBASE_ID")
    membase_account = os.getenv("MEMBASE_ACCOUNT")
    membase_secret = os.getenv("MEMBASE_SECRET_KEY")
    
    print_status("MEMBASE_ID set", bool(membase_id))
    if membase_id:
        print(f"   Value: {membase_id}")
    
    print_status("MEMBASE_ACCOUNT set", bool(membase_account))
    if membase_account:
        print(f"   Value: {membase_account}")
    
    print_status("MEMBASE_SECRET_KEY set", bool(membase_secret))
    if membase_secret:
        print(f"   Value: {'*' * 20} (hidden for security)")
    
    return bool(membase_id and membase_account and membase_secret)

def check_sdk_installation():
    """Check if Membase SDK is installed"""
    print("\n📦 **Membase SDK Check**")
    print("-" * 50)
    
    try:
        import membase
        print_status("Membase package installed", True)
        print(f"   Location: {membase.__file__}")
        
        try:
            from membase.chain.chain import membase_chain
            print_status("Chain module available", True)
        except ImportError as e:
            print_status("Chain module available", False)
            print(f"   Error: {e}")
        
        try:
            from membase.memory.multi_memory import MultiMemory
            print_status("MultiMemory module available", True)
        except ImportError as e:
            print_status("MultiMemory module available", False)
            print(f"   Error: {e}")
        
        try:
            from membase.knowledge.chroma import ChromaKnowledgeBase
            print_status("ChromaKnowledgeBase module available", True)
        except ImportError as e:
            print_status("ChromaKnowledgeBase module available", False)
            print(f"   Error: {e}")
        
        return True
    
    except ImportError:
        print_status("Membase package installed", False)
        print("\n⚠️  Installation instructions:")
        print("   pip install git+https://github.com/unibaseio/membase.git")
        return False

def check_membase_auth():
    """Check if membase_auth module works"""
    print("\n🔐 **Membase Auth Module Check**")
    print("-" * 50)
    
    try:
        from membase_auth import get_credentials, validate_credentials
        
        creds = get_credentials()
        print_status("Credentials loaded", bool(creds))
        
        if creds:
            is_valid = validate_credentials(creds)
            print_status("Credentials valid", is_valid)
            
            if is_valid:
                print(f"   Agent ID: {creds.get('agent_id')}")
                print(f"   Account: {creds.get('account')}")
                print(f"   Has Secret: {bool(creds.get('secret_key'))}")
        
        return bool(creds)
    
    except Exception as e:
        print_status("Membase auth module works", False)
        print(f"   Error: {e}")
        return False

def check_data_storage():
    """Check if data storage directories exist"""
    print("\n💾 **Data Storage Check**")
    print("-" * 50)
    
    storage_path = Path("/tmp/eternalgov_membase_storage")
    print_status("Storage directory exists", storage_path.exists())
    
    if storage_path.exists():
        subdirs = ["proposals", "documents", "conversations", "sentiment"]
        for subdir in subdirs:
            subdir_path = storage_path / subdir
            has_files = bool(list(subdir_path.glob("*.json"))) if subdir_path.exists() else False
            print_status(f"  {subdir}/ directory", subdir_path.exists())
            if has_files:
                file_count = len(list(subdir_path.glob("*.json")))
                print(f"     Files: {file_count}")

def check_ui_dependencies():
    """Check UI dependencies"""
    print("\n🎨 **UI Dependencies Check**")
    print("-" * 50)
    
    deps = {
        "streamlit": "Streamlit",
        "plotly": "Plotly",
        "pandas": "Pandas"
    }
    
    for module_name, display_name in deps.items():
        try:
            __import__(module_name)
            print_status(f"{display_name} installed", True)
        except ImportError:
            print_status(f"{display_name} installed", False)

def check_integration():
    """Check if all integration points work"""
    print("\n🔗 **Integration Points Check**")
    print("-" * 50)
    
    try:
        from eternal_gov import EternalGov
        from config.config import get_config
        
        print_status("EternalGov can be imported", True)
        
        try:
            config = get_config()
            print_status("Config loads successfully", True)
        except Exception as e:
            print_status("Config loads successfully", False)
            print(f"   Error: {e}")
    
    except ImportError as e:
        print_status("EternalGov can be imported", False)
        print(f"   Error: {e}")

def print_summary(env_ok, sdk_ok):
    """Print summary and recommendations"""
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if env_ok and sdk_ok:
        print("\n✅ Your system is ready for real Membase integration!")
        print("\nNext steps:")
        print("1. Run: streamlit run ui.py")
        print("2. Navigate to Settings → Setup page")
        print("3. Verify Membase connection")
        print("4. Enable data ingestion")
    
    elif env_ok:
        print("\n⚠️  Environment configured but SDK not installed")
        print("\nTo complete setup:")
        print("1. pip install git+https://github.com/unibaseio/membase.git")
        print("2. Run this script again to verify")
    
    elif sdk_ok:
        print("\n⚠️  SDK installed but environment not configured")
        print("\nTo complete setup:")
        print("1. Set environment variables:")
        print("   export MEMBASE_ID='eternalgov_delegate'")
        print("   export MEMBASE_ACCOUNT='0x...'")
        print("   export MEMBASE_SECRET_KEY='your_private_key'")
        print("2. Or create .env file in project root")
    
    else:
        print("\n❌ Setup not complete")
        print("\nTo get started:")
        print("1. Install Membase SDK:")
        print("   pip install git+https://github.com/unibaseio/membase.git")
        print("2. Configure environment variables (see instructions above)")
        print("3. Run this script again")

def main():
    """Run all checks"""
    print("\n" + "🔍 ETERNALGOV MEMBASE INTEGRATION TEST".center(50, " "))
    print("=" * 50)
    
    env_ok = check_environment()
    sdk_ok = check_sdk_installation()
    check_membase_auth()
    check_data_storage()
    check_ui_dependencies()
    check_integration()
    
    print_summary(env_ok, sdk_ok)
    
    print("\n" + "=" * 50)
    print("\n📖 Documentation:")
    print("• Membase Docs: https://openos-labs.gitbook.io/unibase-docs/membase")
    print("• Setup Guide: See MEMBASE_SETUP.md in project root")
    print("• Hub Access: https://hub.membase.io/")

if __name__ == "__main__":
    main()
