from __future__ import annotations

from typing import Dict, Optional

from agno.agent import Agent
from agno.workflow import Step, Workflow
from agno.workflow.types import StepInput, StepOutput
from pydantic import BaseModel


def _serialize_content(content) -> str:
    if content is None:
        return "No data was returned."
    if isinstance(content, BaseModel):
        return content.model_dump_json(indent=2, exclude_none=True)
    if isinstance(content, (dict, list)):
        import json

        return json.dumps(content, indent=2, default=str)
    return str(content)


def build_research_workflow(
    web_search_agent: Agent,
    arxiv_agent: Agent,
    writer_agent: Agent,
) -> Workflow:
    """Return a workflow that chains the specialists with lightweight logic."""

    def research_pipeline(step_input: StepInput, session_state: Optional[Dict] = None) -> StepOutput:
        topic = step_input.get_input_as_string()
        if not topic:
            return StepOutput(content="Please provide a research topic to begin.", success=False)

        # Track recently researched topics for Operator context.
        session_state = session_state or {}
        history = session_state.setdefault("topics", [])
        history.append(topic)

        try:
            web_response = web_search_agent.run(topic)
            if not web_response.content:
                return StepOutput(
                    content=f"Web research agent did not return content for '{topic}'.",
                    success=False,
                )

            arxiv_response = arxiv_agent.run(topic)
            if not arxiv_response.content:
                return StepOutput(
                    content=f"ArXiv research agent did not return content for '{topic}'.",
                    success=False,
                )

            research_context = "\n\n".join(
                [
                    f"# Topic\n{topic}",
                    "## Web Intelligence\n" + _serialize_content(web_response.content),
                    "## Academic Sources\n" + _serialize_content(arxiv_response.content),
                    "## Instructions\nSynthesize the material into an executive brief with citations.",
                ]
            )

            writer_response = writer_agent.run(research_context)
            if not writer_response.content:
                return StepOutput(
                    content="Writer agent failed to return a brief.",
                    success=False,
                )

            return StepOutput(content=writer_response.content)
        except Exception as exc:  # pragma: no cover - defensive guard
            return StepOutput(content=f"Research workflow failed: {exc}", success=False, error=str(exc))

    return Workflow(
        name="Multi-Agent Research Workflow",
        description="Runs web + academic research before producing a final brief.",
        steps=[Step(name="research_pipeline", executor=research_pipeline)],
        session_state={"topics": []},
    )
