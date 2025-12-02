"""
Web search specialist agent used in the research workflow.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from cookbook.examples.multi_agent_research_tool.schemas import WebSearchResults


def build_web_search_agent(model_id: str = "gpt-4o-mini") -> Agent:
    """Create an agent that performs focused web research."""

    return Agent(
        name="Web Search Agent",
        model=OpenAIChat(id=model_id),
        tools=[DuckDuckGoTools()],
        output_schema=WebSearchResults,
        instructions=[
            "Search trusted web sources (news sites, blogs, docs) relevant to the query.",
            "Return 3-5 diverse sources with a concise summary and canonical URL.",
            "Prioritize recency and credibility. Never fabricate URLs.",
            "Highlight complementary perspectives or disagreements when possible.",
        ],
        add_name_to_context=True,
        markdown=True,
    )
