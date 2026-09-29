"""D3: rule of thumb -- how many free choices a formula may contain before a match at precision delta means nothing.
Usage: python3 d3_rule_of_thumb.py [MUTATE]   (MUTATE mis-states the budget by 100x; the brute-force self-consistency check must fail, exit 1)"""
import sys, math
import bar_lib as B

MUTATE = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
cal = B.load_cal()
FAIL = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        FAIL.append(name)


rhos = {k: cal[k]["rho_frac"] for k in ("E1_6", "E2_6", "E1_12", "E2_12", "E3_6", "E3_12")}
print("rho (family values per unit relative deviation, as a fraction of the family) measured in d1:")
for k, v in rhos.items():
    print(f"   {k}: {v:.4f}")
rho = cal["E2_12"]["rho_frac"]
print(f"rule uses rho = {rho:.4f} (spread across grammars: {min(rhos.values()):.3f} .. {max(rhos.values()):.3f})")

# lambda = N rho 2 delta  ->  P < P0  <=>  N < -ln(1-P0) / (2 rho delta)
def Nmax(delta, P0):
    lam0 = -math.log1p(-P0)
    return (lam0 / (2 * rho * delta)) * (0.01 if MUTATE else 1.0)


print("\nMaximum family size N (distinct alternatives you could have written down, counted before looking) for which a match at precision delta")
print("is still unlikely by chance, P = 1 - exp(-N rho 2 delta) < P0:")
print(f"{'delta':>10} {'sigma_CODATA':>13} | {'N_max (P0=1e-3)':>16} {'bits':>6} {'int 1..12':>10} {'int 1..100':>11} | {'N_max (P0=0.05)':>16} {'bits':>6}")
deltas = [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 5e-10, 1.6e-10]
rows = []
for d in deltas:
    n3, n5 = Nmax(d, 1e-3), Nmax(d, 0.05)
    print(f"{d:10.1e} {d/B.DELTA_CODATA:13.3g} | {n3:16.4g} {math.log2(max(n3,1e-30)):6.1f} {math.log(max(n3,1e-30),12):10.2f} {math.log(max(n3,1e-30),100):11.2f} | {n5:16.4g} {math.log2(max(n5,1e-30)):6.1f}")
    rows.append((d, n3, n5))

# brute-force self-consistency with the shared bar
print("\nself-consistency against the shared bar (B.evaluate):")
ok_all = True
for d, n3, n5 in rows:
    lo = B.evaluate(d, n3 * 0.99, rho); hi = B.evaluate(d, n3 * 1.01, rho)
    good = lo["p"] < 1e-3 <= hi["p"] * 1.0000001 or (lo["p"] < 1e-3 and hi["p"] >= 1e-3 * 0.999)
    ok_all &= bool(good)
check("N_max sits exactly at P = 1e-3 for every delta (0.99 N_max passes P, 1.01 N_max does not)", ok_all)

print("\nwhat the table means, with the grammars measured in d1 (E1/E2/E3 = at most 1/2/3 binary operations, atoms {1..12, pi, e, Z}):")
for k, lab in (("E1_12", "E1(12)"), ("E2_12", "E2(12)")):
    N = cal[k]["N_distinct"]
    print(f"   {lab}: N = {N:.3g} ({math.log2(N):.1f} bits) -> needs delta <= {1e-3/(2*rho*N):.2e} for P<1e-3")
N3 = cal["E3_12"]["N_est"]
print(f"   E3(12): N ~ {N3:.3g} ({math.log2(N3):.1f} bits, estimated) -> needs delta <= {1e-3/(2*rho*N3):.2e}; the best achievable delta is delta_CODATA = {B.DELTA_CODATA:.1e}: "
      f"lambda at delta_CODATA = {N3*rho*2*B.DELTA_CODATA:.3g}")
check("a 3-operation small-integer formula cannot reach P<1e-3 even at the CODATA limit", N3 * rho * 2 * B.DELTA_CODATA > 1e-3)
check("a 2-operation formula (E2(12)) needs delta <= ~5e-10 (within 3 sigma_CODATA)", 1e-3 / (2 * rho * cal["E2_12"]["N_distinct"]) < 1e-9)

bits3 = lambda d: math.log2(Nmax(d, 1e-3))
print("\nRULE OF THUMB (P<1e-3, rho = 0.025):  bits of freedom allowed  b_max = log2(0.02/delta)")
print(f"   delta 1e-3 -> {bits3(1e-3):.1f} bits (about ONE free integer in 1..12 and nothing else);  1e-5 -> {bits3(1e-5):.1f} bits;  1e-9 -> {bits3(1e-9):.1f} bits (about 6.8 integers in 1..12);  CODATA limit 1.6e-10 -> {bits3(1.6e-10):.1f} bits")
print("   costs: an integer in 1..12 = 3.6 bits; an integer in 1..100 = 6.6 bits; a choice among 5 operations = 2.3 bits; a choice among 3 constants = 1.6 bits; a unary decoration (5 options) = 2.3 bits;")
print("   each extra 'scale of alpha' or 'group/dimension/normalisation' you might have tried multiplies N (adds log2 of its count).")
print("   So: a 1e-3 match is evidence only if the whole family has <= ~20 members; a 1e-5 match, <= ~2000; a 1e-9 match, <= ~2e7 (E2-size); and NO numeric match can support a family larger than ~1e8 (27 bits), because the")
print("   data stop at 1.6e-10. Evidence must come from FORCING the choices (N -> 1), not from a hit.")

print("\nFAILED:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
