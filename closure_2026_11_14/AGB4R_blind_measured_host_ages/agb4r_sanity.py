"""AGB4R sanity checks of the implementation (not frozen checks): distance formula, a second solver,
Delta chi2 refit against formula, bin sizes. Usage: python3 -I agb4r_sanity.py > agb4r_sanity.out"""
import os
import sys
import json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb4r_data as D  # noqa: E402
import agb4r_run as R  # noqa: E402
import numpy as np  # noqa: E402

# 1. mu_flat against the closed form for Omega_m = 1 (Einstein-de Sitter) and against a direct trapezoid for 0.334
z = np.array([0.05, 0.2, 0.4])
dc_eds = 2 * D.C_KMS / D.H0_FID * (1 - 1 / np.sqrt(1 + z))
mu_eds = 5 * np.log10((1 + z) * dc_eds) + 25
print("EdS max |dmu|:", float(np.max(np.abs(D.mu_flat(z, z, 1.0) - mu_eds))))
zz = np.linspace(0, 0.4, 400001)
Ez = np.sqrt(0.334 * (1 + zz) ** 3 + 0.666)
dc = np.concatenate([[0], np.cumsum((1 / Ez[1:] + 1 / Ez[:-1]) / 2 * np.diff(zz))]) * D.C_KMS / D.H0_FID
mu_tr = 5 * np.log10((1 + 0.4) * dc[-1]) + 25
print("Om 0.334 z 0.4 |dmu| vs trapezoid:", float(abs(D.mu_flat(0.4, 0.4, 0.334)[0] - mu_tr)))

X = D.build_samples()
pp = X["pp"]
# 2. bin sizes
for nb in (8, 12):
    print(f"pp {nb} bins sizes:", np.bincount(R.bins_of(pp, nb)).tolist())
print("big 16 bins sizes:", np.bincount(R.bins_of(X["big"], 16)).tolist())
print("rose 4 bins sizes:", np.bincount(R.bins_of(X["rose"], 4)).tolist())

# 3. second solver: numpy lstsq on sqrt(w)-scaled columns, primary M0 and M1
for step in (False, True):
    oc, _ = R.other_columns(pp, 8, step, True)
    M = np.column_stack(oc + [D.SLOPE * pp["age"]])
    sw = np.sqrt(pp["w"])
    beta, *_ = np.linalg.lstsq(M * sw[:, None], (pp["mB"] - pp["mu_fid"]) * sw, rcond=None)
    Q, Rr = np.linalg.qr(M * sw[:, None])
    Rinv = np.linalg.inv(Rr)
    sig = np.sqrt(np.sum(Rinv ** 2, axis=1))
    f = R.fit(pp, "R", 8, step, pp["age"])
    print(f"{'M1' if step else 'M0'} lstsq A = {beta[-1]:+.6f} +- {sig[-1]:.6f}  (main: {f['A']:+.6f} +- {f['sig_A']:.6f})")

# 4. Delta chi2 refit vs formula over every fit written by mode fits and rows
F = json.load(open(os.path.join(HERE, "agb4r_fits.json")))
Rw = json.load(open(os.path.join(HERE, "agb4r_rows.json")))
worst = 0.0
for blob in (F["M0"], F["M1"], Rw["M0"], Rw["M1"]):
    for k, f in blob.items():
        if isinstance(f, dict) and "dchi2_A0" in f:
            worst = max(worst, abs(f["dchi2_A0"] - f["dchi2_A0_formula"]), abs(f["dchi2_A1"] - f["dchi2_A1_formula"]))
print("max |dchi2 refit - formula| over all fits:", worst)
