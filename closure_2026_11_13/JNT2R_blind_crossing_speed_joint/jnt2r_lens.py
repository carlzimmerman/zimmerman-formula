#!/usr/bin/env python3
"""JNT2R (READING.md, 5abea0324b): G4, ONE1's KiDS gate as SRH1 / SRJ2 ran it, under the crossing-speed joint.
SRH1's srh1_lens.py is executed read-only, from its own path, up to its "# ---------------- runs, checkpointed" marker
(as SRJ2 did). Table assembly and lens_v are copied from SRJ2's srj2_lens.py; the node membership is this lane's: a node
(log M_b, z) holds the reference profile (SRH1's f = 0) iff it is above v*(z).
  Memberships: P (log M_b > log M_b*(z)), B (record-halo v_vir > v*(z)); twins V (v_vir > v_stiff), N (none), H / D.
  python3 jnt2r_lens.py           -> jnt2r_lens.json / .out          (f 0 and the primary grid; B where it differs)
  python3 jnt2r_lens.py --twin    -> jnt2r_lens_MUTATE.json / .out   (TW-V, TW-N, TW-H, TW-D at f 1; exits 1)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
TWIN = "--twin" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2r_common as JC
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
SRJ2 = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint")
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
VST = FR["VST"]; assert VST == {"canonical": 265.8, "alt": 288.1}
GF = FR["G"]; lMg, zz1, typ1, n1 = S["lMg"], S["zz1"], np.asarray(O["typ1"]), S["n1"]
STORED = json.load(open(os.path.join(SRH, "srh1_lens.json")))
P(f"JNT2R G4 (READING 5abea0324b){' TWINS (deliberately wrong)' if TWIN else ''}. Host-free lenses (1.0 R_h) {n1:,}: late {int((typ1 == 0).sum()):,}, early {int((typ1 == 1).sum()):,}")

def hb_node(ft, lMb, z):     # SRJ2's, copied
    conc, dta, omz = conc_z(round(z, 6)); Mta = XP[ft] * 10 ** lMb * hh / (1 - FB)
    lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
    return hbz(10 ** lM, conc, dta, omz)
def v_node(ft, lMb, z):
    hb = hb_node(ft, lMb, z); return math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"])
VN = {ft: np.array([[v_node(ft, float(lm), float(z)) for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
LMS = {ft: {s: np.array([math.log10(JC.mbstar(ft, float(z), s)) for z in ZG]) for s in (0.5, 1.0, 2.0)} for ft in VN}
VS_ = {ft: np.array([JC.vstar(ft, float(z)) for z in ZG]) for ft in VN}
def node_above(mode, ft):
    if mode == "N": return np.zeros(VN[ft].shape, bool)
    if mode == "V": return VN[ft] > VST[ft]
    if mode == "B": return VN[ft] > VS_[ft][None, :]
    s = {"P": 1.0, "H": 0.5, "D": 2.0}[mode]; return LMG[:, None] > LMS[ft][s][None, :]
def lens_v(ft, k):           # SRJ2's, copied
    lv = np.log(VN[ft]); x = np.clip((lMg + math.log10(k) - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1 - 1e-9); y = np.clip((zz1 - ZG[0]) / (ZG[1] - ZG[0]), 0, len(ZG) - 1 - 1e-9)
    i = np.floor(x).astype(int); j = np.floor(y).astype(int); wx = x - i; wy = y - j
    return np.exp((1 - wx) * (1 - wy) * lv[i, j] + wx * (1 - wy) * lv[i + 1, j] + (1 - wx) * wy * lv[i, j + 1] + wx * wy * lv[i + 1, j + 1])
def lens_above(mode, ft, k):
    lmb = lMg + math.log10(k)
    if mode == "N": return np.zeros(lmb.shape, bool)
    if mode == "V": return lens_v(ft, k) > VST[ft]
    if mode == "B": return lens_v(ft, k) > np.array([JC.vstar(ft, float(z)) for z in zz1])
    s = {"P": 1.0, "H": 0.5, "D": 2.0}[mode]; return lmb > np.log10([JC.mbstar(ft, float(z), s) for z in zz1])
def table_J(ft, f, ab):
    T = np.empty((len(LMG), len(ZG), len(UT)))
    for i, lm in enumerate(LMG):
        for j, z in enumerate(ZG):
            pc, M3, inf = profile(ft, float(lm), float(z), 0.0 if ab[i, j] else f, "S"); T[i, j] = dsig_prof(UT, pc, M3) / DINF_T
    return T
for ft in VN:
    P(f"[{ft}] lens table grid log M_b {LMG[0]}..{LMG[-1]}, z {ZG[0]}..{ZG[-1]}; nodes above v*(z): P {int(node_above('P', ft).sum())}, B {int(node_above('B', ft).sum())}, "
      f"V {int(node_above('V', ft).sum())}, H {int(node_above('H', ft).sum())}, D {int(node_above('D', ft).sum())} of {VN[ft].size}; log M_b*(z) at z 0.1 / 0.3 / 0.5 / 0.85: "
      + " / ".join(f"{math.log10(JC.mbstar(ft, z)):.3f}" for z in (0.1, 0.3, 0.5, 0.85)))

RES = dict(lane="JNT2R", part="G4" + (" TWINS" if TWIN else ""), reading="5abea0324b", cfg={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
FG = (0.75, 1.00, 1.25, 1.50, 2.00, 3.00)
if TWIN: cfgs = [(f"TW{m}_f1.00", 1.0, m) for m in ("V", "N", "H", "D")]
else: cfgs = [("f0", 0.0, "P")] + [(f"P_f{f:.2f}", f, "P") for f in FG] + [(f"B_f{f:.2f}", f, "B") for f in FG]
def zrow(cfg): L_ = cfg["gate"]["lines"]; return [L_["G-K1 all"]["z"], L_["G-K1 late"]["z"], L_["G-K1 early"]["z"], L_["G-K3 type difference"]["z"]], L_["G-K2 all profile"]["chi2"]
for ft in ("canonical", "alt"):
    X = XP[ft]; lams = O["lam_grid"](X, extra=[1.0, math.sqrt(O["A0C"] / O["A0"]["alt"])]); lams9 = sorted(set([0.65] + list(map(float, lams)) + [2.57]))
    with contextlib.redirect_stdout(io.StringIO()):
        Tr, Ts, npr = O["neighbours"](X, lams9, O["Htab_of"](X))
    SNB, kval = nb_sums(ft, Tr - Ts[2], lams9)
    for name, f, mode in cfgs:
        ab = node_above(mode, ft)
        if mode == "B" and np.array_equal(ab, node_above("P", ft)):
            RES["cfg"][f"{ft}|{name}"] = dict(RES["cfg"][f"{ft}|P_f{f:.2f}"], same_as=f"P_f{f:.2f}"); continue
        T = table_J(ft, f, ab); OS = own_S(ft, T)
        rn = {mk: fit(mk, ft, OS[mk] + SNB[mk], kvalid=kval) for mk in MK}; gt = gate_of(rn)
        cnt = {}
        for sub in ("all", "late", "early"):
            q = rn[("KO1", 1.6, sub)]
            if q is None: continue
            hi = lens_above(mode, ft, q["k"])
            cnt[sub] = dict(k=float(q["k"]), above_all=int(hi.sum()), above_late=int((hi & (typ1 == 0)).sum()), above_early=int((hi & (typ1 == 1)).sum()),
                            max_lMb=float(np.max(lMg) + math.log10(q["k"])))
        RES["cfg"][f"{ft}|{name}"] = dict(f=f, mode=mode, gate=gt, nb={"|".join(map(str, mk)): slim(rn[mk]) for mk in MK}, counts=cnt, nodes_above=int(ab.sum()), nodes_total=int(ab.size))
        L_ = gt["lines"]
        P(f"[{ft}] {name:10s} gate {gt['status']} {gt['failing']}: z all / late / early " + " / ".join(f"{L_['G-K1 ' + s]['z']:+.4f}" for s in ("all", "late", "early"))
          + f", chi2 {L_['G-K2 all profile']['chi2']:.4f}, type diff z {L_['G-K3 type difference']['z']:+.4f}; nodes above {int(ab.sum())}; "
          + "; ".join(f"{s}-fit k {c['k']:.3f}: lenses above {c['above_all']:,} (late {c['above_late']:,}, early {c['above_early']:,}), max log M_b {c['max_lMb']:.2f}" for s, c in cnt.items())
          + f"  [{time.time() - T0:.0f} s]")
chk = {}
for ft in ("canonical", "alt"):
    if TWIN:
        GR = json.load(open(os.path.join(HERE, "jnt2r_lens.json")))["cfg"]; S2 = json.load(open(os.path.join(SRJ2, "srj2_lens.json")))["cfg"]
        p, cp = zrow(GR[f"{ft}|P_f1.00"])
        for m, refrow in (("V", S2[f"{ft}|on_f1.00"]), ("N", STORED["cfg"][f"{ft}|f1.00"]), ("H", None), ("D", None)):
            a, ca = zrow(RES["cfg"][f"{ft}|TW{m}_f1.00"]); o = dict(z=a, chi2=ca, status=RES["cfg"][f"{ft}|TW{m}_f1.00"]["gate"]["status"])
            if refrow is not None:
                b, cb = zrow(refrow); o["reproduces"] = bool(max(abs(x - y) for x, y in zip(a, b)) <= 0.005 and abs(ca - cb) <= 0.01)
            o["moves"] = bool(max(abs(x - y) for x, y in zip(a, p)) > 0.10 or abs(ca - cp) > 0.10)
            o["mark_differs"] = bool(o["status"] != GR[f"{ft}|P_f1.00"]["gate"]["status"])
            chk[f"{ft}|TW{m}"] = o
            P(f"[{ft}] TW-{m} G4 at f 1: early z {a[2]:+.4f} (primary {p[2]:+.4f}), status {o['status']}; " + ", ".join(f"{k} {v}" for k, v in o.items() if k in ("reproduces", "moves", "mark_differs")))
    else:
        a, ca = zrow(RES["cfg"][f"{ft}|f0"]); b, cb = zrow(STORED["cfg"][f"{ft}|f0"])
        chk[f"{ft}|f0"] = dict(max_z_dev=max(abs(x - y) for x, y in zip(a, b)), pass_=bool(max(abs(x - y) for x, y in zip(a, b)) <= 0.005 and abs(ca - cb) <= 0.01))
        P(f"[{ft}] KA4 f 0 against SRH1's stored f0: max z dev {chk[ft + '|f0']['max_z_dev']:.1e} -> {'PASS' if chk[ft + '|f0']['pass_'] else 'FAIL'}")
        for f in FG:
            nm = f"P_f{f:.2f}"; a, ca = zrow(RES["cfg"][f"{ft}|{nm}"]); b0, c0 = zrow(RES["cfg"][f"{ft}|f0"])
            triv = bool(max(abs(x - y) for x, y in zip(a, b0)) <= 0.10 and abs(ca - c0) <= 0.10)
            o = dict(trivial=triv, law_equal_by_membership=RES["cfg"][f"{ft}|{nm}"]["nodes_above"] == 0)
            if f"{ft}|f{f:.2f}" in STORED["cfg"]:
                b, cb = zrow(STORED["cfg"][f"{ft}|f{f:.2f}"]); o["vs_SRH1_no_split"] = dict(max_z_dev=max(abs(x - y) for x, y in zip(a, b)), chi2_dev=abs(ca - cb))
            chk[f"{ft}|{nm}"] = o
            P(f"[{ft}] {nm}: TRIVIAL {triv}; nodes above 0 (law-equal) {o['law_equal_by_membership']}" + (f"; against SRH1's no-split f {f:.2f}: max z dev {o['vs_SRH1_no_split']['max_z_dev']:.1e}, chi2 dev {o['vs_SRH1_no_split']['chi2_dev']:.1e}" if "vs_SRH1_no_split" in o else ""))
RES["checks"] = chk; RES["seconds"] = time.time() - T0
tag = "_MUTATE" if TWIN else ""
json.dump(RES, open(os.path.join(HERE, f"jnt2r_lens{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt2r_lens{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
sys.exit(1 if TWIN else 0)
