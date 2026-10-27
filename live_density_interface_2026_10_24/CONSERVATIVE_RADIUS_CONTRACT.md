# LD-8: complete the radius test with admissible transferred species

LD-7 stopped at its initial feasibility assertion before any optimization.
The outer-wall source is feasible at its own quadrature points but separate
total-density and phase interpolation can increase enclosed T mass on a new
grid. Transfer both species' cumulative masses in cell volume instead, then
reconstruct q. Recover exact source edges from their recorded centers.
If subcell resolution still exposes saturation, allow an explicit uniform
initial radial dilation among 1,1.05,1.1,1.2,1.4, preserving species masses.
Record the dilation and both mass errors; reject loss outside the domain.
This modifies only the initial condition, never fixes the final density.
Same four tau/start cases as LD-7. Failed initialization is numerical evidence
only; it neither rejects an interaction nor satisfies boundary restoration.
