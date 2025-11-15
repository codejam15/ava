class UserDao:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, user_data):
        self.users[user_id] = user_data

    def get_user(self, user_id):
        return self.users.get(user_id)

    def update_user(self, user_id, user_data):
        if user_id in self.users:
            self.users[user_id] = user_data
            return True
        return False

    def delete_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


class PersonalityProfileDao:
    def __init__(self):
        self.profiles = {}

    def add_profile(self, profile_id, profile_data):
        self.profiles[profile_id] = profile_data

    def get_profile(self, profile_id):
        return self.profiles.get(profile_id)

    def update_profile(self, profile_id, profile_data):
        if profile_id in self.profiles:
            self.profiles[profile_id] = profile_data
            return True
        return False

    def delete_profile(self, profile_id):
        if profile_id in self.profiles:
            del self.profiles[profile_id]
            return True
        return False
