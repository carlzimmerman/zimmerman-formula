#!/usr/bin/env python3
"""I2 -- stellar existence window in alpha (pre-registered S1-S5, Carter-type scaling argument, derived symbolically).
Constants G, m_e, m_p are INPUTS (measured). All O(1) prefactors are symbols c1..c5, varied over [1/10, 10] for the sensitivity.
Run:    python3 i2_stellar_window.py           -> exit 0 if all checks pass, writes i2_bands.json
MUTATE: python3 i2_stellar_window.py MUTATE    -> Thomson opacity exponent alpha^2 replaced by alpha^0; the S1 check (exponent 12) must FAIL, exit 1.
"""
import sys, json, itertools
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 30
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

al, aG, me, mp_, N = sp.symbols("alpha alpha_G m_e m_p N", positive=True)
c1, c2, c3, c4, c5 = sp.symbols("c1:6", positive=True)
p_sigma = 0 if MUT else 2                    # sigma_T ~ alpha^p / m_e^2  (Thomson: p = 2)
Tc   = c1*al**2*mp_                          # nuclear burning (Gamow) temperature
sig  = c2*al**p_sigma/me**2                  # Thomson cross section
Tion = c3*al**2*me                           # surface ionisation scale (Hayashi boundary)
R    = aG*N/Tc                               # virial: R T_c = G M m_p = alpha_G N  (hbar=c=1, G = alpha_G/m_p^2)
L    = R**4*Tc**4/(sig*N)                    # radiative diffusion L ~ R^4 T^4/(sigma N)  (derived in I0 text)
Teff4 = sp.simplify(L/R**2)                  # T_eff^4 = L/R^2
print("T_eff^4 =", sp.simplify(Teff4))
Ncrit = sp.solve(sp.Eq(Teff4, Tion**4), N)[0]
Ncrit = sp.simplify(Ncrit)
print("N_crit  =", Ncrit)
Nmax = c4*aG**sp.Rational(-3,2)             # Chandrasekhar-type maximum
EF   = (N/R**3)**sp.Rational(2,3)/me         # nonrelativistic Fermi energy scale
Nmin = sp.solve(sp.Eq(EF, c5*Tc), N)[0]
Nmin = sp.simplify(Nmin)
print("N_min   =", Nmin)

# S1: N_crit = N_max  -> alpha_G = C alpha^12 (m_e/m_p)^4 ; extract exponent of alpha
aG_sol = sp.solve(sp.Eq(Ncrit, Nmax), aG)
aG_eq = aG_sol[0]
expo = sp.simplify(al*sp.diff(sp.log(aG_eq), al))
Cval = sp.simplify(aG_eq/(al**12*(me/mp_)**4))
print("alpha_G(N_crit=N_max) =", sp.simplify(aG_eq), "   exponent of alpha =", expo, "   C =", Cval)
if MUT:
    chk("S1 [MUTATED opacity] exponent of alpha in the boundary relation is 12", expo == 12, f"(got {expo})")
else:
    chk("S1 derived: alpha_G = C alpha^12 (m_e/m_p)^4 (exponent 12)", expo == 12)
    chk("S1 C = 1 at c_i = 1", sp.simplify(Cval.subs({c1:1,c2:1,c3:1,c4:1})) == 1, f"(symbolic C = {Cval})")
    Nmin_1 = Nmin.subs({c1:1,c5:1}); Ncrit_1 = Ncrit.subs({c1:1,c2:1,c3:1})
    chk("S2 exponents: N_min ~ alpha^(3/2), N_crit ~ alpha^6 at fixed alpha_G, m_e, m_p",
        sp.simplify(al*sp.diff(sp.log(Nmin_1),al)) == sp.Rational(3,2) and sp.simplify(al*sp.diff(sp.log(Ncrit_1),al)) == 6)

# ---------------- numerics
G_over = mp.mpf("1.220890e19")               # M_Pl GeV
mpr = mp.mpf("0.938272088"); mer = mp.mpf("0.51099895e-3")
aGv = (mpr/G_over)**2
a0 = 1/mp.mpf("137.035999177")
print(f"alpha_G = (m_p/M_Pl)^2 = {mp.nstr(aGv,5)},  m_e/m_p = {mp.nstr(mer/mpr,5)}")
subs_num = {aG: sp.Float(str(aGv),30), me: sp.Float(str(mer),30), mp_: sp.Float(str(mpr),30)}
fN = {k: sp.lambdify((al, c1, c2, c3, c4, c5), v.subs(subs_num), "mpmath") for k, v in (("min",Nmin),("crit",Ncrit),("max",Nmax))}
def edges(cs):
    """alpha interval where N_min < N_crit < N_max for constants cs=(c1..c5)."""
    up = lambda a: mp.log(fN["crit"](a,*cs)/fN["max"](a,*cs))       # <0 below the upper edge (log ratio: values span 1e60)
    lo = lambda a: mp.log(fN["crit"](a,*cs)/fN["min"](a,*cs))       # >0 above the lower edge
    grid = [mp.mpf(10)**(mp.mpf(k)/40) for k in range(-160, 1)]   # 1e-4 .. 1
    hi_e = lo_e = None
    for x, y in zip(grid[:-1], grid[1:]):
        if up(x)*up(y) < 0: hi_e = mp.findroot(up, (x, y), solver="bisect", tol=1e-25, maxsteps=500)
        if lo(x)*lo(y) < 0: lo_e = mp.findroot(lo, (x, y), solver="bisect", tol=1e-25, maxsteps=500)
    return lo_e, hi_e
if MUT:
    print(f"\n{sum(v for _,v in checks)}/{len(checks)} checks pass"); sys.exit(0 if all(v for _, v in checks) else 1)
lo1, hi1 = edges((1,1,1,1,1))
print(f"point estimate (all c=1): alpha_lo = {mp.nstr(lo1,5)} = {mp.nstr(lo1/a0,4)} alpha_0 ;  alpha_hi = {mp.nstr(hi1,5)} = {mp.nstr(hi1/a0,4)} alpha_0")
if not MUT:
    chk("S3 alpha_0 lies inside the stellar band (c=1)", lo1 < a0 < hi1)
    # S4 sensitivity: all corners of c_i in {1/10, 10}
    lo_all, hi_all = [], []
    for cs in itertools.product([mp.mpf(1)/10, mp.mpf(10)], repeat=5):
        l, h = edges(cs)
        if l is not None: lo_all.append(l)
        if h is not None: hi_all.append(h)
    print(f"S4 corner scan over c_i in [1/10,10] (32 corners): lower edge in [{mp.nstr(min(lo_all),4)}, {mp.nstr(max(lo_all),4)}] = [{mp.nstr(min(lo_all)/a0,3)}, {mp.nstr(max(lo_all)/a0,3)}] alpha_0;"
          f" upper edge in [{mp.nstr(min(hi_all),4)}, {mp.nstr(max(hi_all),4)}] = [{mp.nstr(min(hi_all)/a0,3)}, {mp.nstr(max(hi_all)/a0,3)}] alpha_0")
    chk("S4 alpha_0 inside the band at every corner OR reported: count of corners containing alpha_0",
        True, "(reported: %d of 32 corners contain alpha_0)" % sum(1 for cs in itertools.product([mp.mpf(1)/10, mp.mpf(10)], repeat=5) for l,h in [edges(cs)] if l is not None and h is not None and l < a0 < h))
    # S4b (added in Amendment 1): the factor-10 corner scan is dominated by c3^8; report gentler ranges and one-at-a-time sensitivity
    corner = {}
    for fac in (2, 3):
        lo_f, hi_f, cnt = [], [], 0
        for cs in itertools.product([mp.mpf(1)/fac, mp.mpf(fac)], repeat=5):
            l, h = edges(cs)
            lo_f.append(l); hi_f.append(h)
            if l is not None and h is not None and l < a0 < h: cnt += 1
        corner[fac] = (float(min(lo_f)), float(max(lo_f)), float(min(hi_f)), float(max(hi_f)))
        print(f"S4b corners c_i in [1/{fac},{fac}]: lower edge in [{mp.nstr(min(lo_f)/a0,3)}, {mp.nstr(max(lo_f)/a0,3)}] alpha_0; upper edge in [{mp.nstr(min(hi_f)/a0,3)}, {mp.nstr(max(hi_f)/a0,3)}] alpha_0; corners containing alpha_0: {cnt}/32")
    for i, nm in enumerate(("c1 (T_c/alpha^2 m_p)", "c2 (sigma_T m_e^2/alpha^2)", "c3 (T_ion/alpha^2 m_e)", "c4 (N_max alpha_G^1.5)", "c5 (E_F/T_c at ignition)")):
        row = []
        for f in (mp.mpf(1)/3, mp.mpf(3)):
            cs = [1]*5; cs[i] = f
            l, h = edges(tuple(cs)); row.append((l/a0, h/a0))
        print(f"S4b one at a time {nm:30s}: x1/3 -> [{mp.nstr(row[0][0],3)}, {mp.nstr(row[0][1],3)}]  x3 -> [{mp.nstr(row[1][0],3)}, {mp.nstr(row[1][1],3)}] (units alpha_0)")
    # S6 (Amendment 1): constants calibrated on real stars (RECALLED numbers), reported only
    Creq = aGv/((mer/mpr)**4*a0**12)
    c2r = 8*mp.pi/3                                   # Thomson sigma_T = (8 pi/3) alpha^2/m_e^2 (exact)
    c1r = (mp.mpf("1.57e7")*mp.mpf("8.617333e-5")*1e-9)/(a0**2*mpr)    # T_c(Sun)=1.57e7 K (recalled)
    c3r = (mp.mpf("4000")*mp.mpf("8.617333e-5")*1e-9)/(a0**2*mer)      # Hayashi/H- boundary T_eff ~ 4000 K (recalled, rough)
    c4r = (mp.mpf("1.44")*mp.mpf("1.98847e30")/mp.mpf("1.67262e-27"))*aGv**mp.mpf("1.5")  # M_Chandra = 1.44 Msun (recalled)
    Ccal = c2r**2*c3r**8/(c1r**4*c4r**2)
    aCal = (aGv/(mer/mpr)**4/Ccal)**(mp.mpf(1)/12)
    print(f"S6 calibrated constants (recalled): c1={mp.nstr(c1r,3)} c2={mp.nstr(c2r,4)} c3={mp.nstr(c3r,3)} c4={mp.nstr(c4r,3)} -> C = {mp.nstr(Ccal,3)}; alpha_C(calibrated) = {mp.nstr(aCal,4)} = {mp.nstr(aCal/a0,3)} alpha_0")
    print(f"   a factor {mp.nstr(Creq/Ccal,3)} in C moves alpha only by the 12th root: this is why the window looks narrow in alpha")
    chk("S6 calibrated-constant equality is not a 1e-3 hit", abs(aCal/a0 - 1) > 1e-3)
    # S5 equality reading
    aC = (aGv/(mer/mpr)**4)**(mp.mpf(1)/12)
    print(f"S5 equality reading C=1: alpha_C = (alpha_G (m_p/m_e)^4)^(1/12) = {mp.nstr(aC,6)} = 1/{mp.nstr(1/aC,6)} ; alpha_C/alpha_0 = {mp.nstr(aC/a0,6)}")
    Creq = aGv/((mer/mpr)**4*a0**12)
    print(f"   C required for an exact match: {mp.nstr(Creq,5)} ;  a 1e-3 hit needs C within {mp.nstr(12e-3*Creq,3)} of it (1.2%)")
    chk("S5 C=1 equality is NOT a 1e-3 hit (declared expectation)", abs(aC/a0 - 1) > 1e-3)
    chk("S5 the required C is O(1) (between 1 and 10), i.e. the coincidence holds only at scaling level", 1 < Creq < 10)
    json.dump(dict(alpha0=float(a0), alpha_lo_c1=float(lo1), alpha_hi_c1=float(hi1),
                   lo_corner_min=float(min(lo_all)), lo_corner_max=float(max(lo_all)), hi_corner_min=float(min(hi_all)), hi_corner_max=float(max(hi_all)),
                   alpha_C=float(aC), C_required=float(Creq), alpha_C_calibrated=float(aCal), corners={str(k): v for k, v in corner.items()}), open("i2_bands.json", "w"), indent=1)
ok = all(v for _, v in checks)
print(f"\n{sum(v for _,v in checks)}/{len(checks)} checks pass")
sys.exit(0 if ok else 1)
