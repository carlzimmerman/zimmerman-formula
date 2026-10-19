# QCD-C: exact topological Maxwell calculations

Parent FSP-002; checkpoint FSP-003. Scope: a controlled test of the inference
from gauge topology/contact terms to a linear inverse-size vacuum stress.
No parameter is fitted to dark energy, a proton mass, or alpha.

The strongest result is an exact cancellation. In compact 2D Maxwell theory,
the fully summed topological sectors leave **zero linear-H coefficient** on a
large sphere and an exponentially small finite-area stress, while the
topological susceptibility approaches a nonzero constant. A separate compact
4D Maxwell flux calculation gives explicit nonperturbative coupling dependence,
inverse-fourth-length stress, and exact cancellation of that stress on an
equal-sided four-torus. Neither is a calculation of the QCD coefficient c_H.

## 1. Action, state, geometry and subtraction

Use units hbar=c=1. A compact connection a has holonomies modulo 2pi and
integer first Chern class k=(2pi)^-1 integral_M F. In two dimensions,

    S_E = (1/(2 e2)) integral_M F wedge *F - i theta/(2pi) integral_M F,
    e2 = e^2 > 0, [e]=mass, theta modulo 2pi.

M is a closed oriented Riemannian two-torus of area A=beta L, or a round
two-sphere of area A=4pi/H^2. No boundary, charged matter, or imposed source
varies with H. The torus path integral is the canonical trace on the compact
holonomy Hilbert space, at fixed theta. Its zero-temperature limit beta->infinity
is the corresponding ground-state sector, or the equal trace over exactly
degenerate sectors at theta=pi. The sphere is a Euclidean observable; no
Lorentzian cosmological state is inferred from it.

Use normalized Haar measure da/(2pi) for the holonomy, and the associated
heat-kernel measure. Set the cosmological counterterm to zero. The sole
topology-dependent constant multiplying Z is set to one by this gluing
normalization. For metric stress subtract the same-theta infinite-area value
epsilon_infinity(theta), holding e2 and theta fixed. The comparison is

    delta epsilon(A,theta) = -d_A log Z(A,theta) - epsilon_infinity(theta).

Define the metric response by W=-logZ and
delta W=(1/2) integral sqrt(g) E^{ab} delta g_ab. Because W depends only
on area, E^{ab}=epsilon g^{ab}, epsilon=d_A W. On the torus this yields
the physical energy density -(1/L)d_beta logZ=epsilon and Lorentzian pressure
p=(1/beta)d_L logZ=-epsilon. This states the metric-variation convention,
including its sign, without treating W/A as a stress.

## 2. Exact partition function and its measure

Gauss's law leaves the circle-valued spatial holonomy phi=integral a. The
Hamiltonian is

    H_theta = (e2 L/2)(-i d_phi - theta/(2pi))^2,
    E_n = (e2 L/2)(n-x)^2, x=theta/(2pi), n in Z.

Consequently, with u=e2 A/2,

    Z(A,theta) = sum_n exp[-u(n-x)^2]
               = sqrt(pi/u) sum_k exp[-pi^2 k^2/u + i k theta].        (1)

The second equality is Poisson summation. It also follows by decomposing F
into the harmonic flux F_k=(2pi k/A)vol_M and Gaussian fluctuations. The
classical action is 2pi^2 k^2/(e2 A), and the normalized Gaussian/zero-mode
measure supplies sqrt(2pi/(e2 A)). Omitting this prefactor changes the
theory and the metric observable.

For the sphere an independent gluing argument gives the same expression.
The disc heat kernel is K_u(phi)=sum_n exp[-u(n-x)^2] exp(i n phi).
Gluing discs with opposite boundary orientation and normalized Haar measure
gives integral K_{u1}(phi)K_{u2}(-phi) dphi/(2pi)=Z(u1+u2,theta).
All U(1) representation dimensions are one. There is no sphere-specific
power of representation dimension or area in this measure.

The torus formulas and their prefactor are authenticated in Cao, van Caspel
and Zhitnitsky, [arXiv:1301.1706v2](https://arxiv.org/pdf/1301.1706v2),
Section II, equations (6)-(16); their Appendix A gives the susceptibility
limit. The numerical source-byte hash, exact version and extraction caveat
are in `source_records.json`. The sphere gluing and calculations below are
derived here rather than ascribed to the torus source. Their conclusion's
QCD extrapolation does not supply a dimensional or state-matching theorem.

## 3. Metric stress, the cancellation, and susceptibility

Write brackets_e for the positive electric-sector weights in (1). Then

    epsilon(A,theta) = (e2/2) <(n-x)^2>_e.                            (2)

At theta=0, the flux weights are also positive. Differentiating their
normalization as well as their action gives

    epsilon(A,0) = 1/(2A) - 2pi^2/(e2 A^2) <k^2>_flux.               (3)

This is the load-bearing cancellation. At large A,
<k^2>_flux ~ e2 A/(4pi^2); its contribution cancels 1/(2A).
Keeping only k=0 is controlled at **small** e2 A, since omitted fluxes
scale as exp[-2pi^2/(e2 A)]. It is invalid for the large-area limit where
one would attempt a small-H coefficient.

For theta=0 define q=exp(-u). Equation (2) gives

    epsilon/e2 = [sum_{n>=1} n^2 exp(-u n^2)]
                 /[1+2 sum_{n>=1} exp(-u n^2)]
               = q - 2q^2 + O(q^3).                                (4)

Here epsilon_infinity=0. A direct uniform bound is

    q(1-q)/(1+q) <= epsilon/e2 <= q(1+q)/(1-q)^3.                     (5)

The upper bound uses n^2>=n and sum n^2 q^n=q(1+q)/(1-q)^3;
the lower keeps n=1 in the numerator and bounds the denominator by
1+2q/(1-q). Thus the leading coefficient e2 is calculated rather than
fitted, and every finite power-law correction in 1/A vanishes.

The theta susceptibility is a different derivative:

    chi(A,0) = -(1/A) d_theta^2 logZ|_0
             = <k^2>_flux/A
             = e2/(4pi^2) - [e2 A/(2pi^2)]epsilon(A,0).              (6)

Therefore chi_infinity=e2/(4pi^2) is nonzero while epsilon_infinity=0
and the finite-area stress is exponential. The topological contact response
does not by itself imply a power-law vacuum stress.

For fixed x reduced to [-1/2,1/2],

    epsilon_infinity(theta) = (e2/2)x^2.

Away from the endpoints the first gap is Delta=1-2|x|>0 in the
exponent u Delta. At x=0 there are two first excited states, producing
the coefficient in (4). At |x|=1/2 there are two degenerate ground states
and the first excitation has gap 2:

    Z(A,pi) = 2 exp(-u/4)[1+exp(-2u)+...],
    epsilon_infinity(pi) = e2/8,
    delta epsilon(A,pi) = e2 exp(-2u)+... .                          (7)

The large-area expansion is nonuniform if theta approaches pi as A grows.
Varying that source while taking H->0 would change the contracted path.

## 4. Sphere curvature and the logZ/metric distinction

On the sphere, R=2H^2, u=2pi e2/H^2. Equations (4)-(5) establish

    delta epsilon(H,0) = e2 exp[-2pi e2/H^2](1+O(exp[-2pi e2/H^2])),
    c_1^(2D) := lim_{H->0+} delta epsilon/(H e) = 0.                 (8)

This is an exact result in a genuine gauge theory with summed topological
sectors. It neither identifies e with Lambda_QCD nor turns H e into the
four-dimensional quantity H Lambda_QCD^3.

In contrast the intensive effective action is f=W/A=-logZ/A. It is
negative at theta=0 even though epsilon is positive; its leading term is
-2 exp(-u)/A. At theta=pi,

    f = e2/8 - (log2)/A + O(exp(-2u)/A),

while its metric derivative has no -(log2)/A term. Inserting that
degeneracy term as an energy would create a spurious H^2 term on the
sphere. A local Euler term lambda integral R/(4pi)=lambda chi(M)
likewise changes f by a constant divided by A but has zero bulk metric
stress at fixed topology. A constant cosmological counterterm cancels in
the stated subtraction. Higher local curvature counterterms can alter
analytic higher-curvature response; their coefficients were set to zero
by the explicitly chosen heat-kernel model. None of these observations
supplies a universal nonanalytic linear-H coefficient for QCD.

## 5. Exact coupling dependence in 2D

At fixed area and theta, the response to e2 is calculated directly:

    d epsilon/d log e2 = epsilon - (e2^2 A/4) Var_e[(n-x)^2].         (9)

At theta=0 and large area this is
e2(1-u)exp(-u)+O(e2 u exp(-2u)). The limiting susceptibility is
linear in e2. If one defines a dimensionless alpha_2=e2/(4pi mu^2)
at a fixed reference mass mu, its logarithmic derivative is (9), but
that definition depends on mu and is not the physical 4D alpha(0).
The coefficient (8) and its fixed-e2 coupling derivative are zero for
every positive e2. No preferred value of the electromagnetic coupling
is selected by this result.

## 6. A four-dimensional Maxwell calculation with explicit alpha_M

For a second, independently defined controlled model use pure compact
Maxwell theory on a flat rectangular T^4, the same action normalization
S=(1/(2 e4^2)) integral F wedge *F, and theta_4=0. Now e4 is
dimensionless, alpha_M=e4^2/(4pi), and the six fluxes k_mu_nu are
integers. There is no charged matter and hence no matching or running
calculation that identifies alpha_M with measured alpha(0).

Let the coordinate periods be L_mu. The harmonic representative has
F_mu_nu=2pi k_mu_nu/(L_mu L_nu), and its exact classical action is

    S_k = (2pi^2/e4^2) sum_{mu<nu} k_mu_nu^2 V4/(L_mu^2 L_nu^2).

The Gaussian fluctuation and zero-mode integrals are identical in every
bundle: harmonic and exact forms are orthogonal, and the Abelian Hessian
is independent of k. Normalize by the zero-bundle partition function,
with the same metric, to cancel that determinant and measure. This
defines an exact **sector-comparison** observable, not the full photon
vacuum relative to infinite Minkowski space.

For L0=beta=rL and L1=L2=L3=L, let

    a=2pi^2/e4^2=pi/(2 alpha_M), S(t)=sum_k exp(-t k^2),
    M(t)=sum_k k^2 exp(-t k^2)/S(t),
    Z_flux/Z_0 = S(a r)^3 S(a/r)^3.                                (10)

This includes **all six** fluxes. Its thermodynamic metric response is

    rho_flux = -(1/L^3)d_beta log(Z_flux/Z_0)
             = (3a/L^4)[M(a r)-r^-2 M(a/r)].                       (11)

At fixed aspect r, the entire stress scales as L^-4. The response to
each of the four metric lengths has zero summed trace, since every
V4/(L_mu^2 L_nu^2) is invariant under a common rescaling. At r=1 the
Euclidean permutation symmetry and this trace relation force each
component to vanish, also visible directly in (11). Thus

    rho_flux(r=1,alpha_M)=0 for every alpha_M>0,

despite log(Z_flux/Z0)=6 log S(a)>0. Again, dividing the effective
action by volume would give an incorrect local stress. Dropping the
three time-space fluxes would also destroy this cancellation and
change the model.

Let V(t)=Var_t(k^2). The explicit coupling responses are

    d_logalpha log(Z_flux/Z0) = 3a[r M(ar)+r^-1 M(a/r)],
    d_logalpha rho_flux = (3a/L^4)[-M(ar)+r^-2 M(a/r)
                              +ar V(ar)-a r^-3 V(a/r)].             (12)

At weak coupling and fixed r the leading flux corrections are
exp[-pi r/(2alpha_M)] and exp[-pi/(2alpha_M r)], an explicit
nonperturbative dependence. It is an exponential in inverse coupling,
not an adjustable linear-H coefficient.

There is an additional exact normalization control. Poisson duality
gives S(t)=sqrt(pi/t)S(pi^2/t), hence for F=log(Z_flux/Z0),

    F(a,r)=3 log(pi/a)+F(pi^2/a,r).

At the Maxwell self-dual value alpha_M=1/2, d_logalpha F=3/2
independently of r, so d_logalpha rho_flux=0. This explains an exact
zero encountered by the numerical audit. Self-duality is a property
of this theory and charge convention; it is not a mechanism selecting
the observed fine-structure constant.

## 7. Bounded computation and evidence

`check_maxwell.py` implements the electric and flux sums separately,
fixed cutoff |n|,|k|<=80, at 120 and 150 decimal digits. Inputs are
the deterministic grid in `inputs.json`: 35 (u,theta) pairs per
precision, 6 sphere values, and 12 (alpha_M,r) pairs. The 4D couplings
1/500, 1/137, 1/20 and 1/2 are externally chosen benchmarks. The
1/137 benchmark is not a fit, prediction or physically matched value.

There are 378 checks per precision. They include both representations
of Z, stress and susceptibility; independent five-point derivatives in
area, theta and coupling; theta periodicity and reflection; numerical
Haar normalization and disc gluing; variation of the six separately
constructed 4D flux actions; metric trace; aspect inversion; scale
response; analytic versus numerical coupling derivatives; and the
self-dual zero. The repeated-precision observable error is at most
2.039e-89 on the stated scales. Exact-zero comparisons use the scale
of the noncancelled stress terms.

For each Gaussian moment of order p<=4, the omitted tail is bounded
analytically. With b=N+1-|x| and
r_p=((b+1)/b)^p exp[-t(2b+1)]<1, the two-sided tail is at most
2 b^p exp(-t b^2)/(1-r_p). These bounds are emitted for the 2D grid.
They control truncation; mpmath rounding is tested by higher precision
but not certified by interval arithmetic. The all-H limit is proved
by (5), rather than extrapolated from the grid.

Representative results with e2=1:

| H/e | delta epsilon/e2 | delta epsilon/(H e) |
|---:|---:|---:|
| 1 | 1.86049404813e-3 | 1.86049404813e-3 |
| 0.5 | 1.21615567091e-11 | 2.43231134182e-11 |
| 0.25 | 2.18754339521e-44 | 8.75017358085e-44 |

At the last point chi/(e2/(4pi^2))=1-8.7966e-42 approximately:
the contact susceptibility persists while the stress vanishes rapidly.
For the 4D coupling benchmark alpha_M=1/137, L=1, r=2,
rho_flux=-6.01231303265e-45 and
d_logalpha rho_flux=-6.40909854032e-43; at r=1 both vanish exactly.

Outcome: **implementation and finite assertion verified in the stated
range**, subject to the explicit arbitrary-precision rounding caveat.
`run_002/manifest.json` is the completed v2 evidence record. `run_001`
is preserved as a failed audit of a relative-error normalization at an
exact zero; its note and original source snapshot explain the failure.
No numerical failure was interpreted as new physics.

## 8. First unresolved implication and continuation

The implication established here is narrow but decisive: summed gauge
topology and a nonzero susceptibility do not force an algebraic finite-size
stress, let alone its power, coefficient or electromagnetic derivative.
The corresponding inference from these Maxwell examples to a universal
QCD H Lambda_QCD^3 term is unsupported. The exact zero in (8) is not a
proof that 4D QCD's coefficient vanishes.

The next executable continuation is the actual source-level Schwinger
comparison being pursued by the coordinator: derive the massive scalar
Green function from the cited torus metric/spectrum, retain all zero-mode
and determinant factors, and check whether a proposed tilted-torus 1/L
condensate survives normalized subtraction. A different subsequent
physical task is a fully specified QCD stress/topological-correlator
calculation in a fixed state and geometry. The Maxwell models contain
neither quarks nor a proton and therefore cannot provide c_H/C_p^3,
an independently matched alpha(0), or a physical alpha root.
