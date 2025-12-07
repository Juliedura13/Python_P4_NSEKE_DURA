import numpy as np
from pettingzoo.classic import connect_four_v3
from smart_agent import SmartAgent
env = connect_four_v3.env(render_mode=None)
env.reset(seed=42)
smart_agent = SmartAgent(env)

def test_detect_immediate_win():
    """Detect an immediate win"""
    board = np.zeros((6, 7, 2), dtype=int)
    board[5, 0, 0] = 1
    board[5, 1, 0] = 1
    board[5, 2, 0] = 1
    valid_actions = [0, 1, 2, 3, 4, 5, 6]
    winning_move = smart_agent._find_winning_move(board, valid_actions, channel=0)
    assert winning_move == 3

def test_block_opponent():
    """Block the opponent's immediate winning threat"""
    board = np.zeros((6, 7, 2), dtype=int)
    board[5, 0, 1] = 1
    board[5, 1, 1] = 1
    board[5, 2, 1] = 1
    action_mask = [1, 1, 1, 1, 1, 1, 1]
    action = smart_agent.choose_action(board, action_mask=action_mask)
    assert action == 3

def test_winning_is_better():
    """Focus on vertical win over blocking the opponent"""
    board = np.zeros((6, 7, 2), dtype=int)
    board[5, 0, 0] = 1
    board[4, 0, 0] = 1
    board[3, 0, 0] = 1
    board[5, 6, 1] = 1
    board[5, 5, 1] = 1
    board[5, 4, 1] = 1
    action_mask = [1, 1, 1, 1, 1, 1, 1]
    action = smart_agent.choose_action(board, action_mask=action_mask)
    assert action == 0

def test_winning_is_better():
    """Focus on diagonal win over blocking the opponent"""
    board = np.zeros((6, 7, 2), dtype=int)
    board[2, 3, 0] = 1
    board[3, 4, 0] = 1
    board[4, 5, 0] = 1
    board[3, 2, 1] = 1
    board[4, 3, 1] = 1
    board[5, 4, 1] = 1
    action_mask = [1, 1, 1, 1, 1, 1, 1]
    action = smart_agent.choose_action(board, action_mask=action_mask)
    assert action == 6

def test_respect_action_mask():
    """Select a column allowed by the action mask"""
    board = np.zeros((6,7,2), dtype=int)
    board[5, 4, 0] = 1
    board[4, 4, 1] = 1
    board[3, 4, 1] = 1
    board[2, 4, 1] = 1
    board[1, 4, 0] = 1
    board[0, 4, 0] = 1
    action_mask = [1, 1, 1, 1, 0, 1, 1]
    action = smart_agent.choose_action(board, action_mask=action_mask)
    assert action == 3
