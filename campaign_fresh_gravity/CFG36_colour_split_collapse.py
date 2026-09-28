#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG36 -- CFG35's conservation rule with MEASURED, colour-split collapse masses: can it fit the X-ray ellipticals AND leave the massive
spirals alone?

WHY.  CFG35 derived T5's conservation form from T4 (the cold mass is fixed at collapse; the leftover after the law's phantom stays as
collapse debris).  With a colour-blind stellar-to-halo relation (Moster+13) it closed the X-ray ellipticals (0.1 sigma) but broke the most
massive SPARC spirals (+0.30 dex in v at R_HI), because it put every log M_* ~ 11.4 galaxy in a ~1e14 Msun collapse.  Weak lensing
measures the collapse mass separately by colour: Mandelbaum+2016 (MNRAS 457, 3200, Table 3; real_research/data/
mandelbaum2016_lbg_halo_mass.tsv) find passive centrals in halos 3-7x more massive than star-forming ones at the same stellar mass.
That is measured, not fitted, and it is the one input CFG35 said was missing.

THE METHOD (declared before this script's first run).  CFG35's machinery exec'd read-only (the conservation form, the edge at x_e =
0.40, h10's ellipticals, h48's Dutton-Maccio NFW, SPARC from the master table with M_* = 0.61 L_3.6 + 1.33 M_HI).  Collapse mass:
Mandelbaum's <M_200m> (h^-1 Msun, h = 0.673) interpolated in log M_* (clamped at the table's ends), converted to M_200c on the same
NFW (Dutton-Maccio c) by solving for the mass inside 200 x the mean density.  Colour: the seven X-ray ellipticals take the RED relation;
SPARC late types (T >= 1) take the BLUE relation and its S0s (T = 0) the RED.  Stellar masses: Humphrey's Kroupa and SPARC's 3.6-micron
masses stand in for Mandelbaum's Chabrier masses (declared).

PRE-DECLARED
  C1  CONTROL  the table reproduced: 14 rows; the red-blue gap at log M_* = 11.29 / 11.28 is 13.25 - 12.69 = 0.56 dex.
  C2  CONTROL  the 200m -> 200c conversion: the NFW mass inside the solved R_200m equals the target to 1e-6.
  H1  THE ELLIPTICALS STAY CLOSED with the red relation: the conservation form fits the seven at better than 1 sigma (CFG35's error
      model), both footings.
  H2  [HEADLINE; MUTATE must fail] THE SPIRALS ARE LEFT ALONE with the blue relation: over SPARC the leftover is zero in >= 90% of
      galaxies and raises v_c at R_HI by < 0.03 dex in every galaxy (canonical, x_e = 0.40).
  R1-R3 (reported): the edge window's ends; H2 with every blue halo mass at its +1 sigma bound; the largest SPARC leftovers.
  READING (declared): H1 and H2 PASS -> with measured colour-split collapse masses, B's derived conservation rule fits massive
  ellipticals and massive spirals together; B adopts it.  H2 FAIL -> even the measured split cannot keep the spirals clean.  H1 FAIL
  -> the red relation's collapse masses do not supply the ellipticals.
CHANGED AFTER THE FIRST MUTATE RUN, BEFORE THE MAIN RUN (disclosed): clamping the table at its low end gave dwarfs (log M_* ~ 7) the
  collapse mass of a log M_* = 10.2 galaxy (~1e12 Msun) and would decide H2 by an artefact.  H2 is evaluated only over SPARC galaxies
  inside the table's measured range (log M_* >= 10.0); below it CFG35's colour-blind SHMR already gave f_ex = 0 for every dwarf.
MUTATE=1: the colours swapped (ellipticals blue, spirals red) -- H2 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG36_colour_split_collapse.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG36_colour_split_collapse", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: colours swapped -- H2 must FAIL ***")
FOOTS = ("canonical", "alt")

# CFG35's machinery, exec'd read-only with its own MUTATE off
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG35_cold_mass_conservation.py")).read()
g35 = {"__file__": os.path.join(HERE, "CFG35_cold_mass_conservation.py"), "__name__": "cfg35"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ C1")], "CFG35", "exec"), g35)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
GAL, M_hern, M_nfw_h10, edge_phantom, FB = g35["GAL"], g35["M_hern"], g35["M_nfw_h10"], g35["edge_phantom"], g35["FB"]
nfw_enclosed, G_, KPC, MSUN, A0SI, RADII, g10 = g35["nfw_enclosed"], g35["G_"], g35["KPC"], g35["MSUN"], g35["A0SI"], g35["RADII"], g35["g10"]
RHO_C = g35["g48"]["_RHO_C"]                                                   # Msun / Mpc^3 (h48's, H0 = 67.4)
OM = 0.315

# ================================================================================================ the table
T = [l.rstrip("\n").split("\t") for l in open(os.path.join(C.REPO, "real_research", "data", "mandelbaum2016_lbg_halo_mass.tsv")) if l.strip() and not l.startswith("#")]
TAB = {c: np.array([[float(r[1]), float(r[3]), float(r[4])] for r in T[1:] if r[0] == c]) for c in ("red", "blue")}
R.banner("C1  CONTROL: the table")
gap = float(TAB["red"][4, 1] - TAB["blue"][4, 1])
check("C1 CONTROL: Mandelbaum+2016 Table 3 as transcribed: 14 rows; red - blue at log M_* ~ 11.29 = 0.56 dex",
      f"{len(T) - 1} rows; gap {gap:.2f} dex", len(T) - 1 == 14 and abs(gap - 0.56) < 1e-9)


def m200c_from_m200m(M200m):
    """Msun -> Msun: the 200c mass of the Dutton-Maccio NFW whose mean density inside R_200m is 200 x the mean matter density."""
    def m200m_of(M200c):
        c = 10 ** (0.905 - 0.101 * (math.log10(M200c * 0.674) - 12.0))
        R200 = (3 * M200c / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.)
        m = lambda x: math.log1p(x) - x / (1 + x)
        lo, hi = R200, 10 * R200
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            dens = M200c * m(c * mid / R200) / m(c) / (4 * math.pi / 3 * mid ** 3)
            lo, hi = (mid, hi) if dens > 200 * OM * RHO_C else (lo, mid)
        return M200c * m(c * lo / R200) / m(c)
    lo, hi = math.log10(M200m) - 1, math.log10(M200m)
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if m200m_of(10 ** mid) < M200m else (lo, mid)
    return 10 ** lo, m200m_of(10 ** lo)


def collapse(Ms, colour, sig=0.0):
    t = TAB[colour]
    lx = np.interp(math.log10(Ms), t[:, 0], t[:, 1] + sig * t[:, 2])
    return m200c_from_m200m(10 ** lx / 0.673)[0]


R.banner("C2  CONTROL: the 200m -> 200c conversion")
errs = [abs(m200c_from_m200m(M)[1] / M - 1) for M in (1e12, 1e13, 1e14)]
check("C2 CONTROL: the NFW mass inside the solved R_200m equals the target", f"max relative error {max(errs):.1e}; M200c/M200m at 1e12 / 1e13 / 1e14: "
      + ", ".join(f"{m200c_from_m200m(M)[0] / M:.3f}" for M in (1e12, 1e13, 1e14)), max(errs) < 1e-6)

COL_E = "blue" if MUTATE else "red"


def gal_offsets(g, foot, xe=0.40, ups="uk", radii=RADII):
    a0 = A0SI[foot]
    Mfit = g["uf"] * g["LK"]; Mdm = max(g["Mvir"] - Mfit, 1e9); Ms = g[ups] * g["LK"]
    Mh = collapse(g["uk"] * g["LK"], COL_E); Mc = (1 - FB) * Mh
    fex = max(0.0, 1.0 - edge_phantom(Ms, foot, xe) / Mc)
    out = []
    for r in radii:
        Mtot = M_hern(r, Mfit, g["Re"]) + M_nfw_h10(r, Mdm, g["Rvir"], g["c"])
        Mb = M_hern(r, Ms, g["Re"]); gb = G_ * Mb * MSUN / (r * KPC) ** 2
        out.append(math.log10(Mtot / (float(C.nu_mono(np.array([gb / a0]))[0]) * Mb + fex * (1 - FB) * float(nfw_enclosed(Mh, r)))))
    return float(np.median(out)), fex, Mh


def sample(foot, **kw):
    per = np.array([gal_offsets(g, foot, **kw)[0] for g in GAL])
    return dict(per=per, mean=float(per.mean()), err=float(per.std(ddof=1) / math.sqrt(len(per))))


# ================================================================================================ H1
R.banner("H1  THE ELLIPTICALS with the red relation")
RES = {}
for f in FOOTS:
    b = sample(f); s = sample(f, ups="us"); r4 = sample(f, radii=(5.0, 10.0, 20.0, 40.0))
    tot = math.hypot(b["err"], math.hypot(s["mean"] - b["mean"], r4["mean"] - b["mean"]))
    RES[f] = dict(mean=b["mean"], tot=tot, z=b["mean"] / tot, per=b["per"].tolist(), x031=sample(f, xe=0.31)["mean"], x048=sample(f, xe=0.48)["mean"],
                  fex=[gal_offsets(g, f)[1] for g in GAL], Mh=[gal_offsets(g, f)[2] for g in GAL])
    P(f"    {f:9s}: " + ", ".join(f"{g['name']} {o:+.2f} (f_ex {x:.2f}, M200c {m:.1e})" for g, o, x, m in zip(GAL, b["per"], RES[f]["fex"], RES[f]["Mh"]))
      + f";  mean {b['mean']:+.3f} +- {tot:.3f} -> {RES[f]['z']:+.2f} sigma")
check("H1 THE ELLIPTICALS STAY CLOSED with the red relation: better than 1 sigma, both footings" + ("  [MUTATE: blue relation]" if MUTATE else ""),
      "; ".join(f"{f}: {v['mean']:+.3f} +- {v['tot']:.3f} ({v['z']:+.2f} sigma)" for f, v in RES.items()), all(abs(v["z"]) < 1 for v in RES.values()))

# ================================================================================================ H2 SPARC
R.banner("H2  THE SPIRALS with the blue relation")


def sparc(sig=0.0, xe=0.40):
    rows = []
    for name, m in g10["read_master"]().items():
        Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
        if Ms <= 0 or m["RHI"] <= 0 or math.log10(Ms) < 10.0:      # only where the colour split is MEASURED (the table's range)
            continue
        colour = ("blue" if m["T"] >= 1 else "red")
        if MUTATE:
            colour = "red" if colour == "blue" else "blue"
        Mh = collapse(Ms, colour, sig); Mc = (1 - FB) * Mh
        fex = max(0.0, 1.0 - edge_phantom(Mb, "canonical", xe) / Mc)
        r = m["RHI"]; gb = G_ * Mb * MSUN / (r * KPC) ** 2
        Mlaw = float(C.nu_mono(np.array([gb / A0SI["canonical"]]))[0]) * Mb
        rows.append((name, fex, 0.5 * math.log10(1 + fex * (1 - FB) * float(nfw_enclosed(Mh, r)) / Mlaw), math.log10(Ms), m["T"]))
    return rows


S0 = sparc(); fz = np.array([r_[1] for r_ in S0]); dv = np.array([r_[2] for r_ in S0])
frac0 = float(np.mean(fz == 0)); worst = sorted(S0, key=lambda t: -t[2])[:5]
check("H2 [HEADLINE] THE SPIRALS ARE LEFT ALONE with the blue relation: f_ex = 0 in >= 90% of SPARC and d log v at R_HI < 0.03 dex in every galaxy"
      + ("  [MUTATE: red relation]" if MUTATE else ""),
      f"{len(S0)} galaxies; f_ex = 0 in {100 * frac0:.0f}%; max d log v {dv.max():+.3f} dex; largest: "
      + ", ".join(f"{n} (T {t}, log M_* {l:.1f}, f_ex {x:.2f}, {d:+.3f})" for n, x, d, l, t in worst), frac0 >= 0.90 and dv.max() < 0.03)
S1 = sparc(sig=+1.0); dv1 = np.array([r_[2] for r_ in S1])
check("R1 (reported) H2 with every halo mass at its +1 sigma bound; the edge window's ends for the ellipticals",
      f"+1 sigma: f_ex = 0 in {100 * np.mean(np.array([r_[1] for r_ in S1]) == 0):.0f}%, max d log v {dv1.max():+.3f}; ellipticals x_e 0.31 / 0.48: "
      + "; ".join(f"{f} {v['x031']:+.3f} / {v['x048']:+.3f}" for f, v in RES.items()), True, load_bearing=False)
h1 = all(abs(v["z"]) < 1 for v in RES.values()); h2 = frac0 >= 0.90 and dv.max() < 0.03
reading = ("with measured colour-split collapse masses, B's derived conservation rule fits massive ellipticals and massive spirals together"
           if h1 and h2 else ("even the measured split cannot keep the spirals clean" if not h2 else
                              "the red relation's collapse masses do not supply the ellipticals"))
P(f"\n    READING (declared): {reading}")
R.num("RES", RES); R.num("SPARC", dict(n=len(S0), frac_fex0=frac0, max_dlogv=float(dv.max()), worst=worst, plus1sig_max=float(dv1.max())))
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
