# Why the late transfer changes the discrete mass

This is an interpretation of the failed transfer screen, not a repaired restart or a modified acceptance rule.

The regular radial envelope has a cubic reference-element interpolant a_h. Its stored mass is the lumped quadrature sum

    M_h = sum_i w_i |a_h(x_i)|^2 = sum_i |u_i|^2.

Nested interpolation reproduces that same cubic function, but the new lumped weights integrate its squared modulus differently. A changing discrete norm under this operation is not physical mass escaping from the dwarf. It also is not permission to normalize the candidate and declare convergence.

On one reference interval [-1,1], write a_h=sum_(k=0)^3 c_k P_k. Four-point Gauss-Lobatto quadrature is exact through degree5. Orthogonality gives integral(P3^2)=2/7, whereas its Lobatto sum is2/3. Therefore, for a constant positive B=dr/dz,

    M_lumped - M_integral = (8/21) B |c_3|^2.

After halving the element, each child's cubic Legendre coefficient is c_3/8, and each child has Jacobian B/2. The total remaining error is1/64 of the old error. Hence

    M_old_lumped - M_nested_lumped = (3/8) B |c_3|^2.

The actual sinh map has a varying Jacobian, so this last formula is only a leading local diagnostic there. `diagnostics.py` evaluates the actual interpolant integral with8,16,32-point Gauss-Legendre quadrature and records the mapped-Jacobian correction, without changing any field or conserved reference. The exact constant-J coefficients are checked with rational arithmetic and independent analytic polynomial controls.

This distinguishes quadrature error from physical escape, but supplies no bound on local force error, future nonlinear evolution or independent spatial convergence. The failed candidates remain ineligible. The independent16384runs start from the analytic initial conditions with their own initial discrete references, not an altered late state. Their attained early overlap must remain separate from the unresolved later collapse.
