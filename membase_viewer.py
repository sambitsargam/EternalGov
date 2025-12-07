"""
Membase Storage Viewer for Streamlit
Displays all data stored in Membase
"""

import json
from pathlib import Path
from typing import Dict, List


class MembaseStorageViewer:
    """View Membase storage data"""
    
    @staticmethod
    def get_storage_path() -> Path:
        """Get Membase storage directory"""
        return Path("/tmp/eternalgov_membase_storage")
    
    @staticmethod
    def get_proposals() -> List[Dict]:
        """Get all stored proposals"""
        storage_path = MembaseStorageViewer.get_storage_path()
        proposals_dir = storage_path / "proposals"
        
        proposals = []
        if proposals_dir.exists():
            for file in sorted(proposals_dir.glob("*.json")):
                try:
                    with open(file) as f:
                        proposals.append(json.load(f))
                except:
                    pass
        
        return proposals
    
    @staticmethod
    def get_documents() -> List[Dict]:
        """Get all stored documents"""
        storage_path = MembaseStorageViewer.get_storage_path()
        docs_dir = storage_path / "documents"
        
        documents = []
        if docs_dir.exists():
            for file in sorted(docs_dir.glob("*.json")):
                try:
                    with open(file) as f:
                        documents.append(json.load(f))
                except:
                    pass
        
        return documents
    
    @staticmethod
    def get_conversations() -> List[Dict]:
        """Get all stored conversations"""
        storage_path = MembaseStorageViewer.get_storage_path()
        conv_dir = storage_path / "conversations"
        
        conversations = []
        if conv_dir.exists():
            for file in sorted(conv_dir.glob("*.json")):
                try:
                    with open(file) as f:
                        conversations.append(json.load(f))
                except:
                    pass
        
        return conversations
    
    @staticmethod
    def get_sentiment() -> List[Dict]:
        """Get all stored sentiment data"""
        storage_path = MembaseStorageViewer.get_storage_path()
        sentiment_dir = storage_path / "sentiment"
        
        sentiment = []
        if sentiment_dir.exists():
            for file in sorted(sentiment_dir.glob("*.json")):
                try:
                    with open(file) as f:
                        sentiment.append(json.load(f))
                except:
                    pass
        
        return sentiment
    
    @staticmethod
    def get_summary() -> Dict:
        """Get storage summary"""
        return {
            "proposals": len(MembaseStorageViewer.get_proposals()),
            "documents": len(MembaseStorageViewer.get_documents()),
            "conversations": len(MembaseStorageViewer.get_conversations()),
            "sentiment": len(MembaseStorageViewer.get_sentiment()),
            "storage_path": str(MembaseStorageViewer.get_storage_path())
        }
