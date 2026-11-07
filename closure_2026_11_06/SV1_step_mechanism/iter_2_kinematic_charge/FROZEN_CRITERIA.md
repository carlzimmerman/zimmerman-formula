# SV1 iter_2: can a scalar the action already carries (the switched-stiffness charge, or the khronon's response to the matter flow) separate hot from cold systems? FROZEN CRITERIA

Frozen before any script or graded number, together with iter_1's (run only as the next mechanism if iter_1 is short).
Rules: SWARM_BRIEF.md. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Both footings, never pooled.

## The two keys (both already in the action; no new constant)
- K_Pi, the khronon / stiffness charge Pi = D.P + 2X (AC2q; v3s is X = 0). For a stationary source the switched
  stiffness leaves the statics unchanged and D.P = 0 at static order (EQUATIONS_IN_ORDER.md 8.3, 9.1), so
  Pi = 2X = s^2/N^2 with N = 1 + Phi/c^2. Its only variation between systems is the depth: dPi/Pi = -2 Phi/c^2 (to first
  order). So any multiplier F(Pi) on the phantom is a monotone function of the depth |Phi|/c^2 (QX20 V6, QX5 class a key).
- K_v, the khronon's response to the matter flow. Matter couples minimally (S_m); a rotating disc and a pressure-supported
  system of equal rho differ only in T^{0i} and T^{ij}, which enter the weak-field equations at relative order v^2/c^2
  (rotation) or sigma^2/c^2 (pressure). The key is k_v = v^2/c^2 with v = the measured circular speed (QX20 V2, v_obs)
  for every class (for hot systems v_obs^2 = G M_obs / r, the virial speed of the support).

## Tests
- T1 overlap (sandwich): for each key, count SPARC and hot points inside the common key range, per footing, from QX20's
  build() (read-only). If they overlap and the hot points in the overlap sit above SPARC by more than SPARC's G line
  (0.057 dex, QX20 Z line) plus 2 sigma of the hot class, QX5_monotone_sandwich.mono_dead applies: no monotone F of the
  key exists. Label DEAD for the key. An antitone F is checked the same way (anti_dead).
- T2 amplitude (K_v only): with an O(1) coefficient the term moves g by <= k_v. Needed coefficient
  C_need,c = (10^Delta_c - 1)/median(k_v,c) per class (Delta_c as in iter_1). If C_need > 100 for every class, the
  mechanism needs a new large constant set by the hot classes (CLUSTER-SET = FAIL, no-tuning rule); then the SPARC check:
  the same C applied to SPARC's own k_v must move SPARC's mean by <= 0.057 dex, else it also BREAKS SPARC.
- T3 support (K_v at fixed M and sigma): QX22's measured D = +0.002 +- 0.045 ln (dispersion- vs rotation-supported red
  galaxies at fixed M*, sigma) is carried, not recomputed; a K_v term that separates rotation from pressure predicts
  the support split and is graded against it there.

## Labels
- Per key per footing: DEAD (T1 fires), or CLUSTER-SET (T2), or ALIVE.
- iter_2 label: NO-GO IN CLASS (terms carried by Pi or by T^{0i}/T^{ij} with no new constant) if both keys are DEAD or
  CLUSTER-SET on both footings.

## Controls
- KA1: QX20's overlap counts for V2 and V6 (48 / 522 canonical, 535 alt for V6) reproduced exactly.
- MUTATE M1 (plant a cluster-only key: hot keys x 1e10): the overlap must vanish and T1 must read not-DEAD. Bites if so.
- MUTATE M2 (Newton): SPARC's mean offset must move by > 0.3 dex (the loaders see the law). Bites if so.

Kappa = 1/2 FITTED; not theory closed.
