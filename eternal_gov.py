"""
Main Orchestrator for EternalGov
Coordinates all components for autonomous governance
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime

from src.membase import AgentIdentity, MembaseMemoryManager, GovernanceKnowledgeBase
from src.data_ingestion import DataAggregator
from src.memory_layers import (
    ProposalMemory, SentimentMemory, PreferenceMemory, OutcomeMemory
)
from src.reasoning import VoteReasoning, JustificationReporter
from src.blockchain import ChainRegistry, VoteCaster


class EternalGov:
    """
    The Immortal AI DAO Delegate
    Coordinates decentralized memory, governance analysis, and autonomous voting
    """
    
    def __init__(self, config: Dict):
        """
        Initialize EternalGov
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.start_time = datetime.utcnow()
        
        # Initialize Membase components
        self.identity = AgentIdentity("EternalGov")
        self.memory_manager = MembaseMemoryManager(
            membase_account=config["membase"]["account"]
        )
        self.knowledge_base = GovernanceKnowledgeBase(
            membase_account=config["membase"]["account"]
        )
        
        # Initialize data ingestion
        self.aggregator = DataAggregator()
        
        # Initialize memory layers
        self.proposal_memory = ProposalMemory(config["membase"]["account"])
        self.sentiment_memory = SentimentMemory(config["membase"]["account"])
        self.preference_memory = PreferenceMemory(config["membase"]["account"])
        self.outcome_memory = OutcomeMemory(config["membase"]["account"])
        
        # Initialize reasoning
        self.vote_reasoning = VoteReasoning()
        self.justification_reporter = JustificationReporter()
        
        # Initialize blockchain
        self.chain_registry = ChainRegistry(config["blockchain"]["rpc_url"])
        self.vote_caster = VoteCaster(config["blockchain"]["delegate_address"])
        
        print("[INIT] EternalGov initialized successfully")
    
    async def register_identity(self) -> bool:
        """
        Register EternalGov's identity on-chain
        
        Returns:
            True if successful
        """
        print("[REGISTER] Registering EternalGov delegate on-chain...")
        
        self.identity.register_on_chain()
        
        tx_hash = self.chain_registry.register_delegate(
            delegate_address=self.config["blockchain"]["delegate_address"],
            agent_name="EternalGov",
            membase_id=self.identity.membase_id
        )
        
        print("[REGISTER] Identity registration complete")
        return True
    
    async def ingest_governance_data(self, dao_name: str) -> Dict:
        """
        Ingest all governance data for a DAO
        
        Args:
            dao_name: Name of DAO to ingest
            
        Returns:
            Dictionary of aggregated data
        """
        print(f"[INGEST] Gathering governance data for {dao_name}...")
        
        from config.config import SUPPORTED_DAOS, GOVERNANCE_FORUMS, TWITTER_HANDLES
        
        dao_config = SUPPORTED_DAOS.get(dao_name)
        if not dao_config:
            return {}
        
        # Aggregate data
        data = self.aggregator.aggregate_dao_governance(
            dao_name=dao_name,
            snapshot_space=dao_config["space"],
            governance_forums=[GOVERNANCE_FORUMS.get(dao_name, "")],
            twitter_handles=TWITTER_HANDLES
        )
        
        # Store proposals in memory
        for proposal in data.get("proposals", []):
            self.proposal_memory.store_proposal(
                proposal_id=proposal.proposal_id if hasattr(proposal, 'proposal_id') else str(proposal),
                dao=dao_name,
                title=getattr(proposal, 'title', 'Unknown'),
                body=getattr(proposal, 'body', ''),
                author=getattr(proposal, 'author', 'Unknown'),
                created_at=getattr(proposal, 'created_at', ''),
                end_time=getattr(proposal, 'end_time', ''),
                choices=getattr(proposal, 'choices', []),
                url=getattr(proposal, 'url', '')
            )
        
        print(f"[INGEST] Ingested {len(data.get('proposals', []))} proposals")
        return data
    
    async def analyze_proposal(self, proposal_id: str, dao_name: str) -> Dict:
        """
        Analyze a governance proposal
        
        Args:
            proposal_id: Proposal ID
            dao_name: DAO name
            
        Returns:
            Analysis results
        """
        print(f"[ANALYZE] Analyzing proposal {proposal_id}...")
        
        # Fetch proposal details
        proposal = self.proposal_memory.get_proposal(proposal_id)
        if not proposal:
            print(f"[ANALYZE] Proposal {proposal_id} not found in memory")
            return {}
        
        # Get sentiment data
        sentiment = self.sentiment_memory.get_proposal_sentiment(proposal_id)
        
        # Get community consensus
        consensus = self.sentiment_memory.get_community_consensus(proposal_id)
        
        # Get preference alignment
        preference_prediction = self.preference_memory.predict_proposal_preference({
            "category": proposal.category
        })
        
        print(f"[ANALYZE] Analysis complete. Consensus: {consensus}")
        
        return {
            "proposal_id": proposal_id,
            "sentiment": sentiment,
            "community_consensus": consensus,
            "preference_prediction": preference_prediction
        }
    
    async def generate_vote_recommendation(
        self,
        proposal_id: str,
        dao_name: str
    ) -> Optional[Dict]:
        """
        Generate a vote recommendation for a proposal
        
        Args:
            proposal_id: Proposal ID
            dao_name: DAO name
            
        Returns:
            Vote decision and justification
        """
        print(f"[VOTE] Generating vote recommendation for {proposal_id}...")
        
        proposal = self.proposal_memory.get_proposal(proposal_id)
        if not proposal:
            return None
        
        # Build reasoning context
        from src.reasoning.vote_reasoning import ReasoningContext
        
        sentiment = self.sentiment_memory.get_proposal_sentiment(proposal_id)
        
        context = ReasoningContext(
            proposal_id=proposal_id,
            proposal_title=proposal.title,
            proposal_body=proposal.body,
            dao=dao_name,
            voting_options=proposal.choices,
            community_sentiment=sentiment.get("by_source", {}),
            historical_preferences={"support": 0.6},  # Placeholder
            similar_past_proposals=[],
            arguments_for=[],
            arguments_against=[],
            expected_impact=proposal.expected_impact
        )
        
        # Generate decision
        decision = self.vote_reasoning.analyze_proposal(context)
        
        # Create justification report
        report = self.justification_reporter.create_justification_report(
            proposal_id=proposal_id,
            vote_choice=decision.choice,
            confidence=decision.confidence,
            reasoning=decision.reasoning_summary,
            sentiment_data=sentiment.get("by_source", {}),
            preference_alignment=decision.alignment_with_dao_values,
            risk_level=decision.risk_assessment,
            data_sources={
                "sentiment_analysis": "Multi-source sentiment aggregation",
                "historical_patterns": "Preference memory learning",
                "proposal_analysis": "LLM-based reasoning"
            }
        )
        
        print(f"[VOTE] Recommendation: {decision.choice} (confidence: {decision.confidence:.1%})")
        
        return {
            "decision": decision,
            "report": report,
            "markdown_report": self.justification_reporter.get_full_report_markdown(proposal_id)
        }
    
    async def cast_vote(
        self,
        proposal_id: str,
        choice: str,
        dao_name: str,
        justification_hash: str
    ) -> bool:
        """
        Cast a vote on a proposal
        
        Args:
            proposal_id: Proposal ID
            choice: Vote choice
            dao_name: DAO name
            justification_hash: Hash of justification
            
        Returns:
            True if vote cast successfully
        """
        print(f"[VOTE-CAST] Casting vote on {proposal_id}: {choice}")
        
        if self.config["voting"]["require_approval"]:
            # Requires human approval
            self.vote_caster.cast_vote_with_delegation_option(
                proposal_id=proposal_id,
                choice=choice,
                dao=dao_name,
                justification_hash=justification_hash,
                allow_human_override=True
            )
            print(f"[VOTE-CAST] Vote pending human approval")
            return True
        else:
            # Cast directly
            self.vote_caster.cast_vote_on_chain(
                proposal_id=proposal_id,
                dao_governance_contract=dao_name,
                choice=choice,
                justification_hash=justification_hash
            )
            print(f"[VOTE-CAST] Vote cast on-chain")
            return True
    
    def get_status(self) -> Dict:
        """Get current status of EternalGov"""
        
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            "agent_name": "EternalGov",
            "identity": self.identity.to_dict(),
            "uptime_seconds": uptime,
            "registered_on_chain": self.chain_registry.verify_on_chain(
                self.config["blockchain"]["delegate_address"]
            ),
            "memory_status": {
                "proposals_stored": len(self.proposal_memory.proposals),
                "sentiment_entries": len(self.sentiment_memory.sentiment_entries),
                "outcomes_recorded": len(self.outcome_memory.outcomes),
            },
            "voting_status": {
                "votes_cast": len(self.vote_caster.votes_cast),
                "pending_votes": len(self.vote_caster.pending_votes),
                "prediction_accuracy": self.outcome_memory.get_prediction_accuracy(),
            },
            "last_update": datetime.utcnow().isoformat(),
        }
    
    async def run_governance_cycle(self, dao_name: str):
        """
        Execute a complete governance analysis cycle
        
        Args:
            dao_name: DAO to analyze
        """
        print(f"\n[CYCLE] Starting governance cycle for {dao_name}")
        
        try:
            # Ingest data
            data = await self.ingest_governance_data(dao_name)
            
            # Analyze active proposals
            for proposal in data.get("proposals", [])[:3]:  # Analyze first 3
                proposal_id = getattr(proposal, 'proposal_id', str(proposal))
                
                # Analyze
                await self.analyze_proposal(proposal_id, dao_name)
                
                # Generate recommendation
                recommendation = await self.generate_vote_recommendation(proposal_id, dao_name)
                
                if recommendation and self.config["voting"]["autonomous"]:
                    # Cast vote
                    await self.cast_vote(
                        proposal_id=proposal_id,
                        choice=recommendation["decision"].choice,
                        dao_name=dao_name,
                        justification_hash=recommendation["report"].reasoning_hash
                    )
            
            print(f"[CYCLE] Governance cycle complete")
            print(f"[STATUS]\n{self.get_status()}")
            
        except Exception as e:
            print(f"[ERROR] Governance cycle failed: {str(e)}")


async def main():
    """Main entry point"""
    
    from config.config import get_config
    
    print("=" * 60)
    print("EternalGov: The Immortal AI DAO Delegate")
    print("Powered by Unibase's Decentralized Membase")
    print("=" * 60)
    
    config = get_config()
    governor = EternalGov(config)
    
    # Register identity
    await governor.register_identity()
    
    # Run governance cycle for each DAO
    for dao_name in ["uniswap", "aave"]:
        await governor.run_governance_cycle(dao_name)
    
    # Show final status
    print("\n" + "=" * 60)
    print("FINAL STATUS")
    print("=" * 60)
    import json
    print(json.dumps(governor.get_status(), indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
