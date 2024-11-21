# Pazaak Game Application

This is a Python-based implementation of the Pazaak game, featuring a graphical user interface (GUI) built with Tkinter. The game allows players to compete against an AI opponent in a strategic card game where the goal is to reach a total of 20 points on the board without exceeding it.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Rules](#rules)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [License](#license)

## Description

Pazaak is a turn-based card game where two players (you and an AI opponent) take turns drawing cards and playing cards from their hand to reach a total as close to 20 as possible. The first player to win three rounds wins the game.

## Features

1. **Core Gameplay**:
   - Turn-based mechanics.
   - AI opponent with strategic behavior.
2. **Interactive GUI**:
   - Hand cards that can be played or inverted.
   - Dynamic board and score updates.
3. **Customizable Rules**:
   - Automatic pass at 20 points.
   - Handling of exceeding 20 points with card inversion.
4. **Game Feedback**:
   - Round results and game winners are displayed with message boxes.

## Rules

- **Objective**:
  - The goal is to have your total points on the board equal to or as close to 20 as possible without exceeding it.
- **Winning a Round**:
  - If both players pass, the player closest to 20 without exceeding it wins the round.
  - If a player exceeds 20 points, they lose the round unless they can adjust their total before passing.
- **Winning the Game**:
  - The first player to win three rounds wins the game.
- **Gameplay**:
  - Draw a card from the deck automatically at the start of your turn.
  - Play hand cards to adjust your total or invert their values (e.g., +3 to -3).
  - Pass to end your turns for the current round.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:
```bash
   git clone <repository-url>
   cd <project-directory>
```
2. Ensure the necessary Python libraries are installed.

3. Save all the files in the appropriate project structure as listed below.

## Running the Application

1. Run the main script:
```bash
   python main.py
```
2. The application window will open, and you can start playing Pazaak.

## Project Structure

project/
├── game.py                  # Core game logic
├── pazaakui.py              # Graphical user interface (Tkinter)
├── main.py                  # Entry point for the application
└── README.md                # Documentation

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this project.
