#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG42 -- B's derived cold-mass rule on the DWARFS: does the leftover collapse debris close the ultra-faint failure (CFG28-29: 3.5-3.8 sigma),
or does it over-predict the classical dwarfs?

WHY.  The rule (CFG35-39) says the cold fluid is conserved and keeps its collapse mass: dark = phantom + leftover collapse debris (an NFW shape
carrying f_ex (1 - f_b) M_collapse, f_ex = max(0, 1 - M_phantom,edge / [(1 - f_b) M_collapse])).  CFG36-41 tested it where a MEASURED collapse mass
exists (weak lensing, log M_* > 10.2).  It has never been applied to the satellites, where the largest standing failure of B sits: the Milky Way's
ultra-faints, whose measured dispersions are 0.30-0.33 dex above the isolated law of their stars (3.5-3.8 sigma, CFG28).  An NFW cusp has a property
that makes the answer nearly independent of the (unmeasured) halo mass: inside a small radius the enclosed mass scales only as M_halo^~0.13.  So the
rule makes a nearly parameter-free prediction for the ultra-faints.  The classical dwarfs are the other side of the same coin: with a full NFW
added to the law their dispersions could be over-predicted (the cusp problem).

THE METHOD (declared before this script's first run).  CFG36's machinery (exec'd read-only): the conservation form at x_e = 0.40, the Dutton-Maccio
NFW, nu_mono, both footings.  Collapse mass: the Moster+2013 stellar-to-halo relation of CFG35 (h48's halo_mass), at the satellite's M_* = Upsilon_V L_V
(Upsilon_V = 2, FG001's).  THE TRAP, declared: that function is CLAMPED at M_halo = 1e9 M_sun for M_* <~ 1.6e4 (its grid floor), so all ultra-faints
below that mass get 1e9; it is an extrapolation, not a measurement.  Sensitivity: the collapse mass of every satellite with M_* < 1e5 set to 1e8, 3e8,
1e9, 3e9, 1e10 (R1).  Estimator: FG001's (committed): sigma^2 = g(r) r / 3 at r = (4/3) r_half with the half of the baryons enclosed; the rule
adds G f_ex (1 - f_b) M_NFW(<r) / r^2 to g.  Baryons: M_* (+ current gas; for the classical satellites also the CFG18 infall gas, here the
deterministic expectation: the mean of the k = 5 nearest field-dwarf gas ratios, non-detections as zero).  Samples: FG001's MW ultra-faints (31
resolved, plus the 9 upper limits by Kaplan-Meier as in CFG28), MW classical dSphs (14), M31 Collins+13 (14), M31 LVD (34).  Offset = log10(sigma_obs /
sigma_pred).  Errors: the sample's error of the median (1.2533 rms / sqrt n; the bootstrap for the Kaplan-Meier median) plus a floor in quadrature: Upsilon_V
1 to 4 (half the shift of the median) and the collapse-mass floor variants above (half the range).

PRE-DECLARED
  C1  CONTROL  FG001's committed isolated medians (current stars) are reproduced for the four samples, both footings.
  C2  CONTROL  the rule is a strict addition: for f_ex = 0 the prediction equals FG001's, and the NFW piece is non-negative and monotone in radius.
  H1  [HEADLINE; MUTATE must fail] THE RULE CLOSES THE ULTRA-FAINT FAILURE: the Kaplan-Meier median offset (limits included), with the floor, is
      within 2 sigma of zero on both footings (the bare law's is +0.325 / +0.304, 3.8 / 3.5 sigma).
  H2  THE RULE DOES NOT OVER-PREDICT THE CLASSICAL SATELLITES: for the MW classical dSphs, M31 Collins+13 and M31 LVD, the median offset is not
      below -2 sigma on either footing (the floor included).
  H3  THE RULE BITES: f_ex > 0.5 for at least 80% of the ultra-faints.
  H4  THE RULE LEAVES SPARC DWARFS ALONE: over SPARC galaxies with log M_* < 10 (M_* = 0.61 L_3.6, R_HI, point mass), the rule raises v_c at R_HI by
      < 0.03 dex in at least 90% (CFG36's criterion, extended below the measured table's range where the Moster relation is used).
  R1-R3 (reported): the collapse-mass floor variants; the halo mass that would zero the ultra-faint offset (against Moster's); per-sample offsets and
      f_ex.
  READING (declared): H1, H2, H4 PASS -> B's derived rule closes B's largest failure without breaking the dwarfs; B adopts it everywhere.
      H1 PASS and H2 or H4 FAIL -> the rule fixes the ultra-faints by adding a cusp that the classical dwarfs reject (a double count): B needs a rule
      that switches off the debris where the phantom already supplies the mass.  H1 FAIL -> the debris is not enough.  H3 FAIL -> the ultra-faints do not test it.
MUTATE=1: every collapse mass divided by 100 -- H1 must FAIL (rc = 1).
CHANGED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed): control C2 first failed on a bug of mine -- its f_ex = 0 override (floor_mh) only reached
  satellites with M_* < 1e5, so the three classical dSphs it tested kept their rule.  The override now applies to every satellite (mh_all); the control's
  tolerance is unchanged.  No hypothesis or threshold changed.
Run: python3 campaign_fresh_gravity/CFG42_satellites_rule.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, csv, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG42_satellites_rule", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass / 100 -- H1 must FAIL ***")
MCF = 0.01 if MUTATE else 1.0
FOOTS = ("canonical", "alt")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG36_colour_split_collapse.py")).read()
g36 = {"__file__": os.path.join(HERE, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g36)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
edge_phantom, FB, nfw_enclosed = g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]
halo_mass = g36["g35"]["halo_mass"]
g10 = g36["g10"]

FGP = os.path.join(HERE, "CFG7_hierarchy_fg001.py")
ns = {"np": np, "math": math, "os": os, "csv": csv, "C": C, "HL": HL}
ns = C.C4.exec_slices(FGP, [("G, kpc, Msun, A0H = HL.G", "# ================================================================================================ K1 h43"),
                            ("MW_MB, M31_MB, UPS_V = 6.0e10", "REF43 = {")], ns=ns, name="fg001_slices")[0]
A0H, UPS_V, resid, a_int, G, Msun, fnum = ns["A0H"], ns["UPS_V"], ns["resid"], ns["a_int"], ns["G"], ns["Msun"], ns["fnum"]
SAMPLES = {"ufd": ns["ufd"], "cls": ns["cls"], "col": ns["col"], "m31": ns["m31"]}
LABEL = {"ufd": "MW ultra-faint", "cls": "MW classical dSph", "col": "M31 Collins+2013", "m31": "M31 LVD"}
FG = json.load(open(os.path.join(HERE, "CFG7_hierarchy_fg001_results.json")))["numbers"]

# the ultra-faint upper limits (as CFG28)
UL = []
for r in csv.DictReader(open(os.path.join(ns["DSPH"], "lvd_dwarf_mw.csv"))):
    ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if ul is None or MV is None or rh is None or Dh is None or MV <= -7.7:
        continue
    MHI = fnum(r["mass_HI"])
    UL.append(dict(name=r["name"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, D=Dh, sig_ul=ul, MHI=(10 ** MHI if MHI is not None else 0.0), host_mb=ns["MW_MB"]))

# infall gas calibration (CFG18's set; deterministic expectation)
CAL = []
for r in csv.DictReader(open(os.path.join(ns["DSPH"], "lvd_dwarf_local_field.csv"))):
    MV = fnum(r["M_V"]); mh = fnum(r["mass_HI"]); ul = fnum(r["mass_HI_ul"])
    if MV is None or (mh is None and ul is None):
        continue
    ms = UPS_V * 10 ** (0.4 * (4.83 - MV)); det = mh is not None
    CAL.append((math.log10(ms), 1.33 * 10 ** (mh if det else ul) / ms if det else 0.0))
CAL.sort(); LCAL = np.array([c[0] for c in CAL]); RAT = np.array([c[1] for c in CAL]); LO = LCAL.min()


def infall_gas(d):
    lm = math.log10(UPS_V * d["LV"])
    if lm < LO:
        return 0.0
    nn = np.argsort(np.abs(LCAL - lm))[:5]
    return float(RAT[nn].mean()) * UPS_V * d["LV"]


def sigma_rule(d, foot, ups=None, rule=True, floor_mh=None, gas=False, mh_all=None):
    a0 = A0H[foot]; ups = UPS_V if ups is None else ups
    Ms = ups * d["LV"]
    Mb = Ms + (max(1.33 * d["MHI"], infall_gas(d)) if gas else 1.33 * d["MHI"])
    rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
    g = a_int(G * 0.5 * Mb * Msun / rh ** 2, 0.0, a0)
    fex = 0.0
    if rule:
        Mh = float(halo_mass(UPS_V * d["LV"])) * MCF
        if floor_mh is not None and UPS_V * d["LV"] < 1e5:
            Mh = floor_mh * MCF
        if mh_all is not None:
            Mh = mh_all
        fex = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB) * Mh))
        g += G * fex * (1 - FB) * float(nfw_enclosed(Mh, rh_pc / 1000.0)) * Msun / rh ** 2
    return math.sqrt(g * rh / 3.0) / 1e3, fex


def offs(sample, foot, **kw):
    return np.array([math.log10(d["sig"] / sigma_rule(d, foot, **kw)[0]) for d in sample])


# ================================================================================================ C1 / C2
R.banner("C1 / C2  CONTROLS")
dev = 0.0
for foot in FOOTS:
    for key in ("cls", "m31", "col", "ufd"):
        dev = max(dev, abs(float(np.median(offs(SAMPLES[key], foot, rule=False))) - FG["SAT"][f"{foot}|{key}"]["med_iso"]))
check("C1 CONTROL: FG001's committed isolated medians (current stars) reproduced for the four samples, both footings", f"max |d| {dev:.1e}", dev <= 1e-9)
d0 = SAMPLES["ufd"][0]
same = all(abs(sigma_rule(d, "canonical", rule=False)[0] - sigma_rule(d, "canonical", rule=True, mh_all=1e-30)[0]) < 1e-9 * sigma_rule(d, "canonical", rule=False)[0] for d in SAMPLES["cls"][:3])
rr = [float(nfw_enclosed(1e10, x)) for x in (0.1, 0.3, 1.0, 3.0)]
check("C2 CONTROL: the rule is a strict addition (f_ex = 0 reproduces FG001's prediction); the NFW piece is non-negative and monotone in radius",
      f"f_ex=0 identical: {same}; NFW(<r) at 0.1/0.3/1/3 kpc for 1e10: " + ", ".join(f"{x:.2e}" for x in rr), same and all(x > 0 for x in rr) and rr == sorted(rr))


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


def ufd_stat(foot, rule=True, ups=None, floor_mh=None):
    x = offs(SAMPLES["ufd"], foot, rule=rule, ups=ups, floor_mh=floor_mh)
    xu = np.array([math.log10(d["sig_ul"] / sigma_rule(d, foot, rule=rule, ups=ups, floor_mh=floor_mh)[0]) for d in UL])
    return km_median(x, xu), x, xu


FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)
R.banner("H1 / H3  THE ULTRA-FAINTS")
UF = {}
for foot in FOOTS:
    for rule in (False, True):
        m, x, xu = ufd_stat(foot, rule)
        err = boot(x, xu)
        ups_var = [ufd_stat(foot, rule, ups=u)[0] for u in (1.0, 4.0)]
        f_ups = 0.5 * abs(ups_var[1] - ups_var[0])
        flo = [ufd_stat(foot, rule, floor_mh=fm)[0] for fm in FLOORS] if rule else [m]
        f_mh = 0.5 * (max(flo) - min(flo))
        tot = math.sqrt(err ** 2 + f_ups ** 2 + f_mh ** 2)
        UF[(foot, rule)] = dict(km=m, resolved_median=float(np.median(x)), err=err, f_ups=f_ups, f_mh=f_mh, tot=tot, z=m / tot, floors=flo)
        P(f"    {foot:9s} {'rule' if rule else 'law ':4s}: KM median {m:+.3f} (resolved-only median {np.median(x):+.3f}) +- {tot:.3f} (bootstrap {err:.3f}, "
          f"Upsilon {f_ups:.3f}, collapse-mass floor {f_mh:.3f}) -> {m / tot:+.2f} sigma")
fx = [sigma_rule(d, "canonical")[1] for d in SAMPLES["ufd"]]
frac = float(np.mean(np.array(fx) > 0.5))
h1 = all(abs(UF[(f, True)]["z"]) < 2 for f in FOOTS)
check("H1 [HEADLINE] THE RULE CLOSES THE ULTRA-FAINT FAILURE: KM median (limits included) within 2 sigma of zero, both footings" + ("  [MUTATE: collapse masses / 100]" if MUTATE else ""),
      "; ".join(f"{f}: law {UF[(f, False)]['km']:+.3f} ({UF[(f, False)]['z']:+.2f}), rule {UF[(f, True)]['km']:+.3f} ({UF[(f, True)]['z']:+.2f})" for f in FOOTS), h1)
check("H3 THE RULE BITES: f_ex > 0.5 for at least 80% of the ultra-faints", f"{100 * frac:.0f}% (median f_ex {np.median(fx):.2f})", frac >= 0.80)

# ================================================================================================ H2
R.banner("H2  THE CLASSICAL SATELLITES")
CL = {}
for key in ("cls", "col", "m31"):
    for foot in FOOTS:
        for rule in (False, True):
            x = offs(SAMPLES[key], foot, rule=rule, gas=True)
            ups = [offs(SAMPLES[key], foot, rule=rule, gas=True, ups=u) for u in (1.0, 4.0)]
            f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
            flo = [float(np.median(offs(SAMPLES[key], foot, rule=rule, gas=True, floor_mh=fm))) for fm in FLOORS] if rule else [float(np.median(x))]
            err = 1.2533 * float(np.std(x)) / math.sqrt(len(x)); tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
            CL[(key, foot, rule)] = dict(med=float(np.median(x)), tot=tot, z=float(np.median(x)) / tot, fex=float(np.median([sigma_rule(d, foot, gas=True)[1] for d in SAMPLES[key]])))
            P(f"    {LABEL[key]:18s} {foot:9s} {'rule' if rule else 'law ':4s}: median {np.median(x):+.3f} +- {tot:.3f} -> {np.median(x) / tot:+.2f} sigma"
              + (f"; median f_ex {CL[(key, foot, rule)]['fex']:.2f}" if rule else ""))
h2 = all(CL[(k, f, True)]["z"] > -2 for k in ("cls", "col", "m31") for f in FOOTS)
check("H2 THE RULE DOES NOT OVER-PREDICT THE CLASSICAL SATELLITES: median offset not below -2 sigma (MW classical, Collins+13, M31 LVD; both footings)",
      "; ".join(f"{LABEL[k]} {f[:3]} {CL[(k, f, True)]['med']:+.3f} ({CL[(k, f, True)]['z']:+.2f})" for k in ("cls", "col", "m31") for f in FOOTS), h2)

# ================================================================================================ H4 SPARC dwarfs
R.banner("H4  SPARC DWARFS")
rows = []
for name, m in g10["read_master"]().items():
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
    if Ms <= 0 or m["RHI"] <= 0 or not (math.log10(Ms) < 10.0):
        continue
    Mh = float(halo_mass(Ms)) * MCF
    fex = max(0.0, 1.0 - edge_phantom(Mb, "canonical", 0.40) / ((1 - FB) * Mh))
    r = m["RHI"]; gb = g10["G"] * Mb * g10["Msun"] / (r * g10["kpc"]) ** 2
    Mlaw = float(C.nu_mono(np.array([gb / A0H["canonical"]]))[0]) * Mb
    rows.append((name, fex, 0.5 * math.log10(1 + fex * (1 - FB) * float(nfw_enclosed(Mh, r)) / Mlaw), math.log10(Ms)))
fz = np.array([x[1] for x in rows]); dv = np.array([x[2] for x in rows])
h4 = float(np.mean(dv < 0.03)) >= 0.90
worst = sorted(rows, key=lambda t: -t[2])[:4]
check("H4 THE RULE LEAVES SPARC DWARFS ALONE: v_c at R_HI raised by < 0.03 dex in >= 90% of SPARC galaxies with log M_* < 10",
      f"{len(rows)} galaxies; f_ex > 0 in {int((fz > 0).sum())}; d log v < 0.03 in {100 * np.mean(dv < 0.03):.0f}%; max {dv.max():+.3f}; largest: "
      + ", ".join(f"{n} (log M_* {l:.1f}, f_ex {x:.2f}, {d:+.3f})" for n, x, d, l in worst), h4)

# ================================================================================================ reported
lm = {}
for foot in ("canonical",):
    needed = []
    for fm in np.logspace(7.5, 12, 19):
        m, _, _ = ufd_stat(foot, True, floor_mh=fm)
        needed.append((fm, m))
    zc = [(a, b) for (a, b) in needed]
    cross = None
    for (a1, b1), (a2, b2) in zip(zc[:-1], zc[1:]):
        if b1 >= 0 >= b2 or b1 <= 0 <= b2:
            cross = a1 + (a2 - a1) * (0 - b1) / (b2 - b1) if b2 != b1 else a1
    lm[foot] = (needed, cross)
check("R1 (reported) the ultra-faint KM median offset against the collapse mass set for every satellite with M_* < 1e5 (canonical)",
      "; ".join(f"{fm:.0e}: {m:+.3f}" for fm, m in lm["canonical"][0][::3]) + f"; zero near {lm['canonical'][1]:.1e}" if lm["canonical"][1] else
      "; ".join(f"{fm:.0e}: {m:+.3f}" for fm, m in lm["canonical"][0][::3]) + "; no zero crossing in range", True, load_bearing=False)
check("R2 (reported) the Moster relation's collapse mass for the ultra-faints (clamped at 1e9)",
      f"median M_h {np.median([float(halo_mass(UPS_V * d['LV'])) for d in SAMPLES['ufd']]):.1e}; log M_* range {min(math.log10(UPS_V * d['LV']) for d in SAMPLES['ufd']):.1f}-{max(math.log10(UPS_V * d['LV']) for d in SAMPLES['ufd']):.1f}", True, load_bearing=False)
reading = ("B's derived rule closes B's largest failure without breaking the dwarfs" if (h1 and h2 and h4 and frac >= 0.8) else
           ("the rule fixes the ultra-faints by adding a cusp that the dwarfs reject (a double count)" if (h1 and not (h2 and h4)) else
            ("the debris is not enough for the ultra-faints" if not h1 else "the ultra-faints do not test the rule")))
P(f"\n    READING (declared): {reading}")
R.num("UF", {f"{a}|{'rule' if b else 'law'}": v for (a, b), v in UF.items()}); R.num("CL", {f"{a}|{b}|{'rule' if c else 'law'}": v for (a, b, c), v in CL.items()})
R.num("H4", dict(n=len(rows), nfex=int((fz > 0).sum()), max=float(dv.max()), frac=float(np.mean(dv < 0.03)))); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
