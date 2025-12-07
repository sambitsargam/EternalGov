"""
Agent Identity Management for EternalGov
Registers and manages the immortal AI delegate identity on Membase
"""

import os
from typing import Optional
from dataclasses import dataclass

try:
    from membase.chain.chain import membase_chain
    MEMBASE_AVAILABLE = True
except ImportError:
    MEMBASE_AVAILABLE = False


@dataclass
class AgentIdentity:
    """
    Represents EternalGov's decentralized identity on Membase
    """
    
    agent_name: str
    membase_id: str
    membase_account: str
    secret_key: str
    
    def __init__(self, agent_name: str = "EternalGov"):
        """
        Initialize agent identity from environment or parameters
        
        Args:
            agent_name: Name of the AI delegate
        """
        self.agent_name = agent_name
        self.membase_id = os.getenv("MEMBASE_ID", f"{agent_name}_delegate")
        self.membase_account = os.getenv("MEMBASE_ACCOUNT", "default")
        self.secret_key = os.getenv("MEMBASE_SECRET_KEY", "")
    
    def get_identity_proof(self) -> dict:
        """
        Return identity information for on-chain verification
        
        Returns:
            Dictionary containing identity proof
        """
        return {
            "agent_name": self.agent_name,
            "membase_id": self.membase_id,
            "membase_account": self.membase_account,
            "identity_type": "autonomous_dao_delegate",
            "memory_layer": "membase",
            "capabilities": [
                "proposal_analysis",
                "sentiment_tracking",
                "autonomous_voting",
                "memory_persistence"
            ]
        }
    
    def register_on_chain(self):
        """
        Register this agent identity on-chain via Membase
        """
        if not MEMBASE_AVAILABLE:
            print(f"[PLACEHOLDER] Registering {self.agent_name} on-chain (Membase SDK not available)")
            return
        
        try:
            # Real Membase chain registration
            membase_chain.register(self.agent_name)
            print(f"[MEMBASE] Successfully registered {self.agent_name} on-chain")
        except Exception as e:
            print(f"[ERROR] Failed to register on-chain: {str(e)}")
    
    def to_dict(self) -> dict:
        """Serialize identity to dictionary"""
        return {
            "agent_name": self.agent_name,
            "membase_id": self.membase_id,
            "membase_account": self.membase_account,
        }
