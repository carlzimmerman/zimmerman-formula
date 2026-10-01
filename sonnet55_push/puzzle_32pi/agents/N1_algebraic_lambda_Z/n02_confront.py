"""n02: confront the declared menu's Z values with lane V's a0 numbers; decoys; Omega_Lambda; kernel table.
Reads n01_Z.json. Data numbers are lane V's (read, not refit). a0 in 1e-10 m/s^2."""
import json, math, numpy as np, sys, hashlib
npass = nfail = 0
def chk(name, cond):
    global npass, nfail
    if cond: npass += 1; print("PASS", name)
    else: nfail += 1; print("FAIL", name)
chk("predeclaration hash matches file", hashlib.sha256(open("PREDECLARED.md","rb").read()).hexdigest() == open("PREDECLARED.sha256").read().split()[0])
Zm = json.load(open("n01_Z.json"))
c = 2.99792458e8; Mpc = 3.0856775814913673e22
OmL = 0.685
def cH0(H0): return c*H0*1e3/Mpc          # m/s^2
def Zdata(a0, H0, footing):                # a0 in 1e-10
    return cH0(H0)*(math.sqrt(OmL) if footing == "Lam" else 1.0)/(a0*1e-10)
# scenarios: (label, a0, rel err)
scen = [("E ensemble (1.097, 12.2%)", 1.097, .122), ("record quoted (1.0766, 5.44%)", 1.0766, .0544),
        ("record + systematics (1.081, 16.1%)", 1.081, .161), ("Upsilon-free alpha1 (1.083, 8.2%)", 1.083, .082),
        ("Upsilon-free RAR (0.873, 8.2%)", 0.873, .082), ("Upsilon-free simple (0.881, 8.2%)", 0.881, .082),
        ("Upsilon-free standard (1.117, 8.2%)", 1.117, .082), ("MLS16 RAR fixed (1.20, 20.1%)", 1.20, .201)]
cands = {"F sqrt(32pi/3)": math.sqrt(32*math.pi/3), "V 6": 6.0, "M 2pi": 2*math.pi,
         "N1 Nariai@L 3sqrt3 (A1)": Zm["A1"], "A7 4sqrt3 (Schw ISCO)": Zm["A7"], "A11a 2": 2.0, "A2-5 sqrt3": Zm["A2"],
         "A8 sqrt3/2": Zm["A8"], "A6 4/(3sqrt3)": Zm["A6"], "A10 1/sqrt3": Zm["A10"], "A11b 1": 1.0}
H0s = {"Planck 67.4": 67.4, "SH0ES 73.0": 73.0}
sH = 0.0074*1 + 0  # H0 +-0.5/67.4 = 0.74% ; added in quadrature with OmegaLambda 0.5% (Lam footing)
def zscore(Zc, Zd, s, foot):
    se = math.sqrt(s*s + (0.0074**2) + ((0.005**2) if foot == "Lam" else 0))
    return (math.log(Zc) - math.log(Zd))/se
res = {}
print("\n== z-scores (candidate Z vs data Z; + = candidate above data), s_tot includes H0 (0.74%) and Omega_L (0.5%, Lam) ==")
for foot in ("Lam", "tot"):
    for hl, H0 in H0s.items():
        for lab, a0, s in scen:
            Zd = Zdata(a0, H0, foot)
            row = {k: zscore(v, Zd, s, foot) for k, v in cands.items()}
            res[(foot, hl, lab)] = (Zd, row)
            if hl == "Planck 67.4" or lab.startswith("E "):
                print("%-4s %-11s %-38s Zdata=%.3f | " % (foot, hl, lab, Zd) + " ".join("%s:%+.2f" % (k.split()[0], row[k]) for k in list(cands)[:5]))
# LRs
print("\n== likelihood ratios (point hypotheses, no free parameter) ==")
def LR(row, a, b): return math.exp(-0.5*(row[a]**2 - row[b]**2))
F, V, Mm, N, A7 = "F sqrt(32pi/3)", "V 6", "M 2pi", "N1 Nariai@L 3sqrt3 (A1)", "A7 4sqrt3 (Schw ISCO)"
lrtab = []
for foot in ("Lam", "tot"):
    for lab, a0, s in scen:
        Zd, row = res[(foot, "Planck 67.4", lab)]
        lrtab.append((foot, lab, LR(row, N, F), LR(row, N, V), LR(row, N, Mm)))
        print("%-4s %-38s LR N:F=%.2f  N:6=%.2f  N:2pi=%.2f" % lrtab[-1])
chk("LR N:F on Lam footing (E) ~ 2 (weak, < 3)", 1.0 < lrtab[0][2] < 3.0)
# sanity: hand check of E/Lam numbers against lane V (Z_Lam 4.94; N +0.42, F +1.30 at V's s_tot ~12.4%)
Zd, row = res[("Lam", "Planck 67.4", scen[0][0])]
chk("reproduces lane V: Z_Lam(E) ~ 4.94", abs(Zd - 4.94) < 0.03)
chk("reproduces lane V: N offset ~ +0.4 sigma, F ~ +1.3 sigma (Lam, E)", abs(row[N] - 0.42) < 0.06 and abs(row[F] - 1.30) < 0.06)
# stability across kernels: which candidates have |z|<1 in which (footing, kernel)
print("\n== stability across kernels (Planck H0; scenarios 4-7 = Upsilon-free alpha1/RAR/simple/standard, same stat 8.2%) ==")
ker = [scen[3][0], scen[4][0], scen[5][0], scen[6][0]]
for foot in ("Lam", "tot"):
    print(foot, "footing Z_data:", ["%.2f" % res[(foot, "Planck 67.4", k)][0] for k in ker])
    for cn in [F, V, Mm, N, A7]:
        print("   %-26s z:" % cn, ["%+.2f" % res[(foot, "Planck 67.4", k)][1][cn] for k in ker])
# which candidate is |z|<1 for ALL four kernels on a footing?
for foot in ("Lam", "tot"):
    stable = [cn for cn in cands if all(abs(res[(foot, "Planck 67.4", k)][1][cn]) < 1.0 for k in ker)]
    print(foot, "candidates with |z|<1 under all four kernels:", stable)
    stable2 = [cn for cn in cands if all(abs(res[(foot, "Planck 67.4", k)][1][cn]) < 2.0 for k in ker)]
    print(foot, "candidates with |z|<2 under all four kernels:", stable2)
# kernel flip
zr_N = res[("Lam","Planck 67.4",ker[1])][1][N]; zr_M = res[("Lam","Planck 67.4",ker[1])][1][Mm]
za_N = res[("Lam","Planck 67.4",ker[0])][1][N]
chk("kernel dependence: best of {N,M} flips between alpha1 and RAR on Lam footing", abs(za_N) < abs(res[("Lam","Planck 67.4",ker[0])][1][Mm]) and abs(zr_M) < abs(zr_N))

# Omega_Lambda prediction from a0 (candidate's Z): Om = Z^2 (a0/cH0)^2
print("\n== Omega_Lambda implied by a0 and Z (Planck H0 = 67.4 +-0.5; observed 0.685+-0.007) ==")
for lab, a0, s in [scen[0], scen[1], scen[3], scen[4]]:
    x = a0*1e-10/cH0(67.4); sO = 2*math.sqrt(s**2 + 0.0074**2)
    print(lab)
    for cn in [F, N, V, Mm]:
        Om = cands[cn]**2*x*x
        print("   %-26s Omega_L = %.3f +- %.3f  (%+.2f sigma of Omega_obs incl. its 0.007)" % (cn, Om, Om*sO, (Om-0.685)/math.hypot(Om*sO, 0.007)))
x = 1.0766e-10/cH0(67.4)
chk("Omega_L(F) at record a0 = 0.906 (lane V), Omega_L(N) = 0.73", abs(32*math.pi/3*x*x - 0.906) < 0.002 and abs(27*x*x - 0.730) < 0.002)
# predicted a0 at the observed Omega_Lambda
print("\n== a0 predicted (1e-10) at H0 = 67.4 / 73, Omega_L = 0.685 ==")
for hl, H0 in H0s.items():
    print(hl, {cn.split()[0]+"_"+str(round(cands[cn],3)): round(cH0(H0)*math.sqrt(OmL)/cands[cn]*1e10, 4) for cn in [F, N, V, Mm]})
chk("a0_F at Planck = 0.936e-10 (lane V footing)", abs(cH0(67.4)*math.sqrt(OmL)/cands[F]*1e10 - 0.936) < 0.002)
print("a0_N/a0_F - 1 = %.4f ; boost sensitivity dln nu/dln a0 ~ 0.4 (y~0.3) -> wide-binary boost differs by ~%.1f%%" % (cands[F]/cands[N]-1, 100*0.4*math.log(cands[F]/cands[N])))

# D1 integer family a0 = c^2 sqrt(Lambda)/n  (Z = n/sqrt3)
print("\n== D1: a0 = c^2 sqrt(Lambda)/n, z vs E/Lam ==")
Zd, _ = res[("Lam","Planck 67.4",scen[0][0])]
d1 = {n: zscore(n/math.sqrt(3), Zd, .122, "Lam") for n in range(6, 13)}
print({n: round(v, 2) for n, v in d1.items()})
nfit = [n for n, v in d1.items() if abs(v) < 1]
print("integers n with |z|<1:", nfit, "; with |z|<2:", [n for n, v in d1.items() if abs(v) < 2])
chk("D1: more than one integer n fits at 1 sigma (so 1/9 is not special)", len(nfit) >= 2)
# D2: Monte-Carlo false-match probability
rng = np.random.default_rng(32032)
zN = abs(row[N]); zbest_menu = min(abs(zscore(v, Zd, .122, "Lam")) for k, v in cands.items() if k not in (F, V, Mm) and not k.startswith("A11b") and not k.startswith("A8") or k in (N,) )
# independent MENU (A1..A11, distinct Z>0): values
menuZ = sorted(set(round(v, 9) for k, v in Zm.items() if v is not None and math.isfinite(v)))
print("\nD2: menu distinct Z:", [round(z, 3) for z in menuZ], " n =", len(menuZ))
obsbest = min(abs(zscore(z, Zd, .122, "Lam")) for z in menuZ)
print("best menu |z| (E, Lam) = %.3f" % obsbest)
lo, hi = math.log(min(menuZ)), math.log(max(menuZ))
T = 200000
draws = rng.uniform(lo, hi, size=(T, len(menuZ)))
zz = np.abs((draws - math.log(Zd))/math.sqrt(.122**2 + .0074**2 + .005**2)).min(axis=1)
p_mc = (zz <= obsbest).mean()
w = 2*obsbest*math.sqrt(.122**2 + .0074**2 + .005**2)
p_an = 1 - (1 - w/(hi-lo))**len(menuZ)
print("D2 false-match P(best |z| <= %.3f) = %.3f (MC) vs %.3f (analytic)" % (obsbest, p_mc, p_an))
chk("D2: MC agrees with analytic (control of the machinery)", abs(p_mc - p_an) < 0.01)
# planted control: a menu that contains the data value always reaches |z|<=0.01
draws2 = np.concatenate([draws[:, :-1], np.full((T, 1), math.log(Zd))], axis=1)
chk("D2 control: planted true value always gives best |z| ~ 0", (np.abs((draws2 - math.log(Zd))).min(axis=1) < 1e-9).all())
# a menu that is tighter than data (all far away) must have P = 0
chk("D2 mutation: menu Zs all >= 20 gives best |z| > 5", abs((math.log(20) - math.log(Zd))/0.12) > 5)
# D2b: probability to have a value within the A1 offset but only among menu members with a *self-consistent* radius (A2-A5,A6,A8,A10,A11)
selfc = [Zm[k] for k in ("A2","A6","A8","A10","A11a","A11b")]
print("self-consistent (no chosen radius, in M_N geometry) menu Zs:", [round(z, 3) for z in sorted(set(selfc))], " min |z| =", round(min(abs(zscore(z, Zd, .122, "Lam")) for z in selfc), 2))
chk("self-consistent menu members are all excluded at > 5 sigma (E, Lam)", min(abs(zscore(z, Zd, .122, "Lam")) for z in selfc) > 5)
# D3 grammar decoys
vals = sorted(set(round(p*math.sqrt(q)/r_, 10) for p in range(1,7) for r_ in range(1,7) for q in (1,2,3,5,6,7)))
frac = sum(1 for v in vals if abs(zscore(v, Zd, .122, "Lam")) <= abs(row[N])) / len(vals)
inwin = [v for v in vals if abs(zscore(v, Zd, .122, "Lam")) <= 1.0]
print("\nD3: grammar p*sqrt(q)/r: %d distinct values, %d within |z|<=1 of data (E/Lam): e.g. %s" % (len(vals), len(inwin), [round(v,3) for v in inwin[:12]]))
chk("D3: many grammar values fit as well as N (look-elsewhere: >= 5 within 1 sigma)", len(inwin) >= 5)
print("\nn02 checks: %d pass, %d fail" % (npass, nfail))
sys.exit(1 if nfail else 0)
