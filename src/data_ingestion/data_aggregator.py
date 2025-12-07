"""
Data Aggregator for EternalGov
Coordinates scraping from multiple sources and aggregates governance data
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

from .snapshot_scraper import SnapshotScraper, SnapshotProposal
from .forum_scraper import ForumScraper, ForumDiscussion
from .twitter_scraper import TwitterScraper, Tweet
from .blog_scraper import BlogScraper, BlogArticle


@dataclass
class AggregatedGovernanceData:
    """Aggregated governance data from all sources"""
    proposal_id: str
    proposal: SnapshotProposal
    forum_discussions: List[ForumDiscussion]
    tweets: List[Tweet]
    articles: List[BlogArticle]
    aggregated_at: str
    sentiment_summary: Dict[str, float]


class DataAggregator:
    """
    Aggregates governance data from multiple public sources
    """
    
    def __init__(self):
        """Initialize data aggregator"""
        self.snapshot = SnapshotScraper()
        self.forum = ForumScraper()
        self.twitter = TwitterScraper()
        self.blog = BlogScraper()
    
    def aggregate_proposal_data(
        self,
        proposal_id: str,
        snapshot_space: str,
        dao_name: str
    ) -> Optional[AggregatedGovernanceData]:
        """
        Aggregate all available data about a proposal
        
        Args:
            proposal_id: Snapshot proposal ID
            snapshot_space: Snapshot space name
            dao_name: DAO name
            
        Returns:
            AggregatedGovernanceData or None
        """
        # Fetch proposal from Snapshot
        proposal = self.snapshot.fetch_proposal_details(proposal_id, snapshot_space)
        if not proposal:
            return None
        
        # Fetch forum discussions
        forum_discussions = self.forum.get_discussions_for_proposal(proposal_id)
        
        # Search for tweets about the proposal
        search_terms = [proposal.title, dao_name, f"#{proposal_id}"]
        tweets = self.twitter.search_governance_tweets(search_terms)
        
        # Get related blog articles
        articles = self.blog.get_proposal_postmortems(proposal_id)
        
        # Calculate sentiment summary
        sentiment_summary = self._calculate_sentiment_summary(
            proposal,
            forum_discussions,
            tweets,
            articles
        )
        
        return AggregatedGovernanceData(
            proposal_id=proposal_id,
            proposal=proposal,
            forum_discussions=forum_discussions,
            tweets=tweets,
            articles=articles,
            aggregated_at=datetime.utcnow().isoformat(),
            sentiment_summary=sentiment_summary
        )
    
    def aggregate_dao_governance(
        self,
        dao_name: str,
        snapshot_space: str,
        governance_forums: Optional[List[str]] = None,
        twitter_handles: Optional[List[str]] = None
    ) -> Dict:
        """
        Aggregate all governance data for a DAO
        
        Args:
            dao_name: DAO name
            snapshot_space: Snapshot space name
            governance_forums: Optional forum URLs
            twitter_handles: Optional Twitter handles to monitor
            
        Returns:
            Dictionary of aggregated governance data
        """
        data = {
            "dao_name": dao_name,
            "aggregated_at": datetime.utcnow().isoformat(),
            "proposals": [],
            "discussions": [],
            "sentiment_trends": {},
            "influential_voices": []
        }
        
        # Get active proposals
        proposals = self.snapshot.fetch_dao_proposals(snapshot_space)
        data["proposals"] = proposals
        
        # Aggregate forum discussions
        if governance_forums:
            for forum_url in governance_forums:
                discussions = self.forum.scrape_discourse(forum_url)
                data["discussions"].extend(discussions)
        
        # Get influencer sentiment
        if twitter_handles:
            influencer_sentiment = self.twitter.get_influencer_sentiment(twitter_handles)
            data["influential_voices"] = influencer_sentiment
        
        return data
    
    def _calculate_sentiment_summary(
        self,
        proposal: SnapshotProposal,
        discussions: List[ForumDiscussion],
        tweets: List[Tweet],
        articles: List[BlogArticle]
    ) -> Dict[str, float]:
        """
        Calculate aggregated sentiment across all sources
        
        Args:
            proposal: Proposal data
            discussions: Forum discussions
            tweets: Tweets
            articles: Blog articles
            
        Returns:
            Dictionary of sentiment metrics
        """
        sentiment_scores = {
            "forum_support": 0.0,
            "forum_concern": 0.0,
            "twitter_sentiment": 0.0,
            "overall_sentiment": 0.0
        }
        
        # Calculate forum sentiment
        if discussions:
            support_count = sum(1 for d in discussions if "support" in d.sentiment_tags)
            concern_count = sum(1 for d in discussions if "concern" in d.sentiment_tags)
            sentiment_scores["forum_support"] = support_count / len(discussions)
            sentiment_scores["forum_concern"] = concern_count / len(discussions)
        
        # Calculate Twitter sentiment
        if tweets:
            sentiment_scores["twitter_sentiment"] = sum(
                t.sentiment_score for t in tweets
            ) / len(tweets)
        
        # Overall sentiment
        weights = 0.4  # forum support weight
        weights += 0.2  # forum concern weight
        weights += 0.4  # twitter weight
        
        sentiment_scores["overall_sentiment"] = (
            sentiment_scores["forum_support"] * 0.4 -
            sentiment_scores["forum_concern"] * 0.2 +
            sentiment_scores["twitter_sentiment"] * 0.4
        )
        
        return sentiment_scores
