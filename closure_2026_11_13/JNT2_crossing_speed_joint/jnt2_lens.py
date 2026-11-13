#!/usr/bin/env python3
"""JNT2 (FROZEN_CRITERIA.md, e186b314ef): G4, ONE1's KiDS gate as SRH1 ran it, under the crossing-speed joint. SRJ2's
srj2_lens.py content copied (cited): SRH1's srh1_lens.py is executed read-only from its own path up to its
"# ---------------- runs, checkpointed" marker. The only change from SRJ2: the boundary. A table node (log M_b, z) holds the
reference profile (f = 0) when its speed exceeds the mode's boundary at the node's z:
  main / H / D: the lemma's v_L = (10 G (1 + 5.41) M_b H(z))^(1/3) against v*(z) (x 1/2, x 2);
  S: SRJ2's node speed (FRZ1 halo with X ~ 56) against v_stiff (TW-S);  0: no node switched (TW-0).
  python3 jnt2_lens.py [--mode main|S|0|H|D] -> jnt2_lens[_MUTATE_<mode>].json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2_common as C
MODE = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "main"; assert MODE in C.MODES
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
SRC = os.path.join(SRH, "srh1_lens.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srh1_lens_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# ---------------- runs, checkpointed\n")], SRC, "exec"), S)
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
O, FR = S["O"], S["FR"]
profile, dsig_prof, DINF_T, LMG, ZG, UT, own_S, nb_sums, fit, gate_of, slim, MK, XP = (S[k] for k in (
    "profile", "dsig_prof", "DINF_T", "LMG", "ZG", "UT", "own_S", "nb_sums", "fit", "gate_of", "slim", "MK", "XP"))
conc_z, hbz, FB, hh = S["conc_z"], S["hbz"], S["FB"], S["hh"]
assert FR["VST"] == C.VSTIFF
GF = FR["G"]; lMg, zz1, typ1, n1 = S["lMg"], S["zz1"], np.asarray(O["typ1"]), S["n1"]
P(f"JNT2 G4 mode {MODE} (criteria e186b314ef). SRH1 lens prefix executed. Host-free lenses {n1:,}: late {int((typ1 == 0).sum()):,}, early {int((typ1 == 1).sum()):,}")
P(f"node grid log M_b {LMG[0]:.2f} .. {LMG[-1]:.2f}, z {ZG[0]:.2f} .. {ZG[-1]:.2f}")

def hb_node(ft, lMb, z):                      # SRJ2's (SRH1's halo construction)
    conc, dta, omz = conc_z(round(z, 6)); Mta = XP[ft] * 10 ** lMb * hh / (1 - FB)
    lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
    return hbz(10 ** lM, conc, dta, omz)
def v_node(ft, lMb, z):
    if MODE == "S":
        hb = hb_node(ft, lMb, z); return math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"])
    return C.vL_kms(10 ** lMb, z)
VN = {ft: np.array([[v_node(ft, float(lm), float(z)) for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
VB = {ft: np.array([[C.vstar_kms(ft, float(z), MODE) for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
for ft in VN:
    edge = [float(np.interp(0.0, VN[ft][:, j] - VB[ft][:, j], LMG)) if (VN[ft][:, j] > VB[ft][:, j]).any() else math.inf for j in range(len(ZG))]
    P(f"[{ft}] boundary in log M_b at z 0.1 / 0.3 / 0.5: " + " / ".join(f"{edge[int(round((z - ZG[0]) / (ZG[1] - ZG[0])))]:.3f}" for z in (0.1, 0.3, 0.5))
      + f"; nodes switched to the reference {int((VN[ft] > VB[ft]).sum())} / {VN[ft].size}")
def table_J(ft, f):
    T = np.empty((len(LMG), len(ZG), len(UT))); Sm = np.empty((len(LMG), len(ZG)))
    for i, lm in enumerate(LMG):
        for j, z in enumerate(ZG):
            ff = 0.0 if VN[ft][i, j] > VB[ft][i, j] else f
            pc, M3, inf = profile(ft, float(lm), float(z), ff, "S"); T[i, j] = dsig_prof(UT, pc, M3) / DINF_T; Sm[i, j] = inf["s"]
    return T, Sm
def lens_v(ft, k):
    """each lens's speed at M_b = k M_gal and its z (bilinear in log v over the node grid), and its boundary."""
    lv = np.log(VN[ft]); x = np.clip((lMg + math.log10(k) - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1 - 1e-9); y = np.clip((zz1 - ZG[0]) / (ZG[1] - ZG[0]), 0, len(ZG) - 1 - 1e-9)
    i = np.floor(x).astype(int); j = np.floor(y).astype(int); wx = x - i; wy = y - j
    v = np.exp((1 - wx) * (1 - wy) * lv[i, j] + wx * (1 - wy) * lv[i + 1, j] + (1 - wx) * wy * lv[i, j + 1] + wx * wy * lv[i + 1, j + 1])
    vb = np.array([C.vstar_kms(ft, float(z), MODE) for z in zz1])
    return v, vb

CFG = {"main": [("f0", 0.0)] + [(f"f{f:.2f}", f) for f in (0.75, 1.0, 1.25, 1.5, 2.0, 3.0)],
       "S": [("f1.00", 1.0)], "0": [("f1.00", 1.0)], "H": [("f1.25", 1.25), ("f2.00", 2.0)], "D": [("f1.25", 1.25), ("f2.00", 2.0)]}[MODE]
RES = dict(lane="JNT2", part="G4", mode=MODE, criteria="e186b314ef", cfg={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
for ft in ("canonical", "alt"):
    X = XP[ft]; lams = O["lam_grid"](X, extra=[1.0, math.sqrt(O["A0C"] / O["A0"]["alt"])]); lams9 = sorted(set([0.65] + list(map(float, lams)) + [2.57]))
    with contextlib.redirect_stdout(io.StringIO()):
        Tr, Ts, npr = O["neighbours"](X, lams9, O["Htab_of"](X))
    SNB, kval = nb_sums(ft, Tr - Ts[2], lams9)
    P(f"[{ft}] neighbours {npr:,} pairs  [{time.time() - T0:.0f} s]")
    for name, f in CFG:
        T, Sm = table_J(ft, f); OS = own_S(ft, T)
        rn = {mk: fit(mk, ft, OS[mk] + SNB[mk], kvalid=kval) for mk in MK}; gt = gate_of(rn)
        cnt = {}
        for sub in ("all", "late", "early"):
            q = rn[("KO1", 1.6, sub)]
            if q is None: continue
            v, vb = lens_v(ft, q["k"]); hi = v > vb
            cnt[sub] = dict(k=float(q["k"]), above_all=int(hi.sum()), above_late=int((hi & (typ1 == 0)).sum()), above_early=int((hi & (typ1 == 1)).sum()),
                            n_all=int(n1), v_max=float(v.max()), v_over_vb_max=float((v / vb).max()) if MODE != "0" else 0.0)
        L_ = gt["lines"]
        RES["cfg"][f"{ft}|{name}"] = dict(f=f, gate=gt, z=[L_["G-K1 all"]["z"], L_["G-K1 late"]["z"], L_["G-K1 early"]["z"], L_["G-K3 type difference"]["z"]],
                                          chi2=L_["G-K2 all profile"]["chi2"], counts=cnt, nodes_reference=int((VN[ft] > VB[ft]).sum()), nodes_total=int(VN[ft].size))
        P(f"[{ft}] {name:6s} gate {gt['status']} {gt['failing']}: z all / late / early " + " / ".join(f"{L_['G-K1 ' + s]['z']:+.4f}" for s in ("all", "late", "early"))
          + f", chi2 {L_['G-K2 all profile']['chi2']:.4f}, type diff z {L_['G-K3 type difference']['z']:+.4f}; "
          + "; ".join(f"{s}-fit k {c['k']:.3f}: above {c['above_all']:,} (late {c['above_late']:,}, early {c['above_early']:,}), max v/v_b {c['v_over_vb_max']:.3f}" for s, c in cnt.items())
          + f"  [{time.time() - T0:.0f} s]")
tag = "" if MODE == "main" else f"_MUTATE_{MODE}"
json.dump(RES, open(os.path.join(HERE, f"jnt2_lens{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt2_lens{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
