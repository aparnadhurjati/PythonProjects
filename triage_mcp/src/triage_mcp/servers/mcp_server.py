from mcp.server.fastmcp  import FastMCP # For Streamable HTTP Server

mcp = FastMCP("LogTools", stateless_http=True, host="0.0.0.0", port=8000) # comment this line and uncomment below line for stdio
# mcp = FastMCP("LogTools") # comment the above line and uncomment this for stdio transport

@mcp.tool()
def extract_errors(log_data: str) -> str:
    """Extracts error lines and exceptions from logs.
    Args:
        log_data: The log data to extract errors from.
    Returns:
        A string containing the extracted errors.
    """
    return "\n".join([
        line for line in log_data.splitlines()
        if any(keyword in line for keyword in ['Exception', 'ERROR', 'Traceback'])
    ])

@mcp.tool()
def summarize_stack_trace(log_data: str) -> str:
    """Summarizes stack trace details from a log.
    Args:
        log_data: The log data to summarize.
    Returns:
        A string containing the summarized stack trace.
    """
    lines = log_data.splitlines()
    summary = []
    print("summarize_stack_trace" + log_data)
    for line in lines:
        if 'Exception' in line or 'Caused by' in line:
            summary.append(line)
    return "\n".join(summary[:5])  # Limit output for brevity

if __name__ == "__main__":
    # Initialize and run the server
    # mcp.run(transport="stdio")
    mcp.run(transport="streamable-http")
    # )