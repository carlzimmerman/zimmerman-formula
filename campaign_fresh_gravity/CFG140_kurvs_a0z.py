#!/usr/bin/env python3
"""CFG140 -- a0 AT z ~ 1.4 FROM KURVS-CDFS'S OUTERMOST OBSERVED ROTATION POINTS: FLAT a0 AGAINST a0 PROPORTIONAL TO H(z).
One pipeline for three samples: KURVS-CDFS (Puglisi+2023; the 10 rotation-supported galaxies), a SPARC same-pipeline z = 0 anchor, and a
KROSS V2 z ~ 0.9 same-instrument control.  g_obs = V_c^2 / R (spherical surrogate) at the outermost measured point; g_bar from thin
exponential discs (stars R_d, gas 2 R_d); the gas is UNMEASURED for KURVS and KROSS -- a declared bracket, not data.

Criteria frozen and committed before any acceleration number: campaign_fresh_gravity/CFG140_FROZEN_CRITERIA.md (28dca75b8; pre-run C2
correction 49baf209f).
  grid     gas mu = M_gas/M* in {0.25, 0.67, 1.5, 4} x coherent M* offset delta in {-0.2, 0, +0.2} dex x pressure support {P0: none,
           P1: V_c^2 = V^2 + 2 sigma0^2 R/R_d} x a0 footing {canonical, alt} = 48 cells.
  readings flat: g_pred = nu_mono(g_bar/a0) g_bar;  rival: a = a0 E(z).  Delta = log10 g_obs - log10 g_pred; anchor-corrected
           Delta' = Delta(KURVS) - Delta(SPARC, measured gas, same P, delta, footing).
PRE-DECLARED (from the frozen file)
  C1 CONTROL  SPARC anchor (measured gas, P0, delta 0, canonical): median Delta_flat within +-0.10 dex of zero.
  C2 CONTROL  nu_mono's limits to 1e-5 at y = 1e-12 (sqrt(g a)) and 1e12 (g_bar)  [pre-run correction].
  C3 CONTROL  the 10 KURVS IDs are exactly the f_DM rows; every value used finite.
  R0 POWER    (printed before any g_obs or Delta) pooled expected separation log g_pred,H - log g_pred,flat per cell over the pooled
              per-object error (velocity error evaluated at the flat prediction's V); KURVS objects with g_bar < a0 at R.
  H0          feasibility (load-bearing): separation >= 2 sigma in the central cell (mu 0.67, delta 0, P1, canonical).
  H1 [HEADLINE; MUTATE must change it] flat a0 NOT disfavoured: NOT (Delta'_flat > +2 sigma in every one of the 48 cells).
  H2          (reported verdict) the rival disfavoured: Delta'_H < -2 sigma in every cell.
  R1-R6 (reported): the grid; per galaxy; KROSS and the differential; all-22 variant; the model R'_6D variant; SPARC with the bracket.
MUTATE=1: every KURVS v_last x 10^0.3 (g_obs x 4) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG140_kurvs_a0z.py   (MUTATE=1 for the control)
"""
import os, sys, io, csv, math, contextlib, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import CFG7_common as C
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG140_kurvs_a0z", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every KURVS v_last x 10^0.3 (g_obs x 4) -- H1 must FAIL ***")

G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = C4.A0
nu = lambda y: C4.nu_mono(np.asarray(y, float))
OM, OL = 0.315, 0.685
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + OL)
MUS, DELS, PS, FOOTS = (0.25, 0.67, 1.5, 4.0), (-0.2, 0.0, 0.2), ("P0", "P1"), ("canonical", "alt")
DINC = math.radians(5.0)
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")


def rd(path):
    return list(csv.DictReader(open(path)))


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def menc(M, R, s):
    y = R / s
    return M * (1 - math.exp(-y) * (1 + y))


# ------------------------------------------------------------------ the samples: (name, z, logM*, R, Rd, V, eV, sig, esig, inc_deg, einc, mgas_measured or None, sigma_Mstar)
def kurvs(ids=None, v_col="v_at_last_point_kms", e_col="e_v_last", r6d=False):
    I = {r["kurvs_id"]: r for r in rd(os.path.join(AT, "kurvs2023_integrated.csv"))}
    K = {r["kurvs_id"]: r for r in rd(os.path.join(AT, "kurvs2023_kinematics.csv"))}
    V = {r["kurvs_id"]: r for r in rd(os.path.join(AT, "kurvs2023_velocities_at_radii.csv"))}
    out = []
    for k in sorted(I, key=lambda s: int(s)):
        if ids is not None and int(k) not in ids:
            continue
        i, kk, vv = I[k], K[k], V[k]
        Rd = f(i["reff_kpc"]) / 1.68
        Rr = 6 * Rd if r6d else f(vv["R_halpha_max_kpc"])
        v = f(vv[v_col]) * (10 ** 0.3 if MUTATE else 1.0)
        out.append(dict(name=f"KURVS-{k}", z=f(i["z_halpha"]), lm=f(i["logMstar"]), R=Rr, Rd=Rd, V=v, eV=f(vv[e_col]) * (10 ** 0.3 if MUTATE else 1.0),
                        sig=f(kk["sigma0_kms"]), esig=f(kk["e_sigma0"]), inc=f(i["inc_star_deg"]), einc=DINC, mgas=None, sm=0.15,
                        vs=f(kk["vrot_over_sigma0"])))
    return out


def sparc():
    rows = []
    for line in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
        t = line.split()                                   # the data rows do not follow the header's byte columns; the field ORDER does
        if len(t) < 18:
            continue
        try:
            name = t[0]; inc = float(t[5]); einc = float(t[6]); L = float(t[7]); rdisk = float(t[11]); mhi = float(t[13]); q = int(t[17])
            float(t[2]); int(t[1])
        except ValueError:
            continue
        if not name or q not in (1, 2, 3):
            continue
        lm = math.log10(0.5 * L * 1e9) if L > 0 else -9
        if q > 2 or inc < 30 or lm < 9.5 or rdisk <= 0:
            continue
        fn = os.path.join(REPO, "real_research", "data", "sparc_data", f"{name}_rotmod.dat")
        if not os.path.exists(fn):
            continue
        pts = [l.split() for l in open(fn) if l.strip() and not l.startswith("#")]
        if not pts:
            continue
        last = pts[-1]
        rows.append(dict(name=name, z=0.0, lm=lm, R=float(last[0]), Rd=rdisk, V=float(last[1]), eV=float(last[2]), sig=10.0, esig=0.0, inc=inc,
                         einc=math.radians(einc), mgas=1.33 * mhi * 1e9, sm=0.10, vs=float("inf")))
    return rows


def kross():
    out = []
    for r in rd(os.path.join(REPO, "data_assembly", "high_z_tf_tables", "kross_v2.csv")):
        if r["kin_type"] not in ("RT", "RT+"):
            continue
        v, s, ms, rim, ba = f(r["vc_kms_intrinsic_at_2Rhalf"]), f(r["sigma0_kms"]), f(r["mstar_msun"]), f(r["rim_kpc"]), f(r["b_over_a"])
        if not all(np.isfinite([v, s, ms, rim, ba])) or v <= 0 or s <= 0 or ms <= 0 or rim <= 0 or v / s < 1:
            continue
        ev = 0.5 * (abs(f(r["e_vc_lower"])) + abs(f(r["e_vc_upper"])))
        out.append(dict(name="KROSS-" + r["kid"], z=f(r["z_halpha"]), lm=math.log10(ms), R=2 * rim, Rd=rim / 1.68, V=v, eV=ev if np.isfinite(ev) else 0.1 * v,
                        sig=s, esig=f(r["e_sigma0"]) if np.isfinite(f(r["e_sigma0"])) else 0.0, inc=math.degrees(math.acos(min(max(ba, 0.0), 1.0))),
                        einc=DINC, mgas=None, sm=0.15, vs=v / s))
    return out


# ------------------------------------------------------------------ the one pipeline
def gbar(o, mu, dlt, measured_gas=False):
    Ms = 10 ** (o["lm"] + dlt)
    Mg = o["mgas"] if (measured_gas and o["mgas"] is not None) else mu * Ms
    return G * (menc(Ms, o["R"], o["Rd"]) + menc(Mg, o["R"], 2 * o["Rd"])) * MSUN / (o["R"] * KPC) ** 2


def gobs(o, Pv, V=None):
    V = o["V"] if V is None else V
    vc2 = V ** 2 + (2 * o["sig"] ** 2 * o["R"] / o["Rd"] if Pv == "P1" else 0.0)
    return vc2 * 1e6 / (o["R"] * KPC), vc2


def dlog_gobs(o, Pv, V=None):
    V = o["V"] if V is None else V
    g, vc2 = gobs(o, Pv, V)
    tv = 2 * V * o["eV"]
    ts = 4 * o["sig"] * o["esig"] * o["R"] / o["Rd"] if Pv == "P1" else 0.0
    inc = math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60)
    ti = 2 * V ** 2 * o["einc"] / math.tan(inc)                    # V ~ 1/sin i -> dV^2 = 2 V^2 cot(i) di
    return math.sqrt(tv ** 2 + ts ** 2 + ti ** 2) / vc2 / math.log(10)


def gpred(gb, a):
    return float(nu(gb / a) * gb)


def slope(gb, a):
    h = 1e-4
    return (math.log(gpred(gb * (1 + h), a)) - math.log(gpred(gb * (1 - h), a))) / (math.log(1 + h) - math.log(1 - h))


def pooled(d, s):
    d, s = np.asarray(d), np.asarray(s)
    w = 1 / s ** 2
    m = float(np.sum(w * d) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w)))
    chi = float(np.sum(w * (d - m) ** 2)); dof = max(len(d) - 1, 1)
    if chi / dof > 1:
        e *= math.sqrt(chi / dof)
    return m, e


def score(objs, mu, dlt, Pv, foot, measured_gas=False, rival=False, V_override=None):
    D, S = [], []
    for o in objs:
        a = A0[foot] * (E(o["z"]) if rival else 1.0)
        gb = gbar(o, mu, dlt, measured_gas)
        gp = gpred(gb, a)
        V = None if V_override is None else V_override(o, gp)
        go, _ = gobs(o, Pv, V)
        s = math.hypot(dlog_gobs(o, Pv, V), slope(gb, a) * o["sm"])
        D.append(math.log10(go / gp)); S.append(s)
    return pooled(D, S), np.array(D), np.array(S)


KU_IDS = {3, 7, 8, 9, 11, 13, 15, 16, 17, 21}
KU = kurvs(KU_IDS); SP = sparc(); KR = kross()

# ================================================================== C1-C3
R.banner("C1 / C2 / C3  CONTROLS")
fdm_ids = {int(r["kurvs_id"]) for r in rd(os.path.join(AT, "kurvs2023_fdm.csv"))}
fin = all(np.isfinite([o[k] for k in ("z", "lm", "R", "Rd", "V", "eV", "sig", "esig")]).all() for o in KU)
check("C3 CONTROL: the 10 KURVS IDs are exactly the f_DM rows and every value used is finite",
      f"f_DM IDs {sorted(fdm_ids)}; selected {sorted(int(o['name'][6:]) for o in KU)}; finite {fin}; SPARC anchor N = {len(SP)}; KROSS control N = {len(KR)}",
      fdm_ids == KU_IDS and len(KU) == 10 and fin)
d1 = abs(gpred(1e-12 * A0["canonical"], A0["canonical"]) / math.sqrt(1e-12 * A0["canonical"] * A0["canonical"]) - 1)
d2 = abs(gpred(1e12 * A0["canonical"], A0["canonical"]) / (1e12 * A0["canonical"]) - 1)
check("C2 CONTROL: nu_mono's limits to 1e-5 at y = 1e-12 (sqrt(g a)) and 1e12 (g_bar)  [pre-run correction]", f"{d1:.1e}, {d2:.1e}", d1 < 1e-5 and d2 < 1e-5)

# ================================================================== R0: power, before any g_obs
R.banner("R0 / H0  POWER (baryons and quoted errors only; the velocity error is evaluated at the flat prediction's V -- no observed velocity enters)")


def power(objs, mu, dlt, Pv, foot):
    sep, S = [], []
    for o in objs:
        gb = gbar(o, mu, dlt)
        gf = gpred(gb, A0[foot]); gh = gpred(gb, A0[foot] * E(o["z"]))
        vc2 = gf * o["R"] * KPC / 1e6
        vpred = math.sqrt(max(vc2 - (2 * o["sig"] ** 2 * o["R"] / o["Rd"] if Pv == "P1" else 0.0), 1.0))
        s = math.hypot(dlog_gobs(o, Pv, vpred), slope(gb, A0[foot]) * o["sm"])
        sep.append(math.log10(gh / gf)); S.append(s)
    w = 1 / np.array(S) ** 2
    return float(np.sum(w * np.array(sep)) / np.sum(w)), float(1 / math.sqrt(np.sum(w)))


PW = {}
for mu in MUS:
    for dlt in DELS:
        for Pv in PS:
            for foot in FOOTS:
                PW[(mu, dlt, Pv, foot)] = power(KU, mu, dlt, Pv, foot)
nlow = {mu: sum(1 for o in KU if gbar(o, mu, 0.0) < A0["canonical"]) for mu in MUS}
cen = (0.67, 0.0, "P1", "canonical")
s0, e0 = PW[cen]
P("    expected separation (dex) / pooled error per cell, canonical, delta 0:  " + "; ".join(f"mu {mu} {Pv}: {PW[(mu, 0.0, Pv, 'canonical')][0]:+.3f}/{PW[(mu, 0.0, Pv, 'canonical')][1]:.3f}"
                                                                                       for mu in MUS for Pv in PS))
P(f"    KURVS objects with g_bar < a0 (canonical) at R_max by mu: {nlow};  median z {np.median([o['z'] for o in KU]):.3f} (E = {E(np.median([o['z'] for o in KU])):.2f})")
h0 = s0 / e0 >= 2
check("H0 FEASIBILITY: expected separation >= 2 sigma in the central cell (mu 0.67, delta 0, P1, canonical)",
      f"separation {s0:+.3f} dex, pooled error {e0:.3f} -> {s0 / e0:.2f} sigma; range over all 48 cells {min(v[0] / v[1] for v in PW.values()):.2f}-{max(v[0] / v[1] for v in PW.values()):.2f} sigma; "
      "CFG52's correlated mass-scale floor caps any such test near 2.3 sigma", h0)

# ================================================================== H1 / H2
R.banner("H1 / H2  THE GRID (anchor-corrected; every cell)")
GRID = {}
for mu in MUS:
    for dlt in DELS:
        for Pv in PS:
            for foot in FOOTS:
                (kf, ekf), _, _ = score(KU, mu, dlt, Pv, foot)
                (kh, ekh), _, _ = score(KU, mu, dlt, Pv, foot, rival=True)
                (af, eaf), _, _ = score(SP, mu, dlt, Pv, foot, measured_gas=True)
                (ah, eah), _, _ = score(SP, mu, dlt, Pv, foot, measured_gas=True, rival=True)
                GRID[(mu, dlt, Pv, foot)] = dict(kf=kf, ekf=ekf, kh=kh, ekh=ekh, af=af, eaf=eaf, ah=ah, eah=eah,
                                                 df=kf - af, edf=math.hypot(ekf, eaf), dh=kh - ah, edh=math.hypot(ekh, eah))
for foot in FOOTS:
    for Pv in PS:
        P(f"    {foot} {Pv}: " + "; ".join(f"mu {mu}: D'_flat {GRID[(mu, 0.0, Pv, foot)]['df']:+.3f}+-{GRID[(mu, 0.0, Pv, foot)]['edf']:.3f}, D'_H {GRID[(mu, 0.0, Pv, foot)]['dh']:+.3f}"
                                   for mu in MUS) + "  (delta 0)")
fl_dis = all(v["df"] > 2 * v["edf"] for v in GRID.values())
fl_kill = all(v["df"] > 3 * v["edf"] for v in GRID.values())
rv_dis = all(v["dh"] < -2 * v["edh"] for v in GRID.values())
rv_kill = all(v["dh"] < -3 * v["edh"] for v in GRID.values())
n_fav_flat = sum(1 for v in GRID.values() if abs(v["df"]) <= 2 * v["edf"])
n_fav_h = sum(1 for v in GRID.values() if abs(v["dh"]) <= 2 * v["edh"])
check("H1 [HEADLINE] THE FRAMEWORK'S FLAT a0 IS NOT DISFAVOURED: NOT (anchor-corrected Delta'_flat > +2 sigma in every one of the 48 cells)" + ("  [MUTATE: v x 2]" if MUTATE else ""),
      f"cells with Delta'_flat > +2 sigma: {sum(1 for v in GRID.values() if v['df'] > 2 * v['edf'])}/48; cells where flat is within 2 sigma: {n_fav_flat}/48; "
      f"central cell Delta'_flat {GRID[cen]['df']:+.3f} +- {GRID[cen]['edf']:.3f}", not fl_dis)
check("H2 (reported verdict) THE RIVAL a0 ~ H(z) IS DISFAVOURED: Delta'_H < -2 sigma in every cell",
      f"cells with Delta'_H < -2 sigma: {sum(1 for v in GRID.values() if v['dh'] < -2 * v['edh'])}/48; cells where the rival is within 2 sigma: {n_fav_h}/48; "
      f"central cell Delta'_H {GRID[cen]['dh']:+.3f} +- {GRID[cen]['edh']:.3f}", rv_dis, load_bearing=False)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
anc = GRID[(0.67, 0.0, "P0", "canonical")]
_, Dan, _ = score(SP, 0.67, 0.0, "P0", "canonical", measured_gas=True)
check("C1 CONTROL: the SPARC anchor (measured gas, P0, delta 0, canonical): median Delta_flat within +-0.10 dex of zero",
      f"median {np.median(Dan):+.3f} dex (pooled {anc['af']:+.3f} +- {anc['eaf']:.3f}; N = {len(Dan)})", abs(np.median(Dan)) <= 0.10)
check("R1 (reported) the grid extremes: anchor-corrected Delta'_flat and Delta'_H over the 48 cells",
      f"Delta'_flat {min(v['df'] for v in GRID.values()):+.3f} .. {max(v['df'] for v in GRID.values()):+.3f}; Delta'_H {min(v['dh'] for v in GRID.values()):+.3f} .. "
      f"{max(v['dh'] for v in GRID.values()):+.3f}; SPARC anchor Delta_flat {min(v['af'] for v in GRID.values()):+.3f} .. {max(v['af'] for v in GRID.values()):+.3f}",
      True, load_bearing=False)
_, Dk, Sk = score(KU, 0.67, 0.0, "P1", "canonical")
_, Dkh, _ = score(KU, 0.67, 0.0, "P1", "canonical", rival=True)
check("R2 (reported) per KURVS galaxy, central cell: g_bar/a0 at R_max, Delta_flat, Delta_H (unanchored)",
      "; ".join(f"{o['name']} z {o['z']:.2f} R {o['R']:.1f} kpc g_bar/a0 {gbar(o, 0.67, 0.0) / A0['canonical']:.2f} D_flat {d:+.2f} D_H {dh:+.2f} (+-{s:.2f})"
                for o, d, dh, s in zip(KU, Dk, Dkh, Sk)), True, load_bearing=False)
zk, zr = float(np.median([o["z"] for o in KU])), float(np.median([o["z"] for o in KR]))
rows3 = []
for Pv in PS:
    (rf, erf), _, _ = score(KR, 0.67, 0.0, Pv, "canonical")
    (kf, ekf), _, _ = score(KU, 0.67, 0.0, Pv, "canonical")
    rows3.append(f"{Pv}: KROSS Delta_flat {rf:+.3f} +- {erf:.3f} (N {len(KR)}, median z {zr:.2f}); KURVS {kf:+.3f} +- {ekf:.3f}; differential {kf - rf:+.3f} +- {math.hypot(ekf, erf):.3f}")
pred_diff = math.log10(E(zk) / E(zr)) * 0.5
check("R3 (reported) KROSS (z ~ 0.9) through the same pipeline (mu 0.67, delta 0, canonical) and the differential KURVS - KROSS",
      "; ".join(rows3) + f"; predicted differential: flat 0, rival about +{pred_diff:.3f} dex in the deep regime (half the log E ratio)", True, load_bearing=False)
K22 = [o for o in kurvs(None) if o["vs"] >= 1]
(k22, ek22), _, _ = score(K22, 0.67, 0.0, "P1", "canonical")
(k22h, _), _, _ = score(K22, 0.67, 0.0, "P1", "canonical", rival=True)
check("R4 (reported) the all-22 variant with v/sigma0 >= 1 (central cell, unanchored)", f"N = {len(K22)}: Delta_flat {k22:+.3f} +- {ek22:.3f}, Delta_H {k22h:+.3f}",
      True, load_bearing=False)
K6 = kurvs(KU_IDS, v_col="v_at_R6D_kms", e_col="e_v_R6D", r6d=True)
(k6, ek6), _, _ = score(K6, 0.67, 0.0, "P1", "canonical")
(k6h, _), _, _ = score(K6, 0.67, 0.0, "P1", "canonical", rival=True)
check("R5 (reported) the R'_6D model-extrapolated velocities at 6 R_eff/1.68 (no seeing term; rough; central cell, unanchored)",
      f"Delta_flat {k6:+.3f} +- {ek6:.3f}, Delta_H {k6h:+.3f}", True, load_bearing=False)
r6 = []
for mu in MUS:
    (sf, esf), _, _ = score(SP, mu, 0.0, "P0", "canonical")
    r6.append(f"mu {mu}: {sf:+.3f} +- {esf:.3f}")
check("R6 (reported) SPARC with the mu bracket instead of its measured gas (P0, delta 0, canonical): pooled Delta_flat", "; ".join(r6), True, load_bearing=False)

if not h0:
    reading = "NON-DIAGNOSTIC: the test lacks the power to separate flat a0 from a0 ~ H(z) even before the brackets"
elif fl_kill:
    reading = "the framework's flat a0 is KILLED by KURVS across every declared bracket cell (> 3 sigma)"
elif fl_dis:
    reading = "the framework's flat a0 is DISFAVOURED by KURVS across every declared bracket cell (> 2 sigma)"
elif rv_kill:
    reading = "the rival a0 ~ H(z) is KILLED across every declared bracket cell (< -3 sigma); flat a0 not disfavoured"
elif rv_dis:
    reading = "the rival a0 ~ H(z) is DISFAVOURED across every declared bracket cell (< -2 sigma); flat a0 not disfavoured"
else:
    reading = "NON-DIAGNOSTIC over the declared brackets: some cells favour flat a0, some the rival; measured gas and a pressure-free tracer would settle it"
P(f"\n    READING (declared): {reading}")
R.num("grid", {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": v for k, v in GRID.items()}); R.num("power", {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": list(v) for k, v in PW.items()})
R.num("central", GRID[cen]); R.num("n_low", nlow); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
