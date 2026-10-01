# Independent FGF007 energy remainder and limit analysis

Auditor /root/metric_intake. Frozen from task007 and original stage03 dynamics before reading any new author or root proof or receiving a formula preview. Keep a>0 constant within each diagnostic comparison, K=2 positive, and the Q and RAR inverse laws separate. Let x=g0/a, h=delta-gradient/a, y=B/a and w(x)=W(ax;a)/a². The potential-gradient sign is opposite physical acceleration as in the pinned action; the energy expansion uses the gradient vector itself.

Let f_Q(y)=sqrt(y²+y), f_R(y)=y/[1-exp(-sqrt(y))]. Use the source coordinate t=sqrt(y). Then x=f(t²), and integration by parts gives an independent source-parameter energy representation

 w(x)=x t²-integral_0^t 2s f(s²) ds,
 w'(x)=y=t², w''(x)=2t/[d f(t²)/dt].

For Q, y=2x²/[sqrt(1+4x²)+1] is cancellation-safe and w''=2x/sqrt(1+4x²). For RAR, f(t²)=t²/[-expm1(-t)], with f(0)=0 continuously. This is strictly increasing, with t<=x since 1-exp(-t)<=t, giving a root bracket [0,x]. Its derivative is [2t(1-exp(-t))-t²exp(-t)]/[1-exp(-t)]²>0. Source quadrature avoids integrating the inverse-gradient law used in the original definition. High-precision checks at two working precisions will compare results and inversion residuals; they are finite numerical checks, not interval certification.

## Increment and Hessian

Take the background vector x e1 and increment h. After subtracting the correct linear work, the dimensionless exact increment is

 D(x,h)=w(|x e1+h|)-w(x)-y(x) h_parallel.

For positive background x, the Hessian approximation is

 Q2(x,h)=[w''(x) h_parallel²+(y(x)/x)|h_transverse|²]/2.

All parallel signs must enter the linear subtraction. For ratio r=|h|/x use h=+rx e1, h=-rx e1, or a perpendicular vector of magnitude rx. The anti-parallel r=1 case has final gradient exactly zero and must not call a nonzero-root solver there. Report D, Q2, signed remainder D-Q2 and (D-Q2)/Q2. There are36 cases PER LAW,72 total for2 laws x3 backgrounds x4 ratios x3 orientations; two precisions test the same cases, not additional physics samples.

For each fixed x>0, smooth radial Taylor expansion gives parallel relative remainder

 (D-Q2)/Q2 = +/- [x w'''(x)/(3w''(x))] r+O(r²),

and transverse relative remainder

 (D-Q2)/Q2 = [(x w''(x)/w'(x)-1)/4] r²+O(r^4).

The transverse absence of an odd term follows rotational symmetry and sqrt(x²+|h|²), not a general cancellation for arbitrary orientations. Thus the relevant relative-amplitude parameter is r, not absolute amplitude alone.

## Deep and zero-background controls

Both laws have y(x)~x² and w(x)~x³/3. Q has y=x²+O(x^4); RAR has y=x²-x³+O(x^4). For fixed r in[0,1] and x->0,

 D_parallel_plus/Q2 -> 1+r/3,
 D_parallel_minus/Q2 -> 1-r/3,
 D_transverse/Q2 -> 2[(1+r²)^(3/2)-1]/(3r²).

The last ratio is 1+r²/4+O(r^4). These give exact deep-leading remainder controls and demonstrate that a fixed nonzero ratio does not become a small relative Taylor error merely because the absolute gradients tend to zero.

At exactly x=0 the Hessian spatial stiffness is zero, while D(0,h)=w(|h|)~|h|³/3. Thus leading nonzero energy is cubic, not a quadratic wave-energy term. With K=2 the separately assumed time kinetic coefficient stays positive; disappearance of spatial quadratic stiffness is not a ghost claim.

## Raw versus normalized orders of limits

For the RAW increment and raw remainder, both iterated limits x->0 and |h|->0 give zero. There is no noncommuting raw-energy limit to claim. The relative expansion is nonuniform: at fixed x>0, |h|->0 gives D/Q2->1; taking x->0 afterwards retains1. For fixed |h|>0, x->0 instead gives D->w(|h|)>0 and Q2->0+, hence D/Q2->+infinity; the subsequent |h|->0 does not convert that normalized iterated limit into1. The ratio is undefined at the exact zero-background point; these are one-sided limiting statements. Equivalently, along h=r x, the raw energy vanishes like x³ while the normalized ratio tends the nontrivial functions of r above.

The warning is a nonuniform relative approximation/normalization statement, not raw-energy noncommutation, nonlinear ill-posedness or an empirical failure. No finite table proves global PDE stability or instability.

## Planned finite verification

Use one bounded source-parameter implementation,72 cases at x=.1,.01,.001 and r=.001,.03,.3,1 for Q/RAR and three directions, at80 and110 decimal working precision. Preserve code/contract/run manifest. Root inversion uses a monotone bounded bracket; source integration uses high-precision quadrature. Declare a relative precision-agreement tolerance1e-55 for D,Q2,remainder ratio and a root residual tolerance1e-70 at the80-digit pass (tighter at110 as appropriate). Check positive D and Q2, correct anti-parallel linear sign, exact final zero endpoint, Q analytic primitive agreement and zero-background cubic scaling on the specified amplitude values. Quantify finite errors rather than assert a universal numeric threshold. A failed accuracy gate is an implementation/numerical issue until investigated; preserve it.

Dimensionless energies restore with a², field energy density with a²/(4piG); gradients restore with a. Hessian eigenvalues are dimensionless and c_mode²/c² equals the respective eigenvalue/K on the fixed nonzero uniform background. Both a0=9.3619e-11 and1.1279e-10 remain separate physical hypotheses; constant vacuum and prescribed H histories are distinct. This calculation does not supply an M action, filtered-MONO metric/photon dynamics, source/mass discrepancy, observation or closure.
