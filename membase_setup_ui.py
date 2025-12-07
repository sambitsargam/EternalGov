"""
Membase Configuration UI Page
Helps users set up real Membase credentials
"""

import streamlit as st
import os
from pathlib import Path


def membase_setup_page():
    """Display Membase setup and configuration page"""
    
    st.title("🔐 Membase Setup & Configuration")
    
    st.markdown("""
    Configure real Membase authentication to sync governance data to the decentralized Hub.
    """)
    
    # Check current status
    membase_id = os.getenv("MEMBASE_ID")
    membase_account = os.getenv("MEMBASE_ACCOUNT")
    membase_secret = os.getenv("MEMBASE_SECRET_KEY")
    
    has_credentials = bool(membase_id and membase_account and membase_secret)
    
    # Status indicator
    if has_credentials:
        st.success("✅ Membase credentials are configured!")
    else:
        st.warning("⚠️ Membase credentials not configured - using fallback mode")
    
    st.divider()
    
    # Setup instructions
    st.subheader("1️⃣ Environment Setup")
    
    st.markdown("""
    Set the following environment variables:
    
    ```bash
    export MEMBASE_ID="eternalgov_delegate"
    export MEMBASE_ACCOUNT="0x1234567890abcdef..."
    export MEMBASE_SECRET_KEY="your_private_key"
    ```
    
    Or create a `.env` file:
    
    ```
    MEMBASE_ID=eternalgov_delegate
    MEMBASE_ACCOUNT=0x1234567890abcdef...
    MEMBASE_SECRET_KEY=your_private_key
    ```
    """)
    
    st.divider()
    
    st.subheader("2️⃣ Credentials Explained")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **MEMBASE_ID**
        - Unique agent identifier
        - Example: `eternalgov_delegate`
        - Used for on-chain registration
        """)
    
    with col2:
        st.markdown("""
        **MEMBASE_ACCOUNT**
        - Your wallet/account address
        - Example: `0x1234567...`
        - Owner of agent identity
        """)
    
    with col3:
        st.markdown("""
        **MEMBASE_SECRET_KEY**
        - Private key for authentication
        - Enables real Membase sync
        - ⚠️ Keep this secret!
        """)
    
    st.divider()
    
    st.subheader("3️⃣ Current Configuration")
    
    st.markdown("**Current Environment Variables:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"```")
        st.markdown(f"MEMBASE_ID = {membase_id or '❌ Not set'}")
        st.markdown(f"MEMBASE_ACCOUNT = {membase_account or '❌ Not set'}")
        st.markdown(f"MEMBASE_SECRET_KEY = {'*' * 20 if membase_secret else '❌ Not set'}")
        st.markdown(f"```")
    
    with col2:
        st.markdown("**Installation:**")
        st.code("""
pip install git+https://github.com/unibaseio/membase.git
        """, language="bash")
    
    st.divider()
    
    st.subheader("4️⃣ Installation & SDK")
    
    with st.expander("📦 Install Membase SDK"):
        st.markdown("""
        ```bash
        # Option 1: From GitHub
        pip install git+https://github.com/unibaseio/membase.git
        
        # Option 2: Local installation
        git clone https://github.com/unibaseio/membase.git
        cd membase
        pip install -e .
        ```
        """)
    
    st.divider()
    
    st.subheader("5️⃣ Verify Configuration")
    
    if st.button("✅ Test Membase Connection", type="primary"):
        try:
            # Check if SDK is installed
            from membase.chain.chain import membase_chain
            st.success("✅ Membase SDK is installed")
            
            # Check credentials
            if membase_account and membase_secret:
                st.success("✅ Credentials are configured")
                st.info("🔗 Ready to sync governance data to Membase Hub!")
            else:
                st.warning("⚠️ Credentials not fully configured - see setup steps above")
        
        except ImportError:
            st.error("""
            ❌ Membase SDK not installed
            
            Install with:
            ```bash
            pip install git+https://github.com/unibaseio/membase.git
            ```
            """)
    
    st.divider()
    
    st.subheader("🌐 Access Your Data")
    
    st.markdown("""
    Once configured and synced, visit:
    **https://hub.membase.io/**
    
    Your governance data will appear under your MEMBASE_ACCOUNT.
    """)
    
    st.divider()
    
    st.subheader("📖 Documentation")
    
    st.markdown("""
    - [Membase Docs](https://openos-labs.gitbook.io/unibase-docs/membase)
    - [Quick Start](https://openos-labs.gitbook.io/unibase-docs/membase/quick-start)
    - [Identity System](https://openos-labs.gitbook.io/unibase-docs/membase/identity)
    - [Multi-Memory](https://openos-labs.gitbook.io/unibase-docs/membase/multi-memory)
    - [GitHub Repository](https://github.com/unibaseio/membase)
    """)


if __name__ == "__main__":
    membase_setup_page()
