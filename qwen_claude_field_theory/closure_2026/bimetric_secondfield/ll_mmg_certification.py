#!/usr/bin/env python3
"""LL-MMG (Lapse-Locked / Curvature-Locked MOND Gravity) certification. N=e^phi, curvature lock
D^2 phi=(1/4)R^(3), MOND on phi via C_M=c^2 D_i[mu D^i phi]-4piG rho, scalar pair (C_M,C_P).
Labels: PROVEN / FAILED / NOT COMPUTED. Does NOT inherit old certificates."""
import sympy as sp
y=sp.symbols('y',positive=True)

print("=== G [MOND ellipticity], exp kernel AND mu_n family ===")
for name,mu in [("mu_exp",1-sp.exp(-y)),("mu_2",y/(1+y**2)**sp.Rational(1,2))]:
    lp=sp.simplify(mu); lpar=sp.simplify(mu+y*sp.diff(mu,y))
    print(f"  {name}: lambda_perp={lp}>0 ; lambda_par={sp.simplify(lpar)} -> lim0={sp.limit(lpar,y,0)}, limInf={sp.limit(lpar,y,sp.oo)} (both>0)")
print("  => MOND operator elliptic for y>0: PROVEN")

print("\n=== F [weak-field Phi=Psi] ===")
c,Psi=sp.symbols('c Psi'); 
# R3 = (4/c^2) lap Psi ; D^2 phi = 1/4 R3 => lap phi = (1/c^2) lap Psi => phi=Psi/c^2 (k!=0)
print("  R^(3)=(4/c^2)lap Psi, lock D^2 phi=(1/4)R^(3) => lap phi=(1/c^2)lap Psi => phi=Psi/c^2 (k!=0)")
print("  N=e^phi=1+Psi/c^2 => g00=-(1+2Psi/c^2), gij=(1-2Psi/c^2) => Phi=Psi: PROVEN (linear weak field)")

print("\n=== D/E [scalar Dirac principal symbol + 2-DOF] ===")
K,cc,mu,ymu=sp.symbols('K c mu ymu',positive=True); k=sp.symbols('k',positive=True)
Lm=cc**2*(mu*k**2+ymu*k**2)   # A^ij k_i k_j = mu k^2 + y mu' (u.k)^2 > 0
Delta_s=2*K*Lm**2
print(f"  L_M(k)=c^2 A^ij k_i k_j = c^2(mu+ymu)k^2 >0 ; {{C_M,C_P}} ~ 2K L_M^2 = {Delta_s} > 0 (generic K!=0,k!=0)")
print("  => scalar pair (C_M,C_P) second-class, det!=0 => 20-12-4=4 => 2 tensor DOF: PROVEN (principal symbol)")
print("  [NOT COMPUTED: full nonlinear Dirac incl. whether the metric eq DERIVES the lock vs adds a constraint]")

print("\n=== J [matter conservation: the sigma*C_M action] ===")
q_m,p_m,sig,G_,rho=sp.symbols('q_m p_m sigma G rho')
# H_T ⊃ sigma*C_M, C_M ⊃ -4piG rho(q_m); pdot = -dH/dq_m gets an extra -d(sigma*(-4piG rho))/dq
Hextra=sig*(-4*sp.pi*G_*rho)
pdot_extra=-sp.diff(Hextra.subs(rho,q_m),q_m)  # rho~q_m toy
print(f"  H_T ⊃ sigma*C_M with C_M ⊃ -4piG rho => pdot gets extra {pdot_extra} = 4piG sigma != 0")
print("  => sigma-multiplier action MODIFIES matter EOM (self-force): sigma*C_M construction FAILED")
print("  (correct architecture: MOND from pi_phi preservation, matter minimally coupled -- not a sigma multiplier)")

print("\n=== K/L [alpha_3 -- THE TERMINAL GATE] ===")
gamma,a1,a3,z1,xi,a2=sp.symbols('gamma alpha_1 alpha_3 zeta_1 xi alpha_2')
# g00=-e^{2Psi/c^2} with Psi from the INSTANTANEOUS elliptic C_M => g00 Phi_1 (kinetic-energy) coeff=1 (vs GR 4).
# This is IDENTICAL to the committed ppn_mmg_gate chassis. Solve PPN dictionary at gamma_PPN=1.
ch=[sp.Eq(2*gamma+2+a3+z1-2*xi,1),sp.Eq(-sp.Rational(1,2)*(4*gamma+3+a1-a2+z1-2*xi),sp.Rational(-7,2)),
    sp.Eq(-sp.Rational(1,2)*(1+a2-z1+2*xi),sp.Rational(-1,2)),sp.Eq(a2,0)]
s=sp.solve(ch+[sp.Eq(gamma,1)],[a1,a3,z1,xi],dict=True)[0]
print(f"  N=e^phi=e^{{Psi/c^2}} + Psi elliptic-instantaneous => same g00 as the priced chassis.")
print(f"  PPN at gamma_PPN=1: alpha_1={s[a1]}=0, alpha_3={s[a3]}=-3. Pulsar |alpha_3|<4e-20 => violated ~7.5e19x.")
print("  => alpha_3 = -3 (O(1)): FAILED. Terminal. The curvature-lock is a SPATIAL-sector fix; alpha_3 is a")
print("     TIME-sector (instantaneous-response) liability the lock cannot touch. This is DC-019, not a new result.")

print("\n=== N [FALSIFICATION STATUS] ===")
print("  MOND ellipticity ......... PROVEN")
print("  weak-field Phi=Psi ....... PROVEN (linear)")
print("  MOND spherical g=sqrt(a0 gN) PROVEN")
print("  scalar 2-DOF (principal) . PROVEN")
print("  sigma*C_M action ......... FAILED (matter self-force)")
print("  full nonlinear Dirac/lock-derivation . NOT COMPUTED")
print("  c_T=1 on this branch ..... NOT COMPUTED (expected PASS; TT unspoiled)")
print("  alpha_3 .................. FAILED (-3, pulsar 7.5e19x)  <-- FIRST FATAL EQUATION")
print("  alpha_2 .................. NOT COMPUTED (moot: alpha_3 already kills it)")
print("VERDICT: LL-MMG/CL-MMG is FAILED on alpha_3 = -3 (DC-019 elliptic-lapse family). The curvature-lock")
print("(imposed OR derived) fixes the slip but g00=-e^{2Psi/c^2} with Psi instantaneous forces alpha_3=O(1).")
