# A22 — preferred-frame PPN: `alpha_1`, `alpha_2`, and the nonlinear `beta`

**Lane:** A22_ppn_frames · **Date:** 2026-10-21 · **Base:** `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md` ·
**Script:** `a22_checks.py` (13/13 PASS, exit 0) · **Output:** `a22.out` · **Data:** `a22_results.json` ·
**Action:** the round-2 ADM action verbatim (`core_open_problems_round2_2026_10_20/03_relativity/report.md` §2),
`c = 1`, signature `(-+++)`, `K = 4 pi G`.

## Claim

For the round-2 action the three preferred-frame / nonlinear PPN parameters are

> **`alpha_1 = 0` and `alpha_2 = 0` at PPN order, identically, for every value of the ADM coefficient
> `beta_ADM`; and `beta_PPN = 1`.** The P sector contributes no `O(w^2 U)` term to `g_00` at all.

This closes the gate `FINAL_THEORY.md` §3/§8 names as the last open one ("the `(1+beta)theta^2` route to
`alpha_1`, `alpha_2` ... remains open"). It is not a tuning; two structural facts force it:

* **(F1)** `theta == 0` *identically* on any static configuration in the preferred (unitary, `T = t`) frame,
  because `theta = (1/(N sqrt h)) d_i(N sqrt h n^i)` and `n^i = 0`. Since `R3 + K_ijK^ij - theta^2 = R +`
  total derivative, the gravitational sector is **exactly Einstein–Hilbert on the whole static branch**, for
  every `beta_ADM`. In Einstein-aether variables it is `c1 = c3 = c4 = 0`, `c2 = -beta_ADM`, and the published
  `alpha_1`, `alpha_2` both vanish there. The `theta^2` operator also has **no linearised stress** about a
  constant background (`theta` starts at `O(h)`), so it cannot feed back into a linearised `g_00` either.
* **(F2)** The P sector's only `O(rho)` stress component is the **charge** `-D.P`: the clock term
  `P^i D_i ln N` has no shift `N^i` in it and its `h_ij`-variation is `O(rho^2)`; every other P operator is
  quadratic in `P`, so its `N^i`-variation is quadratic in `P`. Hence `T^t_t =` charge, `T^t_i = 0`,
  `T^i_j = 0` at `O(rho)`: no momentum density (`g_0i = 0`), no anisotropic stress (`Phi = Psi`).

The only frame dependence left is a pure isotropic rescaling of the P source, `(1 + 2w^2)`. That kills `alpha_2`
outright (no `(w.nhat)^2` structure) and gives `alpha_1 = 0` because the rescaled quantity is a **linear**
potential, not `U = GM/r`. The one new Solar-System observable the P sector produces is a **constant sunward
anomaly**

> **`a_P = GM/L*^2 = 2.42e-16 m/s^2`** (Sun, `L* = 24 pc`), i.e. **`6.6e-3` of the Earth–Mars bound**.

On FRW the P field has **no cosmic VEV**: no source (`a_mu = D_mu ln N = 0` by isotropy) and a positive mass
`m^2 = K/eta` with `m/H_0 = 2.6e8`, so `P = 0` is the unique attractor — the framework's cleanest structural
advantage over khronon/aether theories, where the aether norm is `1` by the unit constraint.

## Derivation
### D1. Notation and the two betas

`L/(N sqrt h) = [R3 + K_ijK^ij - (1+beta_ADM)theta^2 - 2Lambda]/(4K) + P^i D_i ln N - W(u)
+ (eta/2)E_iE^i - (gamma/2)(D_iP^i)^2 - (gamma/4)F_ijF^ij`, with `W = (a0^2/K)[-u/a0 - ln(1-u/a0)]`,
`u = K|P|`, `E_i = (Pdot_i - Lie_N P_i)/N`, `F_ij = d_iP_j - d_jP_i`. `beta_ADM` is the coefficient of
`theta^2` in the *action*; `beta_PPN` is the PPN parameter of `g_00`. They are unrelated, and one result below
is that `beta_ADM` is invisible to both `alpha_1` and `beta_PPN`.

Matching convention (Foster–Jacobson; the one validated in
`nbody_2026/stage72_alpha2_first_principles_2026.py`, whose C1 gate reproduces the literature
`alpha_1 = -4K_B` for the Maxwell-form aether): if the `O(w^2 U)` part of `g_00` for a static source seen from a
frame moving at `w` w.r.t. the preferred foliation is `[P_iso w^2 + S (w.nhat)^2] U`, then

  (1)  `alpha_1 = P_iso + S/2`,   `alpha_2 = -S/2`.
### D2. (F1) — `theta` vanishes on the static branch

In the unitary gauge `T = t` and `n^mu = (1/N, -N^i/N)`. With `N^i = 0` (static: `g_0i = 0`) and
`d_t h_ij = 0`,

  (2)  `theta = (1/(N sqrt h)) d_i(N sqrt h n^i) = 0`   **identically**,  and  `K_ij = 0`.

So on every static configuration `[R3 + K_ijK^ij - (1+beta_ADM)theta^2]/(4K) = R3/(4K) = R/(4K) + td`, i.e. the
static sector is **Einstein–Hilbert for any `beta_ADM`**. (Gauss–Codazzi: `R = R3 + K_ijK^ij - theta^2 + td`, so
the coefficient is `-(1+beta_ADM)+1 = -beta_ADM` in `R`-form: `R - beta_ADM theta^2`, the aether Lagrangian with
`c1 = c3 = c4 = 0`, `c2 = -beta_ADM`.) The published aether results then give
`alpha_1 = -8(c3^2+c1c4)/(2c1-c1^2+c3^2) = 0` and `alpha_2 = c14(c14+2c2c14-c2)/[c2(2-c14)] = 0`
(as tabulated in `data_assembly/DOOR11_LITERATURE_2026-09-29.md` §1, from Oost–Mukohyama–Wang 2018).

For a *tilted* background it is still inert at the order that matters: `theta = gamma(d_t + w.grad)(h/2)/(1+h/2)`
is linear in the metric perturbation about a constant background, so `theta^2` is `O(h^2)` and its contribution
to the **linearised** stress — from which `alpha_1`, `alpha_2`, `gamma-1`, `beta_PPN-1` are read — is zero (K5).
### D3. (F2) — the `O(rho)` stress inventory of the P sector

Static, `P = O(rho)` (sourced by `grad ln N`; D4). Varying the action:

* `w.r.t. N`: the clock term gives `-d_i(sqrt h P^i)`, i.e. the **charge** `psi = D_iP^i`, at `O(rho)`; `W`,
  `(gamma/2)(D.P)^2` and `F^2` are `O(P^2) = O(rho^2)` and contribute nothing at `O(rho)`.
* `w.r.t. N^i`: the clock term *contains no* `N^i` (`D_i` of a scalar is `d_i`; `P^i = h^ij P_j` is
  shift-independent), and `E_iE^i` is a square, so its cross term `(linear in N^i) x (linear in P)` vanishes
  identically (K12). Hence `T^t_i(P) = 0` at `O(rho)`.
* `w.r.t. h_ij`: the clock term's variation is `O(P dN) = O(rho^2)`; `W` is isotropic; `(D.P)^2` and `F^2` are
  `O(P^2)`. Hence `T^i_j(P) = 0` at `O(rho)`, in particular no anisotropic stress.

So at `O(rho)`: `g_0i = 0` (no momentum source, matter at rest) and `Phi = Psi` — lane A12's dust lemma,
re-derived here with no assumption about the frame.
### D4. The exact linearised static system, and the exact identity

Linearising in the conformal gauge `N = 1+Phi`, `h_ij = (1-2Psi)delta_ij` gives exactly (K3):

  (4)  `lap^2 Psi = K(psi + rho)`   ·   (5)  `lap^2(Phi - Psi) = 0`   ·   (6)  `gamma lap^2 psi = K psi - lap^2 Phi`

(the lapse, trace and P equations). Eliminating `lap^2Phi` between (4) and (6):

  (7)  **`lap^2 psi = -(K/gamma) rho`**   — **exact**, no approximation.

`psi` is the (negative) Newtonian potential of `rho` scaled by `K/gamma`: for a point mass
`psi = GM/(gamma r) = M/(2 pi L*^2 r)` (using `gamma = K L*^2/2 = 2 pi G L*^2`, A12 eq. (5) / A20).
Substituting into (4),

  (8)  **`Phi = Psi = -GM/r + (GM/L*^2) r + const`**,   i.e.  **`a_P = GM/L*^2`** (sunward).

Both equations of (8) hold identically (K4), and the result is reproduced by an independent FFT solve of
(4)/(7) and by quadrature of the same two Poisson equations (K13). With `L* = 24 pc`,
`a_P = 2.4205e-16 m/s^2`, `a_P/B_E = 6.613e-3` against `B_E = 3.66e-14 m/s^2` (A4's Earth 2σ
constant-anomaly bound) — **151x inside**. Since `a_P ∝ 1/L*^2`, `L* = 24 pc` is the worst case of A20's
window `[24, 90] pc`.

`P` itself: `p = |P|` obeys `p(K + 2gamma/r^2) = |grad ln N|`. For `r << L*` (all Solar-System radii)
`p = GM/(2gamma)` is spatially constant and

  (9)  `u = K|P| = GM/(2 lambda^2) = 2.42e-16 m/s^2 = 2.59e-6 a0`,   `lambda = sqrt(gamma/K) = L*/sqrt2 = 17.0 pc`.

So `P = O(eps)` as A12 assumed, but *not* through the saturated relation `u = g` that A12 used: inside `lambda`
the gradient term beats the mass term and `P` is a hedgehog of constant magnitude. A12's `g = K W'(u)` holds for
`r >> L*`, which is exactly the galactic regime it was applied to — so A12's theorem survives, but its hypothesis
"(ii) gamma terms negligible" fails inside 17 pc and the Solar System is **not** in the P sector's MOND regime (the MI kernel is separate).
The crossover defines a mass threshold: `r_MOND = sqrt(GM/a0) > L*` requires `M > a0 L*^2/G = 3.87e5 Msun`, i.e.
**no MOND below ~3.9e5 Msun**.
### D5. `alpha_2 = 0` (no `(w.nhat)^2` structure)

For a static source seen from a frame moving at `w`, with `-(dT)^2 = 1 - 2gamma^2(Phi - w.B + w^2 Psi)`,

  (10) `ln N_T = -1/2 ln[1 - 2gamma^2(Phi - w.B + w^2 Psi)] = Phi + w.B + w^2(Phi + Psi) + O(Phi^2)`.

To linear order in the potentials the `w^2` coefficient is `Phi + Psi` — **isotropic**: no term linear in `B` at
`O(w^2)` and no `(w.nhat)^2` (K6). With `B = 0` (D3) and `Psi = Phi`, `ln N_T = Phi(1+2w^2)`. The P source is
`D ln N_T`, so the *only* frame dependence is the scalar rescaling `(1+2w^2)`. Hence `S = 0` and

  (11) **`alpha_2 = 0` exactly.**   Bound `|alpha_2| < 2.4e-7`.
### D6. `alpha_1 = 0` at PPN order

The rescaling multiplies the charge, `psi(w) = (1+2w^2) psi_0`, so by linearity of (4)

  (12) `delta Phi = 2 w^2 Phi_c`,   `Phi_c = (GM/L*^2) r`   (the charge's contribution to `Phi`, eq. 8).

`delta Phi ∝ r`, **not** `U = GM/r`, so it contains no `w^2 U` term:

  (13) **`alpha_1 = 0` at PPN order.**

A conservative *measure* of residual `w^2U` content — `alpha_1(r) ≡ 2 Phi_c/U = 2r^2/L*^2` — gives
`8.16e-14` (1 AU) and `7.35e-11` (30 AU), i.e. `3.1e9` and `3.4e6` inside `|alpha_1| < 2.5e-4` (2σ,
Müller–Williams–Turyshev–Shelus 2005 LLR, `DOOR11...md` line 36; the same `1e-4`-class bound is what Oost et al.
adopt). Physically the `w^2` effect is a `3.0e-6` relative change of `a_P`, i.e. `7.3e-22 m/s^2`: unobservable.
### D7. `beta_PPN = 1`

`beta_PPN` is the coefficient of `-2 beta U^2` in `g_00`, so it needs a `1/r^2` term in `Phi`, i.e. a `1/r^4`
source in the constraint. The P sector's `O(rho^2)` sources are

  (14) `W = K p^2/2 = const` (`p` constant, eq. 9) · `(gamma/2)psi^2 ∝ r^-2` · `p Phi' ∝ r^-2`

— exponents `{0, -2}`, never `-4` (K8). So `Phi_2 = A ln r + B r^2`: no `1/r^2`, hence

  (15) **`beta_PPN = 1`**, with a non-PPN residual `(r^2/L*^2)|ln(r/L*)| = 4.4e-10` at 30 AU (`2.3e5` inside
       `|beta-1| < 1e-4`; the on-disk Nordtvedt number is `eta_N = (-6.6 +- 7.2)e-5`, Genova et al. 2018,
       `prep_2026/planetary_doors/BOUNDS.md` line 43).

Equivalently the Nordtvedt parameter `eta_N = 4 beta - gamma - 3 - alpha_1 = 0` at PPN order.
### D8. FRW: the no-cosmic-aether theorem

On flat FRW in the cosmic foliation, `N = 1`, `N^i = 0`, `h_ij = a^2 delta_ij`, `P_i = P_i(t)`:

* the clock source vanishes **identically** (`D_i ln N = 0`), so nothing generates `P`;
* `W(u) = u^2/(2K) + O(u^3)` has its minimum at `u = 0`, so the potential does not break `P = 0`;
* the linearised EOM is `eta(Pddot_i + 3H Pdot_i) + K P_i = 0`, a massive vector with `m^2 = K/eta` (K9); with
  the framework's `eta = gamma` this is `m = sqrt(2)/L*`, `m/H_0 = 2.62e8` (robust for any `eta < 7e16 gamma`).

**Theorem.** On exact FRW with the cosmic foliation, `P = 0` is the unique solution of the P equation: it is the
potential's minimum, it has no source, and every linearised mode is a massive vector whose amplitude decays as
`a^{-3/2}` for `m >> H` (satisfied by `2.6e8`). Hence **no cosmic aether VEV**, hence no `O(1)`
preferred-frame background in the Solar System.

One loophole, stated: for `m <~ H` a homogeneous mode would freeze rather than decay. Even then CMB isotropy
bounds it, since a homogeneous `P` carries anisotropic stress `K P_iP_j`: `Pi/rho_crit < 1e-5` gives
`u = K|P| < 2.54e-12 m/s^2 = 0.027 a0` (K10). Unlike an Einstein-aether — whose norm is `1` by the unit
constraint, so its VEV is non-negotiable — here the VEV is `0` by the potential's minimum plus the absence of a
source. The uniqueness half is the coordinator's (`_parent/a22_no_cosmic_aether.py`, 4/4: `dW/du` has its
only zero at `u = 0`); the legs added here are the mass `m^2 = K/eta`, the `a^{-3/2}` decay and the
CMB-isotropy bound on a pre-existing mode.

## Status

**`CLOSED-DERIVED`** for `alpha_1 = 0`, `alpha_2 = 0`, `beta_PPN = 1` and the no-VEV theorem (D2, D3, D5–D8),
each earned from the action's own structure with no new fitted number. **`CONDITIONAL(linear branch,
r << lambda)`** for the numerical values: `a_P`, `alpha_1(r)`, the `beta` residual. The numbers use `L* = 24 pc`
(A20's surviving value); `a_P ∝ L*^{-2}`, so that is the worst case of the `[24, 90] pc` window. Two premises
are named and are *derived*, not assumed: the solution sits on the gradient branch (`F = 0`, `E = 0`, static)
and the cap is unsaturated (`u/a0 = 2.6e-6`, eq. 9).

## Checks (`a22_checks.py`, 13/13 PASS, exit 0)

| id | what it proves | measured |
|---|---|---|
| K1 | 3-Ricci formula `-(1/f)[2L''+4L'/r+L'^2/2]` on unit `S^3` and isotropic Schwarzschild | 0, 0 |
| K2 | `P = 0` branch is **exactly** isotropic Schwarzschild (lapse + trace residuals) | 0, 0 |
| K3 | (4)(5)(6) exact; identity (7) `lap^2 psi = -K rho/gamma` | 0 |
| K4 | (8) satisfies both Poisson equations identically; `a_P/B_E` | 6.61e-3 |
| K5 | `theta == 0` static; `d(theta^2)/dh|_0 = 0`; aether `alpha_1(c1=c3=c4=0) = 0` | 0, 0, 0 |
| K6 | `ln N_T`'s `w^2` coefficient `= w^2(Phi+Psi)`, isotropic, no `B`-linear term, `S = 0` | exact |
| K7 | `\|alpha_1\|` from (13) at 1 AU / 30 AU | 8.16e-14 / 7.35e-11 |
| K8 | no `r^-4` source at `O(rho^2)`; `beta` residual | 4.41e-10 |
| K9 | FRW EOM `eta(Pddot+3HPdot)+KP = 0`, source `0`, `m/H_0` (corroborates `_parent/a22_no_cosmic_aether.py`) | 0, 0, 2.62e8 |
| K10 | charge is load-bearing; CMB bound on a homogeneous `P` | `u < 2.54e-12 m/s^2` |
| K11 | framework identity `gamma = K L*^2/2` exact; `lambda` finite | 5.24e17 m |
| K12 | no `O(rho)` momentum density (clock shift-free, `E^2` quadratic) | 0, 0 |
| K13 | independent FFT + quadrature: `psi = mu/(gamma r)`, slope `= GM/L*^2` | 2.3e-6, 2.3e-6 |

Mutation (`--mutate`), each altering a **term**, each breaking a check and exiting 1: `drop_clock` (K3, K10),
`gamma_zero` (K3, K11), `theta_stress` (K5), `alpha1_forced` (K7), `frw_source` (K9), `beta_forced` (K8) —
records in `MUTATE.md`.

**Cross-check against lane A3** (run read-only from this lane; `a3_checks.py` 15/15 PASS at read time): its K0
prints `R3 = 4K(rho + div P + W + gamma d^2/2)` — the same charge, same sign, same `K = 4 pi G` as (4); its K7
gives `c_T^2 = 1` exactly; its K4 gives `Pi = O(P^2)`.

## The four gates

| gate | status after this lane | source |
|---|---|---|
| **lensing = dynamics** | `DERIVED` to `O(Psi)`: `Phi = Psi` at `O(eps)` (dust-like charge), first slip `O(Psi^2)`, `\|1-Phi/Psi\| = 2.6e-7` in a galaxy | A12 (11/11); A3 K4, K13; re-derived here (K12) |
| **GW speed** | `c_T^2 = 1` **exactly**: the TT kinetic term is `hdot^2/4` with no `beta_ADM` and no `P`; a naive `\|DP\|^2` stiffness would give `1+2K\|P\|^2` | A3 `a3_checks.py` K5–K7 (15/15, run from this lane) + coordinator 6/6; `FINAL_THEORY.md` §3 |
| **Solar System** | `alpha_1 = 0`, `alpha_2 = 0`, `beta = 1`, all passing by `>=2.3e5`. The **live** problem is unchanged and is not PPN: the MOND kernel's constant anomaly `a0` is `2557x B_E` (canonical) / `1279x` (quadrature). The P sector *adds* `a_P = 6.6e-3 B_E`, 151x inside | this lane (K4, K7, K8) + A4 (`a4_checks.py` 13/13, D2, K2, K9) |
| **stability** | linear response positive-definite at every acceleration, both interpolations; patched law monotone for `y_t > 0.06253`; principal symbol positive at all angles iff `beta_ADM > 2 eta a0^2/K`; P modes massive, `m/H_0 = 2.6e8` | A4 D7 (K11, K12); round-2 §4; this lane K9 |

## What this does not do

- **No second-order metric.** `beta_PPN = 1` comes from the source-exponent argument (D7), not from solving the `O(rho^2)` system; a full second-order computation would confirm it and is not done here.
- **No galactic-regime `alpha_1`.** D5–D6 are exact only for `r << lambda = 17 pc`. At `r >> lambda` the P field
  is MOND-slaved (`u ~ a0`, `|P| = u/K`) and the same `(1+2w^2)` rescaling would give an `O(w^2)` *relative*
  modulation of the phantom mass, i.e. an effective `alpha_1 ~ O(1)` where the PPN expansion is itself invalid
  (the field is logarithmic, not `1/r`). Not computed; it is the framework's real preferred-frame exposure — at
  `w = 369 km/s` a `3e-6` modulation of a galactic MOND field, a prediction rather than a bound.
- **The matching (1) is imported**, not re-derived (validated in `stage72_alpha2_first_principles_2026.py`);
  a wrong convention there would rescale `alpha_1`, `alpha_2` but not `beta`.
- **No strong-field** `alpha_hat_1`, `alpha_hat_2`; no binary-pulsar analysis. **No EFE**: `a_P` is the
  isolated-source monopole and a galactic external field would modify it.
- **`L*` is an input.** `a_P`, `lambda`, `M_crit` and `m/H_0` all scale with it.

## Next

1. **The deep-MOND preferred-frame response.** Compute `alpha_1^{gal}(w)` for `r >> lambda`. It is the only
   place the framework can produce an `O(1)` preferred-frame parameter, and D6's argument says the `(1+2w^2)`
   rescaling survives — so it must be either computed or bounded. Sharpest open test in this lane.
2. **Second-order metric**, to confirm `beta = 1` beyond (14) including the `O(rho^2)` slip.
3. **Book-keeping against A4.** `a_P = 2.42e-16 m/s^2` is a *second*, independent constant anomaly; it **adds**
   to the kernel's `a0`, so the ephemeris budget should carry both.
4. **`M_crit = 3.9e5 Msun`.** The `r_MOND > L*` threshold predicts no MOND below a globular cluster. Wide-binary
   and dwarf-spheroidal tests then probe `L*` directly — `L* = 24 pc` is falsifiable there, independently of `a0`.
5. **The covariant parent.** Check that `div P = rho - rhobar` (BRIEF §1) reproduces (7) with `rhobar` as the
   background subtraction; (7) is its static, asymptotically flat limit.
