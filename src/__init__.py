"""
EternalGov - The Immortal AI DAO Delegate
"""

__version__ = "0.1.0"
__author__ = "EternalGov Contributors"

from src.membase import AgentIdentity, MembaseMemoryManager, GovernanceKnowledgeBase
from src.data_ingestion import DataAggregator
from src.memory_layers import ProposalMemory, SentimentMemory, PreferenceMemory, OutcomeMemory
from src.reasoning import VoteReasoning, JustificationReporter
from src.blockchain import ChainRegistry, VoteCaster

__all__ = [
    "AgentIdentity",
    "MembaseMemoryManager",
    "GovernanceKnowledgeBase",
    "DataAggregator",
    "ProposalMemory",
    "SentimentMemory",
    "PreferenceMemory",
    "OutcomeMemory",
    "VoteReasoning",
    "JustificationReporter",
    "ChainRegistry",
    "VoteCaster",
]
