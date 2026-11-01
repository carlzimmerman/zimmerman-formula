#!/usr/bin/env python3
"""NR2 (FROZEN_CRITERIA.md): eta at 1e10, 1e11 from the ng 80 zooms, then version N on SPARC with all three anchors at ng 80, through NR1's path.
    python3 nr2.py          # K1, measure, K2, median, band runs, MUTATE
kappa = 1/2 FITTED; no a0 in the cold sector; not theory closed."""
import json, math, os, sys
import numpy as np
THIS = os.path.abspath(__file__); HERE0 = os.path.dirname(THIS); RB0 = os.path.dirname(HERE0); X48R = os.path.join(RB0, "X48_native_cf_zoom", "runs"); X81P = os.path.join(RB0, "X81_core_convergence", "x80_core_convergence.py")
_a = sys.argv; sys.argv = [X81P]; _s = open(X81P).read(); NS = dict(__file__=X81P, __name__="x81_prefix"); exec(compile(_s[:_s.index("# K1: exact smooth core")], X81P, "exec"), NS); sys.argv = _a
fit, a_fit, M_nfw, eta_of = NS["fit"], NS["a_fit_profile"], NS["M_nfw"], NS["eta_of"]
_t = open(os.path.join(RB0, "NR1_native_n_ng80", "nr1.py")).read();
G = dict(__file__=THIS, __name__="nr1_prefix"); exec(compile(_t[:_t.index('P("NR1: version N')], "nr1_prefix", "exec"), G); P, run, line, T0, OUT = G["P"], G["run"], G["line"], G["T0"], G["OUT"]; HERE = G["HERE"]; assert HERE == HERE0
def measure(root, M, ng):
    v = {}; flagged = []
    for s in range(1, 10):
        k = f"M{M:.0e}".replace("+", "") + f"_s{s}_ng{ng}"; sn = os.path.join(root, k, "snap_zf.npz")
        if not (os.path.exists(sn) and os.path.exists(os.path.join(root, k, "done.json"))): continue
        Z = np.load(sn); x, m = Z["x"], float(Z["m"]); meta = json.loads(str(Z["meta"])); rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3
        o, res = fit(x, m, rho, meta["eps"]); c = o.get("c_nfw_fit") if res is not None else None
        if not c: flagged.append(k); continue
        v[k] = float(eta_of(a_fit(M_nfw(c), 0.001)))
    return np.array(list(v.values())), flagged
def boot(A, g): return np.median(A[g.integers(0, len(A), (10000, len(A)))], axis=1)
def band(a, b):
    g = np.random.default_rng(20261030); d = boot(b, g); return [float(x) for x in np.percentile(boot(a, g) / d, [16, 84])]
P("NR2: version N with eta at ng 80 at 1e10, 1e11, 1e12; kappa = 1/2 FITTED; not theory closed")
E = {}; FL = {}
for M, ng, root in ((1e10, 64, X48R), (1e11, 64, X48R), (1e12, 64, X48R), (1e10, 80, os.path.join(HERE, "runs")), (1e11, 80, os.path.join(HERE, "runs")), (1e12, 80, X48R)):
    E[M, ng], FL[M, ng] = measure(root, M, ng); v = E[M, ng]; g = np.random.default_rng(20261030); b = boot(v, g); P(f"  M {M:.0e} ng {ng} (n {len(v)}, flagged {len(FL[M, ng])}): eta_conv {np.median(v):.2f} [68% {np.percentile(b, 16):.2f}, {np.percentile(b, 84):.2f}], per seed {min(v):.1f} to {max(v):.1f}")
med = lambda M, ng: float(np.median(E[M, ng])); d1 = max(abs(med(1e10, 64) - 29.26), abs(med(1e11, 64) - 24.34)); k1 = d1 <= 0.01; P(f"K1 estimator on X80's ng 64: {med(1e10, 64):.3f}, {med(1e11, 64):.3f} against 29.26, 24.34: {'PASS' if k1 else 'FAIL'}")
d12 = abs(med(1e12, 80) - 21.53); P(f"A5's anchor re-read: {med(1e12, 80):.3f} against 21.53: {'agrees' if d12 <= 0.01 else 'DIFFERS'}")
n10, n11 = len(E[1e10, 80]), len(E[1e11, 80])
if n10 < 6 or n11 < 6: P(f"UNDECIDED: finished and measured {n10}, {n11}"); open(os.path.join(HERE, "nr2.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)
for M in (1e10, 1e11, 1e12): l, h = band(E[M, 80], E[M, 64]); P(f"  eta(ng 80)/eta(ng 64) at {M:.0e}: {med(M, 80) / med(M, 64):.3f} [68% {l:.3f}, {h:.3f}]")
ETA = 21.53; r10, r11 = med(1e10, 80) / ETA, med(1e11, 80) / ETA; (l10, h10), (l11, h11) = band(E[1e10, 80], E[1e12, 80]), band(E[1e11, 80], E[1e12, 80]); P(f"rho10 {r10:.3f} [{l10:.3f}, {h10:.3f}], rho11 {r11:.3f} [{l11:.3f}, {h11:.3f}]; slope per dex 1e10-1e12 {math.log10(r10) / 2:.4f}, 1e11-1e12 {math.log10(r11):.4f}")
XN = json.load(open(os.path.join(RB0, "X80_low_mass_floor_emergence", "x80_converged.json"))); E0 = json.load(open(os.path.join(RB0, "CE1_converged_eta_grade", "ce1_a4_results.json")))["eta"]["12"]["med"]; K2 = run("NR2_K2", E0, XN["r10"], XN["r11"]); NN = json.load(open(os.path.join(RB0, "NF1_no_floor_rule", "NF1_NATIVE_x74_results_fs0.034_nat_s2.7774.json")))["footings"]["canonical"]["sparc"]; d2 = max(max(abs(v["U_median"] - NN[t]["U_median"]), abs(v["rms"] - NN[t]["rms"])) for t, v in K2["footings"]["canonical"]["sparc"].items()); k2 = d2 <= 1e-9; P(f"K2 A4 anchor, X80's rho against NF1_NATIVE: max |d| {d2:.1e}: {'PASS' if k2 else 'FAIL'}")
RES = {}
for t, a in dict(MEDIAN=(r10, r11), LOW=(l10, l11), HIGH=(h10, h11)).items(): RES[t] = line(f"{t} eta12 {ETA}, rho {a[0]:.3f}, {a[1]:.3f}", run(f"NR2_{t}", ETA, *a))
M_ = line(f"MUTATE rho {r10 / 2:.3f}, {r11 / 2:.3f}", run("NR2_MUTATE", ETA, r10 / 2, r11 / 2)); dm = max(abs(M_[t][0] - RES["MEDIAN"][t][0]) for t in M_); mt = dm > 0.02; P(f"MUTATE moves U by {dm:.3f}: {'BITES' if mt else 'INSENSITIVE'}")
ok = k1 and k2 and mt; L = lambda r: all(v[2] for v in RES[r].values()); U = [v[0] for v in RES["MEDIAN"].values()]; side = "" if L("MEDIAN") else (" (Upsilon high)" if max(U) > 0.80 else " (Upsilon low)" if min(U) < 0.50 else " (rms)")
V = "NOT DECIDED" if not ok else ("ALL-NG80 PASSES" if L("MEDIAN") else "ALL-NG80 FAILS" + side) + (" [NOISE-LIMITED]" if (L("LOW") != L("MEDIAN") or L("HIGH") != L("MEDIAN")) else ""); P("VERDICT: " + V)
json.dump(dict(verdict=V, r10=r10, r11=r11, r10_68=[l10, h10], r11_68=[l11, h11], eta={f"{M:.0e}_ng{ng}": E[M, ng].tolist() for M, ng in E}, flagged={f"{M:.0e}_ng{ng}": FL[M, ng] for M, ng in FL}, runs=RES, K1=d1, K2=d2, mutate=dm), open(os.path.join(HERE, "nr2_results.json"), "w"), indent=1); open(os.path.join(HERE, "nr2.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
