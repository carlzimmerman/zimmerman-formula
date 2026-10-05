# CFG337: a stable action for candidate B's bound-only switch?

Criteria: `FROZEN_CRITERIA.md` (commit 5176d8ea3, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; c_T = 1; beta = 0 chassis; the switch reads baryons only; no DM particle (the cold mass is still required).

**Verdict (frozen rule): PARTIAL, for both doors.** The best candidate (a leaf-normalised, saturating, inverted
symmetron) is healthy on FRW, where Z2 makes it exactly OFF at linear order, so growth is LCDM. It is also healthy
in the bound interior. It fails in the transition region. No ghost and no Hadamard instability appear there, but the
switch's bounded growth of transition gas outruns gravity unless the switch length is far above the record's
100 kpc tolerance. The single-constant version needs a length of 29 Mpc or more. This is not a candidate found.

## Part 1: why each prior gated action failed (from the record)
| construction | failure type | regime | source |
|---|---|---|---|
| DE7 curvature-reading gate | wrong-sign k^4 term on the metric (higher-derivative gradient instability); repair costs slip (lensing != dynamics, ~6% at z 0.25 to ~100% at z 4) | every smooth gate layer | DE7 095ab610a; N14 |
| DE12 MOND-sector gate (CV3 form; V0's region gate) | gradient instability of the BARYONS: the gate's second variation is a k^0 negative pressure, amplified by A^2 (A = nu + y nu' cos^2 theta, ~50-100); c_gate 1500-3700 km/s against gas at 37-117 km/s; growth ~ k (Hadamard ill-posed), 2-5e4 H at k = 1/kpc | the half of every transition layer where W'' > 0 (gate flat at both ends => W'' of both signs, DE7 T1) | DE12; N14 |
| DE13 gradient repair (mu \|grad f\|^2, mu \|grad U\|^2) | the repair's own background term is negative: a negative-energy mode at long wavelength for every mu >= 0 (24/24 layers; Lean 8 thms) | all galaxy layers z 0.25-4 | DE13 a7abb4d4f / e9a9978f9 |
| MS5 kappa cap | k^4 bracket W''U + W'/2 changes sign in the layer; still needs DE7's repair | cap-active layers | MS5 61a3a0858 |
| XR36 theta (turnaround) gate, Brown-Schutz dust | ghost: every saturated gate has a wrong-sign kinetic coefficient with a pole (1/k_g = 132-1756 kpc, Gamma 0.7-4.7 H), i.e. strong coupling at the pole; the unsaturated version costs SPARC | 24/24 layers, MOND-on side | XR36_gate_action.out; N15 |
| CFG48 local gates | DE12-type baryon gradient instability (44/48); a prescribed gate breaks momentum conservation | layers | CFG48 0dba13349 |
| CFG48 nonlocal enclosed-mass gate | stable 48/48 but bilocal (not a legal local term); edge at 0.11-0.24 r_ta, below B's window | - | CFG48, referee 35eebbe99 |
| CFG49 dynamical gate scalar (CV6) | stable only with two new untied constants (mu >= 1.5e28 J/m, m2 >= 1e-12 Pa), then pays DE13's potential cost (Phi_chi(r_F) = -13.5 v_f^2) and a UV speed of 2.3c (superluminal) | edge layers | CFG49 b899e204e |
| CFG172D theta-flow gate (V0) | d1 blind (never switches); d2 gradient instability, c_eff 4e3-9e3 km/s against a 37 km/s line | 96 cells | 249fa4ec8 |
| CFG242 latch / BIMOND + foliation | latch: no memory (n(t_ff) = 0.79, not an instability); BIMOND: TT mode d_t^2 h = 0 (weak hyperbolicity, Hadamard sense) + nullity 2 (indeterminate) | static bound / linear | e04b22b5a |
| CFG243-245 ownership classes | not instabilities: cosmic amount (10^-1377), radial scale M^0.33 not M^0.5, vacuum clock too slow (Gamma tau 0.14-0.79 vs 4.1) | cosmology / galaxies | e8b702457, 50c8c7267, 48ef9f534 |
| MS1 curvature / matter-door reading | not an instability: first-variation leak (the carrier's potential is shifted by -1/2 C W'B or -C W'B/8 pi G), 0.06-2300x the carrier's gravity | lenses, flagship hosts | MS1 |

**Common thread.** Every LOCAL prescribed gate is the slaved limit of a field with no kinetic or gradient energy. Its
second variation lands on whatever it reads, and the gate's W'' takes both signs. Where it reads baryons through the
phantom, that gives a k-linear (Hadamard) baryon instability. Gradient energy on the gate cannot cure this (DE13). A
truly dynamical gate cures the Hadamard part, but only at the price of new constants (CFG49).

## Part 2: screen
- **S1, k-mouflage / kinetic switch: FAIL (constraint).** It screens at HIGH gradient, the wrong direction. The
  reversed form is admissible only as a band kernel that changes nu below ~0.015 a0, where galaxy outskirts and the
  web overlap (N12). That breaks nu_mono.
- **S2, symmetron: PROMISING (carried on).** The standard sign is OFF in dense regions, the wrong direction. The
  inverted (density-triggered SSB) sign is ON in dense regions, and Z2 makes it exactly OFF at linear order on FRW.
- **S3, cubic Galileon / Vainshtein: FAIL.** It only suppresses. The inverted branch has no static solution above
  s = -1/(4c), and its Z = 1 + 2cx -> 0 there (strong coupling).
- **S4, virial T^mu_mu or P/rho switch: FAIL.** The dust trace reduces to the density door. P/rho is zero per stream
  for stars. A prescribed W(P/rho) brings back N14 on the gas temperature.
- **S5, leaf average alone: blind.** It is constant on each leaf. It is used here as the threshold normaliser.
- **S6, nonlocal enclosed-mass gate:** record reference only (CFG48).

## Part 3: the candidate action
S_sw = Int sqrt(-g) [ -(1/2)(d sigma)^2 - V ], with
V = -(1/2) mu0^2 T(U) sigma^2 + (lambda/4) sigma^4 and T(U) = 1 - 1/U.

The chassis' MOND sector is multiplied by f = sigma^2/v^2, with v^2 = mu0^2/lambda. The condensation energy is
E_c = lambda v^4, and R = E_c/B.

The switch is minimally coupled, so c_T = 1 and beta = 0 are untouched. Two readers U are used:
- **C1:** the MOND-sector door (DE12's contrast form, amplified by A).
- **C2:** the baryon-density door, rho_b / (Delta_e <rho_b>_leaf), with the edge at the same radius as DE12.

| background | result |
|---|---|
| (a) FRW, linear | sigma_bar = 0, so g_x = E_dir = df/dsigma = 0: exactly OFF, LCDM growth. M^2 = mu0^2(1/U - 1) > 0. K > 0; speeds^2 c_s^2 and 1 (luminal); bounded. PASS |
| (b) static bound (r = 30 kpc, z 0.25, 1e11) | broken phase: M^2 = 2 lambda sigma_bar^2 > 0. Direct trigger stiffness >= 0 (T concave). K > 0; speeds^2 in (0, 1]; maximum growth equals the Jeans rate (ratio 1.0000). Law overshoot f - 1 = 2/R (fidelity needs R >> 1). PASS |
| (c) transition, 24 record transitions per door | H1-H3 pass: the dynamical switch makes the growth bounded, omega^2 >= -(Gamma_g^2 + rho g_x^2). **H4 fails.** The extra growth is M(c_g - c_eff), with c_g^2 = rho E_c T'^2 / 2. C1, lenient (local E_c, R = 4): c_g up to 1640 km/s, 29x Gamma_g at 100 kpc, ell_min 2.9 Mpc. C2, lenient: 1.8x (1e6 K) / 3.8x (1e5 K), ell_min 183-378 kpc; it passes at 500 kpc only in this lenient per-system case. C2 with a single E_c (one field, one constant, R = 4): 291x, ell_min 29 Mpc. R = 40 makes every case worse. |

**The obstruction.** Take the switch's slaved coupling c_g^2 = rho g_x^2 / M^2. To switch the MOND energy B with the
law kept to within 2/R, it must reach at least rho R B T'^2 / 2. A heavy (sharp) switch turns this into DE12's
Hadamard failure. A light switch makes it bounded, at rate c_g / ell. For that rate to be no faster than gravity,
ell must be at least c_g / Gamma_g, which is Mpc scale. So the switch cannot resolve B's edge. Sharpness and
stability trade off one for one. This is XR15's "no single smoothing length", now derived from an action.

Even C2's one lenient corner reads a pure density edge. That edge carries the record's matter-only liabilities
(L392 KiDS +118/+128; the DE4/DE6 flagship needs >= 30% CGM; the CFG21 edge tension). It encodes neither turnaround
nor top-level ownership, and it adds declared constants (mu0 or ell, E_c or R, Delta_e).

## Controls
- **R1, the known failure returns:** DE12's gate gives min c_gate 1526.2 km/s and min Gamma/H 1.982e4 at z = 0.25,
  matching the committed values. The slaved limit sends omega^2 -> -infinity, and W'' spans [-9.84, 9.84].
- **R2, GR limit:** healthy (Jeans only).
- **MUTATE (CFG337_MUTATE=1):** with the switch kinetic sign flipped, the ghost is flagged (FRW, bound and transition
  H1 all FAIL) and the run exits 1.

## Lean
`CFG337_switch_certificates.lean` holds 9 theorems with standard axioms and no sorry. They cover:
- kinetic positivity, and the ghost under the sign flip;
- the bounded dispersion against the unbounded slaved limit;
- the exact maximum of the extra growth;
- the concave-trigger stiffness sign;
- the FRW mass;
- the transition-length obstruction, with the numeric ell_min instances.

Compile with `cd fable_independent_2026/lean_2026 && lake env lean <abs path>`; the output is in the `.out` file.

## Run
```
python3 campaign_fresh_gravity/CFG337_stable_switch_action/cfg337_switch.py > campaign_fresh_gravity/CFG337_stable_switch_action/cfg337_switch.out          # rc 0
CFG337_MUTATE=1 python3 campaign_fresh_gravity/CFG337_stable_switch_action/cfg337_switch.py > campaign_fresh_gravity/CFG337_stable_switch_action/cfg337_switch_MUTATE.out   # rc 1
```
DE12's `transition()` is loaded read-only by exec (no DE12 file is written).

**Scope:**
- quadratic level only;
- quasi-static Newtonian limit on the leaves, WKB with k well above the background gradient;
- B is treated as a local background coefficient (its nonlocal 1/k piece is dropped, as in DE12);
- point-mass baryons with NFW-tracing gas (DE12's profiles).
