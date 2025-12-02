from agno.os import AgentOS

from cookbook.examples.multi_agent_research_tool.agents.arxiv_agent import build_arxiv_agent
from cookbook.examples.multi_agent_research_tool.agents.supervisor_agent import build_supervisor_team
from cookbook.examples.multi_agent_research_tool.agents.web_search_agent import build_web_search_agent
from cookbook.examples.multi_agent_research_tool.agents.writer_agent import build_writer_agent
from cookbook.examples.multi_agent_research_tool.workflows.research_workflow import build_research_workflow

# Instantiate core agents once so both the workflow and AgentOS share state.
web_search_agent = build_web_search_agent()
arxiv_agent = build_arxiv_agent()
writer_agent = build_writer_agent()

supervisor_team = build_supervisor_team(
    members=[web_search_agent, arxiv_agent, writer_agent],
)

research_workflow = build_research_workflow(
    web_search_agent=web_search_agent,
    arxiv_agent=arxiv_agent,
    writer_agent=writer_agent,
)

agent_os = AgentOS(
    agents=[web_search_agent, arxiv_agent, writer_agent],
    teams=[supervisor_team],
    workflows=[research_workflow],
)

app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app="cookbook.examples.multi_agent_research_tool.app:app", reload=True)
