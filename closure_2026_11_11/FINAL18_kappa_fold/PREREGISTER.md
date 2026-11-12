# FINAL-18 (KAPPA_B) PRE-REGISTRATION -- 2026-11-11

Committed **alone**, before any FINAL-18 script exists and before any FINAL-18 number is computed.
Footings never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2). Cold dark energy is a
gravitating field component; no particle is added. **kappa = 1/2 FITTED; not theory closed.**

**Id checked free:** no `closure_2026_11_11/FINAL18*` path exists, and no commit subject on any branch
names FINAL18, FINAL-18 or kappa_fold.

## 0. The question, in one line

> CLOSURE.md names one missing ingredient -- *what the clock does when it folds* -- and FLD1 has now measured
> where the fold is. Can `kappa` be **derived** from a matching condition imposed **at the fold**, where the
> law's halo is first established?

Split, as FINAL16 did, because the halves have different answers:
- **Q1 (form / structure).** Does the fold-matching condition *pin* kappa (unique root), or is it another
  flat direction like FINAL16's J1?
- **Q2 (value).** Does the number it pins agree with the frozen target `kappa = 1/2`?

## 1. The two conditions, stated now, before any number

**(V) -- the vacuum normalisation (the definition of kappa).**

    a_0 = kappa * c * sqrt(G * rho_Lambda),     rho_Lambda = Omega_L * rho_crit,0

from the footing's own background (Planck 2018 TT,TE,EE+lowE+lensing: H0 = 67.36 km/s/Mpc,
Om = 0.3153, OL = 0.6847). **(V) is a definition, not a constraint**: for any a_0 it returns
kappa = a_0/(c sqrt(G rho_L)). Alone it outputs nothing. What can output kappa is a second equation
that fixes a_0. The candidate is (M).

**(M) -- the fold matching condition.**

The record says the law exists only where the clock is static (FB1/COL1: a free-falling clock carries
`A = 0`, so `P = 0`), and CLOSURE.md says the joint to be supplied is the fold -- the surface where
falling clock dust first goes multi-stream and (in a completion) settles into the law's static halo.
FLD1 measured that surface: `R_fold(z, M_b)`, 0.52 R_ta today, growing roughly as M_b^{1/3}.

> **(M). At every epoch the law's static halo is first established at the fold front. Where it is born
> it must join continuously to the dust it is made of, in the one quantity the record conserves: its
> enclosed cold charge. Therefore the halo's enclosed cold mass at the fold equals the cold charge the
> clock carried across the front:**
>
>     M_ph(R_fold(t); a_0)  =  Q_fold(t)                                        (M)
>
> with
> - `M_ph(R; a_0) = M_b * X`, `X = (sqrt(1 + 4 x^2) - 1)/2`, `x = R/r_M`, `r_M = sqrt(G M_b / a_0)` --
>   the record's own exact quadratic `g_b X (1+X) = a_0` (FINAL16 F1/KA-3), inverted;
> - `Q_fold(t) = (4 pi/3) rho_d0 x_L(t)^3` = the comoving cold charge inside the Lagrangian radius
>   `x_L(t)` of the shell sitting at the front at time `t` -- FINAL3's history integral (H),
>   "settling rearranges cold charge, it does not create it";
> - `R_fold(t)`: FLD1's fold front, from COL1's exact X14 shells in the law-dominated limit.

Written in shares, `q := Q_fold/M_b`, (M) is **`X_fold = q`**.

**(M) has one unknown (a_0, i.e. kappa) only if its two sides are built from different physics.** This is
the whole question, and it is the first graded item:

- the **left** side is the halo's law-dependent structure, `M_ph ∝ a_0^{+1/2}` in the deep regime
  (exactly: strictly increasing in a_0, 0 at a_0 = 0, → ∞ as a_0 → ∞);
- the **right** side is the *fold kinematics* of cold clock shells. In action (A) with the law on, the law
  force and the clock's own excess gravity cancel at first order: writing the clock's excess (polarization)
  field `u = G (M_X - M_bg)/r^2 >= 0` and the law force `U(u) = a_0 u/(a_0 - u)`, the clock's inward
  acceleration is exactly
  `g_clock = -G M_X/r^2 + U(u) = -G M_bg/r^2 + u^2/(a_0 - u)` (COL1 Part 1's suppressed self-growth).
  **The perturbation does not gravitate; only the background clock mass does.** The residual `u^2/(a_0-u)`
  is the *entire* a_0-dependence of infall, and it is second order: relative to the excess's own
  Newtonian pull `u` it is `u/(a_0 - u)`.

**Pre-registered reading.** If `u/a_0 << 1` on the fold shells, `R_fold` and `Q_fold` are kappa-blind,
(M) is **not** FINAL16's `G_lam`-covariant, and (M) + (V) is one equation in one unknown: **kappa is
pinned**. Prediction: `max_t u/a_0 ~ 6e-10` in FLD1's own runs ⟹ **Q1 = PINS**.

**The closed form (derived now; no number has been computed yet).** `X(1+X) = x^2` with `X = q` gives
`q(1+q) = a_0 R_fold^2/(G M_b)`, so **exactly**, with no deep-regime approximation,

    a_0^M  =  G M_b q (1 + q) / R_fold^2 ,        kappa_M = G M_b q(1+q) / (c sqrt(G rho_Lambda) R_fold^2)

    kappa_M / kappa_frozen  =  q(1+q) / [ X_fold (1 + X_fold) ]      (exact; both shares at the same R_fold)

and the (M)-deficit statistic

    D  =  log10 ( X_fold / q )          (M) holds  <=>  D = 0 at every epoch and every mass.

FLD1's published numbers already say what D must come out near: its corrected charge reads are
"1.6 to 5.1 % of the law's halo" inside 10 to 300 kpc, i.e. **short by 20 to 60**. Since
`kappa_M ∝ q^2` at large q, (M) is then expected to land ~2.2 to 2.5 dex below the frozen 1/2.

## 2. Conventions

SI in the printed kappa; internal work in kpc, km/s, Msun (G = 4.30091e-6, TU = 0.977792 Gyr), as in
COL1/FLD1. `rho_Lambda = OL * 3 H0^2/(8 pi G)` with the footing's own h, omega_b, omega_d (KD1).
Fold inputs are **read from FLD1's committed runs** (`fable52_push/FLD1_fold_reach/runs/*.json`,
origin bce6d61451) for the production rows, and reproduced by a **patched copy** of FLD1's own solver
kept inside this folder (identical equation, integrator, reflection and start-redshift handling, plus the
`q_fold(t)` series and an `a_0` scale knob that FLD1's file does not expose). The copy is validated
against the committed rows (KA-1) before it is used for anything. Footings never pooled.

## 3. The graded items (criteria fixed now; no item added or dropped)

**G1 -- the cancellation identity (exact; sympy, and Lean-certified).** *(graded)*
`g_clock = -G M_X/r^2 + U(u)`, `u = G(M_X - M_bg)/r^2`, `U(u) = a_0 u/(a_0 - u)`.
**PASS iff** the identity `g_clock = -G M_bg/r^2 + u^2/(a_0 - u)` holds exactly for `0 <= u < a_0`
(sympy `simplify` to 0), **and** the residual bound `|u^2/(a_0-u)| <= (u^2/a_0) * 1/(1-eps)` for
`u <= eps*a_0`, `0<eps<1`, is proven.
*Predicted:* PASS. This is the load-bearing step: it is the only place a_0 enters the fold kinematics.

**G2 -- are the fold inputs kappa-blind? (graded; the crux of Q1).** *(graded)*
Run the fold solver at `a_0 -> s * a_0` for `s in {0.1, 1, 10}` (and `100` as a bracket), at
log M_b 8 and 10.45, both footings, N = 1200, z_i = 10, law on.
**PASS iff** `|R_fold(0;s)/R_fold(0;1) - 1| < 1e-6` and `|q(0;s)/q(0;1) - 1| < 1e-6` at every s, when the
a_0-scaling of the wall radius `r_w = sqrt(G m/a_0) * FW` is switched **off** (the wall is a cap on the
law's flux and must not be used as a hidden lever), and the same holds with it switched on.
*Predicted:* PASS with the wall held fixed (residual relative O(6e-10)); with the wall scaled, the deviation
stays below 1e-6 as well because `r_w` sits below the crossing radius for the shells that set the front.
Meaning if PASS: **the RHS of (M) carries no kappa** ⟹ (M) is not `G_lam`-covariant ⟹ **kappa is pinned**.

**G3 -- the number (graded; the crux of Q2).** *(graded)*
Evaluate `kappa_M = G M_b q(1+q)/(c sqrt(G rho_Lambda) R_fold^2)` at z = 0 on the FLD1 grid
log M_b = 6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12, both footings.
**PASS iff** `|kappa_M - 1/2| <= 0.025` on both footings (the FINAL16 band, i.e. 5%).
*Predicted:* **FAIL**, kappa_M ~ 2.4e-3, a factor ~210 below the band, i.e. |kappa_M - 1/2| ~ 0.498.

**G4 -- universality (graded).** *(graded)*
**PASS iff** the dex span of kappa_M across the frozen mass grid is `<= 0.0411 dex` (the footing separation /
observational allowance FINAL16 froze).
*Predicted:* **FAIL**. `R_fold ∝ M_b^{1/3}` (FLD1) while `q` is mass-independent (FLD1's corrected
reads: the charge that turns around is ~1.06 M_b at every mass), so `kappa_M ∝ M_b^{1/3}` -- about 1.8 dex
across the grid, a factor ~45 over the allowance.

**G5 -- epoch (graded).** *(graded)*
Report `D(z) = log10(X_fold(z)/q_fold(z))` at z = 0, 1, 2, 4 from the fold series.
**PASS iff** `|D(z)| <= 0.0411 dex` at every reported z (the joint must hold *at every epoch*, since a
static halo is continuously being born at the moving front).
*Predicted:* **FAIL** by 1-2 dex, and **non-monotone-free**: `D` must be 0 at *all* z, so its *drift*, not
just its value, is a falsification. (FRZ2/FINAL2's looser forest window, 0.3 <~ d log a0/d log(1+z) <~ 0.7,
is a bound on epoch-keyed a0 channels and is **not** the allowance here; the requirement is exactness at
every epoch, and the tolerance above is applied only to absorb numerical noise.)

**G6 -- the grade the brief asks for (graded).** *(graded)*
State, from G1+G2+G3+G4+G5: does the fold-matching condition pin kappa, leave it free, or pin a
falsified number? **PASS** iff G1 and G2 pass (the structural answer is established either way).
*Predicted:* PASS, with **Q1 = PINS**, **Q2 = NO**.

## 4. Known answers (each must pass, both footings)

- **KA-1 (code fidelity).** A patched copy of FLD1's `fld1_shells.py` run at N = 1200, z_i = 10,
  log M_b 10.45, law on, `s = 1`, reproduces FLD1's committed
  `hubble_canonical_M10.45_zi10_N1200.json` in `R_fold_end_kpc` (139.2516) and
  `charge_turned_around_over_Mb` (1.0554545) to `|rel| <= 1e-9`. Same for the N = 2400 canonical row
  (139.3048417 / 1.0590110) and the N = 2400 alt row (139.2882051 / 1.0590110).
- **KA-2 (halo share).** At the frozen kappa = 1/2 the record's quadratic reproduces FLD1's published
  `X_fold` = 31.6 / 21.0 / 19.1 / 17.6 at log M_b 9.4 / 10.45 / 10.7 / 10.9 to 1 %.
- **KA-3 (exact inversion).** `X(1+X) = x^2` with `X, x >= 0` has the unique solution
  `X = (sqrt(1+4x^2)-1)/2`, and `X = q ⟺ x^2 = q(1+q)` (sympy, exact; Lean-certified).
- **KA-4 (the record's tie).** `Z = c H_Lambda/a_0 = sqrt(32 pi/3) = 5.78881` to 1e-4
  (carries FINAL16's KA-1; confirms the footing's rho_Lambda is the record's).

## 5. MUTATE -- three false twins, each of which MUST be rejected by the same machinery

- **MU1 -- "the fold matching condition derives kappa = 1/2."** The machinery must reject via G3:
  the band miss is ~0.498 against a 0.025 band (~20x).
- **MU2 -- "the deficit is a counting convention: charge the halo with the whole cosmic cold charge of
  the patch, `q = f_cdm = 5.3640`, and the fold matching lands on 1/2."** The machinery must reject
  via G3 + the conservation clause of (M): (H) allows only *crossed* shells to be rearranged, and even
  granting the whole patch the pinned value sits ~1.1 dex below the band; it is also mass-independent, so it
  cannot repair G4.
- **MU3 -- "kappa is another flat direction, so the fold route is vacuous: by FINAL16's J1 the matching
  condition cannot pin it either."** The machinery must reject via G1+G2: the RHS of (M) is kappa-free
  *by an exact identity* (the residual is `u^2/(a_0-u)`, and `u/a_0 <= 6e-10` on the fold shells), so
  (M) is **not** `G_lam`-covariant and *does* pin kappa -- to the wrong number. This is the guard against
  the lazy negative: the lane must not fail the route by calling it empty when it is in fact falsified.

## 6. Labels

- **KAPPA DERIVED (FOLD MATCHING).** (M), with no free dimensionless input, pins kappa and the pinned
  value satisfies G3, G4 and G5 on both footings.
- **KAPPA NOT DERIVED (FOLD MATCHING FALSIFIED).** G1+G2 pass; (M) pins kappa uniquely; the pinned value
  fails G3 and/or G4 and/or G5. *This is the pre-registered expectation* (kappa_M ~ 2.4e-3, ~2.3 dex
  below the band, mass-dependent ∝ M_b^{1/3}, epoch-drifting).
- **KAPPA NOT DERIVED (FOLD MATCHING VACUOUS).** (M) is covariant in `G_lam` (leaves kappa free) or
  ill-posed.
- **OPEN** if any known answer fails or a numerical step fails.

**Standing, whatever the outcome:** kappa stays FITTED unless a route outputs it.

## 7. Scope

The fold solver and its committed runs (FLD1/COL1), the record's halo quadratic, and the footing
background. sympy for every exact algebraic step; Lean for the load-bearing algebra (G1 item, KA-3).
No refit of a_0, no new sector, no new data, no download, no CLASS run. Literature attributions
PROVISIONAL.
