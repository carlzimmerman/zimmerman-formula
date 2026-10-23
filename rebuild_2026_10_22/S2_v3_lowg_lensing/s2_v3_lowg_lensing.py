#!/usr/bin/env python3
"""S2_v3_lowg_lensing: batch R2 of N0 (status-board tiles 17 'Isolated-galaxy lensing, inner' and 30 'Red (early-type)
lenses') recomputed for v3: AQUAL mu = x/(1+x) with the external field solved (F2's own solver, imported read-only),
F2's inventory baryons, native h and Omega_m, screening L* 24 / 90 pc, no supply rule; mu_K^2 term deferred to R6.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (c94150c05d, committed before any script or number).
Run (from anywhere):  OMP_NUM_THREADS=1 nice -n 15 python3 s2_v3_lowg_lensing.py [--mutate]
Outputs: s2_v3_lowg_lensing{,_MUTATE}.out and s2_v3_lowg_lensing_results{,_MUTATE}.json in this lane.
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time, resource
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
F2DIR = os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing")
sys.path.insert(0, F2DIR)
import f2_aqual as AQ                                   # F2's AQUAL solver + projection (side-effect-free module)

np.seterr(all="ignore")
MUT = "--mutate" in sys.argv[1:]
SFX = "_MUTATE" if MUT else ""
T0 = time.time()
OUT, CHK = [], {}
RES = {"lane": "S2_v3_lowg_lensing", "criteria": "c94150c05d", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, val, thr):
    CHK[name] = bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")


def finish():
    n, k = len(CHK), sum(CHK.values())
    P(f"\n  peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB; runtime {time.time() - T0:.0f} s")
    P(f"S2_V3_LOWG_LENSING COMPLETE: {k}/{n} checks PASS.")
    RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
    json.dump(RES, open(os.path.join(HERE, f"s2_v3_lowg_lensing_results{SFX}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"s2_v3_lowg_lensing{SFX}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if k == n else 1)


DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
B21 = os.path.join(DATA, "brouwer2021_rar")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
G_pc, PCm = 4.52e-30, 3.086e16                  # B21 README / CFG829: g_obs = 4 G ESD
GCONV = 4 * G_pc * PCm                          # (m/s^2) per (Msun/pc^2), applied identically to data and model
Gpc = 4.30091e-3                                # pc (km/s)^2 / Msun (F2)
G_SI, MSUN, MPC, PC = 6.674e-11, 1.989e30, 3.0857e22, 3.0857e16
def a0u(foot): return A0[foot] * 3.0857e16 / 1e6   # (km/s)^2 / pc
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_1 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-15)))   # v3: mu = x/(1+x)

P(f"S2_v3_lowg_lensing{'  [MUTATE: B21 g_obs x 1.10]' if MUT else ''}   criteria c94150c05d   kappa = 1/2 FITTED; "
  f"footings never pooled; mu_K^2 term deferred to R6")

# ============================================================================ 1. B21 RAR data (own re-implementation of CFG829's loader)
FILES = {"blue": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
         "red": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
         "all": ("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", None)}
NAME829 = {"blue": "blue (u-r<2.5)", "red": "red (u-r>2.5)", "all": "all isolated"}
CLS = ("blue", "red", "all")


def load(esd, cov, binmin):
    d = np.loadtxt(os.path.join(B21, esd)); gb, esdt, bias = d[:, 0], d[:, 1], d[:, 4]
    fac = 1.10 if MUT else 1.0
    go = GCONV * esdt / bias * fac
    c = np.loadtxt(os.path.join(B21, cov)); n = len(gb); C = np.zeros((n, n))
    sel = c if binmin is None else c[np.isclose(c[:, 0], binmin) & np.isclose(c[:, 1], binmin)]
    def idx(x):
        k = int(np.argmin(np.abs(gb / x - 1))); return k if abs(gb[k] / x - 1) < 1e-3 else None
    for row in sel:
        i, j = idx(row[2]), idx(row[3])
        if i is not None and j is not None:
            C[i, j] = row[4] / row[6]
    return gb, go, C * GCONV ** 2 * fac ** 2


DAT = {k: load(*v) for k, v in FILES.items()}
W = (10 ** -13.3, 10 ** -11.9); WC = (10 ** -11.9, 10 ** -10.9)


def wmask(gb, win, shift=0.0):
    g = gb * 10 ** shift
    return (g >= win[0]) & (g < win[1])


def gls(go, C, gm, msk):
    if msk.sum() < 2: return None
    Cs = C[np.ix_(msk, msk)]; m = gm[msk]; y = go[msk]
    Cim = np.linalg.solve(Cs, m); F = float(m @ Cim)
    A = float(y @ Cim) / F; r = y - A * m
    return dict(A=A, sA=F ** -0.5, n=int(msk.sum()), chi2_fit=float(r @ np.linalg.solve(Cs, r)))


def chi2_full(go, C, gm):
    r = go - gm; return float(r @ np.linalg.solve(C, r))


def cls_amp(A, s):
    if A - 1 > 3 * s: return "short"
    if 1 - A > 3 * s: return "over"
    if abs(A - 1) <= 2 * s: return "consistent"
    return "between"


# ---- K0a: CFG829 reproduction (algebraic nu_e, B21 distances)
J829 = json.load(open(os.path.join(CFG, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829_results.json")))
K0 = {}; dev = 0.0
for foot in FOOTS:
    for k in CLS:
        gb, go, C = DAT[k]
        a = gls(go, C, gb * nu_e(gb / A0[foot]), wmask(gb, W))
        ref = J829[f"{foot}|nu_e|{NAME829[k]}"]["window"]
        dev = max(dev, abs(a["A"] - ref["A"]), abs(a["sA"] - ref["sA"]))
        K0[f"{foot}|{k}"] = a
    P(f"  [{foot}] CFG829 (nu_e, algebraic, B21 distances): " + "  ".join(
        f"{k} A {K0[f'{foot}|{k}']['A']:.4f}+-{K0[f'{foot}|{k}']['sA']:.4f}" for k in CLS))
check("K0a_CFG829_reproduction", dev <= 5e-4, f"max|dA|,|dsA| {dev:.1e}", "<=5e-4")
RES["L0_CFG829"] = K0
if not CHK["K0a_CFG829_reproduction"]:
    P("K0a FAILED: the record is not reproduced; the lane stops here (criteria Sec. 5).")
    finish()

# ---- K0b: CFG850/926 algebraic shifted-g_bar path (window on the shifted g_bar), red lenses
J926 = json.load(open(os.path.join(CFG, "CFG926_small_reframings_B", "cfg926_results.json")))
D_RED = float(J926["R5"]["relation"]["D_red"]); D_BLUE = float(J926["R5"]["relation"]["D_blue"]); S667 = 0.123
dev = 0.0; K0b = {}
for foot in FOOTS:
    gb, go, C = DAT["red"]
    for lab, sh in (("before", S667), ("after", S667 + D_RED), ("IMF_alone", D_RED)):
        gbs = gb * 10 ** sh
        a = gls(go, C, gbs * nu_e(gbs / A0[foot]), wmask(gb, W, sh))
        ref = J926["R5"]["byfoot"][foot]["window850"][lab]["A_red"]
        dev = max(dev, abs(a["A"] - ref)); K0b[f"{foot}|{lab}"] = a
check("K0b_CFG926_window850_reproduction", dev <= 1e-6, f"max|dA_red| {dev:.1e} (D_red {D_RED:.5f})", "<=1e-6")
RES["K0b_CFG926"] = K0b

# ============================================================================ 2. native background on the data (CFG885 T, F2 h)
H_NAT = {"mid": 0.679, "lo": 0.672, "hi": 0.686}; OM_NAT = 0.3085
J885 = json.load(open(os.path.join(CFG, "CFG885_kids_rar_native_distances", "cfg885_results.json")))
TOM = {k: float(J885["fiducial_envelope"]["0.2793"]["T_window"][FILES[k][0]]) for k in CLS}
check("K7_T_Om_all_equals_F2", abs(TOM["all"] - 1.0128) <= 5e-4, f"{TOM['all']:.5f} (blue {TOM['blue']:.5f}, red {TOM['red']:.5f})", "|T-1.0128|<=5e-4")
RES["T_Om"] = TOM


def data_nat(k, h, pz=1.0):
    gb, go, C = DAT[k]; f = (h / 0.70) * TOM[k] * pz
    return gb, go * f, C * f * f


# ============================================================================ 3. lenses, weights, colours
LN = np.load(os.path.join(DATA, "lr_lenses.npz"))
PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
STK = np.load(os.path.join(DATA, "cfg96_stack.npz"))
WW, WG, GBE = PL["WW"], PL["WG"], PL["gbar_edges"]
logM70, Mgal70, zl, TYP = LN["logM"], LN["Mgal"], LN["z"], LN["typ"]
NL = len(zl)
# K4: the record's per-lens weights reproduce its W10 stack (per patch, per typ); B21 labels sit inside the weight bins
wsum = np.zeros((50, 2, 15)); gsum = np.zeros((50, 2, 15))
np.add.at(wsum, (STK["patch"], TYP), WW); np.add.at(gsum, (STK["patch"], TYP), WG)
k4 = float(max(np.max(np.abs(wsum - STK["W_10"])) / np.max(np.abs(STK["W_10"])),
               np.max(np.abs(gsum - STK["wgE_10"])) / np.max(np.abs(STK["wgE_10"]))))
inside = all(bool(np.all((DAT[k][0] >= GBE[:-1]) & (DAT[k][0] < GBE[1:]))) for k in CLS)
check("K4_weights_vs_record_stack", k4 <= 1e-10 and inside, f"{k4:.1e}; labels inside bins {inside}", "<=1e-10")
del gsum


def chi_flat(z, om):
    zz = np.linspace(0, 1.0, 4001); E = np.sqrt(om * (1 + zz) ** 3 + 1 - om)
    ch = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))])
    return np.interp(z, zz, ch)


qB = chi_flat(zl, OM_NAT) / chi_flat(zl, 0.3)              # F2's Omega_m-only D_A ratio for the record lenses
# u-r reconstruction (variant split 2.5): the record's CFG96 selection, matched by position
from astropy.io import fits
from scipy.spatial import cKDTree
import gc


def fcols(path, names, chunk=100000):
    """read the named columns of the first binary-table HDU in row chunks straight from the file (no scaled columns
    among them: checked from the header), so the table's pages never sit in this process's RSS"""
    with fits.open(path, memmap=True) as hd:
        h = hd[1].header; dt = hd[1].columns.dtype.newbyteorder(">"); off = hd[1].fileinfo()["datLoc"]   # FITS is big-endian
        n = int(h["NAXIS2"])
        for i in range(1, int(h["TFIELDS"]) + 1):
            if h[f"TTYPE{i}"] in names:
                assert h.get(f"TSCAL{i}") is None and h.get(f"TZERO{i}") is None, (path, h[f"TTYPE{i}"])
    assert dt.itemsize == int(h["NAXIS1"])
    out = {k: [] for k in names}
    with open(path, "rb") as f:
        f.seek(off)
        for i0 in range(0, n, chunk):
            a = np.fromfile(f, dtype=dt, count=min(chunk, n - i0))
            for k in names:
                out[k].append(a[k].copy() if a.dtype[k].kind == "S" else a[k].astype(a.dtype[k].newbyteorder("=")))
    gc.collect()
    return {k: np.concatenate(v) for k, v in out.items()}


_b = fcols(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), ("ID", "MAG_AUTO_CALIB", "zphot_ANNz2", "masked", "RAJ2000", "DECJ2000"))
_l = fcols(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), ("ID", "MASS_MED", "MAG_ABS_u", "MAG_ABS_r"))
idok = bool(np.array_equal(_b["ID"], _l["ID"]))
_lm = _l["MASS_MED"].astype("f8") + 0.15
_ur = _l["MAG_ABS_u"].astype("f8") - _l["MAG_ABS_r"].astype("f8")
_sel = (_b["MAG_AUTO_CALIB"] < 20) & (_b["zphot_ANNz2"] > 0.1) & (_b["zphot_ANNz2"] < 0.5) & (_b["masked"] == 0) & \
    np.isfinite(_lm) & (_lm > 7) & (_lm < 11.0) & np.isfinite(_ur)
_ra = _b["RAJ2000"].astype("f8")[_sel]; _de = _b["DECJ2000"].astype("f8")[_sel]
_lm = _lm[_sel]; _ur = _ur[_sel]
del _b, _l, _sel; gc.collect()


def uvec(ra, de):
    a, d = np.radians(ra), np.radians(de)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]


_dd, _jj = cKDTree(uvec(_ra, _de)).query(uvec(LN["ra"], LN["dec"]))
UR = _ur[_jj]
recon = idok and float(np.max(_dd)) <= 1e-9 and bool(np.allclose(_lm[_jj], logM70, atol=1e-9, rtol=0)) and \
    bool(np.array_equal((UR > 2.0).astype(int), TYP))
TYP25 = (UR > 2.5).astype(int)
del _ra, _de, _lm, _ur, _dd, _jj
MEMB = {"typ": {"blue": TYP == 0, "red": TYP == 1, "all": np.ones(NL, bool)},
        "ur25": {"blue": TYP25 == 0, "red": TYP25 == 1, "all": np.ones(NL, bool)}}
# K5: record re-measured stack per class vs B21 Fig-8 colour bins (calibration information)
SIGU = (3.0857e16) ** 2 / 1.989e30; ONEK = 0.9853
k5 = {}
for split in ("typ", "ur25"):
    for k in ("blue", "red"):
        m = MEMB[split][k]
        d = WG[m].sum(0) / WW[m].sum(0) * SIGU / ONEK
        f8 = np.loadtxt(os.path.join(B21, FILES[k][0])); y8 = f8[:, 1] / f8[:, 4]; e8 = f8[:, 3] / f8[:, 4]
        good = (y8 / e8 > 3) & np.isfinite(d)
        k5[f"{split}|{k}"] = float(np.median(d[good] / y8[good]))
ok5 = all(0.8 <= k5[f"typ|{k}"] <= 1.25 for k in ("blue", "red")) and recon
check("K5_colour_sanity_and_reconstruction", ok5,
      f"record/B21 median ratio typ blue {k5['typ|blue']:.3f} red {k5['typ|red']:.3f} (u-r 2.5: {k5['ur25|blue']:.3f} / "
      f"{k5['ur25|red']:.3f}); reconstruction exact {recon}; n blue/red typ {int((TYP == 0).sum())}/{int((TYP == 1).sum())}, "
      f"u-r 2.5 {int((TYP25 == 0).sum())}/{int((TYP25 == 1).sum())}", "[0.8,1.25] & exact")
RES["K5"] = dict(ratios=k5, reconstruction_exact=recon, n_typ=[int((TYP == 0).sum()), int((TYP == 1).sum())],
                 n_ur25=[int((TYP25 == 0).sum()), int((TYP25 == 1).sum())])
del WG
gc.collect()
P(f"  [{time.time() - T0:.0f} s] lenses {NL:,}; colours reconstructed; RSS so far {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB")

# R70[i, k]: radius at which lens i contributes to B21 bin k (h70 physical Mpc); labels identical across the 3 files?
LABELS = {k: tuple(np.round(DAT[k][0], 20)) for k in CLS}
R70 = {}
for k in CLS:
    key = LABELS[k]
    if key not in R70:
        R70[key] = np.sqrt(G_SI * Mgal70[:, None] * MSUN / DAT[k][0][None, :]) / MPC
R70c = {k: R70[LABELS[k]] for k in CLS}

# ============================================================================ 4. AQUAL solver (F2's) and checks K1, K3
YE = {f: {"zero": 0.0, "noclu": 10 ** -3.215 * 1.2e-10 / A0[f], "maxclu": 10 ** -2.30 * 1.2e-10 / A0[f]} for f in FOOTS}
J2 = json.load(open(os.path.join(F2DIR, "f2_outer_lensing_results.json")))
dye = max(abs(YE[f][k] - J2["y_e"][f][k]) / max(J2["y_e"][f][k], 1e-30) for f in FOOTS for k in ("noclu", "maxclu"))
RES["y_e"] = YE
SOL = {}
for f in FOOTS:
    for k in ("noclu", "maxclu"):
        SOL[(f, k)] = AQ.solve_efe(YE[f][k])
        s = SOL[(f, k)]
        P(f"  AQUAL EFE [{f} {k}] y_e {s['y_e']:.3e} -> x_e {s['x_e']:.4f}; iters {s['iters']}, change {s['resid']:.1e}; r_e = {1 / s['x_e']:.0f} r_M")
s1 = AQ.solve_efe(1e-6)
sg = np.array([0.1, 0.3, 1, 3, 10])
k1a = float(np.max(np.abs(np.interp(np.log(sg), np.log(s1["r"]), s1["M"]) / AQ.M_iso(sg) - 1)))
k1b = max(float(np.max(np.abs(s["M"][s["r"] >= 10 / s["x_e"]] / s["M_far"] - 1))) for s in SOL.values())
check("K1_solver_isolated_far_field_and_y_e", k1a <= 1e-3 and k1b <= 0.02 and dye <= 1e-12,
      f"iso {k1a:.1e}; far {k1b:.1e}; y_e vs F2 JSON {dye:.1e}", "<=1e-3, <=0.02, <=1e-12")
Rt = np.array([0.03, 0.3, 3.0]); rg = np.logspace(-6, 6, 6001)
pm = AQ.delta_sigma(Rt, rg, np.ones_like(rg), "const") * math.pi * Rt ** 2
sis = AQ.delta_sigma(Rt, rg, rg.copy(), "linear") * 4 * Rt
k3 = float(max(np.max(np.abs(pm - 1)), np.max(np.abs(sis - 1))))
check("K3_projection", k3 <= 1e-3, f"{k3:.1e}", "<=1e-3")
P(f"  [{time.time() - T0:.0f} s]")

# ============================================================================ 5. v3 model tables (F2's inventory and EFE construction)
LMG = np.round(np.arange(7.70, 11.80, 0.025), 3)            # native log M* (before any star shift)
LRT = np.linspace(math.log(0.001), math.log(8.0), 141)      # native Mpc
RGRID_PC = np.logspace(1.0, 10.0, 3601)
TAB = {}


def meff(foot, Ms, Mcold, Mhot, yk):
    """F2's meff_profile: isolated AQUAL on the inventory x the point-mass EFE ratio C(r; y_e)."""
    a0 = a0u(foot); Mpt = Ms + Mcold
    Mb = Mpt + Mhot * np.minimum(1.0, (RGRID_PC / 1e5) ** 3)
    Miso = Mb * AQ.nu_simple(Gpc * Mb / RGRID_PC ** 2 / a0)
    if yk == "zero":
        return Miso, "linear"
    s = SOL[(foot, yk)]
    rM = math.sqrt(Gpc * (Mpt + Mhot) / a0); sgr = RGRID_PC / rM
    Me = np.interp(np.log(sgr), np.log(s["r"]), s["M"], left=np.nan, right=s["M_far"])
    return Miso * np.where(np.isnan(Me), 1.0, Me / AQ.M_iso(sgr)), "const"


def table(foot, h, yk, fhot, dcold, dMs):
    key = (foot, h, yk, fhot, dcold, round(dMs, 8))
    if key in TAB: return TAB[key]
    tab = np.empty((len(LMG), len(LRT)))
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * math.log10(0.70 / h)
        Mcold = 10 ** (lm + (-0.69 * lm70 + 6.63) + dcold)            # cold gas tied to the catalogue M* (F2)
        M, tail = meff(foot, 10 ** (lm + dMs), Mcold, fhot * 10 ** lm, yk)   # hot gas tied to the catalogue M* (F2)
        tab[gi] = np.log(AQ.delta_sigma(np.exp(LRT) * 1e6, RGRID_PC, M, tail))
    TAB[key] = tab
    return tab


def perlens(tab, idx, h, k):
    """model Delta Sigma (native Msun/pc^2) for lenses idx at all 15 bins of class file k (bilinear in log)."""
    lMn = logM70[idx] + 2 * np.log10(0.70 / h) + 2 * np.log10(qB[idx])
    Rn = R70c[k][idx] * (0.70 / h) * qB[idx][:, None]
    gx = np.clip((lMn - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1.001)
    gy = np.clip((np.log(Rn) - LRT[0]) / (LRT[1] - LRT[0]), 0, len(LRT) - 1.001)
    i0 = gx.astype(int); fx = (gx - i0)[:, None]; j0 = gy.astype(int); fy = gy - j0
    I0 = i0[:, None]
    v = (1 - fx) * ((1 - fy) * tab[I0, j0] + fy * tab[I0, j0 + 1]) + fx * ((1 - fy) * tab[I0 + 1, j0] + fy * tab[I0 + 1, j0 + 1])
    return np.exp(v)


CENTRAL = dict(h=H_NAT["mid"], ye="noclu", fhot=0.5, dcold=0.0, dMs=0.0, red_shift=0.0, blue_shift=0.0, pz=1.0,
               win=W, split="typ", winshift_red=False)


def model_g(foot, k, cfg):
    """stacked v3 g_model (m/s^2, native) for class k; red lenses carry cfg['red_shift'], blue cfg['blue_shift']."""
    memb = MEMB[cfg["split"]][k]; red = MEMB[cfg["split"]]["red"]
    num = np.zeros(15); den = np.zeros(15)
    for sub, sh in ((memb & ~red, cfg["blue_shift"]), (memb & red, cfg["red_shift"])):
        idx = np.where(sub)[0]
        if idx.size == 0: continue
        tab = table(foot, cfg["h"], cfg["ye"], cfg["fhot"], cfg["dcold"], cfg["dMs"] + sh)
        for c0 in range(0, idx.size, 20000):                         # chunks keep the temporaries small (< 1 GB RSS)
            ic = idx[c0:c0 + 20000]; w = WW[ic]
            num += np.sum(w * perlens(tab, ic, cfg["h"], k), axis=0); den += w.sum(0)
    return GCONV * num / den


def cell(foot, k, cfg):
    gb, go, C = data_nat(k, cfg["h"], cfg["pz"])
    gm = model_g(foot, k, cfg)
    sh = (cfg["red_shift"] if k == "red" else 0.0) if cfg.get("winshift_red") else 0.0
    a = gls(go, C, gm, wmask(gb, cfg["win"], sh))
    a["cls"] = cls_amp(a["A"], a["sA"])
    c = gls(go, C, gm, wmask(gb, WC)); a["A_calib"] = c["A"]; a["sA_calib"] = c["sA"]
    a["chi2_15_A1"] = chi2_full(go, C, gm)
    return a


def fmt(a):
    return f"A {a['A']:.3f}+-{a['sA']:.3f} [{a['cls']}]"


# ---- K2: forward model of an isolated point mass is mass-independent at fixed g_bar and equals an independent quadrature
def shape_quad(x):
    """Delta Sigma / (M/r_M^2) at x = R/r_M for the isolated AQUAL point mass: point mass + rho_law (CFG804)."""
    sig = quad(lambda t: 1.0 / (math.pi * math.hypot(x, t) * math.sqrt(1 + 4 * (x * x + t * t))), 0, np.inf, limit=400)[0]
    m3 = (math.sqrt(1 + 4 * x * x) - 1) / 2
    tail = quad(lambda s: 2 * s / math.sqrt(1 + 4 * s * s) * (1 - math.sqrt(max(0.0, 1 - (x / s) ** 2))), x, np.inf, limit=400)[0]
    return 1.0 / (math.pi * x * x) + (m3 + tail) / (math.pi * x * x) - sig


k2s, k2q = 0.0, 0.0
gw = DAT["blue"][0][wmask(DAT["blue"][0], W)]
for foot in FOOTS:
    tab = table(foot, H_NAT["mid"], "zero", 0.0, 0.0, 0.0)
    vals = []
    for gi in range(20, len(LMG) - 20, 15):
        lm = LMG[gi]; lm70 = lm - 2 * math.log10(0.70 / H_NAT["mid"])
        Mpt = 10 ** lm + 10 ** (lm + (-0.69 * lm70 + 6.63))
        Rn = np.sqrt(G_SI * Mpt * MSUN / gw) / MPC
        gy = (np.log(Rn) - LRT[0]) / (LRT[1] - LRT[0]); j0 = gy.astype(int); fy = gy - j0
        # exact mass row (no mass interpolation): value at LMG[gi]
        v = np.exp((1 - fy) * tab[gi, j0] + fy * tab[gi, j0 + 1]) * GCONV
        vals.append(v)
        rM = math.sqrt(Gpc * Mpt / a0u(foot))
        q = np.array([shape_quad(x) for x in Rn * 1e6 / rM]) * Mpt / rM ** 2 * GCONV
        k2q = max(k2q, float(np.max(np.abs(v / q - 1))))
    vals = np.array(vals)
    k2s = max(k2s, float(np.max(vals.max(0) / vals.min(0) - 1)))
check("K2_forward_point_mass", k2s <= 1e-3 and k2q <= 2e-3, f"mass spread {k2s:.1e}; vs quadrature {k2q:.1e}", "<=1e-3, <=2e-3")
P(f"  [{time.time() - T0:.0f} s]")

# ============================================================================ 6. ladder (one ingredient at a time)
LAD = {}
for foot in FOOTS:
    P(f"\n  LADDER [{foot}]  A = data / model in CFG829's window (6 B21 points), GLS, full window covariance")
    L = {}
    L["L0 CFG829 (nu_e, algebraic, B21 distances)"] = {k: dict(K0[f"{foot}|{k}"], cls=cls_amp(K0[f"{foot}|{k}"]["A"], K0[f"{foot}|{k}"]["sA"])) for k in CLS}
    L["L1 kernel nu_1 (algebraic)"] = {}
    L["L2 + native h 0.679, Om 0.3085 (algebraic)"] = {}
    for k in CLS:
        gb, go, C = DAT[k]; a = gls(go, C, gb * nu_1(gb / A0[foot]), wmask(gb, W)); a["cls"] = cls_amp(a["A"], a["sA"])
        L["L1 kernel nu_1 (algebraic)"][k] = a
        gb, go, C = data_nat(k, H_NAT["mid"]); a = gls(go, C, gb * nu_1(gb / A0[foot]), wmask(gb, W)); a["cls"] = cls_amp(a["A"], a["sA"])
        L["L2 + native h 0.679, Om 0.3085 (algebraic)"][k] = a
    steps = [("L3 forward 4G DeltaSigma, isolated AQUAL, B21 baryons", dict(CENTRAL, ye="zero", fhot=0.0)),
             ("L4 + hot CGM 0.5 M* (v3 at y_e = 0)", dict(CENTRAL, ye="zero")),
             ("L5 + EFE primary y_e (T_central)", dict(CENTRAL))]
    for lab, cfg in steps:
        L[lab] = {k: cell(foot, k, cfg) for k in CLS}
    for lab, row in L.items():
        P(f"    {lab:58s} " + "  ".join(f"{k} {fmt(row[k])}" for k in CLS))
    LAD[foot] = L
    P(f"  [{time.time() - T0:.0f} s]")
RES["ladder"] = LAD

# ---- screening L* 24 / 90 pc: l_g = L*^2 / (2 r_M) (M2's definition) vs the smallest window radius
scr = {}
for foot in FOOTS:
    a0 = a0u(foot); h = H_NAT["mid"]
    Mn = Mgal70 * (0.70 / h) ** 2 * qB ** 2
    rM = np.sqrt(Gpc * Mn / a0)                                      # pc
    Rmin = (R70c["all"][:, wmask(DAT["all"][0], W)] * (0.70 / h) * qB[:, None]).min(1) * 1e6   # pc
    for Ls in (24.0, 90.0):
        lg = Ls ** 2 / (2 * rM)
        scr[f"{foot}|{Ls:.0f}"] = dict(lg_max_pc=float(lg.max()), lg_over_Rmin_max=float(np.max(lg / Rmin)))
P("\n  L6 screening L* 24 / 90 pc: l_g = L*^2/(2 r_M) (M2) max " + ", ".join(
    f"{k} {v['lg_max_pc']:.2f} pc (l_g/R_min <= {v['lg_over_Rmin_max']:.1e})" for k, v in scr.items())
  + " -> every lens is unscreened at its window radii; the L6 rows equal L5 by construction.")
RES["screening"] = scr

# ---- lens-weighted median native radius of each window point (T_central inventory), per class
RMEDW = {}
for k in CLS:
    m = MEMB["typ"][k]; wk = wmask(DAT[k][0], W)
    Rn = R70c[k][m] * (0.70 / H_NAT["mid"]) * qB[m][:, None]
    med = []
    for j in np.where(wk)[0]:
        o = np.argsort(Rn[:, j]); cw = np.cumsum(WW[m, j][o]); med.append(float(Rn[o, j][np.searchsorted(cw, 0.5 * cw[-1])] * 1e3))
    RMEDW[k] = med
P("  window points' lens-weighted median R (native kpc): " + "; ".join(f"{k} {np.round(v, 0).tolist()}" for k, v in RMEDW.items()))
RES["window_median_R_kpc"] = RMEDW

# ============================================================================ 7. cells for the verdicts: readings x y_e x brackets
READ = {"R0": 0.0, "R1": S667, "R2": S667 + D_RED}
YK = ("zero", "noclu", "maxclu")
BRK = {"central": {}, "f_hot 0": dict(fhot=0.0), "f_hot 1.0": dict(fhot=1.0), "f_cold -0.2": dict(dcold=-0.2),
       "f_cold +0.2": dict(dcold=0.2), "M* -0.2 (E1)": dict(dMs=-0.2), "M* +0.2": dict(dMs=0.2),
       "h 0.672": dict(h=H_NAT["lo"]), "h 0.686": dict(h=H_NAT["hi"]), "Sigma_crit -3%": dict(pz=0.97),
       "Sigma_crit +3%": dict(pz=1.03), "window -0.3 dex": dict(win=(W[0] / 2, W[1] / 2)),
       "window +0.3 dex": dict(win=(W[0] * 2, W[1] * 2))}
CELLS = {}
for foot in FOOTS:
    CELLS[foot] = {}
    for bname, bcfg in BRK.items():
        for yk in YK:
            # blue and all at R0; red at R0 / R1 / R2; all also under R2 (red lenses shifted) for tile 31
            base = dict(CENTRAL, **bcfg, ye=yk)
            CELLS[foot][(bname, "R0", yk, "blue")] = cell(foot, "blue", base)
            CELLS[foot][(bname, "R0", yk, "all")] = cell(foot, "all", base)
            for rd, sh in READ.items():
                CELLS[foot][(bname, rd, yk, "red")] = cell(foot, "red", dict(base, red_shift=sh))
            CELLS[foot][(bname, "R2", yk, "all")] = cell(foot, "all", dict(base, red_shift=READ["R2"]))
    P(f"  [{time.time() - T0:.0f} s] cells [{foot}] done ({len(TAB)} tables)")

# K6: EFE monotonicity at central inputs
mono = True
for foot in FOOTS:
    for (b, rd, yk, k) in CELLS[foot]:
        if b != "central" or yk != "zero": continue
        a = [CELLS[foot][(b, rd, y, k)]["A"] for y in YK]
        mono &= a[0] <= a[1] + 1e-9 and a[1] <= a[2] + 1e-9
check("K6_EFE_monotonic", mono, "A(0) <= A(noclu) <= A(maxclu) for every class/reading/footing", "monotone")
# POST-RESULT diagnostic (AMENDMENT A1; reported only): size of the departure from monotonicity, and why
dip = []
for foot in FOOTS:
    for (b, rd, yk, k) in CELLS[foot]:
        if b != "central" or yk != "zero": continue
        a = [CELLS[foot][(b, rd, y, k)] for y in YK]
        for i in range(2):
            if a[i + 1]["A"] < a[i]["A"]:
                dip.append(dict(foot=foot, reading=rd, cls=k, step=f"{YK[i]}->{YK[i + 1]}", dA=a[i + 1]["A"] - a[i]["A"],
                                in_sigma=(a[i + 1]["A"] - a[i]["A"]) / a[i]["sA"]))
P(f"  A1 (post-result) K6 departures: {len(dip)}; largest |dA| {max([abs(d['dA']) for d in dip], default=0):.4f} = "
  f"{max([abs(d['in_sigma']) for d in dip], default=0):.3f} sigma_A; " + "; ".join(f"{d['foot']} {d['cls']} {d['reading']} {d['step']} {d['dA']:+.4f}" for d in dip))
dsr = {}
for f in FOOTS:
    for kk in ("noclu", "maxclu"):
        s = SOL[(f, kk)]; xs = np.array([5.0, 10.0, 15.0, 20.0, 30.0, 40.0])
        dsr[f"{f}|{kk}"] = dict(zip(xs.tolist(), (AQ.delta_sigma(xs, s["r"], s["M"], "const") /
                                                   AQ.delta_sigma(xs, s["r"], AQ.M_iso(s["r"]), "linear")).tolist()))
P("  A1 (post-result) point-mass Delta Sigma(EFE) / Delta Sigma(isolated) at R/r_M = 5, 10, 15, 20, 30, 40: " +
  "; ".join(f"{k} " + ", ".join(f"{v:.4f}" for v in d.values()) for k, d in dsr.items()))
RES["A1_K6_departures"] = dip; RES["A1_DS_ratio_point_mass"] = dsr

P("\n  CENTRAL CELLS (A = data / v3; y_e 0 / primary noclu / maxclu)")
for foot in FOOTS:
    for (k, rd) in (("blue", "R0"), ("red", "R0"), ("red", "R1"), ("red", "R2"), ("all", "R0"), ("all", "R2")):
        P(f"    [{foot}] {k:4s} {rd}: " + "   ".join(f"y_e {yk}: {fmt(CELLS[foot][('central', rd, yk, k)])}" for yk in YK))
    for yk in YK:
        for rd in ("R0", "R2"):
            r_, b_ = CELLS[foot][("central", rd, yk, "red")], CELLS[foot][("central", "R0", yk, "blue")]
            z = (r_["A"] - b_["A"]) / math.hypot(r_["sA"], b_["sA"])
            CELLS[foot][("split", rd, yk)] = z
        P(f"    [{foot}] red - blue split z, y_e {yk}: R0 {CELLS[foot][('split', 'R0', yk)]:+.2f}  R2 {CELLS[foot][('split', 'R2', yk)]:+.2f}")
    for yk in YK:
        a = CELLS[foot][("central", "R0", yk, "blue")]
        P(f"    [{foot}] blue y_e {yk}: calibration window [1e-11.9, 1e-10.9) A {a['A_calib']:.3f}+-{a['sA_calib']:.3f}; "
          f"chi2(15 pts, A = 1) {a['chi2_15_A1']:.1f}")

# ============================================================================ 8. verdicts (criteria Sec. 4)
ORDER = ["PASS", "CONDITIONAL", "NOT DECIDABLE", "FAIL"]


def verdict(foot, k, readings, bname="central"):
    c = lambda rd, yk: CELLS[foot][(bname, rd, yk, k)]["cls"]
    S = [(rd, yk) for rd in readings for yk in YK if c(rd, yk) == "consistent"]
    if ("R0", "zero") in S and ("R0", "noclu") in S:
        return "PASS", S, [("R0", "zero"), ("R0", "noclu")]
    if k == "blue":
        if c("R0", "zero") == "short": return "FAIL", S, [("R0", "zero")]
        if c("R0", "maxclu") == "over": return "FAIL", S, [("R0", "maxclu")]
        return ("CONDITIONAL", S, S) if S else ("NOT DECIDABLE", S, [])
    if S:
        return "CONDITIONAL", S, S
    dec = []
    for rd in readings:
        if c(rd, "zero") == "short": dec.append((rd, "zero"))
        elif c(rd, "maxclu") == "over": dec.append((rd, "maxclu"))
        else: return "NOT DECIDABLE", S, []
    return "FAIL", S, dec


VER = {}
P("\n  VERDICTS (per footing; robustness = deciding cells keep their class under every bracket)")
for tile, k, readings in (("tile17_blue", "blue", ("R0",)), ("tile30_red", "red", ("R0", "R1", "R2"))):
    VER[tile] = {}
    for foot in FOOTS:
        v, S, dec = verdict(foot, k, readings)
        frag = []
        for bname in BRK:
            if bname == "central": continue
            for (rd, yk) in dec:
                if CELLS[foot][(bname, rd, yk, k)]["cls"] != CELLS[foot][("central", rd, yk, k)]["cls"]:
                    frag.append(f"{bname} ({rd}, y_e {yk}: {CELLS[foot][(bname, rd, yk, k)]['cls']})")
        under = {bname: verdict(foot, k, readings, bname)[0] for bname in BRK if bname != "central"}
        tag = "n/a" if not dec else ("ROBUST" if not frag else "FRAGILE")
        extra = ""
        if tile == "tile30_red":
            extra = f"; old COND survives (R2 at y_e 0 and primary consistent): {('R2', 'zero') in S and ('R2', 'noclu') in S}"
        VER[tile][foot] = dict(verdict=v, consistent_cells=S, deciding=dec, robustness=tag, fragile=frag, verdict_under_brackets=under)
        P(f"    {tile} [{foot}]: {v} ({tag}); consistent cells {S}{extra}")
        if frag: P(f"        fragile under: {'; '.join(frag)}")
        P(f"        verdict under each bracket: " + ", ".join(f"{b}: {x}" for b, x in under.items()))
    vs = [VER[tile][f]["verdict"] for f in FOOTS]
    VER[tile]["board"] = max(vs, key=ORDER.index)
    VER[tile]["split"] = vs[0] != vs[1]
    P(f"    {tile} BOARD VERDICT (less favourable footing): {VER[tile]['board']}" + (f"  (footing split: canonical {vs[0]}, alt {vs[1]})" if vs[0] != vs[1] else "")
      + "  [before R6: mu_K^2 term not included]")
RES["verdicts"] = VER

# ============================================================================ 9. reported only (no verdict weight)
P("\n  REPORTED ONLY")
REP = {}
for foot in FOOTS:
    # colour split u-r 2.5 (variant) at central inputs
    for yk in YK:
        for k in ("blue", "red"):
            a = cell(foot, k, dict(CENTRAL, ye=yk, split="ur25"))
            REP[f"{foot}|ur25|{k}|R0|{yk}"] = a
        P(f"    [{foot}] u-r 2.5 split, y_e {yk}: blue {fmt(REP[f'{foot}|ur25|blue|R0|{yk}'])}  red R0 {fmt(REP[f'{foot}|ur25|red|R0|{yk}'])}")
    # R2 with CFG850's window convention (labels x 10^shift) and R5-blue (IMF on blue stars too)
    for yk in YK:
        a = cell(foot, "red", dict(CENTRAL, ye=yk, red_shift=READ["R2"], winshift_red=True)); REP[f"{foot}|R2_win850|{yk}"] = a
        b = cell(foot, "blue", dict(CENTRAL, ye=yk, blue_shift=D_BLUE)); REP[f"{foot}|R5blue|{yk}"] = b
        P(f"    [{foot}] y_e {yk}: red R2 with CFG850 window convention {fmt(a)};  R5-blue (IMF on blue, +{D_BLUE:.3f}) blue {fmt(b)}")
    # external-field scan
    scan = {}
    for ye in (1e-6, 1e-5, 3e-5, 1e-4, 3e-4):
        kk = f"scan{ye:g}"
        SOL[(foot, kk)] = AQ.solve_efe(ye, maxit=200)
        scan[f"{ye:g}"] = {"blue": cell(foot, "blue", dict(CENTRAL, ye=kk)), "red_R0": cell(foot, "red", dict(CENTRAL, ye=kk)),
                           "red_R2": cell(foot, "red", dict(CENTRAL, ye=kk, red_shift=READ["R2"]))}
        P(f"    [{foot}] y_e scan {ye:7.0e}: blue {fmt(scan[f'{ye:g}']['blue'])}  red R0 {fmt(scan[f'{ye:g}']['red_R0'])}  red R2 {fmt(scan[f'{ye:g}']['red_R2'])}")
    grid = [("0", CELLS[foot][("central", "R0", "zero", "blue")]["cls"])] + [(y, scan[y]["blue"]["cls"]) for y in scan] + \
        [(f"noclu {YE[foot]['noclu']:.1e}", CELLS[foot][("central", "R0", "noclu", "blue")]["cls"]),
         (f"maxclu {YE[foot]['maxclu']:.1e}", CELLS[foot][("central", "R0", "maxclu", "blue")]["cls"])]
    P(f"    [{foot}] blue class along y_e: " + ", ".join(f"{y}: {c}" for y, c in grid))
    REP[f"{foot}|ye_scan"] = scan
# F2's ESD-space inner amplitude (all lenses, R <= 0.31 Mpc), read from F2's committed JSON
f2in = {}
for foot in FOOTS:
    t = J2["trackA"][foot]
    f2in[foot] = {lab: (t[key]["A_in"], t[key]["sA_in"]) for lab, key in
                  (("y_e 0", "L4_plus_hotCGM"), ("noclu", "L5_plus_EFE_noclu=T_central"), ("maxclu", "OAT EFE y_e = maxclu"))}
    P(f"    [{foot}] F2 ESD-space A_in (all lenses, 4 mass bins, R <= 0.31 Mpc; F2 JSON): " +
      ", ".join(f"{k} {a:.3f}+-{s:.3f} [{cls_amp(a, s)}]" for k, (a, s) in f2in[foot].items()))
REP["F2_A_in"] = f2in
# P2 lane outputs (spectroscopic outer test), if committed
p2 = {d: sorted(os.listdir(os.path.join(REPO, "rebuild_2026_10_22", d)))
      for d in os.listdir(os.path.join(REPO, "rebuild_2026_10_22")) if d.startswith("P2")}
p2res = {d: [x for x in fl if x.endswith(".json") or x == "README.md"] for d, fl in p2.items()}
REP["P2_lane_files"] = p2
P(f"    P2 lane: {p2 if p2 else 'absent'}; result files {p2res if any(p2res.values()) else 'none yet (criteria only; nothing to read)'}")
RES["reported"] = REP
RES["cells_central"] = {f"{foot}|{rd}|{yk}|{k}": CELLS[foot][("central", rd, yk, k)]
                        for foot in FOOTS for (b, rd, yk, k) in [key for key in CELLS[foot] if len(key) == 4 and key[0] == "central"]}
RES["cells_brackets"] = {f"{foot}|{b}|{rd}|{yk}|{k}": dict(A=v["A"], sA=v["sA"], cls=v["cls"])
                         for foot in FOOTS for (key, v) in CELLS[foot].items() if len(key) == 4 for (b, rd, yk, k) in [key]}
RES["splits"] = {f"{foot}|{rd}|{yk}": CELLS[foot][("split", rd, yk)] for foot in FOOTS for rd in ("R0", "R2") for yk in YK}
RES["readings"] = dict(READ, D_red=D_RED, D_blue=D_BLUE)
RES["n_tables"] = len(TAB)
finish()
