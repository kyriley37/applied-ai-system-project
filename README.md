# The Mood Machine (Advanced Submission)

This project is based on the AI110 Module 3 starter repo: `ai110-module3tinker-themoodmachine-starter`.
It extends the original Mood Machine with an **agentic workflow**, **retrieval-augmented reasoning**, **logging**, **validation**, and **system architecture documentation**.

## What this project does

The Advanced Mood Machine analyzes short text and predicts mood labels such as **positive**, **negative**, **neutral**, or **mixed**.
It combines:

- A rule-based sentiment scorer in `mood_analyzer.py`
- A retrieval system in `retrieval.py` that finds similar examples from the dataset
- An agent orchestrator in `mood_agent.py` that reasons through multiple steps
- A validation suite in `validator.py` to measure consistency, accuracy, and confidence calibration
- A logger in `logger.py` to capture reasoning and errors

## Repo structure

```plaintext
├── assets/                 # Architecture diagrams and demo screenshots
├── dataset.py              # Sample posts, labels, and word lists
├── logger.py               # Central logging and guardrails
├── main.py                 # Entry point with interactive and validation modes
├── mood_agent.py           # Agentic workflow with RAG integration
├── mood_analyzer.py        # Enhanced rule-based scoring model
├── model_card.md           # Reflections, biases, testing, and limitations
├── requirements.txt        # Python dependencies
├── retrieval.py            # Retrieval-Augmented Generation knowledge base
├── test_system.py          # Quick end-to-end verification script
├── validator.py            # Reliability and testing suite
└── README.md               # Project overview and submission guide
```

## Setup and run

1. Open this folder in VS Code.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python main.py
```

4. Select a mode:

- `1` → Quick evaluation against the sample dataset
- `2` → Batch demo predictions
- `3` → Interactive analysis (type text, or `verbose` for detailed reasoning)
- `4` → Run the validation suite
- Enter nothing to run all modes

## Demo walkthrough

### Example inputs and AI responses

- Input: `I love this class so much` → Prediction: **positive**
- Input: `Today was a terrible day` → Prediction: **negative**
- Input: `Feeling tired but kind of hopeful` → Prediction: **negative**
- Input: `This is fine` → Prediction: **negative**
- Input: `So excited for the weekend` → Prediction: **positive**
- Input: `I am not happy about this` → Prediction: **negative**

These examples show how the system uses both rule-based scoring and retrieved similar posts to create a final prediction.

### Screenshots

Below are screenshots from the running system and architecture visuals.

![System Architecture](assets/System_architecture.png)

![RAG System](assets/RAG_system.jpeg)

![Testing Framework](assets/Testing_Framework.jpeg)

## Submission checklist

- [x] Code pushed to public GitHub repository
- [x] Functional code present: `main.py`, `mood_analyzer.py`, `mood_agent.py`, `retrieval.py`, `logger.py`, `validator.py`
- [x] Comprehensive `README.md`
- [x] `model_card.md` completed with reflections
- [x] System architecture diagram available in `assets/`
- [x] Organized assets in `assets/`
- [x] Demo walkthrough included via screenshots above
- [x] Final changes committed and pushed

## Notes on the architecture

The system architecture is stored in `assets/System_architecture.png` and embedded above. The architecture shows how input text flows through the agent, rule-based scoring, retrieval, logging, and output.

## Additional documentation

- `model_card.md` contains reflection prompts and answers for model behavior, bias, dataset limitations, and testing.
- `assets/` contains architecture and demo images.
- `test_system.py` provides a quick end-to-end verification script.
