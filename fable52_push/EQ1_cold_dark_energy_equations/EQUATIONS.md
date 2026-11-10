# The equations of the cold dark energy, in one place (2026-11-10)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered. **A reference sheet, not a lane and not a new
result.** It collects every equation the record has for the cold component under the owner's form B (the a0 law with
cold dark energy counted once), says where each comes from, and says which questions the equations do not answer.

Status tags: **[C]** certified in a lane of the record (named); **[H]** hand algebra checked symbolically
(`eq1_check.py` here, or the FB1 note's check); **[M]** measured; **[X]** the equations do not give this.

Units c = 1 unless shown, K = 4 pi G. Footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt), never pooled.

## 1. What the cold dark energy is

In the adopted action the non-gravitational, non-baryonic sector is one clock field tau (unit normal n, rate Q) and a
polarization P on the clock's leaves. Its gravitating density, seen by the clock's observers, is **[C: QX17 K5]**

    rho_c = (mu_K^2 / 2K)(Q^2 - 1) + W(K|P|) + Pi + gamma_L F(Pi),      Pi = D_m P^m ,

which in the weak field is

    rho_c = D.P + n_d ,        n_d = mu_K^2 (Q - 1) / K .

D.P is the law's halo. n_d is the clock's dust. Both belong to one conserved charge (section 2, E3). That is what "counted
once" means in equations.

## 2. The covariant equations [C: QX17, action (A); all certified there]

    S = Int sqrt(-g) { [R - 2 Lambda + 2 mu_K^2 (Q - 1)^2] / (4K) + P^m A_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m } + S_m

    W(p) = (a0^2 / K) [ -p/a0 - ln(1 - p/a0) ],   F(Pi) = [max(Pi, 0)]^2 / 2,   gamma_L = K Lstar^2 / 2,
    Q = sqrt(-g^{mn} d_m tau d_n tau),   n_m = -d_m tau / Q,   A_m = n^n nabla_n n_m .

- **(E1)** n^m P_m = 0.
- **(E2), the law.** On the leaves: (1 + gamma_L Pi_+) A_m + gamma_L D_m Pi_+ = K W'(K|P|) Phat_m. At gamma_L = 0 this
  is K|P| = a0 u / (1 + u), u = |A| / a0.
- **(E3), conservation.** nabla_m [ n^m rho_Q - lambda P^m / Q ] = 0, with
  rho_Q = nabla_m[(1 + gamma_L Pi_+) P^m] / Q + mu_K^2 (Q - 1) / K, to leading order D.P + n_d.
- **(E4), gravity.** G_mn + Lambda g_mn = 2K (T^matter + T^Q + T^W + T^P), stresses as printed in QX17.
- **(E5), baryons.** Minimal coupling: baryons fall on geodesics.
- **(E6)** The sector's stress is conserved on shell; the Bianchi identity holds.

Eliminating P at gamma_L = 0 gives the law's Lagrangian **[C: QX17 K0]**

    J(|A|) = (a0^2 / K) [ u - ln(1 + u) ] .

## 3. The expanding background [C: QX17 limits; MK1]

With P = 0: n_d a^3 = constant. Writing I0 = 8 pi G rho_c0 (in c = 1 units, 3 (H0/c)^2 Omega_c):

    Qbar - 1 = I0 / (2 mu_K^2 a^3),     w = w0 / (w0 + a^3),     w0 = I0 / (4 mu_K^2),
    c_s^2 = (Qbar - 1) / Qbar,          Jeans wavenumber k_J = mu_K (physical)   [C: MK1 row 2, QX3].

Numbers **[C: MK1]**: I0 = 4.037e-8 per Mpc^2; cold by z 3400 (w at most 0.01) needs mu_K at least 198 per Mpc; the
record's CMB-lensing Jeans line needs 2.5e4.

## 4. Small disturbances

- **About the background, law on [C: TPA1 4.4]:** omega^2 = -K nbar [1 - k^2 / (mu_K^2 + k^2)], so the clock's own
  density grows at rate^2 K nbar / (1 + k^2 / mu_K^2). Below the scale 1/mu_K the law cancels the clock's self-gravity.
  Law off: the Jeans form K nbar (1 - k^2 / mu_K^2).
- **About a static galaxy, gravity coupled [C: SCS1]:** omega^2 = K G [(1 - K m) k^2 - mu_K^2 Qbar^2] / (mu_K^2 Qbar^2 + K m k^2),
  with G = Qbar n_d + D.P (m as defined in SCS1's RESULT.md). At mu_K = 0 it tends to D.P (1 - K m) / m at high k.
  Stable wherever the halo density D.P is positive: point masses (SCS1) and isolated discs (SCS2).

## 5. The static weak field, any geometry

    K P = (1 - mu) grad Phi,   mu(u) = u / (1 + u),   u = |grad Phi| / a0                       [C: QX17]
    div[ mu grad Phi ] + mu_K^2 Phi = K rho_b                                                    [C: QX17]
    rho_c = D.P + n_d,   n_d = -mu_K^2 Phi / K   (static clock)                                 [C: QX17; TPA1 4.5]
    Poisson: lap Phi = K (rho_b + rho_c)                                                         [C: QX17]

The halo is held by the law's own stress **[H: FB1 note; re-checked independently by the closure session]**:

    Pi_ij = J(g) delta_ij - g_i g_j / (K (1 + u)),       d_j Pi_ij = (D.P) g_i .

With the screening on **[C: QX17]**: (1 + gamma_L Pi_+) grad Phi + gamma_L grad Pi_+ = K W' Phat.

## 6. Around a round galaxy of baryon mass M_b (mu_K = 0, gamma_L = 0) [H: `eq1_check.out`, all pass]

Scales: r_M = sqrt(G M_b / a0), x = r / r_M, g_N = G M_b / r^2 = a0 / x^2.

| Quantity | Equation |
|---|---|
| The law | g_N = g^2 / (g + a0), i.e. g = g_N [1/2 + sqrt(1/4 + a0 / g_N)] |
| The cold component's pull | g_c = g - g_N = a0 g / (g + a0); equivalently g_c g = a0 g_N. It never exceeds a0 |
| Enclosed cold mass | M_c(<r) = M_b X(x), X = [sqrt(1 + 4 x^2) - 1] / 2 = M_b a0 / g |
| Density | rho_c = (M_b / (4 pi r_M^3)) 2 / (x sqrt(1 + 4 x^2)) |
| Strong field (x much less than 1) | rho_c = a0 / (2 pi G r): one column density a0 / (2 pi G) for every galaxy |
| Weak field (x much more than 1) | rho_c = sqrt(G M_b a0) / (4 pi G r^2): an isothermal halo |
| Flat speed | v^4 = G M_b a0 |
| Pressure that holds it (isotropic form) | P = J(g); in the weak field P = rho_c sigma^2 with sigma^2 = (1/2) sqrt(G M_b a0) |
| Where the halo ends, for a share X_s | x_t^2 = X_s (X_s + 1); beyond it g = G M_b (1 + X_s) / r^2 [C: ONE1 Lean] |
| Far-field lensing against the law | 4 (1 + X_s) / (pi u_r), u_r = r / r_M [C: ONE1 Lean] |

With the owner's relation a0 = (1/2) c sqrt(G rho_DE) **[H]**: the pressure scale a0^2 / (8 pi G) = rho_DE c^2 / (32 pi),
and the column density a0 / (2 pi G) = c sqrt(rho_DE / G) / (4 pi) (106.9 and 129.2 Msun/pc^2 on the two footings,
from the SHAPE_search route D note).

## 7. What is measured [M]

- **SHP1:** everything that is not baryons follows X(x) of section 6 on SPARC rotation curves, within 0.057 / 0.021 dex
  in every bin from x = 0.18 to 10. KiDS's published isolated lenses sit 1.40 / 1.28 times the law.
- **ONE1:** with a share of 59.5 M_b and neighbours carrying it, host-free KiDS lenses pass at the widest veto; so does
  the law with no end.

## 8. What the equations do not give [X]

| Question | State | Lane |
|---|---|---|
| One value of mu_K for the CMB and for galaxies | none exists for this dust term | MK1 |
| A different one-variable dust term | the exponential one fails on clusters and groups | MK2 |
| How the charge gets from dust to halo | a cold clock folds and the equations stop | COL1 |
| The law out to where lensing sees it | the folded region stops 1.3 to 5.4 times short | FLD1 |
| A law that does not need a static clock | unstable (fourth order in time) | REL1 |
| Clusters and groups | a static clock gives the law plus -mu_K^2 Phi / K, which leaves X-COP short | QX2, MK1 |
| The share X_s | an input rule (PD1's 59.5 M_b), not an output | PD1, ONE1 |
| The number kappa = 1/2 | fitted | the record's kappa ledger |
| Why J has this form between its two ends | not derived (four attempts) | SHAPE_search |
| A disc in an external field | reads slowly unstable; no verdict | SCS2, SCS3 |

So the equations above describe the cold dark energy completely where it is settled, and say nothing about how it
settles. Two lanes are testing ways around that (KDE1, GRW1).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
