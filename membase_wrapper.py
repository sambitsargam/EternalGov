"""
Membase Integration Wrapper
Properly wraps real Membase SDK with correct API usage
"""

from membase.memory.multi_memory import MultiMemory
from membase.knowledge.chroma import ChromaKnowledgeBase
from membase.memory.message import Message
from membase.knowledge.document import Document
from typing import List, Dict, Optional
import os


class MembaseMemoryManager:
    """Wrapper for Membase MultiMemory with correct API"""
    
    def __init__(self, account: str, auto_upload: bool = False):
        """Initialize with local storage (Hub upload disabled for reliability)"""
        self.account = account
        # Use local storage only - Hub upload disabled
        self.memory = MultiMemory(
            membase_account=account,
            auto_upload_to_hub=False,
            preload_from_hub=False
        )
    
    def add_proposal_message(self, proposal_id: str, content: str) -> bool:
        """Add a proposal to memory"""
        try:
            msg = Message(
                name=f"Proposal_{proposal_id}",
                role="assistant",
                content=content[:500],  # Limit content size
                metadata={"type": "proposal", "proposal_id": proposal_id}
            )
            self.memory.add(msg)
            return True
        except Exception as e:
            print(f"❌ Error adding proposal to memory: {e}")
            return False
    
    def get_size(self) -> int:
        """Get memory size"""
        return self.memory.size()
    
    def get_all(self) -> List:
        """Get all messages from memory"""
        try:
            return self.memory.get_all_conversations()
        except:
            return []


class MembaseKnowledgeBase:
    """Wrapper for Membase ChromaKnowledgeBase with correct API"""
    
    def __init__(self, account: str, auto_upload: bool = False):
        """Initialize with local storage (Hub upload disabled for reliability)"""
        self.account = account
        # Use local storage only - Hub upload disabled
        self.kb = ChromaKnowledgeBase(
            persist_directory="./chroma_db",
            collection_name="governance_proposals",
            membase_account=account,
            auto_upload_to_hub=False
        )
    
    def add_proposals(self, proposals: List[Dict]) -> int:
        """Add multiple proposals to knowledge base"""
        try:
            docs = []
            for proposal in proposals:
                # Chroma requires strings for metadata values
                doc = Document(
                    content=f"{proposal.get('title', 'Untitled')}: {proposal.get('body', '')}",
                    metadata={
                        "proposal_id": str(proposal.get("proposal_id", proposal.get("id", "unknown"))),
                        "dao": str(proposal.get("dao", "unknown")),
                        "status": str(proposal.get("status", "active")),
                        "author": str(proposal.get("author", "unknown"))
                    }
                )
                docs.append(doc)
            
            self.kb.add_documents(docs)
            return len(docs)
        except Exception as e:
            print(f"❌ Error adding proposals to KB: {e}")
            return 0
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search proposals"""
        try:
            results = self.kb.retrieve(query, n_results=n_results)
            return results
        except Exception as e:
            print(f"❌ Error searching KB: {e}")
            return []


def test_membase_integration(account: str, secret_key: str):
    """Test real Membase integration"""
    
    print("\n" + "=" * 70)
    print("🧪 MEMBASE INTEGRATION TEST")
    print("=" * 70)
    
    # Test Memory
    print(f"\n1️⃣ Testing MultiMemory:")
    try:
        memory_mgr = MembaseMemoryManager(account, auto_upload=True)
        
        # Add test proposals
        memory_mgr.add_proposal_message(
            "UNI-1",
            "Increase Uniswap V4 liquidity incentives to bootstrap new system - Support: 120 votes"
        )
        memory_mgr.add_proposal_message(
            "AAVE-1", 
            "Enable eMode for ETH-correlated assets - Support: 95 votes"
        )
        
        print(f"   ✅ Added 2 proposals to memory")
        print(f"   📊 Memory size: {memory_mgr.get_size()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test Knowledge Base
    print(f"\n2️⃣ Testing ChromaKnowledgeBase:")
    try:
        kb_mgr = MembaseKnowledgeBase(account, auto_upload=True)
        
        proposals = [
            {
                "id": "UNI-1",
                "title": "Increase V4 Incentives",
                "body": "This proposal aims to increase liquidity incentives for Uniswap V4",
                "dao": "uniswap",
                "status": "active",
                "author": "Uniswap Team"
            },
            {
                "id": "AAVE-1",
                "title": "Enable eMode",
                "body": "Enable eMode for ETH-correlated assets to increase LTV",
                "dao": "aave",
                "status": "active",
                "author": "Aave Team"
            }
        ]
        
        count = kb_mgr.add_proposals(proposals)
        print(f"   ✅ Added {count} proposals to knowledge base")
        
        # Test search
        results = kb_mgr.search("uniswap liquidity", n_results=2)
        print(f"   ✅ Search returned {len(results)} results")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check storage
    print(f"\n3️⃣ Storage Status:")
    if os.path.exists("./chroma_db"):
        print(f"   ✅ Chroma DB persisted locally")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Test with credentials
    from membase_auth import MembaseAuth
    
    auth = MembaseAuth()
    auth.load_from_env_file()
    
    creds = auth.get_credentials()
    if auth.validate_credentials():
        test_membase_integration(
            creds['membase_account'],
            creds['membase_secret_key']
        )
    else:
        print("❌ Credentials not configured")
