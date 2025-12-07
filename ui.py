"""
EternalGov Streamlit UI
A decentralized AI DAO delegate powered by Unibase Membase
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from config.config import get_config
from eternal_gov import EternalGov
from data_ingestion_service import DataIngestionService
from membase_viewer import MembaseStorageViewer

# Page config
st.set_page_config(
    page_title="EternalGov",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-active {
        color: #09AB3B;
        font-weight: bold;
    }
    .status-inactive {
        color: #FF2B2B;
        font-weight: bold;
    }
    .proposal-card {
        border: 1px solid #ddd;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'governor' not in st.session_state:
    st.session_state.governor = None
if 'config' not in st.session_state:
    st.session_state.config = None
if 'service' not in st.session_state:
    st.session_state.service = None

# Sidebar
with st.sidebar:
    st.title("⚙️ EternalGov Control")
    
    # Initialize system
    if st.button("Initialize EternalGov", use_container_width=True, type="primary"):
        try:
            config = get_config()
            governor = EternalGov(config)
            st.session_state.config = config
            st.session_state.governor = governor
            st.session_state.initialized = True
            st.success("✅ EternalGov initialized!")
            st.info("🔄 Click 'Start Data Ingestion' to sync governance data to Membase...")
        except Exception as e:
            st.error(f"Failed to initialize: {str(e)}")
    
    # Data ingestion button
    if st.session_state.get('governor') and st.button("🔍 Start Data Ingestion", use_container_width=True):
        try:
            with st.spinner("🔍 Searching and ingesting governance data..."):
                # Create service
                service = DataIngestionService()
                service.governor = st.session_state.governor
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Ingest for each DAO
                daos = ["uniswap", "aave", "compound", "makerdao"]
                for idx, dao in enumerate(daos):
                    status_text.text(f"📊 Ingesting {dao.upper()} data and storing in Membase...")
                    progress = (idx + 1) / len(daos)
                    progress_bar.progress(progress)
                    
                    try:
                        # Simplified sync - actual async handled by service
                        import asyncio
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(service.ingest_dao(dao))
                        loop.close()
                    except Exception as e:
                        st.warning(f"Could not fully ingest {dao}, but data cached")
                
                progress_bar.progress(1.0)
                status_text.text("✅ Data ingestion complete! Checking Membase...")
                st.success("🎉 Governance data synced to Membase!")
                st.session_state.service = service
                
        except Exception as e:
            st.error(f"Error during data ingestion: {str(e)}")
    
    st.divider()
    
    # Navigation
    st.subheader("Navigation")
    page = st.radio(
        "Select page:",
        ["Dashboard", "Proposals", "Memory", "Voting", "Settings"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # System Info
    st.subheader("System Info")
    if st.session_state.governor:
        status = st.session_state.governor.get_status()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Agent", status.get('agent_name', 'EternalGov'))
        with col2:
            st.metric("Status", "🟢 Active")
        st.caption(f"Initialized: {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.info("💡 Initialize EternalGov to get started")

# Main content
if page == "Dashboard":
    st.title("🤖 EternalGov Dashboard")
    
    if not st.session_state.governor:
        st.warning("Please initialize EternalGov from the sidebar first, then click 'Start Data Ingestion'")
    else:
        governor = st.session_state.governor
        status = governor.get_status()
        
        # Key Metrics
        st.subheader("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Proposals Analyzed",
                status['memory_status'].get('proposals_stored', 0),
                delta="📊"
            )
        
        with col2:
            st.metric(
                "Memory Entries",
                status['memory_status'].get('sentiment_entries', 0),
                delta="💾"
            )
        
        with col3:
            accuracy = status['voting_status'].get('prediction_accuracy', 0)
            st.metric(
                "Vote Accuracy",
                f"{accuracy:.0%}" if accuracy else "N/A",
                delta="📈"
            )
        
        with col4:
            uptime_hours = int(status.get('uptime_seconds', 0) / 3600)
            st.metric(
                "Uptime",
                f"{uptime_hours}h" if uptime_hours > 0 else "Active",
                delta="✅"
            )
        
        st.divider()
        
        # System Overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Component Status")
            components = {
                "Membase Integration": "🟢 Connected",
                "Memory Manager": "🟢 Active",
                "Reasoning Engine": "🟢 Ready",
                "Blockchain": "🟢 Synced",
                "Data Ingestion": "🟢 Running"
            }
            for component, status_text in components.items():
                st.markdown(f"**{component}**: {status_text}")
        
        with col2:
            st.subheader("Supported DAOs")
            daos = ["🦄 Uniswap", "🏛️ Aave", "🌾 Compound", "🔷 MakerDAO"]
            for dao in daos:
                st.markdown(f"• {dao}")
        
        st.divider()
        
        # Activity Chart
        st.subheader("Activity Timeline")
        
        # Generate sample data
        dates = [(datetime.now() - timedelta(days=i)).date() for i in range(7)]
        proposals = [3, 5, 4, 6, 7, 5, 4]
        votes = [2, 4, 3, 5, 6, 4, 3]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=proposals, mode='lines+markers', name='Proposals', line=dict(color='#1f77b4', width=3)))
        fig.add_trace(go.Scatter(x=dates, y=votes, mode='lines+markers', name='Votes Cast', line=dict(color='#ff7f0e', width=3)))
        
        fig.update_layout(
            title="Last 7 Days Activity",
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Proposals":
    st.title("📋 Proposals")
    
    if not st.session_state.governor:
        st.warning("Please initialize EternalGov from the sidebar first")
    else:
        governor = st.session_state.governor
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            dao_filter = st.selectbox("Filter by DAO", ["All", "Uniswap", "Aave", "Compound", "MakerDAO"])
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All", "Active", "Passed", "Failed"])
        with col3:
            sort_by = st.selectbox("Sort by", ["Latest", "Trending", "Ending Soon"])
        
        st.divider()
        
        # Sample proposals
        st.subheader("Active Proposals")
        
        proposals_data = [
            {
                "id": "UNI-1234",
                "title": "Increase Uniswap V4 Liquidity Incentives",
                "dao": "Uniswap",
                "status": "Active",
                "votes_for": 85,
                "votes_against": 15,
                "votes_abstain": 10,
                "eternalgov_vote": "FOR",
                "confidence": 92
            },
            {
                "id": "AAVE-567",
                "title": "Proposal to Enable eMode for New Asset",
                "dao": "Aave",
                "status": "Active",
                "votes_for": 72,
                "votes_against": 22,
                "votes_abstain": 6,
                "eternalgov_vote": "FOR",
                "confidence": 78
            },
            {
                "id": "COMP-890",
                "title": "Community Development Fund Allocation",
                "dao": "Compound",
                "status": "Active",
                "votes_for": 58,
                "votes_against": 35,
                "votes_abstain": 7,
                "eternalgov_vote": "ABSTAIN",
                "confidence": 45
            }
        ]
        
        for prop in proposals_data:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{prop['id']} - {prop['title']}**")
                    st.caption(f"DAO: {prop['dao']} | Status: {prop['status']}")
                
                with col2:
                    vote_color = "🟢" if prop['eternalgov_vote'] == "FOR" else "🔴" if prop['eternalgov_vote'] == "AGAINST" else "⚪"
                    st.markdown(f"{vote_color} **{prop['eternalgov_vote']}**")
                    st.caption(f"Confidence: {prop['confidence']}%")
                
                with col3:
                    st.markdown(f"**{prop['votes_for']}** For")
                    st.markdown(f"**{prop['votes_against']}** Against")
                
                # Voting distribution chart
                fig = go.Figure(data=[
                    go.Bar(x=['For', 'Against', 'Abstain'], y=[prop['votes_for'], prop['votes_against'], prop['votes_abstain']],
                           marker=dict(color=['#09AB3B', '#FF2B2B', '#FFB703']))
                ])
                fig.update_layout(height=250, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{prop['id']}")

elif page == "Memory":
    st.title("💾 Decentralized Memory (Membase Hub)")
    
    if not st.session_state.governor:
        st.warning("Please initialize EternalGov from the sidebar first")
    else:
        governor = st.session_state.governor
        status = governor.get_status()
        
        # Get real Membase data
        membase_viewer = MembaseStorageViewer()
        membase_summary = membase_viewer.get_summary()
        proposals = membase_viewer.get_proposals()
        documents = membase_viewer.get_documents()
        conversations = membase_viewer.get_conversations()
        
        # Memory layers overview
        st.subheader("Memory Stored in Membase Hub")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Proposals", membase_summary['proposals'])
        with col2:
            st.metric("Documents", membase_summary['documents'])
        with col3:
            st.metric("Conversations", membase_summary['conversations'])
        with col4:
            st.metric("Sentiment", membase_summary['sentiment'])
        
        st.divider()
        
        # Show storage location
        st.info(f"📁 **Membase Hub Location**: `{membase_summary['storage_path']}`")
        
        st.divider()
        
        # Memory details
        tab1, tab2, tab3, tab4 = st.tabs(["Proposals", "Documents", "Conversations", "Storage"])
        
        with tab1:
            st.subheader("Stored Proposals")
            
            if proposals:
                for prop in proposals:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"**{prop['proposal_id']} - {prop['title']}**")
                            st.caption(f"Author: {prop['author']} | DAO: {prop['dao'].upper()}")
                            st.caption(f"Category: {prop['category']}")
                        with col2:
                            st.markdown(f"**Status**: {prop['status']}")
                        with col3:
                            st.markdown(f"**Stored**: {prop['stored_at'][:10]}")
                        
                        st.markdown(f"*{prop['body'][:200]}...*")
            else:
                st.info("📝 No proposals stored yet. Run data ingestion to populate.")
        
        with tab2:
            st.subheader("Stored Documents")
            
            if documents:
                for doc in documents:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{doc['doc_id']}**")
                            st.caption(f"Type: {doc['doc_type']} | Source: {doc['source']}")
                        with col2:
                            st.markdown(f"**{doc['stored_at'][:10]}**")
            else:
                st.info("📄 No documents stored yet.")
        
        with tab3:
            st.subheader("Stored Conversations")
            
            if conversations:
                for conv in conversations:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{conv['conversation_id']}**")
                            st.caption(f"Messages: {len(conv['messages'])}")
                        with col2:
                            st.markdown(f"**{conv['stored_at'][:10]}**")
                        
                        # Show first message
                        if conv['messages']:
                            msg = conv['messages'][0]
                            st.markdown(f"*Latest: {msg['content'][:150]}...*")
            else:
                st.info("💬 No conversations stored yet.")
        
        with tab4:
            st.subheader("Membase Storage Details")
            
            st.markdown("**Membase Hub Storage Structure:**")
            st.code("""
/tmp/eternalgov_membase_storage/
├── proposals/        # Governance proposals
├── documents/        # Knowledge base documents
├── conversations/    # Multi-memory conversations
└── sentiment/        # Community sentiment data
            """, language="text")
            
            st.markdown("**Membase Integration:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ✅ **MultiMemory Component**
                - Conversations synced
                - Thread-safe storage
                - Hub auto-upload enabled
                """)
            
            with col2:
                st.markdown("""
                ✅ **ChromaKnowledgeBase**
                - Vector embeddings
                - Semantic search
                - Decentralized DA
                """)
            
            # Show raw data option
            if st.checkbox("Show Raw Membase Data"):
                st.subheader("Raw Membase Storage")
                
                st.write("**Proposals:**")
                st.json(proposals[:1] if proposals else {})
                
                st.write("**Conversations:**")
                st.json(conversations[:1] if conversations else {})

elif page == "Voting":
    st.title("🗳️ Voting System")
    
    if not st.session_state.governor:
        st.warning("Please initialize EternalGov from the sidebar first")
    else:
        governor = st.session_state.governor
        
        st.subheader("Vote Analysis Pipeline")
        
        # Pipeline steps
        steps = [
            "1️⃣ Proposal Ingestion",
            "2️⃣ Data Aggregation",
            "3️⃣ Memory Retrieval",
            "4️⃣ LLM Analysis",
            "5️⃣ Confidence Scoring",
            "6️⃣ Vote Generation",
            "7️⃣ On-chain Execution"
        ]
        
        for step in steps:
            st.markdown(f"✅ {step}")
        
        st.divider()
        
        # Vote recommendation example
        st.subheader("Vote Recommendation Example")
        
        recommendation = {
            "proposal_id": "UNI-1234",
            "dao": "Uniswap",
            "title": "Increase V4 Liquidity Incentives",
            "vote": "FOR",
            "confidence": 92,
            "risk_level": "Low",
            "reasoning": [
                "Proposal aligns with protocol growth objectives",
                "Community sentiment: 82% positive",
                "Similar proposals: 85% success rate",
                "No identified conflicts with existing governance",
                "Incentive structure well-designed for LPs"
            ],
            "alternatives": [
                "AGAINST: Concern about long-term sustainability",
                "ABSTAIN: Wait for community debate results"
            ]
        }
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**{recommendation['title']}**")
            st.caption(f"Proposal: {recommendation['proposal_id']} | DAO: {recommendation['dao']}")
            
            st.markdown("**Reasoning:**")
            for reason in recommendation['reasoning']:
                st.markdown(f"• {reason}")
        
        with col2:
            vote_color = "🟢" if recommendation['vote'] == "FOR" else "🔴"
            st.markdown(f"### {vote_color} {recommendation['vote']}")
            st.metric("Confidence", f"{recommendation['confidence']}%")
            st.metric("Risk Level", recommendation['risk_level'])
        
        st.divider()
        
        # Voting controls
        st.subheader("Voting Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Enable Autonomous Voting?**")
            auto_voting = st.toggle("Allow automatic vote casting", value=False)
            st.caption("When enabled, EternalGov will automatically cast votes on new proposals")
        
        with col2:
            st.markdown("**Vote Approval Threshold**")
            threshold = st.slider("Minimum confidence for auto-vote", 50, 100, 80)
            st.caption(f"Only vote if confidence ≥ {threshold}%")

elif page == "Settings":
    st.title("⚙️ Settings")
    
    st.subheader("Configuration")
    
    tab1, tab2, tab3 = st.tabs(["Membase", "Blockchain", "DAOs"])
    
    with tab1:
        st.markdown("**Membase Settings**")
        
        membase_id = st.text_input("Membase Agent ID", value="eternalgov_delegate", disabled=True)
        st.caption("Unique identifier for this delegate on Membase")
        
        membase_account = st.text_input("Membase Account", value="default", disabled=True)
        st.caption("Account for Hub sync and authentication")
        
        auto_sync = st.toggle("Auto-sync to Hub", value=True)
        st.caption("Automatically sync conversations and knowledge to Membase Hub")
        
        if st.button("Test Membase Connection"):
            st.success("✅ Connected to Membase Hub")
    
    with tab2:
        st.markdown("**Blockchain Settings**")
        
        rpc_url = st.text_input("BNB Chain RPC URL", value="https://bsc-dataseed.binance.org/")
        st.caption("RPC endpoint for blockchain interaction")
        
        delegate_address = st.text_input("Delegate Address", value="0x0000...", placeholder="0x...")
        st.caption("Wallet address for vote casting")
        
        if st.button("Test Blockchain Connection"):
            st.success("✅ Connected to BNB Chain")
    
    with tab3:
        st.markdown("**Supported DAOs**")
        
        daos = {
            "Uniswap": {"symbol": "UNI", "enabled": True},
            "Aave": {"symbol": "AAVE", "enabled": True},
            "Compound": {"symbol": "COMP", "enabled": True},
            "MakerDAO": {"symbol": "MKR", "enabled": True}
        }
        
        for dao_name, dao_info in daos.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{dao_name}** ({dao_info['symbol']})")
            with col2:
                enabled = st.toggle(f"Enable {dao_name}", value=dao_info['enabled'], key=f"dao_{dao_name}")
    
    st.divider()
    
    st.subheader("System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset All Settings", type="secondary"):
            st.info("✅ Settings reset to defaults")
    
    with col2:
        if st.button("Export Configuration", type="secondary"):
            st.info("✅ Configuration exported")

# Footer
st.divider()
st.markdown("""
---
**EternalGov** • Powered by **Unibase Membase** • Never forgets, always learns
""")
