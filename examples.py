"""
Quick Start Examples for EternalGov
"""

# Example 1: Initialize EternalGov with Membase
def example_initialization():
    """Example: Initialize EternalGov agent"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    print("EternalGov initialized successfully")


# Example 2: Register identity on-chain
async def example_register_identity():
    """Example: Register delegate identity on BNBChain"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    
    success = await governor.register_identity()
    print(f"Registration {'successful' if success else 'failed'}")


# Example 3: Ingest governance data
async def example_ingest_data():
    """Example: Gather governance data from public sources"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    
    # Ingest Uniswap governance data
    data = await governor.ingest_governance_data("uniswap")
    
    print(f"Ingested data:")
    print(f"  - Proposals: {len(data.get('proposals', []))}")
    print(f"  - Discussions: {len(data.get('discussions', []))}")


# Example 4: Analyze a proposal
async def example_analyze_proposal():
    """Example: Analyze a governance proposal"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    
    # First ingest data
    await governor.ingest_governance_data("uniswap")
    
    # Analyze a proposal
    analysis = await governor.analyze_proposal("proposal_123", "uniswap")
    
    print("Proposal Analysis:")
    print(f"  - Community Consensus: {analysis.get('community_consensus')}")
    print(f"  - Sentiment: {analysis.get('sentiment')}")


# Example 5: Generate vote recommendation
async def example_vote_recommendation():
    """Example: Generate vote recommendation with justification"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    
    # Ingest and analyze
    await governor.ingest_governance_data("uniswap")
    recommendation = await governor.generate_vote_recommendation("proposal_123", "uniswap")
    
    if recommendation:
        decision = recommendation["decision"]
        print("Vote Recommendation:")
        print(f"  - Choice: {decision.choice}")
        print(f"  - Confidence: {decision.confidence:.1%}")
        print(f"  - Risk Level: {decision.risk_assessment}")
        print(f"\n{recommendation['markdown_report']}")


# Example 6: Cast a vote
async def example_cast_vote():
    """Example: Cast a vote on a proposal"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    config["voting"]["autonomous"] = True  # Enable autonomous voting
    
    governor = EternalGov(config)
    
    # Generate recommendation and cast vote
    success = await governor.cast_vote(
        proposal_id="proposal_123",
        choice="for",
        dao_name="uniswap",
        justification_hash="0xabc123"
    )
    
    print(f"Vote {'cast successfully' if success else 'failed'}")


# Example 7: Access memory layers
def example_memory_layers():
    """Example: Access EternalGov's memory layers"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    
    # Access proposal memory
    proposals = governor.proposal_memory.get_dao_proposals("uniswap")
    print(f"Proposals in memory: {len(proposals)}")
    
    # Access sentiment memory
    sentiment = governor.sentiment_memory.get_proposal_sentiment("proposal_123")
    print(f"Sentiment for proposal: {sentiment}")
    
    # Access outcome memory
    pass_rate = governor.outcome_memory.get_pass_rate("uniswap")
    print(f"Uniswap proposal pass rate: {pass_rate:.1%}")


# Example 8: Continuous governance cycle
async def example_governance_cycle():
    """Example: Run continuous governance analysis"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    
    # Register identity
    await governor.register_identity()
    
    # Run governance cycle
    await governor.run_governance_cycle("uniswap")
    
    # Check status
    status = governor.get_status()
    print("EternalGov Status:")
    print(f"  - Uptime: {status['uptime_seconds']:.0f}s")
    print(f"  - Proposals: {status['memory_status']['proposals_stored']}")
    print(f"  - Votes Cast: {status['voting_status']['votes_cast']}")
    print(f"  - Prediction Accuracy: {status['voting_status']['prediction_accuracy']:.1%}")


# Example 9: Integration with Membase
async def example_membase_integration():
    """Example: Store and retrieve governance data in Membase"""
    from eternal_gov import EternalGov
    from config.config import get_config
    
    config = get_config()
    governor = EternalGov(config)
    
    # Store a message in Membase
    governor.memory_manager.add_message(
        conversation_id="uniswap_governance_2025",
        content="Analysis of Uniswap v4 governance proposal...",
        role="assistant",
        metadata={"proposal_id": "123", "dao": "uniswap"}
    )
    
    # Add document to knowledge base
    governor.knowledge_base.add_proposal(
        proposal_id="123",
        proposal_text="Full proposal text...",
        url="https://snapshot.org/#/uniswap.eth/proposal/...",
        author="UNI Team",
        timestamp="2025-01-01T00:00:00Z"
    )
    
    print("Data stored in Membase for decentralized persistence")


# Run an example
if __name__ == "__main__":
    import asyncio
    
    print("EternalGov Quick Start Examples")
    print("=" * 60)
    
    # Run a simple initialization example
    print("\nExample 1: Initialization")
    example_initialization()
    
    # Run async example
    print("\nExample 6: Memory Layers")
    example_memory_layers()
