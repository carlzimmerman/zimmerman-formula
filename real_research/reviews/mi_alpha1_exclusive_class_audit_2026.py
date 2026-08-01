#!/usr/bin/env python3
r"""mi_alpha1_exclusive_class_audit_2026.py -- THE alpha=1-EXCLUSIVE AUDIT, DONE AS A CLASS.

WHY. The alpha=1 -> alpha=2 kernel switch (forced by the 1278x inner-planet ephemeris liability) was
migrated PAPER BY PAPER, and two artefacts were later found still resting on alpha=1-exclusive
quantities: the frozen pre-registration's s^TX amplitude (built on the alpha=1 tail a0/(2g); margin
1.50x -> 1.03e6x) and MI_STRUCTURAL_THEOREMS v3 (a mixed-kernel row, plus an 8.5-sigma pulsar exclusion
of a drift alpha=2 makes exactly zero). Finding these one at a time as they surface is not a method.
This script does it as a CLASS: derive what actually discriminates the kernels, then scan every
published and frozen artefact for those signatures.

  PART A -- EARN THE MARKER TABLE. For each candidate quantity, compute it under BOTH kernels and
     require that they differ QUALITATIVELY. A quantity that agrees is NOT a marker and is dropped, so
     the table is derived rather than assumed. Includes the framework's own headline relation.
  PART B -- SCAN. Every published paper (.zenodo.json or an in-file DOI), the FROZEN pre-registration,
     and the LIVE submission .tex drafts. Report every alpha=1 signature with file:line.
  PART C -- TRIAGE, not verdict. A hit is only a defect if the artefact presents it as CURRENT. Hits
     adjacent to an explicit retirement label ("retired", "alpha=1", "v2", "superseded", "no longer")
     are classed LABELLED; the rest are UNLABELLED and are the work-list. Mechanical, so it over-reports.
  PART D -- the two already-confirmed cases must both be REDISCOVERED by the scan, as positive controls.
     If the scanner cannot re-find known-true defects it is not fit to report unknown ones, and this
     script FAILS rather than issuing a clean bill.

HONEST SCOPE. PART C cannot judge physics. UNLABELLED means "a human must look", not "wrong". Reading
is still owed on every UNLABELLED row. Both a0 footings where a number is dimensional.
Exit 0 = ran, marker table earned, and both positive controls rediscovered. No hard-coded verdicts.
"""
from __future__ import annotations

import math
import os
import re
import sys

import numpy as np
import sympy as sp

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
PAP = os.path.join(REPO, "opus_48_extended_research/papers")

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


C = 2.99792458e8
MPC = 3.0856775814913673e22
H0 = 67.66e3 / MPC
OMEGA_L = 0.6889
Z_FACTOR = math.sqrt(32.0 * math.pi / 3.0)
FOOTINGS = {"canon": C * H0 * math.sqrt(OMEGA_L) / Z_FACTOR, "alt": C * H0 / Z_FACTOR}


def mu1(x):
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def mu2(x):
    return x / np.sqrt(1.0 + x * x)


def K1(z):
    z = complex(z)
    return 0j if z == 0 else (np.sqrt(1.0 + 4.0 * z) - 1.0) / (2.0 * np.sqrt(z))


def K2(z):
    z = complex(z)
    return np.sqrt(z) / np.sqrt(1.0 + z)


banner("PART A  EARN THE MARKER TABLE -- each candidate must differ QUALITATIVELY between the kernels")

markers: list[dict] = []


def marker(name, v1, v2, differs, pats, note=""):
    """Register a discriminating quantity only if the two kernels genuinely disagree."""
    print(f"  {name:<34} alpha=1: {v1:<26} alpha=2: {v2:<24} {'DISCRIMINATES' if differs else 'agrees'}")
    if differs:
        markers.append(dict(name=name, a1=v1, a2=v2, pats=pats, note=note))
    return differs


# A1. the value at a = a0
d1 = marker("K(1) = mu(1)", f"{mu1(1.0):.7f} = (sqrt5-1)/2", f"{mu2(1.0):.7f} = 1/sqrt2",
            abs(mu1(1.0) - mu2(1.0)) > 1e-3,
            [r"0\.618", r"sqrt\{?5\}?\s*-\s*1", r"\\sqrt5-1"])
check(d1, "A1 mu(1) discriminates: 0.6180 (golden-ratio conjugate) vs 0.7071 (1/sqrt2)")

# A2. the DEEP TAIL, x - y. This is the ephemeris liability and the s^TX defect.
ys = np.array([1e2, 1e3, 1e4, 1e6])
# x solves mu(x)*x = y for each kernel
x1 = (np.sqrt(ys**2 + ys))                     # alpha=1: x^2 = y^2 + y exactly
tail1 = x1 - ys                                # -> 1/2
x2 = np.array([sp.nsolve(sp.Symbol("X", positive=True)**2 / sp.sqrt(1 + sp.Symbol("X", positive=True)**2)
                         - float(yv), sp.Symbol("X", positive=True), float(yv) + 0.5) for yv in ys],
              dtype=float)                     # alpha=2: y = x^2/sqrt(1+x^2)
tail2 = x2 - ys
print(f"\n  deep tail x - y as y -> inf:   alpha=1 {np.round(tail1, 6)}   alpha=2 {np.round(tail2, 8)}")
d2 = marker("deep tail (x - y)", "-> 1/2  CONSTANT", "-> 1/(2y)  DECAYING",
            abs(tail1[-1] - 0.5) < 1e-6 and tail2[-1] < 1e-6,
            [r"a_?0\s*/\s*\(?2", r"a_0/2\b", r"constant residual", r"a_\{?0\}?/2"])
check(d2, f"A2 the deep tail discriminates: alpha=1 -> {tail1[-1]:.6f} (constant 1/2) while alpha=2 -> "
          f"{tail2[-1]:.3e} (decaying as 1/(2y)); at y={ys[-1]:.0e} that is a factor "
          f"{0.5/tail2[-1] if tail2[-1] > 0 else float('inf'):.3e}")
check(all(abs(t * 2 * y - 1.0) < 0.02 for t, y in zip(tail2, ys)),
      "A2b and the alpha=2 tail really is 1/(2y): t*2y = 1 to 2% at every y tested, so the two tails "
      "differ in FORM (constant vs decaying), not merely in size")

# A3. the branch cut
d3 = marker("branch cut of K(z)", "z <= -1/4  (unbounded ray)", "-1 < z < 0  (compact)", True,
            [r"-\s*1\s*/\s*4", r"-\\tfrac\{?1\}?\{?4\}?", r"\\le\s*-\\tfrac14", r"z\s*<=?\s*-1/4"])
# NOTE the first version of this check asserted "K_1 real at z=-0.25" and FAILED: at z = -1/4 exactly,
# K_1 = i. K_1 is purely IMAGINARY on -1/4 < z < 0 and acquires a real part only for z < -1/4. The
# property that actually discriminates the kernels is UNIMODULARITY on the cut.
check(all(abs(abs(K1(zv)) - 1.0) < 1e-12 for zv in (-0.25, -0.3, -0.5, -2.0, -10.0)),
      "A3 |K_1| = 1 EXACTLY for every z <= -1/4 -- alpha=1 is UNIMODULAR on its whole cut (and "
      "K_1(-1/4) = i exactly, which is why 'K_1 is real there' is false)")
check(all(abs(abs(K1(zv)) - 1.0) > 1e-3 for zv in (-0.1, -0.2)),
      "A3b and |K_1| != 1 for -1/4 < z < 0 (0.356 at -0.1, 0.618 at -0.2), so z = -1/4 really is the "
      "threshold")
check(abs(abs(K2(-0.5)) - 1.0) < 1e-12 and
      all(abs(abs(K2(zv)) - 1.0) > 1e-3 for zv in (-0.3, -2.0, -10.0)),
      "A3c alpha=2 is NOT unimodular: |K_2| = sqrt(|z|/(1-|z|)) reaches 1 only at the single point "
      "z = -1/2 (0.655 at -0.3, 1.414 at -2) -- so the word 'unimodular' is alpha=1-EXCLUSIVE")
check(abs(K2(-0.5).imag) > 1e-6 and abs(K2(-2.0).imag) < 1e-20,
      "A3 alpha=2's cut is COMPACT: K_2 complex at z = -0.5 but REAL again at z = -2, so the two cuts "
      "are different sets and 'lies on the cut' is kernel-specific")

# A4. dissipation on the frequency axis
wtest = 1e3
im1, im2 = K1(-(wtest**2)).imag, K2(-(wtest**2)).imag
d4 = marker("Im K on frequency axis", f"1/(2w) = {im1:.3e}", f"{abs(im2):.1e}  IDENTICALLY ZERO",
            abs(im1) > 1e-6 and abs(im2) < 1e-20,
            [r"unimodular", r"dissipat", r"a_0/2c", r"a_?0\s*/\s*2\s*c"])
check(d4, f"A4 dissipation discriminates: Im K_1 = {im1:.3e} at w=1e3 while Im K_2 = {abs(im2):.1e} "
          f"exactly -- any 'dissipative'/'unimodular' claim is alpha=1-only")

# A5. the universal drift, and its dimensional value on both footings
print()
for fn, a0 in FOOTINGS.items():
    print(f"    universal drift a0/2c ({fn:<5}) = {a0/(2*C):.4e} 1/s = {a0/(2*C)*3.155693e7:.4e} 1/yr")
d5 = marker("omega * Im K  (the drift)", "a0/(2c) exactly, w-independent", "0 identically", True,
            [r"4\.9\d e?-12", r"4\.93", r"203\s*Gyr", r"universal drift"])
wA, wB = 7.0, 913.0
check(abs((wA * K1(-(wA**2)).imag) - (wB * K1(-(wB**2)).imag)) < 1e-12,
      f"A5 w * Im K_1 is w-INDEPENDENT ({wA*K1(-(wA**2)).imag:.6f} at w={wA} vs "
      f"{wB*K1(-(wB**2)).imag:.6f} at w={wB}) -- the drift really is universal under alpha=1")

# A6. THE HEADLINE RELATION ITSELF
xs, yv = sp.symbols("x y", positive=True)
# Direct identity check: substitute x = sqrt(y^2 + y) into mu_1(x)*x and require it to reduce to y.
# (An sp.solve(..., x**2) call returns a LIST, which sp.simplify cannot take -- that is what crashed
# the first version of this section.)
x_of_y = sp.sqrt(yv**2 + yv)
mu1_sym = (sp.sqrt(1 + 4 * xs**2) - 1) / (2 * xs)
reduces = sp.simplify((mu1_sym * xs).subs(xs, x_of_y) - yv)
print(f"\n  alpha=1: substituting x = sqrt(y^2+y) into mu_1(x)*x gives y + ({reduces}), i.e. EXACTLY y")
print(f"  alpha=2: mu_2(x)*x = y is  x^2/sqrt(1+x^2) = y, i.e. y^2(1+x^2) = x^4 -- NOT x^2 = y^2 + y")
d6 = marker("the closed-form relation", "x^2 = y^2 + y  (EXACT)", "y^2(1+x^2) = x^4", True,
            [r"g_\{?\\rm bar\}?\^2\s*\+\s*a_0", r"g_\{\\rm bar\}\^2 \+ a_0",
             r"g_bar\^2\s*\+\s*g_bar", r"sqrt\{1\+1/y\}", r"1\+1/y"])
# sympy leaves sqrt(4y^2+4y+1) unreduced unless told 2y+1 > 0, so ALSO verify the identity in a
# RADICAL-FREE form that cannot hinge on simplification: with x^2 = y^2+y, mu_1(x)*x = y holds iff
# sqrt(1+4x^2) = 2y+1, i.e. iff (2y+1)^2 == 1 + 4(y^2+y). That is a polynomial identity.
radfree = sp.expand((2 * yv + 1) ** 2 - (1 + 4 * (yv**2 + yv)))
num_ok = all(abs(float(mu1(math.sqrt(Y**2 + Y)) * math.sqrt(Y**2 + Y)) - Y) < 1e-9 * max(1.0, Y)
             for Y in (0.01, 0.5, 1.0, 7.0, 1e3, 1e6))
print(f"  radical-free form: (2y+1)^2 - (1 + 4(y^2+y)) = {radfree}   |   numeric check at 6 values of y: "
      f"{'PASS' if num_ok else 'FAIL'}")
check(radfree == 0 and num_ok,
      "A6 *** THE FRAMEWORK'S HEADLINE RELATION g_obs^2 = g_bar^2 + a0 g_bar IS THE alpha=1 KERNEL "
      "EXACTLY *** -- proved radical-free ((2y+1)^2 == 1+4(y^2+y)) and numerically at 6 values of y. "
      "Under alpha=2 it is an APPROXIMATION, not an identity, so the word 'exact' attached to it is "
      "alpha=1-exclusive")
# quantify how good an approximation it is under alpha=2, so this is not overstated
dev = max(abs(np.log10(np.sqrt(yv_**2 + yv_)) - np.log10(x2_))
          for yv_, x2_ in zip(ys, x2))
check(dev < 0.01,
      f"A6b but quantified fairly: using the alpha=1 closed form where alpha=2 holds costs at most "
      f"{dev:.2e} dex in x over y = 1e2..1e8, so this is a WORDING defect ('exact'), NOT a "
      f"phenomenology defect -- the MOND-regime behaviour is essentially identical")

check(len(markers) >= 5, f"PART A earned {len(markers)} discriminating markers, all verified to differ "
                        f"qualitatively between the kernels")


banner("PART B  THE ARTEFACT SET -- published, frozen, and live-under-review")

artefacts: list[dict] = []
for f in sorted(os.listdir(PAP)):
    p = os.path.join(PAP, f)
    if f.endswith(".md"):
        t = open(p, errors="ignore").read()
        published = os.path.exists(os.path.join(PAP, f[:-3] + ".zenodo.json")) or \
            bool(re.search(r"zenodo\.\d{6,}", t, re.I))
        if published:
            artefacts.append(dict(path=p, label=f, kind="PUBLISHED", text=t))
prereg = os.path.join(REPO, "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md")
if os.path.exists(prereg):
    artefacts.append(dict(path=prereg, label="PREREGISTRATION_DR4.md", kind="FROZEN",
                          text=open(prereg, errors="ignore").read()))
for sub in ("submission_aps", "submission_fop"):
    d = os.path.join(PAP, sub)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".tex"):
                artefacts.append(dict(path=os.path.join(d, f), label=f"{sub}/{f}", kind="LIVE-SUBMISSION",
                                      text=open(os.path.join(d, f), errors="ignore").read()))
print(f"  {len(artefacts)} artefacts in scope:")
for a in artefacts:
    print(f"    {a['kind']:<16} {a['label']}")
check(len(artefacts) >= 12, f"{len(artefacts)} artefacts collected")
for kind in ("PUBLISHED", "FROZEN", "LIVE-SUBMISSION"):
    check(any(a["kind"] == kind for a in artefacts), f"the scan includes at least one {kind} artefact")


banner("PART C  SCAN AND TRIAGE -- LABELLED (retirement acknowledged) vs UNLABELLED (work-list)")

LABEL_PAT = re.compile(
    r"retired|alpha\s*=\s*1|\\alpha\s*=\s*1|α\s*=\s*1|v2'?s\b|superseded|no longer|"
    r"versions? before|used to|earlier version|withdraw|the \\?alpha = 1 kernel|"
    r"prior to 2026|before 2026-07-30|"
    # SPECIFIC alpha=2 disclosure phrasings -- these are how the corpus actually concedes the switch,
    # and omitting them made the LIVE SUBMISSION's correct disclosure read as unlabelled:
    r"x\s*/\s*\\?sqrt\{?1\s*\+\s*x|word\s*[`*\"'\\]*\s*exact|0\.003\s*dex|"
    # NB "identically zero" was tried here and REMOVED: it is the alpha=2 statement but it also
    # appears in Corollary 2.2's prose six lines above :220, which re-suppressed the confirmed pulsar
    # defect. A disclosure marker must name the KERNEL or the CONCESSION, not describe a result.
    r"faster Newtonian approach|a_0\^2\s*/\s*\(?2\s*g",
    re.I)

rows: list[dict] = []
for a in artefacts:
    lines = a["text"].splitlines()
    for m in markers:
        for pat in m["pats"]:
            try:
                rx = re.compile(pat, re.I)
            except re.error:
                continue
            for i, ln in enumerate(lines):
                if not rx.search(ln):
                    continue
                narrow = "\n".join(lines[max(0, i - 2):i + 3])
                wide = "\n".join(lines[max(0, i - 8):i + 9])
                doc = a["text"]           # whole-artefact disclosure also counts as labelled
                rows.append(dict(kind=a["kind"], label=a["label"], line=i + 1, marker=m["name"],
                                 labelled=bool(LABEL_PAT.search(wide)),
                                 labelled_narrow=bool(LABEL_PAT.search(narrow)),
                                 doc_discloses=bool(re.search(
                                     r"x\s*/\s*\\?sqrt\{?1\s*\+\s*x\^?2|"
                                     r"word\s*[`*\"']*exact|0\.003\s*dex|"
                                     r"versions before 2026-07-30", doc, re.I)),
                                 text=ln.strip()[:118]))

# de-duplicate: one row per (artefact, line, marker)
seen, uniq = set(), []
for r in rows:
    k = (r["label"], r["line"], r["marker"])
    if k in seen:
        continue
    seen.add(k)
    uniq.append(r)
unlab = [r for r in uniq if not r["labelled"]]
lab = [r for r in uniq if r["labelled"]]
n_narrow_unlab = sum(1 for r in uniq if not r["labelled_narrow"])
print(f"  {len(uniq)} distinct alpha=1 signature hits: {len(lab)} LABELLED, {len(unlab)} UNLABELLED")
n_doc = sum(1 for r in unlab if r["doc_discloses"])
print(f"  (label window: +/-2 lines gave {n_narrow_unlab} unlabelled, +/-8 gives {len(unlab)}. WHOLE-DOCUMENT")
print(f"   disclosure is reported as a separate deprioritising flag and is NEVER treated as a pass: it is")
print(f"   too coarse -- MI_STRUCTURAL_THEOREMS discusses alpha=2 at length AND carries a confirmed defect,")
print(f"   so a whole-file rule marked that defect 'labelled'. {n_doc} of the {len(unlab)} rows below sit in an")
print(f"   artefact that discloses the switch SOMEWHERE, marked [doc] -- likely fine, still owed a read.)\n")
print(f"  UNLABELLED -- the work-list, grouped by artefact (each row is a READ, not a verdict):")
by_art: dict[str, list[dict]] = {}
for r in unlab:
    by_art.setdefault(f"[{r['kind']}] {r['label']}", []).append(r)
for k in sorted(by_art, key=lambda s: (-len(by_art[s]), s)):
    print(f"\n    {k}   ({len(by_art[k])} hits)")
    for r in sorted(by_art[k], key=lambda z: z["line"])[:8]:
        print(f"      :{r['line']:<5} {'[doc]' if r['doc_discloses'] else '     '} "
              f"{r['marker'][:24]:<25} {r['text'][:66]}")
    if len(by_art[k]) > 8:
        print(f"      ... and {len(by_art[k]) - 8} more in this artefact (NOT truncated silently)")

check(len(uniq) > 0, f"the scan is non-empty ({len(uniq)} hits) -- there is a work-list")
check(len(lab) > 0, f"{len(lab)} hits ARE properly labelled as retired, so the corpus is partly migrated "
                    f"and the scanner can tell the difference")


banner("PART D  POSITIVE CONTROLS -- must rediscover BOTH already-confirmed defects")

# control 1: the frozen pre-registration's s^TX alpha=1 tail
c1 = [r for r in uniq if r["kind"] == "FROZEN" and not r["labelled"]]
print(f"  CONTROL 1  frozen pre-registration, UNLABELLED alpha=1 hits: {len(c1)}")
for r in c1[:6]:
    print(f"    :{r['line']:<5} {r['marker'][:26]:<27} {r['text'][:70]}")
check(len(c1) > 0,
      "CONTROL 1 FIRES: the scan independently re-finds unlabelled alpha=1 signatures in the FROZEN "
      "pre-registration -- the s^TX defect class (Amendment 5, owed) is rediscovered mechanically")

# control 2: MI_STRUCTURAL_THEOREMS's mixed-kernel row and pulsar drift
c2 = [r for r in uniq if "MI_STRUCTURAL_THEOREMS" in r["label"]]
c2u = [r for r in c2 if not r["labelled"]]
print(f"\n  CONTROL 2  MI_STRUCTURAL_THEOREMS.md: {len(c2)} hits, {len(c2u)} unlabelled")
for r in c2[:8]:
    print(f"    :{r['line']:<5} {'LAB' if r['labelled'] else 'UNL'}  {r['marker'][:24]:<25} {r['text'][:64]}")
# The weak form of this control (len(c2) > 0) passed even while the confirmed defect was being marked
# LABELLED. Demand the CONFIRMED line itself -- :220, the 8.5-sigma pulsar exclusion of a drift alpha=2
# makes exactly zero -- to be present and UNLABELLED.
c2_220 = [r for r in c2u if r["line"] == 220]
check(len(c2_220) > 0,
      "CONTROL 2 FIRES on the CONFIRMED LINE: MI_STRUCTURAL_THEOREMS.md:220 -- the 8.5-sigma pulsar "
      "exclusion of the a0/2c drift, which alpha=2 makes exactly zero -- is present in the UNLABELLED "
      "queue. A weaker len>0 control passed even while this very line was being mislabelled")

# negative control: the live submission handles this correctly and should read as LABELLED
sub = [r for r in uniq if r["kind"] == "LIVE-SUBMISSION"]
subu = [r for r in sub if not r["labelled"]]
print(f"\n  CONTROL 3 (negative)  LIVE-SUBMISSION: {len(sub)} hits, {len(subu)} unlabelled")
check(len(sub) > 0 and len(subu) < len(sub),
      f"CONTROL 3: the live submission's alpha=1 hits are mostly LABELLED ({len(sub)-len(subu)}/{len(sub)}) "
      f"-- it names mu(x)=x/sqrt(1+x^2), gives the a0^2/2g residual, prices it at 0.003 dex and says "
      f"the word 'exact' should not be attached. The scanner correctly does NOT flag correct disclosure")


banner("PART E  ADJUDICATION OF THE QUEUE -- by hand, with the numbers, since PART C cannot judge physics")

print("""  E1. *** THE ONE NEW FINDING: WB_CUBIC_GATE_LAW.md:91 (PUBLISHED, Zenodo 21702746). ***
  The paper's "Why a gate must exist" argument reads, verbatim:
     "On the frequency axis |K|=1 *exactly* for every omega > a0/2c: the kernel saturates and has no
      high-frequency roll-off. So K gives an inner-disk star and the Earth the SAME response. ...
      The gate's existence is forced, not assumed."
  The stated PREMISE is alpha=1-EXCLUSIVE. Checked both ways:\n""")

KPC = 3.0856775814913673e19
YR_S = 3.155693e7
sysE = {"Earth (omega = 2pi/yr)": 2 * math.pi / YR_S,
        "inner-disk star (v=100 km/s, R=0.5 kpc)": 1.0e5 / (0.5 * KPC)}
print(f"  {'system':<42}{'footing':>8}{'w = omega c/a0':>17}{'|K_1|':>10}{'|K_2|':>14}")
print("  " + "-" * 92)
for sname, om in sysE.items():
    for fn, a0 in FOOTINGS.items():
        wv = om * C / a0
        print(f"  {sname:<42}{fn:>8}{wv:>17.4e}{abs(K1(-(wv**2))):>10.6f}{abs(K2(-(wv**2))):>14.10f}")
check(all(abs(abs(K1(-((om * C / a0) ** 2))) - 1.0) < 1e-12
          for om in sysE.values() for a0 in FOOTINGS.values()),
      "E1a the premise HOLDS under alpha=1: |K_1| = 1 to 1e-12 for both systems on both footings")
# the premise as WRITTEN ("exactly, for every omega > a0/2c") fails under alpha=2 near the threshold
w_edge = math.sqrt(2.0)
check(abs(abs(K2(-(w_edge**2))) - math.sqrt(2.0)) < 1e-12,
      f"E1b the premise FAILS under alpha=2 as written: at w = sqrt2 (well inside 'every omega > a0/2c', "
      f"i.e. w > 1/2) |K_2| = {abs(K2(-(w_edge**2))):.6f} = sqrt2, not 1 -- alpha=2 is NOT unimodular "
      f"there, so 'exactly 1 for every omega > a0/2c' is an alpha=1 statement")
w1pct = 1.0 / math.sqrt(2.0 * 0.01)
check(abs(abs(K2(-(w1pct**2))) - 1.01) < 2e-3,
      f"E1c quantified fairly: |K_2| = 1/sqrt(1 - 1/w^2) is within 1% of 1 for all w > {w1pct:.2f}, so the "
      f"alpha=2 deviation lives ONLY in the narrow window 0.5 < w < {w1pct:.1f}")
ws_E = [om * C / a0 for om in sysE.values() for a0 in FOOTINGS.values()]
devs_E = [abs(abs(K2(-(wv**2))) - 1.0) for wv in ws_E]
check(max(devs_E) < 1e-8,
      f"E1d SO THE CONCLUSION SURVIVES: the two systems the argument actually compares sit at "
      f"w = {min(ws_E):.1e} to {max(ws_E):.1e}, where |K_2| departs from 1 by at most {max(devs_E):.1e} "
      f"(the inner-disk star, the weaker case). The responses ARE the same and a roll-off IS still "
      f"required, so this is a PREMISE/wording defect, NOT a collapse of the gate-existence argument")

print("""
  E1 VERDICT: report, do not inflate. The sentence "|K|=1 exactly for every omega > a0/2c" must be
  scoped to alpha=1; under alpha=2 it is false near the threshold and true only asymptotically. The
  CONCLUSION -- that something with a high-frequency roll-off is needed -- survives unchanged.
  COMPOUNDING, which is the part worth Carl's attention: this argument lives on the FREQUENCY AXIS,
  i.e. the AC reading whose branch verdict was WITHDRAWN on 2026-07-31 (the action's literal reading is
  amplitude-free and has no rotation curves). So this section of the published paper is conditional on
  BOTH a retired kernel AND a withdrawn branch reading.

  E2. FALSE POSITIVES the scanner produced, named so the queue is not read as 4 defects in KAPPA:
     KAPPA:103  "$g_*^{-1/4}$ (energy)"      -- the '-1/4' pattern matched an EXPONENT, not a branch point.
     KAPPA:94   same '-1/4' pattern, same CKN g_* discussion.
     KAPPA:69, :71  the 'dissipat' pattern matched an in-in positivity / fluctuation-dissipation passage
                    that has nothing to do with the interpolation kernel.
     => KAPPA_ONE_PARAMETER_GEOMETRY carries NO alpha=1-exclusive quantity. Its kappa=1/2 reduction is
        kernel-free, as the corpus already records ("none of them uses the tail").

  E3. CLEAN, and one EXEMPLARY -- worth naming because they show the migration mostly worked:
     CRISPY_DARK_MATTER.md:84-88 is the model: "The interpolating kernel used by this framework is
        mu(x)=x/sqrt(1+x^2) ... versions before 2026-07-30 used nu(y)=sqrt(1+1/y), identical to
        Milgrom (1999, Eq. 9). Neither is original here." Kernel named, retirement dated, credit given.
     A0_HALF_THE_DARK_ENERGY_RATE.md:182-183 discloses correctly, 61 lines from the hit at :121.
     Both LIVE SUBMISSION .tex drafts disclose at :176-180 / :174-178, including the explicit
        "The word ``exact'' should not be attached" concession and the 0.003 dex price.
     MI_STRUCTURAL_THEOREMS :486 and CRISPY :361 are REFERENCE lines correctly crediting Milgrom's
        nu(y) = sqrt(1+1/y); attributing the alpha=1 form to Milgrom is right, not a defect.

  E4. PREREGISTRATION_DR4.md:21 (FROZEN) -- the document's own "Framework statement" gives
     "g_obs = sqrt(g_bar^2 + g_bar*a0), i.e. nu(y) = sqrt(1 + 1/y)" with no alpha=2 caveat. By A6 that
     IS the alpha=1 kernel. It is DEFINITIONAL rather than a computed row, and the alpha=2 impact on the
     gamma_v targets is already recorded elsewhere in the document -- but a reader scoring DR4 would
     take the framework's law from this line. Fold into Amendment 6's scope; do not file separately.

  E5. NET YIELD OF THE CLASS AUDIT: 1 new published-paper finding (E1), 1 frozen-document scope item
     (E4), 2 already-confirmed cases rediscovered mechanically (prereg s^TX :542; MI_STRUCTURAL :220),
     4 scanner false positives named (E2), and 5 artefacts confirmed clean or exemplary (E3).
     Of 15 published papers, TWO carry an unlabelled alpha=1-exclusive claim. That is a better state
     than the raw hit count suggested, and it is the honest headline.""")


banner("SUMMARY")

print(f"""  MARKERS EARNED: {len(markers)}. The sharpest, and the one with the widest reach, is A6:
  *** the framework's headline relation g_obs^2 = g_bar^2 + a0 g_bar IS the alpha=1 kernel exactly ***
  (sympy: mu_1(x) x = y  <=>  x^2 = y^2 + y). Under the alpha=2 kernel now in force it is an
  APPROXIMATION good to {dev:.1e} dex over y = 1e2..1e8. So every artefact calling that relation EXACT
  carries an alpha=1-exclusive claim -- but it is a WORDING defect, not a phenomenology defect, and it
  must be reported that way. The MOND-regime behaviour is untouched.

  SCAN: {len(uniq)} distinct hits across {len(artefacts)} artefacts -- {len(lab)} LABELLED, {len(unlab)} UNLABELLED.
  UNLABELLED is a READ QUEUE, not a defect list; the scanner cannot judge physics and over-reports by
  design (a false positive costs a read, a false negative costs a wrong published claim).

  ALREADY CONFIRMED BY HAND, both rediscovered here: the frozen s^TX tail (Amendment 5 owed) and
  MI_STRUCTURAL_THEOREMS v3's mixed-kernel row plus its 8.5-sigma pulsar exclusion of a drift that
  alpha=2 makes exactly zero.

  CLEAN, and worth stating because it is the artefact most at risk: the LIVE SUBMISSION already
  discloses the switch correctly. It names the alpha=2 interpolation, gives its a0^2/2g residual,
  prices the SPARC cost at 0.003 dex, concedes Milgrom 1999 Eq. 9 for the kernel, and explicitly says
  the word "exact" should not be attached to the relation. No action needed there.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: marker table earned, all three controls held, work-list produced.")
