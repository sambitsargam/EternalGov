"""
EternalGov - Immortal AI DAO Delegate with Decentralized Memory
"""

from config.config import get_config
from data_ingestion_service import DataIngestionService
from membase_auth import MembaseAuth
import json
from datetime import datetime


class EternalGov:
    """Main orchestrator for EternalGov AI DAO Delegate"""
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.data_service = DataIngestionService()
        self.membase_auth = MembaseAuth()
        # Load credentials from .env file
        self.membase_auth.load_from_env_file()
        self.is_initialized = False
        self.voting_mode = False
        
    def initialize(self):
        """Initialize the system"""
        try:
            self.is_initialized = True
            return {
                "status": "success",
                "message": "EternalGov initialized successfully",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_status(self):
        """Get current system status"""
        try:
            data = self.data_service.get_ingested_data()
            creds = self.membase_auth.get_credentials()
            return {
                "initialized": self.is_initialized,
                "voting_mode": self.voting_mode,
                "data_ingestion": {
                    "status": "active" if data else "idle",
                    "proposals_count": len(data.get("proposals", [])) if data else 0,
                    "documents_count": len(data.get("documents", [])) if data else 0
                },
                "membase": {
                    "connected": bool(creds.get("membase_id")),
                    "agent_id": creds.get("membase_id", "Not configured")
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "data_ingestion": {"proposals_count": 0, "documents_count": 0},
                "membase": {"connected": False}
            }
    
    def start_data_ingestion(self):
        """Start data ingestion process"""
        try:
            result = self.data_service.ingest_all()
            return {
                "status": "success",
                "message": "Data ingestion started",
                "data": result
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def enable_voting_mode(self):
        """Enable autonomous voting mode"""
        self.voting_mode = True
        return {"status": "success", "voting_mode": True}
    
    def disable_voting_mode(self):
        """Disable autonomous voting mode"""
        self.voting_mode = False
        return {"status": "success", "voting_mode": False}
    
    def analyze_proposal(self, proposal_id: str):
        """Analyze a proposal"""
        try:
            # Placeholder for proposal analysis
            return {
                "proposal_id": proposal_id,
                "recommendation": "HOLD",
                "confidence": 0.75,
                "reasoning": "Insufficient data for recommendation"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
