#!/usr/bin/env python3
"""NC2 gate G1 (primary CMB), FROZEN_CRITERIA.md row G1, readings Z / P / C, KA1, KA4, MUTATE M1 / M2.
Reuses QX15's footing parameter builder, CAMB wrapper and grader by import (nothing is written into QX15's dirs).
Modes:
  run <foot>        -> parts/g1_<foot>.json          (env NC2_MUTATE=1 -> parts/g1_<foot>_MUTATE.json, M1 + M2 only)
  grade             -> nc2_g1.json / nc2_g1.out      (env NC2_MUTATE=1 -> nc2_g1_MUTATE.json / .out)
Both footings (canonical, alt), never pooled. The component is cold dark energy; no particle.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
QXD = os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood")
sys.path.insert(0, QXD)
import qx15 as Q                                   # import only: defines functions, no runs
import camb

PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
NOTE = "kappa = 1/2 FITTED; not theory closed"
MUT = os.environ.get("NC2_MUTATE", "0") == "1"
KEYS = ["omega_b", "omega_d", "lnAs1e10", "n_s", "tau"]
RHO_UNIT = 2.77536627e11                           # Msun / Mpc^3 per unit omega
Z_REC, K_P = 1090.0, 0.05
B_LIST = [1.2, 1.5, 2.0]
MCL = [1e13, 1e14, 1e15]
STEP = np.array([1.5e-4, 0.004, 0.02, 0.008, 0.008])


def label(d):
    if not np.isfinite(d): return "NO VERDICT (non-finite)"
    return "PASS" if d <= 4 else ("TENSION" if d <= 25 else "FAIL")


def main_theta(foot):
    r = json.load(open(os.path.join(QXD, "parts", f"fit_{foot}_main.json")))
    return np.array([r["theta"][k] for k in KEYS]), r["chi2_PA"]


def qx15_ref(foot):
    return json.load(open(os.path.join(QXD, "qx15.json")))["footings"][foot]["main"]["chi2_PA"]


def peak_rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6   # macOS: bytes


# ---------------- reading Z: transfer ratio and mixed-mode spectra ----------------
def transfer_ratio(foot, th):
    """delta_cdm(z_rec, k_p) for the vector (1,0,0,0,0) and (0,1,0,0,0); synchronous gauge (CAMB's CDM frame) for both."""
    pr = Q.pars_foot(foot, list(th), "main")[0]; out = {}
    for name, vec in (("ad", [1, 0, 0, 0, 0]), ("cdi", [0, 1, 0, 0, 0])):
        p = camb.CAMBparams(); p.set_cosmology(**pr["cosmo"]); p.InitPower.set_params(As=pr["As"], ns=pr["ns"])
        p.scalar_initial_condition = "initial_vector"; p.InitialConditionVector = vec
        r = camb.get_results(p)
        out[name] = float(r.get_redshift_evolution([K_P], [Z_REC], vars=["delta_cdm"])[0, 0, 0])
    return out


def a_of_b(b, T):
    # delta_c,mix = T_ad + a T_cdi = b T_ad  ->  a = (b - 1) T_ad / T_cdi
    return (b - 1.0) * T["ad"] / T["cdi"]


def D_mixed(foot, th, a):
    pr = Q.pars_foot(foot, list(th), "main")[0]
    pr["extra"] = {"scalar_initial_condition": "initial_vector", "InitialConditionVector": [1.0, float(a), 0.0, 0.0, 0.0]}
    return Q.camb_D(pr)


def chi2_mixed(foot, th, a, x0=None):
    g = Q.QL.grade_spectra(D_mixed(foot, th, a), x0=x0); return g["PA"], g


# ---------------- readings P and C: uncorrelated CDI with a clump spectrum ----------------
def clump(th, M):
    ob, od = th[0], th[1]; R = od / ob
    rho_c = od * RHO_UNIT; rho_m = (ob + od) * RHO_UNIT
    n_cl = rho_c / M; r_cl = (3 * M * (1 + 1 / R) / (4 * math.pi * rho_m)) ** (1 / 3)
    return dict(R=R, f_c=R / (1 + R), rho_c=rho_c, n_cl=n_cl, r_cl=r_cl)


def u_th(x):
    x = np.asarray(x, float); out = np.ones_like(x); m = x > 1e-3
    xm = x[m]; out[m] = 3 * (np.sin(xm) - xm * np.cos(xm)) / xm ** 3
    out[~m] = 1 - x[~m] ** 2 / 10; return out


def D2S(k, cp, reading):
    x = k * cp["r_cl"]; PS = u_th(x) ** 2 / cp["n_cl"]          # f_in = 1, Mpc^3
    if reading == "C": PS = PS * np.minimum(1.0, x ** 4)
    return k ** 3 * PS / (2 * math.pi ** 2)


def kgrid(r_cl):
    lo = np.logspace(-6, -2, 300)
    hi = np.arange(0.01, 20.0, min(0.05 / r_cl, 0.01))          # dx <= 0.05 through the window oscillations
    return np.unique(np.concatenate([lo, hi]))


def cls_iso(foot, th, k=None, PK=None, powerlaw=False, lmax=7000):
    """pure CDI (vector (0,1,0,0,0)), UNLENSED scalar C_l in muK^2 (D_l), table = dimensionless power of S."""
    pr = Q.pars_foot(foot, list(th), "main")[0]
    p = camb.CAMBparams(); p.set_cosmology(**pr["cosmo"])
    if powerlaw:
        p.InitPower.set_params(As=pr["As"], ns=pr["ns"])
    else:
        ip = camb.initialpower.SplinedInitialPower(); ip.set_scalar_table(k, PK); p.set_initial_power(ip)
    p.set_for_lmax(lmax, lens_potential_accuracy=0); p.DoLensing = False
    p.scalar_initial_condition = "initial_vector"; p.InitialConditionVector = [0.0, 1.0, 0.0, 0.0, 0.0]
    r = camb.get_results(p); return r.get_unlensed_scalar_cls(lmax, CMB_unit="muK")


def cls_ad_unlensed(foot, th, lmax=7000):
    pr = Q.pars_foot(foot, list(th), "main")[0]
    p = camb.CAMBparams(); p.set_cosmology(**pr["cosmo"]); p.InitPower.set_params(As=pr["As"], ns=pr["ns"])
    p.set_for_lmax(lmax, lens_potential_accuracy=0); p.DoLensing = False
    r = camb.get_results(p); return r.get_unlensed_scalar_cls(lmax, CMB_unit="muK")


def grade_iso(Dad, cl_iso):
    Di = Q.pad(cl_iso); D = {k: Dad[k] + Di[k] for k in ("tt", "ee", "te")}
    g = Q.QL.grade_spectra(D); return g["PA"], g, D


# ---------------- refit (frozen rule: only when the no-refit Delta lies in 4-200) ----------------
def refit_Z(foot, th0, b, ref):
    cache = {}; st = {"x0": None, "best": None}
    def f(x):
        x = np.array(x, float); key = tuple(np.round(x, 9))
        if key in cache: return cache[key]
        pp = Q.pen(x, False)
        if pp > 0: cache[key] = 1e7 + 1e4 * pp; return cache[key]
        try:
            T = transfer_ratio(foot, x); a = a_of_b(b, T)          # b held fixed: a recomputed at each theta
            v, g = chi2_mixed(foot, x, a, st["x0"])
            if not np.isfinite(v): raise ValueError("nan")
            st["x0"] = {"Pcut": np.array(g["Pcut"]["nuis"]), "A": np.array(g["A"]["nuis"])}
            if st["best"] is None or v < st["best"][0]: st["best"] = (v, x.tolist(), a)
        except Exception as e:
            v = 1e8; print("ERR", repr(e), flush=True)
        cache[key] = v; return v
    Q.nm(f, th0, STEP, 120)
    v, x, a = st["best"]
    return dict(chi2_PA=v, delta=v - ref, theta=dict(zip(KEYS, x)), a=a, nfev=len(cache))


# ---------------- runner ----------------
def run(foot):
    t0 = time.time(); th, chi_fit = main_theta(foot); ref = qx15_ref(foot)
    out = dict(foot=foot, theta_main=dict(zip(KEYS, th.tolist())), chi2_PA_qx15_main=ref, mutate=MUT, note=NOTE)
    pr = Q.pars_foot(foot, list(th), "main")[0]
    As, ns = pr["As"], pr["ns"]
    D2z = lambda k: As * (k / 0.05) ** (ns - 1)
    if not MUT:
        # KA1
        tt = time.time(); g = Q.QL.grade_spectra(Q.camb_D(pr)); Dad = None
        out["KA1"] = dict(chi2_PA=g["PA"], ref=ref, diff=g["PA"] - ref, pass_=bool(abs(g["PA"] - ref) <= 1e-2), sec=time.time() - tt)
        print("KA1", out["KA1"], flush=True)
        if not out["KA1"]["pass_"]:
            out["stopped"] = "KA1 failed"; json.dump(out, open(os.path.join(PARTS, f"g1_{foot}.json"), "w"), indent=1, default=float); return
        # Z
        T = transfer_ratio(foot, th); out["Z_transfer"] = dict(delta_cdm_ad_vec=T["ad"], delta_cdm_cdi_vec=T["cdi"], z=Z_REC, k=K_P,
                                                             gauge="synchronous (CDM rest frame), CAMB get_redshift_evolution")
        cacheZ = {}
        def dZ(b):
            if b not in cacheZ:
                a = a_of_b(b, T); tt = time.time(); v, g = chi2_mixed(foot, th, a)
                cacheZ[b] = dict(b=b, a=a, chi2_PA=v, delta=v - ref, sec=time.time() - tt); print("Z", cacheZ[b], flush=True)
            return cacheZ[b]["delta"]
        rows = []
        for b in [1.0] + B_LIST:
            d = dZ(b); r = dict(cacheZ[b]); r["label_norefit"] = label(d)
            if 4 < d <= 200 and b != 1.0:
                rf = refit_Z(foot, th, b, ref); r["refit"] = rf; r["label"] = label(rf["delta"])
            else:
                r["label"] = label(d); r["refit"] = None
            rows.append(r)
        out["Z_table"] = rows
        # tolerated b: bisection on t = log10|b - 1|, no-refit Delta <= 4
        def tol(sign):
            lo, hi = -7.0, math.log10(0.2)                # |b-1| from 1e-7 to 0.2
            blo = 1 + sign * 10 ** lo
            if dZ(blo) > 4: return dict(b=None, note="Delta > 4 already at |b-1| = 1e-7")
            if dZ(1 + sign * 10 ** hi) <= 4: return dict(b=1 + sign * 10 ** hi, note="edge of bracket (|b-1| = 0.2) still passes")
            for _ in range(16):
                m = 0.5 * (lo + hi)
                if dZ(1 + sign * 10 ** m) <= 4: lo = m
                else: hi = m
            return dict(b=1 + sign * 10 ** lo, b_fail=1 + sign * 10 ** hi, a=a_of_b(1 + sign * 10 ** lo, T), delta=cacheZ[1 + sign * 10 ** lo]["delta"])
        out["Z_tolerated"] = dict(upper=tol(+1), lower=tol(-1))
        out["Z_evals"] = sorted(cacheZ.values(), key=lambda r: r["b"])
        # P and C
        Dad = Q.camb_D(pr); PC = []
        for rd in ("P", "C"):
            for M in MCL:
                cp = clump(th, M); k = kgrid(cp["r_cl"]); PK = D2S(k, cp, rd)
                tt = time.time(); cl = cls_iso(foot, th, k, PK); v, g, D = grade_iso(Dad, cl)
                row = dict(reading=rd, M_cl=M, r_cl_Mpc=cp["r_cl"], n_cl_perMpc3=cp["n_cl"], chi2_PA=v, delta=v - ref, label=label(v - ref),
                           D2S={str(kk): float(D2S(np.array([kk]), cp, rd)[0]) for kk in (0.01, 0.05, 0.2)},
                           D2zeta={str(kk): D2z(kk) for kk in (0.01, 0.05, 0.2)},
                           Dtt_iso_l={str(l): float(cl[l, 0]) for l in (10, 200, 1000)}, sec=time.time() - tt,
                           refit="not run (Delta > 200)" if v - ref > 200 else ("not needed (Delta <= 4)" if v - ref <= 4 else "REQUIRED by frozen rule"))
                row["ratio_D2S_over_D2zeta"] = {kk: row["D2S"][kk] / row["D2zeta"][kk] for kk in row["D2S"]}
                PC.append(row); print("PC", rd, M, row["delta"], flush=True)
        out["PC_table"] = PC
        cp = clump(th, 1e14); out["clump_params_1e14"] = cp
        # KA4
        ci = cls_iso(foot, th, powerlaw=True, lmax=2500); ca = cls_ad_unlensed(foot, th, lmax=2500)
        fc = th[1] / (th[0] + th[1]); rat = ci[10, 0] / ca[10, 0]
        out["KA4"] = dict(C10_iso=float(ci[10, 0]), C10_ad=float(ca[10, 0]), ratio=float(rat), SW=(2 * fc) ** 2, ratio_over_SW=float(rat / (2 * fc) ** 2),
                          pass_=bool((1 / 1.5) <= rat / (2 * fc) ** 2 <= 1.5))
        print("KA4", out["KA4"], flush=True)
        tag = f"g1_{foot}.json"
    else:
        # M2: uniform (b = 1, a = 0) through the initial_vector path
        v, g = chi2_mixed(foot, th, 0.0)
        out["M2"] = dict(chi2_PA=v, ref=ref, delta=v - ref, reproduces_KA1=bool(abs(v - ref) <= 1e-2), label=label(v - ref))
        print("M2", out["M2"], flush=True)
        # M1: reading P, M_cl 1e14, Delta^2_S(0.05) placed in a scale-invariant (n_iso = n_s) uncorrelated CDI mode
        cp = clump(th, 1e14); A0 = float(D2S(np.array([K_P]), cp, "P")[0])
        k = np.logspace(-6, math.log10(20.0), 800); PK = A0 * (k / K_P) ** (ns - 1)
        cl = cls_iso(foot, th, k, PK); v, g, D = grade_iso(Q.camb_D(pr), cl)
        out["M1"] = dict(D2S_kp=A0, chi2_PA=v, delta=v - ref, label=label(v - ref), bites=bool((v - ref) > 25))
        print("M1", out["M1"], flush=True)
        tag = f"g1_{foot}_MUTATE.json"
    out["sec"] = time.time() - t0; out["peak_rss_MB_selfreport"] = peak_rss_mb()
    json.dump(out, open(os.path.join(PARTS, tag), "w"), indent=1, default=float)


def grade():
    J = {f: json.load(open(os.path.join(PARTS, f"g1_{f}{'_MUTATE' if MUT else ''}.json"))) for f in ("canonical", "alt")}
    rss = {}
    for f in J:
        fn = os.path.join(PARTS, f"time_{f}{'_MUTATE' if MUT else ''}.txt")
        if os.path.exists(fn):
            for line in open(fn):
                if "maximum resident set size" in line: rss[f] = int(line.split()[0]) / 1e6
    res = dict(gate="G1 primary CMB", footings=J, peak_rss_MB_time_l=rss, note="Isocurvature lensing neglected for P and C (disclosed). " + NOTE)
    L = [f"NC2 G1{' MUTATE' if MUT else ''} (primary CMB, QX15 grader PA). {NOTE}"]
    for f, r in J.items():
        L.append(f"== {f}  (QX15 main chi2_PA {r['chi2_PA_qx15_main']:.3f})  run {r['sec']:.0f} s  peak RSS {rss.get(f, float('nan')):.0f} MB")
        if not MUT:
            k = r["KA1"]; L.append(f"KA1 chi2_PA {k['chi2_PA']:.3f} diff {k['diff']:+.4f} pass={k['pass_']}")
            if "stopped" in r: continue
            T = r["Z_transfer"]; L.append(f"Z transfer delta_cdm(z 1090, k 0.05): vec(1,0) {T['delta_cdm_ad_vec']:.4f}  vec(0,1) {T['delta_cdm_cdi_vec']:.4f}")
            for z in r["Z_table"]:
                L.append(f"Z b {z['b']:.2f} a {z['a']:+.5f} Delta {z['delta']:+.2f} -> {z['label']}" + (f" (refit Delta {z['refit']['delta']:+.2f})" if z["refit"] else ""))
            for s in ("upper", "lower"):
                t = r["Z_tolerated"][s]; L.append(f"Z tolerated {s}: b {t.get('b')} (first failing {t.get('b_fail')}) a {t.get('a')} Delta {t.get('delta')} {t.get('note', '')}")
            for p in r["PC_table"]:
                L.append(f"{p['reading']} M_cl {p['M_cl']:.0e} r_cl {p['r_cl_Mpc']:.2f} Mpc Delta {p['delta']:+.4g} -> {p['label']}; D2S/D2zeta k .01/.05/.2: "
                         + " / ".join(f"{p['ratio_D2S_over_D2zeta'][kk]:.3g}" for kk in ("0.01", "0.05", "0.2")))
            k = r["KA4"]; L.append(f"KA4 C10 iso/ad {k['ratio']:.3f} vs (2 f_c)^2 {k['SW']:.3f}: ratio {k['ratio_over_SW']:.3f} pass={k['pass_']}")
        else:
            L.append(f"M2 uniform Delta {r['M2']['delta']:+.4f} reproduces KA1={r['M2']['reproduces_KA1']} -> {r['M2']['label']}")
            L.append(f"M1 flat CDI at D2S(0.05) {r['M1']['D2S_kp']:.4g}: Delta {r['M1']['delta']:+.4g} -> {r['M1']['label']} bites={r['M1']['bites']}")
    tag = "nc2_g1_MUTATE" if MUT else "nc2_g1"
    json.dump(res, open(os.path.join(HERE, tag + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "run": run(a[1])
    elif a[0] == "grade": grade()
