"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
#import math

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    score_dict = {}
    # Base case of the recursion, when the winner is decided
    # return a score and an illegal move 
    if board.check_win() != None:
        return SCORES[board.check_win()], (-1, -1)
    else:
        for square in board.get_empty_squares():
            playboard = board.clone()
            playboard.move(square[0], square[1], player)
            new_player = provided.switch_player(player)
            score, dummy_pos = mm_move(playboard, new_player)
            score_dict[square] = score
        # Maximize
        if player == provided.PLAYERX:
            best_score = max(score_dict.values())
            for pos in score_dict:
                if score_dict[pos] == best_score:
                    return best_score, pos
        # Minimize
        elif player == provided.PLAYERO:
            best_score = min(score_dict.values())
            for pos in score_dict:
                if score_dict[pos] == best_score:
                    return best_score, pos

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#Test
board = provided.TTTBoard(3)
board.move(0, 1, provided.PLAYERX)
board.move(1, 1, provided.PLAYERO)
board.move(1, 0, provided.PLAYERX)
board.move(0, 0, provided.PLAYERO)
board.move(2, 2, provided.PLAYERX)
board.move(0, 2, provided.PLAYERO)
board.move(2, 0, provided.PLAYERX)
#board.move(1, 2, provided.PLAYERO)
#board.move(2, 0, provided.PLAYERX)
#board.move(2, 1, provided.PLAYERO)
print board
print move_wrapper(board, provided.PLAYERX, 50)

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
