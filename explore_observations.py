"""Exploration script to understand the structure of observations in Connect Four."""
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print("Agent:", agent)
    print("Observation keys:", observation.keys())
    print("Observation shape:", observation['observation'].shape)
    print("Action mask:", observation['action_mask'])

    env.step(3)
    break

env.close()


def print_board(observation):
    """Print a human-readable version of the board."""
    for i in range(6):
        row = ""
        for j in range(7):
            if observation[i,j,0] == 1: #piece of the current player
                row += 'X'
            elif observation[i,j,1] == 1: #opponent's piece
                row += 'O'
            else:
                row += '.'
        print(row)
    pass

# Test your function
env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])

    # Make a few moves to see the board change
    env.step(3)
    if agent == env.agents[0]:
        break

env.close()

#simple_game.py
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        if reward == 1:
            print(f"{agent} wins!")
        elif reward == 0:
            print("It's a draw!")
    else:
        # Take a random valid action
        mask = observation["action_mask"]
        action = env.action_space(agent).sample(mask)
        print(f"{agent} plays column {action}")

    env.step(action)

input("Press Enter to close...")
env.close()
