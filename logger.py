"""
Centralized logging system for the Mood Machine.

Tracks all AI agent decisions, reasoning steps, and system events
for transparency and debugging.
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class MoodMachineLogger:
    """
    Unified logger for the mood analysis system.
    Logs to both file and console with structured format.
    """

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("mood_machine")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # File handler
        log_file = self.log_dir / f"mood_machine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log a structured event with details."""
        message = f"[{event_type}] {json.dumps(details, indent=2)}"
        self.logger.debug(message)

    def log_agent_reasoning(self, step: int, action: str, observation: str) -> None:
        """Log an agent reasoning step."""
        self.log_event("AGENT_STEP", {
            "step": step,
            "action": action,
            "observation": observation
        })

    def log_mood_prediction(self, text: str, predicted_mood: str, 
                           confidence: float, reasoning: str) -> None:
        """Log a mood prediction with reasoning."""
        self.log_event("MOOD_PREDICTION", {
            "input_text": text[:100],  # First 100 chars
            "predicted_mood": predicted_mood,
            "confidence": confidence,
            "reasoning": reasoning
        })

    def log_retrieval(self, query: str, retrieved_items: int, 
                     top_match: Optional[str] = None) -> None:
        """Log RAG retrieval operation."""
        self.log_event("RAG_RETRIEVAL", {
            "query": query[:100],
            "items_retrieved": retrieved_items,
            "top_match": top_match[:50] if top_match else None
        })

    def log_error(self, error_type: str, message: str, 
                  context: Optional[Dict[str, Any]] = None) -> None:
        """Log an error with context."""
        error_details = {"error_type": error_type, "message": message}
        if context:
            error_details["context"] = context
        self.log_event("ERROR", error_details)
        self.logger.error(f"{error_type}: {message}")

    def log_info(self, message: str) -> None:
        """Log general info."""
        self.logger.info(message)
