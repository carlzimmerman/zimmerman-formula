"""CFG689 (criteria 1c237145d + addenda A1 0db6da294, A2 bb21587be): BAO with the framework's own ruler and no LCDM assumption in the chain.
CFG654's principle (pre-switch universe = framework physics; A1 pair omega_b 0.02236 / omega_c 0.1202) fixes r_d with CAMB, and
CFG253 (<= 3% of the cold mass made after recombination) fixes rho_m(z) = omega_m (1+z)^3. DESI DR2 D_H/r_d is then an absolute
H(z); the physical dark-energy density w(z) = rho_DE/rho_crit,100 is free per node (6 nodes, w(0) free) and, after A1, the
curvature omega_k is free too (no flatness assumption). No CMB distance except theta* (A2 modes only), no CPL, no LCDM late-time fit.
Modes (env CFG689_MODE): primary F M1 M2 M3 M1k M2k B1 B2 B3m B3p B4m B4p B5a B5b B5c B6 B7 B8 B9 B10 B12 T TF TD5F TU3F D5 U3 M4 P5 (A2: theta*, SN swaps, P6).
Outputs cfg689[_MODE].out/.json. Exit 75 = a PM / 1024^3 / chain process appeared: no verdict is written, the waiter re-gates and
reruns the mode. Implementation notes (not in the criteria, no verdict weight): B5/B9 free omega_c over 0.05-0.25, where a +-2 sigma
power law in omega_c cannot be trusted, so they interpolate a CAMB table in omega_c (21 points, cubic in log-log; K2b checks it at
three off-grid points); the free fit also starts from the constant-w best fit (it can only lower the free chi^2)."""
import json, os, sys, subprocess, numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as CHI2, norm as NORM
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__)); MODE = os.environ.get("CFG689_MODE", "primary")
NSTEP = int(os.environ.get("CFG689_NSTEP", "60000")); FROZEN_NSTEP = 60000
EXTD = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data")); EXT = os.path.join(EXTD, "pantheonplus_dr")
TAG = "" if MODE == "primary" else "_" + MODE
OUTF = open(os.path.join(HERE, f"cfg689{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
import re   # guard reads `ps` (no pattern in any argv, so other chains' pgrep gates never match this process); shell wrappers ignored
BUSY = re.compile(r"cfg[0-9]{3}_pm\.py|cfg59[6]_pm|run_6[0-9]{2}\.py|^\s*bash \S*chain[0-9]*\.sh|argon11_run\.py|cfg[0-9]{3}_native\.py|cfg9[0-9]{2}_rescore\.py")
WRAP = re.compile(r"^\s*(\S*/)?(ba|z)?sh -c ")
PARALLEL = os.environ.get("CFG689_PARALLEL", "") == "1"   # owner 2026-10-20: small runs may go beside a 1024^3 job, under a memory watchdog
SWAP0 = [None]
def mem_state():          # (free+inactive GB, swap used MB) from vm_stat / sysctl
    vs = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout; pg = int(re.search(r"page size of (\d+)", vs).group(1))
    fi = sum(int(re.search(k + r":\s+(\d+)", vs).group(1)) for k in ("Pages free", "Pages inactive"))*pg/1e9
    used = float(re.search(r"used = ([0-9.]+)M", subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout).group(1))
    return fi, used
def guard():
    if PARALLEL:          # exit long before a 1024^3 job's own swap guard (+5 GB) could trip: swap +1 GB over its minimum, or < 8 GB free
        fi, used = mem_state(); SWAP0[0] = used if SWAP0[0] is None else min(SWAP0[0], used)
        if used > SWAP0[0] + 1000 or fi < 8:
            P(f"GUARD (parallel): swap {used:.0f} MB (min {SWAP0[0]:.0f}) or free+inactive {fi:.1f} GB -> exit 75 (no verdict; mode {MODE} reruns later)"); sys.exit(75)
        return
    cmds = subprocess.run(["ps", "-axo", "command="], capture_output=True, text=True).stdout.splitlines()
    if any(BUSY.search(c) and not WRAP.match(c) for c in cmds):
        P(f"GUARD: a PM / 1024^3 / chain process is alive -> exit 75 (no verdict; mode {MODE} reruns later)"); sys.exit(75)
guard()
P(f"CFG689 mode={MODE}  NSTEP={NSTEP}" + ("" if NSTEP == FROZEN_NSTEP else f"  (NOT the frozen {FROZEN_NSTEP}: no verdict weight)"))

# ---- addendum A1 constants from DESI's own papers (P4, P5, K7, B12; read on the arXiv HTML pages 2026-10-20) ----
FID = dict(h=0.6736, wb=0.02237, wc=0.1200, mnu=0.06)       # DESI fiducial, arXiv 2503.14739 Table 1 (Planck 2018 LCDM)
FID_LYA = (8.6172, 39.1879)                                # DESI's fiducial D_H/r_d, D_M/r_d at z 2.33 (same table) -> K7
SPAN_ISO, SPAN_AP = (0.963, 1.075), (0.976, 1.029)         # grid offsets covered by c001-c004, arXiv 2404.03000 Table 10
SNL = 0.01                                                  # declared conservative nonlinear/recon shift scale (addendum A1.4)
DR1PRE = [("BGS", 0.295, 0.9646, 0.0258), ("LRG1", 0.510, 0.9760, 0.0171), ("LRG2", 0.706, 0.9505, 0.0191),   # 2404.03000 Table 15
          ("LRG3+ELG1", 0.930, 1.0027, 0.0114), ("ELG2", 1.317, 0.9882, 0.0176), ("QSO", 1.491, 0.9967, 0.0229)]  # z_eff: 2404.03002 Table 1
DR1SYS = 0.00245                                            # DR1 Table 13, xi(r) total systematic on alpha_iso
DR1POST = [("BGS", 0.295, 0.9829, 0.0185), ("LRG1", 0.510, 0.9792, 0.0113), ("LRG2", 0.706, 0.9661, 0.0117),   # 2404.03000 Table 15 POST-recon:
           ("LRG3+ELG1", 0.930, 0.9983, 0.0081), ("ELG2", 1.317, 0.9876, 0.0147), ("QSO", 1.491, 1.0015, 0.0256)]  # POST-HOC control B12c (not frozen)

# ---- P5: framework-native bound from committed same-seed PM pairs (addendum A1.4); reads JSONs only ----
if MODE == "P5":
    W = lambda *p: os.path.join(EXTD, *p)
    PAIRS = {"NC1x_vs_NCS0": (W("cfg654_work", "NC1x", "cfg654cmb_cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json"),
                              W("cfg654_work", "NCS0", "cfg654cmb_cfg650_na_S0_canonical_N1024_L100_ns1024_lean.json")),
             "T1x_vs_P0": (W("cfg650_work", "T1x", "cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json"),
                           W("cfg596_work", "P0", "cfg596_S0_canonical_N1024_L100_ns1024_lean.json")),
             "T2x_vs_P0": (W("cfg650_work", "T2x", "cfg650_m1m2m3_RES_alt_N1024_L100_ns1024_lean.json"),
                           W("cfg596_work", "P0", "cfg596_S0_canonical_N1024_L100_ns1024_lean.json"))}
    out, mx = {}, []
    for name, (fa, fb) in PAIRS.items():
        if not (os.path.exists(fa) and os.path.exists(fb)): out[name] = dict(used=False, why="missing file"); P(f"{name}: missing file"); continue
        a, b = json.load(open(fa)), json.load(open(fb)); k6 = {x: (a.get(x), b.get(x)) for x in ("seed", "L", "z_i", "np")}
        if any(u != v for u, v in k6.values()): out[name] = dict(used=False, why=f"K6 mismatch {k6}"); P(f"{name}: K6 FAIL {k6}"); continue
        rows = {}
        for zk in ("z1", "z0.5", "z0"):
            if zk not in a.get("snap", {}) or zk not in b.get("snap", {}): rows[zk] = "snapshot missing"; continue
            ka, kb = np.array(a["snap"][zk]["k"], float), np.array(b["snap"][zk]["k"], float)
            if len(ka) != len(kb) or np.max(np.abs(ka/kb - 1)) > 1e-6: rows[zk] = "k grids differ"; continue
            m = ka <= 0.33; Ps = np.array(b["snap"][zk]["P"], float)[m]
            rg = np.array(a["snap"][zk]["P_grav"], float)[m]/Ps - 1; rp = np.array(a["snap"][zk]["P"], float)[m]/Ps - 1
            s0g = np.array(b["snap"][zk].get("P_grav", b["snap"][zk]["P"]), float)[m]/Ps - 1
            v = float(np.nanmax(np.abs(np.r_[rg, rp]))); mx.append(v)
            rows[zk] = dict(k=ka[m].tolist(), r_grav=rg.tolist(), r_part=rp.tolist(), S0_grav_vs_part=s0g.tolist(), max_abs=v)
            P(f"{name} {zk}: k {np.round(ka[m], 3).tolist()}  P_grav/P_S0-1 {np.round(rg, 4).tolist()}  P/P_S0-1 {np.round(rp, 4).tolist()}")
        out[name] = dict(used=True, K6=k6, rows=rows)
    if mx:
        dA = max(mx)*SNL; cls = "NEGLIGIBLE" if dA <= 7e-4 else "NOT NEGLIGIBLE"
        P(f"P5: max|r| {max(mx):.4f} x s_NL {SNL} = {dA:.2e} vs 7e-4 -> {cls}  (box L 100 Mpc/h: k < 0.063 h/Mpc absent; linear in both runs)")
    else: dA, cls = None, "UNAVAILABLE"; P("P5: no usable pair -> UNAVAILABLE")
    json.dump(dict(mode=MODE, pairs=out, max_abs_r=max(mx) if mx else None, s_NL=SNL, dalpha_NL=dA, P5_class=cls), open(os.path.join(HERE, "cfg689_P5.json"), "w"), indent=1)
    P("wrote cfg689_P5.json"); sys.exit(0)

# ---- constants and data (DESI DR2 table verbatim from cfg681_bao.py) ----
C = 299792.458; G = 6.67430e-11; CMS = 2.99792458e8; RHO100 = 1.87847e-26; OMG = 2.4728e-5
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
ISO = [(0.295, 7.942, 0.075)]                                # (z, D_V/r_d, sigma): DR2 BGS
if MODE == "B10": ANISO = [t for t in ANISO if t[0] != "Lya"]
if MODE in ("B12", "B12c"): ANISO = [t for t in ANISO if t[0] == "Lya"]    # DR1 pre-recon D_V replaces the DR2 galaxy/QSO points (below)
zg = np.linspace(0, 2.5, 5001); ZS = (1.0, 1.2, 1.5, 2.33)
def cumchi(Hg): return np.r_[0, np.cumsum(0.5*(1/Hg[1:] + 1/Hg[:-1])*np.diff(zg))]*C       # line-of-sight comoving distance, Mpc
CFG683_W = {1.0: 0.853, 1.5: 1.596, 2.33: 2.183}                     # CFG683 CMB-free BAO+SN tracking band widths
P3S = {"KURVS-CDFS z~1.5 (gas unmeasured)": (1.5, 0.30), "z~1.2 multi-tracer (deep-MOND best case)": (1.2, 0.162),
       "RC100/CRISTAL optimistic": (2.33, 0.125), "RC100/CRISTAL realistic": (2.33, 0.40)}

# ---- mode configuration (base sections 3, 7, 9; addendum A1.1, A1.2) ----
cfg = dict(wb=0.02236, sb=0.00015, wc=0.1202, sc=0.0014, rho=0.0, mnu=0.0, f=0.0, hp=None, wcfree=False,
           nodes=np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33]), rds=1.0, freek=True, wmin=-2.0, snz="zHD", snzmin=0.01, theta=False, sn="PP")
if MODE in ("F", "M1", "M2", "M3"): cfg.update(freek=False)
elif MODE == "B1": cfg.update(wb=0.02193, sb=0.00022)
elif MODE == "B2": cfg.update(mnu=0.06)
elif MODE == "B3m": cfg.update(rho=-0.5)
elif MODE == "B3p": cfg.update(rho=0.5)
elif MODE == "B4m": cfg.update(f=-0.03)
elif MODE == "B4p": cfg.update(f=0.03)
elif MODE in ("B5a", "B5b", "B5c"): cfg.update(wb=0.02193, sb=0.00022, wcfree=True, hp=({"B5a": 0.680, "B5b": 0.700, "B5c": 0.7304}[MODE], 0.0104))
elif MODE == "B6": cfg.update(nodes=np.array([0, 0.7, 1.5, 2.33]))
elif MODE == "B7": cfg.update(snz="zCMB", snzmin=0.03)
elif MODE == "B8": cfg.update(sb=0.00030, sc=0.0028)
elif MODE == "B9": cfg.update(wb=0.02193, sb=0.00022, wcfree=True, hp=None, freek=False, wmin=0.0)
elif MODE == "T": cfg.update(theta=True)                                          # addendum A2.3
elif MODE == "TF": cfg.update(theta=True, freek=False)
elif MODE == "TD5F": cfg.update(theta=True, freek=False, sn="DES5")
elif MODE == "TU3F": cfg.update(theta=True, freek=False, sn="U3")
elif MODE == "D5": cfg.update(sn="DES5")
elif MODE == "U3": cfg.update(sn="U3")
elif MODE == "M4": cfg.update(theta=True, freek=False)
elif MODE not in ("primary", "M1k", "M2k", "B10", "B12", "B12c"): sys.exit(f"unknown CFG689_MODE {MODE}")
if MODE == "M3": cfg.update(rds=1.02)
NODES = cfg["nodes"]; NN = len(NODES); wb0, sb, wc0, sc = cfg["wb"], cfg["sb"], cfg["wc"], cfg["sc"]
OMNU = cfg["mnu"]/93.14; NREL = 3.044 if cfg["mnu"] == 0 else 3.044*2/3; OMR = OMG*(1 + 0.2271*NREL)
FREEK = cfg["freek"]; WMIN = cfg["wmin"]; TRUTH = "M1" if MODE == "M4" else (MODE[:2] if MODE in ("M1", "M2", "M1k", "M2k") else None)
TH_OBS, TH_SIG = 1.04109, 0.00030; TH_DATA = TH_OBS                 # 100 theta_*, Planck 2018 TT,TE,EE+lowE (cfg654_ics.py PROVENANCE)

# ---- the ruler: CAMB in the pre-switch era (cfg654_ics.camb_results settings) ----
def camb_rdrag(wb, wc, mnu=0.0, h=0.6777):
    import camb
    p = camb.CAMBparams()
    p.set_cosmology(H0=100*h, ombh2=wb, omch2=wc, omk=0.0, mnu=mnu, num_massive_neutrinos=(1 if mnu > 0 else 0), nnu=3.044,
                    TCMB=2.7255, tau=0.0544)
    p.set_dark_energy(w=-1.0, wa=0.0); p.set_accuracy(AccuracyBoost=1.5, lAccuracyBoost=1.0); p.WantCls = False
    return float(camb.get_background(p).get_derived_params()["rdrag"])
def fid_bg():              # DESI's fiducial (flat LCDM, one massive neutrino counted in matter): H grid, D_M grid, r_d
    omf = FID["wb"] + FID["wc"] + FID["mnu"]/93.14; omrf = OMG*(1 + 0.2271*3.044*2/3)
    Hf = 100*np.sqrt(omf*(1 + zg)**3 + omrf*(1 + zg)**4 + (FID["h"]**2 - omf - omrf)); return Hf, cumchi(Hf), camb_rdrag(FID["wb"], FID["wc"], FID["mnu"], FID["h"])
res = {"mode": MODE, "nstep": NSTEP, "cfg": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in cfg.items()}}
if MODE in ("primary", "B12", "B12c"):
    HF, DMF, RDF = fid_bg()
    def dvf(z): dm, dh = np.interp(z, zg, DMF), C/np.interp(z, zg, HF); return (z*dm**2*dh)**(1/3)/RDF
if MODE in ("B12", "B12c"):   # B12c (POST HOC): same conversion with DR1 POST-recon alpha_iso, to separate reconstruction from DR1-vs-DR2 data
    ISO = [(z, a*dvf(z), np.hypot(s, DR1SYS)*dvf(z)) for (_, z, a, s) in (DR1PRE if MODE == "B12" else DR1POST)]
    res["B12_data"] = [dict(name=n, z=z, alpha_iso=a, sig=s, DV_rd=d[1], sig_DV=d[2]) for (n, z, a, s), d in zip(DR1PRE if MODE == "B12" else DR1POST, ISO)]
CINV = [np.linalg.inv(np.array([[s1**2, r*s1*s2], [r*s1*s2, s2**2]])) for (_, _, _, s1, _, s2, r) in ANISO]
R0 = camb_rdrag(wb0, wc0, cfg["mnu"])
BEXP = -np.log(camb_rdrag(wb0 + 2*sb, wc0, cfg["mnu"])/camb_rdrag(wb0 - 2*sb, wc0, cfg["mnu"]))/np.log((wb0 + 2*sb)/(wb0 - 2*sb))
if not cfg["wcfree"]:
    CEXP = -np.log(camb_rdrag(wb0, wc0 + 2*sc, cfg["mnu"])/camb_rdrag(wb0, wc0 - 2*sc, cfg["mnu"]))/np.log((wc0 + 2*sc)/(wc0 - 2*sc))
    def rdrag(wb, wc): return R0*(wb/wb0)**(-BEXP)*(wc/wc0)**(-CEXP)
else:
    CEXP = None; WCG = np.linspace(0.05, 0.25, 21); SPL = CubicSpline(np.log(WCG), np.log([camb_rdrag(wb0, x, cfg["mnu"]) for x in WCG]))
    def rdrag(wb, wc): return float(np.exp(SPL(np.log(wc))))*(wb/wb0)**(-BEXP)
res["ruler"] = dict(r_d0=R0, b=BEXP, c=CEXP)
P(f"ruler: r_d0 = {R0:.4f} Mpc at omega_b {wb0} omega_c {wc0} mnu {cfg['mnu']}; exponents b {BEXP:.5f} c {CEXP}; curvature free: {FREEK}")
checks = {}
if MODE == "primary":
    k1 = dict(A1=camb_rdrag(0.02236, 0.1202), BBN=camb_rdrag(0.02193, 0.1202), BBN_mnu=camb_rdrag(0.02193, 0.1202, 0.06))
    tgt = dict(A1=147.0667, BBN=147.5453, BBN_mnu=147.5381)
    checks["K1"] = dict(values=k1, targets=tgt, ok=bool(all(abs(k1[k] - tgt[k]) <= 0.02 for k in tgt)))
    dev = [abs(rdrag(wb0 + i*2*sb, wc0 + j*2*sc)/camb_rdrag(wb0 + i*2*sb, wc0 + j*2*sc) - 1) for i in (-1, 1) for j in (-1, 1)]
    dh = [abs(camb_rdrag(wb0, wc0, 0.0, h)/R0 - 1) for h in (0.6277, 0.7277)]
    checks["K2"] = dict(corner_dev=dev, h_dev=dh, ok=bool(max(dev) <= 2e-4 and max(dh) < 1e-4))
    k7 = (C/np.interp(2.33, zg, HF)/RDF, np.interp(2.33, zg, DMF)/RDF)
    checks["K7"] = dict(values=k7, targets=FID_LYA, r_d_fid=RDF, ok=bool(abs(k7[0]/FID_LYA[0] - 1) <= 1e-3 and abs(k7[1]/FID_LYA[1] - 1) <= 1e-3))
if cfg["wcfree"]:
    dev = [abs(rdrag(wb0, x)/camb_rdrag(wb0, x, cfg["mnu"]) - 1) for x in (0.087, 0.143, 0.211)]
    checks["K2b"] = dict(dev=dev, ok=bool(max(dev) <= 2e-4))
for k, v in checks.items(): P(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v}")

# ---- supernovae: Pantheon+ (as CFG681; B7 uses zCMB > 0.03, no peculiar-velocity model), or DES-SN5YR / Union3 (A2, CFG684 loaders) ----
EXT684 = os.path.join(EXTD, "cfg684_inputs")
if cfg["sn"] == "PP":
    raw = np.genfromtxt(os.path.join(EXT, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
    covfull = np.loadtxt(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1); NSN = int(round(np.sqrt(covfull.size))); covfull = covfull.reshape(NSN, NSN)
    sel = (raw["IS_CALIBRATOR"] == 0) & (raw[cfg["snz"]] > cfg["snzmin"])
    zsn, zhel, MB = raw[cfg["snz"]][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float); Wsn = np.linalg.inv(covfull[np.ix_(sel, sel)])
    del covfull; SNLAB = f"Pantheon+ non-calibrators, {cfg['snz']} > {cfg['snzmin']}"
elif cfg["sn"] == "DES5":     # SNANA format: SN: CID IDSURVEY zHD zHEL MU ...; STAT+SYS.npz = upper triangle of the inverse covariance
    rows = [l.split() for l in open(os.path.join(EXT684, "des5", "DES-Dovekie_HD.csv")) if l.startswith("SN:")]
    dz = np.array([float(r[3]) for r in rows]); dzh = np.array([float(r[4]) for r in rows]); dmu = np.array([float(r[5]) for r in rows])
    npz = np.load(os.path.join(EXT684, "des5", "STAT+SYS.npz")); n_ = int(npz[npz.files[0]][0]); Wd = np.zeros((n_, n_)); Wd[np.triu_indices(n_)] = npz[npz.files[1]]
    Wd = Wd + np.triu(Wd, 1).T; ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]
    zsn, zhel, MB, Wsn = dz[ww], dzh[ww], dmu[ww], np.linalg.inv(Cd); SNLAB = "DES-SN5YR Dovekie (CFG684 loader)"
else:                         # Union3: spline-node mu with weight matrix
    from astropy.io import fits
    M_ = fits.open(os.path.join(EXT684, "union3", "mu_mat_union3_cosmo=2_mu.fits"))[0].data
    zsn, MB, Wsn = M_[0, 1:], M_[1:, 0], M_[1:, 1:]; zhel = zsn; SNLAB = "Union3 nodes (CFG684 loader)"
one = np.ones(len(MB)); A11 = one@Wsn@one
DATA_A, DATA_I = list(ANISO), list(ISO)
P(f"SN: {len(MB)} {SNLAB}; BAO anisotropic {[t[0] for t in ANISO]} + isotropic D_V at z {[round(t[0], 3) for t in ISO]}; theta*: {cfg['theta']}")

# ---- theta* (A2.1): r_s(z*) from CAMB (power-law emulator, as r_d), z* fixed at the mode's centres, chi integrated to z* ----
def camb_star(wb, wc):
    import camb
    p = camb.CAMBparams()
    p.set_cosmology(H0=67.77, ombh2=wb, omch2=wc, omk=0.0, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, tau=0.0544)
    p.set_dark_energy(w=-1.0, wa=0.0); p.set_accuracy(AccuracyBoost=1.5, lAccuracyBoost=1.0); p.WantCls = False
    d = camb.get_background(p).get_derived_params(); return float(d["rstar"]), float(d["zstar"])
if cfg["theta"]:
    RS0, ZSTAR = camb_star(wb0, wc0)
    BS = -np.log(camb_star(wb0 + 2*sb, wc0)[0]/camb_star(wb0 - 2*sb, wc0)[0])/np.log((wb0 + 2*sb)/(wb0 - 2*sb))
    CS = -np.log(camb_star(wb0, wc0 + 2*sc)[0]/camb_star(wb0, wc0 - 2*sc)[0])/np.log((wc0 + 2*sc)/(wc0 - 2*sc))
    def rstar(wb, wc): return RS0*(wb/wb0)**(-BS)*(wc/wc0)**(-CS)
    UG = np.linspace(np.log(3.5), np.log(1 + ZSTAR), 4001); ZH = np.exp(UG) - 1; HU = UG[1] - UG[0]
    res["theta_ruler"] = dict(r_s_star=RS0, z_star=ZSTAR, b=BS, c=CS)
    P(f"theta*: r_s(z*) {RS0:.4f} Mpc at z* {ZSTAR:.3f}; exponents {BS:.5f} {CS:.5f}")
    if MODE == "T":
        cor = [(camb_star(wb0 + i*2*sb, wc0 + j*2*sc), rstar(wb0 + i*2*sb, wc0 + j*2*sc)) for i in (-1, 1) for j in (-1, 1)]
        dv9 = [abs(e/c_[0] - 1) for c_, e in cor]; zs9 = [c_[1] for c_, _ in cor]
        checks["K9"] = dict(dev=dv9, z_star=zs9, ok=bool(max(dv9) <= 2e-4 and max(zs9) - min(zs9) < 1)); P(f"K9: {'PASS' if checks['K9']['ok'] else 'FAIL'}  {checks['K9']}")
def theta_model(om, wk, w_last, chi25, wb, wc):
    E2 = om*(1 + ZH)**3 + OMR*(1 + ZH)**4 + wk*(1 + ZH)**2 + w_last
    if np.any(E2 <= 0): return None
    f = C*(1 + ZH)/(100*np.sqrt(E2)); chi_hi = HU/3*(f[0] + f[-1] + 4*f[1:-1:2].sum() + 2*f[2:-1:2].sum())
    return float(100*rstar(wb, wc)/dm_from_chi(np.array([chi25 + chi_hi]), wk)[0])

# ---- model (A1.1: curvature) ----
def dm_from_chi(chi, wk):
    if wk == 0: return chi
    s = 100*np.sqrt(abs(wk))/C
    return np.sinh(s*chi)/s if wk > 0 else np.sin(s*chi)/s
def bg(wn, wb, wc, wk=0.0):
    om = wb + wc*(1 + cfg["f"]) + OMNU
    E2 = om*(1 + zg)**3 + OMR*(1 + zg)**4 + wk*(1 + zg)**2 + np.interp(zg, NODES, wn)
    if np.any(E2 <= 1e-8): return None
    Hg = 100*np.sqrt(E2); chi = cumchi(Hg); return om, Hg, dm_from_chi(chi, wk), chi
def bao_pred(Hg, DM):
    ms = [np.array([np.interp(t[1], zg, DM), C/np.interp(t[1], zg, Hg)]) for t in ANISO]
    mv = [(t[0]*np.interp(t[0], zg, DM)**2*C/np.interp(t[0], zg, Hg))**(1/3) for t in ISO]
    return ms, mv
def bao_chi2(Hg, DM, rd):      # rd None: the scale is profiled analytically like CFG681's q (K3 only)
    ms, mv = bao_pred(Hg, DM); ds = [np.array([t[2], t[4]]) for t in DATA_A]
    if rd is None:
        s = (sum(m@Ci@d for m, d, Ci in zip(ms, ds, CINV)) + sum(v*t[1]/t[2]**2 for v, t in zip(mv, DATA_I)))/(
             sum(m@Ci@m for m, Ci in zip(ms, CINV)) + sum(v*v/t[2]**2 for v, t in zip(mv, DATA_I)))
    else: s = 1/rd
    return sum((d - s*m)@Ci@(d - s*m) for m, d, Ci in zip(ms, ds, CINV)) + sum(((t[1] - s*v)/t[2])**2 for v, t in zip(mv, DATA_I))
def sn_chi2(DM):
    r = MB - 5*np.log10((1 + zhel)*np.interp(zsn, zg, DM)); v = Wsn@r; b = one@v
    return r@v - b*b/A11
def prior(wb, wc, om, w0, wk):
    c = ((wb - wb0)/sb)**2
    if cfg["wcfree"]:
        if cfg["hp"] is None: return c
        h2 = om + OMR + wk + w0
        return 1e9 if h2 <= 0 else c + ((np.sqrt(h2) - cfg["hp"][0])/cfg["hp"][1])**2
    d = np.array([wb - wb0, wc - wc0]); rho = cfg["rho"]; Cp = np.array([[sb**2, rho*sb*sc], [rho*sb*sc, sc**2]])
    return float(d@np.linalg.solve(Cp, d))
def split(p, const=False):
    nw = 1 if const else NN; wn = np.full(NN, p[0]) if const else np.asarray(p[:NN])
    return wn, (p[nw] if FREEK else 0.0), p[-2], p[-1]
NEVAL = [0]
def chi2_total(p, use_sn=True, const=False):
    NEVAL[0] += 1
    if NEVAL[0] % 2000 == 0: guard()                     # also guards the fitting stages (every ~2000 evaluations)
    wn, wk, wb, wc = split(p, const)
    if np.any(wn < WMIN) or np.any(wn > 3) or abs(wk) > 0.25 or not (0 < wb < 0.05) or not (0.05 <= wc <= 0.25): return 1e9
    b = bg(wn, wb, wc, wk)
    if b is None: return 1e9
    om, Hg, DM, chi = b
    c = bao_chi2(Hg, DM, rdrag(wb, wc)*cfg["rds"]) + prior(wb, wc, om, wn[0], wk)
    if cfg["theta"]:
        th = theta_model(om, wk, wn[-1], chi[-1], wb, wc)
        if th is None: return 1e9
        c += ((th - TH_DATA)/TH_SIG)**2
    return c + sn_chi2(DM) if use_sn else c

# ---- fitting in standardised coordinates ----
def scales(const): return np.r_[[0.03]*(1 if const else NN), ([0.01] if FREEK else []), sb, (0.005 if cfg["wcfree"] else sc)]
def starts(const):
    w3 = (0.25, 0.31, 0.38); tail = ([0.0] if FREEK else []) + [wb0, 0.12 if cfg["wcfree"] else wc0]
    if const: return [[w] + tail for w in w3]
    return [list(np.full(NN, w)) + tail for w in w3] + [list(np.linspace(0.38, 0.25, NN)) + tail, list(np.linspace(0.25, 0.38, NN)) + tail]
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
    wn, wk, wb, wc = split(ff[0])
    return fc, ff, dict(chi2_const=fc[1], w_const=float(fc[0][0]), chi2_free=ff[1], nodes_free=wn.tolist(), omega_k=float(wk),
                        omega_b=float(wb), omega_c=float(wc), pbest=ff[0].tolist(), dchi2=float(d), dof=dof, p=p, sigma_equiv=s, P2_class=cls)

# ---- posterior: Metropolis-Hastings (base section 5) ----
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
    wn = S[..., :NN]; wk = S[..., NN] if FREEK else 0.0; om = S[..., -2] + S[..., -1]*(1 + cfg["f"]) + OMNU; w0 = wn[..., 0]
    h2 = om + OMR + wk + w0; d = {"H0": 100*np.sqrt(h2), "omega_m": om + 0*w0, "Omega_k": wk/h2}
    for z in ZS:
        wz = wn@wvec(z); X = np.where(w0 > 0, wz/np.where(w0 > 0, w0, 1.0), -1.0)
        d[f"sqrtX_{z}"] = np.sqrt(np.clip(X, 0, None)); d[f"E_{z}"] = np.sqrt((om*(1 + z)**3 + OMR*(1 + z)**4 + wk*(1 + z)**2 + wz)/h2); d[f"w_{z}"] = wz
    for i, z in enumerate(NODES): d[f"a0_node_{z}"] = 0.5*CMS*np.sqrt(G*RHO100*np.clip(wn[..., i], 0, None))
    for z in Z6:          # A2.4: z > 2.33 assumes w = w(2.33) beyond the last BAO node (extrapolation, flagged)
        wz = wn@wvec(z); d[f"sqrtX6_{z}"] = np.sqrt(np.clip(np.where(w0 > 0, wz/np.where(w0 > 0, w0, 1.0), -1.0), 0, None))
    return d
Q = [2.5, 16, 50, 84, 97.5]
Z6 = (2.0, 2.5, 3.25)     # A2.4: LCDM's own emergent-scale ratios from the record (prep_2026/a0z_crossscale, 9d40e9c15c) - the alternative, not a yardstick
LAWS = {"DM14": {2.0: 1.756, 2.5: 2.126, 3.25: 2.823}, "D08": {2.0: 2.284, 2.5: 2.802, 3.25: 3.667}, "MAG": {2.0: 2.748, 2.5: 3.166, 3.25: 3.785}}
def p6_block(D):
    out, k20 = {}, np.sqrt(2*np.log(20))
    for z in Z6:
        q = np.percentile(D[f"sqrtX6_{z}"], Q); l84, l50 = np.log10(max(q[3], 0.01)), np.log10(max(q[2], 0.01)); sF = l84 - l50
        row = dict(sqrtX_q=q.tolist(), extrapolated=bool(z > 2.33))
        for law, vals in LAWS.items():
            L = np.log10(vals[z]); dc, dm = L - l84, L - l50
            row[law] = dict(ratio=vals[z], d_close=float(dc), d_med=float(dm), e20_close=float(dc/k20) if dc > 0 else None, e20_med=float(dm/k20) if dm > 0 else None)
        if z == 3.25:
            x, sx, LD = 0.06, 0.22, np.log10(LAWS["DM14"][3.25])
            row["BigWheel_log10B_tracking_over_DM14"] = float(((x - LD)**2 - (x - l50)**2)/(2*np.log(10)*(sx**2 + sF**2)))
        out[str(z)] = row
    e = out["2.5"]["DM14"]["e20_close"]
    out["P6_class"] = "NO SEPARATION" if e is None else ("TARGET HOLDS" if e >= 0.13 else ("TARGET TIGHTER" if e >= 0.10 else "TARGET HARDER"))
    return out
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
      f" omega_k {p2['omega_k']:+.4f} omega_b {p2['omega_b']:.5f} omega_c {p2['omega_c']:.5f}\n  P2: dchi2 {p2['dchi2']:.2f}/{p2['dof']}  p {p2['p']:.3g}  ~{p2['sigma_equiv']:.2f} sigma -> {p2['P2_class']}")
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
    p3 = dict(H0_q=np.percentile(D["H0"], Q).tolist(), omega_m_q=np.percentile(D["omega_m"], Q).tolist(),
              a0_node_q={str(z): np.percentile(D[f"a0_node_{z}"], Q).tolist() for z in NODES}, P_w_le0={str(z): float(np.mean(D[f"w_{z}"] <= 0)) for z in ZS})
    p0 = None
    if FREEK:
        qk = np.percentile(D["Omega_k"], Q); sk = 0.5*(qk[3] - qk[1]); zk = abs(qk[2])/sk if sk > 0 else 99.0
        p0 = dict(Omega_k_q=qk.tolist(), sigma=float(sk), z=float(zk), P0_class="CURVATURE REQUIRED" if zk >= 3 else ("FLAT CONSISTENT" if zk < 2 else "HINT"))
    post = dict(node_mean=S[:, :NN].mean(0).tolist(), node_std=S[:, :NN].std(0).tolist(), omega_b=[float(S[:, -2].mean()), float(S[:, -2].std())],
                omega_c=[float(S[:, -1].mean()), float(S[:, -1].std())], omega_k=([float(S[:, NN].mean()), float(S[:, NN].std())] if FREEK else None))
    for z in ZS:
        o = p1[str(z)]
        P(f"  z*={z}: tracking sqrtX 68% [{o['sqrtX_q'][1]:.3f}, {o['sqrtX_q'][3]:.3f}] (median {o['sqrtX_q'][2]:.3f}, width {o['width68']:.3f}"
          + (f" vs CFG683 {CFG683_W[z]:.3f}" if z in CFG683_W else "") + f")  rival E 68% [{o['E_q'][1]:.3f}, {o['E_q'][3]:.3f}]"
          f"  gap {o['gap_dex']:+.3f} dex  e_3sigma {o['e_3sigma']}")
    P(f"  P1: {cls} ({nb}/3 widths <= half CFG683)")
    for nm, g in grades.items(): P(f"    {nm}: e={g['e']} at z*={g['z']} -> S = {g['S']:.2f} -> {g['grade']}")
    if p0: P(f"  P0: Omega_k median {p0['Omega_k_q'][2]:+.4f} 68% [{p0['Omega_k_q'][1]:+.4f}, {p0['Omega_k_q'][3]:+.4f}] ({p0['z']:.2f} sigma) -> {p0['P0_class']}")
    P(f"  P3: native H0 68% [{p3['H0_q'][1]:.2f}, {p3['H0_q'][3]:.2f}] median {p3['H0_q'][2]:.2f}; omega_m 95% [{p3['omega_m_q'][0]:.4f}, {p3['omega_m_q'][4]:.4f}];"
      " a0(kappa=1/2) medians by node " + ", ".join(f"z{z}: {p3['a0_node_q'][str(z)][2]:.3e}" for z in NODES) + "  (kappa fitted; not a footing change)")
    P(f"  K4: {'PASS' if k4 else 'FAIL'}  acceptance {np.round(accs, 3).tolist()}  max R-hat {max(rh.values()):.4f}  hessian_ok {hok}")
    p6 = p6_block(D)
    for z in Z6:
        r6 = p6[str(z)]
        P(f"  P6 z={z}{' (EXTRAPOLATED beyond the last BAO node)' if r6['extrapolated'] else ''}: tracking sqrtX 68% [{r6['sqrtX_q'][1]:.3f}, {r6['sqrtX_q'][3]:.3f}]; "
          + "; ".join(f"{law} x{r6[law]['ratio']}: gap {r6[law]['d_close']:+.3f} dex (median {r6[law]['d_med']:+.3f}), e_20 {r6[law]['e20_close']}" for law in LAWS)
          + (f"; Big Wheel log10 B (tracking/DM14) {r6['BigWheel_log10B_tracking_over_DM14']:+.2f} [reported only]" if z == 3.25 else ""))
    P(f"  P6: {p6['P6_class']} (z 2.5, DM14, closest edges) - names the decisive measurement; not a result")
    return dict(P2=p2, P1=p1, P1_class=cls, P1_n_narrow=int(nb), grades=grades, P0=p0, P3=p3, P6=p6, posterior=post, K4=dict(ok=k4, accept=accs, rhat=rh, hessian_ok=hok))

# ---- K3 (ruler-free reproduction of CFG681; Omega_r exactly CFG681's) and K5 (curvature distance check): primary only ----
if MODE == "primary":
    OMR681 = 2.469e-5/0.68**2*(1 + 0.2271*3.046); H2 = 0.68**2
    def chi681(om, use_sn):
        if not 0.15 <= om <= 0.45: return 1e9
        Hg = 100*np.sqrt(om*H2*(1 + zg)**3 + OMR681*H2*(1 + zg)**4 + (1 - om - OMR681)*H2)
        I = cumchi(Hg); return bao_chi2(Hg, I, None) + (sn_chi2(I) if use_sn else 0.0)
    r1 = minimize(lambda p: chi681(p[0], False), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
    r2 = minimize(lambda p: chi681(p[0], True), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
    checks["K3"] = dict(bao=[float(r1.fun), float(r1.x[0])], bao_sn=[float(r2.fun), float(r2.x[0])],
                        ok=bool(abs(r1.fun - 10.5515) <= 0.01 and abs(r1.x[0] - 0.2970) <= 0.001 and abs(r2.fun - 1400.143) <= 0.02 and abs(r2.x[0] - 0.3039) <= 0.001))
    P(f"K3: {'PASS' if checks['K3']['ok'] else 'FAIL'}  BAO chi2 {r1.fun:.4f} Om {r1.x[0]:.5f} (10.5515, 0.2970); BAO+SN chi2 {r2.fun:.3f} Om {r2.x[0]:.5f} (1400.143, 0.3039)")
    from scipy.integrate import quad
    k5 = []
    for wk_ in (0.05, -0.05):
        om_, Hg_, DM_, _ = bg(np.full(NN, 0.31), 0.02236, 0.1202, wk_)
        for z in (0.5, 2.33):
            chq = C*quad(lambda x: 1/(100*np.sqrt(om_*(1 + x)**3 + OMR*(1 + x)**4 + wk_*(1 + x)**2 + 0.31)), 0, z, epsabs=0, epsrel=1e-12)[0]
            k5.append(abs(np.interp(z, zg, DM_)/dm_from_chi(np.array([chq]), wk_)[0] - 1))
    checks["K5"] = dict(dev=k5, ok=bool(max(k5) <= 1e-6)); P(f"K5: {'PASS' if checks['K5']['ok'] else 'FAIL'}  max dev {max(k5):.2e}")

# ---- MUTATE truths (M1, M2, M1k, M2k): noiseless flat predictions at the same errors ----
if TRUTH:
    fk_ = FREEK; FREEK = False; wc_ = fit(True, True, starts(True))[0][0]; FREEK = fk_     # the flat primary's constant fit (real data)
    wtrue = wc_*np.ones(NN) if TRUTH == "M1" else wc_*np.array([1, 1, 1, 0.5, 0, 0])
    om_, Hg_, DM_, CHI_ = bg(wtrue, wb0, wc0, 0.0); ms_, mv_ = bao_pred(Hg_, DM_)
    DATA_A = [(t[0], t[1], m[0]/R0, t[3], m[1]/R0, t[5], t[6]) for t, m in zip(ANISO, ms_)]; DATA_I = [(t[0], v/R0, t[2]) for t, v in zip(ISO, mv_)]
    MB = 5*np.log10((1 + zhel)*np.interp(zsn, zg, DM_))
    if cfg["theta"]: TH_DATA = theta_model(om_, 0.0, wtrue[-1], CHI_[-1], wb0, wc0)          # M4: theta* datum from the same truth
    res["truth"] = dict(w_const_real=float(wc_), w_nodes=wtrue.tolist(), omega_k=0.0, theta_100=(TH_DATA if cfg["theta"] else None))
    P(f"{MODE} truth: w nodes {np.round(wtrue, 4).tolist()}, flat, A1 centres" + (f", 100 theta* {TH_DATA:.6f}" if cfg["theta"] else ""))
if MODE == "T":   # K8 (A2.1): the long integral reproduces CFG654 A1's theta*-solved h = 0.67770 at the A1 pair
    wk8 = 0.6777**2 - (0.02236 + 0.1202) - OMR; om8, _, _, chi8 = bg(np.full(NN, wk8), 0.02236, 0.1202, 0.0)
    th8 = theta_model(om8, 0.0, wk8, chi8[-1], 0.02236, 0.1202)
    checks["K8"] = dict(theta_100=th8, target=1.04109, ok=bool(abs(th8 - 1.04109) <= 5e-5)); P(f"K8: {'PASS' if checks['K8']['ok'] else 'FAIL'}  100 theta* {th8:.6f} vs 1.04109")

# ---- run ----
def load(name):
    pj = os.path.join(HERE, name); return json.load(open(pj)) if os.path.exists(pj) else None
if MODE == "M3":
    prim = load("cfg689_F.json")
    if prim is None: P("M3 needs the flat bracket's cfg689_F.json first"); sys.exit(2)
    ff = fit_pair(True)[1]
    w233, w233p, sig = float(ff[0][NN - 1]), prim["BAO+SN"]["P2"]["nodes_free"][-1], prim["BAO+SN"]["posterior"]["node_std"][-1]
    bites = abs(w233 - w233p) >= sig
    res["M3"] = dict(w233_M3=w233, w233_F=w233p, sigma_F=sig, shift_sigma=abs(w233 - w233p)/sig, bites=bool(bites))
    P(f"M3 (r_d x 1.02, flat): w(2.33) {w233:.4f} vs F {w233p:.4f} (sigma {sig:.4f}) -> shift {abs(w233 - w233p)/sig:.2f} sigma -> {'BITES' if bites else 'FAILS (does not bite)'}")
else:
    res["BAO+SN"] = analyse(True, f"{MODE} BAO + Pantheon+ shape")
    if MODE in ("primary", "F"): res["BAO"] = analyse(False, f"{MODE} BAO only")
    a = res["BAO+SN"]
    if MODE == "M4":       # A2.5: P2 dchi2 <= 0.1 and 100 theta* recovered to <= 1e-5 at the best fit
        wn4, wk4, wb4, wc4 = split(np.array(a["P2"]["pbest"])); om4, _, _, chi4 = bg(wn4, wb4, wc4, wk4); th4 = theta_model(om4, wk4, wn4[-1], chi4[-1], wb4, wc4)
        ok = a["P2"]["dchi2"] <= 0.1 and abs(th4 - TH_DATA) <= 1e-5
        res["M4"] = dict(pass_=bool(ok), theta_best=th4, theta_truth=TH_DATA); P(f"M4: {'PASS' if ok else 'FAIL'} (dchi2 {a['P2']['dchi2']:.3f} <= 0.1; 100 theta* {th4:.6f} vs truth {TH_DATA:.6f})")
    elif TRUTH == "M1":
        ok = a["P2"]["dchi2"] <= 0.1 and all(a["P1"][str(z)]["sqrtX_q"][1] <= 1 <= a["P1"][str(z)]["sqrtX_q"][3] for z in ZS)
        res[MODE] = dict(pass_=bool(ok), frozen_rule=(MODE == "M1")); P(f"{MODE}: {'PASS' if ok else 'FAIL'} (dchi2 {a['P2']['dchi2']:.3f} <= 0.1; 68% tracking bands contain 1)" + ("" if MODE == "M1" else "  [reported only]"))
    if TRUTH == "M2":
        nodes = np.array(a["P2"]["nodes_free"]); sd = np.array(a["posterior"]["node_std"]); wt = np.array(res["truth"]["w_nodes"])
        ok_n = bool(np.all(np.abs(nodes - wt) <= np.maximum(sd, 0.03))); ok_d = a["P2"]["dchi2"] >= 9; ok_b = a["P1"]["2.33"]["sqrtX_q"][3] < 1
        res[MODE] = dict(nodes_ok=ok_n, dchi2_ok=bool(ok_d), band_ok=bool(ok_b), pass_=bool(ok_n and ok_d and ok_b), frozen_rule=(MODE == "M2"))
        P(f"{MODE}: {'PASS' if ok_n and ok_d and ok_b else 'FAIL'} (nodes within max(1 sigma, 0.03): {ok_n}; dchi2 {a['P2']['dchi2']:.2f} >= 9: {ok_d}; 68% upper at 2.33 {a['P1']['2.33']['sqrtX_q'][3]:.3f} < 1: {ok_b})" + ("" if MODE == "M2" else "  [reported only]"))
    prim = load("cfg689.json")
    if (MODE.startswith("B") or MODE == "F") and prim is not None:
        b = prim["BAO+SN"]; res["flips"] = dict(P1=a["P1_class"] != b["P1_class"], P2=a["P2"]["P2_class"] != b["P2"]["P2_class"])
        P(f"{MODE} vs primary: P1 {a['P1_class']} vs {b['P1_class']}; P2 {a['P2']['P2_class']} vs {b['P2']['P2_class']} -> flips {res['flips']}"
          + ("  (F: FLATNESS-SENSITIVE if any flip)" if MODE == "F" else ""))
    if MODE == "TU3F":     # A2.3 P2-with-theta* rule: all three SN sets (flat + theta*) must reach >= 3 sigma
        tri = {m_: (load(f"cfg689_{m_}.json") or {}).get("BAO+SN", {}).get("P2", {}).get("sigma_equiv") for m_ in ("TF", "TD5F")}; tri["TU3F"] = a["P2"]["sigma_equiv"]
        if all(v is not None for v in tri.values()):
            n3 = sum(v >= 3 for v in tri.values()); weakest = min(tri.values())
            cls3 = "EVOLVING DE REQUIRED with theta*" if n3 == 3 else ("SN-DEPENDENT" if n3 >= 1 else ("HINT" if weakest >= 2 else "CONSISTENT WITH CONSTANT"))
            res["P2_theta_rule"] = dict(sigma=tri, P2_theta_class=cls3); P(f"P2 with theta* across SN sets {tri} -> {cls3} (5-dof node test; DESI's w0-wa test has 2 dof)")
        else: P(f"P2 with theta*: needs cfg689_TF.json and cfg689_TD5F.json first ({tri})")
if MODE == "primary":   # P4 (A1.3): native best fit vs DESI's fiducial, at each tracer z
    wn, wk, wb, wc = split(np.array(res["BAO+SN"]["P2"]["pbest"])); _, Hn, DMn, _ = bg(wn, wb, wc, wk); rdn = rdrag(wb, wc)
    al = {}
    for t in ANISO:
        ap = (np.interp(t[1], zg, DMn)/rdn)/(np.interp(t[1], zg, DMF)/RDF); apar = (np.interp(t[1], zg, HF)*RDF)/(np.interp(t[1], zg, Hn)*rdn)
        al[t[0]] = dict(a_perp=float(ap), a_par=float(apar), a_iso=float((ap*ap*apar)**(1/3)), a_AP=float(apar/ap))
    inside = all(SPAN_ISO[0] <= v["a_iso"] <= SPAN_ISO[1] and SPAN_AP[0] <= v["a_AP"] <= SPAN_AP[1] for v in al.values())
    res["P4"] = dict(fiducial=FID, r_d_fid=RDF, alphas=al, span_iso=SPAN_ISO, span_AP=SPAN_AP, P4_class="INSIDE TESTED SPAN" if inside else "OUTSIDE")
    P(f"P4: DESI fiducial r_d {RDF:.3f}; alpha_iso/alpha_AP " + "; ".join(f"{k} {v['a_iso']:.4f}/{v['a_AP']:.4f}" for k, v in al.items())
      + f" vs spans {SPAN_ISO}/{SPAN_AP} -> {res['P4']['P4_class']}")
res["checks"] = checks
if MODE == "primary":
    a = res["BAO+SN"]; e3 = "/".join(str(None if a["P1"][str(z)]["e_3sigma"] is None else round(a["P1"][str(z)]["e_3sigma"], 3)) for z in ZS)
    P(f"\nVERDICT (curvature-free primary; F, brackets, MUTATE and P5 in their own files): P0 {a['P0']['P0_class']}; P1 {a['P1_class']} (e_3sigma at z* 1.0/1.2/1.5/2.33 = {e3}; record samples "
      + "; ".join(f"{k} {g['grade']}" for k, g in a["grades"].items()) + f"); P2 {a['P2']['P2_class']} (dchi2 {a['P2']['dchi2']:.2f}/{a['P2']['dof']}, "
      f"{a['P2']['sigma_equiv']:.2f} sigma); native H0 {a['P3']['H0_q'][2]:.2f} [{a['P3']['H0_q'][1]:.2f}, {a['P3']['H0_q'][3]:.2f}]; P4 {res['P4']['P4_class']}; "
      + "; ".join(f"{k} {'PASS' if v['ok'] else 'FAIL'}" for k, v in checks.items()) + f"; K4 {'PASS' if a['K4']['ok'] else 'FAIL'}")
    P("kappa fitted; cold energy mass required; not theory closed; nothing here says the data favour the framework over LCDM.")
json.dump(res, open(os.path.join(HERE, f"cfg689{TAG}.json"), "w"), indent=1, default=float)
P(f"wrote cfg689{TAG}.json")
