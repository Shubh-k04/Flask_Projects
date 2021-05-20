from random import randint
class Game:
    def __init__(self) -> None:
        self.abilities = [
            'rock',
            'paper',
            'scissors'
        ]
        
        self.player_score = 0
        self.bot_score = 0
        self.bot = None
        self.winner = None
        self.games = 0
        self.user = None
        self.started = False
        self.is_in_progress = False
        
    def select(self):
        self.bot = self.abilities[randint(0 , 2)]
    
    def set_winner(self , user_choice):
        self.user = user_choice
        
        self.select()
        
        self.games += 1
        
        if(user_choice == self.bot):
            self.winner = 'Draw'
             
        elif((user_choice == 'rock' and self.bot == 'paper') or (user_choice == 'paper' and self.bot == 'scissors') or (user_choice == 'scissors' and self.bot == 'rock')):
            self.bot_score += 1
            self.winner = "Bot"
        else:
            self.winner = "Player"
            self.player_score += 1
            return "Player"
    
    def refresh_content(self):
        self.__init__()
