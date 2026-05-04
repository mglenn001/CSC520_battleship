# CSC520_battleship
Project: Battleship<br>
Course: CSC 520<br>
Group 4<br>
Team Members: Bhavana Chappidi (bchappi) and Mia Glenn (mglenn2)

**Project Description**

This project explores how different AI techniques perform at playing Battleship, a classic strategy game where a player must locate and sink hidden ships on a 10x10 grid using only hit, miss, or sunk feedback. Since the agent cannot see the opponent's board, this is a problem of search under uncertainty in a partially observable environment. We implement and compare three agents of increasing intelligence: a random baseline, a local search agent using hill climbing, and a CSP-based agent that uses constraint propagation and probability scoring to identify the most likely ship locations. Each agent is evaluated over 500 simulated games, tracking average shots to win, best and worst games, and standard deviation.

**How to Run:**
* Python version is Python 3
* How to clone: git clone [repo-url]
* How to run: python main.py

**File Structure**
* main.py - entry point, runs the experiment
* game.py - game engine and stats collection
* board.py - board logic and ship placement
* random_agent.py - Agent 1: random baseline
* hill_climbing_agent.py: Agent 2: local search
* csp_agent.py - Agent 3: CSP + informed search

**Figure**: Sample game boards showing the final shot patterns for each agent. The CSP Agent (left) finishes in just 42 shots with a focused, clustered pattern, while the Hill Climbing Agent (middle, 95 shots) and Random Agent (right, 97 shots) show much more scattered coverage of the board.
<img width="565" height="277" alt="agents" src="https://github.com/user-attachments/assets/2df87d86-e0ec-4288-aa5a-198aea130434" />

**Table**: Performance comparison of the three agents over 500 simulated games. The CSP + Informed Search Agent achieves the lowest average shots to win (64.80), outperforming both the Hill Climbing Agent (80.90) and the Random baseline (95.44).
<img width="633" height="199" alt="experiments" src="https://github.com/user-attachments/assets/793a2af5-9b05-4158-abb5-1794ebbfa7d6" />

Final Presentation Slides: https://docs.google.com/presentation/d/1qCk_C0ll_yHSFDrgnJhlNew5QD_iw3L6kfU9N1hCtQc/edit?usp=sharing 

