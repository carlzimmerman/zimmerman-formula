#!/usr/bin/env python3
r"""mi_horizon_entropy_route_2026.py -- THE HORIZON-ENTROPY ROUTE TO kappa. The last "outside the family"
route named by mi_kappa_linear_class_2026. It is ADMISSIBLE for Z^2 and OBSTRUCTED for Z, every concrete
construction it supplies lands at Z of order one, and two of them reproduce PRIOR ART rather than kappa = 1/2.

WHERE THIS COMES FROM. mi_kappa_linear_class_2026 proved that no tail functional of the kernel's own spectral
measure can force kappa (W_n ~ kappa^n identically, so the family is a relabelling), and reduced the open
problem to ONE number: Z^2 = 4 x (8pi/3), i.e. kappa^2 = 1/4. It named three untried routes from OUTSIDE that
family, the first being "horizon ENTROPY rather than horizon density". This is the swing at it.

THE DISCIPLINE. Every construction below is derived IN FULL in this docstring, BEFORE any number is
evaluated, and every one is reported with whatever it gives. Six forced-condition attempts are already on the
board (see mi_kappa_linear_class_2026's ledger) plus two functional enumerations = 8, log2(8) = 3.00 bits of
look-elsewhere. Picking a construction after seeing which lands is the failure mode PAPER_ATOMOS_NULL
(DOI 10.5281/zenodo.21654272) documents, and it is worthless.

WHAT THE HORIZON SUPPLIES, all forced, no freedom:
    R_H = c/H_Lambda            de Sitter horizon radius (pure Lambda)
    A   = 4 pi R_H^2            area
    l_P^2 = G hbar / c^3        Planck area
    N   = A / l_P^2             Planck-cell count on the horizon
    S/k_B = A/(4 l_P^2) = N/4   Gibbons-Hawking entropy -- THE 4 THIS ROUTE WAS CHOSEN FOR
    T_GH = hbar H_Lambda/(2 pi k_B)   Gibbons-Hawking temperature
    a_Unruh(T) = 2 pi c k_B T / hbar  Unruh inversion
    M c^2 = rho_Lambda V c^2,  V = (4/3) pi R_H^3,  rho_Lambda = 3H_Lambda^2/(8 pi G)

CONSTRUCTION C1 -- UNRUH/GIBBONS-HAWKING TEMPERATURE MATCHING.
  Derivation: if a0 IS the de Sitter-Unruh scale, the acceleration whose Unruh temperature equals the horizon
  temperature is the scale. a0 = a_Unruh(T_GH). Zero parameters. (Included for completeness -- this is the
  corpus's already-recorded F1 result and it must reproduce, or this script's machinery is wrong.)

CONSTRUCTION C2 -- PADMANABHAN HOLOGRAPHIC EQUIPARTITION, CELL COUNT.
  Derivation: Padmanabhan's emergent-gravity statement is that a static horizon satisfies
  E = (1/2) N k_B T with N the surface Planck-cell count. Evaluate both sides for de Sitter and take the
  ratio E_surf/Mc^2. If equipartition holds exactly the ratio is 1; if it does not, the mismatch is a forced
  factor, and the acceleration follows from the temperature that WOULD make it hold, through a_Unruh.

CONSTRUCTION C3 -- THE SAME, BUT WITH THE ENTROPY COUNT S = N/4.
  Derivation: identical to C2 except that the number of degrees of freedom is the ENTROPY S/k_B = N/4 rather
  than the raw cell count N. This is the construction the Bekenstein-Hawking quarter actually enters, and it
  is the whole reason this route was flagged: it is the only place in the problem where a factor 4 is forced
  rather than chosen.

CONSTRUCTION C4 -- KOMAR/TOLMAN ACTIVE MASS.
  Derivation: for Lambda the active gravitational mass density is rho + 3p/c^2 = rho_Lambda - 3 rho_Lambda =
  -2 rho_Lambda, so the Komar acceleration carries |rho+3p| = 2 rho_Lambda. Reported here for completeness
  because a0 ~ sqrt(G rho) makes this a factor sqrt(2), not 2 -- already retired in
  mi_kappa_linear_class_2026 and re-derived here so the retirement is in code, not prose.

  H1  what the route supplies, and the NUMBER-FIELD structure of its ingredients
  H2  the four constructions, all evaluated, all reported
  H3  the combinatorial look-elsewhere: how cheap is it to hit 32pi/3 from these ingredients?
  H4  verdict, and what remains

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 106)
    print(f"  {t}")
    print("=" * 106)


Z_FW = math.sqrt(32 * math.pi / 3)
K_REF = math.sqrt(8 * math.pi / 3)          # kappa at Z = 1
A0_BOX = 0.16                                # the corpus's own empirical +/-16% box on a0


def kappa_of_Z(Z):
    return K_REF / Z


def in_box(k):
    return abs(k / 0.5 - 1) <= A0_BOX


banner("H1  WHAT THE ROUTE SUPPLIES -- and the number-field structure of its ingredients")

# symbolic, in units where the horizon quantities are expressed through H_Lambda
c, G, hb, HL, kB = sp.symbols("c G hbar H_Lambda k_B", positive=True)
R_H = c / HL
A = 4 * sp.pi * R_H**2
lP2 = G * hb / c**3
N_cells = sp.simplify(A / lP2)
S_over_kB = sp.simplify(A / (4 * lP2))
T_GH = hb * HL / (2 * sp.pi * kB)
rho_L = 3 * HL**2 / (8 * sp.pi * G)
V = sp.Rational(4, 3) * sp.pi * R_H**3
Mc2 = sp.simplify(rho_L * V * c**2)

print(f"  N (Planck cells on the horizon) = {N_cells}")
print(f"  S/k_B = A/(4 l_P^2)             = {S_over_kB}")
check(sp.simplify(S_over_kB - N_cells / 4) == 0,
      f"H1a S/k_B = N/4 exactly -- the Bekenstein-Hawking quarter is the ONE forced factor 4 in this problem, "
      f"and it is why this route was flagged as the lead for Z^2 = 4 x (8pi/3)")
print(f"  M c^2 (enclosed de Sitter energy) = {Mc2}")

# THE STRUCTURAL POINT: every ingredient is rational x a power of pi. Z^2 is; Z is not.
Z2_sym = sp.nsimplify(32 * sp.pi / 3)
print(f"\n  Z^2 = {Z2_sym} -- a RATIONAL multiple of pi^1")
print(f"  Z   = sqrt(32pi/3) = {sp.sqrt(Z2_sym)} -- carries sqrt(pi), i.e. pi^(1/2)")
check(sp.simplify(Z2_sym / sp.pi).is_rational and not sp.simplify(sp.sqrt(Z2_sym) / sp.sqrt(sp.pi)).has(sp.pi),
      f"H1b *** THE ADMISSIBILITY SPLIT. *** Every ingredient this route supplies (4pi area, the 4 in S=A/4G, "
      f"4pi/3 volume, 2pi in Unruh and in T_GH, 8pi Einstein, 3 Friedmann) is a rational multiple of an "
      f"INTEGER power of pi. Products of those can equal Z^2 = 32pi/3 (rational x pi^1, ADMISSIBLE) but can "
      f"never equal Z = sqrt(32pi/3), which carries pi^(1/2). So the route can only force Z^2 -- confirming "
      f"mi_kappa_linear_class_2026's K4b that the quadratic variable is the right one -- and any construction "
      f"that fixes Z or a TEMPERATURE linearly is obstructed before it starts")
print("""
  This is the same argument class as the corpus's particle-sector obstruction (Z carries sqrt(pi) while all
  flavour data are algebraic), so it is not new evidence -- it is that argument applied here. What is new is
  the DIRECTION it gives: an admissible construction must be an AREA/ENTROPY relation (quadratic in R_H),
  not a temperature or count matching (linear).""")


banner("H2  THE FOUR CONSTRUCTIONS -- all evaluated, all reported")

results = []

# ---- C1: Unruh temperature matching, a0 = a_Unruh(T_GH)
a_C1 = sp.simplify(2 * sp.pi * c * kB * T_GH / hb)
Z_C1 = sp.simplify(c * HL / a_C1)
results.append(("C1 Unruh/GH temperature matching", float(Z_C1), "a0 = a_Unruh(T_GH)"))

# ---- C2: Padmanabhan equipartition with the CELL count N
E_C2 = sp.simplify(sp.Rational(1, 2) * N_cells * kB * T_GH)
ratio_C2 = sp.simplify(E_C2 / Mc2)
# the temperature that WOULD make equipartition hold, and its Unruh acceleration
T_C2 = sp.simplify(2 * Mc2 / (N_cells * kB))
Z_C2 = sp.simplify(c * HL / (2 * sp.pi * c * kB * T_C2 / hb))
results.append(("C2 equipartition, cell count N", float(Z_C2), f"E_surf/Mc^2 = {ratio_C2}"))

# ---- C3: the same with the ENTROPY count S/k_B = N/4  <-- the BH quarter enters here
T_C3 = sp.simplify(2 * Mc2 / (S_over_kB * kB))
Z_C3 = sp.simplify(c * HL / (2 * sp.pi * c * kB * T_C3 / hb))
ratio_C3 = sp.simplify(sp.Rational(1, 2) * S_over_kB * kB * T_GH / Mc2)
results.append(("C3 equipartition, ENTROPY count N/4", float(Z_C3), f"E_surf/Mc^2 = {ratio_C3}"))

# ---- C4: Komar/Tolman active mass -- enters a0 ~ sqrt(G rho) as sqrt(2)
Z_C4 = Z_FW / math.sqrt(2)
results.append(("C4 Komar |rho+3p| = 2 rho_Lambda", Z_C4, "factor sqrt(2) in a0, not 2"))

print(f"  {'construction':<38}{'Z':>10}{'kappa':>10}{'vs 1/2':>10}{'in a0 box?':>12}  note")
print("  " + "-" * 104)
for nm, Zv, note in results:
    kv = kappa_of_Z(Zv)
    print(f"  {nm:<38}{Zv:>10.5f}{kv:>10.5f}{100*(kv/0.5-1):>+9.1f}%{'YES' if in_box(kv) else 'no':>12}  {note}")
print(f"  {'framework (target)':<38}{Z_FW:>10.5f}{0.5:>10.5f}{0.0:>+9.1f}%{'YES':>12}  kappa = 1/2")

check(abs(float(Z_C1) - 1.0) < 1e-9,
      f"H2a C1 reproduces the corpus's recorded F1 result exactly: Unruh/GH matching gives Z = "
      f"{float(Z_C1):.6f}, kappa = {kappa_of_Z(float(Z_C1)):.5f}, i.e. a0 = cH_Lambda and "
      f"a0_temp/a0_dens = {Z_FW/float(Z_C1):.4f} = Z. Machinery validated against a known number before any "
      f"new construction is trusted")
check(sp.simplify(ratio_C2 - 2) == 0,
      f"H2b C2: the horizon's equipartition energy on the CELL count is E_surf/Mc^2 = {ratio_C2} EXACTLY -- a "
      f"clean forced factor of 2, which is the size of the discrepancy this whole route was chosen to explain "
      f"(Z^2 needs a 4, i.e. Z needs a 2). Promising, and H2c is what it actually gives")
check(abs(float(Z_C3) - 0.5) < 1e-9,
      f"H2c *** C3 -- THE ONE WITH THE BEKENSTEIN-HAWKING QUARTER IN IT -- GIVES Z = {float(Z_C3):.5f}, i.e. "
      f"a0 = 2 c H_Lambda, WHICH IS MILGROM 1999's COEFFICIENT, NOT OURS. *** kappa = "
      f"{kappa_of_Z(float(Z_C3)):.4f}, a factor {kappa_of_Z(float(Z_C3))/0.5:.2f} from 1/2. So the forced 4 in "
      f"S = A/4G does enter, and it enters on the WRONG SIDE: it makes a0 LARGER, not smaller. This is the "
      f"lead the previous script flagged, cashed out, and it lands on prior art")
check(not any(in_box(kappa_of_Z(Zv)) for _, Zv, _ in results),
      f"H2d NO construction lands inside the empirical a0 box. The four give kappa = "
      f"{', '.join(f'{kappa_of_Z(Zv):.3f}' for _, Zv, _ in results)} against the required 0.500. Every one is "
      f"an O(1) multiple of cH_Lambda because that is the only acceleration a horizon supplies -- exactly the "
      f"pattern H1b predicts for constructions that fix a temperature or a count LINEARLY")


banner("H3  THE COMBINATORIAL LOOK-ELSEWHERE -- how cheap is it to hit 32pi/3?")

# Enumerate rational x pi^k from the ingredients the route actually supplies, and count how many land in the
# empirical box ON Z^2. If many do, then "32pi/3 is entropy-natural" is worth nothing.
Z2_TARGET = 32 * math.pi / 3
z2_lo = (Z_FW * (1 - A0_BOX)) ** 2 / Z2_TARGET      # a0 ~ 1/Z, so the box maps to a Z^2 window
z2_hi = (Z_FW / (1 - A0_BOX)) ** 2 / Z2_TARGET
print(f"  the +/-{100*A0_BOX:.0f}% a0 box maps to Z^2 within [{z2_lo:.4f}, {z2_hi:.4f}] x 32pi/3, i.e. "
      f"Z^2 in [{z2_lo*Z2_TARGET:.3f}, {z2_hi*Z2_TARGET:.3f}]")
NUMS = list(range(1, 37))   # must reach 32/3 or the admissibility check in H3a is vacuous
DENS = [1, 2, 3, 4, 6, 8, 12]
KS = [0, 1, 2]
vals = set()
for p, q, k in itertools.product(NUMS, DENS, KS):
    f = Fraction(p, q)
    v = float(f) * math.pi**k
    if v > 0:
        vals.add((f, k, v))
inbox = [(f, k, v) for f, k, v in vals if z2_lo * Z2_TARGET <= v <= z2_hi * Z2_TARGET]
exact = [(f, k, v) for f, k, v in vals if abs(v / Z2_TARGET - 1) < 1e-12]
print(f"  enumerated {len(vals)} distinct values r*pi^k with r = p/q, p in 1..36, q in {DENS}, k in {KS}")
print(f"  landing inside the box: {len(inbox)}")
for f, k, v in sorted(inbox, key=lambda t: t[2])[:14]:
    tag = "  <-- 32pi/3, THE FRAMEWORK" if abs(v / Z2_TARGET - 1) < 1e-12 else ""
    print(f"      {str(f):>7} * pi^{k}  = {v:8.4f}   kappa = {kappa_of_Z(math.sqrt(v)):.5f}{tag}")
check(len(exact) == 1,
      f"H3a 32pi/3 IS in the enumerated class -- exactly {len(exact)} hit (32/3 x pi^1) -- confirming H1b's "
      f"admissibility claim CONSTRUCTIVELY rather than by assertion. Note the enumeration had to be widened "
      f"to p <= 36 to contain it: at p <= 16 the target is not reachable at all, which would have made this "
      f"check vacuous. Widening it also raises the look-elsewhere in H3b, which is the honest direction")
bits = math.log2(len(inbox)) if len(inbox) > 1 else 0.0
check(len(inbox) > 3,
      f"H3b *** BUT IT IS CHEAP. *** {len(inbox)} distinct values in this small, honestly-bounded ingredient "
      f"set land inside the empirical box, so 'Z^2 = 32pi/3 is entropy-natural' is worth at most "
      f"log2({len(inbox)}) = {bits:.2f} bits -- and that is BEFORE the 3.00 bits already spent on this axis. "
      f"A construction that merely PRODUCES a rational x pi in the box has explained nothing; only one that "
      f"forces 32/3 specifically, derived before evaluation, would count")


banner("H4  VERDICT")

print(f"""  *** THE HORIZON-ENTROPY ROUTE IS ADMISSIBLE IN PRINCIPLE AND EMPTY IN PRACTICE, and the reason is
  structural rather than a run of bad luck. ***

  ADMISSIBLE: Z^2 = 32pi/3 is a rational multiple of pi, and every ingredient the horizon supplies is a
  rational multiple of an integer power of pi (H1b, H3a). So unlike the particle sector -- where Z's sqrt(pi)
  against algebraic flavour data is a hard obstruction -- there is no number-field barrier here, PROVIDED the
  construction fixes Z^2. That confirms K4b's direction: the quadratic variable is the right one.

  EMPTY: all four constructions fix a TEMPERATURE or a COUNT, which are linear, and every one lands at Z of
  order one: {', '.join(f'{Zv:.3f}' for _, Zv, _ in results)} against the required {Z_FW:.3f}. That is not
  coincidence -- cH_Lambda is the only acceleration a de Sitter horizon supplies, so any linear matching
  returns an O(1) multiple of it, and the framework needs a suppression of {Z_FW:.2f} carrying sqrt(pi) that
  no product of the route's ingredients can produce (H1b).

  AND THE SHARPEST RESULT, which cuts against the framework: C3 is the construction the Bekenstein-Hawking
  quarter actually enters -- equipartition on the ENTROPY count S = N/4 rather than the cell count -- and it
  gives a0 = 2 c H_Lambda, i.e. **MILGROM 1999's coefficient**, not ours. The forced 4 does appear, and it
  appears on the WRONG SIDE: it makes a0 larger. The factor-4 coincidence flagged as a lead in
  mi_kappa_linear_class_2026 is hereby CASHED OUT AND CLOSED -- it was real, and it points at prior art.
  Together with the spectral axis picking 2pi (that script's K3c), this is now the SECOND independent
  theory-side argument that lands on a rival coefficient rather than kappa = 1/2.

  LOOK-ELSEWHERE, honestly: {len(inbox)} values in a small bounded ingredient set already land inside the
  empirical a0 box, so 'entropy-natural' is worth <= {bits:.2f} bits on its own, on top of the 3.00 bits already
  spent. Total attempts on deriving kappa is now 8 + 4 = 12, log2(12) = {math.log2(12):.2f} bits.

  WHAT REMAINS OF THIS ROUTE, stated precisely so it is not re-opened casually: an AREA or ENTROPY relation
  that fixes Z^2 DIRECTLY -- quadratic in R_H, never passing through a temperature -- and derived before its
  value is evaluated. H1b says that is the only shape that can work. This script did not find one, and
  inventing one now, after seeing that C1-C4 fail, would be the exact move the atomos null paper documents.

  *** kappa = 1/2 REMAINS FITTED, NOT DERIVED. *** Two of the three routes named as outside the spectral
  family are now closed (this one, and the CKN/boundary-counting slot closed earlier). The third -- a
  first-principles derivation of the kernel measure that does not pass through the RAR calibration -- is
  untouched and is the only one left.""")

banner("RESULT")
nn = sum(1 for x, _ in ok if x)
print(f"  {nn}/{len(ok)} checks held.")
if nn != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: admissible for Z^2, obstructed for Z; the BH quarter cashes out to Milgrom 1999's 2cH_Lambda.")
