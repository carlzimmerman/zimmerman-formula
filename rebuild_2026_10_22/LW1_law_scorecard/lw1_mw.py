#!/usr/bin/env python3
"""LW1 Milky Way (FROZEN_CRITERIA.md part 4): X5's 175 cells, the plain law (AQUAL L* = 0, and round rule on Newton), UR3's gate. Checkpoints per cell in cache_mw; rerun resumes.
    python3 lw1_mw.py canonical|alt [--mutate]    then python3 lw1_mw.py --grade
kappa = 1/2 FITTED; not theory closed."""
import itertools, json, math, os, sys
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "X5_mw_joint_baryons")); import x5_lib as L
ns = L.load_p4(); F = L.Family(ns); PS = ns["S"]; vE, eE = L.eilers_target(ns); R0, BR_R, BR_K, BR_E5 = ns["R0_MW"], ns["BR_R"], ns["BR_K"], ns["BR_E5"]; G = 4.30091e-6; KZU = 2 * math.pi * G * 1e6; KZ, KZE = 66.4, 2.2; LK, LO = L.LINE_CHI2, 59.89250004508689
ou = np.loadtxt(os.path.join(L.DATA, "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14); OR, OV = ou[:, 0], ou[:, 1]; OE = np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(OR <= 22.0, 0.03, 0.15) * OV)
CD = os.path.join(HERE, "cache_mw"); os.makedirs(CD, exist_ok=True); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def lines(vc, K, K0, vo):
    cK = float(np.sum(((np.asarray(K) - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((np.asarray(vo) - OV) / OE) ** 2)); return dict(vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO, L1=bool(abs(vc - L.VC_BRIEF) <= L.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE), L2a=bool(cK <= LK), L2b=bool(abs(K0 - KZ) <= 2 * KZE), L3=bool(cO <= LO), D=max(cK / LK, abs(vc - vE) / (2 * eE), cO / LO, abs(K0 - KZ) / (2 * KZE)))
def cell(rhof, a0):
    Mu = PS.mass_unit(a0); g = ns["mw_grid"](6.6e10 / Mu); rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol)); pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0)
    PhiN = pr.solve_newton(); oN = ns["mw_obs"](g, PhiN, a0); Rall = np.r_[R0, OR, BR_R]; vb = L.vc_plane(ns, g, PhiN, a0, Rall)
    Phi, res, it = pr.solve_aqual(); oA = ns["mw_obs"](g, Phi, a0); voA = L.vc_plane(ns, g, Phi, a0, OR)
    a0k = a0 * PS.KPC / 1e6; gb = vb ** 2 / Rall; gc = (0.5 + np.sqrt(0.25 + a0k / np.maximum(gb, 1e-30)) - 1) * gb; nR = 1 + len(OR); vR = np.sqrt(vb ** 2 + Rall * gc); K = np.array(oN["K"]) + gc[nR:] * 1.1 / BR_R / KZU; K0 = oN["K_R0"] + gc[0] * 1.1 / R0 / KZU
    A = lines(oA["vc_R0"], oA["K"], oA["K_R0"], voA); Rr = lines(float(vR[0]), K, float(K0), vR[1:nR])
    A["x5_chi2"] = oA["chi2_kz"]; return dict(A=A, R=Rr, N=dict(vc_R0=oN["vc_R0"], K_R0=oN["K_R0"]), res=float(res), Mb=Mt * Mu)
def spec():
    o = []
    for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID): rhof, p = F.rho(sb, mbb, rd); o.append((dict(sig_b=sb, M_bb=mbb, R_d=rd, Mstar=p["Mstar"], tag_Rd_IN=bool(L.RD_TAG[0] <= rd <= L.RD_TAG[1]), tag_Mstar_IN=bool(L.MSTAR_TAG[0] <= p["Mstar"] <= L.MSTAR_TAG[1])), rhof))
    return o
def run(foot, ax):
    a0 = L.A0_SI[foot] * ax; f = os.path.join(CD, f"{foot}_{ax}.jsonl"); done = [json.loads(l) for l in open(f)] if os.path.exists(f) else []; S = spec()
    if not any(d.get("mcm") for d in done):
        with open(f, "a") as w: w.write(json.dumps(dict(mcm=True, **cell(ns["rho_mcm"], a0))) + "\n")
    nd = sum(1 for d in done if not d.get("mcm"))
    with open(f, "a") as w:
        for i, (c, rhof) in enumerate(S):
            if i < nd: continue
            w.write(json.dumps(dict(c, **cell(rhof, a0))) + "\n"); w.flush()
def classify(rows, form):
    a = [r for r in rows if all(r[form][l] for l in ("L1", "L2a", "L2b", "L3"))]; vk = [r for r in rows if all(r[form][l] for l in ("L1", "L2a", "L2b"))]; x5 = [r for r in rows if r[form]["L1"] and r[form]["L2a"]]
    cls = "FEASIBLE IN PRIORS" if any(r["tag_Rd_IN"] and r["tag_Mstar_IN"] for r in a) else "FEASIBLE (WIDE PRIORS ONLY)" if a else "V+K ONLY" if vk else "INFEASIBLE"
    b = min(rows, key=lambda r: r[form]["D"]); ip = [r for r in rows if r["tag_Rd_IN"] and r["tag_Mstar_IN"]]; bi = min(ip, key=lambda r: r[form]["D"]) if ip else None; ds = lambda r: dict(sig_b=r["sig_b"], M_bb=r["M_bb"], R_d=r["R_d"], Mstar=r["Mstar"], **{k: r[form][k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "D", "L1", "L2a", "L2b", "L3")})
    return dict(cls=cls, n_all=len(a), n_VK=len(vk), n_x5gate=len(x5), counts={l: sum(r[form][l] for r in rows) for l in ("L1", "L2a", "L2b", "L3")}, best=ds(b), best_in_prior=ds(bi) if bi else None, label="PASS" if cls == "FEASIBLE IN PRIORS" else "FAIL", Kz_R0_range_of_x5gate=[min(r[form]["K_R0"] for r in x5), max(r[form]["K_R0"] for r in x5)] if x5 else None)
if "--grade" in sys.argv:
    R = {}; P("LW1 Milky Way, plain law, X5's 175 cells, UR3's gate (L1 v_c, L2a chi2_Kz, L2b K_z(R0), L3 Ou). Form A AQUAL L* = 0; form R round rule on Newton. kappa = 1/2 FITTED; not theory closed"); k6 = 0.0
    for foot in ("canonical", "alt"):
        X = json.load(open(os.path.join(RB, "X5_mw_joint_baryons", f"x5_grid_{foot}.json")))["cells"]; R[foot] = {}
        for ax in (1.0, 1.5):
            ds = [json.loads(l) for l in open(os.path.join(CD, f"{foot}_{ax}.jsonl"))]; m = [d for d in ds if d.get("mcm")][0]; rows = [d for d in ds if not d.get("mcm")]; assert len(rows) == 175
            if ax == 1.0:
                for r, x in zip(rows, X):
                    for a, b in ((r["A"]["x5_chi2"], x["L0"]["chi2_kz"]), (r["A"]["K_R0"], x["L0"]["K_R0"]), (r["A"]["vc_R0"], x["L0"]["vc_R0"])): k6 = max(k6, abs(a / b - 1))
                nf = abs(m["N"]["vc_R0"] - 177.092) if foot == "canonical" else None; nk = abs(m["N"]["K_R0"] - 61.889) if foot == "canonical" else None
                if foot == "canonical": R["K6_newton"] = [nf, nk]; P(f"K6 Newton McMillan V_b {m['N']['vc_R0']:.3f} K_z,b {m['N']['K_R0']:.3f} (GD3 177.092, 61.889)")
            for form in ("A", "R"):
                c = classify(rows, form); c["mcmillan"] = {k: m[form][k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "L1", "L2a", "L2b", "L3")}; R[foot][f"{form}|{ax}"] = c; P(f"[{foot}] {'MUTATE ' if ax != 1 else ''}form {form}: {c['cls']} all4 {c['n_all']} V+K {c['n_VK']} X5-gate (chi2_Kz + v_c) {c['n_x5gate']} K(R0) of those {c['Kz_R0_range_of_x5gate']}; counts {c['counts']}; best D {c['best']['D']:.2f} Rd {c['best']['R_d']:.2f} Vc {c['best']['vc_R0']:.1f} K {c['best']['K_R0']:.1f} chi2Kz {c['best']['chi2_Kz']:.1f} chi2Ou {c['best']['chi2_Ou']:.1f}; in-prior best D {c['best_in_prior']['D'] if c['best_in_prior'] else None:.2f} Vc {c['best_in_prior']['vc_R0']:.1f} K {c['best_in_prior']['K_R0']:.1f}; McMillan Vc {c['mcmillan']['vc_R0']:.1f} K {c['mcmillan']['K_R0']:.1f}: {c['label']}")
    R["K6_rel"] = k6; P(f"K6 AQUAL L* = 0 vs X5's stored L0 max rel |d| {k6:.1e}: {'PASS' if k6 <= 1e-6 else 'FAIL'}"); json.dump(R, open(os.path.join(HERE, "lw1_mw.json"), "w"), indent=1); open(os.path.join(HERE, "lw1_mw.out"), "w").write("\n".join(OUT) + "\n")
else:
    run(sys.argv[1], 1.5 if "--mutate" in sys.argv else 1.0)
