# Thermal and classical-field calibration of the channel response

Date: 2026-09-20. Source revision: `928c61c79b4a74bd47ecf515be19da2342cde093`.
Scope: L230, L234, L237, L238, PD01, PD03, and `kappa_closure/README.md`.
This is a bounded route investigation and self-review, not a universal no-go theorem.
No dark-matter particle is introduced. All proposed response models below are
conditional statistical models, not an identified physical gravitational mechanism.

**Claim and verdict:** with independently fixed
\(s=c\sqrt{G\rho_\Lambda}>0\), establish \(p(0)=0\),
\(p'(0^+)=1\) for each of two independent OR channels, and hence
\(a_0/s=1/2\). **Incomplete, with the smallest missing implication:** the
thermal or classical-field calculation must fix the acceleration-to-response
calibration. The examined sources do not supply that identity.

## Exact dependency

Let \(y=g/s\), and suppose the gravitational constitutive response is
\(\mu(y)=1-[1-p(y)]^2\). If \(p(0)=0\) and
\(p(y)=\lambda y+o(y)\), then

\[
\mu(y)=2\lambda y+o(y),\qquad
g_N=\mu(g/s)g\sim\frac{2\lambda}{s}g^2,
\qquad \kappa=\frac{a_0}{s}=\frac1{2\lambda}.
\]

This uses the usual spherical constitutive matching to
\(g^2\sim a_0g_N\). Both the OR rule and its identification with gravity
are additional physical premises. Even granting them and the channel count,
unit slope remains necessary.

PD01 lines 24 and 91 explicitly assume unit slope as an “s-units
normalisation.” Fixing the unit of the independent variable does not fix the
derivative of a response function. L237 starts from a geometric distribution
with mean occupancy already called \(Y\), then identifies it with \(g/s\).
Its distribution identity is correct; the identification is the missing step.

## A constructive classical route, and the coefficient it leaves

A particle-free classical realization of the rational response is available.
Take two real Gaussian field quadratures with quadratic energy
\(E=K(Q_1^2+Q_2^2)/2\), at a temperature \(T>0\). Their radial energy
distribution is

\[
dP(E)=\frac{e^{-E/(k_BT)}}{k_BT}\,dE,\qquad E\geq0.
\]

Assume a channel's averaged response is
\(p(y)=\langle1-e^{-\eta y E/E_*}\rangle\), with
\(\eta,E_*>0\). Direct integration gives

\[
p(y)=\frac{\lambda y}{1+\lambda y},\qquad
\lambda=\frac{\eta k_BT}{E_*}.
\]

Thus the exact shape needs neither a particle count nor a species mass.
However, the response functional, its coupling \(\eta\), and its energy
scale \(E_*\) are new premises. Equipartition determines the energy
distribution; it does not establish \(E_*=\eta k_BT\). Setting that equality
is exactly the missing unit calibration in this realization.

A second constructive realization exposes the same freedom as infrared
spectral weight. Let \(\nu\geq0\) be a dimensionless activation gap and
let \(f\) be a normalized, nonnegative, bounded density continuous at zero.
Define the thermal activation response

\[
p(y)=\int_0^\infty f(\nu)e^{-\nu/y}\,d\nu,\qquad y>0.
\]

After \(\nu=yt\), dominated convergence gives

\[
\lim_{y\downarrow0}\frac{p(y)}y
=\int_0^\infty f(0)e^{-t}\,dt=f(0).
\]

The normalized family \(f_\lambda(\nu)=\lambda e^{-\lambda\nu}\)
therefore gives exactly

\[
p_\lambda(y)=\frac{\lambda y}{1+\lambda y},\qquad
p_\lambda'(0^+)=\lambda,\qquad p_\lambda(\infty)=1.
\]

Here \(\lambda>0\) is unrestricted even though every density is normalized.
This construction shows why the fixed-frequency obstruction in L238 cannot
be promoted to an obstruction for all gapless statistical field models.
It is a genuine possible mathematical mechanism for the needed power law.
It does not fix the physical gap measure or its coupling to \(g/s\).
The concrete next obligation is to derive the physical spectral measure and
show \(f(0)=1\) in the already fixed units, without tuning a coupling.

## Horizon calibration checked against primary sources

Write \(A=cH_\Lambda\) and \(q=\sqrt{8\pi/3}\). With
\(\rho_\Lambda\) a mass density, the de Sitter Friedmann relation gives
\(A=qs\). Deser and Levin's constant-acceleration detector temperature is,
in SI units,

\[
k_BT(g)=\frac{\hbar}{2\pi c}\sqrt{g^2+A^2}.
\]

Source checked: S. Deser and O. Levin, *Accelerated Detectors and Temperature
in (Anti) de Sitter Spaces*, arXiv:gr-qc/9706018v1, 6 June 1997,
[Eq. (8), page 3](https://arxiv.org/pdf/gr-qc/9706018v1).
This is a detector result in de Sitter, not a derivation of a galactic
constitutive law.

Our coefficient checks using that formula are:

- The flat-space Unruh and de Sitter temperatures obey
  \(T_U(g)/T_\Lambda=g/A=y/q\), not \(y\). Even assuming a
  classical energy ratio gives the mean occupancy, its slope is \(1/q\).
  Two OR channels would give \(\kappa=q/2\approx1.44720\).
- A fixed positive gap \(\epsilon\) at \(T_U(g)\) has geometric-mode
  engagement \(p=\exp[-\epsilon/(k_BT_U)]
  =\exp[-B/y]\), \(B>0\). Its right derivative at zero is zero.
  This reconstructs the low-acceleration obstruction already in L238.
- At the full de Sitter temperature the same engagement is nonzero at
  \(g=0\). Subtracting that background leaves an \(O(y^2)\) response,
  since \(\sqrt{q^2+y^2}-q=y^2/(2q)+O(y^4)\). A smooth
  finite-gap function of this temperature cannot produce a nonzero linear
  coefficient after background subtraction.

The different identification
\(\mu(g/s)=[\sqrt{g^2+A^2}-A]/g\) has slope \(1/(2q)\),
and therefore \(a_0=2A\), \(\kappa=2q\approx5.78881\).
This matches the conditional temperature-excess proposal in M. Milgrom,
*The modified dynamics as a vacuum effect*, arXiv:astro-ph/9805346v2,
26 January 1999,
[Eqs. (8)–(9), page 5](https://arxiv.org/pdf/astro-ph/9805346v2).
That source explicitly leaves the inertia interpretation and extension to
general trajectories unresolved. Neither paper establishes unit channel slope.
The nearby number \(q/(2\pi)\approx0.460659\) in `kappa_closure` follows
from a different scale identification \(a_0=A/(2\pi)\); it is not one half.

No local exact-version source copies were found by filename search; the two
primary PDFs were read online on 2026-09-20. No literature-wide absence or
novelty claim is made, and no source cache was changed in this scoped report.

## Why PD03's energy argument does not supply the missing arrow

PD03 line 129 identifies the response scale with the vacuum's
channel-kinetic energy share:

\[
\frac{a_0^2}{G}=\frac{u_\Lambda}{4}.
\]

Since \(u_\Lambda=c^2\rho_\Lambda\) and \(s^2=Gu_\Lambda\), this is
exactly \(\kappa^2=1/4\). A horizon potential coefficient or a kinetic
equipartition factor does not determine the coefficient that identifies
\(a_0^2/G\) with a physical field energy density. Keeping that coefficient
explicit, \(C a_0^2/G=u_\Lambda/4\) gives
\(\kappa=1/(2\sqrt C)\). The checked code states mode matching as a
premise and evaluates an identity; it does not vary an independently
normalized energy functional to fix \(C=1\).

## Verification and obligation ledger

An inline `python3`/SymPy calculation was run against the source revision
above. Eight exact assertions passed: normalization of \(f_\lambda\),
its activation integral, the origin slope, saturation, the two-channel
slope, positivity formula \(\mu'=2\lambda/(1+\lambda y)^3\),
\(\kappa=1/(2\lambda)\), and the de Sitter temperature-excess slope.
Separate symbolic calculations returned the classical energy integral,
fixed-gap derivative zero, and the quadratic de Sitter expansion.

The central checks can be reproduced without editing source files:

```python
import sympy as S
y, lam, v = S.symbols('y lam v', positive=True)
f = lam*S.exp(-lam*v)
p = S.integrate(f*S.exp(-v/y), (v, 0, S.oo))
assert S.integrate(f, (v, 0, S.oo)) == 1
assert S.simplify(p-lam*y/(1+lam*y)) == 0
assert S.limit(p/y, y, 0, dir='+') == lam
assert S.limit(p, y, S.oo) == 1
mu = 1-(1-p)**2
assert S.limit(mu/y, y, 0, dir='+') == 2*lam
assert S.simplify(S.diff(mu,y)-2*lam/(1+lam*y)**3) == 0
assert S.simplify(1/S.limit(mu/y,y,0,dir='+')-1/(2*lam)) == 0
q = S.sqrt(8*S.pi/3)
mu_ds = y/(S.sqrt(y*y+q*q)+q)
assert S.limit(mu_ds/y,y,0,dir='+') == 1/(2*q)
```

| Obligation | Status |
| --- | --- |
| OR slope and MOND scale matching | Passed, conditional on the stated constitutive assumptions |
| Geometric distribution implies its mean equals \(g/s\) | Not established |
| Classical field statistics can produce the rational shape | Passed for the two explicitly stipulated response models |
| Equipartition fixes response coupling | Not established |
| Fixed positive-gap Unruh mode produces linear deep response | Failed for the model examined |
| Gapless continuum is ruled out by the fixed-gap result | False; explicit counterfamily above |
| de Sitter temperature fixes unit channel slope | Not established; direct identifications give other slopes or zero |
| PD03 mode matching follows from an independent energy normalization | Not established |

The strongest safe outcome is a sharpened constructive research target:
derive an acceleration-coupled, particle-free field spectral measure whose
infrared response weight is exactly one in \(s\)-units, or prove the
equivalent source/temperature normalization from an independently specified
action. The statistical shape and channel count alone do not do that work.
