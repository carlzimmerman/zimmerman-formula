# Quantitative confinement time for canonical data

19 October 2026. Claim ZAR-Q4. All data below are strictly radial canonical rearrangements of F with the same initial full supports K_i and sufficiently small size. This yields a finite-time theorem with a radius independent of the perturbation amplitude. It does not supply confinement of one nonstationary solution for all time.

## Canonical energy gives a uniform stability size

Use the earlier local nonlinear coercivity constants d_*>0 and gamma>0 in the form

\[
\Delta H:=\mathcal H(f)-\mathcal H(F)\ge\gamma D_0(f)
\quad\hbox{when }f\preceq_L F,\ D_0(f)\le d_*.
\tag{12}
\]

Use also X(f-F)<=C_X(sqrt(Dtilde)+Dtilde). These are fixed equilibrium constants from [the proved nonlinear theorem](../nonlinear_radial_2026_10_19/NONLINEAR_COERCIVITY.md), not new computed tolerances. Canonical transport preserves exact equimeasurability and Delta Psi=0, so Dtilde=D_0 at every time. Assume initially

\[
D_0(f_0)<d_*/2,\qquad
0\le\Delta H<\gamma d_*/2.
\tag{13}
\]

A first time with D_0=d_* would contradict conservation of Delta H and (12). Therefore

\[
\sup_{t\ge0}D_0(f(t))\le\Delta H/\gamma,
\quad
\sup_{t\ge0}X(f(t)-F)\le\epsilon_H,
\]

\[
\epsilon_H=C_X\left(\sqrt{\Delta H/\gamma}
+\Delta H/\gamma\right).
\tag{14}
\]

If Delta H=0, (3) of the rigidity proof forces f_0=F. A nonstationary small canonical datum has positive Delta H. The formula supplies the size O(sqrt(Delta H)) in terms of the named analytic constants, without an explicit numerical evaluation of those constants.

## A common inner radius and a fixed negative initial gap

Set A_G=G(M_b+T+U), c=G^2/a_0. On the original K_i,

\[
v^2/2+L/(2r^2)-A_G/r\le E_i^F\le-\beta_0<0,
\]

because Phi_i^F>=-A_G/r for both species. The global characteristic theorem therefore has E_+=0 for every datum with these same initial supports and masses, and supplies the common inner radius

\[
\rho=\ell/(2A_G)>0.
\tag{15}
\]

The corresponding velocity constants are also uniform because the initial velocities lie in the fixed compact supports. Impose the explicit initial smallness D<=beta_0/(2C_gap) from [the gap estimate](CANONICAL_RIGIDITY_AND_SUPPORT.md). Then E_i(0)<=-beta_0/2.

## Work rate and the protection interval

The exact current formulas and the equilibrium's zero current give

\[
\sum_i\int|j_i(t,r)|dr\le\epsilon_H/2.
\]

With r>=rho and M_t<=T, their one-sided potential-work rates obey

\[
\sup_{r\ge\rho}[\partial_t\Phi_i(t,r)]_+
\le\Gamma\epsilon_H,
\quad
\Gamma=\frac G{2\rho^2}+\frac{cT}{\rho^4}.
\tag{16}
\]

This gamma-independent capital Gamma is a fixed work-rate coefficient, distinct from the coercivity constant gamma. The exact particle work identity implies

\[
E_i(t)\le-\beta_0/2+\Gamma\epsilon_Ht.
\]

Thus, if Delta H>0,

\[
\boxed{0\le t\le T_H:=\frac{\beta_0}{4\Gamma\epsilon_H}
\quad\Longrightarrow\quad
E_i(t)\le-\beta_0/4,\qquad
R_{\rm supp}(t)\le R_H:=4A_G/\beta_0.}
\tag{17}
\]

The radius R_H is independent of the small canonical perturbation. As Delta H tends to zero, T_H grows on the scale (Delta H)^(-1/2). This is a lower bound on the guaranteed protection interval, not an upper bound on the true confinement time and not a prediction of escape afterward.

For every prescribed finite T one can choose a sufficiently small canonical neighborhood satisfying (13), the initial gap bound and Gamma epsilon_H T<=beta_0/4. Every solution in it is confined to the same R_H on [0,T]. The neighborhood may shrink with T. These quantifiers cannot be exchanged to produce one nonstationary neighborhood valid for every T.

## The law and radial warmth

The all-time bound (14) retains the previously proved cumulative-mass and force-law estimates on the original law annulus, and integrated raw/centered radial pressure control. For any fixed radial resolution in that annulus the averaged centered dispersion has the positive all-time lower bound in checkpoint 06, provided epsilon_H is chosen sufficiently small. Smooth canonical positivity sets also retain pointwise positive radial dispersion on the original law annulus on every finite time interval for each solution. The exact density law is not asserted to stay equal under general nonstationary motion.

Equation (17) adds a protected hard enclosing radius on its time interval. It does not supply an all-time pointwise dispersion floor, a fixed original orbital support, or an infinite-time work bound. The remaining gap is the uniform-in-time estimate for the accumulated signed work or canonical energy-label displacement developed in [the resonant work analysis](RESONANT_WORK_PROGRESS.md).
