# IC42: fourth-time preservation decides the IC41 profile

Base 32f7dc6ffdd685ed9e50e9bf53a1500ec5f103d6. The previous turn made
progress by constructing a numerical third-time-compatible profile. The full
gravity target remains OPEN. Carl requested credit efficiency, so this run
tests that fixed profile before any interval-root certificate or broader search.
No action, kernel, coefficient table or initial data were refitted. All prior
constructions and outcomes remain preserved.

## Fourth-order matter terms from the same action

Use pressure P=c_P(v^2-k)^n, n=(1+w_f)/(2w_f), and fix canonical j=P_v.
Implicit differentiation gives v_k=(1-w_f)/(2v0) at k=0. Since
H_k=j/(2v), its Hamiltonian expansion is

    H=c_H j^(1+w_f) + j k/(2v0)
      - (1-w_f) j k^2/(8v0^3) + O(k^3),
    v0=(1+w_f)c_H j^w_f,  k=exp(-2Q) g^2.

c_H is the Legendre-dual energy normalization, not an assertion c_H=c_P.
The quartic coefficient h4=-(1-w_f)j/(8v0^3) is negative even for a healthy
fluid (as in expanding a positive square root). Its sign alone is not a ghost.

Minimal coupling gives the clock trace contribution
3j H_j-4H+2kH_k. Thus its quartic part is 3(1-3w_f)h4 k^2.
The independent radial/angular metric variations give added trace and shear
flows exp(S)(2-9w_f/2)h4 k^2 and 2 exp(S)h4 k^2.
The extra canonical j flux is

    4 exp(S-4Q) h4 [3g^2 g_r
        +(S_r-Q_r+2/r+(1-3w_f)j_r/j)g^3].

The sigma flow is the radial derivative of exp(S) H_j. These terms are included
before differentiating four times. Initially g=0, so the old second/third
results are unaffected, but a fourth-order calculation cannot omit these terms.
O(k^3)=O(t^6) does not affect this gate. The radial momentum constraint is
independently evaluated, not imposed after evolution.

## Exact fourth-time pin identity

Let A=eta exp(S), W+A ell=0, ell=ell_t=0 initially, E=W_tt, T=W_ttt,
and V=W_tttt. Differentiation of the actual multiplier equation gives

    V + A ell_tttt + 4 A_t ell_ttt + 6 A_tt ell_tt = 0.

Eliminating the lower multiplier derivatives yields the necessary condition

    R = V - 4 B T + (12 B^2-6 D)E = O(eta),
    B=A_t/A, D=A_tt/A.

Ratios are interpreted by one-sided Laurent expansion, never division by tiny
sampled eta. For x=a delta+c delta^2/2+..., x_t=t0+t1 delta+..., b=1/4:

    B = b_-1/delta + b0 + O(delta),
    b_-1=4t0/a,
    b0=4t1/a-2t0 c/a^2+4t0/b+U0,
    D = 12t0^2/(a^2 delta^2) + d_-1/delta + O(1),
    d_-1=24t0 t1/a^2-12t0^2 c/a^3+32t0^2/(ba)+4x_tt/a+8U0 t0/a.

On exactly compatible lower jets, the quadratic requirement is particularly
simple:

    R_rr(0) = V_rr(0) - 6 E_rrrr(0) (x_t/x_r)^2 = 0.

This identity is derived symbolically. The cubic condition in the executable
also retains E's fifth spatial derivative, T's fourth, and the Laurent
coefficients. The actual lapse operator fixes S_ttt and S_tttt; it is not
replaced by a prescribed evolution equation. Pin contributions to the metric
and lapse variations contain (w-wc) and vanish on the pinned branch; their
clock variation, eta exp(S)ell, is retained in the identities above.

## Result

At the fixed IC41 profile, the moving-face-corrected fourth-time derivatives are

    R_rr  = -4862983801.45869141730907177191498
    R_rrr = -1394597285573.36891922578719557727

in the existing normalized model units. Working at 40/60 digits and spatial
degrees 11/12 reproduces these to relative discrepancies below 2e-30.
The lower third-time residual is still below 4.9e-25 (the rounded numerical
root), while the fourth momentum residual is below 2.4e-50 at 60 digits.
The computed lapse-boundary matrix determinant is 499101.5721590787, nonzero;
it is NOT a Poisson-bracket determinant.

Even granting exact vanishing of the lower jets, this nonzero quadratic term
would force

    ell_tttt ~ -b^4 R_rr/[2 exp(S0)a^4] delta^(-2).

Thus the IC41 profile has not supplied a regular evolving solution. The
numerical evidence rules out treating that profile as closure; it is not an
interval-certified universal no-go for all nearby data or for the action.
This result does not retract the lower-order conditional calculation. It
identifies the next independent equation that calculation did not satisfy.

## Verification and credit

All newly created scripts executed. The new tests first failed because the
implementation was missing, then passed. The combined targeted suite has
12 passing tests, child exit 0. Both scientific runs use the documented
--strict OPEN sentinel: child exit 2, runner exit 1, not Python exceptions.
Three manifests record commands, hashes, runtime and limits; all validated.
No empirical analysis or Lean certificate is claimed. The earlier 328-test
regression run remains at the unchanged IC41 checkpoint; it was not rerun here.

Mathbox computation-audit separated finite evidence from exact existence;
proof-audit exposed the fourth-order matter and moving-face obligations.
Self-proofreading covered this note and its definitions; no proofreading-driven
mathematical-token changes. Credit Carl Zimmerman for the original framework
and clock direction; L44's activation suggestion remains credited in IC39.

## Next route, not another isolated jet fit

Do NOT spend credits interval-certifying this particular third-order root.
Do NOT call the whole IC39 action dead from this one initial-data family.
The constructive remaining task is a regular moving-interface formulation
enforcing C=0 and W=-eta exp(S)ell as functions of (t,r), with bounded ell,
rather than fixing ell=ell_t=0 across the entire initial collar and successively
fitting more time derivatives. That restricted initial multiplier choice was
an ansatz, not a requirement of the target theory.

First derive the constraint-compatible boundary evolution system with nonzero
initial multiplier data and the actual remaining lapse/clock equations.
Use IC38's function-level compatibility test to decide whether its boundary
conditions are mutually consistent, then undertake a bounded evolution solve.
Do not claim this reformulation works until those equations are derived and
tested. Full Dirac closure, global joining, k=0 treatment and observational
gates still belong to the unchanged full target.
