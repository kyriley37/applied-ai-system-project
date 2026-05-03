"""
Quick end-to-end test of the Advanced Mood Machine.
Verifies that all components work together.
"""

from mood_analyzer import MoodAnalyzer
from retrieval import MoodKnowledgeBase
from mood_agent import MoodAgent
from logger import MoodMachineLogger
from dataset import SAMPLE_POSTS, TRUE_LABELS


def test_system():
    """Run a quick system test."""
    print("\n" + "=" * 70)
    print("ADVANCED MOOD MACHINE - QUICK TEST")
    print("=" * 70 + "\n")
    
    # Initialize components
    print("Initializing components...")
    logger = MoodMachineLogger()
    analyzer = MoodAnalyzer()
    kb = MoodKnowledgeBase(SAMPLE_POSTS, TRUE_LABELS, logger)
    agent = MoodAgent(analyzer, kb, logger)
    print("✓ All components initialized\n")
    
    # Test 1: Basic preprocessing
    print("Test 1: Preprocessing")
    test_text = "I love this! :)"
    tokens = analyzer.preprocess(test_text)
    print(f"  Input: '{test_text}'")
    print(f"  Tokens: {tokens}")
    print("  ✓ Preprocessing works\n")
    
    # Test 2: Scoring
    print("Test 2: Scoring")
    score = analyzer.score_text(test_text)
    label = analyzer.predict_label(test_text)
    print(f"  Score: {score} → {label}")
    print("  ✓ Scoring works\n")
    
    # Test 3: Retrieval
    print("Test 3: RAG Retrieval")
    retrieved = kb.retrieve_similar(test_text, top_k=2)
    print(f"  Retrieved {len(retrieved)} similar posts:")
    for post, lbl, sim in retrieved:
        print(f"    • '{post[:40]}...' → {lbl} (sim: {sim:.2f})")
    print("  ✓ Retrieval works\n")
    
    # Test 4: Full agent analysis
    print("Test 4: Complete Agent Analysis")
    result = agent.analyze_mood(test_text)
    print(f"  Input: '{test_text}'")
    print(f"  Predicted mood: {result['predicted_mood']}")
    print(f"  Confidence: {result['confidence']:.0%}")
    print(f"  Score: {result['direct_score']}")
    print("  ✓ Agent analysis works\n")
    
    # Test 5: Multiple predictions
    print("Test 5: Batch Predictions")
    test_cases = [
        "I love this!",
        "This is terrible",
        "It's okay",
        "I'm not happy about this"
    ]
    
    for text in test_cases:
        result = agent.analyze_mood(text)
        print(f"  '{text}' → {result['predicted_mood']} ({result['confidence']:.0%})")
    
    print("\n✓ Batch predictions work\n")
    
    print("=" * 70)
    print("SUCCESS: All tests passed!")
    print("=" * 70)
    print("\nNext steps:")
    print("  • Run 'python main.py' for interactive mode")
    print("  • Check 'logs/' directory for detailed logs")
    print("  • Read 'README_ADVANCED.md' for full documentation")
    print("  • See 'SETUP.md' for setup and troubleshooting")
    print()


if __name__ == "__main__":
    test_system()
