class UserNotFound(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


class UserAlreadyExists(Exception):
    pass
