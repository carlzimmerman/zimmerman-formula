# Causality: what it has meant, and what the spec's requirement 7 can and cannot mean

Written 2026-09-05 for the field-theory effort. Plain history first, then the point this repository has been treating loosely.

## 1. Four different things called "causality"

1. **Instantaneous action at a distance (Newton, 1687).** Gravity acts across space with no delay. Newton disliked it ("so great an absurdity") but the theory worked, and it was accepted for 218 years.
2. **Finite propagation speed (Laplace 1805, Maxwell 1865, Poincaré 1905).** Laplace argued that if gravity propagated at a finite speed the Earth would feel the Sun's force from where the Sun *was*, producing an aberration torque that would visibly spiral the orbit; from the absence of that effect he concluded gravity travels at least 7 million times faster than light. The argument is wrong, and the reason it is wrong matters below: in any field theory that conserves momentum and has velocity-dependent terms, the retardation and the velocity-dependent corrections cancel to high order, so the force points at the *present* position of the source even though the field propagates at finite speed. Carlip (2000) made this precise for gravity. Absence of aberration is not evidence of instantaneous propagation, and instantaneous propagation is not needed to explain it.
3. **Lorentz-invariant causality (Einstein 1905, Minkowski 1908).** No signal outside the light cone, because a superluminal signal in one frame is a backward-in-time signal in another, which allows closed causal loops (the tachyonic antitelephone, Tolman 1917). This is the meaning most physicists intend by default, and it presupposes Lorentz invariance.
4. **Well-posedness of the initial-value problem (Hadamard 1902, Choquet-Bruhat 1952).** A theory is causal in this sense if data on one surface determine the future uniquely and continuously, with a finite domain of dependence. General relativity was shown to satisfy this in 1952; the proof needs the field equations to split into *elliptic constraints on the slice* and *hyperbolic evolution off it*.

## 2. The point usually overlooked: general relativity itself carries an instantaneous elliptic sector

In the ADM form, the Hamiltonian and momentum constraints are elliptic equations on each slice. Solve them and the lapse and shift respond *instantly* across the whole slice to a change in the matter distribution. Nobody calls general relativity acausal, for two reasons that must be kept apart:

- The instantaneous pieces are **gauge**: no measurable quantity depends on them faster than light. (Electrodynamics in Coulomb gauge is the textbook case: the scalar potential is instantaneous, the fields are retarded.)
- The constraints are **preserved by the evolution** (the Bianchi identity), so the elliptic and hyperbolic parts never disagree.

So "elliptic" is not the same as "acausal". A theory with an elliptic auxiliary field is acausal in sense 3 only if a measurable, gauge-invariant response between two separated bodies arrives faster than light; and it is ill-posed in sense 4 only if the elliptic operator fails to be invertible somewhere (loss of ellipticity) or the constraints are not preserved.

## 3. Preferred foliations (Hořava 2009; Blas, Pujolàs, Sibiryakov 2010–2011)

Once a theory has a preferred time foliation, sense 3 is gone by construction: Lorentz invariance is broken, and "superluminal" no longer implies "backward in time in some frame", because one frame is special. What replaces it is:

- **No closed causal loops**, guaranteed if every signal moves forward along the preferred time. Instantaneous propagation *along a leaf* satisfies this.
- **A well-posed Cauchy problem on the leaves** (sense 4).
- **No observational conflict**: no detected superluminal signal, no gravitational Cherenkov emission from high-energy cosmic rays (Elliott, Moore, Stoica 2005). The Cherenkov bound constrains modes *slower* than the particle; superluminal or instantaneous modes are immune to it.

Khronometric gravity has an instantaneous mode in this exact sense (the lapse-like equation of the khronon is elliptic on the leaves), and it has a literature of black holes with "universal horizons" precisely because signals can be instantaneous on the leaves. The theory is not considered acausal; it is considered Lorentz-violating.

## 4. What requirement 7 can therefore mean

The spec says: "no unacceptable superluminal or instantaneous physical channel." Given the four senses:

- Sense 3 cannot be the test, because every host on the table (aether, clock, khronon) breaks Lorentz invariance already, and the tensor sector still has c_T = c (requirement 6).
- The defensible reading is: **(i) no closed causal loops, (ii) a well-posed Cauchy problem on the leaves including the zero-field limit, (iii) no observable superluminal signalling and no Cherenkov catastrophe.**
- Under that reading an *elliptic* MOND auxiliary (the Newtonian potential u of QUMOND, astra's U and heat coordinate in C-H) is acceptable **if and only if** its elliptic operator is uniformly invertible and its constraints are preserved by the evolution. That is not requirement 7 at all; it is requirement 9, the controlled zero-field limit. The bare AQUAL operator loses ellipticity as μ → 0. The repository's previous kills of "elliptic-constraint carriers" (MMG, York/CMC, spec line 68) were argued from the instantaneous channel; the sharper statement is that they were never shown to be uniformly elliptic and constraint-preserving.

## 5. What this says to the current candidates

- **The coherence length is the thing that repairs ellipticity.** A term ξ²|∇⊥V|² with its own positive coefficient (outside the MOND function J, not multiplying J_Y) gives the static operator the principal symbol J_Y k² + c_ξ ξ² k⁴, which is invertible even where J_Y → 0. Inside J (the f32/f33 form, J_Y → J_Y(1 + ξ²k²)) it does not, because J_Y multiplies everything. The two forms coincide for the PPN ladder (J_Y is constant there) and differ only at zero field. So the same length that screens the Solar System can close requirement 9, but only in the "outside J" form. That is a calculation, not yet done: the zero-field limit of the static law with c_ξ ξ² k⁴ present.
- **The hyperbolic form** (f32/f33 in a clock host) has dispersion ω² = c_s²k²(1 + ξ²k²), Hořava's z = 2 form, with unbounded group velocity at short wavelength. It passes (i) and (iii); (ii) is the standard Lifshitz Cauchy problem, well-posed. What is left is judgment about "unacceptable", and the history says that judgment has always been made observationally, never by fiat.
- **Astra's C-H** has an elliptic heat sector on the leaves. Its report says the "naive scalar-wave realization fails" the causal screen. Under section 4 the question to ask instead is whether U and W are gauge-like shadows of the lapse (2|DU − a|² ties U to the clock's acceleration) and whether the heat operator is uniformly invertible. If both hold, the instantaneous channel is of the general-relativity kind, not the tachyon kind.

## 6. One-line summary

Instantaneous is not the same as acausal; acausal has meant four different things; in a preferred-foliation theory the only ones left are well-posedness and observation; and well-posedness at zero field is where a coherence length placed *outside* the MOND function does work that nothing else in the repository does.
