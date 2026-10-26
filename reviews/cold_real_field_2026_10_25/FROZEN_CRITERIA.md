# Direct nonlinear real-field evolution

Base 082a94d0ab. Evolve q_tt=radial_laplacian(q)-V_q on spherical cell-centred
finite volumes with the full canonical potential, no EOS or cycle averaging.
Initial vacuum packets q=qvac-A exp(-(r/R0)^2), p=0 for (A,R0)=(.5,3),(1.2,3),
(1.6,3),(1.6,6). Restored comparison d=60, q=.8 exp(-(r/3)^2), p=0.
These are prepared sensitivity states, not predicted merger products.
Outer absorbing layer lies in the last 15 units; core radius 10 has no damping.
Use radius60, dx=.05, dt=.005, t_final=200. Track total discrete energy plus
explicit absorbed energy, core energy, field amplitude and compactness estimate.
Require relative energy ledger error <.005 and remain |q|<pi. A damping-ledger
mutation must fail. Preserve outputs before adaptive selection/refinement.

Full Einstein evolution is not asserted: compute kappa=8pi G D_mass Lunit²/c²
from the unchanged constants and quantify when the weak-metric approximation
is controlled. Large compactness would invalidate the flat evolution, not prove
formation of a relativistic star. If localization survives, refine grid/time,
move boundary, and extend duration before claiming a candidate. Finite retention
is not an asymptotic stability or abundance result.
