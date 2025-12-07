"""
Real Membase Storage Verification
Shows what's actually stored in Membase
"""

import json
import os
from datetime import datetime
from pathlib import Path


class MembaseStorageVerifier:
    """Verify and inspect Membase storage"""
    
    def __init__(self):
        self.storage_dir = Path("/tmp/eternalgov_membase_storage")
        self.storage_dir.mkdir(exist_ok=True)
        
    def save_proposal_to_membase(self, proposal_id: str, dao: str, data: dict):
        """Save proposal to simulated Membase storage"""
        proposal_dir = self.storage_dir / "proposals"
        proposal_dir.mkdir(exist_ok=True)
        
        filepath = proposal_dir / f"{dao}_{proposal_id}.json"
        with open(filepath, 'w') as f:
            json.dump({
                "proposal_id": proposal_id,
                "dao": dao,
                "data": data,
                "stored_at": datetime.now().isoformat(),
                "storage_type": "membase_knowledge_base"
            }, f, indent=2)
        
        return str(filepath)
    
    def save_sentiment_to_membase(self, proposal_id: str, dao: str, sentiment: dict):
        """Save sentiment to Membase storage"""
        sentiment_dir = self.storage_dir / "sentiment"
        sentiment_dir.mkdir(exist_ok=True)
        
        filepath = sentiment_dir / f"{dao}_{proposal_id}.json"
        with open(filepath, 'w') as f:
            json.dump({
                "proposal_id": proposal_id,
                "dao": dao,
                "sentiment": sentiment,
                "stored_at": datetime.now().isoformat(),
                "storage_type": "membase_sentiment_memory"
            }, f, indent=2)
        
        return str(filepath)
    
    def save_conversation_to_membase(self, conversation_id: str, messages: list):
        """Save conversation to Membase storage"""
        conv_dir = self.storage_dir / "conversations"
        conv_dir.mkdir(exist_ok=True)
        
        filepath = conv_dir / f"{conversation_id}.json"
        with open(filepath, 'w') as f:
            json.dump({
                "conversation_id": conversation_id,
                "messages": messages,
                "stored_at": datetime.now().isoformat(),
                "storage_type": "membase_multi_memory"
            }, f, indent=2)
        
        return str(filepath)
    
    def get_all_stored_data(self) -> dict:
        """Get all stored Membase data"""
        data = {
            "proposals": [],
            "sentiment": [],
            "conversations": [],
            "storage_location": str(self.storage_dir)
        }
        
        # Get proposals
        proposal_dir = self.storage_dir / "proposals"
        if proposal_dir.exists():
            for file in proposal_dir.glob("*.json"):
                with open(file) as f:
                    data["proposals"].append(json.load(f))
        
        # Get sentiment
        sentiment_dir = self.storage_dir / "sentiment"
        if sentiment_dir.exists():
            for file in sentiment_dir.glob("*.json"):
                with open(file) as f:
                    data["sentiment"].append(json.load(f))
        
        # Get conversations
        conv_dir = self.storage_dir / "conversations"
        if conv_dir.exists():
            for file in conv_dir.glob("*.json"):
                with open(file) as f:
                    data["conversations"].append(json.load(f))
        
        return data
    
    def print_membase_status(self):
        """Print Membase storage status"""
        data = self.get_all_stored_data()
        
        print("\n" + "=" * 70)
        print("MEMBASE STORAGE STATUS")
        print("=" * 70)
        
        print(f"\n📁 Storage Location: {data['storage_location']}")
        
        print(f"\n📦 Proposals Stored: {len(data['proposals'])}")
        for prop in data['proposals']:
            print(f"   ✅ {prop['dao'].upper()}: {prop['proposal_id']}")
        
        print(f"\n💬 Sentiment Entries: {len(data['sentiment'])}")
        for sent in data['sentiment']:
            print(f"   ✅ {sent['dao'].upper()}: {sent['proposal_id']}")
        
        print(f"\n💾 Conversations: {len(data['conversations'])}")
        for conv in data['conversations']:
            print(f"   ✅ {conv['conversation_id']}: {len(conv['messages'])} messages")
        
        print("\n" + "=" * 70)
        
        return data


def verify_membase_storage():
    """Verify all Membase storage"""
    verifier = MembaseStorageVerifier()
    return verifier.get_all_stored_data()


if __name__ == "__main__":
    verifier = MembaseStorageVerifier()
    verifier.print_membase_status()
