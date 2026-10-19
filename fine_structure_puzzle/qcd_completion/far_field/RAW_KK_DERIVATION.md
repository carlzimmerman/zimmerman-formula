# Independent raw derivation: full charged circle tower

Saved 2026-10-19 UTC after the static raw derivation and project-input read,
before reading external derivative-action or beta-function source formulas.

For q=+1 the frequencies are `a_k=2pi k/L+h`, `m_k=|a_k|`.
The q=-1 tower maps onto this tower by `k -> -k`; consequently the same
charged-pair vector/ghost factor as in the static calculation applies once
for every integer k. In a chamber `0<x=Lh/(2pi)<1`, the gradient of m_k
has magnitude |grad h|. Thus the contribution of each k is

`Gamma_k,2=-11/(24pi) integral d^3x (E^2+B^2)/m_k`.

With symmetric cutoff -N<=k<=N the mass sum is exactly

`S_N(h)=L/(2pi) [psi(N+1+x)+psi(N+1-x)-psi(x)-psi(1-x)]`.

Subtracting `L H_N/pi` defines a harmonic subtraction, giving

`S_H(h)=L/(2pi) F(x)`,
`F(x)=-psi(x)-psi(1-x)-2 gamma_E`
`=1/x+sum_(k>=1) [1/(k+x)+1/(k-x)-2/k]`.

In particular `F(1/2)=4 log 2`, and
`F(x)=1/x+2 sum_(j>=1) zeta(2j+1) x^(2j)` for |x|<1.

The harmonic-subtracted loop density is
`c_H(h)(E^2+B^2)`, `c_H(h)=-11 L F(x)/(48pi^2)`.
This sign and the static limit follow directly from the frozen static
calculation, independently of a literature convention for logweight.

With microscopic classical density `L(E^2+B^2)/(2g_b^2)`, define

`1/g_H^2(mu)=1/g_b^2-11/(12pi^2)[H_N-log(mu L/(2pi))]`.

Then the common local classical-plus-loop coefficient is

`C(h;mu)=L/(2g_H^2(mu))-11L/(24pi^2)log(mu L/(2pi))`
`          -11L/(48pi^2)F(x)`.

Here `d(1/g_H^2)/d log mu=11/(12pi^2)` and
`beta(g_H)=-11 g_H^3/(24pi^2)+O(g_H^5)`.
Finite matching from g_H to any other specified scheme is still required.
At mu=2pi/L the explicit scale logarithm vanishes.

## Zero-derivative tower

Dimensional regularization of a fixed charged-pair frequency gives
`V3,k=-m_k^3/(3pi)`. Analytic continuation of the full periodic sum uses
`zeta(-3,x)=-B4(x)/4`, hence

`V3(h)-V3(0)=4pi^2/(3L^3) x^2(1-x)^2`
`=h^2/(3L)-h^3/(3pi)+Lh^4/(12pi^2)`.

This is the pure gauge/ghost potential on a fixed background. A deformation
that stabilizes center holonomy adds its own potential and determinant.

## Universal 1/R extraction within this local truncation

For smooth c(h), `4pi(1+n_mag^2) integral_(r_c)^R dr c(v-1/r)/r^2`
has 1/R coefficient `-4pi(1+n_mag^2)c(v)`. Higher Taylor coefficients of c
first contribute 1/R^2. Thus the harmonic-subtracted two-derivative loop has

`[Gamma_1,2]_(1/R)=+11L/(12pi)(1+n_mag^2)F(Lv/(2pi))`.

The quartic term in V3 gives
`[Gamma_1,0]_(1/R)=-L/(3pi)`.
This statement keeps the full periodic potential, with its constant vacuum
reference removed; it extracts the 1/R coefficient after separately keeping
the R^2,R,log R pieces. Subtracting additional local potential terms would
change the problem and must be declared.

Consequently the local one-loop bulk coefficient of logweight is

`[-Gamma_1]_(1/R)= L/(3pi)-11L/(12pi)(1+n_mag^2)F(Lv/(2pi))`,

at the harmonic scale `mu=2pi/L`. The corresponding combined
classical-plus-one-loop logweight coefficient is

`2pi L(1+n_mag^2)/g_H^2(2pi/L)`
` +L/(3pi)-11L/(12pi)(1+n_mag^2)F(Lv/(2pi))`.

For center holonomy and unit magnetic tail, n_mag=1 and v=pi/L, this is
`4pi L/g_H^2(2pi/L) + L/(3pi)-22L log(2)/(3pi)`.

No physical vacuum-stress or full determinant claim follows. The background
is off-shell, the deformed large-R saddle can screen E, and the core,
boundary/domain determinant, and nonlocal pieces are not evaluated here.
