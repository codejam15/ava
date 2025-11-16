from dataclasses import dataclass

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from src.config import settings as s
from src.models.feedback import FeedbackPromptModel, PersonalityProfileModel
from src.models.meeting import MeetingResponseModel


@dataclass
class FeedbackDependecies:
    user_id: str
    personality_profile: PersonalityProfileModel


model = OpenAIChatModel(
    "gpt-5-mini",
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

feeback_agent = Agent(
    model=model,
    deps_type=FeedbackDependecies,
    output_type=FeedbackPromptModel,
    system_prompt=(
        "You are an expert Agile Scrum Master and coach, skilled at providing constructive feedback to team members."
        "You understand the importance of fostering a positive team environment while addressing areas for improvement."
        "You tailor your feedback based on individual personality profiles, ensuring it resonates effectively."
        "You focus on communication skills, collaboration, clarity, and overall contribution to meetings."
    ),
)
