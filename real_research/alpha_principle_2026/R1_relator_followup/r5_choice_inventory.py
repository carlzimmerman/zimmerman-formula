#!/usr/bin/env python3
"""r5_choice_inventory.py -- lane R1, part 1: the inventory of EVERY choice in the 'Relator' alpha construction, each with (i) the paper equation, (ii) a regex that must match a line of the
author's published program (Sep-2025 Zenodo 17109113 program; April-2026 GitHub 3a2614a program) so that the location claims are machine-checked, (iii) the printed value, (iv) the alternatives counted,
(v) whether r3 computed the alternative and the shift it produces, (vi) what changed in the April lineage; plus the numerical settings that are NOT choices and every place a measured quantity enters.
Programs are read from the cache written by r2 ($R1_CACHE/prog/*.py); nothing third-party is copied into the repo.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 r5_choice_inventory.py    -> exit 0 iff every registered regex matches and the number of computed choice points is 17
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 r5_choice_inventory.py --mutate   -> one regex is corrupted (C_UV with ln 3); the location check must fail: exit 1
"""
import sys, os, re, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = "--mutate" in sys.argv
CACHE = os.environ.get("R1_CACHE", "./r1_cache")
def P(*a):
    print(" ".join(str(x) for x in a), flush=True)
sep = open(os.path.join(CACHE, "prog", "zen17109113.py"), encoding="utf-8").read().splitlines()
apr = open(os.path.join(CACHE, "prog", "gh3a2614a.py"), encoding="utf-8").read().splitlines()
r3 = json.load(open(os.path.join(HERE, "r3_results.json")))
shift = {row["id"]: row for row in r3["shifts"]}

def locate(lines, rx):
    for i, l in enumerate(lines, 1):
        if re.search(rx, l):
            return i
    return None

# (id, class, element, paper eq, regex in Sep program, printed value, alternatives counted [a_i], r3 id or 'U'/'-' , April change)
SEP = [
 ("A1", "A", "chi (map) ladder", "(54)-(55)", r"CHI_LADDER_ON\s*=\s*True", "on", "on/off [2]", "A1", "removed; replaced by the reduced 'return' factor R_chi = 1 + beta_chi F_chi (hand-set A_ret, B_ret)"),
 ("A2", "A", "self-feedback ladder", "(56)-(58)", r"SELF_LADDER_ON\s*=\s*True", "on", "on/off [2]", "A2", "removed (see A1)"),
 ("A3", "A", "exterior-term evaluator", "(41)-(45)", r"a_l\s*=\s*- \(rstar\*\*\(l \+ 2\)\) \* s / Il", "literal projection with T_l = (1-x^2)P_l' (program 'exact')", "literal / closed (44) / l=1 / physical energy [4]", "A3", "kept (same literal projection); the April paper states the exact infinite sum = -1/2 ||J||^2"),
 ("A4", "A", "gamma_geom", "(50)", r"return mp.mpf\('0.5'\) \* \(1 \+ curvature_series_eta", "sinh(eta)/(2 eta) via a 12th-order series", "with curvature / without [2]", "A4", "kept (GAMMA_GEOM = 1/2 sinh(eta0)/eta0)"),
 ("A5", "A", "C_log target", "(75),(80)", r"\(mp.mpf\('3'\) / 2\) \* K \* Lambda", "1/3 (enters as the 3/2 in G_ind)", "1/3 / 2/3 [2]", "A5", "kept"),
 ("A6", "A", "zeta built from Lambda with sync", "(62),(84)", r"zeta_k = \(K / \(2 \* pi\*\*2\)\) \* Lambda_eff", "Lambda_eff (with sync)", "with / without sync [2]", "A6", "kept (Lambda_geom includes the return factor)"),
 ("A7", "A", "content of D_C", "(33)", r"D  = \(a / pi\) \* mp.sqrt\(1 - xi\) - \(a / pi\) \* \(xi / 2\) \* K", "uniform + K + L_2m (m>=2)", "full / K only / uniform only [3]", "A7", "replaced entirely by the 'rank-5 scalar evaluator' (radicand 1 - Theta D + D^2 Phi(D))"),
 ("B1", "B", "thin-ring constant in Lambda_ind", "(37)", r"LAMBDA_IND = mp.log\(8 \* mp.sqrt\(pi\)\) - 2", "-2", "-2 / -7/4 [2]", "B1", "kept"),
 ("B2", "B", "Gaussian UV constant", "(38)", r"C0_GAUSS\s*=\s*mp.mpf\('0.5'\) \* \(mp.log\(2\) \+ mp.euler\)", "(ln 2 + gamma)/2", "(ln2+gamma)/2 / gamma/2 [2]", "B2", "kept"),
 ("B3", "B", "weight for the near-shell energy C_uni", "(25)-(28)", r"C0_UNI\s*=\s*\(1 / pi\) \* \(mp.mpf\('4'\) / 3 \+ 1 / \(4 \* pi\*\*2\)\)", "j0^2 weight on a uniformly charged sphere", "|u0|^2 / uniform volume [2]", "B3", "kept (theta1_core = 2 pi C_uni)"),
 ("C1", "C", "coefficient of f_swirl in P_IR", "(47)", r"\(1 - mp.mpf\('1'\)/3 \* f_swirl\(x, ell\)\)", "1/3", "1/3, 1/2, 2/3 [3]", "C1", "kept"),
 ("C2", "C", "Gaussian exponent in P_IR", "(47)", r"mp.e\*\*\(-\(\(1 - x\)/ell\)\*\*2\)", "2", "2 / 1 [2]", "C2", "kept"),
 ("C3", "C", "f_swirl profile", "(47)", r"return \(\(1 - x\)\*\*2\) / \(\(\(1 - x\)\*\*2\) \+ ell\*\*2\)", "(1-x)^2/((1-x)^2 + l^2)", "two forms [2]", "C3", "kept"),
 ("C4", "C", "C_chi", "(66)", r"\(mp.mpf\('3'\) / 2\) \* K \* Lambda \* \(1 \+ \(K \* Lambda\) / \(2 \* pi\*\*2\)\)", "2 pi^2", "2 pi^2 / 2 pi [2]", "C4", "kept (C_CHI = 2 pi^2)"),
 ("C5", "C", "dressing (1+zeta)", "(68)-(71)", r"\(1 \+ \(K \* Lambda\) / \(2 \* pi\*\*2\)\)", "present", "present / absent [2]", "C5", "kept"),
 ("C6", "C", "eps_Dy definition", "(56)", r"ep = \(alpha / mp.pi\) \* \(K / \(2 \* mp.pi\*\*2\)\) \* P_ir \* Lambda_eff", "(alpha/pi)(K/2pi^2) P_IR Lambda", "3 forms [3]", "C6", "removed with the ladders"),
 ("C7", "C", "kappa", "(53)", r"k = mp.sinh\(eta\) / eta - 1", "sinh(eta)/eta - 1", "sinh(eta)/eta - 1 / eta^2/6 [2]", "C7", "kept inside beta_chi/gamma_geom only (A_ret, B_ret replace the ladder)"),
 ("U1", "C", "node index n", "(22)-(24)", r"ETA0\s*=\s*1 / pi", "n = 1 (r* = pi R, eta = 1/pi)", "n = 1, 2, 3 [3] (not computed)", "U", "kept"),
 ("U2", "C", "Gaussian width convention sigma_C = R/sqrt(pi)", "(13),(15)", r"EPSILON = 1 / mp.sqrt\(pi\)", "epsilon = 1/sqrt(pi)", "two conventions [2] (not computed)", "U", "kept"),
 ("U3", "C", "weight function of P_IR and of |u0|^2", "(47)", r"w = lambda x: \(x\*\*2\) \* \(mp.sin\(pi \* x\)\*\*2\)", "x^2 sin^2(pi x)", "two [2] (not computed)", "U", "kept"),
 ("U4", "C", "evaluation point of D_C in X and alpha in eps_Dy", "(59) 'avoiding circularity'", r"gamma_k = gamma_eff\(ETA0, K, DC_k, P_ir\)", "the lock value D_C(alpha_k)", "lock value / leading order alpha/pi [2] (not computed)", "U", "not applicable"),
]
NUMERIC = [
 ("dps, GL nodes, spectral depth SPEC_M_MAX, tail tolerance", r"mp.mp.dps = 90", "no effect above 1e-16 (Table VI cfgs 2-5)"),
 ("OUT_LMAX (odd cut-off of the literal exterior sum)", r"OUT_LMAX\s*=\s*19", "the literal sum converges algebraically: l<=19 vs l<=100 changes Delta Lambda_out by 5.3e-13 and alpha^-1 by 1.1e-10 (relative 8e-13): cfg-1 (137.0359991769773) vs cfg-2..5 (...770872/3)"),
 ("Aitken extrapolation of three partial sums", r"Sout = S1 - \(S2 - S1\)\*\*2 / denom", "applied to partial sums (l = 19, 21, 23) of an algebraically decaying tail that differ by 4e-12 and 2e-12 (r3); leaves 5.3e-13 of Delta Lambda_out unremoved (Table VI cfg-1)"),
 ("curvature series order", r"CURV_SERIES_ORDER = 12", "< 1e-15"),
 ("Delta Lambda_dyn and eps_Lambda knobs (default 0)", r"EPS_GIND\s*=\s*mp.mpf\('0'\)", "eps_Lambda = +-1e-9 moves alpha^-1 by 4.3e-7 relative (lane Q4, T6): a load-bearing knob set to zero"),
]
MEAS = [
 ("Sep-2025: reference alpha in the program", r"ALPHA_REF = mp.mpf\('7.297352564311e-3'\)", "logging only: replacing it by None or 7.4e-3 leaves alpha^-1 unchanged (r2, 0 change)"),
 ("Sep-2025: CODATA values in tables (Table IV/V), lock deviation at alpha_lab (Table III note), g_e comparison (Table X)", None, "comparisons in the paper, not in the code; Table X's g_e uses the emergent alpha and reports a 1.462 ppb mismatch that the text says is 'removed by two surgical edits' (exclude Delta Lambda_sync when forming zeta; TT-A kernel instead of TT-chi): edits made in the g_e sector; applied to the alpha closure the first edit would move alpha by 9.3e-4 (r3, 'no sync'), so it is NOT part of the alpha value"),
]
APR = [
 ("A_UV = ln2 eta^4", r"A_UV = mp.log\(TWO\) \* ETA_0\*\*4"), ("B_IR = eta^4/(8 pi^2)", r"B_IR = ETA_0\*\*4 / \(8 \* PI\*\*2\)"), ("N_omega = sqrt(2/pi)", r"N_OMEGA = mp.sqrt\(TWO / PI\)"),
 ("C_chi = 2 pi^2", r"C_CHI = TWO \* PI\*\*2"), ("S_UV = ln 2", r"S_UV = mp.log\(2\)"), ("S_IR = 1/(8 pi^2)", r"S_IR = ONE / \(8 \* PI\*\*2\)"),
 ("K closed form", r"\(150 \* PI\*\*2 - 8 \* PI\*\*4 - 315\) / \(180 \* PI\*\*6\)"), ("beta_cur = P_IR gamma_geom + P_IR Lambda_UV->IR/(2(1+A_UV))", r"return p_ir \* GAMMA_GEOM \+ \(p_ir \* lambda_uv_to_ir\) / \(TWO \* \(ONE \+ A_UV\)\)"),
 ("phi_j = (1 + B m/2)/(1 + A m)", r"phi_j = \(ONE \+ HALF \* B_IR \* m\) / \(ONE \+ A_UV \* m\)"), ("exterior memory = Lambda_out R_chi", r"exterior_memory = source.lambda_out \* R_chi"),
 ("theta1_core = 2 pi C_uni", r"theta1_core = TWO \* PI \* C_UNI"), ("theta1_coll = (gamma/pi^2) c11", r"theta1_coll = \(GAMMA_E / PI\*\*2\) \* c11"), ("theta1_log = eta^2/(8(1-eta^2/4))", r"theta1_log = ETA_0\*\*2 / \(8 \* \(ONE - ETA_0\*\*2 / FOUR\)\)"),
 ("a_shell = pi^2 c11 + gamma/4", r"a_shell = PI\*\*2 \* c11 \+ GAMMA_E / FOUR"), ("gamma_clog(D, ell) closed form", r"return \(SQRT_PI \* ell / TWO\) \* mp.e \*\* \(\(ell\*\*2 / FOUR\)"), ("N_c = sqrt(pi/8) ell0", r"n_c = mp.sqrt\(PI / 8\) \* base.ell0"),
 ("Delta a_mix = (gamma/pi^2) c_1n^2/(n^2-1)", r"delta_a_mix \+= \(GAMMA_E / PI\*\*2\) \* \(c1n\*\*2 / gap\)"), ("Delta a_0 = -(gamma/pi^2) c_1n^2 c_nn/(n^2-1)^3", r"delta_a0 \+= -\(GAMMA_E / PI\*\*2\)"), ("Delta a_diag = -eta^2 Delta a_0", r"delta_a_diag = -\(base.eta0\*\*2\) \* delta_a0"),
 ("chi = (Delta a_mix)^2", r"chi = delta_a_mix\*\*2"), ("article rank = 5", r"ARTICLE_RANK = 5"), ("refined kernel powers {1, 2}", r"REFINED_REALIZED_KERNEL_POWER = 2"), ("radicand 1 - Theta D + D^2 Phi", r"return ONE - scenario.theta_eff \* d_value \+ d_value\*\*2 \* scalar_dynamic_phi"),
 ("reference alpha^-1 (comparison layer)", r'ALPHA_INV_REF = mp.mpf\("137.035999177"\)'), ("pure-photonic QED coefficients A_1^(2n), n<=5 (comparison layer; A_1^(10) = 5.891)", r'5: mp.mpf\("5.891"\)'),
]
bad = 0
P("== Sep-2025 construction: choice inventory (locations checked against the published program, Zenodo 17109113) ==")
P("  %-3s %-2s %-46s %-9s %-5s %-28s %-42s %-8s %s" % ("id", "cl", "element", "paper eq", "line", "printed value", "alternatives [a_i]", "r3 shift", "April 2026"))
n_computed = 0; prod_c = 1; prod_u = 1
for cid, cl, el, eq, rx, pv, alt, r3id, apr_ch in SEP:
    if MUTATE and cid == "B2":
        rx = r"C0_GAUSS\s*=\s*mp.mpf\('0.5'\) \* \(mp.log\(3\) \+ mp.euler\)"
    ln = locate(sep, rx)
    if ln is None: bad += 1
    if r3id in shift:
        n_computed += 1
        row = shift[r3id]
        sh = "%.2e" % row["maxshift"]
        a_i = int(re.search(r"\[(\d+)\]", alt).group(1)); prod_c *= a_i
    else:
        sh = "n/c"
        a_i = int(re.search(r"\[(\d+)\]", alt).group(1)); prod_u *= a_i
    P("  %-3s %-2s %-46s %-9s %-5s %-28s %-42s %-8s %s" % (cid, cl, el[:46], eq, ln if ln else "NONE", pv[:28], alt[:42], sh, apr_ch[:90]))
P("\n  computed choice points: %d ; product of their a_i = %d ; uncomputed points U1-U4: product of a_i = %d ; N_all = %d = 2^%.1f" % (n_computed, prod_c, prod_u, prod_c * prod_u, __import__("math").log2(prod_c * prod_u)))
P("  (the 'max shift' column is the largest relative shift of alpha^-1 over the alternatives when swapped alone; n/c = not computed)")
P("\n== settings that are NOT choices but move the printed digits ==")
for el, rx, note in NUMERIC:
    ln = locate(sep, rx)
    if ln is None: bad += 1
    P("  line %-4s %-62s %s" % (ln if ln else "NONE", el[:62], note))
P("\n== where a measured quantity enters (Sep-2025) ==")
for el, rx, note in MEAS:
    ln = locate(sep, rx) if rx else "-"
    if rx and ln is None: bad += 1
    P("  line %-4s %-60s %s" % (ln, el[:60], note))
P("\n== April-2026 construction (GitHub 3a2614a): hand-set constants and forms read from the program (COUNT only; not re-implemented) ==")
n_apr = 0
for el, rx in APR:
    ln = locate(apr, rx)
    if ln is None: bad += 1
    else: n_apr += 1
    P("  line %-5s %s" % (ln if ln else "NONE", el))
P("  entries located: %d of %d. Of these, shared with the Sep-2025 construction: Lambda_ind, C_UV, gamma_geom, C_uni, C_chi, K (value), P_IR, eta, ell, the literal exterior projection; new in April: A_UV/A_ret, B_IR/B_ret, N_omega, S_UV, S_IR, the return factor, the rank-5 scalar evaluator" % (n_apr, len(APR)))
P("  measured quantities in April: the comparison layer (alpha^-1 reference, QED A_1^(2n)) is 'reference-only' in 3a2614a; the default lock of a635b6e used alpha_exp (r2); the QED-assisted branch (alpha_QED->D = 137.035999174117) uses A_1^(2n), n<=5, as input and is labelled 'one-way reference check' by the author")
P("\n== changes between versions that matter for the look-elsewhere count ==")
P("  Sep-2025 (Aug 30 - Oct 18): D_C = uniform + K + L_2m series; Lambda = Lambda_ind + Delta Lambda_UV->IR + Delta Lambda_out + sync (order-one + chi ladder + self ladder); value 137.0359991770873 (0.004 sigma from the CODATA-2022 centre)")
P("  Apr-08-2026: D_C = rank-5 'mother' radicand; Lambda includes the return factor R_chi (a 'representative' value 1.0459313210773864 supplied as a fixed input in the paper, later reproduced by a formula with hand-set A_ret, B_ret to 1e-14); value 137.03599917315644 (headline) / 137.03599916349474 (lock table)")
P("  Apr-27-2026: headline 137.035999163494704; the text calls it a 'realization-level output ... not asserted to be a certified operator-limit value'; the primary claim is 'conditional on the explicit postulates, branch calibrations, scalar evaluator, and vector-shell datum'")
ok = (bad == 0 and n_computed == 17) if not MUTATE else (bad == 0 and n_computed == 17)
P("\nlocation failures: %d ; computed choice points: %d (expected 17)" % (bad, n_computed))
P("VERDICT of script: %s" % ("all registered locations found (exit 0)" if ok else "a registered location was not found (exit 1)"))
json.dump(dict(n_computed=n_computed, prod_computed=prod_c, prod_uncomputed=prod_u, N_all=prod_c * prod_u, n_april_entries=n_apr, location_failures=bad), open(os.path.join(HERE, "r5_results%s.json" % ("_MUTATE" if MUTATE else "")), "w"), indent=1)
sys.exit(0 if ok else 1)
