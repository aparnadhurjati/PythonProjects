# Triage - AI-Powered Bug Triage System

An intelligent bug triage system built with CrewAI that automatically classifies, assesses severity, routes ownership, and summarizes bug reports using multiple specialized AI agents.

## 🎯 Overview

Triage is an automated system that processes bug reports through a pipeline of AI agents, each specializing in different aspects of bug analysis:

- **Bug Classifier**: Categorizes bugs into UI, Backend, Database, Performance, Logic, or Other
- **Severity Assessor**: Assigns severity levels (Critical, High, Medium, Low) based on impact
- **Owner Router**: Recommends the appropriate team or engineer to handle the bug
- **Triage Summarizer**: Creates clear, actionable summaries for stakeholders

## 🏗️ Architecture

The system uses CrewAI's multi-agent framework with a sequential process flow:

```
Bug Report → Classification → Severity Assessment → Owner Routing → Summary
```

### Agents

- **Bug Classifier**: Experienced QA engineer specializing in defect categorization
- **Severity Assessor**: Senior support engineer with deep understanding of production impact
- **Owner Router**: Engineering lead familiar with all teams and components
- **Triage Summarizer**: Technical communicator who writes actionable summaries

### Tools

- **Log Parser**: Extracts important error messages and stack traces from raw logs
- **Exception Summarizer**: Summarizes exceptions and stack traces for concise error context

## 🚀 Quick Start

### Prerequisites

- Python 3.10-3.13
- OpenAI API key (for GPT-4 models)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd triage
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Usage

#### Basic Execution

Run the triage system with the default bug report:

```bash
python -m triage.main
```

#### Training

Train the crew for a specified number of iterations:

```bash
python -m triage.main train <iterations> <filename>
```

#### Testing

Test the crew execution:

```bash
python -m triage.main test <iterations> <eval_llm>
```

#### Replay

Replay execution from a specific task:

```bash
python -m triage.main replay <task_id>
```

## 📁 Project Structure

```
triage/
├── src/triage/
│   ├── main.py              # Main execution script
│   ├── crew.py              # CrewAI crew definition
│   ├── config/
│   │   ├── agents.yaml      # Agent configurations
│   │   ├── tasks.yaml       # Task definitions
│   │   └── tools.yaml       # Tool specifications
│   ├── tools/
│   │   ├── log_parser.py    # Log parsing utilities
│   │   ├── exception_tools.py # Exception handling tools
│   │   └── custom_tool.py   # Custom tool implementations
│   └── bug_report_2.txt     # Sample bug report
├── output/                  # Generated triage outputs
├── knowledge/               # Knowledge base files
├── tests/                   # Test files
└── pyproject.toml          # Project configuration
```

## 📊 Output

The system generates four output files in the `output/` directory:

- `classify_defect.txt`: Bug classification with rationale
- `assign_severity.txt`: Severity assessment with justification
- `route_to_owner.txt`: Ownership recommendation
- `triage_summary.txt`: Consolidated triage summary

## 🔧 Configuration

### Agents Configuration (`config/agents.yaml`)

Each agent is configured with:
- Role and goal
- Backstory for context
- LLM model (GPT-4o, GPT-4o-mini)
- Temperature settings
- Context dependencies

### Tasks Configuration (`config/tasks.yaml`)

Tasks define:
- Detailed descriptions
- Expected outputs
- Agent assignments
- Input/output variables
- Output file paths

### Tools Configuration (`config/tools.yaml`)

Tools specify:
- Function mappings
- Input/output parameters
- Descriptions

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📝 Example

Given this bug report:

```yaml
title: Order submission fails on null customer
description: Submitting an order intermittently fails when no customer is selected.
steps_to_reproduce: |
  1. Go to Orders screen
  2. Click "Submit" without selecting a customer
expected: Should prompt to select a customer
actual: Application crashes with server error
logs: |
  2024-06-21 10:14:32 ERROR com.example.OrderService - Failed to process order 
  java.lang.NullPointerException: Cannot invoke "String.trim()" because "order.customerId" is null 
    at com.example.OrderService.processOrder(OrderService.java:58) 
    at com.example.OrderController.submitOrder(OrderController.java:22)
```

The system will:
1. **Classify**: Backend (null pointer exception in order processing)
2. **Assess Severity**: High (causes application crashes)
3. **Route Owner**: Backend team (OrderService component)
4. **Summarize**: "Backend defect causing application crashes due to null customer ID validation"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the [CrewAI documentation](https://docs.crewai.com/)
- Review the configuration files for customization options
- Open an issue in the repository
