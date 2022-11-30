import dataclasses


@dataclasses.dataclass
class Guess:
    id: int
    game_id: int
    guessword_id: int

    def __init__(self, game_id, guessword_id):
        self.game_id = game_id
        self.guessword_id = guessword_id

    def __init__(self, id, game_id, guessword_id):
        self.id = id
        self.game_id = game_id
        self.guessword_id = guessword_id

    def setId(self, id):
        self.id = id
