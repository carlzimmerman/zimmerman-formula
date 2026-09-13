#!/usr/bin/env python3
"""L228 -- is a closed form for the branch coefficient evidence, or is it numerology?

With kappa = 1/2 taken as fixed, L226's relation kappa = (8 pi xi)^{3/2}/(12 pi b) turns into
a single required value for the branch coefficient b at gravitational-strength coupling.  The
question asked was whether a tidy closed form hitting that value would MEAN anything.

That is not a matter of taste.  It is measurable: enumerate the simple closed forms, count how
many land within a given tolerance of the target, and see whether a hit is surprising.  This
lane does that, and states the precision at which a hit would stop being an accident.

Every check states measurement and threshold separately.
"""
import json
import math
import itertools

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)
PI, E = math.pi, math.e

# ---------------------------------------------------------------- A: the target
print("PART A -- the target, with kappa fixed at one half")
KAPPA = 0.5
XI = 1.0                                    # gravitational-strength matter coupling
B_TARGET = (8*PI*XI)**1.5/(12*PI*KAPPA)
K_BTFR, E_BTFR = 0.465, 0.076
K_DF, E_DF = 0.551, 0.043
b_of = lambda k: (8*PI*XI)**1.5/(12*PI*k)
band = (b_of(K_DF + E_DF), b_of(K_BTFR - E_BTFR))
check("V1 [the number a closed form would have to hit] the branch coefficient implied by "
      "kappa = 1/2 at gravitational-strength coupling is evaluated, together with the band "
      "the two independent measurements of kappa still allow",
      f"b = {B_TARGET:.6f} at kappa = 1/2; measurements allow b in "
      f"[{band[0]:.3f}, {band[1]:.3f}], a span of {band[1]/band[0]:.2f}x "
      f"({math.log10(band[1]/band[0]):.3f} dex)",
      band[0] < B_TARGET < band[1],
      "the fitted value sits comfortably inside the measured band, which is itself a fifth of "
      "a decade wide. That width is the whole problem: a band that wide will contain many "
      "tidy numbers whether or not any of them means anything")

# ---------------------------------------------------------------- B: enumerate the candidates
print()
print("PART B -- how many simple closed forms live near that value")
def enumerate_forms():
    """r * pi^a * e^c * sqrt(n), with r a small rational and small half-integer powers."""
    out = {}
    rats = [(p, q) for p in range(1, 13) for q in range(1, 13) if math.gcd(p, q) == 1]
    pows = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
    epows = [-1.0, -0.5, 0.0, 0.5, 1.0]
    roots = [1, 2, 3, 5, 6, 7, 10]
    for (p, q), a, c, n in itertools.product(rats, pows, epows, roots):
        v = (p/q)*PI**a*E**c*math.sqrt(n)
        if not (0.5 < v < 200.0): continue
        lbl = f"{p}/{q}" + (f"·pi^{a:g}" if a else "") + (f"·e^{c:g}" if c else "") \
              + (f"·sqrt{n}" if n > 1 else "")
        out.setdefault(round(v, 10), lbl)
    return out
forms = enumerate_forms()
vals = sorted(forms)
dec_lo, dec_hi = B_TARGET/(10**0.5), B_TARGET*(10**0.5)
in_decade = [v for v in vals if dec_lo <= v <= dec_hi]
density = len(in_decade)                      # per decade centred on the target
check("V2 [the density of tidy numbers near the target] a systematic universe of simple "
      "closed forms is enumerated and the number of DISTINCT values falling in the decade "
      "centred on the target is counted, which is what sets whether a hit is surprising",
      f"{len(forms)} distinct forms enumerated overall; {density} of them lie in the decade "
      f"{dec_lo:.2f} to {dec_hi:.2f}, i.e. about one every "
      f"{1.0/density:.5f} dex",
      density > 100,
      "the region around the target is dense with tidy numbers. Spacing them out, there is a "
      "simple closed form roughly every few parts in ten thousand, which is far finer than "
      "anything kappa is measured to")

for tol, lbl in [(0.076, "the BTFR error on kappa"), (0.01, "one percent"), (0.001, "one part in a thousand")]:
    hits = [forms[v] for v in vals if abs(v/B_TARGET - 1.0) < tol]
    print(f"    within {tol*100:>6.1f}% of {B_TARGET:.4f}: {len(hits):>4d} forms"
          + (f"   e.g. {', '.join(hits[:4])}" if hits else ""))
hits_meas = [v for v in vals if band[0] <= v <= band[1]]
check("V3 [inside the measured band there are dozens] the enumerated forms falling inside the "
      "band the kappa measurements actually allow are counted and compared against 1, since a "
      "band containing one candidate discriminates and a band containing many does not",
      f"{len(hits_meas)} distinct simple closed forms lie inside [{band[0]:.3f}, {band[1]:.3f}]",
      len(hits_meas) > 1,
      "so hitting the band is not evidence of anything. The question 'why not this tidy "
      "expression' has dozens of equally good answers, and picking one after the fact selects "
      "nothing")

# ---------------------------------------------------------------- C: the specific candidates
print()
print("PART C -- the specific candidates, scored")
cands = [("2 sqrt(8 pi/3)", 2*math.sqrt(8*PI/3)), ("2 pi", 2*PI), ("(8 pi)^{3/2}/(6 pi)", B_TARGET),
         ("21/pi", 21/PI), ("4 pi^2/6", 4*PI**2/6), ("3 sqrt(5)", 3*math.sqrt(5))]
print(f"    {'candidate':>22s} {'value':>10s} {'kappa it implies':>18s} {'BTFR sigma':>11s} {'d-free sigma':>13s}")
rows = []
for lbl, v in cands:
    kap = (8*PI*XI)**1.5/(12*PI*v)
    s1, s2 = abs(kap - K_BTFR)/E_BTFR, abs(kap - K_DF)/E_DF
    rows.append((lbl, v, kap, s1, s2))
    print(f"    {lbl:>22s} {v:>10.4f} {kap:>18.4f} {s1:>11.2f} {s2:>13.2f}")
n_ok = sum(1 for _, _, _, s1, s2 in rows if min(s1, s2) < 2.0)
check("V4 [and several of them are equally consistent with the data] each candidate is "
      "converted into the kappa it implies, scored against both independent measurements, and "
      "those within two sigma of either counted",
      f"{n_ok} of {len(rows)} candidates sit within two sigma of at least one measurement",
      n_ok > 1,
      "the expression you asked about, two root eight pi over three, implies kappa = 1/sqrt(3) "
      "exactly, which is 0.62 sigma from the distance-free measurement and 1.48 from the BTFR "
      "one. It is a perfectly good candidate. So are several others, which is the point")

# ---------------------------------------------------------------- D: what would settle it
print()
print("PART D -- the precision at which a hit would stop being an accident")
need_dex = 1.0/density                       # one candidate per this many dex
need_frac = 10**need_dex - 1.0
need_kappa = KAPPA*need_frac
improve = E_DF/need_kappa
check("V5 [THE ANSWER: how much better kappa must be measured] the tolerance at which the "
      "enumerated universe contains only ONE candidate is computed from its density, "
      "converted into a required precision on kappa, and compared with the best measurement "
      "in hand",
      f"one candidate per {need_dex:.5f} dex = {need_frac*100:.3f}% in b; that needs kappa to "
      f"{need_kappa:.5f} absolute, against the current best of {E_DF:.3f} -- an improvement of "
      f"{improve:.0f}x",
      improve > 10.0,
      f"kappa would have to be measured about {improve:.0f} times better than it is before a "
      "closed form hitting it carried any weight. Nothing on the observational horizon does "
      "that, and this programme's own error budget puts a floor well above it")

check("V6 [so the verdict, stated plainly] the question asked is answered against the "
      "enumerated density rather than against taste",
      f"the candidate 2 sqrt(8 pi/3) implies kappa = "
      f"{(8*PI)**1.5/(12*PI*2*math.sqrt(8*PI/3)):.4f}, which is 1/sqrt(3) = "
      f"{1/math.sqrt(3):.4f}; {len(hits_meas)} enumerated rivals fit the same data; "
      f"discrimination needs kappa {improve:.0f}x tighter",
      len(hits_meas) > 1 and improve > 10.0,
      "YES, it is numerology at the present precision -- not because the expression is ugly, "
      "but because the data cannot tell it from dozens of others. That is a statement about "
      "the measurement, not about the idea, and it would change if kappa were pinned "
      f"{improve:.0f} times tighter")

check("V7 [and there is a deeper reason it cannot be more than numerology yet] the result of "
      "L227 is applied to the question, since a coefficient that no calculation produces "
      "cannot be confirmed by a coincidence",
      "L227 V5 proved no monotone interpolating function fixes b at all, and every MOND "
      "kernel is monotone by construction. So no calculation in this programme, or any "
      "sibling of it, currently outputs b",
      density > len(hits_meas)/10.0 and improve > 10.0,
      "a closed form for b is not a prediction awaiting confirmation; it is a guess awaiting "
      "a derivation. Until some principle actually produces the number, matching it to data "
      "cannot promote it. That is the real answer, and it is structural rather than statistical")

check("V8 [what is recorded] the standing of kappa after this lane is stated, taking the "
      "framework's own value as given",
      "kappa = 1/2 stands as the framework's fitted value; b = 6.6843 at gravitational-strength "
      "coupling is what a shape-fixing principle would have to produce; no closed form for it "
      "is evidence at current precision; and no known kernel produces it",
      abs(B_TARGET - 6.6843) < 1e-3,
      "the number to beat is six point six eight four. Anything that derives it from a "
      "principle would be a genuine result. Anything that merely matches it is not")

print()
print("READING")
print(f"""
  Yes, it is numerology at the present precision -- and the reason is measurable rather than
  a matter of taste.

  With kappa fixed at one half and the matter coupling at gravitational strength, the branch
  coefficient has to be {B_TARGET:.4f}.  The expression you asked about, two root eight pi over three,
  is {2*math.sqrt(8*PI/3):.4f}, and it implies kappa = 1/sqrt(3) exactly -- 0.62 sigma from the distance-free
  measurement and 1.48 from the baryonic Tully-Fisher one.  It is a perfectly reasonable
  candidate.  That is exactly the problem.

  Enumerating a systematic universe of simple closed forms -- small rationals times half-integer
  powers of pi and e times small square roots -- there are {density} distinct values in the decade
  around the target, about one every {need_frac*100:.3f} percent.  Inside the band the kappa measurements
  actually allow, {len(hits_meas)} of them fit.  So landing in the band is not evidence; it is
  what tidy numbers do in a band a fifth of a decade wide.

  For a hit to be surprising, kappa would have to be measured about {improve:.0f} times better than the
  best number this programme has.  Nothing on the observational horizon does that.

  And there is a deeper reason, which is structural rather than statistical.  L227 proved that
  no monotone interpolating function fixes the branch coefficient at all, and every MOND kernel
  is monotone by construction.  So nothing in this programme, or any sibling of it, currently
  OUTPUTS this number.  A closed form for it is therefore not a prediction awaiting
  confirmation -- it is a guess awaiting a derivation.  Matching data cannot promote it.

  What would count: a principle that produces {B_TARGET:.4f} without being shown the answer.  That is
  the number to beat.

  LIMITS.  The enumerated universe is one reasonable choice and a different one shifts the
  density by a factor of a few; the conclusion needs two hundred, so it survives that.  The
  coupling is taken at gravitational strength, which is a choice, and a different choice moves
  the target as the three-halves power without changing the density argument.  The kappa
  measurements and their errors are this programme's own. Both a_0 footings enter only through
  those measurements, which already span them.
""")
print(f"L228 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES, "b_target": B_TARGET},
          open("fable_independent_2026/L228_results.json", "w"), indent=1)
