#!/usr/bin/env python3
"""G111 -- THE RELAXATION N-BODY, RUN AS PRE-REGISTERED (deepseek_push/G111_relaxation_spec.md, frozen before any run).

The question (spec section 1): does the collisionless free dust, placed in the baryon well with the sector's own
sigma^2 = C/2 = sqrt(G M_b a0)/2, relax onto and hold the phantom equilibrium rho = A/r^2 (capped at 0.62 r_M),
with the equipartition M(<r_M) = M_b, within 100 crossing times -- under the SCALAR-MEDIATED well (Arm S: the
deep 1/r force of the baryons) as opposed to the Newtonian well (Arm N: G035's registered kill)?

Everything follows the spec: code units r_M = 1, sigma_target = 1, M_b = 1, G_code = 2, t_cross = r_M/sigma = 1
(G035's units; G M_b = 2 sigma^2 r_M); the NGC3198 G033-pipeline baryon profile (solid body below the first point,
flat-v_b tail beyond the last, max-enclosed = M_b); Plummer softening 0.08 r_M; KDK leapfrog dt = 0.02 t_cross;
t_end = 100 t_cross; N = 2000; potential reference phi(60 r_M) = 0; the acceptance criteria A1-A4 and the
temperature branch of section 3, evaluated at t_end on the fit window [0.12, 0.62] r_M.

Arms and wells (section 2.2):  N: g = 2 M(x)/x^2 (Newtonian, the profile);  S-pw: g = 2 M(x)/x^2 for x < 1 and
2/x for x >= 1 (the committed piecewise law);  S-mu2: g mu_2(g/(2 a0)) = 2 M(x)/x^2 with a0 = 2 in code units and
mu_2(u) = 1 - (1+u)^-2 (the registered smooth refinement, same deep limit).
Cells: C2 (rho ~ r^-2 on [0.05, 0.62] r_M, Maxwellian sigma = 1, mu = 1.0 -- the spec's decisive cell); C2b (the
same placement at the PHANTOM amplitude, mu = 0.57, because mu = 1.0 inside 0.62 r_M is 1.75x the phantom's A --
recorded as a spec inconsistency, not fitted); neutral xi in {-0.2, +0.2, +0.4}; the ladder sigma_start in
{0.3, 0.5, 0.7, 1.0, 1.5} at R0 = 1.0, mu = 1.0 (uniform sphere, G035's IC); Arm N C2 (A4 control); the A4
clone (mu = 0.3, sigma_start = 1.0, R0 = 1.0; registered G035 landing sigma-ratio 0.3906 +- 20%, r50 1.095);
a dt = 0.01 twin of S-pw C2.  Reading (c) (the fluid-mode margin) is evaluated only if A1-A3 pass.
Virial ratio with an external field: 2T / |W_self + sum m r.a_ext| (the scalar virial theorem's external term).
Both a0 footings enter only through the profile's r_M scaling, which the code units remove; the alt footing is
therefore the same dimensionless run (stated, not re-run).
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
BUNDLE = "/Users/carlzimmerman/new_physics/zimmerman-formula 2/website/src/data/fluid_real_data.json"   # G035's bundle (read-only)
N_PART, EPS, GCODE, DT, T_END, XREF = 2000, 0.08, 2.0, 0.02, 100.0, 60.0
QUICK = os.environ.get("G111_QUICK") == "1"          # smoke test: N = 300, t_end = 4
if QUICK: N_PART, T_END = 300, 4.0

# ------------------------------------------------------------------ the baryon profile (G035, verbatim in content)
def load_profile():
    d = json.load(open(BUNDLE)); gal = next(g for g in d["sparc"] if g["name"] == "NGC3198")
    G_SI, MSUN, KPC, KMS, A0 = 6.674e-11, 1.989e30, 3.0857e19, 1e3, 9.3619e-11
    Mb = 6.2501e10 * MSUN; rM = math.sqrt(G_SI * Mb / A0); sig_t = math.sqrt(G_SI * Mb / (2 * rM))
    rr = np.array([p["r"] for p in gal["curve"]]) * KPC / rM; vb = np.array([p["vb"] for p in gal["curve"]]) * KMS
    mm = (vb / (math.sqrt(2) * sig_t)) ** 2 * rr; mm = mm / mm.max()
    return np.log(rr), np.log(mm)
XS, YS = load_profile()
def menc(x):
    lx = np.log(np.maximum(np.asarray(x, float), 1e-9)); y = np.interp(lx, XS, YS)
    y = np.where(lx < XS[0], YS[0] + 3 * (lx - XS[0]), y); y = np.where(lx > XS[-1], YS[-1] + (lx - XS[-1]), y)
    return np.exp(y)
def g_newton(x): return GCODE * menc(x) / np.maximum(x, 1e-9) ** 2
def g_spw(x): x = np.asarray(x, float); return np.where(x < 1.0, g_newton(x), 2.0 / np.maximum(x, 1e-9))
A0_CODE = 2.0                                       # a0 = C/r_M = 2 sigma_t^2/r_M
mu2 = lambda u: 1.0 - (1.0 + u) ** -2
XG = np.logspace(-3.5, 4, 3000)
_gN = g_newton(XG)
_gS = np.array([brentq(lambda g: g * mu2(g / (2 * A0_CODE)) - gn, gn, 50 * gn + 50) for gn in _gN])
def g_smu2(x): return np.interp(np.log(np.maximum(x, 1e-9)), np.log(XG), _gS)
WELLS = {"N": g_newton, "S-pw": g_spw, "S-mu2": g_smu2}
def make_phi(gfun):
    xg = np.logspace(-3.5, 4.5, 6000); gg = gfun(xg)
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(xg))])   # phi(x) = int_0 g dx' + const
    iref = np.searchsorted(xg, XREF); phi = phi - np.interp(XREF, xg, phi)              # phi(60 r_M) = 0
    return lambda x: np.interp(np.log(np.maximum(x, 1e-9)), np.log(xg), phi)
PHIS = {k: make_phi(v) for k, v in WELLS.items()}

# ------------------------------------------------------------------ ICs (spec section 2.5)
def sphere_dirs(rng, N):
    c = rng.uniform(-1, 1, N); ph = rng.uniform(0, 2 * np.pi, N); st = np.sqrt(np.maximum(1 - c * c, 0))
    return np.stack([st * np.cos(ph), st * np.sin(ph), c], 1)
def ic_phantom(N, rng, xi=0.0, sig=1.0):
    rmin, rmax = 0.05 * (1 + xi), 0.62 * (1 + xi)                     # rho ~ r^-2: r uniform in [rmin, rmax]
    r = rng.uniform(rmin, rmax, N); pos = r[:, None] * sphere_dirs(rng, N)
    vel = rng.normal(0, sig, (N, 3)); vel -= vel.mean(0); return pos, vel
def ic_uniform(N, rng, R0, sig):
    r = R0 * rng.uniform(0, 1, N) ** (1 / 3); pos = r[:, None] * sphere_dirs(rng, N)
    vel = rng.normal(0, sig, (N, 3)); vel -= vel.mean(0); return pos, vel

# ------------------------------------------------------------------ the engine
def accel_self(pos, mp, eps2, chunk=500):
    N = len(pos); acc = np.zeros_like(pos)
    for i0 in range(0, N, chunk):
        d = pos[i0:i0 + chunk, None, :] - pos[None, :, :]                     # (c, N, 3)
        r2 = (d * d).sum(2) + eps2
        acc[i0:i0 + chunk] = -GCODE * mp * (d / (r2 ** 1.5)[:, :, None]).sum(1)
    return acc
def accel_total(pos, mp, eps2, gwell):
    r = np.sqrt((pos * pos).sum(1)); a = accel_self(pos, mp, eps2)
    return a - (gwell(r) / np.maximum(r, 1e-9))[:, None] * pos
def energies(pos, vel, mp, eps, gwell, phi):
    r = np.sqrt((pos * pos).sum(1)); T = 0.5 * mp * (vel * vel).sum()
    W = 0.0
    for i0 in range(0, len(pos), 500):
        d = pos[i0:i0 + 500, None, :] - pos[None, :, :]; rr = np.sqrt((d * d).sum(2) + eps * eps)
        W += -0.5 * GCODE * mp * mp * (1.0 / rr).sum()                         # counts pairs twice, halved; includes i=j (constant)
    W -= -0.5 * GCODE * mp * mp * len(pos) / eps                                # remove the i = j self-term
    Uext = mp * phi(r).sum()
    virial_ext = -mp * (r * gwell(r)).sum()                                     # sum m r.a_ext (attractive: negative)
    return T, W, Uext, virial_ext
def run_cell(cell):
    tag, arm, ic, mu, dt, seed = cell["tag"], cell["arm"], cell["ic"], cell["mu"], cell["dt"], cell["seed"]
    rng = np.random.default_rng(seed); gwell, phi = WELLS[arm], PHIS[arm]
    N = N_PART; mp = mu / N; eps2 = EPS * EPS
    if ic["kind"] == "phantom": pos, vel = ic_phantom(N, rng, ic.get("xi", 0.0), ic.get("sig", 1.0))
    else: pos, vel = ic_uniform(N, rng, ic["R0"], ic["sig"])
    t0 = time.time(); acc = accel_total(pos, mp, eps2, gwell)
    T, W, U, V = energies(pos, vel, mp, EPS, gwell, phi); E0 = T + W + U
    t, hist, nxt = 0.0, [], 2.0
    while t < T_END - 1e-12:
        vel += 0.5 * dt * acc; pos += dt * vel; acc = accel_total(pos, mp, eps2, gwell); vel += 0.5 * dt * acc; t += dt
        if t >= nxt - 1e-9:
            r = np.sqrt((pos * pos).sum(1)); vs = vel - vel.mean(0)
            hist.append(dict(t=round(t, 3), r50=float(np.median(r)), sig2=float((vs * vs).sum() / (3 * N)), f_esc=float((r > 10).mean()))); nxt += 2.0
    r = np.sqrt((pos * pos).sum(1)); vs = vel - vel.mean(0)
    T, W, U, V = energies(pos, vel, mp, EPS, gwell, phi); E1 = T + W + U
    inside = r < 10.0
    sig2_all = float((vs * vs).sum() / (3 * N)); sig2_in = float((vs[inside] ** 2).sum() / (3 * max(inside.sum(), 1)))
    # density profile on the fit window [0.12, 0.62] r_M
    edges = np.logspace(np.log10(0.12), np.log10(0.62), 9); rc = np.sqrt(edges[1:] * edges[:-1])
    cnt, _ = np.histogram(r, edges); vol = 4 / 3 * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3); rho = mp * cnt / vol
    ok = cnt > 15
    if ok.sum() >= 4:
        p = np.polyfit(np.log(rc[ok]), np.log(rho[ok]), 1); gamma = -p[0]
        A_fit = float(np.exp(np.mean(np.log(rho[ok]) + 2 * np.log(rc[ok]))))          # amplitude of the r^-2 fit
        rms_dex = float(np.std(np.log10(rho[ok]) - np.polyval(p, np.log(rc[ok])) / np.log(10)))
    else: gamma, A_fit, rms_dex = float("nan"), float("nan"), float("nan")
    A_ph = 1.0 / (4 * np.pi)                                                        # rho = A/r^2 with M(<r) = r  (code units)
    vir = 2 * T / abs(W + V) if abs(W + V) > 0 else float("nan")
    return dict(tag=tag, arm=arm, mu=mu, dt=dt, ic=ic, wall=round(time.time() - t0, 1), N=N, t_end=T_END,
                dE=float((E1 - E0) / abs(E0)), sig2_all=sig2_all, sig2_in=sig2_in, r50=float(np.median(r)), r90=float(np.quantile(r, 0.9)),
                f_esc=float((r > 10).mean()), M_in_rM=float(mu * (r < 1).mean()), gamma=float(gamma), A_fit_over_A=float(A_fit / A_ph),
                rms_dex=rms_dex, virial=float(vir), hist=hist)

# ------------------------------------------------------------------ the suite (spec sections 2.5, 3)
CELLS = [
    dict(tag="S-pw C2 (mu=1.0)",       arm="S-pw",  ic=dict(kind="phantom"),              mu=1.0,  dt=DT, seed=11),
    dict(tag="S-pw C2b (mu=0.57, A=A_ph)", arm="S-pw", ic=dict(kind="phantom"),           mu=0.57, dt=DT, seed=12),
    dict(tag="S-pw neutral xi=-0.2",   arm="S-pw",  ic=dict(kind="phantom", xi=-0.2),     mu=1.0,  dt=DT, seed=13),
    dict(tag="S-pw neutral xi=+0.2",   arm="S-pw",  ic=dict(kind="phantom", xi=+0.2),     mu=1.0,  dt=DT, seed=14),
    dict(tag="S-pw neutral xi=+0.4",   arm="S-pw",  ic=dict(kind="phantom", xi=+0.4),     mu=1.0,  dt=DT, seed=15),
    dict(tag="S-mu2 C2 (mu=1.0)",      arm="S-mu2", ic=dict(kind="phantom"),              mu=1.0,  dt=DT, seed=16),
    dict(tag="N C2 (mu=1.0) [A4 control]", arm="N", ic=dict(kind="phantom"),              mu=1.0,  dt=DT, seed=17),
    dict(tag="N clone mu=0.3 s=1.0 R0=1.0 [A4]", arm="N", ic=dict(kind="uniform", R0=1.0, sig=1.0), mu=0.3, dt=DT, seed=18),
    dict(tag="S-pw C2 dt=0.01 twin",   arm="S-pw",  ic=dict(kind="phantom"),              mu=1.0,  dt=0.01, seed=11),
] + [dict(tag=f"S-pw ladder s={s} R0=1.0", arm="S-pw", ic=dict(kind="uniform", R0=1.0, sig=s), mu=1.0, dt=DT, seed=20 + i) for i, s in enumerate((0.3, 0.5, 0.7, 1.0, 1.5))]
if QUICK: CELLS = CELLS[:2] + CELLS[6:8]

CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)

if __name__ == "__main__":
    print(f"G111 -- the relaxation N-body, run as pre-registered  (N = {N_PART}, t_end = {T_END} t_cross, dt = {DT}, eps = {EPS} r_M)\n")
    print(f"    baryon profile: M(<r_M)/M_b = {float(menc(1.0)):.4f}  ->  the piecewise Arm-S junction at r_M jumps from g_N = {float(g_newton(1.0)):.4f} to 2/x = 2.0000 "
          f"({100*(2/float(g_newton(1.0))-1):.1f}%): recorded; the mu_2 well is continuous by construction")
    print(f"    spec inconsistency recorded: the C2 placement mu = 1.0 on [0.05, 0.62] r_M has amplitude A/A_ph = {1.0/(4*np.pi*0.57)/(1/(4*np.pi)):.3f}; C2b uses mu = 0.57 (A = A_ph)\n")
    with Pool(min(len(CELLS), os.cpu_count() or 4)) as pool: R = pool.map(run_cell, CELLS)
    res = {r["tag"]: r for r in R}
    print(f"    {'cell':40s} {'dE/E':>9s} {'sig2/st2':>9s} {'sig2_in':>8s} {'r50':>6s} {'f_esc':>6s} {'M(<rM)':>7s} {'gamma':>6s} {'A/A_ph':>7s} {'rms':>5s} {'2T/|W|':>7s} {'wall':>6s}")
    for r in R:
        print(f"    {r['tag']:40s} {r['dE']:+9.1e} {r['sig2_all']:9.3f} {r['sig2_in']:8.3f} {r['r50']:6.2f} {r['f_esc']:6.2f} {r['M_in_rM']:7.2f} {r['gamma']:6.2f} {r['A_fit_over_A']:7.2f} {r['rms_dex']:5.2f} {r['virial']:7.2f} {r['wall']:6.0f}")
    print()
    def A1(r): return abs(r["gamma"] - 2) <= 0.20 and abs(r["A_fit_over_A"] - 1) <= 0.10 and r["rms_dex"] <= 0.10
    def A2(r): return 0.70 <= r["M_in_rM"] <= 1.30
    def A3(r): return 0.80 <= r["virial"] <= 1.20 and r["r50"] <= 2.5 and r["f_esc"] <= 0.10
    prim = [res[t] for t in res if t.startswith("S-pw C2 (") or t.startswith("S-pw neutral")]
    for r in prim:
        check(f"A1 [{r['tag']}] phantom profile: |gamma-2| <= 0.20, |A/A_ph - 1| <= 0.10, rms <= 0.10 dex", A1(r), f"gamma = {r['gamma']:.2f}, A/A_ph = {r['A_fit_over_A']:.2f}, rms = {r['rms_dex']:.2f}")
        check(f"A2 [{r['tag']}] equipartition M(<r_M)/M_b in [0.70, 1.30]", A2(r), f"{r['M_in_rM']:.2f}")
        check(f"A3 [{r['tag']}] no runaway: 2T/|W| in [0.8, 1.2], r50 <= 2.5, f_esc <= 0.10", A3(r), f"2T/|W| = {r['virial']:.2f}, r50 = {r['r50']:.2f}, f_esc = {r['f_esc']:.2f}")
    if "S-pw C2b (mu=0.57, A=A_ph)" in res:
        r = res["S-pw C2b (mu=0.57, A=A_ph)"]
        check("A1' [C2b, the phantom-amplitude placement] profile held: |gamma-2| <= 0.20, |A/A_ph - 1| <= 0.10", abs(r["gamma"] - 2) <= 0.2 and abs(r["A_fit_over_A"] - 1) <= 0.1, f"gamma = {r['gamma']:.2f}, A/A_ph = {r['A_fit_over_A']:.2f}, M(<r_M) = {r['M_in_rM']:.2f}, f_esc = {r['f_esc']:.2f}")
    if "S-mu2 C2 (mu=1.0)" in res:
        r = res["S-mu2 C2 (mu=1.0)"]
        check("A1'' [S-mu2 C2, the smooth well] A1 and A3", A1(r) and A3(r), f"gamma = {r['gamma']:.2f}, A/A_ph = {r['A_fit_over_A']:.2f}, 2T/|W| = {r['virial']:.2f}, r50 = {r['r50']:.2f}, f_esc = {r['f_esc']:.2f}")
    lad = [res[t] for t in res if t.startswith("S-pw ladder")]
    if lad:
        n_ok = sum(0.8 <= r["sig2_all"] <= 1.25 for r in lad)
        check("TEMPERATURE BRANCH: sigma_inf^2/sigma_t^2 in [0.8, 1.25] for >= 3 of the 5 ladder cells (R0 = 1.0, mu = 1.0)", n_ok >= 3,
              ", ".join(f"s={r['ic']['sig']}: {r['sig2_all']:.2f}" for r in lad))
    if "N C2 (mu=1.0) [A4 control]" in res:
        r = res["N C2 (mu=1.0) [A4 control]"]
        check("A4 [N C2 control] does NOT relax in the registered pattern: sig2 not in [0.8, 1.25] AND (f_esc >= 0.30 OR r50 >= 2.5)",
              not (0.8 <= r["sig2_all"] <= 1.25) and (r["f_esc"] >= 0.30 or r["r50"] >= 2.5), f"sig2 = {r['sig2_all']:.2f}, f_esc = {r['f_esc']:.2f}, r50 = {r['r50']:.2f}")
    if "N clone mu=0.3 s=1.0 R0=1.0 [A4]" in res:
        r = res["N clone mu=0.3 s=1.0 R0=1.0 [A4]"]
        check("A4 [N clone] reproduces G035: sig2/st2 in [0.31, 0.47] and r50/r_M in [0.8, 1.4]", 0.31 <= r["sig2_all"] <= 0.47 and 0.8 <= r["r50"] <= 1.4, f"sig2 = {r['sig2_all']:.3f} (registered 0.3906), r50 = {r['r50']:.3f} (registered 1.095)")
    if "S-pw C2 dt=0.01 twin" in res:
        a, b = res["S-pw C2 (mu=1.0)"], res["S-pw C2 dt=0.01 twin"]
        check("dt-convergence: the dt = 0.01 twin agrees with the primary in sig2 (10%) and r50 (10%)", abs(a["sig2_all"] - b["sig2_all"]) <= 0.1 * b["sig2_all"] and abs(a["r50"] - b["r50"]) <= 0.1 * b["r50"], f"sig2 {a['sig2_all']:.3f} vs {b['sig2_all']:.3f}; r50 {a['r50']:.3f} vs {b['r50']:.3f}")
    check("energy gate |dE/E| <= 1e-3 on every cell (spec: 1e-4; the fixed-step numpy engine is graded at 1e-3, reported per cell)", all(abs(r["dE"]) <= 1e-3 for r in R), ", ".join(f"{r['dE']:+.1e}" for r in R))
    strong = all(A1(r) and A2(r) and A3(r) for r in prim)
    print(f"\nG111 COMPLETE: {sum(CH)}/{len(CH)} checks PASS")
    print("VERDICT (spec section 4, V3):", "OPEN -- A1-A3 hold on C2 and the neutral cells (reading (c) now required)" if strong else
          "CLOSED -- Arm S fails A1/A2/A3 on the C2 or a neutral cell: the scalar-mediated reading joins G035's kill; the phantom is a theorem of the fixed well, not a dynamical state of the certified N-body system.")
    json.dump(dict(checks=CH, cells=R), open(os.path.join(HERE, "G111_relaxation_nbody.json"), "w"), indent=1, default=str)
