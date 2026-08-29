# FC-AeST + c_2* (Maxwell corner) — PREFERRED-FRAME alpha_2 VERDICT

## VERDICT: PPN-KILL-alpha2-too-large

**alpha_2 is DERIVED and is > 1e-7 throughout the entire allowed region.**
FC-AeST + c_2* dies at the preferred-frame gate.

- GR gate: **GR-VALIDATED** (fc_aniso_grgate.py, 16/16 certificates, exit 0).
- Two independent full-anisotropic O(w^2) 1PN solves (Route A = Setup-M direct
  coupled solve; Route B = Foster-Jacobson c-tensor map + independent Setup-M
  solve) **AGREE on the physics** (see reconciliation below).
- alpha_2 is derived via a gauge-invariant extraction (2b+d) that is independently
  validated on TWO published limits: GR (alpha=0) and Einstein-aether at the Maxwell
  corner (alpha_1=-4K_B, alpha_2=0, matches Foster-Jacobson exactly).

---

## THE DECIDING NUMBER

At the FROZEN, committed evaluation point
`beta_0 ~ 0.3-0.5` (UNSCREENED, forced by the committed Cassini-vs-fold no-go
`fc_beta0_cassini_nogo_2026.py`), with `K_B < 2.5e-5` (from |alpha_1^EA|<1e-4),
`K2>0`, `0<c_s^2<=1`, `c_T=1`:

|            | Route A (Setup-M direct) | Route B (FJ-map + Setup-M) |
|------------|--------------------------|----------------------------|
| alpha_2 (beta_0=0.5, K_B=2.5e-5) | 2.0e4 | 2.7e4 |
| alpha_2 (beta_0=0.33, K_B=2.5e-5) | 8.9e3 | 1.3e4 |
| alpha_1 (scalar ON, beta_0=0.5) | ~-2.7 | -8/(1+J_Y) = -2.67 |

Both routes: **alpha_2 ~ 1e4 >> 1e-7 bound (FATAL by ~11 orders).**
Independent second kill: **alpha_1 ~ -2.7 >> 1e-4 bound (FATAL by ~4 orders).**

alpha_2 functional form (agreed structure, 1/K_B simple pole):
- Route A: `alpha_2 = 1/lam_s + 2/(K_B lam_s^2) + O(lam_s^-3)`  (asymptotic, large lam_s)
- Route B: `alpha_2 = 4/(J_Y(1+J_Y)) * 1/K_B` + O(1) leading  (K_B->0 pole, fixed J_Y)
- `lam_s = J_Y`, `beta_0 = 1/lam_s`.

---

## RECONCILIATION — why the two routes AGREE (and why Route A's headline "PASS" is invalid)

Route A's summary line reads "alpha_2 = 1/lam_s -> PASSES", but that PASS is obtained
ONLY by setting `lam_s = J_Y = 1.3e8` (the LOCAL MOND-function derivative 2 g_bar/a_0
at 1 AU), i.e. `beta_0 = 1/lam_s = 7.7e-9`. **That is precisely the small-beta_0
screening escape that the committed Cassini-vs-fold no-go CLOSES.** The brief freezes
`beta_0 ~ 0.5 (UNSCREENED)` and explicitly forbids invoking screening to suppress alpha_2.

Evaluated at the MANDATED `beta_0~0.5` (lam_s~2), Route A's OWN formula contains the
same pole: its subleading term `2/(K_B lam_s^2) = 0.5/K_B` gives `alpha_2 ~ 2e4` —
matching Route B's `0.667/K_B ~ 2.7e4` to a factor 1.33. The routes differ only in the
exact pole residue (Route A `2/lam_s^2`; Route B `4/(J_Y(1+J_Y))`, agreeing at large
J_Y as `4/lam_s^2` up to a factor ~2 in the O(1)/lam_s^2 coefficient) — a precision
difference that does not touch the verdict, since both give alpha_2 ~ 1e4 at the frozen
point.

**Physics of the kill (both routes):** the c_2* term at the Maxwell corner
`c2* = K_B/(1-2K_B)` liberates the spin-0 aether mode with a SOFT kinetic term ~ c2* ~ K_B.
The O(1) AeST acceleration coupling `2(2-K_B) J^mu grad_mu phi` sources it, producing a
1/K_B strong-coupling response into the preferred-frame metric. With the scalar OFF
(J-coupling off) the sector decouples and one recovers the healthy EA value
alpha_1=-4K_B, alpha_2=0; with it ON at unscreened beta_0 the response diverges.

---

## WHY THIS IS A KILL AND NOT INCONCLUSIVE

The INCONCLUSIVE triggers are: GR gate failed / channels disagree / solve did not close.
None fire:
1. **GR gate PASSED** (GR-VALIDATED, 16/16).
2. **The solve CLOSED** — both routes: all gates pass, exit 0. Route A's anisotropic
   consistency checks (rot_ok, av_ok, aw_ok, cd_ok across 3 w-samples) all True — the
   exact internal test the old isotropic ansatz FAILED.
3. **Channels agree (gauge-invariant sense).** Per GR gate [I1] the naive g_00-alone
   iso (v^2 U, coeff c) and aniso ((v.x)^2 U/r^2, coeff d) channels are individually
   gauge-dependent and disagree even for pure GR; the unique convention-robust
   determination is the gauge-invariant `2b+d`, which BOTH routes use and which agrees
   qualitatively (same sign, same 1/K_B pole, same ~1e4 magnitude at the frozen point).
4. **alpha_2 is DERIVED**, cross-validated against two published limits (GR, EA/FJ).

Therefore: alpha_2 derived AND > 1e-7 throughout the allowed region => **PPN-KILL**.

---

## HONEST CAVEATS (do not affect the verdict)

- The exact pole residue differs by a factor ~1.3-2 between the two independent solves
  (Route A `2/lam_s^2` vs Route B `4/(J_Y(1+J_Y))`). This is a precision-of-machinery
  residual, not a sign/scale disagreement; both give alpha_2 ~ 1e4 at beta_0~0.5.
- The extraction SLOPE (Will's standard-PPN definition) is EXTERNAL-INPUT (textbook),
  but the OFFSET is validated: GR gives 0 and EA/FJ gives the published alpha_1=-4K_B,
  alpha_2=0, using the SAME extraction that yields the AeST number.
- `beta_0 ~ 0.3-0.5 UNSCREENED` is an EXTERNAL-INPUT from the committed no-go
  `fc_beta0_cassini_nogo_2026.py` (Cassini-safe kernels need p>=4 => beta0_min>=0.27).
  If that no-go were wrong and deep screening (lam_s > ~1/K_B ~ 4e4, beta_0 < ~2e-5)
  were allowed, alpha_2 could be pushed below 1e-7 — but that door is externally shut.
- alpha_1 ~ -2.7 at beta_0~0.5 is an INDEPENDENT kill (bound 1e-4). Note the
  "established alpha_1 = -4K_B" is the scalar-DECOUPLED value; with the scalar ON at
  unscreened beta_0 the acceleration coupling drags alpha_1 to O(1). This resolves the
  "alpha_1 exact FC-AeST OPEN" item adversely.

---

## FILES
- fc_aniso_grgate.py / .out — GR gate (16/16, exit 0)
- fc_solveA_setupM.py / .out — Route A direct anisotropic solve (all gates, exit 0)
- fc_solveB_partA_fj.py / .out — Route B Foster-Jacobson vector-sector map (6/6)
- fc_solveB_final.py / .out — Route B consolidated (7 blocks, exit 0)
- FC_ANISO_REPORT.md — full narrative
- closure_results.json — machine-readable verdict
