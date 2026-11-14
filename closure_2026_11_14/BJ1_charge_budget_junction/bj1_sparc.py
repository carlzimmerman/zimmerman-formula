#!/usr/bin/env python3
"""BJ1 (FROZEN_CRITERIA.md 9e7ce0dfe6, section 2, G-RC): SPARC rotation curves with the charge-budget junction at z = 0.
A copy of XJ1's xj1_sparc.py (closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface; PD1's sparc(), QX8's loader,
grid of mass-to-light ratios and exact-field term read as PD1 reads them, per-galaxy best mass-to-light ratio, pooled
weighted rms and mean, all 175 galaxies and the massive tail V_flat >= 250 km/s) with the model of the criteria in place
of XJ1's factor s:
    g = glaw(g_N)                 for r <= R_set
    g = g_N + G M_b C(r) / r^2    for r >  R_set
C (in units of M_b) and R_set from bj1_lens.py's profile_B (SRH1's lens profile chain, XJ1's caustic reader) at z = 0 and
the galaxy's M_b (PD1's: the largest enclosed baryon mass at mass-to-light 0.5), JNT2's boundary as the lens chain
applies it (v_L(M_b, 0) > v*(0): the reference at every radius, g = g_N + G M_b C_R(r) / r^2). QX8's exact-field term is
added to log g at every point, as xj1_sparc.py adds it to its model (a reported variant adds it only inside R_set).
PD1's gate: rms <= L0 + 0.010 and |mean| <= 0.05, all galaxies and the massive tail.
Known answer (viii): R_set = infinity for every galaxy (cap charge infinite) reproduces PD1's stored L0 to 1e-9.
Reported: galaxies whose last measured point lies beyond R_set, names and ratios, at mass-to-light 0.5, 0.3 and 0.8
(M_b and R_set recomputed at each, as XJ1's xj1_contain.py recomputes M_b).
  nice -n 19 python3 -I -B bj1_sparc.py -> bj1_sparc.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
# ---------------- PD1's constants and QX8's loader, as PD1 reads them
G, MS, PC = 6.6743e-11, 1.98892e30, 3.0857e16; KPC = 1e3 * PC; G_KPC = 4.3009172706e-6
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; FOOTS = ("canonical", "alt")
def glaw(g, a0): g = np.asarray(g, float); return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))
CL6 = os.path.join(REPO, "closure_2026_11_06")
sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field")); a_ = sys.argv; sys.argv = [a_[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import qx8 as Q8
sys.argv = a_
GALS = Q8.load_sparc(); lU, lN = np.log(Q8.UPS), np.log(Q8.NODES)
PRE = {f: [np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])]) for T in (np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False)["T"] for i in range(len(GALS)))] for f in FOOTS}
PD1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")))
# ---------------- BJ1's lens prefix (SRH1's profile chain, XJ1's shell runs and reader, profile_B), executed read-only
SRC = os.path.join(HERE, "bj1_lens.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "bj1_lens_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# ---------------- JNT2's boundary (main mode), copied")], SRC, "exec"), S)
profile_B, halo, JC = S["profile_B"], S["halo"], S["C"]; GS, MSUN = S["S"]["G"], S["S"]["Msun"]       # SRH1's (ONE1's) SI constants
KPC_S = 3.0857e19
def Mb_of(q):
    R = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
    return max(float(np.max(np.clip(VB2 * R / G_KPC, 0, None))), 1e3)
def model_of(ft, lMb, k):
    """(R_set in kpc, function R_kpc -> G M_b C(r) / r^2 in m/s^2, info) for one galaxy at z = 0; k = None: the law everywhere."""
    if k is None: return math.inf, None, dict(branch="law")
    above = JC.vL_kms(10 ** lMb, 0.0) > JC.vstar_kms(ft, 0.0, "main")
    pc, M3, inf = profile_B(ft, lMb, 0.0, 0 if above else k); rM = inf["rM"]
    Mb = 10 ** lMb * MSUN
    gC = lambda Rk: GS * Mb * M3(np.asarray(Rk) * KPC_S / rM) / (np.asarray(Rk) * KPC_S) ** 2
    return inf["xset"] * rM / KPC_S, gC, dict(inf, above=bool(above), Rset_kpc=inf["xset"] * rM / KPC_S, Rk_kpc=inf.get("xk", 0.0) * rM / KPC_S, Rfold_kpc=inf["xf"] * rM / KPC_S)
def sparc(f, models, tf_inside_only=False):
    """PD1's sparc() without truncation; models[i] = (R_set kpc, gC, info): the law inside R_set, g_N + gC beyond."""
    a0 = A0[f]; rows = []; ups = []
    for q, Tf, (Rs, gC, _) in zip(GALS, PRE[f], models):
        g = q["GB"]; inside = (q["R"] <= Rs)[:, None]
        ge = np.where(inside, glaw(g, a0), g + (gC(q["R"])[:, None] if gC is not None else 0.0))
        lgp = np.log10(np.maximum(ge, 1e-300)) + (np.where(inside, Tf, 0.0) if tf_inside_only else Tf); OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k])); ups.append(float(Q8.UPS[k]))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
    return dict(all=pooled(range(len(rows))), massive=pooled(massive), n_massive=len(massive), U_median=float(np.median(ups)),
                U_at_top=int(sum(1 for u in ups if u >= float(Q8.UPS[-1]) - 1e-9)), U_at_bottom=int(sum(1 for u in ups if u <= float(Q8.UPS[0]) + 1e-9)))
def gate(st, L0):
    ok = (st["all"]["rms"] <= L0["all"]["rms"] + 0.010 and abs(st["all"]["mean"]) <= 0.05 and st["massive"]["rms"] <= L0["massive"]["rms"] + 0.010 and abs(st["massive"]["mean"]) <= 0.05)
    return "PASS" if ok else "FAIL"

def lMb_at(q, ups):
    VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + ups * q["Vdisk"] ** 2 + 1.4 * ups * q["Vbul"] ** 2
    return math.log10(max(float(np.max(np.clip(VB2 * q["R"] / G_KPC, 0, None))), 1e3))
RES = dict(lane="BJ1", part="G-RC: SPARC with the charge-budget junction at z = 0", criteria="9e7ce0dfe6", n_galaxies=len(GALS),
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.", footings={})
lMb = np.array([math.log10(Mb_of(q)) for q in GALS])
assert max(abs(lMb[i] - lMb_at(q, 0.5)) for i, q in enumerate(GALS)) < 1e-12
P(f"BJ1 G-RC, SPARC with the charge-budget junction at z = 0. {len(GALS)} galaxies; log M_b {lMb.min():.2f} to {lMb.max():.2f}, median {np.median(lMb):.2f}")
kaok = True
for ft in FOOTS:
    L0s = PD1[ft]["P2_SPARC"]["L0"]; base = sparc(ft, [model_of(ft, float(lm), None) for lm in lMb])
    dv = max(abs(base[a][b] - L0s[a][b]) for a in ("all", "massive") for b in ("rms", "mean")); kaok &= dv <= 1e-9
    P(f"[{ft}] known answer (viii), R_set = infinity against PD1's stored L0: rms {base['all']['rms']:.6f} (stored {L0s['all']['rms']:.6f}), massive {base['massive']['rms']:.6f} (stored {L0s['massive']['rms']:.6f}); max abs dev {dv:.1e} -> {'PASS' if dv <= 1e-9 else 'FAIL'}; median mass-to-light {base['U_median']:.2f}")
    R = dict(L0=base, KA_viii_dev=dv, KA_viii_pass=bool(dv <= 1e-9), cases={})
    for k in (1, 2, 3):
        nm = f"B{k}"
        models = [model_of(ft, float(lm), k) for lm in lMb]
        st = sparc(ft, models); w = gate(st, base); st2 = sparc(ft, models, tf_inside_only=True)
        info = [m[2] for m in models]
        nab = sum(1 for i_ in info if i_["above"]); nun = sum(1 for i_ in info if i_["branch"] == "under"); nov = sum(1 for i_ in info if i_["branch"] == "over")
        rf = np.array([i_["Rset_kpc"] / i_["Rfold_kpc"] for i_ in info if i_["branch"] in ("under", "over")])
        beyond = {}
        for ups in (0.5, 0.3, 0.8):
            rows = []
            for q in GALS:
                lm = lMb_at(q, ups); Rs, _, ii = model_of(ft, lm, k); rows.append((q["name"], float(q["R"][-1]) / Rs if Rs > 0 else math.inf, ii["branch"], lm))
            v = np.array([x[1] for x in rows]); j = int(np.argmax(v))
            beyond[f"ups{ups}"] = dict(n_beyond=int((v > 1).sum()), beyond=[(rows[i][0], round(float(v[i]), 3), rows[i][2], round(rows[i][3], 2)) for i in np.argsort(-v) if v[i] > 1],
                                       worst=rows[j][0], worst_ratio=float(v[j]), median_ratio=float(np.median(v)))
        R["cases"][nm] = dict(st, word=w, line_all=base["all"]["rms"] + 0.010, line_massive=base["massive"]["rms"] + 0.010,
                              n_above_vstar=nab, n_under=nun, n_over=nov, Rset_over_Rfold_min_med_max=[float(rf.min()), float(np.median(rf)), float(rf.max())] if len(rf) else None,
                              beyond_Rset=beyond, variant_Tf_inside_only=dict(st2, word=gate(st2, base)))
        b5 = beyond["ups0.5"]
        P(f"[{ft}] {nm}: G-RC {w}  rms {st['all']['rms']:.4f} (line {base['all']['rms'] + 0.010:.4f}; law {base['all']['rms']:.4f}) mean {st['all']['mean']:+.4f}; massive rms {st['massive']['rms']:.4f} (line {base['massive']['rms'] + 0.010:.4f}) mean {st['massive']['mean']:+.4f}; "
          f"fitted median mass-to-light {st['U_median']:.2f} (law {base['U_median']:.2f}), {st['U_at_top']} at the grid's top (law {base['U_at_top']})")
        P(f"[{ft}] {nm}: branches under {nun} / over {nov} / above v* {nab}; R_set / R_fold min / median / max " + (" / ".join(f"{x:.3f}" for x in R['cases'][nm]['Rset_over_Rfold_min_med_max']) if len(rf) else "-")
          + f"; variant (exact-field term only inside R_set): {R['cases'][nm]['variant_Tf_inside_only']['word']} rms {st2['all']['rms']:.4f} mean {st2['all']['mean']:+.4f}, massive {st2['massive']['rms']:.4f} / {st2['massive']['mean']:+.4f}")
        for u in ("ups0.5", "ups0.3", "ups0.8"):
            bb = beyond[u]
            P(f"[{ft}] {nm}: mass-to-light {u[3:]}: {bb['n_beyond']} galaxies with the last point beyond R_set (median last radius / R_set {bb['median_ratio']:.3f}; worst {bb['worst']} {bb['worst_ratio']:.3f})"
              + (": " + ", ".join(f"{n_} {r_:.3f} ({b_}, log M_b {m_:.2f})" for n_, r_, b_, m_ in bb["beyond"]) if bb["n_beyond"] else ""))
    RES["footings"][ft] = R
RES["known_answer_viii_ok"] = bool(kaok)
P(f"known answer (viii): {'PASS' if kaok else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "bj1_sparc.json"), "w"), indent=1)
open(os.path.join(HERE, "bj1_sparc.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
