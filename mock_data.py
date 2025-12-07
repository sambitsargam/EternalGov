"""
Mock Data Generator for EternalGov
Creates realistic governance data for testing and demonstration
"""

from datetime import datetime, timedelta
from typing import List, Dict


class MockGovernanceData:
    """Generate realistic mock governance data"""
    
    @staticmethod
    def get_mock_proposals(dao: str, count: int = 5) -> List[Dict]:
        """Generate mock proposals for a DAO"""
        
        proposals_db = {
            "uniswap": [
                {
                    "id": "UNI-1",
                    "title": "Increase Uniswap V4 Liquidity Incentives",
                    "body": "This proposal aims to increase liquidity incentives for Uniswap V4 concentrated liquidity positions. The increased incentives will help bootstrap liquidity in the new V4 system.",
                    "author": "Uniswap Team",
                    "created_at": (datetime.now() - timedelta(days=7)).isoformat(),
                    "end_time": (datetime.now() + timedelta(days=3)).isoformat(),
                    "choices": ["For", "Against", "Abstain"],
                    "url": "https://snapshot.org/uniswap",
                    "category": "tokenomics"
                },
                {
                    "id": "UNI-2",
                    "title": "Enable UNI on Layer 2 Governance",
                    "body": "Proposal to enable native UNI governance participation on Arbitrum and Optimism to reduce transaction costs for token holders.",
                    "author": "Community",
                    "created_at": (datetime.now() - timedelta(days=14)).isoformat(),
                    "end_time": (datetime.now() + timedelta(days=10)).isoformat(),
                    "choices": ["For", "Against"],
                    "url": "https://snapshot.org/uniswap",
                    "category": "governance"
                }
            ],
            "aave": [
                {
                    "id": "AAVE-1",
                    "title": "Enable eMode for New Assets",
                    "body": "This proposal enables eMode (efficiency mode) for ETH-correlated assets, allowing higher LTV ratios for these assets when used in the same eMode category.",
                    "author": "Aave Team",
                    "created_at": (datetime.now() - timedelta(days=5)).isoformat(),
                    "end_time": (datetime.now() + timedelta(days=5)).isoformat(),
                    "choices": ["For", "Against", "Abstain"],
                    "url": "https://snapshot.org/aave",
                    "category": "risk"
                },
                {
                    "id": "AAVE-2",
                    "title": "Increase Reserve Factor for stETH",
                    "body": "Increase the reserve factor for stETH to 20% to reduce risk exposure and increase protocol revenue from the large stETH supply.",
                    "author": "Risk Team",
                    "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
                    "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
                    "choices": ["For", "Against"],
                    "url": "https://snapshot.org/aave",
                    "category": "risk"
                }
            ],
            "compound": [
                {
                    "id": "COMP-1",
                    "title": "Community Development Fund Allocation",
                    "body": "Allocate COMP tokens to community development initiatives and ecosystem grants to accelerate innovation on top of Compound.",
                    "author": "Community",
                    "created_at": (datetime.now() - timedelta(days=10)).isoformat(),
                    "end_time": (datetime.now() + timedelta(days=2)).isoformat(),
                    "choices": ["For", "Against", "Abstain"],
                    "url": "https://snapshot.org/compound",
                    "category": "treasury"
                }
            ],
            "makerdao": [
                {
                    "id": "MKR-1",
                    "title": "Increase Dai Savings Rate",
                    "body": "Proposal to increase the Dai Savings Rate (DSR) to 5% to incentivize Dai holding and reduce supply pressure.",
                    "author": "Maker Team",
                    "created_at": (datetime.now() - timedelta(days=6)).isoformat(),
                    "end_time": (datetime.now() + timedelta(days=4)).isoformat(),
                    "choices": ["For", "Against"],
                    "url": "https://snapshot.org/makerdao",
                    "category": "monetary-policy"
                }
            ]
        }
        
        return proposals_db.get(dao, [])[:count]
    
    @staticmethod
    def get_mock_sentiment(dao: str) -> Dict:
        """Generate mock sentiment data"""
        
        sentiment_db = {
            "uniswap": {
                "UNI-1": {"support": 120, "opposition": 30, "neutral": 20, "score": 0.75},
                "UNI-2": {"support": 85, "opposition": 45, "neutral": 15, "score": 0.65}
            },
            "aave": {
                "AAVE-1": {"support": 95, "opposition": 35, "neutral": 25, "score": 0.70},
                "AAVE-2": {"support": 72, "opposition": 55, "neutral": 18, "score": 0.58}
            },
            "compound": {
                "COMP-1": {"support": 68, "opposition": 42, "neutral": 30, "score": 0.60}
            },
            "makerdao": {
                "MKR-1": {"support": 110, "opposition": 25, "neutral": 35, "score": 0.80}
            }
        }
        
        return sentiment_db.get(dao, {})
    
    @staticmethod
    def get_mock_votes() -> Dict:
        """Generate mock vote recommendations"""
        
        return {
            "UNI-1": {"vote": "FOR", "confidence": 0.92, "risk": "low"},
            "UNI-2": {"vote": "FOR", "confidence": 0.78, "risk": "medium"},
            "AAVE-1": {"vote": "FOR", "confidence": 0.70, "risk": "medium"},
            "AAVE-2": {"vote": "ABSTAIN", "confidence": 0.45, "risk": "high"},
            "COMP-1": {"vote": "FOR", "confidence": 0.65, "risk": "medium"},
            "MKR-1": {"vote": "FOR", "confidence": 0.82, "risk": "low"}
        }
