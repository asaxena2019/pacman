# SidescrollGameMode will establish a randomly generated board every single time
# a new game starts, will allow the user to travel off screen
class SidescrollGameMode(Mode):
    pass

# CreativeMode will allow the user to create their own map, will play like
# original mode
class CreativeMode(Mode):
    pass

# MultiplayerMode will allow two users to player, one as ghost
# can play in original mode
class MultiplayerMode(Mode):
    pass
