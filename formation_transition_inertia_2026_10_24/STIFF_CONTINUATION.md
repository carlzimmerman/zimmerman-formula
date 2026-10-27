# FT-I4S numerical continuation

The high-coherence FT-I4 trajectories exceed the 30-second explicit-integrator
cap. This is resource inconclusiveness, not a negative physical result.
Change solver to implicit Radau and persist accepted half-dynamical-time
segments. First resolve alpha=1,iota=.1,f=.95,nu0=1,profile1,scale30,
n6,nq256,duration12,rtol2e-7. Stop at the unchanged radial-domain event.
Overall cap150s. Every completed segment is written; a partial trajectory is
not a persistence pass. The model, initial conditions and force are unchanged.
If an inner-domain exit occurs, inspect a smaller inner boundary and matched
quadrature before calling it physical collapse. No clipping or imposed phase.
