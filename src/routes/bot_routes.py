from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter
from pydantic_ai import AgentRunResult

from src.agent import summary_agent
from src.agent.prompt import TranscriptPrompt, TranscriptPromptModel
from src.agent.tools import buildTeamsFeedbackMessage
from src.models.meeting import MeetingResponseModel
from src.routes.confluence_routes import createPage
from src.routes.test_transcript import transcript

router = APIRouter()


@router.get("/teamsummary")
async def team_summary_endpoint():
    # async def teamSummary(transcript: str, start_time: datetime) -> str:
    start_time = datetime.now(timezone.utc) - timedelta(hours=1)
    end_time = datetime.now(timezone.utc)

    prompt = TranscriptPrompt.generate_prompt(
        TranscriptPromptModel(
            transcript=transcript,
            meeting_date=date.fromtimestamp(start_time.timestamp()).isoformat(),
            meeting_time=f"{start_time.isoformat()} to {end_time.isoformat()}",
        )
    )

    response: AgentRunResult[MeetingResponseModel] = await summary_agent.run(prompt)

    # call daniel's method which will make the confluence page and it will return the url
    url = createPage(response.output)

    # call my function which will take the url and the summary from the llm response and build the teams message
    teams_message = buildTeamsFeedbackMessage(url, response.output.group_feedback)

    # return this message
    return teams_message
