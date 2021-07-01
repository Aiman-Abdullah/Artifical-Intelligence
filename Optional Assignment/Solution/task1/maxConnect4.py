import sys
from MaxConnect4Game import MaxConnect4game
import time

def oneMoveGame(gameboard):
    start_time = time.time()
    if gameboard.piece_count >= 42:
        print('Game board is full !\n Game Over !')
        sys.exit(0)
    print ('Gameboard state before move:')
    gameboard.print_gameboard()
    gameboard.aiPlay()
    print ('Gameboard state after move:')
    gameboard.print_gameboard()
    gameboard.count_score()
    print('Score: Player-1 = %d, Player-2 = %d\n' % (gameboard.player1Score, gameboard.player2Score))
    gameboard.PrintingGameBoardToFile()
    gameboard.gameFile.close()
    print("Total Execution Time:")
    print (time.time() - start_time)

def interactive_game(gameboard, next_player):
    start_time = time.time()
    print('Current Board state')
    gameboard.print_gameboard()
    gameboard.count_score()
    print('Score: Player-1 = %d, Player-2 = %d\n' % (gameboard.player1Score, gameboard.player2Score))
    if next_player == 'human-next':
        human_turn(gameboard)
    else:
        gameboard.aiPlay()
        gameboard.gameFile = open('computer.txt', 'w')
        gameboard.PrintingGameBoardToFile()
        gameboard.gameFile.close()
        gameboard.print_gameboard()
        gameboard.count_score()
        print('Score: Player-1 = %d, Player-2 = %d\n' % (gameboard.player1Score, gameboard.player2Score))
        human_turn(gameboard)

    if gameboard.getPieceCount() == 42:
        if gameboard.player1Score > gameboard.player2Score:
            print("Player 1 wins !")
        if gameboard.player1Score < gameboard.player2Score:
            print("Player 2 wins !")
        if gameboard.player1Score == gameboard.player2Score:
            print("The game is a Tie !")
        print("Game Over")
        print("Total Execution Time:")
        print (time.time() - start_time)




def human_turn(gameboard):
    while gameboard.getPieceCount() != 42:
        print("your turn.")
        user_input = int(input("Enter a column number between 1 - 7: "))
        if user_input<1 or user_input >7:
            print("Column that was entered not valid.")
            continue
        if not gameboard.playPiece(user_input - 1):
            print("Column number: %d is full. Try other column." % user_input)
            continue
        print("You made a move in column : " + str(user_input))
        gameboard.print_gameboard()
        gameboard.gameFile = open("human.txt", 'w')
        gameboard.PrintingGameBoardToFile()
        gameboard.gameFile.close()
        if gameboard.getPieceCount() == 42:
            print("No more moves possible, Game Over !")
            gameboard.count_score()
            print('Score: Player-1 = %d, Player-2 = %d\n' % (gameboard.player1Score, gameboard.player2Score))
            break
        else:
            print("AI is computing based on next " + str(gameboard.depth) + " steps!")
            gameboard.change_move()
            gameboard.aiPlay()
            gameboard.print_gameboard()
            gameboard.gameFile = open('computer.txt', 'w')
            gameboard.PrintingGameBoardToFile()
            gameboard.gameFile.close()
            gameboard.count_score()
            print('Score: Player-1 = %d, Player-2 = %d\n' % (gameboard.player1Score, gameboard.player2Score))


def main(argv):
    gameboard = MaxConnect4game()
    try:
        gameboard.gameFile = open(argv[2], 'r')
        file_lines = gameboard.gameFile.readlines()
        gameboard.gameboard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
        gameboard.current_move = int(file_lines[-1][0])
        gameboard.gameFile.close()
    except:
        print('File not found, begin new game.')
        gameboard.current_move = 1
    gameboard.checkPieceCount()
    gameboard.depth = argv[4]
    if argv[1] == 'one-move':
        try:
            gameboard.gameFile = open(argv[3], 'w')
        except:
            sys.exit('Error while opening output file.')
        oneMoveGame(gameboard)
    if argv[1] == 'interactive':
        interactive_game(gameboard, argv[3])


main(sys.argv)
