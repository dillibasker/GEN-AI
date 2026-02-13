import os
import sys

# Absolute path of project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add orchestrator folder to Python path
ORCHESTRATOR_PATH = os.path.join(BASE_DIR, "orchestrator")
sys.path.append(ORCHESTRATOR_PATH)

from orchestrator import Orchestrator


def main():
    print("Multi-Agent Code Generator (With Orchestration)")

    requirement = input("\nEnter requirement:\n")
    language = input("\nTarget language (python/javascript): ").strip()

    orchestrator = Orchestrator(language)
    result = orchestrator.run(requirement)

    print("\n--- PLAN ---\n", result["plan"])
    print("\n--- DESIGN ---\n", result["design"])
    print("\n--- GENERATED CODE ---\n", result["code"])
    print("\n--- TEST RESULT ---\n", result["test_result"])


if __name__ == "__main__":
    main()
