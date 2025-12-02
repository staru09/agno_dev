from agno.agent import Agent
from agno.models.openai import OpenAIChat

from cookbook.examples.multi_agent_research_tool.schemas import ResearchBrief


def build_writer_agent(model_id: str = "gpt-4o-mini") -> Agent:
    """Create the final writer that produces a structured brief."""

    return Agent(
        name="Research Writer",
        model=OpenAIChat(id=model_id),
        output_schema=ResearchBrief,
        instructions=[
            "You receive compiled insights (web + academic).",
            "Write a concise executive overview followed by bullet findings that cite sources inline.",
            "Close with recommended next steps or open questions.",
            "Return markdown that strictly follows the ResearchBrief schema.",
            "Never introduce information that was not present in the provided research context.",
            "Write the final report as an Abstract for a professional audience.",
        ],
        markdown=True,
    )
