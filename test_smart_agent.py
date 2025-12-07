"""Tests for SmartAgent. """
import tracemalloc
import time
from pettingzoo.classic import connect_four_v3
from smart_agent import SmartAgent
from random_agent import WeightedRandomAgent
from test_my_random_agent import stat_games

env = connect_four_v3.env(render_mode=None)
env.reset(seed=42)

smart_agent = SmartAgent(env)
random_agent = WeightedRandomAgent(env)
winner = None

for agent_name in env.agent_iter():
    obs, reward, terminated, truncated, info = env.last()

    if terminated or truncated:
        if reward == 1:
            winner = agent_name
        env.step(None)
        continue

    board = obs["observation"]
    mask = obs["action_mask"]

    if agent_name == "player_0":
        # SmartAgent plays with his rules
        action = smart_agent.choose_action(board, action_mask=mask)
    else:
        # the opponent plays randomly
        action = random_agent.choose_action_manual(obs, action_mask=mask)

    env.step(action)

if __name__ == "__main__":
    tracemalloc.start()
    start = time.time()
    stats, moves = stat_games(100)
    end = time.time()
    current_size, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    #Results
    print(f"Temps pour choose_action : {end - start} s")
    print(f"Mémoire actuelle : {current_size / 1024:.2f} Ko")
    print(f"Pic mémoire: {peak / 1024:.2f} Ko")
