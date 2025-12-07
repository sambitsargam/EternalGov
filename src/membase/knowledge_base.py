"""
Governance Knowledge Base for EternalGov
Stores and manages governance documents, proposals, and contextual data
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GovernanceDocument:
    """Represents a governance document or proposal"""
    doc_id: str
    content: str
    source: str  # "snapshot", "discourse", "twitter", "medium", etc.
    doc_type: str  # "proposal", "discussion", "analysis", "article"
    metadata: dict = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    added_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class GovernanceKnowledgeBase:
    """
    Manages governance knowledge documents using Membase backend
    Integrates with Chroma for vector embeddings
    """
    
    def __init__(
        self,
        persist_directory: str = "/tmp/eternalgov_kb",
        membase_account: str = "default",
        auto_upload: bool = True
    ):
        """
        Initialize knowledge base
        
        Args:
            persist_directory: Local persistence directory
            membase_account: Membase account for storage
            auto_upload: Whether to sync to Membase Hub
        """
        self.persist_directory = persist_directory
        self.membase_account = membase_account
        self.auto_upload = auto_upload
        self.documents: Dict[str, GovernanceDocument] = {}
        
        # In production: 
        # from membase.knowledge.chroma import ChromaKnowledgeBase
        # self.kb = ChromaKnowledgeBase(
        #     persist_directory=persist_directory,
        #     membase_account=membase_account,
        #     auto_upload_to_hub=auto_upload
        # )
    
    def add_document(
        self,
        doc_id: str,
        content: str,
        source: str,
        doc_type: str,
        metadata: Optional[dict] = None
    ) -> None:
        """
        Add a document to the knowledge base
        
        Args:
            doc_id: Unique document identifier
            content: Document content
            source: Source platform
            doc_type: Type of document
            metadata: Additional metadata
        """
        doc = GovernanceDocument(
            doc_id=doc_id,
            content=content,
            source=source,
            doc_type=doc_type,
            metadata=metadata or {}
        )
        
        self.documents[doc_id] = doc
        
        if self.auto_upload:
            self._sync_to_hub(doc)
    
    def add_proposal(
        self,
        proposal_id: str,
        proposal_text: str,
        url: str,
        author: str,
        timestamp: str,
        metadata: Optional[dict] = None
    ) -> None:
        """
        Add a governance proposal to knowledge base
        
        Args:
            proposal_id: Snapshot or DAO proposal ID
            proposal_text: Full proposal text
            url: Proposal URL
            author: Proposal author
            timestamp: Creation timestamp
            metadata: Additional metadata
        """
        meta = metadata or {}
        meta.update({
            "proposal_id": proposal_id,
            "url": url,
            "author": author,
            "timestamp": timestamp,
            "category": "governance_proposal"
        })
        
        self.add_document(
            doc_id=f"proposal_{proposal_id}",
            content=proposal_text,
            source="snapshot",
            doc_type="proposal",
            metadata=meta
        )
    
    def add_discussion(
        self,
        discussion_id: str,
        content: str,
        source: str,
        url: str,
        sentiment: Optional[str] = None
    ) -> None:
        """
        Add governance discussion/forum content
        
        Args:
            discussion_id: Discussion identifier
            content: Discussion content
            source: Platform (discourse, commonwealth, github)
            url: Discussion URL
            sentiment: Sentiment label if available
        """
        meta = {
            "source_platform": source,
            "url": url,
            "sentiment": sentiment or "neutral",
            "category": "governance_discussion"
        }
        
        self.add_document(
            doc_id=f"discussion_{discussion_id}",
            content=content,
            source=source,
            doc_type="discussion",
            metadata=meta
        )
    
    def search_documents(
        self,
        query: str,
        doc_type: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 10
    ) -> List[GovernanceDocument]:
        """
        Search knowledge base
        
        Args:
            query: Search query
            doc_type: Filter by document type
            source: Filter by source
            limit: Maximum results
            
        Returns:
            List of matching documents
        """
        results = []
        
        for doc in self.documents.values():
            # Apply filters
            if doc_type and doc.doc_type != doc_type:
                continue
            if source and doc.source != source:
                continue
            
            # Simple substring matching (in production: semantic search)
            if query.lower() in doc.content.lower():
                results.append(doc)
        
        return results[:limit]
    
    def get_proposals_by_dao(self, dao_name: str) -> List[GovernanceDocument]:
        """Get all proposals for a specific DAO"""
        return [
            doc for doc in self.documents.values()
            if doc.metadata.get("dao") == dao_name and doc.doc_type == "proposal"
        ]
    
    def _sync_to_hub(self, document: GovernanceDocument) -> None:
        """
        Sync document to Membase Hub
        In production: kb.add_documents(document)
        """
        # Placeholder for hub sync
        # from membase.knowledge.document import Document
        # doc = Document(
        #     content=document.content,
        #     metadata=document.metadata
        # )
        # self.kb.add_documents(doc)
        pass
    
    def get_document_count(self) -> dict:
        """Get count of documents by type"""
        counts = {}
        for doc in self.documents.values():
            counts[doc.doc_type] = counts.get(doc.doc_type, 0) + 1
        return counts
