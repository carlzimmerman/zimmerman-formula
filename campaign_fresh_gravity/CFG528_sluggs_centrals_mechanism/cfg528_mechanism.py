#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG528 -- the four SLUGGS centrals (M87, NGC 4365, NGC 4374, NGC 5846): data/assumption re-check, missing hot gas, derived
mechanisms, and a (non-derived) X-COP unsettled-cold-energy template.  Frozen criteria: FROZEN_CRITERIA.md (5ad8324fa).

Machinery: CFG331's source exec'd read-only up to its "run" block (as CFG466).  gamma = 3 primary; nu_mono; kappa = 1/2 FITTED;
footings 9.36e-11 | 1.13e-10, never pooled.  Per-galaxy errors: CFG466's GC bootstrap at gamma = 3.
CFG528_MUTATE=1: MA (Chabrier, no gas, no members), MB (M* x 8), MC (template x 0); separate outputs.
"""
import os, sys, math, json, contextlib, io
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG528_MUTATE", "0") == "1"
POSTFREEZE = os.environ.get("CFG528_POSTFREEZE", "0") == "1"   # post-freeze diagnostic (README disclosure 2026-10-09), not a decision row
TAG = "_MUTATE" if MUTATE else ("_POSTFREEZE" if POSTFREEZE else "")
OUT = []
def P(s=""):
    print(s); OUT.append(s)

# ------------------------------------------------------------------ 0. CFG331 machinery, read-only
os.environ.pop("CFG331_MUTATE", None)
_src = open(os.path.join(LANES, "CFG331_sluggs_centrals_environment", "cfg331_environment.py")).read()
_cut = _src.index("\n# ------------------------------------------------------------------ run")
NS = {"__file__": os.path.join(LANES, "CFG331_sluggs_centrals_environment", "cfg331_environment.py"), "__name__": "cfg331_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "cfg331_environment", "exec"), NS)
B, GAL, GAS, MEM, GE, A3 = NS["B"], NS["GAL"], NS["GAS"], NS["MEM"], NS["GE"], NS["A3"]
RG, LR, G, KPC, MSUN = NS["RG"], NS["LR"], NS["G"], NS["KPC"], NS["MSUN"]
nu, sig_los, calib, jam_mass, ffl, ARCSEC = NS["nu"], NS["sig_los"], NS["calib"], NS["jam_mass"], NS["f"], NS["ARCSEC"]
CEN = (4486, 4365, 4374, 5846)
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
HOSTC = (4486, 5846)                                            # host centres (PAPER35 sec. 2 / CFG331)

sys.path.insert(0, os.path.join(LANES, "CFG515_census_edge_resolution"))
import cfg515_lib as L515                                       # fret_census, read-only import (K4)

K0J = json.load(open(os.path.join(LANES, "CFG330_sluggs_icgc_clip", "cfg330_summary_K0.json")))["CFG330"]
C331 = json.load(open(os.path.join(LANES, "CFG331_sluggs_centrals_environment", "cfg331_environment_results.json")))["summary"]
C466 = json.load(open(os.path.join(LANES, "CFG466_sluggs_free_tracer_slope", "cfg466_free_slope_results.json")))
C432 = json.load(open(os.path.join(LANES, "CFG432_unsettled_cold_profile_xcop", "cfg432_results.json")))
SIG = {(n, ft): C466["reported"][f"NGC{n}|K0|{ft}"]["sig_g3.0"] for n in CEN for ft in A0}

# saved originals (distance rows rebuild and restore)
ORIG = {n: dict(D=GAL[n]["D"], B=dict(B[n]), GAS=GAS[n], MEM=MEM[n]) for n in CEN}
DA = {n: ffl(A3[f"NGC{n:04d}"]["Dist_Mpc"]) for n in CEN}


def set_distance(n, D):
    GAL[n]["D"] = D
    b = NS["bins_for"](n); a = A3[f"NGC{n:04d}"]
    b["Mjam"] = 10 ** (ffl(a["logML_JAM"]) + ffl(a["logL"])) * D / DA[n]
    b["r12"] = 10 ** ffl(a["logr12"]) * ARCSEC * D * 1e3
    b["ah"] = b["Re"] / 1.8153
    B[n] = b
    GAS[n] = NS["gas_on_RG"](n)
    MEM[n] = NS["members"](n)


def restore(n):
    GAL[n]["D"] = ORIG[n]["D"]; B[n] = dict(ORIG[n]["B"]); GAS[n] = ORIG[n]["GAS"]; MEM[n] = ORIG[n]["MEM"]


def Mpop(n, row):
    a = A3[f"NGC{n:04d}"]; base = ffl(a["logML_Salp"]) + ffl(a["logL"])
    d = {"salp": 0.0, "chab": -0.25, "chab2x": -0.25 + math.log10(2.0)}[row]
    return 10 ** (base + d) * GAL[n]["D"] / DA[n]


def gas_profile(n, mode, x=1.0):
    if mode is None or x == 0:
        return None
    Mg, info = GAS[n]
    Mg = Mg * x
    if mode == "trunc":
        rm = info["r_meas"]
        Mg = np.where(RG > rm, float(np.interp(math.log(rm), LR, Mg)), Mg)
    return Mg


def template_Mu(n, a0, foot, rfac=1.0, flat_inner=False):
    """X-COP unsettled template (3d): M_u(<r) = Q(r/R500) M_gas,host(<r); Newtonian."""
    cell = C432[f"{foot}|b0.0"]
    Q01 = float(np.median([r["Q_01"] for r in cell["rows"]])); s = float(cell["gas"]["median"])
    R500 = {4486: 700.0, 5846: 380.0}[n] * rfac
    x = RG / R500
    Q = Q01 * (x / 0.1) ** s
    if flat_inner:
        Q = np.where(x < 0.1, Q01, Q)
    return Q * GAS[n][0], dict(Q01=Q01, s_gas=s, R500=R500)


def build(n, a0, mstar="jam", gas=None, gx=1.0, own=False, extraM=None, mmult=1.0, cap=None):
    """returns (g, gN, Mstar, eps_in).  mstar: 'jam' (law-calibrated to JAM inside r12, incl. gas + extraM) or a pop row."""
    b = B[n]; Mg = gas_profile(n, gas, gx)
    Mx = np.zeros_like(RG) if Mg is None else Mg.copy()
    Mu = np.zeros_like(RG) if extraM is None else extraM
    r12 = b["r12"]; Mg12 = float(np.interp(math.log(r12), LR, Mx)); Mu12 = float(np.interp(math.log(r12), LR, Mu))
    lawM = lambda M: (0.5 * M + Mg12) * float(nu(G * (0.5 * M + Mg12) * MSUN / (r12 * KPC) ** 2 / NS_A0[0])) + Mu12
    NS_A0[0] = a0
    if mstar == "jam":
        if Mg is None and extraM is None:
            M = jam_mass(b["Mjam"], r12, a0, "nu_mono")
        else:
            fn = lambda lm: math.log10(lawM(10 ** lm)) - math.log10(0.5 * b["Mjam"])
            lo = math.log10(b["Mjam"]) - 4
            if fn(lo) > 0:
                return None
            M = 10 ** brentq(fn, lo, math.log10(b["Mjam"]) + 1, xtol=1e-12)
        M *= mmult
    else:
        M = Mpop(n, mstar) * mmult
    eps = math.log10(lawM(M) / (0.5 * b["Mjam"]))
    if own and n in HOSTC and Mg is not None:
        for rp, dk in zip(MEM[n]["Rp"], MEM[n]["dK"]):
            Mx = Mx + gx * M * 10 ** (-0.4 * dk) * (RG >= rp)
    gN = G * (M * RG ** 2 / (RG + b["ah"]) ** 2 + Mx) * MSUN / (RG * KPC) ** 2
    g = nu(gN / a0) * gN
    if cap is not None:                                          # supply cap: phantom mass limited to the supply
        Mph = (g - gN) * (RG * KPC) ** 2 / G / MSUN
        g = gN + np.minimum(Mph, cap) * G * MSUN / (RG * KPC) ** 2
    g = g + G * Mu * MSUN / (RG * KPC) ** 2
    return g, gN, M, eps


NS_A0 = [9.36e-11]


def offset(n, g, beta=0.0, mask="outer"):
    b = B[n]; s = sig_los(b["Rb"], g, 3.0, beta)
    if mask == "outer":
        k = b["outer"]
    elif mask == "all":
        k = np.ones(len(b["Rb"]), bool)
    elif mask == "last":
        k = np.zeros(len(b["Rb"]), bool); k[-1] = True
    elif mask == "first_outer":
        k = np.zeros(len(b["Rb"]), bool); k[np.argmax(b["outer"])] = True
    return float(np.mean(np.log10(b["Sb"][k] / s[k])))


def score(per, foot):
    """per: {n: offset or None}"""
    Z = {n: (per[n] / SIG[(n, foot)] if per[n] is not None and np.isfinite(per[n]) else float("nan")) for n in CEN}
    cl = sum(1 for n in CEN if np.isfinite(Z[n]) and Z[n] < 2); rv = sum(1 for n in CEN if np.isfinite(Z[n]) and Z[n] < -2)
    ok = [n for n in CEN if per[n] is not None and np.isfinite(per[n])]
    mean = float(np.mean([per[n] for n in ok])) if ok else float("nan")
    err = math.sqrt(sum(SIG[(n, foot)] ** 2 for n in ok)) / len(ok) if ok else float("nan")
    return dict(per={f"NGC{n}": per[n] for n in CEN}, Z={f"NGC{n}": Z[n] for n in CEN}, n_cleared=cl, n_reversed=rv,
                closes=bool(cl >= 3 and rv == 0 and len(ok) == 4), mean=mean, err=err, Z_class=mean / err if ok else float("nan"))


ROWS = {}
def row(name, fn, item, admissible=True, derived=False, note=""):
    res = {}
    for foot, a0 in A0.items():
        per = {}
        for n in CEN:
            try:
                per[n] = fn(n, a0, foot)
            except Exception as e:                                # recorded, never silently dropped
                per[n] = None; P(f"    [{name}] NGC{n} {foot}: not computable ({e})")
        res[foot] = score(per, foot)
    closes = all(res[ft]["closes"] for ft in A0)
    ROWS[name] = dict(item=item, admissible=admissible, derived=derived, note=note, closes_both=closes, **res)
    for ft in A0:
        r = res[ft]
        P(f"  {name:34s} {ft:9s} " + " ".join(f"{(r['per'][f'NGC{n}'] if r['per'][f'NGC{n}'] is not None else float('nan')):+.3f}({r['Z'][f'NGC{n}']:+5.1f})" for n in CEN)
          + f" | mean {r['mean']:+.3f} Zc {r['Z_class']:+5.1f} | cleared {r['n_cleared']}/4" + (f" rev {r['n_reversed']}" if r['n_reversed'] else ""))
    P(f"  {'':34s} -> CLOSES both footings: {closes}" + ("" if admissible else "  [INADMISSIBLE]") + (f"  ({note})" if note else ""))
    return ROWS[name]


def eps_row(mstar):
    return {ft: {f"NGC{n}": build(n, a0, mstar)[3] for n in CEN} for ft, a0 in A0.items()}


def off_of(n, a0, **kw):
    beta = kw.pop("beta", 0.0); mask = kw.pop("mask", "outer")
    r = build(n, a0, **kw)
    return None if r is None else offset(n, r[0], beta, mask)


def dist_off(n, a0, D, **kw):
    set_distance(n, D)
    try:
        return off_of(n, a0, **kw)
    finally:
        restore(n)


P("=" * 120)
P("CFG528 -- SLUGGS centrals: data re-check, missing hot gas, derived mechanisms" + ("   *** MUTATE ***" if MUTATE else ""))
P("=" * 120)
P("columns: offset dex (Z = offset / sigma_i, CFG466 bootstrap at gamma 3) for NGC 4486 | 4365 | 4374 | 5846")
P("sigma_i: " + "; ".join(f"{ft}: " + ", ".join(f"{n} {SIG[(n, ft)]:.4f}" for n in CEN) for ft in A0))

ok = []
def check(lbl, cond, det):
    ok.append(bool(cond)); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")

if POSTFREEZE:
    P("\nPOST-FREEZE DIAGNOSTIC (not a decision row): can the CLOSES criterion fire?  MB (M* x8) over-shot to REVERSED;")
    P("planted M* x5 (log 0.70, inside the post-hoc null range +0.59..+0.78) on the JAM ceiling, K0")
    pf = row("PF planted M* x5 (K0)", lambda n, a0, ft: off_of(n, a0, mmult=5.0), "PF")
    check("PF planted x5 CLOSES on both footings", pf["closes_both"], f"cleared {pf['canonical']['n_cleared']}/{pf['alt']['n_cleared']}")
    res = dict(lane="CFG528", postfreeze=True, rows=ROWS, checks_pass=sum(ok), checks_total=len(ok))
elif not MUTATE:
    # ---------------------------------------------------------------- item 1
    P("\nITEM 1 -- data / assumption re-check")
    P(" 1a stellar M/L and IMF (inner excess eps_in = log law-pred M(<r12) / (M_JAM/2); admissible <= +0.06 dex)")
    EPS = {r: eps_row(r) for r in ("jam", "salp", "chab", "chab2x")}
    for r, e in EPS.items():
        P(f"    eps_in {r:6s}: " + "; ".join(f"{ft}: " + ", ".join(f"{k[3:]} {v:+.3f}" for k, v in e[ft].items()) for ft in A0))
    row("1a(i) JAM-law ceiling (K0, record)", lambda n, a0, ft: off_of(n, a0), "1a")
    for r, lbl in (("salp", "1a(ii) Salpeter population"), ("chab", "1a(iii) Chabrier = Salp-0.25"), ("chab2x", "1a(iv) 2x Chabrier (bottom-heavy)")):
        adm = all(v <= 0.06 for ft in A0 for v in EPS[r][ft].values())
        row(lbl, lambda n, a0, ft, r=r: off_of(n, a0, mstar=r), "1a", admissible=adm,
            note="eps_in max %+.3f" % max(v for ft in A0 for v in EPS[r][ft].values()))
    NULLM = {}
    for ft, a0 in A0.items():
        for n in CEN:
            fn = lambda lm: off_of(n, a0, mmult=10 ** lm)
            try:
                lm = brentq(fn, -0.5, 2.5, xtol=1e-5)
                NULLM[(n, ft)] = dict(log_mult=lm, eps_in=build(n, a0, mmult=10 ** lm)[3])
            except ValueError:
                NULLM[(n, ft)] = dict(log_mult=float("nan"), eps_in=float("nan"))
    P("    post hoc (reported): M* multiplier on the JAM ceiling that nulls each central (log), and its inner excess")
    for ft in A0:
        P(f"      {ft}: " + "; ".join(f"{n} x10^{NULLM[(n, ft)]['log_mult']:+.3f} (eps_in {NULLM[(n, ft)]['eps_in']:+.3f})" for n in CEN))

    P(" 1b distances (SBF record; ATLAS3D; SBF x0.9 / x1.1)")
    P("    D_SBF / D_ATLAS3D (Mpc): " + ", ".join(f"{n} {ORIG[n]['D']:.2f}/{DA[n]:.2f}" for n in CEN))
    row("1b ATLAS3D distance", lambda n, a0, ft: dist_off(n, a0, DA[n]), "1b")
    row("1b SBF x0.9", lambda n, a0, ft: dist_off(n, a0, 0.9 * ORIG[n]["D"]), "1b")
    row("1b SBF x1.1", lambda n, a0, ft: dist_off(n, a0, 1.1 * ORIG[n]["D"]), "1b")
    NULLD = {}
    for ft, a0 in A0.items():
        for n in CEN:
            try:
                fd = brentq(lambda lf: dist_off(n, a0, 10 ** lf * ORIG[n]["D"]), -0.7, 1.3, xtol=1e-4)
                NULLD[(n, ft)] = 10 ** fd
            except ValueError:
                NULLD[(n, ft)] = float("nan")
    P("    post hoc: distance factor that nulls each central: " + "; ".join(f"{ft}: " + ", ".join(f"{n} x{NULLD[(n, ft)]:.2f}" for n in CEN) for ft in A0))

    P(" 1c anisotropy (gamma 3)")
    row("1c beta -0.5", lambda n, a0, ft: off_of(n, a0, beta=-0.5), "1c")
    row("1c beta +0.5", lambda n, a0, ft: off_of(n, a0, beta=0.5), "1c")
    P("    CFG466 free-gamma classes (quoted): " + "; ".join(f"{k} {C466['classes'][k]['cls']}" for k in ("K0|canonical", "K0|alt", "own|canonical", "own|alt"))
      + "; beta+0.5: " + "; ".join(f"{k} {C466['reported_classes'][k]['cls']}" for k in ("beta+0.5|K0|canonical", "beta+0.5|own|canonical", "beta+0.5|own|alt")))

    P(" 1d radial range")
    row("1d all bins", lambda n, a0, ft: off_of(n, a0, mask="all"), "1d")
    row("1d outermost bin only", lambda n, a0, ft: off_of(n, a0, mask="last"), "1d", admissible=False, note="reported")
    row("1d innermost outer bin only", lambda n, a0, ft: off_of(n, a0, mask="first_outer"), "1d", admissible=False, note="reported")

    P(" 1e round rule: the field is the spherical algebraic law on sphere-enclosed baryons (= CFG516 RM = spherical QUMOND)")
    r1 = 0.0
    for ft, a0 in A0.items():
        for n in CEN:
            g, gN, M, _ = build(n, a0, gas="extrap")
            Mph = (g - gN) * (RG * KPC) ** 2 / G / MSUN
            rho = np.gradient(Mph, RG) / (4 * math.pi * RG ** 2)              # phantom density from its own mass profile
            dm = 4 * math.pi * RG ** 2 * rho
            Mre = np.concatenate([[Mph[0]], Mph[0] + np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RG))])
            k = (RG > B[n]["Rb"][0] * 0.5) & (RG < B[n]["Rb"][-1] * 1.5)
            r1 = max(r1, float(np.max(np.abs(Mre[k] / Mph[k] - 1))))
    check("R1 phantom mass rebuilt from its own density reproduces the field used, <= 1e-3 relative over the GC range", r1 <= 1e-3, f"max rel diff {r1:.2e}")

    P(" 1f EFE")
    efe = row("1f R-efe (CFG331)", lambda n, a0, ft: NS["run"](n, a0, 1.0, "efe"), "1f", admissible=False, note="EFE raises offsets")
    k0 = ROWS["1a(i) JAM-law ceiling (K0, record)"]
    e1 = all(efe[ft]["per"][f"NGC{n}"] >= k0[ft]["per"][f"NGC{n}"] - 1e-12 for ft in A0 for n in CEN)
    check("E1 EFE lowers no offset", e1, "R-efe >= K0 for every central, both footings")

    # ---------------------------------------------------------------- item 2
    P("\nITEM 2 -- missing baryons: hot gas")
    for n in CEN:
        i = GAS[n][1]
        P(f"    NGC{n}: {i['src']}; measured to {i['r_meas']:.0f} kpc; outermost GC bin {B[n]['Rb'][-1]:.0f} kpc; "
          f"M_gas(<R_out) extrap {np.interp(math.log(B[n]['Rb'][-1]), LR, GAS[n][0]):.2e} vs trunc {np.interp(math.log(B[n]['Rb'][-1]), LR, gas_profile(n, 'trunc')):.2e} Msun")
    row("2a R-bar gas truncated at measured edge", lambda n, a0, ft: off_of(n, a0, gas="trunc"), "2a", derived=True)
    row("2b R-bar gas extrapolated (CFG331)", lambda n, a0, ft: off_of(n, a0, gas="extrap"), "2b", derived=True)
    row("2c R-own (CFG331)", lambda n, a0, ft: off_of(n, a0, gas="extrap", own=True), "2c", derived=True)
    NULLG = {}
    for ft, a0 in A0.items():
        for n in CEN:
            def fg(lx):
                o = off_of(n, a0, gas="extrap", gx=10 ** lx)
                return -1.0 if o is None else o
            try:
                NULLG[(n, ft)] = 10 ** brentq(fg, 0.0, 3.0, xtol=1e-4)
            except ValueError:
                NULLG[(n, ft)] = float("nan")
    P("    post hoc: gas multiplier (measured shape, extrapolated; stars re-calibrated) that nulls each central: "
      + "; ".join(f"{ft}: " + ", ".join(f"{n} x{NULLG[(n, ft)]:.1f}" for n in CEN) for ft in A0)
      + "  (nan = no root below x1000 or the inner JAM mass is exceeded first)")

    # ---------------------------------------------------------------- item 3
    P("\nITEM 3 -- derived mechanisms")
    P(" 3a census edge / supply cap")
    CENS = {}
    for ft, a0 in A0.items():
        for n in CEN:
            for who in ("own", "host"):
                if who == "host" and n not in HOSTC:
                    continue
                g, gN, M, _ = build(n, a0, gas="extrap")
                Rout = float(B[n]["Rb"][-1])
                if who == "own":
                    Mb = M + float(np.interp(math.log(Rout), LR, GAS[n][0]))
                else:
                    Rh = 1200.0 if n == 4486 else 3 * Rout
                    Mb = M + float(np.interp(math.log(Rh), LR, GAS[n][0]))
                fr, lMta = L515.fret_census(Mb)
                redge = L515.r_edge_pm(Mb * MSUN, G, a0, fr) / KPC
                supply = L515.COLD_PER_B * Mb / fr
                Mph = float(np.interp(math.log(Rout), LR, (g - gN) * (RG * KPC) ** 2 / G / MSUN))
                binds = bool(redge < Rout or Mph > supply)
                CENS[(n, ft, who)] = dict(Mb=Mb, f_ret=fr, logMta=lMta, r_edge_kpc=redge, R_out_kpc=Rout, supply=supply,
                                          Mph_Rout=Mph, binds=binds)
                P(f"    {ft:9s} NGC{n} {who:4s}: M_b {Mb:.2e}  f_ret {fr:.3f}  r_edge {redge:7.0f} kpc vs R_out {Rout:5.0f}  "
                  f"M_ph(<R_out) {Mph:.2e} vs supply {supply:.2e}  -> cap binds: {binds}")
    anybind = any(v["binds"] for v in CENS.values())
    def capped(n, a0, ft):
        c = CENS[(n, ft, "own")]
        return off_of(n, a0, gas="extrap", cap=c["supply"] if c["binds"] else None)
    row("3a census edge (own supply cap)", capped, "3a", derived=True, note="cap binds somewhere: %s" % anybind)
    P(" 3b round rule = 1e (prediction already RM; no change).  3c host ownership = row 2c.")

    P(" 3d TEMPLATE (not derived): host unsettled cold energy from X-COP (CFG432), host centres only, Newtonian")
    TPL = {}
    for ft, a0 in A0.items():
        for n in HOSTC:
            Mu, info = template_Mu(n, a0, ft)
            TPL[(n, ft)] = dict(info, Mu_Rout=float(np.interp(math.log(B[n]["Rb"][-1]), LR, Mu)),
                                Mu_r12=float(np.interp(math.log(B[n]["r12"]), LR, Mu)), Mjam_half=0.5 * B[n]["Mjam"])
        P(f"    {ft}: " + "; ".join(f"NGC{n}: Q01 {TPL[(n, ft)]['Q01']:.2f}, s {TPL[(n, ft)]['s_gas']:+.3f}, R500 {TPL[(n, ft)]['R500']:.0f}, "
                                   f"M_u(<R_out) {TPL[(n, ft)]['Mu_Rout']:.2e}, M_u(<r12) {TPL[(n, ft)]['Mu_r12']:.2e} vs M_JAM/2 {TPL[(n, ft)]['Mjam_half']:.2e}" for n in HOSTC))
    def tpl(n, a0, ft, rfac=1.0, flat=False):
        if n not in HOSTC:
            return off_of(n, a0, gas="extrap", own=True)
        Mu, _ = template_Mu(n, a0, ft, rfac, flat)
        return off_of(n, a0, gas="extrap", own=True, extraM=Mu)
    TROWS = []
    for lbl, kw in (("3d template R-own (primary)", {}), ("3d template flat Q inward", dict(flat=True)),
                    ("3d template R500 x0.7", dict(rfac=0.7)), ("3d template R500 x1.3", dict(rfac=1.3))):
        TROWS.append(row(lbl, lambda n, a0, ft, kw=kw: tpl(n, a0, ft, **kw), "3d", admissible=False, note="TEMPLATE, not derived"))
    def tlabel(r):
        if r["closes_both"]:
            return "TEMPLATE CLOSES"
        hc = all(r[ft]["Z"][f"NGC{n}"] < 2 for ft in A0 for n in HOSTC if np.isfinite(r[ft]["Z"][f"NGC{n}"]))
        return "TEMPLATE PARTIAL" if hc else "TEMPLATE NO"
    TLAB = tlabel(TROWS[0])
    P(f"    template label (primary): {TLAB}; brackets: " + ", ".join(tlabel(r) for r in TROWS[1:]))

    # ---------------------------------------------------------------- joint best case
    P("\nJOINT BEST CASE (R-own extrapolated gas, beta +0.5, heaviest admissible IMF per galaxy, D x1.1, outer bins)")
    def heaviest(n, ft):
        best, bm = "jam", None
        for r in ("salp", "chab2x", "chab"):
            if EPS[r][ft][f"NGC{n}"] <= 0.06:
                m = Mpop(n, r)
                if m > build(n, A0[ft])[2] and (bm is None or m > bm):
                    best, bm = r, m
        return best
    HEAV = {(n, ft): heaviest(n, ft) for n in CEN for ft in A0}
    P("    IMF row used: " + "; ".join(f"{ft}: " + ", ".join(f"{n} {HEAV[(n, ft)]}" for n in CEN) for ft in A0))
    joint = row("JOINT best case", lambda n, a0, ft: dist_off(n, a0, 1.1 * ORIG[n]["D"], mstar=HEAV[(n, ft)], gas="extrap", own=True, beta=0.5), "joint")
    jt = row("JOINT + template (reported)", lambda n, a0, ft: dist_off(n, a0, 1.1 * ORIG[n]["D"], mstar=HEAV[(n, ft)], gas="extrap", own=True, beta=0.5,
             extraM=(template_Mu(n, a0, ft)[0] if n in HOSTC else None)) if True else None, "joint", admissible=False, note="TEMPLATE")

    # ---------------------------------------------------------------- checks
    P("\nCHECKS")
    d1 = max(abs(ROWS["1a(i) JAM-law ceiling (K0, record)"][ft]["per"][f"NGC{n}"] - K0J[ft]["per_galaxy"][f"NGC{n}"]) for ft in A0 for n in CEN)
    check("K1 K0 path reproduces CFG330 K0 per central to 1e-9", d1 < 1e-9, f"max |diff| {d1:.2e}")
    d2 = max(max(abs(ROWS["2c R-own (CFG331)"][ft]["per"][f"NGC{n}"] - C331[f"{ft}|own"]["per"][f"NGC{n}"]),
                 abs(ROWS["2b R-bar gas extrapolated (CFG331)"][ft]["per"][f"NGC{n}"] - C331[f"{ft}|bar"]["per"][f"NGC{n}"])) for ft in A0 for n in CEN)
    check("K2 R-own / R-bar reproduce CFG331 JSON to 1e-9", d2 < 1e-9, f"max |diff| {d2:.2e}")
    check("K3 sigma_i loaded from CFG466 for 4 x 2", len(SIG) == 8 and all(np.isfinite(v) and v > 0 for v in SIG.values()), f"{len(SIG)} values")
    check("K4 fret_census is CFG515's (imported module)", L515.__file__.endswith(os.path.join("CFG515_census_edge_resolution", "cfg515_lib.py")), L515.__file__.split("campaign_fresh_gravity")[-1])

    # ---------------------------------------------------------------- verdict
    P("\nVERDICT (frozen order)")
    item1 = [k for k, v in ROWS.items() if v["item"] in ("1a", "1b", "1c", "1d") and v["admissible"] and v["closes_both"] and not k.startswith("1a(i)")]
    mech = [k for k, v in ROWS.items() if v["derived"] and v["closes_both"]]
    if item1:
        V = "DATA-ISSUE"; why = item1
    elif mech:
        V = "MECHANISM FOUND"; why = mech
    elif joint["closes_both"]:
        V = "NOT DIAGNOSTIC"; why = ["joint best case closes"]
    else:
        zc = min(joint[ft]["Z_class"] for ft in A0)
        V = f"GENUINE TENSION ({zc:.1f} sigma, joint best case, less favourable footing)"; why = []
    P(f"  headline: {V}  {why}")
    P(f"  joint best case Z_class: " + ", ".join(f"{ft} {joint[ft]['Z_class']:+.2f} (cleared {joint[ft]['n_cleared']}/4)" for ft in A0))
    P(f"  primary Z_class K0: " + ", ".join(f"{ft} {k0[ft]['Z_class']:+.2f}" for ft in A0) + "; R-own: "
      + ", ".join(f"{ft} {ROWS['2c R-own (CFG331)'][ft]['Z_class']:+.2f}" for ft in A0))
    P(f"  template (not derived): {TLAB}")
    res = dict(lane="CFG528", frozen_commit="5ad8324fa", mutate=False, kappa="1/2 FITTED", a0=A0, sigma_i={f"NGC{n}|{ft}": SIG[(n, ft)] for n in CEN for ft in A0},
               rows=ROWS, eps_in=EPS, null_mstar={f"NGC{n}|{ft}": v for (n, ft), v in NULLM.items()},
               null_distance={f"NGC{n}|{ft}": v for (n, ft), v in NULLD.items()}, null_gas={f"NGC{n}|{ft}": v for (n, ft), v in NULLG.items()},
               census={f"NGC{n}|{ft}|{w}": v for (n, ft, w), v in CENS.items()}, template={f"NGC{n}|{ft}": v for (n, ft), v in TPL.items()},
               template_label=TLAB, joint_imf={f"NGC{n}|{ft}": v for (n, ft), v in HEAV.items()}, headline=V, headline_rows=why,
               checks_pass=sum(ok), checks_total=len(ok))
else:
    P("\nMUTATE")
    k0 = {ft: {n: off_of(n, a0) for n in CEN} for ft, a0 in A0.items()}
    ma = row("MA Chabrier, gas x0, members x0", lambda n, a0, ft: off_of(n, a0, mstar="chab"), "M")
    ca = (not ma["closes_both"]) and all(ma[ft]["n_cleared"] <= 1 for ft in A0) and all(ma[ft]["per"][f"NGC{n}"] >= k0[ft][n] for ft in A0 for n in CEN)
    check("MA must NOT close; >= 3/4 Z >= 2; every offset >= K0", ca, "offsets vs K0: " + "; ".join(f"{ft}: " + ", ".join(f"{n} {ma[ft]['per'][f'NGC{n}'] - k0[ft][n]:+.3f}" for n in CEN) for ft in A0))
    mb = row("MB planted M* x8 (K0)", lambda n, a0, ft: off_of(n, a0, mmult=8.0), "M")
    check("MB must CLOSE on both footings", mb["closes_both"], f"cleared {mb['canonical']['n_cleared']}/{mb['alt']['n_cleared']}")
    mc = 0.0
    for ft, a0 in A0.items():
        for n in CEN:
            a = off_of(n, a0, gas="extrap", own=True, extraM=np.zeros_like(RG)); b = C331[f"{ft}|own"]["per"][f"NGC{n}"]
            mc = max(mc, abs(a - b))
    check("MC template x0 reproduces row 2c (CFG331 R-own) to 1e-9", mc < 1e-9, f"max |diff| {mc:.2e}")
    res = dict(lane="CFG528", mutate=True, rows=ROWS, checks_pass=sum(ok), checks_total=len(ok))

P(f"\n  {sum(ok)}/{len(ok)} checks pass")
json.dump(res, open(os.path.join(HERE, f"cfg528_mechanism{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg528_mechanism{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(ok) else 1)
