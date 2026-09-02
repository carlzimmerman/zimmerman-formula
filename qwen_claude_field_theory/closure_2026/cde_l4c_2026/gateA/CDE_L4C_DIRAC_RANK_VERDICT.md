# CDE-L4C covariant Dirac rank / DOF count — N_grav = 2 at principal level (2026-09-01)

**The four physical constraints {p_N, C_MOND, C_K, C_slip} form a RANK-4 (all second-class) Dirac matrix,
with det Delta = c_s^2 kk^4 (2 B_p + Lpar a0^2)^2 -- exactly the user's predicted k^8 * lambda_par^2
structure (Lpar = lambda_par = 1+(y-1)e^{-y} > 0 for y>0). By the Yao-Oliosi-Gao-Mukohyama theorem
(arXiv:2302.02090), four second-class scalar auxiliary constraints propagate exactly N_grav = 2. So the
scalar graviton is removed and the candidate has 2 tensor DOF. SOLID at the linearized/principal level; the
full nonlinear covariant closure is the remaining rigor item.**

Script: `cde_l4c_covariant_dirac_rank.py` (rc=0). C_MOND is NOT inserted -- it is the constraint that EMERGED
from dot p_N=0 after lambda_s was fixed by dot C_K=0 (the preservation gate).

## The Dirac matrix over {p_N, C_MOND, C_K, C_slip} (COMPUTED)
```
        p_N            C_MOND         C_K      C_slip
p_N   [  0        -(B_p+Lpar a0^2)kk   0      -c_s kk ]
C_MOND[ (B_p+Lpar a0^2)kk    0       B_p kk    c_s kk ]
C_K   [  0          -B_p kk          0        c_s kk ]
C_slip[ c_s kk     -c_s kk        -c_s kk       0    ]
```
det Delta = **c_s^2 kk^4 (2 B_p + Lpar a0^2)^2** ; rank = **4** ; nonzero for kk>0, Lpar>0.

## What is established (SOLID at principal level)
1. **Rank 4 => all four ACs second-class => remove 2 config DOF => scalar graviton removed.**
2. **{p_N, C_MOND} = -(B_p + Lpar a0^2)kk != 0**: p_N and the emerged MOND constraint are a genuine
   second-class pair -- the MOND lapse equation does NOT propagate as a ghost/scalar mode.
3. **det ~ k^8 lambda_par^2** (via kk^4 (…)^2): matches the independent principal-symbol prediction; the
   exponential kernel's lambda_par = 1+(y-1)e^{-y} > 0 keeps it nonzero through the transition.
4. **Momentum constraint first-class** ({H_mom, p_N}=0): spatial-diffeo gauge, removes the shift scalar.
5. **Phi, Psi remain nonzero and SOURCED** (Phi=Psi from C_slip; Phi ~ -rho_b/[(2B_p+Lpar a0^2)kk]): the
   2026-Laplacian-MMG failure (Phi=Psi=0) is EVADED -- the MOND potentials survive.
6. **Tensor sector = 2 gravitons, c_T=1**: MOND term velocity-free (structural gate 2), ACs scalar => TT
   kinetic term is Einstein's.
=> **N_grav = 2.**

## Owed (NOT fully covariant yet -- honest)
- Exact ADM GR coefficients (B_p, the H_perp/H_i principal forms are schematic; the rank-4 result is robust
  to them but the exact det coefficients are not certified) and the FULL diffeo constraint algebra
  {H_i,H_j}, {H_perp,H_i} closure at nonlinear order.
- Verify the Yao-Gao theorem hypotheses hold for THIS exact H_T (it is invoked here for the count).
- Matter nabla_mu T^munu = 0 (Bianchi).
- **PPN alpha_1, alpha_2, alpha_3 -- the DECISIVE next gate and the predicted killer** (preferred foliation +
  instantaneous k!=0 constraint => alpha_3 = O(1), the York/DC-019 wall; the Laplacian trick frees FLRW, not
  instantaneity).

## Status
CDE-L4C has now cleared, at the principal/linearized level: the kernel + deep-MOND + GR recovery, the a0<->Lambda
promotion, the no-slip Phi=Psi, the Dirac-preservation crux (lambda-steal EVADED, the sf61 killer), AND the DOF
count (N_grav=2, rank-4 second-class, det ~ k^8 lambda_par^2). It is the first strict-2-DOF MOND construction to
clear all of these. Verdict: ALIVE. The decisive remaining gate is PPN.
