"""
Configuration for EternalGov
"""

import os
from typing import Dict, List, Optional

# Membase Configuration
MEMBASE_ID = os.getenv("MEMBASE_ID", "EternalGov_delegate")
MEMBASE_ACCOUNT = os.getenv("MEMBASE_ACCOUNT", "")
MEMBASE_SECRET_KEY = os.getenv("MEMBASE_SECRET_KEY", "")
MEMBASE_STORAGE_DIR = os.getenv("MEMBASE_STORAGE_DIR", "/tmp/eternalgov_membase")
AUTO_UPLOAD_TO_HUB = os.getenv("AUTO_UPLOAD_TO_HUB", "true").lower() == "true"
PRELOAD_FROM_HUB = os.getenv("PRELOAD_FROM_HUB", "true").lower() == "true"

# Blockchain Configuration
BNB_CHAIN_RPC = os.getenv("BNB_CHAIN_RPC", "https://bsc-dataseed.binance.org/")
DELEGATE_ADDRESS = os.getenv("DELEGATE_ADDRESS", "")
DELEGATE_PRIVATE_KEY = os.getenv("DELEGATE_PRIVATE_KEY", "")

# Data Ingestion Configuration
SNAPSHOT_SPACES = [
    "uniswap.eth",
    "aave.eth",
    "compound.eth",
    "maker.eth",
]

GOVERNANCE_FORUMS = {
    "uniswap": "https://gov.uniswap.org",
    "aave": "https://governance.aave.com",
    "compound": "https://compound.community",
    "makerdao": "https://forum.makerdao.com",
}

TWITTER_HANDLES = [
    "UniswapProtocol",
    "aaveaave",
    "compoundfinance",
    "MakerDAO",
]

BLOG_SOURCES = {
    "medium": ["Uniswap", "Aave", "Compound", "MakerDAO"],
    "mirror": ["Uniswap", "Aave", "Compound", "MakerDAO"],
}

# Reasoning Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
REASONING_TEMPERATURE = 0.3  # Lower = more deterministic
CONFIDENCE_THRESHOLD = 0.5   # Minimum confidence to cast vote

# Memory Configuration
KNOWLEDGE_BASE_DIR = os.getenv("KB_DIR", "/tmp/eternalgov_kb")
PROPOSAL_MEMORY_SYNC_INTERVAL = 3600  # seconds
SENTIMENT_UPDATE_INTERVAL = 1800  # seconds
OUTCOME_ANALYSIS_INTERVAL = 86400  # seconds

# Voting Configuration
ALLOW_AUTONOMOUS_VOTING = os.getenv("ALLOW_AUTONOMOUS_VOTING", "false").lower() == "true"
REQUIRE_HUMAN_APPROVAL = not ALLOW_AUTONOMOUS_VOTING
VOTING_TIMEOUT = 3600  # seconds before vote expiration
MAX_SLIPPAGE = 0.01  # Maximum acceptable vote variance

# Monitoring Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENABLE_LOGGING = True
LOG_FILE = os.getenv("LOG_FILE", "/tmp/eternalgov.log")
METRICS_ENABLED = True

# DAO Configuration
SUPPORTED_DAOS = {
    "uniswap": {
        "space": "uniswap.eth",
        "governance_token": "UNI",
        "delegate_weight": 0.0,
    },
    "aave": {
        "space": "aave.eth",
        "governance_token": "AAVE",
        "delegate_weight": 0.0,
    },
    "compound": {
        "space": "compound.eth",
        "governance_token": "COMP",
        "delegate_weight": 0.0,
    },
    "makerdao": {
        "space": "maker.eth",
        "governance_token": "MKR",
        "delegate_weight": 0.0,
    },
}

def get_config() -> Dict:
    """Get complete configuration dictionary"""
    return {
        "membase": {
            "id": MEMBASE_ID,
            "account": MEMBASE_ACCOUNT,
            "storage_dir": MEMBASE_STORAGE_DIR,
            "auto_upload": AUTO_UPLOAD_TO_HUB,
        },
        "blockchain": {
            "rpc_url": BNB_CHAIN_RPC,
            "delegate_address": DELEGATE_ADDRESS,
        },
        "reasoning": {
            "llm_model": LLM_MODEL,
            "temperature": REASONING_TEMPERATURE,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
        },
        "voting": {
            "autonomous": ALLOW_AUTONOMOUS_VOTING,
            "require_approval": REQUIRE_HUMAN_APPROVAL,
            "timeout": VOTING_TIMEOUT,
        },
        "daos": SUPPORTED_DAOS,
    }
