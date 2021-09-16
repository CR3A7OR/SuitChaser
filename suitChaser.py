#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  - Download more projects at: https://github.com/CR3A7OR - #
import random
import time
import curses 
from curses import wrapper
import textwrap
import sys

# ------ Variables-----#

screen = curses.initscr()
odds = []
suits = ['♥','♦','♠','♣']
menu = ['Play', 'Rules', 'Exit']
bet = []
winner = ""


text = r"""
   _____ __  ____________   ________  _____   _____ __________
  / ___// / / /  _/_  __/  / ____/ / / /   | / ___// ____/ __ \
  \__ \/ / / // /  / /    / /   / /_/ / /| | \__ \/ __/ / /_/ /
 ___/ / /_/ // /  / /    / /___/ __  / ___ |___/ / /___/ _  _/ 
/____/\____/___/ /_/     \____/_/ /_/_/  |_/____/_____/_/ |_|  """

definition = r"""
Suit Chaser is like betting on the horses but          ♥ - 21/1  
here you are betting on which suit will cross          ♦ - 13/1
the line first and win the race.                       ♠ - 6/1
                                                       ♣ - 2/1
Each suit is generated a standard fraction odd 
and you can place a bet on your winning suit.
Once bets have been made the race begins with the cards proceeding forward 
each time a card of the matching suit is shown in the bottom right deck

┌──────┐     To add further risk to the game during the race you
│░░░░░░│     can press the "up arrow key" to flip a hidden card.
│░░░░░░│     These 4 hidden cards are randomly selected at the start
│░░░░░░│     and when flipped will set back the suit is holds by one,
└──────┘     Use wisely since you may end up setting your own suit back

The grid is a 5x5 grid with the aces playing as the
horses. The first ace to make it 5 spaces up wins the
race and movement is based on a random card generated 
in the bottom right acting as the 52 standard deck. 
The house minimum is a bet of 2 and when starting you 
have 100 which can be found in balance.txt. Standard 
fraction betting rules apply and you only lose how 
much you put in when you bet."""

# ------ Variables-----#


# ------ MAIN FUNCTIONS -----#

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def print_odds(stdscr, selected_row_idx):
    stdscr.refresh()
    h, w = stdscr.getmaxyx()
    printer = []
    for array in odds:
        printer.append(array[0] + " - " + str(array[1]))

    for idx, row in enumerate(printer):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx + 5
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def title(stdscr):
    screen.border(0)
    dims3 = screen.getmaxyx()
    for y, line in enumerate(text.splitlines(), 1):
        stdscr.addstr(y, int(int(dims3[1])/2-1 - 30),line)
    stdscr.refresh()

def makeBets():
    dims4 = screen.getmaxyx()
    bet_list = list(range(2, 22))
    num = 19
    t = int(int(dims4[0])/2-1)
    t += 5
    odds.clear()
    for suit in suits:
        odd = []
        temp = random.randint(2, num)
        odd.append(suit)
        odd.append(str(bet_list[temp]) + "/1")
        odds.append(odd)
        del bet_list[temp]
        t += 1
        num -= 1

def my_raw_input(stdscr, r, c, prompt_string):
    title(stdscr)
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.addstr(r + 1, c, ">  _______")
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c + 3, 20)
        
    return input   

def fake_card():
    value = str(random.randint(2,9))
    CARD = """
┌────────┐
│{}      │
│        │
│   {}   │
│        │
│      {}│
└────────┘""".format(value + ' ' , suits[random.randint(0,3)] + ' ', value + ' ')
    return CARD

def create_card(v, s):
    if s == 'H':
        s = "♥"
    elif s == "D":
        s = "♦"
    elif s == "S":
        s = "♠"
    elif s == "C":
        s = "♣"

    CARD = """\
┌──────┐
│{}    │
│  {}  │
│    {}│
└──────┘""".format(v + ' ' , s + ' ', v + ' ').split("\n")
    return CARD

BLANK_CARD = """\
┌──────┐
│      │
│      │
│      │
└──────┘""".split("\n")

HIDDEN_CARD = """\
┌──────┐
│░░░░░░│
│░░░░░░│
│░░░░░░│
└──────┘""".split("\n")

def print_cards(grid):
    screen.clear()
    screen.border(0)
    dims2 = screen.getmaxyx()
    y = 5
    for x in range(len(grid)):
        y += 5
        y2 = y
        try:
            for row in zip(grid[x][0], grid[x][1], grid[x][2], grid[x][3], grid[x][4]):
                screen.addstr(y2, int(int(dims2[1])/2-1 - 21),row[0] + " " + row[1] + " " + row[2] + " " + row[3] + " " + row[4])
                y2 += 1
        except Exception:
            screen.clear()
            print_center(screen,"PLEASE INCREASE SIZE OF TERMINAL")
        screen.refresh()
    for y, line in enumerate(text.splitlines(), 1):
        screen.addstr(y, int(int(dims2[1])/2-1 - 30),line)

def card_checker(card):
    value = ""
    suit = ""
    if card.value == 11:
        value = "J"
    elif card.value == 12:
        value = "Q"
    elif card.value == 13:
        value = "K"
    elif card.value == 10:
        value = "⑩"
    else:
        value = card.value

    if card.color == "heart":
        suit = 'H'
    elif card.color == "diamonds":
        suit = 'D'
    elif card.color == "spades":
        suit = 'S'
    elif card.color == "clubs":
        suit = 'C'        

    return value, suit

def flip(card, fc, heart, diamond, spade, club, grid):
    test = card_checker(card)
    grid[fc][4] = create_card(str(test[0]), str(test[1]))
    if test[1] == "H" and heart != 0:
        grid[4 - heart][0] = BLANK_CARD
        heart -= 1
        grid[4 - heart][0] = create_card("A","H")
    elif test[1] == "D" and diamond != 0:
        grid[4 - diamond][1] = BLANK_CARD
        diamond -= 1
        grid[4 - diamond][1] = create_card("A","D")
    elif test[1] == "S" and spade != 0:
        grid[4 - spade][2] = BLANK_CARD
        spade -= 1
        grid[4 - spade][2] = create_card("A","S")
    elif test[1] == "C" and club != 0:
        grid[4 - club][3] = BLANK_CARD
        club -= 1
        grid[4 - club][3] = create_card("A","C")

    return heart, diamond, spade, club

# ------ MAIN FUNCTIONS -----#


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color


# ------ MAIN GAME LOGIC -----#

f = open("balance", "r")
lines=f.readlines()

def main(stdscr):
    progress = False
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0
    print_menu(stdscr, current_row)
    while 1:
        value = lines[1].replace('Balance: ',"")
        value = value.strip()
        bet = []

        dims4 = stdscr.getmaxyx()
        title(stdscr)
        stdscr.addstr(2,2,lines[1].strip())

        key0 = stdscr.getch()
        if key0 == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key0 == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
        elif key0 == curses.KEY_ENTER or key0 in [10, 13]:
            if current_row == len(menu)-1:
                quit()

            elif current_row == len(menu)-2:
                    stdscr.clear()
                    box1 = curses.newwin(27, 80, int(int(dims4[0])/2-1) - 10, int(int(dims4[1])/2-1) - 38)
                    box1.box()
                    title(stdscr)
                    for y, line in enumerate(definition.splitlines(), 1):
                        box1.addstr(y, 2,line)
                    for y, line in enumerate(fake_card().splitlines(), 1):
                        box1.addstr(y + 15, 60,line)
                    box1.refresh()
                    stdscr.refresh()
                    stdscr.getch()

            elif current_row == len(menu)-3:
                stdscr.clear()
                stdscr.border(0)
                try:
                    makeBets()
                    print_odds(stdscr, current_row)
                    choice = int(my_raw_input(stdscr, int(int(dims4[0])/2-1), int(int(dims4[1])/2-1 - 5), "MAKE A BET"))
                    if int(value) == 0:
                        choice = 0
                    elif choice > int(value):
                        choice = value
                    elif choice <= 1:
                        choice = 2

                    bet.append(choice)
                    stdscr.addstr(int(int(dims4[0])/2-1 + 3), int(int(dims4[1])/2-1 - 5), "PICK A SUIT")
                    
                    curses.curs_set(0)
                    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
                    current_row2 = 0

                    print_odds(stdscr, current_row2)

                    while 1:
                        title(stdscr)
                        key0 = stdscr.getch()
                        if key0 == curses.KEY_UP and current_row2 > 0:
                            current_row2 -= 1
                        elif key0 == curses.KEY_DOWN and current_row2 < len(suits)-1:
                            current_row2 += 1
                        elif key0 == curses.KEY_ENTER or key0 in [10, 13]:
                            if current_row2 == len(suits)-1:
                                bet.append(odds[len(suits)-1][0])
                                bet.append(odds[len(suits)-1][1])
                            elif current_row2 == len(suits)-2:
                                bet.append(odds[len(suits)-2][0])
                                bet.append(odds[len(suits)-2][1])
                            elif current_row2 == len(suits)-3:
                                bet.append(odds[len(suits)-3][0])
                                bet.append(odds[len(suits)-3][1])
                            elif current_row2 == len(suits)-4:
                                bet.append(odds[len(suits)-4][0])
                                bet.append(odds[len(suits)-4][1])
                            progress = True
                            break
                        
                        print_odds(stdscr, current_row2)

                except ValueError:
                    print_center(stdscr, "INVALID BET PLACED")
                
                stdscr.refresh()
                curses.napms(500)

                if progress == True:
                    #Initialise screen
                    curses.initscr()
                    curses.noecho()
                    curses.cbreak()

                    stdscr.border(0)
                    stdscr.refresh()
                    stdscr.keypad(1)

                    colors = ['heart', 'diamonds', 'spades', 'clubs']
                    deck = [Card(value, color) for value in range(1, 13) for color in colors]

                    #Generate grid to display
                    w, h = 5, 5;
                    grid = [[BLANK_CARD for x in range(w)] for y in range(h)]

                    grid[4][0] = create_card("A","H")
                    grid[4][1] = create_card("A","D")
                    grid[4][2] = create_card("A","S")
                    grid[4][3] = create_card("A","C")

                    grid[0][4] = HIDDEN_CARD
                    grid[1][4] = HIDDEN_CARD
                    grid[2][4] = HIDDEN_CARD
                    grid[3][4] = HIDDEN_CARD
                    print_cards(grid)

                    #Pick 4 random cards to be hidden
                    j = 0
                    hidden = [ ]
                    x = 47
                    while j < 4:
                        temp = random.randint(0,x)
                        hidden.append(deck[temp])
                        del deck[temp]
                        j += 1
                        x -= 1

                    #43 random cards left
                    x = 42
                    numsec = 1000
                    fc = 3
                    heart, diamond, spade, club = 0,0,0,0

                    title(stdscr)
                    stdscr.refresh()
                    while x > 0:
                        dims = stdscr.getmaxyx()
                        curses.napms(numsec)
                        temp = random.randint(0,x)
                        test = card_checker(deck[temp])
                        grid[4][4] = create_card(str(test[0]), str(test[1]))   
                        if deck[temp].color == "heart":
                                grid[4 - heart][0] = BLANK_CARD
                                heart += 1
                                grid[4 - heart][0] = create_card("A","H")
                                print_cards(grid)
                                if heart == 5:
                                    stdscr.clear()
                                    title(stdscr)
                                    print_center(stdscr, "HEART WINS")
                                    winner = suits[0]
                                    stdscr.refresh()
                                    break
                                
                        elif deck[temp].color == "diamonds":
                                grid[4 - diamond][1] = BLANK_CARD
                                diamond += 1
                                grid[4 - diamond][1] = create_card("A","D")
                                print_cards(grid)
                                if diamond == 5:
                                    stdscr.clear()
                                    title(stdscr)
                                    print_center(stdscr, "DIAMOND WINS")
                                    winner = suits[1]
                                    stdscr.refresh()
                                    break
                                
                        elif deck[temp].color == "spades":
                                grid[4 - spade][2] = BLANK_CARD
                                spade += 1
                                grid[4 - spade][2] = create_card("A","S")
                                print_cards(grid)        
                                if spade == 5:
                                    stdscr.clear()
                                    title(stdscr)
                                    print_center(stdscr, "SPADE WINS")
                                    winner = suits[2]
                                    stdscr.refresh()
                                    break
                                
                        elif deck[temp].color == "clubs":
                                grid[4 - club][3] = BLANK_CARD
                                club += 1
                                grid[4 - club][3] = create_card("A","C")
                                print_cards(grid)  
                                if club == 5:
                                    stdscr.clear()
                                    title(stdscr)
                                    print_center(stdscr, "CLUB WINS")
                                    winner = suits[3]
                                    stdscr.refresh()
                                    break
                                
                        del deck[temp]
                        x -= 1

                        stdscr.nodelay(True)

                        key0 = stdscr.getch()
                        if key0 == curses.KEY_UP and len(hidden) != 0:
                            heart, diamond, spade, club = flip(hidden[0], fc, heart, diamond, spade, club, grid)
                            print_cards(grid)
                            del hidden[0]
                            fc -= 1
                        stdscr.refresh()

                    stdscr.nodelay(False)
                    if bet[1] == winner:
                        win_odd = int((bet[2].replace('/1','').strip())) * bet[0]
                        bal = int(value) + win_odd
                        stdscr.addstr(int(int(dims[0])/2-1) + 4,int(int(dims[1])/2-1) - 2,"WINNER")
                        stdscr.addstr(int(int(dims[0])/2-1) + 6,int(int(dims[1])/2-1) - 2,"Payout:" + str(win_odd))
                        stdscr.refresh()
                        lines[1] = "Balance: " + str(bal)
                        with open('balance', 'w') as file:
                            file.writelines(lines)    
                    else:
                        bal = int(value) - int(bet[0])
                        stdscr.addstr(int(int(dims[0])/2-1) + 4,int(int(dims[1])/2-1),"LOSER")
                        stdscr.addstr(int(int(dims[0])/2-1) + 6,int(int(dims[1])/2-1),"Loss:" + str(bet[0]))
                        stdscr.refresh()
                        lines[1] = "Balance: " + str(bal)
                        with open('balance', 'w') as file:
                            file.writelines(lines)
                    
                    curses.napms(3000)
                    progress = False
                    winner = ""
                
        print_menu(stdscr, current_row)

# ------ MAIN GAME LOGIC-----#

curses.wrapper(main)
