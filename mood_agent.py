"""
Agentic Mood Analyzer with Reasoning and RAG Integration.

This module implements an intelligent agent that:
1. Retrieves similar posts from the knowledge base
2. Performs multi-step reasoning about mood
3. Builds confidence scores
4. Provides detailed explanations
"""

from typing import List, Dict, Tuple, Optional
from enum import Enum
from mood_analyzer import MoodAnalyzer
from retrieval import MoodKnowledgeBase
from logger import MoodMachineLogger


class AgentAction(Enum):
    """Possible actions the agent can take."""
    PREPROCESS = "preprocess"
    RETRIEVE_SIMILAR = "retrieve_similar"
    SCORE_TEXT = "score_text"
    ANALYZE_RETRIEVED = "analyze_retrieved"
    PREDICT_MOOD = "predict_mood"
    EVALUATE_CONFIDENCE = "evaluate_confidence"


class MoodAgent:
    """
    Intelligent mood analyzer using agentic workflow with RAG.
    
    The agent follows these steps:
    1. Preprocess the input text
    2. Retrieve similar posts from knowledge base
    3. Score the text using rule-based approach
    4. Analyze the mood distribution in retrieved posts
    5. Synthesize a final prediction with confidence
    """

    def __init__(
        self,
        rule_analyzer: MoodAnalyzer,
        knowledge_base: MoodKnowledgeBase,
        logger: MoodMachineLogger
    ):
        """
        Initialize the mood agent.
        
        Args:
            rule_analyzer: Rule-based mood analyzer
            knowledge_base: RAG knowledge base with similar posts
            logger: Logger for tracking decisions
        """
        self.rule_analyzer = rule_analyzer
        self.knowledge_base = knowledge_base
        self.logger = logger
        self.step_count = 0

    def _log_step(self, action: AgentAction, observation: str) -> None:
        """Log an agent step."""
        self.step_count += 1
        self.logger.log_agent_reasoning(self.step_count, action.value, observation)

    def _get_default_label(self, score: int) -> str:
        """Convert numeric score to default mood label."""
        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"

    def analyze_mood(self, text: str) -> Dict:
        """
        Perform full agentic mood analysis with reasoning.
        
        Returns a dictionary with:
        - predicted_mood: The final mood prediction
        - confidence: Confidence score (0-1)
        - direct_score: Rule-based score
        - retrieved_posts: Similar posts found
        - consensus_label: Label distribution from retrieved posts
        - reasoning: Detailed explanation
        """
        self.step_count = 0
        
        try:
            # Step 1: Preprocess
            tokens = self.rule_analyzer.preprocess(text)
            self._log_step(
                AgentAction.PREPROCESS,
                f"Tokenized input into {len(tokens)} tokens"
            )
            
            # Step 2: Retrieve similar posts
            retrieved = self.knowledge_base.retrieve_similar(text, top_k=3)
            self._log_step(
                AgentAction.RETRIEVE_SIMILAR,
                f"Retrieved {len(retrieved)} similar posts"
            )
            
            # Step 3: Score the text directly
            score = self.rule_analyzer.score_text(text)
            direct_label = self._get_default_label(score)
            self._log_step(
                AgentAction.SCORE_TEXT,
                f"Direct score: {score}, Label: {direct_label}"
            )
            
            # Step 4: Analyze retrieved posts
            label_dist = self.knowledge_base.get_label_distribution(retrieved)
            consensus_label = max(label_dist.items(), key=lambda x: x[1])[0] if label_dist else "neutral"
            self._log_step(
                AgentAction.ANALYZE_RETRIEVED,
                f"Retrieved moods: {label_dist}, Consensus: {consensus_label}"
            )
            
            # Step 5: Synthesize prediction
            # If retrieved posts and direct analysis agree, confidence is high
            agreement = direct_label == consensus_label
            confidence = 0.9 if agreement else 0.7
            
            # If there's significant agreement in retrieved posts
            if label_dist and max(label_dist.values()) >= 2:
                confidence = min(confidence + 0.1, 1.0)
            
            # Final prediction: favor direct score but consider consensus
            final_mood = direct_label if score != 0 else consensus_label
            
            self._log_step(
                AgentAction.PREDICT_MOOD,
                f"Final mood: {final_mood}, Agreement: {agreement}"
            )
            
            # Step 6: Evaluate confidence
            self._log_step(
                AgentAction.EVALUATE_CONFIDENCE,
                f"Confidence: {confidence:.2f}"
            )
            
            # Build explanation
            reasoning = self._build_explanation(
                text, score, direct_label, 
                retrieved, consensus_label, confidence
            )
            
            return {
                "predicted_mood": final_mood,
                "confidence": confidence,
                "direct_score": score,
                "direct_label": direct_label,
                "retrieved_posts": [
                    {"text": post[0][:50] + "...", "label": post[1], "similarity": f"{post[2]:.2f}"}
                    for post in retrieved
                ],
                "consensus_label": consensus_label,
                "label_distribution": label_dist,
                "reasoning": reasoning
            }
            
        except Exception as e:
            self.logger.log_error(
                "MoodAnalysisError",
                str(e),
                {"input_text": text[:100]}
            )
            # Fallback to basic analysis
            return {
                "predicted_mood": "neutral",
                "confidence": 0.3,
                "error": str(e),
                "reasoning": "Analysis encountered an error; returning neutral as fallback."
            }

    def _build_explanation(
        self,
        text: str,
        score: int,
        direct_label: str,
        retrieved: List[Tuple[str, str, float]],
        consensus: str,
        confidence: float
    ) -> str:
        """Build a detailed explanation of the mood analysis."""
        lines = [
            f"Analysis of: '{text}'",
            f"",
            f"Direct Analysis:",
            f"  - Score: {score} → {direct_label}",
            f"",
            f"Retrieved Similar Posts ({len(retrieved)} found):",
        ]
        
        for i, (post, label, sim) in enumerate(retrieved, 1):
            lines.append(f"  {i}. '{post[:40]}...' → {label} (similarity: {sim:.2f})")
        
        lines.extend([
            f"",
            f"Synthesis:",
            f"  - Consensus mood from similar posts: {consensus}",
            f"  - Confidence: {confidence:.0%}",
            f"  - Agent reasoning: {'Agreement between direct and retrieved analysis' if direct_label == consensus else 'Some disagreement in analysis'}"
        ])
        
        return "\n".join(lines)
