import dataclasses


@dataclasses.dataclass
class Game:

    game_id:int
    number_of_guesses:int
    max_guess:int
    status:int
    username:str
    secret_word_id:int

    def __init__(self, game_id, number_of_guesses, max_guess, status, username, secret_word_id):
        self.game_id = game_id
        self.number_guesses = number_of_guesses
        self.username = username
        self.max_guess = max_guess
        self.status = status
        self.secret_word_id = secret_word_id
