from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from src.config import settings as s
from src.db.dao import MeetingTranscriptDAO, PersonalityProfileDAO, UserDao
from src.db.schema import MeetingTranscript, PersonalityProfile, User
from src.models.feedback import FeedbackEventModel
from src.models.meeting import MeetingResponseModel

model = OpenAIChatModel(
    "gpt-4o",
    provider=OpenAIProvider(api_key=s.OPENAI_API_KEY),
)

summary_agent = Agent(
    model=model,
    output_type=MeetingResponseModel,
    system_prompt=(
        "You embody the personality of a seasoned Agile Scrum Master and coach."
        "You have a strong affinity for collaboration, continuous improvement, psychological safety, and servant leadership."
        "You naturally think in terms of Agile values, empiricism, transparency, and incremental progress."
        "You excel at identifying patterns in communication, understanding team morale, and recognizing strengths and impediments."
    ),
)


@dataclass
class FeedbackDependecies:
    username: str
    personality_profile_dao: PersonalityProfileDAO
    user_dao: UserDao
    transcript_dao: MeetingTranscriptDAO


feedback_agent = Agent(
    model=model,
    deps_type=FeedbackDependecies,
    output_type=FeedbackEventModel,
    system_prompt=(
        "You are an expert Agile Scrum Master and coach, skilled at providing constructive feedback to team members."
        "You understand the importance of fostering a positive team environment while addressing areas for improvement."
        "You tailor your feedback based on individual personality profiles, ensuring it resonates effectively."
        "You focus on communication skills, collaboration, clarity, and overall contribution to meetings."
        "You engage in discussion with the user after providing feedback to ensure understanding and encourage growth."
    ),
)


@feedback_agent.tool
async def get_personality_profile(
    ctx: RunContext[FeedbackDependecies],
) -> str:
    try:
        user: User = await ctx.deps.user_dao.get_user_by_username(ctx.deps.username)

        profile: PersonalityProfile = (
            await ctx.deps.personality_profile_dao.get_profile_by_id(user.id)
        )

        return profile.summary

    except Exception:
        return "No personality profile found."


@feedback_agent.tool
async def get_last_meeting_transcript(
    ctx: RunContext[FeedbackDependecies],
) -> MeetingTranscript:
    try:
        transcript = await ctx.deps.transcript_dao.get_latest_transcript()
        return transcript
    except Exception as e:
        raise e
