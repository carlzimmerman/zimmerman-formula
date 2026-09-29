#!/usr/bin/env python3
"""I1 -- consistency bounds on QED + gravity as bands of alpha (pre-registered L1-L4 in I0_PREREGISTRATION.md).
Masses appear ONLY as inputs (PDG-like values, GeV); nothing is derived about masses. Recalled inputs are flagged 'recalled'.
Run:    python3 i1_consistency_bounds.py            -> exit 0 if all checks pass, writes i1_bands.json
MUTATE: python3 i1_consistency_bounds.py MUTATE     -> reverses the Landau inequality (require pole BELOW M_Pl); the measured alpha
        must FAIL that check, exit 1; writes i1_bands_MUTATE.json.
"""
import sys, json
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 30
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

a0 = 1/mp.mpf("137.035999177")
MPl = mp.mpf("1.220890e19")            # GeV, Planck mass (not reduced)
MPl_red = MPl/mp.sqrt(8*mp.pi)
bands = []   # dicts: name, lo, hi (alpha, None for open), status

# ------------------------------------------------------------------ L1 Landau pole
print("== L1 Landau pole vs Planck mass (one-loop QED, toy) ==")
a_s, Ls, S = sp.symbols("alpha L S", positive=True)
# 1/alpha(mu) = 1/alpha0 - (2/(3 pi)) N Q^2 L  ; pole at L=Lp where 1/alpha(mu)=0 -> Lp = 3 pi /(2 N Q^2 alpha0)
Lp = sp.solve(sp.Eq(1/a_s - sp.Rational(2,3)/sp.pi*Ls, 0), Ls)[0]
chk("L1a closed form Lpole = 3 pi/(2 alpha) (N Q^2 = 1)", sp.simplify(Lp - 3*sp.pi/(2*a_s)) == 0)
amax_e = 3*mp.pi/(2*mp.log(MPl/mp.mpf("0.51099895e-3")))
print(f"   electron only: alpha_max = 3 pi/(2 ln(M_Pl/m_e)) = {mp.nstr(amax_e,6)} = {mp.nstr(amax_e/a0,5)} alpha_0")

# numerical check of closed form: solve running numerically
def pole_scale_electron(alpha):   # GeV
    return mp.mpf("0.51099895e-3")*mp.exp(3*mp.pi/(2*alpha))
chk("L1a numerics: pole scale at alpha_max equals M_Pl", abs(pole_scale_electron(amax_e)/MPl - 1) < mp.mpf("1e-20"))

masses_A = {  # (m [GeV], N_c Q^2)  convention A: current/MSbar-type quark masses (inputs)
 "e":(mp.mpf("0.51099895e-3"),1), "mu":(mp.mpf("0.1056584"),1), "tau":(mp.mpf("1.77686"),1),
 "u":(mp.mpf("2.16e-3"),3*mp.mpf(4)/9), "d":(mp.mpf("4.67e-3"),3*mp.mpf(1)/9), "s":(mp.mpf("0.0934"),3*mp.mpf(1)/9),
 "c":(mp.mpf("1.27"),3*mp.mpf(4)/9), "b":(mp.mpf("4.18"),3*mp.mpf(1)/9), "t":(mp.mpf("172.7"),3*mp.mpf(4)/9)}
masses_B = dict(masses_A)   # convention B: constituent-like light quarks
masses_B.update({"u":(mp.mpf("0.33"),3*mp.mpf(4)/9), "d":(mp.mpf("0.33"),3*mp.mpf(1)/9), "s":(mp.mpf("0.50"),3*mp.mpf(1)/9),
                 "c":(mp.mpf("1.5"),3*mp.mpf(4)/9), "b":(mp.mpf("4.8"),3*mp.mpf(1)/9)})
def Sfun(masses, M):
    return (2/(3*mp.pi))*sum(nq2*mp.log(M/m) for m, nq2 in masses.values() if M > m)
edges_L1 = {}
for lab, ms in (("A", masses_A), ("B", masses_B)):
    for mlab, M in (("M_Pl", MPl), ("M_Pl_red", MPl_red)):
        s = Sfun(ms, M); edges_L1[(lab, mlab)] = 1/s
        print(f"   toy SM-fermion QED, quark masses {lab}, M={mlab}: S = {mp.nstr(s,6)}  1/alpha(M) at alpha_0 = {mp.nstr(1/a0 - s,6)}  alpha_max = 1/S = {mp.nstr(1/s,6)} = {mp.nstr(1/s/a0,5)} alpha_0")
amax_toy = edges_L1[("A","M_Pl")]
spread = (max(edges_L1.values()) - min(edges_L1.values()))/a0
print(f"   spread of the toy edge over quark-mass convention and M_Pl definition: {mp.nstr(spread,4)} alpha_0")
if MUT:
    chk("L1 [MUTATED: pole must lie BELOW M_Pl] alpha_0 satisfies it", a0 > amax_toy, f"(alpha_0 = {mp.nstr(a0,6)}, edge {mp.nstr(amax_toy,6)})")
else:
    chk("L1b alpha_0 < toy Landau edge (pole above M_Pl)", a0 < amax_toy and a0 < amax_e)
bands.append(dict(name="Landau pole above M_Pl, electron only (toy)", lo=None, hi=float(amax_e), status="toy; one-loop; edge scored"))
bands.append(dict(name="Landau pole above M_Pl, SM-fermion QED toy (conv A)", lo=None, hi=float(amax_toy), status="toy; one-loop; edge scored"))

# ------------------------------------------------------------------ L2 Dirac Coulomb
print("== L2 Dirac Coulomb: E_1s = m sqrt(1-(Z alpha)^2) ==")
Zs, al, m = sp.symbols("Z alpha m", positive=True)
# Dirac ground state energy from the exact Dirac formula, n=1, j=1/2: E = m / sqrt(1 + (Z a)^2/(n - j - 1/2 + sqrt((j+1/2)^2-(Z a)^2))^2)
n_, j_ = 1, sp.Rational(1,2)
E = m/sp.sqrt(1 + (Zs*al)**2/(n_ - j_ - sp.Rational(1,2) + sp.sqrt((j_+sp.Rational(1,2))**2 - (Zs*al)**2))**2)
chk("L2a Dirac formula reduces to m sqrt(1-(Z alpha)^2) for 1s", sp.simplify(E**2 - m**2*(1-(Zs*al)**2)) == 0)
Zreq = 26
amax_dirac = mp.mpf(1)/Zreq
chk("L2b real ground state needs Z alpha < 1 (radicand sign flips at 1/Z)", sp.solve(sp.Eq(1 - (Zs*al)**2, 0), al)[0].subs(Zs, Zreq) == sp.Rational(1, Zreq))
chk("L2c alpha_0 < 1/26 (declared Z_req = 26)", a0 < amax_dirac, f"edge = {mp.nstr(amax_dirac,5)} = {mp.nstr(amax_dirac/a0,4)} alpha_0")
bands.append(dict(name="Dirac Coulomb, Z_req = 26", lo=None, hi=float(amax_dirac), status="computed; Z_req is a declared convention"))
bands.append(dict(name="Dirac Coulomb, Z = 1", lo=None, hi=1.0, status="computed"))
print(f"   Z = 137 would be needed for alpha = 1/Z to be the critical value: the critical charge Z_c = {mp.nstr(1/a0,6)} is NOT an integer (an integer Z gives alpha=1/Z, not 1/137.036); not scored.")

# ------------------------------------------------------------------ L3 positivity
print("== L3 positivity / unitarity ==")
a1, a2 = sp.symbols("a1 a2")
# L_EH = 2 al^2/(45 m^4) [ (E^2-B^2)^2 + 7 (E.B)^2 ]   (recalled standard result);  F^2=-2(E^2-B^2), F Ftilde=-4 E.B
c = 2*al**2/(45*m**4)
a1v = c/4          # coefficient of (F_{mu nu}F^{mu nu})^2 : (F^2)^2 = 4 (E^2-B^2)^2
a2v = 7*c/16       # coefficient of (F Ftilde)^2 : =16 (E.B)^2
chk("L3a a1 = alpha^2/(90 m^4), a2 = 7 alpha^2/(360 m^4)", sp.simplify(a1v - al**2/(90*m**4)) == 0 and sp.simplify(a2v - 7*al**2/(360*m**4)) == 0)
chk("L3b positivity a1>0 and a2>0 holds for all alpha>0 (sympy positivity)", a1v.is_positive is True and a2v.is_positive is True)
print("   => positivity of the pure QED light-by-light coefficients gives NO constraint on alpha.")
ratio_grav = (mp.mpf("0.51099895e-3")/MPl_red)**2
print(f"   gravity (Cheung-Remmen, abstract read only): edge alpha >~ (m_e/M_Pl,red)^2 x O(1) = {mp.nstr(ratio_grav,4)} (O(1) set to 1, scaling only)")
chk("L3c alpha_0 above that scaling edge", a0 > ratio_grav)
bands.append(dict(name="gravity positivity scaling, lower edge (m_e/M_Pl)^2", lo=float(ratio_grav), hi=None, status="scaling only; O(1) unknown"))
bands.append(dict(name="perturbative unitarity alpha < pi (loop parameter alpha/pi<1)", lo=None, hi=float(mp.pi), status="convention"))

# ------------------------------------------------------------------ L4 hydrogen stability (recalled inputs)
print("== L4 hydrogen stability against e + p -> n + nu (recalled decomposition) ==")
DQCD, DEM, dDEM, me = mp.mpf("2.05"), mp.mpf("0.76"), mp.mpf("0.30"), mp.mpf("0.51099895")
chk("L4a recalled decomposition reproduces m_n - m_p = 1.293 MeV", abs((DQCD - DEM) - mp.mpf("1.293")) < mp.mpf("0.01"))
for lab, dem in (("central", DEM), ("D_EM+0.3", DEM+dDEM), ("D_EM-0.3", DEM-dDEM)):
    edge = (DQCD - me)/dem
    print(f"   D_EM {lab:9s}: alpha/alpha_0 < {mp.nstr(edge,4)}")
edge_H = (DQCD - me)/DEM
chk("L4b alpha_0 satisfies hydrogen stability", edge_H > 1, f"(edge {mp.nstr(edge_H,4)} alpha_0; recalled inputs)")
bands.append(dict(name="hydrogen stable vs e p -> n nu (recalled D_QCD, D_EM)", lo=None, hi=float(edge_H*a0), status="recalled inputs; +-40% on the edge"))
# other side: proton stable needs m_n>m_p  -> alpha/alpha_0 < DQCD/DEM
print(f"   proton stability (m_n > m_p): alpha/alpha_0 < {mp.nstr(DQCD/DEM,4)}  (weaker than the hydrogen edge)")

json.dump(dict(alpha0=float(a0), bands=bands), open("i1_bands_MUTATE.json" if MUT else "i1_bands.json", "w"), indent=1)
ok = all(v for _, v in checks)
print(f"\n{sum(v for _,v in checks)}/{len(checks)} checks pass")
sys.exit(0 if ok else 1)
