# Import Brython browser tools
from browser import document, timer, window 

# Get canvas element from HTML
canvas = document["game"]

# Get drawing context (used to draw shapes)
ctx = canvas.getContext("2d")

# Resize canvas to match the browser window
width = 800
height = 300

def set_canvas_size(event=None):
    global width, height
    width = int(window.innerWidth)
    height = int(window.innerHeight)
    canvas.attrs["width"] = width
    canvas.attrs["height"] = height
    canvas.style.width = f"{width}px"
    canvas.style.height = f"{height}px"

set_canvas_size()
window.bind("resize", set_canvas_size)

# -------------------------------
# GAME STATE
# -------------------------------
game_result = ""

# This variable controls whether the game is running
game_running = True
# This variable controls whether the game has started
game_started = False
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

def spawn_unit():
    ground_y = int(canvas.height * 0.7)
    unit = Unit(80, ground_y - 10)
    units.append(unit)


def spawn_enemy():
    if not game_started or not game_running:
        return

    ground_y = int(canvas.height * 0.7)
    enemy = Unit(canvas.width - 100, ground_y - 10, direction=-1)
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
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    # Compute layout based on current canvas size
    width = canvas.width
    height = canvas.height
    ground_y = int(height * 0.7)
    base_size = min(60, int(height * 0.15))
    player_base_x = 20
    player_base_y = ground_y - base_size
    enemy_base_x = width - 20 - base_size
    enemy_base_y = ground_y - base_size
    score_x = max(20, width - 150)

    # Draw ground
    ctx.fillStyle = "lightgreen"
    ctx.fillRect(0, ground_y, width, height - ground_y)

    # Draw player base
    ctx.fillStyle = "blue"
    ctx.fillRect(player_base_x, player_base_y, base_size, base_size)

    # Draw enemy base
    ctx.fillStyle = "red"
    ctx.fillRect(enemy_base_x, enemy_base_y, base_size, base_size)

    # Draw all units
    for unit in units:
        unit.draw()
    
    # Draw enemy units
    for enemy in enemy_units:
        ctx.fillStyle = "darkred"
        ctx.fillRect(enemy.x, enemy.y, 10, 10)

    # Display base health 
    ctx.fillStyle = "black"
    ctx.fillText(f"Player: {player_base_health}", 20, 20)
    ctx.fillText(f"Enemy: {enemy_base_health}", score_x, 20)

    # Display win/lose message
    if not game_running and game_started:
        ctx.fillStyle = "black"
        ctx.font = "30px Arial"
        ctx.fillText(game_result, 300, 150)

    if not game_started:
        ctx.fillStyle = "rgba(255, 255, 255, 0.9)"
        ctx.fillRect(0, 0, 800, 300)
        ctx.fillStyle = "black"
        ctx.font = "34px Arial"
        ctx.fillText("Mini Age of War", 240, 120)
        ctx.font = "20px Arial"
        ctx.fillText("Click Start to begin", 285, 160)
        ctx.fillText("Then click the battlefield to spawn units.", 215, 190)
        return
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

    width = canvas.width
    right_limit = width - 70

    # Player units hitting enemy base
    for unit in units:
        if unit.x > right_limit:  # reached enemy base
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
    if game_started and game_running:

        # Move units
        for unit in units:
            unit.move()

        for enemy in enemy_units:
            enemy.move()

        # Combat first
        handle_combat()

        # Then base damage
        handle_base_damage()

    # Always draw so the start screen or game over state is visible
    draw()

# Run the game loop every 16 ms (~60 FPS)
timer.set_interval(game_loop, 16)

# Enemy spawns every 2 seconds
timer.set_interval(spawn_enemy, 2000)

# -------------------------------
# INPUT (MOUSE CLICK)
# -------------------------------
def start_game(event=None):
    global game_started, game_running, player_base_health, enemy_base_health, game_result

    if game_started:
        return

    game_started = True
    game_running = True
    game_result = ""
    player_base_health = 20
    enemy_base_health = 20
    units.clear()
    enemy_units.clear()
    
    # Hide the start button
    try:
        document["startButton"].style.display = "none"
    except Exception:
        pass
    
    draw()


def on_click(event):
    """
    This function is called whenever the player clicks
    on the canvas. It spawns a new unit if the game has started.
    """
    if game_started and game_running:
        spawn_unit()


# Bind mouse click to function
canvas.bind("click", on_click)

# Bind start button click to function
try:
    document["startButton"].bind("click", start_game)
except Exception:
    pass