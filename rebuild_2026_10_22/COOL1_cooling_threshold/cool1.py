#!/usr/bin/env python3
"""COOL1_cooling_threshold (FROZEN_CRITERIA.md): t_cool(r_s) = t_dyn(r_s) threshold mass, native background.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I cool1.py [--mutate]  (--mutate: Lambda/10, separate outputs)"""
import itertools, json, math, os, sys
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# cgs
G, KB, MP, MSUN, KPC, GYR, KEV = 6.674e-8, 1.380649e-16, 1.67262e-24, 1.98847e33, 3.0857e21, 3.15576e16, 1.602177e-9
h, Om, Or, FB = 0.6776978854572208, 0.31040265376181814, 9.106163175213682e-05, 0.15684624017957352  # CFG654 A1 native
OL = 1 - Om - Or
H0 = 100 * h * 1e5 / (KPC * 1e3)
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G)
MU, XH = 0.59, 0.76
YH = (1 - XH) / (4 * XH)  # n_He / n_H
A0 = {"canonical": 9.3603e-9, "alt": 1.1312e-8}  # cm/s^2
W = (12.19, 12.39); WP = (12.19, 12.6)
DV = dict(zip([0, .5, 1, 2, 3, 5, 7, 9], [303.9, 220.0, 196.7, 183.3, 180.1, 178.2, 177.8, 177.5]))  # cfg934.out

def E2(z): return Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + OL
def rhoc(z): return RHOC0 * E2(z)
def rhom(z): return RHOC0 * Om * (1 + z) ** 3
def dvir(z): return float(np.interp(z, list(DV), list(DV.values())))

def cie(T):
    """Katz, Weinberg & Hernquist 1996 Table 2 closed forms; fractions per n_H."""
    sq = math.sqrt(T); t3, t6 = T / 1e3, T / 1e6; d = 1 + math.sqrt(T / 1e5)
    aHp = 8.4e-11 / sq * t3 ** -0.2 / (1 + t6 ** 0.7)
    aHep = 1.5e-10 * T ** -0.6353
    ad = 1.9e-3 * T ** -1.5 * math.exp(-470000 / T) * (1 + 0.3 * math.exp(-94000 / T))
    aHepp = 3.36e-10 / sq * t3 ** -0.2 / (1 + t6 ** 0.7)
    gH0 = 5.85e-11 * sq * math.exp(-157809.1 / T) / d
    gHe0 = 2.38e-11 * sq * math.exp(-285335.4 / T) / d
    gHep = 5.68e-12 * sq * math.exp(-631515.0 / T) / d
    nH0 = aHp / (aHp + gH0); nHp = 1 - nH0
    # guard the He0 share against underflow at high T
    r0 = (aHep + ad) / gHe0 if gHe0 > 0 else 1e300; r2 = gHep / aHepp
    nHep = YH / (1 + r0 + r2); nHe0 = nHep * r0; nHepp = nHep * r2
    ne = nHp + nHep + 2 * nHepp
    return dict(H0=nH0, Hp=nHp, He0=nHe0, Hep=nHep, Hepp=nHepp, ne=ne, n=1 + YH + ne)

def lam_hhe(T):
    """Lambda per n_e n_H, H-He CIE, KWH96 Table 1 (Cen 1992, Black 1981)."""
    f = cie(T); sq = math.sqrt(T); t3, t6 = T / 1e3, T / 1e6; d = 1 + math.sqrt(T / 1e5); lg = math.log10(T)
    g = 1.1 + 0.34 * math.exp(-(5.5 - lg) ** 2 / 3)
    per_ne = (7.5e-19 * math.exp(-118348 / T) / d * f["H0"]
              + 5.54e-17 * T ** -0.397 * math.exp(-473638 / T) / d * f["Hep"]
              + 1.27e-21 * sq * math.exp(-157809.1 / T) / d * f["H0"]
              + 9.38e-22 * sq * math.exp(-285335.4 / T) / d * f["He0"]
              + 4.95e-22 * sq * math.exp(-631515.0 / T) / d * f["Hep"]
              + 8.7e-27 * sq * t3 ** -0.2 / (1 + t6 ** 0.7) * f["Hp"]
              + 1.55e-26 * T ** 0.3647 * f["Hep"]
              + 3.48e-26 * sq * t3 ** -0.2 / (1 + t6 ** 0.7) * f["Hepp"]
              + 1.24e-13 * T ** -1.5 * math.exp(-470000 / T) * (1 + 0.3 * math.exp(-94000 / T)) * f["Hep"]
              + 1.42e-27 * g * sq * (f["Hp"] + f["Hep"] + 4 * f["Hepp"]))
    return per_ne

def lam_tn(T):
    """CFG640 lam_cool: Tozzi & Norman 2001, Z = 0.3, CFG370's normalisation."""
    kT = min(max(KB * T / KEV, 0.01), 20.0)
    return (8.6e-3 * kT ** -1.7 + 5.8e-2 * kT ** 0.5 + 6.3e-2) * 1e-22

def lam(T, Z):
    L = lam_hhe(T)
    if Z > 0: L += (Z / 0.3) * max(lam_tn(T) - L, 0.0)
    return L / 10 if MUTATE else L

def R200(Mg, z): return (3 * Mg / (4 * math.pi * 200 * rhoc(z))) ** (1 / 3)
def Rvir(Mg, z): return (3 * Mg / (4 * math.pi * dvir(z) * rhom(z))) ** (1 / 3)
def Tof(V): return MU * MP * V * V / (2 * KB)

def tcool(T, rho, Z):
    if T < 8e3: return math.inf  # below the atomic range: no H-He cooling (grid low end only)
    nH = XH * rho / MP; f = cie(T)
    return 1.5 * f["n"] * nH * KB * T / (f["ne"] * nH * nH * lam(T, Z))

def ratio(lgM, z, Z=0.0, fg=1.0, x=1.0, density="iso", tdyn="rV", halo="200c", form="RO", law=None):
    """t_cool / t_dyn at r_s = x R; form BD: t_cool,post / (1.4 r_s/|u1|). fg in units of f_b."""
    M = 10 ** lgM * MSUN
    R = R200(M, z) if halo == "200c" else Rvir(M, z)
    V = (G * FB * M * law) ** 0.25 if law else math.sqrt(G * M / R)
    r = x * R; f = fg * FB
    rho = f * M / (4 * math.pi * R * r * r) if density == "iso" else f * 3 * M / (4 * math.pi * R ** 3)
    if form == "RO":
        tc = tcool(Tof(V), rho, Z)
        td = r / V * (math.pi / (2 * math.sqrt(2)) if tdyn == "ff" else 1.0)
        return tc / td
    u0 = math.sqrt(2) * V; T1 = 3 * MU * MP * u0 ** 2 / (16 * KB)
    return tcool(T1, 4 * rho, Z) / (1.4 * r / (u0 / 4))

GRID = np.arange(7.0, 16.5, 0.01)
def mthr(z, **k):
    """largest log M with ratio <= 1; None if none."""
    v = np.array([ratio(float(m), z, **k) for m in GRID]) - 1
    idx = np.where(v <= 0)[0]
    if len(idx) == 0: return None
    i = idx[-1]
    if i == len(GRID) - 1: return float(GRID[-1])
    return brentq(lambda m: ratio(m, z, **k) - 1, GRID[i], GRID[i + 1], xtol=1e-10)

def to200(lgMv, z):
    return lgMv + 0.5 * math.log10(dvir(z) * rhom(z) / (200 * rhoc(z)))

ZH = ([10, 11, 12, 14], [1.33, 1.14, 0.94, 0.56]); ZFS = ([10, 11, 12], [2.19, 1.89, 1.58]); FS = 0.1441
def desc(tab, f, **k):
    """M0 with f M0 = M_thr(z(f, M0)); fixed point in log M0."""
    m0 = 12.0
    for _ in range(60):
        z = float(np.interp(m0, *tab)); mt = mthr(z, **k)
        if mt is None: return None, z
        new = mt - math.log10(f)
        if abs(new - m0) < 1e-8: break
        m0 = new
    return m0, float(np.interp(m0, *tab))
def inw(m, w=W): return m is not None and w[0] <= m <= w[1]
def fm(m): return "none" if m is None else f"{m:.3f}"

# ---------------------------------------------------------------- checks
res = dict(checks={}, mutate=MUTATE)
P("COOL1_cooling_threshold", "MUTATE Lambda/10" if MUTATE else "primary", "criteria b154df6559")
P(f"native h {h:.5f} Om {Om:.5f} f_b {FB:.5f}; target W {W}, width {W[1]-W[0]:.2f} dex; W' {WP}")
def k(name, ok, msg):
    res["checks"][name] = bool(ok); P(f"  {name}: {'PASS' if ok else 'FAIL'}  {msg}")
V4 = math.sqrt(2 * KB * 1e4 / (MU * MP))
mc = lambda z: V4 ** 3 / (G ** 1.5 * math.sqrt(4 * math.pi / 3 * dvir(z) * rhom(z))) / MSUN
k("K1", abs(mc(0) / 2.338e9 - 1) < 2e-3 and abs(mc(2) / 5.792e8 - 1) < 2e-3, f"M_cool z=0 {mc(0):.4e} vs CFG934 2.338e9; z=2 {mc(2):.4e} vs 5.792e8")
_m, MUTATE = MUTATE, False
T1k = KEV / KB; l1k = lam(T1k, 0.0); T12 = 0.12 * T1k; zr = lam(T12, 1.0) / lam(T12, 0.0)
MUTATE = _m
k("K2", abs(l1k / 8.917e-24 - 1) < 0.15 and 1 / 1.5 < zr / 30.1 < 1.5, f"Lambda(1 keV,0) {l1k:.3e} vs AtomDB 8.917e-24 ({l1k/8.917e-24-1:+.3f}); Z=1/Z=0 at 0.12 keV {zr:.1f} vs 30.1")
g, gc = 5 / 3, 10 / 7
crit = 1 / (g - gc) / 3  # t_cool/(r/|u1|) from gamma_eff = gamma - (rho/rhodot)/t_cool, rhodot/rho = 3|u1|/r
coef = (3 / 2 * (3 / 4) / 4) / (4 * 4 * crit)  # e1 = (3/2)(P1/rho1) with P1 = (3/4) rho0 u0^2, rho1 = 4 rho0; t_comp = crit r 4/u0
k("K3", abs(coef / ((9 / 32) / 22.4) - 1) < 1e-3 and abs(crit - 1.4) < 1e-9, f"crit {crit:.4f}, coefficient {coef:.5f}")
ok4 = all(abs(f["H0"] + f["Hp"] - 1) < 1e-12 and abs(f["He0"] + f["Hep"] + f["Hepp"] - YH) < 1e-12 for f in map(cie, np.geomspace(1e4, 1e8, 50)))
f7 = cie(1e7); mu7 = (1 + 4 * YH) / f7["n"]
k("K4", ok4 and abs(mu7 / MU - 1) < 0.01, f"mu(1e7 K) {mu7:.4f}")
m0 = mthr(0.0)
k("K5", abs(ratio(m0, 0.0) - 1) < 1e-6, f"ratio at root {ratio(m0, 0.0):.9f}")
a, b, c = ratio(12.3, 0, x=1.0), ratio(12.3, 0, x=0.5), ratio(12.3, 0, fg=0.5)
k("K6", abs(b / a - 0.5) < 1e-10 and abs(c / a - 2) < 1e-10, f"x 0.5: {b/a:.12f}; f_g 0.5: {c/a:.12f}")
ALLOK = all(res["checks"].values())

# ---------------------------------------------------------------- Lambda table
P("\nLambda(T) per n_e n_H, erg cm3/s")
for T in (1e5, 3e5, 1e6, 3e6, 1e7):
    P(f"  T {T:.0e}: Z=0 {lam_hhe(T):.3e}  TN Z=0.3 {lam_tn(T):.3e}  used Z=0.3 {lam(T,0.3):.3e}")

# ---------------------------------------------------------------- primary
P("\nPRIMARY: Z 0, f_g f_b, r_s R200c, isothermal, t_dyn r/V")
PF, zh = desc(ZH, 0.5); PFS, zs = desc(ZFS, FS)
p = dict(P0=m0, Pf=PF, z_half=zh, Pfs=PFS, z_fs=zs)
rat = ratio(12.3, 0.0)
P(f"  P0  z 0: log M_thr {m0:.3f}, miss from W's nearer edge {m0-W[0]:+.3f}; V {math.sqrt(G*10**m0*MSUN/R200(10**m0*MSUN,0))/1e5:.0f} km/s, T {Tof(math.sqrt(G*10**m0*MSUN/R200(10**m0*MSUN,0))):.2e} K")
P(f"  Pf  z_half {zh:.2f}: descendant log M0 {PF:.3f} (instantaneous {PF-math.log10(2):.3f})")
P(f"  Pfs z(f_s) {zs:.2f}: descendant log M0 {PFS:.3f} (instantaneous {PFS+math.log10(FS):.3f})")
P(f"  t_cool/t_dyn at 10^12.3, primary, z 0: {rat:.2f}")
res["primary"] = p; res["ratio_12p3_z0"] = rat

# ---------------------------------------------------------------- sensitivity
ZS, FG, XS = (0, .03, .1, .3, 1), (1, .5, .2), (1, .5, .3, .1)
P("\nONE AT A TIME (log M_thr; P0 = z 0 instantaneous, Pf = descendant at z_half)")
sens = {}
def row(name, kw, conv=None):
    a = mthr(0.0, **kw); b, _ = desc(ZH, 0.5, **kw)
    if conv: a = conv(a, 0.0)
    sens[name] = dict(P0=a, Pf=b)
    P(f"  {name:32s} P0 {fm(a):>7s}{' IN W' if inw(a) else '     '}   Pf {fm(b):>7s}{' IN W' if inw(b) else ''}")
for Z in ZS: row(f"Z {Z}", dict(Z=Z))
for fg in FG: row(f"f_g/f_b {fg}", dict(fg=fg))
for x in XS: row(f"r_s/R {x}", dict(x=x))
row("density uniform", dict(density="uni"))
row("t_dyn free fall", dict(tdyn="ff"))
row("halo native Delta_vir (->200c)", dict(halo="vir"), conv=to200)
for x in (1, .5, .3, .1): row(f"BD shock form, r_s/R {x}", dict(form="BD", x=x))
row("BD, r_s/R 0.1, Z 0.1", dict(form="BD", x=.1, Z=.1))
P("\nM_thr(z), instantaneous, primary and Z 0.1, 0.3 at r_s/R 1; Z 0.1 at r_s/R 0.1")
zrow = {}
for z in (0, .5, 1, 2, 3, 4, 6):
    zrow[z] = [mthr(z), mthr(z, Z=.1), mthr(z, Z=.3), mthr(z, Z=.1, x=.1)]
    P(f"  z {z}: " + "  ".join(fm(v) for v in zrow[z]))
res["sens"] = sens; res["z_row"] = zrow

P("\nCORNERS: Z x f_g x r_s/R, 60 cells of the frozen lists (not a search: every cell reported as a count)")
cells = []
for Z, fg, x in itertools.product(ZS, FG, XS):
    cells.append(dict(Z=Z, fg=fg, x=x, P0=mthr(0.0, Z=Z, fg=fg, x=x), Pf=desc(ZH, 0.5, Z=Z, fg=fg, x=x)[0]))
for key in ("P0", "Pf"):
    v = [c[key] for c in cells if c[key] is not None]
    nw = [c for c in cells if inw(c[key])]
    res[f"corners_{key}"] = dict(min=min(v), max=max(v), spread=max(v) - min(v), in_W=len(nw), in_WP=sum(inw(c[key], WP) for c in cells), n=len(cells))
    P(f"  {key}: range {min(v):.3f} to {max(v):.3f}, spread {max(v)-min(v):.3f} dex = {(max(v)-min(v))/(W[1]-W[0]):.1f} x W; in W {len(nw)}/{len(cells)}; in W' {res[f'corners_{key}']['in_WP']}/{len(cells)}")
    P("    cells in W (each a choice): " + "; ".join(f"Z {c['Z']} f {c['fg']} x {c['x']}: {c[key]:.2f}" for c in nw))
res["cells"] = cells
oat = lambda ks, key: [sens[s][key] for s in ks if sens[s][key] is not None]
for lab, ks in (("Z", [f"Z {z}" for z in ZS]), ("f_g", [f"f_g/f_b {f}" for f in FG]), ("r_s", [f"r_s/R {x}" for x in XS])):
    a = oat(ks, "P0"); b = oat(ks, "Pf"); P(f"  one-at-a-time spread {lab}: P0 {max(a)-min(a):.3f}, Pf {max(b)-min(b):.3f} dex")
    res[f"oat_{lab}"] = dict(P0=max(a) - min(a), Pf=max(b) - min(b))

# ---------------------------------------------------------------- footings
P("\nFOOTINGS. Cold branch: no a0 in V or T, identical by construction. Law branch: V^4 = G a0 f_b M (a0 flat, disclosed)")
fo = {}
for foot, a0 in A0.items():
    r = {}
    for nm, kw in (("primary", {}), ("Z 0.3", dict(Z=.3)), ("r_s/R 0.1", dict(x=.1)), ("Z 0.1, r_s/R 0.1", dict(Z=.1, x=.1))):
        r[nm] = dict(P0=mthr(0.0, law=a0, **kw), Pf=desc(ZH, 0.5, law=a0, **kw)[0], cold_P0=mthr(0.0, **kw))
        P(f"  {foot:9s} {nm:18s} law P0 {fm(r[nm]['P0'])}  Pf {fm(r[nm]['Pf'])}   cold P0 {fm(r[nm]['cold_P0'])}")
    fo[foot] = r
res["footings"] = fo
d = fo["alt"]["primary"]["P0"] - fo["canonical"]["primary"]["P0"]
P(f"  alt - canonical, law branch, primary P0: {d:+.3f} dex")

# ---------------------------------------------------------------- link: ledger, membership
P("\nLINK: energy ledger at 10^12.3, z 0 (isothermal)")
M = 10 ** 12.3 * MSUN; R = R200(M, 0); V = math.sqrt(G * M / R); T = Tof(V)
Eth = 0.75 * FB * M * V ** 2; Ebc = 0.5 * (1 - FB) * M * V ** 2
P(f"  V {V/1e5:.0f} km/s, T {T:.2e} K ({KB*T/KEV:.3f} keV), R200 {R/KPC:.0f} kpc; gas thermal {Eth:.2e} erg, cold binding {Ebc:.2e} erg, ratio cold/gas {Ebc/Eth:.2f}")
res["ledger"] = dict(V=V / 1e5, T=T, Eth=Eth, Ebc=Ebc, ratio=Ebc / Eth)
P("\nBS1's membership against a per-halo cooling read at z 0: BS1 flags, primary t_cool/t_dyn, and Z 0.1 r_s/R 0.1")
mem = {}
for nm, lm in (("LMC", 10.709), ("M33", 11.093), ("MW", 11.880), ("M31", 12.151)):
    a = ratio(lm, 0.0); b = ratio(lm, 0.0, Z=.1, x=.1)
    mem[nm] = dict(lgM=lm, primary=a, Z01x01=b)
    P(f"  {nm:4s} log M200 {lm:.3f}: BS1 route E (in LG basin); ratio primary {a:8.2f}, Z 0.1 x 0.1 {b:6.2f}; own mass vs T 12.3: {'below, would cool, no halo' if lm < 12.3 else ''}")
Mb = 10 ** 12.3925 * MSUN; R0 = 794.7 * KPC; Vb = math.sqrt(G * Mb / R0); rho = FB * Mb / (4 * math.pi * R0 ** 3)
tb = tcool(Tof(Vb), rho, 0.0) / (R0 / Vb)
P(f"  LG basin log 12.3925 at R0 795 kpc as if one isothermal sphere: V {Vb/1e5:.0f} km/s, T {Tof(Vb):.2e} K, t_cool/t_dyn {tb:.1f}; it's a turnaround surface, so no accretion shock sits there")
mem["LG_basin"] = dict(V=Vb / 1e5, T=Tof(Vb), ratio=tb); res["membership"] = mem

# ---------------------------------------------------------------- label
P("\nCHECKS " + ("ALL PASS" if ALLOK else "FAILED: NO VERDICT"))
sp = max(res["corners_P0"]["spread"], res["corners_Pf"]["spread"])
anyin = res["corners_P0"]["in_W"] + res["corners_Pf"]["in_W"] + sum(inw(s["P0"]) or inw(s["Pf"]) for s in sens.values())
if inw(m0) and inw(PF) and sp <= 0.20: lab = "DERIVED"
elif anyin: lab = "CHOICE-DEPENDENT"
else: lab = "NOT REACHED"
res["label_threshold"] = lab if ALLOK else "NO VERDICT"; res["spread_max"] = sp
P(f"THRESHOLD LABEL: {res['label_threshold']}; max free-input spread {sp:.3f} dex vs W 0.20")
if MUTATE:
    base = json.load(open(os.path.join(HERE, "cool1_results.json")))
    bite = m0 - base["primary"]["P0"]; res["mutate_shift"] = bite
    P(f"MUTATE: P0 moves {bite:+.3f} dex; {'BITES' if bite < -0.3 else 'DOES NOT BITE'}")
json.dump(res, open(os.path.join(HERE, f"cool1_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cool1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
