"""
Preference Memory Layer for EternalGov
Learns and stores community governance preferences and values
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PreferencePattern:
    """Stores identified preference patterns"""
    pattern_id: str
    category: str  # "security", "decentralization", "tokenomics", "efficiency"
    description: str
    confidence: float  # 0.0 to 1.0
    supporting_proposals: List[str]
    historical_weight: float  # How much this pattern historically predicts outcomes


class PreferenceMemory:
    """
    Manages preference memory layer
    Learns community values and voting patterns
    """
    
    def __init__(self, membase_account: str):
        """
        Initialize preference memory
        
        Args:
            membase_account: Membase account
        """
        self.membase_account = membase_account
        self.patterns: Dict[str, PreferencePattern] = {}
        self.voting_history: Dict[str, Dict[str, int]] = {}  # proposal_id -> {choice: votes}
        self.category_success_rate: Dict[str, float] = {}  # category -> pass rate
    
    def record_proposal_outcome(
        self,
        proposal_id: str,
        category: str,
        votes: Dict[str, int],
        passed: bool,
        participation_rate: float
    ) -> None:
        """
        Record outcome of a proposal for learning
        
        Args:
            proposal_id: Proposal ID
            category: Proposal category
            votes: Final vote counts {choice: count}
            passed: Whether proposal passed
            participation_rate: Voting participation percentage
        """
        self.voting_history[proposal_id] = votes
        
        # Update category success rate
        current_rate = self.category_success_rate.get(category, 0.5)
        if passed:
            # Exponential moving average
            self.category_success_rate[category] = current_rate * 0.7 + 1.0 * 0.3
        else:
            self.category_success_rate[category] = current_rate * 0.7 + 0.0 * 0.3
    
    def record_community_value(
        self,
        value_name: str,
        category: str,
        description: str,
        proposals_indicating: List[str]
    ) -> None:
        """
        Record an identified community value or preference
        
        Args:
            value_name: Name of the value/preference
            category: Value category
            description: Description
            proposals_indicating: Proposals that demonstrate this value
        """
        pattern_id = f"preference_{category}_{value_name}"
        
        pattern = PreferencePattern(
            pattern_id=pattern_id,
            category=category,
            description=description,
            confidence=0.5,  # Initial confidence
            supporting_proposals=proposals_indicating,
            historical_weight=0.5  # Initial weight
        )
        
        self.patterns[pattern_id] = pattern
    
    def get_community_values(self) -> Dict[str, PreferencePattern]:
        """Get all identified community values"""
        return self.patterns
    
    def get_category_preferences(self, category: str) -> List[PreferencePattern]:
        """Get preferences for a specific category"""
        return [p for p in self.patterns.values() if p.category == category]
    
    def get_category_success_rate(self, category: str) -> float:
        """
        Get historical success rate for a proposal category
        
        Args:
            category: Proposal category
            
        Returns:
            Success rate (0.0 to 1.0)
        """
        return self.category_success_rate.get(category, 0.5)
    
    def update_pattern_confidence(
        self,
        pattern_id: str,
        new_confidence: float
    ) -> None:
        """
        Update confidence in a preference pattern
        
        Args:
            pattern_id: Pattern ID
            new_confidence: New confidence score (0.0 to 1.0)
        """
        if pattern_id in self.patterns:
            self.patterns[pattern_id].confidence = max(0.0, min(1.0, new_confidence))
    
    def analyze_voting_patterns(self, num_proposals: int = 10) -> Dict:
        """
        Analyze voting patterns from recent proposals
        
        Args:
            num_proposals: Number of recent proposals to analyze
            
        Returns:
            Dictionary of voting pattern analysis
        """
        recent_proposals = list(self.voting_history.items())[-num_proposals:]
        
        analysis = {
            "average_participation": 0.0,
            "majority_threshold": 0.0,
            "common_choices": {},
            "controversial_proposals": 0
        }
        
        if not recent_proposals:
            return analysis
        
        # Analyze voting distributions
        for proposal_id, votes in recent_proposals:
            total_votes = sum(votes.values())
            if total_votes > 0:
                # Track choice frequency
                for choice, count in votes.items():
                    analysis["common_choices"][choice] = analysis["common_choices"].get(choice, 0) + 1
                
                # Identify controversial proposals (close votes)
                max_votes = max(votes.values())
                if max_votes < total_votes * 0.6:
                    analysis["controversial_proposals"] += 1
        
        return analysis
    
    def predict_proposal_preference(self, proposal: Dict) -> str:
        """
        Predict community preference based on proposal characteristics
        
        Args:
            proposal: Proposal data
            
        Returns:
            Predicted preference: "likely_support", "likely_oppose", "uncertain"
        """
        category = proposal.get("category", "general")
        success_rate = self.get_category_success_rate(category)
        
        # Simple heuristic: use category success rate
        if success_rate > 0.65:
            return "likely_support"
        elif success_rate < 0.35:
            return "likely_oppose"
        else:
            return "uncertain"
