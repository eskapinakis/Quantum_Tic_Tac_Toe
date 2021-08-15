from boards import RegularTicTacToe as R, QuantumTicTacToe as Q
import PySimpleGUI as sg

# from ai import SimpleAlgorithm as SA  # To use the simple algorithm
from ai import MiniMax as SA  # To use the minimax algorithm


def makeLayout(is_quantum=False, two_players=False):

    if is_quantum:
        return [[sg.Button('Quantum', key='quantum', auto_size_button=False, size=(8, 4)),
                 sg.Button('Regular', key='regular', auto_size_button=False, size=(7, 4))]
                ]
    if two_players:
        return [[sg.Button('Two Players', key='two', auto_size_button=False, size=(7, 4)),
                 sg.Button('Against Computer', key='one', auto_size_button=False, size=(8, 4))]
                ]

    if quantum:
        return [[sg.Button('', key='11', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='12', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='13', auto_size_button=False, size=(6, 4))],
                [sg.Button('', key='21', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='22', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='23', auto_size_button=False, size=(6, 4))],
                [sg.Button('', key='31', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='32', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='33', auto_size_button=False, size=(6, 4))],
                [sg.Button('', key='v', visible=False), sg.Button('Play again', key='a', visible=False)],
                [sg.Button('', key='c1', auto_size_button=False, size=(3, 2)),
                 sg.Button('', key='c2', auto_size_button=False, size=(3, 2))]
                ]
    else:
        return [[sg.Button('', key='11', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='12', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='13', auto_size_button=False, size=(6, 4))],
                [sg.Button('', key='21', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='22', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='23', auto_size_button=False, size=(6, 4))],
                [sg.Button('', key='31', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='32', auto_size_button=False, size=(6, 4)),
                 sg.Button('', key='33', auto_size_button=False, size=(6, 4))],
                [sg.Button('', key='v', visible=False), sg.Button('Play again', key='a', visible=False)]
                ]


rb = R.RegularTicTacToe()  # regular board
qb = Q.QuantumTicTacToe()  # quantum board


def menu():

    isQuantum = False
    isComputer = False

    menuWindow = sg.Window('Menu', default_element_size=(12, 12), margins=(70, 50),
                           size=(400, 510), font='Any 14').Layout(makeLayout(True))
    event1, values1 = menuWindow.Read()
    menuWindow.close()

    if event1 == 'quantum':
        isQuantum = True

    menuWindow = sg.Window('Menu', default_element_size=(12, 12), margins=(70, 50),
                           size=(400, 510), font='Any 14').Layout(makeLayout(False, True))
    event1, values1 = menuWindow.Read()

    if event1 == 'one':
        isComputer = True

    menuWindow.close()

    return [isQuantum, isComputer]


if __name__ == '__main__':

    player = 'O'
    game = True
    choosing = False
    first = True
    index = 0
    line = 0
    col = 0
    window = None

    quantum = True  # make it true or false if tic tac toe is supposed to be quantum or not
    computer = True  # make it true or false to play against computer or not
    computerFirst = False  # make it true or false for the computer to play first

    choice = menu()
    quantum = choice[0]
    computer = choice[1]

    window = sg.Window('Quantum Tic Tac Toe', default_element_size=(12, 12), margins=(70, 50),
                       size=(400, 510), font='Any 14').Layout(makeLayout())

    if computerFirst:
        window.Finalize()

    while True:

        # print('Main Board')
        # printBoard(qb.getBoard())
        # print(sb.isFull())
        # printBoard(sb.getCounters())
        # print('col: ', sb.getWinCol())
        # print('line: ', sb.getWinLine())
        # print(index)

        event = "Banana"  # This is just to not have a yellow warning

        if computerFirst:  # To define the first player
            remainder = 1
        else:
            remainder = 0

        # only ask for user input when it's the player's turn
        if not computer or not game or choosing:
            event, values = window.Read()
        elif int(index) % 2 == remainder or choosing:
            event, values = window.Read()

        if int(index) % 2 == 0:  # alternate between X and O
            player = 'X'
        if int(index) % 2 == 1:
            player = 'O'

        if event in ('Exit', None):  # if player wants to exit
            break

        # Quantum Tic Tac Toe

        if quantum:

            # when the player chooses a tile
            if (int(index) % 2 == remainder and computer) or not computer:
                if game and not choosing and event not in ['a', 'v', 'c1', 'c2'] and \
                        len(window[event].get_text()) <= 3 and qb.getWinner() == "banana" and \
                        len(window[event].get_text()) != 1:

                    line = int(event[0]) - 1
                    col = int(event[1]) - 1

                    qb.play(line, col, player + str(int(index)))
                    if window[event].get_text() == '':
                        window[event].update(text=player + str(int(index)))
                    else:
                        window[event].update(text=window[event].get_text() + ' ' +
                                                  player + str(int(index)))
                    index += 0.5

            # if second player is the computer
            elif computer and game and int(index) % 2 == 1 - remainder and \
                    not choosing and qb.getWinner() == "banana":

                # sa = SA.SimpleAlgorithm(sb, player)  # initialize the simple opponent
                sa = SA.Minimax(qb, player, True, int(index))  # initialize the minimax opponent

                coord = sa.getMove()

                if first:
                    line = coord[0][0]
                    col = coord[0][1]
                    first = False
                else:
                    line = coord[1][0]
                    col = coord[1][1]
                    first = True
                qb.play(line, col, player + str(int(index)))
                # Update the first move
                name = str(line + 1) + str(col + 1)
                text = window.FindElement(name).get_text()
                if text == '':
                    window.FindElement(name).update(text=player + str(int(index)))
                else:
                    window.FindElement(name).update(text=text + ' ' + player + str(int(index)))
                index += 0.5

            if index % 2 == 0 or index % 2 == 1:  # checks if there is a cycle

                if qb.sameSymbol(line, col):
                    name = str(line + 1) + str(col + 1)
                    window.FindElement(name).update(text=qb.getTile(line, col))

                if qb.hasCycle(line, col):
                    choosing = True
                    message = qb.getMessage()
                    window.FindElement('c1').Update(text=message[0])
                    window.FindElement('c2').Update(text=message[1])

            if choosing and event in ['c1', 'c2']:
                choosing = False
                qb.collapseUncertainty(window[event].get_text())  # collapse uncertainty
                for i in range(3):
                    for j in range(3):
                        window.FindElement(str(i + 1) + str(j + 1)).Update(text=qb.getTile(i, j))

                window.FindElement('c1').Update(text='')
                window.FindElement('c2').Update(text='')

            if not choosing and qb.getWinner() != "banana":  # this is to show the 'you win' messages
                game = False
                window.FindElement('v').Update(text=qb.getWinner())
                window.FindElement('v').Update(visible=True)
                window.FindElement('a').Update(visible=True)
                index = 0

            if not game and event == 'a':  # this is just to reset the game
                game = True
                qb = Q.QuantumTicTacToe()
                window.close()

                choice = menu()
                quantum = choice[0]
                computer = choice[1]

                window = sg.Window('Quantum Tic Tac Toe',
                                   default_element_size=(12, 12), margins=(70, 50), size=(400, 510),
                                   font='Any 14').Layout(makeLayout())
                window.Finalize()
                computerFirst = computerFirst is False

        # Regular Tic Tac Toe

        if not quantum:

            # when the player chooses a tile
            if (index % 2 == remainder and computer) or not computer:
                if game and event not in ['a', 'v', 'c1', 'c2'] and \
                        rb.getWinner() == "banana" and len(window[event].get_text()) != 1:

                    line = int(event[0]) - 1
                    col = int(event[1]) - 1

                    rb.play(line, col, player)
                    if window[event].get_text() == '':
                        window[event].update(text=player)
                    index += 1

            # if second player is the computer
            elif computer and game and index % 2 == 1 - remainder and \
                    rb.getWinner() == "banana":

                # sa = SA.SimpleAlgorithm(sb, player)  # initialize the simple opponent
                sa = SA.Minimax(rb, player)  # initialize the minimax opponent

                coord = sa.getMove()
                line = coord[0]
                col = coord[1]
                rb.play(line, col, player)
                window.FindElement(str(line + 1) + str(col + 1)).update(text=player)
                index += 1

            if rb.getWinner() != "banana":  # this is to show the 'you win' messages
                game = False
                window.FindElement('v').Update(text=rb.getWinner())
                window.FindElement('v').Update(visible=True)
                window.FindElement('a').Update(visible=True)
                index = 0
                rb = R.RegularTicTacToe()

            if not game and event == 'a':  # this is just to reset the game
                game = True
                window.close()

                choice = menu()
                quantum = choice[0]
                computer = choice[1]

                window = sg.Window('Quantum Tic Tac Toe', default_element_size=(12, 12), margins=(70, 50),
                                   size=(400, 510), font='Any 14').Layout(makeLayout())
                window.Finalize()
                computerFirst = computerFirst is False

        window.Refresh()
