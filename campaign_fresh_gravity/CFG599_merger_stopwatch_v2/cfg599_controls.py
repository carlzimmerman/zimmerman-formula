#!/usr/bin/env python3
"""CFG599 controls C1, C2, C3, C4(a), C5, C6 (FROZEN_CRITERIA.md section 5; C4(b) runs in cfg599_main.py before any merger run).
C1-C3 test CFG597's Poisson, hydro and phantom routines, which this lane imports unchanged; they are re-run here.
Run: nice -n 10 python3 cfg599_controls.py   -> cfg599_controls.out, cfg599_controls_results.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys, json, math, io, contextlib, runpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg599_lib as L
import cfg599_sim as S

OUT = []; RES = {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, measured):
    RES[name] = dict(ok=bool(ok), measured=measured)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")


P("CFG599 controls (criteria 8a10775bd). Units kpc, Gyr, Msun.")

# ---------------------------------------------------------------- C1-C3: CFG597's control script, executed read-only in memory
# (its file outputs are redirected: we run its code with its output writers disabled and read its RES dict)
src = open(os.path.join(HERE, "..", "CFG597_merger_settling_stopwatch", "cfg597_controls.py")).read()
src = src.split("# ---------------------------------------------------------------- C5")[0]       # C1-C3 only
ns = {"__name__": "cfg597_controls_readonly", "__file__": os.path.join(HERE, "..", "CFG597_merger_settling_stopwatch", "cfg597_controls.py")}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src, "cfg597_controls.py(C1-C3)", "exec"), ns)
r597 = ns["RES"]
for k, v in r597.items():
    if isinstance(v, dict) and "ok" in v:
        check("[CFG597 routine] " + k, v["ok"], v["measured"])
RES["C3b_reported"] = r597.get("C3b_reported")

# ---------------------------------------------------------------- C4(a) estimator at t = 0 on exactly centred isolated halos
c4a = {}
for which in ("main", "sub"):
    sim = S.Sim(dict(foot="can", alpha=1.0, mode="isolated", iso_which=which))
    d = sim.diagnose()[which]
    offs = {k: float(np.hypot(*d[k])) for k in ("gal", "gas", "lens")}
    c4a[which] = dict(offsets_from_true_centre_kpc=offs, lens_spread=d["lens_spread"])
ok4a = all(v <= 3.0 for w in c4a.values() for v in w["offsets_from_true_centre_kpc"].values())
check("C4(a) t = 0, exactly centred isolated main and sub: gas, galaxy and lensing peaks within 3 kpc of the true centre", ok4a,
      json.dumps({w: {k: round(v, 2) for k, v in c4a[w]["offsets_from_true_centre_kpc"].items()} for w in c4a}))
RES["C4a_detail"] = c4a

# ---------------------------------------------------------------- C5 conservation in the settle step (new particle set)
sim = S.Sim(dict(foot="can", alpha=1.0, mode="isolated", iso_which="sub"))
c = sim.is_c
m0 = sim.m[c].sum(); p0 = (sim.m[c, None] * sim.v[c]).sum(0)
vscale = np.sqrt((sim.m[c, None] * sim.v[c] ** 2).sum(0)).sum() * math.sqrt(sim.m[c].sum())
rho_tot = sim.U[0] + sim.g.deposit(sim.x, sim.m)
sim.settle(0.004, rho_tot)
m1 = sim.m[c].sum(); p1 = (sim.m[c, None] * sim.v[c]).sum(0)
dp = float(np.linalg.norm(p1 - p0) / vscale)
check("C5 settle step: settled cold mass unchanged exactly; cold momentum conserved to <= 1e-3 of its |p| scale",
      (m1 == m0) and dp <= 1e-3, f"dM = {m1 - m0:.3e}, |dp|/scale = {dp:.2e}")

# ---------------------------------------------------------------- C6 drag unit test
def drag_box(mscale, nsteps):
    sim = S.Sim(dict(foot="can", alpha=0.0, mode="isolated", iso_which="sub", eta=1.0))
    g = sim.g
    rho_u = 3.0e5                                                 # uniform gas at rest (Msun/kpc^3), ~ the main's central density
    Pu = rho_u * (1500 * L.KMS) ** 2 / L.GAMMA
    sim.U = L.cons(np.full(g.n, rho_u), np.zeros((3,) + g.n), np.full(g.n, Pu), np.zeros(g.n))
    gsel = sim.is_g
    sim.x = sim.x[gsel] - np.array([1500.0, 0, 0]); sim.m = sim.m[gsel] * mscale; sim.tag = sim.tag[gsel]; sim.kind = sim.kind[gsel]
    sim.is_g = np.ones(sim.x.shape[0], bool); sim.is_s = ~sim.is_g; sim.is_c = ~sim.is_g; sim.is_bp = sim.is_g.copy()
    V0 = 3000.0 * L.KMS
    sim.v = np.zeros_like(sim.x); sim.v[:, 0] = V0                # no dispersion: a pure bulk test
    k = sim.eta * rho_u / sim.Sigma_cc                            # Sigma_cc is the frozen M_cc/(pi a^2), independent of mscale
    t_d = 1.0 / (k * V0)
    def totals():
        p = (sim.m[:, None] * sim.v).sum(0) + sim.U[1:4].sum((1, 2, 3)) * g.dV
        E = 0.5 * (sim.m * (sim.v ** 2).sum(1)).sum() + sim.U[4].sum() * g.dV
        return p, E
    p_a, E_a = totals(); pcl = float(np.linalg.norm((sim.m[:, None] * sim.v).sum(0))); kecl = 0.5 * float((sim.m * (sim.v ** 2).sum(1)).sum())
    dt = t_d / 200; tt = 0.0; worst = 0.0
    for n in range(nsteps):
        sim.drag(dt); sim.x += sim.v * dt; tt += dt
        vnum = float(np.average(sim.v[:, 0], weights=sim.m))
        worst = max(worst, abs(vnum / (V0 / (1 + k * V0 * tt)) - 1))
    p_b, E_b = totals()
    return dict(worst=worst, t_d=t_d, Sigma=sim.Sigma_cc, dp_rel_cloud=float(np.linalg.norm(p_b - p_a) / pcl),
                dE_rel_cloudKE=float(abs(E_b - E_a) / kecl))
kin = drag_box(1e-6, 200)          # (i) kinematics: a test cloud too light to entrain the gas, over one drag time
cons_ = drag_box(1.0, 200)         # (ii) conservation with the real cool-core mass (entrains its cells' gas)
ok6 = kin["worst"] <= 0.02 and cons_["dp_rel_cloud"] <= 1e-6 and cons_["dE_rel_cloudKE"] <= 1e-6
check("C6 drag: (i) light test cloud in uniform gas at rest follows v0/(1 + k v0 t) to <= 2% over one drag time; (ii) real-mass cloud: "
      "cloud + gas momentum and total energy conserved to <= 1e-6 of the cloud's initial |p| and KE", ok6,
      f"(i) max |v/v_an - 1| = {kin['worst']:.2e} over t_d = {kin['t_d']:.4f} Gyr (Sigma_cc = {kin['Sigma']:.3e} Msun/kpc^2); "
      f"(ii) |dp|/p_cl = {cons_['dp_rel_cloud']:.2e}, |dE|/KE_cl = {cons_['dE_rel_cloudKE']:.2e}; (ii) bulk-speed deviation from the "
      f"no-entrainment law {cons_['worst']:.3f} (reported: the real core entrains the gas of its own cells)")
RES["C6_detail"] = dict(kinematics=kin, conservation=cons_)

RES["all_pass"] = all(v["ok"] for kk, v in RES.items() if isinstance(v, dict) and "ok" in v)
P(f"\nCONTROLS C1-C3, C4(a), C5, C6: {'ALL PASS' if RES['all_pass'] else 'SOME FAIL'}")
open(os.path.join(HERE, "cfg599_controls.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg599_controls_results.json"), "w"), indent=1)
sys.exit(0 if RES["all_pass"] else 1)
