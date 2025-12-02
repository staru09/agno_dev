# Multi-Agent Research Tool (Agno)

This example mirrors the “web search + ArXiv + writer + supervisor” project layout using Agno primitives and the OpenAI API.

## Project Structure

```
cookbook/examples/multi_agent_research_tool/
├── agents/
│   ├── arxiv_agent.py        # Academic researcher with ArXivTools
│   ├── supervisor_agent.py   # Team leader coordinating everyone
│   ├── web_search_agent.py   # DuckDuckGo-powered web scout
│   └── writer_agent.py       # Final brief generator
├── workflows/
│   └── research_workflow.py  # Chains agents into a deterministic pipeline
├── schemas.py                # Shared Pydantic models for structured outputs
└── app.py                    # AgentOS entrypoint that exposes the system
```

## Prerequisites

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U agno openai duckduckgo-search arxiv
export OPENAI_API_KEY=sk-...
```

## Run the AgentOS

```bash
python -m cookbook.examples.multi_agent_research_tool.app
```

This starts AgentOS (FastAPI) on `http://127.0.0.1:8000`. Open [os.agno.com](https://os.agno.com) and point it at your local URL to drive the supervisor team UI.

## Run From the CLI (No AgentOS)

```bash
python cookbook/examples/multi_agent_research_tool/local_run.py --target workflow "State of RAG safety research" --show-steps
python cookbook/examples/multi_agent_research_tool/local_run.py --target workflow "LLM security best practices" --save-report reports/security.md
python cookbook/examples/multi_agent_research_tool/local_run.py --target team "Summarize scalable oversight techniques"
python cookbook/examples/multi_agent_research_tool/local_run.py --target web "Latest multimodal agent demos"
```

Use `--show-steps` to print each tool’s output, and `--save-report path.md` to capture the final brief in Markdown.

## Run the Workflow Programmatically

```python
from cookbook.examples.multi_agent_research_tool import app

result = app.research_workflow.run(input="Latest alignment techniques for biological LLMs")
print(result.content)
```

## How it Works

- **Specialist agents** live in `agents/` and each exposes a `build_*` helper that returns a configured `Agent`.
- **`schemas.py`** defines the structured responses shared between agents so downstream steps receive typed content (Pydantic models).
- **`supervisor_agent.py`** actually builds a `Team` that orchestrates member agents for ad-hoc conversations (via AgentOS or API).
- **`workflows/research_workflow.py`** wires agents together deterministically: run web search → run ArXiv researcher → pass both outputs to the writer.
- **`app.py`** instantiates everything once, registers them with `AgentOS`, and exposes the FastAPI `app` for serving or tests.

You can customize the system by editing any agent instructions, swapping OpenAI models, or injecting extra tools (e.g., Exa, Tavily, company-specific APIs) without changing the rest of the scaffolding.
