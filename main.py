"""
Entry point for the Advanced Mood Machine with Agentic Workflow.

Features:
- Agentic Mood Analysis: Intelligent multi-step reasoning
- Retrieval-Augmented Generation (RAG): Retrieves similar posts for context
- Comprehensive Logging: Tracks all decisions for transparency
- Validation Suite: Tests consistency, accuracy, and calibration
"""

from typing import List

from mood_analyzer import MoodAnalyzer
from retrieval import MoodKnowledgeBase
from mood_agent import MoodAgent
from logger import MoodMachineLogger
from validator import MoodMachineValidator
from dataset import SAMPLE_POSTS, TRUE_LABELS


# Initialize system components
logger = MoodMachineLogger(log_dir="logs")
rule_analyzer = MoodAnalyzer()
knowledge_base = MoodKnowledgeBase(SAMPLE_POSTS, TRUE_LABELS, logger)
agent = MoodAgent(rule_analyzer, knowledge_base, logger)
validator = MoodMachineValidator(agent, logger)


def display_analysis_result(result: dict) -> None:
    """Pretty-print an analysis result."""
    print("\n" + "=" * 70)
    print(f"Mood: {result['predicted_mood'].upper()}")
    print(f"Confidence: {result['confidence']:.0%}")
    
    if "error" not in result:
        print(f"\nScore: {result['direct_score']}")
        print(f"\nSimilar Posts:")
        for post in result['retrieved_posts']:
            print(f"  • {post['text']}")
            print(f"    → {post['label']} (similarity: {post['similarity']})")
    
    print(f"\nReasoning:")
    print(result['reasoning'])
    print("=" * 70)


def evaluate_rule_based(posts: List[str], labels: List[str]) -> float:
    """
    Evaluate the agent on a labeled dataset (compatible with old interface).
    """
    correct = 0
    total = len(posts)

    print("\n=== Agent Evaluation on SAMPLE_POSTS ===")
    for text, true_label in zip(posts, labels):
        result = agent.analyze_mood(text)
        predicted_label = result["predicted_mood"]
        is_correct = predicted_label == true_label
        if is_correct:
            correct += 1

        print(
            f'"{text}" -> predicted={predicted_label}, '
            f'true={true_label} (conf={result["confidence"]:.0%})'
        )

    if total == 0:
        print("\nNo labeled examples to evaluate.")
        return 0.0

    accuracy = correct / total
    print(f"\nAgent accuracy on SAMPLE_POSTS: {accuracy:.2f}")
    return accuracy


def run_batch_demo() -> None:
    """
    Run the agent on the sample posts and print predictions.
    """
    print("\n=== Batch Demo on SAMPLE_POSTS (agent-based) ===")
    for text in SAMPLE_POSTS:
        result = agent.analyze_mood(text)
        print(
            f'"{text}" -> {result["predicted_mood"]} '
            f'(confidence: {result["confidence"]:.0%})'
        )


def run_interactive_loop() -> None:
    """
    Let the user type sentences and see the analysis.
    Type 'quit' or press Enter on an empty line to exit.
    """
    print("\n=== Interactive Mood Machine (agent-based with RAG) ===")
    print("Type a sentence to analyze its mood.")
    print("Type 'quit' or press Enter on an empty line to exit.")
    print("Type 'verbose' to see detailed reasoning.\n")

    verbose_mode = False

    while True:
        user_input = input("You: ").strip()
        if user_input == "" or user_input.lower() == "quit":
            print("Goodbye from the Mood Machine.")
            break

        if user_input.lower() == "verbose":
            verbose_mode = not verbose_mode
            print(f"Verbose mode: {'ON' if verbose_mode else 'OFF'}")
            continue

        result = agent.analyze_mood(user_input)

        if verbose_mode:
            display_analysis_result(result)
        else:
            print(
                f"Model: {result['predicted_mood']} "
                f"(confidence: {result['confidence']:.0%})"
            )


def run_validation_suite() -> None:
    """
    Run the comprehensive validation suite.
    """
    print("\n=== Running Validation Suite ===")
    validator.run_full_validation()
    validator.print_validation_report()


if __name__ == "__main__":
    logger.log_info("Starting Advanced Mood Machine")
    
    # Display welcome message
    print("\n" + "=" * 70)
    print("ADVANCED MOOD MACHINE")
    print("Agentic Workflow with RAG and Comprehensive Testing")
    print("=" * 70)
    print("\nAvailable modes:")
    print("1. Quick evaluation")
    print("2. Batch demo")
    print("3. Interactive analysis")
    print("4. Validation suite")
    print("5. All (default)\n")

    user_choice = input("Choose mode (1-5, or enter for all): ").strip()

    if user_choice in ["1", ""]:
        evaluate_rule_based(SAMPLE_POSTS, TRUE_LABELS)
    if user_choice in ["2", ""]:
        run_batch_demo()
    if user_choice in ["3", ""]:
        run_interactive_loop()
    if user_choice in ["4", ""]:
        run_validation_suite()
    if user_choice == "5":
        evaluate_rule_based(SAMPLE_POSTS, TRUE_LABELS)
        run_batch_demo()
        run_validation_suite()

    logger.log_info("Mood Machine session ended")
    print("\n✓ Check 'logs/' directory for detailed logs of all operations.")
