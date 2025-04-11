import random

import unittest
from unittest.mock import patch

class TestGetRPS(unittest.TestCase):
    def test_getRPS_returns_valid_choices(self):
        for _ in range(100):
            self.assertIn(getRPS(), ['rock', 'paper', 'scissors'])

if __name__ == '__main__':
    unittest.main()

def getRPS():
    choice = random.choice(["rock", "paper", "scissors"])
    return choice

# def decide_winner(cpu: str, player: str):
#     outcome: str = ""
#     if(cpu == "rock"):
#         if (player == "rock"):
#             outcome = "draw"
#         elif (player == "scissors"):
#             outcome = "lose"
#         elif (player == "paper"):
#             outcome = "win"
#     elif(cpu == "paper"):
#         if (player == "rock"):
#             outcome = "lose"
#         elif (player == "scissors"):
#             outcome = "win"
#         elif (player == "paper"):
#             outcome = "draw"
#     elif(cpu == "scissors"):
#         if (player == "rock"):
#             outcome = "win"
#         elif (player == "scissors"):
#             outcome = "draw"
#         elif (player == "paper"):
#             outcome = "lose" 

#     return outcome