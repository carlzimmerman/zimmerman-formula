#!/usr/bin/env python3
"""XG1_sluggs_atlas_gas: Chandra Galaxy Atlas emission-measure profiles (NGC 4374, NGC 5846) -> beta-model deprojection ->
does the record's extrapolated hot gas (CFG331) exist beyond the measured edge? Frozen criteria ef0c2788ae (committed alone).
CFG331's machinery executed read-only (as CFG528 does). Data-only; no gravity model enters.

kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 python3 -I xg1_atlas_gas.py      (XG1_MUTATE=1 twin)
"""
import os, sys, io, json, math, hashlib, contextlib
import numpy as np
from scipy.optimize import least_squares
from scipy.integrate import quad

MUT = os.environ.get("XG1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
LANES = os.path.join(REPO, "campaign_fresh_gravity"); ATL = os.path.join(REPO, "_external_data", "chandra_galaxy_atlas")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"XG1_sluggs_atlas_gas (criteria ef0c2788ae){'  [MUTATE: beta = 1/3]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
_src = open(os.path.join(LANES, "CFG331_sluggs_centrals_environment", "cfg331_environment.py")).read()
_src = _src[:_src.index("\n# ------------------------------------------------------------------ run")]
os.environ.pop("CFG331_MUTATE", None)
NS = {"__file__": os.path.join(LANES, "CFG331_sluggs_centrals_environment", "cfg331_environment.py"), "__name__": "cfg331_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src, "cfg331_environment", "exec"), NS)
GAS, GAL, B, RG = NS["GAS"], NS["GAL"], NS["B"], NS["RG"]
LR = np.log(RG)
def m_extrap(n, r): return float(np.interp(math.log(r), LR, GAS[n][0]))
def m_trunc(n, r):
    rm = GAS[n][1]["r_meas"]; return m_extrap(n, min(r, rm))
checks = {}
k0 = all(abs(m_trunc(n, r) / m_extrap(n, r) - 1) < 1e-12 for n in (4374, 5846) for r in np.geomspace(1, GAS[n][1]["r_meas"] * 0.999, 5))
checks["K0"] = bool(k0)

def proj(R, A, rc, b): return A * (1 + (R / rc) ** 2) ** (-3 * b + 0.5)
RES = dict(criteria="ef0c2788ae", mutate=MUT, galaxies={}); k1 = True; k2 = True
for n, tag in ((4374, "N4374_90301"), (5846, "N5846_90201")):
    tarp = os.path.join(ATL, tag, "pack1.tar"); sha = hashlib.sha256(open(tarp, "rb").read()).hexdigest()
    T = np.loadtxt(os.path.join(ATL, tag, "pack1", f"{tag}_v01_AB_sn20_APECnPL_sum.dat"), comments="#")
    D = GAL[n]["D"]; kpc_per_arcmin = D * 1e3 * math.pi / (180 * 60)
    R = T[:, 1] * kpc_per_arcmin; Sig = T[:, 10]; lo, hi = T[:, 11], T[:, 12]; Tk = T[:, 6]
    ok = (R >= 2.0) & np.isfinite(Sig) & (Sig > 0) & (lo > 0) & (hi > lo)
    Rf, Sf = R[ok], Sig[ok]; ef = 0.5 * (np.log(hi[ok]) - np.log(lo[ok]))
    Rmax = float(R[np.isfinite(Sig) & (Sig > 0)].max()); rmeas = GAS[n][1]["r_meas"]; rgc = float(B[n]["Rb"][-1])
    fit = least_squares(lambda p: (np.log(proj(Rf, math.exp(p[0]), math.exp(p[1]), p[2])) - np.log(Sf)) / ef,
                        x0=[math.log(Sf.max()), math.log(2.0), 0.6], bounds=([-50, math.log(0.05), 0.35], [50, math.log(200), 3.0]))
    A, rc, beta = math.exp(fit.x[0]), math.exp(fit.x[1]), float(fit.x[2])
    k2 &= not MUT
    bu = (1 / 3) if MUT else beta
    ne = lambda r: (1 + (r / rc) ** 2) ** (-1.5 * bu)
    Mshape = lambda r: quad(lambda x: 4 * math.pi * x * x * ne(x), 0, r, limit=200)[0]
    # K1: projecting n_e^2 reproduces the fitted projected shape (relative, three radii)
    pr = [2 * quad(lambda z: ne(math.hypot(Rq, z)) ** 2, 0, 50 * max(rc, Rq), limit=400)[0] for Rq in (3.0, 8.0, 15.0)]
    rel = [pr[i] / pr[0] / (proj(Rq, 1, rc, bu) / proj(3.0, 1, rc, bu)) - 1 for i, Rq in enumerate((3.0, 8.0, 15.0))]
    k1 &= max(abs(x) for x in rel) < 1e-3
    rn = min(rmeas, Rmax); rt = min(rgc, Rmax)
    norm = m_trunc(n, rn) / Mshape(rn)
    Ma, Mt, Me = norm * Mshape(rt), m_trunc(n, rt), m_extrap(n, rt)
    informative = Rmax > rmeas
    f = (Ma - Mt) / (Me - Mt) if (Me - Mt) > 0 else float("nan")
    v = "NOT INFORMATIVE" if not informative else ("EXTRAPOLATED GAS SUPPORTED" if f >= 0.5 else "EXTRAPOLATED GAS NOT SUPPORTED")
    Mcont = norm * Mshape(rgc)
    RES["galaxies"][f"NGC{n}"] = dict(sha256=sha, D_Mpc=D, n_bins=int(ok.sum()), Rmax_kpc=Rmax, r_meas_kpc=rmeas, r_GC_outer_kpc=rgc, r_t_kpc=rt,
                                      rc_kpc=rc, beta=beta, T_range=[float(np.nanmin(Tk[ok])), float(np.nanmax(Tk[ok]))],
                                      M_atlas=Ma, M_trunc=Mt, M_extrap=Me, f=f, M_atlas_continued_to_rGC=Mcont, M_extrap_rGC=m_extrap(n, rgc), verdict=v)
    P(f"\n== NGC {n} ({tag}, D {D:.2f} Mpc): {int(ok.sum())} bins with R >= 2 kpc; atlas R_max {Rmax:.1f} kpc; record r_meas {rmeas:.1f} kpc; outer GC bin {rgc:.1f} kpc")
    P(f"   beta-model: r_c {rc:.2f} kpc, beta {beta:.3f}; T {np.nanmin(Tk[ok]):.2f}-{np.nanmax(Tk[ok]):.2f} keV")
    P(f"   at r_t {rt:.1f} kpc: M_atlas {Ma:.3e}, M_trunc {Mt:.3e}, M_extrap {Me:.3e} -> f {f:.2f} -> {v}")
    P(f"   (reported) beta-model continued to r_GC {rgc:.1f}: {Mcont:.3e} vs extrap {m_extrap(n, rgc):.3e}")
checks["K1"] = bool(k1); checks["K2"] = bool(k2)
vs = [g["verdict"] for g in RES["galaxies"].values() if g["verdict"] != "NOT INFORMATIVE"]
RES["verdict"] = "NOT INFORMATIVE" if not vs else ("EXTRAPOLATED GAS SUPPORTED" if all(x == "EXTRAPOLATED GAS SUPPORTED" for x in vs) else "EXTRAPOLATED GAS NOT SUPPORTED")
RES["checks"] = checks
P(f"\n  K0 trunc = extrap inside r_meas: {'PASS' if checks['K0'] else 'FAIL'}; K1 deprojection round trip: {'PASS' if k1 else 'FAIL'}; K2 fitted beta used: {'PASS' if k2 else 'FAIL'}")
P(f"=== VERDICT (overall): {RES['verdict']}")
fn = os.path.join(HERE, f"xg1_atlas_gas_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"xg1_atlas_gas{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
