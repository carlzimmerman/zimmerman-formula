#!/usr/bin/env python3
"""Q3 -- dictionary between Salam-Sezgin and lane F/N1's variables, free-parameter count, alpha along the flat direction, and the declared scoring (H5, H6).
Pre-registered in Q3_PREREGISTRATION.md (written before this script was run).

It runs q2 (real mode) as a subprocess to read the SU(2) coefficient, so it has no dependence on saved files or run order.

Run:   python3 q3_dictionary_and_scoring.py            (real run, exits 0)
       python3 q3_dictionary_and_scoring.py --mutate   (control: loosen lane D's bar to accept any probability and any miss; the PLANTED 1e-3 match
                                                        must then be (wrongly) accepted, so the check 'planted match rejected' FAILS and the script exits 1)
"""
import sys, os, math, subprocess, re
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import sympy as sp

MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
DBAR = os.path.join(HERE, "..", "D_calibration_bar")
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


ALPHA = 1 / 137.035999177
print("=" * 100)
print("Q3 dictionary and scoring -- mode: " + ("MUTATE CONTROL (bar loosened)" if MUTATE else "REAL RUN"))
print("=" * 100)

# ---------------------------------------------------------------- C1: dictionary to lane F (f2_flux_freund_rubin.py) and N1
print("\nC1  dictionary: Salam-Sezgin (g, p, kappa) <-> lane F (g_F, Lambda_6, chat = g_F^2/kappa_6)")
g, p, kap, N = sp.symbols("g p kappa N", positive=True)      # kap = kappa_6 (length^2); action R/(2 kappa^2); lane F's `kappa` is this kappa
E = sp.exp(p / 2)
gF2 = 2 * kap ** 2 * g ** 2 / E                              # (1/(2k^2)) (1/4) e^{p/2} F_hat^2 = F_F^2/(4 g_F^2) with A_F = g A_hat
chat = sp.simplify(gF2 / kap)
R2_ss = E / (8 * g ** 2)                                     # q1 A1b
R2_F = N ** 2 * kap ** 2 / (4 * gF2)                         # lane F Minkowski R*^2 = N^2 kappa^2/(4 g^2) (f2 B2a)
Lam_F = 1 / (2 * R2_F)                                       # lane F Lambda_6 = 1/(2 R*^2) (f2 B2b)
Lam_ss = 8 * g ** 2 / E / 2                                  # L = R - 8 g^2 e^{-p/2} = R - 2 Lambda
check("C1a g_F^2 = 2 kappa^2 g^2 e^{-p/2}, so chat = 2 kappa g^2 e^{-p/2}", sp.simplify(chat - 2 * kap * g ** 2 / E) == 0)
check("C1b at N = 1 lane F's Minkowski radius equals the Salam-Sezgin radius e^{p/2}/(8 g^2) for EVERY p", sp.simplify((R2_F - R2_ss).subs(N, 1)) == 0)
check("C1c at N = 1 lane F's Lambda_6 (= 1/(2R^2), the value that had to be tuned) equals the Salam-Sezgin potential's Lambda = 4 g^2 e^{-p/2}: the 'tuning' is a SUSY relation, not a choice", sp.simplify((Lam_F - Lam_ss).subs(N, 1)) == 0)
l2 = kap ** 2 / (32 * sp.pi ** 2 * R2_ss)                    # l_P^2 = G_4 = kappa_4^2/(8 pi), kappa_4^2 = kappa^2/(4 pi R^2)
R_over_lP_sq = sp.simplify(R2_ss / l2)
check("C1d (R/l_P)^2 = 2 pi^2/chat^2 (= lane F's sqrt2 pi N^2/chat at N = 1, squared)", sp.simplify(R_over_lP_sq - 2 * sp.pi ** 2 / chat ** 2) == 0)
# invariance under the rescaling symmetry p -> p + d, g -> g e^{d/4}: only chat matters
d = sp.symbols("d", real=True)
chat_shift = sp.simplify(chat.subs({g: g * sp.exp(d / 4), p: p + d}, simultaneous=True))
check("C1e chat, R/l_P (hence alpha) are invariant under p -> p + d, g -> g e^{d/4}: the source's 'only g e^{-phi0/4} is physical'; exactly ONE dimensionless real (chat) remains", sp.simplify(chat_shift - chat) == 0)

# q2's coefficient (subprocess, real mode)
out = subprocess.run([sys.executable, os.path.join(HERE, "q2_pauli_su2_coupling_and_u1.py")], capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
m = re.search(r"^ALPHA_SU2_COEFF = (\d+)$", out.stdout, re.M)
m2 = re.search(r"^ALPHA_SU2_COEFF_NOH = (\d+)$", out.stdout, re.M)
coeff_ss = int(m.group(1)) if m else None
coeff_noh = int(m2.group(1)) if m2 else None
check("C1f q2 (real mode) exits 0 and reports alpha_SU2 = 2 l_P^2/R^2 (with H_(3)) and 3 l_P^2/R^2 (without)", out.returncode == 0 and coeff_ss == 2 and coeff_noh == 3, f"[q2 exit {out.returncode}, coeff {coeff_ss}, no-H {coeff_noh}]")
al_su2 = sp.simplify(coeff_ss / R_over_lP_sq) if coeff_ss else None
print(f"    alpha_SU2 = {coeff_ss} l_P^2/R^2 = {al_su2}  (Salam-Sezgin);  lane F/N1 (no H_(3)): {sp.simplify(coeff_noh / R_over_lP_sq)} = 3 chat^2/(2 pi^2)")
check("C1g alpha_SU2 = chat^2/pi^2 on the Salam-Sezgin vacuum (N = 1), versus 3 chat^2/(2 pi^2) in lane F at N = 1", al_su2 is not None and sp.simplify(al_su2 - chat ** 2 / sp.pi ** 2) == 0)

# ---------------------------------------------------------------- C2: parameter table and the massive U(1)
print("\nC2  what is fixed and what is free (Salam-Sezgin bosonic sector, S^2 vacuum)")
print("    FIXED by the theory:   N = 1 (flux number, q1 A3), Lambda_6 = 2 g_F^2/kappa^2 (C1c), V = 0 exactly, the SU(2) isometry group, alpha_SU2/alpha_(SU2 flux) structure (2 l_P^2/R^2).")
print("    FREE (not fixed by SUSY or the vacuum equations):  chat = 2 kappa g^2 e^{-p/2} (equivalently the dilaton vev at fixed g; also R/l_P and alpha_SU2);")
print("                           the 6D gauge couplings g' of any additional 6D vector multiplets (source (5.5)-(5.7): 'absence of fine-tuning we would expect g' ~ g'), the matter content (anomaly cancellation gives")
print("                           n_H = dim G + 244, an integer relation, not a coupling), branes and their tensions (not studied).")
print("    ABSENT: a massless 6D U(1) photon (q2 B7); so N1's alpha_U1(unit) = N^2 l_P^2/(2R^2) has nothing to describe here.")
gp = sp.symbols("gprime", positive=True)
ratio_bulk = sp.simplify(((2 * gp) ** 2) / ((2 * g) ** 2))
check("C2a (source-based, not derived here) a bulk 6D YM group with F^I = dA + g' f A^A shares the same 4D kinetic function (source 5.6), so alpha_I/alpha_SU2 = (g'/g)^2 x (group normalisation): a free ratio", sp.simplify(ratio_bulk - (gp / g) ** 2) == 0)

# ---------------------------------------------------------------- C3: scoring
print("\nC3  scoring against lane D's bar (declared family: T1 7 trials + T2 9 trials = 16; N = 1 forced, not a trial)")
x = 2.8485e-122                                         # Lambda l_P^2 (lane F / AH5)
Rl_of_c = lambda c: c * (8 * math.pi / x) ** 0.25       # R/l_P for R = c/rho^(1/4), rho = x/(8 pi l_P^4)
T1, T2 = [], []
for cval in (1 / (2 * math.pi), 0.5, 1 / math.sqrt(2), 1.0, math.sqrt(2), 2.0, 2 * math.pi):
    a = 2.0 / Rl_of_c(cval) ** 2
    T1.append((cval, Rl_of_c(cval), a))
for name, h in (("1/(4pi)", 1 / (4 * math.pi)), ("1/(2pi)", 1 / (2 * math.pi)), ("1/pi", 1 / math.pi), ("1/2", 0.5), ("1", 1.0), ("2", 2.0), ("pi", math.pi), ("2pi", 2 * math.pi), ("4pi", 4 * math.pi)):
    T2.append((name, h, (h / math.pi) ** 2))
print("    T1: R = c/rho_Lambda^{1/4},  alpha_SU2 = 2 l_P^2/R^2")
for cval, Rl, a in T1:
    print(f"        c = {cval:.4f}: R/l_P = {Rl:.3e}, alpha_SU2 = {a:.3e}, miss vs Thomson = {abs(a / ALPHA - 1):.3e} (log10 alpha/alpha_T = {math.log10(a / ALPHA):.1f})")
print("    T2: chat = h,  alpha_SU2 = (h/pi)^2   (N = 1)")
for name, h, a in T2:
    print(f"        h = {name:8s}: alpha_SU2 = {a:.4e} (1/alpha = {1 / a:.4g}), miss = {abs(a / ALPHA - 1):.3e}")
allmiss = [abs(a / ALPHA - 1) for *_, a in T1] + [abs(a / ALPHA - 1) for *_, a in T2]
best = min(allmiss)
best_T2 = min(abs(a / ALPHA - 1) for *_, a in T2)
best_T1 = min(abs(a / ALPHA - 1) for *_, a in T1)
print(f"    best T1 miss = {best_T1:.3e};  best T2 miss = {best_T2:.3e};  16 trials, best overall {best:.3e}")
check("C3a NO trial reaches the bar's precision: every miss > 5e-10 (T1 misses are ~57-61 decades; T2's best is 41%)", best > 5e-10)
check("C3b T1 predicts alpha_SU2 ~ 1e-61 (KK scale tied to the observed vacuum energy, M_KK^4 = rho_Lambda, in the spirit of the SLED discussion in hep-th/0304256): 57-61 decades below alpha", all(a < 1e-59 for _, _, a in T1))
# requirement (not a prediction)
chat_req = math.pi * math.sqrt(ALPHA)
Rl_req = math.sqrt(2 / ALPHA)
print(f"    REQUIREMENT (not a prediction): alpha_SU2 = alpha_Thomson needs chat = pi sqrt(alpha) = {chat_req:.6f} and R/l_P = sqrt(2/alpha) = {Rl_req:.4f}"
      f"  (lane F had chat = 2 pi sqrt(alpha) N = 0.537 N and R/l_P = 8.28 N^2 ... with 3 instead of 2 and no H_(3)).")
check("C3c the required chat is a free real, not a Salam-Sezgin output: it is a one-parameter fit, i.e. 1 fitted real", True)
# consistency with the source's abstract number: KK scale 1e-3 eV -> bulk gauge coupling of order 1e-31
hbar_c_eVm = 1.973269804e-7
lP_m = 1.616255e-35
R_m = hbar_c_eVm / 1e-3
Rl_gp = R_m / lP_m
gYM_gp = math.sqrt(4 * math.pi * 2.0 / Rl_gp ** 2)
print(f"    consistency: M_KK = 1e-3 eV -> R = {R_m:.3e} m = {Rl_gp:.3e} l_P -> g_YM = sqrt(4 pi alpha_SU2) = {gYM_gp:.2e} (source abstract: 'of the order of 1e-31')")
check("C3d my alpha_SU2 = 2 l_P^2/R^2 reproduces the ORDER of the source's abstract estimate (bulk gauge coupling ~ 1e-31 at a 1e-3 eV KK scale): within a factor 10", 1e-32 < gYM_gp < 1e-30)

# planted match and the bar
sys.path.insert(0, DBAR)
import bar_lib as B                                       # noqa: E402
import alpha_bar_checker as AC                            # noqa: E402
if MUTATE:
    B.BAR_P = 2.0
    B.BAR_DELTA = 1.0
r_best = AC.assess(delta=best, size=16, verbose=False)
r_plant = AC.assess(delta=1e-3, size=16, verbose=False)
print(f"    bar on the best of the 16 trials (miss {best:.3e}, family size 16, 0 fitted reals): P = {r_best['p']:.3g}, precision ok: {r_best['c2_precision']}, clears: {r_best['clears']}")
print(f"    bar on a PLANTED 1e-3 match in the same family: P = {r_plant['p']:.3g}, clears: {r_plant['clears']}")
check("C3e lane D's bar does not clear the best trial", not r_best["clears"])
check("C3f the bar rejects a planted 1e-3 match in the same family (control of the scorer; precision criterion: 1e-3 > 5e-10)", not r_plant["clears"])

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("VERDICT (q3):")
print("  * Dictionary: the Salam-Sezgin S^2 vacuum IS lane F's Minkowski point (N = 1, Lambda_6 = 2 g_F^2/kappa^2, R^2 = e^{p/2}/(8 g^2)) with chat = 2 kappa g^2 e^{-p/2}; the SUSY relation removes lane F's Lambda_6 tuning (V = 0 for every p) but chat survives as the dilaton vev.")
print("  * alpha_SU2 = 2 l_P^2/R^2 = chat^2/pi^2 (not 3 l_P^2/R^2); R/l_P = sqrt2 pi/chat is FREE along the flat direction; the U(1) is massive.")
print("  * Scoring: 16 declared trials, none within 5e-10 (best miss {:.2e}); T1 (KK scale from the observed vacuum energy) gives alpha_SU2 ~ 1e-61. Alpha stays an INPUT (the dilaton vev).".format(best))
sys.exit(0 if n_ok == len(CHECKS) else 1)
