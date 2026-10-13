# CFG657 FROZEN CRITERIA: a derived cold-energy capture rule for the NGC 1052 trail (DF2, DF4, DF9) and LEDA 4014647

Committed ALONE, before the script exists and before any capture fraction is computed for the four galaxies.

## Purpose

CFG655 (criteria 0207b6abe, result ec4a7d14d) passed DF2/DF4/DF9 Newtonian (no cold-energy supply) and LEDA 4014647 on
the law (own supply) ONLY with van Dokkum+22's pre-kinematic labels. Its partial-supply bounds (R2, Z = +2, can / alt):
f_s <= 0.36 / 0.33 (DF2), 0.29 / 0.26 (DF4), 0.52 / 0.46 (DF9). This lane derives, with no new constant, how much cold
energy a dwarf that condensed from collision gas can capture, and asks whether that derived fraction alone reproduces
CFG655's labels for all four galaxies, without using any measured dispersion as an input.

## Honest status of blinding

The four dispersions and CFG655's bounds are known. CFG655's Rule A (age) and Rule M (trail membership) outcomes are known
(both fail). No capture fraction has been computed for any of the four galaxies. Order-of-magnitude expectations were
reasoned in planning (escape speeds of 10-30 km/s against ambient speeds of 100-300 km/s); they are not results.

## Framework inputs (Theory v2, THEORY_v2_CANDIDATE_2026-10-12.md; CFG541)

- Law: g = nu_mono(g_N/a0) g_N, both footings a0 = 9.3603e-11 / 1.1312e-10 m/s^2 (never pooled), kernel copied from CFG655.
- Target (A5): M_tgt(<r_1/2) = (nu(r_1/2) - 1) M_b/2 (CFG655's estimator: f_s is a fraction of this).
- Supply (A3, A6): cold energy accompanies baryons at Omega_c/Omega_b = 5.364 in a host's catchment.
- Settled halo of a host with condensed baryons M_b: isothermal, rho = V_f^2/(4 pi G r^2), V_f = (G M_b a0)^(1/4),
  1-D dispersion V_f/sqrt(2), out to the exhaustion radius r_* = r_M / ln(1 + 1/5.364), r_M = sqrt(G M_b/a0)
  (CFG541 T2a point-mass edge with f_ret = 1); beyond r_*, Kepler with M_tot = 6.364 M_b. Escape speed
  v_esc^2(r) = 2[V_f^2 ln(r_*/r) + G M_tot/r_*] for r < r_*.
- Settling drift (CFG541 eq. 5): v_s = alpha tau_ff grad psi, tau_ff = (4 pi G rho_m)^(-1/2), grad psi = deficit field.
  Energy handed off per unit mass (CFG542): dE/dt = alpha tau_ff |grad psi| |grad Phi|. alpha is free O(1) in the record:
  bracket [0.5, 2], primary 1. If the verdict flips inside [0.5, 2], the result is labelled **KNOB (alpha)**.

## The derived rule (every galaxy treated as collision debris, since all four are on the vD+22 trail list)

A dwarf that condensed from collision gas holds cold energy only from three channels. Each is computed as an UPPER bound.

**S. Separation retention.** In the collision the gas stalls; each progenitor's collisionless cold energy moves on at
V_shift = V_coll/2 relative to the stalled gas (equal-mass centre of momentum; the smallest shift, so the largest retention).
- Fallback test: if V_shift < v_esc,p(r0) of the progenitor (framework potential above, M_b,p, r0 = the dwarf's r_1/2),
  the gas is re-bound to its own cold energy -> f_S = min(1, X * 5.364 M_b,d / M_tgt) (full supply).
- Otherwise M_S = X * 5.364 M_b,d * P_S, where P_S = probability that a co-located cold-energy element (velocity V_shift +
  isotropic Maxwellian with 1-D sigma_p = V_f,p/sqrt(2), untruncated) has |v| < v_esc,d(0), the debris dwarf's central
  Newtonian escape speed (Plummer, scale a = r_1/2/1.305). X = local cold/baryon enhancement over the cosmic ratio,
  bracket [1, 2].

**F. Sudden capture at formation.** Ambient cold energy inside the dwarf's catchment radius R_c with relative speed below
v_esc,d(0) is bound when the potential forms: M_F = rho_amb(R) (4 pi/3) R_c^3 P(|u| < v_esc,d(0)), Maxwellian with the
ambient 1-D sigma, bulk speed 0 (upper bound).

**D. Drift capture after formation (Gould-type, framework dissipation).** Ambient cold energy streams through the
catchment; along a radial chord (deepest path, upper bound) the drift removes
Delta E(w) = (2/w) Int_0^{R_c} g_N(r) v_s(r) dr, v_s = alpha tau_ff(r) (nu(r) - 1) g_N(r) (full deficit, no cold energy
yet), rho_m = rho_b(r) + rho_amb. An element with speed at infinity u (w^2 = u^2 + v_esc,d(0)^2) is captured iff
u^2/2 <= Delta E(w). Rate Mdot = rho_amb Int d^3u f(u) u pi R_c^2 (1 + v_esc,d(0)^2/u^2) 1[captured]; M_D = Mdot * t,
t = time since the collision.

**f_cap = min(1, (M_S + M_F + M_D) / M_tgt).** A6-strict variant (reported): the ambient cold energy belongs to the
group's catchment (no pooling), so M_F = M_D = 0.

Ambient field: settled halos of NGC 1052 and NGC 1035 superposed, rho_amb = k * Sum_h V_f,h^2/(4 pi G R_h^2), sigma =
the smaller host sigma (upper bound on capture). R_c = min(Jacobi radius vs NGC 1052, R_J = R (nu_d M_b,d / (2 M_g(<R)))^(1/3)
with M_g(<R) = V_f,g^2 R/G, and the dwarf's own exhaustion radius r_*,d).

## Inputs and brackets (PROVISIONAL unless marked V; no downloads)

| input | primary | bracket | source |
|---|---|---|---|
| dwarf M_*, R_e, D | CFG655 frozen table | CFG655 | CFG655 (V) |
| positions (J2000 deg) | DF2 40.4451 -8.4028; DF4 39.8128 -8.1160; DF9 40.0292 -8.2290; LEDA 39.7021 -8.0494 | - | vD+22 2205.08552 Table 1 (V via ar5iv) |
| NGC 1052 / NGC 1035 positions | 40.2700 -8.2558 / 39.8713 -8.1328 | - | standard catalogue values (PROVISIONAL) |
| R (3-D distance to host) | projected at the galaxy's D | [R_proj/2, R_proj] | upper ambient at R_proj/2 |
| V_coll | 358 km/s ("relative radial velocity ... 358") | [250, 450] | vD+22 (V); ">~300" (V) |
| t since collision | 8 Gyr ("around eight billion years ago") | [6, 9] | vD+22 (V; minimum ~6 Gyr V) |
| progenitor M_b,p (each) | 1e9 Msun | [3e8, 1e10] | not measured; lower = trail stellar sum scale, upper = gas-rich x10 (PROVISIONAL) |
| NGC 1052 condensed M_b | 1e11 Msun | [5e10, 3e11] | literature ~1e11 (PROVISIONAL) |
| NGC 1035 condensed M_b | 5e9 Msun | [3e9, 1e10] | PROVISIONAL |
| k (unsettled reservoir) | 1 | [1, 3] | Theory v2 eq. 7 (unsettled cold energy, up to twice the settled) |
| X (local enhancement) | 1 | [1, 2] | - |
| alpha | 1 | [0.5, 2] | CFG541 V5 (free O(1)) |

Bracket evaluation: every input at primary; then the all-upper corner (every input at the value that maximises f_cap)
and the all-lower corner; plus one-at-a-time scans. The verdict uses the primary and the all-upper corner for the E side,
the primary and the all-upper corner for LEDA (the most favourable case for LEDA reaching full supply).

## LEDA threshold (derived from CFG655's estimator, uses sigma only for scoring, never as a rule input)

f_min(LEDA) = smallest f_s with Z >= -2 under sigma^2 = sigma_N^2 [1 + f_s(nu - 1)], each footing.

## Pass rule (both footings; the lane verdict needs both)

- **PASS:** at primary AND at the all-upper corner, f_cap <= the CFG655 alt bound for DF2 (0.33), DF4 (0.26), DF9 (0.46)
  (canonical bounds also reported), AND f_cap(LEDA) >= f_min(LEDA). The derived rule then reproduces CFG655's label for all
  four without sigma and without the vD+22 label.
- **FAIL (LEDA not derived):** the E side holds at primary and all-upper, but f_cap(LEDA) < f_min(LEDA) even at the all-upper
  corner. Then LEDA's supply must come from a pre-existing channel (stars and cold energy formed before the collision move
  together and keep their own catchment), which the framework's own observables (CFG655 Rule A age, Rule M membership) do
  not assign: the label stays external. Reported as "E side DERIVED; LEDA NOT DERIVED".
- **FAIL (E side):** any E galaxy exceeds its alt bound at PRIMARY inputs.
- **BRACKET-DEPENDENT:** the E side holds at primary but fails at the all-upper corner: report which input does it
  (one-at-a-time scan). If it is alpha within [0.5, 2] -> **KNOB (alpha)**.

Reported: channel decomposition S/F/D; A6-strict variant; alpha at which each E bound would be reached and alpha needed for
LEDA; escape speeds and compactness of all four (what distinguishes LEDA physically); fallback margins V_shift - v_esc,p.

## MUTATE (MUTATE=1, separate outputs)

- M1: V_coll -> 1e-6 km/s must give f_cap = 1 (full supply) for all four on both footings.
- M2: ambient and progenitor cold energy -> 0 (k = 0, cosmic ratio factor 0) must give f_cap = 0 for all four.
- Either tooth failing is reported as a construction failure of the rule.

## Compute

One process, < 100 MB, nice -n 10, seconds. No downloads.

kappa = 1/2 fitted; cold energy mass required; not theory closed.
