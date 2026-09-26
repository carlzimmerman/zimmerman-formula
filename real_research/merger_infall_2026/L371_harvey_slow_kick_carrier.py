#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L371 -- THE HARVEY TEST ON L366's SLOW-KICK CARRIER: does the virialization-triggered carrier kicked at v_k ~ 650 km/s
keep enough collisionless mass in group cores to hold the lensing peak on the galaxies when the gas is knocked loose?

WHY.  L370 (B3, B6, B7): L357's vacuum-gated carrier (3000 km/s kicks, decayed cores) pulls a substructure's lensing peak
toward its displaced gas, +1.8 to +3.4 sigma against Harvey+2015 (<beta> = -0.04 +/- 0.07, 72 substructures).  The failure
survives with the MOND kernel switched off: it is the hollowed core (the Bullet-cluster logic), not the boost.  An intact
carrier passes.  L366 found a joint window for the slow-kick carrier (x_c = 5, v_k ~ 650 km/s) whose clusters keep part of
their carrier (median retention 0.32).  This lane asks whether that is enough in group-mass substructures.

INPUT FROM L366 (committed 2f8e3e2c5; retention eps = M_c(<1 Mpc/h) / LCDM at z = 0, v_k = 650 km/s, by the halo's LCDM
mass M(<1 Mpc/h) in Msun/h):
  6e13-1e14: median 0.18 (range 0.06-0.26);  1e14-1.5e14: 0.24 (0.07-0.51);  1.5e14-2.5e14: 0.40 (0.14-0.73);  >= 2.5e14: 0.75.
  Harvey's substructures by lensing mass (Msun -> Msun/h): 1e14 -> 0.18 (bin maximum 0.26); 3e14 -> 0.40 (maximum 0.73);
  the 1e15 main cluster -> 0.75.  L366's retention is at z = 0; Harvey's systems sit at z ~ 0.2-0.6 (stated, not corrected:
  L366's trigger acts as halos form, so most of a group's decays precede z ~ 0.4).
  L366's 0.39 Mpc/h mesh does not resolve HOW that carrier sits inside a core, so three shapes bracket it, each rescaled so
  that M_c(<1 Mpc/h comoving) = eps x LCDM's:
    S1 scaled NFW -- the retained carrier keeps the original cusp (optimistic);
    S2 the phase-mixed profile of daughters kicked at 650 km/s in the halo's own potential (L321's retained(), Newtonian
       orbits as L353 requires, every carrier particle decayed as L366's mesh trigger does inside a halo);
    S3 recaptured, marginally bound daughters, rho ~ sqrt(2[Phi(2 R200) - Phi(r)]) -- the hottest a bound population can be
       (pessimistic; L366's low retention says most of a group's daughters left its progenitors and some fell back).
METHOD.  L370's machinery, loaded unedited: its definitions (cosmology, the L340 kernel, L359's switch, L361's region
  kernel, the construction's real halo solved to the lensing M200, the periodic-FFT QUMOND grid) and its Harvey helpers
  (iterated centroids in 100 / 150 kpc apertures, the Lenstool-like projected-NFW fit on 40-300 kpc).  The same eight
  substructure configurations (lensing M200 1e14 / 3e14, 400 kpc from a 1e15 main cluster at z = 0.4, gas displaced by
  60 / 120 kpc, perpendicular to / toward the main cluster); LCDM = the same components, all real; canonical footing.
CHECKS
  C1 CONTROL: L370's machinery is reproduced -- this lane's intact carrier gives L370's configuration-averaged excess beta
     (all three estimators, to 0.005), read from L370's committed results.
  H1 S1 (scaled cusp) at L366's median retention: the population-mean excess beta lies within 2 sigma of Harvey's
     (<= +0.10) for all three estimators.
  H2 S2 (phase-mixed daughters) at the median: the same.
  H3 S3 (recaptured, marginally bound) at the median: the same.
  H4 (reported) S1 at each bin's MAXIMUM retention -- the most favourable case L366 allows.
MUTATE=1 sets every retention to 1 (the intact carrier in every variant): H1-H3 must then pass, the inverted control of a
  failure (rc = 0 expected for MUTATE if the main run fails, and the verdict line states which).

Run from the repository root:  python3 real_research/merger_infall_2026/L371_harvey_slow_kick_carrier.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FAST", "0") == "1"                             # smoke test only (coarse grid, few radii); never committed
SLUG = "L371_harvey_slow_kick_carrier" + ("_MUTATE" if MUTATE else "") + ("_FAST" if FAST else "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L371", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: every retention set to 1 (intact carrier) -- H1-H3 must pass ***")

# ------------------------------------------------------------------------------------------------ L370's machinery, unedited
P70 = os.path.join(HERE, "L370_boosted_infall_mergers.py")
_s70 = open(P70).read()
_head = _s70.split("# ============================================================================================================ C1")[0]
_head = _head.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
L = {"__name__": "l370", "__file__": P70}
exec(_head, L)
L["MUTATE"] = False                                                   # L371's MUTATE changes the retention, never L370's kernel
RealHalo, cum_mass, m_in, RG, GK, A0K, SW_DEF, Grid, phantom_felt = (L[k] for k in (
    "RealHalo", "cum_mass", "m_in", "RG", "GK", "A0K", "SW_DEF", "Grid", "phantom_felt"))
h, Ez2 = L["h"], L["Ez2"]
from scipy.optimize import brentq
from scipy.interpolate import PchipInterpolator
# L370's Harvey helpers (centroid, sig_nfw_shape, nfw_fit_centre, paint_at), loaded unedited on the same grid
ZH, NH, LH = 0.4, (160 if FAST else 400), 10000.0
GH = Grid(NH, LH); DXH = GH.dx
XSUB, HARV_BETA, HARV_ERR = 400.0, -0.04, 0.07
_i0, _i1 = _s70.index("def centroid(S, x0, y0, Rap, it=12):"), _s70.index("HB = []")
L.update(dict(GH=GH, DXH=DXH, NH=NH, LH=LH))
exec(_s70[_i0:_i1], L)
centroid, nfw_fit_centre, paint_at = L["centroid"], L["nfw_fit_centre"], L["paint_at"]
P(f"\n  L370 machinery loaded (grid {NH}^3 over {LH / 1e3:.0f} Mpc, {DXH:.1f} kpc cells)   [{time.time() - T0:.0f}s]")

# ------------------------------------------------------------------------------------------------ L366's retention
EPS = {"med": {1e14: 0.18, 3e14: 0.40, 1e15: 0.75}, "max": {1e14: 0.26, 3e14: 0.73, 1e15: 0.80}}
FGAS_S, FSTAR_S = 0.10, 0.02                                          # substructures (as L370)
RN = 1000.0 / h / (1 + ZH)                                            # 1 Mpc/h comoving, physical kpc at z = 0.4
VK = 650.0


def q_static(args):
    """S2's shape: L321's retained() (Newtonian orbits, f_d = 1, v_k = 650 km/s) at a set of radii for one halo."""
    M200r, c, Mb_tab, gates = args
    import io, contextlib
    P21 = os.path.join(REPO, "real_research", "dark_sector_2026", "L321_carrier_z0_retention_gate.py")
    src = open(P21).read()
    top = src.split("# ============================================================================================ controls")[0].split("P(__doc__)", 1)[1]
    Lm = {"__name__": "l321", "__file__": P21, "HERE": os.path.dirname(P21), "MUTATE": False, "P": (lambda *a: None),
          "banner": (lambda t: None), "json": json, "os": os, "math": math, "np": np, "time": time, "T0": time.time(),
          "CH": [], "OUT": {"numbers": {}}, "check": (lambda *a, **k: True), "SLUG": "l321"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec("import os, sys, json, math, time\nimport numpy as np\n" + top, Lm)
    g21 = Lm["gravity"]
    Lm["gravity"] = lambda gb, gc, ge, cp: (gb + gc) if cp == "newtonian" else g21(gb, gc, ge, cp)
    Mb_fn = lambda r: np.interp(np.asarray(r, float), RG, Mb_tab)
    rhoc = 2.775e11 * h ** 2 / 1e9 * Ez2(ZH)
    return [Lm["retained"](Mb_fn, M200r, c, rg, 0.0, "newtonian", VK, 1.0, rhoc=rhoc)[0] for rg in gates]


def shape_ratio(H0, shape, eps, qtab=None):
    """density ratio w(r) = rho_retained / rho_carrier,LCDM on RG, normalized to eps within RN."""
    rc0 = H0.rho_c
    Mc0 = cum_mass(rc0)
    if MUTATE or shape == "intact":
        return np.ones_like(RG)
    if shape == "S1":
        return np.full_like(RG, eps)
    if shape == "S2":
        gates, q = qtab
        f = PchipInterpolator(np.log(gates), q)
        qr = np.where(RG < gates[0], q[0], np.where(RG > gates[-1], q[-1], f(np.log(np.clip(RG, gates[0], gates[-1])))))
        Mret = qr * Mc0
    else:                                                              # S3: rho ~ sqrt(2 [Phi(R_out) - Phi(r)])_+
        Mtot = cum_mass(H0.rho)
        g = GK * Mtot / RG ** 2
        seg = 0.5 * (g[1:] + g[:-1]) * np.diff(RG)
        Phi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])     # Phi(r) - Phi(RG[-1])
        Rout = 2.0 * H0.R200
        dPhi = np.maximum(float(np.interp(Rout, RG, Phi)) - Phi, 0.0)
        rho3 = np.sqrt(2 * dPhi)
        Mret = cum_mass(rho3)
    s = eps * float(np.interp(RN, RG, Mc0)) / float(np.interp(RN, RG, Mret))
    Mret = s * Mret
    dM = np.gradient(Mret, RG)
    rho_ret = np.maximum(dM / (4 * math.pi * RG ** 2), 0.0)
    return np.where(rc0 > 0, rho_ret / np.maximum(rc0, 1e-300), 0.0)


def build(M200r, M200L_target, shape, eps, qtab, fgas, fstar):
    H = RealHalo(M200r, ZH, fgas, fstar, "intact")
    w = shape_ratio(H, shape, eps, qtab)
    H.rho_c = w * H.rho_c; H.rho = H.rho_b + H.rho_c
    return H


def solve_l366(M200L, shape, eps, qtab, fgas, fstar, kernel=True):
    fn = lambda M: build(M, M200L, shape, eps, qtab, fgas, fstar).lensing(A0K["canonical"], SW_DEF, kernel)["M200L"] - M200L
    M = brentq(fn, 0.2 * M200L, 6.0 * M200L, rtol=1e-6)
    return build(M, M200L, shape, eps, qtab, fgas, fstar)


# ================================================================================================ S2's shape
banner("S2  THE PHASE-MIXED SHAPE of daughters kicked at 650 km/s (L321's retained(), Newtonian orbits, f_d = 1)")
GATES = np.array([50.0, 150.0, 400.0, RN] if FAST else [25.0, 50.0, 100.0, 150.0, 250.0, 400.0, 700.0, RN])
QTAB = {}
jobs = []
for Ml in (1e14, 3e14, 1e15):
    fg, fs = (FGAS_S, FSTAR_S) if Ml < 1e15 else (0.125, 0.015)
    H0 = RealHalo(Ml, ZH, fg, fs, "intact")                            # the shape proxy uses the lensing-mass halo
    jobs.append((H0.M200, H0.c, cum_mass(H0.rho_b), GATES))
for Ml, q in zip((1e14, 3e14, 1e15), map(q_static, jobs)):
    if True:
        QTAB[Ml] = (GATES, np.array(q))
        P(f"    lensing M200 {Ml:.0e}: retained/control within r = " + ", ".join(f"{g:.0f}:{v:.3f}" for g, v in zip(GATES, q))
          + f"   [{time.time() - T0:.0f}s]")
OUT["numbers"]["S2_q"] = {f"{k:.0e}": dict(gates=list(map(float, v[0])), q=list(map(float, v[1]))) for k, v in QTAB.items()}

# ================================================================================================ the Harvey configurations
banner("H  HARVEY+2015 ON THE SLOW-KICK CARRIER: substructures 400 kpc from a 1e15 main cluster, z = 0.4")
CONF = [(Msub, dSG, orient) for Msub in (1e14, 3e14) for dSG in (60.0, 120.0) for orient in ("perp", "toward_main")]
VARIANTS = {"intact": ("intact", "med"), "S1_med": ("S1", "med"), "S2_med": ("S2", "med"), "S3_med": ("S3", "med"),
            "S1_max": ("S1", "max")}
RES = {}
for (Msub, dSG, orient) in CONF:                                       # LCDM: the same components, all real
    gx, gy = (XSUB, dSG) if orient == "perp" else (XSUB - dSG, 0.0)
    ux, uy = ((0.0, 1.0) if orient == "perp" else (-1.0, 0.0))
    HsL = solve_l366(Msub, "intact", 1.0, None, FGAS_S, FSTAR_S, kernel=False)
    SL = (paint_at(HsL.rho_c + HsL.rho_s, XSUB, 0.0, m_in(HsL.rho_c + HsL.rho_s, 1e9))
          + paint_at(HsL.rho_g, gx, gy, m_in(HsL.rho_g, 1e9))).sum(axis=2) * DXH
    res = dict(Msub=Msub, dSG=dSG, orient=orient, gx=gx, gy=gy, ux=ux, uy=uy)
    for Rap in (100.0, 150.0):
        cx, cy = centroid(SL, XSUB, 0.0, Rap); res[f"LCDM_{Rap:.0f}"] = (cx - XSUB) * ux + cy * uy
    fx, fy = nfw_fit_centre(SL, XSUB, 0.0); res["LCDM_fit"] = (fx - XSUB) * ux + fy * uy
    RES[(Msub, dSG, orient)] = res
P(f"    LCDM substructure maps done   [{time.time() - T0:.0f}s]")
ic0 = NH // 2; icx = int(round((XSUB + LH / 2) / DXH))
CORE = {}
for vname, (shape, which) in VARIANTS.items():
    Hm = solve_l366(1e15, shape, EPS[which][1e15], QTAB[1e15], 0.125, 0.015)
    bm = paint_at(Hm.rho_b, 0.0, 0.0, m_in(Hm.rho_b, 1e9)); cm = paint_at(Hm.rho_c, 0.0, 0.0, m_in(Hm.rho_c, 1e9))
    _, _, rph, _ = phantom_felt(GH, bm, bm + cm, ZH, A0K["canonical"], SW_DEF, [(ic0, ic0, ic0)])
    SMAIN = (bm + cm + rph).sum(axis=2) * DXH
    del rph
    for Msub in (1e14, 3e14):
        Hs = solve_l366(Msub, shape, EPS[which][Msub], QTAB[Msub], FGAS_S, FSTAR_S)
        CORE[(vname, Msub)] = m_in(Hs.rho_c, 150.0) / max(m_in(Hs.rho_b, 150.0), 1e-30)
        ss = paint_at(Hs.rho_s, XSUB, 0.0, m_in(Hs.rho_s, 1e9)); cs = paint_at(Hs.rho_c, XSUB, 0.0, m_in(Hs.rho_c, 1e9))
        for (Ms_, dSG, orient) in CONF:
            if Ms_ != Msub:
                continue
            res = RES[(Msub, dSG, orient)]
            gs = paint_at(Hs.rho_g, res["gx"], res["gy"], m_in(Hs.rho_g, 1e9))
            rb = bm + ss + gs; rreal = rb + cm + cs
            gfelt, labs, rph, _ = phantom_felt(GH, rb, rreal, ZH, A0K["canonical"], SW_DEF, [(ic0, ic0, ic0), (icx, ic0, ic0)])
            S = (rreal + rph).sum(axis=2) * DXH - SMAIN
            for Rap in (100.0, 150.0):
                cx, cy = centroid(S, XSUB, 0.0, Rap)
                res[f"beta_{vname}_{Rap:.0f}"] = ((cx - XSUB) * res["ux"] + cy * res["uy"] - res[f"LCDM_{Rap:.0f}"]) / dSG
            fx, fy = nfw_fit_centre(S, XSUB, 0.0)
            res[f"beta_{vname}_fit"] = ((fx - XSUB) * res["ux"] + fy * res["uy"] - res["LCDM_fit"]) / dSG
            del gs, rb, rreal, gfelt, rph
        del ss, cs
    del bm, cm, SMAIN
    P(f"    {vname:7s} (shape {shape}, retention {which}): carrier/baryons inside 150 kpc of the galaxies "
      f"{CORE[(vname, 1e14)]:.2f} (1e14) / {CORE[(vname, 3e14)]:.2f} (3e14)   [{time.time() - T0:.0f}s]")
OUT["numbers"]["core_carrier_to_baryons_150kpc"] = {f"{k[0]}|{k[1]:.0e}": v for k, v in CORE.items()}
EST = ("100", "150", "fit")
MEAN = {v: {e: float(np.mean([RES[c][f"beta_{v}_{e}"] for c in CONF])) for e in EST} for v in VARIANTS}
OUT["numbers"]["mean_beta"] = MEAN
OUT["numbers"]["rows"] = [dict(RES[c], Msub=c[0], dSG=c[1], orient=c[2]) for c in CONF]
for c in CONF:
    r = RES[c]
    P(f"    sub {c[0]:.0e} dSG {c[1]:.0f} {c[2]:11s}: excess beta (100 / 150 / fit) " + "; ".join(
        f"{v} {r[f'beta_{v}_100']:+.3f}/{r[f'beta_{v}_150']:+.3f}/{r[f'beta_{v}_fit']:+.3f}" for v in VARIANTS))
P("    population means (100 / 150 / fit): " + "; ".join(f"{v} " + "/".join(f"{MEAN[v][e]:+.3f}" for e in EST) for v in VARIANTS))
P("    in sigma from Harvey's <beta>:     " + "; ".join(f"{v} " + "/".join(f"{(MEAN[v][e] - HARV_BETA) / HARV_ERR:+.1f}" for e in EST)
                                                         for v in VARIANTS))

# ================================================================================================ checks
banner("CHECKS")
p70 = os.path.join(HERE, "L370_boosted_infall_mergers_results.json")
if os.path.exists(p70) and not MUTATE:
    ref = json.load(open(p70))["numbers"]["B_mean_beta"]["intact"]
    diffs = [abs(MEAN["intact"][e] - ref[e]) for e in EST]
    check("C1 CONTROL: L370's machinery reproduced -- the intact carrier's configuration-averaged excess beta equals L370's "
          "committed value (all three estimators, to 0.005)", f"this lane {[round(MEAN['intact'][e], 4) for e in EST]} vs "
          f"L370 {[round(ref[e], 4) for e in EST]}", max(diffs) < 0.005)
else:
    check("C1 CONTROL: L370's machinery reproduced (skipped: L370's results absent, or MUTATE)", "not run", True, load_bearing=False)
ok_b = lambda v: all(MEAN[v][e] <= HARV_BETA + 2 * HARV_ERR for e in EST)
for tag, v, what in (("H1", "S1_med", "S1 (the retained carrier keeps the cusp) at L366's median retention"),
                     ("H2", "S2_med", "S2 (phase-mixed 650 km/s daughters) at L366's median retention"),
                     ("H3", "S3_med", "S3 (recaptured, marginally bound daughters) at L366's median retention")):
    check(f"{tag} {what}: the population-mean excess beta lies within 2 sigma of Harvey's <beta> (<= +0.10) for all three "
          "estimators", "/".join(f"{MEAN[v][e]:+.3f}" for e in EST) + " (100 / 150 / fit)", ok_b(v))
check("H4 (reported) S1 at each mass bin's MAXIMUM retention in L366 (0.26 / 0.73 / 0.80): the most favourable case",
      "/".join(f"{MEAN['S1_max'][e]:+.3f}" for e in EST), ok_b("S1_max"), load_bearing=False)

banner("VERDICT")
n_ok = sum(1 for _, ok, _ in CH if ok); n_lb_fail = sum(1 for _, ok, lb in CH if (not ok) and lb)
P(f"  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}   [{time.time() - T0:.0f}s]")
with open(os.path.join(HERE, SLUG + "_results.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
P(f"  wrote {SLUG}_results.json")
rc = 1 if n_lb_fail else 0
P(f"rc={rc}")
sys.exit(rc)
