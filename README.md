This project simulates 1,000,000 rounds of blackjack using basic strategy for both card counting and non card counting hands. The purpose is to determine if there is actually an advantage to card counting in casinos and if so to calculate the advantage for the player with card counting. Just like typical blackjack tables found in most casinos, a blackjack pays 3:2. There are 6 decks to a shoe and the shoe will be reshuffled when there are less than 75 cards left similar to real life blackjack where shoes are reshuffled when there are 1-2 decks left.

**blackjack_terminal.py:**
This is the backbone for the whole project. This is a terminal blackjack game where the user can manually place bets and play a game a blackjack such as hitting, standing, splitting, and doubling.

**blackjack_simulation.py:**
This takes the original blackjack_terminal file and simulates 1,000,000 rounds of blackjack with a starting bankroll of $10,000,000 and standard bet of $50 per hand. This implements basic strategy based on many blackjack strategy cards found online. 

**blackjack_simulation_card_counting.py:**
This takes the previous blackjack_simulation.py file and adds a hi-lo system for card counting allowing the program to adjust their bet depending on the running count. A higher running count means a higher bet would be placed where a lower running count would be the minimum bet would be placed which is 50. 

blackjack_strategy_analysis.pbix:
This is a Power BI dashboard that containts various charts and graphs comparing the results of Basic Strategy vs. Hi-Lo card counting.

Based on the findings of this simulation, card counting will have around a 1.0-1.5% advantage over non card counting. These findings are typical to the actual statistics of real life card counting. No matter if you do basic strategy or Card counting, the win/loss/push percentages will always be around 43.5/48/8.5. Its whether you adjust your bet depending on the count that causes players to profit from playing blackjack.

---

# SAMPLE OUTPUTS (numbers will vary due to randomness of shuffling the shoe)

**blackjack_simulation.py:**

```
Simulating 1,000,000 rounds...

       CHECKPOINTS       
-------------------------
   checkpoint_round  profit       roi
0            100000  -13550 -0.271000
1            200000  -65200 -0.652000
2            300000  -78475 -0.523167
3            400000  -65625 -0.328125
4            500000  -89925 -0.359700
5            600000 -113675 -0.378917
6            700000 -145075 -0.414500
7            800000 -147850 -0.369625
8            900000 -174325 -0.387389
9           1000000 -204075 -0.408150

       SIMULATION RESULTS       
-------------------------------
Rounds played: 1000000
Wins: 388180 (38.82%)
Losses: 482508 (48.25%)
Pushes: 84181 (8.42%)
Blackjacks: 45131 (4.51%)

Starting money: $10000000
Final money: $9795925
Profit/Loss: $-204075
ROI: -0.41%

Time elapsed: 7.98 seconds

Simulating 1,000,000 rounds...

       CHECKPOINTS       
-------------------------
   checkpoint_round  profit       roi
0            100000   55283  1.105660
1            200000  103213  1.032130
2            300000   95141  0.634273
3            400000  167965  0.839825
4            500000  186528  0.746112
5            600000  213138  0.710460
6            700000  214833  0.613809
7            800000  264092  0.660230
8            900000  313328  0.696284
9           1000000  344575  0.689150

       SIMULATION RESULTS       
-------------------------------
Rounds played: 1000000
Wins: 388305 (38.83%)
Losses: 482345 (48.23%)
Pushes: 84070 (8.41%)
Blackjacks: 45280 (4.53%)

Starting money: $10000000
Final money: $10344575
Profit/Loss: $344575
ROI: 0.69%

Time elapsed: 8.39 seconds

```
Setup

```
python -m venv .venv

# Windows
.venv\Scripts\activate 

# Mac
source .venv/bin/activate

pip install -r requirements.txt

# Play the terminal version of blackjack
python blackjack_terminal.py

# Run simulation (no card counting)
python blackjack_simulation.py

# Run simulation (card counting)
python blackjack_simulation_card_counting.py
