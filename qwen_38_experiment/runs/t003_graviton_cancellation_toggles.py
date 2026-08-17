#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T003 -- graviton-bath cancellation, assumption-minimal.

Hypothesis (TASKS.md T003): EXACTLY ONE assumption in the committed chain
    S_dS = pi/(G H^2),  T_dS = H/2pi,  eps_1 = G T_dS^2/8,  eps_tot = S_dS*eps_1,
    H^2 = 8 pi G rho/3,  a0^2 = 3 eps_tot c^2 H^2,  kappa^2 = a0^2/(c^2 G rho)
is load-bearing for kappa^2 = 8 pi eps_tot.

Method: sympy re-derivation with a per-assumption coefficient knob; toggle each knob
and record which toggles move kappa. PASS = the assumption-dependency table.
KILL guard = the cancellation must REPRODUCE (S_dS*G H^2 = pi, kappa^2 = 8 pi eps_tot,
eps_tot = 1/(32 pi)); if it fails to reproduce the committed memory
(real_research/reviews/mi_graviton_bath_ctp_2026.py Part C) is flagged for
correction (DEFICIT-risk).

Symbolic re-derivation, NOT a search -> no FDR pre-registration needed.
Both footings N/A: kappa is a dimensionless, footing-invariant pure number.
"""
import sympy as sp

_fail = []
def check(cond, msg, detail=""):
    if cond:
        print("  ok   " + msg)
    else:
        _fail.append(msg)
        print("  FAIL " + msg + (("  [" + detail + "]") if detail else ""))

# ---------------------------------------------------------------------------
# symbols
# ---------------------------------------------------------------------------
G, H, rho = sp.symbols('G H rho', positive=True)
c = sp.Symbol('c', positive=True)                 # c, cancels
# per-assumption coefficient knobs; committed values below
c1, c2, c3, c4, c5, c6, c7 = sp.symbols('c1 c2 c3 c4 c5 c6 c7', positive=True)
ASSUMP = {
 "A1 entropy        S_dS = pi/(G H^2)":          c1,
 "A2 temperature    T_dS = H/(2 pi)":            c2,
 "A3 two-point      eps_1 = G T_dS^2/8":         c3,
 "A4 incoherent-sum eps_tot = S_dS*eps_1":       c4,
 "A5 Friedmann      H^2 = 8 pi G rho/3":         c5,
 "A6 mechanism      a0^2 = 3 eps_tot c^2 H^2":   c6,
 "A7 kappa-def      kappa^2 = a0^2/(c^2 G rho)": c7,
}
# committed knob values (A5=8/3 and A6=3 are the only non-unit coefficients)
COMMITTED = {c1:1, c2:1, c3:1, c4:1, c5:sp.Rational(8,3), c6:3, c7:1}

# ---------------------------------------------------------------------------
# build the chain symbolically with knobs
# ---------------------------------------------------------------------------
S_dS   = c1 * sp.pi/(G*H**2)
T_dS   = H/(2*sp.pi*c2)
eps_1  = c3 * G*T_dS**2/8
eps_tot = c4 * S_dS * eps_1
H2     = c5 * sp.pi * G * rho
a0_sq  = c6 * eps_tot * c**2 * H2
kappa_sq = sp.simplify(c7 * a0_sq/(c**2 * G * rho))

print("=" * 78)
print("T003  graviton-bath cancellation -- assumption-dependency table")
print("=" * 78)

# ---------------------------------------------------------------------------
# [1] KILL GUARD -- does the committed cancellation REPRODUCE?
# ---------------------------------------------------------------------------
print("\n[1] KILL GUARD -- reproduce the committed cancellation")
subs = dict(COMMITTED)
eps_tot_c = sp.simplify(eps_tot.subs(subs))
kappa_sq_c = sp.simplify(kappa_sq.subs(subs))
S_dS_c = sp.simplify(S_dS.subs(subs))
check(sp.simplify(S_dS_c*G*H**2 - sp.pi) == 0,
      "C2  S_dS*G H^2 = pi  (holographic cancellation: G & H drop out)")
check(sp.simplify(kappa_sq_c - 8*sp.pi*eps_tot_c) == 0,
      "C3  kappa^2 = 8 pi eps_tot  EXACTLY  (the relation that replaces the question)")
check(sp.simplify(eps_tot_c - 1/(32*sp.pi)) == 0,
      "C4  eps_tot = 1/(32 pi)  under normalisation A")
check(kappa_sq_c == sp.Rational(1,4),
      "C5  kappa^2 = 1/4  (kappa = 1/2 == framework's ADOPTED/FITTED 0.551+/-0.043)")
if _fail:
    print("\nKILL FIRED: the committed cancellation does NOT reproduce -- the memory "
          "mi_graviton_bath_ctp_2026.py Part C needs correction (DEFICIT-risk).")
    print("   eps_tot_c =", eps_tot_c, "  kappa_sq_c =", kappa_sq_c)
    raise SystemExit(1)
print("  -> KILL guard held: cancellation reproduces; proceed to the dependency table.")

# ---------------------------------------------------------------------------
# [2] TOGGLE TABLE -- which knob moves kappa?
# ---------------------------------------------------------------------------
print("\n[2] TOGGLE TABLE -- baseline = committed; toggle ONE knob to 2, recompute kappa^2")
print("    kappa_sq(knobs) =", kappa_sq, "   (G, H absent => the cancellation is intact)")
check(not kappa_sq.has(G) and not kappa_sq.has(H),
      "CANCEL  G and H ABSENT from kappa_sq -- holographic cancellation survives all toggles")

def k2_at(toggle=None, to=2):
    s = dict(COMMITTED)
    if toggle is not None:
        s[toggle] = to
    return sp.simplify(kappa_sq.subs(s))

k_base = k2_at()
load_bearing, inert = [], []
for name, knob in ASSUMP.items():
    k_tog = k2_at(toggle=knob, to=2)
    moves = (k_tog - k_base).simplify() != 0
    tag = "LOAD-BEARING" if moves else "inert"
    (load_bearing if moves else inert).append(name)
    print("   %-13s %-40s  kappa^2(=1)=%.6f -> kappa^2(=2)=%.6f"
          % (tag, name, float(k_base), float(k_tog)))

n_lb = len(load_bearing)
print("\n   load-bearing for kappa^2 = 8 pi eps_tot : %d" % n_lb)
for nm in load_bearing:
    print("      - " + nm)
if inert:
    print("   inert (absorbed by cancellation) : %d -> %s" % (len(inert), ", ".join(inert)))
else:
    print("   inert (absorbed by cancellation) : 0 (every form-coefficient moves kappa)")

# ---------------------------------------------------------------------------
# [3] single-knob demonstration: the two-point normalisation A3 alone spans 3 kappa
# ---------------------------------------------------------------------------
print("\n[3] one assumption (A3, two-point normalisation) alone spans the framework's kappa spread")
for lbl, factor in [("A  <h^2>=G T^2 (loose)", 1),
                    ("B  <phi^2>=T^2/12 (standard)", 32*sp.pi/12),
                    ("C  B x 2 graviton polarisations", 2*32*sp.pi/12)]:
    k2 = sp.simplify(kappa_sq.subs({**COMMITTED, c3: factor}))
    print("   %-36s  kappa = %.4f" % (lbl, float(sp.sqrt(k2))))

# ---------------------------------------------------------------------------
# [4] GRADE the hypothesis "EXACTLY ONE assumption is load-bearing"
# ---------------------------------------------------------------------------
print("\n[4] GRADE -- hypothesis: EXACTLY ONE assumption is load-bearing for kappa^2 = 8 pi eps_tot")
print("   load-bearing count = %d" % n_lb)
verdict = "REFUTED" if n_lb != 1 else "CONFIRMED"
print("   HYPOTHESIS %s (n_load-bearing = %d, not 1)" % (verdict, n_lb))
print("\n" + ("=" * 78))
print("T003 DONE: %d/7 form-assumptions LOAD-BEARING (count=%d != 1 -> HYP %s); "
      "cancellation S_dS*G H^2=pi & kappa^2=8 pi eps_tot & eps_tot=1/32pi all reproduce "
      "(KILL not fired); both footings N/A (dimensionless kappa)"
      % (n_lb, n_lb, verdict))

# internal checks (reproduction) must all hold; the hypothesis grade is a RESULT, not a check
if _fail:
    print("\n%d internal check(s) failed" % len(_fail))
    raise SystemExit(1)
