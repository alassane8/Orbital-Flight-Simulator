# Orbital Flight Simulator

Simulateur de vol orbital que je développe pour appliquer le plus de réalisme possible à chaque étape du vol — du décollage jusqu'à l'injection orbitale, et au-delà.

Ce projet vient d'une conviction : la meilleure façon de vraiment comprendre la mécanique orbitale et le GNC, c'est de l'implémenter soi-même, équation par équation.

---

## Ce que le simulateur couvre

Le vol complet d'un lanceur, de la rampe de lancement à l'orbite lunaire :

- **Phase atmosphérique** — modèle ISA, traînée aérodynamique, gravity turn, consommation d'ergols (Tsiolkovsky)
- **Insertion orbitale** — intégrateur RK4, transition vers les éléments kepleriens
- **Mécanique orbitale** — propagateur keplerien, perturbation J2 (aplatissement terrestre), manœuvres impulsionnelles Δv
- **Transfert Terre–Lune** — manœuvre de Hohmann, calcul du budget Δv
- **Dynamique d'attitude (en cours)** — représentation quaternion, équations d'Euler, contrôleur PD

La simulation avance par pas de temps fixes. La physique est intégrée numériquement à chaque tick, avec une visualisation pygame en temps réel.

---

## Architecture technique

```
orbital-flight-simulator/
├── main/
│   ├── config/           — paramètres de simulation
│   ├── launch_site/      — sites de lancement
│   ├── orbital_core/     — noyau de calcul (RK4, Kepler, J2, Hohmann)
│   ├── orbital_target/   — orbites cibles
│   ├── payload/          — charge utile
│   ├── rocket/           — modèle du lanceur
│   ├── shared/           — utilitaires communs
│   ├── spaceflight/      — séquence de vol et intégration mission
│   └── main.py
└── requirements.txt
```

**Stack :** Python pour la logique mission et la visualisation · C++ (pybind11 + Eigen) pour le noyau de calcul numérique · Simulink pour la validation croisée des lois de contrôle

La frontière Python/C++ est intentionnelle : l'assemblage des forces reste en Python pour garder de la flexibilité, le calcul pur (RK4, Kepler, J2) tourne en C++ pour les performances.

---

## Ce que le projet contiendra

- Modèle atmosphérique ISA (troposphère → 80 km)
- Dynamique de lancement 3-DOF avec gravity turn et consommation d'ergols
- Intégrateur RK4 en C++ (pybind11 + Eigen)
- Propagateur keplerien avec perturbation J2
- Manœuvres impulsionnelles Δv et transfert de Hohmann Terre–Lune
- Dynamique d'attitude 6-DOF — quaternions, équations d'Euler, contrôleur PD
- Visualisation temps réel pygame (trajectoire 3D, HUD)
- Validation croisée Python / Simulink sur les lois de contrôle

---

## Pourquoi ce projet

Je voulais comprendre comment un lanceur réel passe de 0 m/s sur une rampe à une orbite précise. Pas en lisant des formules, mais en les faisant tourner et en regardant si la trajectoire converge.

Chaque module a été l'occasion de creuser un sujet : pourquoi RK4 et pas Euler, comment le gravity turn minimise les contraintes structurelles, ce que J2 fait réellement à une orbite sur quelques révolutions, pourquoi les quaternions et pas les angles d'Euler pour l'attitude.

L'objectif final est un simulateur qui se rapproche autant que possible des pratiques industrielles — la séparation 3-DOF/6-DOF, le workflow Python→Simulink→C embarqué, les modèles de référence (ISA, WGS84, EGM2008).