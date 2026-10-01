# One released support coefficient: exact target audit

This audit fixes its algebra before reading the FGF029 worker calculation.
The inherited finite binary64 matrix U has fifteen rows and fifteen pressure
coefficients, fixed map offset zero and zero endpoint at radius5. Its exact
rational interpretation is invertible. Let c be the new node5 hat response,
with support [4,6]. Old columns retain their former shapes, so the extended
operator is H=[U,c]. This is a finite response-model statement, not a theorem
about continuum deprojection or an observed pressure profile.

Write p=(x,s) and target t=Lx, where s is pressure at node5 and L is the old
gradient row at radius1. Since U is invertible, all noiseless solutions have
x=U^{-1}d-U^{-1}c s. If rU=L, then

    t=r d-h s,       h=r c.

Consequently v=(-U^{-1}c,1) spans the nullspace and Lv=-h (with extended last
target coefficient zero). If h is nonzero, the augmented target has rank16
while H has rank15: all fifteen annuli do not identify the target once this
single support assumption is relaxed. This is not established by rank counts
alone; the exact nonzero target response is essential.

Choose an explicit strictly decreasing positive synthetic baseline at all
sixteen free nodes, with fixed p6=0. Its successive gaps m_i are positive.
Let delta_i=v_i-v_{i+1}, using v_16=0 at the fixed endpoint. Set
epsilon=(1/2) min_{delta_i!=0} m_i/|delta_i|. Both p+/-epsilon v remain
strictly decreasing and positive, H(p+/-epsilon v)=Hp exactly, while their
target difference is -2 epsilon h. Positivity of every gap includes the last
free-node-to-zero gap. These are synthetic witnesses, not fits to measured bins.

One extra scalar row (a,b) gives a residual response
k=b-a U^{-1}c along v. If k!=0, that row fixes s and hence the target; if k=0,
it adds no information along this ambiguity. Directly measuring s is one
mathematical example (k=1), not a claimed available observation. Duplicate
rows have k=0. With an externally justified interval of width Delta s and
exact old bins, the algebraic target width is |h| Delta s before imposing
other constraints. This is not a confidence interval or covariance estimate.

Controls require exact old-column equality; p5=0 recovers the old finite
identification; a deliberately altered target fails its certificate; an
extra coordinate row for s restores full rank while an old-row duplicate
does not. Exact means rational arithmetic on saved binary64 response values.
The response audit separately checks numerical construction to stated tolerance;
neither establishes continuum convergence or authenticates all calibration.

No mass or acceleration is computed. A later physical inference must convert
electron to total pressure and supply density and calibrated response, then
use the appropriate MOND source law. Both a0 normalizations, constant-vacuum
and distinct H(z) histories, and Q/RAR/registered M remain separate. This
result does not repair or refute the dynamical or physical metric sector.
