# TK1 AMENDMENT A1 (POST HOC; committed alone, before the graded A3 runs)

Criteria 98f2ab2b6e. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What was seen before this amendment.** One toy evaluation of the primary's Friedmann function
G(H) = H^2 - rest - xK(3H) at a patch-like state (Omega_n = 12, rest = -14 in H0 units; not a graded row). It showed that
G is not monotone in H when the floor is on: the stiff part 0.75 Omega_n^2 / M_2 (1 + theta M_2'/M_2) peaks near
theta ~ 1e-5 H0 (the factor 1 + theta M_2'/M_2 rises to 1 + 2p while 1/M_2 is capped by the floor). So the expanding
root H(a) can reach a fold (G_H = 0), where dH/dt diverges and the homogeneous solution cannot be continued. It also showed
lambda_eff passing -2/3 at a larger H than the fold. No graded A3 number (calibrated patch, times, labels) had been
computed.

**What changes.**

1. **s2 is read two ways.** The frozen s2 (the fixed-lapse velocity Hessian, h_tr = 0, lambda_eff = -2/3) is kept and
   reported first, with its label. But the lapse N is auxiliary with its own equation, so whether the evolution is
   singular is decided by the principal matrix of (gamma-ddot, N-dot), [[L_vv, L_vN], [L_Nv, L_NN]], i.e. by its Schur
   complement L_vv - L_vN L_Nv / L_NN (the Hessian of the Lagrangian with N eliminated). The added reading **s2'**: that
   matrix is singular. In the homogeneous patch it is D = L_adot,adot L_NN - L_adot,N^2 = 0 in clock time, which is the
   fold of the Friedmann root (G_H = 0). Checked numerically along each track (D and G_H printed at the event).
2. **s1 is extended** to include dH/dt diverging at finite proper time (the fold), which s1 as frozen did not name.
3. **Labels.** A3 and the lane label are printed twice: as frozen (s2 = h_tr) and under A1 (s2' and the extended s1 in
   place of s2 and s1). The frozen label is printed first. Under A1 the K4 kinetic-coefficient line s3 is unchanged.

Nothing else changes.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
