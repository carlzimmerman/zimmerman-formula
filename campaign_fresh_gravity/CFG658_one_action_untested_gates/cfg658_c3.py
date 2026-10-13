#!/usr/bin/env python3
"""CFG658 G-C3 (FROZEN_CRITERIA.md, 12c5ab6b3): early types under the one-action construction's law nu_s = 1/2 + sqrt(1/4 + 1/y).
C3-R (verdict, framework-native): CFG669's T2 Ks statistic, data A_obs vs the law's own prediction A_law from per-lens model ESDs
       (CFG669 definitions exec'd read-only up to its main loop; CFG531 fin / r_ta_law_k code; no environment, no stripping).
C3-A (CONTEXT, environment term LCDM-built): CFG531 eps with LAW_RTA tables rebuilt with nu_s at the footings (afac = 1).
MUTATE controls run in the same pass (M-K: nu_mono reproduces CFG531's recorded eps; A_obs reproduces CFG669; M-T tooth).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg658_c3.py   -> cfg658_c3.out, cfg658_c3_results.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
T0 = time.time(); OUT, RES, CHK = [], {"lane": "CFG658", "gate": "C3", "criteria": "12c5ab6b3"}, {}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}"); return bool(ok)


try:
    os.nice(10)
except OSError:
    pass
for v in ("CFG585_MUTATE", "CFG531_MUTATE", "CFG669_MUTATE", "CFG669_M"):
    os.environ.pop(v, None)
# ---- CFG669 definitions (read-only exec up to its main loop; it execs CFG585's head, which execs CFG531's head)
P669 = os.path.join(LANES, "CFG669_nearir_mass_rescore", "cfg669.py")
src = open(P669).read(); cut = 'P(f"CFG669  near-IR'
assert src.count(cut) == 1
N9 = {"__file__": P669, "__name__": "cfg669_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src.split(cut)[0], P669, "exec"), N9)
G = N9["esd_loo"].__globals__                                                    # CFG531 head namespace
C, FOOTS, CONS, A0F, WW, NPATCH = G["C"], G["FOOTS"], G["CONS"], G["A0F"], G["WW"], G["NPATCH"]
fin, r_ta_law_k, KERN = G["fin"], G["r_ta_law_k"], G["KERN"]
MGL = G["MGL"]; ZL = np.asarray(G["lens"]["z"], float)
EST, t2, k9, W9, K9 = N9["EST"], N9["t2"], N9["k9"], N9["W"], N9["K9"]
TYP, F30 = N9["TYP"], N9["F30"]
KS_ = {"simple": KERN["simple"], "mono": C.nu_mono}
P(__doc__.split("Run:")[0].strip())
P(f"\nCFG669 / CFG531 definitions exec'd read-only ({time.time() - T0:.0f} s); kernels: nu_s = CFG531's nu_simple (identical formula)")

# ============================================================================ C3-R
P("\n== C3-R  CFG669 T2 on Ks masses: data vs the law's own prediction ==")
lmb = EST["K"][1]
em, lm, rw, offs = t2(lmb)
a = k9(em, lm, ra=rw)
Aobs, sAobs = a["K9"]
check("CONTROL A_obs reproduces CFG669 T2 Ks K9 (+0.2802 +- 0.0832, 1e-4)", abs(Aobs - 0.2802) < 1e-4 and abs(sAobs - 0.0832) < 1e-4,
      f"{Aobs:+.4f} +- {sAobs:.4f}; bins {len(offs)}")
sel = np.where(em | lm)[0]
P(f"  lenses in the matched stacks: {len(sel)} (early {em.sum()}, late {lm.sum()})")


def law_vec(Mnode, Mb, z, a0, kn):
    nu = KS_[kn]
    rta = C.r_ta_law(Mb, a0, z) if kn == "mono" else r_ta_law_k(Mb, a0, z, nu)
    r = np.geomspace(1e-4, rta, 1500)
    Md = Mb * (nu(C.G_MPC * Mb / r ** 2 / a0) - 1.0)
    return fin(Mnode, Mb, r, Md)


def A_of(Mvec):
    """CFG669's K9 combination on model stacks (weights WW x r, combined with W over K9)."""
    def stack(mask):
        w = WW[mask] * rw[mask][:, None]
        return (w * Mvec[mask]).sum(0) / w.sum(0)
    da, db = stack(em), stack(lm)
    return math.log10((W9[K9] @ da[K9]) / (W9[K9] @ db[K9])), da, db


Mb_all = 10 ** lmb
MODEL = {}
for kn in ("simple", "mono"):
    for foot in FOOTS:
        Mv = np.zeros((len(TYP), 15))
        for i in sel:
            Mv[i] = law_vec(float(MGL[i]), float(Mb_all[i]), float(ZL[i]), A0F[foot], kn)
        MODEL[(kn, foot)] = Mv
        P(f"  model ESDs {kn:6s} {foot:9s} done ({time.time() - T0:.0f} s)")
C3R = {}
for kn in ("simple", "mono"):
    for foot in FOOTS:
        Al, da, db = A_of(MODEL[(kn, foot)])
        D = Aobs - Al; Z = D / sAobs
        C3R[f"{kn}|{foot}"] = dict(A_law=Al, D=D, Z=Z, model_early=da.tolist(), model_late=db.tolist())
        P(f"  {kn:6s} {foot:9s}: A_law {Al:+.4f};  D = A_obs - A_law = {D:+.4f} +- {sAobs:.4f} (Z {Z:+.2f})")


def lab(zs):
    if all(abs(z) < 2 for z in zs):
        return "PASS"
    if all(z >= 3 for z in zs):
        return "FAIL"
    return "TENSION"


c3r = lab([C3R[f"simple|{f}"]["Z"] for f in FOOTS])
P(f"  C3-R verdict (nu_s, frozen rule: PASS |D| < 2 sigma both; FAIL D >= 3 sigma both): {c3r}")
# M-T tooth: early lenses' model mass x 10^0.3 (nu_s, both footings)
tooth = {}
for foot in FOOTS:
    Mv = MODEL[("simple", foot)].copy()
    for i in np.where(em)[0]:
        Mv[i] = law_vec(float(MGL[i]), float(Mb_all[i]) * 10 ** 0.3, float(ZL[i]), A0F[foot], "simple")
    tooth[foot] = A_of(Mv)[0] - C3R[f"simple|{foot}"]["A_law"]
check("M-T tooth: early model mass x 10^0.3 moves A_law by >= 0.05 (both footings)", all(v >= 0.05 for v in tooth.values()),
      ", ".join(f"{f} dA {v:+.4f}" for f, v in tooth.items()))
RES["C3R"] = dict(A_obs=Aobs, sigma=sAobs, n_bins=len(offs), rows=C3R, verdict=c3r, tooth=tooth)

# ============================================================================ C3-A (CONTEXT)
P("\n== C3-A  CFG531 eps with nu_s LAW_RTA tables at the footings (CONTEXT: CFG529 environment is LCDM-built; no verdict weight) ==")
GSEL, GM, GZ, GS = G["GSEL"], G["GM"], G["GZ"], G["GS"]
G["TAB"]["kern_simple_fp"] = np.array([G["law_vecs"]((float(GM[g]), float(GZ[g]), float(GS[g]), 0.0, "simple", 1.0, float(GS[g])))
                                       for g in GSEL])
P(f"  nu_s LAW_RTA tables rebuilt for {len(GSEL)} f30 groups ({time.time() - T0:.0f} s)")
J531 = json.load(open(os.path.join(LANES, "CFG531_inner_halo_shortfall", "cfg531_kids_results.json")))
EARLY = TYP == 1
MASKS = {"all": F30, "early": F30 & EARLY, "late": F30 & ~EARLY}
C3A, dmk = {}, 0.0
for cls, mk in MASKS.items():
    dcl, Ccl, _ = G["esd_loo"](mk)
    for c in CONS:
        for foot in FOOTS:
            fm = G["all_bands"](dcl, Ccl, G["comps"](c, foot, mk))                           # nu_mono (recorded tables)
            fs = G["all_bands"](dcl, Ccl, G["comps"](c, foot, mk, tab="kern_simple_fp"))      # nu_s
            rec = J531["base"][f"{c}|{foot}|LAW_RTA"] if cls == "all" else J531["c"][f"{cls}|{c}|{foot}"]["bands"]
            for b in ("K-in", "K9"):
                dmk = max(dmk, abs(fm[b]["eps"] - rec[b]["eps"]))
            C3A[f"{cls}|{c}|{foot}"] = {b: dict(eps_mono=fm[b]["eps"], eps_s=fs[b]["eps"], sig_s=fs[b]["sig"], Z_s=fs[b]["Z"],
                                                d_eps=fs[b]["eps"] - fm[b]["eps"]) for b in ("K-in", "K-mid", "K-out", "K9")}
            P(f"  {cls:5s} [{c} {foot:9s}] K-in: mono {fm['K-in']['eps']:+.3f} -> nu_s {fs['K-in']['eps']:+.3f} +- {fs['K-in']['sig']:.3f} "
              f"(Z {fs['K-in']['Z']:+.1f}) | K9: mono {fm['K9']['eps']:+.3f} -> nu_s {fs['K9']['eps']:+.3f} +- {fs['K9']['sig']:.3f} (Z {fs['K9']['Z']:+.1f})")
check("M-K CFG531 recorded eps (K-in, K9; all / early / late; A, B; both footings) reproduced with nu_mono (1e-6)", dmk < 1e-6,
      f"max |d| {dmk:.1e}")
RES["C3A"] = C3A
RES["checks"] = CHK
RES["elapsed_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "cfg658_c3_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg658_c3.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v["ok"] for v in CHK.values()) else 1)
