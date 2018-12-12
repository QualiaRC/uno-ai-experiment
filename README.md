# Uno AI Experiment
An AI project for the Fall 2018 University of Minnesota course: CSCI 4511W: Introduction to Artificial Intelligence.

## Instructions
Run `execute.py` in the root directory to play the game.
You can change the number of opponents and run count in `execute.py` as needed.

## Files
<b>execute.py</b><br>Runs the program

<b>uno/match.py</b><br>The match class, contains players, deck and discard pile. Contains game loop and handles player moves.

<b>uno/game_components/card.py</b><br>The card class, contains the information for a card (Color, Type) as well as comparison methods.

<b>uno/game_components/deck.py</b><br>The deck class, is a list of cards with draw and recycle methods. Contains 108 cards.

<b>uno/game_components/discard_pile.py</b><br>The discard pile class, is a list of cards with a top property and add card method.

<b>uno/players/player.py</b><br>The base player class, has a name and hand, as well as methods for interacting with the game.

<b>uno/players/random_ai.py</b><br>A player that randomly chooses cards to play.

<b>uno/players/minimax_player.py</b><br>A player that chooses cards to play using a Minimax algorithm.

<b>uno/players/human_player.py</b><br>A player that chooses cards to play via user input.

<b>uno/players/minimax_algorithm/minimax_algo.py</b><br>An adversarial search that determines which cards to play given information about the game.

<b>uno/players/minimax_algorithm/heuristics.py</b><br>The class for heuristic functions that are used in the Minimax algorithm.

## DISCLAIMER
Uno is owned by Mattel, Inc. This repo is protected under Fair Use, as it is being used for educational purposes.

This code is intended for educational purposes only, and is not indended for redistribution of the game itself, nor is it a substitute for the original game.
