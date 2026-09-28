#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG7 / FG001 -- HIERARCHICAL OWNERSHIP OF THE PHANTOM, scored population by population on the record's own statistics.

THE PRINCIPLE (FG001, with CFG4's T5 "in bound regions the cold component IS the phantom").  The framework's law acts on a
system's own baryons only if that system is TOP-LEVEL (the outermost bound system).  Three classes follow, with no new
constant:
  T  top-level (isolated galaxies, groups' and clusters' centrals): the law on their own baryons, no external-field effect
     (the web is not a host; a uniform external field drops out of a system's internal dynamics).
  A  accreted (formed top-level, later embedded: satellites, cluster members, UDGs): they keep the cold component they owned
     at infall -- by T5 their phantom WAS cold matter, collisionless, bound inside their tidal radius.  Their internal
     dynamics is Newtonian with that retained cold matter, i.e. the ISOLATED law of their infall baryons, with NO external-
     field effect.
  E  formed embedded, without a cold component (tidal dwarfs, globular clusters, collision debris such as NGC 1052-DF2/DF4,
     wide binaries, the Solar System): NEWTONIAN from their baryons.
The rival reading, scored beside it on the same statistics: the law acts on every system's own baryons with its host's
external field (the record's chain/M*/QUMOND reading; XR27's L -> infinity rows; h43's EFE column).

WHAT IS RE-USED (read-only; each reproduced as a control): h43 (hunt_2026, the LG dwarf dispersions), f13 (hunt_2026, the
outer-halo globular clusters), XR27 (the cluster-infall BTFR, the LV dwarfs' host statistic, DF2/DF4, Chae's EFE fits), and
this campaign's FG041 (tidal dwarfs).  Data: real_research/data/dsph (LVD 2024, Collins+2013), globular_clusters (Baumgardt).

PRE-DECLARED (before this script's first run)
  K1  CONTROL  h43's committed medians log10(sigma_obs/sigma_pred) (EFE, isolated, Newtonian; MW ultra-faint / classical / all,
      M31 Collins / LVD; both footings; and the isolated field dwarfs' -0.044 / -0.062) are reproduced to 0.001 dex.
  K2  CONTROL  f13's committed medians (+0.302 dex with the external field, +0.561 without; 16 discriminating clusters) are
      reproduced to 0.001 dex.
  K3  CONTROL  XR27's committed significances are recomputed from its own committed obs/err/prediction numbers (LV dwarfs'
      statistic, the cluster slope and zero point) to 0.01 sigma.
  K4  CONTROL  FG041 (CFG7_tdg_fg041_results.json) is committed with 0 load-bearing failures.
  H1  CASSINI WITHOUT xi (FG029): the Sun owns no phantom; the only non-Newtonian tide in the Solar System is the Milky Way's
      phantom field's, and it is below Cassini's quadrupole bound 5.2e-27 s^-2 by >= 1e3 on both footings.
  H2  GLOBULAR CLUSTERS (class E): the Newtonian dynamical M/L_V of the discriminating clusters with >= 20 radial velocities has
      a median inside the stellar-population range [1.0, 2.5]; the law with the external field needs a median M/L_V (dynamical
      over its boost) below 1.0 (reported).
  H3  TIDAL DWARFS (class E): FG041's kill test passed (from its committed results).
  H4  SATELLITES (class A = the isolated law): the median offset is within 2 sigma of zero for the MW classical dSphs and the
      M31 LVD sample on both footings (reported: M31 Collins, the MW ultra-faints); the external-field column fails them.
  H5  THE HOST STATISTICS (class A predicts no host dependence): the LV dwarfs' statistic and the cluster-infall BTFR slope and
      zero point are within 2 sigma of zero on both footings.
  H6  DF2 and DF4 (class E): Newtonian within 2 sigma at 20 Mpc for the central measurements (Danieli+19, van Dokkum+19).
  H7  THE COST (reported, pre-declared as a likely failure): Chae's EFE fits (D1, D2) against zero external field.
  H0  [HEADLINE] FG001 passes strictly more of the gates G1-G14 than the law-with-external-field reading, on both footings.
  H8  (reported; EXPLORATORY, declared after seeing h43's isolated offsets) the fossil-gas account under the max rule: a satellite
      keeps the cold component set by its pre-infall baryons, so if it has since lost its gas it sits above the isolated law
      for its current stars by (1/4) log(1 + f_g) in the deep regime; f_g(M_*) from the isolated LG dwarfs' own HI.
MUTATE=1: every system is treated as top-level with its host's external field (no hierarchy) -- the FG001 column becomes the
rival's, the headline H0 must FAIL (rc = 1).

SCOPE: the record's statistics as committed (their conventions, their samples, their error models); class assignments are
FG001's rule, not fitted per object; Upsilon_V = 2 (h43's) throughout; no new data.  kappa = 1/2 fitted, both footings.
Run: python3 campaign_fresh_gravity/CFG7_hierarchy_fg001.py   (MUTATE=1 for the control; ~10 s)
"""
import os, sys, math, csv, json, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG7_hierarchy_fg001", MUTATE)
P, check = R.P, R.check
P(__doc__.split("SCOPE:")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: no hierarchy -- every system is top-level with its host's external field; H0 must FAIL ***")

G, kpc, Msun, A0H = HL.G, HL.kpc, HL.Msun, HL.A0                                          # h43/f13's own constants
XR = os.path.join(C.REPO, "real_research", "cross_thread_review_2026_09_26")
DSPH = os.path.join(C.REPO, "real_research", "data", "dsph")
nu_s = HL.nu_s
GATES = {}                                                                                  # gate -> {foot: (z_FG001, z_rival)}


def gate(name, foot, z_fg, z_rv, note=""):
    GATES.setdefault(name, {})[foot] = dict(fg001=z_fg, rival=z_rv, note=note)


# ================================================================================================ K1 h43 reproduced
R.banner("K1  CONTROL: h43's LG dwarf-dispersion medians reproduced (its estimator, samples and constants)")
MW_MB, M31_MB, UPS_V = 6.0e10, 1.2e11, 2.0


def a_int(gNi, gNe, a0):
    nt = nu_s((gNi + gNe) / a0)
    ne = nu_s(gNe / a0) if gNe > 0 else 0.0
    return gNi * nt + gNe * (nt - ne)


def sigma_pred(Mb, rh_pc, Dh_kpc, Mhost, a0, efe=True):
    Mh = 0.5 * Mb * Msun; rh = rh_pc * 3.0857e16; gNi = G * Mh / rh ** 2
    if not efe or Mhost is None or Dh_kpc is None or Dh_kpc <= 0:
        return math.sqrt(a_int(gNi, 0.0, a0) * rh / 3.0) / 1e3
    gNe = G * Mhost * Msun / (Dh_kpc * kpc) ** 2
    return math.sqrt(a_int(gNi, gNe, a0) * rh / 3.0) / 1e3


def sigma_newt(Mb, rh_pc):
    return math.sqrt(G * (0.5 * Mb * Msun) / (3 * rh_pc * 3.0857e16)) / 1e3


def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def load_lvd(fname, host_mb, host_name):
    out = []
    for r in csv.DictReader(open(os.path.join(DSPH, fname))):
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
        rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
        if sig is None or ul is not None or MV is None or rh is None or Dh is None or sig <= 0:
            continue
        em = fnum(r["vlos_sigma_em"]) or 0.2 * sig; ep = fnum(r["vlos_sigma_ep"]) or 0.2 * sig
        MHI = fnum(r["mass_HI"])
        out.append(dict(name=r["name"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, D=Dh, sig=sig, esig=0.5 * (em + ep),
                        MHI=(10 ** MHI if MHI is not None else 0.0), host_mb=host_mb))
    return out


def load_field():
    out = []
    for r in csv.DictReader(open(os.path.join(DSPH, "lvd_dwarf_local_field.csv"))):
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
        rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        MHI = fnum(r["mass_HI"])
        rec = dict(name=r["name"], MV=MV, LV=(10 ** (0.4 * (4.83 - MV)) if MV is not None else None), rh=rh, D=None, sig=sig,
                   MHI=(10 ** MHI if MHI is not None else None), host_mb=None, has_sig=(sig is not None and ul is None and sig > 0
                                                                                           and MV is not None and rh is not None))
        out.append(rec)
    return out


mw = load_lvd("lvd_dwarf_mw.csv", MW_MB, "MW"); m31 = load_lvd("lvd_dwarf_m31.csv", M31_MB, "M31")
FIELD_ALL = load_field()
fld = [dict(d, MHI=(d["MHI"] or 0.0)) for d in FIELD_ALL if d["has_sig"]]
col = []
for line in open(os.path.join(DSPH, "collins2013_m31_dsph.tsv"), encoding="latin-1"):
    if line.startswith("#") or not line.strip():
        continue
    f = line.split("\t")
    if len(f) < 25 or not f[0].strip().isdigit():
        continue
    try:
        MV = float(f[7]); rh = float(f[8]); Dist = float(f[11]); sig = float(f[18]); Esig = float(f[19]); esig = float(f[21])
    except ValueError:
        continue
    if sig <= 0:
        continue
    col.append(dict(name=f[1].strip(), MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, D_helio=Dist, sig=sig, esig=0.5 * (Esig + esig),
                    MHI=0.0, host_mb=M31_MB, ra=f[5].strip(), dec=f[6].strip()))


def sph2cart(ra_hms, dec_dms, d):
    h, m, s = [float(x) for x in ra_hms.split()]; ra = (h + m / 60 + s / 3600) * 15.0
    sgn = -1.0 if dec_dms.strip().startswith("-") else 1.0
    dd, dm, ds = [abs(float(x)) for x in dec_dms.replace("+", "").replace("-", "").split()]
    dec = sgn * (dd + dm / 60 + ds / 3600)
    ra, dec = math.radians(ra), math.radians(dec)
    return np.array([d * math.cos(dec) * math.cos(ra), d * math.cos(dec) * math.sin(ra), d * math.sin(dec)])


M31_XYZ = sph2cart("00 42 44.3", "+41 16 09", 785.0)
for d in col:
    d["D"] = float(np.linalg.norm(sph2cart(d["ra"], d["dec"], d["D_helio"]) - M31_XYZ))
ufd = [d for d in mw if d["MV"] > -7.7]; cls = [d for d in mw if d["MV"] <= -7.7]


def resid(sample, a0, efe=True, newt=False, extra_mass=None):
    out = []
    for d in sample:
        Mb = UPS_V * d["LV"] + 1.33 * d["MHI"]
        if extra_mass is not None:
            Mb = Mb + extra_mass(d)
        rh = (4.0 / 3.0) * d["rh"]
        sp = sigma_newt(Mb, rh) if newt else sigma_pred(Mb, rh, d.get("D"), d["host_mb"], a0, efe)
        out.append(math.log10(d["sig"] / sp))
    return np.array(out)


REF43 = {("canonical", "ufd"): (0.825, 0.355, 1.108), ("canonical", "cls"): (0.320, 0.067, 0.616), ("canonical", "mw"): (0.660, 0.303, 1.048),
         ("canonical", "col"): (0.480, 0.226, 0.853), ("canonical", "m31"): (0.381, 0.116, 0.714),
         ("alt", "ufd"): (0.806, 0.334, 1.108), ("alt", "cls"): (0.302, 0.047, 0.616), ("alt", "mw"): (0.642, 0.283, 1.048),
         ("alt", "col"): (0.461, 0.207, 0.853), ("alt", "m31"): (0.363, 0.096, 0.714)}
REF43_FIELD = {"canonical": -0.044, "alt": -0.062}
SAMPLES = {"ufd": ufd, "cls": cls, "mw": mw, "col": col, "m31": m31}
LABEL = {"ufd": "MW ultra-faint", "cls": "MW classical dSph", "mw": "MW all", "col": "M31 Collins+2013", "m31": "M31 LVD"}
SAT = {}
dev1 = 0.0
for foot, a0 in A0H.items():
    for key, smp in SAMPLES.items():
        re_, ri_, rn_ = resid(smp, a0), resid(smp, a0, efe=False), resid(smp, a0, newt=True)
        med = (float(np.median(re_)), float(np.median(ri_)), float(np.median(rn_)))
        ref = REF43[(foot, key)]
        dev1 = max(dev1, max(abs(round(a, 3) - b) for a, b in zip(med, ref)))
        SAT[(foot, key)] = dict(n=len(smp), med_efe=med[0], med_iso=med[1], med_newt=med[2], rms_efe=float(re_.std()),
                                rms_iso=float(ri_.std()), resid_iso=ri_.tolist(), resid_efe=re_.tolist())
        P(f"    {foot:9s} {LABEL[key]:18s} N={len(smp):3d}: EFE {med[0]:+.3f} (h43 {ref[0]:+.3f}) | isolated {med[1]:+.3f} ({ref[1]:+.3f}) | "
          f"Newton {med[2]:+.3f} ({ref[2]:+.3f})")
    rf = float(np.median(resid(fld, a0, efe=False)))
    dev1 = max(dev1, abs(round(rf, 3) - REF43_FIELD[foot]))
    SAT[(foot, "field")] = dict(n=len(fld), med_iso=rf, rms_iso=float(resid(fld, a0, efe=False).std()))
    P(f"    {foot:9s} isolated LG field dwarfs N={len(fld)}: isolated {rf:+.3f} (h43 {REF43_FIELD[foot]:+.3f})")
check("K1 CONTROL: h43's committed medians (EFE / isolated / Newtonian for five samples, and the isolated field dwarfs) reproduced "
      "to 0.001 dex on both footings", f"max |dev| = {dev1:.4f} dex", dev1 <= 0.0011)

# ================================================================================================ K2 f13 reproduced
R.banner("K2  CONTROL: f13's outer-halo globular-cluster medians reproduced (Baumgardt catalogue, its prescription)")


def num13(s):
    s = s.strip()
    if not s or s == "-":
        return float("nan")
    exp = 0.0
    if "·" in s:
        base_part, _, tail = s.partition("·")
        te = re.search(r"10\s*(\d+)", tail.replace(" ", ""))
        if te:
            exp = float(te.group(1))
        s = base_part
    m = re.match(r"\s*([-+]?\d+\.?\d*)", s.strip())
    return float(m.group(1)) * 10.0 ** exp if m else float("nan")


GCF = os.path.join(C.REPO, "real_research", "data", "globular_clusters", "baumgardt_gc_parameters.tsv")
gcs = []
with open(GCF, encoding="latin-1") as fh:
    header = None
    for line in fh:
        if line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if header is None:
            header = parts; continue
        if len(parts) < 23:
            continue
        d = dict(zip(header, parts))
        try:
            M = num13(d["Mass[Msun]"]) * Msun; Rgc = num13(d["R_GC[kpc]"]) * kpc
            rhm = num13(d["rh_m[pc]"]) * 3.0857e16; sig0 = num13(d["sigma0[km/s]"]); MLV = num13(d["M/L_V"])
        except Exception:
            continue
        if not all(np.isfinite(x) for x in (M, Rgc, rhm, sig0)) or M <= 0 or rhm <= 0 or Rgc <= 0:
            continue
        try:
            nrv_ = num13(d.get("N_RV", ""))
        except Exception:
            nrv_ = float("nan")
        gcs.append(dict(name=d["ClusterName"].split("  ")[0].strip(), M=M, Rgc=Rgc, rhm=rhm, sig0=sig0, MLV=MLV,
                        nrv=int(nrv_) if np.isfinite(nrv_) else 0))
MW_VC = 233e3
for r in gcs:
    r["g_int"] = G * r["M"] / (2 * r["rhm"] ** 2); r["g_ext"] = MW_VC ** 2 / r["Rgc"]


def pred_sigma13(r, a0, efe=True, boost_only=False):
    gN = r["g_int"]
    boost = nu_s((r["g_ext"] + gN) / a0) if efe else nu_s(gN / a0)
    if boost_only:
        return boost
    return math.sqrt(max(0.4 * G * r["M"] * boost / r["rhm"], 0.0)) / 1e3


disc = [r for r in gcs if r["g_int"] < A0H["canonical"] and r["g_ext"] < A0H["canonical"] and np.isfinite(r["sig0"]) and r["sig0"] > 0]
rg13 = np.array([math.log10(pred_sigma13(r, A0H["canonical"], True) / r["sig0"]) for r in disc])
ri13 = np.array([math.log10(pred_sigma13(r, A0H["canonical"], False) / r["sig0"]) for r in disc])
P(f"    discriminating clusters: {len(disc)}; with the external field {np.median(rg13):+.3f} dex (f13 +0.302); without {np.median(ri13):+.3f} "
  f"(f13 +0.561)")
check("K2 CONTROL: f13's committed medians (+0.302 / +0.561 dex, 16 clusters) reproduced to 0.001 dex",
      f"N = {len(disc)}; {np.median(rg13):+.4f} / {np.median(ri13):+.4f}",
      len(disc) == 16 and abs(round(float(np.median(rg13)), 3) - 0.302) <= 0.001 and abs(round(float(np.median(ri13)), 3) - 0.561) <= 0.001)

# ================================================================================================ K3 XR27 recomputed
R.banner("K3  CONTROL: XR27's committed significances recomputed from its own committed numbers")
X27D = json.load(open(os.path.join(XR, "XR27_efe_disfavouring_results.json")))["numbers"]
X27F = json.load(open(os.path.join(XR, "XR27_efe_favouring_results.json")))["numbers"]
dw = X27D["dwarfs"]["inf"]["rows"]; cl = X27D["clusters"]["inf"]["rows"]
dev3 = 0.0
for k, v in dw.items():
    dev3 = max(dev3, abs(abs(v["slope"] - v["obs"]) / v["err"] - v["sigma"]))
for k, v in cl.items():
    dev3 = max(dev3, abs(abs(v["slope_scalar"] - v["obs"]) / v["err"] - v["sigma_scalar"]),
               abs(abs(v["zp_pred"] - v["zp_obs"]) / v["zp_err"] - v["zp_sigma"]))
P(f"    {len(dw)} LV-dwarf rows and {len(cl)} cluster rows: max |recomputed - committed| = {dev3:.2e} sigma")
check("K3 CONTROL: XR27's committed significances (LV dwarfs' statistic; cluster slope and zero point) recomputed from its own "
      "committed obs/err/prediction numbers to 0.01 sigma", f"max deviation {dev3:.2e}", dev3 <= 0.01)

# ================================================================================================ K4 FG041
R.banner("K4  CONTROL: FG041 (tidal dwarfs) is committed and passes its own controls")
J41 = json.load(open(os.path.join(HERE, "CFG7_tdg_fg041_results.json")))
check("K4 CONTROL: CFG7_tdg_fg041_results.json exists with 0 load-bearing failures (C1, C2, H1)",
      f"{J41['summary']['n_pass']}/{J41['summary']['n_checks']} pass, load-bearing failures {J41['summary']['load_bearing_failures']}",
      J41["summary"]["load_bearing_failures"] == 0)
N41 = J41["numbers"]

# ================================================================================================ H1 Cassini without xi
R.banner("H1  CASSINI WITHOUT xi: the Sun owns no phantom; the Milky Way's phantom tide at the Sun")
R0 = 8.2 * kpc
MD, RD, MBUL, ABUL, MGAS, RGAS = 4.5e10, 2.6, 0.9e10, 0.5, 1.2e10, 5.0                       # a standard MW baryon budget (Msun, kpc)


def M_exp(Md, Rd, R):
    x = R / (Rd * kpc)
    return Md * (1 - (1 + x) * math.exp(-x))


def gN_MW(R):
    M = M_exp(MD, RD, R) + M_exp(MGAS, RGAS, R) + MBUL * (R / kpc) ** 2 / (R / kpc + ABUL) ** 2
    return G * M * Msun / R ** 2


Q2_BOUND = 5.2e-27
CAS = {}
for foot, a0 in C.A0_SI.items():
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        gph = lambda R: (float(kf(gN_MW(R) / a0)) - 1.0) * gN_MW(R)
        dR = 0.01 * R0
        dgdR = (gph(R0 + dR) - gph(R0 - dR)) / (2 * dR)
        tide = max(abs(dgdR), gph(R0) / R0)
        gtot = gph(R0) + gN_MW(R0)
        CAS[(foot, kn)] = dict(g_N=gN_MW(R0), g_ph=gph(R0), v_c=math.sqrt(gtot * R0) / 1e3, tide=tide, ratio=Q2_BOUND / tide)
        P(f"    {foot:9s} {kn:8s}: g_N(R0) = {gN_MW(R0):.3e}, phantom g = {gph(R0):.3e} m/s^2 (v_c = {math.sqrt(gtot * R0) / 1e3:.0f} km/s); "
          f"phantom tide ~ {tide:.2e} s^-2 vs Cassini bound {Q2_BOUND:.1e}: margin {Q2_BOUND / tide:.1e}")
h1 = all(v["ratio"] >= 1e3 for v in CAS.values())
check("H1 CASSINI WITHOUT xi (FG029): under FG001 the Sun owns no phantom (it is embedded in the Milky Way), so the only "
      "non-Newtonian tide in the Solar System is the host's smooth phantom field -- below Cassini's 5.2e-27 s^-2 by >= 1e3",
      "; ".join(f"{k[0][:3]}/{k[1]}: tide {v['tide']:.1e}, margin {v['ratio']:.1e}" for k, v in CAS.items()), h1 and not MUTATE)
for f in C.FOOTS:
    # the rival needs the declared screening length xi (FP17/CFG4's M_* window) to pass Cassini; FG001 needs none
    gate("G1 Cassini (no screening constant)", f, 0.0 if not MUTATE else float("inf"), float("inf"),
         "FG001 passes with no xi; the rival passes only with the declared xi (M_* window), so it fails the no-constant gate")
R.num("H1", {f"{k[0]}|{k[1]}": v for k, v in CAS.items()})

# ================================================================================================ H2 globular clusters
R.banner("H2  OUTER-HALO GLOBULAR CLUSTERS (class E): Newtonian dynamical M/L_V against stellar populations")
UPS_LO, UPS_HI = 1.0, 2.5
GC = {}
for foot, a0 in A0H.items():
    dd = [r for r in gcs if r["g_int"] < a0 and r["g_ext"] < a0 and np.isfinite(r["sig0"]) and r["sig0"] > 0 and r["nrv"] >= 20
          and np.isfinite(r["MLV"]) and r["MLV"] > 0]
    ml_N = np.array([r["MLV"] for r in dd])
    boost = np.array([pred_sigma13(r, a0, True, boost_only=True) for r in dd])
    ml_law = ml_N / boost
    def zmed(x):
        med = float(np.median(x)); err = 1.2533 * float(np.std(x, ddof=1)) / math.sqrt(len(x))
        if UPS_LO <= med <= UPS_HI:
            return med, err, 0.0
        edge = UPS_LO if med < UPS_LO else UPS_HI
        return med, err, abs(med - edge) / err
    mN, eN, zN = zmed(ml_N); mL, eL, zL = zmed(ml_law)
    GC[foot] = dict(n=len(dd), names=[r["name"] for r in dd], ml_newton=ml_N.tolist(), boost=boost.tolist(), med_N=mN, err_N=eN, z_N=zN,
                    med_law=mL, err_law=eL, z_law=zL)
    P(f"    {foot:9s}: {len(dd)} discriminating clusters with N_RV >= 20 ({', '.join(r['name'] for r in dd)})")
    P(f"        Newtonian M/L_V median {mN:.2f} +- {eN:.2f} ({zN:.1f} sigma outside [{UPS_LO}, {UPS_HI}]); the law with the external field "
      f"(boost {np.median(boost):.2f}) needs M/L_V {mL:.2f} +- {eL:.2f} ({zL:.1f} sigma below {UPS_LO})")
    gate("G2 outer-halo globular clusters (M/L_V)", foot, zN if not MUTATE else zL, zL)
h2 = all(UPS_LO <= GC[f]["med_N"] <= UPS_HI for f in A0H) and all(GC[f]["med_law"] < UPS_LO for f in A0H)
check("H2 OUTER-HALO GLOBULAR CLUSTERS: the Newtonian dynamical M/L_V median lies in the stellar-population range [1.0, 2.5]; the "
      "law with the external field would need M/L_V below 1.0 (a stellar population with almost no low-mass stars)",
      "; ".join(f"{f}: Newton {GC[f]['med_N']:.2f}, law {GC[f]['med_law']:.2f} (N = {GC[f]['n']})" for f in A0H), h2 and not MUTATE)
R.num("H2", GC)

# ================================================================================================ H3 tidal dwarfs
R.banner("H3  TIDAL DWARFS (class E): FG041")
chiN41 = N41["H1"]["chi2_newton"]
for f in C.FOOTS:
    best_rival = min(N41["H2"][f"{f}|P2"]["chi_efe"], N41["H2"][f"{f}|nu_mono"]["chi_efe"])
    # express as sigma via the chi^2 tail for 6 dof
    from scipy.stats import chi2 as CHI2, norm
    zs = lambda c: float(norm.isf(CHI2.sf(c, 6) / 2)) if CHI2.sf(c, 6) < 1 else 0.0
    zN_ = zs(chiN41) if chiN41 > 6 else 0.0
    gate("G3 tidal dwarf galaxies (6, Lelli+15)", f, zN_ if not MUTATE else zs(best_rival), zs(best_rival))
    P(f"    {f:9s}: Newton chi^2 {chiN41:.2f} (6 TDGs) -> {zN_:.2f} sigma; the law with the host's field (best kernel, most favourable M_host) "
      f"chi^2 {best_rival:.2f} -> {zs(best_rival):.2f} sigma")
check("H3 TIDAL DWARFS: FG041's kill test passed (committed) -- the six TDGs are Newtonian, no MOND-like discrepancy",
      f"chi^2 {chiN41:.2f}; <M_dyn/M_bar> = {N41['H1']['mean_ratio']:.2f} +- {N41['H1']['err_mean_ratio']:.2f}", J41["checks"][2]["ok"] and not MUTATE)

# ================================================================================================ H4 satellites
R.banner("H4  SATELLITES (class A): the isolated law of their infall baryons, no external-field effect")
for foot in A0H:
    for key in ("cls", "m31", "col", "ufd"):
        s_ = SAT[(foot, key)]
        err_i = 1.2533 * s_["rms_iso"] / math.sqrt(s_["n"]); err_e = 1.2533 * s_["rms_efe"] / math.sqrt(s_["n"])
        zi, ze = abs(s_["med_iso"]) / err_i, abs(s_["med_efe"]) / err_e
        s_["z_iso"], s_["z_efe"] = zi, ze
        gname = {"cls": "G4 MW classical dSphs", "m31": "G5 M31 dwarfs (LVD)", "col": "G6 M31 dwarfs (Collins+13)",
                 "ufd": "G7 MW ultra-faints"}[key]
        gate(gname, foot, zi if not MUTATE else ze, ze)
        P(f"    {foot:9s} {LABEL[key]:18s} N={s_['n']:3d}: isolated {s_['med_iso']:+.3f} +- {err_i:.3f} ({zi:.1f} sigma) | "
          f"with the external field {s_['med_efe']:+.3f} +- {err_e:.3f} ({ze:.1f} sigma)")
h4 = all(SAT[(f, k)]["z_iso"] <= 2.0 for f in A0H for k in ("cls", "m31")) and all(SAT[(f, k)]["z_efe"] > 2.0 for f in A0H for k in ("cls", "m31"))
check("H4 SATELLITES: the isolated law (FG001's class A) puts the MW classical dSphs and the M31 LVD dwarfs within 2 sigma of zero on "
      "both footings, while the external-field column fails both",
      "; ".join(f"{f[:3]}/{k}: iso {SAT[(f, k)]['z_iso']:.1f} vs EFE {SAT[(f, k)]['z_efe']:.1f} sigma" for f in A0H for k in ("cls", "m31")),
      h4 and not MUTATE)

# ================================================================================================ H5 host statistics
R.banner("H5  THE HOST STATISTICS: class A predicts no dependence on the host's field")
H5 = {}
for foot in C.FOOTS:
    dws = [v for k, v in dw.items() if k.startswith(foot + "/")]
    zd_fg = abs(dws[0]["obs"]) / dws[0]["err"]; zd_rv = min(v["sigma"] for v in dws)
    cls_ = [v for k, v in cl.items() if k.startswith(foot + "/")]
    zs_fg = max(abs(v["obs"]) / v["err"] for v in cls_); zs_rv = min(min(v["sigma_scalar"], v["sigma_subtract"]) for v in cls_)
    zz_fg = max(abs(v["zp_obs"]) / v["zp_err"] for v in cls_); zz_rv = min(v["zp_sigma"] for v in cls_)
    H5[foot] = dict(dwarfs=(zd_fg, zd_rv), slope=(zs_fg, zs_rv), zero_point=(zz_fg, zz_rv))
    gate("G8 LV dwarfs' host statistic", foot, zd_fg if not MUTATE else zd_rv, zd_rv)
    gate("G9 cluster-infall BTFR slope", foot, zs_fg if not MUTATE else zs_rv, zs_rv)
    gate("G10 cluster-infall BTFR zero point", foot, zz_fg if not MUTATE else zz_rv, zz_rv)
    P(f"    {foot:9s}: LV dwarfs obs {dws[0]['obs']:+.4f} +- {dws[0]['err']:.4f} -> FG001 (0) {zd_fg:.2f} sigma; rival (best variant) {zd_rv:.2f}")
    P(f"               cluster slope obs {cls_[0]['obs']:+.4f} +- {cls_[0]['err']:.4f} -> FG001 {zs_fg:.2f} sigma (worst variant); rival (best) {zs_rv:.2f}")
    P(f"               cluster zero point obs {cls_[0]['zp_obs']:+.4f} +- {cls_[0]['zp_err']:.4f} -> FG001 {zz_fg:.2f} sigma; rival (best) {zz_rv:.2f}")
h5 = all(max(v["dwarfs"][0], v["slope"][0], v["zero_point"][0]) <= 2.0 for v in H5.values())
check("H5 THE HOST STATISTICS: the LV dwarfs' statistic and the cluster-infall BTFR slope and zero point are within 2 sigma of FG001's "
      "zero on both footings", "; ".join(f"{f[:3]}: dwarfs {v['dwarfs'][0]:.2f}, slope {v['slope'][0]:.2f}, zero point "
                                         f"{v['zero_point'][0]:.2f} sigma (rival best {v['dwarfs'][1]:.1f}/{v['slope'][1]:.1f}/{v['zero_point'][1]:.1f})"
                                         for f, v in H5.items()), h5 and not MUTATE)
R.num("H5", H5)

# ================================================================================================ H6 DF2 / DF4
R.banner("H6  NGC 1052-DF2 AND DF4 (class E): Newtonian")
DFD = [dict(name="NGC1052-DF2", LV=1.1e8, rh=2200.0 * 0.75), dict(name="NGC1052-DF4", LV=1.0e8, rh=1600.0 * 0.75)]
OBS = {"NGC1052-DF2": [("Danieli19", 8.5, 3.1, 2.3), ("Emsellem19", 10.8, 4.0, 3.2), ("u02 (8.5+-2.3)", 8.5, 2.3, 2.3)],
       "NGC1052-DF4": [("vanDokkum19", 4.2, 2.2, 4.4), ("u02 (4.2+-1.5)", 4.2, 1.5, 1.5)]}


def sig_of(B, sig, em, ep):
    e = em if B > 0 else ep
    return abs(B) / (2.0 * e / (sig * math.log(10)))


DF = {}
dfr = X27F["df2_df4"]["inf"]["rows"]
for d in DFD:
    for (on, s, em, ep) in OBS[d["name"]]:
        for dist in (13.0, 20.0, 22.1):
            f_ = dist / 20.0
            Mb = 2.0 * d["LV"] * f_ ** 2; rh = (4.0 / 3.0) * d["rh"] * f_
            sN = sigma_newt(Mb, rh)
            B = 2 * math.log10(s / sN)
            DF[(d["name"], on, dist)] = dict(sig_N=sN, z_N=sig_of(B, s, em, ep),
                                             z_rival={foot: dfr[f"{foot}/{d['name']}/{on}/{dist:g}Mpc/proj1"]["sigma"] for foot in C.FOOTS
                                                      if f"{foot}/{d['name']}/{on}/{dist:g}Mpc/proj1" in dfr})
for (nm, on, dist), v in DF.items():
    if dist == 20.0:
        P(f"    {nm} {on:16s} at {dist:g} Mpc: Newton {v['sig_N']:.2f} km/s -> {v['z_N']:.2f} sigma; the law (XR27) " +
          ", ".join(f"{k} {z:.2f}" for k, z in v["z_rival"].items()) + " sigma")
for foot in C.FOOTS:
    for nm, on, gn in (("NGC1052-DF2", "Danieli19", "G11 NGC 1052-DF2"), ("NGC1052-DF4", "vanDokkum19", "G12 NGC 1052-DF4")):
        v = DF[(nm, on, 20.0)]
        zr = v["z_rival"].get(foot, v["z_rival"].get("canonical"))
        gate(gn, foot, v["z_N"] if not MUTATE else zr, zr)
h6 = DF[("NGC1052-DF2", "Danieli19", 20.0)]["z_N"] <= 2 and DF[("NGC1052-DF4", "vanDokkum19", 20.0)]["z_N"] <= 2
check("H6 DF2 AND DF4: Newtonian (FG001 class E) within 2 sigma at 20 Mpc for the central measurements",
      f"DF2 (Danieli+19) {DF[('NGC1052-DF2', 'Danieli19', 20.0)]['z_N']:.2f} sigma, DF4 (van Dokkum+19) "
      f"{DF[('NGC1052-DF4', 'vanDokkum19', 20.0)]['z_N']:.2f} sigma; over all distances and measurements "
      f"{min(v['z_N'] for v in DF.values()):.2f}-{max(v['z_N'] for v in DF.values()):.2f}", h6 and not MUTATE)
R.num("H6", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in DF.items()})

# ================================================================================================ H7 the cost: Chae
R.banner("H7  THE COST: Chae's external-field fits in SPARC (D1, D2) against FG001's zero")
ch = X27F["chae"]["inf"]["3d"]; cs = X27F["chae_samples"]
zD1 = cs["median143"] / cs["err143"][0]
zD2 = ch["D2"]["fit_median"] / ch["D2"]["fit_err"][0]
for foot in C.FOOTS:
    gate("G13 Chae D1 (143 galaxies)", foot, zD1 if not MUTATE else ch["D1"]["z"], ch["D1"]["z"])
    gate("G14 Chae D2 (90 galaxies)", foot, zD2 if not MUTATE else ch["D2"]["z"], ch["D2"]["z"])
P(f"    D1: median fitted e = {cs['median143']:.3f} (-{cs['err143'][0]:.3f}/+{cs['err143'][1]:.3f}) vs FG001's 0: {zD1:.2f} sigma; the chain "
  f"(L -> infinity) predicts {ch['D1']['pred_median']:.3f} ({ch['D1']['z']:.2f} sigma)")
P(f"    D2: median fitted e = {ch['D2']['fit_median']:.3f} (-{ch['D2']['fit_err'][0]:.3f}) vs 0: {zD2:.2f} sigma; the chain's band contains it")
check("H7 (reported; pre-declared as a likely failure) THE COST: Chae's EFE fits against FG001's zero external field",
      f"D1 {zD1:.1f} sigma, D2 {zD2:.1f} sigma (CFG1 rates Chae's signal CONTESTED)", zD1 <= 2 and zD2 <= 2, load_bearing=False)

# ================================================================================================ H0 the scorecard
R.banner("H0  THE SCORECARD: gates G1-G14, FG001 against the law with the external field (pass = <= 2 sigma)")
SC = {}
for foot in C.FOOTS:
    nf, nr = 0, 0
    for gname in sorted(GATES, key=lambda s: int(s.split()[0][1:])):
        v = GATES[gname][foot]
        pf, pr = v["fg001"] <= 2.0, v["rival"] <= 2.0
        nf += pf; nr += pr
        P(f"    {foot:9s} {gname:42s}: FG001 {v['fg001']:6.2f} {'pass' if pf else 'FAIL'} | rival {v['rival']:6.2f} {'pass' if pr else 'FAIL'}")
    SC[foot] = (nf, nr)
    P(f"    {foot:9s} TOTAL: FG001 passes {nf}/{len(GATES)}, the rival {nr}/{len(GATES)}")
SC_PHYS = {}
for foot in C.FOOTS:
    phys = [g for g in GATES if not g.startswith("G1 ")]
    SC_PHYS[foot] = (sum(GATES[g][foot]["fg001"] <= 2.0 for g in phys), sum(GATES[g][foot]["rival"] <= 2.0 for g in phys), len(phys))
    P(f"    {foot:9s} the {len(phys)} physical gates only (G1, the no-constant Cassini gate, left out): FG001 {SC_PHYS[foot][0]}, rival {SC_PHYS[foot][1]}")
R.num("SCORE_PHYSICAL", SC_PHYS)
h0 = all(SC[f][0] > SC[f][1] for f in C.FOOTS)
check("H0 [HEADLINE] FG001 passes strictly more of the gates G1-G14 than the law-with-external-field reading, on both footings",
      "; ".join(f"{f}: FG001 {v[0]}/{len(GATES)} vs rival {v[1]}/{len(GATES)}" for f, v in SC.items()), h0)
R.num("GATES", GATES); R.num("SCORE", SC); R.num("SAT", {f"{k[0]}|{k[1]}": {kk: vv for kk, vv in v.items() if not kk.startswith("resid")}
                                                       for k, v in SAT.items()})

# ================================================================================================ H8 fossil gas (exploratory)
R.banner("H8  (EXPLORATORY) THE FOSSIL-GAS ACCOUNT: satellites keep the cold component of their gas-rich infall baryons")
fg = [(math.log10(UPS_V * d["LV"]), math.log10(1.33 * d["MHI"] / (UPS_V * d["LV"]))) for d in FIELD_ALL
      if d["LV"] and d["MHI"] and d["MHI"] > 0]
if len(fg) >= 6:
    xs_, ys_ = np.array([a for a, b in fg]), np.array([b for a, b in fg])
    cf = np.polyfit(xs_, ys_, 1)
    fgas = lambda d: UPS_V * d["LV"] * 10 ** np.polyval(cf, math.log10(UPS_V * d["LV"]))
    P(f"    isolated LG field dwarfs with HI: {len(fg)}; log(M_gas/M_*) = {cf[0]:+.3f} log M_* {cf[1]:+.3f} (at M_* = 1e6/1e7: "
      f"{10 ** np.polyval(cf, 6):.2f}/{10 ** np.polyval(cf, 7):.2f})")
    FOS = {}
    for foot, a0 in A0H.items():
        for key in ("cls", "m31", "col", "ufd"):
            rr = resid(SAMPLES[key], a0, efe=False, extra_mass=fgas)
            FOS[(foot, key)] = float(np.median(rr))
            P(f"    {foot:9s} {LABEL[key]:18s}: isolated law of (stars + the gas an isolated dwarf of that M_* holds): median "
              f"{np.median(rr):+.3f} dex (stars only {SAT[(foot, key)]['med_iso']:+.3f})")
    moved = all(abs(FOS[(f, k)]) < abs(SAT[(f, k)]["med_iso"]) for f in A0H for k in ("cls", "m31", "col", "ufd"))
    check("H8 (reported, exploratory) the fossil-gas account moves every satellite sample's isolated-law offset toward zero, with the "
          "gas fraction taken from the isolated field dwarfs (no fitted constant)",
          "; ".join(f"{f[:3]}/{k}: {SAT[(f, k)]['med_iso']:+.3f} -> {FOS[(f, k)]:+.3f}" for f in A0H for k in ("cls", "m31", "col", "ufd")),
          moved, load_bearing=False)
    R.num("H8", dict(gas_fit=list(cf), n=len(fg), offsets={f"{k[0]}|{k[1]}": v for k, v in FOS.items()}))

# ================================================================================================ verdict
R.banner("VERDICT")
P(f"    FG001 (the phantom belongs to the top-level system; accreted systems keep their infall cold component; systems formed "
  f"embedded are Newtonian) passes {SC['canonical'][0]}/{len(GATES)} of the record's own population gates (canonical; "
  f"{SC['alt'][0]}/{len(GATES)} alt) against {SC['canonical'][1]}/{len(GATES)} for the law with the external field.  Constant ledger: xi "
  f"(the Solar-System screening length) is not needed (-1); nothing is added (the ownership rule is FG001's principle; the retained "
  f"cold component is CFG4's T5).  Its cost: Chae's external-field fits in SPARC ({zD1:.1f}/{zD2:.1f} sigma against zero; contested).")
nf_ = R.write()
sys.exit(1 if nf_ else 0)
