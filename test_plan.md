**Conception de stratégie de test**

1. Que tester?
Test fonctionnels:
    - sélection de coup valide: action_mask nous retourne une liste de colonnes où l'agent peut jouer.
    - respect du masque d'action: soit il est fourni soit nous lui disons à quoi il correspond dans notre test.
    - gestion de fin de partie: la partie s'arrête bien après la condition de fin ('terminated' ou 'truncated').

Test de performance:
    - temps par coup: le temps par coup est très faible (voir test à la fin du fichier test_smart_agent.py)
    - utilisation de la mémoire: à part quelques copies temporaires et le plateau (fourni par l'environnement), notre code n'utilise rien d'autre. Il n'utilise qu'environ 8 Ko.

Test stratégiques:
    - gagne contre un agent aléatoire: sur 100 parties, SmartAgent (agent_0) gagne en moyenne 70% des parties contre WeightedRandomAgent (agent_1). Il y a pas souvent de matchs nuls mais quand c'est le cas il y en a au plus 2%. 
    - bloque les menaces évidentes: grâce à la bibliothèque loguru, nous voyons que SmartAgent bloque bien les menaces évidentes.
    - exploitation des coups gagnants: dès qu'il a l'occasion de gagner, SmartAgent la saisie.

2. Comment tester?
Dans notre document *test_smart_agent*, nous avons ajouté des lignes de codes nous permettant de répondre aux questions sur la performances de notre agent.

3. Critères de succès
Nous avons choisi les critères suivants:
    - gagner au moins 85% des parties contre WeightedRandomAgent et au moins 90% des parties contre RandomAgent.