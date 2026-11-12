# BI1 AMENDMENT A1: carrier (iii), bimetric (committed alone, before any number under it)

Criteria 91e81dcd76; result 059458c5d4 (FAIL at B0 on carriers (i) and (ii)) has landed. The orchestrator relayed carrier (iii)
afterwards. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

## Carrier (iii), frozen (static, Newtonian limit of a bimetric coupling)

The component couples to its own potential Phi_chi; baryons and photons couple to Phi. The field Lagrangian is
-(1/8 pi G) grad Psi^T K(f) grad Psi - rho_b Phi - rho_chi Phi_chi, with Psi = (Phi, Phi_chi). The mixing is chosen so that
K^-1 = [[1, f], [f, 1]]:
- baryon-baryon and component-component gravity stay standard;
- the component sources the baryons' potential with weight f, and by symmetry the baryons source the component's potential with
  weight f (Newton's third law kept);
- f = f(Xi) is the switch.

## Grading

**(a) Ghost and conservation (sympy).**
- The eigenvalues of K(f): positive-definite iff |f| < 1. The limit f -> 1 is the single-metric (stiff relative mode) limit.
- The divergence of the field stress tensor with x-dependent f is -(dL/df) grad f. This is conserved only if Xi is a dynamical
  local field whose own stress balances it.
- The lane states what the switch adds to the unswitched bimetric class (AX1 graded it; constant f has no such term).

**(b) Size.** The unbalanced force density (dL/df) |grad f| per unit component mass,
a_switch = |grad Phi| |grad Phi_chi| |grad f| / (4 pi G rho_chi).
- Evaluated for an L* galaxy (M_b 8e10; SS1 primary halo, cosmic mean outside R200; |grad f| = 1 / R_W, R_W 1.5 Mpc) at 0.1, 0.3,
  1, 3 Mpc.
- Compared with a0 and with the law's g.
- If Xi is promoted to a local field, this is the force density its coupling transmits to the component (through Xi's source,
  the component's dispersion). Either it is balanced and felt, or it is unbalanced and violates conservation.

**B0(iii) line (same tolerance as (i) / (ii)).**
- PASS iff (a) holds with Xi promoted to a local field (ghost-free, with a conserved total stress) AND (b) a_switch <= 1e-3 of the
  law's g at every radius 0.1-3 Mpc.
- Otherwise FAIL.
- **(c)** If (iii) passes, the usual gates are frozen in a further amendment before any of their numbers. If it fails, the label
  stays FAIL at B0, with all three carriers reported.

## Hand estimate

At 0.3 Mpc: g_b about 1.2e-13, g_chi about 5e-13, rho_chi at the mean 2.3e-27 kg/m^3, |grad f| 2e-23 /m. That gives a_switch about
7e-13 m/s^2, about 0.2 of the law's g. Expected FAIL on (b).
