"""
Sentiment Memory Layer for EternalGov
Tracks community sentiment and opinions across sources
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SentimentEntry:
    """Stores sentiment data for a proposal"""
    proposal_id: str
    dao: str
    source: str  # "forum", "twitter", "snapshot_votes"
    sentiment_score: float  # -1.0 to 1.0
    support_count: int
    opposition_count: int
    neutral_count: int
    key_topics: List[str] = field(default_factory=list)
    recorded_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class SentimentMemory:
    """
    Manages sentiment memory layer
    Tracks community opinions and sentiment trends
    """
    
    def __init__(self, membase_account: str):
        """
        Initialize sentiment memory
        
        Args:
            membase_account: Membase account
        """
        self.membase_account = membase_account
        self.sentiment_entries: Dict[str, List[SentimentEntry]] = {}
        self.sentiment_trends: Dict[str, List[float]] = {}  # proposal_id -> [scores over time]
    
    def record_sentiment(
        self,
        proposal_id: str,
        dao: str,
        source: str,
        sentiment_score: float,
        support_count: int,
        opposition_count: int,
        neutral_count: int,
        topics: Optional[List[str]] = None
    ) -> None:
        """
        Record sentiment data from a source
        
        Args:
            proposal_id: Proposal ID
            dao: DAO name
            source: Data source (forum, twitter, etc.)
            sentiment_score: Calculated sentiment score (-1 to 1)
            support_count: Number of support indicators
            opposition_count: Number of opposition indicators
            neutral_count: Number of neutral indicators
            topics: Key topics mentioned
        """
        entry = SentimentEntry(
            proposal_id=proposal_id,
            dao=dao,
            source=source,
            sentiment_score=sentiment_score,
            support_count=support_count,
            opposition_count=opposition_count,
            neutral_count=neutral_count,
            key_topics=topics or []
        )
        
        if proposal_id not in self.sentiment_entries:
            self.sentiment_entries[proposal_id] = []
            self.sentiment_trends[proposal_id] = []
        
        self.sentiment_entries[proposal_id].append(entry)
        self.sentiment_trends[proposal_id].append(sentiment_score)
        
        self._sync_to_membase(entry)
    
    def get_proposal_sentiment(self, proposal_id: str) -> Dict:
        """
        Get aggregated sentiment for a proposal
        
        Args:
            proposal_id: Proposal ID
            
        Returns:
            Dictionary with sentiment analysis
        """
        entries = self.sentiment_entries.get(proposal_id, [])
        
        if not entries:
            return {}
        
        # Aggregate by source
        by_source = {}
        for entry in entries:
            if entry.source not in by_source:
                by_source[entry.source] = []
            by_source[entry.source].append(entry)
        
        # Calculate averages per source
        aggregated = {}
        for source, source_entries in by_source.items():
            avg_score = sum(e.sentiment_score for e in source_entries) / len(source_entries)
            total_support = sum(e.support_count for e in source_entries)
            total_opposition = sum(e.opposition_count for e in source_entries)
            
            aggregated[source] = {
                "average_sentiment": avg_score,
                "support_count": total_support,
                "opposition_count": total_opposition,
                "entries": len(source_entries)
            }
        
        # Overall sentiment
        overall_score = sum(e.sentiment_score for e in entries) / len(entries)
        
        return {
            "proposal_id": proposal_id,
            "overall_sentiment_score": overall_score,
            "by_source": aggregated,
            "total_entries": len(entries),
            "last_updated": entries[-1].recorded_at if entries else None
        }
    
    def get_sentiment_trend(self, proposal_id: str) -> List[float]:
        """Get sentiment trend over time"""
        return self.sentiment_trends.get(proposal_id, [])
    
    def get_top_topics(self, proposal_id: str) -> Dict[str, int]:
        """
        Get most discussed topics for a proposal
        
        Args:
            proposal_id: Proposal ID
            
        Returns:
            Dictionary of topic: mention_count
        """
        entries = self.sentiment_entries.get(proposal_id, [])
        topic_counts = {}
        
        for entry in entries:
            for topic in entry.key_topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return dict(sorted(topic_counts.items(), key=lambda x: x[1], reverse=True))
    
    def get_community_consensus(self, proposal_id: str) -> str:
        """
        Determine community consensus based on sentiment
        
        Args:
            proposal_id: Proposal ID
            
        Returns:
            "strong_support", "moderate_support", "neutral", "concern", "strong_opposition"
        """
        sentiment = self.get_proposal_sentiment(proposal_id)
        
        if not sentiment:
            return "neutral"
        
        score = sentiment.get("overall_sentiment_score", 0)
        
        if score > 0.6:
            return "strong_support"
        elif score > 0.2:
            return "moderate_support"
        elif score > -0.2:
            return "neutral"
        elif score > -0.6:
            return "concern"
        else:
            return "strong_opposition"
    
    def _sync_to_membase(self, entry: SentimentEntry) -> None:
        """Sync sentiment data to Membase"""
        print(f"[MEMBASE] Syncing sentiment for {entry.proposal_id} from {entry.source}")
        
        # Save to disk to simulate Membase
        try:
            import json
            from pathlib import Path
            from datetime import datetime
            
            storage_dir = Path("/tmp/eternalgov_membase_storage/sentiment")
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = storage_dir / f"{entry.proposal_id}.json"
            
            # Read existing or create new
            if filepath.exists():
                with open(filepath) as f:
                    data = json.load(f)
                    data["entries"].append({
                        "dao": entry.dao,
                        "source": entry.source,
                        "sentiment_score": entry.sentiment_score,
                        "support_count": entry.support_count,
                        "opposition_count": entry.opposition_count,
                        "neutral_count": entry.neutral_count,
                        "topics": entry.topics,
                        "timestamp": datetime.utcnow().isoformat()
                    })
            else:
                data = {
                    "proposal_id": entry.proposal_id,
                    "entries": [{
                        "dao": entry.dao,
                        "source": entry.source,
                        "sentiment_score": entry.sentiment_score,
                        "support_count": entry.support_count,
                        "opposition_count": entry.opposition_count,
                        "neutral_count": entry.neutral_count,
                        "topics": entry.topics,
                        "timestamp": datetime.utcnow().isoformat()
                    }],
                    "membase_account": "default"
                }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"[MEMBASE] ✅ Synced sentiment to Membase at {filepath}")
        except Exception as e:
            print(f"[WARNING] Failed to sync sentiment: {str(e)}")
