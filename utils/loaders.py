
def load_activity():
    import level
    '''# Function to load all parameters of the activity, and this build the entities for each level.
    # Is important that this function, is called before the system which has globals.world.entities.'''

    level.loadLevel()
