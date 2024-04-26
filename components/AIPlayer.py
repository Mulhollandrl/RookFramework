from components.Player import Player


class AIPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "AI"
