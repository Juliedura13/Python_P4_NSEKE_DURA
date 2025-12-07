"""Tournament script to compare SmartAgent with Minimax, Random and WeightedRandom agents."""
from pettingzoo.classic import connect_four_v3

from random_agent import RandomAgent, WeightedRandomAgent
from smart_agent import SmartAgent
from minimax_agent import MinimaxAgent


# pylint: disable=too-many-locals
def play_one_game(agent0_class, agent1_class, seed = 42):
    """Play a single game between agent0 (player_0) and agent1 (player_1)."""
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=seed)

    if agent0_class in [SmartAgent, MinimaxAgent]:
        agent0 = agent0_class(env, player_id="player_0")
    else:
        agent0 = agent0_class(env)

    if agent1_class in [SmartAgent, MinimaxAgent]:
        agent1 = agent1_class(env, player_id="player_1")
    else:
        agent1 = agent1_class(env)
    winner = None
    rewards = {"player_0": 0, "player_1": 0}
    move_count = 0

    for agent_name in env.agent_iter():
        obs, reward, terminated, truncated, info = env.last()

        rewards[agent_name] = reward

        if terminated or truncated:
            env.step(None)
            continue

        mask = obs["action_mask"]
        board = obs["observation"]

        if agent_name == "player_0":
            if isinstance(agent0, RandomAgent):
                action = agent0.choose_action_manual(obs, action_mask=mask)
            elif isinstance(agent0, WeightedRandomAgent):
                action = agent0.choose_action(obs, action_mask=mask)
            else:  # SmartAgent, MinimaxAgent, etc.
                action = agent0.choose_action(board, action_mask=mask)
        else:  # player_1
            if isinstance(agent1, RandomAgent):
                action = agent1.choose_action_manual(obs, action_mask=mask)
            elif isinstance(agent1, WeightedRandomAgent):
                action = agent1.choose_action(obs, action_mask=mask)
            else:
                action = agent1.choose_action(board, action_mask=mask)

        move_count += 1
        env.step(action)

    env.close()

    if rewards["player_0"] > rewards["player_1"]:
        winner = "player_0"
    elif rewards["player_1"] > rewards["player_0"]:
        winner = "player_1"
    else:
        winner = "draw"

    return winner, move_count

def stat_games(num_games, agent0_class, agent1_class):
    results = {"player_0" : 0, "player_1" : 0, "draw" : 0}
    moves = []

    for i in range(num_games):
        winner, move_count = play_one_game(agent0_class, agent1_class, seed=42 + i)
        results[winner] += 1
        moves.append(move_count)

    win_rate_agent0 = results["player_0"] / num_games
    win_rate_agent1 = results["player_1"] / num_games
    draw_rate = results["draw"] / num_games

    #mean_moves = sum(moves) / num_games

    print("\n=== Résultats sur", num_games, "parties ===")
    print(f"Wins for player_0 : {results['player_0']}  ({win_rate_agent0:.2%})")
    print(f"Wins for player_1 : {results['player_1']}  ({win_rate_agent1:.2%})")
    print(f"Draws        : {results['draw']}      ({draw_rate:.2%})")

    #print(f"Nombre moyen de coups : {mean_moves}")

    return results

if __name__ == "__main__":
    print("_____SmartAgent (player_0) vs RandomAgent (player_1)_____")
    stat_games(100, SmartAgent, RandomAgent)

    print("_____RandomAgent (player_0) vs SmartAgent (player_1)_____")
    stat_games(100, RandomAgent, SmartAgent)

    print("_____SmartAgent (player_0) vs WeightedRandomAgent (player_1)_____")
    stat_games(100, SmartAgent, WeightedRandomAgent)

    print("_____WeightedRandomAgent (player_0) vs SmartAgent (player_1)_____")
    stat_games(100, WeightedRandomAgent, SmartAgent)
    
    print("_____Minimax (player_0) vs SmartAgent (player_1)_____")
    stat_games(100, MinimaxAgent, SmartAgent)

    print("_____SmartAgent (player_0) vs Minimax (player_1)_____")
    stat_games(100, SmartAgent, MinimaxAgent)
