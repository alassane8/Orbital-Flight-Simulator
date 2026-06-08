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

---

## Recompiler le noyau de calcul C++

Le noyau de calcul (`orbital_core`) est un module C++ exposé à Python via pybind11. Il doit être recompilé après toute modification des fichiers `.cpp` ou `.h` dans `main/orbital_core/`.

### Prérequis

Installer pybind11 s'il n'est pas déjà présent :

```powershell
pip install pybind11
```

### Étapes de compilation

Depuis la racine du projet, naviguer dans le dossier de build :

```powershell
cd main\orbital_core\build
```

Configurer CMake en pointant vers Python et pybind11 :

```powershell
$pybind11_dir = python -c "import pybind11; print(pybind11.get_cmake_dir())"
cmake .. -DPYTHON_EXECUTABLE="C:\path\to\executable\python.exe" -Dpybind11_DIR="$pybind11_dir"
```

> Si tu travailles sur une autre machine ou avec une version Python différente, remplace le chemin par le résultat de :
> ```powershell
> Get-Command python | Select-Object -ExpandProperty Source
> ```

Compiler le module :

```powershell
cmake --build . --config Release
```

Copier le `.pyd` généré dans `main/` pour que Python puisse l'importer :

```powershell
copy Release\orbital_core.cp312-win_amd64.pyd ..\..\
```

### Lancer le simulateur

```powershell
cd ..\..
python main.py
```

### Notes

- Le fichier `.pyd` est lié à la version de Python utilisée à la compilation (`cp312` = Python 3.12). Si tu changes de version Python, il faut recompiler.
- Le dossier `build/` peut être supprimé et recréé sans risque si CMake se retrouve dans un état incohérent.
- Sur une nouvelle machine, il faut relancer les étapes CMake depuis le début (le `CMakeCache.txt` contient des chemins absolus qui ne sont pas portables).