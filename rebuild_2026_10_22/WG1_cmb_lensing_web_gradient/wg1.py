#!/usr/bin/env python3
"""WG1: where the potential that CMB lensing measures sits on the law's acceleration scale (FROZEN_CRITERIA.md, commit 2971b542c2).

Planck PR4 lensing, CMB-marginalised, L 8-400 (CFG917's loader, imported read only). Limber projection (Hu 2001 eq. 2) of a broad
potential-spectrum family, Delta^2_Psi = A G(z)^2 / [1 + (k/k_t)^2]^(beta/2), over a 90-member bracket of background (Omega_m, H0),
potential evolution p and high-k slope beta. No LCDM spectrum, transfer function, halofit or LCDM background enters any model or verdict.
Run: python3 wg1.py            (writes wg1_results.json, wg1.out)
     python3 wg1.py --mutate   (lensing kernel loses its factor 2; writes wg1_MUTATE_results.json, wg1_MUTATE.out; K1 must FAIL)
kappa = 1/2 FITTED; the cold sector stays retired; nothing here says the data favour the framework; not theory closed."""
import os, sys, json, math, hashlib, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG917_cmb_lensing_gate")); import cfg917_lib as LB   # read only
sys.path.insert(0, os.path.join(REPO, "a0kit")); import a0kit                                                        # read only
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
t0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

C_KMS = 299792.458; C_MS = 299792458.0; MPC_M = 3.0856775814913673e22
ZS = 1090.0; OMR_H2 = 4.18e-5; ZCAP = 5.0
LS = np.arange(8, LB.LMAX + 1)                      # every L any window touches (W: 8-400, M: 8-2500)
L4 = (LS * (LS + 1.0)) ** 2 / (2 * math.pi)         # X_L = [L(L+1)]^2 C_L / 2 pi
KT_GRID = np.geomspace(1e-3, 1.0, 121)
Z_GRADED = [0.5, 1.0, 1.5, 2.0, 2.33]; Z_CONTEXT = [3.0]
TIE_Z = [0.0, 1.0, 1.5, 2.33]
TIE_LOW = [1.00, 0.76, 0.71, 0.33]; TIE_MID = [1.00, 0.91, 0.94, 0.91]     # PAPER67 v1.0 band (CFG689), 68 % lower edge and centre
FOOT = a0kit.footings()
OMB = [0.0210, 0.0230]                               # D1/D2 bracket, PROVISIONAL from memory (BBN D/H, either rate set)
H100_C2 = (100.0 / C_KMS) ** 2                       # (100 km/s/Mpc / c)^2 in Mpc^-2

# ------------------------------------------------------------------ background bracket and Limber engine
def make_bg(Om, H0):
    h = H0 / 100.0; Or = OMR_H2 / h ** 2; OL = 1.0 - Om - Or
    z = np.concatenate([np.linspace(0.0, 10.0, 8001), np.geomspace(10.0, ZS, 4001)[1:]])
    E = np.sqrt(Or * (1 + z) ** 4 + Om * (1 + z) ** 3 + OL)
    f = C_KMS / H0 / E
    chi = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(z))])
    chis = float(chi[-1])
    cg = np.concatenate([np.geomspace(1e-3, 100.0, 160), np.linspace(100.0, chis, 700)[1:]])
    w = np.zeros_like(cg); w[1:] += 0.5 * np.diff(cg); w[:-1] += 0.5 * np.diff(cg)
    zg = np.interp(cg, chi, z)
    fac = 1.0 if MUT else 2.0                          # MUTATE: the kernel loses its factor 2
    q = fac * (chis - cg) / (cg * chis)
    ker = w * q ** 2 / cg ** 2
    k = (LS[:, None] + 0.5) / cg[None, :]
    return dict(Om=Om, H0=H0, z=z, chi=chi, E=E, chis=chis, cg=cg, zg=zg, ker=ker, k2=k ** 2, kinv3=1.0 / k ** 3)

def limber_core(bg, Pmat, kw=None):
    """C_L for L in LS: sum over the chi grid of ker(chi) * P_Psi((L+1/2)/chi, z(chi)); Pmat has shape (len(LS), len(chi grid))."""
    return (Pmat * (bg["ker"] if kw is None else kw)[None, :]).sum(axis=1)

def chi_of(bg, z): return float(np.interp(z, bg["z"], bg["chi"]))
def E_of(bg, z): return np.interp(z, bg["z"], bg["E"])
def G2(z, p): return (1.0 + np.minimum(z, ZCAP)) ** (2.0 * p)

def shape(x2, beta):
    """1 / (1 + x^2)^(beta/2) without np.power on the big matrix."""
    s = 1.0 + x2
    if beta == 2: return 1.0 / s
    if beta == 4: return 1.0 / (s * s)
    if beta == 3: return 1.0 / (s * np.sqrt(s))
    return s ** (-beta / 2.0)

def limber_X(bg, p, beta, kt, rz=None):
    """X_L for A = 1: [L(L+1)]^2/(2 pi) * sum_chi ker * P_Psi(k, z), P_Psi = 2 pi^2 Delta^2 / k^3; rz(z) multiplies P (V3 only)."""
    kp = bg["ker"] * G2(bg["zg"], p)
    if rz is not None: kp = kp * rz(bg["zg"])
    S = limber_core(bg, bg["kinv3"] * shape(bg["k2"] / kt ** 2, beta), kw=kp)
    X = np.zeros(LB.LMAX + 1); X[LS] = L4 * 2 * math.pi ** 2 * S
    return X

# ------------------------------------------------------------------ gradient of the potential
def grad_var(kt, beta, kmin, kmax, ppd=300):
    """int d ln k k^2 / (1 + (k/k_t)^2)^(beta/2), log-trapezoid at ppd points per decade (A = 1, G = 1)."""
    n = max(int(math.ceil(ppd * math.log10(kmax / kmin))) + 1, 3)
    lk = np.linspace(math.log(kmin), math.log(kmax), n); k = np.exp(lk)
    f = k ** 2 * shape((k / kt) ** 2, beta)
    return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(lk)))

def g_web(bg, p, beta, kt, A, z, full=False):
    """physical rms gradient c^2 (1+z) sigma_gradPsi (m/s^2) over the modes the data see at z (8.5/chi .. 400.5/chi)."""
    ch = chi_of(bg, z)
    kmin, kmax = (1e-4, 1.0) if full else (8.5 / ch, 400.5 / ch)
    s2 = A * G2(z, p) * grad_var(kt, beta, kmin, kmax)
    return C_MS ** 2 * (1 + z) * math.sqrt(max(s2, 0.0)) / MPC_M

# ------------------------------------------------------------------ data and fits
D = LB.load_pr4()
def sha(paths):
    h = hashlib.sha256()
    for f in paths: h.update(open(f, "rb").read())
    return h.hexdigest()
PR4 = lambda s: os.path.join(LB.PR4D, LB.STEM + s)
HASH = {"bandpowers": sha([PR4("_bandpowers.dat")]), "cov_CMBmarged": sha([PR4("_CMBmarged_cov.dat")]),
        "fiducial_correction_CMBmarged": sha([PR4("_CMBmarged_lensing_fiducial_correction.dat")]),
        "windows_W": sha([PR4(f"_window/window{b}.dat") for b in range(1, 10)]),
        "windows_M": sha([PR4(f"_CMBmarged_lens_delta_window/window{b}.dat") for b in range(1, 10)]),
        "cfg917_lib.py": sha([LB.__file__]), "a0kit.py": sha([a0kit.__file__])}

def u_of(X, rule):
    return LB.wsum(D["W"], X) + (LB.wsum(D["M"], X) if rule == "PACKAGE" else 0.0)

def fit_A(u, rule, d):
    """B = A u - F (PACKAGE) or A u (PLAIN); A linear. Returns A, sigma_A, chi2."""
    t = d + D["F"] if rule == "PACKAGE" else d
    b = LB.qform(u, D["Cinv"]); A = LB.qform(u, D["Cinv"], t) / b
    r = A * u - t
    return A, 1.0 / math.sqrt(b), LB.qform(r, D["Cinv"])

def fit_member(bg, p, beta, rules, dvec=None):
    """profile chi2 over k_t (grid + bounded refine) for each rule; returns per-rule dict."""
    d = D["d"] if dvec is None else dvec
    grid = {r: [] for r in rules}
    for kt in KT_GRID:
        X = limber_X(bg, p, beta, kt)
        for r in rules:
            grid[r].append(fit_A(u_of(X, r), r, d))
    res = {}
    for r in rules:
        c2 = np.array([g[2] for g in grid[r]]); i = int(np.argmin(c2))
        lo, hi = math.log(KT_GRID[max(i - 1, 0)]), math.log(KT_GRID[min(i + 1, len(KT_GRID) - 1)])
        f = lambda lk: fit_A(u_of(limber_X(bg, p, beta, math.exp(lk)), r), r, d)[2]
        m = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-6})
        ktb = math.exp(m.x); Ab, sAb, c2b = fit_A(u_of(limber_X(bg, p, beta, ktb), r), r, d)
        if c2[i] < c2b: ktb, (Ab, sAb, c2b) = KT_GRID[i], grid[r][i]
        env = [(KT_GRID[j], grid[r][j][0], grid[r][j][1]) for j in range(len(KT_GRID)) if c2[j] <= c2b + 4.0] + [(ktb, Ab, sAb)]
        res[r] = dict(kt=ktb, A=Ab, sigA=sAb, chi2=c2b, pval=float(CHI2.sf(c2b, len(d) - 2)), env=env)
    return res

# ------------------------------------------------------------------ checks
P(f"WG1{TAG}: CMB-lensing web gradient (FROZEN_CRITERIA.md, 2971b542c2). kappa = 1/2 FITTED; not theory closed.")
P(f"  footings (a0kit): canonical {FOOT['canonical']:.4e}, alt {FOOT['alt']:.4e} m/s^2; MUTATE = {MUT}")
CHK = {}
bgK = make_bg(0.30, 65.0)
Lk = np.array([10, 100, 1000])
Cl = limber_core(bgK, bgK["k2"] ** -2)               # P_Psi = k^-4, G = 1
Xk = Cl[Lk - LS[0]]
Xa = 4 * bgK["chis"] / (3 * (Lk + 0.5) ** 4)
e1 = float(np.max(np.abs(Xk / Xa - 1))); CHK["K1"] = dict(pass_=e1 < 1e-3, max_rel_err=e1, tol=1e-3)
P(f"  K1 Limber vs 4 chi_s/[3(L+1/2)^4] at L 10/100/1000: max rel err {e1:.2e} (tol 1e-3) -> {'PASS' if e1 < 1e-3 else 'FAIL'}")
e2 = max(abs(grad_var(kt, 4, 1e-6 * kt, 1e4 * kt) / (kt ** 2 / 2) - 1) for kt in (0.01, 0.05))
CHK["K2"] = dict(pass_=e2 < 1e-3, max_rel_err=e2, tol=1e-3)
P(f"  K2 gradient integral vs k_t^2/2 at k_t 0.01/0.05: max rel err {e2:.2e} (tol 1e-3) -> {'PASS' if e2 < 1e-3 else 'FAIL'}")
lmin, lmax = D["lmin"], D["lmax"]
contig = bool(lmin[0] == 8 and lmax[-1] == 400 and all(lmin[i + 1] == lmax[i] + 1 for i in range(D["n"] - 1)))
posdef = bool(np.all(np.linalg.eigvalsh(D["C"]) > 0))
CHK["K4"] = dict(pass_=bool(D["n"] == 9 and contig and posdef), n=int(D["n"]), contiguous=contig, posdef=posdef, hashes=HASH)
P(f"  K4 data: {D['n']} bins, contiguous L 8-400 {contig}, covariance positive definite {posdef} -> {'PASS' if CHK['K4']['pass_'] else 'FAIL'}")
for k_, v in HASH.items(): P(f"     sha256 {k_}: {v}")
K3 = []
for (Om, H0, p, beta, kt) in [(0.30, 65.0, 0.0, 3, 0.02), (0.05, 75.0, -0.5, 4, 0.005), (1.00, 65.0, 0.5, 2, 0.05)]:
    bg = make_bg(Om, H0)
    Xt = limber_X(bg, p, beta, kt)
    At = fit_A(u_of(Xt, "PACKAGE"), "PACKAGE", D["d"])[0]
    dsyn = At * u_of(Xt, "PACKAGE") - D["F"]
    fr = fit_member(bg, p, beta, ["PACKAGE"], dvec=dsyn)["PACKAGE"]
    gt = g_web(bg, p, beta, kt, At, 1.5); gr = g_web(bg, p, beta, fr["kt"], fr["A"], 1.5)
    K3.append(dict(member=[Om, H0, p, beta], kt_true=kt, kt_rec=fr["kt"], g_true=gt, g_rec=gr, rel=abs(gr / gt - 1)))
    P(f"  K3 round trip Om {Om} H0 {H0} p {p} beta {beta}: k_t {kt} -> {fr['kt']:.5f}, g_web(1.5) rel err {abs(gr / gt - 1):.2e}")
e3 = max(x["rel"] for x in K3); CHK["K3"] = dict(pass_=e3 < 0.01, max_rel_err=e3, tol=0.01, cases=K3)
P(f"  K3 max rel err {e3:.2e} (tol 1e-2) -> {'PASS' if e3 < 0.01 else 'FAIL'}")
ALLK = all(CHK[k]["pass_"] for k in ("K1", "K2", "K3", "K4"))
P(f"  all K checks: {'PASS' if ALLK else 'FAIL'}  ({time.time() - t0:.0f} s)")

# ------------------------------------------------------------------ the 90-member bracket
RULES = ["PACKAGE", "PLAIN"]
MEM = []
BG = {(Om, H0): make_bg(Om, H0) for Om in (0.05, 0.30, 1.00) for H0 in (65.0, 75.0)}
for (Om, H0), bg in BG.items():
    for p in (-1.0, -0.5, 0.0, 0.5, 1.0):
        for beta in (2, 3, 4):
            fr = fit_member(bg, p, beta, RULES)
            for r in RULES:
                f = fr[r]; acc = f["pval"] >= 1e-3
                row = dict(rule=r, Om=Om, H0=H0, p=p, beta=beta, chi2=f["chi2"], pval=f["pval"], accepted=bool(acc),
                           kt=f["kt"], A=f["A"], sigA=f["sigA"], chis=bg["chis"], g={}, g_hi={}, g_lo={}, g_full={})
                for z in Z_GRADED + Z_CONTEXT:
                    row["g"][str(z)] = g_web(bg, p, beta, f["kt"], f["A"], z)
                    row["g_full"][str(z)] = g_web(bg, p, beta, f["kt"], f["A"], z, full=True)
                    gh = [g_web(bg, p, beta, kt, A + 2 * sA, z) for kt, A, sA in f["env"]]
                    gl = [g_web(bg, p, beta, kt, max(A - 2 * sA, 0.0), z) for kt, A, sA in f["env"]]
                    row["g_hi"][str(z)] = max(gh); row["g_lo"][str(z)] = min(gl)
                MEM.append(row)
    P(f"  background Om {Om} H0 {H0}: chi_s {bg['chis']:.0f} Mpc, 15 members fitted ({time.time() - t0:.0f} s)")

def a0z(fp, rule, z, bg=None):
    if rule == "TIE-LOW": return FOOT[fp] * float(np.interp(z, TIE_Z, TIE_LOW))
    if rule == "TIE-MID": return FOOT[fp] * float(np.interp(z, TIE_Z, TIE_MID))
    return FOOT[fp] * float(E_of(bg, z))

P("")
P("Members (best fit; g in units of the canonical a0(0) at z 1.5, data-range modes):")
P("  rule     Om   H0   p     beta chi2   p-val   acc  k_t[1/Mpc]  g(1.5)/a0c  g_hi(1.5)/a0c")
for m in MEM:
    P(f"  {m['rule']:<8} {m['Om']:<4} {m['H0']:<4.0f} {m['p']:<5} {m['beta']:<4} {m['chi2']:<6.2f} {m['pval']:<7.3g} "
      f"{'Y' if m['accepted'] else 'n'}    {m['kt']:<11.4g} {m['g']['1.5'] / FOOT['canonical']:<11.4g} {m['g_hi']['1.5'] / FOOT['canonical']:.4g}")

# ------------------------------------------------------------------ V1
def label(R):
    return "DEEP" if R < 0.1 else ("TRANSITION" if R < 1.0 else "SHALLOW")
V1 = {}
P(""); P("V1: R = max over accepted members and z in {0.5, 1, 1.5, 2, 2.33} of g_hi(z)/a0(z), TIE-LOW")
for fp in ("canonical", "alt"):
    V1[fp] = {}
    for r in RULES:
        acc = [m for m in MEM if m["rule"] == r and m["accepted"]]
        if not ALLK or not acc:
            V1[fp][r] = dict(label="NOT EVALUABLE", n_accepted=len(acc)); continue
        R, arg = -1.0, None
        for m in acc:
            for z in Z_GRADED:
                v = m["g_hi"][str(z)] / a0z(fp, "TIE-LOW", z)
                if v > R: R, arg = v, (m["Om"], m["H0"], m["p"], m["beta"], z)
        bgs = lambda m: BG[(m["Om"], m["H0"])]
        Rmid = max(m["g_hi"][str(z)] / a0z(fp, "TIE-MID", z) for m in acc for z in Z_GRADED)
        Rriv = max(m["g_hi"][str(z)] / a0z(fp, "RIVAL", z, bgs(m)) for m in acc for z in Z_GRADED)
        rmin = min(m["g_lo"][str(z)] / a0z(fp, "RIVAL", z, bgs(m)) for m in acc for z in Z_GRADED)
        best = [m["g"][str(z)] / a0z(fp, "TIE-MID", z) for m in acc for z in Z_GRADED]
        ctx = max(m["g_hi"]["3.0"] / a0z(fp, "TIE-LOW", 3.0) for m in acc)
        V1[fp][r] = dict(label=label(R), R=R, argmax=arg, n_accepted=len(acc), R_tie_mid=Rmid, R_rival=Rriv, min_glo_over_a0_rival=rmin,
                         best_fit_TIE_MID_range=[min(best), max(best)], context_z3_TIE_LOW=ctx)
        P(f"  {fp:<9} {r:<7}: {len(acc)} accepted; R = {R:.4f} at (Om, H0, p, beta, z) = {arg} -> {label(R)}; "
          f"TIE-MID {Rmid:.4f}, RIVAL {Rriv:.4f}; smallest g_lo/a0 (RIVAL) {rmin:.2e}; best fits (TIE-MID) {min(best):.4f}-{max(best):.4f}; "
          f"z 3 context {ctx:.4f}")
    labs = {V1[fp][r]["label"] for r in RULES}
    V1[fp]["label"] = labs.pop() if len(labs) == 1 else "SPLIT"
    P(f"  {fp}: V1 = {V1[fp]['label']}")

# ------------------------------------------------------------------ V2
mode_a = any(V1[fp]["label"] in ("DEEP", "TRANSITION") for fp in ("canonical", "alt"))
V2 = dict(label="NOT EVALUABLE FOR THE LAW ALONE" if ALLK else "NOT EVALUABLE (K check failed)",
          missing=(["(a) the law's rule on the linear web (V1 puts the measured field inside the law's range)"] if mode_a else []) +
                  ["(b) a baryon field at z 0.5-3 on k ~ 0.003-0.2 / Mpc that doesn't use a cold term"])
P(""); P(f"V2 (board D9, law alone): {V2['label']}; missing: " + "; ".join(V2["missing"]))

# ------------------------------------------------------------------ V3 (frozen: no cap on the a0(z) rules) and a labelled post-hoc cap
def v3(acc, cap=None):
    rows = []
    for m in acc:
        bg = BG[(m["Om"], m["H0"])]
        zc = (lambda z: z) if cap is None else (lambda z: np.minimum(z, cap))
        rr = lambda z: np.interp(zc(z), bg["z"], bg["E"])
        rt = lambda z: np.interp(zc(z), TIE_Z, TIE_MID)
        br = LB.wsum(D["W"], limber_X(bg, m["p"], m["beta"], m["kt"], rz=rr))
        bt = LB.wsum(D["W"], limber_X(bg, m["p"], m["beta"], m["kt"], rz=rt))
        ratio = br / bt
        rows.append(dict(member=[m["Om"], m["H0"], m["p"], m["beta"]], lever_median=float(np.median(ratio)),
                         S=float(ratio.max() / ratio.min() - 1), ratio=ratio.tolist()))
    return rows
accP = [m for m in MEM if m["rule"] == "PLAIN" and m["accepted"]]
V3 = {}
P(""); P("V3: B_b(RIVAL)/B_b(TIE-MID), PLAIN rule, accepted members at best fit (deep limit, P_Psi ~ a0(z) at fixed source)")
for name, cap in (("frozen_no_cap", None), ("POSTHOC_cap_z2.33", 2.33), ("POSTHOC_cap_z5", 5.0)):
    rows = v3(accP, cap) if ALLK else []
    if rows:
        Smax = max(r["S"] for r in rows); lev = [r["lever_median"] for r in rows]
        read = ("C_L^phiphi alone can't separate the two a0(z) rules from the source amplitude; tomography or a fixed source is required"
                if Smax < 0.10 else "S >= 0.10 in: " + ", ".join(str(r["member"]) for r in rows if r["S"] >= 0.10))
        V3[name] = dict(n=len(rows), lever_min=min(lev), lever_max=max(lev), S_max=Smax, reading=read, rows=rows)
        P(f"  {name:<18}: {len(rows)} members; median lever {min(lev):.3g}-{max(lev):.3g}; max shape spread S {Smax:.3f} -> {read}")
    else:
        V3[name] = dict(n=0, reading="NOT EVALUABLE")
        P(f"  {name}: NOT EVALUABLE")

# ------------------------------------------------------------------ D1, D2 (diagnostics, not graded)
P(""); P("D1/D2 (not graded): baryon contrast Delta_db the measured potential needs, per ln k; OFF = Newtonian baryons only, ON = simple form")
DG = {}
for r in RULES:
    acc = [m for m in MEM if m["rule"] == r and m["accepted"]]
    DG[r] = {}
    for z in (1.0, 2.0):
        for kname in ("k_t", "0.02"):
            off, on = [], {"canonical": [], "alt": []}
            for m in acc:
                k = m["kt"] if kname == "k_t" else 0.02
                dpsi = math.sqrt(m["A"] * G2(z, m["p"]) * shape((k / m["kt"]) ** 2, m["beta"]))
                for ob in OMB:
                    v = (2.0 / 3.0) * k ** 2 * dpsi / (ob * H100_C2 * (1 + z)); off.append(v)
                    for fp in on:
                        g = m["g"][str(z)]; on[fp].append(v * g / (g + a0z(fp, "TIE-MID", z)))
            if not off: continue
            DG[r][f"z{z}_k{kname}"] = dict(OFF=[min(off), max(off)], ON_canonical=[min(on["canonical"]), max(on["canonical"])],
                                         ON_alt=[min(on["alt"]), max(on["alt"])])
            P(f"  {r:<7} z {z} k {kname:<4}: OFF {min(off):.3g}-{max(off):.3g}; ON canonical {min(on['canonical']):.3g}-{max(on['canonical']):.3g}, "
              f"alt {min(on['alt']):.3g}-{max(on['alt']):.3g}")

# ------------------------------------------------------------------ write
P(""); P(f"done in {time.time() - t0:.0f} s. kappa = 1/2 FITTED; not theory closed.")
RES = dict(lane="WG1_cmb_lensing_web_gradient", criteria_commit="2971b542c2", mutate=MUT, footings=FOOT, checks=CHK, all_K_pass=ALLK,
           V1=V1, V2=V2, V3=V3, D1_D2=DG, members=[{k: v for k, v in m.items()} for m in MEM],
           inputs=dict(tie_z=TIE_Z, tie_low=TIE_LOW, tie_mid=TIE_MID, omega_b_bracket=OMB, kt_grid=[1e-3, 1.0, 121], z_cap_G=ZCAP,
                       omega_r_h2=OMR_H2, z_s=ZS, data=LB.rel(LB.PR4D) + "/" + LB.STEM))
def _clean(o):
    if isinstance(o, dict): return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(_clean(RES), open(os.path.join(HERE, f"wg1{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"wg1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
