# No transverse-vector rescue of a smooth one-dimensional pure-decay profile

For the declared projected-clock action, no nonzero smooth periodic one-dimensional pure-decaying scalar profile can satisfy the second-order local clock equation by adding any smooth periodic divergence-free relative vector shift. This covers infinitely supported smooth Fourier profiles. It is not an all-three-dimensional-profile theorem, nor a result including additional frozen scalar/relative homogeneous seeds.

## Hypotheses and actual necessary equation

Use the inherited n=3 flat periodic torus and de Sitter branch with a,H,K>0, the actual pure decaying scalar nu=a^-1 f(x), and its constrained scalar shift 2Ha^-1 grad u, u=(-Delta)^(-1)f. Assume f real, zero mean, and sufficiently regular that u is periodic C4 (smooth f suffices). Add a periodic C1 divergence-free transverse relative shift V(t,x,y,z). The inherited second-order normalized-clock equation requires

V·grad w=(H/a)R, w=f'', R=(f f'−2f''u')'.

Its overall positive factors do not affect solvability. This is a necessary local action equation, not a prescribed matter switch. The EH vector constraint permits time-integrated relative spatial-vector data supporting such a shift, so it is useful to exclude even this broad necessary candidate class. No extra first-order frozen scalar/homogeneous relative data are assumed.

## Transverse average before any ODE inference

Average V over periodic y,z. Divergence freedom gives d_x average(Vx)=0, because the transverse divergence integrates to zero. Thus average(Vx)=C(t), regardless of V's transverse spectrum. Since w and R depend only on x, averaging the local equation yields R=c(t) w', where c=a C/H. This step does not falsely replace a general vector by an unconstrained longitudinal field.

At any fixed interior time, integrate once:

f f'−2 f''u'=c f''+d.

Its spatial mean fixes d=0. Indeed integral f f'=0, integral f''=0, and integral f''u'=−integral f'u''=integral f'f=0, using u''=−f. A time-dependent c is allowed; it is only a constant with respect to x.

Put v=u'+c/2. Substitution f=−u'' gives

u'' u'''+2u''''u'=−c u'''',

where the symbol in this line is u (the inverse-Poisson function); equivalently, without ambiguity,

2v v'''+v'v''=0.

The plus sign is essential. On each open connected component where v is nonzero,

(d/dx)[sqrt(|v|) v'']=0.

This follows by multiplying the last ODE by sqrt(|v|)/(2v), and is valid on either sign component.

## Periodic component proof

If v has a zero, every nonempty component of its nonzero set is an open interval on the circle with zero at both endpoints, including the case that they are the same point. Since v'' is bounded and continuous, sqrt(|v|)v'' tends to zero at either endpoint. Its constant on that component is therefore zero. Thus v''=0 inside the component; v is affine there. Its two zero boundary values force v=0 there, a contradiction. Consequently the nonzero set is empty in this case. This reasoning includes flat, accumulating and nonisolated zeros; no simple-crossing assumption is used.

If v has no zero, it has one sign on the connected circle. The invariant yields v''=c0/sqrt(|v|). Unless c0=0 this has a strict fixed sign, contradicting integral v''=0. Hence v''=0, and periodicity makes v constant. Both cases give constant v. Therefore u' is constant; periodicity gives u'=0, and f=−u''=0.

This proves the claimed obstruction at a single time, hence on any regular time interval. It neither requires c to be time independent nor invokes a finite Fourier cutoff.

## Relation to the weighted-sign result

The adjacent weighted_sign child proves that integral w²R has both signs. This proof bypasses that sign question: the full averaged local equation, not one weighted integral, rules out every nonzero smooth one-dimensional profile in the declared class. It does not establish a universal sign or classify general three-dimensional functions. Nor does it exclude rough/nonperiodic fields, additional relative flat seeds, arbitrary mixtures of time branches, modified actions, or cold matter in general.

The exact checks reconstruct the substitution and integrating factor on both sign branches, transverse-average divergence and the zero integration constant. Their finite symbolic results corroborate the identities; the component/periodicity argument above is the actual uniform proof. Controls use the erroneous minus-sign ODE or a varying longitudinal average. Parent inputs remain frozen.
