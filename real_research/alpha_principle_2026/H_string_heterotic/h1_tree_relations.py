#!/usr/bin/env python3
"""H1 -- tree-level gauge/gravity relations of the heterotic, Type I and Horava-Witten regimes: which quantities are free, which forced.
Pre-registered R1-R4 in H0_PREREGISTRATION.md.
Sources (FULL TEXT read): Witten hep-th/9602070 Eq. 1.4,1.5,1.10,1.11,1.13,1.7,1.14; Dienes hep-th/9602045 Eq. 2.6,2.10,10.1,10.4-10.6;
Kaplunovsky erratum hep-th/9205068 Eq. (26) and k g^2 = 32 pi/(alpha' M_P^2).  Formulas are TAKEN AS PRINTED (inputs), everything else is computed here.
Run: python3 h1_tree_relations.py [MUTATE]   (MUTATE: drop the factor 2 in Kaplunovsky's Lambda, i.e. the pre-erratum form; R3 must FAIL, exit 1)"""
import sys
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

phi, V, ap, kap, rho = sp.symbols("phi V alpha_p kappa rho", positive=True)

# ---------------- R1: the three regimes as printed (Witten) ----------------
G_het = sp.exp(2*phi)*ap**4/(64*sp.pi*V);   al_het = sp.exp(2*phi)*ap**3/(16*sp.pi*V)          # Eq. 1.4
G_I   = sp.exp(2*phi)*ap**4/(64*sp.pi*V);   al_I   = sp.exp(phi)*ap**3/(16*sp.pi*V)             # Eq. 1.10 (phi = Type I dilaton, V = V_I)
G_HW  = kap**2/(16*sp.pi**2*V*rho);         al_HW  = (4*sp.pi*kap**2)**sp.Rational(2, 3)/(2*V)   # Eq. 1.13
print("R1 relations as printed:")
print("  het   : G_N/alpha_G =", sp.simplify(G_het/al_het), "  (Witten Eq. 1.5: alpha'/4)")
print("  Type I: G_N/alpha_G =", sp.simplify(G_I/al_I), "  (Witten Eq. 1.11: e^{phi_I} alpha'/4)")
print("  H-W   : G_N/alpha_G =", sp.simplify(G_HW/al_HW))
chk("R1a heterotic G_N = alpha_G alpha'/4 (Witten 1.5) follows from 1.4", sp.simplify(G_het - al_het*ap/4) == 0)
chk("R1b Type I G_N = e^{phi_I} alpha_G alpha'/4 (Witten 1.11) follows from 1.10", sp.simplify(G_I - sp.exp(phi)*al_I*ap/4) == 0)
chk("R1c H-W alpha_G is independent of rho (the interval length)", sp.diff(al_HW, rho) == 0)

MKK = V**sp.Rational(-1, 6)
def jac_rank(outs, params):
    J = sp.Matrix([[sp.diff(o, p) for p in params] for o in outs])
    d = sp.simplify(J.det())
    return J.rank(), d
r_het, d_het = jac_rank([G_het, al_het, MKK], [phi, V, ap])
r_I, d_I = jac_rank([G_I, al_I, MKK], [phi, V, ap])
r_HW, d_HW = jac_rank([G_HW, al_HW, MKK], [kap, V, rho])
print(f"R1 Jacobian ranks of (params)->(G_N, alpha_G, M_KK=V^(-1/6)): het {r_het} (det {d_het}), Type I {r_I} (det {d_I}), H-W {r_HW} (det {d_HW})")
chk("R1d ranks are (3,3,3): NO tree-level equality among (G_N, alpha_G, M_KK) in any regime (only inequalities from e^{2phi}<=1, V>=alpha'^3)", (r_het, r_I, r_HW) == (3, 3, 3))
# the only equality: the definition of alpha' (string scale) from (G_N, alpha_G).  Solve and show alpha_G itself remains a free function of (phi, V/alpha'^3)
Gs, als = sp.symbols("G_N alpha_G", positive=True)
ap_from = sp.simplify(4*Gs/als)
print("R1  forced (het): alpha' = 4 G_N/alpha_G (Witten conv.)  =>  M_s^2 = alpha_G/(4 G_N).  alpha_G = e^{2phi} alpha'^3/(16 pi V): a FREE function of (phi, V/alpha'^3).")
free_dim = sp.simplify(sp.diff(al_het, phi))
chk("R1e d alpha_G/d phi != 0 and d alpha_G/d V != 0 at fixed alpha': the coupling is a continuous modulus (2 free real parameters phi, V/alpha'^3)", free_dim != 0 and sp.diff(al_het, V) != 0)

# ---------------- R2: conventions ----------------
conv = {"Kaplunovsky erratum: k g^2 = 32 pi G/alpha'": sp.Rational(1, 4),   # 8 pi G/alpha' = g^2/4
        "Witten Eq.1.5: G = alpha_G alpha'/4  (g^2=4 pi alpha)": sp.Rational(1, 2),  # 8 pi G/alpha' = 2 pi alpha = g^2/2
        "Dienes Eq.2.6: 8 pi G/alpha' = k g^2": sp.Integer(1)}
print("\nR2 (8 pi G_N/alpha') / g^2 in three sources:")
for k, v in conv.items(): print(f"   {k:55s} -> {v}")
vals = list(conv.values())
print(f"   spread max/min = {max(vals)/min(vals)} (a factor 4).  Origin: generator normalisation (Tr_fund = 1/2 vs 1 in Kaplunovsky's footnote) and the definition of alpha'.  NOT resolved from the papers here.")
chk("R2 three sources disagree on the O(1) coefficient (1/4, 1/2, 1) -- reported convention offsets", len(set(vals)) == 3)
# consistency of the Horava-Witten form Dienes 10.6 with Witten 1.13 : ratio should be the same factor 2 as the weak-coupling forms
HW_D = 16*sp.pi**3*(4*sp.pi/kap)**sp.Rational(2, 3)*rho*G_HW                # = g^2 k as printed in Dienes 10.6
HW_W = 4*sp.pi*al_HW                                                         # g^2 from Witten alpha_G
ratio = sp.simplify(HW_W/HW_D)
print(f"   H-W: (4 pi alpha_G^Witten)/(g^2 k from Dienes 10.6) = {ratio}   (weak-coupling Witten/Dienes offset was 2)")
chk("R2b the H-W offset between Witten and Dienes equals the weak-coupling offset (same factor 2) -> a normalisation of g, not physics", ratio == 2)

# ---------------- R3: Kaplunovsky's corrected unification scale ----------------
MP = 1.2209e19   # GeV, G_N^(-1/2)  (measured G_N: input)
c = float(mp.e**((1 - mp.euler)/2)*mp.mpf(3)**(-mp.mpf(3)/4))
coef = c/(4*float(mp.pi))*MP
print(f"\nR3 c = e^((1-gamma)/2) 3^(-3/4) = {c}; Lambda/g = c M_P/(4 pi) = {coef:.5e} GeV (Dienes 2.10 / Kaplunovsky (26): 5.27e17)")
g, Gsym = sp.symbols("g G", positive=True)
csym = sp.Symbol("c", positive=True)
ap_K = 32*sp.pi*Gsym/g**2                                                    # k g^2 = 32 pi G/alpha' with k = 1
fac = 1 if MUT else 2
Lam_sym = fac*csym/sp.sqrt(2*sp.pi*ap_K)
target_sym = csym*g/(4*sp.pi*sp.sqrt(Gsym))
chk("R3a algebra: 2c/sqrt(2 pi alpha') with alpha' = 32 pi G/g^2 equals c g M_P/(4 pi)", sp.simplify(Lam_sym - target_sym) == 0)
lam_num = coef*(1 if not MUT else 0.5)
chk("R3b numerical coefficient within 0.3 percent of 5.27e17 GeV", abs(lam_num/5.27e17 - 1) < 3e-3, f"({lam_num:.4e})")
ms_over = MP/float(mp.sqrt(32*mp.pi))   # 1/sqrt(alpha') per unit g in Kaplunovsky convention
print(f"   in this convention 1/sqrt(alpha')/g = {ms_over:.4e} GeV; Lambda/(1/sqrt(alpha')) = {coef/ms_over:.4f}  (one-loop scheme factor between the unification scale and the string mass scale)")

# ---------------- R4: Witten's bounds, reported ----------------
G_N = 1/MP**2
al, MG = 1/25, 2e16
b17 = al**(4/3)/MG**2
b114 = al**2/MG**2
print(f"\nR4 (order-of-magnitude, O(1) dropped as printed) G_N = {G_N:.3e} GeV^-2; weak-coupling bound alpha^(4/3)/M^2 = {b17:.3e} (x{b17/G_N:.0f}); strong-coupling bound alpha^2/M^2 = {b114:.3e} (x{b114/G_N:.1f})")
print("   => in the weak-coupling heterotic regime the tree-level G_N is an INEQUALITY on V, not a prediction of alpha; at strong coupling the gap closes.  REPORTED, not scored.")
Gcrit = al**2/(16*float(mp.pi)**2)/MG**2   # Witten Eq. 1.15 with the integral set to 1 in units M_GUT^-2 (order-one factor unknown)
print(f"   Witten Eq.1.15 critical G_N (integral = 1 x M_GUT^-2, UNKNOWN O(1)) = {Gcrit:.3e} GeV^-2 = {Gcrit/G_N:.1f} x measured G_N: an order-of-magnitude statement only")
# R4 is REPORTED, not scored (pre-registration).  See Amendment 1 for the removed unregistered check.

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
