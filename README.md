# Falcon99
This is an open source Game Engine. Seamlessly stream 2D games. Supports Multiplayer games and more. This will be updated as the features get added incrementally.

# TODO
 - the way in which GameInformation Object is injected in the code(FalconServerExample.py L11) is doubtful. Decision 
 needs to be made whether the FalconServer object should be instantiated the way it is now, or should it be instantiated
 and should listen to clients connecting to it on a dedicated port. This would also make the application language 
 agnostic.
 - self.game_workers (FalconServer.py L28) dictionary object stores stale entries of game workers that are no longer active.
 
 # Reference
 - https://docs.python.org/3/library/asyncio.html
 - https://docs.python.org/3/library/asyncio-sync.html
 - https://docs.python.org/3/library/asyncio-task.html
 - https://docs.python.org/3/library/asyncio-subprocess.html#asyncio-subprocess
 - https://realpython.com/async-io-python/
 - https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait
 
 