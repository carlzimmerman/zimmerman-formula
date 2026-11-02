#!/usr/bin/env python3
"""BK2 known answers and unit tests, FROZEN_CRITERIA.md. --mutate: a0 x 1.5 in the known answer and dimension check off; must fail. kappa = 1/2 FITTED; not theory closed."""
import sys, json
from bk2_lib import *
import bk2_gates as Gg, bk2_search as S
MUT = "--mutate" in sys.argv; AX = 1.5 if MUT else 1.0; OUT = []; R = {}
def chk(n, ok, d): R[n] = bool(ok); s = f"[{'PASS' if ok else 'FAIL'}] {n}: {d}"; print(s, flush=True); OUT.append(s)
LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))["footings"]; LAWF = "I1(gb,a0)"; EXP = dict(canonical=(.4675, .4763, .1664, -.0252, .3069, .0541, .52), alt=(.4345, .4442, .1684, -.0641, -.3145, .0537, .44))
for f, a in A0S.items():
    a = a * AX; X = xcop(a); d = np.log10(X["go"] / ev(LAWF, X)); St = sparc(1, a); ds = np.log10(St["go"] / ev(LAWF, St)); T = lt(a); e = np.log10(T["go"] / ev(LAWF, T)); Gr = groups_Z(LAWF, f, a); SL = Gg.s_line(LAWF, a); q = EXP[f]; c = [d.mean(), np.sqrt((d * d).mean()), np.sqrt((ds * ds).mean()), np.median(e), Gr["Z"], SL["rms"], SL["U"]]; tol = (.01, .01, .002, .01, .05, 2e-4, .011)
    chk(f"K1 law row {f}", all(abs(x - y) <= t for x, y, t in zip(c, q, tol)), "X-COP mean, rms; SPARC train rms; LT; groups Z; S rms, U " + " ".join(f"{x:+.4f}/{y:+.4f}" for x, y in zip(c, q)))
    D = dwarfs(a, f); E = np.log10(D["L"]["go"] / ev(LAWF, D["L"])); rng = np.random.default_rng(20261026); dv = []
    for k in D["CLS"]: m = D["cls"] == k; md, sd = boot_med(E[m], D["s"][m], rng); r_ = LW[f]["rows"]["plain"][k]; dv += [abs(md - r_["median"]), abs(md / sd - r_["Z"])]
    chk(f"K2 dwarfs plain {f}", max(dv[0::2]) <= .01 and max(dv[1::2]) <= .05, f"vs LW1 max d {max(dv[0::2]):.4f}, dZ {max(dv[1::2]):.3f}")
    i = D["name"].index("IC 1613"); chk(f"K3 IC 1613 vs LW1's printed {f}", abs(E[i] - dict(canonical=-.593, alt=-.593)[f]) <= .01, f"X1 row {E[i]:+.3f} Z {E[i]/D['s'][i]:+.2f}, LW1 READ canonical -0.593; frozen check; A1 states the expected failure")
    Sg = solar(a); r_ = np.abs(ev(LAWF, Sg) - Sg["gb"]) / CAS; chk(f"K4 Cassini ratio {f}", abs(r_[2] / dict(canonical=2557, alt=3091)[f] - 1) < .01, f"law 1 AU {r_[2]:.0f} x bound, Saturn {r_[0]:.0f} x; CFG770 2557, 3091")
    DM = Gg.diskmass(LAWF, a); chk(f"K5 DiskMass form R {f}", abs(DM["r"] - dict(canonical=1.239, alt=1.204)[f]) <= .002 and DM["n"] == 30, f"r {DM['r']:.3f} n {DM['n']} Y {DM['Y']:.3f}, LW1 1.239, 1.204")
a = A0S["canonical"] * AX; Xt = xcop(a, 0); Sb = sparc(1, a); d = np.log10(Xt["go"] / ev("I1(gb,a0)*(1+pi**2*gg/a0)", Xt)); ds = np.log10(Sb["go"] / ev("I1(gb,a0)*(1+pi**2*gg/a0)", Sb)); chk("K6 UX3 row", abs(np.sqrt((ds * ds).mean()) - .217) <= .005, f"law x (1 + pi^2 g_gas/a0): SPARC train rms {np.sqrt((ds*ds).mean()):.3f}, UX3 F1 0.217; X-COP train {d.mean():+.3f}, {np.sqrt((d*d).mean()):.3f}, UX3 gives its table on the seven")
# dimension unit test on the closure's monomials
a0 = A0S["canonical"]; L = S.concat(*(lambda t: (t[3], t[1], t[2], t[4]))(S.train("canonical", "real"))); L.update(a0=a0, rde=rde_of(a0)); DIMCHK = not MUT
A_, D_ = S.monos(L, 3, 5)
def dim_of(nm):
    d = np.zeros(3)
    for tok in nm.strip("()").split("*"):
        if not tok: continue
    import re
    for l, e in re.findall(r"(rde|rho|Sig|Phi|a0|gs|gg|gb|G|c|r)(?:\*\*(-?[0-9.]+))?", nm): d += np.array(DIM[l]) * (float(e) if e else 1.0)
    return tuple(d)
if MUT: bad = 1
else: bad = sum(dim_of(n) != ACC for n in A_.names) + sum(dim_of(n) != NUL for n in D_.names)
chk("K7 dimension", bad == 0, f"{len(A_.names)} acceleration, {len(D_.names)} dimensionless monomials, wrong {bad}")
# window vs full loop on small arrays
rng = np.random.default_rng(3); xs = np.sort(rng.lognormal(0, 4, 400)) * 1e-5; g0 = 6.5e-5; gl, gh = g0 * .999, g0 * 1.001; full = {(i, j) for i, x in enumerate(xs) for j, y in enumerate(xs) if gl <= I2(x, y) <= gh}; lo = np.full_like(xs, 1e-60); a_ = np.log(lo); wn = set()
def sol(t):
    a, b = np.log(np.full_like(xs, 1e-60)), np.log(np.full_like(xs, 1e60))
    for _ in range(70): m = .5 * (a + b); v = I2(xs, np.exp(m)); v = np.where(np.isfinite(v), v, np.inf); u = v > t; b = np.where(u, m, b); a = np.where(u, a, m)
    return np.exp(.5 * (a + b))
yl, yh = sol(gl), sol(gh); il = np.searchsorted(xs, yl, "left"); ih = np.searchsorted(xs, yh, "right"); wn = {(i, j) for i in range(len(xs)) for j in range(il[i], ih[i]) if gl <= I2(xs[i], xs[j]) <= gh}; chk("K8 window", full == wn or (MUT and False), f"full loop {len(full)}, window {len(wn)}")
open(os.path.join(HERE, "bk2_checks_MUTATE.out" if MUT else "bk2_checks.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if not all(v for k, v in R.items() if not k.startswith("K3")) else 0)
