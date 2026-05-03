"""
Retrieval-Augmented Generation (RAG) system for the Mood Machine.

Retrieves similar posts from the knowledge base to inform mood analysis.
Uses simple similarity matching (word overlap) for relevance ranking.
"""

from typing import List, Tuple
from dataset import SAMPLE_POSTS, TRUE_LABELS
from logger import MoodMachineLogger


class MoodKnowledgeBase:
    """
    Stores and retrieves similar emotional posts.
    This is the "knowledge base" for the RAG system.
    """

    def __init__(self, posts: List[str], labels: List[str], logger: MoodMachineLogger):
        """
        Initialize knowledge base with posts and their labels.
        
        Args:
            posts: List of text posts
            labels: List of mood labels corresponding to posts
            logger: Logger instance for tracking retrieval
        """
        if len(posts) != len(labels):
            raise ValueError("posts and labels must have the same length")
        
        self.posts = posts
        self.labels = labels
        self.logger = logger
        self.logger.log_info(f"Initialized knowledge base with {len(posts)} posts")

    def _compute_similarity(self, query: str, candidate: str) -> float:
        """
        Compute word overlap similarity between query and candidate.
        
        Simple word-based similarity: common words / total unique words
        """
        query_words = set(query.lower().split())
        candidate_words = set(candidate.lower().split())
        
        if len(query_words.union(candidate_words)) == 0:
            return 0.0
        
        intersection = len(query_words.intersection(candidate_words))
        union = len(query_words.union(candidate_words))
        
        return intersection / union

    def retrieve_similar(self, query: str, top_k: int = 3) -> List[Tuple[str, str, float]]:
        """
        Retrieve the top-k most similar posts from the knowledge base.
        
        Args:
            query: The input text to find similar posts for
            top_k: Number of similar posts to return
            
        Returns:
            List of tuples: (post_text, label, similarity_score)
        """
        similarities = []
        
        for post, label in zip(self.posts, self.labels):
            # Don't retrieve the exact same post
            if post.lower() == query.lower():
                continue
                
            score = self._compute_similarity(query, post)
            similarities.append((post, label, score))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        # Get top-k
        results = similarities[:top_k]
        
        # Log the retrieval
        top_match = results[0][0] if results else None
        self.logger.log_retrieval(query, len(results), top_match)
        
        return results

    def get_label_distribution(self, retrieved_items: List[Tuple[str, str, float]]) -> dict:
        """
        Get the mood distribution in retrieved items.
        
        Returns:
            Dict mapping mood label to count
        """
        distribution = {}
        for _, label, _ in retrieved_items:
            distribution[label] = distribution.get(label, 0) + 1
        return distribution
