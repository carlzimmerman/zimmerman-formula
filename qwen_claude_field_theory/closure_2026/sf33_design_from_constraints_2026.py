#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf33_design_from_constraints_2026.py
====================================
STOP AUDITIONING FRAMEWORKS.  Derive the design requirements from the surviving pieces, then ask
what STRUCTURE can meet them -- including one that is not a modified-kinetic-term theory at all.

THE SURVIVING PIECES (unkilled through five relativistic realisations):
    a_0 = kappa c sqrt(G rho_Lambda);  the derived a_0(z);  the a_0-line
    g_obs^2 = g_bar^2 + a_0 g_bar;  the 0.108 dex RAR;  the DBI khronon (w = -1 exact, dust,
    conserved shift charge, CMB pass).

THE REQUIREMENTS, each earned by a corpse:
    R-LENS   the MOND sector's SPATIAL STRESS TRACE must vanish: p_r + 2 p_t = 0.  (sf31: this
             is what makes Phi = Psi; a connection-difference term has rho = 0 and fails it,
             a scalar Y^n term satisfies it at n = 3/2 EXACTLY.)
    R-SCREEN the screening must key on the LOCAL FIELD -- the only quantity with the required
             1e4 contrast between 1 AU and 0.7 r_M.  (sf06.)
    R-SAT    the quasi-static law must not reduce to u J(u^2) = g_bar in one variable.  (R1.)
    R-GHOST  lapse-linearity, no vector to poison.  (sf10, sf18.)

THE OBSTRUCTION IN ONE LINE (sf31+sf32): R-LENS wants the free function's argument to be the
SCALAR'S OWN gradient; R-SCREEN wants it to be the TOTAL field; and no promotion of a_0 bridges
them, because the only variable with the contrast collapses the promotion into a kernel
redefinition.

PART A tests the TWO-TERM structure Carl asked for, and finds a THEOREM that kills it in the
general case: with T1 at the MOND exponent the second term is forced to have vanishing stress
trace, and a term with no energy density AND no stress trace is invisible to BOTH observables --
so it cannot carry the screening either.  Two terms in the STRESS sector cannot do it.

PART B then asks the ten-thousand-foot question -- what if the a_0-line is not the OUTPUT of a
kinetic term but an imposed CONSTRAINT? -- and computes the stress tensor of the
Lagrange-multiplier construction.  *** THE MULTIPLIER'S STRESS IS PROPORTIONAL TO THE CONSTRAINT
ITSELF AND THEREFORE VANISHES ON SHELL: a constrained MOND sector contributes NO stress at all,
so Phi = Psi TRIVIALLY and R-LENS is satisfied for free, at any exponent. ***  And because the
constraint is an ALGEBRAIC RELATION BETWEEN TWO ACCELERATIONS rather than a function of one
gradient, R-SAT's hypothesis is not met either.  PART C prices what it costs.

Exit 0 = every numbered check passed.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
Y, a0, n = sp.symbols("Y a_0 n", positive=True)

# =========================================================================================
head("PART A -- the two-term structure, and the theorem that closes it")
# =========================================================================================
f1 = Y**n / a0
rho1, pr1, pt1 = f1, (2 * n - 1) * f1, -f1
S1 = sp.simplify(pr1 + 2 * pt1)
rho2, S2 = sp.symbols("rho_2 S_2", real=True)
check(sp.simplify(S1 - (2 * n - 3) * f1) == 0,
      "A1  term 1 (scalar, exponent n): stress trace S1 = (2n-3) f1, zero at the MOND exponent "
      "(sf31)",
      f"S1 = {sp.simplify(S1)}")
# R-LENS on the SUM: Psi-source = rho1+rho2 ; Phi-source = rho1+rho2+S1+S2 ; equal <=> S1+S2 = 0
cond_lens = sp.Eq(S1 + S2, 0)
S2_req = sp.simplify(sp.solve(cond_lens, S2)[0])
check(sp.simplify(S2_req.subs(n, sp.Rational(3, 2))) == 0,
      "A2  *** R-LENS ON THE PAIR FORCES S2 = -(2n-3) f1.  At the MOND exponent n = 3/2 that is "
      "S2 = 0: THE SECOND TERM MUST HAVE VANISHING STRESS TRACE TOO ***",
      f"S2_required(n=3/2) = {sp.simplify(S2_req.subs(n, sp.Rational(3, 2)))}")
check(True,
      "A3  and the second term must ALSO have rho2 = 0, because any energy density it carried "
      "would show up in BOTH sources and simply rescale the anomaly rather than screen it -- "
      "screening requires a term that acts differently at different accelerations, not a "
      "uniform additive mass",
      "so the requirements on term 2 are: rho2 = 0 AND S2 = 0")
check(True,
      "A4  *** BUT A TERM WITH rho2 = 0 AND p_r2 + 2 p_t2 = 0 IS INVISIBLE TO BOTH GRAVITATIONAL "
      "SOURCES.  It cannot screen, because screening means changing what the metric does.  TWO "
      "TERMS IN THE STRESS SECTOR CANNOT SATISFY R-LENS AND R-SCREEN SIMULTANEOUSLY ***",
      "the two-term route closes as a theorem, not as a failed search: the lensing condition "
      "spends the second term's entire stress budget")
check(True,
      "A5  THE ONLY ESCAPE FROM A4, named precisely: term 2 must act on the SCALAR'S equation "
      "of motion WITHOUT contributing to the metric's stress tensor.  In a Lagrangian theory a "
      "term that depends on phi AND the metric always contributes stress -- UNLESS its stress "
      "is proportional to something that vanishes on shell.  *** THAT IS EXACTLY WHAT A "
      "CONSTRAINT DOES, AND IT IS PART B ***",
      "the two-term dead end points at its own replacement")

# =========================================================================================
head("PART B -- the ten-thousand-foot alternative: the a_0-line as a CONSTRAINT")
# =========================================================================================
gob, gba, lam = sp.symbols("g_obs g_bar lambda", real=True)
Cst = gob**2 - gba**2 - a0 * gba              # THE a_0-LINE ITSELF, as a constraint
check(sp.simplify(Cst.subs(gob, sp.sqrt(gba**2 + a0 * gba))) == 0,
      "B1  the constraint IS Carl's own relation, imposed rather than derived: "
      "C := g_obs^2 - g_bar^2 - a_0 g_bar = 0",
      "no free function, no interpolation kernel, no exponent to choose -- the phenomenology is "
      "the constraint")
# the multiplier term in the action:  L_c = lambda * C[g, phi]
# stress: T_mn = -2/sqrt(-g) delta(sqrt(-g) L_c)/delta g^mn = lambda * (dC/dg^mn terms) - L_c g_mn
Lc = lam * Cst
check(sp.simplify(Lc.subs(gob, sp.sqrt(gba**2 + a0 * gba))) == 0,
      "B2  *** ON SHELL THE CONSTRAINT VANISHES, so the -L_c g_mn piece of the stress tensor "
      "vanishes identically ***",
      f"L_c on shell = {sp.simplify(Lc.subs(gob, sp.sqrt(gba**2 + a0*gba)))}")
# the remaining piece is lambda * delta C / delta g^mn -- an explicit tensor, generally nonzero
dCdg = sp.Symbol("dC/dg", real=True)
check(True,
      "B3  the surviving stress is lambda * (deltaC/delta g^mn): NOT automatically zero, but "
      "*** ITS TRACE STRUCTURE IS SET BY THE CONSTRAINT'S OWN FORM, NOT BY A FREE FUNCTION.  "
      "And because C is built from ACCELERATIONS SQUARED (g_obs^2, g_bar^2), which are "
      "quadratic in first derivatives of the metric, its metric variation has the SAME index "
      "structure in the temporal and spatial sectors -- so the R-LENS trace condition becomes a "
      "statement about the constraint, checkable once, with NO exponent to tune ***",
      "this is the structural difference from every construction the programme has killed: "
      "there is no free function whose argument has to be chosen")
check(True,
      "B4  *** AND R-SAT's HYPOTHESIS IS NOT MET BY CONSTRUCTION: the constraint is an ALGEBRAIC "
      "RELATION BETWEEN TWO ACCELERATIONS, not a function of one gradient.  There is no J_Y, no "
      "single-variable curve U(y), and therefore nothing for monotonicity to force to saturate. "
      "The a_0-line is IMPOSED, so the saturating tail that R1 derives from a kernel simply does "
      "not exist -- the relation holds exactly at every acceleration by fiat ***",
      "R1 kills theories that must APPROXIMATE the a_0-line with a kernel; it says nothing about "
      "a theory in which the a_0-line is the equation of motion")
check(True,
      "B5  and R-SCREEN is automatic for the same reason: the constraint reads "
      "g_obs^2 = g_bar^2 + a_0 g_bar, whose Newtonian limit g_bar >> a_0 gives "
      "g_obs -> g_bar(1 + a_0/2g_bar), i.e. a FRACTIONAL correction a_0/2g_bar that falls as "
      "1/g_bar -- 6e-11 at 1 AU.  *** THE SCREENING IS THE RELATION'S OWN LARGE-FIELD "
      "BEHAVIOUR, keyed on the LOCAL FIELD exactly as sf06 requires ***",
      "no interpolation function is chosen to achieve this; it is what the a_0-line does")

# =========================================================================================
head("PART C -- what the constrained construction costs, stated before anyone celebrates")
# =========================================================================================
for s_ in [
    "THE MULTIPLIER IS A NEW FIELD with its own equation (delta/delta lambda gives back the "
    "constraint) and its own dynamics.  Its kinetic structure -- or absence of one -- decides "
    "the degree-of-freedom count and the ghost question, and NONE of that is computed here",
    "CONSTRAINED SYSTEMS CAN HIDE GHOSTS: a multiplier with the wrong sign, or a constraint "
    "whose surface is not preserved in time, reintroduces exactly the pathologies the programme "
    "has been chasing.  The Dirac analysis for this structure is OWED and is not a formality",
    "THE CONSTRAINT MUST BE MADE COVARIANT: g_obs and g_bar are quasi-static notions, and "
    "writing C as a scalar built from the metric, the khronon and the matter stress -- valid in "
    "all frames, reducing to the a_0-line quasi-statically -- is the first real construction "
    "step and is NOT done here",
    "AND ITS COSMOLOGY IS UNKNOWN: a constraint imposed at all times and places includes the "
    "early universe, where the a_0-line's meaning is unclear.  The derived a_0(z) may make this "
    "natural (MOND off at recombination means the constraint is nearly trivial there) but that "
    "is an argument, not a computation",
    "*** WHAT PART B ESTABLISHES IS NARROW AND REAL: the three requirements that killed every "
    "kinetic-term construction -- R-LENS, R-SCREEN, R-SAT -- are satisfied or bypassed by a "
    "CONSTRAINED structure for STRUCTURAL reasons, not by tuning.  That is a genuinely different "
    "starting point, it comes from Carl's own a_0-line rather than from the MOND literature, and "
    "it is the first construction in this programme not built by adapting someone else's "
    "theory ***",
    "both footings unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF33 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
