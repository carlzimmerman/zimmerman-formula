#!/usr/bin/env python3
"""q6_blandino_bleger_checks.py -- lane Q4: (B) replication of Blandino's 'quantum expectation' model (Zenodo 19836013) and (G) checks on Bleger's closed form (Zenodo 19702883).
Imports lane D's bar_lib unmodified (constants only). Third-party programs are downloaded to $Q4_CACHE (default: session scratchpad) and hashed, not copied.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 q6_blandino_bleger_checks.py            -> exit 0 iff the flag vector equals the one recorded in Amendment 6 of Q4_PREREGISTRATION.md:
              (H6 printed mean NOT reproduced: False; H9 printed P(q=1) not the stated distribution's: True; G1 Bleger script exit 0 and closed form reproduced: True;
              G2 >= 1 hit simpler than Bleger's: True; b4a S(K=10) within the bar's miss: True; b4c at most two of five CODATA values have K in (9,10): True)
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 q6_blandino_bleger_checks.py --mutate   -> the printed mean is replaced by 137.0359990; H6 becomes True; vector mismatch; exit 1
"""
import sys, os, math, hashlib, subprocess, urllib.request, zipfile, io, re
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import numpy as np
import mpmath as mp
import bar_lib as B
mp.mp.dps = 40
MUTATE = "--mutate" in sys.argv
CACHE = os.environ.get("Q4_CACHE", "./q4_cache")
os.makedirs(CACHE, exist_ok=True)
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)
T = mp.mpf("137.035999177")

def fetch(name, url):
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8"}), timeout=180) as r:
            open(path, "wb").write(r.read())
    P("  fetched %-22s sha256 %s" % (name, hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]))
    return path

# ------------------------------------------------------------------ B1
pi = mp.pi
A = 4 * pi ** 3 + pi ** 2 + pi
def S_of_K(K):
    return A - 1 / (24 * A) - 1 / (A ** 2 * pi ** 2 * K)
P("== B1: K that reproduces a given alpha^-1 in Blandino's formula ==")
Kfit = mp.findroot(lambda K: S_of_K(K) - T, mp.mpf("9.93"))
P("  A(pi) = %s (miss vs T = %s) ; K_fit(CODATA 2022) = %s (paper: 9.9327912864)" % (mp.nstr(A, 14), mp.nstr(abs(A / T - 1), 3), mp.nstr(Kfit, 12)))
def cf(x, n):
    q = []
    for _ in range(n):
        a = int(mp.floor(x)); q.append(a); x = x - a
        if x == 0: break
        x = 1 / x
    return q
F = 10 - Kfit
qs = cf(1 / F, 12)
P("  F = 10 - K = %s ; continued fraction of F: [0; %s]" % (mp.nstr(F, 12), ", ".join(map(str, qs))))
Kcf = 10 - 1 / (14 + 1 / (1 + 1 / (7 + 1 / (3 + 1 / (1 + mp.mpf(1) / 3)))))
P("  the paper's six-quotient K = %s ; S(K_cf) = %s ; miss vs T = %s (sigma_CODATA %s)" % (mp.nstr(Kcf, 12), mp.nstr(S_of_K(Kcf), 14), mp.nstr(abs(S_of_K(Kcf) / T - 1), 3), mp.nstr(abs(S_of_K(Kcf) / T - 1) / mp.mpf("1.6e-10"), 3)))
P("  information: K_fit is ONE real fitted to CODATA (10 significant digits ~ 33 bits); the quotients [14,1,7,3,1,3] are the same number written as a continued fraction (six integers <= 14: ~ 6*log2(45)= 33 bits available): no evidence beyond the fit")

# ------------------------------------------------------------------ B2
P("== B2: Monte Carlo replication of the stated model (numpy float64, 2,000,000 draws, depth 20) ==")
rng = np.random.default_rng(12345)
def simulate(E_int, n=2_000_000, depth=20, qmax=45):
    q = np.arange(1, qmax + 1)
    w = np.exp(-q / (2.0 * E_int)); p = w / w.sum()
    draws = rng.choice(q, size=(n, depth), p=p).astype(np.float64)
    f = draws[:, -1].copy()
    for j in range(depth - 2, -1, -1):
        f = draws[:, j] + 1.0 / f
    Fv = 1.0 / f
    K = 10.0 - Fv
    Af = float(A)
    S = Af - 1.0 / (24.0 * Af) - 1.0 / (Af ** 2 * math.pi ** 2 * K)
    p1 = float((draws[:, 0] == 1).mean())
    return S, p1, p
pub_mean, pub_std, pub_p1 = (137.0359990 if MUTATE else 137.035999167828), 1.40e-8, 0.1815
E = 5.0
S, p1, pvec = simulate(E)
P("  E_int = %.1f (P(q) ~ exp(-q/%.1f)): mean <S> = %.12f ; std = %.3e ; P(q=1) = %.4f ; P(q=1) analytic = %.4f" % (E, 2 * E, S.mean(), S.std(), p1, pvec[0]))
P("  printed: mean = %.12f ; std = %.2e ; P(q=1) = %.4f" % (pub_mean, pub_std, pub_p1))
d_mean = S.mean() - pub_mean
P("  replicated mean - printed mean = %.3e (%.3g x the CODATA 2.1e-8) ; replicated mean - CODATA 2022 = %.3e" % (d_mean, abs(d_mean) / 2.1e-8, S.mean() - float(T)))
h6 = abs(d_mean) > 5e-8
h9 = abs(p1 - pub_p1) > 0.05
P("  H6 the printed mean is NOT reproduced (|diff| > 5e-8): %s ; H9 the printed P(q=1) = 18.15%% is NOT the stated distribution's (|diff| > 5 points): %s" % (h6, h9))
P("  scan of the printed insensitivity claim (mean insensitive to E_int in [3,10]):")
means = {}
for e in (2.5, 3.0, 5.0, 10.0):
    s_, p1_, _ = simulate(e, n=500_000)
    means[e] = s_.mean()
    P("     E_int = %4.1f : mean <S> = %.12f ; P(q=1) = %.4f ; mean - CODATA = %.3e" % (e, s_.mean(), p1_, s_.mean() - float(T)))
spread = max(means[e] for e in (3.0, 5.0, 10.0)) - min(means[e] for e in (3.0, 5.0, 10.0))
P("  spread of the mean over E_int in {3, 5, 10} = %.3e (CODATA 2022 sigma = 2.1e-8): insensitivity %s" % (spread, "HOLDS" if spread < 2.1e-8 else "FAILS"))

# ------------------------------------------------------------------ B3
P("== B3/B4: what K does each CODATA value need, and how sensitive is S to K? ==")
cc = 1 / (A ** 2 * pi ** 2)
base = A - 1 / (24 * A)
P("  A - 1/(24A) = %s (miss vs T = %s = %s sigma_CODATA) ; c = 1/(A^2 pi^2) = %s" % (mp.nstr(base, 14), mp.nstr(abs(base / T - 1), 3), mp.nstr(abs(base / T - 1) / mp.mpf("1.6e-10"), 3), mp.nstr(cc, 8)))
dSdK = cc / Kfit ** 2
P("  dS/dK at K_fit = c/K^2 = %s per unit K ; window of K within 1 sigma_CODATA (2.1e-8 abs): +-%s ; within the bar (6.85e-8 abs): +-%s" % (mp.nstr(dSdK, 5), mp.nstr(mp.mpf("2.1e-8") / dSdK, 3), mp.nstr(mp.mpf("6.85e-8") / dSdK, 3)))
for Kv in (10, mp.mpf("9.5"), 9):
    Sv = S_of_K(mp.mpf(Kv))
    P("  S(K = %s) = %s ; miss vs T = %s (%s sigma_CODATA)%s" % (Kv, mp.nstr(Sv, 14), mp.nstr(abs(Sv / T - 1), 3), mp.nstr(abs(Sv / T - 1) / mp.mpf("1.6e-10"), 3), "  <- no continued fraction at all (F = 0)" if Kv == 10 else ""))
b4a = abs(S_of_K(mp.mpf(10)) / T - 1) <= mp.mpf("5e-10")
codata = {2006: "137.035999679", 2010: "137.035999074", 2014: "137.035999139", 2018: "137.035999084", 2022: "137.035999177"}
P("  (the five CODATA values are RECALLED from memory, not read from a source in this lane)")
inside = 0
allq = []
for y, v in codata.items():
    den = base - mp.mpf(v)
    Ky = cc / den if den > 0 else None
    if Ky is not None and 9 < Ky < 10:
        inside += 1
        qy = cf(1 / (10 - Ky), 8); allq += qy
        P("  %d : K needed = %s (inside (9,10)) ; F = 10 - K has quotients [0; %s]" % (y, mp.nstr(Ky, 10), ", ".join(map(str, qy))))
    else:
        P("  %d : K needed = %s (OUTSIDE the operator domain (9,10): the model cannot represent this value with any single continued fraction)" % (y, mp.nstr(Ky, 8) if Ky is not None else "undefined"))
b4c = inside <= 2
P("  CODATA values with K inside (9,10): %d of 5" % inside)
p_le45 = 1 - math.log2(1 + 1 / 46.0)
P("  Gauss-Kuzmin: P(a quotient > 45) = %.4f ; P(all 8 quotients <= 45) = %.3f ; for the paper's claim over five values (40 quotients) = %.3f" % (1 - p_le45, p_le45 ** 8, p_le45 ** 40))

# ------------------------------------------------------------------ G1
P("== G1: Bleger's script and closed form ==")
zp = fetch("bleger_pkg.zip", "https://zenodo.org/api/records/19702883/files/Alpha%20Inverse%20Paper%20v1.zip/content")
z = zipfile.ZipFile(zp)
name = [n for n in z.namelist() if n.endswith("scripts/alpha_verification.py") and "__MACOSX" not in n][0]
pth = os.path.join(CACHE, "bleger_alpha_verification.py"); open(pth, "wb").write(z.read(name))
r = subprocess.run([sys.executable, pth], capture_output=True, text=True, timeout=120, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
m = re.search(r"closed form\) = ([0-9.]+)", r.stdout)
P("  script exit %d ; printed closed form = %s ; lines printed = %d" % (r.returncode, m.group(1) if m else None, len(r.stdout.splitlines())))
R = mp.log(2 + mp.sqrt(3))
val = mp.mpf(19596) / 143 + 5 * R / (6370 - 2 * R)
P("  independent mpmath: 19596/143 + 5R/(6370 - 2R) = %s ; miss vs T = %s = %s sigma_CODATA (rel 1.6e-10)" % (mp.nstr(val, 15), mp.nstr(abs(val / T - 1), 3), mp.nstr(abs(val / T - 1) / mp.mpf("1.6e-10"), 3)))
Lval = mp.dirichlet(1, [0, 1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 1])
P("  L(1, chi_12) = %s ; R/sqrt(3) = %s ; identity holds to %s" % (mp.nstr(Lval, 15), mp.nstr(R / mp.sqrt(3), 15), mp.nstr(abs(Lval - R / mp.sqrt(3)), 3)))
g1 = (r.returncode == 0) and m and abs(mp.mpf(m.group(1)) - val) < mp.mpf("1e-9")

# ------------------------------------------------------------------ G2
P("== G2: how many formulas of Bleger's shape hit the bar's miss? (A/B + R/C + c3 (R/C)^2, B <= 300, C <= 3000, c3 = p/q in [0,1], q <= 40) ==")
Rf = float(R); Tf = float(T)
fracs = sorted({(p, q) for q in range(1, 41) for p in range(0, q + 1) if math.gcd(p, q) == 1 or p == 0 and q == 1})
Bs = np.arange(1, 301, dtype=np.float64)[:, None]
Cs = np.arange(1, 3001, dtype=np.float64)[None, :]
tol_abs = 5e-10 * Tf
hits = []
tot_expected = 0.0
for (p, q) in fracs:
    c3 = p / q
    rest = Tf - Rf / Cs - c3 * (Rf / Cs) ** 2
    Aint = np.rint(rest * Bs)
    v = Aint / Bs + Rf / Cs + c3 * (Rf / Cs) ** 2
    ok = np.abs(v - Tf) <= tol_abs
    idx = np.argwhere(ok)
    for i, j in idx:
        hits.append((int(Bs[i, 0]), int(Cs[0, j]), p, q, int(Aint[i, j])))
    tot_expected += float((2 * tol_abs * Bs).sum() * Cs.size)
n_comb = len(fracs) * Bs.size * Cs.size
P("  fractions p/q with q <= 40 in [0,1]: %d ; combinations (B, C, c3): %.3g" % (len(fracs), n_comb))
P("  hits within 5e-10 of T: %d ; expected by density (2*tol*B per combination): %.0f" % (len(hits), tot_expected))
simpler = [h for h in hits if h[0] <= 143 and h[1] <= 1274 and h[3] <= 5]
P("  hits with B <= 143, C <= 1274, q <= 5 (simpler than or equal to Bleger's (143, 1274, 2/5) in every coordinate): %d" % len(simpler))
P("  examples (B, C, p/q, A): " + "; ".join("(%d, %d, %d/%d, %d)" % h for h in sorted(simpler, key=lambda h: (h[0] + h[1] + h[3]))[:8]))
bl = [h for h in hits if (h[0], h[1], h[2], h[3]) == (143, 1274, 2, 5)]
P("  Bleger's own (143, 1274, 2/5, 19596) among the hits: %s" % bool(bl))
g2 = len(simpler) >= 1
c3sweep = {(p, q): abs(float(mp.mpf(19596) / 143 + R / 1274 + mp.mpf(p) / q * (R / 1274) ** 2) / Tf - 1) for (p, q) in ((0, 1), (1, 3), (3, 8), (11, 28), (2, 5), (1, 2))}
P("  the source's own c3 sweep, miss vs T (relative): " + "; ".join("%d/%d: %.2e" % (p, q, d) for (p, q), d in c3sweep.items()))

recorded = (False, True, True, True, True, True)
flags = (bool(h6), bool(h9), bool(g1), bool(g2), bool(b4a), bool(b4c))
ok = flags == recorded
if MUTATE:
    P("MUTATE: flags %s vs recorded %s (a live control mismatches here); exit %d" % (flags, recorded, 0 if ok else 1))
    open(os.path.join(HERE, "q6_blandino_bleger_checks_MUTATE.out"), "w").write("\n".join(out) + "\n")
    sys.exit(0 if ok else 1)
P("flags (H6, H9, G1, G2, b4a, b4c) = %s ; recorded %s ; match %s" % (flags, recorded, ok))
open(os.path.join(HERE, "q6_blandino_bleger_checks.out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if ok else 1)
