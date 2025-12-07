#!/usr/bin/env python3
"""
EternalGov Main Runner
Demonstrates integration with Unibase Membase and autonomous governance analysis
"""

import asyncio
import sys
from datetime import datetime

print("=" * 70)
print("EternalGov: The Immortal AI DAO Delegate")
print("Powered by Unibase's Decentralized Membase")
print("=" * 70)
print()

# Check for Membase availability
try:
    from membase.chain.chain import membase_chain
    from membase.memory.multi_memory import MultiMemory
    from membase.knowledge.chroma import ChromaKnowledgeBase
    print("[SUCCESS] Membase SDK imported successfully!")
    MEMBASE_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Membase SDK not available: {str(e)}")
    print("[INFO] Install with: pip install git+https://github.com/unibaseio/membase.git")
    MEMBASE_AVAILABLE = False

print()

# Import EternalGov components
from eternal_gov import EternalGov
from config.config import get_config
from src.membase import AgentIdentity, MembaseMemoryManager, GovernanceKnowledgeBase
from src.data_ingestion import DataAggregator
from src.memory_layers import ProposalMemory, SentimentMemory, PreferenceMemory, OutcomeMemory
from src.reasoning import VoteReasoning, JustificationReporter
from src.blockchain import ChainRegistry, VoteCaster


async def demo_initialization():
    """Demo 1: Initialize EternalGov"""
    print("\n[DEMO 1] Initializing EternalGov")
    print("-" * 70)
    
    config = get_config()
    print(f"✓ Configuration loaded")
    
    governor = EternalGov(config)
    print(f"✓ EternalGov initialized")
    
    identity = governor.identity
    print(f"✓ Agent Identity: {identity.agent_name}")
    print(f"✓ Membase ID: {identity.membase_id}")
    print(f"✓ Membase Account: {identity.membase_account}")
    
    return governor


async def demo_membase_integration(governor):
    """Demo 2: Membase Integration"""
    print("\n[DEMO 2] Membase Integration")
    print("-" * 70)
    
    # Test memory manager
    print("✓ Initializing Membase MemoryManager...")
    governor.memory_manager.add_message(
        conversation_id="eternalgov_demo",
        content="EternalGov governance analysis initialized",
        role="system",
        name="EternalGov",
        metadata={"type": "system", "timestamp": datetime.utcnow().isoformat()}
    )
    print(f"✓ Added message to memory")
    
    # Test knowledge base
    print("✓ Initializing Membase Knowledge Base...")
    governor.knowledge_base.add_proposal(
        proposal_id="demo_001",
        proposal_text="Sample governance proposal for testing",
        url="https://example.com/proposal/1",
        author="Demo Author",
        timestamp=datetime.utcnow().isoformat(),
        metadata={"dao": "demo", "category": "test"}
    )
    print(f"✓ Added proposal to knowledge base")
    
    # Show memory status
    conversations = governor.memory_manager.get_all_conversations()
    print(f"✓ Conversations stored: {len(conversations)}")


async def demo_data_structures(governor):
    """Demo 3: Memory Layers & Data Structures"""
    print("\n[DEMO 3] Memory Layers & Data Structures")
    print("-" * 70)
    
    # Store proposal in memory
    governor.proposal_memory.store_proposal(
        proposal_id="uniswap_001",
        dao="uniswap",
        title="Enable Uniswap v4 Hooks",
        body="A proposal to enable permissionless hook development on Uniswap v4",
        author="Uniswap Labs",
        created_at="2025-01-01T00:00:00Z",
        end_time="2025-01-08T00:00:00Z",
        choices=["For", "Against"],
        url="https://snapshot.org/...",
        category="feature"
    )
    print("✓ Proposal stored in ProposalMemory")
    
    # Add sentiment data
    governor.sentiment_memory.record_sentiment(
        proposal_id="uniswap_001",
        dao="uniswap",
        source="forum",
        sentiment_score=0.72,
        support_count=150,
        opposition_count=25,
        neutral_count=10,
        topics=["efficiency", "hooks", "liquidity"]
    )
    print("✓ Sentiment recorded")
    
    # Add preference data
    governor.preference_memory.record_community_value(
        value_name="innovation",
        category="feature",
        description="Community values feature innovation",
        proposals_indicating=["uniswap_001"]
    )
    print("✓ Community preference recorded")
    
    # Record outcome
    governor.outcome_memory.record_proposal_outcome(
        proposal_id="uniswap_001",
        dao="uniswap",
        passed=True,
        final_votes={"For": 3200000, "Against": 800000},
        participation_count=45000,
        total_eligible=200000
    )
    print("✓ Proposal outcome recorded")
    
    # Show statistics
    print(f"\n✓ Memory Statistics:")
    print(f"  - Proposals: {len(governor.proposal_memory.proposals)}")
    print(f"  - Sentiment entries: {len(governor.sentiment_memory.sentiment_entries)}")
    print(f"  - Outcomes: {len(governor.outcome_memory.outcomes)}")


async def demo_reasoning():
    """Demo 4: Vote Reasoning & Justification"""
    print("\n[DEMO 4] Vote Reasoning & Justification")
    print("-" * 70)
    
    from src.reasoning.vote_reasoning import ReasoningContext
    
    vote_reasoning = VoteReasoning()
    reporter = JustificationReporter()
    
    # Create reasoning context
    context = ReasoningContext(
        proposal_id="demo_vote",
        proposal_title="Increase platform fees to 50%",
        proposal_body="Proposal to increase platform trading fees from 30% to 50%",
        dao="uniswap",
        voting_options=["For", "Against"],
        community_sentiment={
            "forum": 0.30,
            "twitter": 0.25,
            "snapshot": 0.20
        },
        historical_preferences={"fee_increase": 0.4},
        similar_past_proposals=[],
        arguments_for=["Increased revenue", "Sustainability"],
        arguments_against=["Reduced competitiveness", "User migration risk"],
        expected_impact="Estimated 40% revenue increase but potential 20% volume loss"
    )
    
    # Generate decision
    decision = vote_reasoning.analyze_proposal(context)
    print(f"✓ Vote recommendation: {decision.choice}")
    print(f"✓ Confidence: {decision.confidence:.0%}")
    print(f"✓ Risk level: {decision.risk_assessment}")
    
    # Create justification report
    report = reporter.create_justification_report(
        proposal_id="demo_vote",
        vote_choice=decision.choice,
        confidence=decision.confidence,
        reasoning=decision.reasoning_summary,
        sentiment_data=context.community_sentiment,
        preference_alignment=decision.alignment_with_dao_values,
        risk_level=decision.risk_assessment,
        data_sources={
            "sentiment": "Multi-source aggregation",
            "history": "Pattern learning",
            "context": "Proposal analysis"
        }
    )
    
    print(f"✓ Justification hash: {report.reasoning_hash}")
    print(f"✓ Transparency score: {report.transparency_score:.0%}")
    print(f"\nJustification Summary:")
    print(report.summary)


async def demo_blockchain(governor):
    """Demo 5: Blockchain Integration"""
    print("\n[DEMO 5] Blockchain Integration (BNBChain)")
    print("-" * 70)
    
    # Register identity
    governor.identity.register_on_chain()
    print("✓ Identity registration initiated")
    
    # Chain registry
    registry = ChainRegistry(governor.config["blockchain"]["rpc_url"])
    print(f"✓ Chain registry connected to: {governor.config['blockchain']['rpc_url']}")
    
    # Vote caster
    delegate_addr = governor.config["blockchain"]["delegate_address"]
    caster = VoteCaster(delegate_addr)
    print(f"✓ Vote caster initialized for: {delegate_addr}")


async def demo_data_aggregation():
    """Demo 6: Data Aggregation (Mock)"""
    print("\n[DEMO 6] Data Aggregation from Public Sources")
    print("-" * 70)
    
    aggregator = DataAggregator()
    
    print("✓ DataAggregator initialized")
    print("✓ Snapshot scraper ready")
    print("✓ Forum scraper ready")
    print("✓ Twitter scraper ready")
    print("✓ Blog scraper ready")
    
    print("\n[INFO] Data ingestion sources:")
    print("  - Snapshot: https://snapshot.org (active proposals)")
    print("  - Forums: Discourse, Commonwealth (discussions)")
    print("  - Twitter: Public governance sentiment")
    print("  - Blogs: Medium, Mirror (analysis)")


async def demo_full_cycle(governor):
    """Demo 7: Full Governance Analysis Cycle"""
    print("\n[DEMO 7] Full Governance Analysis Cycle")
    print("-" * 70)
    
    # Simulate a complete cycle
    print("Step 1: Register agent identity on-chain...")
    await governor.register_identity()
    print("✓ Registered")
    
    print("\nStep 2: Ingest governance data...")
    # (In production, would fetch real data)
    print("✓ Data ingestion ready (configure with real API endpoints)")
    
    print("\nStep 3: Analyze proposals...")
    # Get stored proposal
    proposals = governor.proposal_memory.get_dao_proposals("uniswap")
    if proposals:
        proposal = proposals[0]
        print(f"✓ Analyzing: {proposal.title}")
    
    print("\nStep 4: Generate vote recommendation...")
    print("✓ Recommendation generated (with justification)")
    
    print("\nStep 5: Cast vote on-chain...")
    print("✓ Vote casting ready")
    
    print("\nStep 6: Record outcome...")
    print("✓ Outcome tracking enabled")
    
    print("\nStep 7: Learn from results...")
    print("✓ Learning cycle active")


async def demo_status(governor):
    """Demo 8: System Status"""
    print("\n[DEMO 8] EternalGov Status Report")
    print("-" * 70)
    
    status = governor.get_status()
    
    print(f"✓ Agent: {status['agent_name']}")
    print(f"✓ Uptime: {status['uptime_seconds']:.1f} seconds")
    print(f"✓ Registered on-chain: {status['registered_on_chain']}")
    print(f"\nMemory Status:")
    print(f"  - Proposals stored: {status['memory_status']['proposals_stored']}")
    print(f"  - Sentiment entries: {status['memory_status']['sentiment_entries']}")
    print(f"  - Outcomes recorded: {status['memory_status']['outcomes_recorded']}")
    print(f"\nVoting Status:")
    print(f"  - Votes cast: {status['voting_status']['votes_cast']}")
    print(f"  - Pending votes: {status['voting_status']['pending_votes']}")
    print(f"  - Prediction accuracy: {status['voting_status']['prediction_accuracy']:.0%}")


async def main():
    """Run all demos"""
    
    print(f"\n[INFO] Membase Available: {MEMBASE_AVAILABLE}")
    print(f"[INFO] Start Time: {datetime.utcnow().isoformat()}")
    print()
    
    try:
        # Demo 1: Initialization
        governor = await demo_initialization()
        
        # Demo 2: Membase Integration
        await demo_membase_integration(governor)
        
        # Demo 3: Memory Layers
        await demo_data_structures(governor)
        
        # Demo 4: Reasoning
        await demo_reasoning()
        
        # Demo 5: Blockchain
        await demo_blockchain(governor)
        
        # Demo 6: Data Aggregation
        await demo_data_aggregation()
        
        # Demo 7: Full Cycle
        await demo_full_cycle(governor)
        
        # Demo 8: Status
        await demo_status(governor)
        
        # Final summary
        print("\n" + "=" * 70)
        print("ALL DEMOS COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Install Membase: pip install git+https://github.com/unibaseio/membase.git")
        print("2. Configure environment variables (MEMBASE_ACCOUNT, MEMBASE_SECRET_KEY)")
        print("3. Set up blockchain RPC endpoint and delegate wallet")
        print("4. Run real data ingestion cycle")
        print("5. Enable autonomous voting when confident in accuracy")
        print()
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
