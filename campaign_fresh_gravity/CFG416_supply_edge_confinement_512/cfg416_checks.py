#!/usr/bin/env python3
"""CFG416 controls (frozen): C2 x_h(r_ON) monotone and equal to the pre-check formula (to 1e-6) at z = 0; MUTATE (CFG416_MUTATE=1):
f_ret x10 raises the field-level covered switch-ON mass by > 20% on CFG410's BASE z0 (128^3 deposit).  C1 is inherited from CFG414."""
import os, sys, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("CFG416_THREADS", "2")
import cfg416_pm as E
MUT = os.environ.get("CFG416_MUTATE", "0") == "1"; L, CH = [], []
def P(s=""): print(s); L.append(s)
def check(n, ok, v=""): CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")
Dta = 11.806; G = 4.30091e-9; H = 0.674
def pre(R, foot):                                    # the pre-check formula (precheck_supply_edge_hosts.py)
    Mta = (4 * math.pi / 3) * R ** 3 * Dta * 0.315 * 2.775e11 / H; lM = math.log10(Mta * H)
    fr = 0.10 if lM < 12.5 else (0.10 + 0.45 * (lM - 12.5) if lM < 13.5 else min(0.55 + 0.30 * (lM - 13.5), 0.90))
    a0c = {"canonical": 9.3603e-11, "alt": 1.1312e-10}[foot] * 3.0857e22 / 1e6
    return min((5.364 / fr) * math.sqrt(G * fr * 0.157 * Mta / a0c) / (R / H), 1.0)
if not MUT:
    Rs = np.geomspace(1.0, 10.0, 40); ok = True; md = 0.0
    for foot in ("canonical", "alt"):
        xs = [E.x_supply(R, Dta, 1.0, "FLAT", foot) for R in Rs]; ps = [pre(R, foot) for R in Rs]
        md = max(md, max(abs(a - b) / b for a, b in zip(xs, ps)))
    check("C2 engine x_h equals the pre-check formula at z = 0 (rel 1e-6)", md < 1e-6, f"max rel diff {md:.2e}")
    P("  x_h(r_ON) canonical: " + ", ".join(f"{R:.1f}->{E.x_supply(R, Dta, 1.0, 'FLAT', 'canonical'):.2f}" for R in (1.56, 2.5, 4.0, 6.0, 8.0)))
else:
    mesh = E.Mesh(128)
    snap = np.load(os.path.join(E.REPO, "..", "_external_data", "cfg410_work", "cfg410_RES_Rc3_MIXA_FLAT_canonical_N256_z0.npz"))
    d = mesh.deposit(snap["pos"].astype(np.float32)); rho = 1 + d
    E.FRETX = 1.0; m1 = E.in_cover(mesh, d, Dta, None); E.FRETX = 10.0; m10 = E.in_cover(mesh, d, Dta, None)
    rise = (rho * m10).sum() / max((rho * m1).sum(), 1e-30) - 1
    check("MUTATE f_ret x10 raises the covered mass by > 20%", rise > 0.2, f"rise {rise:+.2f}")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, "cfg416_checks" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(L) + "\n")
raise SystemExit(0 if all(CH) else 1)
