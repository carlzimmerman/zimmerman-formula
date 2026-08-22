# HARD GATE: GR + CMC + auxiliary MOND has 3 DOF, not 2 (2026-08-22)

## The result
For S = (c^3/16piG) INT N sqrt(h)(K_ij K^ij - K^2 + (3)R)
      + (c^3/16piG) INT N sqrt(h) Lambda(K-q)
      - (1/8piG) INT N sqrt(h)[chi D_i Phi D^i Phi + V(chi,q)],
the local canonical variables (h_ij,pi^ij),(q,p_q),(chi,p_chi),(Lambda,p_Lambda),(N,p_N) give
18 phase-space dims/point.  Shift: 3 momentum + 3 pi_i first-class (remove 6).  Scalar sector:
4 primaries (p_N,p_q,p_chi,p_Lambda) + 4 secondaries (H_perp, K-q, chi-eq, C_q=-Lambda-dV/dq).

CRUX: preservation of p_q FIXES a multiplier / gives the algebraic q-equation -- it does NOT
supply an independent gravitational constraint to eliminate the remaining scalar pair.  And
the CMC restriction changes the classification of H_perp (no longer the GR first-class
refoliation constraint once treated as a physical spatially-covariant condition).  The generic
surviving branch is the standard 3 DOF of spatially-covariant auxiliary-scalar gravity.

  => GR + CMC + auxiliary MOND  ==>  3 LOCAL DOF.  The 'CMC removes the scalar' hope is FALSE.

This supersedes the earlier heuristic 3x3-subblock argument (which suggested 2+0 and was
flagged unproven).  It agrees with the CPC 2026 theorem: a generic auxiliary-scalar SCG has
3 DOF; TWO independent degeneracy conditions are required to reach 2.

## What this proves about the original equations
K=q, D_i q=0, a0=cq/Z are PHENOMENOLOGICAL TARGET equations -- NOT by themselves a sufficient
variational completion.  You cannot bolt them onto GR and get 2 DOF.  The action must be
built so those equations sit inside a Hamiltonian that ALREADY satisfies the two nonlinear
degeneracy conditions.

## The sharply-defined remaining problem (either a Lagrangian or a no-go)
Solve SIMULTANEOUSLY:
  Degeneracy condition 1 = 0     (fixes the allowed gravitational coefficient functions
  Degeneracy condition 2 = 0      c1,c2,c3,c4,d1,d2 of the SCG Lagrangian)
  K = q ,  D_i q = 0 ,  a0(q)=cq/Z
  div[ mu(g/a0) grad Phi ] = 4 pi G rho   (via the auxiliary Legendre sector)
Outcome: an explicit 2-DOF nonlinear-MOND Lagrangian, OR a no-go theorem (the degeneracy
forbids the MOND nonlinearity).  This needs the ACTUAL two degeneracy equations from CPC 2026
(doi 10.1088/1674-1137/ae2ab0), not heuristic counting.

## The exhausted naive constructions (the no-go map)
  GR + A^2 + CMC:           lambda_eff = 2/3, not kinetic-conformal.
  exact d=2 2-DOF branch:   Hessian fixed quadratic => no nonlinear mu; and c_T=D/f(phi) varies.
  GR + CMC + aux MOND:      3 DOF (this gate).
  A1/A2 cubic branches:     2-DOF only through cubic order; MOND embedding + quartic OPEN.
