#level.py
import globals
import logging
from core.states import PlayerState

logger = logging.getLogger(__name__)

class Level:
    def __init__(self, entities=None, scene=None, winFunc=None, loseFunc=None):
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc
        self.scene = scene

    def isWon(self):
        # This defines a method named isWon in the Level class. This method will check if the level has been won
        if self.winFunc is not None:
            win_result = self.winFunc(self)
            # print(f'isWon winFunc result: {win_result}')
            #This calls the winFunc function, passing the current instance of the Level as an argument (self).
            #The result of this function call is stored in the win_result variable.
            if win_result:
                # If win_result is True, it means the level is won, so the method returns True.
                return True
        # If no custom winFunc was provided, the method checks the global player’s state to see if it matches a predefined winning state (engine.PlayerState.RIGHT).
        # The result is stored in player_won.
        player_won = globals.player1.state == PlayerState.RIGHT
        # print(f'isWon player.state: {globals.player1.state}, player_won: {player_won}')
        return player_won

    def isLost(self):
        if self.loseFunc is not None:
            lose_result = self.loseFunc(self)
            # print(f'isLost loseFunc result: {lose_result}')
            if lose_result:
                return True
        player_lost = globals.player1.state == PlayerState.WRONG
        # print(f'isLost player.state: {globals.player1.state}, player_lost: {player_lost}')
        return player_lost

def loadLevel():
    try:
        import constants.global_constants as constants
        from factories.player_factory import makePlayer
        #print(f'loadLevel game_mechanic = {game_mechanic}')
        #logging.exception(f'loadLevel game_mechanic = {game_mechanic}')

        print(f'[L][loadLevel]')
        globals.world = Level(
            scene=[
                1
            ],
            entities=[
                globals.player1
            ]

        )
        print(f'[Level]  globals.world.entities: {globals.world.scene}')
        print(f'[Level]  globals.world.entities: {globals.world.entities}')




    except Exception as e:
        print(f'[Level] error: {e}')
        logger.exception(f'[Level] game_mechanic = ')
