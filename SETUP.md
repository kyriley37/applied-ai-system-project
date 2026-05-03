# Setup Guide: Advanced Mood Machine

## System Overview

This project implements an advanced mood analysis system with three key AI features:

1. **Agentic Workflow** - Multi-step reasoning about mood classification
2. **Retrieval-Augmented Generation (RAG)** - Uses similar examples to inform predictions
3. **Comprehensive Testing** - Validates consistency, accuracy, and confidence calibration

---

## Installation Instructions

### Step 1: Verify Python Installation
```bash
python --version
# Should be 3.8 or higher
```

If you don't have Python, install from https://www.python.org/

### Step 2: Navigate to Project
```bash
cd /Users/karringtonriley/applied-ai-system-project/ai110-module3tinker-themoodmachine-starter
```

### Step 3: Create Virtual Environment (Optional but Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `scikit-learn` - Machine learning utilities
- `matplotlib` - Data visualization
- `ipykernel` - Jupyter notebook support

### Step 5: Verify Installation
```bash
python -c "import sklearn; import matplotlib; print('✓ All dependencies installed')"
```

---

## Running the System

### Quick Start (All Modes)
```bash
python main.py
# Press Enter to run all modes
```

This runs:
1. Quick evaluation on sample posts
2. Batch demo showing predictions
3. Validation suite (consistency, accuracy, calibration)

### Individual Modes

**Mode 1: Quick Evaluation**
```bash
python main.py
# Choose: 1
# Compares predictions to true labels
```

**Mode 2: Batch Demo**
```bash
python main.py
# Choose: 2
# Predicts mood for each sample post
```

**Mode 3: Interactive Analysis**
```bash
python main.py
# Choose: 3
# Type sentences and get mood analysis
# Type 'verbose' for detailed reasoning
# Type 'quit' to exit
```

**Mode 4: Validation Suite**
```bash
python main.py
# Choose: 4
# Tests consistency, accuracy, calibration, edge cases
# Prints professional report
```

---

## Understanding the Output

### Basic Prediction
```
You: I love this!
Model: positive (confidence: 95%)
```

### Verbose Mode Output
```
===============================================================================
Mood: POSITIVE
Confidence: 95%

Score: 2

Similar Posts:
  • "I love this class so much" 
    → positive (similarity: 0.80)

Reasoning:
Analysis of: 'I love this!'

Direct Analysis:
  - Score: 2 → positive

Retrieved Similar Posts (1 found):
  1. 'I love this class so much' → positive (similarity: 0.80)

Synthesis:
  - Consensus mood from similar posts: positive
  - Confidence: 95%
  - Agent reasoning: Agreement between direct and retrieved analysis
===============================================================================
```

### Validation Report
```
MOOD MACHINE VALIDATION REPORT
======================================================================
Accuracy: 83.33% (5/6)
Consistency: 6/6 tests passed
Confidence Calibration: Well-calibrated ✓
  - High confidence accuracy (>=75%): 85%
  - Low confidence accuracy (<75%): 60%

Edge Case Tests:
  ✓ empty_string
  ✓ whitespace_only
  ✓ special_chars_only
  ✓ very_long
  ✓ single_character
  ✓ repeated_words
======================================================================
```

---

## Logs and Debugging

### View Latest Log
```bash
ls -lt logs/ | head -5
cat logs/mood_machine_*.log | tail -50
```

### Log Contents
Each log file contains timestamped entries like:
```
2026-05-03 14:22:15 - mood_machine - DEBUG - [AGENT_STEP] {
  "step": 1,
  "action": "preprocess",
  "observation": "Tokenized input into 4 tokens"
}
2026-05-03 14:22:15 - mood_machine - DEBUG - [AGENT_STEP] {
  "step": 2,
  "action": "retrieve_similar",
  "observation": "Retrieved 3 similar posts"
}
```

### Filter Logs by Type
```bash
# See only predictions
grep "MOOD_PREDICTION" logs/mood_machine_*.log

# See only errors
grep "ERROR" logs/mood_machine_*.log

# See retrieval operations
grep "RAG_RETRIEVAL" logs/mood_machine_*.log
```

---

## Customizing the System

### Add Training Data
1. Edit `dataset.py`
2. Add posts to `SAMPLE_POSTS`
3. Add corresponding labels to `TRUE_LABELS`
4. Keep lists same length

Example:
```python
SAMPLE_POSTS.extend([
    "I'm super excited!",
    "This is frustrating",
    "The weather is fine"
])
TRUE_LABELS.extend(["positive", "negative", "neutral"])
```

### Modify Scoring Rules
Edit `mood_analyzer.py`:
- Change weights in `score_text()` (strong_positive, strong_negative)
- Add negation patterns
- Adjust thresholds in `predict_label()`

### Improve Similarity Matching
Edit `retrieval.py`:
- Replace `_compute_similarity()` with better metric
- Add TF-IDF or embedding-based similarity
- Use fuzzy matching for typos

### Add Custom Tests
Edit `validator.py`:
- Add new test methods to `MoodMachineValidator`
- Call them in `run_full_validation()`
- Create specialized test cases

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'sklearn'"
**Solution:** Install requirements again
```bash
pip install -r requirements.txt
```

### "PermissionError: [Errno 13]" when creating logs
**Solution:** Check directory permissions
```bash
chmod 755 .
```

### "Could not find matching text to replace" (if editing files)
**Solution:** Use proper whitespace matching; use VS Code for editing

### Low accuracy on validation
**Solution:**
1. Add more diverse training data to `dataset.py`
2. Check word lists in `dataset.py` (POSITIVE_WORDS, NEGATIVE_WORDS)
3. Review logs to see which predictions failed
4. Adjust scoring weights in `mood_analyzer.py`

### Same text produces different results
**Solution:** This should not happen (deterministic). Check:
- Random number usage (shouldn't have any)
- File changes during runtime
- Concurrent modifications

---

## Project Files Explained

| File | Purpose |
|------|---------|
| `main.py` | Entry point; orchestrates modes |
| `mood_analyzer.py` | Rule-based scoring and preprocessing |
| `mood_agent.py` | **Agentic workflow (main feature)** |
| `retrieval.py` | **RAG knowledge base system** |
| `logger.py` | **Logging and guardrails** |
| `validator.py` | **Testing and validation suite** |
| `dataset.py` | Training data and word lists |
| `requirements.txt` | Python dependencies |
| `logs/` | Generated at runtime |
| `assets/` | Architecture diagrams/screenshots |

---

## Performance Tips

### Speed Up Processing
- Reduce knowledge base size (fewer similar posts to retrieve)
- Use faster similarity metric
- Cache similarity scores

### Improve Accuracy
- Add diverse training examples
- Expand word lists
- Tune scoring thresholds
- Handle more edge cases (sarcasm, slang)

### Better Confidence
- Calibrate thresholds based on test results
- Increase agreement weight in agent synthesis
- Use confidence history from past predictions

---

## Next Steps

1. **Run the system** with all modes to see it in action
2. **Check logs** to understand agent reasoning
3. **Modify dataset** to add your own posts
4. **Improve accuracy** by adjusting word lists and thresholds
5. **Extend functionality** by adding new features

---

## Key Concepts

### Agentic Workflow
The system acts like an intelligent agent that:
- Takes user input
- Plans its approach (retrieve, score, synthesize)
- Observes intermediate results
- Adjusts final decision based on confidence

### RAG (Retrieval-Augmented Generation)
Instead of predicting in isolation:
- Find similar examples from knowledge base
- Consider mood distribution of similar posts
- Use consensus to inform final prediction

### Confidence Score
Ranges 0-1, indicates how sure the system is:
- Based on agreement between direct analysis and retrieved consensus
- Calibrated so confidence correlates with accuracy
- Helps users understand result reliability

---

## Questions or Issues?

1. Check logs in `logs/` directory
2. Run validation suite (mode 4) for system health check
3. Review `README_ADVANCED.md` for detailed documentation
4. Trace through `mood_agent.py` step-by-step logic
