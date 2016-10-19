"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player

# board = provided.TTTBoard(3)
# player = provided.PLAYERO

# Add your functions here.
def mc_trial(board, player):
    '''This function takes a current board and the next player to move.'''
    while True:
        empty_square = board.get_empty_squares()
        next_move = random.choice(empty_square)
        board.move(next_move[0], next_move[1], player)
        if board.check_win() == None:
            player = provided.switch_player(player)
        else:
            break
    
def mc_update_scores(scores, board, player):
    '''The function scores the completed board and update the scores grid.'''
    dim = board.get_dim()
    winner = board.check_win()
    other_player = provided.switch_player(player)
    if winner == player:
        point = {player: + SCORE_CURRENT, other_player: - SCORE_OTHER, provided.EMPTY: 0}
    elif winner == other_player:
        point = {player: - SCORE_CURRENT, other_player: + SCORE_OTHER, provided.EMPTY: 0}
    else:
        point = {player: 0, other_player: 0, provided.EMPTY: 0}
    for dummy_i in range(dim):
        for dummy_j in range(dim):
            scores[dummy_i][dummy_j] += point[board.square(dummy_i, dummy_j)]
    
def get_best_move(board, scores):
    '''This function takes a current board and a grid of scores.'''
    empty = board.get_empty_squares()
    highest_score = -100*NTRIALS
    highest_pos = []
    for dummy_i in range(len(empty)):
        pos = empty[dummy_i]
        if scores[pos[0]][pos[1]] >= highest_score:
            highest_score = scores[pos[0]][pos[1]]
    for dummy_i in range(len(empty)):
        pos = empty[dummy_i]
        if scores[pos[0]][pos[1]] >= highest_score:
            highest_pos.append(pos)
    pos_choice = random.choice(highest_pos)
    return pos_choice
    
def mc_move(board, player, trials):
    '''This function takes a current board, which player the machine player is, and the number of trials to run.'''
    dim = board.get_dim()
    scores = []
    j_array = []
    for dummy_i in range(dim):
        j_array.append(0)
    for dummy_j in range(dim):
        scores.append(list(j_array))
    for dummy in range(trials):
        new_board = board.clone()
        mc_trial(new_board, player)
        mc_update_scores(scores, new_board, player)
    return get_best_move(board, scores)
        
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, mc_move, NTRIALS, False)
