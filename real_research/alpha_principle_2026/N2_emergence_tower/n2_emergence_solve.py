#!/usr/bin/env python3
"""N2 -- emergence closures with the declared towers (pre-registration: N2_PREREGISTRATION.md, criteria N2-N5).
Run:    PYTHONDONTWRITEBYTECODE=1 python3 n2_emergence_solve.py          (exit 0 iff the integrity checks pass; expectation outcomes are REPORTED, not gating)
MUTATE: PYTHONDONTWRITEBYTECODE=1 python3 n2_emergence_solve.py MUTATE   (positional argv; the self-consistent species cutoff is replaced by the fixed N_0 cutoff; the identity
                                                                          Lambda^2 N(Lambda) = M_red^2 with N counting the tower states below Lambda must then fail -> exit 1)
Method: given the compactification scale M_c = 1/R, Lambda_sp solves Lambda^2 N(Lambda) = M_red^2 (N_0 = 118 plus tower dof below Lambda).
If 1/alpha_i(Lambda_sp) = 0 then 1/alpha_i(M_Z) = (1/2 pi)[ b_SM,i ln(Lambda/M_Z) + sum_j b_ij ln(Lambda/m_j) ] =: F_i(M_c).
Closure i: solve F_i(M_c) = measured 1/alpha_i(M_Z) (this SPENDS the modulus on coupling i); the other two F_j are then predictions.
1/alpha_em(M_Z) = F_Y + F_2; 1/alpha_em(0) = that + 9.106 (measured offset, an input).
"""
import sys, json, math
sys.dont_write_bytecode = True
import tower_lib as T

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
SC = not MUT
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + (" " + m if m else ""))
    if not ok: fails.append(n)

out = {}
print("inputs: measured 1/alpha(M_Z) = (Y %.4f, 2 %.4f, 3 %.4f); M_red = %.4e; N_0 = %d; 1/alpha(0) - 1/alpha(M_Z) = %.3f; target 1/alpha(0) = %.9f" % (T.MEAS + (T.M_RED, T.N0, T.DELTA0, T.ALPHA_INV0)))
print("SM-only reference: Lambda_0 = M_red/sqrt(118) = %.3e GeV" % (T.M_RED / math.sqrt(118)))
for grav in (True, False):
    print("\n################ N convention: KK gravitons %s ################" % ("INCLUDED (main)" if grav else "EXCLUDED (reported)"))
    for tw in T.TOWERS:
        for i in range(3):
            roots, rng = T.find_roots(i, tw, grav=grav, selfcons=SC)
            key = "%s|%s|%s" % (tw.name.split()[0], T.NAMES[i], "G" if grav else "noG")
            out[key] = []
            if not roots:
                print("[%s, closure %s] NO ROOT: over the whole scan (M_c from 1e5 GeV to Lambda_0) F_%s ranges %.3g .. %.3g; the measured 1/alpha_%s(M_Z) = %.4f is not reachable"
                      % (tw.name, T.NAMES[i], T.NAMES[i], rng[0], rng[1], T.NAMES[i], T.MEAS[i]))
                continue
            for Mc in roots:
                s = T.summarize(Mc, tw, grav=grav, selfcons=SC)
                ident = abs(s["Lambda"] ** 2 * T.N_of(tw, s["k"], grav) - T.M_RED ** 2) / T.M_RED ** 2
                out[key].append({k: (v if not isinstance(v, (list, tuple)) else list(v)) for k, v in s.items()})
                print("[%s, closure %s] M_c = %.4e GeV (R = %.3e l_P) | Lambda_sp = %.4e GeV, k = %d levels below, x = Lambda/M_c = %.3f, N = %d%s"
                      % (tw.name, T.NAMES[i], Mc, T.MPL / Mc, s["Lambda"], s["k"], s["x"], s["N"], " (PINNED at a threshold)" if s["pinned"] else ""))
                print("      predicted 1/alpha(M_Z): Y %.4f (meas %.4f)  2 %.4f (meas %.4f)  3 %.4f (meas %.4f) ; sin^2 = %.5f (meas %.5f)"
                      % (s["F"][0], T.MEAS[0], s["F"][1], T.MEAS[1], s["F"][2], T.MEAS[2], s["s2"], T.RC.S2W))
                print("      implied 1/alpha at Lambda_sp (measured minus predicted; emergence needs 0): Y %.3f  2 %.3f  3 %.3f ; em %.3f" % (s["resid"][0], s["resid"][1], s["resid"][2], s["resid_em"]))
                print("      1/alpha_em(M_Z) = %.4f ; 1/alpha_em(0) = %.4f vs 137.036 (miss %.3e relative)" % (s["em_MZ"], s["em_0"], abs(s["em_0"] / T.ALPHA_INV0 - 1)))
                chk("identity Lambda^2 N(Lambda) = M_red^2 at [%s, %s, %s]" % (tw.name.split()[0], T.NAMES[i], "G" if grav else "noG"), s["pinned"] or ident < 1e-9, "rel diff %.2e%s" % (ident, " (pinned, exempt)" if s["pinned"] else ""))

print("\n================ N3: sign-feasibility (pre-registered expectation vs found; main N convention) ================")
def has(t, i): return len(out["%s|%s|G" % (t, T.NAMES[i])]) > 0
exp = {("TA", 0): True, ("TA", 1): True, ("TA", 2): True, ("TB", 1): False, ("TB", 2): False, ("TC", 0): False, ("TC", 1): False, ("TC", 2): False}
for (t, i), e in exp.items():
    got = has(t, i)
    print("EXPECTATION %s closure %s: root %s ; found %s -> %s" % (t, T.NAMES[i], "expected" if e else "not expected", "yes" if got else "no", "met" if got == e else "NOT MET (expectation was wrong)"))
print("(TB closure Y: root exists, %s; TC closure Y: none)" % ("yes" if has("TB", 0) else "no"))

print("\n================ N4: emergence vs requirement 0, at the Y-closure root (main N convention) ================")
for t in ("TA", "TB"):
    for s in out["%s|Y|G" % t]:
        print("%s: x = %.2f, Lambda_sp = %.3e; implied 1/alpha at Lambda_sp: Y %.2f (0 by construction), 2 %.2f, 3 %.2f, em %.2f (SM alone: 107.25 at 2.24e17)" % (t, s["x"], s["Lambda"], s["resid"][0], s["resid"][1], s["resid"][2], s["resid_em"]))

print("\n================ N5: does anything fix x = Lambda/M_c? ================")
for t, tw in (("TA", T.TA), ("TB", T.TB)):
    nl = tw.level_fn(1, True)[0]
    for cg, lab in ((math.pi, "pi (S^1/Z2 of length pi R)"), (2 * math.pi, "2 pi (S^1)")):
        # geometric relation M_red^2 = c_g R M_5^3 with M_5 = Lambda_sp gives N = (M_red/Lambda)^2 = c_g x ; species count gives N = N_0 + n_lvl x
        denom = cg - nl
        print("%s: N = c_g x vs N = %d + %d x, c_g = %s: x = N_0/(c_g - n_lvl) = %.3f -> %s" % (t, T.N0, nl, lab, T.N0 / denom, "NO positive root" if denom <= 0 else "root"))
    xs = []
    for i in range(3):
        for s in out["%s|%s|G" % (t, T.NAMES[i])]:
            xs.append((T.NAMES[i], s["x"], s["Mc"]))
    if xs:
        print("%s closure moduli: %s" % (t, "; ".join("%s: x = %.2f, M_c = %.3e" % a for a in xs)))
        if len(xs) == 3:
            xv = [a[1] for a in xs]
            print("%s spread max/min - 1 = %.1f %% ; x_Y vs mean of (x_2, x_3): %.1f %%" % (t, 100 * (max(xv) / min(xv) - 1), 100 * (xv[0] / (0.5 * (xv[1] + xv[2])) - 1)))
# SM-only 2-3 crossing scale (context for the near-agreement of closures 2 and 3 in TA)
b2, b3 = float(T.b_SM()[1]), float(T.b_SM()[2])
Lc = T.MZ * math.exp(T.TWO_PI * (T.MEAS[1] - T.MEAS[2]) / (b2 - b3))
print("context: SM-only 1/alpha_2 = 1/alpha_3 crossing at %.3e GeV (a species scale M_red/sqrt(N) with N = %.0f)" % (Lc, (T.M_RED / Lc) ** 2))
if out["TA|Y|G"]:
    fa = out["TA|Y|G"][0]["F"]
    print("TA at the Y-closure root: measured minus predicted (1/alpha_2 - 1/alpha_3)(M_Z) = %.3f (measured difference %.3f)" % ((T.MEAS[1] - T.MEAS[2]) - (fa[1] - fa[2]), T.MEAS[1] - T.MEAS[2]))
print("         TA has b~_2 - b~_3 = 1/6 per level, so its 2-3 difference is nearly x-independent: closures 2 and 3 agree in x (38.44 vs 38.60) because Lambda_sp (N ~ 7300) lands where the")
print("         SM 2-3 difference plus the small tower differential is about the measured 21.1. That is a property of the SM 2-3 crossing scale and of N, not of a forced tower principle.")
json.dump(out, open("n2_results_MUTATE.json" if MUT else "n2_results.json", "w"), indent=1)
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
