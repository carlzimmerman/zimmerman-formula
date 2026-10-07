#!/usr/bin/env python3
"""CFG414 field-level controls (frozen): C1 x -> inf covers all cells; C2 analytic top-hat r_ON within one grid step; MUTATE (CFG414_MUTATE=1) x = 0.01
cuts the covered switch-ON mass by > 90% on CFG410's BASE z0 snapshot (128^3 deposit).  Separate outputs."""
import os, sys, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("CFG414_THREADS", "2")
import cfg414_pm as E
MUT = os.environ.get("CFG414_MUTATE", "0") == "1"; L, CH = [], []
def P(s=""): print(s); L.append(s)
def check(n, ok, v=""): CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")
mesh = E.Mesh(128); dx = mesh.dx; Dta = 11.806
g = np.arange(128); g = np.minimum(g, 128 - g) * dx
r = np.sqrt(g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2)
R0, A = 2.5, 200.0
delta = np.where(r <= R0, A - 1.0, 0.0).astype(np.float32); delta -= delta.mean() * 0
Rta = R0 * ((A - 1) / (Dta - 1)) ** (1 / 3)
if not MUT:
    m_inf = E.in_cover(mesh, delta, Dta, 1e3)
    check("C1 x -> inf covers every cell", bool(m_inf.all()), f"covered {m_inf.mean():.4f}")
    m1 = E.in_cover(mesh, delta, Dta, 1.0); rcov = r[m1].max()
    Rg = np.geomspace(dx, 8.0, 14); step = np.max(np.diff(Rg))
    check("C2 analytic top-hat: covered radius within one grid step of the analytic r_ta", abs(rcov - Rta) <= step, f"(frozen tolerance: one grid step) cover {rcov:.2f} vs analytic {Rta:.2f} Mpc/h (step {step:.2f})")
else:
    snap = np.load(os.path.join(E.REPO, "..", "_external_data", "cfg410_work", "cfg410_RES_Rc3_MIXA_FLAT_canonical_N256_z0.npz"))
    d = mesh.deposit(snap["pos"].astype(np.float32)); f = snap["f"].astype(np.float32)
    big = E.in_cover(mesh, d, Dta, 1e3); small = E.in_cover(mesh, d, Dta, 0.01)
    rho = 1 + d; mon = lambda m: float((rho * m).sum())
    drop = 1 - mon(small) / mon(big)
    check("MUTATE x = 0.01 cuts the covered mass by > 90%", drop > 0.9, f"drop {drop:.3f}")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, "cfg414_checks" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(L) + "\n")
raise SystemExit(0 if all(CH) else 1)
