#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG58 -- READINGS (L) AND (S) OF B's COLD-MASS RULE, scored on FIVE POPULATIONS NOT YET SCORED UNDER THE RULE.

WHY.  CFG45 scored four pre-declared readings of B's cold-mass rule on the ultra-faints, the classical satellites, SPARC, UGC 2487, the four Di Teodoro S0,
SLUGGS, the X-ray ellipticals and the Ogle super spirals.  No reading passed all seven gates; the sum (S) was best and failed only the classical satellites
(M31 LVD -2.67 sigma, MW classical -1.8 / -1.9 sigma).  This harness asks the same question of populations the rule has NOT met: where else does the sum add
mass the data do not want (it BREAKS the population), where does it leave the bare law alone (it SPARES it), and where does it help?

THE READINGS (declared; ONLY these two; NO new reading; same definitions as CFG45, same machinery exec'd read-only):
  (L) the bare law (control): g = nu_mono(g_N / a0) g_N, g_N the lane's Newtonian field of the (infall) baryons, isolated.
  (S) the sum as committed (CFG35): g = L + f_ex (1 - f_b) G M_NFW(<r; M_c) / r^2,  f_ex = max(0, 1 - M_phantom,edge / [(1 - f_b) M_c]), the edge at x_e = 0.40
      of r_ta (CFG7's r_ta_law at a = 1, both footings' own a0, nu_mono); Dutton-Maccio NFW; f_b = Omega_b/Omega_m of CFG35.
  Collapse mass M_c for every population below: the Moster+2013 stellar-to-halo relation of CFG35 (h48's halo_mass) at the object's STELLAR mass -- the same
  treatment CFG42 gave the satellites.  THE CLAMP (declared): that function is clamped at M_c = 1e9 Msun for M_* <~ 1.6e4 Msun (its grid floor).  It is NOT reached
  by the Coma UDGs (log M_* 7.70-8.59), DF2/DF4, the tidal dwarfs, or the SPARC galaxies; it IS reached by the faintest Local-Volume dwarfs of the statistic-C
  sample (counted in the output).  Both footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2) everywhere unless stated.  Signs: offset = obs - pred, positive
  = the data sit above the prediction.  'sigma' below = the offset divided by the lane's total error.

THE POPULATIONS, THE STATISTICS (each lane's estimator and error model kept; the lane's data / machinery exec'd read-only) AND THE ACCEPTANCE (declared):
  (a) COMA ULTRA-DIFFUSE GALAXIES -- CFG31 (11 UDGs; L23's data; g_obs = 3 sigma^2 / r_1/2, g_bar = G (M_b/2) / r_1/2^2; the infall gas-to-star ratio drawn per
      galaxy from its 5 nearest members of CFG18's calibration set, non-detections as zero, 2000 realisations, seed 31).  Statistic: the inverse-variance
      weighted mean of log10(g_obs/g_pred) in dex of acceleration.  Error = sqrt(stat^2 + CFG31's recomputed isolated-law floor^2 + realisation spread^2),
      for (S) plus a COLLAPSE-MASS floor: half the range of the (S) mean offset when every M_c is set to x0.1 / x1 / x10 (declared here; CFG31 had no collapse mass).
      (S) adds g_extra at r_1/2 with M_c = Moster(M_* of the UDG), M_b including that realisation's infall gas in f_ex.
      ACCEPT: |offset| < 2 sigma, both footings.  (L) must reproduce CFG31's committed H1 (+0.234 / +0.195 dex, 1.3 / 1.1 sigma).
  (b) NGC 1052-DF2 AND DF4 -- CFG7 / FG001 H6 (class E: formed embedded, no cold component).  TWO treatments, both declared:
      T-E (as FG001 declares, and as the lane scores): no collapse mass exists, so (L) = (S) = the Newtonian prediction, f_ex = 0 by declaration; the lane's
          statistic z_N at 20 Mpc for the central measurements (DF2 Danieli+19, DF4 van Dokkum+19).  ACCEPT: z_N <= 2 for both.  S == L here is a TAUTOLOGY, and is
          reported as such.
      T-B (blind, diagnostic): the readings applied as CFG45 applies them to ANY object, with M_c = Moster(M_* = 2 L_V): (L) = the bare isolated law, (S) = L + the
          added mass, sigma_pred by CFG42's / FG001's estimator (sigma^2 = g r / 3 at r = 4/3 r_half, half the baryons enclosed); the lane's signed z at 20 Mpc.
          ACCEPT (for 'the rule spares it by itself'): |log sigma_S - log sigma_L| < 0.03 dex; the z of L and S are reported.
  (c) THE TIDAL DWARF GALAXIES -- CFG7 / FG041 (the six Lelli+2015 TDGs around NGC 5291 / 7252 / 4694; NOT Milky Way / M31 dwarfs), class E.  T-E: (L) = (S) =
      Newton, statistic chi^2 (6 dof) <= 12.6 (the lane's own kill test), f_ex = 0 by declaration.  T-B (blind): (L) = the bare isolated law (nu_mono, no host
      field), (S) = L + the added mass at R_out with M_c = Moster(M_*), V by the lane's errors (M_bar, R_out propagated).  ACCEPT (spared by the rule itself): the
      largest per-object |log V_S - log V_L| < 0.03 dex (the user's criterion for tidal dwarfs); chi^2 of L and S reported against 12.6.
  (d) THE LOCAL VOLUME DWARFS.  (d1) 'statistic C' (FG001 gate G8 / XR27 Part B / k_contrarian_dwarfefe): the partial slope of log sigma on log(g_e/a0) in the
      quadratic (M_*, r_h) design, N = 92, committed regressor (true external field of the larger host), bootstrap error of the observed (4000, seed 7).  The
      prediction is the same design applied to the model's own log sigma with NO external field (class A / T: isolated): sigma^2 = (2/9) g r_h, g = L or S at r_h
      (KD's estimator; (S) adds the NFW term at r_h; M_c = Moster(2 L_V)).  Signed z = (obs - pred)/err; err for (S) adds the collapse floor (half range of the
      predicted slope over M_c x0.1 / x1 / x10).  ACCEPT: |z| < 2 both footings.  (FG001's G8 takes pred = 0 -> 1.71 sigma; here pred is the computed leakage.)
      (d2) the isolated LV FIELD dwarfs (FG001's `fld`, class T -- the rule DOES apply to them; h43's -0.044 / -0.062 dex): median log10(sigma_obs/sigma_pred), CFG42's
      / CFG45's error model (1.2533 std/sqrt n, Upsilon_V 1 to 4 floor, collapse-mass floor variants 1e8..1e10 for M_* < 1e5 only).  ACCEPT: |median| < 2 sigma, both footings.
  (e) SPARC LOW-SURFACE-BRIGHTNESS galaxies.  THE CUT (declared before the first run): over the SPARC master-table rows with M_* = 0.61 L_3.6 > 0 and R_HI > 0 (the
      rows CFG45's P3 uses), LSB = central disk surface brightness SBdisk (the table's column 'SBdisk', L_sun/pc^2 at 3.6 micron) BELOW the sample median.  Statistic:
      CFG36 / CFG45 P3 exactly (M_* = 0.61 L_3.6, M_gas = 1.33 M_HI, point mass at R_HI, M_c = Moster for log M_* < 10 (CFG42 H4) and the Mandelbaum+2016 blue (T >= 1) /
      red (T <= 0) M_200c relation for log M_* >= 10 (CFG36 H2)): d log v = 0.5 log10(g_S / g_L) at R_HI, and f_ex.
      ACCEPT (E1, the CFG45 A3 / CFG42 H4 criterion): d log v < 0.03 dex in >= 90% of the LSB galaxies, both footings.  REPORTED: (E2) CFG36's strict clause (f_ex = 0 in
      >= 90% AND max d log v < 0.03); (E3) the DATA offset log10(V_flat / v_pred(R_HI)) of the LSB galaxies with V_flat > 0, median, error = sqrt((1.2533 std/sqrt n)^2
      + (0.25 x 0.2)^2) (the UGC 2487 lane's M_* term), |median| < 2 sigma; the HSB complement, for contrast.

WHICH POPULATION IS 'BROKEN' / 'SPARED' (declared classification, by the population's gate above): BREAKS = L passes and S fails; FIXES = L fails and S passes; SPARES
  = both pass and the change of the population's statistic < 0.03 dex; MOVES = both pass and the change > 0.03 dex; BOTH FAIL = neither passes.  The change is in dex of
  the population's own observable: (a) |mean_S - mean_L| / 2 (acceleration -> dispersion); (d2) |median_S - median_L| in log sigma; (e) the median of d log v over the
  LSB galaxies; (b), (c): T-E 0 by declaration, T-B the largest |log ratio| of the predicted sigma / V.  (d1) is a slope: reported as Delta slope.

CONTROLS
  C1  CONTROL  (L) reproduces the committed numbers: CFG31 H1 (mean and total error, both footings), CFG7 H6's z_N (15 rows) and CFG7 FG041's chi^2_Newton and
               chi^2_iso (nu_mono), XR27's observed statistic C (obs and err, both footings), FG001's committed isolated field-dwarf medians, and CFG45's SPARC P3
               numbers for (S) when the LSB cut is removed -- all to 1e-6 (statistic C's observed to 1e-9).
  C2  CONTROL  (S) is a strict addition: with every M_c set to ~0 (f_ex = 0) the (S) prediction equals (L) for the UDGs, the TDGs and the LV dwarfs; the added acceleration is
               >= 0; the edge phantom computed here equals CFG35's.
  C3  CONTROL  (MUTATE=1: every collapse mass divided by 100): (S) must equal (L) -- every population's change < 0.01 dex (Delta slope < 0.01) -- because f_ex -> 0.
  H1  [HEADLINE; MUTATE must fail] the sum changes at least one scored population by > 0.05 dex (in the units of the classification above; T-E rows count 0).
  H2  (reported) the table and the classification.
MUTATE=1: collapse masses / 100 for every S evaluation -- H1 must FAIL (rc = 1).
ADDED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed): control C1 FAILED on XR27's statistic-C observed slope, alt footing (4.8e-9 against a tolerance of 1e-9): the
  campaign footing C.A0_SI is FP0's ROUNDED pair, XR27 used FP0's exact values.  C1 is kept as a FAIL (tolerance unchanged); a reported diagnostic C1b (exact footing, CFG4's A0) was
  added and C1's detail now lists every comparison over tolerance.  No reading, statistic, gate or threshold changed.
  ALSO ADDED after the first main run, before interpretation (all REPORTED, none gates): R1 the field-dwarf (S) median in units of (L)'s total error (because (S) shrinks the scatter of the
  13 dwarfs from 0.124 to 0.077 dex and so its own error); R2 the baryonic mass above which (S) switches itself off (f_ex = 0), against each population's baryonic masses; and the
  statistic-C row is labelled 'slope population' in the classification instead of carrying a dex change of 0.
Nothing here says the theory is closed; a population the sum passes is a population it has not yet failed, and a failure is a valid result.
Run: python3 CFG58_rule_more_populations.py   (MUTATE=1 for the control; CFG58_OUT=<dir> to choose where the outputs go)
"""
import os, sys, math, io, contextlib, csv, json
import numpy as np
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_GUESS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LANES = HERE if os.path.exists(os.path.join(HERE, "CFG7_common.py")) else os.path.join(REPO_GUESS, "campaign_fresh_gravity")
OUT = os.environ.get("CFG58_OUT", HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG58_rule_more_populations", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass / 100 -- S must equal L; H1 must FAIL ***")
MCF = 0.01 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
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
g31 = exec_prefix("CFG31_coma_udgs_under_b.py", BAR + "H1")
gt = exec_prefix("CFG7_tdg_fg041.py", BAR + "H1 Newton")
FB, nfw_enclosed, collapse_raw, edge_phantom36 = g36["FB"], g36["nfw_enclosed"], g36["collapse"], g36["edge_phantom"]
G_, KPC, MSUN, A0SI, RHO_C = g36["G_"], g36["KPC"], g36["MSUN"], g36["A0SI"], g36["RHO_C"]
g10, halo_mass = g36["g10"], g35["halo_mass"]
collapse = lru_cache(maxsize=None)(lambda Ms, colour: collapse_raw(Ms, colour))
NU = lambda y: float(C.nu_mono(np.array([y]))[0])
J = lambda p, n="numbers": json.load(open(os.path.join(p, n)))
J_CAMP = lambda n: json.load(open(os.path.join(LANES, n)))["numbers"]

# ------------------------------------------------------------------------------------------------ the edge (CFG45's, line for line)
_EDGE = {}


def edge_info(Mb, foot):
    k = (float(Mb), foot)
    if k not in _EDGE:
        a0 = C.A0[foot]; rta = C.r_ta_law(Mb, a0, C.nu_mono, 1.0)
        _EDGE[k] = (float(C.M_law(Mb, XE * rta, a0, C.nu_mono)) - Mb, XE * rta * 1000.0)
    return _EDGE[k]


def fex_of(Mb, Mh, foot):
    ph, _ = edge_info(Mb, foot)
    return max(0.0, 1.0 - ph / ((1 - FB) * Mh))


CLAMP = {"n": 0, "of": 0}


def moster(Ms, tag=None):
    CLAMP["of"] += 1
    if Ms < 1.6e4:
        CLAMP["n"] += 1
    return float(halo_mass(Ms))


# ================================================================================================ (a) Coma UDGs
UDG, NAMES = g31["UDG"], g31["NAMES"]
MST, R12, GOBS0, ERR, W, STAT = g31["MST"], g31["R12"], g31["GOBS0"], g31["ERR"], g31["W"], g31["STAT"]
GU, MSU, FLOOR31, RZ = g31["G_"], g31["MSUN"], g31["FLOOR"], g31["RZ"]
A0B = C.A0_SI
KPC_M = 3.0856775814913673e19


def udg_off(foot, reading, mcx=1.0):
    """(N, n) offsets log10(g_obs/g_pred) [dex acc], and the f_ex array; reading L or S; mcx multiplies every M_c (the collapse floor)."""
    a0 = A0B[foot]; n = len(UDG); off = np.zeros(RZ.shape); fx = np.zeros(RZ.shape)
    for j in range(n):
        uq, inv = np.unique(RZ[:, j], return_inverse=True)
        vv, ff = [], []
        for rq in uq:
            mb = MST[j] * (1.0 + rq)
            gb = GU * (mb / 2.0) / R12[j] ** 2; gl = float(C.nu_mono(np.array([gb / a0]))[0]) * gb
            ex, fex = 0.0, 0.0
            if reading == "S":
                Mh = moster(MST[j] / MSU) * MCF * mcx
                fex = fex_of(mb / MSU, Mh, foot)
                ex = fex * (1 - FB) * float(nfw_enclosed(Mh, R12[j] / KPC_M)) * MSU * GU / R12[j] ** 2
            vv.append(math.log10(GOBS0[j]) - math.log10(gl + ex)); ff.append(fex)
        off[:, j] = np.array(vv)[inv]; fx[:, j] = np.array(ff)[inv]
    return off, fx


wm = lambda o: np.sum(W * o, axis=-1) / W.sum()
UD = {}
for foot in FOOTS:
    for rd_ in ("L", "S"):
        off, fx = udg_off(foot, rd_)
        m = wm(off); spread = float(np.std(m))
        flo = FLOOR31[foot]["total"]
        cf = 0.0
        if rd_ == "S":
            v3 = [float(wm(udg_off(foot, "S", mcx=x)[0]).mean()) for x in (0.1, 1.0, 10.0)]
            cf = 0.5 * (max(v3) - min(v3))
        tot = math.sqrt(STAT ** 2 + flo ** 2 + spread ** 2 + cf ** 2); tot0 = math.sqrt(STAT ** 2 + flo ** 2 + spread ** 2)
        UD[(foot, rd_)] = dict(mean=float(m.mean()), spread=spread, floor=flo, collapse_floor=cf, tot=tot, z=float(m.mean()) / tot, z_nofloor=float(m.mean()) / tot0,
                               fex_median=float(np.median(np.median(fx, axis=0))), fex_per=[float(np.median(fx[:, j])) for j in range(len(UDG))],
                               per_gal_mean=[float(x) for x in off.mean(axis=0)])

# ================================================================================================ (b) DF2 / DF4
LV_DF = {"NGC1052-DF2": (1.1e8, 2200.0 * 0.75), "NGC1052-DF4": (1.0e8, 1600.0 * 0.75)}
OBS_DF = {"NGC1052-DF2": [("Danieli19", 8.5, 3.1, 2.3), ("Emsellem19", 10.8, 4.0, 3.2), ("u02 (8.5+-2.3)", 8.5, 2.3, 2.3)],
          "NGC1052-DF4": [("vanDokkum19", 4.2, 2.2, 4.4), ("u02 (4.2+-1.5)", 4.2, 1.5, 1.5)]}
sigma_read_ref = None


def sig_of(B, sig, em, ep):
    e = em if B > 0 else ep
    return abs(B) / (2.0 * e / (sig * math.log(10)))


def zsigned(s, sp, em, ep):
    B = 2.0 * math.log10(s / sp)
    return math.copysign(sig_of(B, s, em, ep), B) if B != 0 else 0.0


# CFG42's estimator (FG001's) with the reading switch, line for line as CFG45's sigma_read (P1/P2)
SAMPLES, UL, LABEL, A0H, UPS_V, a_int, infall_gas = (g42[k] for k in ("SAMPLES", "UL", "LABEL", "A0H", "UPS_V", "a_int", "infall_gas"))
G_SAT, MSUN_SAT = g42["G"], g42["Msun"]
SI_SAT = (g42["G"], g42["Msun"], 1000.0 * 3.0857e16)


def sigma_read(d, foot, reading, ups=None, floor_mh=None, mcx=1.0):
    a0 = A0H[foot]; ups = UPS_V if ups is None else ups
    Ms = ups * d["LV"]
    Mb = Ms + 1.33 * d["MHI"]
    rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
    gN = G_SAT * 0.5 * Mb * MSUN_SAT / rh ** 2
    g = a_int(gN, 0.0, a0); fex = 0.0
    if reading == "S":
        Mh = moster(UPS_V * d["LV"]) * MCF * mcx
        if floor_mh is not None and UPS_V * d["LV"] < 1e5:
            Mh = floor_mh * MCF
        fex = fex_of(Mb, Mh, foot)
        g += G_SAT * fex * (1 - FB) * float(nfw_enclosed(Mh, rh_pc / 1000.0)) * MSUN_SAT / rh ** 2
    return math.sqrt(g * rh / 3.0) / 1e3, fex


DF = {}
for nm, (lv, rhp) in LV_DF.items():
    for (on, s, em, ep) in OBS_DF[nm]:
        for dist in (13.0, 20.0, 22.1):
            f_ = dist / 20.0
            Mb = 2.0 * lv * f_ ** 2; rh = (4.0 / 3.0) * rhp * f_
            sN = math.sqrt(G_SAT * (0.5 * Mb * MSUN_SAT) / (3 * rh * 3.0857e16)) / 1e3
            row = dict(sig_N=sN, z_N=sig_of(2 * math.log10(s / sN), s, em, ep))
            d = dict(LV=lv * f_ ** 2, rh=rhp * f_, MHI=0.0)
            for foot in FOOTS:
                sL, _ = sigma_read(d, foot, "L"); sS, fx = sigma_read(d, foot, "S")
                row[foot] = dict(sig_L=sL, sig_S=sS, zL=zsigned(s, sL, em, ep), zS=zsigned(s, sS, em, ep), fex=fx, dlog=math.log10(sS / sL),
                                 Mh=moster(2.0 * lv * f_ ** 2) * MCF)
            DF[(nm, on, dist)] = row

# ================================================================================================ (c) tidal dwarfs
rowsT, F_ = gt["rows"], gt["F"]
ACCF = gt["ACC"]; V_OBS_T = gt["V_OBS"]


def tdg_fn(reading, foot, mcx=1.0):
    a0 = A0SI[foot]

    def fn(r, Mb, Ro):
        vL = gt["v_pred"](r, a0, C.nu_mono, efe=False, Mbar=Mb, Rout=Ro)
        if reading == "L":
            return vL
        Ms = F_(r, "M_star_1e8") * 1e8
        Mh = moster(Ms) * MCF * mcx
        fex = fex_of(Mb, Mh, foot)
        ex = fex * (1 - FB) * float(nfw_enclosed(Mh, Ro)) * MSUN * G_ / (Ro * KPC) ** 2
        return math.sqrt(vL ** 2 + ex / ACCF * Ro)
    return fn


TD = {}
chiN_T, _rowsN = gt["chi2_of"](lambda r, Mb, Ro: gt["v_newton"](r, Mb, Ro))
for foot in FOOTS:
    for rd_ in ("L", "S"):
        chi, det = gt["chi2_of"](tdg_fn(rd_, foot))
        vs = [d_[1] for d_ in det]
        TD[(foot, rd_)] = dict(chi2=chi, v=vs)
    dl = [abs(math.log10(a / b)) for a, b in zip(TD[(foot, "S")]["v"], TD[(foot, "L")]["v"])]
    a0 = A0SI[foot]
    fx = []
    for i, r in enumerate(rowsT):
        Mh = moster(F_(r, "M_star_1e8") * 1e8) * MCF
        fx.append(fex_of(gt["MB"][i], Mh, foot))
    TD[(foot, "dlog")] = dl; TD[(foot, "fex")] = fx

# ================================================================================================ (d) Local Volume dwarfs
import k_contrarian_dwarfefe as KD
KDd = KD.load(ups_v=2.0)
lsig = np.log10(np.array([g["sig"] for g in KDd])); lM = np.log10(np.array([g["Mb"] for g in KDd]))
lrh = np.log10(np.array([g["rh"] / KD.PC for g in KDd])); gNe0 = np.array([g["gNe"] for g in KDd])
DW_OBS = {}
for foot in FOOTS:
    a0 = A0B[foot]; lge = np.log10(KD.true_external_field(gNe0, a0) / a0)
    q = [lM, lrh, lM * lM, lrh * lrh, lM * lrh, lge]
    cobs, _ = KD.partial_slope(lsig, q); eobs = KD.boot_slope(lsig, q)
    DW_OBS[foot] = (q, float(cobs), float(eobs))


def sigma_C(foot, reading, mcx=1.0, kern=None):
    a0 = A0B[foot]; out = []; fx = []
    for g in KDd:
        Mb = g["Mb"] * KD.MSUN; rh = g["rh"]
        gN = KD.G * Mb / rh ** 2
        gl = (float(C.nu_mono(np.array([gN / a0]))[0]) if kern is None else float(kern(np.array([gN / a0]))[0])) * gN
        ex, fex = 0.0, 0.0
        if reading == "S":
            Mh = moster(2.0 * g["LV"]) * MCF * mcx
            fex = fex_of(g["Mb"], Mh, foot)
            ex = fex * (1 - FB) * float(nfw_enclosed(Mh, rh / KD.KPC)) * KD.MSUN * KD.G / rh ** 2
        out.append(math.sqrt((2.0 / 9.0) * (gl + ex) * rh) / 1e3); fx.append(fex)
    return np.array(out), np.array(fx)


D1 = {}
for foot in FOOTS:
    q, cobs, eobs = DW_OBS[foot]
    for rd_ in ("L", "S"):
        sp, fx = sigma_C(foot, rd_)
        pred = float(KD.partial_slope(np.log10(sp), q)[0])
        cf = 0.0
        if rd_ == "S":
            v3 = [float(KD.partial_slope(np.log10(sigma_C(foot, "S", mcx=x)[0]), q)[0]) for x in (0.1, 1.0, 10.0)]
            cf = 0.5 * (max(v3) - min(v3))
        tot = math.sqrt(eobs ** 2 + cf ** 2)
        D1[(foot, rd_)] = dict(obs=cobs, err=eobs, pred=pred, cf=cf, tot=tot, z=(cobs - pred) / tot, z_nofloor=(cobs - pred) / eobs, fex_median=float(np.median(fx)),
                               n_fex_pos=int((fx > 0).sum()), n=len(KDd))
FLD = g42["ns"]["fld"]


def offs_fld(foot, reading, **kw):
    return np.array([math.log10(d["sig"] / sigma_read(d, foot, reading, **kw)[0]) for d in FLD])


FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)
D2 = {}
for foot in FOOTS:
    for rd_ in ("L", "S"):
        x = offs_fld(foot, rd_)
        ups = [offs_fld(foot, rd_, ups=u) for u in (1.0, 4.0)]
        f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
        flo = [float(np.median(offs_fld(foot, rd_, floor_mh=fm))) for fm in FLOORS] if rd_ == "S" else [float(np.median(x))]
        err = 1.2533 * float(np.std(x)) / math.sqrt(len(x)); tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
        D2[(foot, rd_)] = dict(med=float(np.median(x)), tot=tot, z=float(np.median(x)) / tot, n=len(x),
                               fex=float(np.median([sigma_read(d, foot, rd_)[1] for d in FLD])), per=x.tolist())

# ================================================================================================ (e) SPARC LSB
SPR = []
for name, m in g10["read_master"]().items():
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
    if Ms <= 0 or m["RHI"] <= 0:
        continue
    SPR.append(dict(name=name, Ms=Ms, Mb=Mb, lm=math.log10(Ms), T=m["T"], SB=m["SBdisk"], RHI=m["RHI"], Vf=m["Vflat"], eV=m["eVflat"]))
SB_MED = float(np.median([s["SB"] for s in SPR]))
for s in SPR:
    s["lsb"] = s["SB"] < SB_MED
    s["dwarf"] = s["lm"] < 10.0


def sparc_eval(s, foot, reading):
    Mh = (moster(s["Ms"]) if s["dwarf"] else collapse(s["Ms"], "blue" if s["T"] >= 1 else "red")) * MCF
    fex = fex_of(s["Mb"], Mh, foot)
    r = s["RHI"]; gb = G_ * s["Mb"] * MSUN / (r * KPC) ** 2; gl = NU(gb / A0SI[foot]) * gb
    ex = fex * (1 - FB) * float(nfw_enclosed(Mh, r)) * MSUN * G_ / (r * KPC) ** 2 if reading == "S" else 0.0
    return fex, 0.5 * math.log10(1 + ex / gl), math.sqrt((gl + ex) * r * KPC) / 1e3


SP = {}
for foot in FOOTS:
    for s in SPR:
        s[("S", foot)] = sparc_eval(s, foot, "S"); s[("L", foot)] = sparc_eval(s, foot, "L")


def sp_stats(sel, foot):
    rows = [s for s in SPR if sel(s)]
    dv = np.array([s[("S", foot)][1] for s in rows]); fz = np.array([s[("S", foot)][0] for s in rows])
    out = dict(n=len(rows), frac_lt003=float(np.mean(dv < 0.03)), max=float(dv.max()), median=float(np.median(dv)), frac_fex0=float(np.mean(fz == 0)),
               worst=[(s["name"], round(s[("S", foot)][0], 2), round(s[("S", foot)][1], 3), round(s["lm"], 2)) for s in sorted(rows, key=lambda t: -t[("S", foot)][1])[:3]])
    dat = {}
    vr = [s for s in rows if s["Vf"] > 0]
    for rd_ in ("L", "S"):
        o = np.array([math.log10(s["Vf"] / s[(rd_, foot)][2]) for s in vr])
        err = math.sqrt((1.2533 * float(np.std(o)) / math.sqrt(len(o))) ** 2 + (0.25 * 0.2) ** 2)
        dat[rd_] = dict(med=float(np.median(o)), err=err, z=float(np.median(o)) / err, n=len(o))
    out["data"] = dat
    return out


LSBf = lambda s: s["lsb"]
SETS = {"LSB": LSBf, "LSB dwarf (M*<1e10)": lambda s: s["lsb"] and s["dwarf"], "LSB massive (M*>=1e10)": lambda s: s["lsb"] and not s["dwarf"],
        "HSB (complement)": lambda s: not s["lsb"]}
for foot in FOOTS:
    for k, sel in SETS.items():
        SP[(foot, k)] = sp_stats(sel, foot)

# ================================================================================================ CONTROLS
R.banner("C1  CONTROLS: (L) against the committed numbers")
devs = []
c31 = J_CAMP("CFG31_coma_udgs_under_b_results.json")["RES"]
for foot in FOOTS:
    k = c31[f"{foot}|infall gas, non-detections zero"]
    devs.append((f"CFG31 H1 {foot} mean", abs(UD[(foot, "L")]["mean"] - k["mean"]), 1e-6))
    devs.append((f"CFG31 H1 {foot} tot", abs(UD[(foot, "L")]["tot"] - k["tot"]), 1e-6))
c7 = J_CAMP("CFG7_hierarchy_fg001_results.json")["H6"]
for (nm, on, dist), v in DF.items():
    devs.append((f"CFG7 H6 z_N {nm} {on} {dist:g}", abs(v["z_N"] - c7[f"{nm}|{on}|{dist}"]["z_N"]), 1e-6))
c41 = J_CAMP("CFG7_tdg_fg041_results.json")
devs.append(("FG041 chi2 Newton", abs(chiN_T - c41["H1"]["chi2_newton"]), 1e-6))
for foot in FOOTS:
    devs.append((f"FG041 chi2 isolated nu_mono {foot}", abs(TD[(foot, "L")]["chi2"] - c41["H2"][f"{foot}|nu_mono"]["chi_iso"]), 1e-6))
x27 = json.load(open(os.path.join(C.REPO, "real_research", "cross_thread_review_2026_09_26", "XR27_efe_disfavouring_results.json")))["numbers"]["dwarfs"]["inf"]["rows"]
for foot in FOOTS:
    devs.append((f"XR27 stat C obs {foot}", abs(DW_OBS[foot][1] - x27[f"{foot}/1.0"]["obs"]), 1e-9))
    devs.append((f"XR27 stat C err {foot}", abs(DW_OBS[foot][2] - x27[f"{foot}/1.0"]["err"]), 1e-9))
FG = json.load(open(os.path.join(LANES, "CFG7_hierarchy_fg001_results.json")))["numbers"]
for foot in FOOTS:
    devs.append((f"FG001 field-dwarf isolated median {foot}", abs(D2[(foot, "L")]["med"] - FG["SAT"][f"{foot}|field"]["med_iso"]), 1e-9))
c45 = J_CAMP("CFG45_rule_readings_results.json")["SPARC"]
for kind, tag in (("dwarf", "dwarf|S"), ("spiral", "spiral|S")):
    sel = (lambda s: s["dwarf"]) if kind == "dwarf" else (lambda s: not s["dwarf"])
    dv = np.array([s[("S", "canonical")][1] for s in SPR if sel(s)]); fz = np.array([s[("S", "canonical")][0] for s in SPR if sel(s)])
    if not MUTATE:
        devs.append((f"CFG45 SPARC {kind} n", abs(len(dv) - c45[tag]["n"]), 0.0))
        devs.append((f"CFG45 SPARC {kind} max dlogv", abs(float(dv.max()) - c45[tag]["max"]), 1e-6))
        devs.append((f"CFG45 SPARC {kind} frac<0.03", abs(float(np.mean(dv < 0.03)) - c45[tag]["frac_lt003"]), 1e-9))
        devs.append((f"CFG45 SPARC {kind} f_ex=0", abs(float(np.mean(fz == 0)) - c45[tag]["frac_fex0"]), 1e-9))
worst = max(devs, key=lambda t: t[1] / t[2] if t[2] > 0 else (1e30 if t[1] > 0 else 0.0))
bad = [d for d in devs if d[1] > d[2]]
check("C1 CONTROL: (L) reproduces CFG31 H1, CFG7 H6 (15 rows), FG041's chi^2, XR27's statistic-C observed, FG001's field-dwarf median; the SPARC (S) numbers reproduce CFG45's P3 (LSB cut removed)",
      f"{len(devs)} comparisons; worst deviation {worst[0]}: {worst[1]:.1e} (tolerance {worst[2]:.0e}); over tolerance: " + ("; ".join(f"{a} {b:.1e}" for a, b, c in bad) if bad else "none"), not bad)
# ADDED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed; C1's tolerance unchanged, its FAIL is kept): a diagnostic for why C1 failed -- the campaign footing
# C.A0_SI is the ROUNDED FP0 pair (CFG4_common asserts |A0 - rounded| < 1e-15, i.e. up to 1e-5 relative), XR27's chain uses FP0's exact values.
_d = []
for foot in FOOTS:
    a0x = C.C4.A0[foot]; lgex = np.log10(KD.true_external_field(gNe0, a0x) / a0x)
    qx = [lM, lrh, lM * lM, lrh * lrh, lM * lrh, lgex]
    _d.append(abs(float(KD.partial_slope(lsig, qx)[0]) - x27[f"{foot}/1.0"]["obs"]))
check("C1b (reported diagnostic, added after the first run) statistic C's observed slope with FP0's EXACT footing (CFG4's A0) reproduces XR27's committed to 1e-12",
      f"max |d| {max(_d):.1e}; with the rounded campaign footing the deviation is at the 1e-9..1e-8 level (against an error of 0.047)", max(_d) < 1e-12, load_bearing=False)

R.banner("C2  CONTROLS: (S) is a strict addition; the edge phantom equals CFG35's; the clamp")
dS = []
save_m = MCF
MCF = 1e-30                                                 # f_ex = 0 for everything: (S) must equal (L)
for foot in FOOTS:
    dS.append(("UDG", float(np.max(np.abs(udg_off(foot, "S")[0] - udg_off(foot, "L")[0])))))
    _vS = [d_[1] for d_ in gt["chi2_of"](tdg_fn("S", foot))[1]]; _vL = [d_[1] for d_ in gt["chi2_of"](tdg_fn("L", foot))[1]]
    dS.append(("TDG", max(abs(a - b) for a, b in zip(_vS, _vL))))
    dS.append(("LV stat C", float(np.max(np.abs(sigma_C(foot, "S")[0] - sigma_C(foot, "L")[0])))))
    dS.append(("LV field dwarfs", max(abs(sigma_read(d, foot, "S")[0] - sigma_read(d, foot, "L")[0]) for d in FLD)))
MCF = save_m
d_edge = max(abs(edge_info(Mb, f)[0] / edge_phantom36(Mb, f, XE) - 1) for Mb in (1e4, 1e7, 1e9, 1e11) for f in FOOTS)
nonneg = min(float(nfw_enclosed(Mh, r)) for Mh in (1e9, 1e11, 1e13) for r in (0.1, 1.0, 10.0))
check("C2 CONTROL: with every M_c ~ 0 (f_ex = 0) the (S) prediction equals (L) for the UDGs, TDGs, LV dwarfs and field dwarfs; the added mass is >= 0; the edge phantom equals CFG35's",
      f"max |S - L| at M_c ~ 0: " + ", ".join(f"{a} {b:.1e}" for a, b in dS[:4]) + f"; edge phantom {d_edge:.1e}; min NFW mass {nonneg:.2e}",
      max(b for a, b in dS) <= 1e-9 and d_edge < 1e-9 and nonneg >= 0.0)
nmin = {"UDG": float(np.min(np.log10(MST / MSU))), "TDG": float(np.log10(min(F_(r, "M_star_1e8") for r in rowsT) * 1e8)),
        "LV stat-C": float(np.log10(2.0 * min(g["LV"] for g in KDd))), "field": float(np.log10(UPS_V * min(d["LV"] for d in FLD))),
        "SPARC": float(min(s["lm"] for s in SPR))}
nclamp = sum(1 for g in KDd if 2.0 * g["LV"] < 1.6e4)
P(f"    the Moster clamp (M_c = 1e9 for M_* < 1.6e4): smallest log M_* by population {nmin}; LV statistic-C dwarfs at the clamp: {nclamp} of {len(KDd)}")
R.num("clamp", dict(min_logMs=nmin, lv_statC_at_clamp=nclamp))

# ================================================================================================ the table
R.banner("THE TABLE: offsets in sigma, (L) | (S), canonical | alt  (positive = data above the prediction)")
zz = lambda d, k, rd: f"{d[('canonical', rd)][k]:+.2f}|{d[('alt', rd)][k]:+.2f}"
P(f"    {'population (statistic)':46s}{'L':>16s}{'S':>16s}   f_ex (S)             change L->S")
ch = {}
ch["a"] = max(abs(UD[(f, 'S')]['mean'] - UD[(f, 'L')]['mean']) / 2.0 for f in FOOTS)
P(f"    {'(a) Coma UDGs, weighted mean [sigma]':46s}{zz(UD, 'z', 'L'):>16s}{zz(UD, 'z', 'S'):>16s}   median {UD[('canonical', 'S')]['fex_median']:.2f}/{UD[('alt', 'S')]['fex_median']:.2f}"
  f"      {ch['a']:.3f} dex sigma")
P(f"    {'    mean [dex acc] canonical, +- total':46s}{UD[('canonical', 'L')]['mean']:+.3f}+-{UD[('canonical', 'L')]['tot']:.3f} {UD[('canonical', 'S')]['mean']:+.3f}+-{UD[('canonical', 'S')]['tot']:.3f}"
  f"   (S without the collapse floor: {UD[('canonical', 'S')]['z_nofloor']:+.2f}|{UD[('alt', 'S')]['z_nofloor']:+.2f} sigma; floor {UD[('canonical', 'S')]['collapse_floor']:.3f})")
zdf = lambda nm, on, foot, rd: DF[(nm, on, 20.0)][foot][f"z{rd}"]
for nm, on in (("NGC1052-DF2", "Danieli19"), ("NGC1052-DF4", "vanDokkum19")):
    v = DF[(nm, on, 20.0)]
    P(f"    {'(b) ' + nm[-3:] + ' T-E (Newton; S==L by declaration) [z_N]':46s}{v['z_N']:>+16.2f}{v['z_N']:>+16.2f}   0 (declared)          0 (tautology)")
    zl = f"{v['canonical']['zL']:+.2f}|{v['alt']['zL']:+.2f}"; zs_ = f"{v['canonical']['zS']:+.2f}|{v['alt']['zS']:+.2f}"
    P(f"    {'    ' + nm[-3:] + ' T-B blind: bare law | sum [sigma]':46s}{zl:>16s}{zs_:>16s}   f_ex {v['canonical']['fex']:.2f}/{v['alt']['fex']:.2f}"
      f"           {max(abs(v['canonical']['dlog']), abs(v['alt']['dlog'])):.3f} dex")
P(f"    {'(c) tidal dwarfs T-E: chi^2 Newton (6 dof)':46s}{chiN_T:>16.2f}{chiN_T:>16.2f}   0 (declared)          0 (tautology)")
P(f"    {'    T-B blind: chi^2 bare law | sum (can|alt)':46s}" + f"{TD[('canonical', 'L')]['chi2']:.1f}|{TD[('alt', 'L')]['chi2']:.1f}".rjust(16)
  + f"{TD[('canonical', 'S')]['chi2']:.1f}|{TD[('alt', 'S')]['chi2']:.1f}".rjust(16) + f"   f_ex med {np.median(TD[('canonical', 'fex')]):.2f}/{np.median(TD[('alt', 'fex')]):.2f}"
  f"   max {max(max(TD[('canonical', 'dlog')]), max(TD[('alt', 'dlog')])):.3f} dex")
P(f"    {'(d1) LV dwarfs, statistic C [sigma]':46s}{zz(D1, 'z', 'L'):>16s}{zz(D1, 'z', 'S'):>16s}   f_ex>0 in {D1[('canonical', 'S')]['n_fex_pos']}/{D1[('canonical', 'S')]['n']}"
  f"       d slope {max(abs(D1[(f, 'S')]['pred'] - D1[(f, 'L')]['pred']) for f in FOOTS):.4f}")
P(f"    {'    obs +- err | pred L | pred S (canonical)':46s}{D1[('canonical', 'L')]['obs']:+.4f}+-{D1[('canonical', 'L')]['err']:.4f}   L {D1[('canonical', 'L')]['pred']:+.4f}   S {D1[('canonical', 'S')]['pred']:+.4f}"
  f" (S without collapse floor: {D1[('canonical', 'S')]['z_nofloor']:+.2f}|{D1[('alt', 'S')]['z_nofloor']:+.2f} sigma)")
ch["d2"] = max(abs(D2[(f, 'S')]['med'] - D2[(f, 'L')]['med']) for f in FOOTS)
P(f"    {'(d2) LV field dwarfs, median [sigma]':46s}{zz(D2, 'z', 'L'):>16s}{zz(D2, 'z', 'S'):>16s}   median {D2[('canonical', 'S')]['fex']:.2f}/{D2[('alt', 'S')]['fex']:.2f}"
  f"      {ch['d2']:.3f} dex")
P(f"    {'    median [dex] canonical, +- total':46s}{D2[('canonical', 'L')]['med']:+.3f}+-{D2[('canonical', 'L')]['tot']:.3f} {D2[('canonical', 'S')]['med']:+.3f}+-{D2[('canonical', 'S')]['tot']:.3f}   (n = {D2[('canonical', 'L')]['n']})")
ch["e"] = max(SP[(f, "LSB")]["median"] for f in FOOTS)
for k in SETS:
    sc, sa = SP[("canonical", k)], SP[("alt", k)]
    fr = f"{100 * sc['frac_lt003']:.0f}%|{100 * sa['frac_lt003']:.0f}%"
    P(f"    {'(e) SPARC ' + k + ' (n=' + str(sc['n']) + ') <0.03 dex':46s}{'100%':>16s}{fr:>16s}   f_ex=0 {100 * sc['frac_fex0']:.0f}%|{100 * sa['frac_fex0']:.0f}%   median {sc['median']:.3f} max {sc['max']:.3f} dex")
    zl = f"{sc['data']['L']['z']:+.2f}|{sa['data']['L']['z']:+.2f}"; zs_ = f"{sc['data']['S']['z']:+.2f}|{sa['data']['S']['z']:+.2f}"
    P(f"    {'    data offset log(Vflat/v_pred) [sigma]':46s}{zl:>16s}{zs_:>16s}   (n={sc['data']['L']['n']}; median {sc['data']['L']['med']:+.3f} -> {sc['data']['S']['med']:+.3f} dex, canonical)")
P(f"    LSB cut: SBdisk < median {SB_MED:.1f} L_sun/pc^2 over {len(SPR)} galaxies; LSB n = {sum(s['lsb'] for s in SPR)}; worst LSB (S, canonical): {SP[('canonical', 'LSB')]['worst']}")

# ---------------------------------------------------------------------------------------------- gates and classification
GATE = {}
GATE["a UDGs"] = dict(L=all(abs(UD[(f, "L")]["z"]) < 2 for f in FOOTS), S=all(abs(UD[(f, "S")]["z"]) < 2 for f in FOOTS), change=ch["a"])
zN2 = DF[("NGC1052-DF2", "Danieli19", 20.0)]["z_N"]; zN4 = DF[("NGC1052-DF4", "vanDokkum19", 20.0)]["z_N"]
dfB = max(abs(DF[(nm, on, 20.0)][f]["dlog"]) for nm, on in (("NGC1052-DF2", "Danieli19"), ("NGC1052-DF4", "vanDokkum19")) for f in FOOTS)
GATE["b DF2/DF4 (T-E)"] = dict(L=zN2 <= 2 and zN4 <= 2, S=zN2 <= 2 and zN4 <= 2, change=0.0)
GATE["c TDGs (T-E)"] = dict(L=chiN_T <= 12.6, S=chiN_T <= 12.6, change=0.0)
GATE["d1 LV stat C"] = dict(L=all(abs(D1[(f, "L")]["z"]) < 2 for f in FOOTS), S=all(abs(D1[(f, "S")]["z"]) < 2 for f in FOOTS), change=None,
                            note=f"slope population: Delta slope {max(abs(D1[(f, 'S')]['pred'] - D1[(f, 'L')]['pred']) for f in FOOTS):.4f} (obs err {D1[('canonical', 'S')]['err']:.4f})")
GATE["d2 LV field dwarfs"] = dict(L=all(abs(D2[(f, "L")]["z"]) < 2 for f in FOOTS), S=all(abs(D2[(f, "S")]["z"]) < 2 for f in FOOTS), change=ch["d2"])
GATE["e SPARC LSB"] = dict(L=True, S=all(SP[(f, "LSB")]["frac_lt003"] >= 0.90 for f in FOOTS), change=ch["e"])
BLIND = {"b DF2/DF4 T-B": dict(L=all(abs(DF[(nm, on, 20.0)][f]["zL"]) <= 2 for nm, on in (("NGC1052-DF2", "Danieli19"), ("NGC1052-DF4", "vanDokkum19")) for f in FOOTS),
                                S=all(abs(DF[(nm, on, 20.0)][f]["zS"]) <= 2 for nm, on in (("NGC1052-DF2", "Danieli19"), ("NGC1052-DF4", "vanDokkum19")) for f in FOOTS),
                                change=dfB, spared=dfB < 0.03),
         "c TDGs T-B": dict(L=all(TD[(f, "L")]["chi2"] <= 12.6 for f in FOOTS), S=all(TD[(f, "S")]["chi2"] <= 12.6 for f in FOOTS),
                            change=max(max(TD[(f, "dlog")]) for f in FOOTS), spared=max(max(TD[(f, "dlog")]) for f in FOOTS) < 0.03)}


def classify(L, S, c):
    if c is None:
        return "BOTH PASS" if (L and S) else ("BREAKS" if L else ("FIXES" if S else "BOTH FAIL"))
    if L and not S:
        return "BREAKS"
    if S and not L:
        return "FIXES"
    if S and L:
        return "SPARES" if c < 0.03 else "MOVES"
    return "BOTH FAIL"


R.banner("ACCEPTANCE AND CLASSIFICATION (declared): which populations the sum breaks or spares")
P(f"    {'population':26s}{'L gate':>9s}{'S gate':>9s}{'change [dex]':>14s}   verdict")
for k, v in GATE.items():
    v["verdict"] = classify(v["L"], v["S"], v["change"])
    cs = "n/a" if v["change"] is None else f"{v['change']:.3f}"
    P(f"    {k:26s}{'pass' if v['L'] else 'FAIL':>9s}{'pass' if v['S'] else 'FAIL':>9s}{cs:>14s}   {v['verdict']}" + (f"  ({v['note']})" if "note" in v else ""))
P("    -- T-B (blind application to the class-E objects; diagnostic; 'spared by the rule itself' = |change| < 0.03 dex) --")
for k, v in BLIND.items():
    v["verdict"] = classify(v["L"], v["S"], v["change"])
    P(f"    {k:26s}{'pass' if v['L'] else 'FAIL':>9s}{'pass' if v['S'] else 'FAIL':>9s}{v['change']:>14.3f}   {v['verdict']}  (spared by the rule itself: {v['spared']})")
e2 = all(SP[(f, "LSB")]["frac_fex0"] >= 0.90 and SP[(f, "LSB")]["max"] < 0.03 for f in FOOTS)
e3 = all(abs(SP[(f, "LSB")]["data"]["S"]["z"]) < 2 for f in FOOTS); e3L = all(abs(SP[(f, "LSB")]["data"]["L"]["z"]) < 2 for f in FOOTS)
P(f"    (e) reported: E2 (CFG36 strict: f_ex = 0 in >= 90% AND max < 0.03) {'pass' if e2 else 'FAIL'}; E3 (data offset |median| < 2 sigma) L {'pass' if e3L else 'FAIL'}, S {'pass' if e3 else 'FAIL'}")

# ---------------------------------------------------------------------------------------------- reported diagnostics (added after the first run)
R1 = {f: (D2[(f, "S")]["med"] / D2[(f, "L")]["tot"]) for f in FOOTS}
check("R1 (reported, added after the first run) the field-dwarf (S) median in units of (L)'s total error (S shrinks the scatter, hence its own error)",
      "; ".join(f"{f}: S median {D2[(f, 'S')]['med']:+.3f} dex, own error {D2[(f, 'S')]['tot']:.3f} -> {D2[(f, 'S')]['z']:+.2f} sigma; in L's error {D2[(f, 'L')]['tot']:.3f} -> {R1[f]:+.2f} sigma; "
                f"std of offsets L {np.std(D2[(f, 'L')]['per']):.3f} -> S {np.std(D2[(f, 'S')]['per']):.3f}" for f in FOOTS), True, load_bearing=False)


def switch_off(foot, frac_star):
    lo, hi = 5.0, 12.0
    for _ in range(40):
        mid = 0.5 * (lo + hi); Mb = 10 ** mid
        Mh = float(halo_mass(frac_star * Mb))
        lo, hi = (mid, hi) if fex_of(Mb, Mh, foot) > 0 else (lo, mid)
    return 10 ** (0.5 * (lo + hi))


SW = {f"{f}|M*={fs}Mb": switch_off(f, fs) for f in FOOTS for fs in (1.0, 0.5)}
Mb_pops = {"Coma UDGs (with infall gas)": [MST[j] * (1 + RZ[i, j]) / MSU for j in range(len(UDG)) for i in (0, 500, 1000, 1500)],
           "DF2/DF4": [2.0 * v[0] for v in LV_DF.values()], "tidal dwarfs (M_bar)": [float(x) for x in gt["MB"]],
           "LV statistic-C dwarfs": [g["Mb"] for g in KDd], "LV field dwarfs": [2.0 * d["LV"] + 1.33 * d["MHI"] for d in FLD], "SPARC LSB": [s["Mb"] for s in SPR if s["lsb"]]}
check("R2 (reported, added after the first run) the baryonic mass above which (S) switches itself off (f_ex = 0: the law's edge phantom exceeds the cold budget (1 - f_b) M_c), against each population's M_b",
      "M_b(f_ex -> 0) = " + ", ".join(f"{k} {v:.2e}" for k, v in SW.items()) + "; population M_b [min / median / fraction above the canonical M*=M_b/2 switch-off]: "
      + "; ".join(f"{k} {min(v):.1e}/{np.median(v):.1e}/{np.mean(np.array(v) > SW['canonical|M*=0.5Mb']):.2f}" for k, v in Mb_pops.items()), True, load_bearing=False)
R.num("R1_fld_S_in_L_error", R1); R.num("R2_switch_off", SW)

# ---------------------------------------------------------------------------------------------- headline and controls
mainchg = {"a UDGs": ch["a"], "d2 LV field dwarfs": ch["d2"], "e SPARC LSB (median dlogv)": ch["e"], "b DF2/DF4 (T-E)": 0.0, "c TDGs (T-E)": 0.0}
h1 = any(v > 0.05 for v in mainchg.values())
check("H1 [HEADLINE] THE SUM HAS BITE ON THE NEW POPULATIONS: it changes at least one scored population by > 0.05 dex (dex of sigma / v; T-E rows count 0)"
      + ("  [MUTATE: collapse masses / 100]" if MUTATE else ""), "; ".join(f"{k}: {v:.3f}" for k, v in mainchg.items()), h1)
allchg = dict(mainchg); allchg["b DF2/DF4 T-B"] = dfB; allchg["c TDGs T-B"] = BLIND["c TDGs T-B"]["change"]
allchg["e SPARC LSB max dlogv"] = max(SP[(f, "LSB")]["max"] for f in FOOTS); allchg["d1 stat C |d slope|"] = max(abs(D1[(f, "S")]["pred"] - D1[(f, "L")]["pred"]) for f in FOOTS)
check("C3 CONTROL (MUTATE run only): with every collapse mass / 100, (S) equals (L): every change < 0.01 dex (Delta slope < 0.01)",
      "; ".join(f"{k}: {v:.4f}" for k, v in allchg.items()), (all(v < 0.01 for v in allchg.values())) if MUTATE else True, load_bearing=MUTATE)
check("H2 (reported) the classification", "; ".join(f"{k}: {v['verdict']}" for k, v in GATE.items()) + " | T-B: " + "; ".join(f"{k}: {v['verdict']} (spared by the rule itself: {v['spared']})" for k, v in BLIND.items()),
      True, load_bearing=False)
R.num("UDG", {f"{a}|{b}": v for (a, b), v in UD.items()}); R.num("DF", {f"{a}|{b}|{c}": v for (a, b, c), v in DF.items()})
R.num("TDG", {f"{a}|{b}": v for (a, b), v in TD.items()}); R.num("statC", {f"{a}|{b}": v for (a, b), v in D1.items()})
R.num("field_dwarfs", {f"{a}|{b}": {k: v for k, v in d.items() if k != "per"} for (a, b), d in D2.items()})
R.num("SPARC_LSB", {f"{a}|{b}": v for (a, b), v in SP.items()}); R.num("SB_median", SB_MED)
R.num("GATE", GATE); R.num("BLIND", BLIND); R.num("changes", allchg)
nf = R.write(here=OUT)
sys.exit(1 if nf else 0)
