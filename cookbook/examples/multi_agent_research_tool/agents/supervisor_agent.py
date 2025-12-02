from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team


def build_supervisor_team(
    members: List[Agent],
    model_id: str = "gpt-4o-mini",
) -> Team:
    """Wrap all specialists in a coordinating Team leader."""

    return Team(
        name="Research Supervisor",
        model=OpenAIChat(id=model_id),
        members=members,
        instructions=[
            "You orchestrate research tasks across your specialists.",
            "Decide when each member should contribute and ensure sources are cited.",
            "Ask clarifying questions before delegating if the request is vague.",
            "Summaries should highlight consensus and surface disagreements.",
            "Stop once a useful brief with references is ready.",
        ],
        markdown=True,
        show_members_responses=True,
    )
