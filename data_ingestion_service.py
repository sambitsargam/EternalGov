"""
EternalGov Data Ingestion Service
Handles autonomous governance data collection and storage
"""

from datetime import datetime
from typing import Dict, List
from config.config import get_config
from mock_data import MockGovernanceData
import json
import os


class DataIngestionService:
    """Service for continuous governance data ingestion and storage"""
    
    def __init__(self):
        self.config = get_config()
        self.daos = ["uniswap", "aave", "compound", "makerdao"]
        self.ingestion_results = {}
        self.storage_dir = "/tmp/eternalgov_membase_storage"
        self._ensure_storage_exists()
        
    def _ensure_storage_exists(self):
        """Ensure storage directories exist"""
        os.makedirs(f"{self.storage_dir}/proposals", exist_ok=True)
        os.makedirs(f"{self.storage_dir}/documents", exist_ok=True)
        os.makedirs(f"{self.storage_dir}/conversations", exist_ok=True)
        
    def ingest_all(self) -> Dict:
        """Ingest governance data for all DAOs"""
        print("\n" + "=" * 70)
        print("GOVERNANCE DATA INGESTION")
        print("=" * 70)
        
        all_proposals = []
        all_documents = []
        
        for dao in self.daos:
            print(f"\n[{dao.upper()}] Starting data ingestion...")
            
            try:
                # Get mock governance data
                proposals = MockGovernanceData.get_mock_proposals(dao)
                sentiment_data = MockGovernanceData.get_mock_sentiment(dao)
                
                # Store proposals
                for proposal in proposals:
                    filename = f"{self.storage_dir}/proposals/{proposal['id']}.json"
                    with open(filename, 'w') as f:
                        json.dump(proposal, f, indent=2)
                    all_proposals.append(proposal)
                    print(f"  ✅ Stored proposal: {proposal['id']}")
                
                # Store sentiment data (dict of proposal_id -> sentiment)
                if isinstance(sentiment_data, dict):
                    for prop_id, sentiment_entry in sentiment_data.items():
                        filename = f"{self.storage_dir}/documents/{prop_id}_sentiment.json"
                        sentiment_entry['id'] = prop_id
                        with open(filename, 'w') as f:
                            json.dump(sentiment_entry, f, indent=2)
                        all_documents.append(sentiment_entry)
                
                self.ingestion_results[dao] = {
                    "status": "success",
                    "proposals": len(proposals),
                    "timestamp": datetime.now().isoformat()
                }
                print(f"  ✅ {dao.upper()}: {len(proposals)} proposals ingested")
                
            except Exception as e:
                self.ingestion_results[dao] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"  ❌ Error ingesting {dao}: {str(e)}")
        
        return {
            "proposals": all_proposals,
            "documents": all_documents,
            "results": self.ingestion_results,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_ingested_data(self) -> Dict:
        """Get all ingested data from storage"""
        proposals = []
        documents = []
        conversations = []
        
        # Load proposals
        proposal_dir = f"{self.storage_dir}/proposals"
        if os.path.exists(proposal_dir):
            for filename in os.listdir(proposal_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(proposal_dir, filename), 'r') as f:
                        proposals.append(json.load(f))
        
        # Load documents
        doc_dir = f"{self.storage_dir}/documents"
        if os.path.exists(doc_dir):
            for filename in os.listdir(doc_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(doc_dir, filename), 'r') as f:
                        documents.append(json.load(f))
        
        # Load conversations
        conv_dir = f"{self.storage_dir}/conversations"
        if os.path.exists(conv_dir):
            for filename in os.listdir(conv_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(conv_dir, filename), 'r') as f:
                        conversations.append(json.load(f))
        
        return {
            "proposals": proposals,
            "documents": documents,
            "conversations": conversations,
            "total": len(proposals) + len(documents) + len(conversations)
        }
    
    def get_status(self) -> Dict:
        """Get ingestion status"""
        data = self.get_ingested_data()
        return {
            "status": "active",
            "data_stored": data["total"],
            "proposals": len(data["proposals"]),
            "documents": len(data["documents"]),
            "conversations": len(data["conversations"]),
            "results": self.ingestion_results,
            "timestamp": datetime.now().isoformat()
        }
