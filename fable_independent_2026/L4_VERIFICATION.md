# L4 — independent verification of the lead's IC6 obstruction and IC7 repair

2026-09-08. Lane L4 of [CHARTER.md](CHARTER.md).
Script: [L4_verify_ic7.py](L4_verify_ic7.py) → [L4_verify_ic7.out](L4_verify_ic7.out). Exit 2 by design
(29 checks, 28 PASS; the single FAIL is the programme's 2-DOF requirement, not a reproduction failure).

Method: nothing under `closure_2026/integrable_clock_construction_2026/` was imported, executed or copied.
The action density and curvature coefficient

    h(rho,tau,xi,u) = (2E/m)(tau/J − rho^2/6) + m e^{(3u−2)xi} C − (kappa/2) e^{(3u−4)xi},   c = m e^{u xi} J

were transcribed by hand from IC4_ACTION.md / IC5_ACTION.md / TENSOR_BALANCE.md into sympy, differentiated
symbolically, and evaluated at 60 digits with mpmath. The auxiliary constraints `h_xi = h_u = 0` were solved with an
independent Newton iteration. Five control checks guard my own algebra, two of them GR limits.

## What IC6 hit, and what IC7 adds

**(a) The obstruction.** On the one-parameter isotropic family `lambda_i = −e^{−1/2} j` with the auxiliaries solved,
the reduced scalar quartic stiffness satisfies `S_4(1) = 0` and

    S_4'(1) = − e^{5/6} (5T−27)(8T−27)(8T+27) / (18 T^2 (4T−27))  <  0     for the frozen domain T > 27/4,

so `S_4 < 0` for every small `j − 1 > 0`, and `M_0 zeta_tt + S_4 k^4 zeta = 0` has real growth `~ k^2`.

**(b) The repair.** IC7 adds exactly one term, `Delta H_7 = ∫ d^3x V eta(r) c_7(rho,xi,u) Rbar^2`, with

    M = [[h_rr/4 + h_tau/12, D_t h_r/2],[D_t h_r/2, D_t^2 h]]|_{tau=0},   v = (c_rho/2, D_t c),   D_t = d_u − b d_xi,
    c_raw = v^T M^{−1} v / 8,   c_7 = theta(D) c_raw,   D = det(M)/det(M_star).

## Reproduced

Every load-bearing number of IC6_EVEN_CHARACTERISTICS.md, IC6_DIRAC_FLOW.md and IC7_CURVATURE_SQUARE.md that this
lane recomputed came out identical, to the precision the lead quotes:

| quantity | lead | this lane |
|---|---|---|
| auxiliary Hessian, normalised | `−[[24,−27],[−27,2T+135/8]]`, det `12(4T−27)` | identical, det `476.952638525` |
| branch tangent `dq/dj` | `(−(8T+27)/(4(4T−27)), −18/(4T−27))` | identical to 40 digits |
| `dJ_T/dj`, `dF/dj` | `−4(5T−27)/(3(4T−27))`, `−(5T−27)/(2 l^2 (4T−27))` | identical |
| `h_pp`, `h_p,chi`, `g_chi`, `h_pp'`, `g_p'` | exact identity + four closed forms | all five confirmed |
| `det(M_star)` | `−4 T^2 h0^2 / 81` | `−13.750109935689`, exact match, nonzero |
| **`S_4'(1)`** | boxed closed form | `−11.1407711251147987`, agrees to 6.7e-61 relative |
| `j=1.007`: `xi, u, S_4, lambda^2/k^4` | `0.24297809, 0.66347046, −0.07526051653, 0.03456985650` | all four |
| `c_7` at `j=1.007` | `0.00235189114143216` | `0.00235189114143216072` |
| sheared `xi, u, J_T` | `0.242752746344542675, 0.663589818477735377, 0.986102159712075428` | all three, 18 digits |
| `K`, `Omega_12`, Dirac singular values | `[[−14.971…, 16.372…],[…, −29.744…]]`, `0.06402066864`, `(40.31947, 4.396461)` | all, from my own Hessians |
| IC7 residual sheared quartic `S4_11 + 32 c_7` | `0.0151964888331` | `0.0151964888331` (12 digits) |
| IC6 tensor cone (TENSOR_BALANCE table) | `c_T^2 = 1` (IC6), `= J_T` (IC5 mutation) | both, symbolically exact |

The independently reconstructed witness is an exact stationary point of my own `h` (`|h_xi|, |h_u| < 1e-60`,
`F = 0`, `r = 1`), which validates the whole frozen constant set (`ell`, `T`, `sigma`, `A_R`, `B_R`, `a0^2`,
`Lambda`, `U`, `b`) before any of the above was computed.

**Confirmed claims.** The IC6 obstruction is real and is exactly as stated. IC7's coefficient is exactly as stated.
IC7's own limitation statements are also confirmed: the correction vanishes at the witness (`M11 = v1 = 0` there),
vanishes on the static plateau, and leaves the sheared quartic nonzero at the value it reports.

**The three things most likely to be wrong, checked:**

1. *Constraint algebra.* It closes at the secondary level. `{p_A, S_B} = V h_AB` is invertible at the witness
   (`det = 476.95`) and at the sheared state, so all four auxiliary constraints (`p_xi, p_u, S_xi, S_u`) are second
   class, the Dirac chain terminates, and the full 4×4 Dirac matrix has rank 4 with no null direction. Reproduced
   from my own Hessians. **It does not give 2 DOF** — see below.
2. *Is `c_7` action-derived or reverse-engineered?* `c_raw` is a rational function of partial derivatives of `h` and
   `c` alone: after substituting the frozen constants it has no free symbol besides `(xi,u,rho,tau)`. No wave speed,
   measured eigenvalue or new fitted constant enters. IC7's sentence — *"Neither measured eigenvalues nor a desired
   wave speed define it"* — is **confirmed as written**. The qualification is that `S_4 + 32 c_7 ≡ 0` is an
   *identity of the definition*: `c_7` is `−S_4/32` symbolically, for all `(rho,xi,u)`. It is an exactly tuned
   counterterm expressed in action derivatives, not a coefficient the action forced independently. Both readings
   are true; the file's own wording does not overclaim.
3. *Does the cutoff hide a singularity?* No. `theta ≠ 0` requires `|D−1| < 1/2`, i.e. `|det M| ≥ |det M_star|/2 =
   6.875 > 0`, so the inverse is never taken near a singular `M`. The one place `M` genuinely degenerates is the
   static branch `rho = 0` (there `M12 = D_t h_rho/2` vanishes with `rho`, so `det M = 0` exactly); `D = 0` there and
   `theta = 0`, so the zero extension is doing real work. Both `theta` and `eta` are `C^infinity` at their glue
   points (value and first three derivatives flat to `< 1e-30`), and the `|D−1|` kink sits strictly inside the
   `theta ≡ 1` plateau. The claimed `det(M_star) ≠ 0` holds exactly.

## Not confirmed / added by this lane

Nothing the lead states is **contradicted**. Three findings extend it.

**1. The repaired window is finite and small — quantified.** Along the same isotropic branch, `theta` leaves 1 at
`j = 1.0736445` and reaches 0 at `j = 1.1315852`, where the unrepaired `S_4 = −0.7341` (ten times the `−0.0753` at
`j = 1.007`) is restored in full *while `eta` is still 1* — i.e. still on the expanding plateau, with the IC6
obstruction operating and the IC7 term switched off. The repair covers `|j−1| < 0.074` of the isotropic family. The
lead says only *"Neither cutoff transition is certified healthy"* and *"a local isotropic construction"*; that is
consistent, but the transition is not a far-field detail — it is 7% away in trace momentum.

**2. IC7 detunes the tensor cone off flat backgrounds — quantified.** IC6's tensor luminality was exact: the `1/J_T`
factor cancels and `c_T^2 = 1` identically (reproduced here symbolically, both polarisations, plus the IC5 mutation
returning `J_T`). Adding `c_7 Rbar^2` gives, on any background with barred spatial curvature `Rbar_0 ≠ 0`,

    c_T,physical^2 = 1 − 4 c_7 Rbar_0 / c        (exact, diagonal barred class)

with `4 c_7/c = 0.008571` per unit `Rbar_0` at the sheared state. The lead flags the non-transfer qualitatively —
*"The earlier inhomogeneous odd-sector result is NOT transferred to IC7 when background bar R is nonzero"* — this is
its size and its form. It is a new constraint on the "next design equation": whatever fixes the sheared mixing must
also not spoil the exact `c_T = 1` that IC6 had bought.

**3. Degree-of-freedom count: 3, not 2.** This is the only FAIL. In unitary clock gauge the local phase space is 8
canonical pairs (6 barred-metric + `xi` + `u`) = 16. Four second-class auxiliary constraints remove 4. The lapse
`N = e^xi` is a *field with a second-class constraint*, not a Lagrange multiplier, so there is **no local first-class
Hamiltonian constraint**; only the 3 first-class spatial-momentum constraints remain. Count `= (16 − 4 − 6)/2 = 3`:
two tensor polarisations plus one gravitational scalar. The same counting rule returns 2 for ADM GR (control), and
the kinetic term's DeWitt supermetric was checked to carry the GR value `lambda = 1`, so the extra mode is *not* a
Hořava `lambda`-mode — it is the khronon-type scalar of the clock sector. It is genuinely dynamical and healthy:
the reduced scalar momentum Hessian `A_0 = det M / M22` is positive (`0.4615` at the witness, `0.4593` at
`j = 1.007`), so `zeta` has a positive kinetic term and cannot be gauged away.

The lead does not claim 2 DOF anywhere — IC6_DIRAC_FLOW.md says *"its count is not the field theory's polarization
count"* and IC7 says *"That fact alone is NOT a complete new Dirac or DOF proof."* Its own sector reductions agree
with 3: the even sector carries two canonical pairs `(zeta, gamma)` and the odd sector one. So this is a
requirement not met, not a claim refuted. The strategic consequence is the point: **IC7 is not a step toward two
degrees of freedom. It is a step that makes the third one well-posed** on a 7%-wide isotropic window.

## Scope — not verified here

- The `k^2` reduction giving the witness speeds `(1/3, 1)` and IC7's quoted scalar `c_s^2 = 0.388526918` at
  `k = 1e5`; that needs the background time derivatives of the lead's reduced system.
- The sheared antisymmetric mixing `N2_21 = 0.000563025148111` itself; only its IC7 consequence
  `S4_11 + 32 c_7` was checked.
- IC6_STRONG_AUXILIARY's Sobolev solvability, the odd-sector inhomogeneous geometry, and every empirical gate
  (PPN, galactic matching, measured G, cosmology) — all remain as the lead states them: OPEN.
