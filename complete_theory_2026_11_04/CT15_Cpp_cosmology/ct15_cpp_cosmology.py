"""CT15: G5 (raw Planck TT H3/H2 with the dust amount FITTED), background (DESI DR2 BAO, Pantheon+ diag) and linear growth
for candidate C'' (FROZEN_CRITERIA.md, written first). Dust = v3s's khronon charge through Q6's validated khronon CLASS
(aest_K_type 4 = LOB at mu_K 0.03 / 0.1 Mpc^-1; 0 = exact dust limit, the NOT-FAITHFUL reference; mu_K 10 Mpc^-1 reported).
phi = thawing quintessence fluid (Omega_Lambda = 0, cs2_fld = 1). Run:
OMP_NUM_THREADS=1 nice -n 10 python3 ct15_cpp_cosmology.py > ct15_cpp_cosmology.out   (minutes, < 0.5 GB).
kappa = 1/2 FITTED and unused at linear order. Adopts nothing; reinstates nothing; no particle."""
import json, os, re, subprocess, time, resource
import numpy as np
from scipy.optimize import brentq
from classy import Class

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(ROOT, "..", "_external_data"))
KHR = os.path.join(EXT, "class_khronon_build_2026_10_23", "class_khronon", "class")
RUNS = os.path.join(EXT, "ct15_cpp_cosmology_2026_11_04"); os.makedirs(RUNS, exist_ok=True)
T0 = time.time()
OL = 0.666; H_C = 0.5 * (0.6722 + 0.6856); OB = 0.0224
w_r = 2.4728e-5 * (1 + 0.22711 * 3.046); wDE = OL * H_C ** 2
RAW = {"H3H2": 0.979, "H3H2_err": 0.010, "H2H1": 0.451, "l": (222, 533, 814)}          # ct3_cmb_checks.out:2-5
WIN = (0.969, 0.989); NS = [0.93, 0.9649, 1.0]; GRID = [0.0, 0.06, 0.12, 0.24, 0.48]
MODELS = {"LOB_mu0.1": (4, 0.1), "LOB_mu0.03": (4, 0.03), "DUST_notfaithful": (0, None), "LOB_mu10_BScap_reported": (4, 10.0)}
PHI = {"primary_frozen": (-1 + 1e-4, 0.0), "thaw_w0-0.9_reported": (-0.9, -1.58 * 0.1)}
ENV = dict(os.environ, OMP_NUM_THREADS="1")
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
KH = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0}
OUT = {"inputs": {"omega_DE": wDE, "omega_b": OB, "omega_r": w_r, "h_native": H_C}, "runs": {}}
print(f"inputs: omega_DE {wDE:.4f}  omega_b {OB}  omega_r {w_r:.4e}  (h by flat closure)")
NRUN = 0
CKPT = os.path.join(RUNS, "ct15_checkpoint.json")
CACHE = json.load(open(CKPT)) if os.path.exists(CKPT) else {}

def h_closure(wx): return float(np.sqrt(OB + wx + wDE + w_r))

def run(name, ktype, mu, wx, ns, phi, h=None, wb=OB, lam=False):
    """one khronon-CLASS run; returns dict with peaks, H3/H2, H2/H1, sigma8."""
    global NRUN
    if name in CACHE: OUT["runs"][name] = CACHE[name]; return CACHE[name]
    h = h_closure(wx) if h is None else h
    p = {"output": "tCl,mPk", "l_max_scalars": 2200, "T_cmb": 2.7255, "N_ur": 3.046, "YHe": 0.2454, "write_parameters": "no",
         "input_verbose": 1, "fourier_verbose": 1, "overwrite_root": "yes", **HIGH, **START,
         "omega_b": wb, "h": h, "A_s": 2.1e-9, "n_s": ns, "tau_reio": 0.0544, "omega_cdm": 1e-8, "omega_aest": max(wx, 1e-8),
         **KH, "aest_K_type": ktype, "aest_K2": 1.0 if mu is None else mu ** 2, "P_k_max_h/Mpc": 2.0}
    if not lam:
        p.update({"Omega_Lambda": 0.0, "w0_fld": phi[0], "wa_fld": phi[1], "cs2_fld": 1.0})
    rt = os.path.join(RUNS, name + "_"); p["root"] = rt
    with open(rt + ".ini", "w") as fh:
        fh.writelines(f"{k} = {v}\n" for k, v in p.items())
    t = time.time()
    r = subprocess.run(["nice", "-n", "15", KHR, rt + ".ini"], capture_output=True, text=True, env=ENV, timeout=1800)
    NRUN += 1
    if r.returncode != 0:
        return {"fail": (r.stdout + r.stderr).strip().splitlines()[-1][-300:]}
    assert os.path.getmtime(rt + "_cl.dat") >= t - 1, "stale-output guard"
    a = np.loadtxt(rt + "_cl.dat"); ll, DD = a[:, 0], a[:, 1]
    pk = [(ll[i], DD[i]) for i in range(5, len(DD) - 5) if DD[i] == DD[i - 5:i + 6].max() and ll[i] > 100][:3]
    m = re.search(r"sigma8=([0-9.eE+-]+) for total matter", r.stdout)
    s8 = float(m.group(1)) if m else np.nan
    o = {"h": h, "omega_x": wx, "n_s": ns, "l_peaks": [int(x[0]) for x in pk], "H3H2": pk[2][1] / pk[1][1],
         "H2H1": pk[1][1] / pk[0][1], "sigma8": s8, "sec": round(time.time() - t, 1)}
    OUT["runs"][name] = o; CACHE[name] = o
    json.dump(CACHE, open(CKPT, "w"), default=float)               # checkpoint after every run (resume skips done runs)
    return o

# ---------------- check ----------------
c = run("CHECK_DUST_ct3base", 0, None, 0.12, 0.9649, None, h=0.6736, wb=0.02237, lam=True)
print(f"CHECK binary DUST at CT3 base: H3/H2 {c['H3H2']:.4f} (CT3 0.992; |d| <= 0.004: {'OK' if abs(c['H3H2']-0.992) <= 0.004 else 'FAIL'})  peaks {c['l_peaks']}")
OUT["check"] = c

# ---------------- G5 fit ----------------
G5 = {}
for mn, (kt, mu) in MODELS.items():
    G5[mn] = {}
    for ns in NS:
        vals = {}
        for wx in GRID:
            o = run(f"{mn}_ns{ns}_wx{wx}", kt, mu, wx, ns, PHI["primary_frozen"])
            vals[wx] = o.get("H3H2", np.nan)
        line = "  ".join(f"{wx}: {v:.3f}" for wx, v in vals.items())
        sol = None; xs = list(vals)
        for x1, x2 in zip(xs[:-1], xs[1:]):
            if (vals[x1] - RAW["H3H2"]) * (vals[x2] - RAW["H3H2"]) <= 0:
                f = lambda wx: run(f"{mn}_ns{ns}_solve{wx:.6f}", kt, mu, wx, ns, PHI["primary_frozen"])["H3H2"] - RAW["H3H2"]
                sol = brentq(f, x1, x2, xtol=2e-4); break
        rec = {"grid": {str(k): v for k, v in vals.items()}, "max_grid": float(np.nanmax(list(vals.values())))}
        if sol is not None:
            o = run(f"{mn}_ns{ns}_fit", kt, mu, sol, ns, PHI["primary_frozen"])
            rec.update({"omega_x_fit": sol, "ratio_fit": sol / OB, "fit_run": o})
            print(f"G5 {mn} n_s {ns}: H3/H2 on grid {line} -> fitted omega_x {sol:.4f} (omega_x/omega_b {sol/OB:.2f}); "
                  f"H3/H2 {o['H3H2']:.3f}, H2/H1 {o['H2H1']:.3f} (raw 0.451), peaks l {o['l_peaks']} (raw 222/533/814), sigma8 {o['sigma8']:.4f}")
        else:
            print(f"G5 {mn} n_s {ns}: H3/H2 on grid {line} -> no omega_x reaches 0.979 (max {rec['max_grid']:.3f})")
        G5[mn][str(ns)] = rec
    fits = [G5[mn][str(ns)].get("omega_x_fit") for ns in NS]
    if all(f is not None for f in fits): v = "PASS (fitted omega_x)"
    elif all(G5[mn][str(ns)]["max_grid"] < WIN[0] for ns in NS): v = "FAIL"
    else: v = "NO VERDICT"
    G5[mn]["verdict"] = v
    rr = [f / OB for f in fits if f is not None]
    print(f"G5 VERDICT {mn}: {v}" + (f"; omega_x/omega_b {min(rr):.2f}-{max(rr):.2f} over n_s, in 4.9-5.4: "
                                       f"{'yes' if all(4.9 <= x <= 5.4 for x in rr) else 'no'}" if rr else ""))
OUT["G5"] = G5

# ---------------- background (vanilla classy; LOB's background is the dust background, Q6 A2) ----------------
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = (0.295, 7.942, 0.075)                                # as CT11 (CFG681 transcription)
sn = np.genfromtxt(os.path.join(ROOT, "prep_2026", "sne_lambda", "pantheonplus_full.dat"), names=True, dtype=None, encoding=None)
msk = (sn["IS_CALIBRATOR"] == 0) & (sn["zHD"] > 0.01)
zs, zh, mb, emb = sn["zHD"][msk], sn["zHEL"][msk], sn["m_b_corr"][msk], sn["m_b_corr_err_DIAG"][msk]
def background(wx, phi, lam=False):
    h = h_closure(wx); c = Class()
    p = {"h": h, "omega_b": OB, "omega_cdm": max(wx, 1e-12), "N_ur": 3.046, "YHe": 0.2454}
    if not lam: p.update({"Omega_Lambda": 0.0, "w0_fld": phi[0], "wa_fld": phi[1], "cs2_fld": 1.0})
    c.set(p); c.compute(); rd = c.rs_drag(); chi = 0.0
    for (_, z, dm, sdm, dh, sdh, r) in ANISO:
        m = np.array([c.angular_distance(z) * (1 + z) / rd, 1 / c.Hubble(z) / rd]); d = np.array([dm, dh])
        C = np.array([[sdm ** 2, r * sdm * sdh], [r * sdm * sdh, sdh ** 2]]); chi += (d - m) @ np.linalg.solve(C, d - m)
    z = BGS[0]; dv = (z * (c.angular_distance(z) * (1 + z)) ** 2 / c.Hubble(z)) ** (1 / 3) / rd; chi += ((BGS[1] - dv) / BGS[2]) ** 2
    mu = np.array([5 * np.log10((1 + zh[i]) * c.angular_distance(zs[i]) * (1 + zs[i])) for i in range(len(zs))])
    w = 1 / emb ** 2; res = mb - mu; off = np.sum(w * res) / np.sum(w); chisn = np.sum(w * (res - off) ** 2)
    c.struct_cleanup(); return h, rd, chi, chisn
c0 = background(0.12, None, lam=True)
print(f"CHECK background: Lambda, omega_x 0.12 -> h {c0[0]:.4f} r_d {c0[1]:.1f} BAO chi2 {c0[2]:.1f} (CT11 README: out:23, 46.8)")
BG = {}
for mn in MODELS:
    f = G5[mn][str(0.9649)].get("omega_x_fit")
    if f is None:
        print(f"BG {mn}: no fitted omega_x at n_s 0.9649, not graded"); continue
    for pn, phi in PHI.items():
        h, rd, chi, chisn = background(f, phi)
        v = "PASS" if chi <= 28.3 else "FAIL"
        BG[f"{mn}|{pn}"] = {"omega_x": f, "h": h, "r_d": rd, "chi2_BAO_13": chi, "chi2_SN_diag": chisn, "N_SN": int(msk.sum()), "verdict": v}
        print(f"BG {mn} phi {pn}: omega_x {f:.4f} h {h:.4f} Omega_m {(OB+f)/h**2:.4f} r_d {rd:.1f} Mpc  BAO chi2 (13) {chi:.1f} -> {v};  SN diag chi2 {chisn:.0f}/{msk.sum()} (reported)")
OUT["background"] = BG

# ---------------- growth ----------------
GR = {}
for mn in MODELS:
    rec = G5[mn][str(0.9649)]
    if "fit_run" in rec:
        o = rec["fit_run"]; Om = (OB + o["omega_x"]) / o["h"] ** 2; S8 = o["sigma8"] * np.sqrt(Om / 0.3)
        v = "PASS" if 0.51 <= S8 <= 1.16 else "FAIL"
        GR[mn] = {"sigma8": o["sigma8"], "Omega_m": Om, "S8": S8, "verdict": v}
        print(f"GROWTH {mn} (fitted omega_x {o['omega_x']:.4f}): sigma8 {o['sigma8']:.4f}, Omega_m {Om:.4f}, S8 {S8:.4f} vs raw KiDS ~0.77, line [0.51, 1.16] -> {v}")
    else:
        # no fit: report the growth at the grid point closest to the window (most favourable) for the order of magnitude
        g = {float(k): v for k, v in rec["grid"].items()}; wbest = max(g, key=g.get)
        o = OUT["runs"][f"{mn}_ns0.9649_wx{wbest}"]; Om = (OB + wbest) / o["h"] ** 2; S8 = o["sigma8"] * np.sqrt(Om / 0.3)
        GR[mn] = {"sigma8": o["sigma8"], "S8": S8, "omega_x": wbest, "verdict": "not graded (G5 failed); reported"}
        print(f"GROWTH {mn} (no fit; grid omega_x {wbest} with the highest H3/H2): sigma8 {o['sigma8']:.4f}, S8 {S8:.4f} (reported)")
OUT["growth"] = GR
OUT["n_class_runs"] = NRUN; OUT["elapsed_s"] = round(time.time() - T0, 1)
OUT["peak_rss_GB_children"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9
OUT["peak_rss_GB_self"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
print(f"runs {NRUN}, {OUT['elapsed_s']} s, peak RSS self {OUT['peak_rss_GB_self']:.2f} GB, children {OUT['peak_rss_GB_children']:.2f} GB")
json.dump(OUT, open(os.path.join(HERE, "ct15_cpp_cosmology.json"), "w"), indent=1, default=float)
