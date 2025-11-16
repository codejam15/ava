from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from pydantic import BaseModel

from src.models.meeting import TranscriptPromptModel

T = TypeVar("T", bound=BaseModel)


class BasePrompt(ABC, Generic[T]):
    @abstractmethod
    def _prompt(self, data: T) -> str: ...

    @classmethod
    def generate_prompt(cls, data: T):
        instance = cls()
        return instance._prompt(data)


class TranscriptPrompt(BasePrompt[TranscriptPromptModel]):
    @override
    def _prompt(self, data: TranscriptPromptModel) -> str:
        return f"""
        From the raw transcript of this last meeting (including Metadata about the meeting (title, date, time, attendees, agenda))

        Your job is to:
        A. Analyze the transcript deeply to identify discussions, decisions, blockers, action items, risks, and next steps.
        B. Generate a **clean, structured, Confluence-ready HTML page** for meeting minutes.
        C. Generate **Scrum-focused qualitative feedback** for the group based on the meeting's tone, clarity, focus, and collaboration.

        ### Transcript:
        {data.transcript}

        #### Meeting Metadata:
        - Date: {data.meeting_date}
        - Time: {data.meeting_time}

        Output must your answer using the to the following schema:
    
        {{
        "title:": Title for the meeting minutes,
        "meeting_date": Date of the meeting,
        "meeting_time": Duration of the meeting (including start/end time),
        "attendees": Parse the transcript to extract the list of attendees,
        "updates": Any relevant updates that can be derived from the transcript, if making a list use HTML unordered list format,
        "roadblocks": Any important roadblocks that can be derived from the transcript, if making a list use HTML unordered list format,
        "nextsteps": Any future plans that can be derived from the transcript, if making a list use HTML unordered list format,
        "notes": Any other relevant notes for the meeting that can be derived from the transcript and that are not part of updates, roadblocks or nextsteps, if making a list use HTML unordered list format,
        "group_feedback": This should be a short paragraph including some general feedback for the team, and any actionable insights the team should act on.
        }}
        
        """
