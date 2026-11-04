"""LAM9 stage 0: can the half-light sums carry an IMF fit? Reads only; no fit, no download, no cube.
For KU2's 6056 galaxies: which have a sum (LAM4 + LAM7), rest-frame coverage of the IMF windows (Na I 8190, CaT, TiO1,
TiO2sdss), bad-pixel share, S/N per rest-frame A (formal, and scaled by the LAM4/LAM7 kinematic fit's sqrt(chi2)),
sky-line and telluric exposure, and an observed-frame stack of all sums that shows coherent sky/telluric residuals.
Also: LAM2's fibre gas flag, the Tian+2026 MaNGA ellipticals (HX1's rungs) inside the sample, and two mass-unit checks.
Run: nice -n 10 python3 -I lam9_stage0.py   (single thread, about a minute, < 1 GB). κ = ½ FITTED; not theory closed."""
import os, sys, json, glob
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.ndimage import median_filter
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ROOT = os.path.dirname(RB); EXT = os.path.join(ROOT, "_external_data")
OUT = []; RES = {"lane": "LAM9", "stage": 0, "note": "κ = ½ FITTED; not theory closed. Reads only; no fit, no download."}
def P(s=""): print(s, flush=True); OUT.append(s)
P("LAM9 stage 0 (reads only; no fit, no download). κ = ½ FITTED; not theory closed.")

# ---- KU2's sample, exactly (as LAM6 / LAM7 load it)
KU2 = os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.py"); argv = sys.argv; sys.argv = ["ku2.py"]
K = {"__file__": KU2, "__name__": "ku2"}; exec(compile(open(KU2).read().split("ok1 = slow.sum()")[0], "ku2.py", "exec"), K); sys.argv = argv
rows = np.flatnonzero(K["sel"]); n = len(rows)
dp = fits.open(os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits"))[1].data
pifu = np.char.strip(np.array(dp["plateifu"], str))[rows]; mid = np.char.strip(np.array(dp["mangaid"], str))[rows]
z = K["z"]; sig = K["sig"]; slow = K["slow"]
P(f"KU2 sample {n} galaxies (slow {int(slow.sum())}); z median {np.median(z):.4f}, 5-95 % {np.percentile(z, 5):.4f}-{np.percentile(z, 95):.4f}, max {z.max():.4f}")

# ---- sums and kinematic fits (read only)
S4, S7 = os.path.join(EXT, "lam4_integrated_2026_11_03"), os.path.join(EXT, "lam7_integrated_2026_11_04")
path = {}
for d in (S4, S7):
    for fn in glob.glob(os.path.join(d, "*.npz")): path[os.path.basename(fn)[:-4]] = fn
FIT = {}
for fn in (os.path.join(RB, "LAM4_whole_galaxy_absorption", "lam4_fit.jsonl"), os.path.join(RB, "LAM7_orbit_shape_full_sample", "lam7_fit.jsonl")):
    for l in open(fn):
        if l.strip(): r = json.loads(l); FIT[r["plateifu"]] = r
has = np.array([p in path for p in pifu]); P(f"sums on disk for the sample: {int(has.sum())} of {n} (LAM4 dir {len(glob.glob(os.path.join(S4, '*.npz')))}, LAM7 dir {len(glob.glob(os.path.join(S7, '*.npz')))})")
chi2 = np.array([FIT[p]["chi2"] if p in FIT and FIT[p]["status"] == "ok" else np.nan for p in pifu])
P(f"kinematic fits ok: {int(np.isfinite(chi2).sum())}; their chi2 median {np.nanmedian(chi2):.2f}, 5-95 % {np.nanpercentile(chi2, 5):.2f}-{np.nanpercentile(chi2, 95):.2f}")

# ---- LAM2's fibre gas flag (MPA-JHU H-alpha EW, A1 sign: emission EW = -h_alpha_eqw; gas-poor < 3 A)
LD = os.path.join(EXT, "lam2_sdss_lines_2026_11_03"); EW = {}
for fn in sorted(glob.glob(os.path.join(LD, "lines_*.csv"))):
    for l in open(fn).read().splitlines()[2:]:
        c = l.split(",")
        if c[0].strip(): EW[int(c[0])] = float(c[7]) if c[7] != "" else np.nan
m = np.loadtxt(os.path.join(LD, "dynpop_match.csv"), delimiter=",", skiprows=1, dtype=np.int64); sid = {}
for r_, s_ in m: sid.setdefault(int(r_), int(np.int64(s_).view(np.uint64)))
ew = np.array([-EW.get(sid.get(int(r_), -1), np.nan) for r_ in rows])
gas_known = np.isfinite(ew); poor = gas_known & (ew < 3); s100 = sig >= 100; cand = has & poor & s100
P(f"fibre gas flag known {int(gas_known.sum())}; gas-poor {int(poor.sum())}; Sigma_Re >= 100 {int(s100.sum())}; gas-poor AND Sigma_Re >= 100 with a sum {int(cand.sum())} (slow {int((cand & slow).sum())})")

# ---- Tian+2026 MaNGA ellipticals (HX1's MaNGA rungs)
TI, TS = {}, []
for l in open(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "groups", "J_A_A_710_L39.tsv")):
    f = l.rstrip("\n").split("\t")
    if len(f) >= 13 and f[0].strip().isdigit() and f[1].strip() == "MaNGA elliptical": TI.setdefault(f[2].strip(), (float(f[5]), float(f[7]))); TS.append(10 ** float(f[5]))
q = np.percentile(TS, [25, 50, 75]); tian = np.array([x in TI for x in mid])  # HX1's edges: all catalogue rows of the class
tq = np.array([np.searchsorted(q, 10 ** TI[x][0]) if x in TI else -1 for x in mid])
P(f"Tian MaNGA elliptical rows {len(TS)}, distinct objects {len(TI)}; HX1 sigma quartile edges {q.round(1).tolist()} km/s; in KU2 sample {int(tian.sum())}, with a sum {int((tian & has).sum())}, "
  f"with a sum and gas-poor {int((tian & has & poor).sum())}; per quartile Q1-Q4 with a sum: {[int(((tq == k) & has).sum()) for k in range(4)]}")

# ---- mass-unit checks (input calibration, not graded)
Mr = np.array(dp["nsa_elpetro_absmag"], float)[rows, 4]; LM = np.array(dp["Lum_tot_MGE"], float)[rows]
Lr = -0.4 * (Mr - 4.65); ok = np.isfinite(Lr) & (LM > 0)
d1 = LM[ok] - Lr[ok]; d2 = K["me"][ok] - LM[ok]
P(f"mass units: log L_MGE - log L_r(NSA elpetro absmag as stored) median {np.median(d1):+.3f} (16-84 % {np.percentile(d1, 16):+.3f}, {np.percentile(d1, 84):+.3f}); "
  f"log M_NSA(as stored) - log L_MGE median {np.median(d2):+.3f}")
lt = np.array([TI[x][1] if x in TI else np.nan for x in mid]); okt = np.isfinite(lt)
P(f"mass units: Tian logMbar - NSA elpetro (as stored) on {int(okt.sum())} shared galaxies, median {np.median(lt[okt] - K['me'][okt]):+.3f}")
RES["mass_units"] = dict(LMGE_minus_LNSA=float(np.median(d1)), MNSA_minus_LMGE=float(np.median(d2)), Tian_minus_NSA=float(np.median(lt[okt] - K["me"][okt])))

# ---- windows (rest frame, A): region spans the feature and its pseudo-continua
WIN = {"NaI8190": (8143.0, 8244.0), "CaT": (8474.0, 8792.0), "TiO1": (5816.0, 6103.0), "TiO2sdss": (6066.0, 6455.0), "V_ref": (5070.0, 5950.0)}
FIT_END = 8900.0  # E-MILES keeps FWHM 2.51 A to 8950 A rest
TELL = [(6860, 6960), (7160, 7340), (7590, 7700), (8100, 8380), (8930, 9250), (9270, 9850)]  # nominal observed telluric bands
wave = None; R = np.full((n, 4563), np.nan, np.float32)
stat = {w: {k: np.full(n, np.nan) for k in ("cov", "bad", "sn", "sky", "tell", "fw")} for w in WIN}; reach = np.full(n, np.nan)
for i in np.flatnonzero(has):
    d = np.load(path[pifu[i]]); w = d["wave"].astype(float); f = d["flux"].astype(float); v = d["var"].astype(float); bad = d["bad"]; zz = float(d["z"])
    if wave is None: wave = w
    good = ~bad & (v > 0) & np.isfinite(f); e = np.where(good, np.sqrt(np.clip(v, 1e-30, None)), np.nan)
    sm = median_filter(np.where(good, f, np.nan_to_num(np.nanmedian(f))), 101, mode="nearest"); R[i] = np.where(good & (sm > 0), f / sm - 1, np.nan)
    es = median_filter(np.nan_to_num(e, nan=np.nanmedian(e)), 51, mode="nearest"); spike = e / es > 1.5
    lr = w / (1 + zz); reach[i] = lr[-1]; tl = np.zeros(len(w), bool)
    for a, b in TELL: tl |= (w >= a) & (w <= b)
    for k, (a, b) in WIN.items():
        s = (lr >= a) & (lr <= b); st = stat[k]
        st["cov"][i] = float(lr[0] <= a and lr[-1] >= b)
        if not s.any(): continue
        g = s & good; st["bad"][i] = 1 - g.sum() / s.sum()
        dl = lr[s] * np.log(10) * 1e-4  # rest A per pixel
        if g.any(): st["sn"][i] = float(np.median(f[g] / e[g]) / np.sqrt(np.median(dl)))
        st["sky"][i] = float(np.mean(spike[s])); st["tell"][i] = float(np.mean(tl[s]))
        st["fw"][i] = float(np.median(2.355 * d["lsf_sigma"][s] / (1 + zz)))
stack = np.nanmedian(R[has], axis=0); narrow = stack - median_filter(np.nan_to_num(stack), 21, mode="nearest")
P(f"\nobserved-frame stack of all {int(has.sum())} sums (flux / 101-px running median - 1, median over galaxies; narrow part = minus 21-px running median):")
P("  observed band (A)  rms narrow   99 % |narrow|   pixels with |narrow| > 0.01")
RES["stack"] = {}
for a, b in ((4000, 5500), (5500, 6800), (6800, 7600), (7600, 8100), (8100, 8600), (8600, 9100), (9100, 9600), (9600, 10300)):
    s = (wave >= a) & (wave < b); x = narrow[s]
    P(f"  {a:>5d}-{b:<5d}        {np.sqrt(np.mean(x**2)):.4f}      {np.percentile(np.abs(x), 99):.4f}          {np.mean(np.abs(x) > 0.01):.3f}")
    RES["stack"][f"{a}-{b}"] = dict(rms=float(np.sqrt(np.mean(x**2))), p99=float(np.percentile(np.abs(x), 99)), frac_gt_1pc=float(np.mean(np.abs(x) > 0.01)))
coh = np.abs(narrow) > 0.01  # candidate frozen sky/telluric mask (observed frame)
cohw = {k: np.full(n, np.nan) for k in WIN}; rmsw = {k: np.full(n, np.nan) for k in WIN}
for i in np.flatnonzero(has):
    lr = wave / (1 + z[i])
    for k, (a, b) in WIN.items():
        s = (lr >= a) & (lr <= b)
        if s.any(): cohw[k][i] = float(np.mean(coh[s])); rmsw[k][i] = float(np.sqrt(np.mean(narrow[s] ** 2)))

def pct(x, qq): return float(np.percentile(x, qq)) if len(x) else float("nan")
def block(name, sel):
    P(f"\n[{name}] N {int(sel.sum())}")
    P("  window      covered  bad<20%   S/N per A median (5-95 %)   /sqrt(chi2) median   sky-spike px  telluric px  coherent>1% px  stack rms  rest FWHM")
    out = {}
    for k in WIN:
        st = stat[k]; c = sel & (st["cov"] == 1); cb = c & (st["bad"] < 0.2); sn = st["sn"][cb]; sc = (st["sn"] / np.sqrt(np.clip(chi2, 1, None)))[cb & np.isfinite(chi2)]
        P(f"  {k:<10s}  {c.sum() / max(sel.sum(), 1):.3f}    {cb.sum() / max(sel.sum(), 1):.3f}    {pct(sn, 50):6.1f} ({pct(sn, 5):5.1f}-{pct(sn, 95):6.1f})"
          f"          {pct(sc, 50):6.1f}            {np.nanmedian(st['sky'][cb]):.3f}        {np.nanmedian(st['tell'][cb]):.3f}       {np.nanmedian(cohw[k][cb]):.3f}       {np.nanmedian(rmsw[k][cb]):.4f}    {np.nanmedian(st['fw'][cb]):.2f}")
        out[k] = dict(frac_covered=float(c.sum() / max(sel.sum(), 1)), frac_cov_bad_lt_20pc=float(cb.sum() / max(sel.sum(), 1)), n_ok=int(cb.sum()),
                      sn_per_A_median=pct(sn, 50), sn_p5=pct(sn, 5), sn_p95=pct(sn, 95), sn_min=pct(sn, 0), sn_max=pct(sn, 100),
                      sn_chi2_scaled_median=pct(sc, 50), sky_spike_frac=float(np.nanmedian(st["sky"][cb])), telluric_frac=float(np.nanmedian(st["tell"][cb])),
                      coherent_gt_1pc_frac=float(np.nanmedian(cohw[k][cb])), stack_rms=float(np.nanmedian(rmsw[k][cb])), rest_fwhm=float(np.nanmedian(st["fw"][cb])))
    both = sel & (stat["NaI8190"]["cov"] == 1) & (stat["CaT"]["cov"] == 1) & (stat["NaI8190"]["bad"] < 0.2) & (stat["CaT"]["bad"] < 0.2)
    rf = sel & (reach >= FIT_END)
    P(f"  Na I and CaT both covered with bad < 20 %: {int(both.sum())} ({both.sum() / max(sel.sum(), 1):.3f}); rest coverage reaches {FIT_END:.0f} A: {int(rf.sum())}")
    zt = np.percentile(z[sel], [100 / 3, 200 / 3]) if sel.sum() > 3 else [np.nan, np.nan]
    for j, (lo, hi) in enumerate(((0, zt[0]), (zt[0], zt[1]), (zt[1], 1))):
        t = sel & (z >= lo) & (z < hi)
        P(f"  z third {j + 1} ({lo:.3f}-{hi:.3f}): N {int(t.sum())}; CaT stack rms {np.nanmedian(rmsw['CaT'][t]):.4f}, telluric px {np.nanmedian(stat['CaT']['tell'][t]):.2f}; "
          f"Na I stack rms {np.nanmedian(rmsw['NaI8190'][t]):.4f}, telluric px {np.nanmedian(stat['NaI8190']['tell'][t]):.2f}; S/N per A Na I {np.nanmedian(stat['NaI8190']['sn'][t]):.0f}, CaT {np.nanmedian(stat['CaT']['sn'][t]):.0f}")
    out["n"] = int(sel.sum()); out["n_both_red"] = int(both.sum()); out["n_reach_fit_end"] = int(rf.sum()); return out
RES["all_sums"] = block("all KU2 galaxies with a sum", has)
RES["candidate"] = block("gas-poor (fibre EW < 3 A) and Sigma_Re >= 100, with a sum", cand)
RES["tian_upper"] = block("Tian MaNGA ellipticals with a sum, HX1 quartiles Q2-Q4", has & tian & (tq >= 1))
TR = [(f[2].strip(), 10 ** float(f[5])) for f in (l.rstrip("\n").split("\t") for l in open(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "groups", "J_A_A_710_L39.tsv")))
      if len(f) >= 13 and f[0].strip().isdigit() and f[1].strip() == "MaNGA elliptical"]
cset = set(mid[cand]); tr_q = [int(sum(1 for o, sg in TR if o in cset and np.searchsorted(q, sg) == k)) for k in range(4)]
P(f"\nTian rows (all {len(TR)} catalogue rows, as HX1 counts them) whose galaxy is gas-poor, Sigma_Re >= 100 and has a sum, per HX1 quartile Q1-Q4: {tr_q}; Q2-Q4 total {sum(tr_q[1:])}")
P(f"candidate sample z: median {np.median(z[cand]):.4f}; z <= 0.063 for {int((cand & (z <= 0.063)).sum())} of {int(cand.sum())}")
RES["counts"] = dict(tian_rows_candidate_quartiles=tr_q, cand_z_le_0063=int((cand & (z <= 0.063)).sum()), n_ku2=n, n_sums=int(has.sum()), n_gas_known=int(gas_known.sum()), n_poor=int(poor.sum()), n_sig100=int(s100.sum()), n_candidate=int(cand.sum()),
                     n_candidate_slow=int((cand & slow).sum()), n_tian=len(TI), n_tian_in_ku2=int(tian.sum()), n_tian_sum=int((tian & has).sum()),
                     n_tian_sum_quartiles=[int(((tq == k) & has).sum()) for k in range(4)], tian_sigma_edges=q.tolist())
open(os.path.join(HERE, "lam9_stage0.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "lam9_stage0.json"), "w", encoding="utf-8"), indent=1, default=float, ensure_ascii=False)
SD = os.path.join(EXT, "lam9_stage0_2026_11_04"); os.makedirs(SD, exist_ok=True)
np.save(os.path.join(SD, "narrow_stack.npy"), np.c_[wave, stack, narrow])  # observed-frame stack, outside the repo (recomputed by this script)
