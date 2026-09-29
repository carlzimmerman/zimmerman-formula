#!/usr/bin/env python3
"""q2_structural_scoring.py -- lane Q4: K's structural rubric (S1 mechanism, S2 zero fitted reals with independent inputs, S3 testable beyond alpha, S4 not closed by lanes A-G/N1-N5 and not refuted by CODATA on its own terms)
applied to the ten Q4 claims. Scores are judgements with one evidence line each and a source label; content not read scores 0 on a criterion that needs it (K's policy).

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 q2_structural_scoring.py            -> exit 0 iff no claim scores 4/4 (H4)
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 q2_structural_scoring.py --mutate   -> S2 and S4 forced to 1 for every claim; must produce a spurious 4/4 survivor; exit 1
"""
import sys, os
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = "--mutate" in sys.argv
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# id: (name, [(S, score, evidence, source-status)...])
C = {
 "Q1": ("Primeon Theory: alpha = Delta-theta/(2 pi), phase spacing fixed by zeta(2) curvature of a prime-lattice", [
   ("S1", 1, "stated as a selection of a phase spacing by the curvature of arithmetic space (abstract wording only)", "SNIPPET"),
   ("S2", 0, "no formula or number seen; abstract says only that it 'matches the observed magnitude' (not read further)", "SNIPPET"),
   ("S3", 0, "no second observable visible in the snippet (unread content scores 0)", "SNIPPET"),
   ("S4", 1, "no value to refute; not one of lanes A-G, N1-N5", "SNIPPET")]),
 "Q2": ("Holographic Bit-Mode Balance: bits = U(1) edge modes at R*; F_U(1) = Z0/(Z0+2 R_K) = alpha + O(alpha^2)", [
   ("S1", 1, "a fixed-point condition (bit capacity = redundancy-free mode count) is stated as the selector of R*", "ABSTRACT (Crossref v1, v2)"),
   ("S2", 0, "the abstract itself: Z_int ~ R_K 'up to a dimensionless normalization factor'; Z0/(2 R_K) = alpha is an identity of the measured SI constants (q1 Q2b), so alpha enters as the input ratio", "ABSTRACT + q1"),
   ("S3", 0, "'experimentally testable' is asserted but no testable statement is visible in the abstracts (unread content scores 0)", "ABSTRACT"),
   ("S4", 0, "lane N4: the geometry depends only on alpha N^2, the count coefficient must come from non-geometric physics; the 'accessibility fraction' with a free normalization is that same tie (lane C also)", "N4 .out")]),
 "Q3": ("Xu tensor fields and harmonic cascades: alpha == x* = v/c fixed point of (mu, x)", [
   ("S1", 0, "the identification alpha := v/c is a postulate ('We postulate alpha == x*'); no mechanism connects a drift velocity to a coupling", "FULL TEXT"),
   ("S2", 0, "the published listing starts from a hard-coded 137.035999177 baseline; repaired, it prints 137.1016 for m = 2..8, not Table 1 (q3); kappa/alpha^2 ~ 1e-8 quoted as a magnitude", "FULL TEXT + q3"),
   ("S3", 0, "the hydrogen 1S-2S shift (+2.3e-15, Table 4) comes from a table the code does not reproduce (q3)", "FULL TEXT + q3"),
   ("S4", 1, "not one of lanes A-G, N1-N5; the stated value equals CODATA by construction so CODATA does not refute it (reproducibility failure is recorded under S2)", "FULL TEXT")]),
 "Q4": ("Maya lattice: variational planxel-lattice minimum (golden-ratio angle) plus an RG boundary condition at mu = 1/l_P", [
   ("S1", 1, "a variational principle whose extremum plus an RG boundary condition fixes 1/alpha is stated (abstract-level)", "SNIPPET"),
   ("S2", 0, "fitted reals not determinable from the snippet; lattice extrapolation quoted to +-0.02 cannot fix a 1e-10 number; the 1e-10 'two-loop' claim is unread (unread content scores 0)", "SNIPPET"),
   ("S3", 1, "named predictions: Lamb shift, g-2 and alpha variations in gravitational fields (abstract-level, no numbers read)", "SNIPPET"),
   ("S4", 0, "an RG boundary value at the Planck scale run down is lane B's class (charged content gives ~75-77, not 137); perturbative two-loop SM running cannot reach 1e-10 (hadronic vacuum polarization is non-perturbative; constructed criticism)", "B .out + constructed")]),
 "Q5": ("Relator / C-Space: alpha = the point where the scalar shell block D_C(alpha) meets the vector shell constant Lambda_geom (C_log = 1/3)", [
   ("S1", 1, "a compatibility (lock) condition between a scalar and a vector shell response selects alpha (paper Section I; reproduced by the published programs, q5)", "FULL TEXT (searched) + code"),
   ("S2", 0, "the source's own words: 'surgical edits' made against the g_e mismatch and a kernel-power convention chosen 'to reproduce' its tables; two published values 1.36e-8 apart; >= 25 hand-set choices; first-order elasticities 1.0 for Lambda_ind and K (q5). (T6: the target constant is not an input.)", "FULL TEXT + code"),
   ("S3", 1, "a pure-photonic g-2 series with A_1^(12) as a falsifiable prediction (abstract); the first coefficients are reproduced but were edited against (see S2)", "FULL TEXT (abstract)"),
   ("S4", 1, "not one of lanes A-G, N1-N5; the current value is 0.62 sigma from CODATA, not refuted", "code")]),
 "Q6": ("Kosmoplex: alpha^-1 = 137 + 1/(8 pi) - gamma/(137 + 1/(8 pi) - x) + zeta(3)/(137*20) from an 8D octonionic channel capacity", [
   ("S1", 1, "stated as the channel capacity of a reversible 8D -> 4D projection (poster)", "poster FULL TEXT"),
   ("S2", 0, "42-glyph alphabet chosen from; the correction integers (20 = 21 - 1 or a dodecahedral vertex count), the x-term form and the base 137 (two derivations) are assigned; the printed value is not what the printed formula gives (q4)", "poster + V20 + q4"),
   ("S3", 1, "five stated predictions incl. altitude dependence 4.6e-16 per km (but the slope printed is 1.2e6 x what the formula gives, q4)", "poster FULL TEXT + q4"),
   ("S4", 0, "the printed formula evaluates to 137.0359991003: 3.65 sigma (2.1e-8 unit) from CODATA 2022, not the 1.62 sigma claimed; V20's own evaluation is 773 sigma (q4)", "q4")]),
 "Q7": ("Bleger: alpha^-1 = 19596/143 + 5R/(6370-2R), R = ln(2+sqrt 3)", [
   ("S1", 0, "a formula; the source says 'We do not claim to have derived alpha from first principles'", "FULL TEXT"),
   ("S2", 0, "five integers and a constant; 26 formulas of the same shape are as simple and equally close (q6 G2); c3 = 11/28 fits better than the chosen 2/5 against CODATA 2022", "FULL TEXT + q6"),
   ("S3", 0, "the only prediction is the value itself (CODATA 2026)", "FULL TEXT"),
   ("S4", 1, "matches CODATA 2022 to 3.3e-11; not refuted; not one of lanes A-G, N1-N5", "q6")]),
 "Q8": ("Blandino: alpha^-1 = expectation of A(pi) - 1/(24A) - 1/(A^2 pi^2 K) over bounded continued fractions (E_int = 5, K = 10 - F)", [
   ("S1", 1, "a statistical mechanism is stated (alpha^-1 as the mean of an operator on a Hilbert space of continued fractions)", "FULL TEXT"),
   ("S2", 0, "K fitted to CODATA 2022; E_int 'calibrated'; {4,1,1} 'not derived'; '10' chosen so that <K> ~ 9.93; refs [2], [3] unchecked/suspect", "FULL TEXT"),
   ("S3", 1, "falsifiable statement: a future value needing a quotient > 45 would invalidate it (weak: P(no quotient > 45) ~ 0.78 per value, q6 B4)", "FULL TEXT + q6"),
   ("S4", 0, "on its own terms the model cannot represent 3 of the 5 CODATA values it treats as ensemble members (K needed outside (9,10)); the match is carried by K in a window of +-0.38 (q6)", "q6")]),
 "Q9": ("Reinisch: alpha ~ maximum eigenstate overlap probability of an alpha-free nonlinear Schrodinger-Poisson quantum-dot helium; 7.364e-3", [
   ("S1", 1, "a stated resonance/overlap condition in an alpha-free model determines a number identified with alpha", "HAL manuscript, FULL TEXT to Eq. 24"),
   ("S2", 1, "no fitted real; the model is alpha-free; the identification holds only 'within the ~1% tolerance' of a lowest-order QED argument", "HAL manuscript"),
   ("S3", 0, "the remainder of the paper (numerical evaluation after Eq. 24) was not read; 'stability of alpha' is a remark, not a derived law (unread content scores 0)", "HAL manuscript (partial)"),
   ("S4", 1, "0.9% from CODATA, inside its own stated 1% error; not one of lanes A-G, N1-N5 (cannot reach the bar's 5e-10 without the QED corrections that themselves need alpha)", "HAL manuscript")]),
 "Q10": ("Gilson: alpha^-1 = pi/(n2 cos(pi/n1) tan(pi/(n1 n2))), n1 = 137, n2 = 29", [
   ("S1", 0, "the derivation (stochastic mass-polarized vacuum; polygon wave capture) is only cited in the condensed paper read (unread content scores 0)", "arXiv quant-ph/0112048, condensed"),
   ("S2", 0, "the source: n2 = 25 'gave a theoretical value close to their central recommended value'; changed to 29 when the recommended range changed", "FULL TEXT"),
   ("S3", 1, "the same set C_Q is used to state values for the strong and electroweak couplings and their running", "FULL TEXT"),
   ("S4", 0, "the value misses CODATA 2022 by 27.8 sigma (lane K)", "K + q1")]),
}

P("q2_structural_scoring  MUTATE=%s" % MUTATE)
rows = []
for cid, (name, ss) in C.items():
    sc = {s: v for s, v, _, _ in ss}
    if MUTATE:
        sc["S2"] = 1; sc["S4"] = 1
    tot = sum(sc.values())
    rows.append((cid, name, sc, tot, ss))
for cid, name, sc, tot, ss in rows:
    P("")
    P("%s  %d/4  (%s)  %s" % (cid, tot, " ".join("%s=%d" % (k, sc[k]) for k in ("S1", "S2", "S3", "S4")), name))
    for (s, v, ev, src) in ss:
        P("    %s=%d  %s  [%s]" % (s, sc[s], ev, src))
survivors = [r[0] for r in rows if r[3] == 4]
deserve = [r[0] for r in rows if r[2]["S1"] == r[2]["S2"] == r[2]["S3"] == 1]
P("")
P("== Verdict ==")
P("4/4 survivors: %s" % (survivors if survivors else "none"))
P("claims that 'deserve a proper pre-registered test' (S1 = S2 = S3 = 1): %s" % (deserve if deserve else "none"))
P("3/4: %s" % [(r[0], [k for k in ("S1", "S2", "S3", "S4") if r[2][k] == 0][0]) for r in rows if r[3] == 3])
tag = "_MUTATE" if MUTATE else ""
open(os.path.join(HERE, "q2_structural_scoring%s.out" % tag), "w").write("\n".join(out) + "\n")
sys.exit(1 if survivors else 0)
