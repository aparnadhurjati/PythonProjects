# CrewAI MCP TriageBridge

A Python-based bug triage and classification system using CrewAI and MCP tools. The MCP server runs in a Docker container, while CrewAI agents run on your local machine and access tools exposed by the MCP server.

## Architecture Overview
- **MCP Server**: Runs inside a Docker container, exposing tool APIs on `http://0.0.0.0:8000/mcp` (binds to all interfaces).
- **CrewAI Agents**: Run locally, connect to the MCP server, and use its tools for bug triage and classification.

```
+-------------------+         HTTP API         +-------------------+
|  Local CrewAI     | <---------------------> |   MCP Server      |
|  Agents           |                         |   (Docker)        |
+-------------------+                         +-------------------+
```

## Prerequisites
- Python 3.12 or higher (for local CrewAI agents)
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- Docker (for running the MCP server)
- An OpenAI API key (for LLM-powered features)

## 1. Clone the Repository

```sh
git clone <your-repo-url>
cd triage_mcp
```

## 2. Add Your OpenAI API Key to a `.env` File

Create a file named `.env` in the project root with the following content:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Replace `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your actual OpenAI API key.

## 3. Build and Run MCP Server in Docker

1. **Build the Docker image:**
   ```sh
   docker build -t mcp-server .
   ```
2. **Run the MCP server container:**
   ```sh
   docker run -d -p 8000:8000 --name mcp-server mcp-server
   ```
   The MCP server should be configured to bind to `0.0.0.0` inside the container (not `127.0.0.1`), so it is accessible from your host machine at `localhost:8000`.

## 4. Set Up and Run CrewAI Agents Locally

1. **Create and activate a virtual environment:**
   ```sh
   python3.12 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```sh
   uv pip install .
   # or, if you use requirements.txt
   pip install -r requirements.txt
   ```
3. **Run the CrewAI agents:**
   ```sh
   python src/triage_mcp/main.py
   ```
   The agents will connect to the MCP server at `http://0.0.0.0:8000/mcp` (or `http://localhost:8000/mcp`) and use its tools for triage tasks.

## Project Structure
```
triage_mcp/
  ├── src/triage_mcp/
  ├── output/
  ├── knowledge/
  ├── tests/
  ├── requirements.txt
  ├── pyproject.toml
  ├── uv.lock
  ├── Dockerfile
  ├── .env
  └── README.md
```

## Notes
- **Only the MCP server runs in Docker.** CrewAI agents and the main application logic run on your local machine.
- Ensure the MCP server container is running and is bound to `0.0.0.0` before starting the CrewAI agents locally.
- The agents communicate with the MCP server via HTTP at `http://0.0.0.0:8000/mcp` (or `http://localhost:8000/mcp`).
- Update dependencies in `pyproject.toml` or `requirements.txt` as needed.
- You must provide your OpenAI API key in a `.env` file for the MCP server container.

## License
MIT
