## 2048 Game Solver

This game solver stores game states in tree structure, and predicts game plies with expectiminimax. To boost the efficiency of the algorithm, alpha-beta pruning is utlized.

Main algorithm is in PlayerAI.py
The rest are helper classes

Test by running GameManager.py

Reach score of at least 1024 60% of the time
Reach score of  at least 2048 40% of the time
Reach score of  at least 4096 20% of the time
