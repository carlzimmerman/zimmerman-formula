"""CFG689 (criteria 1c237145d): BAO with the framework's own ruler.
CFG654's principle (pre-switch universe = framework physics; A1 pair omega_b 0.02236 / omega_c 0.1202) fixes r_d with CAMB, and
CFG253 (<= 3% of the cold mass made after recombination) fixes rho_m(z) = omega_m (1+z)^3. DESI DR2 D_H/r_d is then an absolute
H(z), and the physical dark-energy density w(z) = rho_DE/rho_crit,100 is free per node (6 nodes, w(0) free too). No CMB distances,
no CPL, no LCDM late-time fit. Data: DESI DR2 table + Pantheon+ shape, verbatim from CFG681.
Modes (env CFG689_MODE): primary, M1, M2, M3, B1, B2, B3m, B3p, B4m, B4p, B5a, B5b, B5c, B6. Outputs cfg689[_MODE].out/.json.
Exit 75 = a PM / 1024^3 / chain process appeared: no verdict is written, and the waiter re-gates and reruns the mode.
Implementation notes (not in the criteria, no verdict weight): B5 frees omega_c over 0.05-0.25, where a +-2 sigma power law in
omega_c cannot be trusted, so B5 interpolates a CAMB table in omega_c (21 points, cubic in log-log; K2b checks it at three off-grid
points); the free fit also starts from the constant-w best fit (it can only lower the free chi^2)."""
import json, os, sys, subprocess, numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as CHI2, norm as NORM
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__)); MODE = os.environ.get("CFG689_MODE", "primary")
NSTEP = int(os.environ.get("CFG689_NSTEP", "60000")); FROZEN_NSTEP = 60000
EXT = os.path.join(HERE, "..", "..", "..", "_external_data", "pantheonplus_dr")
TAG = "" if MODE == "primary" else "_" + MODE
OUTF = open(os.path.join(HERE, f"cfg689{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
BUSY = r"cfg6[0-9][0-9]_pm\.py|cfg650_pm|cfg596_pm|run_65[04]\.py|overnight_chain/chain[0-9]*\.sh|argon11_run\.py|cfg6[0-9][0-9]_native\.py"
def guard():
    if subprocess.run(["pgrep", "-f", BUSY], capture_output=True).returncode == 0:
        P(f"GUARD: a PM / 1024^3 / chain process is alive -> exit 75 (no verdict; mode {MODE} reruns later)"); sys.exit(75)
guard()
P(f"CFG689 mode={MODE}  NSTEP={NSTEP}" + ("" if NSTEP == FROZEN_NSTEP else f"  (NOT the frozen {FROZEN_NSTEP}: no verdict weight)"))

# ---- constants and data (DESI DR2 table verbatim from cfg681_bao.py) ----
C = 299792.458; G = 6.67430e-11; CMS = 2.99792458e8; RHO100 = 1.87847e-26; OMG = 2.4728e-5
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = (0.295, 7.942, 0.075)
CINV = [np.linalg.inv(np.array([[s1**2, r*s1*s2], [r*s1*s2, s2**2]])) for (_, _, _, s1, _, s2, r) in ANISO]
zg = np.linspace(0, 2.5, 5001); ZS = (1.0, 1.2, 1.5, 2.33)
CFG683_W = {1.0: 0.853, 1.5: 1.596, 2.33: 2.183}                     # CFG683 CMB-free BAO+SN tracking band widths
P3S = {"KURVS-CDFS z~1.5 (gas unmeasured)": (1.5, 0.30), "z~1.2 multi-tracer (deep-MOND best case)": (1.2, 0.162),
       "RC100/CRISTAL optimistic": (2.33, 0.125), "RC100/CRISTAL realistic": (2.33, 0.40)}

# ---- mode configuration (criteria sections 3, 7, 9) ----
cfg = dict(wb=0.02236, sb=0.00015, wc=0.1202, sc=0.0014, rho=0.0, mnu=0.0, f=0.0, hp=None, wcfree=False,
           nodes=np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33]), rds=1.0)
if MODE == "B1": cfg.update(wb=0.02193, sb=0.00022)
elif MODE == "B2": cfg.update(mnu=0.06)
elif MODE == "B3m": cfg.update(rho=-0.5)
elif MODE == "B3p": cfg.update(rho=0.5)
elif MODE == "B4m": cfg.update(f=-0.03)
elif MODE == "B4p": cfg.update(f=0.03)
elif MODE in ("B5a", "B5b", "B5c"): cfg.update(wb=0.02193, sb=0.00022, wcfree=True, hp=({"B5a": 0.680, "B5b": 0.700, "B5c": 0.7304}[MODE], 0.0104))
elif MODE == "B6": cfg.update(nodes=np.array([0, 0.7, 1.5, 2.33]))
elif MODE == "M3": cfg.update(rds=1.02)
elif MODE not in ("primary", "M1", "M2"): sys.exit(f"unknown CFG689_MODE {MODE}")
NODES = cfg["nodes"]; NN = len(NODES); wb0, sb, wc0, sc = cfg["wb"], cfg["sb"], cfg["wc"], cfg["sc"]
OMNU = cfg["mnu"]/93.14; NREL = 3.044 if cfg["mnu"] == 0 else 3.044*2/3; OMR = OMG*(1 + 0.2271*NREL)

# ---- the ruler: CAMB in the pre-switch era (cfg654_ics.camb_results settings) ----
def camb_rdrag(wb, wc, mnu=0.0, h=0.6777):
    import camb
    p = camb.CAMBparams()
    p.set_cosmology(H0=100*h, ombh2=wb, omch2=wc, omk=0.0, mnu=mnu, num_massive_neutrinos=(1 if mnu > 0 else 0), nnu=3.044,
                    TCMB=2.7255, tau=0.0544)
    p.set_dark_energy(w=-1.0, wa=0.0); p.set_accuracy(AccuracyBoost=1.5, lAccuracyBoost=1.0); p.WantCls = False
    return float(camb.get_background(p).get_derived_params()["rdrag"])
res = {"mode": MODE, "nstep": NSTEP, "cfg": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in cfg.items()}}
R0 = camb_rdrag(wb0, wc0, cfg["mnu"])
BEXP = -np.log(camb_rdrag(wb0 + 2*sb, wc0, cfg["mnu"])/camb_rdrag(wb0 - 2*sb, wc0, cfg["mnu"]))/np.log((wb0 + 2*sb)/(wb0 - 2*sb))
if not cfg["wcfree"]:
    CEXP = -np.log(camb_rdrag(wb0, wc0 + 2*sc, cfg["mnu"])/camb_rdrag(wb0, wc0 - 2*sc, cfg["mnu"]))/np.log((wc0 + 2*sc)/(wc0 - 2*sc))
    def rdrag(wb, wc): return R0*(wb/wb0)**(-BEXP)*(wc/wc0)**(-CEXP)
else:
    CEXP = None; WCG = np.linspace(0.05, 0.25, 21); SPL = CubicSpline(np.log(WCG), np.log([camb_rdrag(wb0, x, cfg["mnu"]) for x in WCG]))
    def rdrag(wb, wc): return float(np.exp(SPL(np.log(wc))))*(wb/wb0)**(-BEXP)
res["ruler"] = dict(r_d0=R0, b=BEXP, c=CEXP)
P(f"ruler: r_d0 = {R0:.4f} Mpc at omega_b {wb0} omega_c {wc0} mnu {cfg['mnu']}; exponents b {BEXP:.5f} c {CEXP}")
checks = {}
if MODE == "primary":
    k1 = dict(A1=camb_rdrag(0.02236, 0.1202), BBN=camb_rdrag(0.02193, 0.1202), BBN_mnu=camb_rdrag(0.02193, 0.1202, 0.06))
    tgt = dict(A1=147.0667, BBN=147.5453, BBN_mnu=147.5381)
    checks["K1"] = dict(values=k1, targets=tgt, ok=bool(all(abs(k1[k] - tgt[k]) <= 0.02 for k in tgt)))
    dev = [abs(rdrag(wb0 + i*2*sb, wc0 + j*2*sc)/camb_rdrag(wb0 + i*2*sb, wc0 + j*2*sc) - 1) for i in (-1, 1) for j in (-1, 1)]
    dh = [abs(camb_rdrag(wb0, wc0, 0.0, h)/R0 - 1) for h in (0.6277, 0.7277)]
    checks["K2"] = dict(corner_dev=dev, h_dev=dh, ok=bool(max(dev) <= 2e-4 and max(dh) < 1e-4))
if cfg["wcfree"]:
    dev = [abs(rdrag(wb0, x)/camb_rdrag(wb0, x, cfg["mnu"]) - 1) for x in (0.087, 0.143, 0.211)]
    checks["K2b"] = dict(dev=dev, ok=bool(max(dev) <= 2e-4))
for k, v in checks.items(): P(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v}")

# ---- Pantheon+ (as CFG681) ----
raw = np.genfromtxt(os.path.join(EXT, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
covfull = np.loadtxt(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1); NSN = int(round(np.sqrt(covfull.size))); covfull = covfull.reshape(NSN, NSN)
sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)
zhd, zhel, MB = raw["zHD"][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float); Cisn = np.linalg.inv(covfull[np.ix_(sel, sel)])
del covfull
one = np.ones(len(MB)); A11 = one@Cisn@one
DATA_A, DATA_B = list(ANISO), BGS

# ---- model ----
def bg(wn, wb, wc):
    om = wb + wc*(1 + cfg["f"]) + OMNU
    E2 = om*(1 + zg)**3 + OMR*(1 + zg)**4 + np.interp(zg, NODES, wn)
    if np.any(E2 <= 1e-8): return None
    Hg = 100*np.sqrt(E2); I = np.r_[0, np.cumsum(0.5*(1/Hg[1:] + 1/Hg[:-1])*np.diff(zg))]*C     # D_M in Mpc
    return om, Hg, I
def bao_pred(Hg, I):
    ms = [np.array([np.interp(t[1], zg, I), C/np.interp(t[1], zg, Hg)]) for t in ANISO]
    zb = BGS[0]; DM = np.interp(zb, zg, I); DH = C/np.interp(zb, zg, Hg)
    return ms, (zb*DM**2*DH)**(1/3)
def bao_chi2(Hg, I, rd):      # rd None: the scale is profiled analytically like CFG681's q (K3 only)
    ms, mv = bao_pred(Hg, I); ds = [np.array([t[2], t[4]]) for t in DATA_A]; dv, sdv = DATA_B[1], DATA_B[2]
    if rd is None: s = (sum(m@Ci@d for m, d, Ci in zip(ms, ds, CINV)) + mv*dv/sdv**2)/(sum(m@Ci@m for m, Ci in zip(ms, CINV)) + mv*mv/sdv**2)
    else: s = 1/rd
    return sum((d - s*m)@Ci@(d - s*m) for m, d, Ci in zip(ms, ds, CINV)) + ((dv - s*mv)/sdv)**2
def sn_chi2(I):
    r = MB - 5*np.log10((1 + zhel)*np.interp(zhd, zg, I)); v = Cisn@r; b = one@v
    return r@v - b*b/A11
def prior(wb, wc, om, w0):
    c = ((wb - wb0)/sb)**2
    if cfg["wcfree"]:
        h2 = om + OMR + w0
        return 1e9 if h2 <= 0 else c + ((np.sqrt(h2) - cfg["hp"][0])/cfg["hp"][1])**2
    d = np.array([wb - wb0, wc - wc0]); rho = cfg["rho"]; Cp = np.array([[sb**2, rho*sb*sc], [rho*sb*sc, sc**2]])
    return float(d@np.linalg.solve(Cp, d))
def chi2_total(p, use_sn=True, const=False):
    wn = np.full(NN, p[0]) if const else np.asarray(p[:NN]); wb, wc = p[-2], p[-1]
    if np.any(wn < -2) or np.any(wn > 3) or not (0 < wb < 0.05) or not (0.05 <= wc <= 0.25): return 1e9
    b = bg(wn, wb, wc)
    if b is None: return 1e9
    om, Hg, I = b
    c = bao_chi2(Hg, I, rdrag(wb, wc)*cfg["rds"]) + prior(wb, wc, om, wn[0])
    return c + sn_chi2(I) if use_sn else c

# ---- fitting in standardised coordinates ----
def scales(const): return np.r_[[0.03]*(1 if const else NN), sb, (0.005 if cfg["wcfree"] else sc)]
def starts(const):
    tail = [wb0, 0.12 if cfg["wcfree"] else wc0]
    if const: return [[w] + tail for w in (0.25, 0.31, 0.38)]
    return [list(np.full(NN, w)) + tail for w in (0.25, 0.31, 0.38)] + [list(np.linspace(0.38, 0.25, NN)) + tail, list(np.linspace(0.25, 0.38, NN)) + tail]
def fit(use_sn, const, st):
    s_ = scales(const); best = None
    for s0 in st:
        p0 = np.asarray(s0, float); f = lambda x: chi2_total(p0 + x*s_, use_sn, const); n = len(p0); smp = np.vstack([np.zeros(n), np.eye(n)])
        r = minimize(f, np.zeros(n), method="Nelder-Mead", options=dict(initial_simplex=smp, maxiter=60000, maxfev=60000, xatol=1e-6, fatol=1e-8))
        r = minimize(f, r.x, method="Powell", options=dict(maxiter=60000, xtol=1e-6, ftol=1e-10))
        r = minimize(f, r.x, method="Nelder-Mead", options=dict(initial_simplex=r.x + 0.1*smp, maxiter=60000, maxfev=60000, xatol=1e-7, fatol=1e-9))
        p = p0 + r.x*s_; v = chi2_total(p, use_sn, const)
        if best is None or v < best[1]: best = (p, float(v))
    return best
def fit_pair(use_sn):
    fc = fit(use_sn, True, starts(True))
    ff = fit(use_sn, False, starts(False) + [list(np.full(NN, fc[0][0])) + list(fc[0][1:])])
    d = fc[1] - ff[1]; dof = NN - 1; p = float(CHI2.sf(max(d, 0), dof)); s = float(NORM.isf(p/2)) if p > 0 else 99.0
    cls = "EVOLVING DE REQUIRED" if s >= 3 else ("CONSISTENT WITH CONSTANT" if s < 2 else "HINT")
    return fc, ff, dict(chi2_const=fc[1], w_const=float(fc[0][0]), chi2_free=ff[1], nodes_free=ff[0][:NN].tolist(),
                        omega_b=float(ff[0][-2]), omega_c=float(ff[0][-1]), dchi2=float(d), dof=dof, p=p, sigma_equiv=s, P2_class=cls)

# ---- posterior: Metropolis-Hastings (criteria section 5) ----
def hess(f, x, h=0.1):
    n = len(x); H = np.zeros((n, n)); E = np.eye(n)*h
    for i in range(n):
        for j in range(i, n):
            H[i, j] = H[j, i] = (f(x + E[i] + E[j]) - f(x + E[i] - E[j]) - f(x - E[i] + E[j]) + f(x - E[i] - E[j]))/(4*h*h)
    return H
def mcmc(use_sn, pbest):
    s_ = scales(False); f = lambda x: chi2_total(pbest + x*s_, use_sn); n = len(pbest)
    H = hess(f, np.zeros(n))
    try: Cx = 2*np.linalg.inv(H); np.linalg.cholesky(Cx); hess_ok = True
    except np.linalg.LinAlgError: Cx = np.diag(2/np.maximum(np.abs(np.diag(H)), 1e-6)); hess_ok = False
    Lp = np.linalg.cholesky((2.38**2/n)*Cx); Ls = np.linalg.cholesky(Cx); chains, accs = [], []
    for seed in (6891, 6892, 6893, 6894):
        rng = np.random.default_rng(seed); x = Ls@rng.standard_normal(n); fx = f(x); k = 0
        while fx >= 1e8 and k < 60: x = 0.5*x; fx = f(x); k += 1
        ch = np.empty((NSTEP, n)); acc = 0
        for i in range(NSTEP):
            y = x + Lp@rng.standard_normal(n); fy = f(y)
            if fy < 1e8 and np.log(rng.random()) < -0.5*(fy - fx): x, fx = y, fy; acc += 1
            ch[i] = x
            if (i + 1) % 5000 == 0: guard()
        chains.append(pbest + ch[int(0.2*NSTEP):]*s_); accs.append(acc/NSTEP)
    return np.array(chains), accs, hess_ok
def rhat(ch):
    m, n = ch.shape; W = ch.var(axis=1, ddof=1).mean(); B = n*ch.mean(axis=1).var(ddof=1)
    return float(np.sqrt(((n - 1)/n*W + B/n)/W)) if W > 0 else float("inf")
def wvec(z): return np.array([np.interp(z, NODES, np.eye(NN)[i]) for i in range(NN)])
def derived(S):            # S (..., npar) physical samples -> dict of arrays
    wn = S[..., :NN]; om = S[..., -2] + S[..., -1]*(1 + cfg["f"]) + OMNU; w0 = wn[..., 0]; h2 = om + OMR + w0; d = {"H0": 100*np.sqrt(h2)}
    for z in ZS:
        wz = wn@wvec(z); X = np.where(w0 > 0, wz/np.where(w0 > 0, w0, 1.0), -1.0)
        d[f"sqrtX_{z}"] = np.sqrt(np.clip(X, 0, None)); d[f"E_{z}"] = np.sqrt((om*(1 + z)**3 + OMR*(1 + z)**4 + wz)/h2); d[f"w_{z}"] = wz
    for i, z in enumerate(NODES): d[f"a0_node_{z}"] = 0.5*CMS*np.sqrt(G*RHO100*np.clip(wn[..., i], 0, None))
    return d
Q = [2.5, 16, 50, 84, 97.5]
def sep(sq, E):
    qs, qe = np.percentile(sq, Q), np.percentile(E, Q)
    lx84, lx50 = np.log10(max(qs[3], 0.01)), np.log10(max(qs[2], 0.01))
    gap = np.log10(qe[1]) - lx84; sE = np.log10(qe[2]) - np.log10(qe[1]); sX = lx84 - lx50
    S = lambda e: float(gap/np.sqrt(e**2 + sE**2 + sX**2)) if gap > 0 else 0.0
    ok = [e for e in np.linspace(0.01, 1.0, 1000) if S(e) >= 3]
    return dict(sqrtX_q=qs.tolist(), E_q=qe.tolist(), width68=float(qs[3] - qs[1]), gap_dex=float(gap), sig_E=float(sE), sig_X=float(sX),
                e_3sigma=float(max(ok)) if ok else None, S_at={str(e): S(e) for e in (0.05, 0.10, 0.125, 0.16, 0.162, 0.20, 0.30, 0.40, 0.70)})
def analyse(use_sn, label):
    fc, ff, p2 = fit_pair(use_sn)
    P(f"\n=== {label}: constant w = {p2['w_const']:.4f} chi2 {p2['chi2_const']:.3f} | free chi2 {p2['chi2_free']:.3f} nodes {np.round(p2['nodes_free'], 4).tolist()}"
      f" omega_b {p2['omega_b']:.5f} omega_c {p2['omega_c']:.5f}\n  P2: dchi2 {p2['dchi2']:.2f}/{p2['dof']}  p {p2['p']:.3g}  ~{p2['sigma_equiv']:.2f} sigma -> {p2['P2_class']}")
    ch, accs, hok = mcmc(use_sn, ff[0]); S = ch.reshape(-1, ch.shape[-1]); D = derived(S); Dc = derived(ch)
    rh = {f"par{i}": rhat(ch[..., i]) for i in range(ch.shape[-1])}
    rh.update({k: rhat(Dc[k]) for k in Dc if k.startswith(("sqrtX_", "E_"))})
    k4 = bool(all(v < 1.02 for v in rh.values()) and all(0.1 <= a <= 0.5 for a in accs))
    p1 = {str(z): sep(D[f"sqrtX_{z}"], D[f"E_{z}"]) for z in ZS}
    nb = sum(p1[str(z)]["width68"] <= 0.5*CFG683_W[z] for z in (1.0, 1.5, 2.33))
    cls = "DEGENERACY BROKEN" if nb == 3 else ("PARTLY BROKEN" if nb >= 1 else "NOT BROKEN")
    grades = {}
    for nm, (z, e) in P3S.items():
        o = p1[str(z)]; Sv = o["gap_dex"]/np.sqrt(e**2 + o["sig_E"]**2 + o["sig_X"]**2) if o["gap_dex"] > 0 else 0.0
        grades[nm] = dict(z=z, e=e, S=float(Sv), grade="DECIDES" if Sv >= 3 else ("LEANS" if Sv >= 2 else "CANNOT"))
    p3 = dict(H0_q=np.percentile(D["H0"], Q).tolist(), a0_node_q={str(z): np.percentile(D[f"a0_node_{z}"], Q).tolist() for z in NODES},
              P_w_le0={str(z): float(np.mean(D[f"w_{z}"] <= 0)) for z in ZS})
    post = dict(node_mean=S[:, :NN].mean(0).tolist(), node_std=S[:, :NN].std(0).tolist(), omega_b=[float(S[:, -2].mean()), float(S[:, -2].std())],
                omega_c=[float(S[:, -1].mean()), float(S[:, -1].std())])
    for z in ZS:
        o = p1[str(z)]
        P(f"  z*={z}: tracking sqrtX 68% [{o['sqrtX_q'][1]:.3f}, {o['sqrtX_q'][3]:.3f}] (median {o['sqrtX_q'][2]:.3f}, width {o['width68']:.3f}"
          + (f" vs CFG683 {CFG683_W[z]:.3f}" if z in CFG683_W else "") + f")  rival E 68% [{o['E_q'][1]:.3f}, {o['E_q'][3]:.3f}]"
          f"  gap {o['gap_dex']:+.3f} dex  e_3sigma {o['e_3sigma']}")
    P(f"  P1: {cls} ({nb}/3 widths <= half CFG683)")
    for nm, g in grades.items(): P(f"    {nm}: e={g['e']} at z*={g['z']} -> S = {g['S']:.2f} -> {g['grade']}")
    P(f"  P3: native H0 68% [{p3['H0_q'][1]:.2f}, {p3['H0_q'][3]:.2f}] median {p3['H0_q'][2]:.2f}; a0(kappa=1/2) medians by node "
      + ", ".join(f"z{z}: {p3['a0_node_q'][str(z)][2]:.3e}" for z in NODES) + "  (kappa fitted; not a footing change)")
    P(f"  K4: {'PASS' if k4 else 'FAIL'}  acceptance {np.round(accs, 3).tolist()}  max R-hat {max(rh.values()):.4f}  hessian_ok {hok}")
    return dict(P2=p2, P1=p1, P1_class=cls, P1_n_narrow=int(nb), grades=grades, P3=p3, posterior=post, K4=dict(ok=k4, accept=accs, rhat=rh, hessian_ok=hok))

# ---- K3: ruler-free reproduction of CFG681 (primary only; Omega_r exactly CFG681's) ----
if MODE == "primary":
    OMR681 = 2.469e-5/0.68**2*(1 + 0.2271*3.046); H2 = 0.68**2
    def chi681(om, use_sn):
        if not 0.15 <= om <= 0.45: return 1e9
        Hg = 100*np.sqrt(om*H2*(1 + zg)**3 + OMR681*H2*(1 + zg)**4 + (1 - om - OMR681)*H2)
        I = np.r_[0, np.cumsum(0.5*(1/Hg[1:] + 1/Hg[:-1])*np.diff(zg))]*C
        return bao_chi2(Hg, I, None) + (sn_chi2(I) if use_sn else 0.0)
    r1 = minimize(lambda p: chi681(p[0], False), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
    r2 = minimize(lambda p: chi681(p[0], True), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
    checks["K3"] = dict(bao=[float(r1.fun), float(r1.x[0])], bao_sn=[float(r2.fun), float(r2.x[0])],
                        ok=bool(abs(r1.fun - 10.5515) <= 0.01 and abs(r1.x[0] - 0.2970) <= 0.001 and abs(r2.fun - 1400.143) <= 0.02 and abs(r2.x[0] - 0.3039) <= 0.001))
    P(f"K3: {'PASS' if checks['K3']['ok'] else 'FAIL'}  BAO chi2 {r1.fun:.4f} Om {r1.x[0]:.5f} (10.5515, 0.2970); BAO+SN chi2 {r2.fun:.3f} Om {r2.x[0]:.5f} (1400.143, 0.3039)")

# ---- MUTATE truths (M1, M2): noiseless predictions at the same errors ----
if MODE in ("M1", "M2"):
    wc_ = fit(True, True, starts(True))[0][0]
    wtrue = wc_*np.ones(NN) if MODE == "M1" else wc_*np.array([1, 1, 1, 0.5, 0, 0])
    om_, Hg_, I_ = bg(wtrue, wb0, wc0); ms_, mv_ = bao_pred(Hg_, I_)
    DATA_A = [(t[0], t[1], m[0]/R0, t[3], m[1]/R0, t[5], t[6]) for t, m in zip(ANISO, ms_)]; DATA_B = (BGS[0], mv_/R0, BGS[2])
    MB = 5*np.log10((1 + zhel)*np.interp(zhd, zg, I_))
    res["truth"] = dict(w_const_real=float(wc_), w_nodes=wtrue.tolist()); P(f"{MODE} truth: w nodes {np.round(wtrue, 4).tolist()} (A1 centres)")

# ---- run ----
prim = None
if MODE not in ("primary", "M3"):
    pj = os.path.join(HERE, "cfg689.json"); prim = json.load(open(pj)) if os.path.exists(pj) else None
if MODE == "M3":
    pj = os.path.join(HERE, "cfg689.json")
    if not os.path.exists(pj): P("M3 needs the primary's cfg689.json first"); sys.exit(2)
    prim = json.load(open(pj)); ff = fit_pair(True)[1]
    w233, w233p, sig = float(ff[0][NN - 1]), prim["BAO+SN"]["P2"]["nodes_free"][-1], prim["BAO+SN"]["posterior"]["node_std"][-1]
    bites = abs(w233 - w233p) >= sig
    res["M3"] = dict(w233_M3=w233, w233_primary=w233p, sigma_primary=sig, shift_sigma=abs(w233 - w233p)/sig, bites=bool(bites))
    P(f"M3 (r_d x 1.02): w(2.33) {w233:.4f} vs primary {w233p:.4f} (sigma {sig:.4f}) -> shift {abs(w233 - w233p)/sig:.2f} sigma -> {'BITES' if bites else 'FAILS (does not bite)'}")
else:
    res["BAO+SN"] = analyse(True, f"{MODE} BAO + Pantheon+ shape")
    if MODE == "primary": res["BAO"] = analyse(False, "primary BAO only")
    if MODE == "M1":
        a = res["BAO+SN"]; ok = a["P2"]["dchi2"] <= 0.1 and all(a["P1"][str(z)]["sqrtX_q"][1] <= 1 <= a["P1"][str(z)]["sqrtX_q"][3] for z in ZS)
        res["M1"] = dict(pass_=bool(ok)); P(f"M1: {'PASS' if ok else 'FAIL'} (dchi2 {a['P2']['dchi2']:.3f} <= 0.1; 68% tracking bands contain 1)")
    if MODE == "M2":
        a = res["BAO+SN"]; nodes = np.array(a["P2"]["nodes_free"]); sd = np.array(a["posterior"]["node_std"]); wt = np.array(res["truth"]["w_nodes"])
        ok_n = bool(np.all(np.abs(nodes - wt) <= np.maximum(sd, 0.03))); ok_d = a["P2"]["dchi2"] >= 9; ok_b = a["P1"]["2.33"]["sqrtX_q"][3] < 1
        res["M2"] = dict(nodes_ok=ok_n, dchi2_ok=bool(ok_d), band_ok=bool(ok_b), pass_=bool(ok_n and ok_d and ok_b))
        P(f"M2: {'PASS' if ok_n and ok_d and ok_b else 'FAIL'} (nodes within max(1 sigma, 0.03): {ok_n}; dchi2 {a['P2']['dchi2']:.2f} >= 9: {ok_d}; 68% upper at 2.33 {a['P1']['2.33']['sqrtX_q'][3]:.3f} < 1: {ok_b})")
    if MODE.startswith("B") and prim is not None:
        a, b = res["BAO+SN"], prim["BAO+SN"]
        res["flips"] = dict(P1=a["P1_class"] != b["P1_class"], P2=a["P2"]["P2_class"] != b["P2"]["P2_class"])
        P(f"{MODE} vs primary: P1 {a['P1_class']} vs {b['P1_class']}; P2 {a['P2']['P2_class']} vs {b['P2']['P2_class']} -> flips {res['flips']}")
res["checks"] = checks
if MODE == "primary":
    a = res["BAO+SN"]; e3 = "/".join(str(None if a["P1"][str(z)]["e_3sigma"] is None else round(a["P1"][str(z)]["e_3sigma"], 3)) for z in ZS)
    P(f"\nVERDICT (primary, before brackets/MUTATE): P1 {a['P1_class']} (e_3sigma at z* 1.0/1.2/1.5/2.33 = {e3}; record samples "
      + "; ".join(f"{k} {g['grade']}" for k, g in a["grades"].items()) + f"); P2 {a['P2']['P2_class']} (dchi2 {a['P2']['dchi2']:.2f}/{a['P2']['dof']}, "
      f"{a['P2']['sigma_equiv']:.2f} sigma); native H0 {a['P3']['H0_q'][2]:.2f} [{a['P3']['H0_q'][1]:.2f}, {a['P3']['H0_q'][3]:.2f}]; "
      + "; ".join(f"{k} {'PASS' if v['ok'] else 'FAIL'}" for k, v in checks.items()) + f"; K4 {'PASS' if a['K4']['ok'] else 'FAIL'}")
    P("kappa fitted; cold energy mass required; not theory closed; nothing here says the data favour the framework over LCDM.")
json.dump(res, open(os.path.join(HERE, f"cfg689{TAG}.json"), "w"), indent=1, default=float)
P(f"wrote cfg689{TAG}.json")
