"""
Testing and Validation Suite for the Mood Machine.

Includes:
- Consistency tests (same input → same output)
- Accuracy evaluation
- Edge case testing
- Confidence calibration checks
"""

from typing import List, Dict
from mood_analyzer import MoodAnalyzer
from retrieval import MoodKnowledgeBase
from mood_agent import MoodAgent
from logger import MoodMachineLogger
from dataset import SAMPLE_POSTS, TRUE_LABELS


class MoodMachineValidator:
    """
    Validates the mood analysis system for reliability and consistency.
    """

    def __init__(self, agent: MoodAgent, logger: MoodMachineLogger):
        """Initialize validator with agent and logger."""
        self.agent = agent
        self.logger = logger
        self.results = {}

    def test_consistency(self, texts: List[str], iterations: int = 3) -> Dict:
        """
        Test that same inputs produce same outputs (consistency test).
        
        Runs each text multiple times and checks if results are identical.
        """
        self.logger.log_info("Running consistency tests...")
        
        consistency_results = {
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        for text in texts:
            predictions = []
            for _ in range(iterations):
                result = self.agent.analyze_mood(text)
                predictions.append(result["predicted_mood"])
            
            # Check if all predictions are the same
            if len(set(predictions)) == 1:
                consistency_results["passed"] += 1
                status = "PASS"
            else:
                consistency_results["failed"] += 1
                status = "FAIL"
            
            consistency_results["details"].append({
                "text": text[:50],
                "predictions": predictions,
                "status": status
            })
        
        self.logger.log_event("CONSISTENCY_TEST", {
            "passed": consistency_results["passed"],
            "failed": consistency_results["failed"]
        })
        
        return consistency_results

    def test_accuracy(self, posts: List[str], true_labels: List[str]) -> Dict:
        """
        Test accuracy on labeled dataset.
        """
        self.logger.log_info("Running accuracy tests...")
        
        correct = 0
        total = len(posts)
        predictions = []
        
        for post, true_label in zip(posts, true_labels):
            result = self.agent.analyze_mood(post)
            predicted = result["predicted_mood"]
            is_correct = predicted == true_label
            
            if is_correct:
                correct += 1
            
            predictions.append({
                "text": post[:50],
                "predicted": predicted,
                "true": true_label,
                "correct": is_correct,
                "confidence": result["confidence"]
            })
        
        accuracy = correct / total if total > 0 else 0.0
        
        self.logger.log_event("ACCURACY_TEST", {
            "accuracy": accuracy,
            "correct": correct,
            "total": total
        })
        
        return {
            "accuracy": accuracy,
            "correct": correct,
            "total": total,
            "predictions": predictions
        }

    def test_confidence_calibration(self, posts: List[str], true_labels: List[str]) -> Dict:
        """
        Test if confidence scores correlate with correctness.
        
        High confidence should mean high accuracy.
        """
        self.logger.log_info("Testing confidence calibration...")
        
        high_confidence_correct = 0
        high_confidence_total = 0
        low_confidence_correct = 0
        low_confidence_total = 0
        
        threshold = 0.75  # Confidence threshold
        
        for post, true_label in zip(posts, true_labels):
            result = self.agent.analyze_mood(post)
            predicted = result["predicted_mood"]
            confidence = result["confidence"]
            is_correct = predicted == true_label
            
            if confidence >= threshold:
                high_confidence_total += 1
                if is_correct:
                    high_confidence_correct += 1
            else:
                low_confidence_total += 1
                if is_correct:
                    low_confidence_correct += 1
        
        high_conf_accuracy = high_confidence_correct / high_confidence_total if high_confidence_total > 0 else 0.0
        low_conf_accuracy = low_confidence_correct / low_confidence_total if low_confidence_total > 0 else 0.0
        
        # Good calibration means: high conf accuracy > low conf accuracy
        is_well_calibrated = high_conf_accuracy > low_conf_accuracy
        
        self.logger.log_event("CALIBRATION_TEST", {
            "high_confidence_accuracy": high_conf_accuracy,
            "low_confidence_accuracy": low_conf_accuracy,
            "is_well_calibrated": is_well_calibrated
        })
        
        return {
            "high_confidence_accuracy": high_conf_accuracy,
            "low_confidence_accuracy": low_conf_accuracy,
            "is_well_calibrated": is_well_calibrated,
            "threshold": threshold
        }

    def test_edge_cases(self) -> Dict:
        """
        Test behavior on edge cases.
        """
        self.logger.log_info("Running edge case tests...")
        
        edge_cases = [
            ("", "empty_string"),
            ("   ", "whitespace_only"),
            ("!@#$%^&*()", "special_chars_only"),
            ("very very very very very long text " * 10, "very_long"),
            ("a", "single_character"),
            ("great great great great great", "repeated_words"),
        ]
        
        results = []
        
        for text, case_type in edge_cases:
            try:
                result = self.agent.analyze_mood(text)
                status = "PASS"
                output = result["predicted_mood"]
            except Exception as e:
                status = "FAIL"
                output = str(e)
            
            results.append({
                "case": case_type,
                "status": status,
                "output": output
            })
        
        self.logger.log_event("EDGE_CASE_TEST", {"results": results})
        
        return {"edge_cases": results}

    def run_full_validation(self) -> Dict:
        """
        Run all validation tests.
        """
        self.logger.log_info("=" * 50)
        self.logger.log_info("Starting full validation suite")
        self.logger.log_info("=" * 50)
        
        results = {
            "consistency": self.test_consistency(SAMPLE_POSTS, iterations=2),
            "accuracy": self.test_accuracy(SAMPLE_POSTS, TRUE_LABELS),
            "calibration": self.test_confidence_calibration(SAMPLE_POSTS, TRUE_LABELS),
            "edge_cases": self.test_edge_cases(),
        }
        
        self.results = results
        
        # Summary
        overall_accuracy = results["accuracy"]["accuracy"]
        is_consistent = results["consistency"]["failed"] == 0
        is_calibrated = results["calibration"]["is_well_calibrated"]
        
        self.logger.log_info("=" * 50)
        self.logger.log_info(f"Overall Accuracy: {overall_accuracy:.2%}")
        self.logger.log_info(f"Consistency: {'PASS' if is_consistent else 'FAIL'}")
        self.logger.log_info(f"Calibration: {'PASS' if is_calibrated else 'FAIL'}")
        self.logger.log_info("=" * 50)
        
        return results

    def print_validation_report(self) -> None:
        """Print a human-readable validation report."""
        print("\n" + "=" * 70)
        print("MOOD MACHINE VALIDATION REPORT")
        print("=" * 70)
        
        # Accuracy
        acc = self.results["accuracy"]["accuracy"]
        print(f"\nAccuracy: {acc:.2%} ({self.results['accuracy']['correct']}/{self.results['accuracy']['total']})")
        
        # Consistency
        cons = self.results["consistency"]
        print(f"Consistency: {cons['passed']}/{cons['passed'] + cons['failed']} tests passed")
        
        # Calibration
        calib = self.results["calibration"]
        print(f"Confidence Calibration: {'Well-calibrated ✓' if calib['is_well_calibrated'] else 'Needs improvement ✗'}")
        print(f"  - High confidence accuracy (>={calib['threshold']:.0%}): {calib['high_confidence_accuracy']:.2%}")
        print(f"  - Low confidence accuracy (<{calib['threshold']:.0%}): {calib['low_confidence_accuracy']:.2%}")
        
        print("\nEdge Case Tests:")
        for case in self.results["edge_cases"]["edge_cases"]:
            status = "✓" if case["status"] == "PASS" else "✗"
            print(f"  {status} {case['case']}")
        
        print("\n" + "=" * 70)
