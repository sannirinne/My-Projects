#this game was made by Sanni, Nea and Iiris

import copy, random

def empty_board(board): #creating the empty board
    board = []
    row = [] #first row with the numbers
    row.append("  ")
    for i in range(10):
        row.append(str(i+1))
    board.append(row)
    for j in range(9): #rows 2-9
        row = []
        row.append(str(j+1) + " ") #adding a space so that the columns are in line
        for x in range(10):
            row.append("O") #O marks an empty slot on the board
        board.append(row)
    #last row without the space
    board.append(["10","O","O","O","O","O","O","O","O","O","O"])
    return board  
    
def print_board(player, board): #print the board
    #do the changes to a copy, not the original board
    c_board = copy.deepcopy(board)
    if player == "c": #computer's board
        #player can't see the computer's ships
        for i in range(1,11):
            for j in range(1,11):
                if c_board[i][j] == "A" or c_board[i][j] == "B" or c_board[i][j] == "C" or c_board[i][j] == "S" or c_board[i][j] == "D":
                    c_board[i][j] = "O"
        for line in c_board:
            print " ".join(line) #print the slots with spaces in between
    else: #player's board
        for line in board:
            print " ".join(line)

def player_ships(player,board,ships): #player places his/her ships
    for ship in ships.keys():
        ok = False
        while ok != True:
            print "Here's your board", player,"!"
            print_board(player,board)
            print "Place a " + str(ship) + ". Its length is " + str(ships[ship]) + "."
            coor = coordinates() #get the coordinates
            dire = direction() #get the direction
            ok = valid(board,ships[ship],coor[0],coor[1],dire) #validate if the input is correct
            if ok == True:
                #place the ships
                board = place_ship(board,ships[ship],ship[0],dire,coor[0],coor[1])
            else:
                raw_input("Invalid coordinates. Press enter to try again.")
    print_board(player,board)
    raw_input("Your board is ready! Press enter to continue!")
    return board

def computer_ships(board,ships): #computer places ships
    for ship in ships.keys():
        ok = False
        while ok != True:
            #get random coordinates
            r = random.randint(1,10) #row number
            c = random.randint(1,10) #column number
            d = random.randint(0,1) #direction
            if d == 0:
                dire = "h"
            else:
                dire = "v"
            ok = valid(board,ships[ship],r,c,dire) #validate
            if ok == True:
                #place the ships
                board = place_ship(board,ships[ship],ship[0],dire,r,c)
    return board
        
def coordinates(): #get the coordinates from the user
    x = True
    while x == True:
        coor = raw_input("Enter your coordinates here (row, column): ")
        try:
            coor = coor.split(",")
            if len(coor) != 2: #length must be 2
                print "Invalid coordinates. Input exactly two values please."
            else:
                #turn the coordinates into integers
                coor[0] = int(coor[0])
                coor[1] = int(coor[1])
                #see if the range is correct
                if coor[0] < 1 or coor[0] > 10 or coor[1] < 1 or coor[1] > 10:
                    print "Invalid coordinates. Coordinates must be integers between 1 and 10."
                else:
                    x = False
        #if something above is not correct, give a value error
        except ValueError:
            print "Invalid coordinates. Coordinates must be integers between 1 and 10 (e.g. 2,2)."
    return coor

def direction(): #direction of the ship
    dire = raw_input("Give a direction (v = vertical, h = horizontal): ")
    #define which direction the user wants
    if dire == "v" or "V":
        dire == "v"
        return dire
    elif dire == "h" or "H":
        dire == "h"
        return dire
    #incase of wrong input
    else:
        "Invalid input. Please enter v or h."

def valid(board,ship,r,c,dire): #validate the input
    #horizontal ship can't be placed over the right edge
    if dire == "h":
        if ship + c > 11:
            return False
        #it also can't go to a taken slot
        for i in range(ship):
            if board[r][c+i] != "O":
                return False
        else:
            return True
    #vertical ship can't be placed over the bottom of the board
    if dire == "v":
        if ship + r > 11:
            return False
        #it also can't go to a taken slot
        for i in range(ship):
            if board[r+i][c] != "O":
                return False
        else:
            return True
	    

def place_ship(board,ship,letter,dire,r,c): #place a ship on the board
    if dire == "h":
        for i in range(ship):
            board[r][c+i] = letter #mark the ship with the first letter of said ship
    elif dire == "v":
        for i in range(ship):
            board[r+i][c] = letter
    return board

def move_user(board): #user makes a move on computer's board
    shot = "try again"
    while shot != "miss":
        print_board("c",board)
        coor = coordinates()
        r = coor[0]
        c = coor[1]
        shot = move(board,r,c) #defining where the move hits
        if shot == "miss":
            raw_input("Sorry, it's a miss. Press enter to continue.")
            board[r][c] = "#" #hashtag marks a shot that missed
        elif shot == "hit":
            s = sink(board,r,c) #if the shot is a hit, see if the ship sunk
            board[r][c] = "X" #X marks a hit
            if s == 1: #if the ship sunk, see if the player won
                var = win(board)
                if var == True:
                    board[0][0] = "W" #if the user won, mark the first slot with a W
                    break
            else:
                raw_input("It's a hit. You get a new turn. Press enter to continue.")
        else:
            raw_input("Sorry, you already tried that. Press enter to try again.")
    return board

def move_computer(board): #computer makes a move
    shot = "try again"
    while shot != "miss":
        #get random coordinates
        r = random.randint(1,10)
        c = random.randint(1,10)
        shot = move(board,r,c) #defining where the move hits
        if shot == "miss":
            board[r][c] = "#"
            print_board(player,board)
            raw_input("Computer missed! It's your turn.")
        elif shot == "hit":
            s = sink(board,r,c) #if the shot is a hit, see if the ship sunk
            board[r][c] = "X"
            if s == 1:
                var = win(board)
                if var == True:
                    board[0][0] = "W" #if the computer won, mark the first slot with a W
                    break
            print_board(player,board)
            raw_input("Computer hit your ship! It gets another try.")
        elif shot == "try again":
            continue
    return board

def move(board,r,c): #define where the move hits
    if board[r][c] == "O":
        return "miss"
    elif board[r][c] == "#" or board[r][c] == "X":
        return "try again"
    else:
        return "hit"

def sink(board,r,c): #see if the ship sunk
    #define which ship was hit
    if board[r][c] == "A":
        ship = "Aircraft Carrier"
    elif board[r][c] == "B":
        ship = "Battleship"
    elif board[r][c] == "C":
        ship = "Cruiser"
    elif board[r][c] == "S":
        ship = "Submarine"
    elif board[r][c] == "D":
        ship = "Destroyer"
    #go through the board to see if there is that ship left
    x = 0
    for line in board:
        for slot in line:
            if slot == ship[0]:
                x = x + 1
    if x == 1:
        print ship + " sunk." #print which ship sunk
        return x
            
        
def win(board): #check if the player won
    #go through the board to see if there is any ships left
    for i in range(1,11):
        for j in range(1,11):
            if board[i][j] == "A" or board[i][j] == "B" or board[i][j] == "C" or board[i][j] == "S" or board[i][j] == "D":
                return False
    return True

def moves(board): #count the user's moves for the high score list
    a = 0
    for i in range(1,11):
        for j in range(1,11):
            if board[i][j] == "#" or board[i][j] == "X": #for every move there's either a # or an X on the board
                a = a + 1
    return a

def print_highScores(): #printing the top-10 high score list from the file
    f = open("highscores.txt", "r")
    for i in range(10):
        score = f.readline() #get ten lines from the file
        score = score.strip("\n") #get rid of the \n
        if score != "":
            print score
    f.close()

def write_highScore(player, moves):
    #first get the previous list from the file
    f = open("highscores.txt", "r")
    p = [player,moves] #player of this game
    scores = []
    for i in range(10):
        score = f.readline()
        score = score.strip("\n")
        score = score.split(",") #a list with the name and the number of moves as strings
        #number of moves has to be made an integer to be able to sort the list
        score[1] = int(score[1])
        scores.append(score) #create a list of lists
    f.close()
    scores.append(p) #add the current player to the list
    scores_sorted = sorted(scores, key=lambda x: x[1]) #sort the list
    f2 = open("highscores.txt", "w")
    #write the new top-10 back to the file
    for j in range(10):
        x = ""
        for s in range(2):
            x += str(scores_sorted[j][s]) #has to be as a string
            #add a comma only to the middle, not to the end of the line
            if s != 1:
                x += ","
        x += "\n"
        f2.write(x) #write the string to the file
    f2.close()

#main game
#ships in a dictionary; key is the ship and the value the length of the ship
ships = {"Aircraft Carrier":5,"Battleship":4,"Cruiser":3,"Submarine":3,"Destroyer":2} #ships ad a dictionary
raw_input("Let's play Battleship! Press enter to continue.")
print "Here's the current high score list:"
print_highScores()
player = raw_input("Choose a name: ")
raw_input("Great! Press enter to place your ships!")
#create empty boards for the player and the computer
board = []
board_p = empty_board(board)
board_c = empty_board(board)
#place the ships for both
board_p = player_ships(player,board_p,ships)
board_c = computer_ships(board_c,ships)
#making the moves
main = True
while main == True:
    board_c = move_user(board_c) #user makes the moves on the computer's board
    if board_c[0][0] == "W": #if there's a W, user won
        raw_input("YOU ARE THE WINNER! :) Press enter to see the high score list!")
        m = moves(board_c) #count the moves the user has made
        write_highScore(player,m) #write the current user to the high score list
        print_highScores() #print the current top-10
        break
    board_p = move_computer(board_p) #computer makes the moves on player's board
    if board_c[0][0] == "W": #if there's a W, computer won
        print "Computer won! Better luck next time!"
        break

    
            
