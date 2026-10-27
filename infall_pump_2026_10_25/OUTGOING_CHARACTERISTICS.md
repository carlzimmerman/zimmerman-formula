# Measure radiation, not a moving Coulomb tail

In a source-free radial region choose the known retarded initial scalar gauge
chi_infinity=0 and put u=r chi. Then u_tt-c^2 u_rr=0. The positive outgoing
and incoming energies are one quarter of integral(u_t-/+c u_r)^2 dr.
The original radial energy differs by -c^2[u^2/r]/2 at the interval boundaries.
In particular a STATIC1/r tail has positive field energy and ZERO radiation.
Do not estimate its asymptotic gauge by subtracting chi at a finite radius:
that would subtract part of the physical1/r tail and create balanced spurious
outgoing/incoming terms. The analytic Coulomb calibration caught that error.

On a uniform far grid of spacing h use edge u_t averages and Delta u/h. There
is an exact discrete identity for the half-endpoint finite-volume interval:

 E_field = E_out + E_in -c^2[u^2/r]/2 + E_grid,

 E_grid = sum[h(Delta u_t)^2/8
             +h^3(pi_i^2+pi_j^2)/48
             +c^2 h(Delta chi)^2/8] >=0.

It follows by r_edge^2=r_i r_j+h^2/4 and

 r_i r_j(Delta chi)^2=(Delta u)^2-h Delta(u^2/r).

The temporal kinetic correction uses wave_volume/h=r_i^2+h^2/12.
This isolates the numerical correction instead of calling it radiation.
The analytic tests check Coulomb, low-frequency and20rad/Myr outgoing packets,
the incoming numerical floor and the discrete identity independently.

Actual far-field states can now distinguish exported excitations from the
reactive boundary contribution. The finite-radius signed flux remains an
independent conservation measurement, but is not identical to asymptotic
radiation while the tail is building. The outer material source work is also
checked rather than silently assumed absent.

Spectral bands of a finite outgoing packet are reported with two Hann windows.
They are WINDOWED proxies with their frequency resolution stated, not exact
mode occupations or a proof of a noncollinear material cascade. Ratios below
an explicit relative numerical-energy floor are suppressed. The source-free
annulus and known retarded initial gauge are hypotheses of this analysis.
