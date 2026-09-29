#!/usr/bin/env python3
"""CFG190 POST HOC -- two input checks after the frozen run (not part of the frozen result; labelled).

(1) VERIFIED from MUSE-DARK III's text (arXiv HTML, Sects. 3.1 and 3.2): the errors of Eq. 2 (a0(z~1) = 2.38 +0.12 -0.10) and Eq. 4
    (a0(0) = 1.0 +- 0.04, a1 = 1.59 +- 0.10) are 95% confidence intervals. The frozen run took them as 1 sigma. Here 1 sigma = the 95%
    half-width / 1.96, using the side facing each law (the lower side, -0.10, for laws below III's value).
(2) NOT FOUND in MUSE-DARK II's text (three reads of the arXiv HTML, including Sect. 7.3 and a whole-paper search for 0.16): the only
    0.16 dex is the bTFR's orthogonal intrinsic scatter; II adds no local zero-point uncertainty to its offset 0.00 +- 0.06 dex. So the
    frozen II input stands. Reported here ONLY as a sensitivity: an unstated extra systematic of 0.16 dex added in quadrature.
Everything else is the frozen CFG190 machinery (P2 at fixed g_obs; y bracket deep / 0.3 / 1.0; |pull| <= 2 on both = 'fits both').
Run: python3 campaign_fresh_gravity/CFG190_muse_dark_confrontation/cfg190_posthoc_errors.py
"""
import os, sys, math
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
sys.path.insert(0, CFG)
import CFG7_common as C

R = C.Report("cfg190_posthoc_errors", False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

OM = 0.315
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def tratio(z, om=OM):
    k = math.sqrt((1 - om) / om)
    return math.asinh(k * (1 + z) ** -1.5) / math.asinh(k)


def dlogM(ratio, y):
    if y == 0:
        return -math.log10(ratio)
    gobs2 = y * y + y
    gb = (-ratio + math.sqrt(ratio * ratio + 4 * gobs2)) / 2
    return math.log10(gb / y)


LAWS = {"flat": lambda z: 1.0, "a0 ~ E(z)": E, "T = t(z)/t0": tratio, "III linear": lambda z: 1 + 1.59 * z}
lr3 = math.log10(2.38 / 1.0)
cases = {
    "frozen (errors as 1 sigma; II +-0.06)": dict(s3=math.sqrt((0.10 / 2.38) ** 2 + (0.04 / 1.0) ** 2) / math.log(10), s2=0.06),
    "(1) III errors as 95% CI (II +-0.06)": dict(s3=math.sqrt((0.10 / 1.96 / 2.38) ** 2 + (0.04 / 1.96 / 1.0) ** 2) / math.log(10), s2=0.06),
    "(1)+(2) sensitivity: II +-sqrt(0.06^2 + 0.16^2)": dict(s3=math.sqrt((0.10 / 1.96 / 2.38) ** 2 + (0.04 / 1.96 / 1.0) ** 2) / math.log(10),
                                                          s2=math.hypot(0.06, 0.16)),
}
out = {}
for cname, cs in cases.items():
    R.banner(cname + f":  sigma_III(log ratio) = {cs['s3']:.4f} dex;  sigma_II = {cs['s2']:.3f} dex")
    both = []
    for name, f in LAWS.items():
        p3 = (math.log10(f(0.87)) - lr3) / cs["s3"]
        p2 = {y: (dlogM(f(1.0), y) - 0.0) / cs["s2"] for y in (0, 0.3, 1.0)}
        ok = [y for y in (0, 0.3, 1.0) if abs(p3) <= 2 and abs(p2[y]) <= 2]
        both += [(name, y) for y in ok]
        P(f"  {name:12s}: III pull {p3:+7.1f};  II pulls deep {p2[0]:+5.1f}, y 0.3 {p2[0.3]:+5.1f}, y 1 {p2[1.0]:+5.1f};  fits both at y: {ok}")
    out[cname] = both
    P(f"  -> laws fitting both: {both if both else 'NONE'}")
R.num("fits_both", {k: [f"{n}@{y}" for n, y in v] for k, v in out.items()})
check("PH1 (reported) with the verified 95% CI correction (1), the frozen headline still holds: no law fits both at any declared y",
      str(out["(1) III errors as 95% CI (II +-0.06)"]), True, load_bearing=False)
check("PH2 (reported) sensitivity only: an unstated extra 0.16 dex on II's offset would let III's law fit both at y >= 0.3",
      str(out["(1)+(2) sensitivity: II +-sqrt(0.06^2 + 0.16^2)"]), True, load_bearing=False)
nf = R.write(LANE)
raise SystemExit(1 if nf else 0)
