# Phase-level mixing: a conditional exponent and an unselected amplitude

The strongest result in this lane is a constructive conditional calculation:
three-dimensional, dilute mixing with phase-level volume proportional to
`1/eta` produces an intermediate `v^-5` tail. Its normalization is

    A_tail = 2 K / [3 ln(eta_max/eta_min)],

where K is kinetic energy density in the homogeneous case. This is not a
selection of the phase-level distribution, the energy reservoir, the cutoff
ratio, or an entire halo pressure law. The exact finite-interval mixture is
regular at small velocity and eventually has an exponential cutoff. A tail
alone does not determine the core distribution. No general obstruction to a
finite, exactly logarithmic inner equilibrium is claimed; the parallel compact
kinetic construction supplies one.

## 1. What entropy maximization actually fixes

Let p(x,v,eta) be the probability density of finding fine-grained phase level
eta in a coarse phase cell. Include a discrete vacuum state. The constraints
are local normalization, total energy, and all phase-level volumes
`gamma(eta)=integral p dx dv`. Mass is their first moment. Maximizing

    S = -integral p ln p dx dv deta

at those constraints gives

    p = g(eta) exp[-beta eta E] / Z(E),
    Z(E) = 1 + integral g(eta) exp[-beta eta E] deta,
    f(E) = integral eta g(eta) exp[-beta eta E] deta / Z(E).

The Euler-Lagrange calculation fixes the exponential structure. It does not
fix the function g: g is a multiplier function for the initial phase-level
volumes. A vacuum plus one nonzero level eta0 gives

    f(E) = eta0 b exp[-beta eta0 E] / (1+b exp[-beta eta0 E]),

whose high-energy tail is exponential. Folding or producing many streams does
not change those exact fine-grained level volumes. This is a direct
counterexample to universal logotropic selection by strict mixing entropy.
Perfectly cold delta-function sheets require a finite phase-density
regularization before this entropy problem is even defined; stream number
alone supplies neither its phase levels nor its cutoff.

A power-law fugacity illustrates what an extra assumption accomplishes. For
`g(eta)=g0 eta^(s-1) exp(-b eta)`, dilute occupancy gives

    f(E) = g0 Gamma(s+1)/(b+beta E)^(s+1).

The exponent is 5/2 only for s=3/2. Both g0 and beta remain state-dependent.
This elementary Laplace-transform calculation does not select s.

## 2. Derive the tail and its full kinetic-energy normalization

Now impose the narrower, testable premise that a spatially homogeneous mixture
has phase-level volume per spatial volume

    gamma(eta)=C_eta/eta,  eta_min <= eta <= eta_max.

Set particle mass to one and E=v^2/2. In the dilute limit, each level is a
Maxwellian with inverse velocity variance beta eta. Enforcing its phase volume
determines its fugacity:

    g(eta) = gamma(eta) [beta eta/(2pi)]^(3/2),
    f(v) = C_eta [beta/(2pi)]^(3/2)
           integral_eta_min^eta_max eta^(3/2) exp(-beta eta v^2/2) deta.

Changing variable to t=beta eta v^2/2 gives, in the intermediate band
`beta eta_max v^2/2 >> 1 >> beta eta_min v^2/2`,

    f(v) ~ 3 C_eta/(2pi beta) v^-5.

The finite mixture has exact moments, including both crossover regions:

    rho = integral eta gamma(eta) deta
        = C_eta (eta_max-eta_min),
    K = integral (3/(2 beta eta)) eta gamma(eta) deta
      = 3 C_eta/(2 beta) ln R,     R=eta_max/eta_min.

Thus the logarithm in the energy relation is not obtained by arbitrarily
integrating only an approximate tail. Every logarithmic phase-level interval
contributes the same kinetic energy. If an energy-only marginal continuation
`f(E)=B(E-E0)^(-5/2)` applies in the region of interest, its velocity coefficient
is `C_v=4 sqrt(2) B`; independent velocity integration gives

    A_tail = 8 sqrt(2) pi B/3 = 2pi C_v/3
           = C_eta/beta = 2K/(3 ln R).

The final step relates a tail amplitude to a possible logarithmic equilibrium
gradient. It is not a proof that the finite mixture has that EOS everywhere.

The bounded run used C_eta=eta_max=1, eta_min=1e-12 and three beta values.
Independent log-velocity moment quadrature and log-phase-level quadrature agree
with these formulas to better than 3e-14 relative in the recorded cases.
The same exponent occurs with A=200,100,50: the coefficient changes continuously
with the energy multiplier. The largest nonvacuum partition integral is
1.19725e-4, so retaining the full exclusion denominator at the same fugacity
changes f by at most that relative amount. Enforcing exactly the same phase
volumes in the full excluded problem would also require adjusting g; the
experiment checks the controlled dilute limit, not that nonlinear inversion.

## 3. Initial Gaussian data and an inhomogeneous halo

An elementary level-set calculation for an initial isotropic Gaussian
`f0(v)=eta_max exp[-v^2/(2 sigma0^2)]` gives

    gamma0(eta)=4pi sqrt(2) sigma0^3
                sqrt[ln(eta_max/eta)]/eta.

The logarithmic factor is real. Substitution into the mixture integral gives
`f ~ v^-5 sqrt[ln(beta eta_max v^2/2)]`, up to lower logarithmic corrections.
Its effective velocity slope is -4.73970 at dimensionless energy 100 and
-4.94352 at 1e8 in the recorded calculation. Gaussian initial levels therefore
motivate a marginal exponent asymptotically, not an exact, constant-amplitude
power law. More generally `exp[-(v/v0)^p]` yields a logarithmic exponent
`3/p-1` in gamma; p=3 removes that correction, but p is not selected here.
Extending the Gaussian level distribution to eta=0 makes `integral gamma deta`
diverge, so its fully dilute mixture has infinite kinetic energy. The recorded
Gaussian calculation is an asymptotic shape diagnostic. A finite-energy model
needs a low-level cutoff or a change of regime; it cannot use this formal tail
to eliminate that missing physical input.

For a finite inhomogeneous domain define

    Z_x(eta)=integral_V exp[-beta eta Phi(x)] dx.

The dilute fugacity is instead
`g=gamma_total(eta)[beta eta/(2pi)]^(3/2)/Z_x(eta)`. Local moments acquire
spatial weights `exp[-beta eta Phi]/Z_x`. The global kinetic identity remains
exact in this dilute model:

    K_total = 3/(2beta) integral gamma_total(eta) deta.

If gamma_total=C_total/eta, the potential is bounded on a finite volume V,
and the relevant phase levels satisfy `beta eta DeltaPhi << 1`, then
`Z_x -> V`. The asymptotic coefficient is consequently
`A_tail=C_total/(beta V)=2(K_total/V)/(3 ln R)`. A local halo coefficient does
not follow without these domain, energy and accessible-level conditions.
An isolated infinite spatial domain cannot simply replace Z_x by a finite V.

## 4. The close cosmological number is conditional and has a range problem

Imposing both `K=rho_Lambda c^2` and
`R= rho_Planck/rho_Lambda` gives

    A_tail/(rho_Lambda c^2) = 0.00235494071558,

using the supplied inverse logarithm 0.00353241107337. This is 1.09393 percent
above the canonical 0.0023294580123, or 0.545479 percent above its uncut core
column. These substitutions were not outputs of entropy maximization.
Phase density eta has units mass/(volume times velocity cubed); a density
ratio is not a phase-density ratio unless an additional velocity-volume
relation is specified. Positive peculiar kinetic energy also has a different
stress from vacuum energy, and no transfer law equating them was derived.

There is a further consistency test specific to this Newtonian mixture.
Its total one-dimensional variance and hottest component variance obey

    sigma_1D^2 = ln R/[beta(eta_max-eta_min)],
    sigma_hot^2/sigma_1D^2 = (R-1)/ln R.

The proposed cosmological ratio has ln R=283.09276, or 122.9456 decades. With
`d=rho/rho_Lambda` and the proposed K, the condition sigma_hot<c requires
`d>2(R-1)/(3 ln R)=2.07780e120`. More directly, the fraction of the formal
Newtonian kinetic energy below c is

    F_<c = (1/ln R) integral_ln(q/R)^ln(q) P(5/2,exp x) dx,
    q=3 d ln R/[4(1-1/R)],

where P is the regularized incomplete gamma function. For illustrative d
of 1e3,1e6,1e9 this fraction is .0408442,.0652452,.0896462 respectively.
These are hypothetical density contrasts, not fitted observational inputs.
Thus more than 91 percent of the energy in those formal distributions lies
at v>c, outside the approximation used to obtain the numerical coincidence.
This is a failure of that specific pair of identifications within this
Newtonian mixing model. A relativistic or truncated completion must redo
both the density of states and the energy normalization. It is not a general
no-go theorem for finite logarithmic cores.

## 5. What a cosmological spectrum would add

For linear growing-mode Gaussian perturbations, the continuity equation gives
`v_k=i a H f_g k delta_k/k^2`. With a smoothing window W(kR_s), one component
has variance

    <v_i^2> = (a H f_g)^2/(6pi^2) integral P_delta(k) W(kR_s)^2 dk.

This follows directly by the angular average k_i^2/k^2=1/3. A fixed spectrum
can break the simple scale freedom of isolated dynamics, but now supplies
ensemble energy, epoch and smoothing-scale inputs. Multiplying its amplitude
by q multiplies this variance and the linear kinetic energy by q. The
conditional mixing coefficient scales with it if ln R is fixed. A power
spectrum alone does not determine phase-level volumes, phases, environmental
selection, or a late nonlinear energy-transfer fraction. To turn this into a
prediction one must derive a joint late-time attractor for K, R, and the
finite spatial/escape boundary from the specified initial ensemble.

## 6. Cold gravity does not inherit the plasma diffusion argument automatically

Directly integrating the cold linear susceptibility for f= rho delta(v)
gives, with Newtonian Fourier potential
`uhat=-4piG/[(2pi)^3 k^2]`,

    epsilon(k,omega)=1+omega_J^2/omega^2,  omega_J^2=4piG rho.

The zeros at omega=+/-i omega_J are poles of the response 1/epsilon. One is
growing. Evaluating only the real-frequency denominator formally gives
`|epsilon|^-2 ~ omega^4/omega_J^4`, hence a candidate v^4 diffusion scaling,
but discards the growing Jeans transient. It is not a stationary late-time
diffusion coefficient about a stable cold homogeneous gravitational state.
An expanding, warm, or bound inhomogeneous system must establish its own
response and temporal hierarchy. This argument leaves gravitational diffusion
open in those different regimes; it blocks this particular transfer of the
cold homogeneous plasma derivation.

## Evidence and bounded interpretation

`run/manifest.json` and `run_range/manifest.json` both have status completed
and passed current-input hash validation. Scripts, contracts and results are
contained in this directory. No simulation or observed halo fitting was run.
The literature version audit is in SOURCES.md, and the independent algebraic
review of the coordinator's finite-tail construction is in FINITE_TAIL_REVIEW.md.
OUTPUT_HASHES.txt pins this lane's final artifacts and audited local inputs.

The next necessary mechanism is specific: produce an evolution law for the
coarse phase-level content, with an explicit energy reservoir and physical
cutoffs, which selects both its near-1/eta sector and K/ln R. Strict Vlasov
mixing leaves the fine-grained level content fixed; postulating repeated
coarse-graining or a phase-volume cascade adds a dynamical hypothesis that
must include its resolution and dissipation scale. The computation supplies
a normalization target for such a mechanism, not that mechanism itself.
