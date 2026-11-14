#!/usr/bin/env python3
"""XJ1 (reported, post hoc; a reading, not a re-grade of any Milky Way lane): what the exact junction does to the Milky
Way's enclosed mass at 150 kpc and beyond, where the settled radius now lies inside the measured radii.
- The lens-chain layout of this lane (xj1_lens3.py's profile_E, executed up to its boundary marker; SRH1's halo and
  profile) gives, for log M_b = log10(6.681e10) at z = 0, the ratio of each case's enclosed mass to the law's own.
- That ratio multiplies PLT1's no-field line (its nu function and M_b, copied: closure_2026_11_12/
  PLT1_outer_mass_vs_literature/plt1.py), and PLT1's pull (20 per cent floor, copied) is evaluated on the seven rows at
  r >= 150 kpc printed in PLT1's RESULT.md (values typed from that table).
Known answers: the law case reproduces PLT1's printed line (10.4 / 11.4, 13.7 / 15.0, 20.4 / 22.4 e11 at 150, 200,
300 kpc, within 1 %) and its printed no-field pulls (within 0.03).
Limits: PLT1's zip of published masses is not re-read (seven rows from its RESULT table; the rows at 100 kpc are not
used); the ratio comes from the layout's algebraic law and a point baryon mass, PLT1's line from its nu function.
  python3 -I -B xj1_mw.py -> xj1_mw.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "xj1_lens3.py")).read(); cut = src.index("# ---------------- JNT2's boundary (main mode), copied")
NS = {"__file__": os.path.join(HERE, "xj1_lens3.py"), "__name__": "xj1_lens3_lib"}
exec(compile(src[:cut], "xj1_lens3_prefix", "exec"), NS)
halo, profile, profile_E, Mph, XP = NS["halo"], NS["profile"], NS["profile_E"], NS["Mph"], NS["XP"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
# PLT1's constants, line and pull (copied)
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; MB = 6.681e10; FLOOR = 0.20
def nu(y): return 1.0 / (1.0 - math.exp(-math.sqrt(max(y, 1e-14))))
def M_line(r_kpc, a0): return nu(G * MB * MSUN / (r_kpc * KPC) ** 2 / a0) * MB / 1e11
def pull(Ml, M, elo, ehi, floor=FLOOR):
    slo = math.log10(M / (M - elo)); shi = math.log10((M + ehi) / M); s = math.log10(1.0 + floor)
    side = slo if Ml < M else shi
    return (math.log10(Ml) - math.log10(M)) / math.sqrt(side * side + s * s)
ROWS = [("H", 150, 7.50, 2.50, 2.50, "Deason12b"), ("H", 200, 6.80, 4.10, 4.10, "Bhattacharjee14"), ("H", 200, 8.11, 0.50, 0.41, "Hattori21"),
        ("S", 200, 11.00, 2.20, 2.70, "CorreaMagnus22"), ("S", 200, 14.90, 4.00, 4.00, "Li25"), ("S", 240, 7.90, 2.30, 2.30, "Makarov25"), ("S", 273, 14.30, 3.20, 3.50, "Fritz20")]
PRINTED = {"canonical": [0.95, 1.39, 2.78, 0.77, -0.23, 2.33, 0.92], "alt": [1.22, 1.57, 3.27, 1.10, 0.03, 2.62, 1.25]}
LINE = {"canonical": {150: 10.4, 200: 13.7, 300: 20.4}, "alt": {150: 11.4, 200: 15.0, 300: 22.4}}
lMb = math.log10(MB)
RES = dict(lane="XJ1", part="Milky Way enclosed mass beyond 150 kpc under the exact junction (reported, post hoc; a reading)", logMb=lMb,
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})
ok = True
for ft in ("canonical", "alt"):
    X, xs, xta, xf, rM = halo(ft, lMb, 0.0); kpc = lambda x: x * rM / 3.0857e19
    ka1 = max(abs(M_line(r, A0[ft]) / v - 1) for r, v in LINE[ft].items())
    law = lambda x: 1.0 + float(min(Mph(x), X))
    cases = [("the law at every radius", None), ("exact, third caustic", ("E", "k3")), ("exact, second caustic", ("E", "k2")), ("exact, 0.5 R_fold", ("E", 0.5)), ("exact, 0.75 R_fold", ("E", 0.75)),
             ("exact, R_fold", ("E", 1.0)), ("record's junction, 2 R_fold", ("J", 2.0)), ("record's junction, 1.25 R_fold", ("J", 1.25)), ("reference at every radius", ("J", 0.0))]
    R = dict(R_fold_kpc=kpc(xf), r_ta_kpc=kpc(xta), cap_kpc=kpc(math.sqrt(X * (X + 1))), X=X, KA_line_max_rel=ka1, cases={})
    P(f"[{ft}] log M_b {lMb:.3f}, z 0: R_fold {kpc(xf):.0f} kpc, halo r_ta {kpc(xta):.0f} kpc, the law's cap {kpc(math.sqrt(X * (X + 1))):.0f} kpc, share X {X:.2f}; PLT1's line reproduced within {ka1:.2%}")
    for name, spec in cases:
        if spec is None: M3 = None; rs = float("inf"); extra = {}
        elif spec[0] == "E": pc, M3, inf = profile_E(ft, lMb, 0.0, spec[1]); rs = kpc(inf["xset"]); extra = dict(t=inf["t"], s=inf["s"])
        else: pc, M3, inf = profile(ft, lMb, 0.0, spec[1], "S"); rs = kpc(inf["xset"]); extra = dict(s=inf["s"])
        z = []; lines = {}
        for cls, r, M, lo, hi, lab in ROWS:
            x = r * 3.0857e19 / rM; ratio = 1.0 if M3 is None else (1.0 + float(M3(x))) / law(x)
            Ml = M_line(r, A0[ft]) * ratio; z.append(pull(Ml, M, lo, hi)); lines[f"{lab}@{r}"] = Ml
        zH, zS = float(np.median(z[:3])), float(np.median(z[3:]))
        if spec is None:
            dv = max(abs(a - b) for a, b in zip(z, PRINTED[ft])); ok &= dv <= 0.03 and ka1 <= 0.01; extra = dict(KA_pulls_max_abs_dev=dv)
        R["cases"][name] = dict(R_set_kpc=rs, pulls=z, median_H=zH, median_S=zS, line_e11_at_150_200_273=[lines["Deason12b@150"], lines["Hattori21@200"], lines["Fritz20@273"]], **extra)
        P(f"[{ft}] {name:30s} R_set {rs:6.0f} kpc; line at 150 / 200 / 273 kpc {lines['Deason12b@150']:.1f} / {lines['Hattori21@200']:.1f} / {lines['Fritz20@273']:.1f} e11; pulls " + " ".join(f"{v:+.2f}" for v in z)
          + f"; median field stars {zH:+.2f}, satellites and streams {zS:+.2f}" + (f"   [known answer: max dev from PLT1's printed pulls {extra['KA_pulls_max_abs_dev']:.3f}]" if spec is None else "")
          + (f"; t {extra['t']:.3f}" if "t" in extra else "") + (f"; s {extra['s']:.3f}" if "s" in extra else ""))
    RES["footings"][ft] = R
RES["known_answers_ok"] = bool(ok)
P(f"known answers (PLT1's printed line and no-field pulls): {'PASS' if ok else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "xj1_mw.json"), "w"), indent=1)
open(os.path.join(HERE, "xj1_mw.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
