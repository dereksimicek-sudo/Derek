# Import Brython browser tools
from browser import document, timer 

# Get canvas element from HTML
canvas = document["game"]

# Get drawing context (used to draw shapes)
ctx = canvas.getContext("2d")

# -------------------------------
# GAME STATE
# -------------------------------
game_result = ""

# This variable controls whether the game is running
game_running = True
player_base_health = 20
enemy_base_health = 20

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

    # Display base health (OUTSIDE loop!)
    ctx.fillStyle = "black"
    ctx.fillText(f"Player: {player_base_health}", 20, 20)
    ctx.fillText(f"Enemy: {enemy_base_health}", 650, 20)

    # Display win/lose message
    if not game_running:
        ctx.fillStyle = "black"
        ctx.font = "30px Arial"
        ctx.fillText(game_result, 300, 150)
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

def handle_base_damage():
    global player_base_health, enemy_base_health, game_running

    # Player units hitting enemy base
    for unit in units:
        if unit.x > 730:  # reached enemy base
            enemy_base_health -= 1
            unit.health = 0  # unit disappears

    # Enemy units hitting player base
    for enemy in enemy_units:
        if enemy.x < 70:  # reached player base
            player_base_health -= 1
            enemy.health = 0

        global game_result

        if enemy_base_health <= 0:
            game_result = "YOU WIN!"
            game_running = False

        if player_base_health <= 0:
            game_result = "YOU LOSE!"
            game_running = False

# -------------------------------
# GAME LOOP
# -------------------------------

def game_loop():
    if game_running:

        # Move units
        for unit in units:
            unit.move()

        for enemy in enemy_units:
            enemy.move()

        # Combat first
        handle_combat()

        # Then base damage
        handle_base_damage()

        # THEN draw (last!)
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