# First-principles reduction of the two-state model

Date: 2026-10-24. Scope: the effective model in `../DERIVATION.md`,
`../field3d_capture/DERIVATION.md`, and `DERIVATION.md` in this directory.
This is an analytic reduction and self-review, not a new simulation or a
derivation of the model from the linked paper. Existing simulation results and
their manifests are unchanged. All conclusions below are conditional on the
explicit assumptions stated; no astrophysical mechanism is established.

## 1. Fix the field function rather than fit it

Assume spherical symmetry, positive unit tether charge per unit T mass, the
existing field-energy ansatz, and a cold static T component with no pressure or
centrifugal support. Let u=G M_T(<r)/r², z=u/a0, and

    U_T = a0²/(4πG) ∫ w(|u|/a0) d³x.

Moving a spherical T shell gives an outward field acceleration a0 w'(z).
The gravitational acceleration is g=g_b+g_F+u. For a pure-T medium, demand
the adopted relation g_b=g²/(g+a0). Then

    u=g-g_b=a0 g/(g+a0),
    g/a0=z/(1-z),
    w'(z)=z/(1-z).

With zero vacuum energy w(0)=0, integration fixes

    w(z)=-log(1-z)-z,       0≤z<1.

Thus the interpolation function, its amplitude relative to unit source charge,
and the coefficients w(z)=Σ_{n≥2} z^n/n are not independent tuning knobs within
this ansatz. Introducing a new coefficient changes the prescribed relation or
the charge convention. This does NOT derive a0 or choose a unique 3D extension.
The spherical target relation itself is an input, not a first-principles law.

Since w'(z)≥0 and w''(z)=1/(1-z)²>0, the radial vector energy is convex
(radial Hessian eigenvalue w'', transverse eigenvalue w'/z=1/(1-z)).
It is nonnegative and vanishes only at zero field. This proves positivity of
the added field energy, not stability of self-gravitating matter as a whole.
At fixed positions and gravitational masses all-F has U_T=0 and minimizes
this contribution. It does not prove every individual removal lowers energy:
different source vectors can cancel locally. No pointwise monotonicity of
multi-source charging work is assumed.

## 2. Tie collision strength to compactness across all systems

Use baryonic mass M and length b as units, with

    v0=√(GM/b), t0=√(b³/(GM)),
    κ=a0 b²/(GM), c=C M/b².

C is the existing constant normal-flux coefficient, with units area/mass.
Exactly, for one universal C and a0,

    κ c = χ,       χ=C a0/G,       c=χ/κ.

Consequently κ and c cannot be independently chosen for each galaxy. At fixed
M,b and globally fixed a0, only the single universal χ sets this rate
normalization. This identity removes redundant scan axes, but does not reduce
an already universal C by another degree of freedom.

If G and a0 are the ONLY dimensional constants allowed in a constant C,
dimensional analysis gives C=χ G/a0: solving the mass and time exponents yields
G¹ a0⁻¹. Nothing fixes χ=1. A velocity-dependent cross section or microscopic
mass, mediator scale, ℏ, or c_light would introduce further dimensionless
ratios. Those possibilities cannot be excluded by dimensional analysis.

The reservoir ratio η=M_medium/M_b, presently 5.364, is a dimensionless
abundance/initial-condition input. Neither this scaling nor energy conservation
derives it. Initial angular momentum and phase-space distributions also remain
physical initial conditions; they must not be fit as hidden object labels.

## 3. Energy conservation removes a reaction-output degree of freedom

At fixed positions let Δ be the full finite change in U_T, and K_n=μv_n²/2
the incoming normal relative kinetic energy. For a nonnegative receiver energy R,

    K_n' = K_n-Δ-R ≥ 0,
    0 ≤ R ≤ K_n-Δ.

An admissible reaction requires K_n≥Δ (and K_n≥0). For an endothermic
conversion, outgoing speed, radiation, and threshold cannot be set independently.
Once Δ and R are specified, |v_n'|=√[2(K_n-Δ-R)/μ]. The existing choice
R=(1-e²)(K_n-Δ), 0≤e≤1, is one permissible family; e=.3 is not derived.
The baryon cooling restitution .5 is another independent closure choice.

The receiver can absorb released kinetic energy but cannot supply missing
charging work. Conservative live gravity can release energy through motion;
therefore the fixed-position all-F energy minimum is not a theorem forbidding
assembly. Nor may we infer a global capture-fraction bound without bounding
gravitational contraction and the changing field geometry.

Microscopic reversibility would relate a radiative forward channel to its
inverse absorption channel with phase-space factors and a specified radiation
state. Conservation alone does not determine those rates or an equilibrium
T/F ratio. The current radiation sink with no absorption is an open closure;
we must not eliminate its free parameters by invoking equilibrium detailed
balance that the implemented model does not possess.

## 4. Eliminate direct rotation gates from a point-local collision law

Consider a Galilean-invariant, isotropic, point-local binary collision operator
depending only on the two local velocity distributions and internal states.
A common boost v→v+V leaves relative velocities unchanged. It therefore leaves
all scalar conversion rates unchanged. At one point a common rigid flow
v(x)=Ω×x is just such a boost. Two systems with identical local relative
distributions, densities, and states cannot acquire different rates solely
because their common mean flow has different global circulation.

At finite separation, the rigid-flow contribution is

    (v_j-v_i)·(x_j-x_i) = (Ω×d)·d = 0.

This also explains the existing central-normal rigid-rotation null test.
It does NOT imply that disks and dwarfs have the same distributions: transport,
cooling, relative streaming, and gravity can produce real differences.

Any direct rotation sensitivity requires additional inputs (gradients, finite
interaction range, spin, anisotropic states, or memory) and their consistent
energy dynamics. A fitted Ω threshold is not supplied by the present operator.
For a smooth cold common flow, the leading finite-separation normal velocity
is nᵀ(∇v)n |d|; only the symmetric strain contributes. Finite-cell compression
events can therefore be numerical error rather than physical local capture,
as already measured in `run_flow`.

## 5. Enforce the existing free-mass constraint before fitting capture

This restates the parent derivation as a parameter filter. Under the same cold
spherical equilibrium assumptions, set S=g_b+g_F. Force balance gives
S=g²/(g+a0), hence g=law(S). Let g0=law(g_b), x=g0/a0>0, and t=10^δ≥1,
where δ is an allowed positive logarithmic residual. Since S(g) is strictly
increasing for g>0, g≤t g0 holds exactly when

    0 ≤ g_F/g_b ≤ t² (x+1)/(t x+1) - 1.

For δ>0 the right side decreases with x because its derivative is
t²(1-t)/(t x+1)². The deep-acceleration limit is t²-1; the high-acceleration
limit is t-1. At δ=0 no positive g_F is allowed in this equilibrium branch.
For the illustrative δ=.05 dex, these limits are approximately 26% and 12%.
The tolerance is a design choice here, not an observational confidence bound.

This is a constraint on enclosed free mass relative to enclosed baryonic mass
in spherical symmetry, not a global free fraction or a general disk theorem.
Non-equilibrium, pressure, geometry, and finite observational apertures matter.
Keeping a large total free reservoir at large radii may evade the inner bound;
leaving that reservoir co-spatial with baryons generally does not.

## 6. Remove numerical charging scales from the physical parameter list

For an isolated Gaussian packet of mass m and fixed smoothing σ, the weak-field
quadratic energy is U_self=Gm²/(2√π σ). Thus U_self/m=Gm/(2√π σ)→0 as
m→0 at fixed σ. More generally the expansion is controlled by Gm/(a0σ²);
the isolated nonlinear terms also vanish faster than m in this limit.

With fixed macro mass ratio and relative speed, K_n scales as m, so the
isolated self-charging threshold relative to K_n scales as m/σ. It cannot
be identified with a resolution-independent microscopic binding energy.
This statement is for first isolated capture; in an existing background,
cross-field charging work can remain linear in m and survive the limit.

Consequences: sample number, cell width, time step, field box, quadrature, and
gravitational softening are convergence controls, not physical fit parameters.
The present σ=b is a numerical/modeling regulator with unresolved continuum
behavior. If σ is promoted to physical structure, a universal physical rule
and its energy must be derived; choosing it by object is not a reduction.
Likewise a failed opacity-resolution screen excludes a simulation from evidence,
not the corresponding physical cross section from nature.

## Reduced parameter map and next discriminating work

| Quantity | Treatment from these restrictions |
|---|---|
| w and its series coefficients | Fixed by the adopted spherical law within the stated ansatz |
| a0 | Universal input; not derived here |
| Constant collision strength | One universal χ; c=χ/κ in every system |
| Radiation/output speed | One choice fixes the other through the event energy equation |
| Direct global rotation/type thresholds | Absent from the point-local symmetry-respecting operator |
| Abundance η, initial distributions | Physical inputs requiring independent justification |
| Restitutions, species masses, inverse channels | Still unclosed microphysics; conservation does not determine them |
| Resolution and smoothing controls | Must pass convergence; cannot be fitted to select populations |
| Three-dimensional field extension | Structural assumption still open despite fixed spherical w |

There is no justified claim that the complete model now has only one parameter.
The constant rate sector has one universal normalization; the physical model
still contains unspecified functions and structural choices.

The next useful mechanism test is whether a specified microscopic channel gives
a finite, resolution-independent formation work and forward/inverse rates.
It must recover the adopted field law, account for its energy receiver, obey
the local symmetry restriction, and leave sufficiently little inner free mass
where the acceleration relation is required. Until then, varying restitution,
packet self-energy, and a rotation gate together would obscure the missing
physics. A higher-rate numerical run alone cannot supply it.

## Self-review and evidence limits

Primary verdict: **conditional on the stated effective-model assumptions**.
No independent review was performed. The algebra above is the load-bearing
evidence; no new numerical experiment or literature claim is used.

| Obligation | Status and dependency |
|---|---|
| Field-function reconstruction | Passed algebraically under cold spherical equilibrium and unit charge |
| Positivity/convexity | Passed on 0≤z<1; whole-system stability not addressed |
| Dimensionless rate identity | Passed by substitution and units; constant universal C assumed |
| Event energy interval | Passed from K_n'≥0 and R≥0; no microscopic rate derived |
| Rotation restriction | Passed for point-local Galilean-invariant kernels; gradients excluded by hypothesis |
| RAR free-mass filter | Passed by monotone inversion; general nonspherical application not addressed |
| Packet threshold scaling | Passed for isolated Gaussian, fixed σ and weak-field limit |
| Galaxy population separation | Incomplete: no derived microphysical channel or converged formation demonstration |

The field-function and free-mass arguments consolidate existing project
derivations; the cross-system rate identity and explicit symmetry/granularity
filters make the allowed future search smaller. Historical simulation files
remain unchanged so their provenance is preserved.
