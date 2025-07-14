# tools/exception_tools.py
from crewai.tools import tool

@tool
def summarize_stack_trace(log_data: str) -> str:
    """Summarizes stack trace details from a log."""
    lines = log_data.splitlines()
    summary = []
    for line in lines:
        if 'Exception' in line or 'Caused by' in line:
            summary.append(line)
    return "\n".join(summary[:5])  # Limit output for brevity
