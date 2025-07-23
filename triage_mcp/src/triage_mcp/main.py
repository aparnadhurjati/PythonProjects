from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
import yaml
from mcp import StdioServerParameters
from dotenv import load_dotenv

load_dotenv()

# Create a StdioServerParameters object
# server_params=StdioServerParameters(
#     command="python", 
#     args=["src/triage_mcp/servers/mcp_server.py"],
#     env={"UV_PYTHON": "3.12", **os.environ},
# )
# Streamable HTTP server
server_params = {
    "url": "http://localhost:8000/mcp", 
    "transport": "streamable-http"
}
   
# Use the StdioServerParameters object to create a MCPServerAdapter
with MCPServerAdapter(server_params) as tools:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")
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
    with open("src/triage_mcp/bug_report_2.txt", "r") as f:
        bug = yaml.safe_load(f)

    bug_classifier = Agent(
        role="Bug Classifier",
        goal="Classify bugs into categories like UI, Backend, Database, or Performance",
        backstory=(
            "An experienced QA engineer who specializes in defect categorization. "
            "This agent has seen thousands of bug reports and can quickly determine which component or system area is responsible."
        ),
        llm="gpt-4o",
        temperature=0.0,
        tools=tools,
        max_iterations=1
    )

    severity_assessor = Agent(
        role="Severity Assessor",
        goal="Evaluate bugs and assign severity like Critical, High, Medium, or Low",
        backstory=(
            "A senior support engineer with deep understanding of production impact, SLAs, and business priorities. "
            "This agent determines how urgent or disruptive a defect is based on the bug description."
        ),
        llm="gpt-4o-mini",
        temperature=0.0,
        context=["bug_classifier"]
    )

    owner_router = Agent(
        role="Ownership Router",
        goal="Recommend the best team or engineer to handle the defect based on keywords and components",
        backstory=(
            "An engineering lead familiar with all teams and components in the system. "
            "This agent maps reported defects to the correct owners using technical knowledge and past assignments."
        ),
        llm="gpt-4o-mini",
        temperature=0.0,
        context=["bug_classifier", "severity_assessor"]
    )

    triage_summarizer = Agent(
        role="Triage Summary Writer",
        goal="Summarize triage decisions clearly for PMs and engineering leads",
        backstory=(
            "A technical communicator who writes actionable summaries from multiple reviewers. "
            "This agent compiles the classification, severity, and routing into a single triage statement."
        ),
        llm="gpt-4o-mini",
        temperature=0.0,
        context=["bug_classifier", "severity_assessor", "owner_router"]
    )


    classify_defect = Task(
        description=(
            """Read the full bug report carefully and classify the root cause of the defect into one of the following categories:\n
            UI, Backend, Database, Performance, Logic, or Other.\n
            DO NOT base your decision solely on where the problem appears (e.g., UI unresponsiveness).\n
            Instead, use Title, Description, Steps to Reproduce, Expected, Actual, logs and environment to determine the *source* of the issue.\n
            If the bug is not clear, return \"Other\".\n
            The classification should be based on the root cause of the defect, not just the symptoms.\n
            Examples:\n
            - If the UI freezes due to slow backend processing, classify as Performance or Backend.
            - If data is lost or corrupted, it might be a Database issue.
            - If the logic flow is wrong, choose Logic.
            - Choose UI only if the bug is strictly in layout, rendering, buttons, etc.
            Return the category and a brief explanation for your decision."""
        ),
        expected_output=(
            "A root-cause-based classification along with 1-2 lines justifying the classification."
        ),
        agent=bug_classifier,
        async_execution=True,
        input_variables=["bug_report", "log_data"],
        output_file="output/classify_defect.txt"
    )

    assign_severity = Task(
        description=(
            """Given the bug description, assess the severity level based on its user impact, frequency, data loss risk, and urgency.\n
            Choose one of the following levels: Critical, High, Medium, Low."""
        ),
        expected_output=(
            "A severity level string and a brief rationale for why this level was chosen."
        ),
        agent=severity_assessor,
        output_file="output/assign_severity.txt"
    )

    route_to_owner = Task(
        description=(
            """Based on the keywords, files mentioned, and bug context, identify the responsible team or engineer who should fix the bug.\n
            Use ownership mappings if needed."""
        ),
        expected_output=(
            "The name of the suggested team or engineer with a one-line justification."
        ),
        agent=owner_router,
        output_file="output/route_to_owner.txt"
    )

    summarize_triage = Task(
        description=(
            """Generate a triage summary that consolidates the results from all previous steps.\n
            The summary should be written in clear prose, suitable for sharing with product managers and engineers.\n
            It must include classification, severity, and suggested owner."""
        ),
        expected_output=(
            "A 3-4 sentence triage summary that clearly states the defect category, its severity, and routing recommendation."
        ),
        agent=triage_summarizer,
        output_file="output/triage_summary.txt"
    )
    crew = Crew(
        agents=[bug_classifier, severity_assessor, owner_router, triage_summarizer],
        tasks=[classify_defect, assign_severity, route_to_owner, summarize_triage],
        verbose=True,
        output_log_file=True
    )


    inputs = prepare_inputs_from_bug_report(bug)
    crew.kickoff(inputs=inputs)

    def run():
        print("completed")




