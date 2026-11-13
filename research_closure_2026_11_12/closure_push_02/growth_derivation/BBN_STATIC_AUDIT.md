# Independent audit of the unchanged-FRW radiation budget and static repair bound

This audit is separate from the corrected growth operator. It does not restore the withdrawn isolated-fluid growth floor. It checks whether the specified perspective repair can obey two **declared, conditional requirements** while preserving the same homogeneous clock history and the stated weak-field annulus.

## 1. Exact clock contribution versus a declared radiation proxy

For `F=mu^2(Q-1)^2/(2K)`, `K=4piG`, homogeneous charge conservation gives `n=n0 a^-3`. Therefore

```text
rho_clock = n0 a^-3 + K n0^2/(2mu^2) a^-6,
rho_stiff = K n0^2/(2mu^2) a^-6.
```

Define the present **dust coefficient** by `n0=Omega_d rho_crit0`, with `rho_crit0=3H0^2/(2K)`. Then `I0=2K n0=3H0^2 Omega_d`. For the proxy `rho_r=Omega_r rho_crit0 a^-4`,

```text
rho_stiff/rho_r = Omega_d I0/(4 mu^2 Omega_r a^2).             (1)
```

This is exact for the specified homogeneous clock and radiation scaling; it does not require a cold early clock. Indeed the clock is very far from cold for the low-mu case at this epoch. The perspective repair keeps `H(Q,0)=F(Q)` and all its compensator terms vanish on homogeneous Pi=0, so it retains (1).

The frozen KD1 proxy selects `epsilon_r=0.067`, `T=0.1 MeV`, `T0=2.7255 K`, and `a_star=1/(1+T/(k_B T0))` with `k_B=8.617333262e-5 eV/K`. This last convention differs negligibly from `k_B T0/T`, but neither is a complete entropy/thermal-history calculation. The proxy implies

```text
mu >= sqrt[Omega_d I0/(4 epsilon_r Omega_r a_star^2)].        (2)
```

The independent calculation uses the pinned KD1 canonical and alternative inputs, checks `I0=3H0^2 Omega_d`, and also reconstructs (1) directly from `n0`, `rho_crit0` and the action energy. For the canonical inputs it reproduces `mu>=8.8901135e6 Mpc^-1`. At the background-coldness value `mu=198.2542`, the ratio in (1) is about `1.347e8`; at the old growth value `mu=25118.8643` it is about `8392.46`.

This is **not a new empirical BBN likelihood or a precision measured mu bound**. The adopted 0.067 is a frozen gate. Standard BBN is sensitive to the expansion history over a temperature interval, and a stiff component scales differently from an extra relativistic species. Its ratio to radiation changes as `a^-2`; converting its value at one epoch into a constant Delta N_eff through BBN is unjustified. Photon heating during electron-positron annihilation also requires entropy accounting for precision T-to-a conversion. A reaction network, the thermal history, abundance data, and their uncertainties would be needed for a quantitative BBN likelihood.

Primary convention checks: the PDG [2025 Big-Bang Cosmology review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-bbang-cosmology.pdf), equations (22.40)–(22.42) and (22.49)–(22.51), gives radiation thermodynamics and entropy/photon heating. The PDG [2025 Big Bang Nucleosynthesis review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-bbang-nucleosynthesis.pdf), section 24.2, explains expansion-rate sensitivity at weak freeze-out and subsequent nuclear formation. These sources support the physical interpretation and caveats, not the chosen 0.067 number or a QX17 likelihood.

## 2. Independent static bound, permitting deformation of P

For the same perspective repair, let `Q in [1,Qmax]`, `Pi>=0` be an independently admissible rectangular domain. Retain the original W, require concavity in Pi there, and set the compensator value and first derivative to zero at Pi=0. Impose the annular clock-energy fraction ceiling `delta=(mu_gal/mu)^2`, with the declared target `mu_gal=1 Mpc^-1`. In formulas below mu is numerically measured in Mpc^-1.

The finite-Q-band argument gives

```text
K B_band >= (Qmax-1)^2/[2 Qmax (-log(1-delta))],
I_delta = 3 exp(-2/3) - (1-3log(delta))delta,
K mean(p) >= K B_band I_delta =: P_floor(mu).                (3)
```

Here `S<=delta` is forced by the energy ceiling itself. Thus the finite-Pi moment bound yielding `I_delta` applies at every actual annular Pi. No unperturbed AQUAL Pi profile is used in (3). The normal density is nonnegative: the repaired clock energy is a nonnegative fraction of the quadratic-clock energy at Q>=1, and Pi, W and the original active stiffness contribute nonnegative terms. On the P shell the W terms cannot lower the mean pressure, since `P W_P>=2W>=0`.

For a static metric with vanishing shift, Einstein's normal-normal Ricci equation gives `D^2 N=N[K(rho+3mean(p))-Lambda]`. Therefore the specified weak spatial geometry obeys the necessary lapse-flux bound

```text
R^2 N'(R)-r1^2 N'(r1)
 >= [P_floor(mu)-Lambda/3] Nmin (R^3-r1^3),                 (4)
```

where the bracket is positive in the evaluated cases. The weak-geometry approximation and prescribed Q/force boundary values remain hypotheses. The bound allows deformed P; it excludes an extra compensating negative-active-energy sector. A positive Lambda is included explicitly.

The function `P_floor` is strictly increasing for `mu>exp(1/3)` in these units. To see this, set `T=-log(1-delta)` and `I=I_delta`: on `0<delta<exp(-2/3)`, `I>0`, `I'=2+3log(delta)<0`, and `T'>0`, so `(I/T)'<0`. Since delta decreases with mu, the floor increases. A scalar root of equality in (4) is consequently a genuine necessary upper endpoint for this class and target.

An independent bisection using only pinned matching endpoints, not the static agent's solver, reproduces the reported ceilings: `435.3271 Mpc^-1` for Lambda=0; `445.3183` for Lambda=`1e-7 Mpc^-2`; `446.3052` for Lambda=`1.1e-7 Mpc^-2`. These are necessary ceilings, not constructed viable solutions below them. The separate stronger test of the particular quiet P profile is not needed for this conclusion.

## 3. Conditional incompatibility and what would change it

Equations (2) and (4) have no common mu for the same canonical dust normalization, unchanged homogeneous charge history, declared radiation gate, specified energy suppression, rectangular concavity requirement and static target. The conclusion survives the illustrated Lambda contribution. It does not depend on the withdrawn 25120 growth bound.

At the largest of these static ceilings, satisfying the frozen early radiation budget would require the early comoving clock charge to be at most roughly `5.02e-5` of the present dust coefficient: (1) scales quadratically with that charge. The unchanged homogeneous conservation law supplies no such later production. Introducing charge production, another homogeneous action, a different thermal history, a correlated state domain, a different annulus or extra stress changes the premises and requires a new derivation.

This closes the specified unchanged-history repair as a joint solution of these conditional requirements. It is not an all-theory no-go, a fit to primordial abundances, or a reason to keep an incorrect historical growth operator.

## 4. Evidence and independent code review

`check_bbn_static.py` independently reconstructs the homogeneous energy and radiation ratio, checks the pinned KD1 numerical normalizations, and uses bisection on (3)–(4) to compare the static ceilings. Its canonical bounded run is separate from the growth run. It does not import either companion agent's numerical driver.

Read-only review of `growth_gate_audit/growth.py` found the ordering `(delta_b,delta_b',delta_d,delta_d')`, Hubble drag, Poisson normalization, unsuppressed baryon forcing and independent midpoint matrix consistent with the derivation in this lane. Matched Meszaros initial data, smooth radiation in the background and zero radiation perturbations are declared diagnostic choices; they do not produce a pre-recombination adiabatic transfer function. No sign or factor error was found in that bounded system.
