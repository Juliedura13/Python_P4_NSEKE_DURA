Après avoir implémenté un agent de niveau 1 (joueur aléatoire ne jouant seulement des coups valides), nous avons fait une analyse statistique de 100 parties simulées entre deux agents. 

Nous nous intéresserons aux questions suivantes:

1. Distribution des victoires : Les victoires sont-elles à peu près égales entre le joueur 1 et le joueur 2 ?
2. Avantage du premier coup : Le joueur 1 (qui commence) a-t-il un avantage ?
3. Durée de la partie : Quel est le nombre moyen de coups ? Min et max ?
4. Fréquence des matchs nuls : À quelle fréquence les parties se terminent-elles par un match nul ?


1. Distribution des victoires
Nous remarquons avec notre code que les victoires entre le joueur 1 et le joueur 2 ne sont pas parfaitement équilibrées. Le joueur 0 (qui commence) gagne un peu plus que le joueur 1. Mais les deux gagnent obtiennent au moins 38% de victoires sur l'ensemble des parties.
Cependant avec l'agent "plus intelligent", comme l'agent 0 commence il a souvent plus de chances de gagner. Les écarts de victoires sont plus marqués!

2. Avantage du premier coup
Celui qui joue en premier a un avantage car il pose toujours son pion avant son adversaire. C'est comme s'il avait un coup d'avance. Il aura donc plus de chance de gagant avant l'adversaire. On peut observer cela avec le code de l'agent "plus intelligent".

3. Durée de la partie
On peut jouer au moins 7 coups et au plus 42 coups dans une partie. Cependant, la partie s'achèvent entre 7 et 40 coups.

4. Fréquence des matchs nuls
Ils sont peu fréquents. Il faudrait augmenter le nombre de parties jouer pour avoir plus de matchs nuls.