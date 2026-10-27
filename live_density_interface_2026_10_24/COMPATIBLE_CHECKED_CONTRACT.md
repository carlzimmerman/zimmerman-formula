# LD-16: make the cold benchmark feasible before checking curvature

LD-15 stopped in its check because the scale4b density, when treated as
entirely T rather than the specified partial phase, exceeds u=1. No scientific
experiment ran. For the cold-Hessian check and all-T controls, use an unrelated
scale8b Plummer start, verify u<1, then run the planned compatible quadrature
tests unchanged. The physical joint seed retains scale4b and tiny T fraction,
which is feasible. Keep the failed check as numerical provenance.
