#!/usr/bin/env python3
"""U1-3 -- number-returning and duality principles P15-P18: Nariai-reduced critical damping, membrane quantum Hall, electric-magnetic self-duality, self-dual maps of the response functions.
Pre-registered in U1_PREREGISTRATION.md (written before this script was run; see its Amendment 1).

Run:    python3 u1_3_numbers_duality.py            (real run; exit 0 iff every check passes)
        python3 u1_3_numbers_duality.py --mutate   (control: the measured 1/alpha is replaced by 4*108/pi = 137.5099...; the Nariai-Dirac N = 108 candidate then hits the target exactly and
                                                    lane D's bar must clear, so check E1 ('no P15 candidate clears the bar') must FAIL; exit 1 = the control works)
Environment: PYTHONDONTWRITEBYTECODE=1
"""
import sys
sys.dont_write_bytecode = True
import math
import sympy as sp
import u1_lib as L

MUT = "--mutate" in sys.argv
chk = L.Checks()
PI = math.pi
TARGET_INV = 4 * 108 / PI if MUT else L.INV_ALPHA           # MUTATE: a target the P15 Dirac N=108 candidate hits exactly
print("=" * 118)
print("U1-3 P15-P18 -- " + ("MUTATE CONTROL (target replaced by 4*108/pi)" if MUT else "REAL RUN") + f"   target 1/alpha = {TARGET_INV:.9f}")
print("=" * 118)
REC = []


def cands(x):
    """floor / nearest / ceil integer candidates of a real N* (deduplicated, in that order)."""
    out = []
    for v in (math.floor(x), round(x), math.ceil(x)):
        if v not in out:
            out.append(v)
    return out


def score(pid, var, inv_pred, family_bits, extra=""):
    delta = abs(inv_pred / TARGET_INV - 1)
    bar = L.bar_assess(delta, family_bits)
    REC.append(dict(pid=pid, variant=var, inv_alpha_pred=inv_pred, delta=delta, clears=bool(bar["clears"]), P=bar["p"], extra=extra))
    return delta, bar


# ------------------------------------------------------------------------------------------- P15 Nariai-reduced critical damping
print("\nP15 Nariai-reduced critical damping.  Derivations (sympy):")
l1, l2, Lam = sp.symbols("l1 l2 Lambda", positive=True)
# Einstein G_ab + Lambda g_ab = 0 on dS_2 (radius l1) x S^2 (radius l2): Ricci = (1/l^2) g on each factor, R = 2/l1^2 + 2/l2^2
R_scalar = 2 / l1 ** 2 + 2 / l2 ** 2
eq1 = sp.Eq(1 / l1 ** 2 - R_scalar / 2 + Lam, 0)
eq2 = sp.Eq(1 / l2 ** 2 - R_scalar / 2 + Lam, 0)
sol = sp.solve([eq1, eq2], [l1, l2], dict=True)
print(f"    Nariai: Einstein equations give {sol}")
chk("N1 dS_2 x S^2 with Lambda: both radii equal Lambda^(-1/2), so R H_2 = 1", len(sol) == 1 and sp.simplify(sol[0][l1] * sp.sqrt(Lam) - 1) == 0 and sp.simplify(sol[0][l2] * sp.sqrt(Lam) - 1) == 0)
al, Nn, Rr, H2 = sp.symbols("alpha N R H_2", positive=True)
e4sq = 4 * sp.pi * al
e2sq = e4sq / (4 * sp.pi * Rr ** 2)                              # uniform LLL density 1/(4 pi R^2) (declared input)
res = {}
for lab, mgam in [("Dirac", Nn * e2sq / sp.pi), ("Weyl", Nn * e2sq / (2 * sp.pi))]:
    s_ = sp.solve(sp.Eq(mgam, H2 ** 2 / 4), al)[0]                # critical damping: m_gamma^2 = H_2^2/4 (N5-3)
    res[lab] = sp.simplify(s_.subs(Rr, 1 / H2))                   # R H_2 = 1
    print(f"    {lab}: alpha = {sp.simplify(s_)}  ->  at R H_2 = 1: alpha = {res[lab]}")
chk("N2 alpha = pi/(4N) (Dirac) and pi/(2N) (Weyl) at R H_2 = 1", sp.simplify(res["Dirac"] - sp.pi / (4 * Nn)) == 0 and sp.simplify(res["Weyl"] - sp.pi / (2 * Nn)) == 0)
c15 = []
for lab, fac in [("Dirac 1/alpha = 4N/pi", 4 / PI), ("Weyl 1/alpha = 2N/pi", 2 / PI)]:
    Nstar = TARGET_INV / fac
    print(f"    {lab}: inverse map N* = {Nstar:.4f} (NOT a test)")
    for Nc in cands(Nstar):
        inv = fac * Nc
        d, bar = score("P15", f"{lab}, N={Nc}", inv, math.log2(6))
        c15.append((lab, Nc, inv, d, bar["clears"]))
        print(f"        N = {Nc:4d}: 1/alpha_pred = {inv:.6f}, miss = {d:.3e} ({d / 1.6e-10:.3g} sigma_CODATA), bar clears: {bar['clears']}")
chk("E1 P15: no (variant, integer) candidate clears lane D's bar (nearest-integer miss >= 1e-3)", not any(c[4] for c in c15), f"(best miss {min(c[3] for c in c15):.3e})")
REC_P15_note = "not our dS_4: the geometry is dS_2 x S^2; needs uniform LLL density, N an integer, a charged massless fermion with zero modes"

# ------------------------------------------------------------------------------------------- P16 membrane quantum Hall
print("\nP16 membrane quantum Hall:  Z0 = R_K/N (a: 1/alpha = 2N)   or   Z0 = 2 R_K/N (b: 1/alpha = N)")
c16 = []
for lab, fac in [("a: 1/alpha = 2N", 2.0), ("b: 1/alpha = N", 1.0)]:
    Nstar = TARGET_INV / fac
    print(f"    {lab}: inverse map N* = {Nstar:.6f} (NOT a test)")
    for Nc in cands(Nstar):
        inv = fac * Nc
        d, bar = score("P16", f"{lab}, N={Nc}", inv, math.log2(6))
        c16.append((lab, Nc, inv, d, bar["clears"]))
        print(f"        N = {Nc:4d}: 1/alpha_pred = {inv:.6f}, miss = {d:.3e}, bar clears: {bar['clears']}")
chk("E2 P16: no candidate clears the bar (a: misses 7e-3; b: 137 misses 2.6e-4)", not any(c[4] for c in c16), f"(best miss {min(c[3] for c in c16):.3e})")
chk("E2b P16 non-integrality: N*_a = 1/(2 alpha) is not an integer (distance from the nearest integer > 0.4), so 'Z0 = R_K/N' fails as an exact statement", abs(TARGET_INV / 2 - round(TARGET_INV / 2)) > 0.4)

# ------------------------------------------------------------------------------------------- P17 EM self-duality
print("\nP17 electric-magnetic self-duality: e = g_m with e g_m = 2 pi n (HL) -> alpha = n/2 (n=1: 1/2);  tau = i convention: e^2 = 4 pi -> alpha = 1")
c17 = []
for lab, a_sd in [("e g = 2 pi, e = g: alpha = 1/2", 0.5), ("tau = i: alpha = 1", 1.0)]:
    d, bar = score("P17", lab, 1 / a_sd, 1.0)
    c17.append((lab, d, bar["clears"]))
    print(f"    {lab}: 1/alpha_pred = {1 / a_sd:.3f}, miss = {d:.4f}, bar clears: {bar['clears']}")
chk("E3 P17: neither self-dual coupling clears the bar (misses 0.985, 0.993)", not any(c[2] for c in c17))

# ------------------------------------------------------------------------------------------- P18 self-dual maps
print("\nP18 self-dual maps: is F(lambda') = F(lambda) an IDENTITY for a response function?  (fixed points of a map exist trivially for any F and select only a field value)")
mus = (0.3, 1.0, 2.0)
lams = (0.4, 0.7, 1.3, 2.0, 3.5)
cs = [("1", 1.0), ("1/2", 0.5), ("1/4", 0.25), ("1/pi", 1 / PI), ("1/(2 pi)", 1 / (2 * PI)), ("1/(4 pi)", 1 / (4 * PI)), ("2", 2.0), ("4", 4.0), ("pi", PI)]
funcs = {"r_scalar(lambda,mu)": lambda lam, mu: L.r_s(lam, mu) if mu * mu + lam * lam > 0.25 else float("nan"),
         "J_dirac/lambda": lambda lam, mu: L.J_f2(lam, mu) / lam}
maps = [(f"lambda -> {lab}/lambda", (lambda lam, mu, c=c: (c / lam, mu))) for lab, c in cs] + [("swap (lambda, mu) -> (mu, lambda)", lambda lam, mu: (mu, lam))]
chk("C0 P18 variant count = 10 maps", len(maps) == 10)
n_tests = 0
any_inv = []
print("    map                               " + "  ".join(f"{fn:>22s}" for fn in funcs))
for mlab, mp_ in maps:
    row = []
    for fname, F in funcs.items():
        worst = 0.0
        ndef = 0
        for mu in mus:
            for lam in lams:
                lam2, mu2 = mp_(lam, mu)
                a_, b_ = F(lam, mu), F(lam2, mu2)
                n_tests += 1
                if a_ == a_ and b_ == b_ and a_ != 0:
                    ndef += 1
                    worst = max(worst, abs(b_ / a_ - 1))
                # Amendment 4: points whose image is undefined (mu^2 + lambda'^2 <= 1/4 for the scalar factor) are skipped, as the pre-registration says ('where the image is defined')
        inv = (worst < 1e-6) and ndef >= 6
        row.append((worst, inv))
        if inv:
            any_inv.append((mlab, fname))
        REC.append(dict(pid="P18", variant=f"{mlab} on {fname}", worst=worst, invariant=bool(inv)))
    print(f"    {mlab:34s}" + "  ".join(f"{w:22.3e}" for w, _ in row))
chk("E4 P18: no map leaves either function exactly invariant on the mu > 0 grid (all worst deviations > 1e-6)", len(any_inv) == 0, f"({n_tests} tests; invariant: {any_inv})")
# massless dS_2 Dirac: J/(eH lambda) = 1/pi for every lambda -> invariant under every map, trivially
vals_massless = [L.J_f2(lam, 1e-9) / lam for lam in (0.2, 0.9, 3.0, 10.0)]
print(f"    massless dS_2 Dirac J/(eH lambda) at mu -> 0: {[f'{v:.10f}' for v in vals_massless]} (1/pi = {1 / PI:.10f}): constant, so every map is a symmetry -- and nothing is selected")
chk("E5 P18: the only invariant function is the constant massless dS_2 fermion (trivial: J/(eH lambda) = 1/pi at every lambda)", all(abs(v - 1 / PI) < 1e-8 for v in vals_massless))
REC.append(dict(pid="P18", variant="fixed-point remark", note="lambda = sqrt(c) is a fixed point of lambda -> c/lambda for ANY F; it selects a field value only (E free), so it does not fix alpha"))

fn = L.write_json("u1_3_results.json", MUT, dict(records=REC))
print(f"\nrecords written to {fn.split('/')[-1]}")
print(f"CHECKS: {sum(o for _, o in chk.items)}/{len(chk.items)} passed")
print("VERDICT: P15, P16, P17 DEAD (bar not cleared; integers do not hit 137.036); P18 DEAD (no identity-invariance except the trivial massless fermion). alpha stays an INPUT.")
L.finish(chk, MUT, targeted_tags=["E1"])
