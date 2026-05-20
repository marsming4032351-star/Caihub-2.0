from fastapi import APIRouter, Depends

from app.agents.vision_qa import VisionQAAgent, get_vision_qa_agent
from app.schemas.vision_qa_agent import (
    VisionQAInspectDemoRequest,
    VisionQAInspectDemoResponse,
)

router = APIRouter()


@router.post(
    "/vision-qa/inspect-demo",
    response_model=VisionQAInspectDemoResponse,
    summary="Vision QA Agent mock inspection demo",
)
def inspect_vision_qa_demo(
    payload: VisionQAInspectDemoRequest,
    agent: VisionQAAgent = Depends(get_vision_qa_agent),
) -> VisionQAInspectDemoResponse:
    return agent.inspect_demo(payload)
