#!/usr/bin/env python3
"""ND1_native_dwarfs part C, the measurement (FROZEN_CRITERIA.md section 5b): the zooms' inner profile, per seed, at z_f and, if finished, z = 0. ZN1's measure() and X81's fit, both read-only. Writes nd1_shapes.json, nd1_shapes.out.
    python3 nd1_shapes.py        kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True      # X77's prefix imports x48_analyze from X48's directory; nothing may be written there
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
_s = importlib.util.spec_from_file_location("zn1_measure_ro", os.path.join(REB, "ZN1_zooms_to_z0", "zn1_measure.py")); MEAS = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = ["zn1_measure_ro"]; _s.loader.exec_module(MEAS); sys.argv = _a
X81P = os.path.join(REB, "X81_core_convergence", "x80_core_convergence.py"); src = open(X81P).read(); src = src[:src.index("# K1: exact smooth core")]; NS = dict(__file__=X81P, __name__="x81_prefix"); _a = sys.argv; sys.argv = [X81P]; exec(compile(src, X81P, "exec"), NS); sys.argv = _a
FIT, a_fit, M_nfw, eta_of = NS["fit"], NS["a_fit_profile"], NS["M_nfw"], NS["eta_of"]
mu = lambda y: math.log1p(y) - y / (1 + y)
P("ND1 zoom measurement: M(<r) from ZN1's measure(), reliable only outside 3 eps; X48's c_nfw; kappa = 1/2 FITTED; not theory closed")
k2 = MEAS.k2(); P(f"K5b ZN1's inherited K2 (sampled NFW c 4): {'PASS' if k2 else 'FAIL'}")
X80 = json.load(open(os.path.join(REB, "X80_low_mass_floor_emergence", "x80_converged.json")))["runs"]
X48 = os.path.join(REB, "X48_native_cf_zoom", "runs"); ZN1 = os.path.join(REB, "ZN1_zooms_to_z0", "runs"); ZN2 = os.path.join(REB, "ZN2_native_profile_sparc_groups", "runs")
def one(path, z_snap, name):
    Z = np.load(path, allow_pickle=False); meta = json.loads(str(Z["meta"])); x, m = Z["x"], float(Z["m"]); z = meta["zf"] if z_snap is None else z_snap; eps = meta["eps"]
    o = MEAS.measure(x, m, z, eps); r = o["r"]; Menc = o["Menc"]; rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + z) ** 3
    f0, f1 = FIT(x, m, rho, eps); c = f0.get("c_nfw_fit") if f1 is not None else None
    r3 = 3 * eps; n3 = int(np.searchsorted(r, r3)); M3 = float(np.exp(np.interp(math.log(r3), np.log(r), np.log(Menc)))); M6 = float(np.exp(np.interp(math.log(2 * r3), np.log(r), np.log(Menc)))); r200th = float(r[199])
    d = dict(name=name, seed=meta["seed"], M_nominal=meta["M"], z=z, zf=meta["zf"], eps_pc=eps * 1e6, r3e_pc=r3 * 1e6, rf_pc=meta["rf_phys"] * 1e6, r200th_pc=r200th * 1e6, n_in_3e=n3, m_part=m, N=int(len(x)), R200_pc=o["R200"] * 1e6, M200=o["M200"], x_conv=o["x_conv"], x_edge=o["x_edge"], M_3e=M3, M_6e=M6, lnm=[float(v) for v in o["lnm"]], slope_3e6e=math.log(M6 / M3) / math.log(2.0))
    if c:
        rv = f0["rvir"]; Mv = float((r <= rv).sum() * m); eta = float(eta_of(a_fit(M_nfw(c), 0.001))); y = c * r3 / rv
        d.update(c_nfw=float(c), rvir_pc=rv * 1e6, Mvir=Mv, rconv_pc=f0["rconv"] * 1e6, eta_conv=eta, eta_cut=f1["S"]["eta"], rhos_rs_pc=Mv * c * c / (4 * math.pi * (rv * 1e6) ** 2 * mu(c)), S_conv_pc=eta * 3 * Mv / (4 * math.pi * (rv * 1e6) ** 2), ratio=(c * c / (3 * mu(c))) / eta, slope_nfw_3e6e=(math.log(mu(2 * y)) - math.log(mu(y))) / math.log(2.0), y_3e=y)
    return d
RES = dict(frozen="9230f53a67", x=MEAS.XG.tolist(), zf={}, z0={}, status={}); kd = 0.0; nk = 0
for tag in ("1e10", "1e11", "1e12", "1e13", "1e14"):
    rows = []
    for s in range(1, 10):
        k = f"M{tag}_s{s}_ng64"; f = os.path.join(X48, k, "snap_zf.npz")
        if not os.path.exists(f): continue
        d = one(f, None, k); rows.append(d)
        if tag in ("1e10", "1e11"):
            q = X80[k]; kd = max(kd, abs(d["c_nfw"] - q["c_nfw"]), abs(d["eta_conv"] - q["eta_conv"])); nk += 1
    RES["zf"][tag] = rows; RES["status"][f"zf_{tag}"] = len(rows); print(f"  z_f {tag}: {len(rows)} seeds", flush=True)
    rows = []; root = ZN2 if tag in ("1e10", "1e11") else ZN1
    for s in range(1, 10):
        k = f"M{tag}_s{s}_ng64"; f = os.path.join(root, k, "snap_z0.00.npz")
        if os.path.exists(f) and os.path.exists(os.path.join(root, k, "done.json")): rows.append(one(f, 0.0, k))
    RES["z0"][tag] = rows; RES["status"][f"z0_{tag}"] = len(rows); print(f"  z = 0 {tag}: {len(rows)} seeds", flush=True)
okk = kd <= 1e-9 and nk == 18; RES["K5a"] = kd; RES["K5b"] = bool(k2); P(f"K5a zoom path reproduces X80's c_nfw and eta_conv, {nk} runs at 1e10, 1e11: max |d| {kd:.1e}: {'PASS' if okk else 'FAIL'}")
med = lambda rows, k: float(np.median([q[k] for q in rows if k in q]))
for snap in ("zf", "z0"):
    for tag, rows in RES[snap].items():
        if not rows: P(f"  {snap} {tag}: no finished seeds"); continue
        P(f"  {snap} {tag}: n {len(rows)}, 3 eps {med(rows, 'r3e_pc'):.0f} pc, n(<3 eps) {med(rows, 'n_in_3e'):.0f}, r of 200th particle {med(rows, 'r200th_pc'):.0f} pc, R200 {med(rows, 'R200_pc') / 1e3:.1f} kpc, M200/M nominal {med(rows, 'M200') / rows[0]['M_nominal']:.3f}, c_nfw {med(rows, 'c_nfw'):.2f}, eta_conv {med(rows, 'eta_conv'):.2f}, rho_s r_s / S {med(rows, 'ratio'):.3f}, slope 3-6 eps {med(rows, 'slope_3e6e'):.2f} (NFW {med(rows, 'slope_nfw_3e6e'):.2f}, y(3 eps) {med(rows, 'y_3e'):.3f})")
json.dump(RES, open(os.path.join(HERE, "nd1_shapes.json"), "w")); open(os.path.join(HERE, "nd1_shapes.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (okk and k2) else 1)
