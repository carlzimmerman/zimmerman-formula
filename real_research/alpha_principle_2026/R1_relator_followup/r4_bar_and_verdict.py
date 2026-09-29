#!/usr/bin/env python3
"""r4_bar_and_verdict.py -- lane R1, part 4 and 5: look-elsewhere probability with the family size ESTIMATED from the construction (r3), lane D's checker imported UNMODIFIED, and the
assembly of the pre-registered verdict rule (R1_PREREGISTRATION.md, 'Definitions of the three verdicts' and Amendment 3). Reads r1_results.json (not needed), r2_results.json and r3_results.json.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 r4_bar_and_verdict.py
              -> exit 0 iff the assembled verdict string equals the recorded one:
                 'Sep-2025: ADJUSTED (D3); Apr-2026 published values: UNDECIDABLE; a635b6e default lock: ADJUSTED (D1)'
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 r4_bar_and_verdict.py --mutate
              -> every miss := 1e-11, H2_printed_definitions := True, the D-items and the compensation flag are cleared; the assembled string must change: exit 1.
"""
import sys, os, json, math
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import alpha_bar_checker as ABC       # lane D, unmodified
import bar_lib as B
MUTATE = "--mutate" in sys.argv
def P(*a):
    print(" ".join(str(x) for x in a), flush=True)

r2 = json.load(open(os.path.join(HERE, "r2_results.json")))
r3 = json.load(open(os.path.join(HERE, "r3_results.json")))
r5 = json.load(open(os.path.join(HERE, "r5_results.json")))
RHO = ABC.RHO_DEFAULT
P("lane D checker imported unmodified; rho = %.5f per unit relative deviation (E2(12) calibration)" % RHO)
cc = r3["class_counts"]
prod = lambda l: int(math.prod(l))
N_A = prod(cc["A"]); N_B = prod(cc["B"]); N_C = prod(cc["C"])
N_lower = N_A; N_mid = N_A * N_B; N_upper = N_A * N_B * N_C
P("choice points from r3: class A a_i = %s (product %d), class B %s (%d), class C %s (%d)" % (cc["A"], N_A, cc["B"], N_B, cc["C"], N_C))
P("N_lower = %d (2^%.1f), N_mid = %d (2^%.1f), N_upper = %d (2^%.1f); the uncomputed node index A8 (3 alternatives) multiplies each by 3; 17 of 17 choice points are 'effective' (r3)" %
  (N_lower, math.log2(N_lower), N_mid, math.log2(N_mid), N_upper, math.log2(N_upper)))

MISS = {"Sep-2025 converged headline (cfg-5, 6.4e-13)": 6.379e-13, "Sep-2025 program default (cfg-1, 1.7e-13)": 1.66e-13,
        "Apr-2026 published (Eq. 6, 137.035999163494704)": 9.86e-11, "Apr-08-2026 headline (Eq. 5, 137.03599917315644)": 2.8e-11}
if MUTATE:
    MISS = {k: 1e-11 for k in MISS}
NS = [("N_lower (A only)", N_lower), ("N_mid (A,B)", N_mid), ("N_upper (A,B,C)", N_upper), ("N_upper x3 (node index)", 3 * N_upper), ("N_all (17 computed + U1-U4, r5)", float(r5["N_all"])), ("2^25 (lane Q4 lower bound)", 2.0 ** 25), ("2^40 (lane Q4 upper bound)", 2.0 ** 40)]
P("\n== flat look-elsewhere (lane D): P = 1 - exp(-N rho 2 delta); bar: P < 1e-3, miss <= 5e-10, 0 fitted reals, scale stated ==")
tab = {}
for lab, d in MISS.items():
    P("  %s   (miss %.3e = %.3g sigma_CODATA)" % (lab, d, d / 1.6e-10))
    tab[lab] = {}
    for nl, N in NS:
        r = ABC.assess(delta=d, size=N, verbose=False)
        tab[lab][nl] = r["p"]
        P("      %-30s N = %-10.4g  lambda = %.3e  P = %.3e  bar (all four criteria): %s" % (nl, N, r["lam"], r["p"], "CLEARS" if r["clears"] else "does not clear"))
    nstar = 1e-3 / (RHO * 2 * d)
    P("      break-even family size N* (P = 1e-3) = %.3e = 2^%.1f" % (nstar, math.log2(nstar)))
    tab[lab]["Nstar"] = nstar
sep = "Sep-2025 converged headline (cfg-5, 6.4e-13)"
p2 = tab[sep]["N_mid (A,B)"] < 1e-3 and tab[sep]["N_upper (A,B,C)"] < 1e-3
P("\n  P2 (bar clears at N_mid and N_upper for the Sep-2025 headline): %s" % p2)
P("  reading: the flat formula cannot explain a 6.4e-13 landing by chance with the counted freedom (%d-%d members); it fails only above 2^%.1f = %.2e members. The counted freedom is a LOWER bound on the search actually possible: it excludes" % (N_lower, N_upper, math.log2(tab[sep]['Nstar']), tab[sep]['Nstar']))
P("    the implementation-level departures (r3: the L_2m recurrence shifts alpha by 3.9e-9; the literal exterior projection differs from the printed closed form by 17.5%), any earlier development history, and functional forms with no named alternative.")

P("\n== hierarchical (stage-wise) estimate from r3 section 5 (author-lineage set) ==")
sr = r3["stage_rows"]
land = 1.0
for i in range(2, len(sr)):
    lab, inv, shift, miss = sr[i]
    pi_ = min(1.0, miss / shift)
    land *= pi_
    P("  stage %-34s correction %.3e residual %.3e  chance %.2e" % (lab, shift, miss, pi_))
P("  product over the three stages after the geometric gain: %.2e ; last stage alone: %.2e" % (land, min(1.0, sr[-1][3] / sr[-1][2])))
P("  independent of stages: with the L_2m of the printed definition the chain ends %.2e relative from the target (r3): the last-stage agreement exists only with the recurrence error" % (abs(r3["inv_def"] / 137.035999177 - 1)))

P("\n== registered verdict rule, per lineage ==")
dep = r2["dependency"]
d = r2["derived"]
# evidence items from r2, r3 (real run) -- MUTATE clears them
H2_printed = (abs(r3["inv_def"] / 137.035999177 - 1) <= 1e-9) if not MUTATE else True
P1 = H2_printed
P2 = p2
P3_sep = True    # no documented use of a measured alpha in the Sep-2025 alpha closure: r2 perturbation of its logging constant changes nothing
P3_sep = P3_sep and (dep["sep"] == 0.0)
comp_ratio = abs(float(d["dalpha"]) / (1.003247 * float(d["dl"])))
P4_sep = not (comp_ratio < 1e-3) if not MUTATE else True      # False = drift with compensation of size 1e-6 to within 1e-3 of itself
D1_sep = dep["sep"] > 1e-9
D2_sep = False
D3_sep = (abs(r3["inv_def"] / 137.035999177 - 1) > 5e-10 and abs(r3["inv_tab"] / 137.035999177 - 1) < abs(r3["inv_def"] / 137.035999177 - 1)) if not MUTATE else False
D1_a635 = dep["a635b6e"] > 0.5 and not MUTATE
D1_apr_headline = (dep["0468974"] > 1e-12 or dep["27da3a1"] > 1e-12 or dep["3a2614a"] > 1e-15) and not MUTATE
P("  Sep-2025:  P1 (printed text determines the value; printed L_2m gives miss %.2e vs bar 5e-10): %s" % (abs(r3["inv_def"] / 137.035999177 - 1), P1))
P("             P2 (bar clears at N_mid and N_upper): %s ; P3 (no documented use of a measured alpha in its alpha closure): %s ; P4 (no compensating drift; Sep->Apr ratio %.2e): %s" % (P2, P3_sep, comp_ratio, P4_sep))
P("             D1 (reference alpha is an input): %s ; D2 (text/code says an ingredient was modified against a measured quantity, and it enters alpha): %s ; D3 (printed value fails to follow from the printed equations, departure toward the reference): %s" % (D1_sep, D2_sep, D3_sep))
if D1_sep or D2_sep or D3_sep:
    v_sep = "ADJUSTED (%s)" % ",".join(n for n, f in (("D1", D1_sep), ("D2", D2_sep), ("D3", D3_sep)) if f)
elif P1 and P2 and P3_sep and P4_sep:
    v_sep = "PREDICTION"
else:
    v_sep = "UNDECIDABLE"
P("             -> %s" % v_sep)
P("  Apr-2026 published values (programs 0468974, 27da3a1, 3a2614a): D1 (they depend on alpha_exp): %s (perturbation change: %s, %s, %s) ; D2: False ; D3: not evaluated (April construction not re-implemented)" %
  (D1_apr_headline, dep["0468974"], dep["27da3a1"], dep["3a2614a"]))
v_apr = "ADJUSTED (D1)" if D1_apr_headline else "UNDECIDABLE"
P("             -> %s" % v_apr)
P("  a635b6e default lock (Apr 8, 10:51 UTC): D1 (alpha_out elasticity to alpha_exp = %.3f; refined branch returns alpha_exp identically, labelled a 'self-consistency check of the chosen bridge'): %s" % (dep["a635b6e"], D1_a635))
v_a635 = "ADJUSTED (D1)" if D1_a635 else "UNDECIDABLE"
P("             -> %s" % v_a635)
P("  indicators (never sufficient alone): Sep printed headline %.4f sigma from the CODATA-2022 centre (chance 3.3e-3 for a correct theory); Sep -> Apr compensation ratio %.2e; Lambda(3a2614a) vs Lambda(alpha_exp) %.2e relative; stage-wise landing product %.2e" %
  (0.0042, comp_ratio, abs((float(d["lam_geom"]) - float(d["lam_lock"])) / float(d["lam_lock"])), land))

verdict = "Sep-2025: %s; Apr-2026 published values: %s; a635b6e default lock: %s" % (v_sep, v_apr, v_a635)
expected = "Sep-2025: ADJUSTED (D3); Apr-2026 published values: UNDECIDABLE; a635b6e default lock: ADJUSTED (D1)"
P("\nassembled:", verdict)
P("expected :", expected)
ok = verdict == expected
P("VERDICT of script: %s" % ("recorded verdict string reproduced (exit 0)" if ok else "verdict string differs from the recorded one (exit 1)"))
json.dump(dict(tab=tab, N=dict(lower=N_lower, mid=N_mid, upper=N_upper), verdict=verdict), open(os.path.join(HERE, "r4_results%s.json" % ("_MUTATE" if MUTATE else "")), "w"), indent=1, default=str)
sys.exit(0 if ok else 1)
