from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar, override
from pydantic import BaseModel

class TranscriptPromptModel(BaseModel):
    transcript: str
    # attendees: str
    # meeting_date: str
    # meeting_time: str

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
        
        This is wrong we're not output html we're gonna output the things individually

        ## 1. Confluence Page (HTML)
        Produce **only valid HTML**, clean and readable.  
        Use <h1>, <h2>, <p>, <ul>, <li>, <strong>, etc.

        The Confluence page MUST contain:

        <h1>Meeting Minutes: <Meeting title here/></h1>

        ### Section Requirements:

        #### **1. General Info**
        - Date
        - Time
        - Attendees  
        (All formatted cleanly)

        #### **2. Agenda**
        Rewrite the agenda into HTML bullet points.

        #### **3. Summary of Discussion**
        Derived entirely from transcript. Summaries must be:
        - concise
        - factual
        - well structured
        - separated by topic

        #### **4. Decisions Made**
        List all decisions reached during the meeting.

        #### **5. Action Items**
        For each action:
        - Owner
        - Description
        - Deadline (only if stated or implied)

        #### **6. Risks or Blockers**
        Extract anything that might impact delivery.

        #### **7. Next Steps**
        Short, actionable list.

        ## 2. Scrum Master Feedback Section
        After the HTML page, output a section titled:

        ### SCRUM MASTER FEEDBACK

        Provide constructive group feedback using Scrum best practices.  
        Feedback should include:
        - Team collaboration quality  
        - Communication clarity  
        - How well agenda was followed  
        - Identification of anti-patterns (if any)  
        - Suggestions to improve future standups/sprint planning/retros  
        - Any Scrum guidelines the team should be reminded of

        Tone must be:
        - supportive  
        - objective  
        - practical  
        - focused on continuous improvement  

        ====================
        ### FINAL OUTPUT FORMAT
        ====================

        First output ONLY the full HTML page.  
        Then add a divider:

        ====================
        SCRUM MASTER FEEDBACK
        ====================

        Then provide the feedback text.

        Do NOT include anything else.
        """




# prompt = TranscriptPrompt.generate_prompt(data)



