"""
Reasoning Engine for EternalGov
Implements LLM-based decision-making and vote justification
"""

from .vote_reasoning import VoteReasoning
from .justification_reporter import JustificationReporter

__all__ = [
    "VoteReasoning",
    "JustificationReporter",
]
