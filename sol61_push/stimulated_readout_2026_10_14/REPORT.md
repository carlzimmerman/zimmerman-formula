# Single-pump optical readout is too weak at the current benchmark

Parent checkpoint: 56ba3eee5dbb8172d3cf63245b619b7d2f47c2f8.
An idealized conversion of one stored pair into a photon in an empty output
mode is extremely inefficient with the current couplings. For a 1 m effective
traveling mode and 628 W pump, the optimized capture probability is at most
1.612e-8, even before phase noise, extra photon loss or detector inefficiency.
This is a scoped obstruction to this readout route, not to all possible
creation or detection mechanisms.

## Quantize the assigned coherent optical coupling

Grant two independent traveling optical modes c,d with the same relevant
spatial overlaps as the preparation source. An effective four-mode term is

    H/hbar = chi (a b c† d† + a† b† c d),

where a,b annihilate the carrier pair. With equally populated coherent
optical modes containing N photons each, the pair drive is Omega=chi N.
For ONE optical mode coherently occupied and the other empty, the stored
pair couples to one output photon with strength

    eta=chi sqrt(N)=Omega/sqrt(N).

Thus one cannot reuse the two-bright-pump Rabi frequency as a single-photon
readout frequency. Removing a coherent pump removes a square-root photon
number enhancement.

For an assumed effective traveling-mode length L_eff, adopt

    N=P L_eff/(c E_photon).

This defines the mode normalization; it is not automatically the physical
mirror separation in a dispersive resonator. The preceding Fabry-Perot's two
traveling components are not independent empty/occupied eigenmodes. An
actual implementation needs an independent output mode, such as a separately
engineered mode geometry, with recalculated coupling. Here its availability
and overlap are deliberately granted, not claimed established. A single
standing optical mode has different combinatorics and pump/background
separation; it is outside this model.

## Capture probability with competing escape

Let gamma=2/tau be pair population loss from independent carrier escape.
Let kappa be photon population decay into an ideal detector; all such decay
is counted as useful. In the pair/photon subspace, zero-detuning amplitudes
obey

    p_dot=-(gamma/2)p-i eta q,
    q_dot=-(kappa/2)q-i eta p,
    p(0)=1, q(0)=0.

There is no phase noise, extra photon absorption or finite observation window.
Set A=integral |p|^2 dt and B=integral |q|^2 dt. Integrated population balance
and coherence give gamma A+kappa B=1 and
kappa B=4 eta^2(A-B)/(gamma+kappa). Therefore

    efficiency=kappa B
      =4 eta^2 kappa/[(gamma+kappa)(gamma kappa+4 eta^2)].

The exact identity

    (gamma+kappa)(gamma kappa+4 eta^2)-kappa(gamma+2 eta)^2
      =gamma(kappa-2 eta)^2 >= 0

proves the maximum is attained at kappa=2 eta, for positive eta, with

    efficiency <= [2 eta/(gamma+2 eta)]^2
                = [eta tau/(1+eta tau)]^2.

For eta=0 the efficiency is zero. This is an algebraic optimization of the
specified two-amplitude model, not a theorem covering every optical readout.

## Assigned benchmark

For L_eff=1 m and the inherited tunneling-only tau=527481.639 s:

| Pump power | N | Readout eta | Optimized capture probability |
|---|---:|---:|---:|
| 628 W | 1.308e13 | 2.407e-10/s | 1.612e-8 |
| 6.28 MW | 1.308e17 | 2.407e-8/s | 1.572e-4 |

At 628 W, even the ideal lossless swap time pi/(2 eta) is approximately
207 years. The mathematical optimum kappa corresponds to a photon storage
time around 66 years. At 6.28 MW, those times are approximately 2.07 years
and 0.658 years respectively. No such storage capability is assumed feasible.
At an independently ASSIGNED kappa=1000/s, efficiencies fall to 6.11e-17
and 6.11e-13 respectively. This output rate is a diagnostic, not measured
cavity data.

The length sensitivity is also explicit: reducing the assigned L_eff from
1 m to 0.1 m gives optimized probabilities 1.61e-7 and 0.00149. Changing
mode length assumes the same local classical overlap while changing quantum
normalization; it is not a completed new optical design. These small results
already grant the longer storage assumption that the preceding preparation
study showed was stronger than necessary for production.

## Verification and consequence

Sixteen numerical checks compare the analytic efficiency with an independent
integrated-amplitude Lyapunov equation and test the optimum across bounded
dimensionless cases. SymPy verifies the exact denominator identity. The
numerical manifest validates inputs and outputs.

ReadoutBound.lean compiles successfully using the existing repository Lean
project. It proves the polynomial identity and the efficiency inequality
for gamma>0, kappa>0, eta>=0. The recorded compiler invocation, source hash,
exit code and output are in lean_verification.json. Lean does NOT certify
mode normalization, the effective Hamiltonian, the loss equations or the
existence of these particles. An initial launch failed because the source
was written relative to the Lean working directory; the final source was
written at the absolute package path and the recorded compile succeeded.

A strong two-pump preparation amplitude alone does not provide a useful
empty-mode photon readout. Keeping both pumps bright permits fast coherent
reverse conversion but returns a tiny signal to occupied optical fields;
a shot-noise/background and measurement analysis is required before calling
that detectable. No detector performance is inferred from the microscopic
pair conversion probability.

This particular single-pump readout is not a promising baseline under the
assigned parameters. Other avenues remain untested, including many-pair or
collective readout, another portal, and coherent measurements with an explicit
noise budget. Such changes require their own constraints and dynamics; they
cannot inherit this calculation as proof of feasibility. The lack of a usable
resonance-search/readout channel remains a material gap in the creation
programme, and the overarching goal remains open.
