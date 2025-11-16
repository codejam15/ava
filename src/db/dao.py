from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .schema import (
    FeedbackEvent,
    FeedbackResponse,
    Meeting,
    MeetingSummary,
    MeetingTranscript,
    PersonalityProfile,
    Team,
    User,
)
from ..models.feedback import (
    FeedbackEventCreateRequest,
    FeedbackResponseCreateRequest,
    PersonalityProfileCreateRequest,
    PersonalityProfileUpdateRequest,
)
from ..models.meeting import (
    MeetingCreateRequest,
    MeetingSummaryCreateRequest,
    MeetingTranscriptCreateRequest,
)
from ..models.team import TeamCreateRequest, UserCreateRequest


class UserDao:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def insert_user(self, user_data: UserCreateRequest) -> User:
        # Exclude id from model_dump to let SQLModel use default_factory=cuid
        user_dict = user_data.model_dump(exclude={"id"})
        user = User(**user_dict)
        self._session.add(user)
        await self._session.commit()
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self._session.exec(select(User).where(User.username == username))
        user = result.first()
        return user

    async def delete_user(self, username: str) -> None:
        user = await self.get_user_by_username(username)

        if not user:
            raise Exception("User not found")

        await self._session.delete(user)
        await self._session.commit()


class TeamDao:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def insert_team(self, team_data: TeamCreateRequest) -> Team:
        # Exclude id from model_dump to let SQLModel use default_factory=cuid
        team_dict = team_data.model_dump(exclude={"id"})
        team = Team(**team_dict)
        self._session.add(team)
        await self._session.commit()
        return team

    async def get_team_by_id(self, team_id: str) -> Team | None:
        result = await self._session.exec(select(Team).where(Team.id == team_id))
        team = result.first()
        return team

    async def delete_team(self, team_id: str) -> None:
        team = await self.get_team_by_id(team_id)

        if not team:
            raise Exception("Team does not exist")

        await self._session.delete(team)
        await self._session.commit()


class MeetingDAO:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def insert_meeting(self, meeting_data: MeetingCreateRequest) -> Meeting:
        meeting_dict = meeting_data.model_dump(exclude={"id"})
        meeting = Meeting(**meeting_dict)
        self._session.add(meeting)
        await self._session.commit()
        return meeting

    async def get_meeting_by_id(self, meeting_id: str) -> Meeting | None:
        result = await self._session.exec(
            select(Meeting).where(Meeting.id == meeting_id)
        )
        meeting = result.first()
        return meeting

    async def delete_meeting(self, meeting_id: str) -> None:
        meeting = await self.get_meeting_by_id(meeting_id)

        if not meeting:
            raise Exception("Meeting not found")

        await self._session.delete(meeting)
        await self._session.commit()


class MeetingTranscriptDAO:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_transcript_by_id(
        self, transcript_id: str
    ) -> MeetingTranscript | None:
        result = await self._session.exec(
            select(MeetingTranscript).where(MeetingTranscript.id == transcript_id)
        )
        transcript = result.first()
        return transcript

    async def insert_transcript(
        self, transcript_data: MeetingTranscriptCreateRequest
    ) -> MeetingTranscript:
        transcript_dict = transcript_data.model_dump(exclude={"id"})
        transcript = MeetingTranscript(**transcript_dict)
        self._session.add(transcript)
        await self._session.commit()
        return transcript

    async def delete_transcript(self, transcript_id: str) -> None:
        transcript = await self.get_transcript_by_id(transcript_id)

        if not transcript:
            raise Exception("Meeting Transcript not found")

        await self._session.delete(transcript)
        await self._session.commit()


class MeetingSummaryDAO:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_summary_by_id(self, summary_id: str) -> MeetingSummary | None:
        result = await self._session.exec(
            select(MeetingSummary).where(MeetingSummary.id == summary_id)
        )
        summary = result.first()
        return summary

    async def insert_summary(
        self, summary_data: MeetingSummaryCreateRequest
    ) -> MeetingSummary:
        summary_dict = summary_data.model_dump(exclude={"id"})
        summary = MeetingSummary(**summary_dict)
        self._session.add(summary)
        await self._session.commit()
        return summary

    async def delete_summary(self, summary_id: str) -> None:
        summary = await self.get_summary_by_id(summary_id)

        if not summary:
            raise Exception("Meeting Summary not found")

        await self._session.delete(summary)
        await self._session.commit()


class FeedbackEventDAO:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_feedback_by_id(self, feedback_id: str) -> FeedbackEvent | None:
        result = await self._session.exec(
            select(FeedbackEvent).where(FeedbackEvent.id == feedback_id)
        )
        feedback = result.first()
        return feedback

    async def insert_feedback(
        self, feedback_data: FeedbackEventCreateRequest
    ) -> FeedbackEvent:
        feedback_dict = feedback_data.model_dump(exclude={"id"})
        feedback = FeedbackEvent(**feedback_dict)
        self._session.add(feedback)
        await self._session.commit()
        return feedback

    async def delete_feedback(self, feedback_id: str) -> None:
        feedback = await self.get_feedback_by_id(feedback_id)

        if not feedback:
            raise Exception("Feedback not found")

        await self._session.delete(feedback)
        await self._session.commit()


class FeedbackResponseDAO:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_response_by_id(self, response_id: str) -> FeedbackResponse | None:
        result = await self._session.exec(
            select(FeedbackResponse).where(FeedbackResponse.id == response_id)
        )
        response = result.first()
        return response

    async def insert_response(
        self, response_data: FeedbackResponseCreateRequest
    ) -> FeedbackResponse:
        response_dict = response_data.model_dump(exclude={"id"})
        response = FeedbackResponse(**response_dict)
        self._session.add(response)
        await self._session.commit()
        return response

    async def delete_response(self, response_id: str) -> None:
        response = await self.get_response_by_id(response_id)

        if not response:
            raise Exception("Feedback not found")

        await self._session.delete(response)
        await self._session.commit()


class PersonalityProfileDAO:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_profile_by_id(self, profile_id: str) -> PersonalityProfile | None:
        result = await self._session.exec(
            select(PersonalityProfile).where(PersonalityProfile.id == profile_id)
        )
        profile = result.first()
        return profile

    async def insert_profile(
        self, profile_data: PersonalityProfileCreateRequest
    ) -> PersonalityProfile:
        profile_dict = profile_data.model_dump(exclude={"id"})
        profile = PersonalityProfile(**profile_dict)
        self._session.add(profile)
        await self._session.commit()
        return profile

    async def delete_profile(self, profile_id: str) -> None:
        profile = await self.get_profile_by_id(profile_id)

        if not profile:
            raise Exception("Personality Profile not found")

        await self._session.delete(profile)
        await self._session.commit()

    async def update_profile(
        self, profile_id: str, profile_data: PersonalityProfileUpdateRequest
    ) -> PersonalityProfile:
        profile = await self.get_profile_by_id(profile_id)
        if not profile:
            raise Exception("Profile not found")

        for key, value in profile_data.model_dump(exclude_none=True).items():
            setattr(profile, key, value)

        self._session.add(profile)
        await self._session.commit()

        return profile
