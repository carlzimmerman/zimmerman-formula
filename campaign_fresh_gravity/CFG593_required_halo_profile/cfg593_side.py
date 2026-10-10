#!/usr/bin/env python3
"""CFG593 side constraints (c) (FROZEN_CRITERIA.md sections 2, 3c, 7): the declared profile family against
  groups: CFG543 P2 (Tian+26 groups; stellar Hernquist baryons; f_cond 0.10 catchment), |Z| < 2;
  MW:     |dV_c| <= 5.4 km/s at 8.2, 16, 20, 30 kpc and |dSigma_dark(R0, 1.1 kpc)| <= 5.8 Msun/pc^2 relative to the law (CFG553 band half-widths).
Machinery read-only: CFG543 (imported), CFG513 (exec'd up to its section 1), CFG556 NFW shape (cfg593_lib).
  nice -n 10 python3 cfg593_side.py                 -> cfg593_side.out, cfg593_side_results.json
  CFG593_MUTATE=1 nice -n 10 python3 cfg593_side.py -> *_MUTATE.* (K4 + the family's f = 1, x_e = 1 member reproduces the law in the MW: dV = 0)
DIAGNOSTIC, data-driven.  kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg593_lib as FL
LANES = FL.LANES
MUT = os.environ.get("CFG593_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
try:
    os.nice(10)
except OSError:
    pass
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

H = FL.H556(); h = H["h"]; MPC_M = 3.0856775814913673e22
P(f"CFG593 side constraints {'(MUTATE)' if MUT else ''} -- FROZEN_CRITERIA.md. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P("DIAGNOSTIC, data-driven: allowed profiles are what the data require, NOT a framework derivation.")

# ---------------------------------------------------------------- groups (CFG543 P2)
sys.path.insert(0, os.path.join(LANES, "CFG543_group_supply"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as M43                                       # noqa: E402  (read-only)
M43.GEO = M43.gas_geometry(M43.lovisari())
ROWS = M43.read_groups()
J43 = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results.json")))
FMAP = {"can": "canonical", "alt": "alt"}
FC = 0.10
_SH = {}
def shape(lMta_h):
    k = round(lMta_h, 6)
    if k not in _SH:
        _SH[k] = FL.ML_shape(lMta_h)
    return _SH[k]


def sigma_family(o, a0, xe, f, y, conv="total", mode="family", dlM=0.0):
    lM = o["lM"] + dlM
    M, Mhot, Msup, _ = M43.config_masses(lM, dict(kind="P2"))
    assert Mhot == 0.0
    Re = o["Re"]; a = Re * M43.KPC / M43.HERN_RE
    X = M43.X; r = X * a                                                   # m
    Mb = M * M43.M_T
    gN = M43.G * Mb * M43.MSUN / r ** 2
    nu = M43.C.nu(gN / a0)
    S = (nu - 1.0) * Mb
    if mode == "k4":                                                       # CFG543's discrete supply edge, lane convention
        k = np.where(S >= Msup)[0]
        Mtot = Mb + S
        if len(k):
            xe_i = k[0]; Mtot = np.where(np.arange(len(X)) > xe_i, Mb + S[xe_i], Mtot)
    else:
        Mta = M / FC * (1.0 + M43.COLD_PER_B)                               # catchment M_ta = M / (f_cond f_b): supply = COLD_PER_B M / f_cond = (1 - f_b) M_ta
        lMta_h = math.log10(Mta * h)
        MLx, hb = shape(lMta_h)
        rta = hb["rta"] / h * MPC_M
        rM = math.sqrt(M43.G * M * M43.MSUN / a0)
        cap = True
        if mode == "emg":
            re = rta; f_, rin = 1.0, 0.0
        else:
            re = min(xe * rta, rta); rin = y * rM; f_ = f
        def grid(re_, rin_):
            rr = np.unique(np.concatenate([r[r < rta], [x for x in (re_, rin_) if 0 < x < rta], [rta]]))
            mb = M * np.interp(rr, r, M43.M_T, right=1.0)
            Sg = np.interp(rr, r, S, right=float(np.interp(rta, r, S)))
            return rr, mb, Sg, Mta * MLx(rr / rta)
        rr, mb, Sg, ML = grid(re, rin)
        Mf, inf = FL.family_cum(rr, mb, Sg, ML, Mta, re, rin, f_, Msup, cap)
        if Mf is None:
            re = inf["re_new"]; rr, mb, Sg, ML = grid(re, rin)
            Mf, inf = FL.family_cum(rr, mb, Sg, ML, Mta, re, rin, f_, Msup, cap=False)
        if conv == "lane":
            rin_ = min(rin, re)
            S_in = np.interp(np.minimum(rr, rin_), rr, Sg); S_e = np.interp(np.minimum(rr, re), rr, Sg)
            Mf = mb + S_in + f_ * (S_e - S_in)
        Mtot = np.interp(r, rr, Mf)
    g = M43.G * Mtot * M43.MSUN / r ** 2
    s2 = np.trapezoid(4 * np.pi * X ** 2 * M43.RHO_T * r * g * X, M43.LX) / 3.0
    return 0.5 * math.log10(s2) - 3.0


def run_groups(a0, xe, f, y, conv="total", mode="family"):
    lp = np.array([sigma_family(o, a0, xe, f, y, conv, mode) for o in ROWS])
    lp2 = np.array([sigma_family(o, a0, xe, f, y, conv, mode, 0.01) for o in ROWS])
    D = np.array([o["ls"] for o in ROWS]) - lp
    return M43.stats(D, (lp2 - lp) / 0.01)


# ---------------------------------------------------------------- MW (CFG513 Prof baryons)
P513 = os.path.join(LANES, "CFG513_milky_way_cold_energy_profile", "cfg513_mw_profile.py")
_src = open(P513).read(); _mk = "# ================================================================================================ 1. the framework's MW"
NS = {"__file__": P513, "__name__": "cfg513_ro"}
_e = os.environ.pop("CFG513_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index(_mk)], "cfg513_ro", "exec"), NS)
Prof, G513, A0513, nu513, MB_PRIM = NS["Prof"], NS["G"], NS["A0"], NS["nu_mono"], NS["MB_PRIM"]
sys.path.insert(0, os.path.join(LANES, "CFG515_census_edge_resolution"))
import cfg515_lib as L15                                                    # noqa: E402
fM, lMta_mw = L15.fret_census(MB_PRIM)
RK = (8.2, 16.0, 20.0, 30.0)


def mw_eval(foot, xe, f, y, conv="total"):
    pr = Prof("mw", Mb=MB_PRIM, foot=foot, fret=None)
    a0 = A0513[foot]; Mbt = pr.Mb_tot()
    Mta = 10 ** lMta_mw / L15.H16; supply = (1 - L15.FB) * Mta
    MLx, hb = shape(lMta_mw)
    rta = hb["rta"] / h * 1000.0
    rM = math.sqrt(G513 * Mbt / a0)
    re = min(xe * rta, rta); rin = y * rM
    def grid(re_, rin_):
        rr = np.unique(np.concatenate([np.geomspace(1e-3, rta, 3000)[:-1], [x for x in (re_, rin_, 6.0, 10.5) + RK if 0 < x < rta], [rta]]))
        mb = pr.Mb_enc(rr)
        S = mb * (nu513(G513 * mb / (rr ** 2 * a0)) - 1.0)
        return rr, mb, S, Mta * MLx(rr / rta)
    rr, mb, S, ML = grid(re, rin)
    Mf, inf = FL.family_cum(rr, mb, S, ML, Mta, re, rin, f, supply, True)
    if Mf is None:
        re = inf["re_new"]; rr, mb, S, ML = grid(re, rin)
        Mf, inf = FL.family_cum(rr, mb, S, ML, Mta, re, rin, f, supply, cap=False)
    if conv == "lane":
        rin_ = min(rin, re)
        S_in = np.interp(np.minimum(rr, rin_), rr, S); S_e = np.interp(np.minimum(rr, re), rr, S)
        Mf = mb + S_in + f * (S_e - S_in)
    Mlaw = mb + S
    dV = {str(rk): math.sqrt(G513 * float(np.interp(rk, rr, Mf)) / rk) - math.sqrt(G513 * float(np.interp(rk, rr, Mlaw)) / rk) for rk in RK}
    dsh = (np.interp(10.5, rr, Mf) - np.interp(10.5, rr, Mlaw)) - (np.interp(6.0, rr, Mf) - np.interp(6.0, rr, Mlaw))
    vol = 4 / 3 * math.pi * (10.5 ** 3 - 6.0 ** 3) * 1e9
    dSig = float(2 * 1100.0 * dsh / vol)
    ok = all(abs(v) <= 5.4 for v in dV.values()) and abs(dSig) <= 5.8
    return dict(dV=dV, dSigma=dSig, passed=bool(ok), re_kpc=float(re), rta_kpc=float(rta))


res = dict(lane="CFG593", script="cfg593_side", date="2026-10-10", mutate=MUT, n_groups=len(ROWS),
           settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; candidate B; cold energy mass required; not theory closed; DIAGNOSTIC data-driven")
# K4
k4 = {}
for fk, a0 in M43.FOOT.items():
    st = run_groups(a0, 0, 0, 0, "lane", "k4")
    k4[FMAP[fk]] = abs(st["mean"] - J43["footings"][fk]["configs"]["P2"]["mean"])
k4p = all(v <= 1e-4 for v in k4.values())
P(f"\nK4 group code (lane convention, CFG543 supply edge) vs CFG543 stored P2 mean: |d| {k4} -> {'PASS' if k4p else 'FAIL'}  ({len(ROWS)} groups)")
mwlaw = {ft: mw_eval(ft, 1.0, 1.0, 0) for ft in ("canonical", "alt")}
k5mw = max(abs(v) for o in mwlaw.values() for v in o["dV"].values())
P(f"K-MW the family's x_e = 1, f = 1 member reproduces the law inside 30 kpc: max |dV| {k5mw:.1e} km/s -> {'PASS' if k5mw <= 1e-9 else 'FAIL'}")
res["controls"] = dict(K4=k4, K4_pass=k4p, KMW=k5mw, KMW_pass=k5mw <= 1e-9)

ref = {}
for fk, a0 in M43.FOOT.items():
    ft = FMAP[fk]
    ref[ft] = {"emergent edge, total": run_groups(a0, 0, 0, 0, "total", "emg"), "family NFW member (x_e = 1, f = 0), total": run_groups(a0, 1.0, 0.0, 0, "total"),
               "CFG543 P2 (stored)": J43["footings"][fk]["configs"]["P2"]}
    P(f"  [{ft}] groups: emergent edge total Z {ref[ft]['emergent edge, total']['Z']:+.2f}; NFW member Z {ref[ft]['family NFW member (x_e = 1, f = 0), total']['Z']:+.2f}; "
      f"CFG543 P2 stored mean {J43['footings'][fk]['configs']['P2']['mean']:+.4f}")
    nm = mw_eval(ft, 1.0, 0.0, 0)
    ref[ft]["MW NFW member"] = nm
    P(f"  [{ft}] MW NFW member: dV " + " ".join(f"{k}:{v:+.1f}" for k, v in nm["dV"].items()) + f"; dSigma {nm['dSigma']:+.2f} -> {nm['passed']}")
res["reference"] = {ft: {k: ({kk: vv for kk, vv in v.items() if kk != "Delta"} if isinstance(v, dict) else v) for k, v in d.items()} for ft, d in ref.items()}

if MUT:
    res["all_teeth_bite"] = bool(k4p and k5mw <= 1e-9)
    P(f"\nMUTATE (side): K4 and the MW law member reproduce their sources -> {res['all_teeth_bite']}")
else:
    scan = {}
    PTS = FL.family_points()
    for fk, a0 in M43.FOOT.items():
        ft = FMAP[fk]
        for cv in ("total", "lane"):
            for (xe, f, y) in PTS:
                st = run_groups(a0, xe, f, y, cv)
                mw = mw_eval(ft, xe, f, y, cv)
                scan[f"{ft}|{cv}|{xe:.2f}|{f:.1f}|{y}"] = dict(xe=xe, f=f, y=y, groups_mean=st["mean"], groups_Z=st["Z"], groups_pass=bool(abs(st["Z"]) < 2),
                                                               mw_dV=mw["dV"], mw_dSigma=mw["dSigma"], mw_pass=mw["passed"], allowed=bool(abs(st["Z"]) < 2 and mw["passed"]))
            P(f"  [{ft} | {cv}] scanned ({time.time() - T0:.0f} s): groups pass {sum(1 for k, v in scan.items() if k.startswith(f'{ft}|{cv}|') and v['groups_pass'])}, "
              f"MW pass {sum(1 for k, v in scan.items() if k.startswith(f'{ft}|{cv}|') and v['mw_pass'])}, both {sum(1 for k, v in scan.items() if k.startswith(f'{ft}|{cv}|') and v['allowed'])} / {len(PTS)}")
    res["scan"] = scan
    for ft in ("canonical", "alt"):
        P(f"  [{ft}] groups Z, total, y = 0: rows f = 0..1, columns x_e = " + " ".join(f"{x:g}" for x in FL.XE_GRID))
        for f in FL.F_GRID:
            P(f"     f {f:.1f}: " + " ".join(f"{scan[f'{ft}|total|{xe:.2f}|{f:.1f}|0']['groups_Z']:+5.2f}" for xe in FL.XE_GRID))
        P(f"  [{ft}] MW max|dV| (km/s), total, y = 0:")
        for f in FL.F_GRID:
            P(f"     f {f:.1f}: " + " ".join(f"{max(abs(v) for v in scan[f'{ft}|total|{xe:.2f}|{f:.1f}|0']['mw_dV'].values()):5.1f}" for xe in FL.XE_GRID))

P(f"\nelapsed {time.time() - T0:.0f} s")
json.dump(res, open(os.path.join(HERE, f"cfg593_side_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg593_side{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    sys.exit(1 if res["all_teeth_bite"] else 0)
