# L14 — the candidate action's global admissible region

**Script:** `fable_independent_2026/L14_parameter_sweep.py` (0 FAIL on all 10 controls and all 10
per-gate resolution checks; 2 FAIL by design — see THE TEST). **Output:** `L14_parameter_sweep.out`.
Both footings, a0 = 9.3619e-11 (canonical) and 1.1279e-10 (alt) m s^-2.

---

## THE HEADLINE

**The simultaneous admissible region of the candidate action is EMPTY on both footings**, and the
minimal incompatible subset has **size two**:

> **{G2 clock tachyon, G7 positivity of the Newton constant}** — the condensate's background makes the
> clock equation tachyonic at a rate `sqrt(3 Omega_d / c_14) H_0 a^-3/2`, which stays under H(a) only for
> **c_14 >= 3 Omega_d / Omega_m = 2.533**, while `G_N = G/(1 - c_14/2)` is positive only for **c_14 < 2**.
> No value of c_14 does both. This is an analytic statement, not a grid fact.

Two further size-two subsets, and one size-three, say the same thing through other gates:

| minimal incompatible subset | why |
|---|---|
| **{G2, G7}** | tachyon needs c_14 >= 2.533; a positive Newton constant needs c_14 < 2 |
| **{G2, G1a}** | tachyon needs c_14 >= 2.533; PPN alpha_1 = -4c_14 + drag with \|alpha_1\| < 1e-4 needs c_14 <= 2.5e-5 — **five orders of magnitude** |
| **{G2, G1b}** | at c_14 >= 2.533 with c_2 > 0 the Foster–Jacobson alpha_2 cannot be tuned to zero (c_2* = c_14/(1-2c_14) < 0) and \|alpha_2\| >= 20 against a 4e-7 bound |
| **{G2, G4, G8}** | tachyon needs c_14 >= 2.533, so Cherenkov caps \|K_2\| <= (2-K_B)^2/c_14 <= 1.6, while the dark-sector window needs \|K_2\| ~ 1e5 |

**Every minimal incompatible subset contains G2.** The other nine gates ARE simultaneously satisfiable
— see the surviving region below. G2 is the single load-bearing obstruction.

---

## THE GATES, THEIR SOURCES, AND THEIR ADMITTED FRACTIONS

Each gate's formula is taken verbatim from its source script; each has a CONTROL in the script that
reproduces that source's published number (all 10 PASS). Fractions are over the stated grid (below).

| gate | formula | source | canonical | alt |
|---|---|---|---|---|
| G1a PPN alpha_1 | `alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y(y_e)(1+xi^2 k^2)+1)`, \|alpha_1\| < 1e-4 | `g03z...G2` (f32/f33) | 0.368687 | 0.358437 |
| G1b PPN alpha_2 | Foster–Jacobson at c_1 = -c_3 = K_B, \|alpha_2\| < 4e-7 | `g03v_fast_clock_branch.py ppn()` | 0.278271 | 0.278271 |
| G2 clock tachyon | `rate^2 = \|K_2\|Q_0^2 eps_0 a^-3/c_14 <= H(a)^2` | `g03w_growth_phi_dynamical.py` L164 + `g03v` L196 | 0.090909 | 0.090909 |
| G2b condensate | `eps_0 = 3 Omega_d/(\|K_2\|Q_0^2)` in (1e-5, 1) | `g03v` V6 | 0.273563 | 0.273563 |
| G3 linear growth | `max(S_eff,0)·2.71e6 <= \|K_2\|`, `S_eff = 1-(2-K_B)^2/(c_2\|K_2\|)` | `g03t_flrw_linear_from_action.py` D5+D7 | 0.800486 | 0.800486 |
| G4 dark-sector window | `H = 0.42 e c^2/(\|K_2\| a0)` in [71.0, 710.4] kpc | `g03r...` D, `g03u...` | 0.172414 | 0.137931 |
| G5 Solar System | `xi >= 0.10 pc canonical / 0.15 pc alt` | `g03d_exact_fourth_order_solar.py`, `g03z`, Amdt 11 | 0.529412 | 0.470588 |
| G6 BBN | `K_B <= 0.25` and `\|1/(1+3c_2/2) - 1\| < 0.13` | `route2_full_stack` L613, `g03e` B1 | 0.598916 | 0.598916 |
| G7 tensor + G_N | `c_13 = 0` identically (c_T = 1 exactly); `c_14 < 2`; `K_B < 2` | THE_ACTION §2, f35, `route2_full_stack` L1313 | 0.808081 | 0.808081 |
| G8 Cherenkov | `\|K_2\| <= (2-K_B)^2/c_14` | `g03z...` G3 | 0.386015 | 0.386015 |
| **INTERSECTION** | | | **0** | **0** |

Points on the grid: 120,065,220 per footing. Intersection: **0 points on both footings.**

### The grid (stated so a null is meaningful)

| parameter | points | range |
|---|---|---|
| K_B | 18 | 1e-3 … 5 |
| c_2 | 41 | 1e-9 … 10, **plus every alpha_2 = 0 locus c_2\*(c_14)** |
| c_14 | 22 | 1e-9 … 10 |
| \|K_2\| | 29 | 1e0 … 1e12 |
| Q_0/H_0 | 15 | 1e-4 … 1e4 |
| xi | 17 | 1e-4 … 1e3 pc |

The alpha_2 = 0 band is only ~16% wide in c_2, so a plain log grid would step over it; every positive
`c_2* = c_14/(1-2c_14)` for c_14 on the grid is added to the c_2 grid. This is deliberately generous to
the theory. The grid is positive on every axis because THE_ACTION §2 fixes the signs (c_14 > 0, c_2 > 0,
K_B > 0, \|K_2\| > 0); all minimal-subset statements are conditional on that.

---

## THE SURVIVING REGION WHEN G2 IS DROPPED

Dropping the tachyon gate and nothing else opens a region on **both** footings. This is the target any
completion that cures the tachyon would have to land in.

```
canonical   299,547 grid points (2.50e-03 of the grid)
alt         221,544 grid points (1.85e-03)

  K_B      in [1.0e-03, 2.50e-01]      (upper edge = the BBN cap)
  c_2      in [1.0e-09, 3.16e-05]
  c_14     in [1.0e-09, 1.18e-05]      (upper edge = the PPN alpha_1 ceiling)
  |K_2|    in [5.0e+04, 5.0e+05] canonical / [5.0e+04, 3.16e+05] alt
  Q_0      in [2.15e-03, 1.0] H_0
  xi       in [0.10, 1e3] pc canonical / [0.15, 1e3] pc alt
```

The marginal box is **not** the region. Two correlations are load-bearing:

- **c_2 is tied to c_14** wherever c_14 >= ~2e-7 (= alpha_2 bound / 2): there `c_2/c_2*(c_14)` is confined
  to [1, 3.16]. Below that c_14 the alpha_2 bound is met by \|alpha_2\| ~ 2c_14 alone and c_2 floats free.
- **S_eff is bounded above by G3 ∩ G4 alone**: `S_eff <= |K_2|_max / 2.71e6` = **0.185 canonical / 0.153
  alt**. Every surviving point sits on g03v's fast-clock branch, where the action's own linear scalar
  source is screened off. Grid maximum 0.063; no point anywhere has S_eff > 0.5.

**Representative surviving point** (the admitted grid point closest to the programme's fiducial corner) —
this is exactly the corner the closure documents quote, and it clears all nine non-tachyon gates:

```
K_B = 0.2   c_2 = 1e-5   c_14 = 1e-5   |K_2| = 2.5e5   Q_0 = 0.1 H_0   xi = 0.10 pc (canonical) / 0.15 pc (alt)
  alpha_1 = -4.052e-05      alpha_2 = +1.00e-10       S_eff = -0.296
  H       = 142.1 kpc (canonical) / 117.9 kpc (alt)   eps_0 = 3.19e-04
  gamma_v = 1.0450 (canonical) / 1.0300 (alt)
```

Note the fiducial c_2 is **1e-5, not 0.05**: the alpha_2 bound forces c_2 down onto c_2*(c_14), and that
in turn is what pushes S_eff negative.

### gamma_v over the surviving region (OUTPUT, never a cut)

Gaia DR4 Arm B (`PREREGISTRATION_DR4.md` Amendment 11(b)) registers ceilings 1.0450 canonical /
1.0300 alt at the Cassini-minimal xi. The surviving region's xi runs from the floor upward, so
**gamma_v in (1.0000, 1.0450] canonical and (1.0000, 1.0300] alt** — the registered ceilings are
attained only at the floor. (xi-dependence extrapolated from `g03y`'s exponential-carrier pairs,
exponent p = 0.778 canonical / 1.184 alt; labelled as extrapolation.)

---

## HOW FAR THE KILLING GATE WOULD HAVE TO MOVE

The tachyon gate is `c_14 >= 3 Omega_d / (Omega_m N^2)` if one tolerates a mode growing N e-folds per
Hubble time. Against the PPN ceiling c_14 <= 2.5e-5:

| N tolerated | c_14 required | shortfall vs PPN |
|---|---|---|
| 1 | 2.53 | 1.0e+05 x |
| 10 | 2.53e-02 | 1.0e+03 x |
| 100 | 2.53e-04 | 1.0e+01 x |
| 300 | 2.82e-05 | 1.1 x |

One would have to accept a k-independent mode growing **~300 e-folds per Hubble time** before the PPN-allowed
c_14 becomes reachable.

### The one escape, computed

`g03e` records the dust amplitude as a free cosmological initial datum, so eps_0 need not be tied to
Omega_d. Freeing it, the gate becomes

```
Omega_d,eff = |K_2| Q_0^2 eps_0 / (3 H_0^2)  <=  Omega_m c_14 / 3
```

At the largest PPN-allowed c_14 = 2.5e-5 this is **Omega_d,eff <= 2.6e-06**, i.e. **1.0e+05 times smaller**
than the dark component the dark-sector window (G4) and the cluster atmosphere (`g03u`: M_d/M_b ~ 6.8 at
100 kpc) require the condensate to be. The escape exists and it empties G4 of content: **a tachyon-free
clock and a condensate dark sector cannot both be had.**

---

## PASS/FAIL LINES (verbatim)

```
[PASS] C1 [control, G1a] the alpha_1 formula reproduces g03z's G2 table at both floors to 1%
[PASS] C2 [control, G1b] the Foster-Jacobson alpha_2 reproduces f33's corner within 20% and vanishes at c_2* = c_14/(1 - 2 c_14)
[PASS] C3 [control, G2] the tachyonic rate reproduces g03w's 282 H_0 today and 2.8e5 H_0 at a = 0.01 to 1%
[PASS] C4 [control, G2b] eps_0 reproduces g03v's V6 table (only Q_0 = 0.1 H_0 clears 1e-5 at |K_2| = 2.5e5)
[PASS] C5 [control, G3] S_eff and the growth floor reproduce g03t's D5 and D7 numbers, and the corner FAILS the gate (D7's pincer)
[PASS] C6 [control, G4] the hydrostatic length reproduces g03r's tabulated H, and the canonical window edges are exactly 5e4 and 5e5
[PASS] C7 [control, G5] g03d's published admissibility table gives floors 0.03 pc canonical / 0.05 pc alt for the carrier it solved
[PASS] C8 [control, G6] G_cos/G_N reproduces g03e's B1 numbers: c_2 = 0.05 admitted (-7%), c_2 = 0.1 at the edge (-13.0%), c_2 = 1 killed (-60%)
[PASS] C9 [control, G7] c_13 vanishes identically (c_T = 1) and G_N = G/(1 - c_14/2) is positive only for c_14 < 2
[PASS] C10 [control, G8] the Cherenkov bound reproduces g03z's 3.24e5 and admits |K_2| = 2.5e5 while rejecting 1e6 at the same corner
[PASS] F1-F10  each gate alone admits neither 0 nor 1 of the grid at both footings
[FAIL] T1 [THE TEST] the simultaneous admissible region of all 10 gates is non-empty on at least one footing   (canonical 0 points, alt 0 points)
[PASS] T2 [minimal subset] where the full intersection is empty, a minimal incompatible subset of size <= 3 exists
[FAIL] T3 [what the survivor costs] ... is the action's linear scalar source more than half alive anywhere (S_eff > 0.5)?
[PASS] T4 [the escape is not free] Omega_d,eff <= 2.625e-06 against Omega_d = 0.266 needed: short by 1.01e+05x
```

All 10 gates were reproduced against their sources; **none was excluded as unreproduced.**

---

## CAVEATS (all stated in the script's own footer)

1. "Fraction of the grid" is a measure over the stated log grid and has no prior meaning. Only the
   emptiness/non-emptiness statements are grid-independent, and the size-two subsets were also checked
   analytically.
2. G2 uses the **analytic** term `g03w` identifies in the clock equation, re-derived here independently
   from `g03t`'s printed clock-equation coefficients (coeff(T'') = -2c_14 k^2 a; coeff(T) contains
   -2k^2 K_2 Qbar(Qbar-Q_0)a with Qbar = Q_0(1+eps_0 a^-3), K_2 = -\|K_2\|; the k^2 cancels, hence
   k-independence). It does **not** use `g03w`'s numerical eigenmode, whose separation from a possible
   constraint-differentiation artefact `g03w` itself records as open. **If that analytic term is ever
   shown to be spurious, this entire kill dissolves and the nine-gate region above becomes the answer.**
3. G3 extends `g03t` D7's floor by the D5 screening factor — an interpolation between D7 (S_eff = 1) and
   `g03v`'s fast-branch V4 (S_eff <= 0). It reduces exactly to each at its own end.
4. G4's window edges come from `g03r`'s coarse \|K_2\| grid, re-expressed on H so the alt footing is
   consistent rather than inheriting the coarse grid. The nu_RAR kernel would shift the window by 0.568
   (`g03z` G3, to [2.8e4, 2.8e5]); this does not change any emptiness statement, since the growth floor
   2.71e6 is 5.4x–9.6x above either window's top edge.
5. gamma_v's xi-dependence is extrapolated and is an OUTPUT, never a cut.
6. The grid is positive on every axis, as THE_ACTION §2 fixes the signs.

---

## WHAT ANOTHER AGENT SHOULD TAKE FROM THIS

1. **Do not look for a corner of parameter space.** There isn't one, and the reason is two gates deep,
   not ten. Any repair must attack G2 (the condensate-sourced clock tachyon) directly.
2. **A repair of G2 alone is sufficient and would land in a known region**: K_B <= 0.25, c_2 ≈ c_2*(c_14),
   c_14 <= 1.2e-5, \|K_2\| ∈ [5e4, 5e5], Q_0 <= 1 H_0, xi >= 0.10/0.15 pc, predicting gamma_v <= 1.0450/1.0300.
3. **But that region costs the cosmological source**: G3 ∩ G4 alone cap S_eff at 0.185/0.153. Even with the
   tachyon cured, the action's linear scalar source is screened to under a fifth of itself on linear scales,
   so the surviving cosmology is not distinguishable from LambdaCDM-plus-dust at k = 0.2/Mpc by this source.
4. **The dust-free escape from G2 is real but self-defeating** (Omega_d,eff <= 2.6e-6): it removes the
   tachyon by removing the dark sector that G4 and the cluster atmosphere exist to supply.
