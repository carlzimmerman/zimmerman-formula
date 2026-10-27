# LD-4: independent bulk normalization benchmark

Set q=1, k=tau=K=beta=0; optimize all dark cell masses at fixed total5.364Mb
from a Plummer profile of scale4b, with only W and gravity in energy. n64,
128,256 quadratic grids and domain2. The continuum Euler equation predicts
the galaxy law without supplying its density. This checks whether the joint
gravity/field discretization actually recovers that identity under refinement.
The all-T control is explicitly NOT a solution with a free outer reservoir
or interface. It tests one needed bulk implication, not the user’s full goal.
