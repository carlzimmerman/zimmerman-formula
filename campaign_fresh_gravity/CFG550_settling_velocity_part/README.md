# CFG550: the velocity part of the settling dynamics, from a principle (no knobs)

**Result: no route passes.**
- The target temperature can be DERIVED: it comes out of the law's own phantom, not an insertion. In the deep regime it is
  T = V_f²/2 (sympy).
- But relaxing toward that derived target fails the gate on the bench.
- Labels: a0 INCONSISTENT, a1 INCONSISTENT, b POSITED, c INCONSISTENT.
- Full-system Lyapunov: NOT ESTABLISHED.

κ = ½ is fitted. The footings (9.3603e-11 can / 1.1312e-10 alt) are never pooled. The cold energy's mass is still required.
No dark-matter particle. This is not a closed theory.

Every number below is from `cfg550_results.json`, `cfg550_results_MUTATE.json` or `cfg550_post.json` (post-freeze, no label
depends on it).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (2717e0197).
- **Equations:** `VELOCITY_PART.md`.
- **Script:** `cfg550.py`. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg550.py`: about 40 min on 4 processes, exit 0.
  `CFG550_MUTATE=1` exits 1, as designed: all teeth bite.
- **Bench:** CFG544's toy is imported unchanged from `../CFG544_settling_kinetic_consistency/cfg544.py`, read only. Control C5
  reproduces CFG544's FIX-2 IC-C end states exactly (Δ = 0 in all 4 cells).

## The principle tried

CFG542's metriplectic statement is lifted to phase space:
- **Position part:** S = −(F + F_v)/Θ, with F as before.
- **Velocity part:** F_v = ∫ρ_c T_ph KL(p_c ‖ p_ph), the relative entropy to the law's phase-space phantom (the Eddington DF
  of the untruncated ρ_ph in Φ_law).
- **Velocity pairs:** transfers at fixed x, with the partner taking or giving (v′² − v²)/2.

sympy checks (A2), all PASS:
- M is symmetric PSD;
- M·δE = 0, and dE/dt = 0;
- dS/dt is a sum of squares;
- mass is conserved;
- the continuum limit is OU/Fokker–Planck, ∂_t f = (α/τ)∇_v·(v f + T_ph ∇_v f).

**So the relaxation rate (α/τ) and the target come out of the same statement as the drift. The target T_ph(r) is the second
moment of the law's phase-space phantom.**
- A1 sympy: in the SIS, f ∝ e^(−E/T) reproduces ρ_ph iff T = V_f²/2, with its amplitude fixed.
- Deep numeric T_ph/V_f² = 0.5007–0.5017 in the four cells.

Caveat: this uses the same input class A already takes (ρ_ph). It does **not** answer CFG461's question of what G9
mechanism sets σ⁴ = G M_b a₀/4 without the law.

## Routes and labels

**(a0) Strict GENERIC (Casimir entropy): INCONSISTENT.**
- With the partner, stationarity needs C′(f) equal in every velocity cell, so f is uniform in v: not normalisable, T → ∞.
- With no partner (Landau pairs), a cold element is already stationary and σ stays 0.

**(b) Lynden-Bell, T as a Lagrange multiplier: POSITED.**
- With the zero-entropy partner, β = 0 (sympy), so the temperature is undetermined.
- Closed (sink removed), T is fixed but too hot: σ² is above the required value by +0.163 / +0.175 dex (MW can / alt) and
  +0.172 / +0.183 dex (cluster can / alt).
- With the occupation cap f_ph, β = 0 spreads the cold energy as a uniform fraction of the phantom, D = −0.39 to −0.49 dex.
  β = ∞ is route (c).

**(a1) KL to the law's phantom, target T_ph: INCONSISTENT.** G550 fails in every cell, on IC-B and IC-C.

- **MW:**
  - IC-B: D = −0.112 / −0.116 and log X_J = +0.125 / +0.125.
  - Cause: the untruncated target heats the edge (σ²/σ_eq² = 1.5–2.3 in the outer bins), and the halo spills
    (ln r₉₉/r₉₉,an = +0.47 to +0.72).
- **Cluster:**
  - Cause: the round point-mass phantom is ≈ 0 inside r_M, so T_ph = P/ρ_ph diverges there. T_ph/V_f² is 2.2e3 at
    0.01 r_* and the maximum is 9e59 (post).
  - Effect: the relaxation then ejects particles, and the energy input exceeds 10 V_f² M_cat within 0.25 Gyr. Those runs carry
    no physical meaning beyond this.
  - This is the same fact as A4: in both cluster cells ρ_ph is not monotone in r (its peak is at 0.26 r_M), and the isotropic
    Eddington DF is negative (min f/max f = −0.81). **The isotropic phase-space phantom does not exist for the cluster
    idealisation.** In MW it exists (min f/max f = 1.5e-21 ≥ 0).

**(c) Phase-space inside-out fill (the bathtub f_ph Θ(E_t − E), with E_t fixed by M_cat): INCONSISTENT.**
- MW IC-C passes G550: log X_J = +0.031 / +0.035, D = −0.022 / −0.028.
- MW IC-B fails on D: D = −0.131 / −0.119, with log X_J = +0.069 / +0.071.
- **The bathtub's own density marginal is softer than CFG541's state.**
  - ρ_t/ρ_ph = 0.79 at 0.6 r_* and 0.59 at 0.9 r_*.
  - Its r₉₉ is 1.59–1.61 r_*, i.e. ln = +0.47 to +0.49 against the sharp edge.
  - E_t sits at about Φ_law(r_ta).
- Cluster IC-B fails, and the runs blow up (see a1). cluster_alt IC-C "passes" G550 even though its energy blew up; the few
  ejected particles leave the shell. That pass is not meaningful.

## The checks

**Gate G550 (T1 D, self-Jeans X_J, steady).** Route c passes only on MW IC-C and cluster_alt IC-C (the latter not
meaningful); a1 passes nowhere. CFG544's sharp-edge gate gives the same picture.

**Overfill: NOT HANDLED.**
- a1: P = 0.45 / 0.48 (MW) and 0.37 / 0.31 (cluster).
- c: P = 0.49 / 0.44 / 0.47 / 0.43.
- Relaxing velocities does not remove injected excess within 5 Gyr. FIX-2 had 0.30–0.43.

**Edge: NOT PRESERVED.**
- The allowance is CFG544's pure-Vlasov softening + 0.1.
- MW: a1 gives +0.47 to +0.72 and c gives +0.49 to +0.81, against allowances of 0.355 / 0.433.
- Cluster: a1 gives +6.4 to +8.7 (blow-up), and c gives +0.58 to +1.83.

**Energy-exchange sign: two-way, allowed by M (A3).**
- The rate is γ(3T − ⟨v²⟩)/2 per mass. dS ≥ 0 holds either way.
- In practice it runs both ways at once, as a steady throughput through the partner:
  - drift out to φ: 1.24–1.72 V_f² per M_cat;
  - relaxation in from φ: 1.17–1.83 over 10 Gyr (MW IC-B);
  - relaxation input still running at 0.09–0.14 V_f² M_cat per Gyr over the last 2 Gyr.
- a1 MW net: IC-B −0.13 / −0.11, an inflow, so NOT compatible. IC-C whole-history −0.018 / −0.021.
- c MW: IC-B +0.068 / +0.092 and IC-C whole-history +0.186 / +0.196 (compatible in MW). Clusters are not compatible
  (blow-up).

**H-theorem.**
- The dissipative sub-flow obeys it: dS ≥ 0 (sympy). The discrete velocity model takes KL from 1.023 to 0.0045 with
  |ΔE_total| ≤ 9e-16, and the partner gives 0.41 to the cold start.
- **Full-system Lyapunov: NOT ESTABLISHED.**
  - The phase-space KL changes under Vlasov at the rate −∫f(F′/F)v·∇(Φ_law − Φ) (sympy identity).
  - In the family L_c = cTH − F:
    - c = 1 is Vlasov-invariant, but on a mode about ρ_ph the drift raises it at the rate
      −2πGαε²ρ₀²τ(k²σ² − 4πGρ₀)/k², which is > 0 for k < k_J.
    - For c ≠ 1, dL/dt > 0 for some state whenever α < A/(2√(BC)).
  - Numerically, F rises during route c runs by up to 0.084–0.090 F₀ (MW IC-C).

**Angular momentum: NOT conserved (A6).** d⟨v⟩/dt = −γ⟨v⟩ in the region frame.

**Causality.** The relaxation is an ODE in v at fixed x, so it adds no propagation and no new bound on α.

**Mass** is exact in all runs.

## MUTATE (all bite, exit 1)

- **MT (target ×2 on IC-C):** fails G550 in all 8 route-cells.
  - MW a1: log X_J = +0.52 / +0.54.
  - MW c: log X_J = +0.17 / +0.18.
  - In the clusters the runs also blow up, so the bite there is not informative.
- **MS (S flipped):** the discrete model's KL rises monotonically, 0.0283 → 0.0310.
- **MK (sink removed):** in MW-can a1, IC-C over 2 Gyr, the matter energy changes by +0.638 |E₀| against an integrator error
  of 3.4e-4.

## Disclosures (dated 2026-10-10; the frozen text is not edited)

- **Cluster blow-up.** It comes from the derived target, not from the integrator: T_ph diverges where the point-mass phantom
  vanishes (`cfg550_post.json`). No cap was applied, because a cap would be a knob. The MW-only reading (post) shows that the
  MW verdicts do not depend on it.
- **Route (c) acceptance rule.** A particle already outside |v| < v_t accepts any proposal. In the cluster cells, combined
  with the diverging T_ph, this feeds the blow-up. In MW it is benign (energy errors ≤ 9e-3).
- **Maxwellian closure.** The toy uses the second moment of p_ph (a moment closure). This is exact only where T_ph is
  constant (the deep MW shell, T_ph = 0.50–0.51 V_f²).
- **Toy limits** are those of CFG544: spherical, static baryons, α = 1 (O(1) FREE), 0.05 V_f seed.

## Plain reading

- A principle does produce the velocity part. Lifting the metriplectic statement to phase space, with the law's phase-space
  phantom as the reference measure, gives the relaxation rate and the target temperature from one statement. The temperature
  is V_f²/2, set by the law's own potential.
- But the derived target is the untruncated phantom's temperature. It is too hot at the edge, so the halo spills by
  60–100%. The energy-capped version (route c) softens the edge by itself (+0.47) and still misses T1 on infall.
- Neither version removes overfill.
- The cluster idealisation has no isotropic phase-space phantom at all.
- FIX-2's posited target, the Jeans dispersion of the current density, works precisely because it is not the law's
  temperature. That is why it remains posited.
