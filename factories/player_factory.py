# player_factor.py
from core.entity import Entity

from core.states import PlayerState, CloudState



def makePlayer():
    entity = Entity()
    entity.type = 'player'
    entity.state = PlayerState.IDLE
    return entity