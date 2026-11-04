"""LAM11 core (criteria c6f59aea4c): LAM10's single-slope profile (variant A) with one mask change per run, plus each slope's
step-a chi2 by region; the synthetic sums rebuilt exactly as LAM9/LAM10 built them. Imports LAM9's and LAM10's code read-only.
κ = ½ FITTED; not theory closed."""
import os, sys, json, ctypes, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
L10DIR = os.path.join(RB, "LAM10_imf_single_slope"); L9DIR = os.path.join(RB, "LAM9_imf_from_spectra"); sys.path[:0] = [L10DIR, L9DIR]
import numpy as np
from ppxf.ppxf import ppxf
import lam10_core as C
L9 = C.L9
WORK = os.path.join(L9.EXT, "lam11_work_2026_11_04")
GAM = C.GAM
REG = {"Na": (8143.0, 8244.0), "CaT": (8474.0, 8792.0), "TiO": (5816.0, 6455.0)}; BLUE_END = 7400.0
RUNS = ("M0", "M_Na", "M_CaT", "M_TiO", "M_IMF", "M_blue")
_lib = ctypes.CDLL("/usr/lib/libSystem.B.dylib"); _lib.malloc_zone_pressure_relief.restype = ctypes.c_size_t
_lib.malloc_zone_pressure_relief.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
def relieve(): _lib.malloc_zone_pressure_relief(None, 0)
def mem():
    pid = str(os.getpid()); rss = int(subprocess.run(["ps", "-o", "rss=", "-p", pid], capture_output=True, text=True).stdout or 0) / 1024
    fp = [l.split(":")[1].strip() for l in subprocess.run(["footprint", pid], capture_output=True, text=True).stdout.splitlines() if l.strip().startswith("phys_footprint:")]
    return dict(rss_mb=round(rss), footprint=fp[0] if fp else "?")

def run_inputs(p, run):
    """The run's sum dict and good pixels: LAM10's variant-A mask plus the run's one change."""
    if run == "M0": return p, p["goodA"]
    if run == "M_blue":
        n = int(np.sum(p["lam"] < BLUE_END)); q = dict(p)
        for k in ("lam", "fw", "wobs", "idx", "flux", "noise"): q[k] = p[k][:n]
        return q, p["goodA"][p["goodA"] < n]
    regs = {"M_Na": ("Na",), "M_CaT": ("CaT",), "M_TiO": ("TiO",), "M_IMF": ("Na", "CaT", "TiO")}[run]; bad = np.zeros(len(p["lam"]), bool)
    for r in regs: bad |= (p["lam"] >= REG[r][0]) & (p["lam"] <= REG[r][1])
    return p, p["goodA"][~bad[p["goodA"]]]

def region_masks(lam):
    na = (lam >= REG["Na"][0]) & (lam <= REG["Na"][1]); ca = (lam >= REG["CaT"][0]) & (lam <= REG["CaT"][1]); ti = (lam >= REG["TiO"][0]) & (lam <= REG["TiO"][1])
    return dict(Na=na, CaT=ca, TiO=ti, blue_other=(lam < BLUE_END) & ~ti, red_other=(lam >= BLUE_END) & ~na & ~ca)

def profile_r(p, tpl, lam_t, n_t, kin, good, flux=None):
    """LAM10's profile (lam10_core.profile, variant A) with explicit good pixels, plus each slope's step-a chi2 by region."""
    f = p["flux"] if flux is None else flux; st = L9.kin_start(kin); T = L9.tlib(); R = region_masks(p["lam"])
    gm = np.zeros(len(p["lam"]), bool); gm[good] = True
    chi2, dof, A, regs = np.zeros(len(GAM)), np.zeros(len(GAM)), [], []
    for k, g in enumerate(GAM):
        cols = np.flatnonzero(np.abs(T["gamma"] - g) < 1e-9); tg = tpl[:, cols]
        pa = ppxf(tg, f, p["noise"], L9.VELSCALE, st, moments=6, fixed=[1] * 6, degree=-1, mdegree=10, goodpixels=good, lam=p["lam"], lam_temp=lam_t, quiet=True)
        chi2[k] = float(pa.chi2) * float(pa.dof); dof[k] = float(pa.dof); mp = pa.mpoly
        r2 = np.where(gm, ((f - pa.bestfit) / p["noise"]) ** 2, 0.0); regs.append({nm: float(r2[m].sum()) for nm, m in R.items()})
        pb = ppxf(tg.reshape(tg.shape[0], 14, 6), f / mp, p["noise"] / mp * np.sqrt(float(pa.chi2)), L9.VELSCALE, st, moments=6, fixed=[1] * 6, degree=-1,
                  mdegree=0, regul=100, reg_dim=(14, 6), goodpixels=good, lam=p["lam"], lam_temp=lam_t, quiet=True)
        A.append(C.slope_alpha(np.asarray(pb.weights, float).ravel(), cols, n_t))
    j = int(np.argmin(chi2)); s = chi2[j] / dof[j]
    i3 = [0, 1, 2] if j == 0 else ([len(GAM) - 3, len(GAM) - 2, len(GAM) - 1] if j == len(GAM) - 1 else [j - 1, j, j + 1])
    edge = "low" if j == 0 else ("high" if j == len(GAM) - 1 else "")
    a, b, _ = np.polyfit(GAM[i3], chi2[i3] - chi2[j], 2)
    if edge: gbest = float(GAM[j])
    else: gbest = float(np.clip(-b / (2 * a), GAM[j - 1], GAM[j + 1])) if a > 0 else float(GAM[j])
    sigma = float(1 / np.sqrt(a / s)) if a > 0 else float("nan")
    return dict(gamma_best=gbest, j=j, edge=edge, sigma=sigma, chi2=chi2.tolist(), alpha=A[j]["alpha"], alpha_ku2=A[j]["alpha_ku2"],
                chi2_regions=regs, n_good=int(len(good)))

def build_syn(q, S, narrow, tpl, lam_t, n_t, p):
    """LAM9's K synthetic (as lam9_k.py / lam10_k.py build it) for plan row q, on donor sum p."""
    L9W = os.path.join(L9.EXT, "lam9_work_2026_11_04", "w"); T = L9.tlib(); ug = np.unique(T["gamma"]); pf = q["donor"]; kin = S["FIT"][pf]
    W = np.load(os.path.join(L9W, f"{pf}_A.npz")); wb = W["wb"].astype(float); mp = W["mpoly"].astype(float); chi2a = float(W["chi2a"])
    WL = wb.reshape(L9.REG_DIM).sum(axis=2); w_in = np.zeros(L9.REG_DIM); w_in[:, :, int(np.argmin(np.abs(ug - q["gamma_in"])))] = WL; w_in = w_in.ravel()
    a_in = L9.summary(w_in, n_t)["alpha"]
    pc = ppxf((tpl @ w_in)[:, None], p["flux"] / mp, p["noise"] / mp, L9.VELSCALE, L9.kin_start(kin), moments=6, fixed=[1] * 6, degree=-1, mdegree=0,
              goodpixels=p["goodA"], lam=p["lam"], lam_temp=lam_t, quiet=True)
    syn = pc.bestfit * mp * (1 + narrow[p["idx"]])
    syn = syn + np.random.default_rng(q["seed"]).normal(0, 1, syn.size) * np.where(p["noise"] < 1e9, p["noise"], 0) * np.sqrt(max(chi2a, 1.0))
    return syn, a_in
