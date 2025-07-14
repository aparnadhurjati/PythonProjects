# tools/log_parser.py
from crewai.tools import tool

@tool
def extract_errors(log_data: str) -> str:
    """Extracts error lines and exceptions from logs."""
    return "\n".join([
        line for line in log_data.splitlines()
        if any(keyword in line for keyword in ['Exception', 'ERROR', 'Traceback'])
    ])
