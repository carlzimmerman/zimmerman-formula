> **Forward correction, 2026-11-12:** Dimensional uniqueness is conditional on the chosen available variables and monomial class. A parameter frozen from rho_m at a fixed reference epoch remains constant even when the instantaneous rho_m evolves, so time independence alone does not select rho_Lambda. The two tested per-galaxy constructions fail as stated; this does not exclude every formation history. Kappa remains fitted, not dynamically derived. See the [correction index](../../research_closure_2026_11_12/combined_route/CORRECTIONS.md). The body below is preserved as the historical record.
>
> *Audit note, 2026-11-12 (lead session):* this notice was written by another session and is committed here on the owner's instruction after an independent check, `reviews/codex_corrections_audit_2026_11_12/C3_kappa_and_dt2.md` (grade: CORRECT). The folder `research_closure_2026_11_12/` it links to was not committed with it, so those links may not resolve; the audit file is the checked record. The committed text, labels and outputs below this notice are not edited by this commit.

# FINAL-6 (KAPPA) RESULT: is kappa an OUTPUT of the formation reading? (2026-11-11)

**Label: KAPPA NOT DERIVED (FITTED) + FORMATION REFUTED (per-galaxy).**

Two-part answer:

- **Q1 (form): YES — the formation reading does output something.** Universality forces the *form*
  `a_0 = Phi * c sqrt(G rho_*)` **uniquely** (exact dimensional closure, Lean-certified), and a normalisation
  frozen at an event cannot drift, so `rho_*` must be the only time-independent cosmic density, `rho_Lambda`.
  The formation reading therefore *selects the canonical footing* and turns the alt footing into a different,
  testable hypothesis about epoch dependence.
- **Q2 (coefficient): NO.** `kappa = Phi` is a pure number that **no equation of the formation reading evaluates**.
  Every concrete closing condition either re-states the fit (`kappa = 1/(2 sqrt beta)`, circular) or is excluded
  by the universality of the RAR (both halo-scale routes predict `a_0 ∝ M^(1/3)`). **kappa = 1/2 stays FITTED.**

Criteria: `FROZEN_CRITERIA.md` (local cbba716d05, committed alone before any FINAL6 script or number).
Script `final6_kappa.py` → `final6.out` / `final6.json`; twin `FINAL6_MUTATE=1` → `final6_MUTATE.out` /
`final6_MUTATE.json`; Lean `FINAL6.lean` (`compile.txt`). TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing. Footings never pooled. Cold dark energy is a gravitating field component; no particle is
added anywhere. kappa = 1/2 FITTED; not theory closed.

## 1. Q1 is an output: the only universal form is `c sqrt(G rho)` (K1, exact)

Solve for every monomial `G^a c^b rho^g M^m` with the dimension of an acceleration. The 3×4 exponent system has
rank 3, so the solution is an affine line:

    (a, b, g, m) = (3t − 1, 4 − 6t, t, 2t − 1),   t ∈ ℚ
    equivalently  a_0 = c sqrt(G rho_*) · w^p ,    w ≡ G³ rho_* M² / c⁶ = (G M sqrt(G rho_*)/c³)² ,  p = t − 1/2 .

**Mass-independence (`m = 0`) forces `p = 0`, i.e. `a_0 = Phi · c sqrt(G rho_*)`, and nothing else.** Proved in
`FINAL6.lean` (`accel_family`, `mass_free_unique`), which compiles clean.

So `a_0 ∝ sqrt(G rho_Lambda)` is **not** a numerical accident of the `c H_0` coincidence: given that one number serves
every galaxy, `c sqrt(G rho)` is the *only* dimensionful combination available. What remains free is the *pure number*
multiplying it.

Second half of Q1: the event's density. A value frozen at formation and conserved afterwards cannot inherit the time
dependence of `rho_crit(z)` or `rho_m(z)`. The only cosmic density that is constant in time is `rho_Lambda`. Hence
**F picks `rho_* = rho_Lambda`: the canonical footing, not the alt footing.**

## 2. Q2 is not an output (K4, K5, K3)

**K4 — the matching condition is a trade, not a prediction.** With `rho_* = rho_m(z_f)` the fitted `a_0` requires
`rho_m(z_f) = 4 a_0^2/(c^2 G) = rho_ref`, giving a required freeze-out redshift

| footing | rho_ref/rho_m0 | **z_f required** | z(rho_m = rho_Lambda) |
|---|---|---|---|
| canonical | 2.174151 | **0.295478** | 0.294967 |
| alt | 3.175331 | **0.469816** | 0.294967 |

Canonical agrees with matter–Λ equality to 5×10⁻⁴ in z. That is a genuine consistency check — and it is
**circular as a derivation**: `kappa = 1/(2 sqrt beta)` with `beta ≡ rho_m(z_f)/rho_Lambda`, so `kappa = 1/2` is
*exactly* the statement `beta = 1`, i.e. "freezing happened precisely at equality". Structure growth shuts down
asymptotically, so the dynamics does not single out `beta = 1`. **Sensitivity:** taking the acceleration-epoch definition
(`rho_m = 2 rho_Lambda`) instead gives `kappa = 1/(2 sqrt 2) = 0.35355`, a shift of **−0.1505 dex**, against the
observed footing spread of **0.0411 dex** (0.5 log10(1.1312/0.93603)) — **3.7× larger**. K4 FAILS as a derivation.

**K5 — the two routes that take the scale from the halo itself are refuted by universality.**
- **R-A (internal-acceleration):** BTFR `v_f^4 = G M_b a_0` with `M_b = f_b M_vir`, plus `v_f^2 = G M_vir/R_vir`, gives
  `a_0 = f_b^(−1) G M_vir/R_vir^2 = f_b^(−1) (4π/3)^{2/3} Delta_v^{2/3} G M_vir^{1/3} rho_crit^{2/3}`.
- **R-B (catchment-saturation):** the settled region exhausts the catchment, `R_set = R_c` with `M_b = (4π/3) R_c^3 rho_b`,
  gives `a_0 = f_cdm^2 (4π/3)^{2/3} G M_b^{1/3} rho_b^{2/3}`.
Both are the `p = 1/6` member of the Buckingham family, i.e. `a_0 ∝ G rho^{2/3} M^{1/3}` — **mass dependent**.
Over `1e8 -> 1e12 M_sun` the predicted `a_0` spans **1.333 dex** (×21.5); at `M_b = 6e10 M_sun` it lands at
`a_0/a_0,fit = 7.70e−02` (R-A, −1.113 dex) and `1.47e−03` (R-B, −2.832 dex). Observed non-universality is 0.041 dex.
**Verdict: REFUTED on both footings** — formation read per-galaxy (each element freezing at its own assembly epoch) is
excluded, by 1.3 dex, by the very thing kappa is fitted to.

**K3 — the pure-number scan.** Under F2+F3 `kappa` must be a pure number in
{delta_c, Delta_v, f_cdm, f_b, Omega_Lambda/Omega_m, X, pi}. Of the 21 frozen closed forms, none lands within 5 % of 1/2
except `1/2` itself. (Closest: `1/delta_c` = 0.5932, +18.6 %; `delta_c/pi` = 0.5367, +7.3 %; `(OL/OM)/4` = 0.5429,
+8.6 %.) No route PASSES — a band hit would be numerology, not a derivation, since there is no equation in F that
evaluates Phi.

## 3. What the two footings actually are (K2, KA-2) — the task's parenthetical, confirmed

| footing | a0_fit [m/s²] | rho_ref = 4a0²/(c²G) | rho_ref/rho_Lambda | rho_ref/rho_crit,0 | **kappa** | Z = c H_Lambda/a0 |
|---|---|---|---|---|---|---|
| canonical | 9.36030e−11 | 5.84241e−27 | **1.001183** | 0.685510 | **0.500000** | 5.788810 |
| alt | 1.13120e−10 | 8.53280e−27 | 1.462220 | **1.001182** | **0.500000** | 5.788810 |

Both footings reproduce `kappa = 1/2` **to machine precision under their own density**; the canonical footing is
the Λ-only density (ρ_Λ = 0.6847 ρ_crit) and the alt footing is the total/critical density. So **the 20 % gap
between 9.3603e−11 and 1.1312e−10 is the density convention, not two measurements of kappa** — exactly the
task's caveat, now printed rather than assumed.

## 4. The one real new prediction (K7, reported)

Under F the two conventions stop being conventions. `rho_* = rho_Lambda` gives an epoch-independent `a_0`;
`rho_* = rho_crit(z)` gives `a_0(z)/a_0(0) = E(z)`:

| z | E(z) | a_0(z)/a_0(0), canonical | a_0(z)/a_0(0), alt |
|---|---|---|---|
| 0.3 | 1.17363 | 1.00000 | 1.17363 |
| 0.5 | 1.32244 | 1.00000 | 1.32244 |
| 1.0 | 1.79084 | 1.00000 | 1.79084 |
| 2.0 | 3.03279 | 1.00000 | 3.03279 |
| 6.0 | 10.43229 | 1.00000 | 10.43229 |

FINAL2's bound on any `a_0(z)` arbitrates; FINAL2's verdict stands and is not re-graded here.

## 5. Known answers and twins

- **KA-1** Z = 5.788810 = sqrt(32π/3), both footings: **PASS** (|dZ| = 0.00e+00).
- **KA-2** canonical ↔ ρ_Λ (1.001183), alt ↔ ρ_crit (1.001182), footing-paired: **PASS**.
- **KA-3** R_set = (1+X) r_M with PD1's X → 571.7395 kpc (canonical) / 520.2283 kpc (alt) at M_b = 6e10 M_sun;
  identity verified structurally (R_set/r_M = 1+X; g_N(R_set) = a_0/(1+X)²). **Deviation:** FINAL4 states
  `R_set = r_ta` without publishing a numeric `r_ta`, so KA-3 is verified structurally rather than against an
  external number. Recorded here, not quietly relabelled.
- **MU1** `kappa = 1` → required `rho_* = rho_ref/4` → `z_f = −0.1839` (can) / −0.0741 (alt), both in the **future**: bites.
- **MU2** canonical scored against ρ_crit → kappa = 0.413978, |Δ| = 0.0860 > 0.05: bites.
- **MU3** drop universality (p = 1/6) → predicted a_0 spans 1.333 dex over four decades: bites.

## 6. Verdict, in one line

The formation reading **relocates** kappa, it does not remove it: it fixes the *form* `a_0 = Phi c sqrt(G rho_Lambda)`
(uniquely, and it picks ρ_Λ over ρ_crit), and it hands the coefficient back either as a freeze-out redshift
(`kappa = 1/(2 sqrt beta)`, circular, ±0.15 dex) or as an unexplained pure number. **kappa = 1/2 is FITTED;
the theory is not closed.** No derivation was found, and that is the result.

## 7. Scope / honesty notes

- The refutation in K5 is of the *per-galaxy* formation reading (each element freezing at its own assembly epoch).
  The *global-shutdown* variant survives and is consistent — but it is equivalent to asserting ρ_* = ρ_Λ, so it
  carries no coefficient.
- K3's list is frozen and enumerative; it cannot prove absence, only that no natural closed form in the available data
  works.
- Background inputs (Planck 2018) and FINAL4's `X` are inherited, not re-derived here.
- No data downloaded, no refit of `a_0`, no new sector, no CLASS run.
