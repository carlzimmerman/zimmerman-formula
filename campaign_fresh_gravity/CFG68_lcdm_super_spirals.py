#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG68 -- THE LCDM CONTROL FOR CFG40/CFG56: do standard halos, run through CFG56's exact machinery, reproduce the super spirals (Ogle+2019)?

Criteria frozen and committed before this script: campaign_fresh_gravity/CFG68_FROZEN_CRITERIA.md (commit 1808d8bee).  CFG56's galaxies, baryons (Hernquist bulge +
Freeman disc, gN_bd), radii, stat() and floor() are exec'd read-only from CFG56_super_spirals_bulge.py (its source up to the scoring loop `RES = {}`; its MUTATE
forced off).  LCDM enters only as new branches of the pred() hook that stat() and floor() call; the law's branches are untouched.
Comparator: v^2 = r [g_N,bar(r) + G M_dark(<r) / r^2],  M_dark(<r) = max(0, 1 - M_b / M_200c) M_NFW(<r; M_200c)  (the lensing M_200c taken as the total mass; the
galaxy's baryons counted once, in their observed disc and bulge).  HEADLINE M_200c = CFG36's collapse(M_*, 'blue') (Mandelbaum+2016 weak-lensing <M_200m>, blue
centrals, converted to M_200c); M_NFW = CFG36's nfw_enclosed (h48's Dutton-Maccio c_200c at z = 0).  M_* = 10^logMstars as tabulated, for the baryons and the halo
lookup (the +-0.2 dex floor shift moves both).  LCDM has no a0: one set of numbers.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  CFG56's own controls pass in the exec'd slice; before any mutation stat()/floor() reproduce CFG56's committed law numbers to 1e-6 (canonical mean
               +0.104625, sigma 0.062785, mean_9 +0.163638, z_9 2.3407; alt mean +0.090247, mean_9 +0.148809).
  C2  CONTROL  the exec'd collapse reproduces CFG36's committed red-relation M_200c for its seven X-ray ellipticals to 1e-6 relative; CFG36's 200m -> 200c
               identity holds to 1e-6.
  C3  CONTROL  nfw_enclosed(M, R_200c) = M to 1e-9 at M = 1e12 and 1e13 Msun (R_200c from the machinery's rho_c); the Moster inversion round-trips,
               moster_mstar(log halo_mass(M_*)) = M_*, to 1e-3 at log M_* = 11.2, 11.5, 11.7.
  H1  [HEADLINE; MUTATE must fail] LCDM with the blue relation fits the nine fastest: |z_9| < 2 (CFG56's error model as coded: the all-23 floor terms).
  H2  LCDM fits all 23: |z| < 2.
  R1-R6 (reported; they never change H1 or H2, R5 can only downgrade a pass):  R1 Moster+13 colour-blind (every statistic);  R2 the per-galaxy table;
      R3 the law's committed canonical and alt numbers beside LCDM's, and CFG56's three-clause H2 evaluated on LCDM;  R4 the halo brackets (blue M_200c at +1 sigma
      [collapse(sig=+1), the table's ep], at -1 sigma [the table's em], the full-M_200c halo, the (1 - f_b) M_200c halo);  R5 (leverage) the halo switched off;
      R6 z_9 with its floor terms recomputed as shifts of the nine-fastest mean, for LCDM and for the law.
  READING (declared in the frozen file): H1 PASS -> specific to the law (NON-DIAGNOSTIC if R5 also has |z_9| < 2; 'both lean the same way; only the law crosses
      2 sigma' if mean_9 > 0 and within sigma_9 of +0.164).  H1 FAIL, mean_9 > 0 -> generic.  H1 FAIL, mean_9 < 0 -> LCDM over-predicts where the law under-predicts.
      H2 PASS -> both fit the whole sample; H2 FAIL -> LCDM misses the whole sample where the law does not.  R1/R4 opposite H1 verdicts are named, never adopted.
MUTATE=1: every observed speed x 0.25, applied through CFG56's VF convention (so the same nine are selected) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG68_lcdm_super_spirals.py   (MUTATE=1 for the control)
"""
import os, sys, io, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG68_lcdm_super_spirals", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every observed speed x 0.25 (through CFG56's VF) -- H1 must FAIL ***")
VM = 0.25

# ------------------------------------------------------------------ CFG56's machinery, read-only (its own MUTATE forced off)
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG56_super_spirals_bulge.py")).read()
g56 = {"__file__": os.path.join(HERE, "CFG56_super_spirals_bulge.py"), "__name__": "cfg56"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("RES = {}")], "CFG56", "exec"), g56)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
GALS, stat, floor, pred56, gN_bd, gN_disc = g56["GALS"], g56["stat"], g56["floor"], g56["pred"], g56["gN_bd"], g56["gN_disc"]
collapse, nfw_enclosed, FB, G_, KPC, MSUN = g56["collapse"], g56["nfw_enclosed"], g56["FB"], g56["G_"], g56["KPC"], g56["MSUN"]
g36 = g56["g36"]
h48 = nfw_enclosed.__globals__                                                   # h48's namespace (the committed Moster SHMR + Dutton-Maccio NFW)
halo_mass, moster_mstar, RHO_C = h48["halo_mass"], h48["moster_mstar"], h48["_RHO_C"]
m200c_from_m200m, TAB = g36["m200c_from_m200m"], g36["TAB"]
BLUE_LO, BLUE_HI = float(TAB["blue"][0, 0]), float(TAB["blue"][-1, 0])       # the blue relation's measured log M_* range (clamped outside)
EMB = np.array([[float(r_[1]), float(r_[3]), float(r_[5])] for r_ in g36["T"][1:] if r_[0] == "blue"])   # logMs_eff, logM200m (h^-1), em
ROWS = {r_[0]: dict(zip(g56["H"], r_)) for r_ in g56["T"][1:]}                  # the paper's table (for logMdark; never an input)
NINE = {"OGC 0441", "OGC 0926", "2MFGC 08638", "2MASX J11232039+0018029", "OGC 1312", "2MFGC 12344", "OGC 1304", "2MASX J16184003+0034367", "OGC 0139"}
dname = lambda g: g["alt"] if g["alt"] != "-" else g["name"]


def collapse_em(Ms):
    """the blue relation at its -1 sigma bound with the table's em (CFG36's collapse(sig) applies ep to both signs); same interpolation and clamp."""
    lx = np.interp(math.log10(Ms), EMB[:, 0], EMB[:, 1] - EMB[:, 2])
    return m200c_from_m200m(10 ** lx / 0.673)[0]


LCDM = ("lcdm", "lcdm_moster", "lcdm_p1", "lcdm_m1", "lcdm_full", "lcdm_fb", "newton")


def halo(which, Ms, Mb, r):
    """(M_200c, M_dark(<r)) in Msun for the LCDM branches; 'newton' (R5) has no halo."""
    if which == "newton":
        return 0.0, 0.0
    if which == "lcdm_moster":
        Mh = float(halo_mass(Ms))
    elif which == "lcdm_p1":
        Mh = collapse(Ms, "blue", +1.0)
    elif which == "lcdm_m1":
        Mh = collapse_em(Ms)
    else:
        Mh = collapse(Ms, "blue")
    frac = {"lcdm_full": 1.0, "lcdm_fb": 1.0 - FB}.get(which, max(0.0, 1.0 - Mb / Mh))
    return Mh, frac * float(nfw_enclosed(Mh, r))


def pred(g, foot, model="bd", which="rule", colour=None, dMs=0.0, dMg=0.0, sig=0.0, dbt=0.0):
    """CFG56's pred for the law and the rule (untouched); the LCDM branches: CFG56's baryons with the same shifts, plus the halo.  Returns (v, M_200c, M_b)."""
    if which not in LCDM:
        return pred56(g, foot, model=model, which=which, colour=colour, dMs=dMs, dMg=dMg, sig=sig, dbt=dbt)
    Ms = 10 ** (g["lMs"] + dMs); Mg = 10 ** (g["lMg"] + dMg); Mb = Ms + Mg
    bt = min(max(g["BT"] + dbt, 0.0), 1.0)
    gn = gN_bd(Ms, Mg, g["Rd"], g["r"], bt, g["Reb"]) if model == "bd" else gN_disc(Mb, g["Rd"], g["r"], model)
    Mh, Md = halo(which, Ms, Mb, g["r"])
    gt = gn + G_ * Md * MSUN / (g["r"] * KPC) ** 2
    return math.sqrt(gt * g["r"] * KPC) / 1e3, Mh, Mb


g56["pred"] = pred                                                                # the hook stat() and floor() call; nothing else in CFG56 changes


def score(which, foot="canonical"):
    """CFG56's scoring loop, line for line (its tot / z / zs / zf); tot9 = the nine-fastest sigma it divides by."""
    s = stat(foot, which); mod, ms, mg = floor(foot, which)
    tot = math.sqrt(s["err"] ** 2 + mod ** 2 + ms ** 2 + mg ** 2)
    s.update(mod=mod, ms=ms, mg=mg, tot=tot, z=s["mean"] / tot, zs=s["slope"] / s["slope_se"], zf=s["fast_mean"] / math.hypot(s["fast_err"], math.hypot(mod, math.hypot(ms, mg))))
    s["tot9"] = math.hypot(s["fast_err"], math.hypot(mod, math.hypot(ms, mg)))
    return s


# ================================================================================================ C1 - C3 (before any mutation)
R.banner("C1  CONTROL: CFG56's own controls in the exec'd slice; its committed law numbers reproduced (before any mutation)")
c56 = json.load(open(os.path.join(HERE, "CFG56_super_spirals_bulge_results.json")))["numbers"]["RES"]
own = [(c["name"].split(":")[0], c["ok"]) for c in g56["R"].checks]
LAW0 = {f: score("law", f) for f in ("canonical", "alt")}
pairs = [("canonical", "mean"), ("canonical", "tot"), ("canonical", "fast_mean"), ("canonical", "zf"), ("alt", "mean"), ("alt", "fast_mean")]
dev = max(abs(LAW0[f][k] - c56[f"{f}|law"][k]) for f, k in pairs)
check("C1 CONTROL: CFG56's own controls pass in the exec'd slice; stat()/floor() reproduce CFG56's committed law numbers to 1e-6 (before any mutation)",
      "CFG56's controls: " + ", ".join(f"{n} {'PASS' if ok else 'FAIL'}" for n, ok in own)
      + f"; canonical mean {LAW0['canonical']['mean']:+.6f}, sigma {LAW0['canonical']['tot']:.6f}, mean_9 {LAW0['canonical']['fast_mean']:+.6f},"
        f" z_9 {LAW0['canonical']['zf']:.4f}; alt mean {LAW0['alt']['mean']:+.6f}, mean_9 {LAW0['alt']['fast_mean']:+.6f}; max |dev| from the committed JSON {dev:.1e}",
      len(own) == 3 and all(ok for _, ok in own) and dev < 1e-6)

R.banner("C2  CONTROL: CFG36's committed collapse masses; its 200m -> 200c identity")
c36 = json.load(open(os.path.join(HERE, "CFG36_colour_split_collapse_results.json")))["numbers"]["RES"]["canonical"]["Mh"]
mine = [collapse(gg["uk"] * gg["LK"], "red") for gg in g36["GAL"]]
rel36 = max(abs(a / b - 1) for a, b in zip(mine, c36))
ident = max(abs(m200c_from_m200m(M)[1] / M - 1) for M in (1e12, 1e13, 1e14))
check("C2 CONTROL: the exec'd collapse reproduces CFG36's committed red-relation M_200c for its seven X-ray ellipticals (1e-6 rel.); the 200m -> 200c identity (1e-6)",
      f"{len(mine)} ellipticals, max rel. dev. {rel36:.1e} (e.g. {g36['GAL'][0]['name']} {mine[0]:.4e} vs {c36[0]:.4e}); identity max rel. error {ident:.1e}",
      len(mine) == len(c36) == 7 and rel36 < 1e-6 and ident < 1e-6)

R.banner("C3  CONTROL: the NFW identity; the Moster inversion")
nfw_id = max(abs(float(nfw_enclosed(M, (3 * M / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0)) / M - 1) for M in (1e12, 1e13))
rt = max(abs(float(moster_mstar(math.log10(float(halo_mass(10 ** l))))) / 10 ** l - 1) for l in (11.2, 11.5, 11.7))
check("C3 CONTROL: nfw_enclosed(M, R_200c) = M (1e-9) at 1e12 and 1e13 Msun; moster_mstar(log halo_mass(M_*)) = M_* (1e-3) at log M_* = 11.2, 11.5, 11.7",
      f"NFW max |M(<R200c)/M - 1| = {nfw_id:.1e}; Moster round trip max rel. error {rt:.1e}", nfw_id < 1e-9 and rt < 1e-3)

# ================================================================================================ the mutation (after the controls)
if MUTATE:
    g56["VF"] = VM
    for gg in GALS:
        gg["v"] *= VM; gg["dv"] *= VM
VF = g56["VF"]
sel = sorted(dname(g) for g in GALS if g["v"] / VF > 340)

# ================================================================================================ H1 / H2
R.banner("H1 / H2  LCDM (blue relation; M_200c - M_b bookkeeping; no a0) ON THE 23 SUPER SPIRALS")
RES = {w: score(w) for w in LCDM}
LAWm = score("law", "canonical")                                                 # the law with the speeds as they stand in this run (= CFG56 unless MUTATE)
L, N5 = RES["lcdm"], RES["newton"]
P(f"    the nine fastest selected (v_obs > 340 km/s on the unmutated speeds): {', '.join(sel)}  [frozen list matched: {set(sel) == NINE}]")
P(f"    {'galaxy':>26s} {'logMb':>5s} {'r':>4s} {'r/Rd':>4s} {'v_obs':>5s} {'v_law':>6s} {'v_LCDM':>6s} {'off_law':>7s} {'off_LCDM':>8s} {'logM200c':>8s} {'clamp':>5s}"
  f" {'halo v2':>7s} {'logMdark(paper)':>15s} {'logMdark(LCDM)':>14s} {'logM200c(Moster)':>16s}")
TABLE = []
for g in GALS:
    Ms, Mg = 10 ** g["lMs"], 10 ** g["lMg"]; Mb = Ms + Mg
    gn = gN_bd(Ms, Mg, g["Rd"], g["r"], min(max(g["BT"], 0.0), 1.0), g["Reb"])
    Mh, Md = halo("lcdm", Ms, Mb, g["r"]); gd = G_ * Md * MSUN / (g["r"] * KPC) ** 2
    vl, vL = pred56(g, "canonical", which="law")[0], pred(g, "canonical", which="lcdm")[0]
    row = dict(name=dname(g), logMb=math.log10(Mb), r=g["r"], r_Rd=g["r"] / g["Rd"], v_obs=g["v"] / VF, v_law=vl, v_lcdm=vL,
               off_law=math.log10(g["v"] / vl), off_lcdm=math.log10(g["v"] / vL), logM200c=math.log10(Mh), clamped=bool(g["lMs"] > BLUE_HI or g["lMs"] < BLUE_LO),
               halo_share=gd / (gn + gd), logMdark_paper=float(ROWS[g["name"]]["logMdark"]), logMdark_lcdm=math.log10(Md),
               logM200c_moster=math.log10(float(halo_mass(Ms))), fast=bool(g["v"] / VF > 340))
    TABLE.append(row)
    P(f"    {row['name'][-26:]:>26s} {row['logMb']:5.2f} {row['r']:4.0f} {row['r_Rd']:4.1f} {row['v_obs']:5.0f} {vl:6.1f} {vL:6.1f} {row['off_law']:+7.3f} {row['off_lcdm']:+8.3f}"
      f" {row['logM200c']:8.2f} {'yes' if row['clamped'] else '':>5s} {row['halo_share']:7.2f} {row['logMdark_paper']:15.2f} {row['logMdark_lcdm']:14.2f} {row['logM200c_moster']:16.2f}"
      + ("   *nine" if row["fast"] else ""))


def line(tag, v):
    return (f"    {tag:34s} mean {v['mean']:+.3f} +- {v['tot']:.3f} (gal {v['err']:.3f}, model {v['mod']:.3f}, M* {v['ms']:.3f}, gas {v['mg']:.3f}) -> z {v['z']:+.2f};"
            f" slope {v['slope']:+.3f} +- {v['slope_se']:.3f} ({v['zs']:+.2f}); nine fastest {v['fast_mean']:+.3f} +- {v['tot9']:.3f} -> z_9 {v['zf']:+.2f}")


P("")
P(line("the law (this run's speeds)", LAWm))
for w, tag in (("lcdm", "LCDM headline (blue, M200c - Mb)"), ("lcdm_moster", "R1 LCDM Moster+13 (colour-blind)"), ("lcdm_p1", "R4 blue +1 sigma (ep)"),
               ("lcdm_m1", "R4 blue -1 sigma (em)"), ("lcdm_full", "R4 full M_200c halo"), ("lcdm_fb", "R4 (1 - f_b) M_200c halo"), ("newton", "R5 no halo (Newtonian baryons)")):
    P(line(tag, RES[w]))
h1 = abs(L["zf"]) < 2
h2 = abs(L["z"]) < 2
law9 = c56["canonical|law"]
check("H1 [HEADLINE] LCDM (blue relation) FITS THE NINE FASTEST: |z_9| < 2 (CFG56's error model as coded)" + ("  [MUTATE: v_obs x 0.25]" if MUTATE else ""),
      f"mean_9 {L['fast_mean']:+.3f} +- {L['tot9']:.3f} (gal {L['fast_err']:.3f}; floor model {L['mod']:.3f}, M* {L['ms']:.3f}, gas {L['mg']:.3f}) -> z_9 {L['zf']:+.2f};"
      f" the law (CFG56 committed): {law9['fast_mean']:+.3f} -> z_9 {law9['zf']:+.2f}", h1)
check("H2 LCDM FITS ALL 23: |z| < 2" + ("  [MUTATE: v_obs x 0.25]" if MUTATE else ""),
      f"mean {L['mean']:+.3f} +- {L['tot']:.3f} -> z {L['z']:+.2f}; the law (CFG56 committed): {c56['canonical|law']['mean']:+.3f} -> z {c56['canonical|law']['z']:+.2f}", h2)

# ================================================================================================ reported rows
M1 = RES["lcdm_moster"]
check("R1 (reported) Moster+13 colour-blind halo masses (same NFW, same bookkeeping)",
      f"mean {M1['mean']:+.3f} +- {M1['tot']:.3f} (z {M1['z']:+.2f}); slope {M1['slope']:+.3f} ({M1['zs']:+.2f}); nine fastest {M1['fast_mean']:+.3f} +- {M1['tot9']:.3f}"
      f" (z_9 {M1['zf']:+.2f}); median log M_200c Moster {np.median([t['logM200c_moster'] for t in TABLE]):.2f} vs blue {np.median([t['logM200c'] for t in TABLE]):.2f}",
      True, load_bearing=False)
nine = [t for t in TABLE if t["fast"]]
check("R2 (reported) the per-galaxy table (above); the nine fastest",
      f"LCDM offsets {min(t['off_lcdm'] for t in TABLE):+.3f} to {max(t['off_lcdm'] for t in TABLE):+.3f} (nine: {min(t['off_lcdm'] for t in nine):+.3f} to "
      f"{max(t['off_lcdm'] for t in nine):+.3f}); {sum(t['clamped'] for t in TABLE)} clamped; halo share of v^2 at r {min(t['halo_share'] for t in TABLE):.2f}-"
      f"{max(t['halo_share'] for t in TABLE):.2f}; log M_dark(<r) LCDM minus the paper's fitted logMdark: median {np.median([t['logMdark_lcdm'] - t['logMdark_paper'] for t in TABLE]):+.2f}"
      f" (nine: {np.median([t['logMdark_lcdm'] - t['logMdark_paper'] for t in nine]):+.2f})", True, load_bearing=False)
three = abs(L["z"]) < 2 and abs(L["zs"]) < 2 and abs(L["zf"]) < 2
check("R3 (reported) the law's committed numbers beside LCDM's; CFG56's three-clause H2 (mean, slope, nine fastest, each < 2 sigma) evaluated on LCDM",
      "; ".join(f"law {f}: mean {c56[f'{f}|law']['mean']:+.3f} ({c56[f'{f}|law']['z']:+.2f}), slope {c56[f'{f}|law']['slope']:+.3f} ({c56[f'{f}|law']['zs']:+.2f}),"
                f" nine {c56[f'{f}|law']['fast_mean']:+.3f} ({c56[f'{f}|law']['zf']:+.2f})" for f in ("canonical", "alt"))
      + f"; LCDM: mean {L['mean']:+.3f} ({L['z']:+.2f}), slope {L['slope']:+.3f} ({L['zs']:+.2f}), nine {L['fast_mean']:+.3f} ({L['zf']:+.2f});"
        f" CFG56's three-clause H2 on LCDM: {'PASS' if three else 'FAIL'}", True, load_bearing=False)
check("R4 (reported) the halo brackets: blue M_200c at +1 sigma (ep) and -1 sigma (em); the full-M_200c halo; the (1 - f_b) M_200c halo",
      "; ".join(f"{n}: mean {RES[w]['mean']:+.3f} (z {RES[w]['z']:+.2f}), nine {RES[w]['fast_mean']:+.3f} (z_9 {RES[w]['zf']:+.2f})"
                for n, w in (("+1 sigma", "lcdm_p1"), ("-1 sigma", "lcdm_m1"), ("full M_200c", "lcdm_full"), ("(1 - f_b) M_200c", "lcdm_fb"))),
      True, load_bearing=False)
check("R5 (reported; leverage) the halo switched off (Newtonian baryons only); if |z_9| < 2 here too, an H1 pass is non-diagnostic",
      f"mean {N5['mean']:+.3f} +- {N5['tot']:.3f} (z {N5['z']:+.2f}); nine fastest {N5['fast_mean']:+.3f} +- {N5['tot9']:.3f} (z_9 {N5['zf']:+.2f}); the halo moves mean_9 by "
      f"{N5['fast_mean'] - L['fast_mean']:+.3f} dex ({(N5['fast_mean'] - L['fast_mean']) / L['tot9']:.1f} sigma_9)", True, load_bearing=False)


def own9(which, foot="canonical"):
    """z_9 with its floor terms recomputed as shifts of the nine-fastest mean (CFG56's coded sigma_9 uses the all-23 floor terms)."""
    s = stat(foot, which)
    f9 = lambda **kw: stat(foot, which, **kw)["fast_mean"]
    m = [f9(dbt=d) for d in (-0.10, 0.0, +0.10)]
    mod = 0.5 * (max(m) - min(m)); ms = 0.5 * abs(f9(dMs=+0.2) - f9(dMs=-0.2)); mg = 0.5 * abs(f9(dMg=+0.3) - f9(dMg=-0.3))
    t = math.sqrt(s["fast_err"] ** 2 + mod ** 2 + ms ** 2 + mg ** 2)
    return dict(fast_mean=s["fast_mean"], mod9=mod, ms9=ms, mg9=mg, tot9=t, z9=s["fast_mean"] / t)


O9 = {w: own9(w) for w in ("lcdm", "law")}
check("R6 (reported) z_9 with its floor terms recomputed as shifts of the nine-fastest mean, for LCDM and for the law",
      "; ".join(f"{w}: {v['fast_mean']:+.3f} +- {v['tot9']:.3f} (model {v['mod9']:.3f}, M* {v['ms9']:.3f}, gas {v['mg9']:.3f}) -> z_9 {v['z9']:+.2f}" for w, v in O9.items()),
      True, load_bearing=False)

# ================================================================================================ the declared reading
LAW9 = c56["canonical|law"]["fast_mean"]
if h1:
    if abs(N5["zf"]) < 2:
        reading = "H1 PASS but NON-DIAGNOSTIC: the no-halo row also has |z_9| < 2, so the statistic cannot tell the measured halo from none"
    elif L["fast_mean"] > 0 and abs(L["fast_mean"] - LAW9) < L["tot9"]:
        reading = "H1 PASS: both models lean the same way; only the law crosses 2 sigma"
    else:
        reading = "H1 PASS: the super-spiral miss is SPECIFIC TO THE LAW -- standard LCDM with measured halo masses reproduces the nine fastest"
else:
    reading = ("H1 FAIL: the miss is GENERIC -- LCDM with a measured halo also under-predicts the fastest super spirals" if L["fast_mean"] > 0 else
               "H1 FAIL: LCDM OVER-PREDICTS where the law under-predicts -- the data lie between the two models, so the miss is not generic")
reading += ("; H2 PASS: both models fit the sample as a whole" if h2 else
            f"; H2 FAIL: LCDM misses the whole sample where the law does not ({'too slow' if L['mean'] > 0 else 'too fast'})")
flips = [n for n, w in (("the halo relation (R1 Moster)", "lcdm_moster"), ("the lensing error at these masses (R4 +1 sigma)", "lcdm_p1"),
                        ("the lensing error at these masses (R4 -1 sigma)", "lcdm_m1"), ("the bookkeeping (R4 full M_200c)", "lcdm_full"),
                        ("the bookkeeping (R4 (1 - f_b) M_200c)", "lcdm_fb")) if (abs(RES[w]["zf"]) < 2) != h1]
if flips:
    reading += "; the H1 verdict depends on " + ", ".join(flips)
P(f"\n    READING (declared): {reading}")

R.num("controls", dict(C1_dev=dev, C1_own=own, C2_rel=rel36, C2_identity=ident, C3_nfw=nfw_id, C3_moster=rt))
R.num("RES", {w: {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in s.items()} for w, s in RES.items()})
R.num("LAW_this_run", {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in LAWm.items()})
R.num("LAW_committed", {f: {k: c56[f"{f}|law"][k] for k in ("mean", "tot", "z", "slope", "slope_se", "zs", "fast_mean", "zf")} for f in ("canonical", "alt")})
R.num("TABLE", TABLE); R.num("R6", O9); R.num("nine", sel); R.num("three_clause_H2_on_LCDM", three)
R.num("reading", reading); R.num("flips", flips)
nf = R.write()
sys.exit(1 if nf else 0)
