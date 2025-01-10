from t_ghost import *
from t_door import *
import random, time, sys

doors = [
    tDoor(origin=Vec2D(-300,0), size = 200, autoUpdate = True),
    tDoor(origin=Vec2D(0,0), size = 200, autoUpdate = True),
    tDoor(origin=Vec2D(300,0), size = 200, autoUpdate = True),
]
banner = tBanner(origin=Vec2D(-300, -100))
def DoorReset():
    global score, ghost_pos, game_end
    for d in doors:
        if d.isOpen(): d.Close()
    score = 0
    ghost_pos = random.randint(0, len(doors) - 1); # print(f"GHOST @{ghost_pos}")
    game_end = False
    banner.Message(f'Click any door, please!')
    
def DoorOpenPostEvent():
    global score, ghost_pos, game_end
    for d in doors:
        if d.isOpen():
            if d == doors[ghost_pos]:
                tGhost(origin=d.origin + Vec2D(25, 50), size = 150)
                banner.Message(f"OOPs! You got {score}")
                game_end = True
                time.sleep(1)
                DoorReset()
            else:
                score += 1
                banner.Message(f"Good luck! You got {score}")
                time.sleep(1)
                d.Close()
                ghost_pos = random.randint(0, len(doors) - 1); # print(f"GHOST @{ghost_pos}")
                banner.Message(f'Click any door, please!')
            return True
    return False

DoorReset()
tObject.Done(postEvent=DoorOpenPostEvent)