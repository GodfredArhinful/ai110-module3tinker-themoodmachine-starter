# Model Card: Mood Machine

This model card documents the Mood Machine project, including both the rule-based model in `mood_analyzer.py` and the ML model in `ml_experiments.py`.

## 1. Model Overview

**Model type:**  
I used both models. The rule-based model is the main system for interpreting mood from short text, and the ML model is a comparison using `scikit-learn`.

**Intended purpose:**  
The system is meant to classify short text posts or messages into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**  
- Rule based model: tokenizes input text, looks for positive and negative words, applies simple scoring rules, and maps the score to a label. It also uses a small negation rule and treats emojis as sentiment signals.
- ML model: converts text into bag-of-words features with `CountVectorizer`, then trains a logistic regression classifier on the same labeled dataset.

## 2. Data

**Dataset description:**  
The dataset is stored in `dataset.py`. It includes 14 short example posts after expansion. I added realistic posts with slang, emojis, mixed emotions, and subtle tone.

**Labeling process:**  
Each new post was given one label in `TRUE_LABELS`. I chose labels based on the overall mood expressed. Hard labels included mixed-feeling sentences like `"Feeling tired but kind of hopeful"` and ambiguous tone sentences like `"This is fine"`.

**Important characteristics of your dataset:**  
- Contains slang such as `lowkey`, `no cap`, `highkey`, `sick`, and `fire`
- Includes emojis like `😅`, `🔥`, `🙂`, and `😒`
- Has mixed-emotion examples such as `"Feeling tired but kind of hopeful"`
- Contains short, ambiguous messages like `"This is fine"` and `"I guess it's fine, no big deal"`

**Possible issues with the dataset:**  
- It is small, with only 14 examples
- It is not balanced across all labels and relies on manually chosen vocabulary
- It may miss dialects, cultural references, or longer texts
- Some sentences are ambiguous and could be labeled differently by different people

## 3. How the Rule Based Model Works

**Your scoring rules:**  
- Text is lowercased and tokenized using regex to remove punctuation while preserving emojis.
- Each token is compared to a set of positive words and a set of negative words.
- A positive word or emoji adds `+1`; a negative word or emoji subtracts `-1`.
- Simple negation handling is applied: `not happy` is treated as negative and `not bad` as positive.
- If both positive and negative signals appear in the same sentence, the model returns `mixed`.
- Otherwise, the score is mapped to `positive`, `negative`, or `neutral`.

**Strengths of this approach:**  
- Transparent and easy to reason about
- Works well on clear examples like `"I love this class so much"` and `"Today was a terrible day"`
- Can incorporate slang and emoji rules explicitly

**Weaknesses of this approach:**  
- It depends on the words included in the lexicon
- It misclassifies mixed sentences when one sentiment side is missing from the vocabulary
- It cannot reliably detect sarcasm or subtle tone
- It is brittle for unseen slang or new expressions

## 4. How the ML Model Works

**Features used:**  
The ML model uses a bag-of-words representation with `CountVectorizer`.

**Training data:**  
It trains on the same `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**  
Because the model is evaluated on the same data it was trained on, it usually reports perfect or near-perfect accuracy. This is training accuracy rather than a measure of how well it generalizes to new text.

**Strengths and weaknesses:**  
- Strength: it learns patterns automatically from words in the dataset
- Weakness: it can overfit to the exact training examples and rely on spurious words that happen to appear in one label
- Weakness: it may not handle unseen slang or emojis unless they appear in training data

## 5. Evaluation

**How you evaluated the model:**  
Both versions were evaluated on the labeled posts in `dataset.py`. The rule-based model used `main.py` and the ML model used `ml_experiments.py`.

**Examples of correct predictions:**  
- `"I love this class so much"` → positive: clear positive word `love`.
- `"Today was a terrible day"` → negative: clear negative word `terrible`.
- `"This food is fire 🔥"` → positive: slang `fire` was added to the vocabulary and the emoji is treated as positive.

**Examples of incorrect predictions:**  
- `"Feeling tired but kind of hopeful"` → predicted `negative`, true `mixed`. Failure happened because `tired` was in the negative list but `hopeful` was not recognized as positive.
- `"Ugh, rain again… but honestly cozy vibes"` → predicted `neutral`, true `mixed`. Failure happened because `cozy` was not in the positive vocabulary and the model only saw the negative feeling.
- `"Not sure if I should laugh or cry right now"` → predicted `neutral`, true `mixed`. The model missed both positive and negative signals in that phrase.

If using both models, the ML model can memorize the dataset and achieve near-perfect accuracy on training data, while the rule-based model is more interpretable but limited by its vocabulary.

## 6. Limitations

- The dataset is small (14 examples) and not representative of real-world mood language.
- The rule-based model relies heavily on exact word matches. If words like `hopeful`, `cozy`, or `annoyed` are missing, the model fails.
- The rule-based model cannot reliably detect sarcasm such as `"I love getting stuck in traffic"`.
- The ML model reports perfect accuracy on training data because it is evaluated on the same examples it was trained on; this does not guarantee good performance on new text.
- The system may misinterpret language from communities or dialects not represented in the dataset.

## 7. Ethical Considerations

- Mood detection can be sensitive. Misclassifying text that expresses sadness or distress could cause harm if used in a real application.
- The model is optimized for short English posts with slang and emoji, not for long essays or non-English text.
- It may not work well for people who use very different slang, dialect, or cultural references than those in the dataset.
- If this system were applied to private messages, privacy and consent must be considered.

## 8. Ideas for Improvement

- Add more labeled examples and a separate test set for true evaluation.
- Expand vocabulary with more slang, emoji signals, and synonyms like `hopeful`, `cozy`, `annoyed`, and `laugh`.
- Improve preprocessing to normalize contractions, punctuation, and repeated letters.
- Use TF-IDF or a larger feature set instead of raw CountVectorizer counts.
- Add a more robust mixed-sentiment rule or a learned classifier that can generalize beyond exact word matches.
- Compare the rule-based predictions and ML predictions on held-out examples to find where each model fails.
