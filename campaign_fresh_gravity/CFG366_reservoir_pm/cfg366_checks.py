"""CFG366 field-level controls C1 (compensation), C2 (limits), C3 (S0 read) on a 64^3 mesh with a linearly scaled IC field.
Criteria: FROZEN_CRITERIA.md (5f3a22464). Run: python3 cfg366_checks.py ; CFG366_MUTATE=1 -> C1 must FAIL (rc 1).
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg366_pm as E  # noqa: E402

res = []
def check(n, ok, v):
    res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n + ": " + v)

N = 128
mesh = E.Mesh(N); dta = E.dta_table()
# a REAL evolved field: CFG361's T5 canonical z = 0 particle snapshot (read-only), deposited on 128^3.
# (A first version used a linearly scaled IC field on 64^3: it had NO ON cells, so every check passed vacuously.
#  That was replaced before any PM run; disclosed in the README.)
SNAP = os.path.join(os.path.dirname(E.WORK), "cfg361_work", "cfg361_T5_FLAT_canonical_N256_z0.npz")
pos = np.load(SNAP)["pos"].astype(np.float64)
delta = mesh.deposit(pos).astype(np.float32)

def extra_field(Rc, a=1.0):
    E.RC = Rc
    acc_res, info = E.forces(mesh, delta, a, "RES", "FLAT", "canonical", dta, diag=True)
    acc_s0, _ = E.forces(mesh, delta, a, "S0", "FLAT", "canonical", dta)
    acc_t5, _ = E.forces(mesh, delta, a, "T5", "FLAT", "canonical", dta)
    return acc_res, acc_s0, acc_t5, info

ar, a0, a5, info = extra_field(1.0)
print(f"field: delta max {float(delta.max()):.1f}; e_mean {info['e_mean']:.3e} (must be > 0 for the checks to bite)")
check("C0 the field has ON-cell excess (non-vacuous)", info["e_mean"] > 0, f"e_mean {info['e_mean']:.3e}")
check("C1 compensation: band |extra_k|/|e_k| (k < 0.1/R_c) <= 0.01 and k=0 mode zero", info["C1_band_ratio"] <= 0.01 and info["C1_k0"] <= 1e-6 * max(info["C1_k0_e"], 1.0),
      f"band ratio {info['C1_band_ratio']:.2e}, |extra_k0| {info['C1_k0']:.1e} (|e_k0| {info['C1_k0_e']:.2e}); overdraw mass {info['overdraw_mass']:.3f}; e_mean {info['e_mean']:.3e}")
arL, _, _, _ = extra_field(1e6)
dT5 = max(float(np.abs(x - y).max()) for x, y in zip(arL, a5)); scale = max(float(np.abs(y - z).max()) for y, z in zip(a5, a0))
check("C2a R_c = 1e6 reproduces T5's force (extra = T5 minus its mean; force identical)", dT5 <= 1e-4 * max(scale, 1e-30),
      f"max |F_RES - F_T5| {dT5:.2e} vs T5 extra-force scale {scale:.2e}")
arS, _, _, _ = extra_field(1e-6)
dS0 = max(float(np.abs(x - y).max()) for x, y in zip(arS, a0))
check("C2b R_c = 1e-6 reproduces S0 (extra = 0)", dS0 <= 1e-6 * max(scale, 1e-30) + 1e-12, f"max |F_RES - F_S0| {dS0:.2e}")
W359 = os.path.join(os.path.dirname(E.WORK), "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json")
ok3 = os.path.exists(W359)
s8 = json.load(open(W359))["snap"]["z0"]["sigma8"] if ok3 else float("nan")
check("C3 CFG359 S0 256^3 JSON present and readable", ok3 and np.isfinite(s8), f"sigma8(z0) = {s8:.4f}")
print(f"{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if E.MUTATE else ""))
sys.exit(0 if all(res) else 1)
