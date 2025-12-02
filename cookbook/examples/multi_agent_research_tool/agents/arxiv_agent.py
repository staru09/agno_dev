from pathlib import Path
from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.arxiv import ArxivTools

from cookbook.examples.multi_agent_research_tool.schemas import ArxivPapers


def build_arxiv_agent(model_id: str = "gpt-4o-mini", download_dir: Optional[Path] = None) -> Agent:
    """Create an agent that pulls structured insights from ArXiv."""

    if download_dir is None:
        download_dir = Path(__file__).resolve().parent.parent / "tmp" / "arxiv_pdfs"
    download_dir.mkdir(parents=True, exist_ok=True)

    arxiv_tools = ArxivTools(download_dir=download_dir)

    return Agent(
        name="ArXiv Research Agent",
        model=OpenAIChat(id=model_id),
        tools=[arxiv_tools],
        output_schema=ArxivPapers,
        instructions=[
            "Query ArXiv for the topic and identify 3-4 papers that best answer the question.",
            "Summaries must be approachable and include why each paper matters.",
            "Surface publication date, core method, and any notable limitations.",
            "Add the canonical PDF link and ArXiv ID for every paper.",
        ],
        add_name_to_context=True,
        markdown=True,
    )
