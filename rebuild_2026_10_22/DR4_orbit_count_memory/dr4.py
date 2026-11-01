#!/usr/bin/env python3
"""DR4_orbit_count_memory: box^-1 R and N_dyn at SPARC, X-COP, z = 3 filament. Criteria: FROZEN_CRITERIA.md. MUTATE=1 separate output."""
import os, sys, json, math, glob
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.integrate import solve_ivp, quad
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("MUTATE", "") == "1"; TAG = "_MUTATE" if MUT else ""
out = open(os.path.join(HERE, f"dr4{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
G = 4.30091e-6      # kpc (km/s)^2 / Msun
C = 299792.458; KMS_KPC_GYR = 1.0227  # 1 km/s = 1.0227 kpc/Gyr
NAT = dict(Om=0.2976016, h=0.6856427, Orh2=4.15e-5); C123 = dict(Om=0.3153, h=0.6736, Orh2=4.15e-5)
def H0_gyr(bg): return bg["h"] * 100 * 1.0227e-3   # 1/Gyr
def E2(a, bg, rad=True):
    Or = bg["Orh2"] / bg["h"] ** 2 if rad else 0.0; OL = 1 - bg["Om"] - Or
    return bg["Om"] / a ** 3 + Or / a ** 4 + OL
def age(z, bg, rad=True):
    a1 = 1 / (1 + z); f = lambda a: 1 / (a * math.sqrt(E2(a, bg, rad)))
    return quad(f, 0, a1, epsabs=0, epsrel=1e-11, limit=400)[0] / H0_gyr(bg)
def xbar(bg, ai=1e-7, matter_only=False):
    def rhs(x, y):
        a = math.exp(x)
        if matter_only: return [y[1], -1.5 * y[1] - 3.0]
        Or = bg["Orh2"] / bg["h"] ** 2; OL = 1 - bg["Om"] - Or; Om = bg["Om"]
        e2 = Om / a ** 3 + Or / a ** 4 + OL
        dlnH = (-3 * Om / a ** 3 - 4 * Or / a ** 4) / (2 * e2)
        return [y[1], -(3 + dlnH) * y[1] - 3 * (Om / a ** 3 + 4 * OL) / e2]
    return solve_ivp(rhs, (math.log(ai), 0.0), [0, 0], rtol=1e-10, atol=1e-12, dense_output=True, method="DOP853")
checks = {}
# K1
s = xbar(NAT, ai=1e-3, matter_only=True); k = float(s.y[1, -1]); checks["K1"] = abs(k + 2) <= 1e-3; P(f"K1 matter era X' {k:.6f} (-2): {checks['K1']}")
# K2
s = xbar(C123); v = -float(s.y[0, -1]); checks["K2"] = abs(v / 16.035 - 1) <= 0.02; P(f"K2 Xbar(0) on CFG123 parameters -{v:.3f} vs U-bar 16.035, d {v/16.035-1:+.4f}: {checks['K2']}")
# K3: retarded kernel static limit: X(r) = -int 8 pi G rho(r')/c^2 /(4 pi |x-x'|) d3x', spherical shell theorem form; against 2 Phi for NFW
rs, rho0 = 20.0, 1e7
def rho_nfw(r): return rho0 / ((r / rs) * (1 + r / rs) ** 2)
def phi_nfw(r): return -4 * math.pi * G * rho0 * rs ** 3 * math.log(1 + r / rs) / r
def X_kernel(r):
    # angle-integrated light-cone kernel 1/|x-x'|: 1/max(r,r')
    a = quad(lambda q: rho_nfw(q) * q * q / r, 0, r, epsrel=1e-10, limit=400)[0]
    b = quad(lambda q: rho_nfw(q) * q, r, np.inf, epsrel=1e-10, limit=400)[0]
    return -8 * math.pi * G * (a + b)   # units (km/s)^2 before /c^2
d3 = max(abs(X_kernel(r) / (2 * phi_nfw(r)) - 1) for r in (1, 8, 50, 300)); checks["K3"] = d3 <= 1e-4; P(f"K3 retarded static kernel vs 2 Phi NFW, max d {d3:.2e}: {checks['K3']}")
# K4
Or0 = dict(NAT); a4 = age(0, NAT, rad=False); OL = 1 - NAT["Om"]
cf = 2 / (3 * math.sqrt(OL)) * math.asinh(math.sqrt(OL / NAT["Om"])) / H0_gyr(NAT); checks["K4"] = abs(a4 / cf - 1) <= 1e-6; P(f"K4 age {a4:.5f} Gyr vs closed form {cf:.5f}: {checks['K4']}")
T0 = age(0, NAT); H0 = NAT["h"] * 100 / 1e3  # km/s/kpc
Hg = H0_gyr(NAT); P(f"native t0 {T0:.3f} Gyr; t(z=3) {age(3, NAT):.3f}; 1/H0 {1/Hg:.3f}")
# K6 z_f
RJ = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/X73_smooth_core_all_measured/x73_results_fs0.034_S_nat_s2.7774.json")))["sigma_coll_table"]
LM = np.array([11, 12, 13, 14, 15.0]); ZF = np.array([RJ[f"1e{int(l)}"][1] for l in LM])
k6a = np.allclose(np.round(ZF, 4), [1.1365, 0.9440, 0.7507, 0.5615, 0.3850]); P("z_f table", ZF.round(4), k6a)
def zf_of(M): return float(np.interp(math.log10(M), LM, ZF))
AGEC = {}
def tf(M):
    z = round(zf_of(M), 3)
    if z not in AGEC: AGEC[z] = age(z, NAT)
    return AGEC[z]
XBAR = xbar(NAT); Xb0 = float(XBAR.y[0, -1]); Xp0 = float(XBAR.y[1, -1])
def Xb(z): return float(XBAR.sol(math.log(1 / (1 + z)))[0])
P(f"Native Xbar: z=0 {Xb0:.4f}, z=3 {Xb(3):.4f}, z=16 {Xb(16):.4f}; dX/dlna today {Xp0:.4f}; dX/dlna at z=3 {float(XBAR.sol(math.log(.25))[1]):.4f}")
c2 = C * C
# SPARC
rows = []; files = sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data/*_rotmod.dat")))
gal = []
for f in files:
    d = np.loadtxt(f, comments="#", usecols=(0, 1)); d = np.atleast_2d(d); d = d[(d[:, 0] > 0) & (d[:, 1] > 0)]
    if len(d) == 0: continue
    r, v = d[:, 0], d[:, 1]; Vl = float(np.median(v[-3:])); Vlast = float(v[-1])
    M200 = Vl ** 3 / (10 * G * H0); R200 = Vl / (10 * H0); Rout = max(R200, r[-1])
    # Phi(r) = -[int_r^rlast v^2/r dr + Vl^2 ln(Rout/rlast) + Vl^2]
    I = np.concatenate([np.cumsum((0.5 * (v[1:] ** 2 / r[1:] + v[:-1] ** 2 / r[:-1]) * np.diff(r))[::-1])[::-1], [0.0]])
    Phi = -(I + Vl ** 2 * math.log(Rout / r[-1]) + Vl ** 2)
    T = 2 * math.pi * r / v / KMS_KPC_GYR
    Nf = (T0 - tf(M200)) / T; Nc = T0 / T
    gal.append(dict(name=os.path.basename(f)[:-11], V=Vl, M200=M200, R200=R200, r=r, v=v, T=T, Nf=Nf, Nc=Nc, Phi=Phi, zf=zf_of(M200), dX=2 * Phi / c2))
checks["K7a"] = len(files) == 175 and len(gal) == 175
K5 = []
for g in gal[:20]:
    Tv = 2 * math.pi * g["R200"] / g["V"] / KMS_KPC_GYR; K5.append(abs(Tv * 10 * H0 * KMS_KPC_GYR / (2 * math.pi) - 1))
checks["K5"] = max(K5) <= 1e-10; P(f"K5 virial T = 2 pi/(10 H0) max d {max(K5):.1e}: {checks['K5']}")
aNf = np.concatenate([g["Nf"] for g in gal]); aNc = np.concatenate([g["Nc"] for g in gal]); adX = np.concatenate([g["dX"] for g in gal]); ar = np.concatenate([g["r"] for g in gal])
P(f"SPARC: {len(gal)} galaxies, {len(aNf)} points (K7 {checks['K7a']})")
pc = lambda a, q: float(np.percentile(a, q))
def pr(a): return " ".join(f"p{q} {pc(a,q):.3g}" for q in (0, 5, 25, 50, 75, 95, 100))
P("SPARC N (z_f):", pr(aNf)); P("SPARC N (ceiling):", pr(aNc)); P("SPARC 2Phi/c^2:", pr(adX))
lastNf = np.array([g["Nf"][-1] for g in gal]); P("SPARC N at last measured point (z_f):", pr(lastNf))
medNf = np.array([np.median(g["Nf"]) for g in gal]); P("SPARC per-galaxy median N:", pr(medNf), f"; share of galaxies with median in 30-50: {np.mean((medNf>=30)&(medNf<=50)):.3f}"); P(f"share of SPARC points N in 30-50: {np.mean((aNf>=30)&(aNf<=50)):.3f}; N<=1: {np.mean(aNf<=1):.4f}; N>1 {np.mean(aNf>1):.4f}")
P("By V_last bin: V range, galaxies, median N all points, N last, median zf, median 2Phi/c^2")
for lo, hi in ((0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
    sub = [g for g in gal if lo <= g["V"] < hi]
    if sub:
        P(f"  {lo}-{hi}: {len(sub)}, {np.median(np.concatenate([g['Nf'] for g in sub])):.1f}, {np.median([g['Nf'][-1] for g in sub]):.1f}, {np.median([g['zf'] for g in sub]):.2f}, {np.median(np.concatenate([g['dX'] for g in sub])):.2e}")
# A named L* like the claim's: solar-radius sized reference
Tsun = 2 * math.pi * 8.2 / 230 / KMS_KPC_GYR; Mmw = 230 ** 3 / (10 * G * H0)
P(f"Reference disc, r 8.2 kpc, v 230: T {Tsun:.3f} Gyr, N z_f {(T0 - tf(Mmw)) / Tsun:.1f} (z_f {zf_of(Mmw):.2f}), ceiling {T0 / Tsun:.1f}. Same halo at 100 kpc, v 200: {(T0 - tf(Mmw)) / (2*math.pi*100/200/KMS_KPC_GYR):.1f}; at R200 {230/(10*H0):.0f} kpc: {(T0 - tf(Mmw))*10*H0*KMS_KPC_GYR/(2*math.pi):.2f}")
# X-COP
XR = json.load(open(os.path.join(REPO, "real_research/data/xcop/xcop_r500_ettori2019.json")))
XS = (0.1, 0.2, 0.3, 0.5, 0.7); clu = []; rat = []
for name in sorted(k for k in XR if os.path.isdir(os.path.join(REPO, "real_research/data/xcop", k))):
    with fits.open(os.path.join(REPO, f"real_research/data/xcop/{name}/{name}_hydro_mass.fits")) as h:
        D = h[1].data.copy(); hd = h[1].header; R5 = float(hd["R500"]); z = float(hd["REDSHIFT"])
    rk = np.array(D["RADIUS"], float); MF = np.array(D["M_FORW"], float); MN = np.array(D["M_NFW"], float)
    J = XR[name]; M200 = J["M200"] * 1e14; R2 = J["R200"] * 1e3
    rat.append(float(np.interp(J["R500"] * 1e3, rk, MF)) / (J["M500"] * 1e14))
    clu.append(dict(name=name, z=z, R5=R5, R2=R2, M200=M200, rk=rk, MF=MF, MN=MN, zf=zf_of(M200)))
checks["K6"] = bool(k6a and 0.8 <= np.median(rat) <= 1.25); P(f"K6 X-COP M_FORW(R500)/M500 median {np.median(rat):.3f}: {checks['K6']}"); checks["K7b"] = len(clu) == 12; P(f"K7 clusters {len(clu)}: {checks['K7b']}")
def clprof(c, key="MF", r=None):
    M = float(np.exp(np.interp(math.log(r), np.log(c["rk"]), np.log(np.maximum(c[key], 1)))));
    v = math.sqrt(G * M / r)
    if MUT and True: v /= 30.0
    return M, v
def clphi(c, r, key="MF"):
    gr = np.geomspace(r, max(r * 1.0001, c["R2"]), 400); Ms = np.exp(np.interp(np.log(gr), np.log(c["rk"]), np.log(np.maximum(c[key], 1))))
    I = np.trapz(G * Ms / gr ** 2, gr) if r < c["R2"] else 0.0
    return -(I + G * c["M200"] / max(c["R2"], r))
SEL = []; rep = {}
for c in clu:
    t_ = T0 - tf(c["M200"])
    for lab, r in [("30 kpc", 30.), ("50 kpc", 50.), ("100 kpc", 100.)] + [(f"x{x:g}", x * c["R5"]) for x in XS] + [("R500", c["R5"]), ("R200", c["R2"])]:
        for key in ("MF", "MN"):
            M, v = clprof(c, key, r); T = 2 * math.pi * r / v / KMS_KPC_GYR
            rep.setdefault((lab, key), []).append((t_ / T, T0 / T, T, 2 * clphi(c, r, key) / c2, r))
P("X-COP medians over 12 (M_FORW | M_NFW): site, r kpc, T Gyr, N z_f, N z_f range, N ceiling, 2Phi/c^2")
for lab in ["30 kpc", "50 kpc", "100 kpc"] + [f"x{x:g}" for x in XS] + ["R500", "R200"]:
    a = np.array(rep[(lab, "MF")]); b = np.array(rep[(lab, "MN")])
    P(f"  {lab:8s} r {np.median(a[:,4]):7.0f} T {np.median(a[:,2]):6.3f} N {np.median(a[:,0]):6.2f} ({a[:,0].min():.2f}-{a[:,0].max():.2f}) ceil {np.median(a[:,1]):6.2f} 2Phi/c2 {np.median(a[:,3]):.2e} | NFW N {np.median(b[:,0]):6.2f} 2Phi/c2 {np.median(b[:,3]):.2e}")
xNf = np.concatenate([[v[0] for v in rep[(f"x{x:g}", "MF")]] for x in XS]); xNc = np.concatenate([[v[1] for v in rep[(f"x{x:g}", "MF")]] for x in XS]); xNfN = np.concatenate([[v[0] for v in rep[(f"x{x:g}", "MN")]] for x in XS])
xdX = np.concatenate([[v[3] for v in rep[(f"x{x:g}", "MF")]] for x in XS])
if MUT: xdX = np.full_like(xdX, -1e-12)
P(f"X-COP grid n {len(xNf)}: N z_f {pr(xNf)}; share N<=1 {np.mean(xNf<=1):.3f}; ceiling share N<=1 {np.mean(xNc<=1):.3f}; NFW share N<=1 {np.mean(xNfN<=1):.3f}")
# zf in a cluster core: if age were full ceiling, also z_f; L4 balanced error
def balerr(a_disc, a_clu):
    # discs above threshold, clusters below
    th = np.geomspace(min(a_disc.min(), a_clu.min()), max(a_disc.max(), a_clu.max()), 800)
    e = [0.5 * (np.mean(a_disc <= t) + np.mean(a_clu > t)) for t in th]; i = int(np.argmin(e)); return float(e[i]), float(th[i]), float(np.mean(a_disc <= th[i])), float(np.mean(a_clu > th[i]))
Bf, Bc, Bn = balerr(aNf, xNf), balerr(aNc, xNc), balerr(aNf, xNfN)
P(f"L4 best balanced misclassification (err, N_c, disc below, cluster above): z_f {Bf}; ceiling {Bc}; z_f with M_NFW {Bn}")
Blo = balerr(lastNf, xNf); P(f"  SPARC last point only vs X-COP grid: {Blo}")
# per-mass: fixed N contour radius per site
P("Radius where N = 1, 5, 30: X-COP median (kpc), reference disc (flat 230 km/s)")
for n in (1, 5, 30):
    rc = []
    for c in clu:
        t_ = T0 - tf(c["M200"]); gr = np.geomspace(c["rk"][0], c["rk"][-1], 300)
        Ns = np.array([t_ / (2 * math.pi * r / clprof(c, "MF", r)[1] / KMS_KPC_GYR) for r in gr]); 
        rc.append(float(gr[np.where(Ns >= n)[0][-1]]) if (Ns >= n).any() else float("nan"))
    rd = (T0 - tf(Mmw)) * 230 * KMS_KPC_GYR / (2 * math.pi * n)
    P(f"  N={n}: X-COP {np.nanmedian(rc):.0f} kpc = {np.nanmedian([a/c['R5'] for a,c in zip(rc,clu)]):.2f} R500; disc {rd:.0f} kpc")
# filament and background
rm = lambda z: NAT["Om"] * 2.775e11 * NAT["h"] ** 2 * (1 + z) ** 3 / 1e9   # Msun/kpc^3
GG = 4.30091e-6 * 1.0227 ** 2  # kpc^3 / Msun / Gyr^2
def Tden(rho): return math.sqrt(3 * math.pi / (GG * rho))
t3 = age(3, NAT); FIL = {}
for dlt in (1, 10, 100):
    Tf = Tden(rm(3) * (1 + dlt)); FIL[dlt] = dict(T=Tf, Nceil=t3 / Tf)
    ph = {L: -2 * math.pi * G * dlt * rm(3) * (L * 1e3) ** 2 for L in (0.1, 1.0)}
    FIL[dlt]["dX"] = {str(L): 2 * p / c2 for L, p in ph.items()}
    P(f"Filament z=3 delta {dlt}: T {Tf:.2f} Gyr, N ceiling {t3/Tf:.3f}; 2Phi/c2 L 0.1 Mpc {2*ph[0.1]/c2:.2e}, L 1 Mpc {2*ph[1.0]/c2:.2e}")
for z in (0, 3, 16):
    P(f"Unbound background z={z}: N {age(z,NAT)/Tden(rm(z)):.3f}")
# z=3 galaxy for completeness: same mean density as a disc at z=3 age ceiling
P(f"z=3 disc r 2 kpc, v 200 km/s: N ceiling {t3/(2*math.pi*2/200/KMS_KPC_GYR):.1f}, so age alone doesn't make z=3 wells N<=1")
# Transport form u.grad N = sqrt(4 pi G rho/3)/(2 pi): in the unbound background Friedmann gives dN/dlna = 1/(2 pi sqrt 2)
dNdl = 1 / (2 * math.pi * math.sqrt(2)); P(f"Transport N in the unbound background (flat, Lambda neglected): dN/dlna = {dNdl:.4f} in every era; N reaches 1 after {1/dNdl:.1f} e-folds; from z = 1100 to z = 3 N = {dNdl*math.log(1101/4):.2f}, from z = 1e9 {dNdl*math.log(1e9/4):.2f}. So a covariant N needs its own start surface, standing in for t_coll")
# L1
gapdc = abs(np.median(xdX)) - abs(np.median(adX)); spread = pc(np.abs(adX), 95) - pc(np.abs(adX), 5)
fX = [FIL[100]["dX"]["1.0"], FIL[1]["dX"]["0.1"]]
Xdisc = (Xb0 + pc(adX, 5), Xb0 + pc(adX, 95)); Xclu = (Xb0 + pc(xdX, 5), Xb0 + pc(xdX, 95)); Xfil = (Xb(3) + fX[0], Xb(3) + fX[1])
P(f"Total X: filament z=3 {Xfil[0]:.6f} to {Xfil[1]:.6f}; disc {Xdisc[0]:.7f} to {Xdisc[1]:.7f}; cluster {Xclu[0]:.7f} to {Xclu[1]:.7f}")
between = (Xfil[1] > Xdisc[1]) and (np.median(xdX) < np.median(adX))
overlap = (pc(xdX, 95) > pc(adX, 5)) and (pc(xdX,5) < pc(adX,95))
L1 = (not between) and (gapdc > spread)
P(f"L1 discs strictly between: {between}; |2Phi| median cluster {abs(np.median(xdX)):.2e}, disc {abs(np.median(adX)):.2e}, gap {gapdc:.2e}, disc spread p5-p95 {spread:.2e}, ranges overlap {overlap}; relative to |Xbar| {gapdc/abs(Xb0):.1e}; L1 PASS {L1}")
# depth vs. a z=0 filament: X at z=0 filament same as disc
P(f"z=0 unbound site: X = Xbar(0) {Xb0:.4f}; a disc differs by {abs(np.median(adX)):.2e}; Xbar(0)-Xbar(3) = {Xb0-Xb(3):.3f}, i.e. {abs(Xb0-Xb(3))/abs(np.median(adX)):.1e} disc depths. X's separation of z=3 from z=0 is a calendar: a z=3 galaxy and z=3 filament have the same Xbar")
# L2: X drift per orbit, tracked over a Hubble time: site independent per time
disc_r = 1 / np.median(aNf * 1.0); clu_r = 1 / np.median(xNf)
driftX = dict(disc=Xb0 - Xb(zf_of(Mmw)), cluster=Xb0 - Xb(zf_of(np.median([c["M200"] for c in clu]))))
ratioX = driftX["disc"] / driftX["cluster"]; ratioN = np.median(aNf) / np.median(xNf)
L2 = 0.5 <= ratioX / ratioN <= 2
P(f"L2 X accumulated since t_coll: disc {driftX['disc']:.3f}, cluster {driftX['cluster']:.3f} (ratio {ratioX:.2f}; Xbar(0)-Xbar(z_f): Hubble, not orbital); N ratio {ratioN:.2f}; PASS {L2}. On a fixed circular orbit dX/dN = 0 from the well, drift per orbit = {Xp0*Hg*Tsun:.4f} at the sun, {Xp0*Hg*2*math.pi*1000/1200/KMS_KPC_GYR:.4f} at 1 Mpc in a cluster: X doesn't count orbits, only elapsed cosmic time")
# Retarded correction
tau = 1e3 / C / KMS_KPC_GYR
P(f"Retarded delay: light crossing 1 Mpc {tau*1000:.2f} Myr vs T {2*math.pi*1000/1200/KMS_KPC_GYR:.2f} Gyr; memory in the well is (r/ct)^2 ~ {(tau/T0)**2:.1e}")
# L3
L3f = (np.mean(xNf <= 1) >= 0.9) and (np.mean(aNf > 1) >= 0.9); L3c = (np.mean(xNc <= 1) >= 0.9) and (np.mean(aNc > 1) >= 0.9); L3 = L3f and L3c
L4 = Bf[0] <= 0.05 and Bc[0] <= 0.05
L5 = FIL[100]["Nceil"] < pc(aNf, 5)
P(f"L3 CLAIM (N_c=1): z_f {L3f}, ceiling {L3c}: {L3}"); P(f"L4 any threshold <= 0.05 on both: {L4} (FITTED regardless: N_c {Bf[1]:.2f} z_f, {Bc[1]:.2f} ceiling)"); P(f"L5 filament delta 100 ceiling {FIL[100]['Nceil']:.3f} < SPARC p5 {pc(aNf,5):.2f}: {L5}")
# The density reading: N vs enclosed density
rhobar = lambda n, tt: n ** 2 * 3 * math.pi / (GG * tt ** 2)
for n in (1, 5, 30):
    rb = rhobar(n, 8.0); P(f"N={n} at age 8 Gyr is mean density {rb:.3g} Msun/kpc^3 = {rb/rm(0):.0f} x rho_m(0): N is sqrt(mean enclosed density) times an age")
ok = all(checks.values()); P("checks", checks, "ALL", ok)
label = None
if not ok: label = "NO VERDICT, check failed"
elif L3 and not MUT: label = "SEPARATOR SURVIVES"
elif MUT: label = "MUTATE RUN"
else: label = "ARGUMENT FAILS" + (" [FILAMENT PAIR ONLY]" if L5 else "")
P("LABEL", label)
res = dict(label=label, checks=checks, t0=T0, Xbar={"0": Xb0, "3": Xb(3)}, sparc=dict(N_zf={str(q): pc(aNf, q) for q in (5, 50, 95)}, N_ceil={str(q): pc(aNc, q) for q in (5, 50, 95)}, share_gt1=float(np.mean(aNf > 1)), last_N={str(q): pc(lastNf, q) for q in (5, 50, 95)}, dX50=float(np.median(adX))),
           xcop=dict(N_zf={str(q): pc(xNf, q) for q in (5, 50, 95)}, share_le1=float(np.mean(xNf <= 1)), share_le1_ceil=float(np.mean(xNc <= 1)), by={k: float(np.median([v[0] for v in rep[(k, 'MF')]])) for k in ["30 kpc", "50 kpc", "100 kpc", "x0.1", "x0.2", "x0.3", "x0.5", "x0.7", "R500", "R200"]}, dX50=float(np.median(xdX))),
           L1=bool(L1), between=bool(between), L2=bool(L2), L3=bool(L3), L3f=bool(L3f), L3c=bool(L3c), L4=bool(L4), L4_zf=Bf, L4_ceil=Bc, L5=bool(L5), filament={str(k): v for k, v in FIL.items()})
json.dump(res, open(os.path.join(HERE, f"dr4{TAG}_results.json"), "w"), indent=1, default=float)
out.close(); sys.exit(0 if ok else 1)
