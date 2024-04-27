# Rook Framework
#### Implemented in Python 3.11.9

### Important to Note:

Turn based has not been fully implemented. You can still use it by using Game.next_player_move() or Game.next_bid(), but you would need to pass in parameters.

### Game Theory

Game Theory will be menu option 2. It prompts to enter number of games to simulate. Eeach game has about 15 tricks per game. Then you can enter what you want the starting strategy for each player to be. After that you can say which game you want the players to be able to switch strategies. Players will be locked into their starting before this game and be able to switch after. If you set the game number they can move at higher than the total games you're simulating, the player will be locked into their start strategy for the whole simulation. Players will use one strategy for the duration of one game and get a reward for that strategy if they win the game. Each player will then use epsilon greedy to choose the best strategy so far or pick random. There are 5 strategies, play highest point, play strongest card, play weakest card, flush trump, and random. 

In my tests, when a player can move and is against two agents locked into random mode, the player will converge to the flush-trump strategy. If you then lock in one player to flush trump and the other to random but let the third one converge, it converged to either the highest point strategy or flush trump. If you locked two players into flush trump and let the third one converge, it also converged to flush trump. This is the nash equilibrium. 

### Rules:

The following rules are derived from the official rules of Rook (Roberts; “Rook”).

Rook is played with cards numbered 1-14 of each color red, yellow, black, and green, as well as a Rook bird card.  Of these, 5’s are worth 5 points, 10’s and 14’s are worth 10, and the Rook is worth 20 when scoring.

Cards are dealt to each player until none are left, with five set facedown in the “nest.”

Each round starts with a bidding phase.  Players bid how many points they think they will win if they can choose the trump color and exchange cards with the nest.  If they match or surpass their bid in the round, they keep any earned points like the other players; if they fail, they earn the negative value of their bid.  Bidding continues until all but one player has passed and any players who have passed cannot bid again.

After the winner exchanges any number of cards from their hand with the nest and decides the trump color, play proceeds in tricks.  In a trick, each player sets down a card of the same color as the first card played in the trick (called “following suit”).  If this isn’t possible, they play a card of another color.  The highest-valued card of the color led wins, unless a trump card is played, in which case the highest-valued trump card wins.  The rook card beats any other card and may be played regardless of led color.  The winner takes all of the cards for scoring later.  Each trick is led by the winner of the previous trick, and the winner of the final trick claims the nest and any unused cards.

Every player’s won cards are added together, scores calculated and adjusted depending on initial bids, and a new round started until a point threshold is reached.

For our version, we consider a three-player game with a nest but without partners.  Consequently, bidding starts at 35 instead of 70 and no cards will be excluded from the deck.

### How To Run:

You can use the framework built here in the components, algorithms, and enums files to run your own games, or you can run [main.py](main.py) to have a simulation game run with 3 random AIs.

### Simulation Game:

The simulation game just involves three players playing the game randomly whilst still following the rules. It will tell you who won and with how many points at the end.

### How To Use Framework:

You just have to define a Game object. The Game object takes in a trump color, starting player ID, and a list of Player objects. You can then run tricks one by one, or play the full game.

You can only input alternate moves and bids by going turn by turn and using the Game.next_player_move() and Game.next_bid() methods.

### References:

Roberts, Jason. (2011). Official Rules. Rook Game. 
https://rookgame.com/official-rules/

“Rook.” Hasbro.com, Hasbro, https://www.hasbro.com/common/instruct/Rook.pdf. Accessed 13 Apr. 2024.
