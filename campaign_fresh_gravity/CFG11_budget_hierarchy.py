#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG11 -- THE COLD BUDGET UNDER FG001's OWN HIERARCHY.  Does CFG4's minimal conflict (KiDS's reach against the turned-around cold
matter, 'strict' reading: closed) survive when the phantom is owned only by TOP-LEVEL bound systems?

WHY.  CFG4_target's budget let EVERY galaxy carry its own isolated phantom out to x r_ta (it says so: 'an upper bound:
satellites share their host's phantom').  Under FG001 (CFG7) only the outermost bound system owns a phantom: a group's cold
component is ONE phantom sourced by the group's total baryons, and its members' own cold components are lumps inside it -- never
added on top (T5: the cold matter in a bound region IS the phantom; counting a satellite's cold mass again would count it twice).
The per-system phantom within x r_ta grows SUBLINEARLY with the baryonic mass (~ M_b^(3/4) in the deep regime), so grouping can
only LOWER the sum.  CFG4's only hierarchical variant was a proxy (galaxies below 10^9 Msun carry no phantom).  Here the grouping
is measured: the Kourkchi & Tully 2017 catalogue (ApJ 843, 16; galaxy groups within 3500 km/s, VizieR J/ApJ/843/16, committed in
real_research/data/kt2017_*.tsv) assigns every local galaxy to its bound group (membership inside the group's second-turnaround
radius).

THE MEASUREMENT.  In volume-limited samples (D <= D_max, K_s <= 11.75 at D_max -- the 2MRS limit the catalogue is complete to),
with CFG4's own per-system phantom (the law's isolated profile, the turnaround contrast Delta_ta(0) = 11.81, the phantom out to
x r_ta; the same function CFG4 integrates over the GAMA stellar mass function) and CFG4's own baryons (M_* = Upsilon_K L_K with
Upsilon_K = 0.6 declared; SPARC's gas fraction fit, CFG4's):
      R(x) = SUM over groups of M_ph(SUM of the members' M_b; x)  /  SUM over galaxies of M_ph(M_b; x)
The FG001 budget: Omega_ph,FG001(x) = Omega_ph(x; all galaxies) - [1 - R(x)] * Omega_ph(x; galaxies above the sample's mass
limit) -- the reduction is applied ONLY above the limit (dwarfs below keep their own phantoms: conservative).  The strict edge:
Omega_ph,FG001(x_b) = Omega_c x f_ta (z = 0, the turned-around share 0.602, CFG4's).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG4_target's committed Omega_ph(x) (every galaxy, all four footing/kernel rows, z = 0 and 0.25, M_* cuts 1e7/1e9/
      1e10, x = 0.2-1.0) and its strict and lenient budget edges reproduced to 1e-9 (relative) by this lane's copy of the function.
  C2  CONTROL  the catalogue join: every galaxy's group exists in the group table; the summed member K luminosities reproduce the
      catalogue's group logK (median |d| <= 0.1 dex over groups with Nm >= 3 whose members are all in the galaxy table).
  H0  [MUTATE must fail] grouping lowers the phantom sum in every sample: R(0.31) < 1 (a theorem of the sublinear phantom; a check
      of the join and the arithmetic).
  H1  [HEADLINE] under FG001's hierarchy the strict budget edge reaches the KiDS floor with the 2-halo term (x_b >= CFG4's floor,
      0.303-0.310) for both footings and both kernels, in every declared sample (D_max = 15, 25, 35 Mpc) at Upsilon_K = 0.6.
      Declared EXPECTATION: uncertain (the canonical rows need R <~ 0.90, the alt rows R <~ 0.78).
  R1  (reported) R(x) per sample, with and without the largest group (the Virgo cluster where it is inside D_max); Upsilon_K 0.4 /
      0.8; a deeper K_s limit (13.0); the satellite fraction by stellar mass.
MUTATE=1: every group is split into its galaxies (each its own system) -- R = 1, so H0 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG11_budget_hierarchy.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4                                                                              # CFG4's conventions, exactly
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG11_budget_hierarchy", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every group split into its galaxies -- H0 must FAIL ***")
np.seterr(all="ignore")

SW = json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]
T4 = json.load(open(os.path.join(HERE, "CFG4_target_results.json")))["numbers"]["H3"]
A0 = C.A0
KERN = {"P2": C.nu_p2, "nu_mono": C.nu_mono}

# ================================================================================================ CFG4_target's budget, copied
H_FID = 0.6733167
LMS, PHI1, AL1, PHI2, AL2 = 10.66, 3.96e-3, -0.35, 0.79e-3, -1.47
lmg = np.linspace(7.0, 12.3, 1060)
Mst = 10 ** lmg
x_ = Mst / 10 ** LMS
phi = math.log(10) * np.exp(-x_) * (PHI1 * x_ ** (AL1 + 1) + PHI2 * x_ ** (AL2 + 1))
Mst_h = Mst * (0.7 / H_FID) ** 2
phi_h = phi * (H_FID / 0.7) ** 3
GAL = C.load_sparc()
ls_, lg_ = [], []
for g in GAL:
    m = g["meta"]
    if m and m["MHI"] > 0 and m["L36"] > 0:
        ms_ = 0.5 * m["L36"] * 1e9
        ls_.append(math.log10(ms_)); lg_.append(math.log10(1.33 * m["MHI"] * 1e9 / ms_))
cfit = np.polyfit(ls_, lg_, 1)
fgas = 10 ** np.polyval(cfit, np.log10(Mst_h))
RHOC0 = 3 * (100 * H_FID * 1e3 / C.MPC) ** 2 / (8 * math.pi * C.G_SI)
RHOC0_MSUN = RHOC0 * C.MPC ** 3 / C.MSUN
OM0 = 0.3153; OC0 = 0.1200 / H_FID ** 2
DTA = {z: SW["D1"][str(z)]["one_plus_delta_ta"] for z in (0.0, 0.25)}
RG = np.geomspace(1e-3, 30.0, 3000) * C.MPC
F_TA = max(r_["f_ta"] for r_ in SW["V"]["web"] if r_["z"] == 0.0)
KIDS = SW["H2c"]["x_floor"]


def rta_of(Mb, kfun, a0, z):
    """CFG4_target.r_turnaround, for any array of baryonic masses [kg]: where the law's enclosed mass falls to Delta_ta(z) rho_m."""
    rhom = OM0 * RHOC0 * (1 + z) ** 3
    MR = Mb[:, None] * kfun(C.G_SI * Mb[:, None] / RG[None, :] ** 2 / a0)
    D = MR / (4 / 3 * math.pi * RG[None, :] ** 3 * rhom)
    j = np.argmax(D < DTA[z], axis=1)
    i = np.arange(len(Mb))
    lr = np.log(RG[j - 1]) + (math.log(DTA[z]) - np.log(D[i, j - 1])) * (np.log(RG[j]) - np.log(RG[j - 1])) / \
        (np.log(D[i, j]) - np.log(D[i, j - 1]))
    return np.exp(lr)


def mph_of(Mb, kfun, a0, z, x):
    """the phantom [Msun] inside x r_ta of an isolated system of baryonic mass Mb [kg] (CFG4_target.phantom_budget's integrand)."""
    rc = x * rta_of(Mb, kfun, a0, z)
    return Mb * (kfun(C.G_SI * Mb / rc ** 2 / a0) - 1.0) / C.MSUN


_MB_SMF = Mst_h * (1 + fgas) * C.MSUN
_MPH_CACHE = {}
_RTA_SMF = {}


def omega_ph(kfun, a0, z, x, mcut):
    key = (id(kfun), a0, z, x)
    if key not in _MPH_CACHE:
        k2 = (id(kfun), a0, z)
        if k2 not in _RTA_SMF:
            _RTA_SMF[k2] = rta_of(_MB_SMF, kfun, a0, z)
        rc = x * _RTA_SMF[k2]
        _MPH_CACHE[key] = _MB_SMF * (kfun(C.G_SI * _MB_SMF / rc ** 2 / a0) - 1.0) / C.MSUN
    m = np.log10(Mst_h) >= mcut
    return float(np.trapz((phi_h * _MPH_CACHE[key])[m], lmg[m]) / RHOC0_MSUN)


XG = (0.2, 0.3, 0.31, 0.4, 0.48, 0.6, 0.8, 1.0)


def x_edge(fun, limit, xs):
    om = np.array([fun(x) for x in xs])
    if om[0] > limit:
        return 0.0
    if om[-1] <= limit:
        return float(xs[-1])
    return float(np.interp(limit, om, xs))


# ================================================================================================ C1
R.banner("C1  CONTROL: CFG4_target's committed budget, reproduced")
dev1 = 0.0; nrow = 0
for f in C.FOOTS:
    for kn, kf in KERN.items():
        for z in (0.0, 0.25):
            for mc in (7.0, 9.0, 10.0):
                ref = T4["budget"][f"{f}|{kn}|z{z}|m{mc}"]
                for x in XG:
                    v = omega_ph(kf, A0[f], z, x, mc)
                    dev1 = max(dev1, abs(v / ref[str(x)][0] - 1.0)); nrow += 1
                xb = T4["x_budget"][f"{f}|{kn}|z{z}|m{mc}"]
                mine = dict(x_Omc=x_edge(lambda x: omega_ph(kf, A0[f], z, x, mc), OC0, XG),
                            x_bound=x_edge(lambda x: omega_ph(kf, A0[f], z, x, mc), OC0 * F_TA, XG))
                dev1 = max(dev1, abs(mine["x_Omc"] - xb["x_Omc"]), abs(mine["x_bound"] - xb["x_bound"]))
dev1 = max(dev1, abs(OC0 / T4["Omega_c"] - 1), abs(F_TA / T4["f_ta_web_k1"] - 1))
check("C1 CONTROL: CFG4_target's committed Omega_ph(x), budget edges, Omega_c and turned-around share reproduced to 1e-9",
      f"{nrow} Omega_ph values + edges: max relative deviation {dev1:.1e}", dev1 <= 1e-9)
P(f"    strict edges (every galaxy, z = 0, turned-around share {F_TA:.3f}): " + "; ".join(
    f"{f[:3]}/{kn} {T4['x_budget'][f'{f}|{kn}|z0.0|m7.0']['x_bound']:.3f}" for f in C.FOOTS for kn in KERN) +
  "  | KiDS floors (2-halo): " + "; ".join(f"{k.replace('|A2', '')} {v[0]:.3f}" for k, v in KIDS.items() if k.endswith("A2")))


# ================================================================================================ the catalogue
def read_vizier(path):
    rows, hdr, skip = [], None, 0
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        if hdr is None:
            hdr = line.rstrip("\n").split("\t"); skip = 2; continue
        if skip:
            skip -= 1; continue
        rows.append(line.rstrip("\n").split("\t"))
    return hdr, rows


DD = os.path.join(C.REPO, "real_research", "data")
hg, rg_ = read_vizier(os.path.join(DD, "kt2017_galaxies.tsv"))
hG, rG_ = read_vizier(os.path.join(DD, "kt2017_groups_full.tsv"))
ig = {k: i for i, k in enumerate(hg)}; iG = {k: i for i, k in enumerate(hG)}


def fnum(s):
    s = s.strip()
    return float(s) if s else float("nan")


GRP = {}
for r_ in rG_:
    GRP[int(r_[iG["PGC1"]])] = dict(Nm=int(r_[iG["Nm"]]), logK=fnum(r_[iG["logK"]]), D=fnum(r_[iG["Dist"]]))
gpgc = np.array([int(r_[ig["PGC"]]) for r_ in rg_])
gid = np.array([int(r_[ig["PGC1"]]) for r_ in rg_])
Ks = np.array([fnum(r_[ig["Ksmag"]]) for r_ in rg_])
HRV = np.array([fnum(r_[ig["HRV"]]) for r_ in rg_])
missing = int(sum(1 for k in gid if k not in GRP))
MSUN_K = 3.28
# the catalogue's own distance convention (its group luminosities use it; C2): the group's mean heliocentric velocity / 75.
# The 'Dist' column (a different distance, missing for part of the groups) is carried as a robustness row.  [Adopted after the
# first -- MUTATE -- run, whose C2 used 'Dist' and failed at median |d| 0.151 dex; the diagnosis: V/75 reproduces logK to 0.058.]
_ug, _inv = np.unique(gid, return_inverse=True)
_vmean = np.bincount(_inv, weights=np.nan_to_num(HRV)) / np.maximum(np.bincount(_inv, weights=np.isfinite(HRV).astype(float)), 1)
DV = _vmean[_inv] / 75.0
DIST = np.array([GRP[k]["D"] if k in GRP else np.nan for k in gid])
MODE = {"V/75": DV, "Dist": DIST}


def lum(Dg):
    return 10 ** (-0.4 * (Ks - (5 * np.log10(np.where(Dg > 0, Dg, np.nan)) + 25) - MSUN_K))


Dg = DV
LK = lum(Dg)
P(f"\n  KT2017: {len(gpgc)} galaxies in {len(GRP)} groups; galaxies whose group is missing from the group table: {missing}; "
  f"with a K_s magnitude and a group distance: {int(np.sum(np.isfinite(LK)))}")

# C2: the join -- summed member luminosities against the catalogue's group logK
d2 = []
for k, G_ in GRP.items():
    if G_["Nm"] < 3 or not np.isfinite(G_["logK"]):
        continue
    m = gid == k
    if m.sum() != G_["Nm"] or not np.all(np.isfinite(LK[m])):
        continue
    d2.append(math.log10(np.sum(LK[m])) - G_["logK"])
d2 = np.array(d2)
d2b = []
LKd = lum(DIST)
for k, G_ in GRP.items():
    if G_["Nm"] < 3 or not np.isfinite(G_["logK"]):
        continue
    m = gid == k
    if m.sum() != G_["Nm"] or not np.all(np.isfinite(LKd[m])):
        continue
    d2b.append(math.log10(np.sum(LKd[m])) - G_["logK"])
check("C2 CONTROL: the join -- every galaxy's group is in the group table, and summed member K luminosities reproduce the "
      "catalogue's group logK in its own distance convention (median |d| <= 0.1 dex, groups with Nm >= 3 fully present) "
      "[convention fixed after the first run; the 'Dist' column's value is printed]",
      f"missing groups {missing}; V/75: {len(d2)} groups, median d {np.median(d2):+.3f} dex, median |d| {np.median(np.abs(d2)):.3f}; "
      f"'Dist': {len(d2b)} groups, median |d| {np.median(np.abs(d2b)):.3f}",
      missing == 0 and len(d2) > 50 and np.median(np.abs(d2)) <= 0.1)


def baryons(Lk, upsK):
    Ms = upsK * Lk
    return Ms * (1 + 10 ** np.polyval(cfit, np.log10(Ms))), Ms


def sample(Dmax, Kslim=11.75, drop_largest=False, mode="V/75"):
    Dg_ = MODE[mode]; LK_ = lum(Dg_)
    Llim = 10 ** (-0.4 * (Kslim - (5 * math.log10(Dmax) + 25) - MSUN_K))
    m = np.isfinite(LK_) & (Dg_ <= Dmax) & (LK_ >= Llim)
    if drop_largest:
        gsel = np.unique(gid[m])
        big = max(gsel, key=lambda k: GRP[k]["Nm"])
        m &= gid != big
    return m, Llim


_RC = {}


def ratio(m, upsK, kfun, a0, x, mode="V/75"):
    key = (m.tobytes(), upsK, id(kfun), a0, mode)
    if key not in _RC:
        Mb, Ms = baryons(lum(MODE[mode])[m], upsK)
        groups = gpgc[m] if MUTATE else gid[m]                                         # MUTATE: every galaxy its own system
        ug, inv = np.unique(groups, return_inverse=True)
        Mg = np.bincount(inv, weights=Mb)
        _RC[key] = (Mb * C.MSUN, rta_of(Mb * C.MSUN, kfun, a0, 0.0), Mg * C.MSUN, rta_of(Mg * C.MSUN, kfun, a0, 0.0))
    Mb_kg, rt_g, Mg_kg, rt_G = _RC[key]
    mph = lambda M, rt: M * (kfun(C.G_SI * M / (x * rt) ** 2 / a0) - 1.0) / C.MSUN
    return float(np.sum(mph(Mg_kg, rt_G)) / np.sum(mph(Mb_kg, rt_g)))


def fg001_edge(f, kn, Rfun, mlim):
    kf = KERN[kn]
    xs = np.round(np.arange(0.20, 0.801, 0.01), 2)
    fun = lambda x: omega_ph(kf, A0[f], 0.0, x, 7.0) - (1.0 - Rfun(x)) * omega_ph(kf, A0[f], 0.0, x, mlim)
    return x_edge(fun, OC0 * F_TA, xs)


# ================================================================================================ the samples
R.banner("THE SAMPLES: R(x) and the FG001 strict budget edge")
UPSK = 0.6
SAMPLES = [(15.0, False), (25.0, False), (35.0, False)]
RES = {}
for Dmax, drop in SAMPLES + [(25.0, True), (35.0, True)]:
    m, Llim = sample(Dmax, drop_largest=drop)
    mlim = math.log10(UPSK * Llim)
    nsat = int(np.sum(gpgc[m] != gid[m]))
    lab = f"D<={Dmax:.0f}" + (" no-largest" if drop else "")
    for f in C.FOOTS:
        for kn, kf in KERN.items():
            Rx = {x: ratio(m, UPSK, kf, A0[f], x) for x in (0.31, 0.4)}
            Rfun = lambda x, _m=m, _kf=kf, _a=A0[f]: ratio(_m, UPSK, _kf, _a, x)
            xb = fg001_edge(f, kn, Rfun, mlim)
            RES[(lab, f, kn)] = dict(n=int(m.sum()), n_sat=nsat, log_mstar_lim=mlim, R031=Rx[0.31], R04=Rx[0.4], x_b=xb,
                                     kids_floor=KIDS[f"{f}|{kn}|A2"][0],
                                     x_b_every_galaxy=T4["x_budget"][f"{f}|{kn}|z0.0|m7.0"]["x_bound"])
    P(f"    {lab:16s}: {int(m.sum())} galaxies above log M_* = {mlim:.2f} ({nsat} satellites, {nsat / max(m.sum(), 1):.2f}); " +
      "; ".join(f"{f[:3]}/{kn}: R(0.31) {RES[(lab, f, kn)]['R031']:.3f}, edge {RES[(lab, f, kn)]['x_b']:.3f} (floor "
                f"{RES[(lab, f, kn)]['kids_floor']:.3f})" for f in C.FOOTS for kn in KERN))

h0 = all(RES[(f"D<={d:.0f}", f, kn)]["R031"] < 1.0 for d, _ in SAMPLES for f in C.FOOTS for kn in KERN)
check("H0 grouping lowers the phantom sum in every declared sample: R(0.31) < 1 (the sublinear phantom)" +
      ("  [MUTATE: groups split]" if MUTATE else ""),
      "; ".join(f"D<={d:.0f}: " + "/".join(f"{RES[(f'D<={d:.0f}', f, kn)]['R031']:.3f}" for f in C.FOOTS for kn in KERN)
                for d, _ in SAMPLES), h0)
h1rows = [(d, f, kn, RES[(f"D<={d:.0f}", f, kn)]) for d, _ in SAMPLES for f in C.FOOTS for kn in KERN]
h1 = all(v["x_b"] >= v["kids_floor"] for d, f, kn, v in h1rows)
check("H1 [HEADLINE] under FG001's hierarchy the strict budget edge reaches the KiDS floor (2-halo) for both footings and both "
      "kernels in every declared sample (D_max = 15, 25, 35 Mpc; Upsilon_K = 0.6)",
      "; ".join(f"D{d:.0f} {f[:3]}/{kn}: {v['x_b']:.3f} vs {v['kids_floor']:.3f}" for d, f, kn, v in h1rows), h1)

# ================================================================================================ R1 robustness
R.banner("R1  ROBUSTNESS (reported): Upsilon_K, a deeper K limit, the largest group removed, the satellite fraction")
ROB = {}
for Dmax in (25.0, 35.0):
    for ups in (0.4, 0.8):
        m, Llim = sample(Dmax)
        mlim = math.log10(ups * Llim)
        for f in C.FOOTS:
            kf = KERN["P2"]
            Rfun = lambda x, _m=m, _kf=kf, _a=A0[f], _u=ups: ratio(_m, _u, _kf, _a, x)
            ROB[(f"D<={Dmax:.0f} U_K {ups}", f)] = dict(R031=Rfun(0.31), x_b=fg001_edge(f, "P2", Rfun, mlim))
    m, Llim = sample(Dmax, Kslim=13.0)
    mlim = math.log10(UPSK * Llim)
    for f in C.FOOTS:
        kf = KERN["P2"]
        Rfun = lambda x, _m=m, _kf=kf, _a=A0[f]: ratio(_m, UPSK, _kf, _a, x)
        ROB[(f"D<={Dmax:.0f} Ks<=13", f)] = dict(R031=Rfun(0.31), x_b=fg001_edge(f, "P2", Rfun, mlim))
    m, Llim = sample(Dmax, mode="Dist")
    mlim = math.log10(UPSK * Llim)
    for f in C.FOOTS:
        kf = KERN["P2"]
        Rfun = lambda x, _m=m, _kf=kf, _a=A0[f]: ratio(_m, UPSK, _kf, _a, x, mode="Dist")
        ROB[(f"D<={Dmax:.0f} 'Dist'", f)] = dict(R031=Rfun(0.31), x_b=fg001_edge(f, "P2", Rfun, mlim))
for k, v in ROB.items():
    P(f"    {k[0]:18s} {k[1]:9s} P2: R(0.31) {v['R031']:.3f}, FG001 strict edge {v['x_b']:.3f}")
for lab in ("D<=25 no-largest", "D<=35 no-largest"):
    P(f"    {lab:18s}: " + "; ".join(f"{f[:3]}/{kn} R(0.31) {RES[(lab, f, kn)]['R031']:.3f}, edge {RES[(lab, f, kn)]['x_b']:.3f}"
                                    for f in C.FOOTS for kn in KERN))
m, Llim = sample(35.0)
Mb, Ms = baryons(LK[m], UPSK)
sat = gpgc[m] != gid[m]
bins = [(8.5, 9.5), (9.5, 10.0), (10.0, 10.5), (10.5, 11.0), (11.0, 12.5)]
fs = []
for lo, hi in bins:
    mm = (np.log10(Ms) >= lo) & (np.log10(Ms) < hi)
    fs.append((lo, hi, int(mm.sum()), float(np.mean(sat[mm])) if mm.any() else float("nan")))
P("    satellite fraction by log M_* (D <= 35, Upsilon_K 0.6): " + ", ".join(f"[{lo}, {hi}): {fr:.2f} (N {n})" for lo, hi, n, fr in fs))
check("R1 (reported) robustness: Upsilon_K 0.4/0.8, K_s <= 13, the largest group removed, the satellite fraction",
      "; ".join(f"{k[0]} {k[1][:3]}: edge {v['x_b']:.3f}" for k, v in ROB.items()), True, load_bearing=False)
R.num("RES", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in RES.items()})
R.num("ROB", {f"{k[0]}|{k[1]}": v for k, v in ROB.items()})
R.num("sat_frac", fs)
nf = R.write()
sys.exit(1 if nf else 0)
