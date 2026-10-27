# Continuum comparison: contact pressure changes the saturation exponent

19 October 2026. This is an analytic scaling comparison within the matched
NR daughter functional, with its original repulsive contact. It is not a
computed nonlinear shared-state branch or a relativistic high-field limit.
The constants below have direct quadrature checks in `run_001`.

Take fixed scalar mass M, `K=lambda_rep/(4m^4)>0`,
`tau=hbar^2/(2m^2)`, and a positive Plummer baryon potential

\[
 U_E(r)=-E h(r),\qquad h(r)=\frac{L^2}{\sqrt{r^2+L^2}}.
\]

It has baryon mass `M_b=E L^2/G` and near its center
`h=L-r^2/(2L)+O(r^4/L^3)`. The complete daughter energy in this declared
host is

\[
 {cal E}_E[\rho]=\tau\int|\nabla\sqrt\rho|^2
       +K\int\rho^2-\frac G2 D(\rho,\rho)-E\int h\rho,
 \qquad \int\rho=M .                                      \tag{1}
\]

The source `D_E=∫h rho` is a scalar compression observable bounded above
by ML. It is not the total odd mass dipole, and the baryon profile is an
input rather than the earlier live baryon EOS.

For a localized strong-compression TF comparison, retain contact and the
quadratic trap after subtracting `-E ML`. The unique local minimizer of
that reduced strictly convex fixed-mass problem is

\[
 \rho_{\rm TF}(r)=\frac{E}{4KL}(R^2-r^2)_+,\qquad
 R^5=\frac{15KML}{2\pi E}.                                \tag{2}
\]

Its mean square radius is `3R^2/7`. Consequently the leading source
deficit and excess energy are

\[
 ML-D_E\simeq\frac{3MR^2}{14L}\propto E^{-2/5},\qquad
 {cal E}_E+EML\simeq\frac57 M\lambda\propto E^{3/5},
 \quad\lambda=\frac{ER^2}{2L}.                            \tag{3}
\]

These are TF local asymptotic predictions, not a proved numerical error
bound for (1). At this scale, self-gravity and the next trap term are of
order `E^(1/5)`, and a suitably smoothed TF recovery profile has Fisher
cost at most `E^(2/5) log E`, subleading to `E^(3/5)`. The sharp TF profile
itself has logarithmically divergent Fisher energy and is not an admissible
finite-tau trial state without smoothing. A full convergence proof and
source-derivative error estimate have not been supplied here. The scale
comparison applies only while the compressed state stays within the
dilute NR EFT; a formal `E -> infinity` eventually leaves that regime.

The analogous local polytropic balance `C∫rho^gamma` with gamma>1 gives
`R∝E^(-1/(3gamma-1))` and deficit `E^(-2/(3gamma-1))`. The isothermal
entropy `T∫n log n` is a separate limit with width `E^(-1)`; the ideal
quantum oscillator has width `E^(-1/2)`. Thus finite inventory alone does
not select the rational deficit. The pressure, quantum regime and heat
protocol matter. No Poisson matching or universal G coefficient follows
from this comparison.
