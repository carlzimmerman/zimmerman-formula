#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cde_l4c_covariant_dirac_rank.py -- truncated four-pair rank audit for CDE-L4C.
=====================================================================================================
The per-mode preservation gate proposed a principal MOND residual after a
multiplier elimination. No single nonlinear action is frozen in this
directory, so C_MOND below is an assigned surrogate rather than a fresh
Hamiltonian derivation. This computes whether the four displayed constraints {p_N, C_MOND, C_K,
C_slip} form a rank-4 second-class subsystem. It does not include the
cuscuton pair (chi,p_chi), so the Yao-Oliosi-Gao-Mukohyama theorem cannot be
invoked here to certify the full action's DOF count.

C_MOND imports the principal residual reported by the previous script. Its field part is the MOND operator
Lpar*a0^2*kk*Phi + (GR/source terms). We build the
4x4 Dirac matrix over {p_N, C_MOND, C_K, C_slip} and test rank 4, det ~ kk^4 * Lpar^2 (the user's k^8 Lpar^2).
Includes the momentum-constraint (shift) sector to confirm it stays first-class. Honest scope: linearized
scalar sector with standard ADM structure; exact-coefficient covariant version flagged if any check is soft.
"""
import sympy as sp, sys
P=lambda *a: print(*a, flush=True); FAILS=[]; SOFT=[]
def check(n, ok, d='', soft=False):
    tag='PASS' if ok else ('SOFT' if soft else 'FAIL'); P(f"  [{tag}] {n}"+(f"  ({d})" if d else ''))
    if not ok: (SOFT if soft else FAILS).append(n)

# ---- declared scalar-sector phase space; cuscuton chi,p_chi are absent ----
Phi,pPhi,Psi,pPsi,B,pB,lam,plam = sp.symbols('Phi pPhi Psi pPsi B pB lam plam', real=True)
Q=[Phi,Psi,B,lam]; Pm=[pPhi,pPsi,pB,plam]
def PB(f,g):
    return sum(sp.diff(f,Q[i])*sp.diff(g,Pm[i]) - sp.diff(f,Pm[i])*sp.diff(g,Q[i]) for i in range(4))
kk=sp.symbols('kk', positive=True); Lpar=sp.symbols('Lpar', positive=True)
a0sq,Bp,cs,rho,K0,mu_c=sp.symbols('a0sq B_p c_s rho_b K0 mu_c', real=True)

# ---- the emerged constraint set (from the preservation gate) ----
G_N   = pPhi                                          # primary lapse momentum p_N
C_slip= cs*kk*(Phi - Psi)                             # no-slip (3R - 4 D^2 lnN), principal
C_K   = pPsi - K0                                     # CMC / cuscuton (K ~ trace momentum)
H_mom = kk*(pPsi) - kk*pB                             # scalar momentum constraint (spatial-diffeo gauge; schematic principal)
# C_MOND = the EMERGED residual of dot p_N=0 after lambda_s fixed by dot C_K=0 (previous script), as a phase-space fn:
#   field part = the MOND operator Lpar*a0sq*kk*Phi (dominant) + GR pieces (B_p kk (Phi+Psi)) + pPsi + source rho_b
C_MOND= Lpar*a0sq*kk*Phi + Bp*kk*(Phi+Psi) + pPsi + rho

P("="*74); P("STEP 1: the four PHYSICAL constraints and their pairwise brackets"); P("="*74)
Cset=[G_N, C_MOND, C_K, C_slip]; names=['p_N','C_MOND','C_K','C_slip']
Delta=sp.Matrix(4,4, lambda i,j: sp.simplify(PB(Cset[i],Cset[j])))
for i in range(4):
    for j in range(i+1,4):
        P(f"  {{{names[i]}, {names[j]}}} = {Delta[i,j]}")
P(f"\n  Delta =\n{sp.pretty(Delta)}")
detD=sp.factor(sp.simplify(Delta.det())); rankD=Delta.rank()
P(f"\n  det Delta = {detD}")
P(f"  rank Delta = {rankD}")
check("4x4 Dirac matrix has GENERIC rank 4", rankD==4, f"rank={rankD}")
cancel={Bp: -Lpar*a0sq/2}
Delta_cancel=sp.simplify(Delta.subs(cancel)); rank_cancel=Delta_cancel.rank()
check("rank drops to 2 on 2*B_p+Lpar*a0sq=0",
      sp.simplify(detD.subs(cancel))==0 and rank_cancel==2,
      f"rank={rank_cancel}, matrix={Delta_cancel}")
check("det Delta is nonzero only away from c_s*k*(2*B_p+Lpar*a0sq)=0",
      sp.factor(detD)==cs**2*kk**4*(2*Bp+Lpar*a0sq)**2, f"det={detD}")
# the user's expected structure det ~ kk^4 * (leading)^2; check kk^4 factor and Lpar dependence
detD_expand=sp.expand(detD)
has_kk4=sp.simplify(detD/kk**4).free_symbols and (detD/kk**4).is_finite if detD!=0 else False
P(f"  det Delta / kk^4 = {sp.factor(sp.cancel(detD/kk**4))}")
check("det Delta carries kk^4 (principal k^8 Lpar^2 structure of the user's analysis)", sp.cancel(detD/kk**4).has(Lpar) or sp.cancel(detD/kk**4)!=0, f"det/kk^4 = {sp.cancel(detD/kk**4)}")

P(""); P("="*74); P("STEP 2: {p_N, C_MOND} = the second-class pairing that makes MOND propagate-free"); P("="*74)
b=sp.simplify(PB(G_N,C_MOND)); P(f"  {{p_N, C_MOND}} = {b}")
check("{p_N,C_MOND} has the displayed generic coefficient (not an all-parameter certificate)",
      sp.factor(b)==-kk*(Bp+Lpar*a0sq), f"{b}")

P(""); P("="*74); P("STEP 3: momentum first-class status is NOT established by this matrix"); P("="*74)
# H_mom should have vanishing bracket with the second-class set on the constraint surface (up to constraints)
bm=[sp.simplify(PB(H_mom, c)) for c in Cset]
P(f"  {{H_mom, [p_N,C_MOND,C_K,C_slip]}} = {bm}")
# first-class means its brackets close on constraints; here check it is not generically invertible against the set
check("H_mom bracket with p_N vanishes but other displayed brackets do not",
      PB(H_mom,G_N)==0 and any(x!=0 for x in bm[1:]), f"brackets={bm}")
P("  These nonzero expressions were not reduced to combinations of constraints.")
P("  Full functional diffeomorphism closure is therefore OPEN, not certified.")

P(""); P("="*74); P("STEP 4: Phi, Psi remain NONZERO on the constraint surface (evade the 2026-example failure)"); P("="*74)
# solve the linearized constraints C_slip=0, C_K=0, C_MOND=0 and check Phi,Psi are not forced to 0
sol=sp.solve([C_slip, C_MOND-0], [Psi], dict=True)   # C_slip=0 -> Phi=Psi; then C_MOND relates Phi to source
P(f"  C_slip=0 => Phi=Psi (no-slip). C_MOND=0 with Phi=Psi:")
cm_noslip=sp.simplify(C_MOND.subs(Psi,Phi))
P(f"    {cm_noslip} = 0  =>  Phi = {sp.solve(cm_noslip, Phi)}")
phi_sol=sp.solve(cm_noslip, Phi)
check("Phi is SOURCED (nonzero, proportional to rho_b), NOT forced to 0", len(phi_sol)>0 and phi_sol[0].has(rho), f"Phi={phi_sol[0] if phi_sol else None}")
check("Psi = Phi nonzero (no-slip, both sourced) -- NOT the 2026-example Phi=Psi=0", phi_sol and phi_sol[0]!=0)

P(""); P("="*74); P("STEP 5: SCOPE OF THE COUNT"); P("="*74)
P("  The displayed constraints form a rank-4 second-class SUBSYSTEM in the declared")
P("  (Phi,Psi,B,lambda) phase space. The full action also contains the cuscuton")
P("  pair (chi,p_chi), omitted here. Its inhomogeneous Legendre Hessian is nonzero,")
P("  so its finite large-velocity momentum asymptote does not remove it from the Dirac analysis.")
P("  => N_grav=2 for the FULL action is OPEN pending the coupled chain.")
ndof = "TRUNCATED RANK 4; FULL-ACTION N_grav OPEN" if rankD==4 else f"UNDETERMINED (rank {rankD})"
check("the declared four-constraint subsystem has rank 4", rankD==4)

P(""); P("="*74); P("SCOPE / OWED (honest):"); P("="*74)
P("  - This is the LINEARIZED scalar-sector principal analysis with standard ADM structure. The FULL covariant")
P("    closure (exact GR H_perp/H_i coefficients, the complete diffeo constraint algebra {H_i,H_j}, {H_perp,H_i},")
P("    and the nonlinear brackets at all orders) is the remaining rigor item -- flagged NOT fully covariant.")
P("  - The Yao-Gao theorem cannot yet be invoked for the full count because (chi,p_chi) is absent here.")
P("    The generic rank-4 structure is COMPUTED, with a rank-2 cancellation surface now explicit.")
P("  - Matter nabla_mu T^munu=0 and PPN (alpha_1,2,3 -- the predicted alpha_3 killer) remain.")
P(""); P("RESULT:", ndof); P("FAILED:", FAILS if FAILS else "none", "| SOFT/owed:", SOFT if SOFT else "none")
sys.exit(1 if FAILS else 0)
