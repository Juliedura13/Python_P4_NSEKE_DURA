"""Minimax agent with alpha-beta pruning for Connect Four"""

import random

class MinimaxAgent:

    def __init__(self, env, depth=4, player_name=None, player_id="player_0"):
        self.env = env
        self.action_space = env.action_space("player_0")
        self.depth = depth
        self.player_name = player_name or f"Minimax(d={depth})"

        self.player_id = player_id
        self.my_channel = 0
        self.opp_channel = 1


    def choose_action(self, observation, reward=0.0, terminated=False,
                      truncated=False, info=None, action_mask=None,):
        """Choose action using minimax algorithm"""
        if terminated or truncated:
            return None

        if action_mask is None:
            valid_actions = list(range(self.action_space.n))
        else:
            valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]

        if not valid_actions:
            return None

        board = observation

        best_value = float("-inf")
        best_actions = []

        for action in valid_actions:
            new_board = self._simulate_move(board, action, channel=self.my_channel)
            if new_board is None:
                continue

            value = self._minimax(new_board, depth=self.depth - 1,
                                alpha=float("-inf"), beta=float("inf"),
                                maximizing=False,)

            if value > best_value:
                best_value = value
                best_actions = [action]
            elif value == best_value:
                best_actions.append(action)

        if not best_actions:
            return random.choice(valid_actions)

        return random.choice(best_actions)


    def _minimax(self, board, depth, alpha, beta, maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or self._check_win(board, self.my_channel) or self._check_win(board, self.opp_channel):
            return self._evaluate(board)

        valid_moves = self._get_valid_moves(board)
        if not valid_moves:
            return self._evaluate(board)

        if maximizing:
            value = float("-inf")
            for col in valid_moves:
                new_board = self._simulate_move(board, col, channel=self.my_channel)
                value = max(
                    value,
                    self._minimax(new_board, depth - 1, alpha, beta, maximizing=False),
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for col in valid_moves:
                new_board = self._simulate_move(board, col, channel=self.opp_channel)
                value = min(
                    value,
                    self._minimax(new_board, depth - 1, alpha, beta, maximizing=True),
                )
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def _simulate_move(self, board, col, channel):
        """Simulate placing a piece without modifying original board"""
        new_board = board.copy()
        for row in range(5, -1, -1):
            if new_board[row, col, self.my_channel] == 0 and new_board[row, col, self.opp_channel] == 0:
                new_board[row, col, channel] = 1
                break
        return new_board

    def _get_valid_moves(self, board):
        """Returns list of valid columns"""
        valid_moves = []
        for col in range(7):
            if board[0, col, self.my_channel] == 0 and board[0, col, self.opp_channel] == 0:
                valid_moves.append(col)
        return valid_moves

    def _evaluate(self, board):
        """Evaluate board position"""
        # victoire / défaite
        if self._check_win(board, self.my_channel):
            return 1000.0
        if self._check_win(board, self.opp_channel):
            return -1000.0

        score = 0.0

        # bonus centre (colonne 3)
        center_col = 3
        for row in range(6):
            if board[row, center_col, self.my_channel] == 1:
                score += 3.0
            if board[row, center_col, self.opp_channel] == 1:
                score -= 3.0

        for col in range(7):
            for row in range(6):
                if board[row, col, self.my_channel] == 1:
                    score += (3 - abs(3 - col)) * 0.5
                if board[row, col, self.opp_channel] == 1:
                    score -= (3 - abs(3 - col)) * 0.5

        return score

    def _check_win(self, board, channel):
        """Check if player has won (4 in a row)"""
        # horizontal
        for row in range(6):
            for col in range(4):
                if (
                    board[row, col, channel] == 1
                    and board[row, col + 1, channel] == 1
                    and board[row, col + 2, channel] == 1
                    and board[row, col + 3, channel] == 1
                ):
                    return True

        # vertical
        for col in range(7):
            for row in range(3):
                if (
                    board[row, col, channel] == 1
                    and board[row + 1, col, channel] == 1
                    and board[row + 2, col, channel] == 1
                    and board[row + 3, col, channel] == 1
                ):
                    return True

        # diagonale montante /
        for row in range(3, 6):
            for col in range(4):
                if (
                    board[row, col, channel] == 1
                    and board[row - 1, col + 1, channel] == 1
                    and board[row - 2, col + 2, channel] == 1
                    and board[row - 3, col + 3, channel] == 1
                ):
                    return True

        # diagonale descendante \
        for row in range(3):
            for col in range(4):
                if (
                    board[row, col, channel] == 1
                    and board[row + 1, col + 1, channel] == 1
                    and board[row + 2, col + 2, channel] == 1
                    and board[row + 3, col + 3, channel] == 1
                ):
                    return True

        return False
