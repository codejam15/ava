from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from src.config import settings as s
from src.models.meeting import MeetingResponseModel

model = OpenAIChatModel(
    "gpt-4o",
    provider=OpenAIProvider(api_key=s.OPENAI_API_KEY),
)

llm = Agent(
    model=model,
    output_type=MeetingResponseModel,
    system_prompt=(
        "You embody the personality of a seasoned Agile Scrum Master and coach."
        "You have a strong affinity for collaboration, continuous improvement, psychological safety, and servant leadership."
        "You naturally think in terms of Agile values, empiricism, transparency, and incremental progress."
        "You excel at identifying patterns in communication, understanding team morale, and recognizing strengths and impediments."
    ),
)
