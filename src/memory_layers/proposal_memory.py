"""
Proposal Memory Layer for EternalGov
Stores structured proposal data with vector embeddings for semantic search
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProposalMemoryEntry:
    """Stores a proposal in Membase"""
    proposal_id: str
    dao: str
    title: str
    body: str
    author: str
    created_at: str
    end_time: str
    choices: List[str]
    category: str
    url: str
    embedding: Optional[List[float]] = None
    reasoning_points: List[str] = field(default_factory=list)
    key_arguments: Dict[str, List[str]] = field(default_factory=dict)  # {choice: [args]}
    expected_impact: str = ""
    status: str = "active"  # "active", "ended", "canceled"


class ProposalMemory:
    """
    Manages proposal memory in Membase
    Stores raw proposals, embeddings, reasoning, and impact analysis
    """
    
    def __init__(self, membase_account: str):
        """
        Initialize proposal memory
        
        Args:
            membase_account: Membase account for storage
        """
        self.membase_account = membase_account
        self.proposals: Dict[str, ProposalMemoryEntry] = {}
        self.dao_index: Dict[str, List[str]] = {}  # dao -> [proposal_ids]
    
    def store_proposal(
        self,
        proposal_id: str,
        dao: str,
        title: str,
        body: str,
        author: str,
        created_at: str,
        end_time: str,
        choices: List[str],
        url: str,
        category: str = "general"
    ) -> None:
        """
        Store a proposal in memory
        
        Args:
            proposal_id: Unique proposal ID
            dao: DAO name
            title: Proposal title
            body: Full proposal text
            author: Proposal author
            created_at: Creation timestamp
            end_time: Voting end time
            choices: Voting options
            url: Proposal URL
            category: Proposal category
        """
        entry = ProposalMemoryEntry(
            proposal_id=proposal_id,
            dao=dao,
            title=title,
            body=body,
            author=author,
            created_at=created_at,
            end_time=end_time,
            choices=choices,
            category=category,
            url=url
        )
        
        self.proposals[proposal_id] = entry
        
        # Update DAO index
        if dao not in self.dao_index:
            self.dao_index[dao] = []
        self.dao_index[dao].append(proposal_id)
        
        # In production: sync to Membase
        # from membase.knowledge.chroma import ChromaKnowledgeBase
        # kb.add_documents(Document(content=body, metadata={...}))
        self._sync_to_membase(entry)
    
    def add_reasoning_points(
        self,
        proposal_id: str,
        reasoning_points: List[str]
    ) -> None:
        """
        Add extracted reasoning points to a proposal
        
        Args:
            proposal_id: Proposal ID
            reasoning_points: List of reasoning points
        """
        if proposal_id in self.proposals:
            self.proposals[proposal_id].reasoning_points = reasoning_points
    
    def add_key_arguments(
        self,
        proposal_id: str,
        arguments: Dict[str, List[str]]
    ) -> None:
        """
        Add parsed arguments for each voting choice
        
        Args:
            proposal_id: Proposal ID
            arguments: Dict mapping choices to lists of arguments
        """
        if proposal_id in self.proposals:
            self.proposals[proposal_id].key_arguments = arguments
    
    def set_expected_impact(
        self,
        proposal_id: str,
        impact: str
    ) -> None:
        """
        Set expected impact analysis
        
        Args:
            proposal_id: Proposal ID
            impact: Impact analysis text
        """
        if proposal_id in self.proposals:
            self.proposals[proposal_id].expected_impact = impact
    
    def get_proposal(self, proposal_id: str) -> Optional[ProposalMemoryEntry]:
        """Retrieve a proposal from memory"""
        return self.proposals.get(proposal_id)
    
    def get_dao_proposals(self, dao: str) -> List[ProposalMemoryEntry]:
        """Get all proposals for a DAO"""
        proposal_ids = self.dao_index.get(dao, [])
        return [self.proposals[pid] for pid in proposal_ids if pid in self.proposals]
    
    def search_proposals(
        self,
        query: str,
        dao: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[ProposalMemoryEntry]:
        """
        Search proposals (simple text search; in production: semantic search via embeddings)
        
        Args:
            query: Search query
            dao: Optional DAO filter
            category: Optional category filter
            
        Returns:
            List of matching proposals
        """
        results = []
        query_lower = query.lower()
        
        for proposal in self.proposals.values():
            # Apply filters
            if dao and proposal.dao != dao:
                continue
            if category and proposal.category != category:
                continue
            
            # Search in title and body
            if query_lower in proposal.title.lower() or query_lower in proposal.body.lower():
                results.append(proposal)
        
        return results
    
    def update_status(self, proposal_id: str, status: str) -> None:
        """Update proposal status"""
        if proposal_id in self.proposals:
            self.proposals[proposal_id].status = status
    
    def _sync_to_membase(self, entry: ProposalMemoryEntry) -> None:
        """Sync proposal to Membase for decentralized storage"""
        # Placeholder for Membase sync
        print(f"[MEMBASE] Syncing proposal {entry.proposal_id} to Membase")
