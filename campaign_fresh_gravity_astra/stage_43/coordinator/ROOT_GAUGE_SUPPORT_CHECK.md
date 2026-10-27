# Coordinator check: exterior comparison and two-sided potential matching

A narrow analytic check within FGF056, not independent discovery or a new task.
Root read the pinned FGF053 derivation and corrected FGF055 material. Before
this note, the FGF056 author reported its intended wider-cone remedy: the old
cone's terminal radius3epsilon need not contain the whole fast-field support.
This note does not assume that remedy has been proved or accepted; it checks
the comparison and potential-gauge obligations separately. No new author or
reviewer raw proof has been read. Zero mathematical executable computations.

Sources: FGF053 DERIVATION SHA256
ca6ee84e426a63fc4a6ff3ffedfe4073905338036c2a0e4130d51689baf5ad28;
FGF055 DERIVATION SHA256
289b493bbfba4613cf95f939e343bcdd00f0caf55037d107467c15e525e07b5f,
read jointly with its section6 clarification SHA256
701fd7002edd211b72bf4e9b5892dfc0faef9b26c1fb658ee7edcbd4516350ab.

## Known-background comparison uses unknown gradients

Write the complete compatible diagonal state as U, with
U_i,t+lambda_i(U)U_i,x=F_i(U), and stationary background H. Then delta=U-H
obeys exactly, along H's characteristic family,

 D_lambda_i(H) delta_i = F_i(U)-F_i(H)
                         -(lambda_i(U)-lambda_i(H)) U_i,x.

This identity differs deliberately from the parent field-amplitude identity
along actual solution characteristics, where the background derivative occurs.
On a compact existing classical prefix, the coefficient bounds AND the actual
U_x bound are finite. They give an integral inequality for all components of
delta on any region backward-contained for the H characteristics and supplied
with zero initial/lateral data. Iterating yields zero there. The constant may
blow up as the unknown endpoint approaches: equality still holds on every
strict prefix. It does not give a uniform derivative estimate or an existence
time. All density/scale sources must be included in F.

For fixed S_H greater than every H-family speed, exterior wedges beyond
|x-x*|=epsilon+S_H t are such comparison regions if their outer boundaries
are supplied by exact H overlaps or adequate larger known domains. One must
state those outer data, not infer them from initial compact support alone
on a finite interval. Full germ construction must prove its initial/restart
segments have the required outer overlaps and an inactive time/space buffer.
No upper bound on actual interior speeds is smuggled into this comparison.

## Potential constants are an independent gluing obligation

Assume a compatible classical branch on [A_o,D_o], with exact H on open
outer collars, so p=0,w=0,g=g0,k=k0 there. Initial g and k equal background.
The exact compatibility equations imply

 d/dt integral_(A_o)^(D_o)(g-g0) dx = p(D_o)-p(A_o)=0,
 d/dt integral_(A_o)^(D_o)(k-k0) dx = w(D_o)-w(A_o)=0.

Both integrals therefore stay zero. More strongly, reconstructing
phi(t,x)=phi0(x)+integral_0^t p(s,x) ds gives phi=phi0 on BOTH fixed outer
collars, provided they remain stationary for every earlier time. Thus a
single spatial antiderivative matching the left collar also matches the
right one; no second free gauge constant may be chosen. Likewise chi=chi0
on both collars follows from chi_t=w and initial equality. These conclusions
pass to actual C1 endpoint traces if those traces are proved, not assumed.
The fixed outer interval must contain the whole affected support at every
prefix. This statement says nothing about +/-2epsilon, where fields and
fluid fluxes need not vanish.

At restart, choosing positive compatible extensions outside the fixed patch
and matching the left gauge suffices only after the zero-integral/right-collar
check. Matching g alone would be insufficient in general. The source-pinned
FGF053 method included this gate; FGF056 must reprove it on its NEW outer
collars, not reuse its old small-core stationary endpoints.

## Limits

No germ has been constructed by this note. Existence, enlarged-cone amplitude
control, higher seminorm estimates, genuine endpoint traces, restart and
extension independence remain the parent's obligations. The support comparison
is conditional on existing regular solutions and the explicitly supplied
outer overlaps. It is not a physical propagation-speed theorem after breakdown.
Both scale normalizations, separate autonomous histories and Q/MOND source
remain as registered; no RAR/M/filteredMONO translation, evolving reference,
metric/photon/two-DOF, empirical or novelty conclusion follows.
