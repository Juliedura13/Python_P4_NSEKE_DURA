from pettingzoo.classic import connect_four_v3
from random_agent import RandomAgent, WeightedRandomAgent

def print_board(obs):
    observation = obs["observation"]
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
    print()


def one_game (seed = 42, render = False):
    """Play one game between agent0 (player_0) and agent1 (player_1).""" 
    env = connect_four_v3.env(render_mode="human" if render else None)
    env.reset(seed=seed)

    agent0 = WeightedRandomAgent(env, player_name= "player_0")
    agent1 = RandomAgent(env, player_name = "player_1")

    winner = None
    move_count = 0

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
            if reward == 1:
                winner = agent
            env.step(None)
            continue
        # Take a random valid action
        mask = observation["action_mask"]
        if agent == "player_0":
            action = agent0.choose_action(observation,action_mask = mask)
        else:
            action = agent1.choose_action_manual(observation, action_mask = mask)

        move_count += 1
        env.step(action)

    env.close()

    if winner is None:
        winner = "draw"

    return winner, move_count

def stat_games(num_games):
    results = {"player_0" : 0, "player_1" : 0, "draw" : 0}
    moves = []

    for i in range(num_games):
        winner, move_count = one_game(seed=42 + i)
        results[winner] += 1
        moves.append(move_count)

    win_rate_agent0 = results["player_0"] / num_games
    win_rate_agent1 = results["player_1"] / num_games
    draw_rate = results["draw"] / num_games

    # mean_moves = sum(moves) / num_games
    # min_moves = min(moves)
    # max_moves = max(moves)

    print("\n=== Résultats sur", num_games, "parties ===")
    print(f"Wins of player_0 : {results['player_0']}  ({win_rate_agent0:.2%})")
    print(f"Wins of player_1 : {results['player_1']}  ({win_rate_agent1:.2%})")
    print(f"Draws        : {results['draw']}      ({draw_rate:.2%})")

    #print(f"Nombre moyen de coups : {mean_moves}")
    #print(f"Nombre minimum de coups : {min_moves}")
    #print(f"Nombre maximum de coups : {max_moves}")

    return results, moves

if __name__ == "__main__":
    stat_games(100)
    