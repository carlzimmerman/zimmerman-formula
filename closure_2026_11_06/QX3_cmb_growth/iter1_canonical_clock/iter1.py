#!/usr/bin/env python3
"""QX3 iter1 (FROZEN_CRITERIA.md): Jeans suppression of a c_s^2 = 1 clock on CMB-lensing scales.
kappa = 1/2 FITTED; not theory closed.  QX3_MUTATE=1 sets c_s^2 = 1e-6 (separate outputs)."""
import os, json, numpy as np
from scipy.integrate import quad
MUT = os.environ.get("QX3_MUTATE") == "1"; cs2 = 1e-6 if MUT else 1.0
C = 299792.458
Ls = np.arange(8, 401); zs = np.linspace(0.1, 10, 199)
out = dict(mode="MUTATE_cs2_1e-6" if MUT else "main", cs2=cs2, corners=[])
for Om in (0.05, 0.3, 1.0):
    for H0 in (65.0, 75.0):
        Ode = 1 - Om
        E = lambda z: np.sqrt(Om * (1 + z) ** 3 + Ode)
        chi = np.array([quad(lambda x: C / H0 / E(x), 0, z)[0] for z in zs])          # Mpc
        aH_c = H0 * E(zs) / (1 + zs) / C                                             # comoving aH/c, 1/Mpc
        # k_J,comoving^2 = a^2 4 pi G rho / (c^2 cs2) = (3/2) Omega(z) (aH/c)^2 / cs2
        Ode_z = Ode / E(zs) ** 2
        kJ2_bg = 1.5 * Ode_z * aH_c ** 2 / cs2          # rho_phi = rho_DE (the clock is the dark energy)
        kJ2_bd = 1.5 * 1.0 * aH_c ** 2 / cs2            # C1 bound rho_phi <= rho_tot
        k = (Ls[:, None] + 0.5) / chi[None, :]
        rb = kJ2_bg[None, :] / k ** 2; rB = kJ2_bd[None, :] / k ** 2
        i = np.unravel_index(rb.argmax(), rb.shape); j = np.unravel_index(rB.argmax(), rB.shape)
        out["corners"].append(dict(Om=Om, H0=H0, max_ratio_background=float(rb.max()), at_background=[int(Ls[i[0]]), float(zs[i[1]])],
                                   max_ratio_bound=float(rB.max()), at_bound=[int(Ls[j[0]]), float(zs[j[1]])],
                                   frac_cells_bound_over_0p05=float((rB > 0.05).mean()),
                                   max_ratio_bound_L_ge_30=float(rB[Ls >= 30].max())))
mb = max(c["max_ratio_background"] for c in out["corners"]); mB = max(c["max_ratio_bound"] for c in out["corners"])
out["max_background"] = mb; out["max_bound"] = mB
out["label_background_reading"] = "FAIL (no-go)" if mb <= 0.05 else "OPEN"
out["label_bound_reading"] = "FAIL (no-go)" if mB <= 0.05 else "OPEN"
out["note"] = "kappa = 1/2 FITTED; not theory closed"
fn = "iter1_MUTATE" if MUT else "iter1"
json.dump(out, open(fn + ".json", "w"), indent=1); print(json.dumps(out, indent=1))
