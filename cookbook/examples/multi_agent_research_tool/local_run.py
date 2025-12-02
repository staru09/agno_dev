import argparse
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cookbook.examples.multi_agent_research_tool import app as research_app

COMPONENTS: Dict[str, Any] = {
    "workflow": research_app.research_workflow,
    "team": research_app.supervisor_team,
    "web": research_app.web_search_agent,
    "arxiv": research_app.arxiv_agent,
    "writer": research_app.writer_agent,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the multi-agent research pipeline or any individual agent directly "
            "from the CLI. Requires OPENAI_API_KEY in your environment."
        )
    )
    parser.add_argument(
        "--target",
        choices=COMPONENTS.keys(),
        default="workflow",
        help="Which component to run (default: workflow).",
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Topic or instruction to hand to the agent(s).",
    )
    parser.add_argument(
        "--session-id",
        type=str,
        default=None,
        help="Optional session identifier for stateful runs.",
    )
    parser.add_argument(
        "--user-id",
        type=str,
        default=None,
        help="Optional user identifier passed to the runtime.",
    )
    return parser.parse_args()


def print_response(output):
    if hasattr(output, "content"):
        print(output.content)
        return
    print(output)


def main() -> None:
    args = parse_args()
    component = COMPONENTS[args.target]

    if hasattr(component, "run"):
        response = component.run(
            input=args.prompt,
            session_id=args.session_id,
            user_id=args.user_id,
        )
        print_response(response)
    else:  # pragma: no cover - defensive guard for unexpected component types
        print(f"Unsupported component type for target '{args.target}'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
