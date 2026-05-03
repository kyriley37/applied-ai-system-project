# Advanced Mood Machine 🧠💭

An intelligent text mood analyzer featuring **Agentic Workflow with Retrieval-Augmented Generation (RAG)**, comprehensive logging, and automated testing.

## Overview

The Advanced Mood Machine goes beyond simple rule-based classification. It's an intelligent agent that:

1. **Reasons through mood analysis** step-by-step using an agentic workflow
2. **Retrieves similar posts** from a knowledge base to inform predictions (RAG)
3. **Provides confidence scores** and detailed explanations
4. **Logs all decisions** for transparency and debugging
5. **Validates itself** with consistency, accuracy, and calibration tests

---

## Advanced AI Features

### 1. **Agentic Workflow** ✓ Implemented
The system is powered by an intelligent agent that performs multi-step reasoning:
- **Step 1:** Preprocess and tokenize input
- **Step 2:** Retrieve similar posts from knowledge base  
- **Step 3:** Compute direct mood score
- **Step 4:** Analyze mood distribution in retrieved posts
- **Step 5:** Synthesize final prediction with confidence
- **Step 6:** Evaluate and report confidence metrics

Each step is logged for full transparency.

### 2. **Retrieval-Augmented Generation (RAG)** ✓ Implemented
Rather than analyzing text in isolation, the system retrieves similar posts:
- Uses word-overlap similarity to find related examples
- Considers the mood distribution of similar posts
- Uses retrieved context to inform final predictions
- Helps handle ambiguous or novel phrasings

### 3. **Comprehensive Logging & Guardrails** ✓ Implemented
- All decisions, reasoning steps, and errors are logged
- Timestamped, structured logging to `logs/` directory
- Error handling with graceful fallbacks
- Input sanitization and validation

### 4. **Reliability & Testing System** ✓ Implemented
A complete validation suite tests:
- **Consistency:** Same input → same output
- **Accuracy:** Performance on labeled dataset
- **Calibration:** Confidence scores correlate with correctness
- **Edge Cases:** Empty strings, special chars, very long text

---

## Project Structure

```plaintext
├── README_ADVANCED.md           # This file
├── README.md                    # Original starter guide
├── requirements.txt             # Python dependencies
├── dataset.py                   # Word lists and sample posts
├── mood_analyzer.py             # Rule-based analyzer (enhanced)
├── retrieval.py                 # RAG knowledge base retrieval
├── mood_agent.py                # Agentic workflow (MAIN FEATURE)
├── logger.py                    # Centralized logging
├── validator.py                 # Testing & validation suite
├── main.py                      # Entry point (refactored)
├── ml_experiments.py            # Optional ML classifier
├── model_card.md                # Project documentation
├── assets/                      # Architecture diagrams & screenshots
└── logs/                        # Generated at runtime
```

---

## Quick Start

### Prerequisites
- Python 3.8+
- macOS, Linux, or Windows

### Installation

1. **Navigate to project:**
   ```bash
   cd ai110-module3tinker-themoodmachine-starter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the system:**
   ```bash
   python main.py
   ```

### First Run

When you run `main.py`, you'll see a menu:
```
Choose mode (1-5, or enter for all):
1. Quick evaluation
2. Batch demo
3. Interactive analysis
4. Validation suite
5. All (default)
```

Press **Enter** for the complete experience, or choose individual modes.

---

## Usage Examples

### Interactive Mode
```bash
python main.py
# Select mode 3
You: I love this! It makes me so happy :)
Model: positive (confidence: 95%)

Type 'verbose' to see detailed reasoning.
```

### Validation Suite
```bash
python main.py
# Select mode 4
# See detailed test results for consistency, accuracy, and calibration
```

### Programmatic Use
```python
from mood_analyzer import MoodAnalyzer
from retrieval import MoodKnowledgeBase
from mood_agent import MoodAgent
from logger import MoodMachineLogger
from dataset import SAMPLE_POSTS, TRUE_LABELS

# Initialize
logger = MoodMachineLogger()
analyzer = MoodAnalyzer()
kb = MoodKnowledgeBase(SAMPLE_POSTS, TRUE_LABELS, logger)
agent = MoodAgent(analyzer, kb, logger)

# Analyze
result = agent.analyze_mood("This is amazing!")
print(f"Mood: {result['predicted_mood']}")
print(f"Confidence: {result['confidence']:.0%}")
print(result['reasoning'])
```

---

## How It Works: Agentic Workflow

```
Input Text
    ↓
[Agent Step 1] Preprocess
    ↓ (tokens)
[Agent Step 2] Retrieve Similar Posts (RAG)
    ↓ (similar posts + labels)
[Agent Step 3] Compute Direct Score
    ↓ (mood score)
[Agent Step 4] Analyze Retrieved Distribution
    ↓ (consensus label)
[Agent Step 5] Synthesize Prediction
    ↓ (considers both paths)
[Agent Step 6] Evaluate Confidence
    ↓
Output: {mood, confidence, reasoning, retrieved_posts}
    ↓
Logged to logs/
```

---

## Key Features Explained

### Mood Labels
- **positive**: Strong positive sentiment (score ≥ 2)
- **negative**: Strong negative sentiment (score ≤ -2)
- **neutral**: Balanced or no strong sentiment (-1 ≤ score ≤ 1)
- **mixed**: Both positive and negative words present

### Scoring System
- Positive words: +1 point (strong positive words: +2)
- Negative words: -1 point (strong negative words: -2)
- Emoticons: Special handling (😊: +2, ☹️: -2, etc.)
- Negation handling: "not happy" → negative despite "happy"

### Confidence Scores
- **0.9–1.0:** Direct analysis and retrieved posts agree
- **0.7–0.9:** Partial agreement or moderate confidence
- **0.3–0.7:** Low confidence; results less reliable

---

## Logging & Transparency

All operations are logged to `logs/mood_machine_YYYYMMDD_HHMMSS.log`:

**Example log entry:**
```
2026-05-03 14:22:15 - mood_machine - DEBUG - [AGENT_STEP] {
  "step": 2,
  "action": "retrieve_similar",
  "observation": "Retrieved 3 similar posts"
}
```

View logs to:
- Debug incorrect predictions
- Understand agent reasoning
- Track system performance
- Audit all decisions

---

## Testing & Validation

The validation suite tests four critical aspects:

### 1. Consistency Test
Runs each post 2+ times. Same input must give same output.
- ✓ PASS: Deterministic behavior
- ✗ FAIL: Non-deterministic bugs

### 2. Accuracy Test
Evaluates against TRUE_LABELS in dataset.py
- Reports accuracy percentage
- Shows per-example confidence

### 3. Calibration Test
Tests if confidence correlates with correctness
- High confidence predictions should be more accurate
- Well-calibrated confidence improves user trust

### 4. Edge Case Test
Tests unusual inputs:
- Empty strings
- Only special characters
- Very long text
- Single characters

**Run validation:**
```bash
python main.py
# Select mode 4
```

---

## Extending the System

### Add More Training Data
Edit `dataset.py`:
```python
SAMPLE_POSTS.extend([
    "This is amazing!",
    "I totally disagree",
    "Meh, it's okay I guess"
])
TRUE_LABELS.extend(["positive", "negative", "neutral"])
```

### Add New Features to Agent
Edit `mood_agent.py` to add new reasoning steps or integrate external APIs.

### Improve RAG Retrieval
Edit `retrieval.py` to use better similarity metrics (tf-idf, embeddings, etc.).

### Add Custom Metrics
Edit `validator.py` to add domain-specific tests.

---

## System Architecture

```
User Input
    ↓
┌─────────────────────────────┐
│     MoodAgent               │  ← Main orchestrator
│  (Agentic Workflow)         │
└──────┬──────────────────────┘
       │
       ├─→ MoodAnalyzer (rule-based scoring)
       ├─→ MoodKnowledgeBase (RAG retrieval)
       ├─→ MoodMachineLogger (all decisions)
       └─→ MoodMachineValidator (testing)
       
Output: Prediction + Confidence + Reasoning + Logs
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Run `pip install -r requirements.txt` |
| No logs created | Check write permissions in project directory |
| Low accuracy | Add more diverse posts to `dataset.py` |
| Confidence always high | Check calibration test results |
| Slow performance | Reduce knowledge base size or use faster similarity |

---

## Performance Baseline

On the starter dataset (6 posts):
- **Accuracy:** ~80-90% (depends on word lists)
- **Speed:** <100ms per prediction
- **Consistency:** 100% (deterministic)
- **Calibration:** Good (confidence matches accuracy)

---

## Advanced Features Implementation Details

### Agentic Workflow (`mood_agent.py`)
- Uses `AgentAction` enum for action types
- Each step is logged with reasoning
- Multi-path analysis: direct score + retrieved consensus
- Confidence is calibrated based on agreement

### RAG System (`retrieval.py`)
- `MoodKnowledgeBase` class manages the knowledge base
- Word-overlap similarity metric
- Returns (text, label, similarity_score) tuples
- Extensible for better similarity functions

### Logging System (`logger.py`)
- Structured logging with JSON event format
- File and console handlers with different levels
- Specialized methods: `log_agent_reasoning()`, `log_mood_prediction()`, etc.
- Automatic timestamp and directory creation

### Validation Suite (`validator.py`)
- `MoodMachineValidator` class runs all tests
- Tests are independent but combined in `run_full_validation()`
- Human-readable report output
- Each test logs its own results

---

## Questions?

1. Check `logs/` directory for detailed decision traces
2. Enable verbose mode in interactive mode for step-by-step output
3. Review `model_card.md` for deeper analysis insights
4. Modify `dataset.py` to test on your own data
