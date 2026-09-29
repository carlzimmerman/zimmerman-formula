#!/usr/bin/env python3
"""k2_structural_scoring.py -- lane K: structural-survival rubric S1..S4 (K_PREREGISTRATION.md, Amendments 1-3) and the ranked table.

Run (real):        python3 k2_structural_scoring.py               -> exit 0 iff NO idea scores 4/4
MUTATE (Amend 3):  python3 k2_structural_scoring.py --mutate      -> forces S2 and S4 to 1 for every idea; must produce a spurious survivor => exit 1
                   python3 k2_structural_scoring.py --mutate-s2   -> the originally declared control (S2 only): reports whether the survivor set changes (expected: it does NOT; exit 0 if unchanged, 1 if changed)

Criteria (fixed before scoring): S1 mechanism that would DETERMINE a coupling (not a numerical expression, not a bound); S2 zero fitted reals as stated, dimensionless inputs with independent definitions;
S3 a testable statement beyond reproducing alpha; S4 not closed by lanes A,B,C,E,F,G and not refuted by CODATA on its own terms.
Policy: no credit for content I did not read (SNIPPET / SUMMARY / abstract-only content scores 0 on a criterion that needs it). Each score carries its evidence line.
Numbers are read from k1_results.json (written by k1_numeric_audit.py, real run).
"""
import sys, os, json, math
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MODE = "real"
if "--mutate" in sys.argv:
    MODE = "mutate"
elif "--mutate-s2" in sys.argv:
    MODE = "mutate_s2"

# id: (name, claims, (S1,S2,S3,S4), evidence dict, source status)
IDEAS = [
    ("E1", "alpha^-1 = integer count of exclusion-principle states (Eddington 136 -> 137)", ["K1a", "K1b"], (1, 0, 1, 0),
     ["S1: derivation claimed from Dirac equation + exclusion principle (Kragh, full text)",
      "S2=0: the extra unit was added after experiment showed ~137, Kragh: 'forced to look for a fault ... alpha^-1 = 137 exactly'",
      "S3: same theory gives m_p/m_e from 10x^2 - 136 w x + w^2 = 0 and a cosmic particle number 2*136*2^256 (Kragh)",
      "S4=0: 137.036 is not an integer (miss 2.6e-4 = 1.6e6 sigma_CODATA, k1); alpha runs; Pauli 1929 'complete nonsense' (Kragh); Dirac-Peierls-Pryce 1942"],
     "FULL TEXT (Kragh)"),
    ("E2", "small-integer + transcendental formulas, pre-2019 (Gilson, Anastassov, Eagles list, Dattoli, Sherbon)", ["K2a", "K2b1", "K2b2", "K2b3", "K14"], (0, 0, 0, 0),
     ["S1=0: Dattoli on his own and Gilson-type formulas: 'no physical motivation ... alchemic combination of numbers'",
      "S2=0: integers 29 and 137 are data-selected (k1 s2: the integer 29 is 0.30 from the real a* = 28.695; rounding chance 0.61)",
      "S3=0: no second observable in any of them",
      "S4=0: all miss the 2022 target by 27.8 to 1.4e4 sigma (k1)"],
     "value FULL TEXT (Dattoli, Anastassov); formulas SNIPPET (Gilson, Sherbon)"),
    ("E2b", "2026 self-published closed forms (Bleger 19596/143 + 5R/(6370-2R); Blandino with a fitted K)", ["K11a", "K11b"], (0, 0, 0, 1),
     ["S1=0: formula only; the 'three primes' remark is a SUMMARY of a Zenodo record (unverified by me)",
      "S2=0: five integers (family ~1.4e12, k1 P_decl = 0.90) for Bleger; Blandino fits K to CODATA 2022 by its own account (1 fitted real)",
      "S3=0: none stated in the summaries I read",
      "S4=1: Bleger matches 2022 to 3.3e-11 (0.2 sigma); not refuted, and this is the case the D bar is for: P = 0.9 in its own family, so no evidence"],
     "SUMMARY only (Zenodo record pages)"),
    ("E3", "Atiyah 2018: 1/alpha = T(pi) via the Todd map of a hyperfinite factor (renormalisation of pi)", ["K3"], (1, 0, 0, 1),
     ["S1: stated as a renormalisation-flow definition of 1/alpha (full text)",
      "S2=0: text says the calculation 'Starting from the Eddington number 137' and 'start anew with Zh(1) = 137.035 as starting point': leading digits are input; printed recursion (8.3) is inconsistent (k1 check i); |product of unit roots| = 1 (k1 check ii)",
      "S3=0: only 'more calculations will predict subsequent decimals' and a remark on weak-gravity labs (no testable second observable)",
      "S4=1 formally (no definite value to refute; not covered by lanes A-G) BUT the scale is not consistent: 'Energy increases so pi has to increase to Zh, which models 1/alpha' (an ultraviolet limit) yet Zh is compared with the Thomson value; Buckley: ignores running (Gizmodo SUMMARY)"],
     "FULL TEXT (manuscript); critiques SUMMARY"),
    ("E4", "Wyler: 1/alpha from volumes of D_5, Q_5, S^4 (invariance group O(5,2))", ["K5"], (1, 0, 0, 0),
     ["S1: geometric ratio-of-volumes principle (Jentschura-Nandori, full text)",
      "S2=0: Robertson: an extra scaling factor destroys the agreement; radii set to 1 without reason (as cited in 1411.4673 and D); Pease: wrong Poisson-kernel coefficient",
      "S3=0: no second coupling predicted",
      "S4=0: miss 6.1e-7 = 3.8e3 sigma_CODATA (k1; D)"],
     "FULL TEXT (Jentschura-Nandori)"),
    ("E5", "eigenvalue condition: alpha is a zero of the Gell-Mann-Low / Callan-Symanzik function (Johnson-Baker-Willey, Adler 1972)", ["K6", "K12"], (1, 1, 1, 0),
     ["S1: alpha would be a fixed point (infinite-order zero of the one-loop beta) (Adler's own commentary, full text)",
      "S2: no fitted real: the eigenvalue is whatever the theory dictates",
      "S3: uniform charge for all fermion species; free-propagator asymptotics; infinite-order zeros of all current correlators (Adler commentary)",
      "S4=0: Adler: the conjecture 'turned out to be wrong'; Wilson: the infinite-order zero means no eigenvalue in QED; Adler-Callan-Gross-Jackiw inconsistency; 'No eigenvalue in finite QED' (1997); QED triviality confirmed by lattice/exact-RG (1411.4673, Sec. II A)"],
     "FULL TEXT (Adler commentary); PRD 5 3021 abstract via SNIPPET"),
    ("E6", "dynamical varying alpha: scalar dilaton coupled to F^2 (Bekenstein 1982; Sandvik-Barrow-Magueijo 2002)", ["K7", "K8"], (1, 0, 1, 0),
     ["S1: alpha(t, x) is the exponential of a field (BSBM, full text; Bekenstein 2002 intro, full text)",
      "S2=0: present-epoch alpha is an input (eps set to 1 today); zeta_m/omega = -0.02% used for the plotted run; the dark matter must be magnetic-dominated (BSBM)",
      "S3: predicts Delta alpha/alpha history, Eotvos-test signal (BSBM proposes both)",
      "S4=0: it fixes no value of alpha (Bekenstein: 'the framework's sole parameter'); lane E: attractors reach any target, bounds constrain lambda*delta never alpha_m"],
     "FULL TEXT (BSBM, Bekenstein 2002 intro); Bekenstein 1982 SNIPPET"),
    ("E7", "combinatorial hierarchy: 1/alpha = 137 [1 - 1/(30 x 127)]^-1", ["K9"], (1, 0, 1, 0),
     ["S1: counting principle generating 3, 7, 127 (Noyes, full text)",
      "S2=0: the correction e = 1/(30 x 127) is assigned by a frequency argument specific to one atom model; 137 = nearest integer",
      "S3: also gives G_N^-1 hbar c/m_p^2 = [2^127 + 136][1 - 1/(3.7.10)] = 1.6933e38 vs 1.6936e38 and G_F (Noyes)",
      "S4=0: miss 2.3e-7 = 1450 sigma_CODATA (k1); SNIPPET critique: 'Program Universe' does not produce the hierarchy"],
     "FULL TEXT (Noyes); critique SNIPPET"),
    ("E8", "group-order formula 1/alpha = N(N-1)/(4 pi), N = 42 (Rosen)", ["K13"], (1, 0, 0, 0),
     ["S1: alpha from the order of an invariance group (1411.4673 full text)",
      "S2=0: 1411.4673: S6 and S8 not excluded and give markedly different values",
      "S3=0", "S4=0: miss 2.6e-5 = 1.6e5 sigma_CODATA (k1)"],
     "FULL TEXT of a description (1411.4673)"),
    ("E9", "anthropic / environmental selection of alpha", ["K10"], (0, 1, 0, 1),
     ["S1=0: a window, not a determining condition",
      "S2=1: no fitted real (no formula)",
      "S3=0 by policy: the only content I have is a SNIPPET (a few-percent carbon-production window)",
      "S4=1: not closed by lanes A-G and not refuted; but it cannot reach a 1e-9 value (window is percent-level)"],
     "SNIPPET only"),
    ("E10", "Nambu 1952: particle masses as integer multiples of (1/2)(1/alpha) m_e", ["K4"], (0, 0, 0, 0),
     ["S1=0 no mechanism; S2=0 uses 1/alpha as an INPUT unit; S3=0 by policy (snippet); S4=0 mass-sector relation, SM mass sector walled here"],
     "SNIPPET only"),
    ("E11", "gravity-electromagnetism links: Weyl/Dirac large numbers, Eddington's N_C, Kaluza-Klein alpha ~ G/(r phi)^2, string g_o^2 ~ g_c", ["K-link"], (1, 0, 1, 0),
     ["S1: alpha tied to G, cosmic size or a modulus (1411.4673 Secs. III, V B, V C, full text)",
      "S2=0: proportionality factors 'might depend on other fundamental constants' (1411.4673)",
      "S3: implies time/space variation of alpha or G",
      "S4=0: KK radius unstable and masses far too large (1411.4673 V B); lane F: alpha traded for a free 6D ratio, R=23.4 l_P needs ~115 decades of cancellation"],
     "FULL TEXT (1411.4673)"),
    ("E12", "RG boundary condition: alpha O(1) at the Planck scale, run down (1411.4673 Eqs. 28-29; asymptotic safety)", ["K-RG"], (1, 0, 1, 0),
     ["S1: alpha_IR from running a Planck-scale boundary value",
      "S2=0: kappa0 = 5/9 or 2/3 by cutoff type; N0 from multiplet content; unification value assumed (1411.4673)",
      "S3: 'five or six additional heavy charged leptons, neutrinos and quark multiplets' (1411.4673) -- not observed",
      "S4=0: lane B: charged content gives alpha^-1 ~ 75-77 not 137; fixed points give bounds, not values"],
     "FULL TEXT (1411.4673); lane B outputs"),
    ("E13", "Reinisch 2024: alpha as the solution of an alpha-free nonlinear non-relativistic quantum model", ["K11c"], (1, 0, 0, 1),
     ["S1: alpha stated to be an output of a model with no alpha input (abstract only)",
      "S2=0, S3=0 by policy: not verifiable from an abstract",
      "S4=1: the author's own error is ~1% (mean-field), 1/alpha = 135.8 vs 137.036; not closed by lanes A-G. Worth a full read; it is not a survivor"],
     "abstract via SNIPPET only"),
]

CLAIM_ROWS = [  # id, claim label, idea id, source status, strongest published criticism
    ("K1a/K1b", "Eddington 136 / 137", "E1", "FULL TEXT (Kragh)", "Pauli 1929: 'complete nonsense', 'romantic poetry' (Kragh); Dirac-Peierls-Pryce 1942; 136 abandoned when data said 137"),
    ("K2a", "Gilson pi/(29 cos(pi/137) tan(pi/(29*137)))", "E2", "value FULL (Dattoli); form SNIPPET", "Dattoli (a numerologist's own verdict): no physical motivation; 27.8 sigma off CODATA 2022 (k1)"),
    ("K2b", "Anastassov / Eagles list, Dattoli Pythagorean", "E2", "FULL TEXT", "none needed: 754 to 3.9e3 sigma off"),
    ("K14", "Sherbon 4 pi^3 + pi^2 + pi", "E2", "SNIPPET", "no published critique read; 1.4e4 sigma off"),
    ("K3", "Atiyah Todd-map 1/alpha", "E3", "FULL TEXT + SUMMARY critiques", "Litt: internal inconsistencies (summary); Buckley: ignores running (summary); k1 checks i-iii"),
    ("K5", "Wyler", "E4", "FULL TEXT (JN)", "Pease (Poisson-kernel coefficient), Robertson (extra scaling factor) via JN; 3.8e3 sigma off"),
    ("K6/K12", "Adler eigenvalue / JBW", "E5", "FULL TEXT (Adler commentary)", "Adler himself: 'turned out to be wrong'; Wilson: infinite-order zero => no eigenvalue"),
    ("K7", "Bekenstein 1982", "E6", "SNIPPET (1982); FULL (2002)", "not a derivation claim; sole parameter free"),
    ("K8", "Sandvik-Barrow-Magueijo", "E6", "FULL TEXT", "not a derivation claim; alpha_0 input, zeta fitted"),
    ("K9", "combinatorial hierarchy", "E7", "FULL TEXT (Noyes)", "numerology charge; hierarchy not produced by the program (SNIPPET); 1450 sigma off"),
    ("K13", "Rosen N = 42", "E8", "FULL TEXT of description", "JN: S6/S8 not excluded; 'either exact or group theory fails'; 1.6e5 sigma off"),
    ("K10", "anthropic selection", "E9", "SNIPPET", "gives a window not a value"),
    ("K4", "Nambu 137/2 mass unit", "E10", "SNIPPET", "none read"),
    ("K11a", "Bleger 2026", "E2b", "SUMMARY", "none found; family size gives P = 0.90 (k1)"),
    ("K11b", "Blandino 2026", "E2b", "SUMMARY", "none found; K fitted to CODATA 2022 by the author's own account"),
    ("K11c", "Reinisch 2024", "E13", "abstract SNIPPET", "none read; author's own 1% mean-field error"),
]


def score(idea, mode):
    s = list(idea[3])
    if mode == "mutate":
        s[1] = 1; s[3] = 1
    elif mode == "mutate_s2":
        s[1] = 1
    return s


def main():
    res = json.load(open(os.path.join(HERE, "k1_results.json")))
    numbers = {}
    for k, v in res.items():
        numbers[k] = v
    # helper numbers for claims not in the json
    numbers["K3"] = dict(miss=1.29e-9, P_mdl=None, P_decl=None)
    numbers["K11c"] = dict(miss=0.00905, P_mdl=None, P_decl=None)
    lines = []

    def P(s=""):
        print(s)
        lines.append(s)

    P("k2_structural_scoring  MODE=%s" % MODE)
    survivors, three = [], []
    for idea in IDEAS:
        sc = score(idea, MODE)
        t = sum(sc)
        fails = [("S1", "S2", "S3", "S4")[i] for i in range(4) if sc[i] == 0]
        P("%-4s %d/4 (S1 S2 S3 S4 = %s)  fails: %s  | %s  [%s]" % (idea[0], t, "".join(str(x) for x in sc), ",".join(fails) or "none", idea[1], idea[5]))
        if t == 4:
            survivors.append(idea[0])
        elif t == 3:
            three.append(idea[0])
    P("")
    P("Evidence lines (scores as fixed in the script; MODE only changes S2/S4 in mutation runs):")
    for idea in IDEAS:
        P(" %s %s" % (idea[0], idea[1]))
        for e in idea[4]:
            P("     " + e)
    P("")
    P("Binding criterion per idea (a single criterion whose repair would raise the score is listed; 'S2 binding' means S2 is the only failure):")
    for idea in IDEAS:
        s = score(idea, "real")
        f = [("S1", "S2", "S3", "S4")[i] for i in range(4) if s[i] == 0]
        P("  %s fails %s%s" % (idea[0], ",".join(f) or "none", "  <- S2 is the only failure" if f == ["S2"] else ""))
    s2_only = [i[0] for i in IDEAS if [("S1", "S2", "S3", "S4")[j] for j in range(4) if score(i, "real")[j] == 0] == ["S2"]]
    P("  ideas whose ONLY failure is S2: %s (so forcing S2 = 1 alone cannot create a survivor)" % (s2_only or "none"))
    P("")
    P("Result: 4/4 ideas: %s ; 3/4 ideas: %s" % (survivors or "none", three or "none"))
    base_surv = [i[0] for i in IDEAS if sum(score(i, "real")) == 4]
    if MODE == "mutate_s2":
        P("mutate-s2: survivor set changes vs real (%s -> %s): %s" % (base_surv or "none", survivors or "none", set(survivors) != set(base_surv)))
    P("H3 (first half: at least one idea reaches 3/4; second half: none reaches 4/4): %s / %s" % ("TRUE" if three else "FALSE", "TRUE" if not base_surv else "FALSE"))

    # ranked claim table (real scores)
    if MODE == "real":
        by_id = {i[0]: i for i in IDEAS}
        table = []
        for cid, label, iid, status, crit in CLAIM_ROWS:
            sc = sum(by_id[iid][3])
            ids = {"K1a/K1b": ["K1b"], "K2b": ["K2b3"], "K6/K12": [], "K7": [], "K8": [], "K10": [], "K4": []}.get(cid, [cid])
            nums = numbers.get(ids[0]) if ids else None
            miss = nums["miss"] if nums else None
            pm = nums.get("P_mdl") if nums else None
            pd = nums.get("P_decl") if nums else None
            pu = pd
            if cid == "K2a":
                pu = 0.61
            table.append((sc, pu if pu is not None else 9.0, miss if miss is not None else 9.0, cid, label, status, crit, miss, pm, pd, pu))
        table.sort(key=lambda r: (-r[0], r[1], r[2]))
        md = ["# K -- ranked table of published claims for alpha (bar of lane D; T = 137.035999177)", "",
              "Ranking key (pre-registered): (1) bar cleared [none], (2) structural score S/4 of the associated idea, (3) P_used ascending, (4) miss. 'n/a' = no evaluable formula or no declared family.",
              "P_used = P_decl (declared slot family) except K2a where the rounding chance 0.61 replaces the flat-density 8.9e-6 (Amendment 3).", "",
              "| rank | claim | struct. | miss | sigma_CODATA | P_MDL | P_used | clears bar | source status | strongest published criticism |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r, (sc, _a, _b, cid, label, status, crit, miss, pm, pd, pu) in enumerate(table, 1):
            def f(x, fmt="%.3g"):
                return "n/a" if x is None else fmt % x
            md.append("| %d | %s: %s | %d/4 | %s | %s | %s | %s | no | %s | %s |" % (r, cid, label, sc, f(miss), f(miss / 1.6e-10 if miss else None), f(pm), f(pu), status, crit))
        md += ["", "## Structural ideas (S1 mechanism, S2 zero fitted reals, S3 testable beyond alpha, S4 not closed / not refuted)", ""]
        for idea in sorted(IDEAS, key=lambda i: -sum(i[3])):
            md.append("* %s (%d/4, fails %s): %s" % (idea[0], sum(idea[3]), ",".join(("S1", "S2", "S3", "S4")[j] for j in range(4) if idea[3][j] == 0) or "none", idea[1]))
            for e in idea[4]:
                md.append("    * " + e)
        md += ["", "## Verdict", "", "No claim clears the bar. No idea scores 4/4. Highest structural scores: " + ", ".join("%s (%d/4)" % (i[0], sum(i[3])) for i in sorted(IDEAS, key=lambda i: -sum(i[3]))[:3]) + "."]
        open(os.path.join(HERE, "K_REPORT_TABLE.md"), "w").write("\n".join(md) + "\n")
        P("wrote K_REPORT_TABLE.md")
    tag = {"real": "", "mutate": "_MUTATE", "mutate_s2": "_MUTATE_S2"}[MODE]
    open(os.path.join(HERE, "k2_structural_scoring%s.out" % tag), "w").write("\n".join(lines) + "\n")
    if MODE == "mutate_s2":
        sys.exit(1 if set(survivors) != set(base_surv) else 0)
    sys.exit(1 if survivors else 0)


if __name__ == "__main__":
    main()
