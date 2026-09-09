# IC11: convex clock pressure with its own activation domain

2026-09-08. Base HEAD `347950889570a839af41f6bef0c8bcba7531d02a`.
**Constructive bounded vacuum result; full theory OPEN.** Frozen IC10 and
the exponential primitive are unchanged. This is a new candidate action.

## Complete phase-action lift

Use the fields, boundary conventions and exact smooth eta of
[IC5_ACTION.md](IC5_ACTION.md), and the complete H10 of
[IC10_LOCAL_CLOCK.md](IC10_LOCAL_CLOCK.md). In particular
`X=-g^(mu nu) T_mu T_nu/2>0`, `w=(u-1)ln N`, `0<u<1`, and
`r=-Np/(3 m h0)`. Define, with the same dimensionless clock normalization,

    f(z) = (5 m h0²/64) (2z)^16,
    H11 = H10 - eta(r) exp(-4w) f(exp(2w) X),
    S11 = integral sqrt(-g) [2 P:Q-H11] + Sm[g,psi].

The exponent 16 and coefficient 5/64 are new design choices, not measured
parameters or a derived cosmological scale relation. No ordinary matter
action changes. All new tests use `m=h0=1`, `kappa=6`, and IC10's fixed
`a0²,Lambda,U`. The new term has no metric-momentum dependence on eta=1,
so the stationary trace and trace-free momentum equations are exactly IC10's.
Multiplying its Lagrangian contribution by the conformal volume factor
gives `f(tilde X)`, where `tilde X=exp(2w)X`.

Thus the **derived restriction of this global action**, on eta=1 only, is

    integral sqrt(-tilde g) [m exp(-1/6) tilde R/2 + P0(tilde X,w)+f(tilde X)]
    + Sm[exp(2w) tilde g,psi].

The full switch-dependent momentum equation elsewhere contains the extra
term `-eta_r r_p exp(-4w)f(exp(2w)X)` in H_p. It must be varied and solved;
the compact Einstein-clock restriction does not apply in that region.

At p=0, eta is identically zero on an open neighborhood. Hence the action
difference and **every first jet** with respect to the fields and phase
momenta vanish there. This preserves the static equations under the existing
IC5 boundary prescription, including their exponential constitutive equation.
It does not establish baryon-only physical AQUAL, lensing or PPN.

## Exact pressure derivatives and positivity conditions

Write `x=tilde X=exp(-2S)/2`. Since `f_w=0`, the vacuum equation `P0_w=0`
and its root `w(S)` are unchanged. The actual reduced pressure and energy
are changed. For the family `f=a(2x)^n/(2n)` in the numerical units, put
`g=f_x=a(2x)^(n-1)`. If `p0=P0_eff,x`, `q0=p0+2x P0_eff,xx`, then

    PX = p0+g,
    Qclock = q0+(2n-1)g,
    Qclock-PX = q0-p0+2(n-1)g,
    rho = rho0+(2n-1)x g/n,
    cs² = PX/Qclock.

For positive linear `f=a x`, `Qclock-PX=q0-p0`: it cannot repair a
superluminal point while keeping a positive kinetic coefficient. Convex
pressure can. For n>1 the exact pointwise clock inequalities are

    p0+g > 0,
    q0+(2n-1)g > 0,
    q0-p0+2(n-1)g >= 0.

They are necessary and sufficient for `PX>0`, `Qclock>0`, `0<cs²<=1`.
Add `rho>0` and the physical-expansion condition

    q0+3p0 w_S + [(2n-1)+3w_S]g > 0.

The auxiliary constraint must also remain invertible at fixed canonical
clock momentum. Direct derivatives of P=P0+f give

    Qbare=(P_SS+P_S)/(2x),
    A=P_ww-P_Sw²/(P_SS+P_S)=P_ww Qclock/Qbare.

Require `P_ww!=0`, `Qbare!=0`, `A!=0`; the auxiliary pair has rank two
there. For this term `f_S=-32f`, `f_SS=1024f`, `rho-rho0=31f`.
These identities are checked symbolically. Finite differences of the
root-eliminated pressure independently check the S derivatives.

## Recomputed expansion and exact admissibility predicate

Use the modified pressure, not the old Hubble solution:

    3 mstar Htilde² = rho,                 mstar=m exp(-1/6),
    dS/dtau = 3 Htilde cs²,
    Hphysical = exp(-w) Htilde (1+3cs² w_S),
    r = exp(S) exp(-2w-1/6) Htilde/h0.

The admissible vacuum plateau domain on the chosen root continuation is
**exactly** the set satisfying the stated chart and auxiliary conditions,
the clock and expansion inequalities above, and `3/4 <= r² <= 5/4`.
This definition does not silently retain IC10's activation domain.
Equivalently, in m=h0=1 units, write

    R0=r0², B=J9²(2n-1)/(6n mstar), r²=R0+B g.

Since B>0, activation imposes the additional exact bounds
`(3/4-R0)/B <= g <= (5/4-R0)/B`. They expose the energy cost of
convexification and are useful for other designs. A large kinetic correction
cannot be approved independently of these bounds.

For the selected n=16,a=5/2, numerical roots at 55 decimal digits locate
the component surrounding the `.03--.2` witness:

    lower r²=5/4: S=0.0223221351755311665397405,
    upper r²=5/4: S=0.230122302771866904651217.

These are located crossings, not a rigorous proof of the uniqueness of this
component or an interval-arithmetic sign certificate between the endpoints.
The tests check 101 equally spaced points on [.03,.2]. A separate 501-point
scan on [.0001,.5] contains 208 eta=1 points and no unhealthy eta=1 sample.

| S | PX | Qclock | cs² | rho | Hphysical | r |
|---|---:|---:|---:|---:|---:|---:|
| .03 | 3.087745 | 32.285226 | .095640 | 3.834484 | 1.117612 | 1.096697 |
| .05 | 2.625174 | 20.646843 | .127146 | 3.354336 | 1.023606 | 1.060772 |
| .10 | 2.065168 | 9.118309 | .226486 | 2.769060 | .866660 | 1.044953 |
| .20 | 1.554712 | 6.033178 | .257694 | 2.253969 | .813796 | 1.098455 |

The early continued-pressure controls `.0001,.001,.01` and the late control
`.24` are outside eta=1. In particular, the continued pressure is still
ghostlike at `.0001` and `.001`. They are **not solutions established for
the full transition action**. This construction repairs and extends the
healthy vacuum plateau, not the full early cosmology.

There is also useful analytic endpoint information: on the small-positive-S
root, `C_u=-2a0²u ln²(1-u²)`, and P_w=0 gives
`u^5 ~ S(4Lambda-6)/(8a0²)`, `w~-S/2`. Therefore
`rho0 -> 6-Lambda`, `J9 -> exp(-1/6)`, and

    r² -> exp(-1/6) [6-Lambda+155/64]/3
       = 1.2761753210046295514026378378035146 > 5/4.

Thus this endpoint is excluded from the plateau in a sufficiently small
punctured neighborhood. This asymptotic observation is not a global exclusion
of additional components. It explains why the initially tried a=2 choice
was rejected: it admitted a ghost sample at S=.0001.

Direct quadrature on `.03 <= S <= .1` produces barred e-folds
`.157409880808401112953544534`, physical e-folds
`.135193733447333586951382214940`, and tilde proper time
`.139518420359579405445524093504`. The conserved charge
`barA³ PX sqrt(2x)` agrees to the tested `1e-40` tolerance.

## Computation contract, provenance, and limits

Authoritative paths: [ic11_clock_pressure.py](ic11_clock_pressure.py) and
[test_ic11_clock_pressure.py](test_ic11_clock_pressure.py). Symbolic arithmetic
uses rational coefficients and exact logs/exponentials in SymPy; numerical
root solving, derivatives and quadrature use mpmath at 55 decimal digits.
Software: Python 3.9.6, mpmath 1.3.0, SymPy 1.14.0. No random sampling.
All commands run in this directory, with runs completing in seconds; no
hard CPU/memory cap is asserted. Existing unrelated dirty files are preserved.

The new tests were written first: six tests failed with the expected missing
module assertion; the later static-jet test failed with the expected missing
phase-delta assertion before implementation. Regeneration commands:

    python3 -m unittest test_ic11_clock_pressure.py test_ic10_local_clock.py
    python3 ic11_clock_pressure.py
    python3 ic11_clock_pressure.py --require-full-closure

The required exits are respectively 0, 0 and **2**: the last command refuses
to certify full closure. The root finder can fail outside the stated numerical
range; such failure is not proof of a nonexistent root. No scan is a theorem
over untested states. The report is compact and regenerated rather than
preserving duplicate raw output here; combined run-manifest ownership stays
with the coordinating task.

SHA-256 source pins for this run:

    ic11_clock_pressure.py
      4a6591ef3d09d283271055604947983773a938b9c7b77b2dbce88d93308f567a
    test_ic11_clock_pressure.py
      fb2100b980b87f1b386d7fd98c3390dbf028efeb01e67ed423acdc11615d23e2
    ic10_local_clock.py
      9f76d1355dae2a9bb7066bcdccd477b7364f5af08249bf4288352b2c6f4aef8d
    IC10_LOCAL_CLOCK.md
      7714650a4133836a16bf17da1643c86ad93114ae5d35bbee7419931f01268dcb
    ../FRIED_CHICKEN_SPEC.md
      be0400679673b0bb9463dd399ab8e05b8889659ad97736e1b9926276887361c2

The next liability is the full eta-transition evolution, including the new
eta momentum derivative, its constraint rank and principal operator. In
parallel, ordinary matter must be included in the auxiliary elimination:
although f does not move the **vacuum** root, matter generally does. No
matter-coupled causality, strong-coupling scale, global chart control, sourced
galactic matching, PPN or realistic cosmology follows from these tests.
The a0--Lambda proportionality remains input. Full theory remains OPEN.
