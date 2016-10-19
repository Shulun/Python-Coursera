"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

#define a helper function for performing producing subtrees
def make_children(board, player):
    #make the elements in the subtrees
    for square in board.get_empty_squares():
        child_board = board.clone()
        child_board.move(square[0], square[1], player)
        yield (square, child_board)


def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #base case
    if board.check_win() != None:
        return SCORES[board.check_win()], (-1, -1)
    
    children = make_children(board, player)
    child_player = provided.switch_player(player)
    
    #recursive case
    results = []
    for child in children:
        score, dummy_move = mm_move(child[1], child_player)
        results.append((score, child[0]))
        if score * SCORES[player] == 1:
            return score, child[0]
    if player == provided.PLAYERX:
        return max(results)
    elif player == provided.PLAYERO:
        return min(results)
    
    #return 0, (-1, -1)

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

# provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#Test
#board = provided.TTTBoard(3)
#board.move(0, 1, provided.PLAYERX)
#board.move(0, 0, provided.PLAYERO)
#board.move(1, 0, provided.PLAYERX)
#board.move(1, 1, provided.PLAYERO)
#board.move(0, 2, provided.PLAYERX)
#board.move(0, 2, provided.PLAYERO)
#board.move(2, 1, provided.PLAYERX)
#board.move(1, 2, provided.PLAYERO)
#board.move(2, 0, provided.PLAYERX)
#board.move(2, 1, provided.PLAYERO)
#print board
#print move_wrapper(board, provided.PLAYERO, 50)
