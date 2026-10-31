#!/usr/bin/env python3
"""UV1 (FROZEN_CRITERIA.md): X48's zoom text with two optional changes, ZK1's kernel. X48's files are read only.
    UV1_KCUT=<1/Mpc> and/or UV1_KICK=<km/s, 3D rms> python3 uv1_zoom.py --mass 1e14 --seed 1 --ng 64 --work DIR --resume
    python3 uv1_zoom.py --checks     # K1, K2, K3
kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, math, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); SRC = os.path.join(REB, "X48_native_cf_zoom", "x48_zoom.py"); sys.path.insert(0, os.path.join(REB, "ZK1_fast_force_kernel")); import x48_fast
T = open(SRC).read()
def rep(a, b):
    global T
    assert T.count(a) == 1, a
    T = T.replace(a, b)
rep('Pk[0, 0, 0] = 0.0\n', 'Pk[0, 0, 0] = 0.0\n    if os.environ.get("UV1_KCUT"): Pk[KK > float(os.environ["UV1_KCUT"])] = 0.0\n')
rep('x -= x.mean(0); v -= v.mean(0)\n', 'if os.environ.get("UV1_KICK"): v = v + np.random.default_rng(a.seed + 10000).standard_normal(v.shape) * float(os.environ["UV1_KICK"]) / math.sqrt(3)\n        x -= x.mean(0); v -= v.mean(0)\n')
Z = types.ModuleType("x48_zoom_uv1"); Z.__file__ = SRC; Z.__dict__["__name__"] = "x48_zoom_uv1"; exec(compile(T, SRC, "exec"), Z.__dict__); Z.accel = x48_fast.accel
def band_kick(M=1e14, ng=64, Mtop=1e10):
    C = Z.cosmology(); rho = C["rhom"]; qM = lambda m: (3 * (m / 2) / (4 * math.pi * rho)) ** (1 / 3); k1, k2 = math.pi * ng / (4 * qM(M)), math.pi * ng / (4 * qM(Mtop)); K, PK = C["K"], C["PK"]; s = (K >= k1) & (K <= k2); I = float(np.trapz(PK[s] / (2 * math.pi ** 2), K[s])); zi = 40.0; Di = float(np.interp(zi, C["ZG"], C["DG"])); ai = 1 / (1 + zi); Hi = Z.Hz(C, zi); Om_i = C["Om"] * (1 + zi) ** 3 / (C["Om"] * (1 + zi) ** 3 + C["OL"]); return ai * Hi * Om_i ** 0.55 * Di * math.sqrt(I), k1
def checks():
    OUT = []
    def P(s): print(s, flush=True); OUT.append(s)
    C = Z.cosmology(); S0 = importlib.util.spec_from_file_location("x48_plain", SRC); X0 = importlib.util.module_from_spec(S0); S0.loader.exec_module(X0); q0, p0, m0 = X0.constrained_field(C, 1e14, 1, 64, 1.5); os.environ.pop("UV1_KCUT", None); q1, p1, m1 = Z.constrained_field(C, 1e14, 1, 64, 1.5); d = float(np.abs(p1 - p0).max()); k1 = d == 0.0 and np.array_equal(q0, q1); P(f"K1 no change: ICs against X48's, seed 1: |d| {d:.1e}: {'PASS' if k1 else 'FAIL'}")
    sv, kN = band_kick(); kc = kN / 2; os.environ["UV1_KCUT"] = repr(kc); q2, p2, m2 = Z.constrained_field(C, 1e14, 1, 64, 1.5); os.environ.pop("UV1_KCUT"); dc = max(abs(m2["constraint_check"]["c1"]), abs(m2["constraint_check"]["c2"])); dn = abs(m2["nu"] / m0["nu"] - 1); rms0, rms2 = float(p0.std()), float(p2.std()); k2 = dc <= 1e-9 and dn <= 1e-9; P(f"K2 cut at {kc:.3f}/Mpc: constraint residuals {dc:.1e}, nu changed by {dn:.1e}; displacement rms {rms0:.4f} to {rms2:.4f} Mpc: {'PASS' if k2 else 'FAIL'}")
    rg = np.random.default_rng(11); v = rg.standard_normal((57777, 3)) * sv / math.sqrt(3); sa = float(v.std()); k3 = abs(sa / (sv / math.sqrt(3)) - 1) <= 0.01; P(f"K3 kick: 3D rms {sv:.3f} km/s at z_i, band {kN:.2f}/Mpc up; sample per axis {sa:.4f} against {sv / math.sqrt(3):.4f}: {'PASS' if k3 else 'FAIL'}")
    open(os.path.join(HERE, "uv1_checks.out"), "w").write("\n".join(OUT) + "\n"); json.dump(dict(kick=sv, kN=kN, kcut=kc), open(os.path.join(HERE, "uv1_setup.json"), "w")); return 0 if (k1 and k2 and k3) else 1
if __name__ == "__main__":
    if "--checks" in sys.argv: sys.exit(checks())
    sys.exit(Z.main())
