#from loguru import logger # type: ignore
import random


class SmartAgent:
    def __init__(self, env, player_name=None, player_id="player_0"):
        """Initialize the agent with a PettingZoo Connect Four environment."""
        self.env = env
        self.action_space = env.action_space("player_0")
        self.player_name = player_name or "SmartAgent"

        # nouveau : mémoriser si on est player_0 ou player_1
        self.player_id = player_id
        if self.player_id == "player_0":
            self.my_channel = 0
            self.opp_channel = 1
        else:
            self.my_channel = 1
            self.opp_channel = 0

    def choose_action(self, observation, reward=0.0, terminated=False,
                      truncated=False, info=None, action_mask=None):
        """Select an action according to heuristic rules."""
        if terminated or truncated:
            return None

        valid_actions = self._get_valid_actions(action_mask)

        # Rule 1: Win immediately
        winning_move = self._find_winning_move(observation, valid_actions,
                                               channel=self.my_channel)
        if winning_move is not None:
            #logger.success(f"{self.player_name}: WINNING MOVE -> column {winning_move}")
            return winning_move

        # Rule 2: Block the opponent's winning move
        blocking_move = self._find_winning_move(observation, valid_actions,
                                                channel=self.opp_channel)
        if blocking_move is not None:
            #logger.warning(f"{self.player_name}: BLOCKING -> column {blocking_move}")
            return blocking_move

        # # Rule 3: Create double threat
        # double_threat = self._creates_double_threat(observation, valid_actions, channel=0)
        # if double_threat is not None:
        #     return double_threat

        # Rule 4: Prefer center columns when no tactival move is available
        center_preference = [3, 2, 4, 1, 5, 0, 6]
        for col in center_preference:
            if col in valid_actions:
                #logger.info(f"{self.player_name}: CENTER PREFERENCE -> column {col}")
                return col

        # Rule 5: Random fallback
        action = random.choice(valid_actions)
        #logger.debug(f"{self.player_name}: RANDOM -> column {action}")
        return action

    def _get_valid_actions(self, action_mask):
        """Return the list of indices corresponding to playable columns."""
        if action_mask is None:
            return list(range(self.action_space.n))

        return [i for i, v in enumerate(action_mask) if v == 1]
    def _find_winning_move(self, observation, valid_actions, channel):
        board = observation.copy()

        for col in valid_actions:
            row = self._get_next_row(board, col)
            if row is None: #full column
                continue
            board_simulation = board.copy()
            board_simulation[row, col, channel] = 1

            if self._check_win_from_position(board_simulation, row=row,
                                             col=col, channel=channel):
                return col
        return None

    def _get_next_row(self, board, col):
        for row in range(5, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None

    def _check_win_from_position(self, board, row, col, channel):
        directions = [(0,1), (1,0), (-1,1), (1,1)]
        for d_row, d_col in directions:
            temp = 1
            r, c = row + d_row, col + d_col
            while 0 <= r < 6 and 0 <= c < 7 and board[r,c, channel] == 1:
                r += d_row
                c += d_col
                temp += 1
            r, c = row - d_row, col - d_col
            while 0 <= r < 6 and 0 <= c < 7 and board[r,c, channel] == 1:
                r -= d_row
                c -= d_col
                temp += 1

            if temp >= 4:
                return True

        return False
    