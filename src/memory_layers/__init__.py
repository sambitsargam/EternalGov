"""
Memory Layers for EternalGov
Implements specialized memory systems for different types of governance knowledge
"""

from .proposal_memory import ProposalMemory
from .sentiment_memory import SentimentMemory
from .preference_memory import PreferenceMemory
from .outcome_memory import OutcomeMemory

__all__ = [
    "ProposalMemory",
    "SentimentMemory",
    "PreferenceMemory",
    "OutcomeMemory",
]
