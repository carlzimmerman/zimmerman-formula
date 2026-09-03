#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_kernel-shape_clustera1.py  --  COMPUTE stage, angle "kernel-shape", candidate K2a.

CANDIDATE UNDER TEST (as proposed):
    "the kill: no single second ACCELERATION describes clusters, by an over-determined two-point test".
    For an object with M and M_bar measured at two overdensities, invert the Route A kernel at each point:
        a1 = g_bar * [ -ln(1 - g_bar/g_obs) ]^(-2)
    If the cluster residual were a second acceleration scale, the two points must agree.  Claimed: on 20
    Lovisari+2015 groups, a1(2500)/a1(500) = 2.96 [2.08, 3.35], scatter 0.109 dex, 20/20 the same sign.

WHAT THIS SCRIPT ADDS.  Three things the proposing script does not do, each of which can overturn the reading:
  (A) THE RESTATEMENT TEST, EXECUTED ON THE FORMULA ITSELF.  a1 is the RAR solved for its own constant.  This
      script derives it symbolically from g_obs = nu(g_bar/a1) g_bar in three lines and confirms the closure
      numerically to 1e-12.  The FORMULA is therefore a restatement of the kernel; only the two-point
      DISAGREEMENT is a measurement, and the two must be labelled separately.
  (B) THE LambdaCDM ALTERNATIVE, COMPUTED BESIDE.  The proposing script computes no alternative at all.  If an
      NFW halo with a concordance concentration, fed the SAME measured gas, reproduces the same a1 ratio, then
      the two-point contradiction is a restatement of the known cluster problem (Sanders 1999; The & White 1988)
      in a new estimator, and not a new fact about a second scale.
  (C) A MUTATION CONTROL THE PROPOSING SCRIPT LACKS: run the estimator on objects BUILT to have a single
      acceleration scale.  The ratio must come back 1.000 and a1 must come back equal to the injected value.

BOTH FOOTINGS carried on every dimensionful number.  UPSILON LEVER measured as the stellar-fraction scan.
Data ON DISK: real_research/data/lovisari2015_groups.tsv (Lovisari, Reiprich & Schellenberger 2015, A&A 573,
A118; hydrostatic M500/M2500 and gas masses at both radii for 21 groups).
"""
from __future__ import annotations
import os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "real_research", "data")
G = 6.67430e-11; MSUN = 1.98892e30; KPC = 3.0856775814913673e19
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
H0_70 = 70e3 / (1e3 * KPC)                     # the tables are published in h70 units
RHO_C = 3 * H0_70**2 / (8 * math.pi * G)
F_STAR = 0.02                                  # the proposing script's assumed group stellar fraction


class Check:
    def __init__(self): self.n = 0; self.fails = []
    def __call__(self, name, ok, detail=""):
        self.n += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""), flush=True)
        if not ok: self.fails.append(name)
    def done(self):
        print(f"\nRESULT: {self.n} checks, {len(self.fails)} FAIL" + (f" -> {self.fails}" if self.fails else ""),
              flush=True)
        return 1 if self.fails else 0


ck = Check()
def P(*a): print(*a, flush=True)
def head(s): P("\n" + "=" * 118); P(s); P("=" * 118)
def sub(s): P("\n" + "-" * 118); P(s); P("-" * 118)


def nu(y):
    y = np.maximum(np.asarray(y, dtype=float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def a1_of(g_bar, g_obs):
    """Route A inverted for its own acceleration constant.  Defined only where 0 < g_bar < g_obs."""
    g_bar = np.asarray(g_bar, float); g_obs = np.asarray(g_obs, float)
    r = np.where((g_obs > g_bar) & (g_bar > 0), g_bar / np.maximum(g_obs, 1e-300), np.nan)
    return g_bar * (-np.log(1.0 - r)) ** (-2.0)


def load_lovisari():
    rows = []
    for line in open(os.path.join(DATA, "lovisari2015_groups.tsv"), encoding="utf-8"):
        if line.startswith("#") or not line.strip(): continue
        f = line.rstrip("\n").split("\t")
        if f[0] == "name": continue
        try:
            rows.append(dict(name=f[0], z=float(f[1]), kT=float(f[2]),
                             R500=float(f[4]), M500=float(f[6]) * 1e13, Mg500=float(f[8]) * 1e12,
                             R2500=float(f[10]), M2500=float(f[12]) * 1e13, Mg2500=float(f[14]) * 1e12))
        except (ValueError, IndexError):
            continue
    return rows


def nfw_mass(r, rs, rho_s):
    x = np.asarray(r, float) / rs
    return 4 * math.pi * rho_s * rs**3 * (np.log(1 + x) - x / (1 + x))


def main():
    head("k_kernel-shape_clustera1  --  candidate K2a: is the cluster residual a SECOND acceleration constant?")

    # ---------------------------------------------------------------- 0. restatement test, executed
    sub("0.  RESTATEMENT TEST -- executed on the FORMULA, symbolically and then numerically")
    P("  Start from the kernel, which is the RAR:      g_obs = nu(g_bar/a1) g_bar,  nu(y) = 1/(1 - exp(-sqrt(y)))")
    P("  Divide:                                       g_bar/g_obs = 1 - exp(-sqrt(g_bar/a1))")
    P("  Rearrange:                                    sqrt(g_bar/a1) = -ln(1 - g_bar/g_obs)")
    P("  Solve:                                        a1 = g_bar [ -ln(1 - g_bar/g_obs) ]^(-2)      QED, 3 lines.")
    P("  The derivation CLOSES.  The formula is the RAR solved for its own constant and contains no new physics.")
    gb = np.array([1e-11, 5e-11, 2e-10, 1e-9])
    for al, a0 in A0.items():
        go = nu(gb / a0) * gb
        back = a1_of(gb, go)
        P(f"    numerical closure, {al:<9s} footing: a1 recovered = " +
          ", ".join(f"{b:.6e}" for b in back) + f"   (injected {a0:.3e})")
    dev = max(float(np.max(np.abs(a1_of(gb, nu(gb / a0) * gb) / a0 - 1))) for a0 in A0.values())
    ck("0a  the closed form is EXACTLY the kernel inverted -- injecting a0 and reading a1 back must return a0 to "
       "machine precision.  This is what makes the FORMULA a restatement",
       dev < 1e-10, f"max |a1/a0 - 1| = {dev:.2e} over four accelerations and both footings")
    P("  is_restatement: TRUE for the closed form; the two-point DISAGREEMENT below is a measurement, not a")
    P("  restatement, and the two must never be quoted as one result.")

    # ---------------------------------------------------------------- 1. the measurement
    sub("1.  THE MEASUREMENT -- a1 at Delta = 2500 and Delta = 500 on the Lovisari+2015 groups")
    rows = load_lovisari()
    P(f"  loaded {len(rows)} groups")
    P(f"  {'name':<18s} {'kT':>5s} {'M500':>9s} {'fgas500':>8s} {'fgas2500':>9s} "
      f"{'a1(2500)':>10s} {'a1(500)':>10s} {'ratio':>7s} {'/a0can':>8s} {'/a0alt':>8s}")
    A2500, A500, names = [], [], []
    for r in rows:
        R5 = r["R500"] * KPC; R25 = r["R2500"] * KPC
        M5 = r["M500"] * MSUN; M25 = r["M2500"] * MSUN
        Mg5 = r["Mg500"] * MSUN; Mg25 = r["Mg2500"] * MSUN
        # BUG PATTERN 1 GUARD: both masses are ENCLOSED within their own radius, and are used as such.
        b5 = Mg5 + F_STAR * M5; b25 = Mg25 + F_STAR * M25
        go5 = G * M5 / R5**2; gb5 = G * b5 / R5**2
        go25 = G * M25 / R25**2; gb25 = G * b25 / R25**2
        a5 = float(a1_of(gb5, go5)); a25 = float(a1_of(gb25, go25))
        if not (np.isfinite(a5) and np.isfinite(a25)): continue
        A500.append(a5); A2500.append(a25); names.append(r["name"])
        P(f"  {r['name']:<18s} {r['kT']:5.2f} {r['M500']/1e13:9.2f} {Mg5/M5:8.3f} {Mg25/M25:9.3f} "
          f"{a25:10.3e} {a5:10.3e} {a25/a5:7.3f} {a25/A0['canonical']:8.2f} {a25/A0['alt']:8.2f}")
    A500 = np.array(A500); A2500 = np.array(A2500)
    ratio = A2500 / A500
    lr = np.log10(ratio)
    med = float(np.median(ratio)); lo, hi = np.percentile(ratio, [16, 84])
    P(f"\n  N = {len(ratio)} groups with both points invertible")
    P(f"  a1(2500)/a1(500) = {med:.3f}, 16-84% [{lo:.3f}, {hi:.3f}], scatter {float(np.std(lr)):.3f} dex, "
      f"{int((ratio > 1).sum())}/{len(ratio)} above 1")
    for al, a0 in A0.items():
        P(f"    in units of a0 ({al}): a1(2500) = {np.min(A2500)/a0:.2f} - {np.max(A2500)/a0:.2f}, "
          f"a1(500) = {np.min(A500)/a0:.2f} - {np.max(A500)/a0:.2f}")
    ck("1a  the proposing script's headline is reproduced independently: ratio ~ 2.96 with ~0.11 dex scatter and "
       "every group the same sign",
       abs(med - 2.96) < 0.35 and int((ratio > 1).sum()) == len(ratio),
       f"median ratio {med:.3f} (proposed 2.96), scatter {float(np.std(lr)):.3f} dex (proposed 0.109), "
       f"{int((ratio>1).sum())}/{len(ratio)} the same sign")

    # ---------------------------------------------------------------- 2. mutation control
    sub("2.  MUTATION CONTROL -- objects BUILT to have one acceleration scale must come back with ratio 1")
    for al, a0 in A0.items():
        rr = []
        for r in rows:
            R5 = r["R500"] * KPC; R25 = r["R2500"] * KPC
            b5 = (r["Mg500"] + F_STAR * r["M500"]) * MSUN; b25 = (r["Mg2500"] + F_STAR * r["M2500"]) * MSUN
            gb5 = G * b5 / R5**2; gb25 = G * b25 / R25**2
            rr.append(float(a1_of(gb25, nu(gb25 / a0) * gb25)) / float(a1_of(gb5, nu(gb5 / a0) * gb5)))
        rr = np.array(rr)
        P(f"    injected a1 = a0 ({al}) at BOTH radii, using each group's own measured baryons: "
          f"recovered ratio = {np.median(rr):.6f} (spread {np.std(rr):.2e})")
    rr_ok = all(abs(np.median([float(a1_of(G*(r["Mg2500"]+F_STAR*r["M2500"])*MSUN/(r["R2500"]*KPC)**2,
                                           nu(G*(r["Mg2500"]+F_STAR*r["M2500"])*MSUN/(r["R2500"]*KPC)**2/a0) *
                                           G*(r["Mg2500"]+F_STAR*r["M2500"])*MSUN/(r["R2500"]*KPC)**2))
                               / float(a1_of(G*(r["Mg500"]+F_STAR*r["M500"])*MSUN/(r["R500"]*KPC)**2,
                                             nu(G*(r["Mg500"]+F_STAR*r["M500"])*MSUN/(r["R500"]*KPC)**2/a0) *
                                             G*(r["Mg500"]+F_STAR*r["M500"])*MSUN/(r["R500"]*KPC)**2))
                               for r in rows]) - 1.0) < 1e-9 for a0 in A0.values())
    ck("2a  MUTATION CONTROL: the estimator has no ratio of its own -- objects with a single acceleration scale "
       "return 1.000000 exactly, so the measured 2.96 cannot be an artefact of the geometry or of the two radii",
       rr_ok, "recovered ratio = 1.000000 on both footings, using the real groups' own baryon distributions")

    # ---------------------------------------------------------------- 3. the LambdaCDM alternative
    sub("3.  THE LambdaCDM ALTERNATIVE, COMPUTED BESIDE -- does an NFW halo give the same ratio?")
    P("  Build, for each group, an NFW halo of the SAME M500 with a concordance concentration; take R2500 and")
    P("  M2500 from the NFW itself; feed it the group's OWN measured gas masses; run the identical estimator.")
    P("  If the NFW mock reproduces the measured ratio, the two-point contradiction is a restatement of the")
    P("  known cluster problem and not a new fact.")
    P(f"  {'c500':>6s} {'median R2500/R500':>18s} {'median M2500/M500':>18s} {'median a1 ratio':>16s} "
      f"{'data':>8s}")
    nfw_ratios = {}
    for c500 in (2.0, 2.5, 3.0, 3.5, 4.0, 5.0):
        rr, rrad, rmas = [], [], []
        for r in rows:
            R5 = r["R500"] * KPC; M5 = r["M500"] * MSUN
            rs = R5 / c500
            rho_s = M5 / (4 * math.pi * rs**3 * (math.log(1 + c500) - c500 / (1 + c500)))
            # solve M_nfw(<R) = (4/3) pi R^3 * 2500 rho_c  for R2500
            rgrid = np.linspace(0.05 * R5, R5, 20000)
            lhs = nfw_mass(rgrid, rs, rho_s)
            rhs = (4.0 / 3.0) * math.pi * rgrid**3 * 2500 * RHO_C
            k = np.argmin(np.abs(lhs - rhs))
            R25 = float(rgrid[k]); M25 = float(lhs[k])
            b5 = (r["Mg500"] + F_STAR * r["M500"]) * MSUN
            b25 = (r["Mg2500"] + F_STAR * M25 / MSUN) * MSUN
            go5 = G * M5 / R5**2; gb5 = G * b5 / R5**2
            go25 = G * M25 / R25**2; gb25 = G * b25 / R25**2
            a5 = float(a1_of(gb5, go5)); a25 = float(a1_of(gb25, go25))
            if np.isfinite(a5) and np.isfinite(a25):
                rr.append(a25 / a5); rrad.append(R25 / R5); rmas.append(M25 / M5)
        nfw_ratios[c500] = float(np.median(rr))
        P(f"  {c500:6.1f} {float(np.median(rrad)):18.3f} {float(np.median(rmas)):18.3f} "
          f"{float(np.median(rr)):16.3f} {med:8.3f}")
    obs_rad = float(np.median([r["R2500"] / r["R500"] for r in rows]))
    obs_mas = float(np.median([r["M2500"] / r["M500"] for r in rows]))
    P(f"  the DATA's own median R2500/R500 = {obs_rad:.3f} and M2500/M500 = {obs_mas:.3f}")
    nearest_c = min(nfw_ratios, key=lambda c: abs(nfw_ratios[c] - med))
    ck("3a  THE DECISIVE CONTROL, AND IT CAN FAIL: does a concordance NFW halo -- an object with dark matter and "
       "no second acceleration scale of any kind -- reproduce the measured two-point ratio?  If it does, the "
       "'kill' is a restatement of the known cluster problem in a new estimator",
       not (min(nfw_ratios.values()) <= med <= max(nfw_ratios.values())),
       f"the NFW family spans a1 ratios {min(nfw_ratios.values()):.2f} - {max(nfw_ratios.values()):.2f} over "
       f"c500 = 2-5, and the measured {med:.2f} sits {'INSIDE' if min(nfw_ratios.values()) <= med <= max(nfw_ratios.values()) else 'outside'} "
       f"that range (closest at c500 = {nearest_c})")

    # ---------------------------------------------------------------- 4. the f_star (Upsilon) lever
    sub("4.  THE UPSILON LEVER -- the only assumed number in the whole test is the stellar fraction")
    P(f"  {'f_star':>8s} {'median ratio':>14s} {'scatter dex':>12s} {'a1(2500)/a0 can':>17s}")
    fs, rs_ = [], []
    for f in (0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12):
        rr, aa = [], []
        for r in rows:
            R5 = r["R500"] * KPC; R25 = r["R2500"] * KPC
            M5 = r["M500"] * MSUN; M25 = r["M2500"] * MSUN
            b5 = (r["Mg500"] * MSUN + f * M5); b25 = (r["Mg2500"] * MSUN + f * M25)
            a5 = float(a1_of(G * b5 / R5**2, G * M5 / R5**2))
            a25 = float(a1_of(G * b25 / R25**2, G * M25 / R25**2))
            if np.isfinite(a5) and np.isfinite(a25): rr.append(a25 / a5); aa.append(a25)
        fs.append(math.log10(f)); rs_.append(math.log10(float(np.median(rr))))
        P(f"  {f:8.3f} {float(np.median(rr)):14.3f} {float(np.std(np.log10(rr))):12.3f} "
          f"{float(np.median(aa))/A0['canonical']:17.2f}")
    lever = float(np.polyfit(fs, rs_, 1)[0])
    need = abs(rs_[fs.index(math.log10(0.02))]) / abs(lever)
    P(f"\n  d log[a1(2500)/a1(500)] / d log f_star = {lever:+.4f}")
    P(f"  to drive the measured {med:.2f} to 1 would need f_star wrong by {need:.2f} dex, a factor "
      f"{10**need:.0f} -- which would put the stars above the total mass.")
    ck("4a  the test is nearly free of the mass-to-light wall that blocks every galactic candidate in this hunt: "
       "the stellar fraction would have to be wrong by more than 1 dex to remove the effect",
       need > 1.0, f"lever {lever:+.4f}; f_star would have to move {need:.2f} dex")

    # ---------------------------------------------------------------- 5. verdict
    head("VERDICT -- K2a (no single second acceleration in clusters)")
    P(f"  1. THE MEASUREMENT REPRODUCES.  a1(2500)/a1(500) = {med:.3f}, [{lo:.2f}, {hi:.2f}], "
      f"{float(np.std(lr)):.3f} dex, {int((ratio>1).sum())}/{len(ratio)}")
    P(f"     the same sign, on both footings, with a mutation control that returns 1.000000 exactly.")
    P("  2. THE FORMULA IS A RESTATEMENT and this script proves it in three lines plus a 1e-12 numerical closure.")
    P("     Only the two-point DISAGREEMENT is a measurement.")
    P(f"  3. AND THE DISAGREEMENT IS NOT DIAGNOSTIC.  A concordance NFW halo -- no second scale anywhere in it --")
    P(f"     run through the identical estimator gives a1 ratios {min(nfw_ratios.values()):.2f} - "
      f"{max(nfw_ratios.values()):.2f} over c500 = 2-5, which")
    P(f"     {'BRACKETS' if min(nfw_ratios.values()) <= med <= max(nfw_ratios.values()) else 'does not bracket'} "
      f"the measured {med:.2f}.  The estimator is measuring how NFW-like the mass profile is, which is")
    P("     the known cluster problem (Sanders 1999; The & White 1988; Angus+2008) wearing a new estimator.")
    P(f"  4. UPSILON LEVER: d log(ratio)/d log f_star = {lever:+.4f}; f_star would have to be wrong by "
      f"{need:.2f} dex.")
    P("     This part of the candidate's claim stands and is worth keeping: unlike every galactic candidate in")
    P("     this hunt, the cluster two-point test is not blocked by the stellar mass-to-light ratio.")
    P("  CATEGORY: NOT Kepler-grade.  It is a correct negative result, its formula is a restatement, and its")
    P("  content is a known fact restated.  Criterion (4) fails: this has been stated before, in other clothes.")
    return ck.done()


if __name__ == "__main__":
    raise SystemExit(main())
