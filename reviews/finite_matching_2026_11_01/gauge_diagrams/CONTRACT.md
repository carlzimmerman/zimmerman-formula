# Vector diagram contract

Construct the six vector graph classes SSV, VS, VVS, FFV, barFFV and pure
gauge (including ghosts) in Martin hep-ph/0111209v2 Eqs 4.6-4.11, 4.16,
4.24 and 6.15-6.30, using DRbar-prime functions. The shared builder supplies
canonical scalar, Takagi fermion and vector eigenvectors as columns.
The real scalar basis is sqrt(2)(Re phi, Im phi). Representation matrices
are Hermitian with C_adj=5, and gauge-generator normalization Tr(t_a t_b)=1/2.

First controls: source equation transcription, function symmetries and zero
limits, supersymmetric Abelian Higgs example (Martin Eq 8.31-8.36), then
full-model unbroken-SUSY cancellation and full graph scale consistency.
Pressure derivatives are interpreted only after these controls pass.
Numerical trial inputs are e=.01,.03 on the TP02 valley. No threshold
resummation or finite-current term is inferred from these vacuum graphs.

No random inputs. Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4, mpmath 1.3.0.
Use a fresh v2 run directory, one thread, 180-second wall limit and
170-second CPU limit per first check; report actual RSS. Earlier TP01/02
sources are immutable. All functions return the coefficient V^(2), before
division by (16 pi^2)^2. A failed check remains visible.
