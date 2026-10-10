#!/usr/bin/env python3
"""CFG559 task 1 (FROZEN_CRITERIA.md, criteria commit 8485002fc): the kinetically supported settled cold-energy profile per halo.
CFG544's spherical N-body toy imported unchanged (as CFG554 does); FIX-2 = CFG554 route (b): two-sided drift toward rho_ph + OU relaxation
toward the isotropic Jeans dispersion of the current density in the current real-mass field (G9).  IC-B, 10 Gyr, alpha = 1, N = 30000.
Cells: log M_ta 11..15 (step 0.5) x footings x {primary s_c* (CFG557 alpha-free ceiling), variant s_c = 1}.
Output: Delta m(x) = m_kin(x) - m_sharp(x), x = r / r_*, per cell.
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg559_toy.py               -> cfg559_toy.out, cfg559_toy_results.json
  CFG559_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg559_toy.py -> *_MUTATE.* (MK2: OU target x 4 = sigma x 2, primary cells)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG559_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(10)
except OSError:
    pass
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(LANES, rel))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
_e = os.environ.pop("CFG544_MUTATE", None)
T544 = _load("cfg544", os.path.join("CFG544_settling_kinetic_consistency", "cfg544.py"))
J544 = json.load(open(os.path.join(LANES, "CFG544_settling_kinetic_consistency", "cfg544_results.json")))
JD = json.load(open(os.path.join(LANES, "CFG557_settling_catchment_derived", "cfg557_derive_results.json")))

# CFG556 halo basics (exec'd read-only up to its run block, as CFG557 does)
P556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
_src = open(P556).read(); _cut = _src.index("# ------------------------------------------------------------------ run")
H = {"__file__": P556, "__name__": "cfg556_ro"}
_e6 = os.environ.pop("CFG556_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "cfg556_ro", "exec"), H)
HB, MTA, FB, G, h, A0MPC, fret_of = H["HB"], H["MTA"], H["FB"], H["G"], H["h"], H["A0MPC"], H["fret_of"]
MPC_KM_GYR = 3.0856775814913673e19 / 3.15576e16      # 1 Mpc / (1 km/s) in Gyr

T_GYR, DT_CODE, ALPHA = 10.0, 5e-4, 1.0
NODES = [11.0 + 0.5 * i for i in range(9)]
FOOTS = ("canonical", "alt")
XG_N = 400

def make_cell(lt, foot, variant):
    i = int(np.argmin(abs(np.log10(MTA) - lt))); hb = HB[i]; Mta = hb["Mta"]
    g = JD["grid"][foot]; assert abs(g["log10_Mta"][i] - math.log10(Mta)) < 1e-10
    sc = float(g["ff"][i]) if variant == "primary" else 1.0
    f = fret_of(math.log10(Mta)); Mb = f * FB * Mta; Mset = sc * (1 - FB) * Mta; a0 = A0MPC[foot]
    rM = math.sqrt(G * Mb * h / a0)                                     # Mpc/h
    rs = rM / math.log1p(Mb / Mset)
    Vf = (G * Mb / h * a0) ** 0.25                                      # km/s
    tu = rs / h / Vf * MPC_KM_GYR
    c = dict(sys=f"lM{lt:.1f}", foot=foot, Mb=rM / rs, a=None, rta=hb["rta"] / rs, Mcat=(Mset / Mb) * rM / rs, dt=DT_CODE, tu_Gyr=tu,
             log10_Mta=math.log10(Mta), sc=sc, fret=f, rM_over_rstar=rM / rs, Mset_over_Mb=Mset / Mb, rta_over_rstar=hb["rta"] / rs,
             T_over_tu=T_GYR / tu, rstar_kpc=rs / h * 1000.0, Vf_kms=Vf, variant=variant)
    return c

def run_cell(job):
    """CFG544 run() loop (FIX-2 path) with identical call / RNG order; the energy bookkeeping (no state effect) is skipped;
    particle radii kept at the snapshots of the last 1 Gyr."""
    c, ou_scale, T = job["c"], job.get("ou_scale", 1.0), job.get("T", T_GYR)
    rng = np.random.default_rng(T544.SEED)
    r, vr, L, m = T544.make_ic(c, "B", rng)
    toy = T544.Toy(c, "two", ou=True, ou_scale=ou_scale, drift=True); toy.m = m
    n0 = r.size; dt = c["dt"]; nsteps = int(round(T / (dt * c["tu_Gyr"])))
    every = max(1, int(round(0.25 / (dt * c["tu_Gyr"]))))
    snaps, keep = [], []
    t0 = time.time()
    for it in range(nsteps + 1):
        if it % every == 0 or it == nsteps:
            dg = toy.diag(r, vr, L); t = it * dt * c["tu_Gyr"]; dg["t_Gyr"] = t; snaps.append(dg)
            if t >= T - 1.0 - 1e-9:
                keep.append(np.sort(r.copy()))
        if it == nsteps: break
        r, vr, _ = T544.vlasov_step(toy, r, vr, L, dt)
        vt = L / r
        g, _ = toy.gravity(r)
        rn, _w = toy.drift_step(r, dt, g)
        L = rn * vt; r = rn
        vr, vt, _dk = toy.ou_step(r, vr, vt, dt, g, rng)
        L = r * vt
    fin = snaps[-1]; ref = min(snaps, key=lambda s: abs(s["t_Gyr"] - (fin["t_Gyr"] - 2.0)))
    out = dict(name=job["name"], final_logX=fin["logX"], final_D=fin["D"], beta=fin["beta"], r99_diag=fin["r99"],
               frac_beyond_rta=fin["frac_beyond_rta"], d_logX_last2=fin["logX"] - ref["logX"], d_D_last2=fin["D"] - ref["D"],
               mass_exact=bool(r.size == n0), n=int(r.size), steps=nsteps, wall_s=time.time() - t0)
    out["gate"] = bool(abs(fin["logX"]) <= 0.1 and abs(fin["D"]) <= 0.1 and abs(out["d_logX_last2"]) <= 0.05 and abs(out["d_D_last2"]) <= 0.05)
    if job.get("profile", True):
        xta = c["rta"]; xg = np.geomspace(1e-3, xta, XG_N)
        mk = np.mean([np.searchsorted(np.minimum(rr, xta), xg, side="right") / rr.size for rr in keep], axis=0)
        ms = np.minimum(T544.Mph_enc(c, xg) / c["Mcat"], 1.0)
        dm = mk - ms
        allr = np.concatenate([np.minimum(rr, xta) for rr in keep])
        q = {f"r{p}": float(np.quantile(allr, p / 100)) for p in (50, 90, 99)}
        xs = np.geomspace(1e-3, 1.0, 20001); msx = T544.Mph_enc(c, xs) / c["Mcat"]
        q_sh = {f"r{p}": float(np.interp(p / 100, msx, xs)) for p in (50, 90, 99)}
        out.update(x=xg.tolist(), dm=dm.tolist(), m_kin=mk.tolist(), q_kin=q, q_sharp=q_sh, n_snap_avg=len(keep),
                   C6=float(T544.Mph_enc(c, np.array([1.0]))[0] / c["Mcat"] - 1.0),
                   dm_at={str(x): float(np.interp(x, xg, dm)) for x in (0.05, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0)},
                   ln_r99_over_sharp=math.log(q["r99"] / q_sh["r99"]),
                   poisson_dm_at={str(x): float(math.sqrt(max(np.interp(x, xg, mk) * (1 - np.interp(x, xg, mk)), 0) / n0)) for x in (0.05, 0.1, 0.3)})
    else:
        out.update(final_logX_full=fin["logX"], final_D_full=fin["D"])
    return out

if __name__ == "__main__":
    T0 = time.time()
    P(f"CFG559 toy {'(MUTATE: OU target x 4 = sigma x 2)' if MUTATE else ''} -- FROZEN_CRITERIA.md (8485002fc). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    P(f"Bench: CFG544 toy imported unchanged; FIX-2 (two-sided drift + isotropic Jeans OU), IC-B, T {T_GYR} Gyr, alpha {ALPHA}, N {T544.NPART}, dt_code {DT_CODE}, seed {T544.SEED}")
    jobs = []
    variants = ("primary",) if MUTATE else ("primary", "full")
    for var in variants:
        for ft in FOOTS:
            for lt in NODES:
                jobs.append(dict(name=f"{var}|{ft}|{lt:.1f}", c=make_cell(lt, ft, var), ou_scale=4.0 if MUTATE else 1.0))
    if not MUTATE:   # control C5: CFG544's own cells, its own dt, FIX-2 IC-B 10 Gyr
        for cn in ("MW_can", "cluster_can"):
            sy, fo = cn.split("_")
            jobs.insert(0, dict(name=f"C5|{cn}", c=T544.make_cell(sy, fo), profile=False))
    with get_context("fork").Pool(4) as pool:
        RES = pool.map(run_cell, jobs, chunksize=1)
    R = {o["name"]: o for o in RES}
    res = dict(lane="CFG559", script="cfg559_toy", date="2026-10-10", mutate=MUTATE, criteria_commit="8485002fc",
               settings=dict(T_Gyr=T_GYR, dt_code=DT_CODE, alpha=ALPHA, N=T544.NPART, seed=T544.SEED, ic="B", rule="FIX-2 (two-sided + OU)",
                             ou_scale=4.0 if MUTATE else 1.0, nodes=NODES, kappa=0.5, footings={"canonical": 9.3603e-11, "alt": 1.1312e-10}),
               cells={}, controls={})
    if not MUTATE:
        c5 = {}
        for cn in ("MW_can", "cluster_can"):
            o = R[f"C5|{cn}"]; ref = J544["runs"][f"{cn}|fix2_B"]["final"]
            d = max(abs(o["final_logX"] - ref["logX"]), abs(o["final_D"] - ref["D"]))
            c5[cn] = dict(logX=o["final_logX"], D=o["final_D"], ref_logX=ref["logX"], ref_D=ref["D"], maxd=d, passed=d <= 1e-9)
            P(f"C5 {cn}: this loop logX {o['final_logX']:+.6f} D {o['final_D']:+.6f} vs CFG544 {ref['logX']:+.6f} {ref['D']:+.6f}: max|d| {d:.1e} -> {'PASS' if d <= 1e-9 else 'FAIL'}")
        res["controls"]["C5"] = c5
    c6 = 0.0; c7 = True
    P("\ncell                         rM/r*   Mset/Mb  rta/r*  T/tu   r*[kpc]  s_c   | r50 r90 r99 (kin/r*)  sharp r99  ln(r99/sharp)  r99/rta | dm@0.1  dm@0.3  dm@0.5  dm@1  | logX    D      beta  gate  beyond_rta")
    for j in jobs:
        if j["name"].startswith("C5"): continue
        o = R[j["name"]]; c = j["c"]
        cell = {k: c[k] for k in ("log10_Mta", "sc", "fret", "rM_over_rstar", "Mset_over_Mb", "rta_over_rstar", "T_over_tu", "rstar_kpc", "Vf_kms", "tu_Gyr", "variant", "foot")}
        cell.update({k: v for k, v in o.items() if k != "name"})
        cell["r99_over_rta"] = o["q_kin"]["r99"] / c["rta"]; cell["r99_sharp_over_rta"] = o["q_sharp"]["r99"] / c["rta"]
        res["cells"][j["name"]] = cell
        c6 = max(c6, abs(o["C6"])); c7 = c7 and o["mass_exact"]
        P(f"{j['name']:28s} {c['rM_over_rstar']:.4f} {c['Mset_over_Mb']:7.2f} {c['rta_over_rstar']:6.2f} {c['T_over_tu']:5.2f} {c['rstar_kpc']:8.1f} {c['sc']:.3f} | "
          f"{o['q_kin']['r50']:.3f} {o['q_kin']['r90']:.3f} {o['q_kin']['r99']:.3f}   {o['q_sharp']['r99']:.3f}   {o['ln_r99_over_sharp']:+.3f}   {cell['r99_over_rta']:.3f} | "
          f"{o['dm_at']['0.1']:+.4f} {o['dm_at']['0.3']:+.4f} {o['dm_at']['0.5']:+.4f} {o['dm_at']['1.0']:+.4f} | {o['final_logX']:+.3f} {o['final_D']:+.3f} {o['beta']:+.2f} "
          f"{'pass' if o['gate'] else 'NOT STEADY/FAIL'} {o['frac_beyond_rta']:.4f}")
    res["controls"].update(C6_max=c6, C6_pass=c6 <= 1e-9, C7_mass_exact=c7)
    P(f"\nC6 max |m_sharp(1) - 1| {c6:.1e} -> {'PASS' if c6 <= 1e-9 else 'FAIL'};  C7 mass exact in every run -> {'PASS' if c7 else 'FAIL'}")
    P(f"elapsed {time.time() - T0:.0f} s")
    json.dump(res, open(os.path.join(HERE, f"cfg559_toy_results{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg559_toy{SUF}.out"), "w").write("\n".join(OUT) + "\n")
