#!/usr/bin/env python3
"""CFG591 (FROZEN_CRITERIA.md section 1): CFG559's kinetic toy rerun at each epoch z > 0 for the PRIMARY supply.
cfg559_toy.run_cell imported unchanged (CFG544 toy, FIX-2, IC-B, alpha 1, N 30000, seed 544, code step 5e-4, T = 10 Gyr bench end
state, last-1-Gyr average).  Cell = cfg559_toy.make_cell with the epoch inputs: the epoch halo grid (cfg591_lib.namespace(z)), s_c*(M_ta, z),
and the PHYSICAL turnaround radius r_ta,comoving/(1+z); r_M, r_* physical (true a0, flat).  At z = 0 CFG559's tables are reused (not rerun).
Output cfg591_toy_results.json: per z, a CFG559-format table (settings.nodes, cells["primary|<foot>|<node>"]) + the s_c*(z) grids.
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg591_toy.py   (4 worker processes)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg591_lib as C
try:
    os.nice(10)
except OSError:
    pass
spec = importlib.util.spec_from_file_location("cfg559_toy", os.path.join(C.D559, "cfg559_toy.py"))
T9 = importlib.util.module_from_spec(spec)
sys.modules["cfg559_toy"] = T9                    # so worker processes can pickle run_cell
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(T9)                       # main guarded; defines make_cell / run_cell, imports CFG544 unchanged
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
DESI = os.environ.get("CFG591_DESI", "0") == "1"           # ADDENDUM 1 variant: all five epochs, w0wa background, a0(z) tracking
SUF = "_DESI" if DESI else ""
if DESI:
    import cfg591_desi as DSI
    DESI_INFO = DSI.activate(*DSI.desi_w0wa())
ZRUN = list(C.ZNODES) if DESI else [z for z in C.ZNODES if z > 0]
NODES = T9.NODES


def make_cell_z(H, SC, lt, foot, z):
    """cfg559_toy.make_cell with the epoch inputs (ONE change set: epoch halo, s_c*(z), physical r_ta)."""
    MTA = H["MTA"]; i = int(np.argmin(abs(np.log10(MTA) - lt))); hb = H["HB"][i]; Mta = hb["Mta"]
    sc = float(SC[foot][i])
    FB, G, h = H["FB"], H["G"], H["h"]
    f = H["fret_of"](math.log10(Mta)); Mb = f * FB * Mta; Mset = sc * (1 - FB) * Mta; a0 = H["A0MPC_PHYS"][foot]
    rM = math.sqrt(G * Mb * h / a0)                                     # Mpc/h physical
    rs = rM / math.log1p(Mb / Mset)
    rta_phys = hb["rta"] / (1.0 + z)
    Vf = (G * Mb / h * a0) ** 0.25
    tu = rs / h / Vf * T9.MPC_KM_GYR
    c = dict(sys=f"lM{lt:.1f}", foot=foot, Mb=rM / rs, a=None, rta=rta_phys / rs, Mcat=(Mset / Mb) * rM / rs, dt=T9.DT_CODE, tu_Gyr=tu,
             log10_Mta=math.log10(Mta), sc=sc, fret=f, rM_over_rstar=rM / rs, Mset_over_Mb=Mset / Mb, rta_over_rstar=rta_phys / rs,
             T_over_tu=T9.T_GYR / tu, rstar_kpc=rs / h * 1000.0, Vf_kms=Vf, variant="primary", z=z)
    return c


if __name__ == "__main__":
    T0 = time.time()
    if DESI:
        P("[ADDENDUM 1 DESI-tracking variant: " + str(DESI_INFO) + "]")
    P("CFG591 toy -- FROZEN_CRITERIA.md. CFG559 toy (CFG544 FIX-2, IC-B, T 10 Gyr, alpha 1, N 30000) rerun per epoch, PRIMARY supply. "
      "kappa = 1/2 FITTED; footings never pooled; flat a0; cold energy mass required; not theory closed.")
    jobs, meta, grids = [], {}, {}
    for z in ZRUN:
        H = C.namespace(z)
        SC = {ft: C.sc_grid(H, ft, z) for ft in C.FOOTS}
        grids[str(z)] = dict(log10_Mta=np.log10(H["MTA"]).tolist(), log10_M200m=H["LM"].tolist(), Delta_ta=H["DTA"], Delta_ODE=H["Delta_ODE"], Dz=H["Dz"],
                             **{ft: SC[ft].tolist() for ft in C.FOOTS})
        for ft in C.FOOTS:
            for lt in NODES:
                c = make_cell_z(H, SC, lt, ft, z)
                nm = f"{z}|primary|{ft}|{lt:.1f}"
                jobs.append(dict(name=nm, c=c, ou_scale=1.0)); meta[nm] = c
        P(f"  z {z}: Delta_ta {H['DTA']:.4f} (ODE {H['Delta_ODE']:.4f}), D {H['Dz']:.4f}; s_c* at log M_ta 12/13/14/15 canonical: "
          + "/".join(f"{np.interp(l, np.log10(H['MTA']), SC['canonical']):.3f}" for l in (12, 13, 14, 15)))
    jobs.sort(key=lambda j: -j["c"]["T_over_tu"])            # longest first (steps scale with T/t_u)
    with get_context("fork").Pool(4) as pool:
        RES = pool.map(T9.run_cell, jobs, chunksize=1)
    R = {o["name"]: o for o in RES}
    res = dict(lane="CFG591", script="cfg591_toy", date="2026-10-10",
               settings=dict(T_Gyr=T9.T_GYR, dt_code=T9.DT_CODE, alpha=T9.ALPHA, N=T9.T544.NPART, seed=T9.T544.SEED, ic="B",
                             rule="FIX-2 (two-sided + OU)", ou_scale=1.0, nodes=NODES, kappa=0.5,
                             footings={"canonical": 9.3603e-11, "alt": 1.1312e-10}, z0_tables=("rerun (ADDENDUM 1)" if DESI else "CFG559 cfg559_toy_results.json (reused)"),
                             desi=(DESI_INFO if DESI else None)),
               grids=grids, tables={}, controls={})
    c6 = 0.0; c7 = True; ngate = 0
    P("\ncell                               rM/r*   Mset/Mb  rta/r*  T/tu   r*[kpc]  s_c   | r50 r90 r99 (kin/r*)  sharp r99  ln(r99/sharp)  r99/rta | dm@0.3  dm@0.5  dm@1  | logX    D      beta  gate")
    for z in ZRUN:
        tab = dict(settings=dict(nodes=NODES), cells={})
        for ft in C.FOOTS:
            for lt in NODES:
                nm = f"{z}|primary|{ft}|{lt:.1f}"; o = R[nm]; c = meta[nm]
                cell = {k: c[k] for k in ("log10_Mta", "sc", "fret", "rM_over_rstar", "Mset_over_Mb", "rta_over_rstar", "T_over_tu", "rstar_kpc", "Vf_kms", "tu_Gyr", "variant", "foot", "z")}
                cell.update({k: v for k, v in o.items() if k != "name"})
                cell["r99_over_rta"] = o["q_kin"]["r99"] / c["rta"]; cell["r99_sharp_over_rta"] = o["q_sharp"]["r99"] / c["rta"]
                tab["cells"][f"primary|{ft}|{lt:.1f}"] = cell
                c6 = max(c6, abs(o["C6"])); c7 = c7 and o["mass_exact"]; ngate += int(not o["gate"])
                P(f"{nm:34s} {c['rM_over_rstar']:.4f} {c['Mset_over_Mb']:7.2f} {c['rta_over_rstar']:6.2f} {c['T_over_tu']:5.2f} {c['rstar_kpc']:8.1f} {c['sc']:.3f} | "
                  f"{o['q_kin']['r50']:.3f} {o['q_kin']['r90']:.3f} {o['q_kin']['r99']:.3f}   {o['q_sharp']['r99']:.3f}   {o['ln_r99_over_sharp']:+.3f}   {cell['r99_over_rta']:.3f} | "
                  f"{o['dm_at']['0.3']:+.4f} {o['dm_at']['0.5']:+.4f} {o['dm_at']['1.0']:+.4f} | {o['final_logX']:+.3f} {o['final_D']:+.3f} {o['beta']:+.2f} "
                  f"{'pass' if o['gate'] else 'NOT STEADY/FAIL'}")
        res["tables"][str(z)] = tab
    res["controls"].update(C6_max=c6, C6_pass=c6 <= 1e-9, C7_mass_exact=c7, n_gate_fail=ngate)
    P(f"\nC6 max |m_sharp(1) - 1| {c6:.1e} -> {'PASS' if c6 <= 1e-9 else 'FAIL'};  C7 mass exact -> {'PASS' if c7 else 'FAIL'};  cells failing CFG544's gate: {ngate} of {len(jobs)}")
    P(f"elapsed {time.time() - T0:.0f} s")
    json.dump(res, open(os.path.join(HERE, f"cfg591_toy{SUF}_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg591_toy{SUF}.out"), "w").write("\n".join(OUT) + "\n")
