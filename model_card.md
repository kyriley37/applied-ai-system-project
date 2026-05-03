# Model Card: Mood Machine

This model card documents the advanced Mood Machine system developed from the AI110 Module 3 starter project.
It focuses on the enhanced rule-based model and the agentic workflow with retrieval-augmented reasoning.

## 1. Model Overview

**Model type:**
I used the enhanced rule-based model integrated into an agentic system. The main prediction path uses `MoodAnalyzer` plus `MoodAgent` and `MoodKnowledgeBase`.

**Intended purpose:**
The model classifies short text into mood labels: `positive`, `negative`, `neutral`, or `mixed`.
It is designed to help analyze sentiment in brief messages, including posts with emotional nuance.

**How it works (brief):**
- `MoodAnalyzer` preprocesses text, removes punctuation, normalizes repeated characters, and tokenizes input.
- It assigns scores using positive/negative word lists, weighted strong words, negation detection, and emoticon handling.
- `MoodKnowledgeBase` retrieves similar labeled posts from the sample dataset using word overlap.
- `MoodAgent` synthesizes the direct score and retrieved consensus to make a final prediction and compute confidence.

## 2. Data

**Dataset description:**
The dataset uses the six starter posts in `dataset.py` with matching labels in `TRUE_LABELS`.
No additional posts were added for this submission, so the dataset remains small and focused on the starter examples.

**Labeling process:**
Original labels were kept from the starter dataset. Labels reflect the human interpretation of each snippet's emotional tone.
For example, `Feeling tired but kind of hopeful` was labeled `mixed` because it contains both negative and positive sentiment.

**Important characteristics of your dataset:**
- Contains short, conversational posts
- Includes mixed sentiment and simple negation
- Uses everyday language, with one example of negation (`not happy`)
- Lacks strong slang, emoji diversity, or long-form text

**Possible issues with the dataset:**
- The dataset is extremely small, with only six examples
- It does not cover many language variations, slang, or sarcasm
- Label coverage is limited and may not represent broader mood expressions
- The model is effectively evaluated on its training examples, so accuracy is not a strong generalization measure

## 3. How the Rule Based Model Works

**Your scoring rules:**
- Positive words add score; negative words subtract score.
- Strong sentiment words receive higher weights.
- Negation words like `not`, `no`, `never`, `don't`, and `didn't` flip sentiment for adjacent tokens.
- Emoticons and simple emoji markers are mapped to strong sentiment signals.
- A final label mapping uses thresholds: score ≥ 2 → `positive`, score ≤ -2 → `negative`, and score between -1 and 1 for `neutral` or `mixed`.
- If both positive and negative words appear in weak-score text, the model returns `mixed`.

**Strengths of this approach:**
- Transparent and explainable: each decision is traceable through tokens and scores.
- Deterministic behavior: same input always produces the same output.
- Retrieval support improves reasoning by grounding choices in similar examples.
- Simple preprocessing helps handle punctuation and repeated characters.

**Weaknesses of this approach:**
- It struggles with subtle sentiment, sarcasm, and quieter forms of mixed emotion.
- The current dataset is too small to support generalization.
- The rule set is sensitive to exact wording and may misclassify ambiguous text.
- The `mixed` label logic is limited to simple token overlaps and does not capture nuance well.

## 4. How the ML Model Works (if used)

**Features used:**
The ML model code in `ml_experiments.py` is available but not the primary prediction path for this submission.
It uses scikit-learn and a simple feature representation to explore an alternative classification strategy.

**Training data:**
The model can train on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**
Because the dataset is very small, the ML version would likely overfit and is best used as an experimental comparison rather than a production model.

**Strengths and weaknesses:**
- Strength: ML can capture patterns without explicit rules.
- Weakness: With six examples, it can memorize labels rather than generalize.

## 5. Evaluation

**How you evaluated the model:**
I evaluated the agentic rule-based system on the labeled starter dataset in `dataset.py`.

**Observed accuracy:**
The system achieved **66.7% accuracy** on the six sample posts.

**Examples of correct predictions:**
- `I love this class so much` → **positive** (correct)
- `Today was a terrible day` → **negative** (correct)
- `So excited for the weekend` → **positive** (correct)

**Examples of incorrect predictions:**
- `Feeling tired but kind of hopeful` was predicted **negative** instead of `mixed`.
- `This is fine` was predicted **negative** instead of `neutral`.

These errors show that the system can over-weight negative signals when the text is weakly positive or mixed.

## 6. Limitations

- The dataset is very small and not diverse.
- The system does not generalize reliably to longer or more idiomatic text.
- It can misinterpret mixed mood statements and neutral but emotionally charged phrases.
- The current rule-based scoring is still too coarse for subtle sentiment.
- Retrieval uses simple word overlap, which can miss semantic similarity.

## 7. Ethical Considerations

- Mood detection systems can misclassify emotional expressions and affect trust.
- Incorrect predictions could cause poor support decisions if applied to real user messages.
- The model may not handle language variations, cultural expressions, or nonstandard phrasing fairly.
- If used on personal data, privacy and consent are important concerns.

## 8. Ideas for Improvement

- Add more labeled data and diverse text examples.
- Expand the dataset with slang, emojis, sarcasm, and mixed emotions.
- Use embeddings or TF-IDF for better similarity in retrieval.
- Improve negation and phrase-level sentiment handling.
- Add a separate evaluation set rather than holding out the same training examples.
- Integrate the ML model path more fully and compare performance against the rule-based agent.
