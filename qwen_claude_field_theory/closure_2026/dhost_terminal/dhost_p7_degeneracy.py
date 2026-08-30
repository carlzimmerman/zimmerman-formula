#!/usr/bin/env python3
"""TERMINAL P7 calc: does the DHOST degeneracy escape the P7 collision (screening that protects PPN
also killing the kinetic normalization) where plain khronometric could NOT? 2-field Hessian model:
frame mode pi (screened coupling) + its higher-derivative partner psi; DHOST degeneracy = det H = 0.
Verify a WIN as hard as a loss -- this is the reviewer's allowed-set S; verdict HELD."""
import sympy as sp

sig, Kpsi, b = sp.symbols('sigma K_psi b', positive=True)   # sigma=e^-y (screening), Kpsi finite DHOST norm
# khronometric/stiff-vector P7: the frame mode's kinetic norm K_pi IS the screened coupling: K_pi = sigma.
Kpi = sig
H = sp.Matrix([[Kpi, b],[b, Kpsi]])
print("=== the P7 setup (why plain khronometric / the stiff-vector died) ===")
print("   Frame mode pi: preferred-frame PPN coupling ~ sigma=e^-y (screened for Cassini). In khronometric")
print("   the SAME sigma is the kinetic normalization K_pi=sigma => K_pi->0 in the solar system =>")
print("   STRONG COUPLING (P7). The stiff-vector (FM-000004) had NO second field to rescue K_pi. DEAD.")

print("\n=== the DHOST NEW element: a second field psi + the DEGENERACY det H = 0 ===")
det = sp.simplify(H.det())
print(f"   det H = {det} ;  DHOST degeneracy imposes det H = 0  =>  b^2 = K_pi K_psi = sigma*K_psi")
b_deg = sp.sqrt(Kpi*Kpsi)
eig = H.subs(b, b_deg).eigenvals()
print(f"   eigenvalues at degeneracy: {list(eig.keys())}  (one is 0 = the removed Ostrogradsky mode)")
lam_phys = sp.simplify(Kpi + Kpsi)      # nonzero eigenvalue (trace, since the other is 0)
print(f"   PHYSICAL mode kinetic norm = nonzero eigenvalue = K_pi + K_psi = {lam_phys}")
print(f"   as sigma=e^-y -> 0 (solar system):  K_phys -> {sp.limit(lam_phys, sig, 0)} = K_psi  (FINITE!)")
print("   => the DHOST degeneracy lets the PHYSICAL mode's kinetic norm come from the DHOST sector K_psi,")
print("   INDEPENDENT of the screening sigma. K_phys stays FINITE as sigma->0. P7's 'kinetic norm ->0'")
print("   is STRUCTURALLY AVOIDED -- a genuine escape mechanism the stiff-vector never had.")

print("\n=== the physical eigenvector: where does the PPN coupling sit? ===")
v = sp.Matrix([b_deg, Kpsi])            # eigenvector for lam_phys
v = sp.simplify(v/sp.sqrt((v.T*v)[0]))
print(f"   physical eigenvector ~ (sqrt(sigma), sqrt(K_psi)) : pi-admixture ~ sqrt(sigma) -> 0 as sigma->0")
print("   The frame(pi)-coupling that generates alpha_1,alpha_2 enters the physical mode only through the")
print("   sqrt(sigma) admixture => alpha_1,alpha_2 ~ (sqrt(sigma)*coupling)^2 : still SCREENED, while")
print("   K_phys=K_psi FINITE. So structurally {alpha screened} AND {no strong coupling} CAN coexist.")

print("\n=== HELD VERDICT (the reviewer's allowed set S is NOT excluded) ===")
print("CORRECTION to the earlier 'DHOST collapses into the closed frame family': that was too strong.")
print("The DHOST degeneracy provides a STRUCTURAL P7-ESCAPE the closed khronometric/stiff-vector family")
print("lacked -- the physical mode's kinetic norm can come from the DHOST sector (finite) while the")
print("preferred-frame coupling stays screened. So P7 does NOT automatically close DHOST MOND.")
print("TRUSTED: c_par^2->2, c_perp^2->1; the degeneracy gives finite K_phys. NOT YET A THEOREM:")
print("whether the FULL DHOST reduction (c_T=1 + degeneracy conditions + mu~y) actually lands in")
print("S = {mu~y, c_T=1, K_pi>0, 0<c_par^2<=1, |alpha_1|<<1, |alpha_2|<<1}. That explicit algebra --")
print("the g_0i/g_00 preferred-frame reduction from the SAME action -- is the decisive remaining calc.")
print("=> single-metric MOND is NOT closed. S=empty => no-go; S nonempty => DHOST MOND is the lead")
print("theory. This is the exact terminal open algebra. Verdict HELD; do not call the program closed.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"dhost-p7-degeneracy","status":"HELD-OPEN-S-NOT-EXCLUDED",
 "certificate":("CORRECTS the earlier over-strong 'DHOST collapses to closed frame family'. 2-field "
   "degeneracy (det H=0, b^2=sigma*K_psi): the PHYSICAL mode kinetic norm = K_pi+K_psi -> K_psi FINITE "
   "as the screening sigma=e^-y->0, so the DHOST degeneracy provides a structural P7-ESCAPE the "
   "stiff-vector/khronometric family lacked (physical-mode norm from the DHOST sector, independent of "
   "the screening; pi-admixture ~sqrt(sigma) keeps alpha screened). => P7 does NOT auto-close DHOST "
   "MOND. Trusted: c_par^2=2, c_perp^2=1, finite K_phys. NOT a theorem yet: whether the full reduction "
   "lands in S={mu~y, c_T=1, K_pi>0, 0<c_par^2<=1, |a1|<<1, |a2|<<1}. The explicit g_0i/g_00 PPN "
   "reduction from the same action is the decisive remaining calc: S=empty=>single-metric no-go; S "
   "nonempty=>DHOST MOND is the lead theory. Single-metric NOT closed; verdict HELD."),
 "numeric_values":{"K_phys_limit":"K_psi (finite)","P7":"escaped structurally","S":"not excluded"}}))
