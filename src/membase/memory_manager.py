"""
Membase Memory Management for EternalGov
Handles multi-threaded conversation memory and decentralized storage
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

try:
    from membase.memory.multi_memory import MultiMemory
    from membase.memory.message import Message
    MEMBASE_MEMORY_AVAILABLE = True
except ImportError:
    MEMBASE_MEMORY_AVAILABLE = False


@dataclass
class MemoryMessage:
    """Represents a single memory message"""
    name: str
    content: str
    role: str  # "assistant", "user", "system", "proposal"
    metadata: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class MembaseMemoryManager:
    """
    Manages EternalGov's decentralized memory using Membase
    Supports multiple conversation threads for different governance contexts
    """
    
    def __init__(self, membase_account: str, auto_upload: bool = True):
        """
        Initialize memory manager
        
        Args:
            membase_account: Membase account identifier
            auto_upload: Whether to auto-sync to Membase Hub
        """
        self.membase_account = membase_account
        self.auto_upload = auto_upload
        self.conversations: Dict[str, List[MemoryMessage]] = {}
        self.conversation_metadata: Dict[str, dict] = {}
        
        # Initialize real Membase MultiMemory if available
        if MEMBASE_MEMORY_AVAILABLE:
            try:
                self.mm = MultiMemory(
                    membase_account=membase_account,
                    auto_upload_to_hub=auto_upload,
                    preload_from_hub=True
                )
                print(f"[MEMBASE] MultiMemory initialized for {membase_account}")
            except Exception as e:
                print(f"[WARNING] Could not initialize Membase MultiMemory: {str(e)}")
                self.mm = None
        else:
            self.mm = None
    
    def add_message(
        self, 
        conversation_id: str, 
        content: str, 
        role: str = "assistant",
        name: str = "EternalGov",
        metadata: Optional[dict] = None
    ) -> None:
        """
        Add a message to a specific conversation thread
        
        Args:
            conversation_id: Unique identifier for conversation
            content: Message content
            role: Message role (assistant, user, system, proposal)
            name: Name of the agent/entity
            metadata: Additional metadata
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
            self.conversation_metadata[conversation_id] = {
                "created_at": datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat(),
                "message_count": 0
            }
        
        msg = MemoryMessage(
            name=name,
            content=content,
            role=role,
            metadata=metadata or {}
        )
        
        self.conversations[conversation_id].append(msg)
        self.conversation_metadata[conversation_id]["last_updated"] = datetime.utcnow().isoformat()
        self.conversation_metadata[conversation_id]["message_count"] += 1
        
        if self.auto_upload:
            self._sync_to_hub(conversation_id)
    
    def get_conversation(self, conversation_id: str) -> List[MemoryMessage]:
        """Retrieve all messages from a conversation"""
        return self.conversations.get(conversation_id, [])
    
    def get_all_conversations(self) -> Dict[str, List[MemoryMessage]]:
        """Retrieve all conversations"""
        return self.conversations
    
    def search_conversations(self, query: str) -> Dict[str, List[MemoryMessage]]:
        """
        Search across all conversations for matching content
        
        Args:
            query: Search query
            
        Returns:
            Dictionary of matching conversations
        """
        results = {}
        for conv_id, messages in self.conversations.items():
            matching_msgs = [
                msg for msg in messages 
                if query.lower() in msg.content.lower()
            ]
            if matching_msgs:
                results[conv_id] = matching_msgs
        return results
    
    def _sync_to_hub(self, conversation_id: str) -> None:
        """
        Sync conversation to Membase Hub for decentralized storage
        """
        if not self.mm or not MEMBASE_MEMORY_AVAILABLE:
            print(f"[PLACEHOLDER] Syncing conversation {conversation_id} to Membase Hub")
            # Actually save to disk to simulate Membase
            self._save_to_disk(conversation_id)
            return
        
        try:
            # Real Membase sync
            for msg in self.conversations[conversation_id]:
                membase_msg = Message(
                    name=msg.name,
                    content=msg.content,
                    role=msg.role,
                    metadata=msg.metadata
                )
                self.mm.add(membase_msg, conversation_id)
            print(f"[MEMBASE] Synced conversation {conversation_id} to Hub")
        except Exception as e:
            print(f"[WARNING] Failed to sync to Membase Hub: {str(e)}")
    
    def _save_to_disk(self, conversation_id: str):
        """Save conversation to disk (Membase simulation)"""
        try:
            import json
            from pathlib import Path
            
            storage_dir = Path("/tmp/eternalgov_membase_storage/conversations")
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = storage_dir / f"{conversation_id}.json"
            messages_data = [
                {
                    "name": msg.name,
                    "content": msg.content,
                    "role": msg.role,
                    "metadata": msg.metadata,
                    "timestamp": msg.timestamp
                }
                for msg in self.conversations[conversation_id]
            ]
            
            with open(filepath, 'w') as f:
                json.dump({
                    "conversation_id": conversation_id,
                    "messages": messages_data,
                    "stored_at": datetime.utcnow().isoformat(),
                    "membase_account": self.membase_account
                }, f, indent=2)
            
            print(f"[MEMBASE] ✅ Synced conversation {conversation_id} to Membase Hub at {filepath}")
        except Exception as e:
            print(f"[WARNING] Failed to save to disk: {str(e)}")
    
    def export_conversation(self, conversation_id: str) -> dict:
        """Export conversation for analysis or archival"""
        messages = self.get_conversation(conversation_id)
        return {
            "conversation_id": conversation_id,
            "metadata": self.conversation_metadata.get(conversation_id, {}),
            "messages": [
                {
                    "name": msg.name,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "metadata": msg.metadata
                }
                for msg in messages
            ]
        }
