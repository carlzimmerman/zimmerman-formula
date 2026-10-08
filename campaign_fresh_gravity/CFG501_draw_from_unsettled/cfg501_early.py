#!/usr/bin/env python3
"""CFG501 (d) early-type lensing levels (FROZEN_CRITERIA.md 7b71dd9b5, REPORTED leg): a copy of CFG498's cfg498_early.py with the
PRIMARY cap on the UNSETTLED supply C_u = (1 - f_b) Int_0^{r_ta} (1 - m) dM_law (rows *_ucap); CFG498's full-supply cap kept as *_cap498.
--- CFG498 docstring follows ---
CFG498 (d) early-type lensing levels (FROZEN_CRITERIA.md d9c739010, REPORTED leg; CFG485 caveat 2).
CFG485's R8 construction (CFG95's machinery read-only via CFG485's own prefix, executed read-only up to its C6 banner):
released per-class blocks on K1, two-halo profiled per class (6 dof), and without two-halo.  The phantom is the capped clock
taper to r_ta (V1: rho_X = law mass, MS1 EXCEPTION; V2: rho_X = M_b/f_b, strict MS1) in place of the 5.850 r_M truncation.
Label 'early-type levels OK' iff chi2_early - chi2_B1,early <= 4 on both footings (free 2h).  B1 = CFG95's law to 0.40 r_ta.
Control C4: B1 chi2 reproduces CFG485's committed R8 within 1e-6.
MUTATE (CFG498_MUTATE=1): FRW-firing clock (m = background value on every shell, to r_ta, capped): reported only.
Run: nice -n 10 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_early.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, time, contextlib
import numpy as np
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
sys.path.insert(0, os.path.join(LANES, "CFG487_settled_fraction_switch"))
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
import cfg487_lib as LB                                                      # noqa: E402
import cfg100_lib as C100                                                    # noqa: E402
MUTATE = os.environ.get("CFG501_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(10)
except OSError:
    pass
OUT, CHK = [], {}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
# ---------------------------------------------------------------- CFG485 prefix, read-only (its Step 0 + C1-C5 + stacks)
p485 = os.path.join(LANES, "CFG485_kids_split_settling_completeness", "cfg485_settling_split.py")
src = open(p485).read()
src = src[:src.index("# ================================================================== C6")]
_e = os.environ.get("CFG485_MUTATE"); os.environ["CFG485_MUTATE"] = "0"
g = {"__file__": p485, "__name__": "cfg485_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "cfg485_ro", "exec"), g)
os.environ.pop("CFG485_MUTATE") if _e is None else os.environ.__setitem__("CFG485_MUTATE", _e)
C = g["C"]; FOOTS = g["FOOTS"]; FB = g["FB"]
LMG, ZG, RG, LRG, idx, C30 = g["LMG"], g["ZG"], g["RG"], g["LRG"], g["idx"], g["C30"]
fcold, project, rgrid = g["fcold"], g["project"], g["rgrid"]
contrib, parts, chi2_free, chi2_none, DF, CB95 = g["contrib"], g["parts"], g["chi2_free"], g["chi2_none"], g["DF"], g["CB95"]
d_early, d_late = g["d_early"], g["d_late"]
P(f"\n  CFG485 prefix executed read-only ({time.time() - T0:.0f} s); f_b {FB:.6f}; nodes {len(LMG)} masses x {len(ZG)} z")

SC = LB.ShellClock(Om=C100.OM)
RHO_M0 = C100.OM * C100.RHOC0                                                 # Msun / Mpc^3


def m_of(rho_ratio, a_obs):
    if MUTATE:
        Ebg = quad(lambda x: math.sqrt(1.5 * C100.OM / x ** 3) / (x * math.sqrt(C100.OM / x ** 3 + 1 - C100.OM)), 1e-3, a_obs)[0]
        return np.full(np.shape(rho_ratio), -math.expm1(-Ebg))
    return SC.m_of_rho(rho_ratio, a_obs)[0]


def taper_tables(foot, ver, cap):
    out, qs = {}, []
    a0 = C.A0[foot]
    for b, z in enumerate(ZG):
        tab = np.zeros((len(LMG), len(RG)))
        ao = 1.0 / (1.0 + z)
        for a, lm in enumerate(LMG):
            Mb = 10 ** lm * (1 + fcold(lm))
            rta = C100.r_ta_law(Mb, a0, z)
            r = rgrid[rgrid <= rta]
            ML = np.asarray(C.M_law(Mb, r, a0, C.nu_mono), float)
            rho = ML / (4 * math.pi / 3 * r ** 3) / RHO_M0 if ver == "V1" else (Mb / FB) / (4 * math.pi / 3 * r ** 3) / RHO_M0
            mm = m_of(rho, ao)
            dM = np.diff(np.concatenate([[0.0], ML - Mb]))
            mmid = np.concatenate([[mm[0]], 0.5 * (mm[1:] + mm[:-1])])
            Md = np.cumsum(mmid * dM)
            Mta = 4 * math.pi / 3 * rta ** 3 * RHO_M0 * (1 + z) ** 3 * C100.dta(z)
            q = float(Md[-1] / ((1 - FB) * Mta))
            if cap == "unsettled":                                              # CFG501: the unsettled supply
                q = float(Md[-1] / ((1 - FB) * np.sum((1.0 - mmid) * np.diff(np.concatenate([[0.0], ML])))))
            qs.append(q)
            if cap and q > 1:
                Md = Md / q
            Mfull = np.concatenate([Md, np.full(len(rgrid) - len(r), Md[-1])])  # mass frozen beyond r_ta
            tab[a] = project(rgrid, Mfull, RG)
        out[(foot, b)] = tab
    return out, np.array(qs)


R8 = json.load(open(os.path.join(LANES, "CFG485_kids_split_settling_completeness", "cfg485_settling_split_results.json")))["numbers"]["R8"]
RES = {"lane": "CFG501", "script": "cfg501_early", "mutate": MUTATE, "rows": {}, "q_raw": {}}
c4 = 0.0
for foot in FOOTS:
    RES["rows"][foot] = {}
    for cls, nm, dd, blk in ((1, "early", d_early, slice(15, 30)), (0, "late", d_late, slice(0, 15))):
        Cb = C30[blk, blk][np.ix_(idx, idx)]; Ci = np.linalg.inv(Cb)
        Ph1, Bar1, T1, _ = parts(CB95[(foot, cls)]); m1 = (Ph1 + Bar1)[idx]
        x1, A1 = chi2_free(dd[idx] - m1, Ci, T1[idx]); n1 = chi2_none(dd[idx] - m1, Ci)
        c4 = max(c4, abs(x1 - R8[foot][nm]["chi2_B1"]), abs(n1 - R8[foot][nm]["nofree_B1"]))
        RES["rows"][foot][nm] = dict(B1=dict(chi2=x1, A=A1, no2h=n1), S485=dict(chi2=R8[foot][nm]["chi2_S"], no2h=R8[foot][nm]["nofree_S"]),
                                     data=dd[idx].tolist(), model_B1=m1.tolist())
check("C4 CFG485's machinery (read-only) reproduces its committed R8 B1 chi2 (free 2h and no 2h; early, late; both footings) within 1e-6",
      c4 <= 1e-6, f"max |diff| {c4:.1e}")
for ver in ("V1", "V2"):
    for cap in ("unsettled", "full", False):
        key = f"{ver}_{ {'unsettled': 'ucap', 'full': 'cap498', False: 'nocap'}[cap] }"
        for foot in FOOTS:
            t = time.time()
            TT, qs = taper_tables(foot, ver, cap)
            RES["q_raw"][f"{key}|{foot}"] = dict(median=float(np.median(qs)), max=float(qs.max()), frac_binds=float(np.mean(qs > 1)))
            for cls, nm, dd, blk in ((1, "early", d_early, slice(15, 30)), (0, "late", d_late, slice(0, 15))):
                cb = contrib(cls, foot, TT, DF[foot][cls])
                Ph, Bar, T, _ = parts(cb); mS = (Ph + Bar)[idx]
                Cb = C30[blk, blk][np.ix_(idx, idx)]; Ci = np.linalg.inv(Cb)
                xs, As = chi2_free(dd[idx] - mS, Ci, T[idx]); ns = chi2_none(dd[idx] - mS, Ci)
                RES["rows"][foot][nm][key] = dict(chi2=xs, A=As, no2h=ns, d_vs_B1=xs - RES["rows"][foot][nm]["B1"]["chi2"], model=mS.tolist())
            P(f"  {key} {foot}: tables + stacks {time.time() - t:.0f} s; node q_raw median {np.median(qs):.3f}, max {qs.max():.3f}, binds {np.mean(qs > 1):.3f}")
P("\n  per-class absolute levels on K1 (released blocks; 6 dof with free 2h, 7 without)")
P("  footing   class | B1 (CFG95 law) chi2 / A / no-2h | CFG485 S (5.85 r_M) chi2 / no-2h | V1_ucap chi2 / A / no-2h (d vs B1) | V2_ucap chi2 / A / no-2h (d vs B1) | V1_cap498 / V2_cap498 / V1_nocap / V2_nocap chi2")
for foot in FOOTS:
    for nm in ("early", "late"):
        r = RES["rows"][foot][nm]
        P(f"  {foot:9s} {nm:5s} | {r['B1']['chi2']:7.2f} / {r['B1']['A']:+.2f} / {r['B1']['no2h']:7.2f} | {r['S485']['chi2']:7.2f} / {r['S485']['no2h']:7.2f} | "
          f"{r['V1_ucap']['chi2']:7.2f} / {r['V1_ucap']['A']:+.2f} / {r['V1_ucap']['no2h']:7.2f} ({r['V1_ucap']['d_vs_B1']:+.2f}) | "
          f"{r['V2_ucap']['chi2']:7.2f} / {r['V2_ucap']['A']:+.2f} / {r['V2_ucap']['no2h']:7.2f} ({r['V2_ucap']['d_vs_B1']:+.2f}) | "
          f"{r['V1_cap498']['chi2']:.2f} / {r['V2_cap498']['chi2']:.2f} / {r['V1_nocap']['chi2']:.2f} / {r['V2_nocap']['chi2']:.2f}")
        P(f"      data   {np.round(r['data'], 2).tolist()}\n      B1     {np.round(r['model_B1'], 2).tolist()}\n      V1_ucap {np.round(r['V1_ucap']['model'], 2).tolist()}\n      V2_ucap {np.round(r['V2_ucap']['model'], 2).tolist()}")
if not MUTATE:
    J498 = json.load(open(os.path.join(LANES, "CFG498_clock_taper_capped", "cfg498_early_results.json")))["rows"]
    c2e = max(abs(RES["rows"][f][nm][f"{v}_cap498"]["chi2"] - J498[f][nm][f"{v}_cap"]["chi2"]) for f in FOOTS for nm in ("early", "late") for v in ("V1", "V2"))
    check("C2e the full-supply-cap rows reproduce CFG498's early/late V1_cap / V2_cap chi2 within 1e-6", c2e <= 1e-6, f"max |diff| {c2e:.1e}")
for ver in ("V1", "V2"):
    ok = all(RES["rows"][f]["early"][f"{ver}_ucap"]["d_vs_B1"] <= 4.0 for f in FOOTS)
    RES[f"early_levels_ok_{ver}"] = ok
    check(f"(d) early-type levels OK ({ver} unsettled-cap taper): chi2_early - chi2_B1,early <= 4 on both footings (free 2h)", ok,
          ", ".join(f"{f} {RES['rows'][f]['early'][f'{ver}_ucap']['chi2']:.2f} - {RES['rows'][f]['early']['B1']['chi2']:.2f} = {RES['rows'][f]['early'][f'{ver}_ucap']['d_vs_B1']:+.2f}"
                    for f in FOOTS), lb=False)
RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, f"cfg501_early_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg501_early{SUF}.out"), "w").write("\n".join(OUT) + "\n")
nlb = sum(1 for c in CHK.values() if c["load_bearing"] and not c["ok"])
P(f"\n  load-bearing failures {nlb}; elapsed {RES['elapsed_s']} s")
sys.exit(1 if nlb else 0)
