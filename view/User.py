import dataclasses


@dataclasses.dataclass
class User:

    username: str
    password: str

    def __init__(self, username, password):
        self.username =username
        self.password = password