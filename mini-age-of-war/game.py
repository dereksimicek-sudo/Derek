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
    
# -------------------------------
# GAME STATE
# -------------------------------

# This variable controls whether the game is running
game_running = True

# List to store all units
units = []
enemy_units = []

# -------------------------------
# UNIT CLASS
# -------------------------------
class Unit:
    """
    Represents a single moving unit.
    """

    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = direction  # 1 = right, -1 = left
        self.health = 3  # how many hits unit can take

    def move(self):
        self.x += self.speed * self.direction

    def draw(self):
        # Draw unit as small square
        ctx.fillStyle = "black"
        ctx.fillRect(self.x, self.y, 10, 10)

# Spawn one unit (for testing)
def spawn_unit():
    unit = Unit(80, 190)
    units.append(unit)

spawn_unit()

def spawn_enemy():
    enemy = Unit(700, 190, direction=-1)
    enemy_units.append(enemy)

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

    # Draw enemy units
    for enemy in enemy_units:
        ctx.fillStyle = "darkred"
        ctx.fillRect(enemy.x, enemy.y, 10, 10)

# -------------------------------
# COMBAT
# -------------------------------
def handle_combat():
    for unit in units:
        for enemy in enemy_units:

            if abs(unit.x - enemy.x) < 10:
                unit.health -= 1
                enemy.health -= 1

    # REMOVE DEAD UNITS (must be inside function!)
    units[:] = [u for u in units if u.health > 0]
    enemy_units[:] = [e for e in enemy_units if e.health > 0]

# -------------------------------
# GAME LOOP
# -------------------------------
def game_loop():
    if game_running:

        # Move units ONCE
        for unit in units:
            unit.move()

        for enemy in enemy_units:
            enemy.move()

        # Handle combat
        handle_combat()

        # Draw everything
        draw()

# Run the game loop every 16 ms (~60 FPS)
timer.set_interval(game_loop, 16)

# Enemy spawns every 2 seconds
timer.set_interval(spawn_enemy, 2000)

# -------------------------------
# INPUT (MOUSE CLICK)
# -------------------------------
def on_click(event):
    """
    This function is called whenever the player clicks
    on the canvas. It spawns a new unit.
    """
    spawn_unit()


# Bind mouse click to function
canvas.bind("click", on_click)