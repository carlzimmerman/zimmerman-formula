# The geometric connection exists; the cold-carrier mechanism remains open

2026-10-14. This investigation checks the black-hole/cosmological-horizon link against the current cold-tether question. It establishes conditional geometric identities and tests three physical interpretations. It does not identify a new particle or derive tethering. The geometric-mean radius was already recorded in the project's [October 10 audit](../geometric_selection_2026_10_10/REPORT.md); this work connects it explicitly to horizon-area loss and tests the proposed physical arrows.

## 1. Which horizon and which mass?

Take a true positive cosmological constant, in four dimensions:

\[
\rho_{DE}=\frac{\Lambda c^2}{8\pi G},\qquad
L=\sqrt{3/\Lambda}=c/H_\infty.
\]

This is the de Sitter curvature/horizon radius. It is not generally today's Hubble radius or the event-horizon radius in a time-dependent FLRW spacetime. With the project's assumed law and fitted coefficient,

\[
a_0=\tfrac12c\sqrt{G\rho_{DE}}
 =\alpha\frac{c^2}{L},\qquad
\alpha=\sqrt{\frac{3}{32\pi}}=0.1727470747.
\]

For a spherical source of mass M define its gravitational length \(r_g=2GM/c^2\). Then its model transition radius satisfies

\[
\boxed{r_M=\sqrt{GM/a_0}
 =\frac{\sqrt{r_gL}}{\sqrt{2\alpha}}
 =1.7013\sqrt{r_gL}.}
\]

The coefficient is conditional on the fitted a0 law. No geometric argument here independently selects it. A galaxy has a gravitational length without having a black-hole event horizon at that radius. For a small Schwarzschild black hole, r_g approximates its actual horizon radius.

## 2. An exact relation between the two horizons and entropy

In the vacuum Schwarzschild-de Sitter (Kottler) geometry,

\[
f(r)=1-\frac{r_g}{r}-\frac{r^2}{L^2},
\quad ds^2=-f c^2dt^2+f^{-1}dr^2+r^2d\Omega^2.
\]

The two positive roots rb, rc are the black-hole and cosmological horizons. For \(0<r_g/L<2/(3\sqrt3)\), the cubic gives exactly

\[
r_b^2+r_br_c+r_c^2=L^2,\qquad
r_g=\frac{r_br_c(r_b+r_c)}{L^2}.
\]

Let entropy be measured in units of kB, with \(\ell_P^2=\hbar G/c^3\): \(S_b=\pi r_b^2/\ell_P^2\), \(S_c=\pi r_c^2/\ell_P^2\), \(S_0=\pi L^2/\ell_P^2\). Therefore

\[
\boxed{S_0-S_b-S_c=\frac{\pi r_br_c}{\ell_P^2}=\sqrt{S_bS_c}.}
\]

This is an exact identity for this vacuum solution, not a new entropy law. Its standard entropy-bound setting is discussed in [Bousso's primary paper](https://arxiv.org/pdf/hep-th/0012052). If \(A_0=4\pi L^2\), \(A_c=4\pi r_c^2\), the cosmological horizon's area loss obeys

\[
\Delta A_c=A_0-A_c=4\pi r_b(r_b+r_c),\qquad
\boxed{4\pi r_M^2=\frac{r_c}{2\alpha L}\,\Delta A_c.}
\]

For astrophysical masses rb/L is tiny. Then

\[
r_b\simeq r_g,\quad r_c\simeq L-r_g/2,\quad
\Delta A_c\simeq4\pi r_gL,\quad
\Delta S_c\equiv S_0-S_c\simeq\frac{2\pi McL}{\hbar}.
\]

Thus the transition-sphere area is about 2.8944 times the lost cosmological-horizon area. In this precise sense, the transition radius is tied to the geometric mean of a source mass length and a vacuum horizon length. The total two-horizon entropy deficit and the cosmological entropy loss differ by Sb; they should not be conflated, although their leading small-mass term agrees.

For an extended spherical source with a vacuum exterior, its exterior mass parameter still determines the cosmological horizon. A formal smaller root of that exterior solution is not necessarily a physical interior horizon. The two-actual-horizon entropy identity applies to the actual vacuum black-hole solution; it cannot be asserted for a galaxy's interior without solving the matter geometry.

## 3. Does ordinary vacuum curvature generate the required force?

The weak-field acceleration in the same metric is

\[
\ddot r=-GM/r^2+H_\infty^2r.
\]

The vacuum term is outward. Its balance with Newtonian attraction occurs at

\[
r_{ta}=(GM/H_\infty^2)^{1/3}=(r_gL^2/2)^{1/3},
\]

which scales as M^(1/3), whereas rM scales as M^(1/2). Independently, direct evaluation of the radial-metric curvature invariant gives

\[
R_{abcd}R^{abcd}=\frac{12r_g^2}{r^6}+\frac{24}{L^4}.
\]

Equality of these mass-curvature and vacuum-curvature pieces occurs at \(r_K=2^{1/6}r_{ta}\), also the wrong scaling for rM.

Assigned examples using canonical a0=9.360324825e-11 m/s² and L=5.375398211 Gpc:

| Assigned source | rM | rta | rK | Vacuum acceleration at rM / a0 |
|---|---:|---:|---:|---:|
| 4e6 solar masses | 77.18 pc | 17.68 kpc | 19.85 kpc | 8.31e-8 |
| 1e8 solar masses | 385.89 pc | 51.71 kpc | 58.04 kpc | 4.16e-7 |
| 6e10 solar masses | 9.452 kpc | 436.15 kpc | 489.56 kpc | 1.02e-5 |
| 1e14 solar masses | 385.89 kpc | 5.171 Mpc | 5.804 Mpc | 4.16e-4 |

For the galaxy example, the mass-curvature contribution exceeds the vacuum-curvature contribution by 1.93e10 at rM. Therefore neither ordinary vacuum-force balance nor equality of these curvature invariants explains the model's transition. This is an obstruction to these specific interpretations, not to every nonlocal vacuum response.

## 4. A specified entropy-response proposal: close normalization, different force

[Verlinde 2016](https://arxiv.org/html/1611.02269v2), Eqs 4.28–4.30, postulates a distributed de Sitter entropy and a local mass-induced entropy removal. Restoring SI units and using dimensionless entropy,

\[
S_{DE}(r)=\frac{\pi r^3}{\ell_P^2L},\qquad
|S_M(r)|=\frac{\pi r_gr}{\ell_P^2}.
\]

Their balance gives \(r_*=\sqrt{r_gL}=0.58779r_M\). These local entropy assignments are additional hypotheses, not consequences of the two horizon roots. More generally, multiplying them by independent positive constants eta and zeta gives \(r_*^2=(\zeta/\eta)r_gL\): the square-root mass scaling survives while its normalization varies.

The paper's spherical elastic estimate gives, outside a compact source,

\[
g_D^2=a_Vg_b,\quad a_V=c^2/(6L)=0.964802a_0,
\quad g_V=g_b+\sqrt{a_Vg_b}.
\]

Its assumptions include isolation, approximate spherical equilibrium and saturation of an elastic inequality. It includes hot gas as a source. It does not supply the project's massive carrier, phase-specific tether, or full dynamical action.

Comparison with the current nonstiff simple response, rather than the project's older quadrature kernel:

\[
g_{simple}=\tfrac12\left(g_b+\sqrt{g_b^2+4a_0g_b}\right).
\]

| gb/a0 | gsimple/a0 | gV/a0 | Relative difference |
|---:|---:|---:|---:|
| .01 | .105125 | .108224 | +2.95% |
| .1 | .370156 | .410613 | +10.93% |
| 1 | 1.618034 | 1.982243 | +22.51% |
| 10 | 10.916080 | 13.106126 | +20.06% |

In the strict deep limit, the inferred extra-force amplitude differs by only -1.78%. This makes the horizon elastic estimate a relevant candidate to investigate, but not an exact derivation of the current force law. These are assigned formula comparisons, not rotation-curve fits or a test of the stiffness-corrected Solar System regime.

There is also a direct check on the simplest entropy-force guess. If one identifies a displaced test mass m with the local entropy magnitude \(2\pi mc r/\hbar\), and uses the de Sitter temperature \(k_BT_{dS}=\hbar c/(2\pi L)\), the formal prescription \(F=k_BT_{dS}\,dS/dr\) gives

\[
|F|=mc^2/L,\qquad |F|/m=c^2/L=5.78881a_0.
\]

This has no radius dependence and is not the required deep extra acceleration \(\sqrt{GMa_0}/r\). The identification of an expanding entropy-region radius with the position of a test mass is itself an extra assumption. This calculation rules out that particular naive identification as the full tether law; it does not rule out a properly defined elastic or nonlocal response. The global cosmological entropy deficit alone contains no local test-particle position variable to differentiate.

## 5. Could a central black hole supply or control the cold carrier?

**Mass scaling.** For an assigned galaxy Mbar=6e10 solar masses and central MBH=4e6 solar masses, rM,gal=9.452 kpc, while rM,BH=77.18 pc. The ratio is sqrt(MBH/Mbar)=0.008165. Replacing the source mass by the central BH therefore misses the galaxy scale by a factor 122.5. A mechanism involving BH-mediated global feedback could differ from this direct replacement, but needs its own transport equation. A historical independent warning is the [M33 dynamical study](https://arxiv.org/pdf/astro-ph/0107135), which found a central mass best fit of zero and an upper bound of 1500 solar masses; that is not a claim that M33 contains no smaller black holes or an updated 2026 bound.

**Thermal production.** The [Hawking calculation](https://astrofrelat.fcaglp.unlp.edu.ar/agujeros_negros/media/Papers/Hawking_1975-Particle_creation_by_black_holes.pdf) gives \(k_BT_{BH}=\hbar c^3/(8\pi GM)\) for an approximately Schwarzschild hole. A 1e8-solar-mass BH has kBT=5.317e-20 eV. The de Sitter bath here has kBT=1.893e-34 eV. Both are far below the project's .62, 16 and 143 eV rest-energy benchmarks. Setting kBTBH equal to those rest energies requires masses 1.705e19, 6.608e17 and 7.393e16 kg respectively, in a much smaller BH range. This comparison diagnoses thermal suppression for astrophysical holes; it is not a full emission-rate calculation or an exclusion of nonthermal production. Emission also does not by itself prepare cold, bound material.

**Absorption and angular momentum.** For Schwarzschild timelike geodesics, with x=r/rg and ell=Lspecific/(c rg), the effective potential is \((1-1/x)(1+\ell^2/x^2)\). The marginally bound unstable orbit has x=2, ell=2. Hence, for v much less than c,

\[
b_{cap}\simeq2r_gc/v=4GM_{BH}/(cv),\quad
\sigma_{cap}\simeq16\pi G^2M_{BH}^2/(c^2v^2).
\]

For the 4e6-solar-mass example and v=100 km/s, bcap=.002295 pc. An assigned homogeneous density .01 solar masses/pc³, continuously refilling the incoming capture trajectories, gives only .1693 solar masses captured over 10 Gyr. A real central spike, scattering and non-gravitational interactions could change this; it is not a global halo capture bound. It does show why an absorbing horizon is not automatically a kpc-scale tether. A horizon can receive energy and angular momentum only after something transports them to the capture trajectories. The prior [receiver audit](../cold_final_mile_2026_10_13/OPEN_FLOW_AND_RECEIVER.txt) leaves that transport and reciprocal energy accounting open.

## 6. The missing arrow is now more sharply identified

There is a consistent geometric chain:

positive Lambda -> cosmological horizon length L;
source stress-energy -> a changed cosmological horizon area;
conditional project a0 law -> rM² proportional to the area change.

The missing physical chain is:

horizon entropy change -> a specified local/nonlocal interaction -> a retained cold massive medium -> the measured force and source dependence.

Two important source problems remain even if a horizon response is accepted:

1. The metric responds to total gravitating stress-energy. Equal spherical mass distributions made from stars or hot gas give the same leading exterior mass parameter. The vacuum entropy identity cannot classify their thermodynamic phase. A temperature/current-dependent operator or a medium-state transition needs an actual coupling and reciprocal work term.
2. If the cold carrier is real gravitating rest mass, it contributes to that total mass as well. One cannot insert only Mbar into a horizon's exterior mass parameter and then infer an additional massive halo for free. The geometry must be solved with both components. For the nonstiff spherical simple-law template, Mtotal(<r)/Mbar=(1+sqrt(1+4(r/rM)²))/2, already 10.512 at 10rM. An exterior horizon budget would depend on the finite completed system, not just the baryonic seed. No physical inner horizon is implied by this template.

The most concrete surviving research route is a horizon-normalized constitutive response of the medium, with BH horizons treated as possible receivers. Its decisive requirement is a covariant or controlled effective action that derives the response and its coefficient while keeping a finite carrier/energy budget. For this route to count as the proposed tether mechanism, variation must also derive the phase/current dependence, source reciprocity and dynamical receiver. The preceding geometric equations do not supply these.

## Evidence, limits and resumption

`run_v1/results.json`: 59 checks passed, including exact symbolic root/entropy/curvature/geodesic identities, nine high-precision horizon-ratio cases, five assigned mass examples and three finite-speed capture checks. Ninety decimal digits avoid catastrophic subtraction in tiny horizon-area changes. The validated manifest pins code, contract and canonical project constants. These bounded numerical checks supplement the displayed algebra; they do not establish a universal physical mechanism. No large simulation or external message was launched.

Geometry route: exact conditional connection established. Ordinary local vacuum force/curvature explanation: fails the specified scale and sign tests. Central-BH direct mass replacement and thermal supply at benchmark carrier masses: fail the assigned galaxy/energy-scale tests. Horizon elastic response: relevant but distinct formula and unclosed carrier interpretation. BH receiver: possible, transport unresolved. Resume a mechanism test when a candidate response action, entropy-to-stress rule or quantitative carrier-production/transport interaction is supplied or constructed; its first checks must include total-mass sourcing and reciprocal energy flow.
