"""
Outcome Memory Layer for EternalGov
Tracks proposal outcomes and correlations with memory layers
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProposalOutcome:
    """Records the outcome of a proposal"""
    proposal_id: str
    dao: str
    passed: bool
    final_votes: Dict[str, int]
    participation_rate: float
    participation_count: int
    recorded_at: str
    predicted_vs_actual: Optional[str] = None  # comparison with EternalGov prediction


class OutcomeMemory:
    """
    Manages outcome memory layer
    Records proposal results and analyzes prediction accuracy
    """
    
    def __init__(self, membase_account: str):
        """
        Initialize outcome memory
        
        Args:
            membase_account: Membase account
        """
        self.membase_account = membase_account
        self.outcomes: Dict[str, ProposalOutcome] = {}
        self.prediction_accuracy: Dict[str, float] = {}  # dao -> accuracy
    
    def record_proposal_outcome(
        self,
        proposal_id: str,
        dao: str,
        passed: bool,
        final_votes: Dict[str, int],
        participation_count: int,
        total_eligible: int
    ) -> None:
        """
        Record the final outcome of a proposal
        
        Args:
            proposal_id: Proposal ID
            dao: DAO name
            passed: Whether the proposal passed
            final_votes: Final vote distribution
            participation_count: Number of voters
            total_eligible: Total eligible voters
        """
        participation_rate = participation_count / total_eligible if total_eligible > 0 else 0
        
        outcome = ProposalOutcome(
            proposal_id=proposal_id,
            dao=dao,
            passed=passed,
            final_votes=final_votes,
            participation_rate=participation_rate,
            participation_count=participation_count,
            recorded_at=datetime.utcnow().isoformat()
        )
        
        self.outcomes[proposal_id] = outcome
        self._sync_to_membase(outcome)
    
    def record_prediction(
        self,
        proposal_id: str,
        predicted_outcome: str,
        actual_outcome: str,
        confidence: float
    ) -> None:
        """
        Record EternalGov's prediction vs actual outcome
        
        Args:
            proposal_id: Proposal ID
            predicted_outcome: What EternalGov predicted
            actual_outcome: What actually happened
            confidence: Confidence level of prediction
        """
        if proposal_id in self.outcomes:
            if predicted_outcome == actual_outcome:
                self.outcomes[proposal_id].predicted_vs_actual = "correct"
            else:
                self.outcomes[proposal_id].predicted_vs_actual = "incorrect"
            
            # Update prediction accuracy
            self._update_accuracy_metrics(proposal_id, predicted_outcome == actual_outcome)
    
    def get_proposal_outcome(self, proposal_id: str) -> Optional[ProposalOutcome]:
        """Retrieve a proposal outcome"""
        return self.outcomes.get(proposal_id)
    
    def get_dao_outcomes(self, dao: str) -> List[ProposalOutcome]:
        """Get all outcomes for a DAO"""
        return [o for o in self.outcomes.values() if o.dao == dao]
    
    def get_average_participation(self, dao: str) -> float:
        """
        Get average participation rate for a DAO
        
        Args:
            dao: DAO name
            
        Returns:
            Average participation rate
        """
        outcomes = self.get_dao_outcomes(dao)
        if not outcomes:
            return 0.0
        return sum(o.participation_rate for o in outcomes) / len(outcomes)
    
    def get_pass_rate(self, dao: str) -> float:
        """
        Get proposal pass rate for a DAO
        
        Args:
            dao: DAO name
            
        Returns:
            Percentage of proposals that passed (0.0 to 1.0)
        """
        outcomes = self.get_dao_outcomes(dao)
        if not outcomes:
            return 0.5
        passed = sum(1 for o in outcomes if o.passed)
        return passed / len(outcomes)
    
    def get_prediction_accuracy(self, dao: Optional[str] = None) -> float:
        """
        Get EternalGov's prediction accuracy
        
        Args:
            dao: Optional DAO filter
            
        Returns:
            Accuracy percentage (0.0 to 1.0)
        """
        if dao:
            return self.prediction_accuracy.get(dao, 0.5)
        
        # Overall accuracy
        if not self.prediction_accuracy:
            return 0.5
        
        values = list(self.prediction_accuracy.values())
        return sum(values) / len(values) if values else 0.5
    
    def analyze_outcome_trends(self, dao: str, num_recent: int = 20) -> Dict:
        """
        Analyze trends in proposal outcomes
        
        Args:
            dao: DAO name
            num_recent: Number of recent proposals to analyze
            
        Returns:
            Dictionary of trend analysis
        """
        outcomes = self.get_dao_outcomes(dao)[-num_recent:]
        
        if not outcomes:
            return {}
        
        analysis = {
            "pass_rate": self.get_pass_rate(dao),
            "avg_participation": self.get_average_participation(dao),
            "recent_outcomes": [],
            "participation_trend": []
        }
        
        for outcome in outcomes:
            analysis["recent_outcomes"].append({
                "proposal_id": outcome.proposal_id,
                "passed": outcome.passed,
                "participation": outcome.participation_rate
            })
            analysis["participation_trend"].append(outcome.participation_rate)
        
        return analysis
    
    def _update_accuracy_metrics(self, proposal_id: str, was_correct: bool) -> None:
        """Update accuracy metrics based on prediction result"""
        # Get DAO from outcome
        if proposal_id in self.outcomes:
            dao = self.outcomes[proposal_id].dao
            
            # Exponential moving average of accuracy
            current_acc = self.prediction_accuracy.get(dao, 0.5)
            new_value = 1.0 if was_correct else 0.0
            self.prediction_accuracy[dao] = current_acc * 0.8 + new_value * 0.2
    
    def _sync_to_membase(self, outcome: ProposalOutcome) -> None:
        """Sync outcome to Membase for decentralized storage"""
        print(f"[MEMBASE] Syncing outcome for {outcome.proposal_id} to Membase")
