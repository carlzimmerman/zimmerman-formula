"""D2: audit of known formulas by the look-elsewhere machinery. See D_PREREGISTRATION.md.
Usage: python3 d2_audit_known_formulas.py [MUTATE]
MUTATE: (i) claims 4Z^2+3 matches at 1e-9 and (ii) uses Wyler's formula with exponent 1/3; the consistency checks must FAIL (exit 1)."""
import sys, math, time
import numpy as np
import mpmath as mp
import bar_lib as B

MUTATE = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 40
FAIL = []
RES = {}


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        FAIL.append(name)


cal = B.load_cal()
rho_E2 = cal["E2_12"]["rho_frac"]
Tm = mp.mpf("137.035999177")
lnx_inv = 279.8686   # ln(1/x), x = Lambda G hbar/c^3 = 2.8485e-122, copied from AH5 output (alpha_schwinger_2026/ah5_dimensional_obstruction.out)
x = 2.8485e-122
sigma_rel = B.DELTA_CODATA

print("Building E1/E2 for N = 6 and 12 ...")
G = {N: B.Grammar(N) for N in (6, 12)}
for g in G.values():
    g.build_E2()


def lam_win(arr, center, tol, ws=(1e-2, 3e-2, 1e-1, 3e-1), need=30):
    for w in ws:
        c = B.count_window(arr, center, w)
        if c >= need:
            break
    return B.lam_from_counts(c, w, tol), c, w


def delta(v):
    return float(abs(mp.mpf(v) / Tm - 1))


print("\n=== A1: 1/alpha = 4 Z^2 + 3,  Z = 2 sqrt(8 pi/3) ===")
Zm = 2 * mp.sqrt(8 * mp.pi / 3)
v1 = 4 * Zm ** 2 + 3
d1 = delta(v1)
claim_d1 = 1e-9 if MUTATE else d1
print(f"  value = {mp.nstr(v1, 12)} (= 128 pi/3 + 3);  relative miss = {d1:.3e};  in sigma_CODATA = {d1/sigma_rel:.3g}")
check("A1 stated precision equals computed precision", abs(claim_d1 - d1) < 1e-3 * d1, f"claimed {claim_d1:.2e} vs computed {d1:.2e}")
for N in (6, 12):
    arr = G[N].E2
    i = np.searchsorted(arr, float(v1))
    mem = min(abs(arr[max(i - 1, 0)] / float(v1) - 1), abs(arr[min(i, arr.size - 1)] / float(v1) - 1)) < 1e-12
    lam, c, w = lam_win(arr, B.T, d1)
    print(f"  E2({N}): member={mem};  chance hits at its own precision delta={d1:.2e}: lambda={lam:.3g} (count {c} in window {w:g})  P(>=1)={B.p_from_lam(lam):.4g}  size={arr.size:,}")
    check(f"A1 is an E2({N}) member", bool(mem))
    RES[f"A1_E2_{N}"] = dict(lam=lam, p=B.p_from_lam(lam))
lg, st = B.mdl_size("4*Z**2+3")
print(f"  MDL size of the shape of the expression: 2^{lg:.2f} = {2**lg:.3g}  (E2(12) syntactic count 2^{math.log2(G[12].E2s):.2f})")
check("MDL size reproduces the E2(12) syntactic count for a two-op expression (within 2^0.01)", abs(lg - math.log2(G[12].E2s)) < 0.01)
# most charitable declared family: a Z^s + c
vals = []
for a in range(1, 13):
    for s in (1, 2, 3, 0.5, -1, -2):
        for c in range(0, 13):
            vals.append(a * float(Zm) ** s + c)
vals = np.sort(np.array(vals)); Nt = np.unique(np.round(vals, 12)).size
c25 = B.count_window(vals, B.T, 0.25)
lamT = B.lam_from_counts(c25, 0.25, d1)
print(f"  Template a*Z^s + c (a in 1..12, s in {{1,2,3,1/2,-1,-2}}, c in 0..12; {vals.size} members, {Nt} distinct): count within 25% of target={c25}; lambda at delta={d1:.2e} = {lamT:.3g};  P(>=1)={B.p_from_lam(lamT):.3g}")
ev = B.evaluate(d1, G[12].E2.size, rho_E2)
print(f"  Bar on E2(12): p={ev['p']:.3g} (c1 {ev['c1_lookelsewhere']}), precision c2={ev['c2_precision']} (delta {d1:.1e} vs limit {B.BAR_DELTA:.0e}), clears={ev['clears']}")
evT = B.evaluate(d1, Nt, c25 / Nt / 0.5 / 1.0 if False else (c25 / (2 * 0.25)) / Nt)
print(f"  Bar on the a Z^s + c template: p={evT['p']:.3g}, precision c2={evT['c2_precision']}, clears={evT['clears']}  (the family was defined AFTER seeing the formula: its size is a post-hoc choice)")
RES["A1_template"] = dict(lam=lamT, p=B.p_from_lam(lamT))
check("A1 does not clear the bar", not ev["clears"] and not evT["clears"])

print("\n=== A2: Wyler, alpha = (9/(8 pi^4)) (pi^5/(2^4 5!))^(1/4) ===")
expo = mp.mpf(1) / 3 if MUTATE else mp.mpf(1) / 4
aW = 9 / (8 * mp.pi ** 4) * (mp.pi ** 5 / (2 ** 4 * mp.factorial(5))) ** expo
vW = 1 / aW
dW = delta(vW)
print(f"  1/alpha_W = {mp.nstr(vW, 14)}; literature value quoted by arXiv:1411.4673 Eq.8 = 137.0360824")
check("A2 formula reproduces 137.0360824 (7 dp)", abs(float(vW) - 137.0360824) < 1e-7, f"got {float(vW):.10f}")
print(f"  relative miss = {dW:.3e} ({dW*1e6:.3f} ppm);  = {dW/sigma_rel:.0f} sigma_CODATA (sigma_rel {sigma_rel:.1e}); abs miss {float(vW-Tm):.3e}")
lg2, st2 = B.mdl_size("9/(8*pi**4)*(pi**5/(2**4*factorial(5)))**(1/4)")
print(f"  MDL size (free numerology language, integers up to 1920): 2^{lg2:.1f} trees; binary ops = {st2['nb']}, integer bound {st2['maxint']}")
# templates
Fa = np.array([b * math.pi ** c / a for a in range(1, 17) for b in range(1, 17) for c in range(1, 9)])


def template(ks, tag):
    Gk = np.array([(k * math.pi ** (-d)) ** (1.0 / g) for d in range(1, 9) for g in range(1, 9) for k in ks])
    v = (Fa[:, None] * Gk[None, :]).ravel()
    nsyn = v.size
    v = np.sort(v)
    keep = np.ones(v.size, dtype=bool)
    keep[1:] = (v[1:] - v[:-1]) > 1e-12 * v[1:]
    v = v[keep]
    del keep
    c3 = B.count_window(v, B.T, 1e-3)
    dec = B.decoys(400)
    cd = np.array([B.count_window(v, d, 1e-3) for d in dec])
    lam = B.lam_from_counts(c3, 1e-3, dW)
    lam9 = B.lam_from_counts(c3, 1e-3, 1e-9)
    i = np.searchsorted(v, float(vW))
    mem = min(abs(v[max(i - 1, 0)] / float(vW) - 1), abs(v[min(i, v.size - 1)] / float(vW) - 1)) < 1e-9
    foundW = B.count_window(v, B.T, dW * 1.0000001)
    print(f"  {tag}: syntactic {nsyn:,}, distinct {v.size:,}; Wyler member={mem}; count in 1e-3 window={c3:,} (decoy mean {cd.mean():.0f}); "
          f"lambda at delta_W={dW:.2e}: {lam:.3g}  P(>=1)={B.p_from_lam(lam):.3g};  lambda at 1e-9: {lam9:.3g};  found within delta_W of target: {foundW}")
    return v.size, lam, mem


if not MUTATE:
    nW1, lamW1, memW1 = template(list(range(1, 2001)), "W1 (k in 1..2000)")
    ks2 = sorted({2 ** i * math.factorial(j) for i in range(0, 9) for j in range(1, 9)})
    nW2, lamW2, memW2 = template([float(k) for k in ks2], "W2 (k = 2^i j!, i<=8, j<=8)")
    check("Wyler is a member of W1", bool(memW1)); check("Wyler is a member of W2", bool(memW2))
    RES["A2"] = dict(delta=dW, lamW1=lamW1, lamW2=lamW2, nW1=int(nW1), nW2=int(nW2))
    rho_W = rho_E2
    evW0 = B.evaluate(dW, 1, rho_W)
    print(f"  W0 (all integers forced by a derivation, N=1; rho assumed = E2's {rho_W:.3f}): lambda={evW0['lam']:.2e}, p={evW0['p']:.2e}; c1 {evW0['c1_lookelsewhere']}; precision c2 {evW0['c2_precision']} (miss {dW:.1e} vs {B.BAR_DELTA:.0e}); clears={evW0['clears']}")
    evW2 = B.evaluate(dW, nW2, rho_W)
    check("A2 (Wyler) does not clear the bar even with N=1 (precision fails)", not evW0["clears"])
    check("A2 miss exceeds 1000 sigma_CODATA (exact-formula reading falsified)", dW / sigma_rel > 1000, f"{dW/sigma_rel:.0f} sigma")
else:
    print("  (templates skipped in MUTATE)")

print("\n=== A3: alpha = x^p (x = 2.8485e-122 from AH5), p fitted ===")
p_need = math.log(B.T) / lnx_inv
print(f"  p needed = {p_need:.6f}; AH5 reported 0.017581")
check("A3 p reproduces AH5's 0.017581 to 2e-5", abs(p_need - 0.017581) < 2e-5)
mfp = 1.0 / math.log(B.T)
print("  A fitted real exponent reaches the target with delta = 0 by construction: chance probability 1 (fails c3: one real parameter fitted to one number).")
v57 = math.exp((1 / 57) * lnx_inv); d57 = abs(v57 / B.T - 1)
print(f"  nearest simple rational exponent p = 1/57: alpha^-1 = {v57:.4f}, miss = {d57:.2e} (alpha-miss = |ln alpha| x dp/p: a 2.1e-3 miss in p is a 1.0e-2 miss in alpha; NOT a 1e-3 hit)")
RES["A3"] = dict(p_need=p_need, d57=d57)


def audit_scalar(tag, target, mf, N_list=(6, 12)):
    """Grammar values within rel tol*mf of `target` give alpha-tolerance tol."""
    print(f"  target {target:.6f} (relative tolerance on the grammar value = alpha-tolerance x {mf:.4f})")
    for N in N_list:
        for gn in ("E1", "E2"):
            arr = G[N].E1 if gn == "E1" else G[N].E2
            i = np.searchsorted(arr, target)
            near = arr[max(i - 1, 0):i + 1]
            bestrel = min(abs(near / target - 1))
            best_alpha_delta = bestrel / mf
            row = []
            for tol in (1e-3, 1e-5, 1e-9):
                lam, c, w = lam_win(arr, target, tol * mf)
                found = B.count_window(arr, target, tol * mf)
                row.append(f"tol{tol:.0e}: lam={lam:.3g} found={found}")
            print(f"    {gn}({N}): nearest value gives alpha-miss {best_alpha_delta:.2e}; " + "; ".join(row))
            RES[f"{tag}_{gn}_{N}_best"] = best_alpha_delta


audit_scalar("A3", p_need, mfp)

print("\n=== A4/A5: 1/alpha = a ln(1/x) (a fitted), equivalently 1/alpha = b ln(1/sqrt x), b = 2a ===")
a_need = B.T / lnx_inv
print(f"  a needed = {a_need:.6f} (AH5: 0.489644); b needed = {2*a_need:.6f}")
check("A4 a reproduces AH5's 0.489644 to 1e-5", abs(a_need - 0.489644) < 1e-5)
audit_scalar("A4", a_need, 1.0)
print(f"  natural a = 1/2: 1/alpha = {0.5*lnx_inv:.4f}, miss = {abs(0.5*lnx_inv/B.T-1):.3e} (a 2.1% miss, i.e. {abs(0.5*lnx_inv/B.T-1)/1e-3:.0f} x the 1e-3 hit level);  b = 1: same number")
print(f"  ILLUSTRATIVE (the number m of candidate constants is a free choice; probability is ~0.0092 x m): chance that a fitted a lands within 2.1% of one of m=10 'natural' constants, log-range of a-values ~ ln(10/0.1)=4.6: ~ {10*2*0.021/4.6:.2f}")
RES["A4"] = dict(miss_half=abs(0.5 * lnx_inv / B.T - 1))
check("A4 natural a=1/2 does not hit at 1e-3", abs(0.5 * lnx_inv / B.T - 1) > 1e-3)

print("\n=== A6: AH6 Kaluza-Klein handles, alpha = 4/k^2, k = R/l_P ===")
k_need = 2 * math.sqrt(B.T)
print(f"  k needed = {k_need:.4f} (AH6: 23.41)")
check("A6 k reproduces AH6's 23.41", abs(k_need - 23.41) < 0.01)
handles = {"1": 1.0, "2": 2.0, "sqrt(8pi/3)": math.sqrt(8 * math.pi / 3), "Z": B.Z, "2pi": 2 * math.pi, "4pi": 4 * math.pi, "Z^2": B.Z ** 2}
hd = {}
for n, k in handles.items():
    hd[n] = abs((k * k / 4) / B.T - 1)
for N in (23, 24):
    hd[f"N={N}"] = abs((N * N / 4) / B.T - 1)
best = min(hd, key=hd.get)
print("  misses: " + ", ".join(f"{n}:{d:.2e}" for n, d in hd.items()))
print(f"  best of the 9 declared trials = {best} with alpha-miss {hd[best]:.2e}")
check("A6 no declared handle within 1e-3 (matches AH6 K5)", min(hd.values()) > 1e-3)
audit_scalar("A6", k_need, 0.5)
ev6 = B.evaluate(hd[best], 9, cal["E1_12"]["rho_frac"])
print(f"  9 declared trials at their best miss: lambda={ev6['lam']:.3g}, p={ev6['p']:.3g}: an unremarkable outcome either way")
RES["A6"] = dict(best=best, miss=hd[best])
# a hit at k would be cheap
lamk, ck, wk = lam_win(G[12].E2, k_need, 1e-3 * 0.5)
print(f"  E2(12) expressions within alpha-1e-3 of the KK requirement: expected by chance {lamk:.3g}")

print("\n=== Hypotheses ===")
if not MUTATE:
    print(f"  H3 (4Z^2+3 in E2, chance P at its precision ~1): {'TRUE' if RES['A1_E2_12']['p'] > 0.5 and RES['A1_E2_6']['p'] > 0.5 else 'FALSE'}  (E2(6) p={RES['A1_E2_6']['p']:.3g}, E2(12) p={RES['A1_E2_12']['p']:.3g}; but in the post-hoc template a Z^s+c, p={RES['A1_template']['p']:.3g})")
    print(f"  H4 (Wyler: miss ~6e-7, ~4000 sigma; W1 p={B.p_from_lam(RES['A2']['lamW1']):.3g}, W2 p={B.p_from_lam(RES['A2']['lamW2']):.3g} both >= 0.1; N=1 passes c1, fails precision): "
          f"{'TRUE' if B.p_from_lam(RES['A2']['lamW1']) >= 0.1 and B.p_from_lam(RES['A2']['lamW2']) >= 0.1 else 'FALSE'}")
    pnat = 10 * 2 * abs(0.5 * lnx_inv / B.T - 1) / math.log(100.0)
    print(f"  H5 (fitted real parameter: chance probability 1 by construction (delta=0 always reachable); natural-constant coincidence probability for 10 candidates = {pnat:.3f} > 0.05): {'TRUE' if pnat > 0.05 else 'FALSE'}")
    print(f"  H6 (no declared handle within 1e-3 [{min(hd.values()) > 1e-3}] and E2(12) expects {lamk:.0f} > 100 chance expressions at the KK requirement): {'TRUE' if (min(hd.values()) > 1e-3 and lamk > 100) else 'FALSE'}")

json_out = dict(RES=RES)
import json
json.dump(json_out, open("d2_results_MUTATE.json" if MUTATE else "d2_results.json", "w"), indent=1, default=float)
print("\nFAILED:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
