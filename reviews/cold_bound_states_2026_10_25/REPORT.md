# Boundary modes and self-bound cold clumps

## Result

The unchanged candidate admits localized linear boundary modes, but they are
confined to a microscopic layer on cluster scales. Their inward amplitude decay
length is at most 0.000530–0.003943 pc in the tested constant-density benchmarks.
They do not produce a diffuse interior density profile merely by being occupied.
Their total occupation is not fixed by the existence of an eigenmode.

For a uniform restored background, the exact scalar potential also excludes
nontrivial finite-energy, exactly periodic localized real-field solutions in
flat space under the decay conditions stated below. This includes static clumps;
it does not exclude transient radiating oscillons, gravity, source-supported
walls or additional fields.

Self-gravity is a separate route. A finite-amplitude oscillator calculation
finds effective pressure/energy ratios 0.00251–0.74676 at the earlier required
source densities, far above the cluster velocity-squared scale. This disfavors
treating that excitation as a diffuse pressureless component under the specified
fixed-source averaging. It does not exclude compact relativistic constituents
whose internal gravity is much stronger than the cluster potential.

No new physical constants, occupations or clump masses were fitted. The original
eta and illustrative r=1,s=1/4 remain unselected inputs. A sufficient populated
cluster profile with the galaxy law preserved has **not** been derived.

## 1. Boundary states: existence versus spatial support

Continue 3f3d00e011. Reuse the previously solved sharp planar interface with
conserved Einstein rest density d on the inside and zero outside. The metric
and matter source are fixed. Its background q0(z) defines

    [-partial_z² + V_qq(q0,d)] u = lambda u,
    m_in²=(d-8)/4, m_out²=5.76.

At the minimum and maximum reference gas-shell densities and at d=100, the lowest
finite-domain eigenvalues are positive and below both asymptotic continua:

| d | Lowest eigenvalue | Squared mode norm on inside |
|---|---:|---:|
| 61.9502 | 3.47610 | 0.044571 |
| 100 | 3.50223 | 0.020183 |
| 1741.3366 | 3.52204 | 0.00025061 |

The final entries use L=20 and spacing .01. Changing spacing from .02 to .01
changes the eigenvalue by at most .00370; changing domain L=15 to 20 changes it
by less than 3e-11. This corroborates localized linear states for the fixed-source
planar problem. It is not a full matter/metric stability certificate. Squared
mode norm is not itself an integrated gravitational mass fraction.

Deep inside a homogeneous restored region, any bound mode with lambda<5.76 has

    u ~ exp(-distance/ell),
    ell = (c/omega_unit)/sqrt[(d-8)/4-lambda]
        < (c/omega_unit)/sqrt[(d-31.04)/4].

The inherited frame/mass dictionary gives c/omega_unit=0.0109620 pc. Across the
35 reference shell-average densities, the upper bounds on ell range from
0.0005301 to 0.0039434 pc. In a constant-density extension, even the least
suppressed squared amplitude at 1 kpc is below 10^(-220264) relative to the
asymptotic tail normalization. This logarithm is an analytic exponential
estimate; the computation does not numerically resolve such a tiny amplitude.

For a slowly varying restored region the corresponding expression is an integral
of the local evanescent wave number. We have not reconstructed that continuous
profile from the shell averages. Unresolved low-density corridors, internal
interfaces and moving walls are not excluded by these numbers. The sharp planar
source is a control, not a fitted cluster boundary.

Increasing linear-mode occupation rescales the amplitude but not its penetration
length. Making its tail macroscopically important would first invalidate the
linear background and require nonlinear gravitational/source backreaction. In
a spherical Newtonian source interpretation, an exterior thin shell produces no
interior acceleration; putting all retained mass at the outer boundary therefore
does not reproduce a required enclosed mass throughout the interior. This shell
argument is not a full Palatini lensing or nonspherical-force calculation.

## 2. Exact shape of the bulk potential

At fixed uniform d>=8 define x=sec(q/2), z=x-1>=0 on |q|<pi. Subtract the restored
background energy:

    Vex(q,d)=10x^4-24x²+14+d(x-1)
            =(d-8)z+36z²+40z³+10z^4.

Every coefficient is nonnegative. The field is canonical in the Einstein
variables. The low-amplitude expansion is

    Vex = m² q²/2 + g q^4/4 + O(q^6),
    m²=(d-8)/4, g=(5d+176)/96 > 0.

The quartic coefficient follows by symbolic differentiation of the full
potential. It is not a new adjustable interaction. The intentional sign-flip
mutation fails that derivative check.

A stronger inequality holds throughout the physical branch:

    q Vex_q >= 2 Vex,

with strict inequality for nonzero q. To show it, set t=|q|/2. Then
q z_q=t sec(t) tan(t)>=2[sec(t)-1]=2z. Indeed
h(t)=t tan(t)-2(1-cos(t)) starts at zero; using
t>=sin(t)cos(t) gives h'(t)>=2 sin(t)[sec(t)-1]>=0.
The auxiliary inequality follows because the derivative of
t-sin(t)cos(t) is 2 sin²(t). For the nonnegative polynomial P(z)=Vex,
z P'(z)>=P(z), strictly when z>0 because its quadratic and higher terms
are positive. Combining the two inequalities proves the assertion.

## 3. No isolated exactly periodic scalar clump under fixed-background assumptions

Consider a smooth real solution of

    q_tt - laplacian q + Vex_q=0

in three spatial dimensions, at uniform fixed d>=8 with a flat metric. Assume
it is periodic in time, has finite energy, stays on |q|<pi, and decays sufficiently
rapidly that multiplication by q and the spatial virial integration have no
surface terms. These decay/moment assumptions matter; finite energy alone is
not substituted for all virial regularity requirements.

Write T=average integral(q_t²), G=average integral(|grad q|²),
U=average integral(Vex), J=average integral(q Vex_q). Averaging over one period,
the equation multiplied by q gives T=G+J. The spatial scaling identity gives

    3T/2-G/2-3U=0.

Eliminating T yields

    G + (3/2) average integral[q Vex_q-2Vex] = 0.

Both terms are nonnegative; strict positivity of the nonlinear term away from
q=0 forces the trivial solution. Thus there is no nontrivial exactly periodic
localized solution within these hypotheses. Static solutions are included.
A pulse that radiates away or only approximately repeats does not meet the
hypotheses. Neither does a wall supported by an inhomogeneous source, a
self-gravitating object, a configuration near the broken exterior vacuum, or a
multifield/topologically different construction. This is a scoped analytic
restriction, not a no-go theorem for every cold clump.

## 4. Gravity: first check the controlled small-amplitude regime

If one models the canonical excitation at fixed d as a nonrelativistic envelope,
the quartic interaction gives an effective averaged pressure

    P_eff = [3g/(8m^4 D)] rho_energy²,
    K = 3g c²/(8m^4 D_mass), P_eff=K rho_mass².

For that surrogate with uniform d, the n=1 Newtonian hydrostatic equations give
R=pi sqrt[K/(2pi G)]. This follows by combining dP/dr=-GM(r)rho/r² with
M'=4pi r²rho; the regular density solves the spherical Helmholtz equation and
first reaches zero at that radius. There is no fitted polytropic constant.

At the inherited density values the formal radius is 307–2309 Mpc. Such scales
are outside the local uniform-cluster, static Newtonian approximation; these
are not predictions of actual gigantic stars. They indicate that the repulsive
scale in this simplified closure is not a compact cluster-clump scale.

More importantly, the expansion parameter epsilon=g E/m^4, E=rho_energy/D,
ranges from .00670 to 10.0027 at the 303 previous positive source requirements.
Only one is below the declared diagnostic .1. We therefore do not extrapolate
the quartic hydrostatic model to claim a numerical exclusion of all those states.
The threshold .1 is an approximation diagnostic, not an observational cut.

## 5. Finite-amplitude check, without the quartic truncation

As a follow-up to the expansion failure, solve Vex(q_max,d)=E with the full
potential for every one of the 303 (d,E) benchmarks. Evaluate the homogeneous
oscillator over a full cycle using

    dt = dq/sqrt[2(E-Vex(q))],
    <K> = <E-Vex>, w_eff = [2<K>-E]/E.

Turning points are regularized by q=q_max sin(theta). An independently integrated
virial expression <q Vex_q>/2 agrees with <K> to better than 1.45e-11 fractionally.
The complete results are:

| Quantity | Range |
|---|---:|
| w_eff | .00250693–.74675589 |
| w_eff / (vc²/c²) using earlier speed proxies | 210.75–131842.90 |

This is a dimensionless pressure-scale comparison, not a hydrostatic solution
or a new observed velocity fit. The 303 cases are correlated model/footing/shell
alternatives; some underlying profiles include excluded negative shells.

There is an important stress-tensor distinction. P_eff=<K-Vex> is the canonical
oscillator pressure when the prescribed d A term is treated as a potential.
It is not automatically the full scalar-plus-baryon stress in this scalar-tensor
theory. In a locally homogeneous scalar plus pressureless matter decomposition,
the scalar pressure relative to q=0 is <K-(W/D-2)>D, which exceeds P_eff by
D<d(A-1)>. That positive correction is also recorded. Mechanical support,
source motion, gradients and gravitational backreaction require the full coupled
stress calculation. We do not turn this surrogate into a general relativity
stellar equation of state by assertion.

Under the fixed-source oscillator interpretation, the required excitation is
not a diffuse pressureless fluid that can simply sit in the weak cluster well.
Compact constituents are a different possibility: their internal gravitational
potential could greatly exceed vc² of the host cluster. Neither this pressure
comparison nor the flat-space virial proof rules them out. Their existence,
stability, formation, abundance and forces require a relativistic coupled
boundary-value and evolution calculation, not a freely chosen clump mass.

## 6. Abundance, profile and galaxies remain separate obligations

A boundary eigenfunction has arbitrary linear amplitude. A permitted family
of gravitational clumps would likewise not automatically choose its occupation,
individual masses or cluster radial distribution. Reusing the required inverse
profile to assign those quantities would put the answer in by hand.

In the separate spherical selective-CCT force model, retained enclosed cold mass
still contributes G M_c/r². Keeping the existing galaxy law within allowance
delta requires M_c<=delta [B+sqrt(B²+4AB)]/2, A=a0 r²/G and B=M_b(<r). No numerical
allowance is assigned here. Concentrating a fixed enclosed mass into small clumps
does not generally remove its large-scale gravitational force. The full Palatini
candidate needs its own force and lensing calculation, so this necessary check
in the earlier bookkeeping is not advertised as a completed galaxy test.

## Evidence and continuation

Normal, mutation and finite-amplitude runs have separate manifests and criteria.
The interface background is imported from the previous verified implementation;
that input is hashed along with the scripts and numerical source tables. The
analytical periodic-clump restriction is a self-reviewed proof, not established
by a numerical scan. No external theorem or new empirical dataset is used.

Reproduce from repository root into fresh directories:

    python reviews/cold_bound_states_2026_10_25/check.py --output /tmp/cold-bound-check
    python reviews/cold_bound_states_2026_10_25/eos.py --output /tmp/cold-bound-eos

Surviving routes are nonlinear interface backreaction, internal moving interfaces,
and compact self-gravitating states. They remain open, with explicit missing
steps: solve the coupled configuration and its stability, derive population
from the available energy supply, then calculate the cluster profile and galaxy
forces. The present work narrows those routes; it does not certify a sufficient
retained cold sector or select a0, eta, vacuum energy, or source amplitudes.
