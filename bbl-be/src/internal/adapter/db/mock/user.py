from typing import Dict
from domain.user import User


class MockUser:
    def __init__(self):
        self.users_db: Dict[str, User] = {}

    def get_instance(self):
        return self.users_db
