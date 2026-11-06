# PF06b diagnostic: even-grid derivative null mode

Declared before odd-grid runs. The real collocation first derivative at an even
number of points annihilates the Nyquist alternating mode; using Dxx=Dx@Dx
therefore makes that unresolved mode look spatially constant to the constraints.
Test odd grids 31 and 63, unchanged equations, dt=0.0025, tmax=0.5, with the same
stopping rules. This is a numerical diagnostic outside the original grid list,
not evidence that a filter or extension regularizes AC2q. Compare validation,
constraint drift and stop time. If it removes the failure, require a longer
space/time ladder before any physical interpretation.
