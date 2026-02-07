from agents.planner import planning_agent
from agents.designer import designing_agent
from agents.creator import creating_agent
from agents.tester import testing_agent
from utils.normalize import normalize_output


class Orchestrator:
    def __init__(self, language="python"):
        self.language = language

    def run(self, requirement):
        # Step 1: Planning
        plan_raw = planning_agent(requirement)
        plan = normalize_output(plan_raw)

        # Step 2: Designing
        design_raw = designing_agent(plan)
        design = normalize_output(design_raw)

        # Step 3: Code Generation
        code_raw = creating_agent(design, self.language)
        code = normalize_output(code_raw)

        # Step 4: Testing
        test_raw = testing_agent(code, requirement)
        test_result = normalize_output(test_raw)

        return {
            "plan": plan,
            "design": design,
            "code": code,
            "test_result": test_result
        }
