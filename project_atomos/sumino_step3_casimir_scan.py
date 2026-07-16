#!/usr/bin/env python3
"""
SUMINO STEP 3 -- the (i) condition: does ANY group FORCE p2/p1^2 = 2/3 (r=sqrt2) with ZERO knobs?
A forced Koide needs a symmetry that pins the invariant ratio (Sum l^2)/(Sum l)^2 = 2/3 as a
canonical alignment / Casimir, not a tuned potential minimum. We scan (a) the forced VEV
alignments discrete flavor groups actually produce, (b) small rational alignments, and (c)
quadratic-Casimir ratios of standard Lie reps -- with a look-elsewhere count. Honest prior: null.
"""
import numpy as np
from itertools import product
np.seterr(all="ignore")
TARGET = 2/3

def Q(v):
    v = np.asarray(v, float)
    s = v.sum()
    return (v**2).sum()/s**2 if s != 0 else np.inf

# ---------------------------------------------------------------------------
print("="*84)
print("(a) FORCED VEV ALIGNMENTS that discrete flavor groups (S3,A4,S4,T',Delta27) produce")
print("="*84)
# the standard 0-parameter fixed directions used in flavor model building (real reps):
aligns = {
 "(1,1,1) democratic": (1,1,1),
 "(1,0,0) & perms":    (1,0,0),
 "(1,1,0) & perms":    (1,1,0),
 "(2,1,1)":            (2,1,1),
 "(1,1,2)":            (1,1,2),
 "(3,1,1)":            (3,1,1),
 "(1,1,-2) [traceless]":(1,1,-2),
 "(2,-1,-1) [traceless]":(2,-1,-1),
 "(1,-1,0) [traceless]":(1,-1,0),
}
for name,v in aligns.items():
    q=Q(v); tag = "  <== 2/3!" if abs(q-TARGET)<1e-9 else ""
    print(f"   {name:24s} Q = {q:.5f}{tag}")
print("   -> the real forced alignments give Q in {1/3, 1/2, 1, ...} or are traceless (p1=0).")
print("      NONE equals 2/3.\n")

# ---------------------------------------------------------------------------
print("="*84)
print("(b) is 2/3 reachable by ANY small RATIONAL (integer) alignment?  3(Sum l^2) = 2(Sum l)^2")
print("="*84)
exact=[]; best=(9,None)
for a,b,c in product(range(0,61),repeat=3):
    if a+b+c==0: continue
    q=(a*a+b*b+c*c)/((a+b+c)**2)
    if abs(q-TARGET)<abs(best[0]-TARGET): best=(q,(a,b,c))
    if abs(q-TARGET)<1e-12: exact.append((a,b,c))
print(f"   searched all integer triples 0..60: EXACT Q=2/3 solutions found = {len(exact)}")
print(f"   closest integer triple: {best[1]}  Q={best[0]:.6f}  (|Q-2/3|={abs(best[0]-TARGET):.2e})")
# the exact real solution needs sqrt2:
c = 4+3*np.sqrt(2)
print(f"   the exact solution (1,1,c) needs c = 4 + 3*sqrt(2) = {c:.5f}  -> the amplitude is r=sqrt2.")
print("   -> No small rational alignment gives 2/3 (searched 0..60). Koide's r=sqrt2 is irrational")
print("      but ALGEBRAIC (Q(sqrt2), root of x^2-2). BOTH-WAYS NOTE: sqrt2 is algebraic and CAN appear")
print("      in discrete-group Clebsch-Gordan coefficients, so irrationality ALONE does not forbid a")
print("      discrete group from producing it. Do NOT conflate with the a0/Z obstruction (that is about")
print("      the TRANSCENDENTAL sqrt(pi)). The gap is forcing r=sqrt2 with no knob, not impossibility.\n")

# ---------------------------------------------------------------------------
print("="*84)
print("(c) QUADRATIC-CASIMIR ratios of standard Lie reps -- does C2(R)/C2(R') hit 2/3, forced?")
print("="*84)
# C2 in a common normalization (C2(fund SU(N)) = (N^2-1)/(2N); adjoint = N; etc.)
def c2_suN(N, kind):
    if kind=="fund": return (N*N-1)/(2*N)
    if kind=="adj":  return float(N)
    return None
casimirs = {}
for N in (2,3,4,5,6):
    casimirs[f"SU{N}-fund"]=c2_suN(N,"fund"); casimirs[f"SU{N}-adj"]=c2_suN(N,"adj")
# a few exceptional / SO values (standard C2, GUT-normalized enough for a ratio scan)
casimirs.update({"SO10-16":45/8, "SO10-adj45":8.0, "E6-27":26/6, "E6-adj78":12.0,
                 "G2-7":2.0, "G2-adj14":4.0, "F4-26":6.0, "F4-adj52":9.0})
names=list(casimirs); ratios=[]
for i in names:
    for j in names:
        if i==j or casimirs[j]==0: continue
        r=casimirs[i]/casimirs[j]; ratios.append((r,i,j))
near = [(r,i,j) for (r,i,j) in ratios if abs(r-TARGET)<0.05]
exact_c = [(r,i,j) for (r,i,j) in ratios if abs(r-TARGET)<1e-9]
print(f"   scanned {len(ratios)} Casimir ratios; within 5% of 2/3: {len(near)}; EXACT 2/3: {len(exact_c)}")
for r,i,j in exact_c[:8]:
    print(f"     C2({i})/C2({j}) = {r:.5f} = 2/3 exactly")
print(f"   look-elsewhere: {len(near)} of {len(ratios)} land near 2/3 -> E_chance~{len(near)} >> 1")
print("   -> 2/3 is a SIMPLE rational densely surrounded by Casimir ratios: any hit is UNSURPRISING")
print("      (FDR-dead), AND the 'linear invariant' p1 is a free U(1) charge, not a forced Casimir,")
print("      so C2/p1^2 is dialable -> not forced. AND none of these fixes the 2nd observable (delta).\n")

# ---------------------------------------------------------------------------
print("="*84)
print("VERDICT -- (i) condition (both-ways, no manufactured result)")
print("="*84)
print(f"""  Forced 2/3 with zero knobs: NOT FOUND.
   (a) No real forced discrete-flavor alignment gives 2/3 (they give 1/3, 1/2, 1, or are traceless).
   (b) No small rational alignment gives 2/3 (searched 0..60; closest 6.6e-5 off). Koide's amplitude
       r=sqrt2 is irrational but ALGEBRAIC (Q(sqrt2), root of x^2-2). BOTH-WAYS CORRECTION: sqrt2 is
       algebraic and CAN arise in discrete-group Clebsch-Gordan coefficients, so irrationality does
       NOT by itself forbid a group producing it (DIFFERENT from the a0/Z obstruction, which is the
       TRANSCENDENTAL sqrt(pi)). The scan finds no group that FORCES 2/3; it does not prove impossibility.
   (c) Casimir ratios hitting 2/3 exist but are DENSITY coincidences (2/3 is a simple rational,
       E_chance >> 1 -> FDR-dead), the linear invariant p1 is a free U(1) charge (dialable, not a
       Casimir), and none forces the 2nd observable (delta).

  So the (i) condition -- 2/3 as a FORCED group Casimir RATIO -- FAILS: the 2/3 hits are density
  coincidences (E_chance>>1, FDR-dead), the linear invariant p1 is a free U(1) charge (dialable),
  and none forces the 2nd observable (delta). No standard forced alignment gives 2/3 either. What
  the scan does NOT do is prove impossibility: r=sqrt2 is algebraic (Q(sqrt2)) and could live in a
  Clebsch-Gordan coefficient. The honest open gap: nobody has a structure forcing r=sqrt2 AND delta
  together with zero knobs (Sumino tunes them). Bounded scan, run, honestly null -- un-forced, not
  proven shut. That is why the puzzle is 40+ years open, and it is the clean question for a mathematician.""")
print("EXIT 0")
