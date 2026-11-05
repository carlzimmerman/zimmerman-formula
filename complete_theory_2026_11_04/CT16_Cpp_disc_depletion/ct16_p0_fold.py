"""CT16 P0: does v3s's khronon dust (C'''s dust phase) stay single-stream to z = 0 at a Milky Way disc?
Uses X14's exact planar results (F2): tau_f = w/(K Sigma_b), K = 4 pi G; charged element folds iff omega_p tau_f <= 1/sqrt 2,
omega_p^2 = K rho_tau0 (M_L - 1), M_L = (1+x)^2. Seconds, one thread. Frozen in FROZEN_CRITERIA.md."""
import json, math
import numpy as np

G = 4.30091e-3          # pc (km/s)^2 / Msun
PC_KM = 3.0857e13       # km per pc
MYR_S = 3.15576e13      # s per Myr
K = 4 * math.pi * G     # (km/s)^2 pc / Msun ; K*Sigma [Msun/pc^2] -> (km/s)^2/pc = acceleration

def accel_kms_per_myr(sigma):  # K*Sigma in km/s per Myr
    a = K * sigma                      # (km/s)^2 / pc
    return a / PC_KM * MYR_S           # km/s / Myr

out = {}
sig = np.array([10., 20., 50., 100.])
w = np.array([20., 50., 100., 150., 200., 250., 300., 400.])
tab = {}
for s in sig:
    tab[f"Sigma {s:g}"] = {f"w {v:g}": v / accel_kms_per_myr(s) for v in w}  # Myr
tau_max = max(max(r.values()) for r in tab.values())
tau_min = min(min(r.values()) for r in tab.values())
out["tau_f_Myr"] = tab
out["tau_f_max_Myr"] = tau_max
out["tau_f_min_Myr"] = tau_min
print("tau_f = w/(K Sigma_b) [Myr]; rows Sigma_b Msun/pc^2, cols w km/s", list(w))
for k_, r in tab.items():
    print(f"  {k_:12s}", " ".join(f"{t:8.1f}" for t in r.values()))
print(f"  max tau_f {tau_max:.1f} Myr, min {tau_min:.2f} Myr")

# held (charged) elements: omega_p tau_f against 1/sqrt 2
def omega_p_per_myr(rho, x):
    w2 = K * rho * ((1 + x) ** 2 - 1) / PC_KM ** 2 * MYR_S ** 2   # (km/s)^2/pc^2 -> 1/Myr^2
    return math.sqrt(w2)
held = {}
fold_count = 0; total = 0
for rho in (1e-3, 1e-2, 1e-1):
    for x in (0.5, 2.0, 10.0):
        op = omega_p_per_myr(rho, x)
        vals = {}
        for s in (10., 50., 100.):
            for v in (50., 200., 400.):
                t = v / accel_kms_per_myr(s)
                f = op * t <= 1 / math.sqrt(2)
                vals[f"S{s:g}_w{v:g}"] = (op * t, f)
                fold_count += f; total += 1
        held[f"rho {rho:g} x {x:g}"] = {"omega_p_per_Myr": op, "period_Myr": 2 * math.pi / op,
                                        "omega_p_tau_f": {k2: v2[0] for k2, v2 in vals.items()},
                                        "F2_fold": {k2: v2[1] for k2, v2 in vals.items()}}
print("held elements: omega_p [1/Myr], period [Myr], omega_p tau_f range, F2 folds of 9")
for k_, r in held.items():
    o = list(r["omega_p_tau_f"].values()); f = sum(r["F2_fold"].values())
    print(f"  {k_:16s} omega_p {r['omega_p_per_Myr']:.4f} period {r['period_Myr']:8.1f}  "
          f"omega_p tau_f {min(o):.3f}-{max(o):.2f}  F2 fold {f}/9")
print(f"  F2 folds {fold_count}/{total}; the rest are held and phase-mix to crossing (X14 F3), period above")
out["held"] = held
out["held_F2_folds"] = [fold_count, total]
verdict = "P0 FAIL: G6 NOT DECIDABLE in C''" if tau_max < 1000 else ("P0 PASS" if tau_min > 8000 else "P0 UNDECIDED")
out["verdict"] = verdict
print("P0 line: FAIL if max tau_f < 1000 Myr; PASS if min tau_f > 8000 Myr ->", verdict)
json.dump(out, open(__file__.replace(".py", ".json"), "w"), indent=1)
