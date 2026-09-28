#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k05 -- IS 32 PI SPECIAL?  Can the number in  Lambda l0^2 = 32 pi  (l0 = c^2/a0; equivalently a0 = (1/2) c sqrt(G rho_Lambda)) be read off
the geometry of the actual spacetime, so that the one-half is not fitted?

k01-k04 asked whether an ACTION can relate a0 to Lambda: not in the present class (k01), not by a global constraint (k02, off by 1e5); the
one principle-shaped alternative, the horizon form kappa = 0.461, is data-degenerate with 1/2 (k03); the four-form turns "why 32 pi" into
"why Z = 8 beta^2" (k04).  This lane asks the question of the number itself.

THE THREE TESTS (declared before the first run)
  S1  CONVENTION vs CONTENT (sympy, exact).  With Lambda = 8 pi G rho_Lambda / c^2 (rho_Lambda a mass density):
          a0 = kappa c sqrt(G rho_Lambda)   <=>   Lambda l0^2 = 8 pi / kappa^2   <=>   rho_Lambda c^2 = a0^2 / (kappa^2 G).
      Every pi in "32 pi" is Einstein's 8 pi (the conversion between Lambda and rho_Lambda).  The one convention-free number is
      1/kappa^2 = 4: the vacuum energy density is 4 a0^2 / G.  Rewritings with other pi's (8 x 4pi/3 through the Friedmann factor, 2 x 16 pi
      through the Einstein-Hilbert normalisation) re-express the same 4 in another convention.
  S2  THE HORIZON READING.  a0 = c^2/(2 R*) with R* = c/sqrt(G rho_Lambda) = sqrt(8 pi / Lambda) is the Schwarzschild surface-gravity form,
      and a horizon of radius R* has area A with A Lambda = 32 pi^2 -- the constant that normalises the Euler characteristic in four
      dimensions.  Is that horizon realisable in a spacetime with this Lambda?  The static spherically symmetric vacuum with Lambda > 0 is
      Schwarzschild-de Sitter (f = 1 - 2M/r - Lambda r^2/3, G = c = 1); its horizons are scanned exactly.  (The positive-Lambda horizon-area
      bounds under the dominant energy condition -- black-hole horizons <= 4 pi/Lambda, cosmological <= 12 pi/Lambda, e.g. Maeda, Koike,
      Narita & Ishibashi 1998 -- extend the SdS result; they are cited, not re-derived.)
  S3  THE LOOK-ELSEWHERE CENSUS.  The data (k03's MEAS: BTFR 0.465 +- 0.076, distance-free 0.551 +- 0.043; combined by inverse variance,
      assuming independence) against every constant kappa = (a/b) pi^m sqrt(c/d), a, b in 1..6, m in {-1, -1/2, 0, 1/2, 1}, c, d in 1..8
      (distinct values), complexity a + b + c + d + 2|m| over the simplest representation (1/2 has complexity 5).

  H0  [CONTROL; MUTATE must fail] the SdS family obeys the area bounds on a dense grid of every mass that has horizons: all horizons have
      A Lambda <= 12 pi and black-hole horizons A Lambda <= 4 pi (+1e-9).  MUTATE=1: the sign of Lambda in f(r) is flipped (anti-de Sitter:
      no cosmological horizon, black-hole areas unbounded) -- H0 must FAIL.
  H1  [HEADLINE] the horizon reading is realisable: some SdS horizon has A Lambda = 32 pi^2 (equivalently a horizon at R*).
      Declared expectation: FAIL.
  H2  the data single out 1/2: no other constant of complexity <= 5 lies within 2 sigma of the combined kappa.
      Declared expectation: FAIL (1/sqrt(pi) = 0.564 has complexity 5).
  R1  (reported) the S1 identities; the SdS black hole whose surface gravity IS a0; a horizon at R* would need a negative mass; the census
      table with Lambda l0^2 = 8 pi / kappa^2 for each constant; the alt footing (kappa = 0.602).
Run: python3 kappa_closure/k05_is_32pi_special.py   (MUTATE=1 for the control; ~5 s)
"""
import os, re, sys, json, math, itertools
from fractions import Fraction
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "k05_is_32pi_special" + ("_MUTATE" if MUTATE else "")
LINES, CHECKS, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LINES.append(s)


def check(name, detail, ok, lb=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=lb))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}\n         {detail}")


P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the sign of Lambda flipped in f(r) -- H0 must FAIL ***")

# ================================================================================================ S1 convention vs content
P("\n" + "=" * 110 + "\nS1  CONVENTION vs CONTENT (sympy, exact)\n" + "=" * 110)
a0, c, G, rho, kap = sp.symbols("a0 c G rho kappa", positive=True)
Lam = 8 * sp.pi * G * rho / c ** 2
a0_expr = kap * c * sp.sqrt(G * rho)
lam_l02 = sp.simplify(Lam * (c ** 2 / a0_expr) ** 2)
rho_c2 = sp.simplify(rho * c ** 2 / (a0_expr ** 2 / G))
P(f"    Lambda l0^2 = {lam_l02}   (kappa = 1/2: {sp.simplify(lam_l02.subs(kap, sp.Rational(1, 2)))});   rho_Lambda c^2 / (a0^2/G) = {rho_c2} "
  f"(kappa = 1/2: {sp.simplify(rho_c2.subs(kap, sp.Rational(1, 2)))})")
fr = sp.simplify(sp.Rational(8, 1) * (4 * sp.pi / 3) / (32 * sp.pi) * 12)
eh = sp.simplify(2 * 16 * sp.pi / (32 * sp.pi))
P(f"    rewritings: 32 pi = 8 x (4 pi/3) x 3 [the Friedmann/ball factor, x3 absorbed into l_dS = sqrt(3/Lambda)] -> check {fr} = 1 x 4; "
  f"32 pi = 2 x 16 pi [Einstein-Hilbert] -> check {eh} = 1: same content, other conventions")
s1_ok = sp.simplify(lam_l02 - 8 * sp.pi / kap ** 2) == 0 and sp.simplify(rho_c2 - 1 / kap ** 2) == 0
NUM["S1"] = dict(Lambda_l0sq=str(lam_l02), rhoc2_over_a0sq_G=str(rho_c2), content_kappa_half=4)

# ================================================================================================ S2 the horizon reading, Schwarzschild-de Sitter
P("\n" + "=" * 110 + "\nS2  THE HORIZON READING IN SCHWARZSCHILD-DE SITTER (G = c = 1, lengths in units of 1/sqrt|Lambda|)\n" + "=" * 110)
SGN = -1.0 if MUTATE else 1.0                                                           # f = 1 - 2M/r - SGN r^2/3 in units |Lambda| = 1


def horizons(M):
    """positive roots of r f(r) = r - 2M - SGN r^3/3 = 0, sorted."""
    roots = np.roots([-SGN / 3.0, 0.0, 1.0, -2.0 * M])
    r = np.real(roots[np.abs(np.imag(roots)) < 1e-12])
    return np.sort(r[r > 0])


MG = np.concatenate([np.linspace(1e-6, 1 / 3 - 1e-9, 200001), np.linspace(1 / 3, 10.0, 20001)])
maxA_all, maxA_bh, n_with = 0.0, 0.0, 0
for M in MG:
    h = horizons(M)
    if not len(h):
        continue
    n_with += 1
    A = 4 * math.pi * h ** 2
    maxA_all = max(maxA_all, float(A.max()))
    maxA_bh = max(maxA_bh, float(A[0]))                                                 # the innermost horizon is the black hole's
h0 = maxA_all <= 12 * math.pi + 1e-9 and maxA_bh <= 4 * math.pi + 1e-9
P(f"    masses with horizons: {n_with}; max A Lambda over all horizons {maxA_all:.6f} (12 pi = {12 * math.pi:.6f}); max over black-hole "
  f"horizons {maxA_bh:.6f} (4 pi = {4 * math.pi:.6f})")
check("H0 CONTROL: every Schwarzschild-de Sitter horizon obeys A Lambda <= 12 pi and every black-hole horizon A Lambda <= 4 pi" +
      ("  [MUTATE: Lambda sign flipped]" if MUTATE else ""), f"max {maxA_all:.4f} / {maxA_bh:.4f}", h0)
Rstar = math.sqrt(8 * math.pi)                                                          # R* sqrt(Lambda)
M_Rstar = (Rstar / 2) * (1 - SGN * Rstar ** 2 / 3)                                     # f(R*) = 0  =>  2M = R* (1 - R*^2/3)
target = 32 * math.pi ** 2
h1 = maxA_all >= target - 1e-9 and not MUTATE
P(f"    the horizon reading needs A Lambda = 32 pi^2 = {target:.3f}, i.e. a horizon at R* sqrt(Lambda) = sqrt(8 pi) = {Rstar:.4f}; every "
  f"SdS horizon lies at r sqrt(Lambda) <= sqrt(3) = {math.sqrt(3):.4f}; a horizon at R* needs M sqrt(Lambda) = {M_Rstar:.3f} "
  f"({'a negative mass' if M_Rstar < 0 else 'positive'})")
check("H1 [HEADLINE] the horizon reading is realisable: some Schwarzschild-de Sitter horizon has A Lambda = 32 pi^2 (a horizon at R*) "
      "[declared expectation: FAIL]", f"max A Lambda {maxA_all:.3f} vs {target:.3f}; M(R*) sqrt(Lambda) = {M_Rstar:.3f}", h1)
# the SdS black hole whose surface gravity (Killing normalisation, kappa_b = f'(r_b)/2 = (1 - r_b^2)/(2 r_b)) equals a0 = sqrt(1/(32 pi))
ka0 = 1 / math.sqrt(32 * math.pi)
xb = -ka0 + math.sqrt(ka0 ** 2 + 1)
Mb = (xb / 2) * (1 - xb ** 2 / 3)
P(f"    the SdS black hole with surface gravity a0: r_b sqrt(Lambda) = {xb:.5f} (Nariai: 1), M / M_Nariai = {Mb / (1 / 3):.4f}, A Lambda = "
  f"{4 * math.pi * xb ** 2:.4f} -- a near-Nariai hole, not a horizon at R*; its surface gravity also carries de Sitter's normalisation "
  f"ambiguity (Killing vs Bousso-Hawking), so no coefficient is fixed by it")
NUM["S2"] = dict(max_A_all=maxA_all, max_A_bh=maxA_bh, target=target, M_at_Rstar=M_Rstar, bh_with_kappa_a0=dict(x=xb, M_over_MN=Mb * 3,
                 A_Lambda=4 * math.pi * xb ** 2))

# ================================================================================================ S3 the census
P("\n" + "=" * 110 + "\nS3  THE LOOK-ELSEWHERE CENSUS: simple constants against the measured kappa\n" + "=" * 110)
k03src = open(os.path.join(HERE, "k03_half_vs_two_pi_precision.py")).read()
MEAS = eval(re.search(r"MEAS = (\{[^}]*\})", k03src).group(1))
w = {k: 1 / v[1] ** 2 for k, v in MEAS.items()}
kc = sum(MEAS[k][0] * w[k] for k in MEAS) / sum(w.values())
sc = 1 / math.sqrt(sum(w.values()))
P(f"    k03's MEAS: " + "; ".join(f"{k} {v[0]} +- {v[1]}" for k, v in MEAS.items()) + f"  -> combined {kc:.4f} +- {sc:.4f} (independence assumed)")
best = {}
for a, b in itertools.product(range(1, 7), repeat=2):
    for m in (-1.0, -0.5, 0.0, 0.5, 1.0):
        for cn, cd in itertools.product(range(1, 9), repeat=2):
            if Fraction(cn, cd).denominator != cd or Fraction(a, b).denominator != b:
                continue                                                               # reduced fractions only
            val = (a / b) * math.pi ** m * math.sqrt(cn / cd)
            key = round(val, 12)
            cx = a + b + cn + cd + int(round(2 * abs(m)))
            lab = f"({a}/{b})" + (f" pi^{m:g}" if m else "") + (f" sqrt({cn}/{cd})" if (cn, cd) != (1, 1) else "")
            if key not in best or cx < best[key][0]:
                best[key] = (cx, lab)
rows = sorted([(cx, v, lab) for v, (cx, lab) in best.items() if abs(v - kc) <= 2 * sc and cx <= 7], key=lambda t: (t[0], abs(t[1] - kc)))
for cx, v, lab in rows:
    L = 8 * math.pi / v ** 2
    P(f"    complexity {cx}: kappa = {lab:24s} = {v:.4f}  ({(v - kc) / sc:+.2f} sigma)   Lambda l0^2 = 8 pi / kappa^2 = {L:8.3f} = {L / math.pi:.3f} pi")
n5 = [r for r in rows if r[0] <= 5]
others5 = [r for r in n5 if abs(r[1] - 0.5) > 1e-12]
h2 = len(others5) == 0
check("H2 the data single out 1/2: no other constant of complexity <= 5 within 2 sigma of the combined kappa [declared expectation: FAIL]",
      f"complexity <= 5 within 2 sigma: " + ", ".join(f"{lab} = {v:.4f}" for _, v, lab in n5), h2)
n_all = sum(1 for v in best if abs(v - kc) <= 2 * sc)
P(f"    all distinct grammar constants within 2 sigma (any complexity): {n_all}; within 1 sigma: {sum(1 for v in best if abs(v - kc) <= sc)}")
alt = 0.602
P(f"    footings: canonical kappa = 1/2 -> Lambda l0^2 = 32 pi = {32 * math.pi:.3f}; alt kappa = {alt} -> {8 * math.pi / alt ** 2:.3f} = "
  f"{8 / alt ** 2:.3f} pi ({(alt - kc) / sc:+.2f} sigma)")
NUM["S3"] = dict(MEAS=MEAS, combined=[kc, sc], rows=[dict(complexity=cx, kappa=v, label=lab, Lambda_l0sq=8 * math.pi / v ** 2) for cx, v, lab in rows],
                 n_within_2sigma=n_all)

# ================================================================================================ R1 and the reading
check("R1 (reported) S1's identities hold exactly (32 pi = Einstein's 8 pi x 4; the content is rho_Lambda c^2 = 4 a0^2/G)",
      f"S1 exact: {s1_ok}", s1_ok, lb=False)
# R2 (added after the first run of both modes, reported only; both modes re-run): the kappa that each natural geometric construction on
# the vacuum gives, in a0 = kappa c sqrt(G rho_Lambda) (H_Lambda = sqrt(8 pi G rho_Lambda / 3), c H_Lambda = sqrt(8 pi/3) c sqrt(G rho)).
NAT = [("de Sitter horizon surface gravity c H_Lambda (Killing normalisation at the origin)", math.sqrt(8 * math.pi / 3)),
       ("Newtonian surface gravity of the Hubble sphere as its own Schwarzschild radius, c H_Lambda / 2", math.sqrt(8 * math.pi / 3) / 2),
       ("Gibbons-Hawking temperature read as an Unruh acceleration, c H_Lambda / (2 pi)  [k03]", math.sqrt(8 * math.pi / 3) / (2 * math.pi)),
       ("Newtonian gravity of a ball of vacuum density at R* = c/sqrt(G rho): (4 pi/3) G rho R*", 4 * math.pi / 3),
       ("the same with the vacuum's active density rho + 3p/c^2 = -2 rho (repulsive)", 8 * math.pi / 3)]
for lab, k_ in NAT:
    P(f"    natural construction: {lab:100s} kappa = {k_:.4f}  ({(k_ - kc) / sc:+.1f} sigma from the data; ratio to 1/2: {k_ / 0.5:.3f})")
check("R2 (reported) no natural geometric construction on the vacuum gives kappa = 1/2; the nearest is the Gibbons-Hawking/Unruh form",
      "; ".join(f"{k_:.3f}" for _, k_ in NAT), all(abs(k_ - 0.5) > 1e-6 for _, k_ in NAT), lb=False)
NUM["R2"] = [dict(construction=lab, kappa=k_) for lab, k_ in NAT]
P("\n    READING: 32 pi carries no geometry beyond the integer 4 (= 1/kappa^2); its pi is Einstein's normalisation.  The horizon reading "
  "that makes it look geometric describes a horizon no spacetime with this Lambda can have, and the data cannot pick 1/2 out of the "
  "simple constants around it.  The one-half can only come from dynamics -- which k01-k04 show the present action class does not supply.")
lb = [x for x in CHECKS if x["load_bearing"]]
nf = sum(not x["ok"] for x in lb)
P(f"\n  {sum(x['ok'] for x in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}")
json.dump(dict(slug=SLUG, checks=CHECKS, numbers=NUM), open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf else 0)
