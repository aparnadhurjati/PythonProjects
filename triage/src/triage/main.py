#!/usr/bin/env python
from pathlib import Path
import sys
import warnings
import yaml
from datetime import datetime

from triage.crew import Triage

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# bug_report = Path('src/triage/bug_report.txt').read_text()
# # raw_logs = Path('src/triage/log_data.txt').read_text()
# raw_logs = """
# 2024-06-21 10:14:32 ERROR com.example.OrderService - Failed to process order
# java.lang.NullPointerException: Cannot invoke "String.trim()" because "order.customerId" is null
#     at com.example.OrderService.processOrder(OrderService.java:58)
#     at com.example.OrderController.submitOrder(OrderController.java:22)
#     ...
# 2024-06-21 10:14:33 INFO com.example.OrderService - Retrying request
# """
def prepare_inputs_from_bug_report(bug):
    steps = bug['steps_to_reproduce']
    if isinstance(steps, str):
        # If steps come in as a single multiline string, split properly
        step_lines = steps.strip().splitlines()
    else:
        step_lines = steps

    formatted_steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(step_lines)])

    
    bug_report = f"""Title: {bug['title']}
Description: {bug['description']}
Steps to Reproduce:
{formatted_steps}
Expected: {bug['expected']}
Actual: {bug['actual']}"""


    return {
        "bug_report": bug_report,
        "log_data": bug.get("logs", "No relevant logs found.")
    }
with open("src/triage/bug_report_2.txt", "r") as f:
    bug = yaml.safe_load(f)



def run():
    """
    Run the crew.
    """
    # inputs = {
    #     'bug_report': bug_report

    # }
#     inputs = {
#     "title": "Form not submitting on Chrome",
#     "description": "When clicking submit, nothing happens in the Chrome browser.",
#     "steps_to_reproduce": "1. Open form on Chrome browser\n2. Click Submit button",
#     "logs": "No network request fired, JS error on click handler.",
#     "expected_output": "Form should submit and redirect to confirmation page.",
#     "actual_output": "User stays on same page and error is shown in console.",
#     "log_data": raw_logs
# }"bug_report": 
    inputs = prepare_inputs_from_bug_report(bug)
    
    try:
        Triage().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    # inputs = {
    #     'bug_report': bug_report
    # }
    inputs=prepare_inputs_from_bug_report(bug)
    try:
        Triage().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    inputs=prepare_inputs_from_bug_report(bug)
    try:
        Triage().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    # inputs = {
    #     'bug_report': bug_report
    # }
    inputs=prepare_inputs_from_bug_report(bug)
    try:
        Triage().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
