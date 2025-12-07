"""
Membase Integration Layer for EternalGov
Handles decentralized memory storage and agent identity
"""

from .agent_identity import AgentIdentity
from .memory_manager import MembaseMemoryManager
from .knowledge_base import GovernanceKnowledgeBase

__all__ = [
    "AgentIdentity",
    "MembaseMemoryManager",
    "GovernanceKnowledgeBase",
]
