#!/usr/bin/env python3
"""L1_khronon_pm indicative 128^3 set (FROZEN_CRITERIA.md §4 + AMENDMENT A3): NOT a verdict.

  OMP_NUM_THREADS=1 nice -n 15 python3 l1_indicative.py               -> l1_indicative.out, l1_indicative_results.json
  L1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 l1_indicative.py   -> 32^3 teeth: hold solver capped at 1 iteration (I1 must FAIL),
                                                                         S0 without the khronon in Poisson (I2 must FAIL)
L = 100 Mpc/h, model B, mu_K = 14.8 h/Mpc, same phases (seed 359, NSEED 256).  Runs: S0, LIN, KX-can, KX-alt at z_i = 49;
S0-199, LIN-199, KX-can-199 (X0 flag, A3).  kappa = 1/2 FITTED; footings never pooled; no dark-matter particle."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("L1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
WORKI = os.path.join(HERE, "work", "indicative" + SUF); os.makedirs(WORKI, exist_ok=True)
os.environ["L1_WORK"] = WORKI
import numpy as np
sys.path.insert(0, HERE)
import khronon_pm as K
K.set_threads(1)
OUT, RES, CHK = [], {"lane": "L1_khronon_pm", "part": "indicative_128", "date": "2026-10-23", "mutate": MUT,
                     "note": "indicative, not a verdict; the frozen production run decides"}, {}
T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
P("L1_khronon_pm indicative 128^3 set" + (" [MUTATE, 32^3]" if MUT else "") + ": indicative, NOT a verdict; kappa = 1/2 FITTED; footings never pooled")

N = 32 if MUT else 128; L = 100.0; MU = 14.8
RUNS = [("S0", "S0", "canonical", 49), ("LIN", "LIN", "canonical", 49), ("KX-can", "KX", "canonical", 49), ("KX-alt", "KX", "alt", 49),
        ("S0-199", "S0", "canonical", 199), ("LIN-199", "LIN", "canonical", 199), ("KX-can-199", "KX", "canonical", 199)]
if MUT: RUNS = [r for r in RUNS if r[0] in ("S0", "LIN", "KX-can")]
out = {}
for lab, mode, foot, zi in RUNS:
    cfg = dict(mode=mode, foot=foot, muK=(MU if mode != "S0" else float("inf")), N=N, L=L, zi=zi, nseed=256, seed=359, eps=1.0, bg="B",
               ic="native", tag=f"I_{lab}_N{N}" + SUF, snaps=[0.5, 2 / 3, 1.0], guard=True, ckpt_every=0, resume=False, log=True)
    if MUT and lab == "KX-can": cfg["maxit_cap"] = 1
    if MUT and lab == "S0": cfg["mut"] = "noKhronon"
    r = K.run_sim(cfg)
    s0 = r["snap"]["z0"]
    out[lab] = dict(sigma8_pm=s0["sigma8"], sigma8_b=s0["sigma8_b"], sigma8_tau=s0["sigma8_tau"], sigma8_lin_box=r["ic"]["sigma8_lin_box"],
                    sigma8_lin_box_dust=r["ic"]["sigma8_lin_box_dust"], ratio_pm_lin=s0["sigma8"] / r["ic"]["sigma8_lin_box"],
                    nonconverged=r["nonconverged_calls"], max_iters=r["max_iters"], max_res=r["max_res"], runtime_s=r["runtime_s"],
                    peak_rss_gb=r["peak_rss_gb"], peak_footprint_gb=(r.get("guard") or {}).get("footprint"),
                    sigma8_z1=r["snap"]["z1"]["sigma8"], sigma8_z0p5=r["snap"]["z0.5"]["sigma8"],
                    x_rms_first=(r["diag"][0].get("x_rms") if r["diag"] else None), x_max_all=max([d.get("x_max", 0.0) for d in r["diag"]] or [0.0]),
                    x_rms_by_a=[[d["a"], d.get("x_rms")] for d in r["diag"][::10] if "x_rms" in d], P_z0=dict(k=s0["k"], P=s0["P"]))
    P(f"  {lab}: sigma8_PM(z=0) {s0['sigma8']:.4f} (baryons {s0['sigma8_b']:.4f}, khronon {s0['sigma8_tau']:.4f}); linear box {r['ic']['sigma8_lin_box']:.4f} "
      f"(dust-limit box {r['ic']['sigma8_lin_box_dust']:.4f}); PM/lin {out[lab]['ratio_pm_lin']:.3f}; hold calls not converged {r['nonconverged_calls']}, "
      f"max it {r['max_iters']}, x_max {out[lab]['x_max_all']:.3g}; {r['runtime_s']:.0f} s, peak RSS {r['peak_rss_gb']:.2f} GB")

# linear infinite-volume sigma8 on model B (F3 style), a_start = 1e-3
PkB, s8B = K.pk_model_B()
KT = np.geomspace(1e-3, 3.0, 36)
def sig8(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(np.trapz(Pk * K.W8(K.KS * 8.0) ** 2 * K.KS ** 2, K.KS) / (2 * math.pi ** 2))
Tm = K.linear_transfer(KT, "KX", MU, K.MODEL_B, [1.0])[0]["Tm"]
s8_lin_inf = sig8(PkB, np.interp(np.log(K.KS), np.log(KT), Tm, left=Tm[0], right=Tm[-1]))
RES["sigma8_lin_inf_modelB"] = dict(KX_LIN=s8_lin_inf, dust=s8B, ratio=s8_lin_inf / s8B)
P(f"  linear infinite-volume sigma8 on model B (BSK2 kernel from a = 1e-3): {s8_lin_inf:.4f} (dust limit {s8B:.4f}; ratio {s8_lin_inf / s8B:.3f})")

def rho_nl(kx, lin, s0):
    d = out[s0]["sigma8_pm"] - out[lin]["sigma8_pm"]
    return (out[kx]["sigma8_pm"] - out[lin]["sigma8_pm"]) / d if d != 0 else float("nan")
def reading(r):
    if not math.isfinite(r): return "undefined"
    if r >= 0.5: return "the nonlinear J_x term restores most of the linear deficit at 128^3"
    if r >= 0.1: return "partial"
    if r > -0.1: return "does not restore growth at 128^3"
    return "deepens the deficit"
RNL = {}
pairs = [("can_49", "KX-can", "LIN", "S0"), ("alt_49", "KX-alt", "LIN", "S0"), ("can_199", "KX-can-199", "LIN-199", "S0-199")]
for nm, kx, lin, s0 in pairs:
    if kx in out and lin in out and s0 in out:
        r = rho_nl(kx, lin, s0); RNL[nm] = dict(rho_NL=r, reading=reading(r), sigma8_KX=out[kx]["sigma8_pm"], sigma8_LIN=out[lin]["sigma8_pm"],
                                                sigma8_S0=out[s0]["sigma8_pm"])
        P(f"  rho_NL {nm}: {r:+.4f} -> {reading(r)} (indicative, not a verdict; the frozen production run decides)")
RES["runs"] = out; RES["rho_NL"] = RNL

ok1 = all(v["nonconverged"] == 0 for v in out.values())
check("I1", ok1, "; ".join(f"{k}: nonconverged {v['nonconverged']}, max it {v['max_iters']}" for k, v in out.items()), "every hold call converged")
s0keys = [k for k in out if k.startswith("S0")]
check("I2", all(0.98 <= out[k]["ratio_pm_lin"] <= 1.15 for k in s0keys), "; ".join(f"{k}: {out[k]['ratio_pm_lin']:.3f}" for k in s0keys), "S0 sigma8_PM/sigma8_lin_box in [0.98, 1.15]")
lkeys = [k for k in out if k.startswith("LIN")]
check("I3", all(0.98 <= out[k]["ratio_pm_lin"] <= 1.30 for k in lkeys), "; ".join(f"{k}: {out[k]['ratio_pm_lin']:.3f}" for k in lkeys), "LIN sigma8_PM/sigma8_lin_box in [0.98, 1.30]")
check("I4", all(math.isfinite(v["rho_NL"]) for v in RNL.values()) and (MUT or ("can_49" in RNL and "alt_49" in RNL)),
      "; ".join(f"{k}: {v['rho_NL']:+.4f}" for k, v in RNL.items()), "computed and finite (both footings)")
pk = max(v["peak_rss_gb"] for v in out.values())
check("I5", pk < 1.0, f"max peak RSS {pk:.2f} GB (footprint {max((v['peak_footprint_gb'] or 0) for v in out.values()):.2f} GB)", "< 1 GB")
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
P(f"L1_INDICATIVE COMPLETE: {npass}/{ntot} checks PASS.  ({RES['runtime_s']:.0f} s)  Indicative only; the frozen production run decides.")
K.atomic_json(os.path.join(HERE, f"l1_indicative_results{SUF}.json"), RES)
K.atomic_text(os.path.join(HERE, f"l1_indicative{SUF}.out"), "\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)
