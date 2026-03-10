from app.agents.registry import list_agents
from app.schemas.agent_runtime import AgentRuntimeOverview, AgentRuntimeStatus


RUNTIME_READY_AGENT_IDS = {"ceo-agent"}


class AgentRuntimeService:
    def get_overview(self) -> AgentRuntimeOverview:
        agents = []
        for agent in list_agents():
            has_runtime = agent.agent_id in RUNTIME_READY_AGENT_IDS
            agents.append(
                AgentRuntimeStatus(
                    agent_id=agent.agent_id,
                    enabled=True,
                    mode="orchestrating" if has_runtime else "registered",
                    has_runtime=has_runtime,
                    summary=(
                        "Agent runtime skeleton is wired for orchestration."
                        if has_runtime
                        else "Agent is currently registered in governance metadata only."
                    ),
                )
            )

        return AgentRuntimeOverview(
            total_agents=len(agents),
            runtime_ready_agents=sum(1 for agent in agents if agent.has_runtime),
            orchestration_status="skeleton-ready",
            agents=agents,
        )
