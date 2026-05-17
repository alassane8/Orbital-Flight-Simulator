# Orbital Flight Simulator — Documentation Technique

> Simulateur de vol orbital temps-réel orienté physique de lancement, GNC et mécanique céleste.  
> Architecture modulaire Python/C++ · intégrateur RK4 · modèles ISA/Gravity Turn/Kepler/Hohmann · 3-DOF → 6-DOF

---

## Table des matières

1. [Vision du projet](#1-vision-du-projet)
2. [Architecture générale](#2-architecture-générale)
3. [Feuille de route](#3-feuille-de-route)
4. [Boucle de simulation](#4-boucle-de-simulation)
5. [Modèle atmosphérique ISA](#5-modèle-atmosphérique-isa)
6. [Dynamique de corps sous poussée — Phase atmosphérique](#6-dynamique-de-corps-sous-poussée--phase-atmosphérique)
7. [Traînée aérodynamique](#7-traînée-aérodynamique)
8. [Gravity Turn — Guidage de lancement](#8-gravity-turn--guidage-de-lancement)
9. [Intégrateur numérique — Runge-Kutta 4](#9-intégrateur-numérique--runge-kutta-4)
10. [Propagateur orbital Keplerien](#10-propagateur-orbital-keplerien)
11. [Perturbation J2 — Aplatissement terrestre](#11-perturbation-j2--aplatissement-terrestre)
12. [Manœuvre impulsionnelle — Delta-V](#12-manœuvre-impulsionnelle--delta-v)
13. [Transfert de Hohmann — Voyage Terre–Lune](#13-transfert-de-hohmann--voyage-terrelune)
14. [Extension 6-DOF — Dynamique d'attitude](#14-extension-6-dof--dynamique-dattitude)
15. [Portage C++ du noyau de calcul](#15-portage-c-du-noyau-de-calcul)
16. [Intégration Simulink](#16-intégration-simulink)
17. [Constantes et paramètres de référence](#17-constantes-et-paramètres-de-référence)

---

## 1. Vision du projet

Ce simulateur modélise le vol complet d'un lanceur depuis le décollage jusqu'à l'injection en orbite basse (LEO), puis le transfert vers la Lune via une manœuvre de Hohmann. Il couvre l'ensemble de la chaîne GNC (Guidance, Navigation & Control) :

- **G**uidance : calcul de la trajectoire cible (gravity turn, transfert orbital)
- **N**avigation : propagation de l'état (position, vitesse) par intégration numérique
- **C**ontrol : lois de commande d'attitude (phase 6-DOF)

Le projet est structuré en deux phases successives, reflétant la pratique industrielle :

| Phase | Modèle | Objectif |
|---|---|---|
| Phase 1 | **3-DOF point-masse** | Valider la trajectoire (position + vitesse) |
| Phase 2 | **6-DOF corps rigide** | Ajouter la dynamique de rotation (attitude) |

Cette progression reflète exactement la méthode employée chez ArianeGroup ou dans les équipes GNC d'Arianespace : on valide la mécanique orbitale avant d'ajouter la complexité de l'attitude.

---

## 2. Architecture générale

```
orbital_simulator/
├── core/
│   ├── atmosphere/         — Modèle ISA (densité, pression, température)
│   ├── aerodynamics/       — Traînée atmosphérique (phase de lancement)
│   ├── propulsion/         — Modèle de poussée et consommation d'ergols
│   ├── gravity/            — Gravité newtonienne + perturbation J2
│   └── integrator/         — Intégrateur RK4 (Python + C++ via pybind11)
├── gnc/
│   ├── guidance/
│   │   ├── gravity_turn/   — Loi de guidage atmosphérique
│   │   └── hohmann/        — Calcul des delta-V de transfert orbital
│   ├── navigation/
│   │   └── propagator/     — Propagateur Keplerien (éléments orbitaux → ECEF)
│   └── control/            — Contrôleur PD d'attitude (phase 6-DOF)
├── attitude/               — Quaternions, cinématique, équations d'Euler (phase 6-DOF)
├── mission/
│   ├── launch/             — Séquence décollage → LEO
│   └── transfer/           — Séquence LEO → Lune
├── visualization/          — Rendu matplotlib / pygame (trajectoire 3D, HUD)
└── main.py
```

**Séquence d'états mission :**

```
PRELAUNCH → IGNITION → VERTICAL_RISE → GRAVITY_TURN → STAGING
→ VACUUM_COAST → LEO_INSERTION → COAST → HOHMANN_BURN_1
→ TRANSFER_ORBIT → HOHMANN_BURN_2 → LUNAR_ORBIT
```

---

## 3. Feuille de route

### Phase 1 — 3-DOF Point-masse (MVP)

| Semaine | Objectif |
|---|---|
| S1 | Modèle ISA + dynamique atmosphérique + intégrateur RK4 |
| S2 | Gravity turn + visualisation trajectoire de lancement |
| S3 | Propagateur Keplerien + éléments orbitaux + perturbation J2 |
| S4 | Delta-V + transfert de Hohmann + visualisation orbite complète |

### Phase 2 — 6-DOF Corps rigide

| Semaine | Objectif |
|---|---|
| S5 | Quaternions + cinématique de rotation |
| S6 | Équations d'Euler + moments d'inertie |
| S7 | Contrôleur PD d'attitude (pointage) |
| S8 | Portage C++ du propagateur + binding pybind11 |

---

## 4. Boucle de simulation

La simulation avance par pas de temps fixes. L'intégrateur RK4 (§9) est appelé à chaque pas pour propager l'état du véhicule.

**Vecteur d'état 3-DOF :**

$$\mathbf{x} = \begin{pmatrix} \mathbf{r} \\ \mathbf{v} \end{pmatrix} \in \mathbb{R}^6$$

avec $\mathbf{r} = (x, y, z)$ la position en ECEF [m] et $\mathbf{v} = (\dot{x}, \dot{y}, \dot{z})$ la vitesse [m/s].

**Vecteur d'état 6-DOF (phase 2) :**

$$\mathbf{x} = \begin{pmatrix} \mathbf{r} \\ \mathbf{v} \\ \mathbf{q} \\ \boldsymbol{\omega} \end{pmatrix} \in \mathbb{R}^{13}$$

avec $\mathbf{q} \in \mathbb{R}^4$ le quaternion d'attitude et $\boldsymbol{\omega} \in \mathbb{R}^3$ la vitesse angulaire en rad/s.

**Paramètres de la boucle :**

| Paramètre | Phase atmosphérique | Phase orbitale |
|---|---|---|
| `dt` | 0.1 s | 1.0 s |
| Intégrateur | RK4 | RK4 |
| Référentiel | ECEF | ECI (inertiel) |

---

## 5. Modèle atmosphérique ISA

Identique au simulateur de trafic aérien pour la troposphère, étendu à la stratosphère pour couvrir les 80 km de la phase atmosphérique du lancement.

**Troposphère** ($h < 11\,000\,\text{m}$) :

$$\boxed{\rho(h) = 1.225 \times \max\!\left(0,\; 1 - 2.2558 \times 10^{-5}\, h\right)^{4.2561} \quad [\text{kg/m}^3]}$$

**Stratosphère** ($11\,000 \leq h < 25\,000\,\text{m}$) — couche isotherme à $T = 216.65\,\text{K}$ :

$$\rho(h) = 0.3639 \times e^{-\frac{h - 11000}{6341.6}} \quad [\text{kg/m}^3]$$

Au-delà de 80 km, la densité est considérée nulle : la traînée aérodynamique disparaît et le vol devient purement balistique/orbital.

**Fichier :** `core/atmosphere/isa_model.py` — `compute_density(h)`

---

## 6. Dynamique de corps sous poussée — Phase atmosphérique

Durant la phase atmosphérique, trois forces agissent sur le lanceur :

$$m\,\ddot{\mathbf{r}} = \mathbf{F}_{\text{thrust}} + \mathbf{F}_{\text{gravity}} + \mathbf{F}_{\text{drag}}$$

**Poussée** (dans la direction du vecteur de guidage $\hat{\mathbf{u}}$) :

$$\mathbf{F}_{\text{thrust}} = T \cdot \hat{\mathbf{u}}$$

où $T$ est la poussée moteur en Newtons (paramètre de la fusée).

**Gravité newtonienne** :

$$\mathbf{F}_{\text{gravity}} = -\frac{\mu\, m}{|\mathbf{r}|^3}\, \mathbf{r}$$

avec $\mu = G M_\oplus = 3.986 \times 10^{14}\,\text{m}^3/\text{s}^2$.

**Équation de la masse** — l'ergol se consume pendant la combustion (équation de Tsiolkovsky) :

$$\dot{m} = -\frac{T}{I_{sp}\, g_0}$$

avec $I_{sp}$ l'impulsion spécifique du moteur [s] et $g_0 = 9.80665\,\text{m/s}^2$.

**Fichier :** `core/propulsion/thrust_model.py`

---

## 7. Traînée aérodynamique

La traînée s'oppose au mouvement du lanceur dans l'atmosphère :

$$\mathbf{F}_{\text{drag}} = -\frac{1}{2}\, \rho(h)\, C_D\, A\, |\mathbf{v}_{\text{rel}}|^2 \cdot \hat{\mathbf{v}}_{\text{rel}}$$

| Symbole | Définition | Unité |
|---|---|---|
| $\rho(h)$ | Densité atmosphérique à l'altitude $h$ (§5) | kg/m³ |
| $C_D$ | Coefficient de traînée (0.3 pour un lanceur typique) | — |
| $A$ | Section frontale du lanceur | m² |
| $\mathbf{v}_{\text{rel}}$ | Vitesse relative à l'air (vitesse sol − vent atmosphérique) | m/s |

La traînée est calculée à chaque pas de temps et devient négligeable au-delà de 80 km d'altitude.

**Fichier :** `core/aerodynamics/drag_model.py`

---

## 8. Gravity Turn — Guidage de lancement

Le **gravity turn** est la manœuvre de guidage standard des lanceurs orbitaux. L'idée est d'incliner progressivement la trajectoire vers l'horizontale de façon à maximiser l'énergie orbitale tout en minimisant les contraintes aérodynamiques (angle d'attaque nul → pas de forces latérales sur la structure).

**Principe :** une fois lancé verticalement, le lanceur reçoit une légère inclinaison initiale $\delta\theta_0$. La gravité fait alors naturellement pivoter le vecteur vitesse — le pilote n'a qu'à aligner la poussée sur ce vecteur.

**Vecteur de guidage :**

$$\hat{\mathbf{u}} = \frac{\mathbf{v}}{|\mathbf{v}|}$$

Le vecteur de guidage est simplement la direction du vecteur vitesse courant. C'est la définition formelle du gravity turn : vol à angle d'attaque nul.

**Phases du guidage :**

| Phase | Durée | Action |
|---|---|---|
| Montée verticale | 0 → $t_{\text{tilt}}$ (≈ 10 s) | $\hat{\mathbf{u}} = \hat{\mathbf{z}}$ (vertical pur) |
| Inclinaison initiale | $t_{\text{tilt}}$ | Kick angle $\delta\theta_0 \approx 3°$ vers l'est |
| Gravity turn | $t_{\text{tilt}}$ → MECO | $\hat{\mathbf{u}} = \mathbf{v}/|\mathbf{v}|$ |

**Condition d'insertion orbitale (MECO) :**

Le moteur s'éteint (Main Engine Cut-Off) lorsque la vitesse horizontale atteint la vitesse circulaire à l'altitude courante :

$$v_{\text{circ}}(r) = \sqrt{\frac{\mu}{r}}$$

**Fichier :** `gnc/guidance/gravity_turn/gravity_turn_guidance.py`

---

## 9. Intégrateur numérique — Runge-Kutta 4

L'intégrateur est le moteur mathématique de la simulation. Il transforme les équations différentielles de la physique en une trajectoire discrète pas à pas. L'**Euler explicite** (la méthode naïve) accumule des erreurs trop rapidement pour une simulation orbitale. Le **RK4** est l'équilibre idéal : précis, stable, et peu coûteux.

Pour un vecteur d'état $\mathbf{x}$ régi par $\dot{\mathbf{x}} = f(t, \mathbf{x})$, le RK4 calcule :

$$k_1 = f(t_n,\; \mathbf{x}_n)$$
$$k_2 = f\!\left(t_n + \tfrac{h}{2},\; \mathbf{x}_n + \tfrac{h}{2} k_1\right)$$
$$k_3 = f\!\left(t_n + \tfrac{h}{2},\; \mathbf{x}_n + \tfrac{h}{2} k_2\right)$$
$$k_4 = f\!\left(t_n + h,\; \mathbf{x}_n + h\, k_3\right)$$

$$\boxed{\mathbf{x}_{n+1} = \mathbf{x}_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)}$$

avec $h = \Delta t$ le pas de temps.

L'erreur locale de troncature est $O(h^5)$, soit une précision radicalement supérieure à Euler ($O(h^2)$).

**Ce module est le premier candidat au portage C++** (§15) : il est appelé des millions de fois et son coût de calcul domine le temps total de simulation.

**Fichiers :** `core/integrator/rk4.py` (Python) → `core/integrator/rk4.cpp` (C++)

---

## 10. Propagateur orbital Keplerien

Une fois en orbite (moteurs éteints, hors atmosphère), le mouvement est régi par la seule gravité. Le problème à deux corps (fusée + Terre) a une solution analytique exacte : les **orbites kepléeriennes**.

**Éléments orbitaux classiques** (6 paramètres qui définissent complètement l'orbite) :

| Élément | Symbole | Définition |
|---|---|---|
| Demi-grand axe | $a$ | Taille de l'orbite |
| Excentricité | $e$ | Forme (0 = cercle, 1 = parabole) |
| Inclinaison | $i$ | Angle par rapport à l'équateur |
| RAAN | $\Omega$ | Longitude du nœud ascendant |
| Argument du périapside | $\omega$ | Orientation de l'ellipse |
| Anomalie vraie | $\nu$ | Position sur l'orbite à $t_0$ |

**Conversion éléments orbitaux → vecteur d'état ECEF :**

Position dans le plan orbital (repère périfocal) :

$$\mathbf{r}_{\text{peri}} = \frac{a(1-e^2)}{1 + e\cos\nu} \begin{pmatrix} \cos\nu \\ \sin\nu \\ 0 \end{pmatrix}$$

La rotation vers le référentiel inertiel ECI est donnée par la matrice $R(\Omega, i, \omega)$ (rotations successives en $z$, $x$, $z$).

**Propagation temporelle — Équation de Kepler :**

Pour passer de $\nu(t_0)$ à $\nu(t)$, on résout itérativement l'équation de Kepler :

$$M = E - e\sin E$$

avec $M = n(t - t_p)$ l'anomalie moyenne, $n = \sqrt{\mu / a^3}$ le mouvement moyen, et $E$ l'anomalie excentrique. La résolution se fait par la méthode de Newton-Raphson (converge en 3-5 itérations).

**Fichier :** `gnc/navigation/propagator/kepler_propagator.py`

---

## 11. Perturbation J2 — Aplatissement terrestre

La Terre est légèrement aplatie aux pôles (oblateness). Son potentiel gravitationnel n'est pas parfaitement sphérique. La première correction — le terme $J_2$ — est de loin la plus importante et modifie la trajectoire orbitale sur quelques orbites.

**Accélération perturbatrice due à $J_2$** (en coordonnées ECEF, $r = |\mathbf{r}|$, $z$ = composante polaire) :

$$\mathbf{a}_{J_2} = \frac{3\mu J_2 R_\oplus^2}{2 r^5} \begin{pmatrix} x\!\left(5\frac{z^2}{r^2} - 1\right) \\ y\!\left(5\frac{z^2}{r^2} - 1\right) \\ z\!\left(5\frac{z^2}{r^2} - 3\right) \end{pmatrix}$$

avec $J_2 = 1.08263 \times 10^{-3}$ (coefficient d'aplatissement terrestre) et $R_\oplus = 6\,378\,137\,\text{m}$.

**Effet principal :** précession du plan orbital — le nœud ascendant $\Omega$ tourne lentement :

$$\dot{\Omega} = -\frac{3}{2} n J_2 \left(\frac{R_\oplus}{a}\right)^2 \frac{\cos i}{(1 - e^2)^2}$$

Les orbites héliosynchrones (comme celles des satellites d'observation) exploitent cette précession pour que le plan orbital suive le Soleil.

**Fichier :** `core/gravity/j2_perturbation.py`

---

## 12. Manœuvre impulsionnelle — Delta-V

En mécanique orbitale, changer d'orbite revient à modifier le vecteur vitesse à un instant précis. On modélise cela par une **impulsion instantanée** $\Delta\mathbf{v}$ (approximation valide si la durée de combustion est petite devant la période orbitale).

**Équation de Tsiolkovsky — masse d'ergol nécessaire :**

$$\boxed{\Delta v = I_{sp}\, g_0 \ln\!\frac{m_0}{m_f}}$$

D'où la masse d'ergol consommée :

$$m_{\text{prop}} = m_0 \left(1 - e^{-\Delta v / (I_{sp}\, g_0)}\right)$$

| Symbole | Définition |
|---|---|
| $m_0$ | Masse avant la manœuvre |
| $m_f$ | Masse après la manœuvre |
| $I_{sp}$ | Impulsion spécifique du moteur [s] |
| $\Delta v$ | Module de la variation de vitesse [m/s] |

**Application dans la simulation :** à chaque manœuvre, le vecteur vitesse est mis à jour instantanément et la masse du véhicule est réduite de $m_{\text{prop}}$.

**Fichier :** `gnc/guidance/hohmann/delta_v.py`

---

## 13. Transfert de Hohmann — Voyage Terre–Lune

Le **transfert de Hohmann** est la manœuvre la plus économique (en delta-V) pour passer d'une orbite circulaire à une autre. Il consiste en deux impulsions moteur aux extrémités d'une ellipse de transfert.

**Orbites impliquées :**

| Orbite | Rayon | Description |
|---|---|---|
| $r_1$ | $R_\oplus + 200\,\text{km} \approx 6\,571\,\text{km}$ | Orbite basse initiale (LEO) |
| $r_{\text{transfer}}$ | ellipse de $r_1$ à $r_2$ | Orbite de transfert |
| $r_2$ | $384\,400\,\text{km}$ | Distance Terre–Lune |

**Premier delta-V** (injection sur l'ellipse de transfert, au périgée) :

$$\Delta v_1 = \sqrt{\frac{\mu}{r_1}} \left(\sqrt{\frac{2 r_2}{r_1 + r_2}} - 1\right)$$

**Second delta-V** (circularisation à l'apogée, insertion orbitale lunaire) :

$$\Delta v_2 = \sqrt{\frac{\mu}{r_2}} \left(1 - \sqrt{\frac{2 r_1}{r_1 + r_2}}\right)$$

**Delta-V total :**

$$\Delta v_{\text{total}} = \Delta v_1 + \Delta v_2$$

**Durée du transfert** (demi-période de l'ellipse de transfert) :

$$\boxed{t_{\text{transfer}} = \pi \sqrt{\frac{(r_1 + r_2)^3}{8\mu}} \approx 4.9\,\text{jours}}$$

**Fichier :** `gnc/guidance/hohmann/hohmann_transfer.py`

---

## 14. Extension 6-DOF — Dynamique d'attitude

La phase 6-DOF ajoute 7 variables d'état ($\mathbf{q}$ et $\boldsymbol{\omega}$) et modélise comment la fusée tourne sous l'effet des couples moteurs.

### 14.1 Représentation par quaternions

Les quaternions évitent le **gimbal lock** (singularité des angles d'Euler à $\pm 90°$) et sont numériquement stables. Un quaternion unitaire $\mathbf{q} = (q_0, q_1, q_2, q_3)$ avec $|\mathbf{q}| = 1$ représente une rotation 3D.

**Cinématique — équation différentielle du quaternion :**

$$\dot{\mathbf{q}} = \frac{1}{2} \mathbf{q} \otimes \begin{pmatrix} 0 \\ \boldsymbol{\omega} \end{pmatrix}$$

avec $\otimes$ le produit quaternionique et $\boldsymbol{\omega}$ la vitesse angulaire exprimée dans le repère corps.

La norme est renormalisée à chaque pas de temps pour compenser les erreurs numériques : $\mathbf{q} \leftarrow \mathbf{q} / |\mathbf{q}|$.

### 14.2 Équations d'Euler — dynamique de rotation

La rotation d'un corps rigide est régie par les **équations d'Euler** :

$$\mathbf{I}\, \dot{\boldsymbol{\omega}} = \boldsymbol{\tau} - \boldsymbol{\omega} \times (\mathbf{I}\, \boldsymbol{\omega})$$

| Symbole | Définition |
|---|---|
| $\mathbf{I} = \text{diag}(I_x, I_y, I_z)$ | Tenseur d'inertie du lanceur [kg·m²] |
| $\boldsymbol{\tau}$ | Couple extérieur (propulsion, tuyères de contrôle d'attitude) [N·m] |
| $\boldsymbol{\omega}$ | Vitesse angulaire dans le repère corps [rad/s] |

Le terme $\boldsymbol{\omega} \times (\mathbf{I}\, \boldsymbol{\omega})$ est le couple gyroscopique — il est responsable de la précession des toupies et des effets de couplage entre axes.

### 14.3 Contrôleur PD d'attitude

Un contrôleur **Proportionnel-Dérivé** minimise l'erreur entre l'attitude cible $\mathbf{q}_{\text{cible}}$ et l'attitude courante $\mathbf{q}$ :

$$\boldsymbol{\tau} = -K_p\, \mathbf{e}_q - K_d\, \boldsymbol{\omega}$$

L'erreur d'attitude $\mathbf{e}_q$ est extraite de la partie vectorielle du quaternion d'erreur $\mathbf{q}_{\text{err}} = \mathbf{q}_{\text{cible}}^{-1} \otimes \mathbf{q}$.

**Fichiers :** `attitude/quaternion.py`, `attitude/euler_dynamics.py`, `gnc/control/pd_attitude_controller.py`

---

## 15. Portage C++ du noyau de calcul

Dans l'industrie (ArianeGroup, MBDA, Airbus Defence), les simulateurs temps-réel sont écrits en C++ pour les performances, avec des interfaces Python pour l'analyse et la visualisation. Ce projet reproduit cette architecture.

**Modules portés en C++ :**

| Module | Raison |
|---|---|
| Intégrateur RK4 | Appelé à chaque pas de temps — nœud critique |
| Propagateur Keplerien | Résolution de Kepler iterative — coûteux |
| Calcul J2 | Vectoriel pur — vectorisable |

**Binding Python via pybind11 :**

```cpp
// core/integrator/rk4.cpp
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

Eigen::VectorXd rk4_step(
    std::function<Eigen::VectorXd(double, Eigen::VectorXd)> f,
    double t, Eigen::VectorXd x, double dt) {
    auto k1 = f(t, x);
    auto k2 = f(t + dt/2, x + dt/2 * k1);
    auto k3 = f(t + dt/2, x + dt/2 * k2);
    auto k4 = f(t + dt,   x + dt   * k3);
    return x + dt/6 * (k1 + 2*k2 + 2*k3 + k4);
}

PYBIND11_MODULE(orbital_core, m) {
    m.def("rk4_step", &rk4_step, "RK4 integrator step");
}
```

Usage depuis Python :

```python
import orbital_core
x_next = orbital_core.rk4_step(dynamics_fn, t, x, dt)
```

**Gain de performance mesuré attendu :** ×10 à ×50 sur les longues simulations orbitales.

**Fichiers :** `core/integrator/rk4.cpp`, `CMakeLists.txt`, `core/integrator/rk4_binding.py`

---

## 16. Intégration Simulink

Simulink (MathWorks) est l'outil standard de l'industrie GNC pour prototyper et valider les lois de guidage et de contrôle sous forme de blocs graphiques, avant de les auto-coder en C embarqué.

**Ce qui est modélisé dans Simulink dans ce projet :**

Le **contrôleur PD d'attitude** (§14.3) est implémenté en parallèle dans Simulink :

```
[q_target] → [Quaternion Error] → [PD Controller] → [Torque]
[q_current] ↗                                     ↘
[omega] ──────────────────────────────────────────→ [Euler Dynamics] → [omega_dot]
```

**Workflow de validation croisée :**

1. Implémenter le contrôleur en Python (référence)
2. Reproduire le même contrôleur dans Simulink
3. Comparer les sorties sur les mêmes conditions initiales → les courbes doivent se superposer
4. Exporter le code C généré par Simulink (`Embedded Coder`) pour comparaison avec le C++ manuel

Cette démarche démontre la maîtrise du **workflow industriel GNC complet** : prototype Python → validation Simulink → code embarqué C.

**Accès Simulink :** MATLAB Online (compte étudiant ECE — licence gratuite) ou MATLAB R2024b local.

---

## 17. Constantes et paramètres de référence

| Constante | Symbole | Valeur | Source |
|---|---|---|---|
| Paramètre gravitationnel terrestre | $\mu$ | $3.986 \times 10^{14}$ m³/s² | IAU 2012 |
| Rayon équatorial terrestre | $R_\oplus$ | $6\,378\,137$ m | WGS84 |
| Accélération standard | $g_0$ | $9.80665$ m/s² | ISO 80000-3 |
| Coefficient J2 | $J_2$ | $1.08263 \times 10^{-3}$ | EGM2008 |
| Distance Terre–Lune | $d_{\text{Lune}}$ | $384\,400$ km | moyenne |
| Paramètre gravitationnel lunaire | $\mu_{\text{Lune}}$ | $4.905 \times 10^{12}$ m³/s² | — |
| Densité au sol ISA | $\rho_0$ | $1.225$ kg/m³ | ISA MSL |
| Température au sol ISA | $T_0$ | $288.15$ K | ISA MSL |
| Gradient thermique troposphère | $\Lambda$ | $0.0065$ K/m | ISA |
| Constante des gaz, air sec | $R$ | $287.058$ J/(kg·K) | — |
| Impulsion spécifique Ariane 5 (Vulcain 2) | $I_{sp}$ | $431$ s | ArianeGroup |
| Poussée Vulcain 2 (vide) | $T$ | $1\,340\,000$ N | ArianeGroup |

---

*Document de spécification — les formules reflètent les modèles à implémenter.*
*Progression recommandée : implémenter dans l'ordre des sections, valider chaque module avec des tests unitaires avant de passer au suivant.*