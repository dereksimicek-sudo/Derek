# Import Brython browser tools
from browser import document

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


# Call draw once (for now)
draw()