# -*- coding: utf-8 -*-
import numpy as np
import random
board = None 
winner = None # save winner of the match
stillrunning = None # variable of the game state
counter = None # handle player turns

def display_board():
  print(str(board[0]) + " | " + str(board[1]) + " | " + str(board[2]))
  print(str(board[3]) + " | " + str(board[4]) + " | " + str(board[5]))
  print(str(board[6]) + " | " + str(board[7]) + " | " + str(board[8]))

# displays the current board state then asks the player with position he wants to mark and sets the mark,if all conditions are met
def player():
  display_board()
  global counter
  while True: # https://docs.python.org/3/tutorial/errors.html
    try:
      position = int(input("Please enter a number between 0 and 8: "))
      break
    except ValueError:
      print("Oops! That was no valid number. Try again...")
  if position >= 0 and position < 9:
    if board[position] != "O" and board[position] != "X":
      board[position] = "X"
      counter += 1
    else:
      print("You can't place your mark there.")
  else:
    print("Wrong Input, please enter a number between 0 and 8.")

# got the initial idee of how to build the computer AI from https://techwithtim.net/tutorials/python-programming/tic-tac-toe-tutorial/
# first checks the current state of the game and if a player can win in the next turn in a copy of the board
# if thats the case,either blocks the move for the opponent or place the winning mark on the actual board
# otherwise choeses a random open spot
# Priority: Corner = Mid > Edge 
def computer():
   cornerspot = [] # list for corner spots on the board
   edgespot = [] # list for edge spots on the board
   global counter
   possiblemove = np.logical_and(board != "X", board != "O")
   new_board = board.copy()
   for i in new_board[possiblemove]:
     move = i
     new_board[move] = "O"
     if check_for_winner(new_board):
        board[move] = "O"
        counter += 1
        return 
     new_board[move] = move
   for i in new_board[possiblemove]:
     move = i
     new_board[move] = "X"
     if check_for_winner(new_board):
        board[move] = "O"
        counter += 1
        return 
     new_board[move] = move
   else:
    for i in board[possiblemove]:
      if i in [0, 2, 6, 8, 4]:
        cornerspot.append(i) # if a cornerspot is available, add it to the cornerspotlist
        
      elif i in [1, 3, 5, 7]:
        edgespot.append(i) # if a edgespot is available, add it to the edgespotlist
        
    if len(cornerspot)  > 0: # check if cornersspotlist have a entry and if thats the case,chose a random postion in the following line
      move = random.choice(cornerspot)
    elif len(edgespot) > 0: # check if edgespotlist have a entry and if thats the case,chose a random postion in the following line
      move = random.choice(edgespot)

    board[move] = "O" 
    counter += 1

# announce the winner and change the game state
def whowon():
 global stillrunning
 global winner
 winner = check_for_winner(board)
 if winner == "X":
   stillrunning = False
   print("Congratulations! You won.")
   display_board()
 elif winner == "O":
   print("You lost.")
   stillrunning = False
   display_board()
 
# checks for winner, compares possible winning combinations and if one is True, return the first entry of the winning combination to get which Player ("X" or "O") won
# if there is still no winner, return None
def check_for_winner(board):
#define winning combinations
 row1 = board[0] == board[1] == board[2]
 row2 = board[3] == board[4] == board[5]
 row3 = board[6] == board[7] == board[8]
 col1 = board[0] == board[3] == board[6]
 col2 = board[1] == board[4] == board[7]
 col3 = board[2] == board[5] == board[8]
 diag1 = board[0] == board[4] == board[8]
 diag2 = board[2] == board[4] == board[6]

 if row1 or row2 or row3 or col1 or col2 or col3 or diag1 or diag2:
  if row1:
    return board[0]
  elif row2:
    return board[3]
  elif row3:
    return board[6]
  elif col1:
    return board[0]
  elif col2:
    return board[1]
  elif col3:
    return board[2]
  elif diag1:
    return board[0]  
  elif diag2:
    return board[6]     
  else:
    return None  
 
 
#cheks if all entrys in the board array is full with marks.If thats the case, change the state of the game to a Tie Game
def boardfull():
  global winner
  global stillrunning
  full = all(i == "X" or i == "O" for i in board) # https://docs.scipy.org/doc/numpy/reference/generated/numpy.any.html
  if full and winner == None:
    print("Tie Game.")
    stillrunning = False
    winner = "Tie" #just to exit the while loop in our main function if we have a tie game
    
# if the game is done,ask the player if he wants to play again or not
# if player wants to restart the game,change the game state again
def rematch ():
 global stillrunning
 global winner
 global counter
 if stillrunning == False:
  while True:
   restart = input("Want to restart the game? Enter yes or no: ")
   if restart == "yes":
     stillrunning = True
     winner = None 
     counter = 0
     start_game()
     break
   elif restart == "no":
     print("Thank your for playing. See you later.")
     break
   else:
     print("Sorry, wrong input. Try again.")

# starts playing
def start_game():
  global winner
  global stillrunning
  global counter
  global board
  board = np.array(range(9)).astype("object") # creates a numpy array of range 9 and convert it to a object for better interpretation
  winner = None 
  stillrunning = True 
  counter = 0 
  print("Welcome to Tic Tac Toe!")
  print("You are X and the opponent O.")
  print("Have fun and good luck!")
  # checks if the condition for still playing are fulfilled and if there is a winner
  # Also handle the turn of the players.Even numbers are Player1,odd Player2
  while stillrunning: 
    while winner == None:  
      if counter % 2 == 0:  
        player()
        whowon()
      
      elif counter % 2 != 0:
        computer()
        whowon()
      boardfull()    
    rematch()


start_game()
