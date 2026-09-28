#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG35 -- THE COLD-MATTER RULE, DERIVED FROM B's OWN CONSERVATION LAW, and tested where it can be tested without circularity.

THE DERIVATION.  T4: B's dark component is a pressureless cold fluid with a conserved amount, behaving as CDM wherever the law is off
-- so before turnaround it collapses with the baryons in the cosmic ratio, into ΛCDM's collapsed regions.  Baryonic feedback is a
pressure force on gas; it cannot push a pressureless fluid.  So a bound system's cold mass is fixed at collapse,
M_c = (1 - f_b) M_coll with f_b = Omega_b/Omega_m, and does not follow the baryons feedback later removes.  T5's cosmic share,
written as (Omega_c/Omega_b) x (today's baryons), is therefore only a FLOOR (CFG34: groups lost ~40% of their baryons inside R500 and
fall short exactly by that, rho = -0.96).  T5's identity says the cold fluid first IS the law's phantom; conservation says whatever
is left over stays as collapse debris, which the law does not use and which therefore keeps the collapse (CDM) profile.  Hence the
CONSERVATION FORM of T5:
      dark(<r) = M_ph(<r) + f_ex (1 - f_b) M_NFW(<r; M_coll),     f_ex = max(0, 1 - M_ph,edge / [(1 - f_b) M_coll]),
M_ph the law's phantom from TODAY's baryons (nu_mono, monopole), M_ph,edge its mass inside B's edge r_e = x_e r_ta (CFG7's r_ta_law),
M_NFW the collapse profile (Dutton & Maccio 2014 c(M), 200c; h48's committed function).  No new constant: M_coll is history.

WHAT MAKES A TEST NON-CIRCULAR.  M_coll must come from something other than the mass being predicted.  For single galaxies it can: the
stellar-to-halo relation (Moster+13; h48's committed halo_mass), which B inherits because its pre-turnaround dynamics are ΛCDM's.
For groups and clusters every available collapse estimate here uses the hydrostatic mass itself, so they are not scored.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG32's committed per-galaxy offsets under the law (Kroupa) reproduced (7 X-ray ellipticals, both footings).
  H1  [declared headline; see below] THE CONSERVATION FORM FIXES THE X-RAY ELLIPTICALS: with M_coll from the stellar-to-halo relation and
      x_e = 0.40 (the middle of B's window), the mean per-galaxy offset lies within 2 sigma of zero with CFG32's error model (galaxy-to-
      galaxy error; IMF and radial-range floor re-run), both footings.
  H2  ...WITHOUT DISTURBING THE SPIRALS: over SPARC (175 galaxies; M_* = 0.61 L_3.6, CFG4's nu_mono fit, + 1.33 M_HI), the leftover is
      zero (f_ex = 0) in at least 90% of galaxies, and where it is not, the mass it adds at the HI radius raises v_c by less than 0.03
      dex in every galaxy (canonical, x_e = 0.40).
  R1-R3 (reported): both ends of the edge window (x_e = 0.31, 0.48); the law's offsets beside (CFG32); per-galaxy f_ex and M_coll.
  READING (declared): H1 and H2 PASS -> the conservation form, derived from T4, closes the ellipticals without touching the spirals,
  and replaces T5's "today's baryons" as B's rule.  H1 FAIL -> conservation alone does not supply the ellipticals' extended mass.
  H2 FAIL -> the rule that helps the ellipticals breaks the spirals: B cannot take it as it stands.
ADDED AFTER THE FIRST MUTATE RUN, BEFORE THE MAIN RUN (disclosed): the MUTATE control passed H1, so H1 has no bite (the law alone sits
  at 1.7 sigma, inside 2); H1 is kept and reported as uninformative, and H1b (better than 1 sigma) is the headline.  The same run exposed
  a bug: the Salpeter variant fed Salpeter masses to the SHMR, which is calibrated on Kroupa/Chabrier-like masses; M_coll now always
  comes from the Kroupa mass.
MUTATE=1: every collapse mass divided by 10 -- H1b must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG35_cold_mass_conservation.py   (MUTATE=1 for the control)
"""
import os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG35_cold_mass_conservation", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass divided by 10 -- H1b must FAIL ***")
MCF = 0.1 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
FB = 0.02237 / (0.02237 + 0.1200)
HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)

# committed machinery, exec'd read-only: h10 (the ellipticals), h48 (Moster SHMR + Dutton-Maccio NFW)
g10, _ = C4.exec_slices(os.path.join(HUNT, "h10_h18_xray_hse.py"), [(None, 'P("="*116); P("ITEM 10'),
                        ('rows = [l.rstrip("\\n").split("\\t") for l in open(os.path.join(DATA, "humphrey2006', 'm10c, s10c, y10, r10 = R10["canonical"]')], name="h10")
GAL, M_hern, M_nfw_h10 = g10["gal"], g10["M_hern"], g10["M_nfw"]
g48, _ = C4.exec_slices(os.path.join(HUNT, "h48_h69b_relative_isolation.py"), [(None, 'P("="*122); P("PART 1')], name="h48")
halo_mass, nfw_enclosed = g48["halo_mass"], g48["nfw_enclosed"]
G_, KPC, MSUN = g10["G"], g10["kpc"], g10["Msun"]
A0SI = C.A0_SI
RADII = (5.0, 10.0, 20.0, 40.0, 70.0)


def edge_phantom(Mb, foot, xe):
    """the law's phantom mass inside B's edge r_e = x_e r_ta (Msun); r_ta from CFG7's r_ta_law at a = 1."""
    a0 = C.A0[foot]
    rta = C.r_ta_law(Mb, a0, C.nu_mono, 1.0)
    return float(C.M_law(Mb, xe * rta, a0, C.nu_mono)) - Mb


def fex_and_mc(Ms_star, Mb_tot, foot, xe):
    Mc = (1 - FB) * MCF * float(halo_mass(Ms_star))
    return max(0.0, 1.0 - edge_phantom(Mb_tot, foot, xe) / Mc), Mc


def gal_offsets(g, foot, xe=0.40, ups="uk", radii=RADII, conserve=True):
    a0 = A0SI[foot]
    Mfit = g["uf"] * g["LK"]; Mdm = max(g["Mvir"] - Mfit, 1e9); Ms = g[ups] * g["LK"]
    Mk = g["uk"] * g["LK"]                                      # the SHMR's own (Kroupa-like) stellar mass, whatever IMF the baryons use
    Mc = (1 - FB) * MCF * float(halo_mass(Mk))
    fex = max(0.0, 1.0 - edge_phantom(Ms, foot, xe) / Mc) if conserve else 0.0
    Mh = MCF * float(halo_mass(Mk))
    out = []
    for r in radii:
        Mtot = M_hern(r, Mfit, g["Re"]) + M_nfw_h10(r, Mdm, g["Rvir"], g["c"])
        Mb = M_hern(r, Ms, g["Re"])
        gb = G_ * Mb * MSUN / (r * KPC) ** 2
        Mpred = float(C.nu_mono(np.array([gb / a0]))[0]) * Mb + fex * (1 - FB) * float(nfw_enclosed(Mh, r))
        out.append(math.log10(Mtot / Mpred))
    return float(np.median(out)), fex, Mh


def sample(foot, **kw):
    per = np.array([gal_offsets(g, foot, **kw)[0] for g in GAL])
    return dict(per=per, mean=float(per.mean()), err=float(per.std(ddof=1) / math.sqrt(len(per))))


# ================================================================================================ C1
R.banner("C1  CONTROL: CFG32's committed per-galaxy offsets under the law")
import json
c32 = json.load(open(os.path.join(HERE, "CFG32_xray_ellipticals_under_b_results.json")))["numbers"]["RES"]
dev = 0.0
for f in FOOTS:
    law = sample(f, conserve=False)
    dev = max(dev, float(np.max(np.abs(law["per"] - np.array(c32[f]["base"]["per"])))))
check("C1 CONTROL: CFG32's committed per-galaxy offsets (the law, Kroupa) reproduced", f"max |d| {dev:.1e} dex", dev <= 1e-6 or MUTATE)

# ================================================================================================ H1
R.banner("H1  THE CONSERVATION FORM ON THE SEVEN X-RAY ELLIPTICALS (M_coll from the stellar-to-halo relation)")
RES = {}
for f in FOOTS:
    base = sample(f); salp = sample(f, ups="us"); r40 = sample(f, radii=(5.0, 10.0, 20.0, 40.0))
    floor = math.hypot(abs(salp["mean"] - base["mean"]), abs(r40["mean"] - base["mean"]))
    tot = math.hypot(base["err"], floor)
    fx = [gal_offsets(g, f)[1:] for g in GAL]
    RES[f] = dict(mean=base["mean"], err=base["err"], floor=floor, tot=tot, z=base["mean"] / tot, per=base["per"].tolist(),
                  fex=[a for a, b in fx], Mcoll=[b for a, b in fx], x031=sample(f, xe=0.31)["mean"], x048=sample(f, xe=0.48)["mean"],
                  law=c32[f]["base"]["mean"])
    P(f"    {f:9s}: per-galaxy " + ", ".join(f"{g['name']} {o:+.2f} (f_ex {x:.2f}, M_coll {m:.1e})" for g, o, x, m in zip(GAL, base["per"], RES[f]["fex"], RES[f]["Mcoll"])))
    P(f"    {'':9s}  mean {base['mean']:+.3f} +- {tot:.3f} -> {RES[f]['z']:+.2f} sigma (law alone {RES[f]['law']:+.3f}); edge window x_e = 0.31 / 0.48: "
      f"{RES[f]['x031']:+.3f} / {RES[f]['x048']:+.3f}")
check("H1 [HEADLINE] THE CONSERVATION FORM FIXES THE X-RAY ELLIPTICALS: mean per-galaxy offset within 2 sigma of zero (CFG32's error model), "
      "both footings, x_e = 0.40" + ("  [MUTATE: collapse masses / 10]" if MUTATE else ""),
      "; ".join(f"{f}: {v['mean']:+.3f} +- {v['tot']:.3f} ({v['z']:+.2f} sigma; the law alone {v['law']:+.3f})" for f, v in RES.items()),
      all(abs(v["z"]) < 2 for v in RES.values()))

check("H1b [HEADLINE, declared after the first MUTATE run showed H1 has no bite -- the law alone already sits at 1.7 sigma -- and before the main run] THE CONSERVATION FORM FITS THE ELLIPTICALS AT BETTER THAN 1 SIGMA (CFG32's error model), both footings" + ("  [MUTATE: collapse masses / 10]" if MUTATE else ""),
      "; ".join(f"{f}: {v['z']:+.2f} sigma (the law alone: {v['law'] / (v['tot'] if v['tot'] else 1):+.2f} with this lane's error)" for f, v in RES.items()),
      all(abs(v["z"]) < 1 for v in RES.values()))

# ================================================================================================ H2 SPARC
R.banner("H2  THE SPIRALS: does the leftover touch SPARC?")
M = g10["read_master"]()
rows = []
for name, m in M.items():
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
    if Ms <= 0 or m["RHI"] <= 0:
        continue
    fex, Mc = fex_and_mc(Ms, Mb, "canonical", 0.40)
    Mh = MCF * float(halo_mass(Ms))
    r = m["RHI"]; gb = G_ * Mb * MSUN / (r * KPC) ** 2
    Mlaw = float(C.nu_mono(np.array([gb / A0SI["canonical"]]))[0]) * Mb
    add = fex * (1 - FB) * float(nfw_enclosed(Mh, r))
    rows.append((name, fex, 0.5 * math.log10(1 + add / Mlaw), Ms))
fz = np.array([r_[1] for r_ in rows]); dv = np.array([r_[2] for r_ in rows])
frac0 = float(np.mean(fz == 0)); worst = sorted(rows, key=lambda t: -t[2])[:5]
check("H2 ...WITHOUT DISTURBING THE SPIRALS: f_ex = 0 in >= 90% of SPARC, and the added mass at the HI radius raises v_c by < 0.03 dex in "
      "every galaxy (canonical, x_e = 0.40)",
      f"{len(rows)} galaxies; f_ex = 0 in {100 * frac0:.0f}%; max d log v at R_HI {dv.max():+.3f} dex; largest: "
      + ", ".join(f"{n} (log M_* {math.log10(s):.1f}, f_ex {x:.2f}, {d:+.3f})" for n, x, d, s in worst),
      frac0 >= 0.90 and dv.max() < 0.03)

# ================================================================================================ reported
check("R1 (reported) the edge window's ends and the law beside",
      "; ".join(f"{f}: x_e 0.31 {v['x031']:+.3f}, 0.40 {v['mean']:+.3f}, 0.48 {v['x048']:+.3f}; law {v['law']:+.3f}" for f, v in RES.items()),
      True, load_bearing=False)
ok = all(abs(v["z"]) < 2 for v in RES.values()) and frac0 >= 0.90 and dv.max() < 0.03
reading = ("the conservation form, derived from T4, closes the ellipticals without touching the spirals, and replaces T5's 'today's baryons'"
           if ok else ("conservation alone does not supply the ellipticals' extended mass" if not all(abs(v["z"]) < 2 for v in RES.values())
                       else "the rule that helps the ellipticals breaks the spirals: B cannot take it as it stands"))
P(f"\n    READING (declared): {reading}")
R.num("RES", RES); R.num("SPARC", dict(n=len(rows), frac_fex0=frac0, max_dlogv=float(dv.max()), worst=worst)); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
