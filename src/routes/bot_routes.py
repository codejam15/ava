from datetime import date, datetime, timedelta, timezone
import uuid

from fastapi import APIRouter, Depends
from pydantic_ai import AgentRunResult
from sqlmodel.ext.asyncio.session import AsyncSession

from src.agent import FeedbackDependecies, feedback_agent, summary_agent
from src.agent.prompt import TranscriptPrompt, TranscriptPromptModel
from src.agent.tools import buildTeamsFeedbackMessage
from src.db import get_session
from src.db.dao import MeetingTranscriptDAO, PersonalityProfileDAO, UserDao
from src.models.feedback import FeedbackEventModel
from src.models.meeting import MeetingResponseModel
from src.models.team import TeamCreateRequest, UserCreateRequest
from src.models.feedback import PersonalityProfileCreateRequest, PersonalityProfileUpdateRequest
from src.routes.confluence_routes import createPage
from src.routes.test_transcript import transcript
from src.db.dao import TeamDao, UserDao, PersonalityProfileDAO
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.schema import Team, User, PersonalityProfile

router = APIRouter()


@router.get("/teamsummary/{team_name}")
async def team_summary_endpoint(team_name: str, session: AsyncSession = Depends(get_session)):
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
    team_dao: TeamDao = TeamDao(session)
    team: Team | None = await team_dao.get_team_by_name(team_name)
    if team is None:
        raise Exception("team does not exist")
    url = createPage(team, response.output)

    # call my function which will take the url and the summary from the llm response and build the teams message
    teams_message = buildTeamsFeedbackMessage(url, response.output.group_feedback)

    # return this message
    return teams_message


@router.get("/feedbacksummary/{username}")
async def feedback_summary_endpoint(
    username: str, session: AsyncSession = Depends(get_session)
):
    user_dao = UserDao(session)
    personality_profile_dao = PersonalityProfileDAO(session)
    transcript_dao = MeetingTranscriptDAO(session)

    deps = FeedbackDependecies(
        username=username,
        personality_profile_dao=personality_profile_dao,
        user_dao=user_dao,
        transcript_dao=transcript_dao,
    )

    response: AgentRunResult[FeedbackEventModel] = await feedback_agent.run(
        "Based on the transcript of the last meeting, provide constructive personalised 1-on-1 feedback to team member. Your feedback should focus on areas such as communication skills, collaboration, clarity, and overall contribution to the meeting. Adapt your tone to the person personality profile. Keep this feedback concise and actionable.",
        deps=deps,
    )

    return response.output

@router.post("/init")
async def team_init_endpoint(request: TeamCreateRequest,
                            session: AsyncSession = Depends(get_session)) -> Team:
    dao = TeamDao(session)
    created_team = await dao.insert_team(request)
    return created_team


@router.post("/user")
async def add_user_endpoint(user_info: UserCreateRequest,
                             session: AsyncSession = Depends(get_session)) -> User:
    user_dao: UserDao= UserDao(session)
    user: User = await user_dao.insert_user(user_info)
    return user

@router.delete("/user{username}")
async def delete_user_endpoint(username: str,
                               session: AsyncSession = Depends(get_session)) -> None:
    user_dao: UserDao = UserDao(session)
    await user_dao.delete_user(username)


@router.post("/personality")
async def add_personality_endpoint(personality_info: PersonalityProfileCreateRequest,
                                   session: AsyncSession = Depends(get_session)) -> PersonalityProfile:
    personality_dao: PersonalityProfileDAO = PersonalityProfileDAO(session)
    personality: PersonalityProfile = await personality_dao.insert_profile(personality_info)
    return personality


@router.put("/personality/{personality_id}")
async def update_personality_endpoint(personality_id: str, personality_update: PersonalityProfileUpdateRequest,
                                      session: AsyncSession = Depends(get_session))-> PersonalityProfile:
    personality_dao: PersonalityProfileDAO = PersonalityProfileDAO(session)
    personality: PersonalityProfile = await personality_dao.update_profile(personality_id, personality_update)
    return personality
