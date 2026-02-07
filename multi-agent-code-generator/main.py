from orchestrator.orchestrator import Orchestrator

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
