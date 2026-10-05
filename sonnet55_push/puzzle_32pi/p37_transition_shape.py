"""p37: SPARC measurement of the transition sharpness n in nu_n(y) = (1 + y^-n)^(1/(2n))  (n = 1: the framework kernel sqrt(1 + 1/y)); a0 profiled.
Same deep limit for every n; tail nu - 1 ~ y^-n/(2n) (planets need n >~ 1.5; the vacuum integral is finite only for n > 2). RAR (McGaugh) shown for reference.
Lane V machinery: (i) Upsilon free (175, sigma_int 0.0808), (ii) MLS16 cuts + Upsilon 0.5/0.7 (153, 0.11), (iii) gas-dominated T >= 8 Upsilon free (Upsilon-insensitive).
Delta chi2 relative to n = 1, independent points (lane V's crude clustering deflation ~x18 quoted). Reports best n, its Delta chi2 = 4 range, and a0 at best n.
Run: python3 p37_transition_shape.py  |  MUTATE=1: the family exponent replaced by 1/n (blunter for n > 1): the best n must move (check B fails)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def IFn(n):
    m = (1 / n) if MUTATE else n
    return lambda gb, a: gb * (1 + (gb / a)**(-m))**(1 / (2 * m))
check("0 n = 1 is exactly the framework kernel", all(abs(IFn(1)(np.array([x]), 1.0)[0] - V.IF_alpha1(np.array([x]), 1.0)[0]) < 1e-12 for x in (0.01, 1, 50)))
gals = V.load_sparc()
A = np.exp(np.linspace(math.log(0.4e-10), math.log(2.6e-10), 61))
N = [0.7, 0.85, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0]
samples = {"Upsilon free (all)": (gals, {}, 0.0808),
           "MLS16 cuts, Upsilon 0.5": ([g for g in gals if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30], dict(ufixed=0.5), 0.11),
           "gas-dominated T>=8, Ups free": ([g for g in gals if g["T"] is not None and g["T"] >= 8], {}, 0.0808)}
best = {}
for lab, (sel, kw, sint) in samples.items():
    out = {}
    for n in N:
        ch = V.Profile(sel, IFn(n), **kw).scan(A, sint); i = int(np.argmin(ch))
        out[n] = (ch[i], V.parabola_min(A, ch, k=6)[0])
    rar = V.Profile(sel, V.IF_rar, **kw).scan(A, sint); r_ch = rar.min()
    c1 = out[1.0][0]
    nb = min(out, key=lambda n: out[n][0])
    rng = [n for n in N if out[n][0] - out[nb][0] < 4]
    best[lab] = (nb, out[nb][0] - c1, out[nb][1], min(rng), max(rng))
    print(f"   {lab:30s} ({len(sel)} gal): " + "  ".join(f"n={n:g}:{out[n][0]-c1:+.0f}" for n in N) + f"   | RAR {r_ch - c1:+.0f}")
    print(f"      best n = {nb:g} (Delta chi2 vs n=1: {out[nb][0]-c1:+.1f}, ~{(out[nb][0]-c1)/18:+.1f} deflated); Delta chi2<4 range n in [{min(rng):g}, {max(rng):g}];"
          f" a0(best n) = {out[nb][1]:.3e} vs a0(n=1) = {out[1.0][1]:.3e}")
nbs = [b[0] for b in best.values()]
check("A every sample prefers a SHARPER transition than the framework kernel (best n > 1)", all(n > 1 for n in nbs))
check("B the preferred sharpness is consistent across samples (best n within [1.5, 4] in all three)", all(1.5 <= n <= 4 for n in nbs))
check("C at the preferred n the tail is planet-safe (n >= 1.5)", all(n >= 1.5 for n in nbs))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
