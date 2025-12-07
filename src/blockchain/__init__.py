"""
Blockchain Integration for EternalGov
Handles on-chain identity registration and vote casting on BNBChain
"""

from .chain_registry import ChainRegistry
from .vote_caster import VoteCaster

__all__ = [
    "ChainRegistry",
    "VoteCaster",
]
