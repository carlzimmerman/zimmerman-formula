#!/usr/bin/env python3
"""CFG725 POST-HOC diagnostics (not frozen, no verdict weight): how hard is the merger bound?
P1 escape-speed sensitivity (eta = x^4/2 depends on v_esc^4); P2 the data-normalised sub profile's total mass vs the CFG623
sub progenitor; P3 phase-mixing damping of the galaxy-carrier oscillation (Q = 1, 2); P4 the f half of MUTATE M2/M3;
P5 which statistic (Bullet f or Harvey beta) does the excluding.
Run: nice -n 10 python3 cfg725_posthoc.py -> cfg725_posthoc.out, cfg725_posthoc_results.json"""
import contextlib, io, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg725.py")).read()
src = src[:src.index("runs = {f: json.load")]          # definitions + controls only
ns = {"__file__": os.path.join(HERE, "cfg725.py"), "__name__": "cfg725_defs"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "cfg725.py", "exec"), ns)
g = type("NS", (), ns)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

def layer2(run, foot, rc, vesc_kms=None, Q=None, sign=1.0):
    t, sep, V, uhat = g.fine_history(run)
    rm, rhom, _ = g.norm_piso(g.M_LENS["main"] - g.M_BAR["main"], rc, g.RT["main"])
    rs, rhos, ms = g.norm_piso(g.M_LENS["sub"], rc, g.RT["sub"])
    om = math.sqrt(4 * np.pi / 3 * g.G * rhos[0])
    vesc = math.sqrt(2 * abs(g.phi0(rs, rhos))) if vesc_kms is None else vesc_kms * g.KMS
    wgt = (g.M_LENS["sub"] - g.M_BAR["sub"]) / g.M_LENS["sub"]
    tf = np.linspace(t[0], t[-1], int((t[-1] - t[0]) / 2e-4) + 1)
    sepf = np.interp(tf, t, sep); Vf = np.interp(tf, t, V)
    x = np.minimum(vesc / Vf, 1.0)
    a = sign * x**4 / 2 * g.CM2G * np.interp(sepf, rm, rhom, right=0.0) * Vf**2
    gam = 0.0 if Q is None else om / Q
    d = np.zeros_like(tf); xx = 0.0; vv = 0.0
    for i in range(1, tf.size):                       # semi-implicit (symplectic-Euler) damped oscillator, dt = 2e-4 Gyr
        h = tf[i] - tf[i - 1]
        vv += h * (a[i - 1] - om * om * xx - gam * vv); xx += h * vv; d[i] = xx
    return (wgt * np.interp(t, tf, d))[:, None] * uhat, dict(vesc_kms=vesc / g.KMS, Mtot_sub=float(ms[-1]), omega=om)

def bound(run, disp):
    rows = [g.score(run, disp, s) for s in g.GRID]
    sm, fe, _ = g.smax_of(rows)
    ex = None
    if fe is not None:
        r = rows[list(g.GRID).index(fe)]
        ex = ("f" if abs(r["Z_B"]) >= 2 else "") + ("beta" if abs(r["Z_H"]) >= 2 else "") + ("" if r["scorable"] else "unscorable")
    return sm, ex, rows

runs = {f: json.load(open(os.path.join(g.C623, "runs", g.RUNS[f] + ".json"))) for f in g.RUNS}
R = {"label": "POST-HOC, no verdict weight"}
for foot, run in runs.items():
    RF = {}
    d0, i0 = layer2(run, foot, 100.0)
    P(f"[{foot}] P2: data-normalised sub pseudo-isothermal (r_c 100, r_t 990.9) total mass {i0['Mtot_sub']:.2e} Msun vs CFG623 sub "
      f"progenitor M200 = 6.73 x M_b = {6.73 * run['Mb'][1]:.2e}; v_esc(0) {i0['vesc_kms']:.0f} km/s")
    RF["P2"] = dict(Mtot_sub=i0["Mtot_sub"], M200_sim=6.73 * run["Mb"][1], vesc_frozen=i0["vesc_kms"])
    sm, ex, rows = bound(run, d0)
    P(f"[{foot}] P5 frozen primary: sigma/m_max {sm:.3g}, first exclusion by: {ex}")
    RF["P5"] = dict(smax=sm, excluded_by=ex)
    RF["P1"] = {}
    for ve in (2000.0, 2500.0, 3000.0, 3500.0):
        d, _ = layer2(run, foot, 100.0, vesc_kms=ve)
        sm, ex, _ = bound(run, d)
        RF["P1"][ve] = dict(smax=sm, excluded_by=ex)
        P(f"[{foot}] P1 v_esc {ve:.0f} km/s: sigma/m_max {sm:.3g} (by {ex})")
    RF["P3"] = {}
    for Q in (1.0, 2.0):
        d, _ = layer2(run, foot, 100.0, Q=Q)
        sm, ex, rows = bound(run, d)
        r03, r3 = g.score(run, d, 0.3), g.score(run, d, 3.0)
        RF["P3"][Q] = dict(smax=sm, excluded_by=ex, f_03=r03["f"], f_3=r3["f"], b_03=r03["beta_bar"], b_3=r3["beta_bar"])
        P(f"[{foot}] P3 damping Q {Q:g}: sigma/m_max {sm:.3g} (by {ex}); 0.3 -> 3: f {r03['f']:.3f} -> {r3['f']:.3f}, "
          f"beta_bar {r03['beta_bar']:.3f} -> {r3['beta_bar']:.3f}")
    df, _ = layer2(run, foot, 100.0, sign=-1.0)
    r3f = g.score(run, df, 3.0); b = g.score(run, df, 0.0)
    RF["P4"] = dict(f_flipped_3=r3f["f"], f_0=b["f"], beta_flipped_3=r3f["beta_bar"])
    P(f"[{foot}] P4 MUTATE f half: flipped drag at 3 gives f {r3f['f']:.3f} vs {b['f']:.3f} at 0 (falls: {r3f['f'] < b['f']}); "
      f"beta_bar {r3f['beta_bar']:.3f}. Unflipped oscillation: f samples the first quarter-cycle, Harvey's window the second half.")
    R[foot] = RF
P("POST-HOC only; kappa = 1/2 FITTED; not theory closed.")
open(os.path.join(HERE, "cfg725_posthoc.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(HERE, "cfg725_posthoc_results.json"), "w"), indent=1, default=str)
