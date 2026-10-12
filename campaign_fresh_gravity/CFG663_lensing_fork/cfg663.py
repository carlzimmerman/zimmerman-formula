#!/usr/bin/env python3
"""CFG663 (FROZEN_CRITERIA.md, 93c6e29ce): does the response sector have to lens?  Dynamics vs lensing at the same g_bar.

H-L : SPARC dynamics predicted by the law F(g_bar).
H-NL: lensing sees only Newtonian mass, so KiDS fixes g_cold,req = g_lens,obs - g_bar and SPARC dynamics must be
      F(g_bar) + g_cold,req(g_bar).
Raw data: Brouwer et al. 2021 KiDS-1000 isolated lensing RAR (release tar on disk; extracted into a fresh temp directory) and
SPARC rotmod via the record's CFG4 harness (Upsilon = 0.61).  kappa = 1/2 FITTED; footings never pooled; cold energy mass
required; no particle species; not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I cfg663.py     (CFG663_MUTATE=1 -> _MUTATE outputs, exit 1 iff both teeth bite)"""
import os, sys, io, json, math, tarfile, tempfile, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
    import CFG7_common as C7
MUT = os.environ.get("CFG663_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
FOOTS = ("canonical", "alt")
TAR = os.path.join(os.path.dirname(REPO), "_external_data", "kids_lensing_zsplit", "brouwer2021_rar.tar")
G_PC, PC_M = 4.52e-30, 3.086e16                     # record's loader (prep_2026/mi_lensing_final): g = 4 G ESD / bias
CONV = 4 * G_PC * PC_M
OUT, RES = [], {"lane": "CFG663", "criteria": "93c6e29ce", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


nu = lambda y: np.asarray(C7.nu_mono(np.asarray(y, float)), float)
law = lambda gb, a0: nu(gb / a0) * gb

# ------------------------------------------------------------------------------------------------ lensing data
tmp = tempfile.mkdtemp(prefix="cfg663_b21_")
with tarfile.open(TAR) as tf:
    for m in tf.getmembers():
        if m.isfile() and m.name.endswith(".txt") and ".." not in m.name and not m.name.startswith("/"):
            tf.extract(m, tmp, filter="data")


def find(name):
    for root, _, files in os.walk(tmp):
        if name in files:
            return os.path.join(root, name)
    raise FileNotFoundError(name)


def load(profile, cov, obs_min):
    d = np.loadtxt(find(profile), comments="#")
    gb, esd, err, bias = d[:, 0], d[:, 1], d[:, 3], d[:, 4]
    c = np.loadtxt(find(cov), comments="#")
    sel = (np.isclose(c[:, 0], obs_min) & np.isclose(c[:, 1], obs_min)) if obs_min is not None else np.ones(len(c), bool)
    c = c[sel]
    n = len(gb); C = np.zeros((n, n))
    for row in c:
        i = int(np.argmin(np.abs(np.log(gb) - math.log(row[2])))); j = int(np.argmin(np.abs(np.log(gb) - math.log(row[3]))))
        C[i, j] = row[4] / row[6]
    return dict(gb=gb, gobs=CONV * esd / bias, gerr=CONV * err / bias, esd=esd / bias, cov=C)


LENS = {"blue (primary)": load("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
        "all isolated (secondary)": load("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", None)}
for k, L in LENS.items():
    dchk = float(np.max(np.abs(np.sqrt(np.diag(L["cov"])) - L["gerr"] / CONV)))      # sqrt(cov diag) vs profile error
    L["diag_check"] = dchk
    P(f"{k}: 15 bins g_bar {L['gb'][0]:.2e}..{L['gb'][-1]:.2e}; covariance diag vs profile error max diff {dchk:.2e} (ESD units)")

# ------------------------------------------------------------------------------------------------ SPARC
with contextlib.redirect_stdout(io.StringIO()):
    g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
iu = int(np.argmin(np.abs(g4["UPS"] - 0.61)))
gb4, go4, ok4, ww4 = g4["GB"][:, iu], g4["GO"][:, iu], g4["OK"][:, iu], g4["WW"][:, iu]


def gcold_req(L, gobs):
    gc = np.maximum(gobs - L["gb"], 0.0)
    if MUT and os.environ.get("CFG663_M", "") == "M1":
        gc = 0 * gc
    return lambda g: np.interp(np.log10(g), np.log10(L["gb"]), gc)


def score(L, gobs, a0, rng=None):
    lo = L["gb"][L["gb"] >= 3e-13].min(); hi = L["gb"].max()
    m = ok4 & (gb4 >= lo) & (gb4 <= hi)
    fL = law(gb4[m], a0); gc = gcold_req(L, gobs)(gb4[m]); fNL = fL + gc
    w = ww4[m]; lo_ = np.log10(go4[m])
    rL = float(np.sqrt(np.sum(w * (lo_ - np.log10(fL)) ** 2) / w.sum()))
    rN = float(np.sqrt(np.sum(w * (lo_ - np.log10(fNL)) ** 2) / w.sum()))
    bL = float(np.sum(w * (lo_ - np.log10(fL))) / w.sum()); bN = float(np.sum(w * (lo_ - np.log10(fNL))) / w.sum())
    ratio = float(np.median(gc / fL))
    return dict(n=int(m.sum()), ngal=int(len(np.unique(g4["GI"][m]))), lo=float(lo), hi=float(hi), rms_L=rL, rms_NL=rN,
                d=rN - rL, bias_L=bL, bias_NL=bN, med_gcold_over_F=ratio)


rng = np.random.default_rng(663)
VER = {}
for lk, L in LENS.items():
    gobs = L["gb"].copy() if (MUT and os.environ.get("CFG663_M", "") == "M2") else L["gobs"]
    for foot in FOOTS:
        a0 = C7.A0_SI[foot]
        s0 = score(L, gobs, a0)
        if not (MUT and os.environ.get("CFG663_M", "") == "M2"):
            draws = rng.multivariate_normal(L["esd"], L["cov"], size=2000) * CONV
            dd = np.array([score(L, gd, a0)["d"] for gd in draws])
        else:
            dd = np.zeros(2000)
        frac = float(np.mean(dd >= 0.03))
        if s0["med_gcold_over_F"] < 0.1:
            cls = "NOT DIAGNOSTIC"
        elif s0["d"] >= 0.05 and frac >= 0.95:
            cls = "H-NL EXCLUDED"
        elif s0["d"] <= 0.01:
            cls = "H-NL CONSISTENT"
        else:
            cls = "TENSION"
        resid = L["gobs"] - law(L["gb"], a0)
        Ci = np.linalg.inv(L["cov"] * CONV ** 2)
        chi2_law = float(resid @ Ci @ resid)
        s0.update(frac_draws_d_ge_0p03=frac, d_draw_p05=float(np.percentile(dd, 5)), d_draw_p50=float(np.median(dd)),
                  cls=cls, kids_vs_law_chi2=chi2_law, kids_dof=15)
        VER[f"{lk}|{foot}"] = s0
        P(f"\n[{lk} | {foot}] overlap g_bar {s0['lo']:.2e}..{s0['hi']:.2e}: {s0['n']} SPARC points in {s0['ngal']} galaxies")
        P(f"   rms H-L (law) {s0['rms_L']:.4f}   rms H-NL {s0['rms_NL']:.4f}   d {s0['d']:+.4f} dex   "
          f"(draws: median {s0['d_draw_p50']:+.4f}, 5th pct {s0['d_draw_p05']:+.4f}, frac >= 0.03 {frac:.3f})")
        P(f"   mean residual log(g_obs/g_pred): H-L {s0['bias_L']:+.4f}  H-NL {s0['bias_NL']:+.4f};  median g_cold,req/F {s0['med_gcold_over_F']:.3f}")
        P(f"   context: KiDS lensing vs the law, chi2 {chi2_law:.1f} / 15 bins  -> class {cls}")

prim = [VER[f"blue (primary)|{f}"]["cls"] for f in FOOTS]
label = prim[0] if prim[0] == prim[1] else "MIXED (" + " / ".join(prim) + ")"
RES["verdicts"] = VER; RES["label_primary"] = label
P(f"\nPRIMARY LABEL (blue lenses, both footings): {label}")
rc = 0
if MUT:
    mode = os.environ.get("CFG663_M", "")
    RES["mutate_mode"] = mode
    if mode == "M1":
        bite = all(v["d"] == 0.0 for v in VER.values())
    elif mode == "M2":
        bite = all(v["cls"] == "NOT DIAGNOSTIC" for v in VER.values())
    else:
        bite = False
    RES["tooth_bites"] = bite
    P(f"MUTATE {mode}: tooth bites: {bite}")
    rc = 1 if bite else 0
json.dump(RES, open(os.path.join(HERE, f"cfg663_results{TAG}{os.environ.get('CFG663_M', '')}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg663{TAG}{os.environ.get('CFG663_M', '')}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)
