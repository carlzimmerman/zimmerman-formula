#!/usr/bin/env python3
"""TL1_outer_tail_kids (see FROZEN_CRITERIA.md): GH2's harness with route E's tail outside r_f swapped to r^-9/4 at fixed M(<r_ta).
    PYTHONHASHSEED=0 nice -n 15 python3 tl1_tail.py; kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); GH2 = os.path.join(REB, "GH2_cgm_extent_discriminator", "gh2_discriminator.py")
T = open(GH2).read(); CUT = "# ------------------------------------------------------------ K1 / K2 (KiDS identities) and MUTATE"; assert T.count(CUT) == 1
T = T[:T.index(CUT)].replace("HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)", f"HERE = {HERE!r}; REB = {REB!r}", 1)
D = {"__file__": GH2, "__name__": "gh2_ro"}; exec(compile(T, GH2, "exec"), D)
G = D["G"]; NS, XP, baryons, RG, AQ = G["NS"], G["XP"], G["baryons"], G["RG_ALL"], D["AQ"]; base = G["mass_route_e"]; P = D["P"]; hot_of, lens_models, lens_grade, g09 = D["hot_of"], D["lens_models"], D["lens_grade"], D["g09_chi2"]
CF = 4.0; STATE = dict(mode="base", gam=2.25, tmul=1.0); NOROOT = {}
def parts(foot, l, z, hot):
    Ms, Mc, Mh = baryons(l, hot)
    if hot is None: Mbt = Ms + Mc + 0.5 * Ms
    else:
        f = lambda lr: math.log(XP.rta_pc(Ms + Mc + float(np.interp(math.exp(lr), RG, Mh)), z)) - lr
        rta = math.exp(brentq(f, math.log(1e4), math.log(1e8), xtol=1e-13)); Mbt = Ms + Mc + float(np.interp(rta, RG, Mh))
    Mf = XP.RNAT * Mbt; rta = XP.rta_pc(Mbt, z); Sig = max(NS["SIGA0"][foot], NS["eta_of"](Mf + Mbt, "cf4") * NS["sigma_coll"](Mf + Mbt))
    return Ms + Mc + Mh, Mf, rta, Sig, NS["solve_r0"](Mf, rta, Sig)
def smooth(Sig, r0, r): return math.pi * Sig * r0 ** 2 * NS["B"](r / r0)
def halo(foot, l, z, hot, mode, gam=2.25, tmul=1.0):
    Mb, Mf, rta, Sig, r0 = parts(foot, l, z, hot); e = 3 - gam; rf = CF * r0; r = np.minimum(RG, rta)
    if rf >= rta: return Mb + smooth(Sig, r0, r), Mf, rf, rta, r0
    if mode == "T2":
        Mi = float(smooth(Sig, r0, np.array([rf]))[0]); M = np.where(r <= rf, smooth(Sig, r0, r), Mi + tmul * (Mf - Mi) * (np.log(np.maximum(r, rf) / rf) / math.log(rta / rf) if e == 0 else (r ** e - rf ** e) / (rta ** e - rf ** e))); return Mb + M, Mf, rf, rta, r0
    def tot(q, rr):
        f_ = CF * q; Mi = float(smooth(Sig, q, np.array([f_]))[0]); rhof = (Sig / q) * (1 + CF * CF) ** -1.5
        return Mi + 4 * math.pi * rhof * f_ ** gam * (rr ** e - f_ ** e) / e, f_, Mi
    g = lambda lq: tot(math.exp(lq), rta)[0] - Mf
    lo, hi = math.log(rta / CF) - 25, math.log(rta / CF)
    if g(lo) * g(hi) > 0: NOROOT[(foot, round(l, 2))] = 1; return Mb + smooth(Sig, r0, r), Mf, rf, rta, r0
    q = math.exp(brentq(g, lo, hi, xtol=1e-13)); Mt, f_, _ = tot(q, r); return Mb + np.where(r <= f_, smooth(Sig, q, r), Mt), Mf, f_, rta, q
def patched(foot, l, z, hot):
    if STATE["mode"] == "base": return base(foot, l, z, hot)
    return halo(foot, l, z, hot, STATE["mode"], STATE["gam"], STATE["tmul"])[:2]
G["mass_route_e"] = patched; D["mass_route_e"] = patched
KG = [1, 1.5, 2, 3, 5]; C = json.load(open(os.path.join(REB, "GH2_cgm_extent_discriminator", "gh2_results.json")))["footings"]; RES = dict(footings={}); OK = True
def chk(n, ok, v):
    global OK; OK &= bool(ok); P(f"  {n}: {'PASS' if ok else 'FAIL'} ({v})"); RES[n] = bool(ok)
P("TL1 outer tail on KiDS (see FROZEN_CRITERIA.md); kappa = 1/2 FITTED; footings never pooled; not theory closed")
def kids(foot, k):
    mH, mL = lens_models(foot, hot_of(k)); return lens_grade(mH, mL)
d = 0.0
for foot in ("canonical", "alt"):
    for k in KG:
        g = kids(foot, k); c = C[foot]["rows"][str(k)]["kids"]; d = max(d, abs(g["H2H_b34"] / c["H"] - 1), abs(g["L2H_b34"] / c["L"] - 1))
chk("K1_GH2_identity", d < 1e-6, f"max rel {d:.1e}")
STATE.update(mode="T2", gam=3.0); g = kids("canonical", 3); chk("K2_slope3_near_GH2", abs(g["H2H_b34"] / C["canonical"]["rows"]["3"]["kids"]["H"] - 1) < 0.05, f"{g['H2H_b34']:.1f} vs {C['canonical']['rows']['3']['kids']['H']:.1f}"); STATE.update(gam=2.25)
Mb2, Mf, rf, rta, r0 = halo("canonical", 10.8, 0.285, hot_of(3), "T2"); Bb = base("canonical", 10.8, 0.285, hot_of(3))[0]; Mb1, Mf1, rf1, rta1, _ = halo("canonical", 10.8, 0.285, hot_of(3), "T1")
Mbar = parts("canonical", 10.8, 0.285, hot_of(3))[0]; i = int(np.argmin(abs(RG - rta * 1.5))); mass2 = abs((Mb2 - Mbar)[i] / Mf - 1); mass1 = abs((Mb1 - Mbar)[i] / Mf - 1); inner = float(np.max(np.abs(Mb2[RG <= rf] - Bb[RG <= rf])))
chk("K3_mass_and_inner", mass2 < 1e-9 and mass1 < 1e-9 and inner == 0, f"T2 {mass2:.1e}, T1 {mass1:.1e}, inner |d| {inner:.1e}; r0 {r0:.0f} pc, r_f {rf:.0f}, r_ta {rta:.0f}")
R3 = np.array([3e5]); ds = lambda fn: float(AQ.delta_sigma(R3, RG, fn, "const")[0])
a = ds(Mb2); b = ds(halo("canonical", 10.8, 0.285, hot_of(3), "T2", 2.25, 0.5)[0]); bs = ds(Bb); chk("MUTATE_tail_half_lowers", b < a, f"300 kpc DS {a:.2f} -> {b:.2f}; GH2 {bs:.2f}")
LAB = {}
for foot in ("canonical", "alt"):
    R = {}
    for mode in ("T2", "T1"):
        STATE.update(mode=mode); R[mode] = {}
        for k in KG:
            g = kids(foot, k); c = C[foot]["rows"][str(k)]["kids"]; q = g09(foot, k); R[mode][k] = dict(H=g["H2H_b34"], L=g["L2H_b34"], d=g["d_b34"], cls=g["cls"], gh2_H=c["H"], g09_H=q["H"])
            P(f"  [{foot} {mode} k={k}] KiDS H {g['H2H_b34']:.1f} (GH2 {c['H']:.1f}), L {g['L2H_b34']:.1f}, d {g['d_b34']:+.1f} {g['cls']}; G09 H {q['H']:.1f}")
    bt = min(R["T2"][k]["H"] for k in KG); bl = min(R["T2"][k]["L"] for k in KG); bg = min(R["T2"][k]["gh2_H"] for k in KG)
    LAB[foot] = "NOT DECIDED" if not OK else "CLOSES THE GAP" if bt <= bl + 9 else "IMPROVES" if bt <= bg - 9 else "NO IMPROVEMENT"
    P(f"VERDICT [{foot}] T2: best tail {bt:.1f}, law {bl:.1f}, GH2 route E {bg:.1f}: {LAB[foot]}; k=1 class {R['T2'][1]['cls']}; T1 best {min(R['T1'][k]['H'] for k in KG):.1f}"); RES["footings"][foot] = dict(R, label=LAB[foot])
P(f"T1 halos with no root: {len(NOROOT)}")
json.dump(RES, open(os.path.join(HERE, "tl1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "tl1.out"), "w").write("\n".join(map(str, D["OUT"])) + "\n")
