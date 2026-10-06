# Independent general-dimensional quadrupole audit

**Primary verdict: proved conditional on the explicitly declared general-n QUMOND extension and force convention.** For every integer spatial dimension `n≥3`, spacetime dimension `d=n+1`, the ideal quadrupole continuum has a strictly positive finite coefficient `c_n K_n`. The derivation below reconstructs its Green projection, source normalization and Mellin moment rather than inferring the result from n=3. No relativistic vacuum dictionary is thereby generalized.

Observed HEAD: `30b858d2d7d4b1eff9916a06fcf2e3e8d70842c2`. Inspected immutable source hashes are listed at the end. This audit covers the durable REPORT, the raw derivation supplied by the author and the inspected script; runner checks are bounded corroboration and are not the proof.

## Physical convention and Newton normalization

Let `Ω_j=2pi^((j+1)/2)/Gamma((j+1)/2)` be the area of the unit j-sphere. Fix the measured Newtonian point-source force to have magnitude `mu/r^(n−1)` and define

`r_M=(mu/a0)^(1/(n−1))`, `p=1/(n−1)`, `t=(r_M/r)^(n−1)`.

Thus `r_M` is a force-defined length in every n, not `sqrt(GM/a0)` outside n=3. If a Newtonian Poisson dictionary is `Delta Phi_N=kappa_n rho`, Gauss's law gives `mu=kappa_n M_source/Ω_(n−1)`. This need not equal a tensor-gravity coupling without separately checking physical matter and any scalar force calibration. The continuum theorem below only uses the measured mu and a0.

Use actual Newton force `G/a0=−t rhat+e zhat`, physical phantom force `D=f(|G|/a0)G`, and `psi=−Phi_p`, so `Delta psi=div D` and acceleration is `grad psi`. The STF quadrupole convention is `psi_Q=A r²Y2`, `Y2=mu_angle²−1/n`, `Q_n=psi_zz−psi_xx=2A`. In the parent three-dimensional physical-potential convention `Phi_Q=−(Q2/2)r²Y2`, this gives `Q_n=Q2`. Changing to `Phi_p` while keeping the same Hessian definition would reverse the sign. This distinction resolves an apparent sign mismatch during the audit.

## Green projection reconstructed

Isotropic sphere moments give `<mu_angle²>=1/n`, `<mu_angle⁴>=3/[n(n+2)]`; hence

`N2=integral Y2²dΩ=Ω_(n−1) 2(n−1)/[n²(n+2)]`.

The l=2 radial Poisson operator has solutions `r²` and `r^(−n)` and Wronskian factor `n+2`. Its regular interior coefficient due to an exterior source S is

`A=−1/[(n+2)N2] integral_0^infinity r^(−1)dr integral S Y2 dΩ`.

This also follows directly by expanding the n-dimensional Green kernel; it is not an assumed four-dimensional normalization. For `S=div D`, integration by parts yields the radial/angular bracket

`n D_r Y2−D_tan dot grad_S Y2`.

Put `xi=−mu_angle`, so `y²=e²+t²+2et xi`. For the actual-force convention the bracket is `−a0 f(y) H_n`, where

`H_n=n t(xi²−1/n)+e xi[(n+2)xi²−3]`.

The Green minus sign and the bracket minus sign cancel. The radial Jacobian is `dr/r²=−t^(p−1)dt/[(n−1)r_M]`. Together with `dΩ=Ω_(n−2)(1−xi²)^((n−3)/2)d xi`, these factors give

`Q_n(e)=(a0/r_M)c_n integral f(y) W_n(y,e)dy`,

`c_n=n²Ω_(n−2)/[(n−1)²Ω_(n−1)]`,

`W_n=integral_|y−e|^(y+e) (y/e)t^(p−2)H_n(1−xi²)^((n−3)/2)dt`.

The projected Green and source-IBP boundary terms must vanish. For the parent's regular constitutive class, its high-force tail, finite moment and subtraction of the uniform external field are the relevant inputs. An arbitrary singular measurable kernel should not be used to claim this original point-source PDE construction without additional regularity. Once the displayed weight functional is the declared input, its moment identities hold in the weighted L1 class below.

Scaling gives `W_n(y,e)=y^p F_n(e/y)`. At n=3, `H_3` is minus the parent's raw bracket, and `W_3=−2w_e`: the factor two is the parent's `u²=t` Jacobian, not a free convention.

## Absolute moment and exact positive coefficient

The moment that leaves a y-weight is `integral e^(−p) W_n(y,e)de`. At y=1 insert `delta(1−sqrt(e²+t²+2et xi))` into the unswapped weight integral and put `t=e rho`. Integrating e gives

`K_n=integral_0^infinity rho^(p−1)d rho integral_-1^1 (1−xi²)^((n−3)/2)`

` *[n rho(xi²−1/n)+xi((n+2)xi²−3)]/(1+rho²+2rho xi) d xi`.

The required Fubini exchange is absolutely convergent. In the fixed-y triangle representation, the e-axis strip has width O(e), giving the integrable bound `e^(−p)`; the t-axis gives `t^(p−1)`. In the large diagonal strip, `1−xi²=O(R^(−2))`, and the full absolute measure is bounded by `O(R^(1−n))dR`. Compact portions are harmless. These bounds apply to every integer n≥3, since `0<p<1`, and establish the absolute Mellin kernel moment directly without presupposing endpoint cancellation formulas.

For `xi=cos theta`, the elementary rho integral is

`integral_0^infinity rho^(a−1)/(1+rho²+2rho cos theta)d rho`

`=pi sin((1−a)theta)/[sin(pi a)sin theta]`,

valid for `0<a<2`, `0<theta<pi`, with the removable a=1 limit understood. It follows by factoring the denominator into `(rho+exp(i theta))(rho+exp(−i theta))`, applying the Euler beta integral to the partial fractions initially for `0<a<1`, and continuing within the common ordinary strip `0<a<2`. Both required values a=p and a=p+1 lie in that strip.

Set `G(theta)=sin^(n−1)theta[(n+2)cos²theta−1]`. The angular numerator after rho integration is exactly

`G sin(p theta)+G' cos(p theta)/(n+1)`.

Indeed `G'=(n+1)sin^(n−2)theta cos theta[(n+2)cos²theta−3]`. Integrating the second term by parts, with G=0 at both endpoints, gives a factor `(n+1+p)/(n+1)`. Write

`J_m(p)=integral_0^pi sin^m theta sin(p theta)d theta`.

Since `G=(n+1)sin^(n−1)theta−(n+2)sin^(n+1)theta`, two integrations by parts yield

`J_m=m(m−1)J_(m−2)/(m²−p²)` for m≥2,

with `J_0=(1−cos(pi p))/p` and `J_1=sin(pi p)/(1−p²)`. Combining these exact relations gives

`K_n=pi(1−p²)J_(n−1)(p)/[(n+1−p)sin(pi p)]`.

Every factor is strictly positive: `0<p≤1/2` and `sin(p theta)>0` on the open angular interval. Recurrence, the two base integrals, Gamma recurrence/reflection and duplication give equivalently

`K_n=pi²(1−p²)Gamma(n)/[2^n(n+1−p)cos(pi p/2)`

` *Gamma((n+1+p)/2)Gamma((n+1−p)/2)]`.

Thus positivity holds for every integer n≥3 by analysis, not by the script's n=3,...,12 samples. The familiar sine-power Gamma integral need not be assumed as a new external theorem; the displayed recurrence and base cases already determine it at each required integer m.

## Full continuum conclusion and n=3 control

For `integral y|f(y)|dy<infinity`, absolute kernel integrability and homogeneity justify response-level Fubini and imply

`integral_0^infinity e^(−p)Q_n(e)de=(a0/r_M)c_n K_n integral_0^infinity y f(y)dy`.

At n=3, `p=1/2`, `J_2=16/15`, `K_3=8pi/35`, `c_3=9/8`. The physical coefficient is therefore `9pi/35`, exactly matching the independently derived parent sum rule. The n=3 weight sign and factor are both required; omitting either produces a wrong result despite positivity of K_n.

This theorem is a classical n-spatial-dimensional source/response statement. The Einstein trace, measured versus tensor G, relativistic vacuum action normalization and any dimension-dependent meaning of `C=Lambda/a0²` remain unproved separate dictionaries. It is not a proof that a vacuum coefficient equals this geometric prefactor, a 32pi selector, a physical all-e dataset, or full kernel injectivity in general n.

## Source and computation scope

The author's inspected script implements the correct STF norm, angular recurrence reduction, gamma expression, n=3 force convention and scale index. Its quadratures are finite, non-interval-certified corroboration only; this reviewer did not execute or modify author inputs. Primary identities used here were independently checked against NIST DLMF [5.5](https://dlmf.nist.gov/5.5) and [5.12](https://dlmf.nist.gov/5.12) during the adjacent Mellin audit. No astronomical data analysis is claimed.

- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/continuum_external_field/general_dimension/checks.py`: `e7c222b43d9da75d6f75a0dc1226541e9b0be4710396d7bd84a35314de63e0a0`.
- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/REPORT.md`: `cbc5a75fe84b619ff84f5031c583f9c8d328430b509393ea019be01b8b77b541`.
- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/checks.py`: `3d3e4422d5f066426133a5a2db52bdbb21020c4ebcdeeee68dc10e2e38f25470`.

- `sol61_push/puzzle_32pi/claude_p57_efe_2026_10_06/continuum_external_field/general_dimension/REPORT.md`: `6396c57536a117e2a6c223754d87e5602248356eedea4ecdd473ec1a3641c412`.

The durable report's endpoint estimates were also reconstructed: its large-q leading odd term cancels, and using the z-weighted second moment `1/n` gives exactly `b_n=(n−1)(1+p)B(1/2,(n−1)/2)/n`. Its independent rho/angle absolute-convergence argument and compact-annular-to-functional extension address the boundary and integrability distinction noted above. The n=2 exclusion is appropriate: this proof uses its separately declared n≥3 Green/source and p<1 framework. No dimension-selection implication is supplied.
