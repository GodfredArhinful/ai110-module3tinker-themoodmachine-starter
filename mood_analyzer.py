# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


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

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()

        # Use regex to split into words and preserve emoji/non-word symbols.
        # This is better than a simple split because it removes punctuation
        # like commas and periods while still keeping emojis as tokens.
        raw_tokens = re.findall(r"\w+|[^\w\s]", cleaned)

        punctuation = set(string.punctuation) | {"…", "“", "”", "—", "–"}
        tokens = [token for token in raw_tokens if token not in punctuation]

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.
        """
        tokens = self.preprocess(text)
        score = 0
        negation_words = {"not", "never", "no"}
        positive_emojis = {"🔥", "😂", "😊", "😄", "😅", "🙂", "🤣", "😍"}
        negative_emojis = {"😒", "😢", "😓", "😞", "😠", "😡", "🥲", "💀"}

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token in negation_words and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token in self.positive_words:
                    score -= 1
                    i += 2
                    continue
                if next_token in self.negative_words:
                    score += 1
                    i += 2
                    continue

            if token in self.positive_words or token in positive_emojis:
                score += 1
            elif token in self.negative_words or token in negative_emojis:
                score -= 1

            i += 1

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.
        """
        tokens = self.preprocess(text)
        score = self.score_text(text)
        positive_signals = [t for t in tokens if t in self.positive_words or t in {"🔥", "😂", "😊", "😄", "😅", "🙂", "🤣", "😍"}]
        negative_signals = [t for t in tokens if t in self.negative_words or t in {"😒", "😢", "😓", "😞", "😠", "😡", "🥲", "💀"}]

        if positive_signals and negative_signals:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
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
