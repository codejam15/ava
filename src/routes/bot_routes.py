from fastapi import APIRouter
from pydantic_ai import AgentRunResult

from src.agent.tools import buildTeamsSummaryMessage
from src.models.responsemodel import MeetingResponseModel
from src.models.transcript import MeetingTranscript
from src.agent.prompt import TranscriptPrompt, TranscriptPromptModel
from src.agent.agent import llm

bot_router = APIRouter();


@bot_router.post("/teamsummary")
async def teamSummary(transcript: str):
    # Build/get the prompt to send to the llm, we have transcript already
    data = {
        "transcript": transcript
    }

    prompt = TranscriptPrompt.generate_prompt(TranscriptPromptModel(**data))  

    response: AgentRunResult[MeetingResponseModel] = llm.run_sync(prompt)

    # call daniel's method which will make the confluence page and it will return the url


    # call my function which will take the url and the summary from the llm response and build the teams message
    teams_message = buildTeamsSummaryMessage(response.output.group_feedback)


    # return this message
    return teams_message







