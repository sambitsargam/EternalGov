"""
Vote Caster for EternalGov
Executes on-chain votes for DAO proposals
"""

from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OnChainVote:
    """Records an on-chain vote"""
    proposal_id: str
    dao: str
    vote_choice: str
    voter_address: str
    transaction_hash: str
    block_number: int
    timestamp: str
    justification_hash: str  # Reference to Membase justification
    gas_used: float


class VoteCaster:
    """
    Casts votes on-chain for governance proposals
    """
    
    def __init__(self, delegate_address: str):
        """
        Initialize vote caster
        
        Args:
            delegate_address: Address of EternalGov delegate
        """
        self.delegate_address = delegate_address
        self.votes_cast: Dict[str, OnChainVote] = {}
        self.pending_votes: List[Dict] = []
    
    def cast_vote_snapshot(
        self,
        proposal_id: str,
        choice: str,
        space: str,
        justification_hash: str
    ) -> Optional[str]:
        """
        Cast a vote on Snapshot
        
        Args:
            proposal_id: Snapshot proposal ID
            choice: Vote choice
            space: Snapshot space
            justification_hash: Hash of vote justification
            
        Returns:
            Transaction hash or None
        """
        
        # In production: integrate with Snapshot voting mechanism
        # snapshot.vote(proposal_id, choice, signature)
        
        vote = OnChainVote(
            proposal_id=proposal_id,
            dao=space,
            vote_choice=choice,
            voter_address=self.delegate_address,
            transaction_hash="0x",  # Placeholder
            block_number=0,
            timestamp=datetime.utcnow().isoformat(),
            justification_hash=justification_hash,
            gas_used=0.0
        )
        
        self.votes_cast[proposal_id] = vote
        print(f"[PLACEHOLDER] Casting vote on Snapshot: {space}/{proposal_id} -> {choice}")
        
        return None
    
    def cast_vote_on_chain(
        self,
        proposal_id: str,
        dao_governance_contract: str,
        choice: str,
        justification_hash: str
    ) -> Optional[str]:
        """
        Cast a vote directly on-chain via DAO governance contract
        
        Args:
            proposal_id: Proposal ID
            dao_governance_contract: DAO governance contract address
            choice: Vote choice (usually integer index)
            justification_hash: Hash of justification
            
        Returns:
            Transaction hash or None
        """
        
        # In production: call governance contract castVote function
        # from web3 import Web3
        # contract = w3.eth.contract(address=dao_governance_contract, abi=ABI)
        # tx = contract.functions.castVote(proposal_id, choice).transact({
        #     "from": self.delegate_address
        # })
        
        vote = OnChainVote(
            proposal_id=proposal_id,
            dao=dao_governance_contract,
            vote_choice=str(choice),
            voter_address=self.delegate_address,
            transaction_hash="0x",
            block_number=0,
            timestamp=datetime.utcnow().isoformat(),
            justification_hash=justification_hash,
            gas_used=0.0
        )
        
        self.votes_cast[proposal_id] = vote
        print(f"[PLACEHOLDER] Casting on-chain vote: {proposal_id} -> {choice}")
        
        return None
    
    def cast_vote_with_delegation_option(
        self,
        proposal_id: str,
        choice: str,
        dao: str,
        justification_hash: str,
        allow_human_override: bool = True
    ) -> Optional[str]:
        """
        Cast a vote with optional human delegation
        
        Args:
            proposal_id: Proposal ID
            choice: Recommended vote choice
            dao: DAO name
            justification_hash: Justification hash
            allow_human_override: Whether humans can override
            
        Returns:
            Transaction hash or None
        """
        
        # Log vote with delegation option
        vote_record = {
            "proposal_id": proposal_id,
            "dao": dao,
            "choice": choice,
            "timestamp": datetime.utcnow().isoformat(),
            "justification_hash": justification_hash,
            "allow_human_override": allow_human_override,
            "status": "pending_if_delegated" if allow_human_override else "casting"
        }
        
        self.pending_votes.append(vote_record)
        
        if not allow_human_override:
            # Cast immediately
            return self.cast_vote_on_chain(proposal_id, dao, choice, justification_hash)
        else:
            print(f"[PLACEHOLDER] Vote {proposal_id} ready for delegation approval")
            return None
    
    def get_vote_history(self) -> Dict[str, OnChainVote]:
        """Get all cast votes"""
        return self.votes_cast
    
    def get_pending_votes(self) -> List[Dict]:
        """Get votes pending human approval"""
        return self.pending_votes
    
    def approve_pending_vote(self, proposal_id: str) -> Optional[str]:
        """
        Approve a pending vote for casting
        
        Args:
            proposal_id: Proposal ID
            
        Returns:
            Transaction hash or None
        """
        
        pending = next((v for v in self.pending_votes if v["proposal_id"] == proposal_id), None)
        if pending:
            self.pending_votes.remove(pending)
            return self.cast_vote_on_chain(
                proposal_id,
                pending["dao"],
                pending["choice"],
                pending["justification_hash"]
            )
        
        return None
    
    def reject_pending_vote(self, proposal_id: str) -> bool:
        """
        Reject a pending vote
        
        Args:
            proposal_id: Proposal ID
            
        Returns:
            True if successfully rejected
        """
        
        pending = next((v for v in self.pending_votes if v["proposal_id"] == proposal_id), None)
        if pending:
            self.pending_votes.remove(pending)
            pending["status"] = "rejected"
            print(f"[PLACEHOLDER] Vote {proposal_id} rejected by human")
            return True
        
        return False
    
    def get_vote_verification_data(self, proposal_id: str) -> Optional[Dict]:
        """
        Get data for verifying a vote on-chain
        
        Args:
            proposal_id: Proposal ID
            
        Returns:
            Verification data or None
        """
        
        vote = self.votes_cast.get(proposal_id)
        if not vote:
            return None
        
        return {
            "proposal_id": vote.proposal_id,
            "voter": vote.voter_address,
            "choice": vote.vote_choice,
            "timestamp": vote.timestamp,
            "justification_reference": vote.justification_hash,
            "transaction_hash": vote.transaction_hash,
            "block_number": vote.block_number
        }
