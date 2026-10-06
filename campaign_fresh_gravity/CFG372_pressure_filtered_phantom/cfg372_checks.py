#!/usr/bin/env python3
"""CFG372 controls C1/C2 (+ MUTATE: T = 1e10 K must cut the rms phantom source by > 90%).  Field level on CFG361's T5 canonical
z = 0 snapshot (read-only), deposited 128^3.  CFG372_MUTATE=1 -> separate outputs."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("CFG372_THREADS", "2")
import cfg372_pm as E
MUTATE = os.environ.get("CFG372_MUTATE", "0") == "1"; SLUG = "cfg372_checks" + ("_MUTATE" if MUTATE else "")
LOG, CH = [], []
def P(s=""): print(s); LOG.append(s)
def check(n, ok, v=""): CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")
def kJ(T, a=1.0):
    cs = math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3; return math.sqrt(1.5 * E.Om * a) * 100.0 / cs
W = lambda k, T: 1.0 / (1.0 + (k / kJ(T))**2) if T > 0 else np.ones_like(k)
k = np.logspace(-2, 2, 400)
for T in (1e4, 1e6):
    P(f"  T = {T:.0e} K: k_J(z=0) = {kJ(T):.3f} h/Mpc, k_J(z=1) = {kJ(T, 0.5):.3f}")
check("C1 W(k_J) = 0.5, W <= 1, monotone; T -> 0 gives W = 1", all(abs(W(np.array([kJ(T)]), T)[0] - 0.5) < 1e-12 and np.all(W(k, T) <= 1) and np.all(np.diff(W(k, T)) <= 0) for T in (1e4, 1e6)) and np.all(W(k, 0.0) == 1))
snap = os.path.join(E.REPO, "..", "_external_data", "cfg361_work", "cfg361_T5_FLAT_canonical_N256_z0.npz")
pos = np.load(snap)["pos"].astype(np.float32); mesh = E.Mesh(128); delta = mesh.deposit(pos)
def sph_rms(T):
    a = 1.0; dk = mesh.fwd(delta); phik = (-1.5 * E.Om / a) * dk * mesh.ik2
    if T > 0:
        Wk = (1.0 / (1.0 + (mesh.kx**2 + mesh.ky**2 + mesh.kz**2) / kJ(T)**2)).astype(np.float32)
        gb = [E.FB * (-mesh.inv(1j * kv * phik * Wk)) for kv in mesh.kvec]
    else:
        gb = [E.FB * (-mesh.inv(1j * kv * phik)) for kv in mesh.kvec]
    y = np.sqrt(sum(g**2 for g in gb)) / (a * E.a0_code(a, "FLAT", "canonical")); w = E.nu_mono(y).astype(np.float32) - 1.0
    s = -mesh.inv(sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb)))
    return float(np.sqrt(np.mean(s**2)))
r0 = sph_rms(0.0)
if not MUTATE:
    r6 = sph_rms(1e6); r4 = sph_rms(1e4)
    P(f"  rms phantom source: T=0 {r0:.4e}; T=1e4 {r4:.4e} ({r4/r0:.3f}); T=1e6 {r6:.4e} ({r6/r0:.3f})")
    check("C2 0 < rms(T=1e6) < rms(T=0)", 0 < r6 < r0, f"ratio {r6/r0:.3f}")
else:
    r10 = sph_rms(1e10); P(f"  rms phantom source: T=0 {r0:.4e}; T=1e10 {r10:.4e} ({r10/r0:.4f})")
    check("MUTATE: T = 1e10 K cuts the rms phantom source by > 90%", r10 / r0 < 0.10, f"ratio {r10/r0:.4f}")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
raise SystemExit(0 if all(CH) else 1)
