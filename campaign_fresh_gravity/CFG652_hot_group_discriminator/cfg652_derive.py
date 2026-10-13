#!/usr/bin/env python3
"""CFG652 part 1 (theory + forecast; no lensing data touched): DeltaSigma(R) of hot-gas groups under (a) Theory v2 (phantom from
CONDENSED baryons, per-host supply, rest collisionless via the CFG637 Method A infall) vs (b) candidate B (phantom from ALL
baryons, same everything else), both footings, never pooled.
  G  grid: M_b(<R_X) = M_cond + M_hot in {10^12.5, 13, 13.5, 14}, f_hot = M_hot/M_b in {0, 0.3, 0.6, 0.8, 0.9}, z = 0.3.
  K  brackets on the representative eFEDS-like system (M_b 10^13.3, f_hot 0.8): q 0.05 / 0.2, eps 0.5, uniform draw,
     N 1600, f_BCG 0.3 / 0.8, member R_e 0.25 / 1.0 R_X, gas to 1 / 4 R_X, catchment rule P2 / XCOP.
  M  MUTATE M1: (a) with the hot gas relabelled condensed must reproduce (b) (max |dlog DeltaSigma| < 0.01).
  F  forecast: stacked-lensing noise (declared KiDS-like source density) -> number of groups for 3 sigma between (a) and (b).
R_X(M_hot) is the on-disk Lovisari+2015 scaling (log R500 vs log Mgas500, least squares), used only to place the gas.
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG652_hot_group_discriminator/cfg652_derive.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
try:
    os.nice(10)
except OSError:
    pass
import cfg652_model as M  # noqa: E402

T0 = time.time(); LOG = []; RES = {"lane": "CFG652", "script": "cfg652_derive"}
QUICK = os.environ.get("CFG652_QUICK") == "1"


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


P(__doc__.split("Run from")[0].strip())
# ------------------------------------------------------------------ R_X(M_hot) from the on-disk Lovisari table
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv"))
        if not l.startswith("#") and l.strip()]
H = {h: i for i, h in enumerate(rows[0])}
lov = [(float(r[H["Mgas500_1e12"]]) * 1e12, float(r[H["R500_kpc"]])) for r in rows[1:] if r[H["R500_kpc"]].strip()
       and r[H["Mgas500_1e12"]].strip() and r[0] and r[0][0] != "-"]
lm = np.log10([x[0] for x in lov]); lr = np.log10([x[1] for x in lov])
SL, IC = np.polyfit(lm, lr, 1)
RX = lambda Mh: 10 ** (IC + SL * math.log10(max(Mh, 1e10)))
P(f"\n  R_X(M_hot): log R = {IC:.3f} + {SL:.3f} log M_hot  (Lovisari N = {len(lov)}); R_X(2e12) = {RX(2e12):.0f} kpc")
RES["RX_fit"] = dict(intercept=IC, slope=SL, N=len(lov))

RB = np.geomspace(30, 3000, 13)                  # bin edges (kpc, physical)
RC = np.sqrt(RB[1:] * RB[:-1])
IN = (RC >= 50) & (RC <= 200); OUT = (RC >= 400) & (RC <= 1500)
BAND = (RC >= 250) & (RC <= 1000)          # outer band beyond the members (primary discriminator, see README)
FOOTS = ("canonical", "alt")


def ds_of(o):
    return M.delta_sigma(o["rg"], o["Mbound"], RC, rmax=o["rta"])


def shape(ds):
    return float(np.log10(np.mean(ds[IN]) / np.mean(ds[OUT])))


def aout(ds):
    return float(np.log10(np.mean(ds[BAND])))


def run(Mb, fh, foot, model, **kw):
    Mh = fh * Mb; Mc = Mb - Mh
    Rx = RX(Mh if Mh > 0 else 0.1 * Mb)
    o = M.system(Mc, Mh, Rx, kw.pop("z", 0.3), foot, model, N=kw.pop("N", 800), **kw)
    return o, ds_of(o)


# ------------------------------------------------------------------ G grid
P("\n== G: grid (z = 0.3). DeltaSigma in Msun/pc^2 at bin centres (kpc): " + " ".join(f"{x:.0f}" for x in RC))
P("   S = log10[<DS>(50-200 kpc) / <DS>(400-1500 kpc)]; ratio = DS_a / DS_b per bin")
GR = {}
LMB = (12.5, 13.0, 13.5, 14.0) if not QUICK else (13.0,)
FH = (0.0, 0.3, 0.6, 0.8, 0.9) if not QUICK else (0.0, 0.8)
for foot in FOOTS:
    for lmb in LMB:
        for fh in FH:
            cell = {}
            for model in "ab":
                o, ds = run(10 ** lmb, fh, foot, model)
                cell[model] = dict(ds=ds.tolist(), S=shape(ds), rta=o["rta"], x_edge=o["x_edge"], res_frac=o["res_frac"],
                                   settled_frac=o["settled_frac"], fret=o["fret"], supply=o["supply"])
            rat = np.array(cell["a"]["ds"]) / np.array(cell["b"]["ds"])
            cell["ratio"] = rat.tolist(); cell["dS"] = cell["a"]["S"] - cell["b"]["S"]
            cell["dA"] = aout(np.array(cell["a"]["ds"])) - aout(np.array(cell["b"]["ds"]))
            GR[f"{foot}|{lmb}|{fh}"] = cell
            P(f"  [{foot[:3]}] logMb {lmb:4.1f} f_hot {fh:.1f}: dA_out(250-1000) {cell['dA']:+.3f}; S_a {cell['a']['S']:+.2f} S_b {cell['b']['S']:+.2f} dS {cell['dS']:+.2f};"
              f" res a/b {cell['a']['res_frac']:.2f}/{cell['b']['res_frac']:.2f}; edge a/b "
              f"{cell['a']['x_edge'] if cell['a']['x_edge'] is None else round(cell['a']['x_edge'], 2)}/"
              f"{cell['b']['x_edge'] if cell['b']['x_edge'] is None else round(cell['b']['x_edge'], 2)} r_ta;"
              f" ratio a/b " + " ".join(f"{x:.2f}" for x in rat))
    P(f"  ({time.time() - T0:.0f} s)")
RES["grid"] = GR
RES["R_centres_kpc"] = RC.tolist(); RES["R_edges_kpc"] = RB.tolist()

# ------------------------------------------------------------------ K brackets
P("\n== K: brackets on the representative system (M_b 10^13.3, f_hot 0.8, z 0.3)")
BRK = {"P": {}, "q0.05": dict(q=0.05), "q0.2": dict(q=0.2), "eps0.5": dict(eps=0.5), "uniform": dict(draw_mode="uniform"),
       "N1600": dict(N=1600), "fBCG0.3": dict(f_bcg=0.3), "fBCG0.8": dict(f_bcg=0.8), "sat0.25": dict(re_sat_frac=0.25),
       "sat1.0": dict(re_sat_frac=1.0), "gas1RX": dict(gas_trunc=1.0), "gas4RX": dict(gas_trunc=4.0),
       "ruleP2": dict(rule="P2"), "ruleXCOP": dict(rule="XCOP")}
if QUICK:
    BRK = {k: BRK[k] for k in ("P", "q0.2")}
KB = {}
for foot in FOOTS:
    for bk, kw in BRK.items():
        cell = {}
        for model in "ab":
            o, ds = run(10 ** 13.3, 0.8, foot, model, **dict(kw))
            cell[model] = dict(ds=ds.tolist(), S=shape(ds), res_frac=o["res_frac"])
        cell["dS"] = cell["a"]["S"] - cell["b"]["S"]
        cell["dA"] = aout(np.array(cell["a"]["ds"])) - aout(np.array(cell["b"]["ds"]))
        cell["ratio"] = (np.array(cell["a"]["ds"]) / np.array(cell["b"]["ds"])).tolist()
        KB[f"{foot}|{bk}"] = cell
        P(f"  [{foot[:3]}] {bk:9s}: dA_out {cell['dA']:+.3f}; S_a {cell['a']['S']:+.2f} S_b {cell['b']['S']:+.2f} dS {cell['dS']:+.2f};"
          f" res_a {cell['a']['res_frac']:.2f}; ratio a/b " + " ".join(f"{x:.2f}" for x in cell["ratio"]))
RES["brackets"] = KB
dSall = [v["dS"] for v in KB.values()]; dAall = [v["dA"] for v in KB.values()]
P(f"  dS over all brackets and both footings: min {min(dSall):+.2f}, max {max(dSall):+.2f}")
P(f"  dA_out over all brackets and both footings: min {min(dAall):+.3f}, max {max(dAall):+.3f}")
RES["bracket_range"] = dict(dS=[min(dSall), max(dSall)], dA_out=[min(dAall), max(dAall)])

# ------------------------------------------------------------------ C fixed condensed mass, rising hot gas (the sharp contrast)
P("\n== C: fixed M_cond = 2e12, M_hot = 0, 2e12, 8e12, 1.8e13 (z 0.3): outer-band amplitude A_out = log10 <DS>(250-1000 kpc)")
CC = {}
for foot in FOOTS:
    for model in "ab":
        row = []
        for Mh in ((0.0, 2e12, 8e12, 1.8e13) if not QUICK else (0.0, 8e12)):
            Mb = 2e12 + Mh
            o, ds = run(Mb, Mh / Mb, foot, model)
            row.append(dict(Mhot=Mh, A=aout(ds), ds=ds.tolist(), res_frac=o["res_frac"]))
        x = np.log10([2e12 + r["Mhot"] for r in row]); y = np.array([r["A"] for r in row])
        slope = float(np.polyfit(x, y, 1)[0])
        CC[f"{foot}|{model}"] = dict(rows=row, slope_dA_dlogMb=slope)
        P(f"  [{foot[:3]}] ({model}) A_out: " + " ".join(f"{r['A']:.3f}" for r in row) + f"; d A_out / d log M_b = {slope:+.3f}")
RES["fixed_cond"] = CC

# ------------------------------------------------------------------ M MUTATE M1
P("\n== M: MUTATE M1 (hot gas relabelled condensed in (a) must reproduce (b))")
MU = {}
for foot in FOOTS:
    Mb, fh = 10 ** 13.3, 0.8; Mh = fh * Mb
    oa = M.system(Mb - Mh, Mh, RX(Mh), 0.3, foot, "a", N=800, hot_as_condensed=True)
    ob = M.system(Mb - Mh, Mh, RX(Mh), 0.3, foot, "b", N=800)
    d = float(np.max(np.abs(np.log10(ds_of(oa) / ds_of(ob)))))
    MU[foot] = dict(max_dlog=d, ok=d < 0.01)
    P(f"  [{foot[:3]}] max |dlog DS| = {d:.2e} -> {'PASS' if d < 0.01 else 'FAIL'}")
RES["mutate_M1"] = MU

# ------------------------------------------------------------------ F forecast
P("\n== F: forecast (declared noise model; no data): sigma(DS_bin) = Sigma_crit sigma_e / sqrt(n_eff A_bin N_groups)")
NEFF, SIGE, SCRIT, ZL = 4.0, 0.27, 3300.0, 0.3     # background sources/arcmin^2 after z_B > z_l + 0.2, per-component, Msun/pc^2
DA = ZL * 299792.458 / 70 / (1 + ZL) / 1.1 * 1000.0    # rough angular-diameter distance (kpc) at z 0.3 for arcmin conversion
kpc_per_arcmin = DA * math.pi / 180 / 60
Abin = math.pi * (RB[1:] ** 2 - RB[:-1] ** 2) / kpc_per_arcmin ** 2
sig1 = SCRIT * SIGE / np.sqrt(NEFF * Abin)
P(f"  n_eff {NEFF}/arcmin^2, sigma_e {SIGE}, Sigma_crit {SCRIT:.0f}, {kpc_per_arcmin:.0f} kpc/arcmin; per-group sigma(DS) bins: "
  + " ".join(f"{x:.0f}" for x in sig1))
FC = {}
for foot in FOOTS:
    for lmb in (13.0, 13.5):
        for fh in (0.6, 0.8, 0.9):
            c = GR.get(f"{foot}|{lmb}|{fh}")
            if c is None:
                continue
            da, db = np.array(c["a"]["ds"]), np.array(c["b"]["ds"])
            use = (RC >= 50) & (RC <= 1000)
            chi1 = float(np.sum(((da - db) / sig1)[use] ** 2))      # per group, shape noise only
            N3 = 9.0 / chi1
            FC[f"{foot}|{lmb}|{fh}"] = dict(dchi2_per_group=chi1, N_3sigma=N3)
            P(f"  [{foot[:3]}] logMb {lmb} f_hot {fh}: dchi2/group {chi1:.3f} -> N(3 sigma, shape noise only) = {N3:.1f};"
              f" x4 for LSS / miscentring / photo-z allowance = {4 * N3:.0f}")
RES["forecast"] = dict(neff=NEFF, sige=SIGE, scrit=SCRIT, cells=FC)

RES["runtime_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "cfg652_derive_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg652_derive.out"), "w").write("\n".join(LOG) + "\n")
P(f"\n  done in {time.time() - T0:.0f} s")
