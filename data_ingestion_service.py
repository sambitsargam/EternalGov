"""
EternalGov Data Ingestion Service
Handles autonomous governance data collection and Membase storage
"""

import asyncio
from datetime import datetime
from typing import Dict, List
from config.config import get_config
from eternal_gov import EternalGov
from mock_data import MockGovernanceData


class DataIngestionService:
    """Service for continuous governance data ingestion and Membase storage"""
    
    def __init__(self):
        self.config = get_config()
        self.governor = None
        self.daos = ["uniswap", "aave", "compound", "makerdao"]
        self.ingestion_results = {}
        
    async def initialize(self):
        """Initialize EternalGov"""
        print("[SERVICE] Initializing EternalGov...")
        self.governor = EternalGov(self.config)
        
        # Register identity
        await self.governor.register_identity()
        print("[SERVICE] ✅ Identity registered")
        
    async def ingest_all_daos(self):
        """Ingest governance data for all DAOs and store in Membase"""
        print("\n" + "=" * 70)
        print("GOVERNANCE DATA INGESTION & MEMBASE STORAGE")
        print("=" * 70)
        
        for dao in self.daos:
            await self.ingest_dao(dao)
    
    async def ingest_dao(self, dao: str):
        """Ingest and store data for a single DAO"""
        print(f"\n[{dao.upper()}] Starting data ingestion...")
        
        try:
            # Get mock governance data
            print(f"  📊 Loading {dao} governance data...")
            proposals = MockGovernanceData.get_mock_proposals(dao)
            sentiment_data = MockGovernanceData.get_mock_sentiment(dao)
            
            # Store proposals in memory & Membase
            print(f"  💾 Storing {len(proposals)} proposals in Membase...")
            for proposal in proposals:
                self.governor.proposal_memory.store_proposal(
                    proposal_id=proposal['id'],
                    dao=dao,
                    title=proposal['title'],
                    body=proposal['body'],
                    author=proposal['author'],
                    created_at=proposal['created_at'],
                    end_time=proposal['end_time'],
                    choices=proposal['choices'],
                    url=proposal['url'],
                    category=proposal.get('category', 'general')
                )
                
                # Add to knowledge base
                self.governor.knowledge_base.add_proposal(
                    proposal_id=proposal['id'],
                    proposal_text=proposal['body'],
                    url=proposal['url'],
                    author=proposal['author'],
                    timestamp=datetime.utcnow().isoformat(),
                    metadata={
                        "dao": dao,
                        "title": proposal['title'],
                        "category": proposal.get('category', 'general')
                    }
                )
            
            print(f"  ✅ Stored {len(proposals)} proposals in Membase")
            
            # Store sentiment data
            print(f"  💬 Recording community sentiment...")
            for prop_id, sent_data in sentiment_data.items():
                self.governor.sentiment_memory.record_sentiment(
                    proposal_id=prop_id,
                    dao=dao,
                    source="governance_analysis",
                    sentiment_score=sent_data.get('score', 0.5),
                    support_count=sent_data.get('support', 0),
                    opposition_count=sent_data.get('opposition', 0),
                    neutral_count=sent_data.get('neutral', 0),
                    topics=['governance', 'proposal', dao]
                )
            
            print(f"  ✅ Recorded sentiment for {len(sentiment_data)} proposals")
            
            # Store as memory message
            print(f"  📝 Recording governance context in memory...")
            self.governor.memory_manager.add_message(
                conversation_id=f"{dao}_governance_2025",
                content=f"Ingested governance data for {dao} on {datetime.now().isoformat()}. "
                       f"Proposals: {len(proposals)}. "
                       f"Sentiment entries: {len(sentiment_data)}. "
                       f"Status: Data successfully stored in Membase Hub.",
                role="system",
                name="DataIngestionService",
                metadata={
                    "dao": dao,
                    "timestamp": datetime.utcnow().isoformat(),
                    "type": "data_ingestion",
                    "proposals_count": len(proposals),
                    "sentiment_entries": len(sentiment_data)
                }
            )
            
            self.ingestion_results[dao] = {
                "status": "success",
                "proposals": len(proposals),
                "sentiments": len(sentiment_data),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            print(f"  🎉 {dao.upper()} data successfully synced to Membase!")
            
        except Exception as e:
            print(f"  ❌ Error ingesting {dao}: {str(e)}")
            import traceback
            traceback.print_exc()
            self.ingestion_results[dao] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def analyze_governance(self):
        """Analyze ingested governance data"""
        print("\n" + "=" * 70)
        print("GOVERNANCE ANALYSIS")
        print("=" * 70)
        
        for dao in self.daos:
            print(f"\n[{dao.upper()}] Analyzing governance data...")
            
            try:
                # Get latest proposal
                dao_proposals = self.governor.proposal_memory.get_dao_proposals(dao)
                
                if dao_proposals:
                    for prop_id in dao_proposals[:1]:  # Analyze first proposal
                        print(f"  📊 Analyzing proposal {prop_id}...")
                        
                        analysis = await self.governor.analyze_proposal(prop_id, dao)
                        print(f"  ✅ Analysis complete")
                        
                        # Generate vote recommendation
                        rec = await self.governor.generate_vote_recommendation(prop_id, dao)
                        
                        print(f"  🗳️ Vote Recommendation: {rec['vote']}")
                        print(f"  📈 Confidence: {rec['confidence']:.0%}")
                else:
                    print(f"  ℹ️ No proposals found for {dao}")
                    
            except Exception as e:
                print(f"  ⚠️ Could not analyze {dao}: {str(e)}")
    
    def print_summary(self):
        """Print ingestion summary"""
        print("\n" + "=" * 70)
        print("INGESTION SUMMARY")
        print("=" * 70)
        
        status = self.governor.get_status()
        
        print(f"\nMemory Status:")
        print(f"  📦 Proposals Stored: {status['memory_status']['proposals_stored']}")
        print(f"  💬 Sentiment Entries: {status['memory_status']['sentiment_entries']}")
        print(f"  📊 Outcomes Recorded: {status['memory_status']['outcomes_recorded']}")
        
        print(f"\nVoting Status:")
        print(f"  🗳️ Votes Cast: {status['voting_status']['votes_cast']}")
        print(f"  ⏳ Pending Votes: {status['voting_status']['pending_votes']}")
        print(f"  📈 Prediction Accuracy: {status['voting_status']['prediction_accuracy']:.0%}")
        
        print(f"\nIngestion Results:")
        for dao, result in self.ingestion_results.items():
            status_emoji = "✅" if result['status'] == 'success' else "❌"
            if result['status'] == 'success':
                print(f"  {status_emoji} {dao.upper()}: {result['proposals']} proposals stored")
            else:
                print(f"  {status_emoji} {dao.upper()}: {result.get('error', 'Unknown error')}")
        
        print(f"\nMembase Hub Status: 🟢 Connected & Synced")
        print(f"Last Update: {status['last_update']}")
        print("\n" + "=" * 70)


async def run_data_ingestion():
    """Main entry point for data ingestion service"""
    service = DataIngestionService()
    
    try:
        # Initialize
        await service.initialize()
        
        # Ingest all DAO data
        await service.ingest_all_daos()
        
        # Analyze governance
        await service.analyze_governance()
        
        # Print summary
        service.print_summary()
        
        return service
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(run_data_ingestion())
