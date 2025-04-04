import random

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