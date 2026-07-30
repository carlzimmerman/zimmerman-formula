"""
(d) THE SCEPTIC'S DENSITY ESTIMATE for Z = sqrt(32 pi / 3) = 5.788809...

Question: how many 'simple closed forms built from pi and small integers' land
within 1% of 5.7888?  If many, matching Z is not surprising and a geometric
origin hunt is chasing noise.

Method: exhaustive iterative-deepening enumeration over a closed-form grammar,
with a complexity budget = node count.  Dedup by value.  Then measure:
  (i) raw hit count in +-1% of Z
  (ii) COVERAGE: fraction of a log-uniform reference band that is within 1%
       of SOME expression of the same complexity  -> the honest surprise metric
  (iii) the natural sub-family sqrt(a*pi/b) that Z itself belongs to
  (iv) sensitivity to the real empirical tolerance on a0 (not 1%)
"""
import math, itertools
from fractions import Fraction

PI = math.pi
Z = math.sqrt(32*PI/3)

# ---------------- grammar ----------------
# atoms (complexity 1): small integers and pi
ATOMS = {}
for n in range(1, 13):
    ATOMS[float(n)] = str(n)
ATOMS[PI] = "pi"

UNARY = [
    ("sqrt",  lambda x: math.sqrt(x) if x > 0 else None),
    ("sq",    lambda x: x*x if abs(x) < 1e6 else None),
    ("cube",  lambda x: x**3 if abs(x) < 1e4 else None),
    ("inv",   lambda x: 1.0/x if abs(x) > 1e-12 else None),
    ("cbrt",  lambda x: x**(1/3) if x > 0 else None),
]
BINARY = [
    ("+", lambda a, b: a+b),
    ("-", lambda a, b: a-b),
    ("*", lambda a, b: a*b),
    ("/", lambda a, b: a/b if abs(b) > 1e-12 else None),
]

KEY = 1e-10          # dedup resolution (relative)
LO, HI = 1.0, 40.0   # keep values in a generous band around Z (and Z^2=33.5)

def key(v):
    return round(v/KEY) if abs(v) < 1e7 else None

def enumerate_upto(maxc):
    """levels[c] = dict value->expr for expressions of complexity exactly c"""
    levels = {1: dict(ATOMS)}
    seen = {key(v): v for v in ATOMS}
    for c in range(2, maxc+1):
        cur = {}
        # unary on complexity c-1
        for v, e in levels[c-1].items():
            for nm, f in UNARY:
                try:
                    w = f(v)
                except (OverflowError, ValueError, ZeroDivisionError):
                    w = None
                if w is None or not math.isfinite(w):
                    continue
                k = key(w)
                if k is None or k in seen:
                    continue
                seen[k] = w
                cur[w] = f"{nm}({e})"
        # binary: complexities i + j = c-1
        for i in range(1, c-1):
            j = c-1-i
            if j not in levels:
                continue
            for v1, e1 in levels[i].items():
                for v2, e2 in levels[j].items():
                    for nm, f in BINARY:
                        try:
                            w = f(v1, v2)
                        except (OverflowError, ValueError, ZeroDivisionError):
                            w = None
                        if w is None or not math.isfinite(w) or abs(w) > 1e7:
                            continue
                        k = key(w)
                        if k is None or k in seen:
                            continue
                        seen[k] = w
                        cur[w] = f"({e1}{nm}{e2})"
        levels[c] = cur
    return levels

def all_values(levels, maxc):
    out = {}
    for c in range(1, maxc+1):
        for v, e in levels[c].items():
            if LO <= v <= HI:
                out.setdefault(v, (c, e))
    return out

MAXC = 6
levels = enumerate_upto(MAXC)
vals = all_values(levels, MAXC)
print(f"grammar: atoms 1..12 and pi; unary sqrt/x^2/x^3/1-over-x/cbrt; binary + - * /")
print(f"complexity budget (node count) <= {MAXC}")
print(f"distinct values generated in [{LO},{HI}]: {len(vals)}")

# ---------------- (i) raw hits within 1% of Z ----------------
tol = 0.01
hits = sorted([(v, c, e) for v, (c, e) in vals.items() if abs(v/Z - 1) <= tol],
              key=lambda t: (t[1], abs(t[0]-Z)))
print(f"\n(i) expressions within 1% of Z={Z:.6f}: {len(hits)}")
for v, c, e in hits[:40]:
    print(f"    c={c}  {v:.6f}  ({100*(v/Z-1):+.3f}%)  {e}")
if len(hits) > 40:
    print(f"    ... and {len(hits)-40} more")

# hits at each complexity budget
print("\n    hits within 1% by complexity budget:")
for cb in range(2, MAXC+1):
    sub = all_values(levels, cb)
    n = sum(1 for v in sub if abs(v/Z-1) <= tol)
    print(f"      c<={cb}: {n:6d} hits   (pool {len(sub)} values in band)")

# ---------------- (ii) COVERAGE: is Z special at all? ----------------
# fraction of log-uniform targets in [3,12] matched within 1% by SOME expression
import random
random.seed(0)
band = sorted(v for v in vals if 3.0 <= v <= 12.0)
def matched(t, arr, tol):
    import bisect
    i = bisect.bisect_left(arr, t*(1-tol))
    return i < len(arr) and arr[i] <= t*(1+tol)
N = 200000
lo, hi = math.log(3.0), math.log(12.0)
cov = sum(1 for _ in range(N) if matched(math.exp(random.uniform(lo, hi)), band, tol))/N
print(f"\n(ii) COVERAGE of the grammar (c<={MAXC}) over log-uniform targets in [3,12]:")
print(f"     fraction of ARBITRARY targets matched within 1% : {cov*100:.2f}%")
for cb in range(2, MAXC+1):
    sub = sorted(v for v in all_values(levels, cb) if 3.0 <= v <= 12.0)
    cv = sum(1 for _ in range(20000) if matched(math.exp(random.uniform(lo, hi)), sub, tol))/20000
    print(f"       c<={cb}: coverage {cv*100:6.2f}%  ({len(sub)} values in [3,12])")

# ---------------- (iii) the sub-family Z itself lives in ----------------
# Z = sqrt(a*pi/b).  How many sqrt(a*pi/b), a,b small integers, hit within 1%?
print(f"\n(iii) sub-family sqrt(a*pi/b) (Z's OWN form, Z^2 = 32pi/3 -> a/b = {32/3:.6f}):")
for AMAX, BMAX in [(40, 12), (100, 20), (200, 40)]:
    fam = set()
    for a in range(1, AMAX+1):
        for b in range(1, BMAX+1):
            fr = Fraction(a, b)
            if fr in fam:
                continue
            v = math.sqrt(a*PI/b)
            if abs(v/Z-1) <= tol:
                fam.add(fr)
    print(f"      a<={AMAX}, b<={BMAX}: {len(fam)} distinct reduced ratios a/b give sqrt(a pi/b) within 1% of Z")
    if AMAX == 40:
        for fr in sorted(fam):
            v = math.sqrt(float(fr)*PI)
            print(f"          sqrt({fr.numerator}pi/{fr.denominator}) = {v:.6f}  ({100*(v/Z-1):+.3f}%)"
                  + ("   <-- Z" if fr == Fraction(32,3) else ""))

# also: rational*sqrt(pi), rational*pi^k etc.
print("\n      other one-line families hitting within 1% (a,b<=20):")
fams = {
    "a*pi/b":        lambda a,b: a*PI/b,
    "a/(b*pi)":      lambda a,b: a/(b*PI),
    "sqrt(a/b)*pi":  lambda a,b: math.sqrt(a/b)*PI,
    "a*sqrt(pi)/b":  lambda a,b: a*math.sqrt(PI)/b,
    "(a*pi/b)^(1/3)":lambda a,b: (a*PI/b)**(1/3),
    "a*pi^2/b":      lambda a,b: a*PI*PI/b,
    "a/b (rational)":lambda a,b: a/b,
}
for nm, f in fams.items():
    s = set()
    for a in range(1, 21):
        for b in range(1, 21):
            if abs(f(a,b)/Z-1) <= tol:
                s.add(Fraction(a,b))
    print(f"        {nm:16s}: {len(s)} distinct reduced a/b")

# ---------------- (iv) the REAL tolerance ----------------
print("\n(iv) but 1% is not the honest tolerance. a0 is empirically pinned only to ~10-20%")
print("     (M/L + interpolation systematics), so Z is pinned only to the same relative width.")
for t in [0.01, 0.05, 0.10, 0.16, 0.20]:
    n = sum(1 for v in vals if abs(v/Z-1) <= t)
    b2 = sorted(v for v in vals if 3.0 <= v <= 12.0)
    cv = sum(1 for _ in range(20000) if matched(math.exp(random.uniform(lo, hi)), b2, t))/20000
    print(f"     tol={t*100:5.1f}% : {n:7d} expressions match Z ; coverage of arbitrary targets = {cv*100:6.2f}%")
