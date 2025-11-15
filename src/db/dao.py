from sqlmodel.ext.asyncio.session import AsyncSession


class UserDao:
    def __init__(self, session: AsyncSession):
        self._session = session

    def add_user(self, user_id, user_data): ...

    def get_user(self, user_id): ...

    def update_user(self, user_id, user_data): ...

    def delete_user(self, user_id): ...


class PersonalityProfileDao:
    def __init__(self, session: AsyncSession):
        self._session = session

    def add_profile(self, profile_id, profile_data): ...

    def get_profile(self, profile_id): ...

    def update_profile(self, profile_id, profile_data): ...

    def delete_profile(self, profile_id): ...
