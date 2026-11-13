# Repair checkpoint: construction succeeds, closure mechanism does not

An explicit nonmultiplicative action can preserve the requested FRW derivatives, remain convex in Q and concave in positive Pi, and suppress the clock energy. Thus a blanket mathematical impossibility claim for such H is false. The economical constructions tested here nevertheless fail to preserve the specified galaxy target: the first changes the polarization force coefficient, while a Q-dependent compensation repairs that coefficient at the cost of a large irreducible pressure.

The accepted original flat-gate instability and family result remain unchanged in the parent directory. This folder is a separate action-repair investigation, not a relabeling of the original theory.

## Explicit construction

For C,L,Pi_c>0, x=Q-1, u=Pi/Pi_c and S=exp(-u³), set

```text
F=Cx²,     t=x²/(L²Q),
B=CL²Q(1-exp(-t)),
H=F-B+B S-Q Gamma(u),
Gamma_uu=9CL²u⁴ exp(-u³),    Gamma(0)=Gamma_u(0)=0.
```

The exact identities prove H_QQ>0 for all Q>0 and finite Pi>=0, and H_PiPi<0 for Pi>0. At Pi=0, H=F and H_Pi=H_QPi=H_PiPi=0. The clock-energy fraction is exactly

```text
(QH_Q-H)/[C(Q²-1)] = 1-(1-S)exp[-(Q-1)²/(L²Q)],   Q>1.
```

Global convexity/concavity is not global health. On Q>=1 the relevant enthalpy is positive away from the degenerate vacuum: R=F-B is convex with its minimum at Q=1, B_Q>=0, and

```text
n_eff=Q(R_Q+S B_Q)+Pi-u B S'+Q(u Gamma_u-Gamma)>=0.
```

These signs remove the studied regular-center principal obstruction. Q<1, other inhomogeneous backgrounds, finite wavelengths and nonlinear evolution are not thereby certified. There is no uniform lower bound on the kinetic coefficient as the gate becomes fully suppressed at Q=1.

## Why the repair still fails the target

A Q-independent compensator first supplied the desired concavity, but its asymptotic linear Pi term changes P.A and the normal source together. With the unchanged W it gives `mu_eff(y)=1-beta²/(1+beta*y)` rather than the target law, with beta=1+Gamma'_infinity. The static lane independently checks this force failure.

The Q-dependent compensator above fixes that particular problem because Q Pi is an exact spatial boundary. It leaves an asymptotic QJ term, however, with zero lapse energy and positive pressure. Any compensator in this class preserving global concavity and the flat endpoint obeys the finite-u bound

```text
u Gamma_u-Gamma >= CL²[3 exp(-2/3)-(3u³+1)exp(-u³)]
```

for u>=(2/3)^(1/3). At u=4 the correction to the limiting factor1.5402513571 is only3.09536e-26. The full on-shell spatial stress, including W and optional original positive stiffness, satisfies

```text
p_mean=H-Pi H_Pi+gamma Pi²/2-W+(2/3)|P|W_|P|
      >=H-Pi H_Pi
      >=Q CL²[3 exp(-2/3)-(3u³+1)exp(-u³)].
```

The inequality uses the exact QX17 property `|P|W_|P|>=2W>=0`; it does not discard polarization-gradient stress off center. The original one-sided gamma may be retained: it strengthens the positive-branch concavity and pressure bound, while its Pi=0 nonsmoothness remains separately scoped.

On the supplied canonical annulus, recomputing the perspective candidate's **energy** suppression bound gives:

| Imported mu_K (/Mpc) | Minimum L² | Minimum outer K p_mean (/Mpc²) | Minimum outer pressure/Pi |
|---:|---:|---:|---:|
| 198.25 | 1.93339896106e-7 | .00585207184257 | 8000.867426 |
| 25120 | .00310412987568 | 1,508,484.77082 | 2.06237841745e12 |

The larger-mu pressure curvature scale is about.814 kpc, compared with the .732 Mpc target outer radius. These numbers are conditional on the supplied annulus and its effective clock-energy ceiling, with Q=1+abs(Phi) as the stated weak-potential mapping. They are not a new fit or a solution of the repaired action. They show that the same small-curvature target cannot be retained without an additional compensating stress or another action change. The original bounded-B derivative bound and this perspective-B energy bound are kept distinct.

The separate [rectangular clock-band test](BAND_BOUND.md) restricts concavity to `1<=Q<=qmax`, Pi>=0, rather than all Q. It still gives an outer pressure/Pi lower bound3268.35 for the mu_K=25120 target, but only.20357 for mu_K=198.25. That weaker bound does not exclude the lower-mu target or arbitrary correlated Q(Pi) domains. Its fresh bounded execution is `band_v2_run_001`; preceding accepted runs are unchanged.

## Verification and remaining route

`v2_run_001` is the accepted repair computation, freshly executed through the standard bounded runner and validated against its v2 manifest schema. The numerical output is `v2_run_001/payload/result.json`. It records17 exact identities, two wrong-term controls, a finite sign grid and a70-digit evaluation of the target-cost bound. Earlier `run_001`–`run_003` directories are preserved custom-metadata executions, not canonical runner records. The first diagnostic attempt rounded a positive H_QQ to zero at Q=1,u=4 in a subtractive float expression; the equivalent positive expression fixes that numerical cancellation. No physical conclusion came from the failed attempt.

Independent reviewers reconstructed the convex/concave construction, Q Pi boundary, exact energy fraction and full on-shell pressure variation. Their separate reports are [the health audit](../../health_audit/REPAIR_REVIEW.md) and [the matching audit](../../static_gate/matching/perspective_audit/REVIEW.md); the source snapshots, rather than review arrival order, identify the versions checked.

This closes the tested economical repair classes as solutions to the stated target. A new compensation sector or a derived restricted dynamical state domain remains a different route, requiring its own varied stress, conserved current and constrained spectrum. No such sector, preserved domain, ultraviolet cutoff, coefficient derivation or complete Zimmerman theory is supplied by these repairs.
