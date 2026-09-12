# Local boosted source and tensor checkpoint

Base revision supplied by the parent: `ac2052ae0`; no Git command was run.
This directory records a bounded exact SymPy derivation for the unchanged
action `P(X,tau)-V(tau)+s W(Y,tau)+gamma X Box chi`, signature -+++,
`X=-grad(chi)^2`, `s=sqrt(-grad(tau)^2)`. The metric extension assumes
constant positive Einstein coefficient M2 and minimally coupled matter.
No coefficients are fitted. No PPN parameter is extracted.

At an aligned timelike jet, write chi=q t+pi, tau=s t+sigma. The quadratic
derivative action on a fixed flat metric is exactly

    L2=(PX+2q² PXX) pi_t² - PX |grad pi|²
       +s WY |grad pi-(q/s)grad sigma|² - W0 |grad sigma|²/(2s).

Consequently the exact background identity Y=0 used in raw L204 does not
remove perturbation mixing or preferred-frame response. The raw L204's
double-filter transmission is an additional assumption; it was not run here
because its top-level execution writes an old result file.

For nonzero clock-frame spatial k and W0-2q²WY != 0, clock elimination gives

    sigma/pi = 2q s WY/(2q²WY-W0),
    K0=2PX+4q²PXX,
    G0=2PX-2s WY W0/(W0-2q²WY).

At k=0 the clock principal row vanishes. The quotient above is not a
homogeneous clock equation; lower derivatives and constraints decide it.
W0=0 cancels the entire WY contribution after regular clock elimination.
For an isotropic covariant scalar Hessian diag(H00,Hs,Hs,Hs), direct cubic
linearization and Einstein curvature elimination give

    K=K0+12 gamma Hs+6 gamma² q⁴/M2,
    G=G0+4 gamma(-H00+2Hs)-2 gamma² q⁴/M2.

These agree with the existing cubic metric tensor calculation. They are
principal coefficients, not a solved background. Coefficient derivatives,
clock masses and lower derivative metric terms are excluded. In particular,
their omission is not uniform near a vanishing principal denominator.

For an eternal conserved dust source moving at speed w relative to the
clock, its Fourier support has omega=w*k_parallel. With Gamma²=1/(1-w²),
rho the proper dust density and D=G|k_clock|²-K omega_clock², direct trace
reversal of its stress gives

    a=gamma q²(2 Gamma²-1)/M2,
    pi_hat=-a rho_hat/D,
    D_source_rest=G k_perp²+Gamma²(G-Kw²)k_parallel².

The source is physical minimal matter, not an assigned scalar forcing.
In the stationary source frame R00=Delta Phi; the same cubic stress yields

    Phi_hat=-rho_hat/(2M2 |k_source|²)+a*pi_hat,
    Phi_hat_cubic=-a² rho_hat/D.

This computes the leading local lapse residue as well as the scalar
residue. It excludes homogeneous metric solutions and lower derivative
terms, and is not a full post-Newtonian metric or a global Green function.
No cancellation follows merely from Y_background=0.

Conditionally K>0 and 0<cs²=G/K<w², the moving source encounters angular
zeros cos(theta)=+-cs/|w|. The leading scalar and lapse residues are nonzero
where gamma*q²*rho_hat is nonzero. This statement is a local symbol test;
choosing retarded boundary conditions and solving across the cone remain
necessary. At cs=0, the angular degeneracy is quadratic, not a simple pole;
for a stationary source the entire stationary principal symbol vanishes.
Tiny positive cs gives a simple angular residue proportional to 1/cs at
fixed remaining quantities, without proving such a family solves this action.
All six archived aligned exterior jets have positive K; four have negative
G and two have positive G. The positive rows (indices 138 and 184) have
cs²=0.00044544346 and 0.00009662190. They admit the conditional moving cone
only at source speeds above their respective sound speeds, approximately
0.0211 and 0.00983 in units c=1. Their full health and a localized moving
solution are not established. The independent re-evaluation matches the
archived coefficients to 1e-12; the first jet has K=2.18438106049 and
G=-0.00339447314.

## Tensor/light cone checkpoint

For homogeneous aligned FLRW, use spatial metric a² exp(h), tr h=0. Its
volume is independent of h, X=q², s=tau_dot and Y=0. Thus P/W/V add no TT
principal derivative term. The homogeneous cubic ADM term is
`-(2/3) gamma a³ q³ K`; K=3H identically, so it adds no TT principal kinetic
term either. Direct curvature and ADM computations for a plus-polarized
wave give the rotationally completed tensor principal action

    S_T = (M2/8) integral dt d³x a³
          [dot h_ij dot h_ij - a^-2 partial_k h_ij partial_k h_ij].

The tensor script differentiates this derived plus-polarization Lagrangian
to obtain kinetic coefficient M2*a³/2 and coordinate-gradient coefficient
M2*a/2. It independently constructs F_munu for transverse A_x(t,z), raises
both indices with the FLRW inverse metric, and evaluates -sqrt(-g)F²/4.
The resulting Maxwell action is a*A_t²/2-A_z²/(2a), giving kinetic
coefficient a and coordinate-gradient coefficient 1/a. For each field,
physical speed squared is computed as a² times the ratio of gradient to
kinetic coefficients; both simplify to 1. The speeds are calculated values,
not assigned constants. This result does not equate the scalar sound
speed with either cone. A measured arrival-time offset still requires the
source emission-time offset and propagation history; this computation
does not calculate gamma-ray production or strong-field wave generation.

## Verification and remaining implication

From the repository root, run each command with `python3 -B`:

    .../boosted/derive_boosted.py --output .../boosted/result.json
    .../boosted/test_boosted.py
    .../boosted/check_archived_jets.py --output .../boosted/archived_jets.json
    .../boosted/tensor_cone.py --output .../boosted/tensor_result_v2.json

Here `...` is `qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026`.
Python 3.9.6, SymPy 1.14.0. All commands completed with exit 0. The first
script has 21 exact residual checks; tests independently invert the raw
two-field matrix, inspect k=0 before division, use an exact sound-cone
fixture, test a boosted perturbation projector, and reconstruct the dust
source in its own rest frame. The revised tensor script has 13 explicit
checks and records its own source hash in tensor_result_v2.json. The older
tensor_result.json is preserved as historical output; use v2 for the
computed tensor/Maxwell coefficient ratios.
Scripts print JSON or write only to an explicitly requested --output path.
The archived-jet computation is a check on rounded stored inputs, not a
fresh background integration or interval certificate. Source hashes are
recorded in result.json and archived_jets.json; the parent can add full
execution provenance without this subtask invoking Git.

The exact remaining implication is to establish an on-shell localized
background, its lower derivative operator and global retarded metric response,
then match the physical metric to a defined PPN expansion if desired.
The local denominator and minimal-dust residue established here neither
supply that matching nor support the L204 screening identification.
