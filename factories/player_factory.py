# player_factor.py
from core.entity import Entity

from core.states import PlayerState

def makePlayer():
    entity = Entity()
    entity.type = 'player'
    entity.state = PlayerState.IDLE
    print(f'[L][makePlayer] entity created with type: {entity.type}, state: {entity.state}')
    return entity