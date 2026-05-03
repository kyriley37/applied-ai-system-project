# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

AAVE_PHRASE_NORMALIZATION = {
    "no cap": "no_cap",
    "on fleek": "on_fleek",
    "periodt": "periodt",
    "deadass": "deadass",
}

AAVE_INTENSIFIERS = {
    "mad": 2,
    "highkey": 2,
    "deadass": 2,
}

AAVE_MIXED_TERMS = {"lowkey", "highkey"}

AAVE_POSITIVE_WORDS = {
    "lit",
    "dope",
    "slay",
    "slaying",
    "periodt",
    "no_cap",
    "bet",
}

AAVE_NEGATIVE_WORDS = {
    "salty",
    "wack",
    "trash",
    "annoying",
    "weak",
}


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements implemented:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Removes most punctuation while preserving important markers
          - Handles simple emojis and emoticons
          - Normalizes repeated characters
        """
        import re
        
        cleaned = text.strip().lower()
        
        # Preserve and mark emoticons/emojis before punctuation removal
        emoticon_map = {
            ':)': 'smiley_positive',
            ':-)': 'smiley_positive',
            ':-(': 'smiley_negative',
            ':(': 'smiley_negative',
            ':D': 'smiley_very_positive',
            ':P': 'smiley_playful',
            '😂': 'smiley_positive',
            '🥲': 'smiley_mixed',
            '💀': 'smiley_negative',
        }

        for emoticon, marker in emoticon_map.items():
            if emoticon in cleaned:
                cleaned = cleaned.replace(emoticon, f' {marker} ')

        # Normalize common AAVE phrases before punctuation removal
        for phrase, normalized in AAVE_PHRASE_NORMALIZATION.items():
            cleaned = cleaned.replace(phrase, f' {normalized} ')

        # Remove extra punctuation but keep apostrophes for contractions
        cleaned = re.sub(r'[.,!?;:"@#$%^&*()\-_+=\[\]{}<>|`~]', ' ', cleaned)
        
        # Normalize repeated characters (e.g., "soooo" -> "soo")
        cleaned = re.sub(r'(.)\1{2,}', r'\1\1', cleaned)
        
        # Split on whitespace and filter empty strings
        tokens = [t for t in cleaned.split() if t]
        
        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        Improvements implemented:
          - Handle simple negation such as "not happy" or "not bad"
          - Give some words higher weights (intensifiers)
          - Handle emoticons/emojis as strong signals
        """
        tokens = self.preprocess(text)
        
        # Define word weights (stronger words have higher impact)
        strong_positive = {"love", "amazing", "awesome", "excellent", "wonderful", "fantastic"}
        strong_negative = {"hate", "terrible", "awful", "horrible", "disgusting"}

        # Negation words that flip sentiment
        negation_words = {"not", "no", "never", "ain't", "nah", "naw", "isn't", "doesn't", "don't", "didn't"}
        
        score = 0
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            # Check for negation in previous token
            is_negated = False
            if i > 0 and tokens[i - 1] in negation_words:
                is_negated = True
            
            # Apply AAVE-specific sentiment signals first
            if token in AAVE_POSITIVE_WORDS:
                weight = 2
                if i > 0 and tokens[i - 1] in AAVE_INTENSIFIERS:
                    weight *= AAVE_INTENSIFIERS[tokens[i - 1]]
                score += weight if not is_negated else -weight
            elif token in AAVE_NEGATIVE_WORDS:
                weight = 2
                if i > 0 and tokens[i - 1] in AAVE_INTENSIFIERS:
                    weight *= AAVE_INTENSIFIERS[tokens[i - 1]]
                score -= weight if not is_negated else weight
            # Score positive words
            elif token in self.positive_words:
                weight = 2 if token in strong_positive else 1
                if i > 0 and tokens[i - 1] in AAVE_INTENSIFIERS:
                    weight *= AAVE_INTENSIFIERS[tokens[i - 1]]
                score += weight if not is_negated else -weight
            # Score negative words
            elif token in self.negative_words:
                weight = 2 if token in strong_negative else 1
                if i > 0 and tokens[i - 1] in AAVE_INTENSIFIERS:
                    weight *= AAVE_INTENSIFIERS[tokens[i - 1]]
                score -= weight if not is_negated else weight
            # Score emoticons
            elif token == "smiley_positive":
                score += 2
            elif token == "smiley_very_positive":
                score += 3
            elif token == "smiley_negative":
                score -= 2
            elif token == "smiley_playful":
                score += 1
            elif token == "smiley_mixed":
                score += 0
            
            i += 1
        
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Improvements implemented:
          - Use nuanced thresholds for better classification
          - Support "mixed" label for borderline cases
          - Align with TRUE_LABELS format from dataset.py

        Mapping:
          - score >= 2  -> "positive"
          - score <= -2 -> "negative"
          - -1 <= score <= 1 -> "neutral"
          - score in [-1, 1] with mixed indicators -> "mixed"
        """
        score = self.score_text(text)
        
        if score >= 2:
            return "positive"
        elif score <= -2:
            return "negative"
        elif -1 <= score <= 1:
            # Could be neutral or mixed - check for signs of both sentiments
            tokens = self.preprocess(text)
            has_positive = any(t in self.positive_words for t in tokens)
            has_negative = any(t in self.negative_words for t in tokens)
            
            has_aave_mixed = any(t in AAVE_MIXED_TERMS for t in tokens)
            if has_positive and has_negative:
                return "mixed"
            elif has_aave_mixed and (has_positive or has_negative):
                return "mixed"
            else:
                return "neutral"
        else:
            # -1 to 1 range
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
