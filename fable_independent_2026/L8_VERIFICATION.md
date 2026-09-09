# L8 — independent verification of the lead's IC8, IC9 and IC10

2026-09-08. Lane L8 of [CHARTER.md](CHARTER.md), continuing [L4_VERIFICATION.md](L4_VERIFICATION.md).
Script: [L8_verify_ic10.py](L8_verify_ic10.py) → [L8_verify_ic10.out](L8_verify_ic10.out). Exit 2 by design
(37 checks, 36 PASS; the single FAIL is the programme's `N_grav = 2` requirement read as a total mode count, not a
reproduction failure).

Method: nothing under `closure_2026/integrable_clock_construction_2026/` was imported, executed or copied. The IC10
pressure, the IC9 optical coefficients and the IC8 shear coefficients were transcribed by hand from
`IC10_LOCAL_CLOCK.md` / `OPTICAL_ALIGNMENT.md` / `IC5_ACTION.md` into sympy, differentiated symbolically, and evaluated
at 50 digits with mpmath. The auxiliary equations (`P_w = 0` for IC10, `h_xi = h_u = 0` for IC9) were solved with my own
Newton iteration. Six controls guard my own algebra, three of them GR limits.

## Answer to question 1 — the degree-of-freedom count

**Unchanged: 3.** IC8, IC9 and IC10 do not remove the extra mode L4 found in IC5/IC6/IC7. IC10 says so itself —
*"locally (24-16-2)/2=3 physical modes: **two tensors plus one genuine clock**"* — and its arithmetic reproduces
(L8-D1). The two counting schemes agree: L4's unitary-gauge `(16 − 4 − 6)/2 = 3` and IC10's covariant
`(24 − 16 − 2)/2 = 3` are the same number.

**What did change is the third mode's character, and that is the substantive result** (L8-D3). In IC5/IC6/IC7 the extra
scalar was *gravitational*: the lapse carried a second-class constraint, there was no local first-class Hamiltonian
constraint, and the khronon propagated inside the metric sector. On IC10's η = 1 plateau the metric sector is exactly
Einstein — DeWitt λ = 1 identically, `m* = m e^{-1/6} > 0` — the Hamiltonian constraint is first class again, and the
third mode is a shift-symmetric k-essence **clock** outside the gravity sector. The same counting rule that returns 2
for ADM GR returns 3 for GR + one k-essence scalar (L8-C2, L8-C3), which is exactly what IC10's plateau is. So
`N_grav = 2` and `N_clock = 1`.

Fried-chicken requirement 2 reads: *"Exactly two propagating gravitational DOF, N_grav = 2 — only the two tensor
polarizations. … A genuine matter or clock scalar is allowed ONLY if explicitly counted separately and shown healthy."*
On the lead's sampled window the third mode **is** separately counted and healthy — `P_X > 0`, `Q_clock > 0`,
`0 < c_s^2 < 1`, `ρ_clock > 0` at S = 0.1, 0.15, 0.2 (L8-D4). Read against requirement 2 as written, IC10's plateau
satisfies it there; read as a total mode count, it does not. Both readings are recorded; the FAIL line is the second.

## Answer to question 2 — does IC10's plateau do what it says?

The claim, extracted as an equation:

    S10|_{eta=1} = int sqrt(-gt) [ m* Rt/2 + P(Xt,w) ] + Sm[e^{2w} gt, psi],   m* = m e^{-1/6},
    gt = e^{-2w} g,  Xt = -gt^{mu nu}T_mu T_nu/2,  S = -ln(2 Xt)/2,  xi = S+w,  u = (S+2w)/(S+w),
    P = -m e^{4w}[Lambda + a0^2 U(u^2)] + kappa e^{2w} Xt,   with the w equation ALGEBRAIC: P_w = 0.

**Yes, exactly.** Every step verified independently and symbolically:

| step | result |
|---|---|
| the pressure the run printed vs. the pressure the document specifies | identical, symbolic zero (L8-P1) |
| chart `xi = S+w`, `u = (S+2w)/(S+w)`, `det ∂(S,w)/∂(xi,u) = xi` | confirmed; excluded locus `S+w=0` **is** `xi = 0` (L8-P2) |
| Legendre elimination `P_TF = m J9 Q_TF/2`, `p = -m J9 Q` | confirmed from my own variation (L8-P3) |
| conformal cancellation of the metric sector | exact: every power of `w` cancels, leaving `m e^{-1/6}` (L8-P4) |
| `[Q_TF^2 - 2Q^2/3 + Rhat]` is the ADM Einstein density | confirmed for generic `K_ij`, `h_ij` (L8-C1) |
| clock sector maps to `P(Xt,w)` with `X = e^{-2w}Xt` | confirmed (L8-P5) |
| `P_w = 0` algebraic and local; `P_ww != 0`; root unique in `-S/2 < w < 0` | confirmed (L8-P6, P7, P8) |
| `A = P_ww Q_clock/Q_bare`; reviewer's `A = 58.2357645080571` at S = 0.15 | identity confirmed, number reproduced (L8-D5) |

The structural content of the IC9 → IC10 step is isolated in L8-P9: **IC10's trace kinetic term restores the GR DeWitt
supermetric identically (λ = 1 for every J9), while IC9's compact Lagrangian gives λ = 1/3 + 2/(3 J9)**, equal to 1 only
at the witness `J9 = 1` (w = −1/12). IC9's metric sector is not Einstein off the witness; IC10's is. That is what buys
the clean clock identification, and it is a real change of action, not a re-description.

Scope, verified as a limit rather than asserted (L8-P10): the cancellation works because `J9` carries exactly the factor
`e^{-2w}`, which lives only in the η = 1 term. Set η = 0 and the same reduction leaves a residual `e^{2w}`. The
"Einstein + clock" form is a statement about the expanding plateau, not about the theory.

## Answer to question 3 — do IC8 and IC9 close L4's two liabilities?

**IC9 closes both, structurally. IC8 closes neither.**

**Liability 1, the narrow repair window** (L4: *"the repair covers |j−1| < 0.074 of the isotropic family"*, an artefact
of IC7's `theta` cutoff switching off). IC9's curvature-response vector vanishes **identically**: with
`D_t = ∂_u + xi/(2−u) ∂_xi` — the null direction of IC9's replacement gradient term `|D S|^2` — both components of
IC7's `v = (c_rho/2, D_t c)` are zero for all `(rho,xi,u)`, because `K9` and `c9` depend only on the optical scalar
`S = (2−u)xi`. So IC7's quartic `S_4 = −4 v^T M^{-1} v ≡ 0` with no counterterm and no cutoff, and the window does not
arise (L8-A1). IC8 does **not** achieve this: `D_t c8 ≠ 0` (= 6.4315058 at the witness), so IC8 still carries IC7's
cutoff-defined `d8` and inherits its finite window (L8-A5).

**Liability 2, the tensor-cone detuning** (L4: `c_T^2 = 1 − 4 c_7 Rbar_0 / c`, size 0.008571 per unit `Rbar_0`). IC9
states *"There is **no curvature-square term**"*; with `c_7 = 0` L4's own formula returns exactly 1 for every `Rbar_0`
(L8-A2). Independently, IC9's cone identity `K9 c9 = 2 e^{2S}` holds identically in `(xi,u)`, so `c_T^2 = 1` on every
background of the family, from the same reduction that returns 1 for pure ADM GR (L8-A3). IC9's table entry is confirmed
as an exact identity, not a fit.

**One scope caveat on how that headline reads** (L8-A4). The same identity holds for IC8: `K8 c8 = 2 e^{2S}` identically,
so IC8's *principal* cone is also exactly 1 — yet IC8's own report says

> "on the re-solved sheared background the even tensor speed squared approaches approximately 1.00244, 1.01257 and
> 1.02487 on the three axes"

Those numbers come from the finite-k companion-matrix evolution, not from the principal symbol. IC9's table reports only
the principal quantity, and the corresponding finite-k number is not in IC9's output. So IC9's `cT2 = 1` does not by
itself demonstrate that IC8's detuning is absent in IC9. The gap is in what was reported, not in what was claimed —
IC9's own nonclaims already say "no general-direction characteristic proof".

Also confirmed as written: IC9's `a > 0` with no positive-x pole holds exactly when `T > 27/4` — the denominator root is
`x = (2916 − 432T)/[(64T+243)α]`, negative iff `T > 27/4`, zero at `T = 27/4`, so 27/4 is the exact threshold (L8-A6);
and IC9's own admitted residual reproduces exactly, `d = −1/9 < 0` with uncancelled pole residue `−81/(4α^3)` (L8-A7).

## Answer to question 4 — spot-checks of `optical_run_001/`

Everything rebuilt reproduced to the precision the lead quotes.

| quantity | this lane |
|---|---|
| all 24 numbers of IC10's three plateau rows (w, u, P_X, Q_clock, c_s², energy, physical H, r) | worst relative difference 2.4e-24 (L8-R1) |
| FLRW quadrature: 0.108584184534843401 / 0.0821638533391028370 / 0.110756742119829669 | all three; conserved clock charge closes to 1.0 (L8-R2) |
| next η = 1 boundary S = 0.230723991364997997, u = 0.587907209285499307, c_s² = 0.242306706149330325 | all, r = √5/2 (L8-R3) |
| outside-plateau controls S = 0.5 and S = 1, including c_s² = −0.604346678994200880646694 | all (L8-R4, D6) |
| IC9's principal table: ξ, u, J9, scalar speeds 0.181932469587580540 / 0.203829766908273217 / 0.198458457703891493, scalar mass 176.694087400156673, passive Hessian −24.847606040647032 | all (L8-R5) |
| cross-lane: IC9's passive Hessian **is** L4's verified auxiliary Hessian rotated into the fixed-S direction | confirmed exactly (L8-R6) |

`friedmann_residual = 0.0` is definitional, not a check: `H` is defined as `sqrt(energy/(3 m*))`. `charge_ratio = 1.0`
is a real check and passes.

## Confirmed / unconfirmed / contradicted

**Confirmed.** Every load-bearing IC8/IC9/IC10 number this lane rebuilt came out identical. The IC10 plateau reduction
is an exact field redefinition and does what it says. The IC9 → IC10 DeWitt repair is real. IC9 closes both liabilities
L4 raised against IC7, structurally rather than numerically. IC10's own limitation statements — the η = 1 restriction,
the excluded `xi = 0` chart locus, the `c_s^2 < 0` failure at S = 1, "not a global IC10 Dirac certificate" — are all
confirmed as written. **Nothing the lead states is contradicted.**

**Unconfirmed (not attempted here).** IC8's and IC9's finite-k companion-matrix speeds; IC10's full nonlinear
distribution-valued gravitational bracket (the lead does not claim it); everything off η = 1 — transition,
matter-coupled characteristics, strong coupling, PPN, measured G, lensing, galactic matching, y = 0, realistic
cosmology. All remain as the lead states them: OPEN.

**One new liability, added by this lane (L8-D7, L8-D8).** The healthy window is strictly smaller than the η = 1
plateau, and the difference was never scanned. Continuing the same branch down in S, with `|P_w| < 1e-37`, `u` in
`(0,1)` and the auxiliary root still unique throughout:

    eta = 1 lower edge (r^2 = 3/4)   S = 0.0016326245
    Q_clock = 0  (ghost below)       S = 0.026664091
    c_s^2 = 1    (superluminal below) S = 0.037700985
    eta = 1 upper edge (r^2 = 5/4)   S = 0.230723991

So inside η = 1 there is a ghost region `S < 0.0267` and a superluminal band `0.0267 < S < 0.0377`. The lead's three
samples and its reviewer's 101-point scan all sit in `0.1 ≤ S ≤ 0.2`, entirely inside the healthy part. This matters
because of direction: IC10's own law `dS/dtau = 3 H c_s^2 > 0` makes S increase with time, so running the lead's own
S = 0.1 → 0.2 solution **backwards** drives it through `c_s^2 = 1` and then through `Q_clock = 0` while η is still
exactly 1. The certified healthy region in the clock variable is `0.0377 < S < 0.2307`, not the plateau.

That is a bound on the past of this solution, not a refutation of any sentence in IC10 — the lead claims only
"computationally verified only in the stated range", and the stated range is inside the healthy part.
