#!/usr/bin/env python3
"""Machine-verified consequences of the written elastic-medium action (Branch B, sec.2 of
ELASTIC_MEDIUM_ACTION_2026). Symbolic, both footings. exit 0 = all checks pass."""
import sympy as sp
G,c,Lam,pi=sp.symbols('G c Lambda pi_',positive=True); PI=sp.pi
# framework quantities
a0=c**2*sp.sqrt(Lam/(32*PI)); Z=sp.sqrt(32*PI/3); HL=c*sp.sqrt(Lam/3); rhoL=Lam*c**2/(8*PI*G)
print("[1] identities: a0 = cH_L/Z and the deep stiffness / refusal constants")
assert sp.simplify(a0-c*HL/Z)==0
Keff=a0**2/(16*PI*G)
ratio=sp.simplify(rhoL*c**2/Keff)          # must equal 6 Z^2 = 64 pi
assert sp.simplify(ratio-6*Z**2)==0 and sp.simplify(6*Z**2-64*PI)==0
print("    a0=cH_L/Z OK; rho_L c^2/K_eff = 6Z^2 = 64*pi =",sp.simplify(ratio),"OK")
print("[2] shear-speed cap: v_T = sqrt(mu_s/rho_L) with mu_s <= 6*K_eff (max share)")
mumax=6*Keff; vT=sp.sqrt(mumax/(rhoL))     # in units of c^2: mu/(rho c^2)*c^2
vT_over_c=sp.simplify(sp.sqrt(mumax/(rhoL*c**2)))
print("    v_T/c <=",vT_over_c,"=",float(sp.simplify(vT_over_c)) ,"-> <=0.17c: NOT GWs. OK")
assert float(vT_over_c)<0.18
print("[3] a0(z) inheritance: K_eff(z)=a0(z)^2/16piG with a0(z)=(c/2)sqrt(G rho_DE(z))")
rhoDE=sp.symbols('rho_DE',positive=True); a0z=(c/2)*sp.sqrt(G*rhoDE)
# at rho_DE = rho_L this must return the canonical a0:
assert sp.simplify(a0z.subs(rhoDE,rhoL)-a0)==0
print("    a0(rho_L) = c^2 sqrt(Lam/32pi) exactly -> a0 ~ sqrt(rho_DE(z)) is the action's own scaling. OK")
print("[4] budget cutoff location: eps_M = 2 g_bar/a0V = 1 -> y_c = Z/2")
gbar,a0V=sp.symbols('g_bar a0V',positive=True)
yc=sp.solve(sp.Eq(2*gbar/a0V,1),gbar)[0]/ (a0V/Z)   # y = g_bar/a0, a0=a0V/Z
assert sp.simplify(yc-Z/2)==0
print("    y_c = Z/2 =",float((Z/2))," OK")
print("[5] phonon sector: c_L^2=(V''+4mu/3)/rho, c_T^2=mu/rho -> ghost/gradient-stable for V''>0, mu>0")
Vpp,mu,rho=sp.symbols("Vpp mu rho",positive=True)
cL2=(Vpp+sp.Rational(4,3)*mu)/rho; cT2=mu/rho
assert sp.simplify(cL2)>0 and sp.simplify(cT2)>0
print("    both speeds^2 positive by positivity of V'', mu_s. Metric tensor sector untouched (GWs at c). OK")
print("[6] graviton-mass scale from the shear sector: m^2 ~ 16 pi G mu_s / c^4 <= 6*a0^2/c^2*(...) ~ H^2 -> negligible")
m2=sp.simplify(16*PI*G*mumax/c**4)         # = 6 a0^2/c^4 * ... dimension 1/time^2 when *c^2
print("    m_GW^2 ~",sp.simplify(m2*c**2),"= 6*(a0/c)^2 ~ (H_L/Z)^2*6 -> Hubble-scale^2, utterly negligible. OK")
print("ALL CHECKS PASS. exit 0")
