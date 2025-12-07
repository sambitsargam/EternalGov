"""
Vote Justification Reporter for EternalGov
Creates transparent, on-chain recordable vote justifications
"""

from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class VoteJustificationReport:
    """Structured report of vote justification"""
    proposal_id: str
    vote_choice: str
    timestamp: str
    confidence: float
    reasoning_hash: str  # Hash of full reasoning for on-chain reference
    summary: str
    detailed_reasoning: str
    data_sources: Dict[str, str]  # sources and their contributions
    sentiment_snapshot: Dict[str, float]
    preference_alignment: float
    risk_level: str
    transparency_score: float  # 0.0 to 1.0


class JustificationReporter:
    """
    Generates and manages vote justification reports
    """
    
    def __init__(self):
        """Initialize justification reporter"""
        self.reports: Dict[str, VoteJustificationReport] = {}
    
    def create_justification_report(
        self,
        proposal_id: str,
        vote_choice: str,
        confidence: float,
        reasoning: str,
        sentiment_data: Dict[str, float],
        preference_alignment: float,
        risk_level: str,
        data_sources: Optional[Dict[str, str]] = None
    ) -> VoteJustificationReport:
        """
        Create a structured vote justification report
        
        Args:
            proposal_id: Proposal ID
            vote_choice: The vote choice
            confidence: Confidence level
            reasoning: Detailed reasoning text
            sentiment_data: Sentiment scores from different sources
            preference_alignment: Alignment with community preferences
            risk_level: Risk assessment
            data_sources: Data sources used
            
        Returns:
            VoteJustificationReport
        """
        
        # Generate justification hash
        justification_hash = self._hash_justification(reasoning)
        
        # Create summary
        summary = self._create_summary(
            vote_choice,
            confidence,
            sentiment_data,
            preference_alignment,
            risk_level
        )
        
        report = VoteJustificationReport(
            proposal_id=proposal_id,
            vote_choice=vote_choice,
            timestamp=datetime.utcnow().isoformat(),
            confidence=confidence,
            reasoning_hash=justification_hash,
            summary=summary,
            detailed_reasoning=reasoning,
            data_sources=data_sources or {},
            sentiment_snapshot=sentiment_data,
            preference_alignment=preference_alignment,
            risk_level=risk_level,
            transparency_score=self._calculate_transparency_score(reasoning, data_sources)
        )
        
        self.reports[proposal_id] = report
        return report
    
    def get_report(self, proposal_id: str) -> Optional[VoteJustificationReport]:
        """Retrieve a justification report"""
        return self.reports.get(proposal_id)
    
    def get_reports_for_json(self) -> str:
        """Export all reports as JSON"""
        reports_dict = {
            pid: {
                "vote_choice": r.vote_choice,
                "confidence": r.confidence,
                "timestamp": r.timestamp,
                "reasoning_hash": r.reasoning_hash,
                "summary": r.summary,
                "risk_level": r.risk_level,
                "transparency_score": r.transparency_score
            }
            for pid, r in self.reports.items()
        }
        return json.dumps(reports_dict, indent=2)
    
    def get_full_report_markdown(self, proposal_id: str) -> Optional[str]:
        """Get a report in Markdown format for transparency"""
        
        report = self.get_report(proposal_id)
        if not report:
            return None
        
        markdown = f"""
# EternalGov Vote Justification Report

## Proposal {report.proposal_id}

**Vote Choice:** {report.vote_choice}  
**Confidence:** {report.confidence:.1%}  
**Risk Level:** {report.risk_level}  
**Transparency Score:** {report.transparency_score:.1%}  
**Timestamp:** {report.timestamp}

## Summary

{report.summary}

## Sentiment Analysis

| Source | Score |
|--------|-------|
{chr(10).join(f"| {source} | {score:+.2f} |" for source, score in report.sentiment_snapshot.items())}

**Preference Alignment:** {report.preference_alignment:.1%}

## Data Sources

{chr(10).join(f"- **{source}:** {contribution}" for source, contribution in report.data_sources.items())}

## Detailed Reasoning

{report.detailed_reasoning}

---

*This report is stored in Unibase's decentralized Membase for permanent verification.*  
*Reasoning Hash: {report.reasoning_hash}*
        """.strip()
        
        return markdown
    
    def _create_summary(
        self,
        vote_choice: str,
        confidence: float,
        sentiment_data: Dict[str, float],
        preference_alignment: float,
        risk_level: str
    ) -> str:
        """Create a concise summary of the justification"""
        
        sentiment_avg = sum(sentiment_data.values()) / len(sentiment_data) if sentiment_data else 0
        
        summary = f"""
EternalGov recommends voting **{vote_choice}** with {confidence:.0%} confidence.

**Key Metrics:**
- Community Sentiment: {sentiment_avg:+.2f}
- Preference Alignment: {preference_alignment:.0%}
- Risk Assessment: {risk_level}

This recommendation is based on analysis of community discussions across Snapshot, governance forums, 
social media, and historical voting patterns. The decision prioritizes long-term DAO value alignment 
and community consensus.
        """.strip()
        
        return summary
    
    def _hash_justification(self, reasoning: str) -> str:
        """
        Generate a hash of the reasoning for on-chain verification
        In production: use keccak256 or similar
        """
        import hashlib
        return hashlib.sha256(reasoning.encode()).hexdigest()[:16]
    
    def _calculate_transparency_score(
        self,
        reasoning: str,
        data_sources: Optional[Dict[str, str]] = None
    ) -> float:
        """
        Calculate transparency score based on reasoning quality and data sources
        
        Args:
            reasoning: Reasoning text
            data_sources: Data sources used
            
        Returns:
            Transparency score (0.0 to 1.0)
        """
        score = 0.0
        
        # Length of reasoning (more is better)
        if len(reasoning) > 1000:
            score += 0.3
        elif len(reasoning) > 500:
            score += 0.2
        
        # Number of data sources
        num_sources = len(data_sources) if data_sources else 0
        if num_sources >= 3:
            score += 0.4
        elif num_sources >= 2:
            score += 0.3
        elif num_sources >= 1:
            score += 0.2
        
        # Detail in reasoning
        detail_keywords = ["analyze", "consider", "evidence", "data", "pattern", "trend"]
        keyword_count = sum(1 for kw in detail_keywords if kw in reasoning.lower())
        score += min(0.3, keyword_count * 0.05)
        
        return min(1.0, score)
