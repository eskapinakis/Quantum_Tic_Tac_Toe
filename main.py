from boards import TicTacToe as SB
import PySimpleGUI as sg

layout = [[sg.Button(' ', key='11', auto_size_button=False, size=(6, 4)),
           sg.Button(' ', key='12', auto_size_button=False, size=(6, 4)),
           sg.Button(' ', key='13', auto_size_button=False, size=(6, 4))],
          [sg.Button(' ', key='21', auto_size_button=False, size=(6, 4)),
           sg.Button(' ', key='22', auto_size_button=False, size=(6, 4)),
           sg.Button(' ', key='23', auto_size_button=False, size=(6, 4))],
          [sg.Button(' ', key='31', auto_size_button=False, size=(6, 4)),
           sg.Button(' ', key='32', auto_size_button=False, size=(6, 4)),
           sg.Button(' ', key='33', auto_size_button=False, size=(6, 4))],
          [sg.Button('', key='v', visible=False), sg.Button('Play again', key='a', visible=False)],
          [sg.Button(' ', key='c1', visible=False),
           sg.Button(' ', key='c2', visible=False)]
          ]

sb = SB.SmallBoard()


def printBoard(board):
    for line in board:
        print(line)


def checkVictory():
    if sb.checkVictory('O'):
        return "Player 2 has won"
    if sb.checkVictory('X'):
        return "Player 1 has won"
    if sb.isFull():
        return "It's a Tie"
    return "banana"


def play(piece):
    while True:
        line = int(input("line: "))
        col = int(input("column: "))
        if line not in [0, 1, 2] or col not in [0, 1, 2]:
            print("That tile has not been built yet")
        elif sb.isOccupied(line, col):
            print("That tile is occupied")
        else:
            sb.play(line, col, piece)
            break


if __name__ == '__main__':

    window = sg.Window('Quantum Tic Tac Toe', default_element_size=(12, 12), margins=(100, 100),
                       font='Any 14').Layout(layout)
    player = 'O'
    game = True
    choosing = False
    index = 0

    while True:

        printBoard(sb.getBoard())

        if index % 2 == 0:  # so each player plays twice
            player = 'X'
        if index % 2 == 1:
            player = 'O'

        event, values = window.Read()

        if event in ('Exit', None):  # if player wants to exit
            break

        # when the player chooses a tile
        if game and not choosing and event not in ['a', 'v'] and \
                len(window[event].get_text()) <= 3 and checkVictory() == "banana":
            sb.play(int(event[0]) - 1, int(event[1]) - 1, player + str(int(index)))
            if window[event].get_text() == ' ':
                window[event].update(text=player + str(int(index)))
            else:
                window[event].update(text=window[event].get_text() + ' ' + player + str(int(index)))
            index += 0.5

            if index % 2 == 0 or index % 2 == 1:  # checks if there is a cycle
                if sb.hasCycle(int(event[0]) - 1, int(event[1]) - 1):
                    choosing = True
                    message = sb.getMessage()
                    window.FindElement('c1').Update(text=message[0])
                    window.FindElement('c1').Update(visible=True)
                    window.FindElement('c2').Update(text=message[1])
                    window.FindElement('c2').Update(visible=True)
                    print(sb.getCycle())
            window.Refresh()

        if event in ['c1', 'c2']:
            choosing = False
            index = 0
            sb.collapseUncertainty(window[event].get_text())  # collapse uncertainty
            for i in range(3):
                for j in range(3):
                    window.FindElement(str(i+1)+str(j+1)).Update(text=sb.getTile(i, j))

            window.FindElement('c1').Update(visible=False)
            window.FindElement('c2').Update(visible=False)

        if checkVictory() != "banana":  # this is to show the 'you win' messages
            game = False
            window.FindElement('v').Update(text=checkVictory())
            window.FindElement('v').Update(visible=True)
            window.FindElement('a').Update(visible=True)

        if not game and event == 'a':  # this is just to reset the game
            game = True
            sb = SB.SmallBoard()
            for i in range(1, 4):
                for j in range(1, 4):
                    window.FindElement(str(i) + str(j)).Update(text=' ')
            window.FindElement('v').Update(visible=False)  # hide victory message
            window.FindElement('a').Update(visible=False)
