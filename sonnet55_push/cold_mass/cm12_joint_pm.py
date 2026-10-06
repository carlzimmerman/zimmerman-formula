"""cm12: JOINT particle-mesh test -- two-level cold retention (cm08-cm10) + the framework's QUMOND phantom, run here (owner 2026-10-06).
Engine: CFG359's cfg359_pm.py imported READ-ONLY (Mesh, ICs, EH linear spectrum, nu_mono, a0, growth, P(k)/sigma8); box changed to L = 64 Mpc/h, 128^3.
Model (declared before the run):
  baryons = FB of every particle (unit weight); cold = (1 - FB) with a BOUND weight r_i and a DIFFUSE weight 1 - r_i; the diffuse part is deposited and
  Gaussian-smoothed at R_s (default 1 Mpc/h) -- mass conserved, it follows the large-scale flow but does not cluster below R_s.
  Retention rule (sub-grid, the PM cannot resolve galaxy halos): particle in a halo if 1 + delta_cell > DCUT (default 100, cell 0.5 Mpc/h); its host is
  group-scale if the 1 Mpc/h top-hat mass exceeds M_step = 10^12.5 Msun (1 + delta_1 > 5.82), else galaxy-scale; r_class = 0.60 / 0.13 / 1 (field);
  ramp w(z): 0 at z >= 2.5, 1 at z <= 1.5; r_i = 1 - w (1 - r_class), recomputed each step (instantaneous, not monotone -- stated).
  Phantom (when on): QUMOND, sourced by baryons only (g_b = FB g_N of the unit-weight field), nu_mono, a0 FLAT canonical 9.3603e-11, switch f = 1 everywhere
  (CFG359's bare chassis S1; NOT candidate B's T1 switch).
  Lensing field: delta_lens = -(a / 1.5 Om) lap(phi_total) in Fourier = delta_matter + delta_phantom; sigma8_lens is the S8-relevant amplitude.
AMENDMENT after the first two runs (P with the bare phantom gave sigma8 x5.4 / lens x11.5 -- the known L178 overshoot; R removed only 7% of the cold
  mass because 0.5 Mpc/h cells dilute galaxy halos below the cut): bare-phantom PR runs stopped; added P_T1, PR_T1, PR_T1_d50 with candidate B's T1 switch
  (CFG359 forces(), read-only) and R_d50.
Runs: S0 (LCDM-like control), R (retention only), P (phantom only), PR (both); PR variants DCUT 50/200, R_s 0.5.
Reported: sigma8 of matter and of the lensing field at z = 0, as ratios to S0. Context (provisional, from memory): KiDS/DES S8 ~7% (+-3%) below Planck.
Run: python3 cm12_joint_pm.py RUNNAME   (RUNNAME in S0 R P PR PR_d50 PR_d200 PR_rs05);  python3 cm12_joint_pm.py REPORT
"""
import os, sys, json, math, time, importlib.util
os.environ.setdefault("CFG359_THREADS", "4")
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cfg359_pm", os.path.join(HERE, "..", "..", "campaign_fresh_gravity", "CFG359_native_pm_growth", "cfg359_pm.py"))
cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
import numpy as np
LBOX, NPG = 64.0, 128
cfg.L = LBOX
WORK = os.path.join(HERE, "..", "..", "..", "_external_data", "cm12_work")
FB, Om = cfg.FB, cfg.Om
DTA = cfg.dta_table()
RUNS = {"S0": dict(ret=False, ph=False), "R": dict(ret=True, ph=False), "P": dict(ret=False, ph=True), "PR": dict(ret=True, ph=True),
        "PR_d50": dict(ret=True, ph=True, dcut=50.0), "R_d50": dict(ret=True, ph=False, dcut=50.0), "P_T1": dict(ret=False, ph=True, sw="T1"), "PR_T1": dict(ret=True, ph=True, sw="T1"), "PR_T1_d50": dict(ret=True, ph=True, sw="T1", dcut=50.0), "PR_d200": dict(ret=True, ph=True, dcut=200.0), "PR_rs05": dict(ret=True, ph=True, rs=0.5)}
def wdeposit(mesh, pos, w):
    M = mesh.M; i0, i1, f = mesh.cic_idx(pos); rho = np.zeros(M ** 3)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = f[:, 0] if cx else 1 - f[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = f[:, 1] if cy else 1 - f[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = f[:, 2] if cz else 1 - f[:, 2]
                rho += np.bincount((ix * M + iy) * M + iz, weights=w * wx * wy * wz, minlength=M ** 3)
    return (rho.reshape((M,) * 3) / (len(w) / M ** 3)).astype(np.float32)   # in units of the mean of ALL particles
def gsmooth(mesh, x, R):
    k2 = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    return mesh.inv(mesh.fwd(x) * np.exp(-0.5 * k2 * R * R))
def thsmooth(mesh, x, R):
    kk = np.sqrt(mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2) * R; kk = np.where(kk > 0, kk, 1e-6)
    return mesh.inv(mesh.fwd(x) * 3 * (np.sin(kk) - kk * np.cos(kk)) / kk ** 3)
def fields(mesh, pos, a, opt):
    one = np.ones(len(pos))
    rho_u = wdeposit(mesh, pos, one)                                   # 1 + delta of all particles
    z = 1 / a - 1; w = float(np.clip((2.5 - z) / 1.0, 0, 1)) if opt.get("ret") else 0.0
    if w > 0:
        dcut = opt.get("dcut", 100.0); rho1 = thsmooth(mesh, rho_u, 1.0)
        rc, r1 = mesh.interp([rho_u, rho1], pos).T
        rcls = np.where(rc > dcut, np.where(r1 > 5.82, 0.60, 0.13), 1.0)
        r = 1 - w * (1 - rcls)
    else:
        r = one
    rho_b = wdeposit(mesh, pos, r); rho_d = wdeposit(mesh, pos, 1 - r) if w > 0 else np.zeros_like(rho_b)
    if w > 0: rho_d = gsmooth(mesh, rho_d, opt.get("rs", 1.0))
    rho_tot = FB * rho_u + (1 - FB) * (rho_b + rho_d)
    dk = mesh.fwd(rho_tot - 1.0)
    phik = (-1.5 * Om / a) * dk * mesh.ik2
    if opt.get("ph"):
        gN = [-mesh.inv(1j * kv * (-1.5 * Om / a) * mesh.fwd(rho_u - 1.0) * mesh.ik2) for kv in mesh.kvec]
        gb = [FB * g for g in gN]; del gN
        y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * cfg.a0_code(a, "FLAT", "canonical"))
        wv = (cfg.nu_mono(y) - 1.0).astype(np.float32); del y
        divk = sum(1j * kv * mesh.fwd(wv * g) for kv, g in zip(mesh.kvec, gb))
        if opt.get("sw") == "T1":   # candidate B's CFG354 T1 switch, computed by CFG359's own code (read-only) on the unit-weight field
            _, info = cfg.forces(mesh, (rho_u - 1.0).astype(np.float32), a, "T1", "FLAT", "canonical", DTA, diag=True)
            fsw = info["_grids"][0]; divk = mesh.fwd(mesh.inv(divk) * fsw)
        phik = phik + divk * mesh.ik2
    return phik, rho_tot, (r.mean() if w > 0 else 1.0)
def run(name):
    opt = RUNS[name]; mesh = cfg.Mesh(NPG); t0 = time.time()
    pos, mom = cfg.initial_conditions(NPG); aa = cfg.step_grid()
    def acc_at(a):
        phik, rho_tot, rbar = fields(mesh, pos, a, opt)
        return mesh.interp([-a * mesh.inv(1j * kv * phik) for kv in mesh.kvec], pos), phik, rho_tot, rbar
    accp, *_ = acc_at(aa[0])
    for n in range(len(aa) - 1):
        a0_, a1 = aa[n], aa[n + 1]; am = math.sqrt(a0_ * a1)
        mom += cfg.quad(lambda x: 1 / (x * x * cfg.E(x)), a0_, am)[0] * accp
        pos = (pos + cfg.quad(lambda x: 1 / (x ** 3 * cfg.E(x)), a0_, a1)[0] * mom) % LBOX
        accp, phik, rho_tot, rbar = acc_at(a1)
        mom += cfg.quad(lambda x: 1 / (x * x * cfg.E(x)), am, a1)[0] * accp
    _, _, s8m = cfg.measure_pk(mesh, rho_tot - 1.0, NPG ** 3)
    dlens = mesh.inv(-(1.0 / (1.5 * Om)) * phik / mesh.ik2.clip(1e-30) * (mesh.ik2 > 0))   # a = 1
    _, _, s8l = cfg.measure_pk(mesh, dlens, NPG ** 3)
    out = dict(name=name, opt=opt, sigma8_matter=s8m, sigma8_lens=s8l, mean_r=float(rbar), t=time.time() - t0)
    json.dump(out, open(os.path.join(WORK, f"cm12_{name}.json"), "w")); print(out, flush=True)
def report():
    R = {n: json.load(open(os.path.join(WORK, f"cm12_{n}.json"))) for n in RUNS if os.path.exists(os.path.join(WORK, f"cm12_{n}.json"))}
    s0m, s0l = R["S0"]["sigma8_matter"], R["S0"]["sigma8_lens"]
    print(f"   box {LBOX} Mpc/h, {NPG}^3; S0 sigma8 matter {s0m:.4f}, lens {s0l:.4f} (absolute values low: small box; use ratios)")
    for n, r in R.items():
        print(f"   {n:8s} sigma8_matter/S0 {r['sigma8_matter']/s0m:.3f}   sigma8_lens/S0 {r['sigma8_lens']/s0l:.3f}   mean bound cold weight {r['mean_r']:.3f}   {r['t']:.0f}s")
    res = []
    ok = abs(R["S0"]["sigma8_lens"] / R["S0"]["sigma8_matter"] - 1) < 0.02
    print(("PASS  " if ok else "FAIL  ") + "K control: without phantom the lensing field equals the matter field (S0 lens/matter within 2%)")
    if "R" in R:
        ok2 = R["R"]["sigma8_matter"] < s0m
        print(("PASS  " if ok2 else "FAIL  ") + "C retention alone lowers sigma8 (direction of cm11)")
if __name__ == "__main__":
    report() if sys.argv[1] == "REPORT" else run(sys.argv[1])
