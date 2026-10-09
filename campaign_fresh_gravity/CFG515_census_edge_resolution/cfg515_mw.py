#!/usr/bin/env python3
"""CFG515 (d) Milky Way timing + satellites with each object's census edge (FROZEN_CRITERIA.md 2bbe75602, section 3d).
CFG513's script is executed read-only up to its bias-table helpers (constants, baryon shapes, the Prof class: nu_mono phantom = settled
cold energy, numeric edge M_ph(<r_edge) = 5.364 M_b / f_ret).  The LG timing integrator and the Fritz+18 satellite parsing / turning
points are copied from CFG513 (not edited).  MW: M_b = 6.0e10 (L172 shapes; 7.3e10 reported), M31: 1.2e11 point mass; each with
its OWN f_ret (cfg515_lib: census = CFG416 fret_of self-consistent; bracket 0.07 / 0.18).  O-MW ownership, with Lambda.
PASS iff |z| <= 3 vs -109.3 +- 4.4 km/s (measurement error only) AND CFG433 D = (231.9 - V_c(78 kpc))/21.4 <= 3, both footings.
MUTATE (CFG515_MUTATE=1): f_ret = 1 and 0.01.
Run: nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_mw.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib, re
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, LANES)
import cfg515_lib as L                                                       # noqa: E402
try:
    os.nice(15)
except OSError:
    pass
MUTATE = os.environ.get("CFG515_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
MODES = L.modes()
LOG, CHK = [], {}
RES = {"lane": "CFG515", "script": "cfg515_mw", "mutate": MUTATE, "modes": list(MODES)}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
p513 = os.path.join(LANES, "CFG513_milky_way_cold_energy_profile", "cfg513_mw_profile.py")
src = open(p513).read()
mk = "def verdict(x):"
assert src.count(mk) == 1
_e = os.environ.pop("CFG513_MUTATE", None)
NS = {"__file__": p513, "__name__": "cfg513_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(mk)], "cfg513_ro", "exec"), NS)
if _e is not None:
    os.environ["CFG513_MUTATE"] = _e
Prof, G, FOOTS, GYR, H0, OM_L = NS["Prof"], NS["G"], NS["FOOTS"], NS["GYR"], NS["H0"], NS["OM_L"]
MB_PRIM, MB_HI, MB_M31, D_LG, VR_LG, EVR_LG, T0_GYR = (NS[k] for k in ("MB_PRIM", "MB_HI", "MB_M31", "D_LG", "VR_LG", "EVR_LG", "T0_GYR"))
REPO = NS["C"].REPO
T0U = T0_GYR * GYR
check("K0 CFG513 constants as recorded (M_b 6.0e10 / 7.3e10, M31 1.2e11, LG 780 kpc, -109.3 +- 4.4, t0 13.80)",
      (MB_PRIM, MB_HI, MB_M31, D_LG, VR_LG, EVR_LG, T0_GYR) == (6.0e10, 7.3e10, 1.2e11, 780.0, -109.3, 4.4, 13.80), "read from CFG513")


# ------------------------------------------------------------------ copied from CFG513 (LG timing)
def coll_time(acc, d0, v0, lam=True, tmax=60.0):
    def rhs(t, y):
        d = max(y[0], 1e-3)
        a = -acc(d) + (OM_L * H0 ** 2 * d if lam else 0.0)
        return [-y[1], -a]
    ev = lambda t, y: y[0] - 0.05
    ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, (0, tmax * GYR), [d0, v0], events=ev, rtol=1e-10, atol=1e-10, max_step=0.05 * GYR)
    if s.t_events[0].size:
        te = s.t_events[0][0]; ye = s.y_events[0][0]
        return te + ye[0] / max(abs(ye[1]), 1e-9) * 0.5
    return tmax * GYR


def v_pred(acc, lam=True):
    f = lambda v: coll_time(acc, D_LG, v, lam) - T0U
    lo, hi = -900.0, 600.0
    if f(lo) < 0:
        return np.nan
    return brentq(f, lo, hi, xtol=1e-6)


# ------------------------------------------------------------------ copied from CFG513 (Fritz+18 Tables 2/3, turning points)
TEX = os.path.join(REPO, "..", "_external_data", "cfg433_work", "src", "UFDsmot_arx_final.tex")
txt = open(TEX).read()


def table_rows(label, end=r"\end{array}"):
    i0_ = txt.index(label); i1_ = txt.index(end, i0_)
    out = []
    for line in txt[i0_:i1_].splitlines():
        line = line.strip()
        if "&" not in line or line.startswith("&") or line.startswith("satellite"):
            continue
        c = [x.strip() for x in line.rstrip().rstrip("\\").split("&")]
        if len(c) >= 7:
            out.append(c)
    return out


def pm3(s):
    return [float(v) for v in s.replace(" ", "").split(r"\pm")]


def asym(s):
    s = s.replace(" ", "").rstrip("\\").strip()
    if s.startswith(">"):
        return float(s[1:]), np.nan, np.nan
    m = re.match(r"([-\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}", s)
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


SAT = {}
for c in table_rows(r"\label{KapSou2}"):
    vr = pm3(c[7]); vt = asym(c[8])
    SAT[c[0]] = dict(d=float(c[1]), vrad=vr[0], vtan=vt[0])
for c in table_rows(r"\label{KapSou3}"):
    if c[0] in SAT:
        SAT[c[0]].update(p08=asym(c[4]))
NAMES = [n for n in SAT if "p08" in SAT[n]]


def apo(prof, r0, vr, vt):
    L_ = r0 * vt; E = 0.5 * (vr ** 2 + vt ** 2) + prof.phi(r0)
    f = lambda r: 2 * (E - prof.phi(r)) - L_ ** 2 / r ** 2
    hi = 1e6 * 0.999
    if f(hi) > 0:
        return np.inf
    return brentq(f, r0 * (1 + 1e-9), hi) if f(r0 * (1 + 1e-9)) > 0 else r0


# ------------------------------------------------------------------ score
def cell(foot, f_mw, f_m31, Mb=MB_PRIM):
    mw = Prof("mw", Mb=Mb, foot=foot, fret=f_mw)
    m31 = Prof("m31", Mb=MB_M31, foot=foot, fret=f_m31, point=True)
    vp = v_pred(lambda d: G * float(mw.M_enc(np.array([d]))[0] + m31.M_enc(np.array([d]))[0]) / d ** 2)
    z = (abs(vp) - abs(VR_LG)) / EVR_LG if np.isfinite(vp) else np.inf
    v78 = float(mw.vc_sph(np.array([78.0]))[0])
    D = (231.9 - v78) / 21.4
    nub = sum(not np.isfinite(apo(mw, SAT[n]["d"], SAT[n]["vrad"], SAT[n]["vtan"])) for n in NAMES)
    return dict(f_mw=f_mw, f_m31=f_m31, edge_mw_kpc=mw.redge, edge_m31_kpc=m31.redge, M_mw_total=mw.Mb_tot() + mw.Mcold,
                M_m31_total=MB_M31 + m31.Mcold, v_pred=vp, z=z, Vc78=v78, D=D, unbound=nub, n_sat=len(NAMES),
                passed=bool(abs(z) <= 3.0 and D <= 3.0))


J513 = json.load(open(os.path.join(LANES, "CFG513_milky_way_cold_energy_profile", "cfg513_results.json")))["numbers"]
k7 = []
for foot in FOOTS:
    c_ = cell(foot, 0.18, 0.18)
    k7.append((foot, c_["v_pred"] - J513["lg_timing"][f"{foot}|0.18"]["v_OMW"],
               c_["D"] - J513["post_run"][f"cfg433_D|{foot}|Mb 6.0e+10|f_ret 0.18"], c_["unbound"]))
check("K7 CFG513 reproduction at f_ret = 0.18 (both objects): timing v_r within 0.5 km/s, D within 0.02, unbound = 4",
      all(abs(a) <= 0.5 and abs(b) <= 0.02 and u == 4 for _, a, b, u in k7), "; ".join(f"{f}: dv {a:+.3f}, dD {b:+.4f}, unbound {u}" for f, a, b, u in k7))

OUTR = {}
for mode in MODES:
    OUTR[mode] = {}
    f_mw, f_m31 = L.fret(mode, MB_PRIM), L.fret(mode, MB_M31)
    f_hi = L.fret(mode, MB_HI)
    for foot in FOOTS:
        c_ = cell(foot, f_mw, f_m31)
        v_ = cell(foot, f_hi, f_m31, Mb=MB_HI)
        OUTR[mode][foot] = dict(primary=c_, variant_Mb_7p3e10=v_)
        P(f"  [{mode:6s}|{foot:9s}] f_ret MW {f_mw:.3f} / M31 {f_m31:.3f}; edges {c_['edge_mw_kpc']:.0f} / {c_['edge_m31_kpc']:.0f} kpc; "
          f"totals {c_['M_mw_total']:.2e} / {c_['M_m31_total']:.2e}; LG v {c_['v_pred']:.1f} (z {c_['z']:+.1f}); "
          f"V_c(78) {c_['Vc78']:.1f} (D {c_['D']:+.2f}); unbound {c_['unbound']}/{c_['n_sat']} -> {'PASS' if c_['passed'] else 'FAIL'}")
        P(f"      7.3e10 variant (reported): f_ret {f_hi:.3f}; v {v_['v_pred']:.1f} (z {v_['z']:+.1f}); D {v_['D']:+.2f}; unbound {v_['unbound']}")
    OUTR[mode]["d_pass"] = all(OUTR[mode][f]["primary"]["passed"] for f in FOOTS)
    P(f"  => {mode}: (d) {'PASS' if OUTR[mode]['d_pass'] else 'FAIL'}")

if not MUTATE:
    # post hoc (no verdict weight): the common f_ret the timing needs (CFG513: 0.206), and the M31 f_ret the timing needs with the MW at census
    POST = {}
    for foot in FOOTS:
        def vf(lf, foot=foot):
            return cell(foot, 10 ** lf, 10 ** lf)["v_pred"] - VR_LG
        try:
            POST[f"common_fret_needed|{foot}"] = 10 ** brentq(vf, math.log10(0.1), math.log10(0.9), xtol=1e-4)
        except ValueError:
            POST[f"common_fret_needed|{foot}"] = None
        fm = L.fret("census", MB_PRIM)

        def vm(lf, foot=foot, fm=fm):
            return cell(foot, fm, 10 ** lf)["v_pred"] - VR_LG
        try:
            POST[f"m31_fret_needed_with_mw_census|{foot}"] = 10 ** brentq(vm, math.log10(0.05), math.log10(1.0), xtol=1e-4)
        except ValueError:
            POST[f"m31_fret_needed_with_mw_census|{foot}"] = None
    P("  POST HOC (no verdict weight, not a fit): " + "; ".join(f"{k} {v if v is None else round(v, 3)}" for k, v in POST.items()))
    RES["post_hoc"] = POST
RES["rows"] = OUTR
if MUTATE:
    m1 = max(abs(OUTR["one"][f]["primary"]["z"] - (-22.8)) for f in FOOTS)
    check("M1 (MW) f_ret = 1 reproduces CFG513's timing z -22.8 within 0.3", m1 <= 0.3,
          "; ".join(f"{f} z {OUTR['one'][f]['primary']['z']:+.2f}, D {OUTR['one'][f]['primary']['D']:+.2f}, unbound {OUTR['one'][f]['primary']['unbound']}" for f in FOOTS))
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; load-bearing failures {nlb}; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg515_mw_results{SUF}.json"), "w"), indent=1, default=lambda o: None if o != o else float(o))
open(os.path.join(HERE, f"cfg515_mw{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
