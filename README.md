
Objectif du projet : Prédire le Remaining Useful Life (RUL) d'un système aérospatial à partir de données de télémétrie.



Ici non pas un problème de classification mais un problème de régression temporelle (Dans combien de cycles reste-il avant la panne ?)

RUL = Remaining Useful Life = l'estimation du temps ou du nombre de cycles de fonctionnement qu'il reste à un équipement, une machine ou un composant avant qu'il ne tombe en panne ou n'atteigne un seuil critique nécessitant sa réparation ou son remplacement

Dans notre cas, le RUL représente donc le nombre de cycles restant avant la panne du moteur.

# Explication du Dataset

Le dataset utilisé est C-MAPSS (Commercial Modular Aero-Propulsion System Simulation), développé par la NASA.

Il contient plusieurs séries temporelles multivariées représentant la télémétrie de différents moteurs.

Chaque moteur possède sa propre trajectoire de fonctionnement :

Cycle 1 → Cycle 2 → Cycle 3 → ... → Cycle N → Panne

À chaque cycle, plusieurs variables sont enregistrées :

- numéro du moteur
- numéro du cycle
- 3 paramètres opérationnels
- 21 mesures provenant de capteurs

Les données sont bruitées et les moteurs commencent avec des niveaux d'usure initiaux différents.

Le dataset est divisé en 4 sous-ensembles : FD001, FD002, FD003 et FD004.

Ces sous-ensembles présentent différents niveaux de difficulté selon :

- le nombre de conditions opérationnelles ;
- le nombre de modes de dégradation.


# FD001

100 trajectoires d'entraînement
100 trajectoires de test
1 condition opérationnelle
1 mode de dégradation : HPC degradation

FD001 est le sous-ensemble le plus simple et constitue un bon point de départ pour développer notre premier modèle.

# FD002

260 trajectoires d'entraînement
259 trajectoires de test
6 conditions opérationnelles
1 mode de dégradation : HPC degradation

FD002 est plus difficile que FD001 car le moteur peut fonctionner dans différentes conditions opérationnelles.

Le modèle doit donc distinguer les variations normales liées aux conditions de fonctionnement des variations liées à la dégradation du moteur.

# FD003

100 trajectoires d'entraînement
100 trajectoires de test
1 condition opérationnelle
2 modes de dégradation : HPC degradation, Fan degradation

FD003 introduit donc plusieurs modes de dégradation, ce qui rend le problème plus complexe que FD001.

# FD004

248 trajectoires d'entraînement
249 trajectoires de test
6 conditions opérationnelles
2 modes de dégradation : HPC degradation, Fan degradation

FD004 combine les deux difficultés précédentes :

plusieurs conditions opérationnelles + plusieurs modes de dégradation.

Il constitue donc le sous-ensemble le plus complexe des quatre.



# Explication fichier


RUL_XXXX.txt = contient la vraie valeur de RUL de chaque moteur du jeu de test. (c'est notres reponse à nos test)

train_ XXXX.txt = trajectoires d'entraînement : Evolution du moteur au cours du temps, depuis son fonctionnement normal jusqu'a sa défaillance.
-> dans le train set, on connait toutes les observations jusqu'a la panne (on peut connaitre le RUL).


test_XXXX.txt = La trajectoire s'arrete avant la panne.



26 colonnes
│
├── 1 colonne → identité du moteur
├── 1 colonne → cycle
├── 3 colonnes → conditions opérationnelles
└── 21 colonnes → capteurs

# Les conditions opérationnelles

Une condition opérationnelle est définie par une combinaison particulière de ces trois paramètres

Condition A → (setting_1, setting_2, setting_3)
Condition B → (setting_1, setting_2, setting_3)
Condition C → (setting_1, setting_2, setting_3)
...

# Les données de capteurs

Elles permettent au modèle d'observer l'état du moteur et son évolution au cours du temps, afin d'estimer le RUL.

Le modèle pourra apprendre differnetes relation entre les capteurs.

En résumé : les capteurs sont les observations indirectes de l'état du moteur. Mon modèle doit apprendre à transformer leur évolution dans le temps en une estimation du nombre de cycles restant avant la panne.

