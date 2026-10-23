# An anisotropy-independent occupation bound on finite equilibrium formation

Combining phase-space packing with the global virial identity gives a necessary condition for any finite stationary identified-medium profile. It applies to anisotropic velocity distributions and does not use the local-wave approximation. The coldest tested density requires a maximum phase-space occupation at least about33 times that of the warmest tested equilibrium. Thus collisionless rearrangement of that particular warm example cannot reach that cold density as a stationary finite state, even by choosing a different anisotropy.

This is a conditional formation obstruction for specified initial occupation, not an exclusion of the theory or all primordial distributions. No primordial fine-grained occupation has been supplied.

## Local packing inequality

Let0<=f(x,v)<=fmax and rho(x)=integral f dv. At fixed rho, the smallest total velocity second moment is obtained by filling a velocity ball at fmax, with radius

    vF=[3rho/(4pi fmax)]^(1/3).

This is a classical rearrangement argument, not a fermion/Pauli assumption. To prove it, compare f with the filled ball f_ball. The product (v²-vF²)(f-f_ball) is nonnegative inside and outside the ball, and the density difference integrates to zero. Hence

    integral v² f dv >= (3/5)[3/(4pi fmax)]^(2/3) rho^(5/3).

Streaming and anisotropy cannot lower the total second moment below this bound. Applying it at each position gives

    2T >= c0 fmax^(-2/3) integral rho^(5/3) dV,
    c0=(3/5)[3/(4pi)]^(2/3).

Equality requires the filled velocity ball locally. Most of the constructed equilibria do not saturate it.

## Global force balance

For a stationary finite spherical distribution, with vanishing virial surface term, the identified-medium force is

    a_r=-gNb+R(q)-gamma rho'.

The anisotropic Jeans equation, integrated against radius, gives

    2T=integral rho r[gNb-R(q)+gamma rho'] dV.

Integrating the stiffness term by parts yields

    2T+(3gamma/2) integral rho² dV
       =integral rho r[gNb-R(q)] dV.

No isotropic-pressure closure was used. Finite-boundary surface terms must vanish. In particular this identity cannot be applied after discarding the nonzero surface stress of ANISOTROPIC_RESULT.md's infinite streaming equilibrium.

Define the profile-dependent quantity

    Vkin[rho]=integral rho r[gNb-R(q)] dV
              -(3gamma/2) integral rho² dV.

A nonzero finite stationary distribution must have Vkin>0 and satisfy

    fmax >= [c0 integral rho^(5/3) dV / Vkin]^(3/2).

This is a necessary occupation threshold determined by the proposed density and its native force, independent of the detailed velocity distribution. It is not sufficient for a positive stationary distribution, stability or reachability; the other conserved phase-space quantities may impose further restrictions.

A perfectly cold minimum has Vkin=0. With nonzero density it cannot be realized by a bounded fmax. This makes the singular nature of the cold limit explicit rather than treating it as an ordinary cooling endpoint.

## Test on the four fixed-mass profiles

Reintegrate the accepted COLD_LIMIT_RESULT.md profiles, with gamma0.01, ra1 and mass1. Use rho_hat=integral f dv, so F=A/(16sqrt(2)pi/15) for f=F Q_+. All spatial integrals omit a common4pi; it cancels from the inequalities and thresholds.

| A | computed fmax | 2T | packing lower bound on2T | minimum fmax required by this density |
|---|---:|---:|---:|---:|
| 10 | 1.22423 | 0.198564 | 0.111596 | 0.515799 |
| 100 | 5.49619 | 0.0987530 | 0.0564346 | 2.37440 |
| 1000 | 23.4185 | 0.0426599 | 0.0240788 | 9.93076 |
| 10000 | 96.9965 | 0.0175934 | 0.00980061 | 40.3282 |

The actual kinetic energies are1.75–1.80 times the minimum bound at their own fmax. All obey the inequality. Direct kinetic and force virials agree to approximately2e-13 relative on the refined grid; this is numerical consistency, not an exact error certificate for the continuum solutions.

The important cross-profile comparison is40.3282/1.22423=32.94. A collisionless initial distribution whose true fmax is that of the first profile cannot form the last density as a finite stationary state under the same force model. The conclusion is stronger than merely observing that the last chosen f(Q) has a higher peak: it also excludes alternative anisotropies with the same target density and the lower occupation ceiling. Finite sampling/numerical equilibrium error is far smaller than the factor33 gap in these tests, though no interval-arithmetic certification was performed.

The bound applies to the full closed collisionless system's initial maximum, not just an arbitrarily selected subsystem. A surrounding reservoir with higher occupation would change the relevant initial ceiling and must be included. Particle escape does not increase the fine-grained ceiling of the particles that remain. Time-dependent Hamiltonian baryonic forcing also preserves the fine-grained values of f, although it changes energy and can alter which final stationary profile is relevant.

## What information is actually needed next

The repository's quoted velocity dispersion and mean density alone do not determine an upper bound on fine-grained f. A smooth Maxwellian would specify one, but narrow unresolved streams can have a much larger maximum while sharing the same low moments. It would therefore be invalid to substitute rho/sigma³ as a primordial upper ceiling without a justified distribution model.

A formation proposal needs either an initial fine-grained distribution with adequate occupation and appropriate conserved invariants, or a specified non-Hamiltonian/collision/conversion process with a complete energy and mass budget. Coarse-grained phase mixing by itself does not justify creating the larger occupation. This condition can screen candidate formation mechanisms before expensive simulations.

## Current repository audit update

The concurrent E1_input_audit/README.md (commit77a8b2d4a6) reports that the earlier D7c combined Cassini/SPARC no-go changes to UNDECIDED under a framework-native single footing: some beta-family members pass its primary statistic while the secondary statistic remains unfavorable. Its audit also reports sensitivity of Lstar and retained-fraction statements and flags a native-background H0 tension. Those are that lane's reported results, inspected but not independently reproduced here.

Accordingly, earlier checkpoints in this directory that called the D7c verdict an unresolved no-go should be read with this newer qualification. The screened theory is neither certified nor ruled out by that old two-footing gate. None of those observational reclassifications changes the analytic packing or virial derivation here, which uses no calibrated halo or standard-MOND data machinery.

## Evidence

phase_packing_run/manifest.json validates;5 checks pass: filled-ball coefficient, reproduced finite mass, global virial, occupation inequality and12k/36k-point quadrature refinement. The original equilibrium scripts and manifests remain unchanged. No new mutation or live evolution was performed. Algebra and interpretation are self-reviewed. The packing principle is established classical kinetic reasoning, not a novelty claim; the native-force virial combination supplies a model-specific necessary condition.
