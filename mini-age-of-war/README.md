# Mini Age of War (Python + Brython)

## 📌 Project Description

This project is a simplified browser-based strategy game inspired by the classic *Age of War*.
The player will be able to spawn units that automatically move toward the enemy base and engage in combat.

The goal of the game is to destroy the enemy base while defending your own.

---

## ⚙️ Technologies Used

* **Python** – main game logic
* **Brython** – allows Python code to run in the browser
* **HTML5 Canvas** – used for rendering graphics

---

## 🧠 How It Works

The game runs entirely in the browser using Brython.
Instead of executing Python code through a standard interpreter, the script is executed inside the browser environment.

The main components of the game are:

* **Canvas rendering system** – draws the game world
* **Game loop** – updates the game continuously
* **Units** – player and enemy soldiers
* **Combat system (planned)** – units fight when they meet
* **Base system** – each side has a base with health

---

## 🎮 Current Features

* Basic game window using HTML canvas
* Rendering of:

  * ground
  * player base
  * enemy base
* Structured and commented Python code

---

## 🚀 Planned Features

* Game loop (continuous updates)
* Unit spawning system
* Unit movement
* Combat mechanics
* Enemy AI
* Win / lose conditions

---

## ▶️ How to Run the Game

1. Open the project folder
2. Open `index.html` in a web browser
   (recommended: use **Live Server** in VS Code)
3. The game will automatically start in the browser

---

## 📁 Project Structure

```
project-folder/
│
├── index.html   # Main HTML file with canvas and Brython setup
├── game.py      # Python game logic (executed in browser)
└── README.md    # Project documentation
```

---

## 💡 Notes

* The Python file (`game.py`) cannot be run using the standard Python interpreter.
* It must be executed through the browser using Brython.

---

## 👨‍💻 Author

Student project for learning:

* Git and version control
* Python programming
* Basic game development
* Browser-based technologies

---
