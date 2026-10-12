# The one-field potential selects a cold linear instability band

2026-10-11. Continuation of [the field construction](REPORT.md) and
[the expanding finite-mode calculation](EXPANSION.md).

**Result:** for a homogeneous radial oscillation confined to one vacuum well,
the daughter fluctuation equation of the proposed potential is exactly the
one-gap Lame equation. Its only finite exponential-instability band can be
placed entirely at nonrelativistic momenta. This is a continuum statement
about the linearized, nonexpanding equation, not a selection of a few modes
or a completed nonlinear production history.

## Exact background and change of variables

Use the declared potential

\[
 V=\rho_\Lambda+\frac\lambda4(X^2+Y^2-f^2)^2+\frac{m^2}{2}Y^2,
 \qquad M^2=2\lambda f^2.
\]

Set H=0, Y=0, z=X/f and tau=M t. The radial equation is
z''+(z^2-1)z/2=0. For 1<A<sqrt(2), an exact solution is

\[
 z(\tau)=A\,\operatorname{dn}(A\tau/2,k_e),\qquad
 k_e^2=2-2/A^2,\qquad T_\tau=4K(k_e)/A.
\]

The symbol k_e is an elliptic modulus, not a physical momentum. Substitution
uses dn''=(2-k_e^2)dn-2dn^3, and A^2(2-k_e^2)=2. The lower turning point
is sqrt(2-A^2)>0, so the background stays in the +f well. The source energy
above its vacuum is exactly M^2 f^2(A^2-1)^2/8. There is no external energy
in this homogeneous classical background, but linearizing the daughters
neglects their later depletion of it.

For every physical spatial momentum p>=0, the transverse fluctuation obeys

\[
 Y_p''+\left[\frac{p^2+m^2}{M^2}+\frac{z^2-1}{2}\right]Y_p=0.
\]

With v=A tau/2, r^2=(p^2+m^2)/M^2 and
h_L=k_e^2+4r^2/A^2, this is exactly

\[
 \frac{d^2Y_p}{dv^2}+[h_L-2k_e^2\operatorname{sn}^2(v,k_e)]Y_p=0.
\]

No small-amplitude approximation has entered this reduction. The only
restrictions so far are the fixed background, linear daughters, canonical
action and below-barrier radial orbit.

## Spectral input and its precise application

For 0<k_e<1, the n=1 Lame operator has spectral bands
[k_e^2,1] and [1+k_e^2,infinity), with its sole finite open gap
(1,1+k_e^2). On an open gap, real-time Floquet solutions have growing and
decaying exponential factors. Band edges have zero exponential rate and
may have a second solution with secular growth.

Source: Haragus and Kapitula, *On the spectra of periodic waves for
infinite-dimensional Hamiltonian systems*, author manuscript dated
2007-05-15, [printed page 16, section 3.1.1](https://sites.calvin.edu/tmk5/research/PeriodicWaveSubmissionOld.pdf).
It explicitly identifies the one-gap operator and its edges and dn, cn, sn
edge eigenfunctions. The equation convention was also checked against
[NIST DLMF 29.2](https://dlmf.nist.gov/29.2). Checked 2026-10-11;
no local source copy retained. The source's spatial spectral variable becomes
our time variable v; the Floquet multiplier criterion supplies the translation.
No NLS stability theorem from that paper is transferred to this field theory.

Since r^2>0, h_L>k_e^2. The lower semi-infinite gap is inaccessible.
The only possible exponential instability is consequently

\[
 \boxed{\frac{M^2}{4}(2-A^2)<p^2+m^2<\frac{M^2}{4}A^2.}
\]

This excludes additional hot exponential-resonance bands in this exact
linear problem. It does not assert zero finite-time excitation outside the
band, absence of radial instabilities, or nonlinear stability.

## A cold band without manually deleting hot momenta

Write M=2m sqrt(1+u_*^2) and A=1+epsilon. The full instability interval is

\[
 u_*^2-(1+u_*^2)(2\epsilon+\epsilon^2)
 <p^2/m^2<
 u_*^2+(1+u_*^2)(2\epsilon+\epsilon^2),
\]

intersected with p^2>=0. Both the location and width are now consequences
of the stipulated masses and source amplitude, rather than a truncation
to chosen daughter modes. They remain adjustable physical inputs.

At u_*=0.001 and epsilon=1e-7, the interval is
7.9999979e-7 < p^2/m^2 < 1.20000021e-6, or approximately
0.000894427 < p/m < 0.001095445. Every exponentially growing daughter mode
is therefore nonrelativistic. At epsilon=0.1 the band extends to p/m about
0.458, so cold production is not generic for arbitrary source amplitude.

In a quantum treatment the fluctuation mode functions have nonzero canonical
Wronskian even in their vacuum. Inside an unstable band, a mode function
proportional solely to the real decaying solution would have zero Wronskian;
thus it cannot describe a normalized vacuum mode. Vacuum fluctuations can
seed the growing solution without inserting classical daughter matter.
Backreaction must stop the linear growth before it exceeds the finite source
energy. This statement does not calculate the stopping time or final yield.

## Numerical cross-check and scope

[linear_band.py](linear_band.py) computes monodromies independently of the
band classification, using the exact background in an interaction picture.
This avoids subtracting trace-squared and four near a degenerate multiplier.
It tests epsilon=1e-7,1e-5,0.001,0.1 at specified inside/outside points and
higher momenta, including a zero-modulation control and tighter weak-band
integration. All 104 checks pass. The center amplitude growth rate at
epsilon=1e-7 is 5.00000025e-8 per tau, approximately m epsilon per physical
time. Growth of occupation has twice the amplitude exponent.

[Results](linear_band_run/results.json) and
[manifest](linear_band_run/manifest.json) preserve the finite checks. The
all-momentum assertion rests on the exact reduction and spectral result,
not on the finite sample. The named source supplied the one-gap theorem;
the change of variables and physical inequalities were checked by self-review.
This is a translated application of known mathematics, not a novelty claim.

The full production goal remains incomplete. In particular:

* Expansion destroys strict periodicity. A frozen-background band can guide
  an adiabatic calculation, but is not its result.
* Source fragmentation and radial fluctuations have not been excluded.
* Daughter backreaction, inverse conversion and nonlinear scattering can
  change the spectrum after growth begins.
* Abundance, mass tuning, source preparation and the vacuum/galaxy-law
  connection still require physical mechanisms.

The next useful calculation is a self-consistent parameter and backreaction
screen followed by an expanding, continuum mode evolution, including the
radial response. A lattice initialized only with the desired cold band would
not answer that question.
