# Dilute gravitational clumps with the vacuum retained

## Outcome and scope

The true broken-vacuum branch has an attractive leading interaction after the
cubic term is properly included. That opens a gravitational-clump question which
the previous restored-phase repulsion test did not answer.

However, the resulting **dilute Gaussian variational branch is not compact**.
Its formal attraction-limited mass is 0.1193 solar masses and its smallest
zero-vacuum stable-branch radius is 6.871 billion parsecs. The same positive
vacuum already in the action prevents a stable radial minimum in this model.
The calculation therefore supplies no viable population of compact objects.
These are diagnostics of an inconsistent proposed branch, not predictions of
physical horizon-sized stars.

This is a test of a specified nonrelativistic variational route, not a solution
of the full relativistic real-scalar field equations. Dense relativistic branches,
non-Gaussian solutions, time-dependent formation and complete perturbative
stability remain uncomputed. No adequate abundance, cluster profile or galaxy-law
preservation has been established. The original eta and illustrative action
coefficients remain inputs, not microscopic predictions.

## 1. Do not count the scalar as external matter

Continue 5d3367ed36. The d in V=W+d A is externally supplied baryonic rest density.
A proposed scalar clump's own energy must gravitate through the metric; inserting
it again into d would change the model and double count its effect.

An isolated dilute clump in the broken vacuum therefore uses d=0. With canonical
q=chi/v, subtract the constant vacuum potential but retain it in gravity:

    U(q)/D = W(q)/D-1.6 = 10[sec²(q/2)-6/5]²,
    q0=2 asin(1/sqrt(6)).

This potential has minima at +/-q0 and a barrier of .4 D at q=0. The calculation
here concerns small oscillations around +q0, not excursions across that barrier.
Set h=q-q0 and write the local equation

    h''+m² h+a h²+b h³+...=0.

Direct derivatives give

    m²=144/25=5.76,
    a=864 sqrt(5)/125=15.45570186,
    b=96/5=19.2.

Although b is positive, the cubic interaction changes the leading amplitude
frequency shift. Expanding a periodic solution through second order removes
its mean displacement and second harmonic, giving

    omega(A)=m+[3b/(8m)-5a²/(12m³)] A²+O(A³),
    g_eff=b-10a²/(9m²)=-672/25=-26.88.

Thus the nonrelativistic envelope interaction is attractive. Ignoring the cubic
term would give the wrong sign. Independent full-potential oscillator averages
at E/D=1e-4,3e-5,1e-5 verify

    P/rho_energy ≈ [3 g_eff/(8m^4)] E/D,
    3 g_eff/(8m^4)=-0.3038194444,

with fractional deviations 1.13e-4, 3.97e-5 and 7.32e-6 respectively. The deliberate
mutation deleting the cubic correction fails this check. Unlike the previous
fixed-source oscillator pressure, this vacuum calculation has no d A matter
interaction term to misidentify as scalar pressure.

The envelope uses an approximately conserved occupation over appropriate
nonrelativistic times. The real scalar has no exact U(1) particle-number symmetry;
number-changing radiation and long-term lifetimes require further analysis.

## 2. Gravitational energy without an adjustable self-coupling

Use Einstein-frame eta_E=eta_J sqrt(5/6)=1369.3064 pc km/s. The inherited vacuum
normalization gives

    D_mass=.75 × 3 H_J²/(8pi G), H_J=1.8e-18/s,
    H_E=H_J/sqrt(5/6),
    K=3 g_eff c²/(8m^4 D_mass)=-6.2831153e42 (SI),
    P=K rho_mass².

The excitation density is distinct from the background vacuum density 1.6 D_mass;
indeed 8pi G(1.6 D_mass)/3=H_E². Thus the mass and cosmological terms use the same
vacuum normalization.

For the explicitly chosen normalized Gaussian envelope

    rho(r)=M exp(-r²/R²)/(pi^(3/2) R³),

the nonrelativistic energy is

    E/M = A/R² - b_G G M/R + C_G K M/R³,
    A=3 eta_E²/4, b_G=1/sqrt(2pi), C_G=(2pi)^(-3/2).

The three terms are gradient energy, Newtonian self-gravity, and the integrated
quartic interaction energy. Gaussian integrals fix their coefficients. R and M
are variational/state variables, not new action constants. Choosing this shape
restricts the test: a radial minimum does not certify stability against all
perturbations, and its absence is not an exact theorem for arbitrary profiles.

For K<0, stationary radii obey

    b_G G M R²-2 A R+3 C_G |K| M=0.

There are two extrema below

    Mcrit=A/sqrt(3 b_G C_G G |K|),
    Rcrit=A/(b_G G Mcrit).

The larger-radius extremum is a radial minimum within the ansatz; the smaller
is a maximum. They merge marginally at Mcrit. The stable branch has R>=Rcrit.
The numerical values are

| Formal zero-vacuum variational quantity | Value |
|---|---:|
| Mcrit | 0.1192816 solar masses |
| Rcrit | 6.8707603e9 pc |
| Central excitation density / D_mass at critical point | 1.02854e-24 |
| Dynamical time sqrt(Rcrit³/(G Mcrit)) | 2.45856e22 years |
| H_E times that dynamical time | 1.52984e12 |

The small-amplitude expansion is well controlled at this formal critical point,
but treating such a low-density, huge object as isolated from vacuum gravity is
not. The bottleneck is not merely the sign or size of a chosen self-coupling.

## 3. Keep the positive vacuum in the binding calculation

The local weak-field vacuum potential is Phi_vac=-H_E² r²/2. Its Gaussian average
adds -3 H_E² R²/4 to E/M. Define x=R/Rcrit, mu=M/Mcrit, and

    zeta=3 H_E² Rcrit^4/(4 A).

In units A/Rcrit² the variational energy becomes

    e(x)=x^(-2)-mu/x-mu/(3x³)-zeta x².

At a stationary point,

    mu=2x(1+zeta x^4)/(1+x²),
    e''=2[x²-1-zeta x^4(3x²+5)]/[x^4(1+x²)].

A positive-curvature radial minimum requires x>1 and

    zeta < (x²-1)/[x^4(3x²+5)] <= 3/125=.024.

The last bound follows by maximizing (y-1)/[y²(3y+5)] for y=x²>1; its unique
maximum is at y=5/3. The action's numbers give zeta=4.39992e24. There is therefore
no radial minimum in this variational model with the positive vacuum included.
This is an analytic statement about the model, not a finite mass scan.

For context the critical mass's vacuum turnaround scale (G Mcrit/H_E²)^(1/3)
is only 51.75 pc, while c/H_E is 4.9273e9 pc. The formal Rcrit exceeds even that
horizon scale. The Newtonian calculation is not valid as a physical description
of an object beyond the horizon. Its legitimate use is to reject the proposed
compact dilute branch: positive-curvature extrema already require R>Rcrit, so
none lie in the intended compact local domain. The enormous-radius extrapolation
must not be called a relativistic star solution or a predicted formation time
for an existing object.

A live cluster environment changes the problem again. Its baryonic d can restore
the q=0 phase and remove the vacuum-branch attraction. The preceding restored
calculation found positive quartic response. A putative vacuum clump cannot be
moved into a cluster while keeping its isolated-vacuum equilibrium and ignoring
that environmental change. This calculation does not solve a screened interface
around a compact object in cluster matter.

## 4. Formation and abundance are not selected by an equilibrium family

Even if the formal dilute branch were viable, Mcrit would be a branch endpoint,
not a selected mass for every object. The Gaussian energy has a family of states
indexed by the supplied approximate envelope mass. It contains no production
law selecting that mass or the number of objects. At the formal critical point,
the dynamical time exceeds H_E^-1 by 1.53e12, so this route does not supply a
rapid compact-formation mechanism in its own domain assumptions.

Dividing the 70 earlier inverse cluster mass requirements by Mcrit gives
5.76e14–3.32e15 hypothetical objects per cluster if all were at that endpoint.
These are arithmetic budgets, not an abundance prediction, observed counts,
or evidence that the inconsistent branch exists. The underlying alternatives
include profiles with negative shells and are not independent observations.

The earlier merger calculations established finite source-energy transfer, not
an adequate cold reservoir or a compact-object production channel. No conserved
energy budget, fragmentation calculation or radiation-loss history in this work
turns that result into these object counts. Assigning them from the required
cluster profile would fit a missing population rather than derive it.

## 5. Cluster profile and galaxy law

For a sufficiently dilute population of compact objects with approximately
constant mass m_cl, the coarse mass profile would require

    M_c(<r)=m_cl N(<r).

Neither a mass-radius relation nor radial stability determines N(<r). One must
predict the phase-space population, formation sites, transport and survival.
Clumping also does not remove the large-scale gravity of the enclosed mass.
In the earlier spherical selective-CCT bookkeeping, the existing galaxy
constraint M_c<=delta [B+sqrt(B²+4AB)]/2 still applies, with A=a0 r²/G and
B=M_b(<r). No arbitrary delta or galaxy/cluster occupation threshold is inserted.
The Palatini candidate requires a separate coupled force and lensing calculation;
that galaxy test has not been completed.

## What remains open

The result rules against the specified dilute Gaussian weak-gravity route. It
does not exclude dense relativistic real-field configurations, non-Gaussian
branches, source-supported states, or transients. Existence and stability of a
dense branch require the full Einstein-scalar-matter system with appropriate
vacuum asymptotics. A static real-scalar ansatz or a complex boson-star model
cannot silently replace the original oscillating real field. Formation,
lifetime, environmental survival, population and galaxy forces remain separate
obligations even if a dense branch is found.

## Reproduction and evidence

check.py, FROZEN_CRITERIA.md and contract.json record the finite and symbolic
checks. The normal manifest has completed status; the mutation has the expected
failed status from the full-potential oscillator comparison. Computation and
proof review are self-review, not independent certification. No external
stellar-mass limit or new observational dataset is used.

Run from repository root in a fresh directory:

    python reviews/cold_gravitating_clumps_2026_10_25/check.py --output /tmp/cold-gravity-check

The oscillator check verifies the leading attractive coefficient; it does not
validate the nonrelativistic approximation for dense relativistic stars. The
Gaussian Hessian is exact for its displayed energy functional; that functional
is a restricted approximation, not the full field equations.
