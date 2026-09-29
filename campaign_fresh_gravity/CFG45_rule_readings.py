#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG45 -- FOUR PRE-DECLARED READINGS OF "THE FLUID KEEPS ITS COLLAPSE MASS", scored on every population B's cold-mass rule has met.

WHY.  Candidate B's derived rule (CFG35-CFG42): the cold fluid is conserved and keeps its collapse mass; the law's phantom is part of it.  CFG35
wrote this as a SUM, g = nu(g_N/a0) g_N + G f_ex (1 - f_b) M_NFW,collapse(<r) / r^2, f_ex = max(0, 1 - M_phantom,edge / [(1 - f_b) M_collapse]).  The sum
fits the SLUGGS massive early types (CFG38, 0.4 sigma), leaves star-forming spirals and SPARC dwarfs alone (CFG36, CFG42 H4), is weakly consistent with
Di Teodoro+2023's four S0/S0a (CFG41), and closes the Milky Way ultra-faint failure (CFG42: +0.325 -> -0.059 dex); but it OVER-predicts the classical
satellites (CFG42: M31 LVD -2.67 sigma, MW classical -1.8 / -1.9 sigma) and UGC 2487 (SPARC's one massive S0) by +0.14 dex in v (CFG36 H2).  The
suspicion (CFG42's own reading): the sum double-counts where the law's phantom already supplies the mass.  This harness scores, in one place and with the
EXACT statistic and error model of each lane, a SMALL family of readings written down here BEFORE any of them was run.  It picks no winner by fit, and
it adds no reading after the first run.

THE READINGS (declared; exactly these four; total acceleration g = nu(g_N/a0) g_N + g_extra, g_N the lane's Newtonian field of the baryons):
  (L) the bare law (control): g_extra = 0.
  (S) the sum as committed (CFG35): g_extra = f_ex (1 - f_b) G M_NFW(<r; M_c) / r^2.
  (M) the radial max: the dark mass inside r is max(M_phantom(<r), (1 - f_b) M_NFW(<r; M_c)), M_phantom(<r) = [nu - 1] M_b(<r) the law's own dark mass at
      that radius; no f_ex.  Written as an acceleration: g = g_N + max((nu - 1) g_N, (1 - f_b) G M_NFW(<r) / r^2), i.e. g_extra = max(0, (1 - f_b) G M_NFW(<r)/r^2
      - (g_law - g_N)).  (Where a lane's Newtonian field is not G M_b(<r)/r^2 -- Freeman discs -- the phantom is (g_law - g_N), the acceleration form.)
  (E) the exterior leftover: the law holds inside r_e = 0.40 r_ta (CFG7's r_ta_law at a = 1, both footings' own a0, nu_mono) and the leftover f_ex (1 - f_b) M_c
      is placed as NFW-shaped mass OUTSIDE r_e only: M_left(<r) = L [m(x) - m(x_e)] / [m(c) - m(x_e)] for r_e < r < R200 (m(t) = ln(1+t) - t/(1+t), x = c r / R200,
      L = f_ex (1 - f_b) M_c), and 0 for r <= r_e (and 0 throughout when r_e >= R200: nothing is placed inside the halo).  It contributes nothing inside r_e.
      Every lane radius is checked against r_e (C2); if any lane radius is at or beyond r_e the reading is reported as touching that lane.
Common ingredients (unchanged from the lanes): f_b = Omega_b/Omega_m of CFG35; f_ex from the edge phantom at x_e = 0.40 (CFG35's edge_phantom, both footings);
collapse mass M_c and NFW shape as each lane declares (Moster SHMR for the satellites and the SPARC dwarfs; Mandelbaum+2016's red / blue relation as M_200c
for the ellipticals, SLUGGS, SPARC >= 10, the four S0, Ogle); Dutton-Maccio NFW.  f_ex is used by (S) and (E) only; (M) has no f_ex (it is reported anyway).

THE POPULATIONS AND THEIR STATISTICS (each lane's script exec'd read-only up to its own data / machinery, MUTATE off inside; the estimators re-implemented
here line for line with a reading switch, and controlled in C1 against the lanes' committed results):
  P1  MW ultra-faints -- CFG42 H1 / CFG28: FG001's sigma^2 = g(r) r / 3 at r = (4/3) r_half; Kaplan-Meier median of log10(sigma_obs / sigma_pred) with the 9 upper
      limits; error = sqrt(bootstrap^2 (1000, seed 42) + Upsilon_V^2 floor (half the shift for Upsilon_V 1 to 4) + collapse-mass floor^2 (half the range of the
      KM median over M_c = 1e8, 3e8, 1e9, 3e9, 1e10 for every satellite with M_* < 1e5)).  Offset in sigma = KM median / error.  Both footings.
  P2  MW classical dSph (14), M31 Collins+13 (14), M31 LVD (34) -- CFG42 H2: the same estimator with the infall gas (CFG18's, the k = 5 expectation); sample median
      offset; error = sqrt((1.2533 std/sqrt n)^2 + Upsilon floor^2 + collapse floor^2), as CFG42.  Both footings.
  P3  SPARC dwarfs (log M_* < 10, n = 110; M_c from the Moster SHMR, CFG42 H4) and SPARC log M_* >= 10 (n = 61; M_c from Mandelbaum blue for T >= 1, red for T <= 0,
      CFG36 H2): d log v at R_HI = 0.5 log10(g_total / g_law), point mass, M_* = 0.61 L_3.6, + 1.33 M_HI, canonical, x_e = 0.40.  Reported: the fraction with
      f_ex = 0 (S, E), the maximum d log v, the fraction < 0.03 dex.
  P4a UGC 2487 (SPARC's S0): offset = log10(V_flat / v_pred(R_HI)), V_flat and its error from SPARC's table (332 +- 3.5 km/s), R_HI = 40.2 kpc, the P3 baryons
      and colour (T = 0, red).  CFG36 gave this galaxy NO error, only the +0.14 dex the rule adds; the error DECLARED HERE is
      sigma = sqrt( (eV/V/ln10)^2 + (0.5 x 0.1003)^2 + (0.25 x 0.2)^2 ): the measurement, SPARC's own per-point rms of the law (0.1003 dex in log g, CFG39 C2,
      halved for v), and the stellar mass at 0.2 dex (v goes as M^(1/4) in the deep regime).  Both footings.
  P4b Di Teodoro+2023's 15 massive spirals with the four S0 / S0a -- CFG41: offset = log10(v_flat/v_pred) - B, B = 0.076 +- 0.030 (the selection correction), point
      mass headline, the floor of model / M_* / M_gas / radius / B.  The S0 clause (CFG41 H2b): over the four (T <= 0) mean corrected offset > -2 sigma_S0.  Reported:
      the all-fifteen |mean| < 2 sigma (H2a) and the bare-law H1.
  P5  SLUGGS (19 early types, h50 machinery; CFG38 H1): mean over galaxies of the outer-bin mean of log10(sigma_obs/sigma_pred), red relation; error std/sqrt(19);
      both footings.  Reported: the slope against log M_* (bootstrap, seed 38).
  P6  X-ray ellipticals (7; CFG36 H1 / CFG35): per-galaxy median over 5, 10, 20, 40, 70 kpc of log10(M_total/M_pred), red relation; sample mean; error = sqrt(err^2 +
      Salpeter-shift^2 + (radii <= 40 kpc)-shift^2).  Both footings.
  P7  Ogle+2019 super spirals (23; CFG40): mean offset, slope and the nine fastest, floor model / M_* / M_gas.  Reported only; declared expectation: no change from (L).

ACCEPTANCE (declared): the CONJUNCTION of the lanes' own gates, the same for every reading:
  A1  UFD: |KM median| < 2 sigma, both footings.
  A2  classical satellites: MW classical, M31 Collins+13 and M31 LVD medians all above -2 sigma, both footings.
  A3  SPARC unchanged: d log v at R_HI < 0.03 dex in >= 90% of the dwarfs AND in >= 90% of the log M_* >= 10 galaxies.
  A4  SLUGGS |offset| < 2 sigma, both footings.
  A5  X-ray ellipticals |offset| < 2 sigma, both footings.
  A6  UGC 2487 |offset| < 2 sigma, both footings.
  A7  the DT23 S0 clause: canonical mean corrected offset over the four S0 / S0a above -2 sigma_S0 (CFG41's formula).
  EXTENDED (reported, not in the conjunction): CFG41's H2a (|mean over 15| < 2 sigma); CFG40's H2 (|mean|, |slope|, |fastest 9| each < 2 sigma) and 'no change from L'
  (|mean_reading - mean_law| < 0.03 dex); CFG36's strict SPARC clause (max d log v < 0.03 in every galaxy >= 10).
  REPORT: which readings pass which populations; which satisfy the whole conjunction (possibly none).  A reading that passes every gate is 'consistent with every
  lane', not 'chosen'; the four are not ranked by fit.

CONTROLS
  C1  CONTROL  (S) reproduces the lanes' committed numbers (CFG42 UF / CL / H4, CFG36 H1 / SPARC, CFG38 rule, CFG41 rule, CFG40 rule) to 1e-6 (satellite / DT23 / Ogle
               / SLUGGS / X-ray means and totals); (L) reproduces CFG42's law, CFG32's per-galaxy law offsets (as CFG35 C1), CFG41's and CFG40's law numbers to 1e-6 and
               h50's per-galaxy law offsets to 5e-3 (the printed precision, CFG38's tolerance).
  C2  CONTROL  (E) adds nothing inside r_e: the largest lane radius / r_e over all lanes is < 1 (else E is reported as touching that lane); every reading adds mass
               >= 0 everywhere; the edge phantom computed here equals CFG35's.
  C3  CONTROL  (MUTATE=1: every collapse mass divided by 100, every reading) -- the UFD gate A1 must FAIL for every reading in a MUTATE run.
  H1  [HEADLINE; MUTATE must fail] at least one of (S), (M), (E) passes A1 (the UFD gate) -- the rule has bite on the ultra-faints.
  H2  (reported) the table, and which readings satisfy A1-A7.
MUTATE=1: collapse masses / 100 for every reading -- H1 must FAIL (rc = 1).
ADDED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed): control C2a FAILED as its own text anticipates -- for every lane but SLUGGS the largest data radius is
  < 0.1 r_e, but SLUGGS's isotropic Jeans integral runs outward to very large radius, so E's exterior shell is sampled there.  C2a is kept as a FAIL (tolerance unchanged);
  a reported diagnostic (R1: the largest |E - L| in SLUGGS's per-galaxy offsets and in its mean) was added to say whether that matters.  No reading, gate or threshold changed.
Nothing here says the theory is closed; a reading that passes every declared gate is a reading not yet rejected by these lanes.
Run: python3 CFG45_rule_readings.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, csv, json
import numpy as np
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_GUESS = "/Users/carlzimmerman/new_physics/zimmerman-formula"
LANES = HERE if os.path.exists(os.path.join(HERE, "CFG7_common.py")) else os.path.join(REPO_GUESS, "campaign_fresh_gravity")
OUT = os.environ.get("CFG45_OUT", HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG45_rule_readings", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass / 100, every reading -- H1 must FAIL ***")
MCF = 0.01 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
READ = ("L", "S", "M", "E")
XE = 0.40


def exec_prefix(fname, marker):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(LANES, fname)).read()
    g = {"__file__": os.path.join(LANES, fname), "__name__": fname}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index(marker)], fname, "exec"), g)
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


BAR = "# ================================================================================================ "
g42 = exec_prefix("CFG42_satellites_rule.py", BAR + "C1 / C2")
g36 = g42["g36"]; g35 = g36["g35"]
g38 = exec_prefix("CFG38_sluggs_massive_passive.py", BAR + "C1")
g40 = exec_prefix("CFG40_super_spirals.py", 'R.banner("C2  CONTROL: the Freeman field")')
g41 = exec_prefix("CFG41_massive_spirals_hi.py", "S0 = lambda g:")

FB, nfw_enclosed, collapse_raw, edge_phantom36 = g36["FB"], g36["nfw_enclosed"], g36["collapse"], g36["edge_phantom"]
G_, KPC, MSUN, A0SI, RHO_C = g36["G_"], g36["KPC"], g36["MSUN"], g36["A0SI"], g36["RHO_C"]
g10, halo_mass = g36["g10"], g35["halo_mass"]
collapse = lru_cache(maxsize=None)(lambda Ms, colour: collapse_raw(Ms, colour))
SI_SAT = (g42["G"], g42["Msun"], 1000.0 * 3.0857e16)            # FG001's constants (G, Msun, kpc in m), as its estimator uses
SI_H10 = (G_, MSUN, KPC)

# ------------------------------------------------------------------------------------------------ the edge (phantom at x_e r_ta, and r_e)
_EDGE = {}


def edge_info(Mb, foot):
    k = (float(Mb), foot)
    if k not in _EDGE:
        a0 = C.A0[foot]; rta = C.r_ta_law(Mb, a0, C.nu_mono, 1.0)
        _EDGE[k] = (float(C.M_law(Mb, XE * rta, a0, C.nu_mono)) - Mb, XE * rta * 1000.0)        # (phantom mass inside r_e [Msun], r_e [kpc])
    return _EDGE[k]


TRACK = {"lane": "-", "maxratio": {}, "hits": {}}


def _m(t):
    return np.log1p(t) - t / (1 + t)


def extra_acc(reading, r_kpc, g_law, gN, Mh, fex, r_e_kpc, consts=SI_H10):
    """g_extra [m/s^2] beyond the law's g_law at radius r_kpc; Mh the (already MCF-scaled) M_200c."""
    G, Ms_, kpc = consts
    r = np.asarray(r_kpc, float)
    if reading == "L":
        return 0.0 * r
    conv = G * Ms_ / (r * kpc) ** 2
    if reading == "S":
        return fex * (1 - FB) * np.asarray(nfw_enclosed(Mh, r), float) * conv
    if reading == "M":
        return np.maximum(0.0, (1 - FB) * np.asarray(nfw_enclosed(Mh, r), float) * conv - (np.asarray(g_law, float) - np.asarray(gN, float)))
    if reading == "E":
        lane = TRACK["lane"]
        TRACK["maxratio"][lane] = max(TRACK["maxratio"].get(lane, 0.0), float(np.max(r / r_e_kpc)))
        TRACK["hits"][lane] = TRACK["hits"].get(lane, 0) + int(np.sum(r >= r_e_kpc))
        c = 10 ** (0.905 - 0.101 * (math.log10(Mh * 0.674) - 12.0))
        R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        if r_e_kpc >= R200:
            return 0.0 * r
        Ltot = fex * (1 - FB) * Mh; xe = c * r_e_kpc / R200
        x = np.minimum(c * r / R200, c)
        Mleft = np.where(r > r_e_kpc, Ltot * (_m(x) - _m(xe)) / (_m(c) - _m(xe)), 0.0)
        return Mleft * conv
    raise ValueError(reading)


# ================================================================================================ P1 / P2 satellites (CFG42's estimator)
SAMPLES, UL, LABEL, A0H, UPS_V, a_int, infall_gas = (g42[k] for k in ("SAMPLES", "UL", "LABEL", "A0H", "UPS_V", "a_int", "infall_gas"))
G_SAT, MSUN_SAT = g42["G"], g42["Msun"]


def sigma_read(d, foot, reading, ups=None, floor_mh=None, gas=False):
    a0 = A0H[foot]; ups = UPS_V if ups is None else ups
    Ms = ups * d["LV"]
    Mb = Ms + (max(1.33 * d["MHI"], infall_gas(d)) if gas else 1.33 * d["MHI"])
    rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
    gN = G_SAT * 0.5 * Mb * MSUN_SAT / rh ** 2
    g = a_int(gN, 0.0, a0); fex = 0.0
    if reading != "L":
        Mh = float(halo_mass(UPS_V * d["LV"])) * MCF
        if floor_mh is not None and UPS_V * d["LV"] < 1e5:
            Mh = floor_mh * MCF
        ph, r_e = edge_info(Mb, foot)
        fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
        g += float(extra_acc(reading, rh_pc / 1000.0, g, gN, Mh, fex, r_e, SI_SAT))
    return math.sqrt(g * rh / 3.0) / 1e3, fex


def offs(sample, foot, reading, **kw):
    return np.array([math.log10(d["sig"] / sigma_read(d, foot, reading, **kw)[0]) for d in sample])


def km_median(x, xu):
    y = np.concatenate([-x, -xu]); ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]
    S, n, i = 1.0, len(y), 0
    while i < len(y):
        t = y[i]; j = i; d_ = 0; c_ = 0
        while j < len(y) and y[j] == t:
            d_ += int(ev[j]); c_ += int(not ev[j]); j += 1
        if d_:
            S *= 1.0 - d_ / n
            if S <= 0.5:
                return -t
        n -= d_ + c_; i = j
    return -y[-1]


def boot(x, xu, nb=1000, seed=42):
    rng = np.random.default_rng(seed); v = []
    for _ in range(nb):
        v.append(km_median(x[rng.integers(0, len(x), len(x))], xu[rng.integers(0, len(xu), len(xu))]))
    return float(np.std(v))


def ufd_stat(foot, reading, ups=None, floor_mh=None):
    x = offs(SAMPLES["ufd"], foot, reading, ups=ups, floor_mh=floor_mh)
    xu = np.array([math.log10(d["sig_ul"] / sigma_read(d, foot, reading, ups=ups, floor_mh=floor_mh)[0]) for d in UL])
    return km_median(x, xu), x, xu


FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)
TRACK["lane"] = "P1 ufd"
UF = {}
for foot in FOOTS:
    for rd_ in READ:
        m, x, xu = ufd_stat(foot, rd_)
        err = boot(x, xu)
        ups_var = [ufd_stat(foot, rd_, ups=u)[0] for u in (1.0, 4.0)]
        f_ups = 0.5 * abs(ups_var[1] - ups_var[0])
        flo = [ufd_stat(foot, rd_, floor_mh=fm)[0] for fm in FLOORS] if rd_ != "L" else [m]
        f_mh = 0.5 * (max(flo) - min(flo))
        tot = math.sqrt(err ** 2 + f_ups ** 2 + f_mh ** 2)
        UF[(foot, rd_)] = dict(km=m, resolved_median=float(np.median(x)), err=err, f_ups=f_ups, f_mh=f_mh, tot=tot, z=m / tot, floors=flo)
TRACK["lane"] = "P2 satellites"
CL = {}
for key in ("cls", "col", "m31"):
    for foot in FOOTS:
        for rd_ in READ:
            x = offs(SAMPLES[key], foot, rd_, gas=True)
            ups = [offs(SAMPLES[key], foot, rd_, gas=True, ups=u) for u in (1.0, 4.0)]
            f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
            flo = [float(np.median(offs(SAMPLES[key], foot, rd_, gas=True, floor_mh=fm))) for fm in FLOORS] if rd_ != "L" else [float(np.median(x))]
            err = 1.2533 * float(np.std(x)) / math.sqrt(len(x)); tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
            CL[(key, foot, rd_)] = dict(med=float(np.median(x)), tot=tot, z=float(np.median(x)) / tot,
                                        fex=float(np.median([sigma_read(d, foot, rd_, gas=True)[1] for d in SAMPLES[key]])))

# ================================================================================================ P3 SPARC
NU = lambda y: float(C.nu_mono(np.array([y]))[0])


def sparc_rows(reading, kind):
    rows = []
    for name, m in g10["read_master"]().items():
        Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
        if Ms <= 0 or m["RHI"] <= 0:
            continue
        lm = math.log10(Ms)
        if (kind == "dwarf" and not lm < 10.0) or (kind == "spiral" and lm < 10.0):
            continue
        Mh = (float(halo_mass(Ms)) if kind == "dwarf" else collapse(Ms, "blue" if m["T"] >= 1 else "red")) * MCF
        ph, r_e = edge_info(Mb, "canonical"); fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
        r = m["RHI"]; gb = G_ * Mb * MSUN / (r * KPC) ** 2; gl = NU(gb / A0SI["canonical"]) * gb
        ex = float(extra_acc(reading, r, gl, gb, Mh, fex, r_e))
        rows.append((name, fex, 0.5 * math.log10(1 + ex / gl), lm))
    return rows


TRACK["lane"] = "P3 SPARC"
SP = {}
for kind in ("dwarf", "spiral"):
    for rd_ in READ:
        rows = sparc_rows(rd_, kind); dv = np.array([r_[2] for r_ in rows]); fz = np.array([r_[1] for r_ in rows])
        w = sorted(rows, key=lambda t: -t[2])[:3]
        SP[(kind, rd_)] = dict(n=len(rows), frac_lt003=float(np.mean(dv < 0.03)), max=float(dv.max()), frac_fex0=float(np.mean(fz == 0)),
                               worst=[(a, round(b, 2), round(c, 3)) for a, b, c, d in w])

# ================================================================================================ P4a UGC 2487
TRACK["lane"] = "P4a UGC2487"
UGC = g10["read_master"]()["UGC02487"]
SIG_UGC = math.sqrt((UGC["eVflat"] / UGC["Vflat"] / math.log(10)) ** 2 + (0.5 * 0.1003) ** 2 + (0.25 * 0.2) ** 2)
U2 = {}
for foot in FOOTS:
    for rd_ in READ:
        Ms = 0.61 * UGC["L36"] * 1e9; Mb = Ms + 1.33 * UGC["MHI"] * 1e9
        Mh = collapse(Ms, "blue" if UGC["T"] >= 1 else "red") * MCF
        ph, r_e = edge_info(Mb, foot); fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
        r = UGC["RHI"]; gb = G_ * Mb * MSUN / (r * KPC) ** 2; gl = NU(gb / A0SI[foot]) * gb
        g = gl + float(extra_acc(rd_, r, gl, gb, Mh, fex, r_e))
        vp = math.sqrt(g * r * KPC) / 1e3
        off = math.log10(UGC["Vflat"] / vp)
        U2[(foot, rd_)] = dict(off=off, z=off / SIG_UGC, vpred=vp, fex=fex, dlogv=0.5 * math.log10(g / gl))

# ================================================================================================ P4b DT23
TRACK["lane"] = "P4b DT23"
GALS41, gN41, colour_of, BIAS, DBIAS = g41["GALS"], g41["gN"], g41["colour_of"], g41["BIAS"], g41["DBIAS"]


def pred41(g, foot, reading, model="point", dMs=0.0, dMg=0.0, rfac=1.0):
    a0 = A0SI[foot]; r = g["Rm"] * rfac
    Ms = 10 ** (g["lMs"] + dMs); Mb = Ms + 10 ** (g["lMg"] + dMg)
    gn = gN41(Mb, r, model); gl = NU(gn / a0) * gn; fex = 0.0
    if reading != "L":
        Mh = collapse(Ms, colour_of(g)) * MCF; ph, r_e = edge_info(Mb, foot); fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
        gl += float(extra_acc(reading, r, gl, gn, Mh, fex, r_e))
    return math.sqrt(gl * r * KPC) / 1e3, fex


S0f = lambda g: g["T"] is not None and g["T"] <= 0


def offs41(foot, reading, sel=None, **kw):
    return np.array([math.log10(g["v"] / pred41(g, foot, reading, **kw)[0]) for g in GALS41 if (sel is None or sel(g))])


def stat41(foot, reading, sel=None):
    off = offs41(foot, reading, sel); raw = float(off.mean()); err = float(off.std(ddof=1) / math.sqrt(len(off)))
    mods = [offs41(foot, reading, sel, model=m).mean() for m in ("point", "sphere", "freeman")]; mod = 0.5 * (max(mods) - min(mods))
    ms = 0.5 * abs(offs41(foot, reading, sel, dMs=+0.2).mean() - offs41(foot, reading, sel, dMs=-0.2).mean())
    mg = 0.5 * abs(offs41(foot, reading, sel, dMg=+0.1).mean() - offs41(foot, reading, sel, dMg=-0.1).mean())
    rr = 0.5 * abs(offs41(foot, reading, sel, rfac=1.25).mean() - offs41(foot, reading, sel, rfac=0.75).mean())
    tot = math.sqrt(err ** 2 + mod ** 2 + ms ** 2 + mg ** 2 + rr ** 2 + DBIAS ** 2)
    return dict(n=len(off), raw=raw, corr=raw - BIAS, err=err, mod=mod, ms=ms, mg=mg, rr=rr, tot=tot, z=(raw - BIAS) / tot, per=off.tolist())


DT = {}
for foot in FOOTS:
    for rd_ in READ:
        a = stat41(foot, rd_); s = stat41(foot, rd_, S0f)
        s0err = math.sqrt(np.std(np.array(s["per"]), ddof=1) ** 2 / s["n"] + s["mod"] ** 2 + s["ms"] ** 2 + s["mg"] ** 2 + s["rr"] ** 2 + DBIAS ** 2)
        DT[(foot, rd_)] = dict(all=a, s0=s, s0err=s0err, s0z=s["corr"] / s0err,
                               fex_s0=[pred41(g, foot, rd_)[1] for g in GALS41 if S0f(g)])

# ================================================================================================ P5 SLUGGS
TRACK["lane"] = "P5 SLUGGS"
RES50, sigma_r2, sigma_los, GAMMA, nu_h = g38["RES50"], g38["sigma_r2"], g38["sigma_los"], g38["GAMMA"], g38["nu_h"]
G50, KPC50, MSUN50 = g38["G_"], g38["KPC"], g38["MSUN"]


def sluggs_sigma(r, foot, reading):
    a0 = A0SI[foot]; Ms = r["Mstar"]; a_h = r["Re"] / 1.8153
    Mh = collapse(Ms, "red") * MCF
    ph, r_e = edge_info(Ms, foot); fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))

    def g(rr):
        Mb = Ms * MSUN50 * rr ** 2 / (rr + a_h) ** 2; gN = G50 * Mb / (rr * KPC50) ** 2; gl = gN * nu_h(gN / a0)
        return gl + extra_acc(reading, rr, gl, gN, Mh, fex, r_e, (G50, MSUN50, KPC50))
    return sigma_los(r["Rb"], sigma_r2(g, GAMMA), GAMMA), fex


lms = np.log10([r["Mstar"] for r in RES50])
SL = {}
for foot in FOOTS:
    for rd_ in READ:
        off = np.array([float(np.mean(np.log10(r["Sb"][r["out"]] / sluggs_sigma(r, foot, rd_)[0][r["out"]]))) for r in RES50])
        rng = np.random.default_rng(38)
        sl = lambda y, idx: np.polyfit(lms[idx], y[idx], 1)[0]
        bs = [sl(off, i) for i in (rng.integers(0, len(off), len(off)) for _ in range(2000))]
        s_ = sl(off, np.arange(len(off)))
        SL[(foot, rd_)] = dict(per=off.tolist(), mean=float(off.mean()), err=float(off.std(ddof=1) / math.sqrt(len(off))), z=float(off.mean() / (off.std(ddof=1) / math.sqrt(len(off)))),
                               slope=float(s_), slope_z=float(s_ / np.std(bs)), nfex=sum(sluggs_sigma(r, foot, rd_)[1] > 0 for r in RES50))

# ================================================================================================ P6 X-ray ellipticals
TRACK["lane"] = "P6 X-ray"
GAL, M_hern, M_nfw_h10, RADII = g36["GAL"], g36["M_hern"], g36["M_nfw_h10"], g36["RADII"]


def xray_gal(g, foot, reading, ups="uk", radii=RADII):
    a0 = A0SI[foot]
    Mfit = g["uf"] * g["LK"]; Mdm = max(g["Mvir"] - Mfit, 1e9); Ms = g[ups] * g["LK"]
    Mh = collapse(g["uk"] * g["LK"], "red") * MCF
    ph, r_e = edge_info(Ms, foot); fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
    out = []
    for r in radii:
        Mtot = M_hern(r, Mfit, g["Re"]) + M_nfw_h10(r, Mdm, g["Rvir"], g["c"])
        Mb = M_hern(r, Ms, g["Re"]); gb = G_ * Mb * MSUN / (r * KPC) ** 2; nu = NU(gb / a0)
        ex = float(extra_acc(reading, r, nu * gb, gb, Mh, fex, r_e))
        out.append(math.log10(Mtot / (nu * Mb + ex * (r * KPC) ** 2 / (G_ * MSUN))))
    return float(np.median(out)), fex


def xsample(foot, reading, **kw):
    per = np.array([xray_gal(g, foot, reading, **kw)[0] for g in GAL])
    return dict(per=per, mean=float(per.mean()), err=float(per.std(ddof=1) / math.sqrt(len(per))))


XR = {}
for foot in FOOTS:
    for rd_ in READ:
        b = xsample(foot, rd_); s = xsample(foot, rd_, ups="us"); r4 = xsample(foot, rd_, radii=(5.0, 10.0, 20.0, 40.0))
        tot = math.hypot(b["err"], math.hypot(s["mean"] - b["mean"], r4["mean"] - b["mean"]))
        XR[(foot, rd_)] = dict(mean=b["mean"], tot=tot, z=b["mean"] / tot, per=b["per"].tolist(), fex=[xray_gal(g, foot, rd_)[1] for g in GAL])

# ================================================================================================ P7 Ogle
TRACK["lane"] = "P7 Ogle"
GAL40, gN_disc = g40["GALS"], g40["gN_disc"]


def pred40(g, foot, reading, model="freeman", dMs=0.0, dMg=0.0):
    a0 = A0SI[foot]; Ms = 10 ** (g["lMs"] + dMs); Mb = Ms + 10 ** (g["lMg"] + dMg)
    gn = gN_disc(Mb, g["Rd"], g["r"], model); gl = NU(gn / a0) * gn; fex = 0.0
    if reading != "L":
        col = "blue" if g["lSFR"] - g["lMs"] > -11 else "red"
        Mh = collapse(Ms, col) * MCF; ph, r_e = edge_info(Mb, foot); fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
        gl += float(extra_acc(reading, g["r"], gl, gn, Mh, fex, r_e))
    return math.sqrt(gl * g["r"] * KPC) / 1e3, fex, Mb


def stat40(foot, reading, **kw):
    off = np.array([math.log10(g["v"] / pred40(g, foot, reading, **kw)[0]) for g in GAL40])
    lMb = np.array([math.log10(pred40(g, foot, reading, **kw)[2]) for g in GAL40])
    A = np.vstack([lMb - lMb.mean(), np.ones(len(lMb))]).T
    coef, *_ = np.linalg.lstsq(A, off, rcond=None)
    s2 = float(((off - A @ coef) ** 2).sum() / (len(off) - 2)); se = math.sqrt(s2 / float(((lMb - lMb.mean()) ** 2).sum()))
    fast = np.array([g["v"] > 340 for g in GAL40])
    return dict(off=off, mean=float(off.mean()), err=float(off.std(ddof=1) / math.sqrt(len(off))), slope=float(coef[0]), slope_se=se,
                fast_mean=float(off[fast].mean()), fast_err=float(off[fast].std(ddof=1) / math.sqrt(fast.sum())), nfast=int(fast.sum()))


OG = {}
for foot in FOOTS:
    for rd_ in READ:
        s = stat40(foot, rd_)
        mods = [stat40(foot, rd_, model=mm)["mean"] for mm in ("freeman", "point", "sphere")]; mod = 0.5 * (max(mods) - min(mods))
        ms = 0.5 * abs(stat40(foot, rd_, dMs=+0.2)["mean"] - stat40(foot, rd_, dMs=-0.2)["mean"])
        mg = 0.5 * abs(stat40(foot, rd_, dMg=+0.3)["mean"] - stat40(foot, rd_, dMg=-0.3)["mean"])
        tot = math.sqrt(s["err"] ** 2 + mod ** 2 + ms ** 2 + mg ** 2)
        OG[(foot, rd_)] = dict(mean=s["mean"], tot=tot, z=s["mean"] / tot, zs=s["slope"] / s["slope_se"],
                               zf=s["fast_mean"] / math.hypot(s["fast_err"], math.hypot(mod, math.hypot(ms, mg))), slope=s["slope"], fast_mean=s["fast_mean"])

# ================================================================================================ CONTROLS
R.banner("C1  CONTROLS: (S) and (L) against the lanes' committed results")
J = lambda n: json.load(open(os.path.join(LANES, n)))["numbers"]
c42, c36, c38, c41, c40, c32 = J("CFG42_satellites_rule_results.json"), J("CFG36_colour_split_collapse_results.json"), J("CFG38_sluggs_massive_passive_results.json"), \
    J("CFG41_massive_spirals_hi_results.json"), J("CFG40_super_spirals_results.json"), J("CFG32_xray_ellipticals_under_b_results.json")
devs = []
if not MUTATE:
    for foot in FOOTS:
        for rd_, tag in (("S", "rule"), ("L", "law")):
            devs.append(("CFG42 UF %s %s km" % (foot, tag), abs(UF[(foot, rd_)]["km"] - c42["UF"][f"{foot}|{tag}"]["km"]), 1e-6))
            devs.append(("CFG42 UF %s %s tot" % (foot, tag), abs(UF[(foot, rd_)]["tot"] - c42["UF"][f"{foot}|{tag}"]["tot"]), 1e-6))
            for key in ("cls", "col", "m31"):
                devs.append((f"CFG42 CL {key} {foot} {tag} med", abs(CL[(key, foot, rd_)]["med"] - c42["CL"][f"{key}|{foot}|{tag}"]["med"]), 1e-6))
                devs.append((f"CFG42 CL {key} {foot} {tag} tot", abs(CL[(key, foot, rd_)]["tot"] - c42["CL"][f"{key}|{foot}|{tag}"]["tot"]), 1e-6))
        devs.append((f"CFG36 H1 {foot} mean", abs(XR[(foot, "S")]["mean"] - c36["RES"][foot]["mean"]), 1e-6))
        devs.append((f"CFG36 H1 {foot} tot", abs(XR[(foot, "S")]["tot"] - c36["RES"][foot]["tot"]), 1e-6))
        devs.append((f"CFG32 X-ray law per-galaxy {foot}", float(np.max(np.abs(np.array(XR[(foot, "L")]["per"]) - np.array(c32["RES"][foot]["base"]["per"])))), 1e-6))
        devs.append((f"CFG38 rule {foot} mean", abs(SL[(foot, "S")]["mean"] - c38["RES"][foot]["rule_mean"]), 1e-6))
        devs.append((f"h50 law {foot} per-galaxy", float(np.max(np.abs(np.array(SL[(foot, "L")]["per"]) - np.array(c38["RES"][foot]["law"])))), 5e-3))
        for rd_, tag in (("S", "rule"), ("L", "law")):
            k41 = c41["RES"][f"{foot}|{tag}|all"]
            devs.append((f"CFG41 {foot} {tag} all corr", abs(DT[(foot, rd_)]["all"]["corr"] - k41["corr"]), 1e-6))
            devs.append((f"CFG41 {foot} {tag} all tot", abs(DT[(foot, rd_)]["all"]["tot"] - k41["tot"]), 1e-6))
            devs.append((f"CFG41 {foot} {tag} s0 corr", abs(DT[(foot, rd_)]["s0"]["corr"] - c41["RES"][f"{foot}|{tag}|s0"]["corr"]), 1e-6))
            k40 = c40["RES"][f"{foot}|{tag}"]
            devs.append((f"CFG40 {foot} {tag} mean", abs(OG[(foot, rd_)]["mean"] - k40["mean"]), 1e-6))
            devs.append((f"CFG40 {foot} {tag} tot", abs(OG[(foot, rd_)]["tot"] - k40["tot"]), 1e-6))
    devs.append(("CFG42 H4 dwarfs max", abs(SP[("dwarf", "S")]["max"] - c42["H4"]["max"]), 1e-6))
    devs.append(("CFG42 H4 dwarfs frac<0.03 (all dv < 0.03)", abs(SP[("dwarf", "S")]["frac_lt003"] - c42["H4"]["frac"]), 1e-9))
    devs.append(("CFG36 SPARC>=10 max", abs(SP[("spiral", "S")]["max"] - c36["SPARC"]["max_dlogv"]), 1e-6))
    devs.append(("CFG36 SPARC>=10 f_ex=0 fraction", abs(SP[("spiral", "S")]["frac_fex0"] - c36["SPARC"]["frac_fex0"]), 1e-9))
    worst = max(devs, key=lambda t: t[1] / t[2])
    check("C1 CONTROL: (S) and (L) reproduce the lanes' committed numbers (CFG42 UF/CL/H4, CFG36 H1 & SPARC, CFG32 X-ray law, CFG38, CFG41, CFG40) within 1e-6 (h50's per-galaxy law: 5e-3)",
          f"{len(devs)} comparisons; worst ratio to tolerance {worst[1] / worst[2]:.2e} ({worst[0]}: {worst[1]:.1e})", all(d[1] <= d[2] for d in devs))
else:
    check("C1 CONTROL: skipped in the MUTATE run (the committed numbers are for the unmutated rule)", "-", True, load_bearing=False)

R.banner("C2  CONTROLS: (E) adds nothing inside r_e; every reading adds mass >= 0; the edge phantom equals CFG35's")
mx = max(TRACK["maxratio"].values()) if TRACK["maxratio"] else 0.0; hits = sum(TRACK["hits"].values())
check("C2a CONTROL: reading (E): the largest lane radius / r_e over every lane and footing is < 1 (no lane radius reaches the exterior)",
      f"max r/r_e {mx:.3g}; evaluations with r >= r_e: {hits}; per lane max r/r_e: " + ", ".join(f"{k}: {v:.2g}" for k, v in TRACK["maxratio"].items()), mx < 1.0 and hits == 0)
d_edge = max(abs(edge_info(Mb, f)[0] / edge_phantom36(Mb, f, XE) - 1) for Mb in (1e4, 1e7, 1e9, 1e11) for f in FOOTS)
test = []
for Mb in (1e5, 1e9, 1e11):
    ph, r_e = edge_info(Mb, "canonical"); Mh = 1e11 * MCF
    for r in (0.05, 1.0, 10.0, 100.0):
        gb = G_ * Mb * MSUN / (r * KPC) ** 2; gl = NU(gb / A0SI["canonical"]) * gb
        for rd_ in READ:
            test.append(float(extra_acc(rd_, r, gl, gb, Mh, 0.5, r_e)))
check("C2b CONTROL: the edge phantom computed here equals CFG35's; every reading's added acceleration is >= 0",
      f"max relative difference of the edge phantom {d_edge:.1e}; min added acceleration {min(test):.2e}", d_edge < 1e-9 and min(test) >= 0.0)

# ================================================================================================ the table + acceptance
R.banner("THE TABLE: offsets in sigma as each lane defines them (canonical | alt)")
cf = lambda d, k: f"{d[('canonical', k)]:+.2f}|{d[('alt', k)]:+.2f}"
row = lambda label, fn: P(f"    {label:30s}" + "".join(f"{fn(k):>16s}" for k in READ))
P(f"    {'population (statistic)':30s}" + "".join(f"{k:>16s}" for k in READ))
row("P1 UFD KM median [sigma]", lambda k: f"{UF[('canonical', k)]['z']:+.2f}|{UF[('alt', k)]['z']:+.2f}")
row("   KM median [dex] canonical", lambda k: f"{UF[('canonical', k)]['km']:+.3f}+-{UF[('canonical', k)]['tot']:.3f}")
for key in ("cls", "col", "m31"):
    row(f"P2 {LABEL[key][:24]}", lambda k, key=key: f"{CL[(key, 'canonical', k)]['z']:+.2f}|{CL[(key, 'alt', k)]['z']:+.2f}")
    row(f"   median [dex] canonical", lambda k, key=key: f"{CL[(key, 'canonical', k)]['med']:+.3f}+-{CL[(key, 'canonical', k)]['tot']:.3f}")
for kind, lab in (("dwarf", "P3 SPARC dwarfs (<0.03 dex)"), ("spiral", "P3 SPARC >=10 (<0.03 dex)")):
    row(lab, lambda k, kind=kind: f"{100 * SP[(kind, k)]['frac_lt003']:.0f}% max{SP[(kind, k)]['max']:.3f}")
row("P4a UGC 2487 [sigma]", lambda k: f"{U2[('canonical', k)]['z']:+.2f}|{U2[('alt', k)]['z']:+.2f}")
row("   offset [dex] canonical", lambda k: f"{U2[('canonical', k)]['off']:+.3f}+-{SIG_UGC:.3f}")
row("P4b DT23 four S0 [sigma]", lambda k: f"{DT[('canonical', k)]['s0z']:+.2f}|{DT[('alt', k)]['s0z']:+.2f}")
row("P4b DT23 all 15 [sigma]", lambda k: f"{DT[('canonical', k)]['all']['z']:+.2f}|{DT[('alt', k)]['all']['z']:+.2f}")
row("P5 SLUGGS mean [sigma]", lambda k: f"{SL[('canonical', k)]['z']:+.2f}|{SL[('alt', k)]['z']:+.2f}")
row("   mean [dex] canonical", lambda k: f"{SL[('canonical', k)]['mean']:+.3f}+-{SL[('canonical', k)]['err']:.3f}")
row("P6 X-ray ellipt. [sigma]", lambda k: f"{XR[('canonical', k)]['z']:+.2f}|{XR[('alt', k)]['z']:+.2f}")
row("   mean [dex] canonical", lambda k: f"{XR[('canonical', k)]['mean']:+.3f}+-{XR[('canonical', k)]['tot']:.3f}")
row("P7 Ogle mean [sigma]", lambda k: f"{OG[('canonical', k)]['z']:+.2f}|{OG[('alt', k)]['z']:+.2f}")

ACC = {}
for k in READ:
    a = {}
    a["A1 UFD"] = all(abs(UF[(f, k)]["z"]) < 2 for f in FOOTS)
    a["A2 classical"] = all(CL[(key, f, k)]["z"] > -2 for key in ("cls", "col", "m31") for f in FOOTS)
    a["A3 SPARC"] = SP[("dwarf", k)]["frac_lt003"] >= 0.90 and SP[("spiral", k)]["frac_lt003"] >= 0.90
    a["A4 SLUGGS"] = all(abs(SL[(f, k)]["z"]) < 2 for f in FOOTS)
    a["A5 X-ray"] = all(abs(XR[(f, k)]["z"]) < 2 for f in FOOTS)
    a["A6 UGC2487"] = all(abs(U2[(f, k)]["z"]) < 2 for f in FOOTS)
    a["A7 DT23 S0"] = DT[("canonical", k)]["s0"]["corr"] > -2 * DT[("canonical", k)]["s0err"]
    ACC[k] = a
EXT = {}
for k in READ:
    e = {}
    e["DT23 H2a |mean15|<2s"] = abs(DT[("canonical", k)]["all"]["z"]) < 2
    e["Ogle CFG40-H2"] = abs(OG[("canonical", k)]["z"]) < 2 and abs(OG[("canonical", k)]["zs"]) < 2 and abs(OG[("canonical", k)]["zf"]) < 2
    e["Ogle no change from L"] = abs(OG[("canonical", k)]["mean"] - OG[("canonical", "L")]["mean"]) < 0.03
    e["SPARC>=10 strict max<0.03"] = SP[("spiral", k)]["max"] < 0.03
    EXT[k] = e
R.banner("ACCEPTANCE: which readings pass which gates")
P(f"    {'gate':30s}" + "".join(f"{k:>16s}" for k in READ))
for g_ in ACC["L"]:
    row(g_, lambda k, g_=g_: "pass" if ACC[k][g_] else "FAIL")
row("ALL SEVEN (the conjunction)", lambda k: "PASS" if all(ACC[k].values()) else "no")
P("    -- extended, reported only --")
for g_ in EXT["L"]:
    row(g_, lambda k, g_=g_: "pass" if EXT[k][g_] else "FAIL")
row("conjunction + extended", lambda k: "PASS" if all(ACC[k].values()) and all(EXT[k].values()) else "no")
P("\n    supporting detail (canonical):")
for k in READ:
    P(f"      ({k}) UFD f_ex median {np.median([sigma_read(d, 'canonical', k)[1] for d in SAMPLES['ufd']]):.2f}; classical median f_ex "
      + ", ".join(f"{key} {CL[(key, 'canonical', k)]['fex']:.2f}" for key in ("cls", "col", "m31"))
      + f"; SPARC dwarfs f_ex=0 {100 * SP[('dwarf', k)]['frac_fex0']:.0f}%; spirals f_ex=0 {100 * SP[('spiral', k)]['frac_fex0']:.0f}%; worst spirals {SP[('spiral', k)]['worst']}"
      + f"; UGC2487 v_pred {U2[('canonical', k)]['vpred']:.0f} (V_flat {UGC['Vflat']:.0f}; d log v {U2[('canonical', k)]['dlogv']:+.3f}, f_ex {U2[('canonical', k)]['fex']:.2f});"
      + f" DT23 S0 corrected {DT[('canonical', k)]['s0']['corr']:+.3f} +- {DT[('canonical', k)]['s0err']:.3f}; SLUGGS slope {SL[('canonical', k)]['slope']:+.3f} ({SL[('canonical', k)]['slope_z']:+.1f} sigma);"
      + f" Ogle mean {OG[('canonical', k)]['mean']:+.3f}, slope z {OG[('canonical', k)]['zs']:+.2f}, fast {OG[('canonical', k)]['zf']:+.2f}")

h1 = any(ACC[k]["A1 UFD"] for k in ("S", "M", "E"))
check("H1 [HEADLINE] THE RULE HAS BITE ON THE ULTRA-FAINTS: at least one of (S), (M), (E) passes A1 (|KM median| < 2 sigma, both footings)" + ("  [MUTATE: collapse masses / 100]" if MUTATE else ""),
      "; ".join(f"({k}) {UF[('canonical', k)]['z']:+.2f}/{UF[('alt', k)]['z']:+.2f} sigma" for k in READ), h1)
who = [k for k in READ if all(ACC[k].values())]
check("H2 (reported) which readings satisfy the whole conjunction A1-A7", "readings passing all seven: " + (", ".join(who) if who else "none") + "; per-reading gates passed: "
      + "; ".join(f"({k}) {sum(ACC[k].values())}/7 [fails: {', '.join(g_ for g_, v in ACC[k].items() if not v) or 'none'}]" for k in READ), True, load_bearing=False)
check("C3 CONTROL (MUTATE run only): the UFD gate A1 fails for EVERY reading when every collapse mass is divided by 100",
      "; ".join(f"({k}) A1 {'pass' if ACC[k]['A1 UFD'] else 'FAIL'}" for k in READ), (not any(ACC[k]["A1 UFD"] for k in READ)) if MUTATE else True, load_bearing=MUTATE)

dEL = max(abs(a - b) for f in FOOTS for a, b in zip(SL[(f, "E")]["per"], SL[(f, "L")]["per"]))
dEm = max(abs(SL[(f, "E")]["mean"] - SL[(f, "L")]["mean"]) for f in FOOTS)
check("R1 (reported) does E's exterior shell matter in SLUGGS's Jeans tail?", f"max |E - L| in per-galaxy offsets {dEL:.1e} dex; in the mean {dEm:.1e} dex; SLUGGS z: L "
      + "/".join(f"{SL[(f, 'L')]['z']:+.2f}" for f in FOOTS) + ", E " + "/".join(f"{SL[(f, 'E')]['z']:+.2f}" for f in FOOTS), True, load_bearing=False)
R.num("R1_E_minus_L_SLUGGS", dict(max_per_galaxy=dEL, max_mean=dEm))
R.num("UF", {f"{a}|{b}": v for (a, b), v in UF.items()}); R.num("CL", {f"{a}|{b}|{c}": v for (a, b, c), v in CL.items()})
R.num("SPARC", {f"{a}|{b}": v for (a, b), v in SP.items()}); R.num("UGC2487", {f"{a}|{b}": v for (a, b), v in U2.items()}); R.num("sigma_UGC", SIG_UGC)
R.num("DT23", {f"{a}|{b}": dict(s0z=v["s0z"], s0err=v["s0err"], s0=v["s0"], all={k: v_ for k, v_ in v["all"].items() if k != "per"}, fex_s0=v["fex_s0"]) for (a, b), v in DT.items()})
R.num("SLUGGS", {f"{a}|{b}": v for (a, b), v in SL.items()}); R.num("XRAY", {f"{a}|{b}": v for (a, b), v in XR.items()}); R.num("OGLE", {f"{a}|{b}": v for (a, b), v in OG.items()})
R.num("ACC", ACC); R.num("EXT", EXT); R.num("E_track", TRACK)
nf = R.write(here=OUT)
sys.exit(1 if nf else 0)
