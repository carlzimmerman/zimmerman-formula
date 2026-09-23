# The photospheric phase-gravity law

## 1. Exact physical contract

Consider one unresolved, spherical, radially moving photospheric layer enclosing
a constant gravitating mass M. Its radius R(t)>0 is material: the acceleration
of the gas represented by the fitted atmosphere is R''(t). Time is source-rest
time. Newtonian gravity is valid, and rotation, magnetic stress and other
unmodelled accelerations are negligible.

Let g_s(t) be the *input gravity parameter of a static atmosphere model* matching
the local density, pressure and radiative acceleration. It is not assumed equal
to GM/R². Radiation must be included consistently in both the physical and fitted
atmosphere; g_s is not a gas-pressure-only effective gravity with radiation
subtracted a second time. The existence of such a quasi-static spectral mapping
at each retained epoch is a premise. Exclude shock phases where it fails.

Let the corrected bolometric flux and fitted effective temperature give

    q(t) = sqrt[F(t)/F(t_ref)] [T(t_ref)/T(t)]²,   R(t) = R0 q(t).

Here R0=R(t_ref). A constant flux calibration, luminosity distance and common
lensing magnification cancel in q. Relative magnifications of different lensed
images, time-variable microlensing, host subtraction and variable attenuation do
not cancel automatically. An atmosphere-model bolometric correction is still
required. No Rayleigh-Jeans or single-band approximation is used.

This contract is stronger than merely observing a changing optical-depth surface.
A steady wind can have a stationary photosphere despite rapidly moving gas.
An unresolved ensemble also need not have a single material R(t).

## 2. Derivation, including the sign

Take outward acceleration positive. Radial momentum balance is

    a_gas = -rho^-1 dP_gas/dr - GM/R² + g_rad.

The corresponding static atmosphere satisfies

    0 = -rho^-1 dP_gas/dr - g_s + g_rad.

Subtracting gives a_gas = g_s - GM/R². On a material photosphere:

    g_s(t) = GM/R(t)² + R''(t).                         (1)

Outward *acceleration*, not the sign of velocity alone, makes g_s exceed true
gravity. A decelerating outflow has the opposite correction. A blue absorption
centroid alone cannot fix this term or its sign.

Define A=GM/R0² > 0. Then

    q² [g_s - R0 q''] = A,                             (2)
    Y(t) = A + R0 X(t),  Y=g_s q²,  X=q² q''.           (3)

Every epoch must lie on one line, with positive slope and intercept. Two distinct
X values identify the two constants; further epochs test the relation. For any
three epochs the determinant of the rows (1,X_i,Y_i) vanishes. When the variation
is uninformative (e.g. q constant), the inversion is not identifiable.

    R0 = (Y_i-Y_j)/(X_i-X_j),    M = A R0²/G.           (4)

This weighs the *enclosed mass*, not necessarily the black hole alone. Envelope
self-gravity is included if that enclosed mass is constant; separating the BH
from its envelope requires additional information.

The equation is a Newtonian consequence, not a new modification of gravity.
Its application here removes a missing dynamical assumption from the existing
BH* inference. Stellar photometric-hydrodynamic methods are prior art.

## 3. Integral form: no derivatives of measured radius

On any finite interval [t_a,t_b], choose a smooth test function w with
w=w'=0 at both ends. Twice integrating by parts yields

    integral g_s w dt = A integral q^-2 w dt
                       + R0 integral q w'' dt.        (5)

Only the known weight is differentiated. No period, oscillation-mode constant,
second derivative of noisy data, or complete cycle is needed. Multiple weights
give an overdetermined two-column linear system. Its rank and conditioning must
be checked, and the shared-data covariance must be propagated in a real fit.
Six weights are six mathematical equations, not six independent observations.

With s=(t-t_a)/Delta_t and w_j=s²(1-s)²(2s-1)^j, the stable numerical convention is

    b_j = A U_j + B V_j,
    b_j = integral_0^1 g_s w_j ds,
    U_j = integral_0^1 q^-2 w_j ds,
    V_j = integral_0^1 q d²w_j/ds² ds,
    B = R0/Delta_t².                                  (6)

At least two independent rows determine A,B; other rows are null tests. Positive
A and B are necessary for the model. Smooth fitting to the observations, finite
sampling and flux/gravity covariance remain real measurement problems. One
cannot manufacture the continuous record from four lensed images without a
time-evolution model.

## 4. Two cycle invariants and a harmonic law

If q and q' are periodic, use time averages over a complete cycle. Averaging (1)
and then averaging q times (1), with <q q''>=-<q'^2>, gives

    A = <g_s>/<q^-2>,
    R0 = [A<q^-1> - <g_s q>]/<q'^2>.                  (7)

The numerator must be positive for nonconstant q and positive R0. This is an
alternative inversion, not a claim that a population stack is a time average.

With Fourier convention h_k=<h(t) exp(-i k omega t)>:

    (g_s)_k - A(q^-2)_k = -R0 k² omega² q_k.           (8)

For every measured nonzero q_k, the inferred

    -[(g_s)_k-A(q^-2)_k]/(k² omega² q_k)

must be the same positive real radius. The k² scaling supplies a shape-independent
test across resolved harmonics; it assumes neither a sinusoidal pulsation nor a
universal fundamental-mode eigenvalue. A single detected harmonic carries less
overdetermination. The k=0 equation determines A but contains no radius.

Also, for a closed smooth cycle,

    integral_cycle g_s dq = 0,                        (9)

because both integral q'/q² dt and integral q''q' dt are boundary terms. A zero
signed area alone is necessary, not sufficient: lobes can cancel, and wrong
models may pass this single test. Equation (5) is the stronger test family.

## 5. What replaces the existing Eddington readout

Combining the actual gravity with Stefan-Boltzmann gives

    Gamma_es(t) = kappa_es sigma_SB T(t)^4 /
                 [c (g_s(t)-R0 q''(t))]
               = kappa_es sigma_SB T(t)^4 q(t)²/(c A). (10)

Wave U is recovered when acceleration vanishes. Its numerical value 56.6 is
therefore a static-atmosphere inference, not an acceleration-independent
measurement. A full cycle can determine A without recovering R0, which is useful
if the radius inversion is poorly conditioned. The constant kappa_es convention
defines Gamma_es; it is not the actual flux-mean opacity of a recombining wind.

## 6. A sharp amplitude-period bound

At a smooth local maximum of a material radius, R''<=0. If the fitted atmosphere
has g_s>=0 there, (1) forces

    M >= R_max² |R''_max|/G.                           (11)

For the explicitly assumed waveform R=R0[1+epsilon cos(2 pi t/P)], epsilon>0,

    M >= 4 pi² epsilon (1+epsilon)² R0³/(G P²).        (12)

No mode constant enters. In AU, years and solar masses its coefficient is nearly
one. An example, *not a measurement*: R0=941 au, P=32 rest-frame years and a 10%
radius amplitude require M>=9.85e4 solar masses. R0=2000 au gives 9.45e5 solar
masses. The first example combines a population-scale radius with an illustrative
period; it is not a claim about one observed source. A luminosity amplitude is
not a radius amplitude without the simultaneous temperature curve.

The bound can fail physically if the surface is not material, if a shock invalidates
the atmosphere mapping, if g_s is permitted to be negative, or if forces/model
terms omitted in section 1 matter. It is a falsifier of a joint model, not a
universal lower mass bound for every LRD.

## 7. Important systematic counterexamples

* Material-surface failure: with delta(t)=a_gas-R'' plus atmosphere/force errors,
  (1) gains +delta(t). Residuals need not signal non-Newtonian gravity.
* Absorbable systematics: delta(t)=a/q²+b q'' produces a perfect line with biased
  A and R0. Even infinitely precise satisfaction of (2) cannot exclude these.
* Time dilation: q''_rest=(1+z)² q''_obs. Using observer time without correction
  overestimates R0 by (1+z)² and M by (1+z)^4. Lensing delays also require this
  conversion and a consistent emission-time ordering.
* Multiplicity: identical synchronized emitters have the same q and g_s as one.
  The inferred radius and mass describe a component; the law alone cannot count
  components. Absolute flux could then supply an additional multiplicity test.
* A fixed period adopted from a theoretical mass is not an independent mass test.
  The 32-year period in arXiv:2512.05180v1 is model-adopted, not a directly measured
  period suitable for an unconditional use of (12).

## 8. Secondary route: the exterior-layer density ceiling

Assume the same enclosed point mass dominates at R_phot and r_B>=R_phot, and
the proposed *local-gas-density* transition is GM/r_B²=(c/2)sqrt(G mu_H m_p n_H).
Writing g_N=GM/R_phot² gives

    (r_B/R_phot)² = 2g_N/[c sqrt(G mu_H m_p n_H)],
    n_H <= 4g_N²/(c² G mu_H m_p).                     (13)

This is independent of mass, distance and absolute luminosity. At the median
static reading log10(g/cgs)=-2.2 and mu_H=1.4 it is n_H<=1.13e6 cm^-3;
n_H=1e10 cm^-3 instead implies r_B/R_phot=0.103. A dense *external* absorption
shell and this transition identification cannot both satisfy those static inputs.

This is not a new field equation, nor a measured exclusion of the BH* model.
The theory's cosmological density is not automatically the local gas density.
Line absorption may cover a different emitting region; stratification, clumps,
enclosed mass changes and the g_s-to-g_N correction must be resolved. The June
ABCD covering factors refer to their fitted emitting components and cannot be
inserted as continuum occultation depths without a geometry/transfer mapping.
For that reason the initially attractive absorption-depth bound was not promoted
to an observational result. A shell thickness N_H/n_H is not r_B either.
