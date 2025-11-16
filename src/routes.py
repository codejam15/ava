import uuid
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends
from pydantic_ai import AgentRunResult
from sqlmodel.ext.asyncio.session import AsyncSession

from src.agent import FeedbackDependecies, feedback_agent, summary_agent
from src.agent.prompt import TranscriptPrompt, TranscriptPromptModel
from src.agent.tools import build_team_feedback_message, post_confluence_page
from src.db import get_session
from src.db.dao import MeetingTranscriptDAO, PersonalityProfileDAO, TeamDao, UserDao
from src.db.schema import PersonalityProfile, Team, User
from src.discord_bot import post_meeting_minutes
from src.models.feedback import FeedbackEventModel, PersonalityProfileModel
from src.models.meeting import MeetingResponseModel
from src.models.team import TeamCreateRequest, UserCreateRequest

router = APIRouter()


@router.post("/generate/{team_name}")
async def generate_meeting_minutes(
    transcript: str,
    start_time,
    attendees: dict[str, str],
    team_name: str,
    session: AsyncSession = Depends(get_session),
):
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
    url = post_confluence_page(team, response.output)

    # call my function which will take the url and the summary from the llm response and build the teams message
    teams_message = build_team_feedback_message(url, response.output.group_feedback)

    # post the messages to teams with the bot
    await post_meeting_minutes(teams_message)


@router.post("/init")
async def team_init_endpoint(
    request: TeamCreateRequest, session: AsyncSession = Depends(get_session)
) -> Team:
    dao = TeamDao(session)
    created_team = await dao.insert_team(request)
    return created_team


@router.post("/user")
async def add_user_endpoint(
    user_info: UserCreateRequest, session: AsyncSession = Depends(get_session)
) -> User:
    user_dao: UserDao = UserDao(session)
    user: User = await user_dao.insert_user(user_info)
    return user


@router.delete("/user{username}")
async def delete_user_endpoint(
    username: str, session: AsyncSession = Depends(get_session)
) -> None:
    user_dao: UserDao = UserDao(session)
    await user_dao.delete_user(username)


@router.post("/personality")
async def add_personality_endpoint(
    personality_info: PersonalityProfileModel,
    session: AsyncSession = Depends(get_session),
) -> PersonalityProfile:
    personality_dao: PersonalityProfileDAO = PersonalityProfileDAO(session)
    personality: PersonalityProfile = await personality_dao.insert_profile(
        personality_info
    )
    return personality


@router.put("/personality/{personality_id}")
async def update_personality_endpoint(
    personality_id: uuid.UUID,
    personality_update: PersonalityProfileModel,
    session: AsyncSession = Depends(get_session),
) -> PersonalityProfile:
    personality_dao: PersonalityProfileDAO = PersonalityProfileDAO(session)
    personality: PersonalityProfile = await personality_dao.update_profile(
        personality_id, personality_update
    )
    return personality


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
