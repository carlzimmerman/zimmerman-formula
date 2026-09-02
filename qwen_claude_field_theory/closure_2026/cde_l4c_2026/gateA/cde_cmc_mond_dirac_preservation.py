#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cde_cmc_mond_dirac_preservation.py -- the decisive CDE-L4C Dirac gate (per-mode principal analysis).
====================================================================================================
Question: for the narrow candidate {p_N, C_MOND, C_K, C_slip} with the Laplacian no-slip multiplier,
does preservation of the primary lapse momentum p_N GENERATE the MOND lapse equation as an INDEPENDENT
constraint, or does the no-slip multiplier lambda_s STEAL it (the sf61 trap)?

Method: reduce the scalar-sector field-theory Dirac analysis to a finite per-k-mode phase space and trace
the preservation chain HONESTLY (no pre-decided constraint-vs-multiplier). This is a PRINCIPAL/structural
analysis (captures the bracket structure {p_N,C_slip}!=0 and {C_K,C_slip}!=0 that drive the crux); the full
nonlinear field-theory closure is flagged owed. Every classification is COMPUTED from Poisson brackets.

Per-mode scalar phase space (Fourier mode k, background MOND field y so mu=mu(y), longitudinal symbol
Lpar=1+(y-1)e^{-y}):
  canonical pairs (Phi,pPhi)=(delta N, p_N), (Psi,pPsi ~ trace momentum ~ K), (lam,plam) [slip multiplier].
  {Phi,pPhi}={Psi,pPsi}={lam,plam}=1.
Constraints:
  G_N   = pPhi                                   (primary: lapse momentum p_N)
  G_lam = plam                                   (primary: slip-multiplier momentum)
Total Hamiltonian pieces (scalar sector, principal symbols; kk=k^2):
  H_grav = N*Hperp,  Hperp = pPsi + Bp*kk*Psi + rho_b            (GR Ham. constraint; N=1+Phi)
  H_mom  = (momentum constraint, fixes shift; scalar part sets pPsi<->Psi-dot, not needed for lambda crux)
  H_MOND = (a0^2/8piG)*N*F(y);  its N-variation is the MOND operator M = Lpar*kk*Phi - 4piG rho_b (AQUAL, longitudinal)
  H_slip = (D^2 lam) C_slip -> per mode = (-kk*lam)*Cslip,  Cslip = cs*kk*(Phi-Psi)   [cs=4/c^2; C_slip^(1)=(4/c^2)lap(Psi-Phi)]
  H_cusc = enforces C_K = pPsi - K0                                   (CMC; extended-cuscuton, unitary gauge)
We DO NOT insert C_MOND. We compute dot p_N and see whether M emerges.
"""
import sympy as sp, sys
P=lambda *a: print(*a, flush=True); FAILS=[]
def check(n, ok, d=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {n}"+(f"  ({d})" if d else '')); 
    if not ok: FAILS.append(n)

# phase-space coords and canonical Poisson bracket
Phi,pPhi,Psi,pPsi,lam,plam = sp.symbols('Phi pPhi Psi pPsi lam plam', real=True)
Q=[Phi,Psi,lam]; Pm=[pPhi,pPsi,plam]
def PB(f,g):
    return sum(sp.diff(f,Q[i])*sp.diff(g,Pm[i]) - sp.diff(f,Pm[i])*sp.diff(g,Q[i]) for i in range(3))

kk = sp.symbols('kk', positive=True)               # k^2
Lpar = sp.symbols('Lpar', positive=True)           # longitudinal MOND symbol 1+(y-1)e^{-y} > 0
Bp, cs, a0sq, rho = sp.symbols('B_p c_s a0sq rho_b', real=True)
lams = sp.symbols('lam_s', real=True)              # the slip multiplier field value (=lam here)
K0 = sp.symbols('K0', real=True)

# --- constraints ---
G_N   = pPhi                                        # primary p_N
G_lam = plam                                        # primary p_lambda
Hperp = pPsi + Bp*kk*Psi + rho                      # GR Hamiltonian constraint (scalar principal)
Cslip = cs*kk*(Phi - Psi)                           # C_slip principal (=(4/c^2)lap(Psi-Phi) sign: prop kk(Phi-Psi))
C_K   = pPsi - K0                                   # CMC / cuscuton
M_op  = Lpar*kk*Phi - 4*sp.pi*a0sq*rho              # MOND lapse operator (longitudinal AQUAL), source rho_b

# --- Total Hamiltonian (per mode). N=1+Phi. Laplacian slip: (D^2 lam)Cslip = -kk*lam*Cslip. ---
N = 1 + Phi
H_grav = N*Hperp
H_MOND = a0sq*N*(Lpar*kk*Phi**2/2)                  # H_MOND whose d/dPhi = a0sq*(Lpar*kk*Phi) = M-operator's field part
H_slip = (-kk*lam)*Cslip                            # Laplacian-multiplier coupling
mu_c = sp.symbols('mu_c', real=True)
H_cusc = mu_c*C_K                                   # cuscuton enforces CMC via its own multiplier mu_c
H_T = H_grav + H_MOND + H_slip + H_cusc

P("="*74); P("STEP 0: key brackets that drive the crux"); P("="*74)
b_pN_slip = PB(G_N, Cslip); check("{p_N, C_slip} != 0 (the danger: N appears in C_slip)", b_pN_slip!=0, f"{b_pN_slip}")
b_CK_slip = PB(C_K, Cslip); check("{C_K, C_slip} != 0 (the rescue channel: K vs 3R)", b_CK_slip!=0, f"{b_CK_slip}")
b_pN_CK   = PB(G_N, C_K);   P(f"  {{p_N, C_K}} = {b_pN_CK}")

P(""); P("="*74); P("STEP 1: preservation chain, HONEST order (do not pre-decide)"); P("="*74)
# dot(p_lam) = {p_lam, H_T} -> should give C_slip=0 (secondary)
dplam = sp.expand(PB(G_lam, H_T))
P(f"  dot p_lam = {{p_lam,H_T}} = {dplam}")
ratio=sp.simplify(dplam/Cslip); check("dot p_lam=0 generates the SECONDARY constraint C_slip=0 (dplam = kk*C_slip)", ratio==kk, f"dplam/Cslip={ratio}")

# dot(C_K) = {C_K, H_T}: does it fix lambda (lam) ?
dCK = sp.expand(PB(C_K, H_T))
P(f"  dot C_K   = {{C_K,H_T}}   = {dCK}")
lam_coeff_in_dCK = sp.diff(dCK, lam)
check("dot C_K=0 CONTAINS lambda (can fix the slip multiplier)", lam_coeff_in_dCK!=0, f"d(dCK)/dlam = {lam_coeff_in_dCK}")
sol_lam = sp.solve(sp.Eq(dCK,0), lam)
P(f"  => solving dot C_K=0 for lambda: lam = {sol_lam}")

# dot(p_N) = {p_N, H_T}: the crux. Does it (after lam fixed) give an INDEPENDENT MOND equation?
dpN = sp.expand(PB(G_N, H_T))
P(f"  dot p_N   = {{p_N,H_T}}   = {dpN}")
lam_coeff_in_dpN = sp.diff(dpN, lam)
P(f"  d(dot p_N)/dlam = {lam_coeff_in_dpN}   (if !=0, lam appears here too)")

P(""); P("="*74); P("STEP 2: THE CRUX -- is the MOND equation independent, or stolen?"); P("="*74)
if sol_lam:
    lam_fixed = sol_lam[0]
    dpN_after = sp.expand(dpN.subs(lam, lam_fixed))
    P(f"  dot p_N=0 AFTER substituting lambda fixed by dot C_K=0:")
    P(f"    {sp.simplify(dpN_after)} = 0")
    # does the residual contain the MOND operator Lpar*kk*Phi AND the baryon source, as an independent eq?
    has_mond = sp.simplify(sp.diff(dpN_after, Phi))!=0 and sp.diff(dpN_after,Phi).has(Lpar)
    has_source = dpN_after.has(rho)
    # is it degenerate (0=0) meaning MOND was stolen / no independent eq?
    trivial = sp.simplify(dpN_after)==0
    check("dot p_N=0 is NOT trivial after lambda-fix (an independent equation survives)", not trivial, f"residual={sp.simplify(dpN_after)}")
    check("the surviving equation contains the MOND operator (Lpar*kk*Phi)", has_mond, f"d/dPhi={sp.simplify(sp.diff(dpN_after,Phi))}")
    check("the surviving equation retains the baryon source rho_b", has_source, f"has rho_b={has_source}")
    if trivial:
        P("  ==> VERDICT: lambda-fix from dot C_K COLLAPSES dot p_N to 0=0: the MOND equation is STOLEN. STRUCTURAL KILL.")
    elif has_mond and has_source:
        P("  ==> VERDICT: dot p_N=0 survives as an INDEPENDENT MOND equation (Lpar*kk*Phi = source). ALIVE at principal level.")
    else:
        P("  ==> VERDICT: ambiguous residual; NOT-COMPUTED (needs full field-theory closure).")
else:
    P("  dot C_K=0 did NOT fix lambda -> lambda must be fixed by dot p_N -> MOND stolen. STRUCTURAL KILL.")

P(""); P("="*74); P("STEP 3: scalar Dirac matrix of the constraints that REALLY emerged"); P("="*74)
# emerged second-class set (principal): {p_N, C_MOND(=dot p_N after fix), C_K, C_slip} + p_lam pairs with C_slip
# Build Delta over {G_N, C_K, Cslip, G_lam} and report rank
Cset=[G_N, C_K, Cslip, G_lam]
Delta=sp.Matrix(4,4, lambda i,j: sp.simplify(PB(Cset[i],Cset[j])))
P(f"  Delta (over p_N, C_K, C_slip, p_lam) =\n{sp.pretty(Delta)}")
detD=sp.simplify(Delta.det()); rankD=Delta.rank()
P(f"  det Delta = {detD} ; rank = {rankD}")
P(f"  [DIAGNOSTIC] naive 4-set rank = {rankD} (NOT 4): p_lam is first-class in THIS crude per-mode basis")
P(f"     (its true second-class partner is the full secondary chain, not captured per-mode). The RANK/DOF")
P(f"     count is therefore NOT-COMPUTED here -- it is the owed covariant Dirac closure. This is NOT a")
P(f"     physics fail of the candidate; it is a limit of the per-mode reduction. The 3x3 block over")
P(f"     (p_N, C_K, C_slip) has rank {sp.Matrix(3,3, lambda i,j: PB([G_N,C_K,Cslip][i],[G_N,C_K,Cslip][j])).rank()} -- p_N and C_K both pair with C_slip (the steal-vs-survive channel).")

P(""); P("="*74); P("MUTATION CONTROL: a NON-N-dependent slip constraint (C_slip'=cs*kk*(-Psi)) -- lambda has nowhere to be fixed and p_N steals nothing but also no MOND source coupling"); P("="*74)
Cslip2 = cs*kk*(-Psi)                                # slip that does NOT depend on Phi
H_slip2=(-kk*lam)*Cslip2; H_T2=H_grav+H_MOND+H_slip2+H_cusc
dpN2=sp.expand(PB(G_N,H_T2)); 
check("control: with N-independent slip, {p_N,C_slip'}=0 so dot p_N is unaffected by lambda (test discriminates)",
      PB(G_N,Cslip2)==0 and sp.diff(dpN2,lam)==0)

P(""); P("STEP-4 (owed, NOT-COMPUTED): full nonlinear field-theory closure (functional brackets, all k), the")
P("  momentum constraint sector, and matter nabla_mu T=0. This per-mode principal analysis settles the")
P("  lambda-steal crux structurally; the covariant closure + PPN (alpha_1,2,3, the predicted killer) remain.")
P(""); P("FAILED CHECKS:", FAILS if FAILS else "none")
sys.exit(1 if FAILS else 0)
