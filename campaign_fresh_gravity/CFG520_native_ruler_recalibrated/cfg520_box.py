#!/usr/bin/env python3
"""CFG520 per-box pass (FROZEN_CRITERIA.md sections 0-4, 6; criteria commit 6d184c37d). CFG506's cfg506_box.py, copied, with:
  - the halo catalogue read from CFG506's per-box file (same finder output; count checked), diagnostics D1-D3 dropped;
  - the satellite occupation from cfg520_lib (B, alpha); rules: R0 (B = 17, alpha = 1: CFG506), MAIN (calibrated), M2X (MUTATE, 2x target);
  - two stages: 'sel' (galaxies, lenses, isolation, companion / weight tables; all rules in ONE particle load; R0a check against CFG506)
    and 'ds' (CFG506 sections 2 and 5: lensing source, DeltaSigma stacks; for one rule; G0 check that the galaxies are regenerated identically).
  - no wait-for-other-512^3-jobs loop (another lane's PM job runs concurrently by design); instead a memory guard: wait until >= 14 GB are
    available before loading, and stop if this process's peak RSS exceeds 12.5 GB.
Usage: nice -n 10 python3 -u cfg520_box.py KEY sel        |   nice -n 10 python3 -u cfg520_box.py KEY ds RULE
Writes ../../../_external_data/cfg520_work/cfg520_{sel,box}_<RULE>_<KEY>.npz and updates cfg520_box_results.json / cfg520_box.out here.
"""
import os, sys
os.environ.setdefault("CFG424_THREADS", "2")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = os.environ["CFG424_THREADS"]
import json, math, time, subprocess, importlib.util, resource
import numpy as np
from scipy import fft as sfft
from scipy.spatial import cKDTree
from scipy.special import j1
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg520_lib as LBR  # noqa: E402
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg520_work"); os.makedirs(WORK, exist_ok=True)
W506 = os.path.join(EXT, "cfg506_work")
W424 = "cfg424_work/cfg424_RES_TA_MIXA_MASSCONS_fret1_"
BOXES = {  # CFG506's 512^3 boxes
    "TA512_can359": (W424 + "FLAT_canonical_N512", "TA", "FLAT", "canonical", 512),
    "TA512_can360": (W424 + "FLAT_canonical_N512_seed360", "TA", "FLAT", "canonical", 512),
    "TA512_alt359": (W424 + "FLAT_alt_N512", "TA", "FLAT", "alt", 512),
    "TA512_DEcan359": (W424 + "DE_canonical_N512", "TA", "DE", "canonical", 512),
    "S0512_359": ("cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512", "S0", "FLAT", "canonical", 512),
    "S0512_360": ("cfg424_work/cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360", "S0", "FLAT", "canonical", 512),
}
KEY, STAGE = sys.argv[1], sys.argv[2]
RULE_DS = sys.argv[3] if STAGE == "ds" else None
BASE, KIND, BRANCH, FOOT, N = BOXES[KEY]
T0 = time.time()
LOG = []
CHK = {}
TAGK = f"{STAGE}{'_' + RULE_DS if RULE_DS else ''}|{KEY}"


def say(s):
    s = f"[{KEY} {STAGE}{' ' + RULE_DS if RULE_DS else ''} {time.time() - T0:7.1f}s] {s}"; print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9         # bytes on macOS


def avail_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    pg = 16384; n = 0
    for line in out.splitlines():
        if line.startswith(("Pages free", "Pages inactive", "Pages speculative", "Pages purgeable")):
            n += int(line.split(":")[1].strip().rstrip("."))
    return n * pg / 1e9


PEAK = {}


def guard(step):
    r = rss_gb(); PEAK[step] = round(r, 2)
    say(f"  memory: peak RSS so far {r:.2f} GB after '{step}'")
    if r > 12.5:
        say(f"STOP: peak RSS {r:.2f} GB > 12.5 GB (frozen compute rule)"); write_results(); sys.exit(3)


RESF = os.path.join(HERE, "cfg520_box_results.json")
OUT = dict(key=KEY, stage=STAGE, rule=RULE_DS, base=BASE.split("/")[-1], kind=KIND, branch=BRANCH, foot=FOOT, N=N)


def write_results():
    OUT["checks"] = CHK; OUT["peak_rss_gb"] = PEAK; OUT["elapsed_s"] = round(time.time() - T0, 1); OUT["log"] = LOG
    allres = json.load(open(RESF)) if os.path.exists(RESF) else {}
    allres[TAGK] = OUT
    json.dump(allres, open(RESF, "w"), indent=1)
    with open(os.path.join(HERE, "cfg520_box.out"), "w") as f:
        for k in sorted(allres):
            f.write("\n".join(allres[k]["log"]) + "\n\n")


while True:
    a = avail_gb()
    if a >= 14.0:
        break
    say(f"waiting: {a:.1f} GB available (< 14)"); time.sleep(60)

# ---------------------------------------------------------------- rules
CAL = json.load(open(os.path.join(HERE, "cfg520_calib_results.json")))
RULES = {"R0": (17.0, 1.0)}
if CAL["rule"]["cal_ok"]:
    RULES["MAIN"] = (float(CAL["rule"]["B"]), float(CAL["rule"]["alpha"]))
fm = os.path.join(HERE, "cfg520_calib_results_MUTATE.json")
if os.path.exists(fm):
    CM = json.load(open(fm)); RULES["M2X"] = (float(CM["rule"]["B"]), float(CM["rule"]["alpha"]))
OUT["rules"] = RULES

# ---------------------------------------------------------------- engine (read-only), as CFG506
spec = importlib.util.spec_from_file_location("eng424", os.path.join(LANES, "CFG424_turnaround_catchment", "cfg424_pm.py"))
eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
eng.RC = 0.0; eng.MIX = "MIXA"
Om, FB, L = eng.Om, eng.FB, eng.L
h = 0.6736
RHOM_H = Om * 2.77536627e11
J = json.load(open(os.path.join(EXT, BASE + ".json")))
assert int(J["mesh"]) == N and abs(float(J["L"]) - L) < 1e-9
DTA = float(J["snap"]["z0"]["Delta_ta"])
mesh = eng.Mesh(N); dx = mesh.dx
A = 1.0
say(f"{BASE.split('/')[-1]}: kind {KIND}, branch {BRANCH}, foot {FOOT}, N {N}, dx {dx:.4f} Mpc/h; rules {RULES}")


def sources(delta):
    """CFG506's copy (via CFG495) of the engine's RES / RC = 0 branch at a = 1."""
    a = A
    dk = mesh.fwd(delta)
    phik = (-1.5 * Om / a) * dk * mesh.ik2
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [mesh.inv(mesh.kvec[i] * mesh.kvec[j] * dk * mesh.ik2) for i, j in tk]
    _, l2, _ = eng.eig3(t); del t, dk
    tau = (DTA - 1.0) / 3.0
    fsw = np.clip(0.5 + (l2 - tau) / (2 * eng.EPS), 0, 1).astype(np.float32); del l2
    edge = eng.in_cover(mesh, delta, DTA, None, a, BRANCH, FOOT)
    catch = eng.in_cover(mesh, delta, DTA, 1.0, a, BRANCH, FOOT)
    fsw *= edge.astype(np.float32)
    fc, fh, fs = eng.MIXES["MIXA"]; kk = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    kJ = lambda T: math.sqrt(1.5 * Om / a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    Wk = (fc / (1.0 + kk / kJ(1e4) ** 2) + fh / (1.0 + kk / kJ(1e6) ** 2) + fs).astype(np.float32); del kk
    gb = [FB * (-mesh.inv(1j * kv * phik * Wk)) for kv in mesh.kvec]; del Wk, phik
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * eng.a0_code(a, BRANCH, FOOT))
    w = (eng.nu_mono(y) - 1.0).astype(np.float32); del y
    divk = sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb)); del gb, w
    s_ph = -mesh.inv(divk); del divk
    s_c = ((1.5 * Om * (1.0 - FB) / a) * (1.0 + delta)).astype(np.float32)
    e = (fsw * np.maximum(s_ph - s_c, 0.0) * catch).astype(np.float32); del s_ph
    r, nc = eng.catch_labels(catch); mm = r >= 0
    E_ = np.bincount(r[mm], weights=e.ravel()[mm].astype(np.float64), minlength=nc)
    C_ = np.bincount(r[mm], weights=s_c.ravel()[mm].astype(np.float64), minlength=nc)
    q = E_ / np.maximum(C_, 1e-30)
    comp = np.zeros(e.size, np.float32); comp[mm] = (s_c.ravel()[mm] * q[r[mm]]).astype(np.float32); comp = comp.reshape(e.shape)
    info = dict(q_max=float(q.max()) if nc else 0.0, src_sum=float((e - comp).sum(dtype=np.float64)), e_sum=float(e.sum(dtype=np.float64)),
                n_catch=int(nc))
    return e, comp, info


# ================================================================= particles (+ lensing source in stage ds)
pos32 = np.load(os.path.join(EXT, BASE + "_z0.npz"))["pos"]
NP = len(pos32); MP = RHOM_H * L ** 3 / NP
say(f"loaded {NP:,} particles, m_p {MP:.4e} Msun/h")
guard("load")
SRC = None
if STAGE == "ds" and KIND == "TA":
    delta = mesh.deposit(pos32)
    e, comp, info = sources(delta); del delta
    js = J["snap"]["z0"]
    dq = abs(info["q_max"] / js["q_max"] - 1)
    check("K1 engine q_max reproduced (1e-4 rel)", dq < 1e-4, f"q_max {info['q_max']:.6f} vs run JSON {js['q_max']:.6f} (rel {dq:.1e})")
    check("K2 per-catchment conservation |sum S| / sum e < 1e-3", abs(info["src_sum"]) < 1e-3 * info["e_sum"],
          f"sum S {info['src_sum']:.3e}, sum e {info['e_sum']:.3e}")
    OUT["source_info"] = info
    SRC = ((e - comp) / (1.5 * Om)).astype(np.float32); del e, comp
    guard("sources")
pos = pos32.astype(np.float64) % L
del pos32
tree = cKDTree(pos, boxsize=L, leafsize=32, balanced_tree=False, compact_nodes=False)
guard("tree")

# ================================================================= halo catalogue (CFG506's, same finder output)
C6 = np.load(os.path.join(W506, f"cfg506_box_{KEY}.npz"))
cen = C6["cen"].astype(np.float64); Mta, rta, M200m, r200m = C6["Mta"], C6["rta"], C6["M200m"], C6["r200m"]
J506 = json.load(open(os.path.join(LANES, "CFG506_native_environment", "cfg506_box_results.json")))[KEY]
check("catalogue = CFG506's (halo count)", len(cen) == J506["n_halos"], f"{len(cen)} vs {J506['n_halos']}")
# CFG506 stored cen as float32; its finder used float64 centres. Satellites are placed on particles (not on cen), but lens centrals use cen:
# R0a below tells whether the float32 round-trip matters at the frozen 1e-9 tolerance (CFG506 snaps lenses to the 0.049 Mpc/h fine grid).
lM = np.log10(Mta)

# ================================================================= selection machinery (CFG506 section 4, copied)
LH = 0.6736
V = L ** 3
S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
ZN = np.array([0.15, 0.25, 0.35, 0.45])
DEh = S["DE"]; Hin, Han = S["H_in"], S["H_an"]
KER = []
for n in range(4):
    ex = (Hin[2 * n] + Hin[2 * n + 1]) - (Han[2 * n] + Han[2 * n + 1]) * (0.09 / 20.0)
    ex = 0.5 * (ex + ex[::-1])
    KER.append(ex / ex.sum())
DG = np.arange(0.0, 800.0, 0.5)
PTAB = np.zeros((4, len(DG)))
for n in range(4):
    for i, D in enumerate(DG):
        lo_ = np.maximum(DEh[:-1] + D, -10.0); hi_ = np.minimum(DEh[1:] + D, 10.0)
        PTAB[n, i] = np.clip((KER[n] * np.maximum(hi_ - lo_, 0) / np.diff(DEh)).sum(), 0, 1)
DMAXB = 0.5 * L / LH
IFAR = np.array([2 * np.trapz(PTAB[n][DG >= DMAXB], DG[DG >= DMAXB]) * LH for n in range(4)])
MLIM = np.interp(ZN, S["Z0"], S["mlim"])
xcm = 0.5 * (DEh[1:] + DEh[:-1]); w10 = np.abs(xcm) < 10
zsub = S["z"][S["sub"]]; lmsub = S["logM"][S["sub"]]; ZBs = S["ZB"]
MC = np.zeros(4)
n_smf = LBR.n_smf
for n in range(4):
    lam = (S["H_an"][2 * n][w10].sum() + S["H_an"][2 * n + 1][w10].sum()) / (S["NLZ"][2 * n] + S["NLZ"][2 * n + 1]) * 9.0 / 20.0
    msk = (zsub >= ZBs[2 * n]) & (zsub < ZBs[2 * n + 2]); lmn = lmsub[msk]
    g = lambda mc: float(np.mean(n_smf(np.maximum(lmn - 1.0, mc)))) * 0.343 * math.pi * 9.0 * 20.0 - lam
    MC[n] = brentq(g, 7.0, 12.5)
THRS = {"F": MLIM, "P": MC}
LB = np.round(np.arange(8.5, 11.1001, 0.1), 2)
NB = len(LB) - 1
R_ISO, R_IN, R_A1, R_A2 = 3.0 * LH, 0.5 * LH, 4.0 * LH, 6.0 * LH
AREA_RATIO = R_IN ** 2 / (R_A2 ** 2 - R_A1 ** 2)
DXF = L / (8 * N)


def selection(rule):
    """galaxies, lenses, isolation weights and the companion / weight tables for one occupation rule (CFG506 lines 366-542 + the
    table accumulation of lines 702-728 that does not need the maps)."""
    B, al = RULES[rule]
    sh = LBR.Sham(Mta, MP, B, al)
    GPOS, GLMS, GSAT, GHALO, rng, lms_c, sat_lms, sat_host = LBR.draw_galaxies(sh, cen, Mta, rta, r200m, pos, tree)
    NGAL = len(GPOS)
    mlim_box = sh.mlim_box
    VB = [k for k in range(len(LB) - 1) if LB[k] >= mlim_box - 1e-9]
    info = dict(B=B, alpha=al, m_lim_box=mlim_box, n_sat=int(len(sat_lms)), lMmin_10p5=float(sh.lMmin_of_m(10.5)),
                fsat_par={f"{a:.1f}": float(GSAT[(GLMS >= a) & (GLMS < a + 0.1)].mean()) for a in np.arange(10.0, 11.1, 0.1)
                          if ((GLMS >= a) & (GLMS < a + 0.1)).any()},
                fpar_cal_bins=[float(GSAT[(GLMS >= a) & (GLMS < b)].mean()) for a, b in ((10.5, 10.75), (10.75, 11.0))])
    say(f"  [{rule}] B {B:.3f}, alpha {al:.2f}: m_lim,box {mlim_box:.2f}, log M_min(10.5) {info['lMmin_10p5']:.2f}; {len(cen)} centrals + "
        f"{len(sat_lms)} satellites; parent fraction [10.5, 10.75) {info['fpar_cal_bins'][0]:.3f}, [10.75, 11.0) {info['fpar_cal_bins'][1]:.3f}")
    lens_idx, lens_bin = [], []
    for k in VB:
        for issat in (False, True):
            sel = np.where((GLMS >= LB[k]) & (GLMS < LB[k + 1]) & (GSAT == issat))[0]
            if len(sel) > 6000:
                sel = np.sort(rng.choice(sel, 6000, replace=False))
            lens_idx.append(sel); lens_bin.append(np.full(len(sel), k))
    lens_idx = np.concatenate(lens_idx); lens_bin = np.concatenate(lens_bin)
    NL = len(lens_idx)
    LPOS = GPOS[lens_idx]; LLMS = GLMS[lens_idx]; LSAT = GSAT[lens_idx]
    rng7 = np.random.default_rng(507)
    SPOS = rng7.uniform(0, L, size=(NL, 3))
    LPOS = (np.round(LPOS / DXF) * DXF) % L; SPOS = (np.round(SPOS / DXF) * DXF) % L
    GSORT = np.sort(GLMS)
    def n_box_above(t): return (NGAL - np.searchsorted(GSORT, t)) / V
    WISO = {v: np.zeros((3, 4, NL)) for v in THRS}; CEX = {v: np.zeros((3, 4, NL)) for v in THRS}
    for ax in range(3):
        a2 = [i for i in range(3) if i != ax]
        t2 = cKDTree(GPOS[:, a2] % L, boxsize=L)
        for c0 in range(0, NL, 4000):
            sl = slice(c0, min(c0 + 4000, NL))
            lists = t2.query_ball_point(LPOS[sl][:, a2] % L, R_A2, workers=2)
            ln = np.repeat(np.arange(sl.start, sl.stop), [len(x) for x in lists])
            jn = np.concatenate([np.asarray(x, int) for x in lists])
            selfm = jn != lens_idx[ln]
            ln, jn = ln[selfm], jn[selfm]
            dtr = GPOS[jn][:, a2] - LPOS[ln][:, a2]; dtr -= L * np.round(dtr / L); Rt = np.hypot(dtr[:, 0], dtr[:, 1])
            dl = GPOS[jn, ax] - LPOS[ln, ax]; dl -= L * np.round(dl / L)
            Dm = np.abs(dl) / LH
            for n in range(4):
                p = np.interp(Dm, DG, PTAB[n])
                for v, TH in THRS.items():
                    thr = np.maximum(LLMS[ln] - 1.0, TH[n])
                    iso = (Rt < R_ISO) & (GLMS[jn] > thr)
                    lw = np.bincount(ln[iso] - sl.start, weights=np.log(np.maximum(1 - p[iso], 1e-12)), minlength=sl.stop - sl.start)
                    thr_l = np.maximum(LLMS[sl] - 1.0, TH[n])
                    nthr = n_smf(thr_l); nmiss = np.maximum(nthr - np.array([n_box_above(t) for t in thr_l]), 0)
                    lam = nthr * math.pi * R_ISO ** 2 * IFAR[n] + nmiss * math.pi * R_ISO ** 2 * (2 * 10.0 * LH)
                    WISO[v][ax, n, sl] = np.exp(lw - lam)
                    cm = GLMS[jn] > np.maximum(LLMS[ln], TH[n])
                    wq = 1 - p
                    cin = np.bincount(ln[cm & (Rt < R_IN)] - sl.start, weights=wq[cm & (Rt < R_IN)], minlength=sl.stop - sl.start)
                    can = np.bincount(ln[cm & (Rt >= R_A1) & (Rt < R_A2)] - sl.start, weights=wq[cm & (Rt >= R_A1) & (Rt < R_A2)],
                                      minlength=sl.stop - sl.start)
                    CEX[v][ax, n, sl] = cin - can * AREA_RATIO
        del t2
    NALL = {(b, t): int(((GLMS >= LB[b]) & (GLMS < LB[b + 1]) & (GSAT == t)).sum()) for b in VB for t in (False, True)}
    info["pass_fraction"] = {}
    for v in THRS:
        for n in range(4):
            num = den = 0.0
            for b in VB:
                for t in (False, True):
                    m_ = (lens_bin == b) & (LSAT == t)
                    if m_.any():
                        num += NALL[(b, t)] * WISO[v][:, n, m_].mean(); den += NALL[(b, t)]
            zz = (S["z"] >= ZBs[2 * n]) & (S["z"] < ZBs[2 * n + 2]) & (S["logM"] >= LB[VB[0]])
            info["pass_fraction"][f"{v}|{ZN[n]}"] = dict(box=num / den, kids=float(S["iso10"][zz].mean()))
        # ISO / ALL of the box parent satellite fraction (sampling-corrected, node z 0.25), lens bins
        n = 1; fi = fa = wi = wa_ = 0.0
        for b in VB:
            for t in (False, True):
                m_ = (lens_bin == b) & (LSAT == t)
                if m_.any():
                    ww = NALL[(b, t)] * WISO[v][:, n, m_].mean(); fi += ww * t; wi += ww; fa += NALL[(b, t)] * t; wa_ += NALL[(b, t)]
        info[f"iso_over_all_{v}"] = (fi / wi) / (fa / wa_) if wi > 0 and fa > 0 else None
        say(f"    [{rule}] variant {v}: pass fraction box / KiDS: " + ", ".join(
            f"{ZN[n]}: {info['pass_fraction'][f'{v}|{ZN[n]}']['box']:.3f}/{info['pass_fraction'][f'{v}|{ZN[n]}']['kids']:.3f}" for n in range(4))
            + f"; box ISO/ALL satellite fraction (z 0.25 node) {info[f'iso_over_all_{v}']:.3f}")
    jk = (np.floor(LPOS / (L / 3)).astype(int) % 3) @ np.array([9, 3, 1])
    idx_l = jk * NB + lens_bin
    TABS = {}
    for v in THRS:
        WT = {k: np.zeros((27, NB, 4)) for k in ("all", "cen", "sat")}
        CT = np.zeros((27, NB, 4)); FS = np.zeros((27, NB, 4)); LMW = np.zeros((NB, 4)); LMWW = np.zeros((NB, 4))
        for n in range(4):
            for ax in range(3):
                w = WISO[v][ax, n]
                WT["all"][:, :, n] += np.bincount(idx_l, weights=w, minlength=27 * NB).reshape(27, NB)
                WT["cen"][:, :, n] += np.bincount(idx_l, weights=w * ~LSAT, minlength=27 * NB).reshape(27, NB)
                WT["sat"][:, :, n] += np.bincount(idx_l, weights=w * LSAT, minlength=27 * NB).reshape(27, NB)
                CT[:, :, n] += np.bincount(idx_l, weights=w * CEX[v][ax, n], minlength=27 * NB).reshape(27, NB)
                FS[:, :, n] += np.bincount(idx_l, weights=w * LSAT, minlength=27 * NB).reshape(27, NB)
                LMW[:, n] += np.bincount(lens_bin, weights=w * LLMS, minlength=NB); LMWW[:, n] += np.bincount(lens_bin, weights=w, minlength=NB)
        TABS.update({f"{v}_W_{k}": x for k, x in WT.items()})
        TABS.update({f"{v}_CT": CT, f"{v}_FS": FS, f"{v}_LMW": LMW, f"{v}_LMWW": LMWW})
        den_ = WT["all"].sum(0); fs = FS.sum(0) / np.maximum(den_, 1e-300)
        say(f"    [{rule}] [{v}] f_sat(iso) at z 0.25 per bin: " + ", ".join(f"{LB[b]:.1f}: {fs[b, 1]:.3f}" for b in VB)
            + "; companions: " + ", ".join(f"{LB[b]:.1f}: {CT.sum(0)[b, 1] / max(den_[b, 1], 1e-300):.3f}" for b in VB))
    return dict(GPOS=GPOS, GLMS=GLMS, GSAT=GSAT, lens_idx=lens_idx, lens_bin=lens_bin, LPOS=LPOS, SPOS=SPOS, LLMS=LLMS, LSAT=LSAT,
                WISO_F=WISO["F"], WISO_P=WISO["P"], mlim_box=mlim_box, VB=np.array(VB), LB=LB, NL=NL, **TABS), info


if STAGE == "sel":
    OUT["selection"] = {}
    for rule in RULES:
        d_, info = selection(rule)
        OUT["selection"][rule] = info
        np.savez_compressed(os.path.join(WORK, f"cfg520_sel_{rule}_{KEY}.npz"), **{k: v for k, v in d_.items() if k not in ("GPOS",)},
                            GPOS=d_["GPOS"].astype(np.float64))
        if rule == "R0":
            keys = [f"{v}_{k}" for v in ("F", "P") for k in ("CT", "W_all", "W_cen", "W_sat", "FS", "LMW", "LMWW")]
            dev = max(float(np.max(np.abs(d_[k] - C6[k]) / np.maximum(np.abs(C6[k]), 1e-300 + 1e-9 * np.abs(C6[k]).max())))
                      for k in keys)
            check("R0a box path at B = 17 reproduces CFG506's selection tables (F/P CT, W, FS, LMW, LMWW) within 1e-9 rel", dev < 1e-9,
                  f"max rel dev {dev:.2e}; m_lim,box {d_['mlim_box']:.2f} vs CFG506 {float(C6['mlim_box']):.2f}; NL {d_['NL']} vs {int(C6['NL'])}")
        guard(f"selection {rule}")
    write_results()
    sys.exit(1 if any(c["load_bearing"] and not c["ok"] for c in CHK.values()) else 0)

# ================================================================= stage ds: CFG506 section 5 for one rule
SEL = np.load(os.path.join(WORK, f"cfg520_sel_{RULE_DS}_{KEY}.npz"))
B_, al_ = RULES[RULE_DS]
sh = LBR.Sham(Mta, MP, B_, al_)
GPOS, GLMS, GSAT, _, _, _, _, _ = LBR.draw_galaxies(sh, cen, Mta, rta, r200m, pos, tree)
g0 = np.array_equal(GPOS, SEL["GPOS"]) and np.array_equal(GLMS, SEL["GLMS"]) and np.array_equal(GSAT, SEL["GSAT"])
check("G0 galaxies regenerated identically to the selection stage", g0, f"{len(GLMS)} galaxies")
del GPOS, GLMS, GSAT
lens_idx, lens_bin, LPOS, SPOS, LLMS, LSAT = (SEL[k] for k in ("lens_idx", "lens_bin", "LPOS", "SPOS", "LLMS", "LSAT"))
WISO = {"F": SEL["WISO_F"], "P": SEL["WISO_P"]}
VB = list(SEL["VB"]); mlim_box = float(SEL["mlim_box"]); NL = int(SEL["NL"])

RE = np.geomspace(0.02, 15.0, 41); RM = np.sqrt(RE[1:] * RE[:-1])
NF = 8 * N; DXF = L / NF
kf1 = 2 * np.pi * sfft.fftfreq(NF, d=DXF); kf2 = 2 * np.pi * sfft.rfftfreq(NF, d=DXF)
KK = np.sqrt(kf1[:, None] ** 2 + kf2[None, :] ** 2)
SIGF = DXF
from scipy import stats as sst
WCIC = (np.sinc(kf1[:, None] * DXF / (2 * np.pi)) ** 2 * np.sinc(kf2[None, :] * DXF / (2 * np.pi)) ** 2)
TAPER = np.exp(-0.5 * KK ** 2 * SIGF ** 2) / WCIC


def disc_filter(R):
    x = KK * R; out = np.ones_like(x); nz = x > 1e-12
    out[nz] = 2 * j1(x[nz]) / x[nz]
    return out * TAPER


RHO_E = np.arange(0.0, 2.6 + 1e-9, 0.0025); RHO_C = 0.5 * (RHO_E[1:] + RHO_E[:-1])
PT = np.array([sst.rice.cdf(R, RHO_C / SIGF, scale=SIGF) for R in RE]).T


def node(xy):
    return (np.round(xy / DXF).astype(np.int64)) % NF


xp = np.array([L / 2 + 0.37 * DXF, L / 2 + 0.21 * DXF])
pm = np.zeros(NF * NF); u = xp / DXF; i0 = np.floor(u).astype(np.int64); f = u - i0
for sx in (0, 1):
    for sy in (0, 1):
        pm[((i0[0] + sx) % NF) * NF + (i0[1] + sy) % NF] += (f[0] if sx else 1 - f[0]) * (f[1] if sy else 1 - f[1])
pm = pm.reshape(NF, NF) / DXF ** 2
pk_ = sfft.rfft2(pm, workers=2)
nd = node(xp[None, :])[0]; off = np.hypot(*(xp - nd * DXF))
vals = np.array([sfft.irfft2(pk_ * disc_filter(R), s=(NF, NF), workers=2)[nd[0], nd[1]] * math.pi * R ** 2 for R in RE])
expct = sst.rice.cdf(RE, off / SIGF, scale=SIGF)
okR = RE >= 3 * DXF
c3 = float(np.max(np.abs(vals[okR] / expct[okR] - 1)))
check("C3 Fourier-disc mass of a point mass = M within 2% at R >= 3 fine cells", c3 < 0.02, f"max |M(<R)/expected - 1| {c3:.2e}")
del pm, pk_

MCUM = np.zeros((3, NL, len(RE))); MCUMS = np.zeros((3, NL, len(RE))); MCUM_SRC = np.zeros((3, NL, len(RE)))
for ax in range(3):
    a2 = [i for i in range(3) if i != ax]
    mp2 = np.zeros(NF * NF)
    for c0 in range(0, NP, 16_000_000):
        u = pos[c0:c0 + 16_000_000][:, a2] / DXF; i0 = np.floor(u).astype(np.int64); f = u - i0
        for sx in (0, 1):
            for sy in (0, 1):
                w = (f[:, 0] if sx else 1 - f[:, 0]) * (f[:, 1] if sy else 1 - f[:, 1])
                mp2 += np.bincount(((i0[:, 0] + sx) % NF) * NF + (i0[:, 1] + sy) % NF, weights=w, minlength=NF * NF)
    mp2 = mp2.reshape(NF, NF) * MP / DXF ** 2
    maps = [mp2]
    if SRC is not None:
        sc = SRC.sum(axis=ax, dtype=np.float64) * RHOM_H * dx ** 3
        sf = np.roll(np.kron(sc / 64.0, np.ones((8, 8))), (-4, -4), axis=(0, 1)) / DXF ** 2
        maps = [mp2 + sf, sf]
        del sc, sf
    Fks = [sfft.rfft2(M_, workers=2) for M_ in maps]
    for ir, R in enumerate(RE):
        filt = disc_filter(R)
        for im, Fk in enumerate(Fks):
            sm = sfft.irfft2(Fk * filt, s=(NF, NF), workers=2)
            if im == 0:
                ndl = node(LPOS[:, a2]); MCUM[ax, :, ir] = sm[ndl[:, 0], ndl[:, 1]] * math.pi * R ** 2
                nds = node(SPOS[:, a2]); MCUMS[ax, :, ir] = sm[nds[:, 0], nds[:, 1]] * math.pi * R ** 2
            else:
                ndl = node(LPOS[:, a2]); MCUM_SRC[ax, :, ir] = sm[ndl[:, 0], ndl[:, 1]] * math.pi * R ** 2
            del sm
        del filt
    del Fks, maps, mp2
    say(f"  axis {ax}: maps + disc means done")
    guard(f"maps axis {ax}")

ET = np.load(os.path.join(EXT, "cfg503_work", "cfg503_env_table.npz"))
LMS_, ZG_ = ET["LMS"], ET["ZG"]
from scipy.interpolate import RegularGridInterpolator
frta = RegularGridInterpolator((LMS_, ZG_), ET["moster_RTA"], bounds_error=False, fill_value=None)
RREM = np.zeros((4, NL))
for n in range(4):
    RREM[n] = frta(np.c_[np.clip(LLMS, LMS_[0], LMS_[-1]), np.full(NL, ZN[n])]) * (1 + ZN[n]) * LH
RREM[:, LSAT] = 0.0
OWN = np.zeros((3, 4, NL, len(RE))); OWNS = np.zeros((3, 4, NL, len(RE))); OWN_SRC = np.zeros((3, 4, NL, len(RE)))
rmax = RREM.max(0)
cidx = np.where(~LSAT)[0]


def own_content(P3, rem_max, store, store_src):                     # CFG506's, copied
    for c0 in range(0, len(cidx), 2000):
        ids = cidx[c0:c0 + 2000]
        lists = tree.query_ball_point(P3[ids], rem_max[ids], workers=2)
        for t_, i in enumerate(ids):
            li = np.asarray(lists[t_], int)
            d = pos[li] - P3[i]; d -= L * np.round(d / L)
            r3 = np.sqrt((d ** 2).sum(1))
            if SRC is not None:
                nb = int(math.ceil(rem_max[i] / dx)) + 1; obb = np.arange(-nb, nb + 1)
                cc = np.floor(P3[i] / dx).astype(int)
                gx = (cc[0] + obb) % N; gy = (cc[1] + obb) % N; gz = (cc[2] + obb) % N
                cube = SRC[np.ix_(gx, gy, gz)].astype(np.float64) * RHOM_H * dx ** 3
                off = (obb * dx)[:, None, None], (obb * dx)[None, :, None], (obb * dx)[None, None, :]
                cpos = [(cc[k] * dx + off[k]) for k in range(3)]
                dcx = (cpos[0] - P3[i][0]); dcy = (cpos[1] - P3[i][1]); dcz = (cpos[2] - P3[i][2])
                dcx, dcy, dcz = np.broadcast_arrays(dcx, dcy, dcz)
                rc = np.sqrt(dcx ** 2 + dcy ** 2 + dcz ** 2).ravel(); dcs = np.c_[dcx.ravel(), dcy.ravel(), dcz.ravel()]
                cw = cube.ravel()
            for n in range(4):
                rr = RREM[n, i]
                s_ = r3 < rr
                if SRC is not None:
                    sc_ = rc < rr
                for ax in range(3):
                    a2 = [k for k in range(3) if k != ax]
                    R2 = np.hypot(d[s_][:, a2[0]], d[s_][:, a2[1]])
                    hb = np.bincount(np.minimum((R2 / 0.0025).astype(np.int64), len(RHO_C) - 1), minlength=len(RHO_C))
                    store[ax, n, i] = (hb @ PT) * MP
                    if SRC is not None:
                        Rc_ = np.hypot(dcs[sc_][:, a2[0]], dcs[sc_][:, a2[1]])
                        hs_ = np.bincount(np.minimum((Rc_ / 0.0025).astype(np.int64), len(RHO_C) - 1), weights=cw[sc_], minlength=len(RHO_C))
                        v = hs_ @ PT
                        store[ax, n, i] += v
                        if store_src is not None:
                            store_src[ax, n, i] = v


own_content(LPOS, rmax, OWN, OWN_SRC)
own_content(SPOS, rmax, OWNS, None)
say("own-sphere content done")
guard("own content")


def dsig_from_cum(Mc):
    dM = np.diff(Mc, axis=-1); dA = math.pi * np.diff(RE ** 2)
    Sig = dM / dA
    Mmid = Mc[..., :-1] + dM * (RM ** 2 - RE[:-1] ** 2) / np.diff(RE ** 2)
    return Mmid / (math.pi * RM ** 2) - Sig


def sphere_cum(a):
    a = np.asarray(a, float)[..., None]
    Mt = 4 * math.pi / 3 * a ** 3 * RHOM_H
    x = np.clip(RE / np.maximum(a, 1e-12), 0, 1)
    return np.where(a > 0, Mt * (1 - (1 - x ** 2) ** 1.5), 0.0)


jk = (np.floor(LPOS / (L / 3)).astype(int) % 3) @ np.array([9, 3, 1])
jks = (np.floor(SPOS / (L / 3)).astype(int) % 3) @ np.array([9, 3, 1])
idx_l = jk * NB + lens_bin; idx_s = jks * NB + lens_bin
SAVE = {}
for v in THRS:
    TAB = {k: np.zeros((27, NB, 4, len(RM))) for k in ("E", "E_cen", "E_sat", "E_src", "TOT_cen", "SHUF", "H", "HSHUF")}
    WT = {"shuf": np.zeros((27, NB, 4))}
    for n in range(4):
        Hc = dsig_from_cum(sphere_cum(RREM[n]))
        for ax in range(3):
            w = WISO[v][ax, n]
            Ei = dsig_from_cum(MCUM[ax] - OWN[ax, n])
            Es = dsig_from_cum(MCUMS[ax] - OWNS[ax, n])
            Esrc = dsig_from_cum(MCUM_SRC[ax] - OWN_SRC[ax, n]) if SRC is not None else np.zeros_like(Ei)
            Tc = dsig_from_cum(MCUM[ax])
            for key_, arr, ix_, wsel in (("E", Ei, idx_l, None), ("E_cen", Ei, idx_l, ~LSAT), ("E_sat", Ei, idx_l, LSAT),
                                         ("E_src", Esrc, idx_l, None), ("TOT_cen", Tc, idx_l, ~LSAT), ("SHUF", Es, idx_s, None),
                                         ("H", Hc, idx_l, None), ("HSHUF", Hc, idx_s, None)):
                ww = w if wsel is None else w * wsel
                acc = np.zeros((27 * NB, len(RM)))
                np.add.at(acc, ix_, ww[:, None] * arr)
                TAB[key_][:, :, n] += acc.reshape(27, NB, len(RM))
            WT["shuf"][:, :, n] += np.bincount(idx_s, weights=w, minlength=27 * NB).reshape(27, NB)
    SAVE.update({f"{v}_T_{k}": x for k, x in TAB.items()}); SAVE[f"{v}_W_shuf"] = WT["shuf"]
    for k in ("W_all", "W_cen", "W_sat", "CT", "FS", "LMW", "LMWW"):
        SAVE[f"{v}_{k}"] = SEL[f"{v}_{k}"]
    den_ = SEL[f"{v}_W_all"].sum(0)
    E_all = TAB["E"].sum(0) / np.maximum(den_[..., None], 1e-300)
    for b in VB[::2]:
        say(f"  [{v}] bin {LB[b]:.1f}-{LB[b + 1]:.1f} z 0.25: E_native(R_com 0.1/0.5/1/2/4 Mpc/h) "
            f"{np.round(np.interp([0.1, 0.5, 1, 2, 4], RM, E_all[b, 1]) / 1e12 * LH, 3).tolist()} Msun/pc^2 (z = 0, comoving)")
np.savez_compressed(os.path.join(WORK, f"cfg520_box_{RULE_DS}_{KEY}.npz"), LB=LB, ZN=ZN, mlim_box=mlim_box, MP=MP, dx=dx, RE=RE, RM=RM,
                    VB=np.array(VB), NL=NL, nlens_cen=int((~LSAT).sum()), nlens_sat=int(LSAT.sum()), **SAVE)
say("stacks done")
guard("done")
write_results()
sys.exit(1 if any(c["load_bearing"] and not c["ok"] for c in CHK.values()) else 0)
