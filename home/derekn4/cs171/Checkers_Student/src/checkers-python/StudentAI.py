from random import randint
from BoardClasses import Move
from BoardClasses import Board
from Checker import Checker

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.val = 0

    def miniMax(self, board, depth, maxPlayer, bestMove, alpha, beta):
        #alpha-beta pruning
        #think of more heuristics
            #corner placement
            #pdf chase has bookmarked, LINKED IN PIAZZA
            #increase depth as fewer pieces on board

        if depth == 0:
            return self.heuristics(board), bestMove

        if maxPlayer:
            moves = board.get_all_possible_moves(self.color)
            value = -1000
            for move in moves:
                for subMove in move:
                    #check if num pieces change, if no change BECOME KING
                    #check if subMove isn't for a piece that is ALREADY a king
                    '''
                    if self.color==1:
                        if subMove[0]==board.row-1:
                            bestMove = subMove
                            #depth = 1
                    else:
                        if subMove[0]==0:
                            bestMove = subMove
                            #depth = 1
                    '''

                    board.make_move(subMove, self.color)

                    evalMove = self.miniMax(board, depth - 1, False, bestMove, alpha, beta)[0]
                    board.undo()
                    if evalMove > value:
                        value = evalMove
                        bestMove = subMove
                        alpha = max(alpha, value)
                        if beta<=alpha:
                            break#return value, bestMove
        else:
            if self.color == 1:
                opponent = self.color + 1
            else:
                opponent = self.color - 1

            moves = board.get_all_possible_moves(opponent)
            value = 1000
            for move in moves:
                for subMove in move:
                    board.make_move(subMove, opponent)
                    evalMove = self.miniMax(board, depth - 1, True, bestMove, alpha, beta)[0]
                    board.undo()
                    value = min(value, evalMove)
                    beta = min(beta, value)
                    if beta<= alpha:
                        break#return value, bestMove

        return value, bestMove


    def heuristics(self, board):
        white_score = 0
        black_score = 0

        for row in range(board.row):
            for col in range(board.col):
                if board.board[row][col].color=='w':
                    white_score+=10

                    if col==board.col-1 or col==0:
                        white_score+=2
                        if col== board.col-1 and row!=board.row-1:
                            if board.board[row + 1][col - 1].color == 'w':
                                white_score+=3
                        elif col==0 and row!=board.row-1:
                            if board.board[row+1][col+1].color=='w':
                                white_score += 3

                    if row!=board.row-1 and col!= board.col-1 and col!=0:
                        if board.board[row+1][col-1].color=='w' or board.board[row+1][col+1].color=='w':
                            white_score+=3


                elif board.board[row][col].color=='W':
                    white_score+=20

                if board.board[row][col].color=='b':
                    black_score+=10

                    if col==board.col-1 or col==0:
                        black_score+=2

                        if col== board.col-1 and row!=board.row-1:
                            if board.board[row - 1][col - 1].color == 'b':
                                black_score+=3
                        elif col==0 and row!=board.row-1:
                            if board.board[row-1][col+1].color=='b':
                                black_score += 3

                    if row!=board.row-1 and col!= board.col-1 and col!=0:
                        if board.board[row-1][col-1].color=='b' or board.board[row-1][col+1].color=='b':
                            black_score+=3

                    # if col==board.col-1 or col==0:
                    #     black_score+=5
                    #
                    # if row!=0 and col!= board.col-1 and col!=0:
                    #     if board.board[row-1][col-1].color=='b' or board.board[row-1][col+1].color=='b':
                    #         black_score+=3

                elif board.board[row][col].color=='B':
                    black_score+=20

        if self.color == 2:
            return white_score-black_score
        else:
            return black_score - white_score

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        if self.val<=3:
            self.val += 1
            value, move = self.miniMax(self.board, 3, True, None, -10000, 10000)

        else:
            depthCheck = self.heuristics(self.board)
            self.val+=1

            if self.val>30:
                value, move = self.miniMax(self.board, 3, True, None, -10000, 10000)
            else:
                if depthCheck > 0:
                    value, move = self.miniMax(self.board, 4, True, None, -10000, 10000)
                else:
                    value, move = self.miniMax(self.board, 5, True, None, -10000, 10000)

        self.board.make_move(move, self.color)

        return move
