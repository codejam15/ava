from fastapi import APIRouter

from src.models.transcript import MeetingTranscript
from src.prompts.prompt import TranscriptPrompt, TranscriptPromptModel

bot_router = APIRouter();


@bot_router.post("/teamsummary")
async def teamSummary(transcript: str):
    # Build/get the prompt to send to the llm, we have transcript already
    data = {
        "transcript": transcript
    }

    prompt = TranscriptPrompt.generate_prompt(TranscriptPromptModel(**data))  





