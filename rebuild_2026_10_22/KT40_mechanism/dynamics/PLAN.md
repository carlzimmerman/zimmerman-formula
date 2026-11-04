# Local matter-dynamics discriminator

Starting checkpoint: KT39 p=9/8, ell=3 kpc, with its frozen full tensor law.
The question is whether the extra tidal response stabilizes or destabilizes
ordinary matter. We derive the exact frozen-coefficient Fourier symbol, then
couple it to nonrelativistic continuity and barotropic Euler equations.
The result is conditional on that matter closure, not a new empirical cut,
collisionless theorem or relativistic health claim.

Owner: mechanism_dynamics, writing only this directory. Historical equations,
parameters, data and outputs remain unchanged. The analytic task covers
p>1 wherever the derivatives exist and an explicit positive-density tidal
jet at p=9/8. Finite verification compares independent tensor derivatives
on deterministic jets, checks mixed-derivative cancellation, verifies a
sinusoidal second-energy variation and evaluates the explicit jet in both
original a0 footings. No galaxy or dwarf fit is rerun in this lane.

Distinguish a negative static transfer from a dynamical instability. Success
is a derived dispersion relation and an exact sign conclusion with clear
hypotheses; a fit or a sampled sign alone is insufficient. The numerical
experiment has pinned inputs and explicit wall/CPU/thread/log caps.
