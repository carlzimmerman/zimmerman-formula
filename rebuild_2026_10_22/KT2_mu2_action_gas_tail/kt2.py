#!/usr/bin/env python3
"""KT2: Part A, auxiliary action for mu_n; Part B, tail exponent on gas-dominated SPARC points. See FROZEN_CRITERIA.md."""
import glob, json, math, os, sys
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "../../real_research/data/sparc_data")
MUTATE = os.environ.get("KT2_MUTATE") == "1"
kpc, KMS = 3.0857e19, 1.0e3
c_l, G = 2.99792458e8, 6.674e-11
H0 = 67.4 * 1000 / 3.0857e22
rho_crit = 3 * H0**2 / (8 * math.pi * G)
S = {"rho_DE": c_l * math.sqrt(G * 0.685 * rho_crit), "rho_crit": c_l * math.sqrt(G * rho_crit)}
NS = np.round(np.arange(0.8, 4.0001, 0.1), 3)
PS = np.round(np.arange(0.5, 8.0001, 0.25), 3)
ND = 1000


def part_a():
    chi, g, s, b, Y = sp.symbols("chi g s b Y", positive=True)
    ok = {}
    for n in (1, 2, 3, 4):
        dU = n * (1 - chi) ** 2 * chi ** (n - 3)
        # A1: d/dchi[(1-chi^n) g^2 + (s/b)^2 U] = 0 at chi = 1/(1 + b g/s)
        eom = (-n * chi ** (n - 1) * g**2 + (s / b) ** 2 * dU).subs(chi, 1 / (1 + b * g / s))
        ok[f"A1_n{n}"] = sp.simplify(eom) == 0
        mu = (1 - chi**n).subs(chi, 1 / (1 + b * Y))
        ok[f"A2_n{n}"] = sp.simplify(mu - (1 - (1 + b * Y) ** (-n))) == 0
        slope = sp.diff(mu, Y).subs(Y, 0)
        ok[f"A3_slope_n{n}"] = sp.simplify(slope - n * b) == 0
        tail = sp.limit((1 - mu) * Y**n, Y, sp.oo)
        ok[f"A3_tail_n{n}"] = sp.simplify(tail - b ** (-n)) == 0
        U = sp.integrate(sp.expand(dU), chi)
        print(f"n={n}: U_n = {U}; log term: {U.has(sp.log)}; slope {slope}; kappa = 1/({n}*b)")
        ok[f"A4_log_n{n}"] = U.has(sp.log) == (n in (1, 2))
    U2 = sp.integrate(sp.expand(2 * (1 - chi) ** 2 / chi), chi)
    ok["A4_U2"] = sp.simplify(U2 - (2 * sp.log(chi) - 4 * chi + chi**2)) == 0

    # A5: scaling
    Gs, r, cs, lg, lr, lc = sp.symbols("G rho c l_G l_r l_c", positive=True)
    sv = cs * sp.sqrt(Gs * r)
    a0 = sv / (2 * b)
    k = sp.simplify(a0 / sv)
    k2 = sp.simplify(a0.subs({Gs: lg * Gs, r: lr * r, cs: lc * cs}, simultaneous=True) / (lc * cs * sp.sqrt(lg * Gs * lr * r)))
    ok["A5_invariant"] = sp.simplify(k - k2) == 0
    ok["A5_follows_b"] = sp.simplify(k - 1 / (2 * b)) == 0
    print("A5 kappa =", k)

    # A6: budget. int_0^Yc w d(g^2) in s^2 units at n = 2, with Z = b Y; offset = 8 pi G rho c^2 / c^2 -> 8 pi s^2
    Z, Zc = sp.symbols("Z Z_c", positive=True)
    I = sp.integrate(2 * Z / (1 + Z) ** 2, (Z, 0, Zc)) / b**2
    I_expected = 2 * (sp.log(1 + Zc) + 1 / (1 + Zc) - 1) / b**2
    ok["A6_integral"] = sp.simplify(I - I_expected) == 0
    # I s^2 = 8 pi s^2 => (ln(1+Z)+1/(1+Z)-1) = 4 pi b^2 = pi/kappa^2
    from scipy.optimize import brentq
    f = lambda lz, kap: math.log1p(math.exp(lz)) + 1 / (1 + math.exp(lz)) - 1 - math.pi / kap**2
    out = {}
    for kap in (0.5, 0.4607, 0.482, 0.227, 0.607):
        lz = brentq(f, 0, 400, args=(kap,))
        bb = 1 / (2 * kap)
        out[str(kap)] = {"ln_Z": lz, "log10_Yc": (lz - math.log(bb)) / math.log(10)}
        print(f"A6 kappa {kap}: b {bb:.4f}, ln(1+bYc) ~ {lz:.3f}, Y_c = 10^{out[str(kap)]['log10_Yc']:.2f}, g_c = {math.exp(lz)/bb*S['rho_DE']:.3e} m/s^2")
    return ok, out


def load(fu=1.0):
    gb, go, gal, fg = [], [], [], []
    i = 0
    for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(fn, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, j] for j in range(6))
        m = (R > 0) & (Vo > 0) & (eV > 0) & (eV / Vo < 0.10)
        if m.sum() < 3:
            continue
        R, Vo, Vg, Vd, Vb = R[m], Vo[m], Vg[m], Vd[m], Vb[m]
        G2 = Vg * np.abs(Vg)
        B1 = G2 + 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb)
        Vb2 = G2 + fu * 0.5 * Vd * np.abs(Vd) + fu * 0.7 * Vb * np.abs(Vb)
        ok = (B1 > 0) & (Vb2 > 0)
        if ok.sum() < 3:
            continue
        r = R[ok] * kpc
        gb.append(Vb2[ok] * KMS**2 / r)
        go.append(Vo[ok] ** 2 * KMS**2 / r)
        fg.append(G2[ok] / B1[ok])
        gal.append(np.full(ok.sum(), i))
        i += 1
    return map(np.concatenate, (gb, go, gal, fg))


def select(gb, go, gal, fg):
    k = fg >= 0.5
    keep = np.zeros_like(k)
    for i in np.unique(gal[k]):
        w = k & (gal == i)
        if w.sum() >= 3:
            keep |= w
    gal2 = np.unique(gal[keep], return_inverse=True)[1]
    return gb[keep], go[keep], gal2


def g_pred(gb, s, n, p, it=70):
    lo = gb.copy()
    hi = gb * 10 + np.sqrt(gb * s / n) * 10 + 1e-13
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        f = mid * (1 - (1 + n * mid / s / p) ** (-p)) - gb
        lo = np.where(f < 0, mid, lo)
        hi = np.where(f < 0, hi, mid)
    return 0.5 * (lo + hi)


def table(gb, go, gal, s):
    ng = gal.max() + 1
    cnt = np.bincount(gal, minlength=ng)
    T = np.zeros((len(NS), len(PS), ng))
    lg = np.log10(go)
    for i, n in enumerate(NS):
        for j, p in enumerate(PS):
            r = lg - np.log10(g_pred(gb, s, n, p))
            T[i, j] = np.bincount(gal, r**2, minlength=ng) / cnt
    return T


def best(T, w=None):
    M = T.mean(axis=2) if w is None else (T * w).sum(axis=2) / w.sum()
    i, j = np.unravel_index(np.argmin(M), M.shape)
    return i, j, M[i, j]


def boot(T, seed=20261102):
    rng = np.random.default_rng(seed)
    ng = T.shape[2]
    out = np.zeros((ND, 2))
    for d in range(ND):
        w = np.bincount(rng.integers(0, ng, ng), minlength=ng).astype(float)
        i, j, _ = best(T, w)
        out[d] = NS[i], PS[j]
    return out


def q(x, a, b):
    return [float(np.percentile(x, a)), float(np.percentile(x, b))]


def label(B, n3):
    if n3 < 30:
        return "NO LEVERAGE"
    n95, p95, d95 = q(B[:, 0], 2.5, 97.5), q(B[:, 1], 2.5, 97.5), q(B[:, 0] - B[:, 1], 2.5, 97.5)
    if p95[0] <= PS[0] or p95[1] >= PS[-1] or (p95[0] <= 1 and p95[1] >= 4):
        return "TAIL NOT MEASURED"
    if not d95[0] <= 0 <= d95[1]:
        return "INTERLOCK BROKEN"
    if n95[0] <= 2 <= n95[1] and p95[0] <= 2 <= p95[1]:
        return "INTERLOCK HOLDS AT 2"
    return "INTERLOCK HOLDS, NOT AT 2"


def row(tag, gb, go, gal, s):
    Y = go / s
    n3, n10 = int((Y >= 3).sum()), int((Y >= 10).sum())
    T = table(gb, go, gal, s)
    B = boot(T)
    i, j, m = best(T)
    r = dict(galaxies=int(gal.max() + 1), points=len(gb), n3=n3, n10=n10, Ymax=float(Y.max()), n=float(NS[i]), p=float(PS[j]),
             rms=math.sqrt(m), n68=q(B[:, 0], 16, 84), n95=q(B[:, 0], 2.5, 97.5), p68=q(B[:, 1], 16, 84), p95=q(B[:, 1], 2.5, 97.5),
             d95=q(B[:, 0] - B[:, 1], 2.5, 97.5), label=label(B, n3))
    print(f"{tag}: {r['galaxies']} gal, {r['points']} pts, Y>=3 {n3}, Y>=10 {n10}, Ymax {r['Ymax']:.1f}; best n {r['n']} p {r['p']} rms {r['rms']:.4f}")
    print(f"   n 68% {r['n68']} 95% {r['n95']}; p 68% {r['p68']} 95% {r['p95']}; n-p 95% {[round(x,2) for x in r['d95']]}; {r['label']}")
    return r


res = {}
gb, go, gal, fg = load()
sb, so, sg = select(gb, go, gal, fg)
if MUTATE:
    rng = np.random.default_rng(7)
    s0 = S["rho_DE"]
    r0, rm = math.sqrt(best(table(sb, so, sg, s0))[2]), math.sqrt(best(table(sb, rng.permutation(so), sg, s0))[2])
    print(f"real best rms {r0:.4f}; shuffled best rms {rm:.4f}; {'MUTATE bites' if rm - r0 >= 0.1 else 'MUTATE FAILED'}")
    json.dump({"real": r0, "shuffled": rm}, open(os.path.join(HERE, "kt2_MUTATE.json"), "w"), indent=1)
    sys.exit(1)

print("PART A")
ok, budget = part_a()
print({k: bool(v) for k, v in ok.items()})
print("Part A all pass:", all(ok.values()))
res["A"] = {"checks": {k: bool(v) for k, v in ok.items()}, "budget": budget}

print("\nPART B")
s0 = S["rho_DE"]
scat = np.log10(so) - np.log10(g_pred(sb, s0, 2.0, 2.0))
pl = True
for pp in (2.0, 4.0):
    mock = g_pred(sb, s0, 2.0, pp) * 10 ** (scat - scat.mean())
    Bp = boot(table(sb, mock, sg, s0))
    h = q(Bp[:, 1], 16, 84)
    hit = h[0] <= pp <= h[1]
    pl &= hit
    print(f"PLANTED p={pp}: p 68% {h}, n 68% {q(Bp[:,0],16,84)} {'PASS' if hit else 'FAIL'}")
print("Planted:", "PASS" if pl else "FAIL, reads NO VERDICT")
res["planted_ok"] = bool(pl)
for f, s in S.items():
    res[f] = row(f"PRIMARY {f}", sb, so, sg, s)
for fu in (0.8, 1.25):
    a, b, c, d = load(fu)
    k = select(a, b, c, d)
    for f, s in S.items():
        res[f"U{fu}_{f}"] = row(f"Upsilon x{fu} {f}", *k, s)
json.dump(res, open(os.path.join(HERE, "kt2.json"), "w"), indent=1)
sys.exit(0 if pl and all(ok.values()) else 2)
