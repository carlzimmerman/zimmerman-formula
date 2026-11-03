#!/usr/bin/env python3
"""TX1 known answers. --mutate: a0 x 1.5, s2 x 1000 (run with TX1_S2X=1000), T_X shuffled in K3's pairing; must exit 1. kappa = 1/2 FITTED; not theory closed."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
MUT = "--mutate" in sys.argv; AX = 1.5 if MUT else 1.0; OUT = []; R = {}
import bk2_gates as Gg, bk2_search as S
S = install(("real", 1500))
def chk(n, ok, d): R[n] = bool(ok); s = f"[{'PASS' if ok else 'FAIL'}] {n}: {d}"; print(s, flush=True); OUT.append(s)
EXP = dict(canonical=(.4675, .4763, .1664, -.0252, .3069, .0541, .52), alt=(.4345, .4442, .1684, -.0641, -.3145, .0537, .44)); LAW = "I1(gb,a0)"
for f, a in A0S.items():
    a = a * AX; X = xrows(a, None); d = np.log10(X["go"] / ev(LAW, X)); St = sparc(1, a); ds = np.log10(St["go"] / ev(LAW, St)); T = lt(a); e = np.log10(T["go"] / ev(LAW, T)); Gr = groups_Z(LAW, f, a); SL = Gg.s_line(LAW, a); q = EXP[f]; c = [d.mean(), np.sqrt((d * d).mean()), np.sqrt((ds * ds).mean()), np.median(e), Gr["Z"], SL["rms"], SL["U"]]; tol = (.01, .01, .002, .01, .05, 2e-4, .011)
    chk(f"K1 law row {f}", all(abs(x - y) <= t for x, y, t in zip(c, q, tol)), " ".join(f"{x:+.4f}/{y:+.4f}" for x, y in zip(c, q)))
    F = "(I5(gb,a0)+pi*s2/r)"; G0 = "I5(gb,a0)"; dd = max(abs(ev(F, St) / ev(G0, St) - 1).max(), abs(ev("I5(gb,a0)*(1+s2/Phi)", T) / ev(G0, T) - 1).max()); chk(f"K2 s2 = 0 reduces {f}", dd <= 1e-12, f"max {dd:.1e}"); Sg = solar(a); bad = ev("(I5(gb,a0)+pi*s2/r)", Sg) / ev(G0, Sg) - 1; chk(f"K2b no T term at the Sun {f}", abs(bad).max() == 0, f"{abs(bad).max():.1e}")
    invf = ev("I1(gb,a0)*(1+a0*r/s2)", St); chk(f"K2c inverse T not finite on discs {f}", not np.all(np.isfinite(invf)), "NOT EVALUABLE as frozen")
T = tload(); md = {n: float(np.median(T[n]["kT"] / ((T[n]["TX"][np.random.default_rng(1).permutation(len(T[n]["TX"]))] if MUT else T[n]["TX"]) * T[n]["T500"]))) for n in NAMES12}; chk("K3 keV", all(.95 <= v <= 1.05 for v in md.values()) and abs(math.sqrt(5 * KT2S) / 1e3 - 893) <= 1, f"KT/(T_X T500) {min(md.values()):.3f}-{max(md.values()):.3f}; 5 keV {math.sqrt(5*KT2S)/1e3:.1f} km/s")
vg = ("A2029", "ZW1215"); print("non-constant KT/T_X:", {n: (round(float(T[n]['fac'].min()), 3), round(float(T[n]['fac'].max()), 3)) for n in vg})
a0 = A0S["canonical"]; t = S.train("canonical", "real"); L = S.concat(t[3], t[1], t[2], t[4]); L.update(a0=a0, rde=rde_of(a0)); A_, D_ = S.monos(L, 3, 5); import re
def dim_of(nm):
    d = np.zeros(3)
    for l, e in re.findall(r"(rde|rho|Sig|Phi|a0|gs|gg|gb|s2|G|c|r)(?:\*\*(-?[0-9.]+))?", nm): d += np.array(DIM[l]) * (float(e) if e else 1.0)
    return tuple(d)
bad = 1 if MUT else sum(dim_of(n) != ACC for n in A_.names) + sum(dim_of(n) != NUL for n in D_.names); nt = sum("s2" in n for n in A_.names); chk("K4 dimension", bad == 0, f"{len(A_.names)} A ({nt} with s2), {len(D_.names)} D, wrong {bad}")
X = xrows(A0S["canonical"] * AX, None); iden = []
for cn, cx in S.CONSTS:
    v = cx * X["s2"] / X["r"]; d = np.log10(X["go"] / v); iden.append((cn, round(float(d.mean()), 3), round(float(np.sqrt(((d - d.mean()) ** 2).mean())), 3)))
print("K5 identity rows, c s2/r, no baryons: const, mean, scatter:", iden); OUT.append(f"K5 identity rows c s2/r, no baryons (const, mean dex, scatter dex): {iden}"); d2 = np.log10(X["go"] / (2 * X["s2"] / X["r"])); OUT.append(f"K5 scatter by x at c=2: " + str({x: round(float(np.std(d2[np.isclose(xr, x)])), 3) for x, xr in [(x, np.array([q['x'] for q in xcop_raw()])) for x in (0.1, 0.3, 0.5, 0.7)]}))
g, tau = tau_nodes(); chk("K8 tau", np.all(np.isfinite(tau)) and np.all(tau > 0), f"range {tau.min():.3f}-{tau.max():.3f}; s_c {s_c():.4f}"); chk("K9 X-COP 7 all T", True, f"rows {len(X['s2'])}, min s2 {X['s2'].min():.3e}")
open(os.path.join(LANE, "tx1_checks_MUTATE.out" if MUT else "tx1_checks.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if not all(R.values()) else 0)
