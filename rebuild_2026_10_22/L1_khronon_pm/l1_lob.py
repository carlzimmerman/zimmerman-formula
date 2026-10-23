#!/usr/bin/env python3
"""L1_khronon_pm LOB-IC check at 128^3 (FROZEN_CRITERIA.md AMENDMENT A4 item 5): indicative, NOT a verdict.

  OMP_NUM_THREADS=1 nice -n 15 python3 l1_lob.py               -> l1_lob.out, l1_lob_results.json
  L1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 l1_lob.py   -> khronon delta taken from d_b: K-LOB3 must FAIL (no PM runs)
LOB-IC = per-species linear state at z_i = 199 from Q6's validated Khronon CLASS binary (LOB, j1 = -1, mu_K = 14.8 h/Mpc) at model B.
Control: the indicative S0-199 (same phases, box, step grid).  kappa = 1/2 FITTED; footings never pooled; no dark-matter particle.
Any production reading carries A4's sentence: literal v3's quadratic K has no radiation era (Q6), so these runs are
'v3 on a dust background with a yet-unspecified early K', not the literal theory."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("L1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
WORKI = os.path.join(HERE, "work", "indicative"); os.makedirs(WORKI, exist_ok=True)
os.environ["L1_WORK"] = WORKI
import numpy as np
sys.path.insert(0, HERE)
import khronon_pm as K
K.set_threads(1)
OUT, RES, CHK = [], {"lane": "L1_khronon_pm", "part": "lob_check_128", "mutate": MUT,
                     "note": "indicative, not a verdict; v3 on a dust background with a yet-unspecified early K (A4, Q6)"}, {}
T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
P("L1_khronon_pm LOB-IC check" + (" [MUTATE]" if MUT else "") + ": indicative, NOT a verdict; kappa = 1/2 FITTED")
bg = K.MODEL_B; MU = 14.8
T = K.lob_tables(MU, bg, mut=("tau_from_b" if MUT else None))

# K-LOB1: the DUST normaliser equals this lane's vanilla classy P(k) at z = 0
PkB, s8B = K.pk_model_B()
kd, pd = T["pk0_dust_k"], T["pk0_dust"]; sel = (kd >= 1e-3) & (kd <= 7.0)
r1 = np.interp(np.log(kd[sel]), np.log(K.KS), PkB) / pd[sel]
check("K-LOB1", float(np.max(np.abs(r1 - 1))) <= 1e-3, f"max|P_classy/P_DUST - 1| {np.max(np.abs(r1 - 1)):.2e} (k 1e-3..7 h/Mpc)", "<= 1e-3")
# K-LOB2 (reported): LOB linear sigma8 on model B vs Q6's R_B at its own parameters
RB = float(T["s8_lob"] / T["s8_dust"])
RES["K_LOB2"] = dict(sigma8_LOB=float(T["s8_lob"]), sigma8_DUST=float(T["s8_dust"]), R_B_modelB=RB, R_B_Q6=0.073)
check("K-LOB2", math.isfinite(RB), f"sigma8 LOB {float(T['s8_lob']):.4f}, DUST {float(T['s8_dust']):.4f}: R_B {RB:.4f} on model B (Q6: 0.073 at its own parameters)", "reported")
# K-LOB3: the khronon delta at z_i recomputed independently from the raw transfer file
fn = os.path.join(WORKI, f"lob_class_mu{MU:g}", "LOB__z3_tk.dat")
hdr = [l for l in open(fn) if l.startswith("#")][-1]
names = [c.split(":", 1)[1].strip() for c in hdr.strip("#\n").split("  ") if ":" in c]
raw = np.loadtxt(fn); col = {n: raw[:, i] for i, n in enumerate(names)}
h = bg.h; ob = (bg.Ob * h * h) / h ** 2; oc = 1e-8 / h ** 2; oa = bg.Om - ob - oc
tau_ind = (bg.Om * col["d_m"] - ob * col["d_b"] - oc * col["d_cdm"]) / oa
rel = float(np.max(np.abs(np.asarray(T["tau199"]) - tau_ind) / np.maximum(np.abs(tau_ind), 1e-12)))
check("K-LOB3", rel <= 1e-6, f"max rel |delta_tau(engine) - delta_tau(independent)| {rel:.2e} over {len(tau_ind)} k", "<= 1e-6")

if not MUT:
    out = {}
    for lab, mode, foot in (("LIN-LOB-199", "LIN", "canonical"), ("KX-can-LOB-199", "KX", "canonical")):
        cfg = dict(mode=mode, foot=foot, muK=MU, N=128, L=100.0, zi=199, nseed=256, seed=359, eps=1.0, bg="B", ic="native", ic_src="lob",
                   tag=f"I_{lab}_N128", snaps=[0.5, 2 / 3, 1.0], guard=True, ckpt_every=0, resume=False, log=True)
        r = K.run_sim(cfg); s0 = r["snap"]["z0"]
        out[lab] = dict(sigma8_pm=s0["sigma8"], sigma8_b=s0["sigma8_b"], sigma8_tau=s0["sigma8_tau"], sigma8_lin_box=r["ic"]["sigma8_lin_box"],
                        sigma8_zi=r["snap"]["zi"]["sigma8"], nonconverged=r["nonconverged_calls"], max_iters=r["max_iters"],
                        x_max_all=max([d.get("x_max", 0.0) for d in r["diag"]] or [0.0]), runtime_s=r["runtime_s"], P_z0=dict(k=s0["k"], P=s0["P"]))
        P(f"  {lab}: sigma8_PM(z=0) {s0['sigma8']:.4f} (baryons {s0['sigma8_b']:.4f}, khronon {s0['sigma8_tau']:.4f}); linear box {r['ic']['sigma8_lin_box']:.4f}; "
          f"sigma8 at z_i {r['snap']['zi']['sigma8']:.5f}; hold not converged {r['nonconverged_calls']}, max it {r['max_iters']}, x_max {out[lab]['x_max_all']:.3g}; {r['runtime_s']:.0f} s")
    S0 = json.load(open(os.path.join(WORKI, "I_S0-199_N128", "result.json")))["snap"]["z0"]["sigma8"]
    d = S0 - out["LIN-LOB-199"]["sigma8_pm"]; rho = (out["KX-can-LOB-199"]["sigma8_pm"] - out["LIN-LOB-199"]["sigma8_pm"]) / d
    rd = ("the nonlinear J_x term restores most of the linear deficit at 128^3" if rho >= 0.5 else "partial" if rho >= 0.1 else
          "does not restore growth at 128^3" if rho > -0.1 else "deepens the deficit")
    RES["runs"] = out; RES["S0_199_sigma8"] = S0; RES["rho_NL_LOB"] = dict(rho_NL=rho, reading=rd)
    P(f"  rho_NL (LOB-IC, canonical, z_i 199): {rho:+.4f} -> {rd} (indicative, not a verdict; the production run decides; "
      f"v3 on a dust background with a yet-unspecified early K)")
    check("I-LOB", all(v["nonconverged"] == 0 for v in out.values()) and math.isfinite(rho),
          "; ".join(f"{k}: nonconverged {v['nonconverged']}" for k, v in out.items()) + f"; rho_NL {rho:+.4f}", "converged and rho_NL finite")
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
P(f"L1_LOB COMPLETE: {npass}/{ntot} checks PASS.  ({RES['runtime_s']:.0f} s)  Indicative only.")
K.atomic_json(os.path.join(HERE, f"l1_lob_results{SUF}.json"), RES)
K.atomic_text(os.path.join(HERE, f"l1_lob{SUF}.out"), "\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)
