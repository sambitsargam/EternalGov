"""
Vote Reasoning for EternalGov
LLM-based decision pipeline for proposal analysis
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReasoningContext:
    """Context for reasoning about a proposal"""
    proposal_id: str
    proposal_title: str
    proposal_body: str
    dao: str
    voting_options: List[str]
    community_sentiment: Dict[str, float]
    historical_preferences: Dict[str, float]
    similar_past_proposals: List[Dict]
    arguments_for: List[str]
    arguments_against: List[str]
    expected_impact: str


@dataclass
class VoteDecision:
    """Records a vote decision"""
    proposal_id: str
    choice: str  # The vote choice
    confidence: float  # 0.0 to 1.0
    reasoning_summary: str
    primary_factors: List[str]
    secondary_factors: List[str]
    alignment_with_dao_values: float
    risk_assessment: str  # "low", "medium", "high"


class VoteReasoning:
    """
    Implements LLM-based reasoning for governance decisions
    """
    
    def __init__(self):
        """Initialize vote reasoning engine"""
        self.decision_history: Dict[str, VoteDecision] = {}
        self.reasoning_patterns: List[Dict] = []
    
    def analyze_proposal(self, context: ReasoningContext) -> VoteDecision:
        """
        Analyze a proposal and generate a vote decision
        
        Args:
            context: ReasoningContext with all proposal information
            
        Returns:
            VoteDecision with recommendation
        """
        
        # In production: call LLM (OpenAI, Claude, etc.)
        # prompt = self._build_reasoning_prompt(context)
        # llm_response = await llm_client.generate(prompt)
        # decision = self._parse_llm_response(llm_response)
        
        decision = self._generate_decision(context)
        self.decision_history[context.proposal_id] = decision
        return decision
    
    def _generate_decision(self, context: ReasoningContext) -> VoteDecision:
        """
        Generate a vote decision based on context
        (Placeholder for LLM integration)
        """
        
        # Analyze sentiment
        overall_sentiment = sum(
            context.community_sentiment.values()
        ) / len(context.community_sentiment) if context.community_sentiment else 0
        
        # Analyze preference alignment
        preference_alignment = sum(
            context.historical_preferences.values()
        ) / len(context.historical_preferences) if context.historical_preferences else 0
        
        # Determine best choice
        if overall_sentiment > 0.5 and preference_alignment > 0.5:
            choice = context.voting_options[0] if context.voting_options else "for"
            confidence = 0.75
            primary = ["strong_community_support", "alignment_with_values"]
            secondary = ["positive_expected_impact"]
            risk = "low"
        elif overall_sentiment < -0.3 or preference_alignment < 0.3:
            choice = context.voting_options[-1] if context.voting_options else "against"
            confidence = 0.6
            primary = ["community_concerns", "misalignment_with_preferences"]
            secondary = ["potential_risks"]
            risk = "medium"
        else:
            choice = context.voting_options[1] if len(context.voting_options) > 1 else "abstain"
            confidence = 0.5
            primary = ["mixed_signals"]
            secondary = ["requires_further_analysis"]
            risk = "medium"
        
        reasoning = self._build_reasoning_summary(context, choice, primary, secondary)
        alignment = (overall_sentiment + preference_alignment) / 2
        
        return VoteDecision(
            proposal_id=context.proposal_id,
            choice=choice,
            confidence=confidence,
            reasoning_summary=reasoning,
            primary_factors=primary,
            secondary_factors=secondary,
            alignment_with_dao_values=alignment,
            risk_assessment=risk
        )
    
    def _build_reasoning_summary(
        self,
        context: ReasoningContext,
        choice: str,
        primary: List[str],
        secondary: List[str]
    ) -> str:
        """Build human-readable reasoning summary"""
        
        summary = f"""
EternalGov Vote Analysis for: {context.proposal_title}

Recommendation: {choice.upper()}

Primary Factors:
{chr(10).join(f"  • {f}" for f in primary)}

Secondary Factors:
{chr(10).join(f"  • {f}" for f in secondary)}

Community Sentiment Analysis:
{chr(10).join(f"  • {source}: {score:.2f}" for source, score in context.community_sentiment.items())}

Expected Impact: {context.expected_impact[:200]}...

This recommendation aligns with historical DAO values and community preferences.
        """.strip()
        
        return summary
    
    def get_decision_history(self) -> Dict[str, VoteDecision]:
        """Get all vote decisions"""
        return self.decision_history
    
    def analyze_reasoning_patterns(self) -> Dict:
        """
        Analyze patterns in EternalGov's reasoning
        
        Returns:
            Dictionary of pattern analysis
        """
        if not self.decision_history:
            return {}
        
        decisions = list(self.decision_history.values())
        
        # Analyze decision patterns
        patterns = {
            "average_confidence": sum(d.confidence for d in decisions) / len(decisions),
            "most_common_choice": max(
                set(d.choice for d in decisions),
                key=list(d.choice for d in decisions).count,
                default=None
            ),
            "risk_distribution": {},
            "decision_count": len(decisions)
        }
        
        # Risk distribution
        for decision in decisions:
            risk = decision.risk_assessment
            patterns["risk_distribution"][risk] = patterns["risk_distribution"].get(risk, 0) + 1
        
        return patterns
    
    def _build_reasoning_prompt(self, context: ReasoningContext) -> str:
        """Build LLM prompt for proposal analysis"""
        
        prompt = f"""
Analyze this DAO governance proposal and determine the optimal vote:

Title: {context.proposal_title}
DAO: {context.dao}

Proposal Details:
{context.proposal_body[:500]}

Voting Options: {', '.join(context.voting_options)}

Community Sentiment:
{chr(10).join(f"  • {s}: {context.community_sentiment.get(s, 0):.2f}" for s in context.community_sentiment.keys())}

Arguments For:
{chr(10).join(f"  • {arg}" for arg in context.arguments_for[:3])}

Arguments Against:
{chr(10).join(f"  • {arg}" for arg in context.arguments_against[:3])}

Historical Context:
Similar past proposals and their outcomes:
{chr(10).join(f"  • {p.get('title', 'Unknown')}: {p.get('outcome', 'Unknown')}" for p in context.similar_past_proposals[:3])}

Based on this analysis, what should EternalGov vote? Provide:
1. Vote recommendation (for/against/abstain)
2. Confidence level (0-100)
3. Three primary factors influencing the decision
4. Risk assessment
        """.strip()
        
        return prompt
