#!/usr/bin/env python3
"""XJ1 (AMENDMENT_A2.md): SPARC rotation curves under FZS1's junction at z = 0. Reported, not a label; post hoc.
PD1's sparc() (closure_2026_11_09/PD1_phantom_is_dust/pd1.py lines 120 to 133) copied without its truncation, with the
model g = g_N + s (glaw(g_N) - g_N) and s per galaxy from SRH1's lens profile (FZS1's factor) at z = 0. QX8's loader, grid
of mass-to-light ratios and exact-field term are read as PD1 reads them.
Known answer: s = 1 reproduces PD1's stored L0 (pd1.json) to 1e-9.
  python3 -I -B xj1_sparc.py -> xj1_sparc.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
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
# ---------------- SRH1's lens prefix: FZS1's factor s at z = 0
SRC = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history", "srh1_lens.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srh1_lens_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# ---------------- runs, checkpointed\n")], SRC, "exec"), S)
profile, H = S["profile"], S["H"]; MASSES, FTAB, rfold_kpc = H["MASSES"], H["FT"], H["rfold_kpc"]
def rta_over_rfold(ft, lM):
    """FLD1's R_ta_kpc over R_fold_kpc at z = 0 (SRH1's interpolation in mass, both columns)."""
    def col(c):
        R = np.array([float(np.interp(0.0, FTAB[ft][M][np.argsort(FTAB[ft][M][:, 1]), 1], FTAB[ft][M][np.argsort(FTAB[ft][M][:, 1]), c])) for M in MASSES])
        if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
        if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
        return float(10 ** np.interp(lM, MASSES, np.log10(R)))
    return col(3) / col(2)

def Mb_of(q):
    R = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
    return max(float(np.max(np.clip(VB2 * R / G_KPC, 0, None))), 1e3)
def sparc(f, sfac):
    """PD1's sparc() without truncation, the law's phantom acceleration multiplied by sfac[i] for galaxy i."""
    a0 = A0[f]; rows = []; ups = []
    for q, Tf, s in zip(GALS, PRE[f], sfac):
        g = q["GB"]; ge = g + s * (glaw(g, a0) - g)
        lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k])); ups.append(float(Q8.UPS[k]))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
    return dict(all=pooled(range(len(rows))), massive=pooled(massive), n_massive=len(massive), U_median=float(np.median(ups)),
                U_at_top=int(sum(1 for u in ups if u >= float(Q8.UPS[-1]) - 1e-9)), U_at_bottom=int(sum(1 for u in ups if u <= float(Q8.UPS[0]) + 1e-9)))
def gate(st, L0):
    ok = (st["all"]["rms"] <= L0["all"]["rms"] + 0.010 and abs(st["all"]["mean"]) <= 0.05 and st["massive"]["rms"] <= L0["massive"]["rms"] + 0.010 and abs(st["massive"]["mean"]) <= 0.05)
    return "PASS" if ok else "FAIL"

RES = dict(lane="XJ1", part="SPARC under FZS1's junction at z = 0 (AMENDMENT_A2; reported, post hoc)", n_galaxies=len(GALS),
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})
lMb = np.array([math.log10(Mb_of(q)) for q in GALS])
P(f"XJ1 SPARC under FZS1's junction at z = 0 (AMENDMENT_A2; reported, post hoc). {len(GALS)} galaxies; log M_b {lMb.min():.2f} to {lMb.max():.2f}, median {np.median(lMb):.2f}")
kaok = True
for ft in FOOTS:
    L0s = PD1[ft]["P2_SPARC"]["L0"]; base = sparc(ft, np.ones(len(GALS)))
    dv = max(abs(base[a][b] - L0s[a][b]) for a in ("all", "massive") for b in ("rms", "mean")); kaok &= dv <= 1e-9
    P(f"[{ft}] known answer, s = 1 against PD1's stored L0: rms {base['all']['rms']:.6f} (stored {L0s['all']['rms']:.6f}), massive {base['massive']['rms']:.6f}; max abs dev {dv:.1e} -> {'PASS' if dv <= 1e-9 else 'FAIL'}; median mass-to-light {base['U_median']:.2f}")
    out_fold = [q["name"] for q, lm in zip(GALS, lMb) if q["R"][-1] > rfold_kpc(ft, 0.0, float(lm))]
    P(f"[{ft}] containment: galaxies whose last point lies beyond R_fold(z 0): {len(out_fold)} {out_fold[:5]}")
    R = dict(L0=base, KA_dev=dv, beyond_fold=out_fold, cases={})
    for nm, f in (("f1.25", 1.25), ("f2", 2.0), ("f3", 3.0), ("zv", "zv")):
        sv = np.array([profile(ft, float(lm), 0.0, (rta_over_rfold(ft, float(lm)) if f == "zv" else f), "S")[2]["s"] for lm in lMb])
        st = sparc(ft, sv); w = gate(st, base)
        R["cases"][nm] = dict(st, word=w, line_all=base["all"]["rms"] + 0.010, line_massive=base["massive"]["rms"] + 0.010,
                              s_min_med_max=[float(sv.min()), float(np.median(sv)), float(sv.max())], n_s_below_0p8=int((sv < 0.8).sum()), n_s_above_1p2=int((sv > 1.2).sum()))
        P(f"[{ft}] {nm:5s}: {w}  rms {st['all']['rms']:.4f} (line {base['all']['rms'] + 0.010:.4f}; law {base['all']['rms']:.4f}) mean {st['all']['mean']:+.4f}; massive rms {st['massive']['rms']:.4f} (line {base['massive']['rms'] + 0.010:.4f}) mean {st['massive']['mean']:+.4f}; "
          f"s min / median / max {sv.min():.3f} / {np.median(sv):.3f} / {sv.max():.3f} ({int((sv < 0.8).sum())} galaxies below 0.8, {int((sv > 1.2).sum())} above 1.2); fitted median mass-to-light {st['U_median']:.2f} (law {base['U_median']:.2f}), {st['U_at_top']} galaxies at the grid's top 1.20 (law {base['U_at_top']})")
    RES["footings"][ft] = R
RES["known_answer_ok"] = bool(kaok)
P(f"known answer: {'PASS' if kaok else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "xj1_sparc.json"), "w"), indent=1)
open(os.path.join(HERE, "xj1_sparc.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
