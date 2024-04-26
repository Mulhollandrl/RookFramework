# Rook Framework
#### Implemented in Python 3.11

#### You can find the library versions used in [requirements.txt](requirements.txt)
---

### Table of Contents:

- [**Rules**](#rules)

- [**How to Run & Expected Outputs**](#how-to-run--expected-outputs)

- [**Other Parts of Project**](#other-parts-of-project)

- [**References**](#references)

---

### Rules:

The following rules are derived from the official rules of Rook (Roberts; “Rook”).

Rook is played with cards numbered 1-14 of each color red, yellow, black, and green, as well as a Rook bird card.  Of these, 5’s are worth 5 points, 10’s and 14’s are worth 10, and the Rook is worth 20 when scoring.

Cards are dealt to each player until none are left, with five set facedown in the “nest.”

Each round starts with a bidding phase.  Players bid how many points they think they will win if they can choose the trump color and exchange cards with the nest.  If they match or surpass their bid in the round, they keep any earned points like the other players; if they fail, they earn the negative value of their bid.  Bidding continues until all but one player has passed and any players who have passed cannot bid again.

After the winner exchanges any number of cards from their hand with the nest and decides the trump color, play proceeds in tricks.  In a trick, each player sets down a card of the same color as the first card played in the trick (called “following suit”).  If this isn’t possible, they play a card of another color.  The highest-valued card of the color led wins, unless a trump card is played, in which case the highest-valued trump card wins.  The rook card beats any other card and may be played regardless of led color.  The winner takes all of the cards for scoring later.  Each trick is led by the winner of the previous trick, and the winner of the final trick claims the nest and any unused cards.

Every player’s won cards are added together, scores calculated and adjusted depending on initial bids, and a new round started until a point threshold is reached.

For our version, we consider a three-player game with a nest but without partners.  Consequently, bidding starts at 35 instead of 70 and no cards will be excluded from the deck.

---

### How to Run & Expected Outputs:

#### Requirements: Python 3.11, gymnasium, stable_baselines3, numpy, matplotlib

You can opt to use the requirements.txt that is included with the project, as that is what it was built with.

#### Auction Analysis:
There are two options for running auction analysis: individual games, and measurements. As we worked on the project, both analysis options offered interesting insights, so we have kept them both available in the final deliverable.

If you would like to observe the progress and/or outcomes of individual Rook games that use english, sealed, or dutch auctions for bidding, run play_game.py to simulate a game. You will be prompted with several questions to set up the game, and then the program will run through the game. As the game runs, you may be an observer or an active participant, depending on your responses to the setup prompts. The outcomes of the game are printed to the console - as well as the player actions throughout the game that lead to those outcomes, if you chose to accept the offer of detailed output during setup. 

If you would like to understand how the different auction types perform relative to each other, run compare_bidding.py to run simulations and visualize the results. You will be prompted to enter a number as the sample size for your analysis, and then the program will simulate that number of games with each auction type, using the same card distribution for the three auction types with each game to ensure a fair comparison. When the simulations are finished, you will be offered a menu with options to display charts of the comparative bid amounts, successful fulfillment of bids, and correlation of winning bids with winning games. All charts are displayed with pyplot and will appear in external windows.
Game Theory

#### Reinforcement Learning:
	
To even run any of the Reinforcement Learning code, you will need Python 3.11, as well as the requirements listed in requirements.txt.

A user can train the model by running “train.py” in the main directory. You can then load the model to play against two greedy players by running “run.py”. There are defaults for both files that default to training a PPO algorithm model. There is commented out code to switch it to an AC2 algorithm if that is desired.
	
There are two main expected outputs. The first is the log of all of the data points that were logged with TensorBoard. These can be found in the “reinforcement_learning/board” folder. You can see them in a TensorBoard by running ‘Tensorboard --logdir “reinforcement_learning/board”’ in the main directory. You must have TensorBoard installed for this.

The second expected output is the trained model itself. You can find this within the “reinforcement_learning/tmp”. If you trained it with the default settings, it will be named “best_model_PPO.zip”. You can use this just like any other StableBaselines3 trained model by using the “model.load()” method.

---

### Other Parts of Project:

- [**Project Proposal**](https://docs.google.com/document/d/11lwKcH4fTxylRSHpisRFnG454cWV0q2jCD6ERH_jWf8/edit?usp=sharing)

- [**Final Presentation Slides**](https://docs.google.com/presentation/d/1yGHJio8JCdbwbOZmQ7X9vyuEqH7gxVHal0Hs4oc_Rds/edit?usp=sharing)

- [**Project Final Report**](https://docs.google.com/document/d/1wS5WK6P6hPg2VJCjVdKLrkyw3i2fu-dKQeSsB2mwGHo/edit?usp=sharing)

- [**Best Model "board" Folder**](https://drive.google.com/drive/folders/1XsRqU2qyDnxpYLbj0Fd3qSnL8dz0RjlW?usp=sharing)

- [**Best Model "tmp" Folder**](https://drive.google.com/drive/folders/1UQGPhVXptw2AIicEv_A2iyHSh37TLKas?usp=sharing)

- [**Project Github**](https://github.com/Mulhollandrl/RookFramework)

---

### References:

Roberts, Jason. (2011). Official Rules. Rook Game. https://rookgame.com/official-rules/

“Rook.” Hasbro.com, Hasbro, https://www.hasbro.com/common/instruct/Rook.pdf. Accessed 13 Apr. 2024.

ClarityCoders. (2022). MarioPPO. https://github.com/ClarityCoders/MarioPPO