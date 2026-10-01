# FGF-024: the missing pressure functional

All algebra concerns the stored binary64 coefficients interpreted as exact
rationals. The physical approximation producing them remains conditional.
Fix the post-convolution offset to its baseline value zero. Let A be the
12x12 inner block of H and O its three outer-pressure columns. Ignore H's
offset column only because the offset is fixed, not because it is pressure.
Let p=(i,o), o=(p(2.5),p(3),p(4)), and split L=(l_i,l_o,0).

Prove A invertible by rational Gauss-Jordan elimination, with both inverse
products verified. Set K=A^-1 O and w=l_i A^-1. Then

    i=A^-1 d-K o,
    g=L p=w d+m o,       m=l_o-w O,
    N=(-K; I_3),         H_pressure N=0,   L_pressure N=m.

The numerical coefficients displayed in the report are approximations to
the exact saved row m. Every nuisance direction v changes the target by m v.
Thus m v=0 characterizes the irrelevant nuisance plane; m v!=0 characterizes
target-moving freedom. Each coordinate's relevance is decided by m_j!=0.
The missing information for this scalar target is one linear functional,
even though three pressure coordinates remain undetermined.

For new linear observation rows C=(C_i,C_o), subtract the old-data prediction
to obtain z-C_i A^-1 d=R o, R=C_o-C_i K. The target is identifiable from old
and new exact data iff m belongs to row(R), equivalently rank(R)=rank([R;m]),
equivalently L_pressure belongs to row([H_pressure;C]). If alpha R=m, then

    g=(w-alpha C_i A^-1)d+alpha z.

Necessity: if m is outside row(R), rational elimination gives a v in ker(R)
with m v!=0. Adding N v changes g without changing any old/new observations.
On the inherited strict monotone positive baseline, sufficiently small
positive and negative steps remain admissible. Thus non-identification is
also witnessed inside the pressure inequalities, rather than merely on an
unphysical linear extension. Sufficiency does not need positivity.

This criterion applies globally to the linear family, and locally about any
strict feasible profile. A particular boundary-only feasible set can make a
target unique through inequalities even if row-space membership fails; do not
claim the criterion is necessary for all such degenerate boundary datasets.

Synthetic positive control C=(0,m) has R=m, identifying the target while two
coefficient directions remain unmeasured. Synthetic negative control
C=(0,(m_1,-m_0,0)) annihilates v=m^T, but m v=sum m_j^2>0. Another control
duplicates an existing observation row and supplies no new information.
Three synthetic outer-coordinate rows identify all coefficients. No synthetic
row is asserted to be a realizable or available instrument measurement.

Candidate validation accepts exact rational coefficient strings for beam-
convolved annular-y rows on the inherited fifteen pressure basis functions.
Each row needs construction provenance: annulus edges, mask/weight rule,
beam/transfer source and convolution convention, geometry/distance, same
support p(5)=0, and fixed post-convolution offset. An offset coefficient is
declared separately; for a normalized annular mean it should be one before
subtracting the known offset. Source hashes must accompany any real response
construction. The validator checks algebra and metadata presence, not whether
those physical claims are true. Its output never authenticates an observation.

No new data fit, covariance, noise tolerance, continuum derivative bound,
gravity/mass calculation or historical novelty is asserted. Future hydrostatic
tests must retain both a0 normalizations (9.3619e-11,1.1279e-10 m/s^2), separate
constant-vacuum and a0 E(z) histories and separate Q, RAR and registered M,
with P_total'=-rho F(B;a). A metric/photon coupling is still not derived.

Deterministic exact rational calculation, one operator, no random sweep.
Bounded runner: 120 s wall, 110 s CPU, cooperative one-thread libraries,
1 MiB logs, no memory cap. Stop on failed exact identity or control.
