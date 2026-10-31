#!/usr/bin/env python3
"""SI3_nested_isolation (criteria 60575303a2): route E at X53's text + FC1's rule against the a0 law on KiDS's nested photo-z isolation samples, with and without the isolated-random hole term.
F2's Track B text, X53's text, X79's and FC1's replacements are executed, never re-coded. Hole sums come from si3_hole.py in <work_dir>.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 si3_grade.py <work_dir> [--mutate]
kappa = 1/2 FITTED; footings never pooled; cold dark energy is never a particle; the theory stays open."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ["X79_ETA"] = "native"; os.environ.pop("X79_ETAMULT", None); os.environ.pop("X53_MUTATE", None)
import io, json, math, time, resource, contextlib
import numpy as np
from scipy import stats

T00 = time.time(); SHERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(SHERE); REPO = os.path.dirname(REB); sys.path.insert(0, SHERE)
from si3_hole import f2_sections, SAMPLES, F2SRC, DATA
WORK = sys.argv[1]; MUTS = "--mutate" in sys.argv; SFX = "_MUTATE" if MUTS else ""; OUT = []; RES = dict(lane="SI3_nested_isolation", criteria="60575303a2", mutate=MUTS, K={}); KOK = {}
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def Q(s=""): print(s, flush=True); OUT.append(str(s))
def tick(): return f"[{time.time() - T00:.0f} s, {rss():.2f} GB]"
def kchk(name, ok, val): KOK[name] = bool(ok); RES["K"][name] = val; Q(f"{name}: {'PASS' if ok else 'FAIL'}  {val}")

# ===================================================== X79's text, with FC1's replacement, gives X53's text at FC1's rule; SI3's asserted replacements follow
X79F = os.path.join(REB, "X79_native_eta_mw_kids", "x79_kids.py"); FC1F = os.path.join(REB, "FC1_cold_share_native_eta", "fc1_down.py"); T79 = open(X79F).read(); TFC = open(FC1F).read()
GF = dict(json=json, os=os, FRB=REB); exec(compile(TFC[TFC.index("CE = json.load("):TFC.index('if WHAT in ("mw", "kids"):')], FC1F, "exec"), GF); FC, ETAV = GF["FC"], GF["ETAV"]
PAT = '_EV = np.array([_S77["1e+12_ng64"]["eta_med"], _S77["1e+13_ng48"]["eta_med"], _S77["1e+14_ng48"]["eta_med"]])'; assert TFC.count(PAT) == 1 and T79.count(PAT) == 1
T79 = T79.replace(PAT, "_EV = " + f"np.array({[FC * v for v in ETAV]!r})")
G79 = {"__file__": X79F, "__name__": "x79_ro"}; exec(compile(T79[:T79.index('ns = {"__file__": SRC, "__name__": "__main__"}')], X79F, "exec"), G79); SRC = G79["SRC"]; src = G79["src"]
def rep(a, b):
    global src
    assert src.count(a) == 1, (a[:70], src.count(a)); src = src.replace(a, b)
CUT = 'for foot in FOOTS:\n    P(f"\\n=== [{foot}]  a0'; assert src.count(CUT) == 1; src = src[:src.index(CUT)]                                  # definitions only; K1 below calls them
rep('exec(compile(s1 + "\\n" + s4, F2SRC, "exec"), NF)', 'exec(compile(s1 + "\\n" + s4 + "\\n" + _SI3["f2_extra"], F2SRC, "exec"), NF)')            # F2's Track B in the same namespace
rep("    Ms, Mc = 10 ** lm, 10 ** lmc; Mhot = 0.5 * Ms\n", '    Ms, Mc = 10 ** (lm + _SI3["dMs"]), 10 ** lmc; Mhot = 0.5 * 10 ** lm\n')                # R2, SI2's: stars and M200 move, gas stays at catalogue M*
rep("    rcut = 100 * R200 if MUT else R200\n", '    rcut = _SI3["rcut"](M200, R200, Ms + Mc + Mhot)\n')                                               # reported r_ta variant
rep("    return Mb + Mh, (M200, R200, Sig, above)\n", '    return Mb + _SI3["HF"] * Mh, (M200, R200, Sig, above)\n')                                       # MUTATE only
_, _, F2X = f2_sections(open(F2SRC).read()); S3 = dict(dMs=0.0, HF=0.5 if MUTS else 1.0, rcut=lambda M200, R200, Mbt: R200, f2_extra=F2X)
NS = {"__file__": SRC, "__name__": "x53_ro", "_SI3": S3}; argv0 = sys.argv; sys.argv = [SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, SRC, "exec"), NS)
sys.argv = argv0
AQ, NF, stack_model, stack_H, mass_H, halo_setup, B_, fit, esd2h, REX, IDX_ALL, IDX_PRIM, CENTRAL0, H_PRIMARY, Rn, Yn, Cn, T2n, BG, LMG, RGRID_PC, A0, FOOTS, H_NAT = (NS[k] for k in ("AQ", "NF", "stack_model", "stack_H", "mass_H", "halo_setup", "B", "fit", "esd2h", "REX", "IDX_ALL", "IDX_PRIM", "CENTRAL0", "H_PRIMARY", "Rn", "Yn", "Cn", "T2n", "BG", "LMG", "RGRID_PC", "A0", "FOOTS", "H_NAT"))
SAMP, PATCH, LBIN, WG_L, WW_L, RANGE, RMED, table_RM, perlens_model, trackB_stats, T_OM_B, SIGU, ONEK, NP_, CENTRAL, LRT, R70, qB, logMs70, TYP, zl, meff_profile = (NF[k] for k in ("SAMP", "PATCH", "LBIN", "WG_L", "WW_L", "RANGE", "RMED", "table_RM", "perlens_model", "trackB_stats", "T_OM_B", "SIGU", "ONEK", "NPATCH", "CENTRAL", "LRT", "R70", "qB", "logMs70", "TYP", "zl", "meff_profile"))
assert NP_ == 50 and SAMPLES == tuple(k for k in ("S10", "S20", "S30", "S_strict", "S_x300")) and set(SAMPLES) == set(SAMP)
Q(f"SI3_nested_isolation  criteria 60575303a2{'  [MUTATE: halo x 0.5, lens WG x 1.10, I from cross shear]' if MUTS else ''}"); Q("kappa = 1/2 FITTED; footings never pooled; canonical primary; cold dark energy is a gravitating field component")
Q(f"X53 text at FC1's rule: f_c {FC:.5f}, eta(1e12, 1e13, 1e14) from CE1 x f_c = {[round(FC * v, 3) for v in ETAV]}; F2 checks in its Track B text: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in NF["CHK"].items())); Q(tick())
for k_, v_ in NF["CHK"].items():
    if not v_: KOK["F2_" + k_] = False
if MUTS: WG_L *= 1.10                                                  # in place: F2's own functions see it too
H = H_NAT; RED = TYP == 1; SHIFT = 0.295
F2J = json.load(open(os.path.join(REB, "F2_outer_lensing", "f2_outer_lensing_results.json"))); OKL = (LBIN >= 0) & (LBIN < 4); RUNGS = {"R0": 0.0, "R2": SHIFT}; REST = {"h": H}
fdat = (H / 0.70) * T_OM_B * SIGU / ONEK; hart = lambda p: (NP_ - p - 2) / (NP_ - 1); JKF = (NP_ - 1) / NP_
RALL = (RMED > 0.03) & (RMED <= 3.0); RAN = dict(RANGE); RAN["all"] = RALL; Q(f"cells used: all {int(RALL.sum())} (per mass bin {RALL.sum(1).tolist()}); in {int(RANGE['in'].sum())}, O1 {int(RANGE['O1'].sum())}, O2 {int(RANGE['O2'].sum())}")

# ===================================================== K1: X53 at FC1's rule on B21's bins
def blocks_C(C, idx):
    """per mass bin: the 15-bin block of a 60 x 60 matrix, no Hartlap (B21's released matrix)."""
    return [(b, np.array(idx), np.linalg.inv(C[np.ix_(np.array(idx) + 15 * b, np.array(idx) + 15 * b)]), len(idx)) for b in range(4)]
def chi2b(blk, r): return float(sum(r[b, idx] @ Ci @ r[b, idx] for b, idx, Ci, p in blk))
def nnls_b(blk, r, T):
    out = np.zeros(4)
    for b, idx, Ci, p in blk:
        t = T[b, idx]; Ct = Ci @ t; den = float(t @ Ct); out[b] = max(0.0, float(r[b, idx] @ Ct) / den) if den > 0 else 0.0
    return out
REFJ = json.load(open(os.path.join(REB, "FC1_cold_share_native_eta", "x79_rule", "x79_kids_results_native.json")))["footings"]; dk1 = dk1b = 0.0; KR1 = {}
for foot in FOOTS:
    mL = stack_model(foot, Rn, CENTRAL0); mH, _m = stack_H(foot, H_PRIMARY); rows = {}
    for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
        r = {}
        for mk, m, u2 in (("L", mL, False), ("H", mH, False), ("L2H", mL, True), ("H2H", mH, True)):
            o, _f = fit(m, idx, u2); r[mk] = o; ref = REFJ[foot][lab][mk]; dk1 = max(dk1, abs(o["chi2"] - ref["chi2"])); dk1b = max([dk1b] + [abs(a - b) for a, b in zip(o["b"], ref["b"])])
        rows[lab] = dict(L=r["L"]["chi2"], H=r["H"]["chi2"], L2H=r["L2H"]["chi2"], H2H=r["H2H"]["chi2"], dchi2=r["H"]["chi2"] - r["L"]["chi2"], dchi2_2h=r["H2H"]["chi2"] - r["L2H"]["chi2"], b_L=r["L2H"]["b"], b_H=r["H2H"]["b"])
    bk = blocks_C(Cn, IDX_ALL); bL = nnls_b(bk, Yn - mL, T2n); bH = nnls_b(bk, Yn - mH, T2n)
    rows["block_diag_of_released"] = dict(L=chi2b(bk, Yn - mL), H=chi2b(bk, Yn - mH), dchi2=chi2b(bk, Yn - mH) - chi2b(bk, Yn - mL), dchi2_2h=chi2b(bk, Yn - mH - bH[:, None] * T2n) - chi2b(bk, Yn - mL - bL[:, None] * T2n))
    KR1[foot] = rows; a, c = rows["all"], rows["block_diag_of_released"]
    Q(f"  B21's bins [{foot}] all radii, released matrix: chi2 L {a['L']:.1f}, H {a['H']:.1f}, dchi2 {a['dchi2']:+.1f}; two-halo L2H {a['L2H']:.1f}, H2H {a['H2H']:.1f}, dchi2 {a['dchi2_2h']:+.1f}. Its block-diagonal part: dchi2 {c['dchi2']:+.1f}; two-halo {c['dchi2_2h']:+.1f}")
RES["B21_bins_R0"] = KR1; kchk("K1_FC1_kids_chi2_and_b", dk1 <= 1e-9 and dk1b <= 1e-9, f"max |d chi2| {dk1:.1e}, max |d b| {dk1b:.1e} against x79_rule/x79_kids_results_native.json"); Q(tick())

# ===================================================== own stack functions; K0: F2's committed law amplitudes
def psum(S, arr):
    s = np.zeros((NP_, 4, 15)); ok = S & OKL; np.add.at(s, (PATCH[ok], LBIN[ok]), arr[ok]); return s
LSUM = {s: dict(sg=psum(SAMP[s], WG_L), sw=psum(SAMP[s], WW_L), N=int((SAMP[s] & OKL).sum())) for s in SAMPLES}
def ratio(sg, sw, f=1.0):
    tg, tw = sg.sum(0), sw.sum(0)
    with np.errstate(all="ignore"):
        return tg / tw * f, (tg[None] - sg) / (tw[None] - sw) * f
def mstack(s, MOD):
    sm = psum(SAMP[s], WW_L * MOD); sw = LSUM[s]["sw"]; tw = sw.sum(0); tm = sm.sum(0)
    with np.errstate(all="ignore"):
        return tm / tw, (tm[None] - sm) / (tw[None] - sw)
def amps(d, dj, var, m, mj):
    o = {}
    for lab in ("in", "O1", "O2", "out"):
        sel = RAN[lab] & np.isfinite(d) & (var > 0); w = np.where(sel, m / var, 0.0); A = float(np.sum(w * d) / np.sum(w * m))
        Aj = np.sum(w[None] * dj, axis=(1, 2)) / np.sum(w[None] * mj, axis=(1, 2)); o[f"A_{lab}"] = A; o[f"sA_{lab}"] = float(math.sqrt(JKF * np.sum((Aj - Aj.mean()) ** 2)))
    return o
dk0a = dk0b = 0.0; AK = ("A_in", "sA_in", "A_O1", "sA_O1", "A_O2", "sA_O2"); TLAW0 = {}
for foot in FOOTS:
    cfg = dict(CENTRAL, ye="zero"); TLAW0[foot] = table_RM(foot, cfg); o4, MODL = trackB_stats(foot, cfg, TLAW0[foot]); ox, _ = trackB_stats(foot, cfg, TLAW0[foot], samples=("S_x300",)); ref4 = F2J["trackB"][foot]["zero"]; refx = F2J["posthoc"][f"S_x300_{foot}_zero"]
    for s in SAMPLES:
        rf = refx if s == "S_x300" else ref4[s]; rm = ox[s] if s == "S_x300" else o4[s]; dk0a = max([dk0a] + [abs(rm[k] - rf[k]) for k in AK])
        d_, dj_ = ratio(LSUM[s]["sg"], LSUM[s]["sw"], fdat); var_ = JKF * np.sum((dj_ - dj_.mean(0)) ** 2, axis=0); m_, mj_ = mstack(s, MODL); a_ = amps(d_, dj_, var_, m_, mj_); dk0b = max([dk0b] + [abs(a_[k] - rf[k]) for k in AK])
kchk("K0_F2_law_amplitudes", dk0a <= 1e-9 and dk0b <= 1e-9, f"F2's trackB_stats max |d| {dk0a:.1e}; my stack function max |d| {dk0b:.1e}; A_in, A_O1, A_O2 and errors, five samples, both footings, y_e = 0"); Q(tick())

# ===================================================== model tables per footing and rung
def table_H(foot, dMs, rcut=None):
    S3["dMs"] = dMs; S3["rcut"] = rcut if rcut is not None else (lambda M200, R200, Mbt: R200); tab = np.empty((len(LMG), len(LRT))); Rg = np.exp(LRT) * 1e6
    for gi, lm in enumerate(LMG): tab[gi] = AQ.delta_sigma(Rg, RGRID_PC, mass_H(foot, float(lm), H, H_PRIMARY)[0], "const")
    S3["dMs"] = 0.0; S3["rcut"] = lambda M200, R200, Mbt: R200
    return tab
def mix(tR0, tR2):
    """R0 for blue lenses, the R2 table (at catalogue-M* grid coordinates, as SI2's own()) for red ones."""
    m0 = perlens_model(tR0, REST)
    return m0 if tR2 is None else np.where(RED[:, None], perlens_model(tR2, REST), m0)
# reported profile E: SI1's constants and its r_ta line, one z_ta
SI1T = open(os.path.join(REB, "SI1_spec_isolated_route_e", "si1_grade.py")).read(); assert SI1T.count("rta = (3 * (M200 + Mbt) / (4 * math.pi * DTA * RHOM0)) ** (1 / 3) / (1 + ZT); rc = max(rta, R200)") == 1
_l = [x for x in SI1T.splitlines() if x.startswith("NOM, NH, NWB = ")]; assert len(_l) == 1; GS = dict(HB=BG["A_c2b_refit"]["h"]); exec(_l[0], GS); RHOM0, DTA = GS["RHOM0"], GS["DTA"]
_S = SAMP["S_strict"] & OKL; _w = WW_L[_S].sum(1); _z = zl[_S]; _o = np.argsort(_z); ZT = float(_z[_o][np.searchsorted(np.cumsum(_w[_o]), 0.5 * _w.sum())]); RES["z_ta"] = ZT
RCUT_TA = lambda M200, R200, Mbt: max(R200, (3 * (M200 + Mbt) / (4 * math.pi * DTA * RHOM0)) ** (1 / 3) / (1 + ZT))
MS = {}
for foot in FOOTS:
    MS[foot] = {}
    tL2 = table_RM(foot, dict(CENTRAL, ye="zero", dMs=SHIFT)); tH0 = table_H(foot, 0.0); tH2 = table_H(foot, SHIFT)
    tE0, tE2 = (None, None) if MUTS else (table_H(foot, 0.0, RCUT_TA), table_H(foot, SHIFT, RCUT_TA))
    for rg, (mlaw, mh, me) in dict(R0=(mix(TLAW0[foot], None), mix(tH0, None), None if MUTS else mix(tE0, None)), R2=(mix(TLAW0[foot], tL2), mix(tH0, tH2), None if MUTS else mix(tE0, tE2))).items():
        MS[foot][rg] = {s: dict(L=mstack(s, mlaw), H=mstack(s, mh), E=None if me is None else mstack(s, me)) for s in SAMPLES}
    if foot == "canonical":                                             # K2: tables against direct projection, 300 seeded lenses
        rk = np.random.default_rng(20261031 + 2).choice(np.where(SAMP["S10"] & OKL)[0], 300, replace=False); lMn = logMs70 + 2 * np.log10(0.70 / H) + 2 * np.log10(qB); Rnl = R70 * (0.70 / H) * qB[:, None]; dev = 0.0
        mhl = perlens_model(tH0, REST); mll = perlens_model(TLAW0[foot], REST); DH = np.empty((len(rk), 15)); DL = np.empty((len(rk), 15))
        for i, l in enumerate(rk):
            lm = float(lMn[l]); lm70 = lm - 2 * np.log10(0.70 / H); lmc = lm + (-0.69 * lm70 + 6.63); ML, tail = meff_profile(foot, lm, 0.5, 0.0, "zero", logMcold=lmc)
            DH[i] = AQ.delta_sigma(Rnl[l] * 1e6, RGRID_PC, mass_H(foot, lm, H, H_PRIMARY)[0], "const"); DL[i] = AQ.delta_sigma(Rnl[l] * 1e6, RGRID_PC, ML, tail)
        for b in range(4):
            q_ = LBIN[rk] == b; w_ = WW_L[rk][q_]
            for k in np.where(RALL[b])[0]:
                if w_[:, k].sum() > 0:
                    dev = max(dev, abs(np.sum(w_[:, k] * mhl[rk][q_, k]) / np.sum(w_[:, k] * DH[q_, k]) - 1), abs(np.sum(w_[:, k] * mll[rk][q_, k]) / np.sum(w_[:, k] * DL[q_, k]) - 1))
        dm200 = 0.0
        for lmb in (9.5, 10.0, 10.5, 11.0):
            M200, R200, r0_, Sig_, _ab = halo_setup(foot, lmb, H_PRIMARY); dm200 = max(dm200, abs(math.pi * Sig_ * r0_ ** 2 * float(B_(R200 / r0_)) / M200 - 1))
        kchk("K2_tables_and_M200", dev <= 0.01 and dm200 <= 1e-8, f"stacked table against direct projection, max |ratio - 1| {dev:.1e} on 300 lenses; M_h(R200)/M200 - 1 {dm200:.1e}")
    Q(f"  tables done [{foot}] {tick()}")

# two-halo template per lens, X53's exclusion radii and native factor rule (reported only)
Rt = np.exp(LRT); T2TAB = np.array([esd2h(Rt, REX[b]) for b in range(4)]); T2L = np.empty_like(R70)
for b in range(4):
    q_ = LBIN == b; T2L[q_] = np.stack([np.interp(np.log(R70[q_, k]), LRT, T2TAB[b]) for k in range(15)], 1)
T2L *= (H / 0.70) * T_OM_B; T2S = {s: mstack(s, T2L)[0] for s in SAMPLES}; del T2L; Q(f"  two-halo template stacked {tick()}")

# ===================================================== hole sums
HF_ = [os.path.join(WORK, f"si3_hole_{r}.npz") for r in ("north", "south")]; HAVE = all(os.path.exists(f) for f in HF_); HOLE = {}; KH_OK = HAVE
if HAVE:
    Zs = [dict(np.load(f)) for f in HF_]; done = all(all(v == -2 for v in json.loads(str(z["progress_json"])).values()) and len(json.loads(str(z["progress_json"]))) == 10 for z in Zs)
    if not done: HAVE = False; KH_OK = False; Q("hole sums incomplete: Delta lines NOT DONE")
if HAVE:
    for c in [f"I_{s}" for s in SAMPLES] + [f"R_{s}" for s in SAMPLES]:
        HOLE[c] = {k: Zs[0][f"{c}_{k}"] + Zs[1][f"{c}_{k}"] for k in ("WG", "WX", "WW", "NN")}
    if MUTS:
        for c in HOLE: HOLE[c]["WG"] = HOLE[c]["WX"].copy()
    INFOC = json.load(open(os.path.join(WORK, "si3_cats.json"))); RES["cats"] = INFOC["cats"]; cats = np.load(os.path.join(WORK, "si3_cats.npz")); NI = {s: np.bincount(LBIN[cats[f"I_{s}_li"]], minlength=4) for s in SAMPLES}; del cats
    # K_H1: the estimator
    WGm, WWm, W2m, WXm, WGr, WWr, WXr = (Zs[0]["KH1_" + k] + Zs[1]["KH1_" + k] for k in ("WGm", "WWm", "W2m", "WXm", "WGr", "WWr", "WXr")); nkh = len(Zs[0]["KH1_rk"]) + len(Zs[1]["KH1_rk"])
    with np.errstate(all="ignore"):
        sg_ = np.sqrt(W2m) / WWm; dg = np.abs(WGm / WWm - WGr / WWr) / sg_; dx = np.abs(WXm / WWm + WXr / WWr) / sg_
    ww1 = float(abs(WWm.sum() / WWr.sum() - 1)); ok_ = WWm > 0; k_h1 = ww1 <= 1e-6 and np.nanmax(dg[ok_]) <= 1e-3 and np.nanmax(dx[ok_]) <= 1e-3; mx = max(float(Zs[0]["KH1_maxrelWW"]), float(Zs[1]["KH1_maxrelWW"]))
    kchk("K_H1_estimator_vs_record", k_h1, f"{nkh} real lenses: |sum WW ratio - 1| {ww1:.1e}; stacked DeltaSigma max {np.nanmax(dg[ok_]):.1e} sigma; cross (CFG116 sign flipped) max {np.nanmax(dx[ok_]):.1e} sigma; per-lens max rel |dWW| {mx:.1e}; one-side-empty cells {int(Zs[0]['KH1_nzero'] + Zs[1]['KH1_nzero'])}")
    # K_H2 from the catalogue stage
    kchk("K_H2_veto_on_real_lenses", INFOC["K_H2"]["ok"], INFOC["K_H2"]["mismatches"])
    # K_H3: patches, source-weight ratio
    kp = bool(Zs[0]["kh3a"]) and bool(Zs[1]["kh3a"]); rO2 = {}
    for s in SAMPLES:
        nl = np.bincount(LBIN[SAMP[s] & OKL], minlength=4); twl = LSUM[s]["sw"].sum(0) / nl[:, None]; twi = HOLE[f"I_{s}"]["WW"].sum((0, 1)) / NI[s][:, None]
        with np.errstate(all="ignore"): rr = twl / twi
        rO2[s] = {lab: float(np.mean(rr[RAN[lab]])) for lab in ("in", "O1", "O2")}
    RES["weight_ratio_L_over_I_per_centre"] = rO2; k_h3 = kp and all(abs(rO2[s]["O2"] - 1) <= 0.10 for s in SAMPLES)
    kchk("K_H3_patches_and_weight_ratio", k_h3, f"patch labels {kp}; lens/I weight per centre in O2: " + ", ".join(f"{s} {rO2[s]['O2']:.3f}" for s in SAMPLES))
else:
    Q("hole sums absent: Delta lines NOT DONE")

def blocks_J(d, dj, var, mask):
    """SI3's frozen covariance: per mass bin, delete-one jackknife over the used cells, inverted, with Hartlap."""
    out = []
    for b in range(4):
        idx = np.where(mask[b] & np.isfinite(d[b]) & (var[b] > 0))[0]; p = len(idx)
        if p == 0: continue
        X = dj[:, b][:, idx]; X = X - X.mean(0); out.append((b, idx, hart(p) * np.linalg.inv(JKF * X.T @ X), p))
    return out
def hsum(c, k="WG", half=None):
    H_ = HOLE[c]; a = H_[k] if half is None else H_[k][[half]]; w = H_["WW"] if half is None else H_["WW"][[half]]; return a.sum(0), w.sum(0)
DV = {}
def dvec(s, v):
    """data vector and its jackknife replicates; v: L raw lens, D lens - I, LR lens - R."""
    if (s, v) in DV: return DV[(s, v)]
    d, dj = ratio(LSUM[s]["sg"], LSUM[s]["sw"], fdat)
    if v != "L":
        dh, djh = ratio(*hsum(("I_" if v == "D" else "R_") + s), fdat); d, dj = d - dh, dj - djh
    var = JKF * np.sum((dj - dj.mean(0)) ** 2, axis=0); DV[(s, v)] = (d, dj, var); return DV[(s, v)]
if HAVE:
    # K_H4: cross-shear null of Delta; K_H5: two halves of I
    WXL = -np.load(os.path.join(DATA, "cfg116_perlens.npz"))["WX"]; px4 = {}; px5 = {}
    for s in SAMPLES:
        dl, djl = ratio(psum(SAMP[s], WXL), LSUM[s]["sw"], fdat); dh, djh = ratio(*hsum("I_" + s, "WX"), fdat); d_, dj_ = dl - dh, djl - djh; var_ = JKF * np.sum((dj_ - dj_.mean(0)) ** 2, axis=0); bk = blocks_J(d_, dj_, var_, RALL); c_ = chi2b(bk, d_); n_ = sum(x[3] for x in bk); px4[s] = dict(chi2=c_, n=n_, p=float(stats.chi2.sf(c_, n_)))
        da, dja = ratio(*hsum("I_" + s, half=0), fdat); db, djb = ratio(*hsum("I_" + s, half=1), fdat); d_, dj_ = da - db, dja - djb; var_ = JKF * np.sum((dj_ - dj_.mean(0)) ** 2, axis=0); bk = blocks_J(d_, dj_, var_, RALL); c_ = chi2b(bk, d_); n_ = sum(x[3] for x in bk); px5[s] = dict(chi2=c_, n=n_, p=float(stats.chi2.sf(c_, n_)))
    del WXL; kh4 = all(px4[s]["p"] >= 0.001 for s in SAMPLES); kh5 = all(px5[s]["p"] >= 0.001 for s in SAMPLES)
    if not MUTS: kchk("K_H4_cross_null", kh4, ", ".join(f"{s} {px4[s]['chi2']:.1f}/{px4[s]['n']} p {px4[s]['p']:.3g}" for s in SAMPLES))
    kchk("K_H5_halves_of_I", kh5, ", ".join(f"{s} {px5[s]['chi2']:.1f}/{px5[s]['n']} p {px5[s]['p']:.3g}" for s in SAMPLES))
    KH_OK = all(KOK.get(k, False) for k in ("K_H1_estimator_vs_record", "K_H2_veto_on_real_lenses", "K_H3_patches_and_weight_ratio", "K_H5_halves_of_I")) and (MUTS or KOK.get("K_H4_cross_null", False))
Q(tick())

# ===================================================== the statistic
def cls(dx, D, DL2=None, DH2=None):
    DL2 = D * D if DL2 is None else DL2; DH2 = D * D if DH2 is None else DH2
    if D < 3: return "NOT POWERED"
    if dx >= 0 and abs(dx - DL2) <= 4 * math.sqrt(DL2): return "LAW PREFERRED"
    if dx <= 0 and abs(dx + DH2) <= 4 * math.sqrt(DH2): return "ROUTE E PREFERRED"
    return "NEITHER"
def label(dx, D, pH):
    if D < 3: return "NOT POWERED"
    if D >= 5 and dx >= D * D - 4 * D and pH < 0.01: return "LEAD SURVIVES"
    if dx < D * D - 4 * D: return "LEAD GONE"
    return "MIXED"
def compare(d, blk, mL, mH):
    cL, cH, D2 = chi2b(blk, d - mL), chi2b(blk, d - mH), chi2b(blk, mH - mL); n = sum(x[3] for x in blk); D = math.sqrt(max(D2, 0))
    return dict(chi2_L=cL, chi2_H=cH, dchi2=cH - cL, D=D, Q=(cH - cL) / D2 if D2 > 0 else float("nan"), n=n, p_L=float(stats.chi2.sf(cL, n)), p_H=float(stats.chi2.sf(cH, n)), cls=cls(cH - cL, D))
def two_halo(d, blk, mL, mH, T):
    bL, bH = nnls_b(blk, d - mL, T), nnls_b(blk, d - mH, T); fL, fH = mL + bL[:, None] * T, mH + bH[:, None] * T; cL, cH = chi2b(blk, d - fL), chi2b(blk, d - fH); n = sum(x[3] for x in blk)
    bx = nnls_b(blk, fL - mH, T); DL2 = chi2b(blk, fL - mH - bx[:, None] * T); by = nnls_b(blk, fH - mL, T); DH2 = chi2b(blk, fH - mL - by[:, None] * T); D = math.sqrt(max(min(DL2, DH2), 0))
    return dict(chi2_L=cL, chi2_H=cH, dchi2=cH - cL, D=D, D2_lawtrue=DL2, D2_routeEtrue=DH2, b_L=bL.tolist(), b_H=bH.tolist(), p_L=float(stats.chi2.sf(cL, n - 4)), p_H=float(stats.chi2.sf(cH, n - 4)), cls=cls(cH - cL, D, DL2, DH2))
def line(foot, rg, s, v):
    d, dj, var = dvec(s, v); bk = blocks_J(d, dj, var, RALL); M = MS[foot][rg][s]; (mL, mLj), (mH, mHj) = M["L"], M["H"]; c = compare(d, bk, mL, mH)
    o = dict(all=c, inner=compare(d, blocks_J(d, dj, var, RAN["in"]), mL, mH), outer=compare(d, blocks_J(d, dj, var, RAN["out"]), mL, mH), amps_L=amps(d, dj, var, mL, mLj), amps_H=amps(d, dj, var, mH, mHj), two_halo=two_halo(d, bk, mL, mH, T2S[s]))
    sel = RALL & np.isfinite(d) & (var > 0); o["diag_dchi2"] = float(np.sum(((d - mH) ** 2 - (d - mL) ** 2)[sel] / var[sel]))
    o["per_mass_bin_dchi2"] = [float((d - mH)[b, ix] @ Ci @ (d - mH)[b, ix] - (d - mL)[b, ix] @ Ci @ (d - mL)[b, ix]) for b, ix, Ci, p in bk]
    D2 = c["D"] ** 2; qp = np.array([(chi2b(bk, dj[p_] - mHj[p_]) - chi2b(bk, dj[p_] - mLj[p_])) / D2 for p_ in range(NP_)]) if D2 > 0 else np.full(NP_, np.nan); o["sQ_jack"] = float(math.sqrt(JKF * np.sum((qp - qp.mean()) ** 2)))
    if M["E"] is not None:
        mE, _e = M["E"]; ce = compare(d, bk, mL, mE); o["route_E_to_r_ta"] = dict(chi2_H=ce["chi2_H"], dchi2=ce["dchi2"], D=ce["D"], p_H=ce["p_H"], cls=ce["cls"], A=amps(d, dj, var, mE, _e))
    o["_qp"] = qp
    return o
VARS = (("D", "Delta = L - I"), ("L", "raw L")) + ((("LR", "L - R"),) if HAVE else ())
if not HAVE: VARS = (("L", "raw L"),)
TAB = {}
for foot in FOOTS:
    TAB[foot] = {}
    for v, vname in VARS:
        TAB[foot][v] = {}
        for rg in RUNGS:
            TAB[foot][v][rg] = {s: line(foot, rg, s, v) for s in SAMPLES}
            Q(f"\n=== [{foot}] {vname}, {rg}: dchi2 = chi2(route E) - chi2(law), no fitted parameter, block jackknife with Hartlap, 59 cells. Q = dchi2/D^2: +1 law true, -1 route E true")
            for s in SAMPLES:
                o = TAB[foot][v][rg][s]; c = o["all"]; t = o["two_halo"]; e = o.get("route_E_to_r_ta")
                Q(f"  {s:8s} N {LSUM[s]['N']:6d}  chi2 L {c['chi2_L']:7.1f} (p {c['p_L']:.2g})  H {c['chi2_H']:7.1f} (p {c['p_H']:.2g})  dchi2 {c['dchi2']:+8.1f}  D {c['D']:5.2f}  Q {c['Q']:+6.2f} +- {2 / c['D'] if c['D'] > 0 else float('nan'):.2f} (jack {o['sQ_jack']:.2f})  {c['cls']}; inner {o['inner']['dchi2']:+.1f}, outer {o['outer']['dchi2']:+.1f}; diag {o['diag_dchi2']:+.1f}")
                al, ah = o["amps_L"], o["amps_H"]
                Q(f"           law A_in {al['A_in']:.2f}+-{al['sA_in']:.2f} A_O1 {al['A_O1']:.2f}+-{al['sA_O1']:.2f} A_O2 {al['A_O2']:.2f}+-{al['sA_O2']:.2f} | route E A_in {ah['A_in']:.2f}+-{ah['sA_in']:.2f} A_O1 {ah['A_O1']:.2f}+-{ah['sA_O1']:.2f} A_O2 {ah['A_O2']:.2f}+-{ah['sA_O2']:.2f}; per mass bin {np.round(o['per_mass_bin_dchi2'], 1).tolist()}")
                Q(f"           (reported) X53 two-halo: L2H {t['chi2_L']:.1f}, H2H {t['chi2_H']:.1f}, dchi2 {t['dchi2']:+.1f}, D {t['D']:.2f}, {t['cls']}, b_L {np.round(t['b_L'], 2).tolist()}, b_H {np.round(t['b_H'], 2).tolist()}" + ("" if e is None else f"; halo to r_ta: dchi2 {e['dchi2']:+.1f}, D {e['D']:.2f}, {e['cls']}, A_O1 {e['A']['A_O1']:.2f}"))
    Q(f"  {tick()}")
# Q ladder: paired jackknife differences
LADDER = {}
for foot in FOOTS:
    LADDER[foot] = {}
    for v, _n in VARS:
        for rg in RUNGS:
            r = TAB[foot][v][rg]; LADDER[foot][f"{v}|{rg}"] = {f"S10-{s}": dict(d=r["S10"]["all"]["Q"] - r[s]["all"]["Q"], s=float(math.sqrt(JKF * np.sum(((r["S10"]["_qp"] - r[s]["_qp"]) - (r["S10"]["_qp"] - r[s]["_qp"]).mean()) ** 2)))) for s in ("S_strict", "S_x300")}
    Q(f"\nQ(S10) - Q(sample), paired jackknife, each sample's covariance fixed [{foot}]: " + "; ".join(f"{k}: " + ", ".join(f"{a} {b['d']:+.2f}+-{b['s']:.2f}" for a, b in x.items()) for k, x in LADDER[foot].items()))
# hole's own size
IRTAB = {}
if HAVE:
    Q("\nHole's own size: inverse-variance mean over the range, jackknife error, Msun/pc^2 native. I - R is the isolated environment's signal with no central galaxy")
    for s in SAMPLES:
        di, dji = ratio(*hsum("I_" + s), fdat); dr, djr = ratio(*hsum("R_" + s), fdat); dl, djl, varl = dvec(s, "L"); dd, djd, vard = dvec(s, "D"); IRTAB[s] = {}
        vi = JKF * np.sum(((dji - djr) - (dji - djr).mean(0)) ** 2, axis=0)
        for lab in ("O1", "O2"):
            def mean_of(dd_, djj, va):
                sel = RAN[lab] & np.isfinite(dd_) & (va > 0); w = np.where(sel, 1 / np.where(va > 0, va, 1), 0.0); m = float(np.sum(w * dd_) / np.sum(w)); mj = np.sum(w[None] * djj, axis=(1, 2)) / np.sum(w); return m, float(math.sqrt(JKF * np.sum((mj - mj.mean()) ** 2)))
            IRTAB[s][lab] = dict(I_minus_R=mean_of(di - dr, dji - djr, vi), L=mean_of(dl, djl, varl), R=mean_of(dr, djr, vi), Delta=mean_of(dd, djd, vard))
        Q(f"  {s:8s} " + "  ".join(f"{lab}: I-R {IRTAB[s][lab]['I_minus_R'][0]:+.3f}+-{IRTAB[s][lab]['I_minus_R'][1]:.3f}, R {IRTAB[s][lab]['R'][0]:+.3f}+-{IRTAB[s][lab]['R'][1]:.3f}, L {IRTAB[s][lab]['L'][0]:+.3f}+-{IRTAB[s][lab]['L'][1]:.3f}, L-I {IRTAB[s][lab]['Delta'][0]:+.3f}+-{IRTAB[s][lab]['Delta'][1]:.3f}" for lab in ("O1", "O2")))

# ===================================================== verdict
ALLK = ["K0_F2_law_amplitudes", "K1_FC1_kids_chi2_and_b", "K2_tables_and_M200"]; KPASS = all(KOK.get(k, False) for k in ALLK) and all(v for k, v in KOK.items() if k.startswith("F2_"))
def lab_line(foot, v, rg, s):
    c = TAB[foot][v][rg][s]["all"]; return label(c["dchi2"], c["D"], c["p_H"])
RES["checks_pass"] = KPASS; RES["hole_done"] = bool(HAVE and KH_OK)
if not KPASS:
    VERD = "NO VERDICT"
elif not HAVE:
    VERD = "NOT DONE (no hole term)"
elif not KH_OK:
    VERD = "NO VERDICT (hole-term check failed)"
else:
    a = lab_line("canonical", "D", "R2", "S_strict"); b = lab_line("canonical", "D", "R2", "S_x300"); VERD = {"LEAD SURVIVES": "LEAD SURVIVES STRICT ISOLATION", "LEAD GONE": "LEAD GONE AT STRICT ISOLATION", "NOT POWERED": "NOT POWERED", "MIXED": "MIXED"}[a] + ("" if a == b else f"; S_x300 differs: {b}")
RES["verdict"] = VERD; Q(f"\nVERDICT (frozen; canonical, R2, Delta = L - I, S_strict): {VERD}")
SHOW = "D" if HAVE else "L"
for foot in FOOTS:
    for rg in RUNGS:
        Q(f"  [{foot} {rg}, {'Delta' if HAVE else 'raw L'}] labels: " + ", ".join(f"{s} {lab_line(foot, SHOW, rg, s)}" for s in SAMPLES))

# ===================================================== Argon's lines
def argon(v="D", stat="all"):
    r = TAB["canonical"][v]["R2"]; g = lambda s: r[s]["two_halo"] if stat == "two_halo" else r[s]["all"]; o = {}
    for s, lo, hi in (("S10", 280, 350), ("S30", 80, 140), ("S_strict", -5, 15)):
        o[s] = dict(dchi2=g(s)["dchi2"], band=[lo, hi], score="HIT" if lo <= g(s)["dchi2"] <= hi else "MISS")
    ss = r["S_strict"]; aH, aL = ss["amps_H"], ss["amps_L"]; x = g("S_strict")["dchi2"]; D_ = g("S_strict")["D"]
    o["A_O1_data_over_routeE"] = dict(value=aH["A_O1"], err=aH["sA_O1"], band=[1.10, 1.60], score="HIT" if 1.10 <= aH["A_O1"] <= 1.60 else "MISS")
    o["A_O2_data_over_law"] = dict(value=aL["A_O2"], err=aL["sA_O2"], line=0.35, score="HIT" if aL["A_O2"] <= 0.35 else "MISS")
    pm = lambda a_: abs(a_["A_O2"] - 1) <= 2 * a_["sA_O2"]
    o["pass_line"] = dict(dchi2_at_or_below_15=x <= 15, A_O2_routeE=[aH["A_O2"], aH["sA_O2"]], A_O2_routeE_within_2sigma_of_1=bool(pm(aH)), A_O2_law=[aL["A_O2"], aL["sA_O2"]], A_O2_law_within_2sigma_of_1=bool(pm(aL)), met_on_routeE_reading=bool(x <= 15 and pm(aH)))
    o["fail_line"] = dict(D=D_, dchi2=x, met=bool(D_ >= 5 and x >= 25)); o["falsifier_above_30"] = bool(x > 30)
    return o
if HAVE:
    RES["argon"] = dict(graded=argon("D", "all"), two_halo=argon("D", "two_halo"))
    for nm, A_ in (("graded statistic", RES["argon"]["graded"]), ("X53 two-halo line (reported)", RES["argon"]["two_halo"])):
        Q(f"\nArgon's lines at R2, Delta = L - I, canonical, on the {nm}:")
        for s in ("S10", "S30", "S_strict"): Q(f"  {s}: dchi2 {A_[s]['dchi2']:+.1f}, band {A_[s]['band']}: {A_[s]['score']}")
        Q(f"  S_strict A_O1 data/route E {A_['A_O1_data_over_routeE']['value']:.2f}+-{A_['A_O1_data_over_routeE']['err']:.2f}, band 1.10 to 1.60: {A_['A_O1_data_over_routeE']['score']}; A_O2 data/law {A_['A_O2_data_over_law']['value']:.2f}+-{A_['A_O2_data_over_law']['err']:.2f}, at or below 0.35: {A_['A_O2_data_over_law']['score']}")
        Q(f"  pass line: dchi2 <= +15 {A_['pass_line']['dchi2_at_or_below_15']}; A_O2 route E {A_['pass_line']['A_O2_routeE'][0]:.2f}+-{A_['pass_line']['A_O2_routeE'][1]:.2f} within 2 sigma of 1: {A_['pass_line']['A_O2_routeE_within_2sigma_of_1']}; (law's {A_['pass_line']['A_O2_law'][0]:.2f}+-{A_['pass_line']['A_O2_law'][1]:.2f}: {A_['pass_line']['A_O2_law_within_2sigma_of_1']}); met on route E's reading: {A_['pass_line']['met_on_routeE_reading']}")
        Q(f"  fail line (D >= 5, dchi2 >= +25): D {A_['fail_line']['D']:.2f}, dchi2 {A_['fail_line']['dchi2']:+.1f}: met {A_['fail_line']['met']}; falsifier (above +30): {A_['falsifier_above_30']}")
else:
    RES["argon"] = "NOT SCORED: the predictions are for Delta = L - I"; Q("\nArgon's lines: not scored; they are for Delta = L - I, and no hole term was built")

# ===================================================== outputs
for foot in FOOTS:
    for v in TAB[foot]:
        for rg in TAB[foot][v]:
            for s in TAB[foot][v][rg]:
                TAB[foot][v][rg][s].pop("_qp", None)
PROF = {}
for foot in FOOTS:
    PROF[foot] = {}
    for s in SAMPLES:
        d, dj, var = dvec(s, SHOW); PROF[foot][s] = dict(d=d.tolist(), sig=np.sqrt(var).tolist(), m_L_R0=MS[foot]["R0"][s]["L"][0].tolist(), m_H_R0=MS[foot]["R0"][s]["H"][0].tolist(), m_L_R2=MS[foot]["R2"][s]["L"][0].tolist(), m_H_R2=MS[foot]["R2"][s]["H"][0].tolist())
RES["lines"] = TAB; RES["ladder"] = LADDER; RES["hole_size"] = IRTAB; RES["profiles_Delta_or_raw"] = PROF; RES["Rmed_h70"] = RMED.tolist(); RES["N"] = {s: LSUM[s]["N"] for s in SAMPLES}; RES["red_fraction"] = {s: float(RED[SAMP[s] & OKL].mean()) for s in SAMPLES}
Q(f"\nred fraction: " + ", ".join(f"{s} {RES['red_fraction'][s]:.3f}" for s in SAMPLES) + f"; z_ta {ZT:.3f}")
if MUTS:
    B0 = json.load(open(os.path.join(SHERE, "si3_results.json"))); bite = {}
    for s in SAMPLES:
        c0 = B0["lines"]["canonical"][SHOW]["R0"][s]["all"]; c1 = TAB["canonical"][SHOW]["R0"][s]["all"]
        m0 = np.array(B0["profiles_Delta_or_raw"]["canonical"][s]["m_H_R0"]); m1 = MS["canonical"]["R0"][s]["H"][0]; bite[s] = dict(mH_lower_in_every_used_cell=bool(np.all(m1[RALL] < m0[RALL])), chi2H_changed=abs(c1["chi2_H"] - c0["chi2_H"]) > 1e-3, data_changed=bool(np.nanmax(np.abs(np.array(B0["profiles_Delta_or_raw"]["canonical"][s]["d"])[RALL] - dvec(s, SHOW)[0][RALL])) > 1e-3))
    okm = (not KOK["K0_F2_law_amplitudes"]) and (not KOK["K1_FC1_kids_chi2_and_b"]) and VERD.startswith("NO VERDICT") and all(all(v.values()) for v in bite.values()); RES["mutate_bites"] = dict(ok=okm, K0_failed=not KOK["K0_F2_law_amplitudes"], K1_failed=not KOK["K1_FC1_kids_chi2_and_b"], verdict=VERD, per_sample=bite); Q(f"\nMUTATE bites: {'PASS' if okm else 'FAIL'}  K0 failed {not KOK['K0_F2_law_amplitudes']}, K1 failed {not KOK['K1_FC1_kids_chi2_and_b']}, verdict {VERD}; per sample {bite}")
nK = len(KOK); Q(f"\nchecks {sum(KOK.values())}/{nK}; runtime {time.time() - T00:.0f} s; peak RSS {rss():.2f} GB"); RES["checks"] = KOK
json.dump(RES, open(os.path.join(SHERE, f"si3_results{SFX}.json"), "w"), indent=1, default=float); open(os.path.join(SHERE, f"si3{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(KOK.values()) else 1)
