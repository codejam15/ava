from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar, override
from pydantic import BaseModel

from src.models.promptmodels import TranscriptPromptModel

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
        You are an expert Scrum Master and Agile facilitator. You will be given:
        1. A raw meeting transcript.
        2. Metadata about the meeting (title, date, time, attendees, agenda).

        Your job is to:
        A. Analyze the transcript deeply to identify discussions, decisions, blockers, action items, risks, and next steps.
        B. Generate a **clean, structured, Confluence-ready HTML page** for meeting minutes.
        C. Generate **Scrum-focused qualitative feedback** for the group based on the meeting's tone, clarity, focus, and collaboration.

        ====================
        ### INPUT DATA
        ====================

        **Transcript:**
        {data.transcript}

        **Meeting Metadata:**
        - Date: {data.meeting_date}
        - Time: {data.meeting_time}
        - Attendees: {data.attendees}

        ====================
        ### OUTPUT REQUIREMENTS
        ====================

        The output must include:
    
        {{
        title: Title for the meeting minutes
        meeting_date: Date of the meeting
        meeting_time: Duration of the meeting (including start/end time)
        attendees: a list of the attendees 

        updates: Any relevant updates that can be derived from the transcript 
        roadblocks: Any important roadblocks that can be derived from the transcript
        nextsteps: Any future plans that cna be derived from the transcript

        notes: Any other relevant notes for the meeting that can be derived from the transcript and that are not part of
        updates, roadblocks or nextsteps


        group_feedback: This should be a short paragraph including some general feedback for the team, and any actionable insights the team should act on.
        }}
        
        Tone must be:
        - supportive  
        - objective  
        - practical  
        - focused on continuous improvement  
        """
