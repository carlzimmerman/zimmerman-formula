#!/usr/bin/env python3
"""SRH1 (FROZEN_CRITERIA.md, 5ed8a37ec6): G2 (RC100 coverage, FLD1 line b) and G3 (SPARC coverage, FLD1 line a1; then PD1's
P2-SPARC line with truncation at R_set) for R_set = f R_fold(z, M_b); reported: the family-layout SPARC reading (s-scaled law
inside R_set, FRZ1's NFW reference outside) and s; KA-G2, KA-G3, KA-G3b; MUTATE MU2 (f 0.05), MU3b (R_fold read at 3.1 - z).
Executed read-only from their own paths: srh1_hm.py's prefix (FZS1's rfold_kpc, FRZ1's halo model), FLD1's fld1_compare.py
(sparc, rc100), PD1's pd1.py up to "def xcop(" (QX8 SPARC fit, sparc, share table). Nothing is written outside this folder.
  nice -n 10 python3 srh1_rc.py -> srh1_rc.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
# --- srh1_hm prefix: rfold_kpc and FRZ1's namespace
SRC = os.path.join(HERE, "srh1_hm.py"); src = open(SRC).read()
H = {"__file__": SRC, "__name__": "srh1_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------ checkpointed run\n")], SRC, "exec"), H)
rfold_kpc, FR = H["rfold_kpc"], H["F"]
FB, hh, XTAB = FR["FB"], FR["h"], FR["XTAB"]
# --- FLD1's inputs
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach")
sp_ = importlib.util.spec_from_file_location("fld1_compare_ro", os.path.join(FLD, "fld1_compare.py")); FC = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(FC)
SPF = FC.sparc(); RC = FC.rc100(); FLDJ = json.load(open(os.path.join(FLD, "fld1_compare.json")))
# --- PD1's prefix (functions only)
PD = os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust"); PSRC = os.path.join(PD, "pd1.py"); ps = open(PSRC).read()
PN = {"__file__": PSRC, "__name__": "pd1_lib"}; _a = sys.argv; sys.argv = [PSRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(ps[:ps.index("def xcop(a0, tab, trunc=True):")], PSRC, "exec"), PN)
sys.argv = _a
GALS, PRE, glaw, Mph, G, MS, KPC, MPC, A0 = (PN[k] for k in ("GALS", "PRE", "glaw", "Mph", "G", "MS", "KPC", "MPC", "A0"))
PDJ = json.load(open(os.path.join(PD, "pd1.json")))
FOOTS = ("canonical", "alt"); FGRID = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00, 1.25, 1.50, 2.00]
P(f"SRH1 G2 / G3. kappa = 1/2 FITTED; not theory closed. SPARC (FLD1 loader) {len(SPF)}, RC100 {len(RC)}, SPARC (PD1 / QX8) {len(GALS)}")
RES = dict(lane="SRH1", part="G2 G3", criteria="5ed8a37ec6", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", foot={})

# --- NFW reference at z = 0 (FRZ1's galaxy-regime Rb), physical metres
set_z, hbz, conc_of = FR["set_z"], FR["halo_basics_z"], None
FR["set_z"](0.0); CONC0 = FR["L"]["conc"]; DTA0 = FR["dta_of"](0.0); OMZ0 = FR["Omz"](0.0); m_nfw = FR["m_nfw"]
_HC = {}
def ref_halo(Mb_sun, X):
    key = (round(math.log10(Mb_sun), 6), X)
    if key not in _HC:
        Mta = X * Mb_sun * hh / (1 - FB)
        lM = brentq(lambda l: hbz(10 ** l, CONC0, DTA0, OMZ0)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = hbz(10 ** lM, CONC0, DTA0, OMZ0); _HC[key] = (hb["rs"] / hh * MPC, hb["rta"] / hh * MPC, hb["rta"] / hb["rs"])
    return _HC[key]
def CR(r, Mb_sun, X):
    rs, rta, cta = ref_halo(Mb_sun, X); r = np.minimum(np.asarray(r, float), rta)
    return X * Mb_sun * MS * m_nfw(r / rs) / m_nfw(cta)

def sparc_mode(ft, f, mode):
    """PD1's sparc() body (copied) with the halo replaced: mode 'trunc' (PD1's form at R_set), 'family' (s-scaled law inside,
    NFW reference outside), 'law' (no end)."""
    a0 = A0[ft]; X = XTAB[ft]["z0.0"]; rows = []; svals = []
    for q, Tf in zip(GALS, PRE[ft]):
        R = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mbs = max(float(np.max(np.clip(VB2 * R / PN["G_KPC"], 0, None))), 1e3); g = q["GB"]
        rset = f * rfold_kpc(ft, 0.0, math.log10(Mbs)) * KPC if math.isfinite(f) else math.inf
        if mode == "law" or not math.isfinite(rset):
            ge = glaw(g, a0); rt = math.inf
        elif mode == "trunc":
            rt = rset; gt = G * Mbs * MS / rt ** 2; ph_t = float(glaw(gt, a0)) - gt
            ge = np.where((Rm < rt)[:, None], glaw(g, a0), g + ph_t * (rt / Rm[:, None]) ** 2)
        else:
            rs, rta, cta = ref_halo(Mbs, X); rt = min(rset, rta)
            cb = min(Mph(rt, Mbs * MS, a0), X * Mbs * MS); s = float(CR(rt, Mbs, X)) / cb; svals.append(s)
            ge = np.where((Rm < rt)[:, None], g + s * (glaw(g, a0) - g), g + (G * CR(Rm, Mbs, X) / Rm ** 2)[:, None])
        lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k], rt / KPC, float(Rm[-1] / KPC)))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
    o = dict(all=pooled(range(len(rows))), massive=pooled(massive), n_trunc_inside_Rlast=int(sum(r[3] < r[4] for r in rows)))
    o["line"] = bool(o["all"]["rms"] <= 0.0660 and abs(o["all"]["mean"]) <= 0.05 and o["massive"]["rms"] <= 0.0660 and abs(o["massive"]["mean"]) <= 0.05)
    if svals: o["s_median_5_95"] = [float(np.median(svals)), float(np.percentile(svals, 5)), float(np.percentile(svals, 95))]
    return o

# --- KA-G3b: PD1's own sparc() with its share table, and truncation off
ka3b = {}
for ft in FOOTS:
    tab = PDJ[ft]["share_tables"]["z0.0"]
    with contextlib.redirect_stdout(io.StringIO()):
        a = PN["sparc"](ft, A0[ft], tab); b = PN["sparc"](ft, A0[ft], tab, trunc=False)
    st = PDJ[ft]["P2_SPARC"]
    ka3b[ft] = dict(rms=a["all"]["rms"], stored=st["all"]["rms"], rms_off=b["all"]["rms"], stored_off=st["L0"]["all"]["rms"],
                    pass_=bool(abs(a["all"]["rms"] - st["all"]["rms"]) <= 5e-4 and abs(b["all"]["rms"] - st["L0"]["all"]["rms"]) <= 5e-4))
    lw = sparc_mode(ft, math.inf, "law"); ka3b[ft]["law_mode_rms"] = lw["all"]["rms"]
    P(f"KA-G3b [{ft}] PD1 sparc(): rms {a['all']['rms']:.5f} vs stored {st['all']['rms']:.5f}; truncation off {b['all']['rms']:.5f} vs {st['L0']['all']['rms']:.5f}; this lane's law mode {lw['all']['rms']:.5f} -> {'PASS' if ka3b[ft]['pass_'] else 'FAIL'}")
RES["KA_G3b"] = ka3b

for ft in FOOTS:
    R = RES["foot"][ft] = {}
    # G2
    r22 = np.array([2.2 * g["Re"] / rfold_kpc(ft, g["z"], g["logM"]) for g in RC]); r4 = r22 * 4 / 2.2
    rr = np.array([2.2 * g["Re"] / rfold_kpc(ft, 3.1 - g["z"], g["logM"]) for g in RC])
    oog = sum(not (6.5 <= g["logM"] <= 12) for g in RC)
    R["G2"] = dict(f_min_2p2Re=float(r22.max()), f_min_4Re=float(r4.max()), worst=RC[int(r22.argmax())]["name"], out_of_grid=int(oog),
                   covered_2p2=[float(np.mean(r22 <= f)) for f in FGRID], covered_4=[float(np.mean(r4 <= f)) for f in FGRID],
                   MU3b_f_min=float(rr.max()), MU3b_bites=bool(abs(rr.max() / r22.max() - 1) >= 0.10))
    fw = FLDJ["footings"][ft]["RC100"]["worst"][0]
    R["KA_G2"] = dict(f1_worst=float(r22.max()), FLD1=fw["ratio_2.2"], f1_worst4=float(r4.max()), FLD1_4=fw["ratio_4"], n_beyond_f1=int((r22 > 1).sum()),
                      pass_=bool(abs(r22.max() - fw["ratio_2.2"]) <= 1e-6 and abs(r4.max() - fw["ratio_4"]) <= 1e-6 and (r22 > 1).sum() == 0))
    P(f"[{ft}] G2 RC100: f >= {r22.max():.4f} at 2.2 R_e ({R['G2']['worst']}); 4 R_e needs {r4.max():.4f}; out of FLD1 grid {oog}; "
      f"KA-G2 {r22.max():.6f} vs FLD1 {fw['ratio_2.2']:.6f}, 4 R_e {r4.max():.6f} vs {fw['ratio_4']:.6f} -> {'PASS' if R['KA_G2']['pass_'] else 'FAIL'}; "
      f"MU3b (R_fold at 3.1 - z): f_min {rr.max():.4f} -> {'bites' if R['G2']['MU3b_bites'] else 'DOES NOT BITE'}")
    P(f"[{ft}] G2 fraction covered at 2.2 / 4 R_e per f: " + "; ".join(f"{f:.2f}: {a:.2f} / {b:.2f}" for f, a, b in zip(FGRID, R["G2"]["covered_2p2"], R["G2"]["covered_4"])))
    # G3 (a)
    ratio = np.array([g["R_last"] / rfold_kpc(ft, 0.0, math.log10(0.5 * g["L36"] + 1.33 * g["MHI"])) for g in SPF])
    oog3 = sum(not (6.5 <= math.log10(0.5 * g["L36"] + 1.33 * g["MHI"]) <= 12) for g in SPF)
    fs = FLDJ["footings"][ft]["SPARC"]["worst"][0]
    R["G3a"] = dict(f_min=float(ratio.max()), worst=SPF[int(ratio.argmax())]["name"], out_of_grid=int(oog3), covered=[float(np.mean(ratio <= f)) for f in FGRID])
    R["KA_G3"] = dict(f1_worst=float(ratio.max()), FLD1=fs["ratio"], n=len(SPF), pass_=bool(abs(ratio.max() - fs["ratio"]) <= 1e-6 and len(SPF) == 175))
    P(f"[{ft}] G3(a) SPARC: f >= {ratio.max():.4f} ({R['G3a']['worst']}); out of grid {oog3}; KA-G3 {ratio.max():.6f} vs FLD1 {fs['ratio']:.6f} -> {'PASS' if R['KA_G3']['pass_'] else 'FAIL'}")
    # G3 (b) where (a) fails, and the family-layout reading at every f (reported); MU2 at f 0.05
    R["G3b"] = {}; R["family"] = {}; R["G3_pass"] = {}; R["G2_pass"] = {}
    for f in FGRID + [0.05]:
        key = f"{f:.2f}"; a_ok = bool(ratio.max() <= f)
        if not a_ok: R["G3b"][key] = sparc_mode(ft, f, "trunc")
        R["G3_pass"][key] = bool(a_ok or R["G3b"][key]["line"]); R["G2_pass"][key] = bool(r22.max() <= f)
        if f != 0.05:
            R["family"][key] = sparc_mode(ft, f, "family"); fam = R["family"][key]
            P(f"[{ft}] f {key}: G2 {'pass' if R['G2_pass'][key] else 'FAIL'}; G3(a) {'pass' if a_ok else 'fail'}"
              + ("" if a_ok else f", G3(b) rms {R['G3b'][key]['all']['rms']:.4f} mean {R['G3b'][key]['all']['mean']:+.4f} massive {R['G3b'][key]['massive']['rms']:.4f} -> {'pass' if R['G3b'][key]['line'] else 'FAIL'}")
              + f" => G3 {'PASS' if R['G3_pass'][key] else 'FAIL'} | family layout (reported): rms {fam['all']['rms']:.4f} mean {fam['all']['mean']:+.4f} massive {fam['massive']['rms']:.4f} "
              f"line {'holds' if fam['line'] else 'FAILS'}; s median {fam['s_median_5_95'][0]:.3f} (5-95 % {fam['s_median_5_95'][1]:.3f}-{fam['s_median_5_95'][2]:.3f})")
    R["MU2_bites"] = bool(not R["G2_pass"]["0.05"] or not R["G3_pass"]["0.05"])
    P(f"[{ft}] MU2 (f 0.05): G2 {'pass' if R['G2_pass']['0.05'] else 'FAIL'}, G3 {'pass' if R['G3_pass']['0.05'] else 'FAIL'} -> {'bites' if R['MU2_bites'] else 'DOES NOT BITE'}")
    # tilt (reported): coverage lower limits on f0 for f = f0 (1 + z)^beta
    R["tilt"] = {}
    for beta in (-1.0, -0.5, 0.5):
        g2 = max(2.2 * g["Re"] / (rfold_kpc(ft, g["z"], g["logM"]) * (1 + g["z"]) ** beta) for g in RC); g3 = float(ratio.max())
        R["tilt"][f"{beta:+.1f}"] = dict(f0_min_G2=float(g2), f0_min_G3a=g3)
    P(f"[{ft}] tilt (reported) f0 lower limits G2 / G3(a): " + "; ".join(f"beta {k}: {v['f0_min_G2']:.3f} / {v['f0_min_G3a']:.3f}" for k, v in R["tilt"].items()))
json.dump(RES, open(os.path.join(HERE, "srh1_rc.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "srh1_rc.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
