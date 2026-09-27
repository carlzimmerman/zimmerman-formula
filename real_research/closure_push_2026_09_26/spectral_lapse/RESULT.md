# Nonlinear inhomogeneous data with a positive lapse

This is an explicit new cosmological sector obtained from the IC28 bridge by
flattening its active potential and changing its active lapse-gradient
coefficient. It is not a pass for the original coefficient functions or a
completed splice to filtered MOND.

## The actual nonlinear constraint

After eliminating the algebraic z auxiliary, the proposed sector has

\[
H=\int d^3x\sqrt{\bar h}\,N[\mathcal A-b|D\log N|^2],
\quad N=e^S>0,\quad b>0,
\]

with A independent of N at fixed canonical data. This requires the explicit
gradient counterterm +(B_old-b e^S)|DS|^2 in the Hamiltonian, in addition to
the flattened active potential. It is not supplied by the old IC20 action.
Writing N=y^2 gives

\[
H=\int[\mathcal A y^2-4b|Dy|^2],\qquad
\frac{\delta H}{\delta y}=2(\mathcal A y+4b\Delta y).
\]

The lapse constraint is therefore
\(\mathcal L y=0\), where \(\mathcal L=-4b\Delta-\mathcal A\).
The S-constraint is C_S=(y/2)delta H/delta y=y(Ay+4bDelta y).
On periodic or suitable decaying boundaries, integral(C_S)=H. This is the
weighted S-constraint, not the unweighted integral of delta H/delta y.
The homogeneous mode imposes a global constraint; it is not deleted
by dividing by a nonzero wavenumber. The lapse's overall normalization remains
undetermined by this equation. Whether the complete Dirac chain interprets it
as a first-class global time symmetry must still be derived.

Here N denotes the reduced lapse exp(S). The original physical clock lapse is
exp(S+wc) on the pin; that constant positive factor changes neither the lapse
positivity nor the spectral constraint. Densities and momenta below use the
barred canonical Hamiltonian normalization, not measured cosmological units.

## An exact positive-density family

On a flat connected torus of side 2pi, choose fixed ell,b,Lambda_bar>0,
constant negative trace momentum q, zero traceless momentum, and ordinary
matter initially at rest. In these canonical variables

\[
\mathcal A=-\ell q^2+\bar\Lambda+\rho(x).
\]

For any real epsilon, take

\[
y=e^{\epsilon\cos x_1},\qquad
\rho(x)=\rho_0+4b\epsilon\cos x_1-4b\epsilon^2\sin^2x_1,
\qquad q=-\sqrt{(\bar\Lambda+\rho_0)/\ell}.
\]

If rho0 > 4b(|epsilon|+epsilon^2), the density is strictly positive everywhere.
Direct substitution solves the **nonlinear** lapse equation exactly, with
N=e^(2epsilon cos x1)>0. The momentum constraint is also satisfied: on the flat
slice pi^{ij}=q sqrt(h) h^{ij}/3 has zero divergence and matter momentum is zero.
The negative q gives expansion in the displayed kinetic convention,
K_bar=-3ell q>0. The action coefficients are fixed; q and rho are initial data.

The free overall lapse scale must also respect the original clock chart if
this sector is embedded there. Replace y by exp(S_bar/2)y and choose
S_bar-2|epsilon|>-2wc for wc<0; then S=S_bar+2epsilon cos(x1) stays in
0<u=(S+2wc)/(S+wc)<1. This constant scaling changes neither A, rho, the kernel
shape nor the gap below. Numerical eigenvectors are normalized to compare
shapes; that normalization is not a claim that the unshifted S=0 chart is
admissible. Activation of the full pin and all extra constraints of a proposed
embedding still have to be checked separately.

For a positive solution y, integration by parts gives, for any smooth f,

\[
\langle yf,\mathcal L(yf)\rangle=4b\int y^2|Df|^2\geq0.
\]

Thus the lapse operator has a one-dimensional kernel spanned by y. On the
subspace orthogonal to y, a weighted-mean Poincare estimate gives

\[
\lambda_{\rm gap}\geq4b\frac{(\min y)^2}{(\max y)^2}
=4b e^{-4|\epsilon|}>0.
\]

To see the estimate, put v=yf and use integral(y^2 f)=0. The weighted mean
minimizes integral[y^2(f-c)^2], so comparison with the unweighted mean, the
flat-torus Fourier Poincare inequality and the bounds on y give
integral(y^2 f^2) <= (max y/min y)^2 integral(y^2 |Df|^2).
This proves a controlled inverse on the normalized complement for these data.
It is an elliptic constraint statement, not a kinetic-energy or ghost theorem.

## Fixed-action source control and limits

For a separately prescribed positive density, the numerical control constructs
the lowest eigenpair of L0=-4bDelta-(Lambda_bar+rho). Its lowest eigenvalue is
negative. Choosing q=-sqrt(-lambda0/ell) makes L=L0-lambda0 have zero ground
eigenvalue. This adjusts one initial trace datum; it does not refit Lambda_bar,
b or ell to the source. This finite-grid control is not a general continuum
existence certificate.

The exact family is independently differentiated symbolically. Periodic
finite differences at 64,128,256,512 points converge to its positive root and
zero ground eigenvalue. A separate prescribed-source check tests the global
trace adjustment. The compiler evidence for `PushSpectral20260926.lean`
certifies five algebraic bridges; the continuum integration, spectral and
constraint-preservation arguments are not fully formalized in Lean.

Still open: preservation of all constraints, the full scalar/clock degree
count, nonlinear evolution, a controlled transition to the operative nu_mono
static sector, physical PPN, and empirical cosmology. There is no noncompact
leaf spectral-gap claim and no derived dark-energy magnitude.

## Further audited step: conditional global preservation

The subsequent [spectral reduction audit](../lapse_kinetic/SPECTRAL_REDUCTION_AUDIT.md)
goes beyond constructing one slice. Normalize the positive ground-state shape
by integral(y^2 dV)=1 and keep its independent scale N=c(t)y^2. If the
eigenpair depends smoothly on all canonical data, its projected shape
constraints and primary momenta form a regular second-class block, and no
other lapse-dependent term has been omitted, their reduction leaves the
canonical bracket on the remaining data and H_red=-c lambda0. Therefore
lambda0_dot={lambda0,-c lambda0}=0. Spatial diffeomorphism constraints commute
with this intrinsic eigenvalue when all coefficients transform covariantly.

The metric-volume term cannot be dropped: delta(lambda0)=delta(Q)|y
-lambda0 delta(norm)|y. The normalized total pullback is -lambda0, while the
fixed-shape Hamiltonian variation agrees with -delta(lambda0) on shell. An
exact two-mode model with a changing positive mass matrix checks this
distinction, the second-class bracket block and global preservation in 37
identities. This does not prove continuum functional regularity, compatibility
of omitted embedding constraints, nonlinear existence, or the full field count.
