# Code Review AI

An intelligent Java code review system powered by CrewAI that automatically analyzes code for syntax issues, design patterns, and provides actionable feedback.

## 🚀 Features

- **Syntax Analysis**: Detects syntax errors, formatting issues, and code style violations
- **Design Review**: Evaluates code structure, OOP principles, and SOLID design patterns
- **Automated Feedback**: Generates comprehensive, actionable reports
- **Multi-Agent Architecture**: Uses specialized AI agents for different review aspects
- **Structured Output**: Produces organized feedback in markdown format

## 📋 Prerequisites

- Python 3.10 or higher (but less than 3.14)
- Java development environment (for the code being reviewed)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd codereview
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

   Or if you're using `uv`:
   ```bash
   uv sync
   ```

## 🎯 Usage

### Basic Code Review

Run a code review on the default Java file:

```bash
python -m codereview.main
```

Or use the installed script:

```bash
codereview
```

### Training the Crew

Train the crew for a specified number of iterations:

```bash
python -m codereview.main train <iterations> <filename>
```

### Replaying Execution

Replay crew execution from a specific task:

```bash
python -m codereview.main replay <task_id>
```

### Testing

Test the crew execution:

```bash
python -m codereview.main test <iterations> <eval_llm>
```

## 🏗️ Architecture

### Agents

The system uses three specialized AI agents:

1. **Syntax Checker**: Analyzes Java code for syntax issues, formatting inconsistencies, and style violations
2. **Design Reviewer**: Evaluates design patterns, modularity, OOP principles, and SOLID design principles
3. **Summary Generator**: Consolidates feedback into actionable summaries

### Tasks

The review process consists of three sequential tasks:

1. **Syntax Check Task**: Identifies syntax and style problems
2. **Design Review Task**: Assesses code design and architecture
3. **Summary Task**: Creates a comprehensive feedback report

### Output Files

Reviews are saved to the `output/` directory:
- `syntax_check.md`: Detailed syntax and style analysis
- `design_review.md`: Design and architectural evaluation
- `feedback.md`: Consolidated summary report

## 📁 Project Structure

```
codereview/
├── src/codereview/
│   ├── __init__.py
│   ├── main.py              # Main execution script
│   ├── crew.py              # CrewAI crew definition
│   ├── App.java             # Sample Java code for review
│   ├── config/
│   │   ├── agents.yaml      # Agent configurations
│   │   └── tasks.yaml       # Task definitions
│   └── tools/
│       └── __init__.py
├── output/                  # Generated review reports
├── knowledge/               # Knowledge base files
├── tests/                   # Test files
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## ⚙️ Configuration

### Agents Configuration (`config/agents.yaml`)

Each agent is configured with:
- **Role**: The agent's specific function
- **Goal**: What the agent aims to achieve
- **Backstory**: Context about the agent's expertise
- **LLM**: The language model to use (default: gpt-4o-mini)

### Tasks Configuration (`config/tasks.yaml`)

Tasks define:
- **Description**: What the task does
- **Expected Output**: Format of the results
- **Agent Assignment**: Which agent performs the task
- **Output File**: Where results are saved
- **Dependencies**: Task execution order

## 🔧 Customization

### Adding New Agents

1. Define the agent in `config/agents.yaml`
2. Add the agent method in `crew.py`
3. Create corresponding tasks in `config/tasks.yaml`

### Modifying Review Criteria

Edit the agent goals and task descriptions in the YAML configuration files to adjust what aspects of the code are reviewed.

### Changing Output Format

Modify the `expected_output` fields in `config/tasks.yaml` to change the format of review reports.

## 📝 Example Output

The system generates three types of reports:

1. **Syntax Check Report**: Lists specific syntax errors, style violations, and formatting issues
2. **Design Review Report**: Evaluates code structure, design patterns, and architectural decisions
3. **Feedback Summary**: Provides a consolidated view with prioritized recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing issues in the repository
2. Create a new issue with detailed information about your problem
3. Include relevant error messages and system information

## 🔮 Future Enhancements

- Support for additional programming languages
- Integration with CI/CD pipelines
- Custom review rule sets
- Performance metrics and benchmarking
- Real-time code review feedback
