"""Random agent for Connect Four."""

import random

# pylint: disable=too-few-public-methods
class RandomAgent:
    """An agent that plays random valid moves."""
    def __init__(self, env, player_name=None):
        """Store environment and the optional player name."""
        self.env = env
        self.player_name = player_name
        pass

    def choose_action_manual(self, observation,terminated=False,
                             truncated=False, action_mask=None):
        if terminated or truncated:
            return None

        if action_mask is None:
            action_mask = observation["action_mask"]

        valid_actions = [i for i, value in enumerate(action_mask)
                         if value == 1]

        if not valid_actions:
                return None
        return random.choice(valid_actions)

# pylint: disable=too-many-locals
class WeightedRandomAgent(RandomAgent):
    """Random agent that prefers center columns via predefined weights."""
    def choose_action(self, observation, terminated=False,
                      truncated=False, action_mask=None):
        """Choose a random valid action, biased toward center columns."""
        weights_attribution = [1, 2, 3, 4, 3, 2, 1]

        if terminated or truncated:
            return None

        if action_mask is None:
            action_mask = observation["action_mask"]

        valid_actions = []
        weights = []

        for i, value in enumerate(action_mask):
            if value == 1:
                valid_actions.append(i)
                weights.append(weights_attribution[i])
        return random.choices(valid_actions, weights=weights)[0]
    