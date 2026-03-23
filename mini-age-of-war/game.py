# Import Brython browser tools
from browser import document, timer 

# Get canvas element from HTML
canvas = document["game"]

# Get drawing context (used to draw shapes)
ctx = canvas.getContext("2d")

# -------------------------------
# DRAW FUNCTION
# -------------------------------
def draw():
    """
    This function draws basic elements on the screen.

    It will be expanded later to include units, combat,
    and animations.
    """

    # Clear the screen
    ctx.clearRect(0, 0, 800, 300)

    # Draw ground
    ctx.fillStyle = "lightgreen"
    ctx.fillRect(0, 200, 800, 100)

    # Draw player base (left side)
    ctx.fillStyle = "blue"
    ctx.fillRect(20, 150, 50, 50)

    # Draw enemy base (right side)
    ctx.fillStyle = "red"
    ctx.fillRect(730, 150, 50, 50)

# Import Brython browser tools
from browser import document, timer

# Get canvas element from HTML
canvas = document["game"]

# Get drawing context (used to draw shapes)
ctx = canvas.getContext("2d")

# -------------------------------
# GAME STATE
# -------------------------------

# This variable controls whether the game is running
game_running = True

# List to store all units
units = []

# -------------------------------
# UNIT CLASS
# -------------------------------
class Unit:
    """
    Represents a single moving unit.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1  # movement speed

    def move(self):
        # Move to the right (toward enemy)
        self.x += self.speed

    def draw(self):
        # Draw unit as small square
        ctx.fillStyle = "black"
        ctx.fillRect(self.x, self.y, 10, 10)

# Spawn one unit (for testing)
def spawn_unit():
    unit = Unit(80, 190)
    units.append(unit)

spawn_unit()

# -------------------------------
# DRAW FUNCTION
# -------------------------------
def draw():
    """
    Draws all game elements on the screen.

    This function is called repeatedly in the game loop,
    allowing animations and updates.
    """

    # Clear the screen (important for animation)
    ctx.clearRect(0, 0, 800, 300)

    # Draw ground
    ctx.fillStyle = "lightgreen"
    ctx.fillRect(0, 200, 800, 100)

    # Draw player base
    ctx.fillStyle = "blue"
    ctx.fillRect(20, 150, 50, 50)

    # Draw enemy base
    ctx.fillStyle = "red"
    ctx.fillRect(730, 150, 50, 50)

    # Draw all units
    for unit in units:
        unit.draw()

# -------------------------------
# GAME LOOP
# -------------------------------
def game_loop():
    """
    Main game loop.

    This function runs repeatedly (about 60 times per second).
    It updates the game and redraws everything.
    """

def game_loop():
    if game_running:

        # Move all units
        for unit in units:
            unit.move()

        draw()


# Run the game loop every 16 ms (~60 FPS)
timer.set_interval(game_loop, 16)