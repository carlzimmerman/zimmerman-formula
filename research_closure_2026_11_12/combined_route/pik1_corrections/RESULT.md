# Corrected PIK1 variation and FRM1 interpretation, 2026-11-12

**PIK1 linear invisibility: REFUTED as a universal statement. Corrected constrained
quadratic matter action: symbolically verified. Full coupled-gravity health and
the proposed static data gates: INCOMPLETE.** No completion is claimed.

This authorized forward correction preserves frozen criteria and historical
labels. It repairs the inference, supplies a runnable replacement for the broken
variation draft, and takes the remaining flat-gate possibility one step further.
The calculations use exact SymPy 1.14.0 identities; no external measurements,
cluster fits, cosmological integrations or coefficient fits enter.

## 1. Claim card and dependencies

Objects: `L_K=F(Q)S(Pi/Pi_c)`, `F(Q)=C(Q-1)^2`, `C=mu_K^2/(2K)>0`,
`K=4 pi G>0`, `Pi_c>0`, `Q=sqrt(-g^{mn}d_m tau d_n tau)`, and tangent
polarization `n.P=0`. `S(0)=1`. Coefficients are real. Boundary terms below
vanish for periodic or compactly supported perturbations. On FRW write
`tau=tau(t)`, `q=d tau/dt>0` in background cosmic time. The health statement
additionally assumes `q>1`, fixed metric, frozen background coefficients and
`gamma_L=0`; wavenumber is physical. It is a principal-sector calculation,
not the full linearized Einstein system on an exact cosmological solution.

Dependency chain: exact tangent constraint -> exact Pi in unitary gauge ->
quadratic action -> direct Euler-variation comparison -> auxiliary polarization
elimination -> scoped kinetic/dispersion statement. The inhomogeneous extension
uses only the exact fixed-clock polarization Hessian, not an assumed cosmological
dispersion relation. Cluster/galaxy profiles and observational gates are absent.

## 2. The missing terms

For ADM lapse `N`, shift arbitrary, and spatial metric `h_ij`, unitary gauge
gives `Q=q/N`, `P^0=0` and

    Q sqrt(-g) = q sqrt(h),
    Pi = (sqrt(h))^-1 d_i[sqrt(h) P^i].

Thus lapse and shift cancel from Pi exactly. In the scalar notation
`N=1+alpha`, `h_ij=a^2 exp(2 zeta) delta_ij`, the quadratic part of the added
gate action, after subtracting ungated `F(Q)`, is, modulo spatial boundaries,

    Delta L2 / a^3 = B alpha div(P) + (D/2) [div(P)]^2,
    B = [F(q)-q F'(q)] S'(0)/Pi_c = C(1-q^2) S'(0)/Pi_c,
    D = F(q) S''(0)/Pi_c^2.

The metric-trace contribution is exactly
`3 F(q) S'(0) div(zeta P)/Pi_c`; it is a boundary. The first-order action is
also a boundary, `F(q) S'(0) div(P)/Pi_c`. Neither statement removes the two
bulk quadratic terms. Metric tensor perturbations do not enter the gate at this
order except through the determinant; the quadratic computation resolves its
trace contribution. No Einstein-Hilbert variation is asserted here.

For `S=exp(-u)`, `check_quadratic.py` independently (a) varies the exact nonlinear
gate first and then linearizes, and (b) varies the proposed quadratic action.
Their lapse, polarization and metric-trace Euler derivatives agree identically:

    E_alpha = B div(P),
    E_P = -B grad(alpha) - D grad div(P),
    E_zeta = 0.

Deleting either the mixed term or the squared-divergence term breaks this
comparison. The historical witness remains: `q=2`, `C=Pi_c=k=1`,
`P^x=epsilon sin(x)` on `[0,2pi]` yields quadratic integrated action
`epsilon^2 pi/2`, although its first-order integral vanishes.

## 3. Fixed-metric principal sector and its limitation

On Minkowski with coefficients frozen, put `tau=q t+pi`. Enforcing tangency
before expanding gives

    P^0 = -grad(pi).P / (q+pi_dot),
    Q = q + pi_dot - |grad(pi)|^2/(2q) + O(perturbation^3),
    Pi = div(P) - grad(pi).P_dot/q + O(perturbation^3),
    A_i = -d_i pi_dot/q + O(perturbation^2).

The second-order Pi term matters: retaining only `delta Q delta Pi` gives the
wrong coefficient. Up to explicitly checked time/spatial boundaries, the full
clock/polarization principal quadratic action in this restricted calculation is

    L2 = F'' pi_dot^2/2 - (F'/q) |grad(pi)|^2/2
         + (1-B) pi_dot div(P)/q - K |P|^2/2 + D [div(P)]^2/2.

Here the `K|P|^2/2` term is the quadratic expansion of the original law's convex
potential about `P=0`. All `F` derivatives are at `q`. Eliminating the auxiliary
longitudinal polarization away from `K-D k^2=0` yields

    K_eff(k) = F'' + (1-B)^2 k^2 / [q^2 (K-D k^2)],
    omega^2(k) = (F'/q) k^2 / K_eff(k).

The corresponding polynomial dispersion identity is also checked. At
`K-D k^2=0` the displayed
elimination is invalid, not a legitimate division by zero.

For the exponential gate, `D>0` if `q>1`. If `1-B != 0`, just above
`k_*^2=K/D`, the kinetic coefficient is negative and `omega^2<0` because
`F'>0`. Explicitly, `q=2`, `C=K=Pi_c=1`, `k^2=3/2` give
`B=3`, `D=1`, `K_eff=-1`, `omega^2=-3/2`. More generally, with
`k^2=(1+eta)K/D`,

    lim_(eta -> 0+) eta K_eff = -(1-B)^2/(q^2 D) < 0.

This is a genuine negative-kinetic and growing-mode band of the restricted
fixed-metric principal theory. It is not a proof that the complete theory has
those modes: metric constraints and background equations were not included.
The exceptional `1-B=0` removes this clock mixing but still leaves a singular
auxiliary polarization block. No physical `Pi_c` or ultraviolet domain was fixed.

The original stiffness `-gamma_L [max(Pi,0)]^2/2` has no single quadratic Taylor
form at FRW `Pi=0`. This calculation sets `gamma_L=0` explicitly. Replacing the
one-sided term by an everywhere quadratic term would be a changed theory.

## 4. A flat gate: invisible at FRW, obstructed again at finite density

`S(u)=exp(-u^3)` is positive and nonincreasing, with `S'(0)=S''(0)=0`.
Consequently `B=D=0` about FRW, and the above quadratic sector is exactly the
ungated one. This supplies a counterexample to treating the exponential gate's
FRW obstruction as a universal no-go for all gates.

It does not establish health where the gate actually suppresses dust:

    S''(u) = exp(-u^3) (9u^4-6u) > 0
    for u > (2/3)^(1/3) = 0.8735804647... .

For a fixed clock/metric on any smooth finite-Pi background, Pi is linear in P.
The local second variation in polarization therefore contains

    delta^2 L = -delta P^T H_W delta P/2
                + D_net [div(delta P)]^2/2 + lower-derivative terms,
    D_net = F(Qbar) S''(ubar)/Pi_c^2 - gamma_active.

`H_W` is the positive Hessian of the convex law potential; on `Pbar != 0` its
eigenvalues are `K/(1-K|Pbar|/a0)^2` parallel to Pbar and
`K/(1-K|Pbar|/a0)` transverse, in the domain `K|Pbar|<a0`.
The original stiffness has `gamma_active=gamma_L` at strictly positive Pibar,
zero at strictly negative Pibar; at zero it is again not a smooth Taylor term.
Freezing the coefficients, the polarization constraint block is

    H_W - D_net k k^T,
    det = det(H_W) [1-D_net k^T H_W^(-1) k].

If `D_net>0`, this block is singular at a finite k and changes sign in a
direction beyond it. For `F=Pi_c=1`, `ubar=1`, `gamma_active=0`,
`H_W=diag(4,2,2)`, one gets `D_net=3/e` and a singularity along the first axis
at `k^2=4e/3`. At twice that squared wavenumber the first eigenvalue is `-4`.
These are admissible local jets; no global on-shell background is constructed.

There is a uniform reason this curvature issue returns. Let S be C2,
nonnegative, nonincreasing and nonconstant on `[0,infinity)`. The mean value
theorem gives `S'(u1)<0` somewhere. If `S''<=0` everywhere after u1, then
`S'(u)<=S'(u1)<0`, forcing S to cross zero at finite u. Hence `S''>0` somewhere.
Flatness at the origin does not avoid all positive-curvature regions.

**Exact scope:** the P block loses positivity/invertibility if `D_net>0` and the
required wavelengths are in the model's domain. This does not prove the whole
constraint system is singular or that a physical ghost exists. For example,
the block matrix `[[0,b],[b,1]]` is invertible when `b!=0` despite its zero upper
block; the checker retains this counterexample to that tempting overclaim.
Actual halo backgrounds, active stiffness, metric/clock mixing and the physical
wavelength domain remain to be evaluated. The flat gate is not a demonstrated
rescue and is not globally refuted here.

### Fixed stiffness cannot cover an unrestricted clock-rate domain

Let `gamma_active=gamma>0` be fixed and finite, and select a finite `u_*` with
`s_*=S''(u_*)>0`. If Q and Pi are independently variable local states with
`Q>1`, then

    D_net = C(Q-1)^2 s_*/Pi_c^2 - gamma > 0
    whenever Q > 1 + Pi_c sqrt[gamma/(C s_*)].

The constructive choice `Q=1+2 Pi_c sqrt[gamma/(C s_*)]` gives
`D_net=3 gamma` exactly. Thus **no fixed finite gamma and finite positive Pi_c
keep this polarization block positive for every unrestricted Q>1 and every
u>=0** of a nonconstant positive decreasing C2 gate. For gamma=0, any Q>1
at a positive-curvature u already has `D_net>0`. This remains a statement
about the P block at unrestricted spatial wavenumber, not a ghost theorem.

For a specified allowed joint state domain A and constant gamma>0, the exact
coefficient condition that avoids this particular loss at all spatial k is

    Pi_c^2 >= (1/gamma) sup_((Q,Pi) in A)
                    { F(Q) [S''(Pi/Pi_c)]_+ } .

Here `[v]_+=max(v,0)`. A maximum may replace the supremum when attained. If A
is defined in physical Pi coordinates, this condition is implicit in Pi_c,
since changing Pi_c also changes the gate argument. If the states obey a
derived relation `Q=Q(u)`, use that joint relation inside the supremum; an
independent maximum over Q and u can be needlessly strong.

For the independent box `1<=Q<=Q_max`, `u>=0`, the flat gate has

    sup [S''(u)]_+ = 2.05653250517...,
    attained at u = [1 + sqrt(7)/3]^(1/3).

The exact expression and stationary condition are checked in
`check_stiffness_bound.py`; this gives the explicit design condition
`Pi_c^2 >= 2.05653250517... C (Q_max-1)^2/gamma` for that box. A finite
physical wavenumber cutoff can weaken the all-k requirement: the exact
directional condition is `D_net k^T H_W^(-1)k < 1` whenever `D_net>0`.
No cutoff has been derived here.

**The needed state bound is missing from the source.** QX17's action/definitions
(`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md:21-40`) make Q the
positive norm of the clock gradient; they give no finite upper bound on Q.
The logarithmic W bounds `K|P|<a0`, which bounds the amplitude of P, not its
divergence or Q. PIK1's criteria (`FROZEN_CRITERIA.md:14-31,40-51`) introduce a
fixed Pi_c and no invariant joint `(Q,Pi)` domain or proof that evolution stays
inside one. These constraints alone allow independent local Q and derivative
jets; this does not assert every such jet extends to an on-shell global solution.
Indeed QX17's FRW solution has Q growing without bound towards early times but
Pi=0, where the flat gate has zero curvature: correlated physical states can
avoid the product bound even when Q alone is unbounded. A joint domain must
therefore be derived from the actual background/dynamics before fixed stiffness
can be credited with a physical rescue.

## 5. FRM1 correction

At fixed profile with `g_b,f=g_bar/F_b`, `F_C=1`, `u=a0/g_bar>0`,

    X = [sqrt(1+4u F_b)-1]/(2F_b)
      = 2u/[1+sqrt(1+4u F_b)] <= u.

That channel ceiling holds (also for `0<=F_C<=1`). It does not hold for the
general ledger `X=X_L(g_b,f)F_C/F_b`. The executed exact counterexamples are
`u=1,F_C=2,F_b=1,g_b,f=g_bar`, giving `sqrt(5)-1>1`, and
`F_C=F_b=1,g_b,f=g_bar/100`, giving `(sqrt(401)-1)/2>1`.
Neither counterexample supplies a physical history; they identify missing
hypotheses in the original universal claim. The known prior DD1/HIS1 exposure
also makes the class-band hits retrospective, as the linked lane correction
explains. Frozen labels and numerical class outcomes were not altered.

## 6. Executed checks and provenance

| Run | Outcome | Meaning |
|---|---|---|
| `run_corrected` | 27/27 checks, exit 0, 2.32 s | Exact quadratic identities and scoped principal spectrum agree |
| `run_legacy` | exit 1, expected | Original periodic invisibility assertion fails |
| `run_drop_mixed` | exit 1, expected | Removing mixed term breaks direct-vs-quadratic variation |
| `run_drop_square` | exit 1, expected | Removing squared divergence breaks direct-vs-quadratic variation |
| `run_finite_density` | 9/9 checks, exit 0, 0.19 s | Finite-Pi Hessian, curvature threshold and determinant identities agree |
| `run_stiffness_bound` | 6/6 checks, exit 0 | Unrestricted-Q exceedance, finite-domain condition and flat-gate curvature maximum agree |

Each directory has its own v2 computation manifest and captured stdout/stderr.
Failed-control manifests deliberately say `failed`, not `completed`.
Commands are recorded as argv in the manifests; minimal reruns are:

```bash
python3 research_closure_2026_11_12/combined_route/pik1_corrections/check_quadratic.py
python3 research_closure_2026_11_12/combined_route/pik1_corrections/check_finite_density.py
python3 research_closure_2026_11_12/combined_route/pik1_corrections/check_stiffness_bound.py
python3 research_closure_2026_11_12/combined_route/pik1_corrections/check_quadratic.py --mutation drop-mixed
python3 research_closure_2026_11_12/combined_route/pik1_corrections/check_quadratic.py --mutation drop-divergence-square
python3 research_closure_2026_11_12/combined_route/pik1_corrections/legacy_witness.py
```

The last three commands are expected to return nonzero. The old entrypoints
`fable52_push/PIK1_pi_gated_dust/pik1.py` and `pik1_var.py` now run the corrected
quadratic checker and announce that the historical full pipeline is not run.
Original drafts remain byte-identical under `historical_drafts/`.

SHA-256:

| Artifact | Hash |
|---|---|
| `check_quadratic.py` | `36f1edf615766b4ff8fa93f696e58ba8ea118c7caf008dc45003e531f01fd149` |
| `check_finite_density.py` | `591a9e0db716c1104401e527432f4370210337f8e6f885140d41095535889147` |
| `check_stiffness_bound.py` | `594a715a29ddbebbab612cc95fe90430bdfc6dc00d0a5d3ca53dec099d96c647` |
| original `pik1_var.py` | `b72b1e91e088f22e620f596803e60f9a441d94a2f3b45ddcbcc16ae9a361aa99` |
| original `pik1.py` | `e99c3d2ed67c62021df3ccc74e13dc174a1a27303098c74e384dad5959c1591b` |

This is self-review of a new derivation, with two operation-order checks and
wrong-expression controls, not an independently authored full-theory audit.
The root reviewer independently reproduced the earlier periodic counterexample.
Repository revision, dirty state, runtime and input/output hashes are in each
manifest. No commits were made by this subtask.

## 7. Smallest remaining implication

For the surviving flat gate, derive a preserved joint `(Q,Pi)` state domain
and test the stiffness bound above. Construct or specify an actual background
that enters its positive-curvature region, then derive the **complete constrained
metric-clock-polarization principal symbol**, retaining the active stiffness.
Determine whether its physical modes are healthy over the wavelengths the
effective action claims to describe. A singular auxiliary sub-block alone is
insufficient. Only a successful result there warrants using the gate in the
mass-retention/EFE model and recomputing its data gates. Independent formation
and transport of the required conserved charge remain separate obligations.
