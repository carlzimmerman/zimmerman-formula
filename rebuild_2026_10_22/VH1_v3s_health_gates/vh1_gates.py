"""VH1_v3s_health_gates (criteria FROZEN_CRITERIA.md, commit 837119737f).

v3s through Codex's KT40/KT42 health gates, both footings, never pooled:
  G1  Milky Way vertical-force sign (P4's four baryon models + X5's passing cells), P4's solver at L* = 21.7 / 22.9 pc;
  G2  scalar binding virial W = int rho r dphi/dr dV of KT40's four Plummer dwarfs in a uniform external field;
  G3  planets: C6/C6P's hedgehog GM/L*^2 against AZ11's radial and AZ12's precession lines.
P4's solver and X5's MW loader are imported read-only (no bytecode written). The astra lane's AZ12 rate formula is
re-implemented, not imported.  Usage:  python3 vh1_gates.py --part planets|mw|dwarfs|all [--mutate] [--tag RERUN]
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import sys
sys.dont_write_bytecode = True
import math
import json
import time
import argparse
import resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "X5_mw_joint_baryons"))
sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "P4_v3_galaxy_tiles"))
import p4_solver as S                                                   # noqa: E402  (read-only)

CRITERIA = "837119737f"
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR_PC = {"canonical": 21.7, "alt": 22.9}                               # D10 lower bounds (V3_FULL_PICTURE §1)
PC = S.KPC / 1e3
GM_SUN = 1.32712440018e20
AU = 149597870700.0
YR = 365.25 * 86400
MAS = math.pi / (180 * 3600 * 1000)
ECC = dict(Mercury=.206, Venus=.007, Earth=.017, Mars=.093, Jupiter=.048, Saturn=.054)   # AZ12
ETAS = [0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]                                  # KT40 auxiliary Newtonian
UPS = np.linspace(1.0, 3.0, 41)
DWARFS = ("Draco", "Sculptor", "Leo II", "Fornax")
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, passed=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {detail}", flush=True)


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9      # macOS: bytes -> GB


# ===================================================================================================================  G3
def rate(A, a, e, n, N=256):
    """AZ12's first-order eccentric-anomaly average of a radial monopole A(r) (re-implemented)."""
    t, w = np.polynomial.legendre.leggauss(N)
    E = math.pi * (t + 1); c = np.cos(E); r = a * (1 - e * c)
    return math.sqrt(1 - e * e) / (n * a * e) * float(np.sum(.5 * w * A(r) * (c - e)))


def part_planets(mutate=False):
    print("=== G3 planets: hedgehog GM/L*^2 (C6/C6P carried) vs AZ11 radial and AZ12 precession", flush=True)
    tab = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "RQ3_acceptance_v2", "tolerances.json")))["PLANETS"]
    errs = []
    for name, e in ECC.items():
        root = math.sqrt(1 - e * e)
        for fn, orc in ((lambda r: np.ones_like(r), -root), (lambda r: r, -1.5 * root), (lambda r: 1 / r ** 2, 0.0)):
            errs.append(abs(rate(fn, 1.0, e, 1.0) - orc))
    if not mutate:
        check("K6 AZ12 orbit oracles", max(errs) <= 1e-10, f"max err {max(errs):.2e}")
    out = {}
    for f in FOOTS:
        rows = {}
        for Lpc in [LSTAR_PC[f], 24.0, 50.0, 90.0]:
            A = GM_SUN / (Lpc * PC) ** 2 * (1e3 if mutate else 1.0)
            pl = {}
            for name, d in tab.items():
                a = d["a_au"] * AU; e = ECC[name]; n = math.sqrt(GM_SUN / a ** 3)
                sig_r = d["dg_tight"] * max(d["EPM"], d["INPOP"]) / min(d["EPM"], d["INPOP"])
                rt = rate(lambda r: np.full_like(r, A), a, e, n) * YR / MAS
                pl[name] = dict(A_ms2=A, Z_radial_AZ11=A / sig_r, ratio_dg_tight=A / d["dg_tight"],
                                rate_mas_yr=rt, Z_prec_AZ12=abs(rt) / max(d["EPM"], d["INPOP"]))
            ok = all(v["Z_radial_AZ11"] <= 2 and v["Z_prec_AZ12"] <= 2 for v in pl.values())
            rows[f"{Lpc:g}"] = dict(Lstar_pc=Lpc, planets=pl, all_pass=ok)
        prim = rows[f"{LSTAR_PC[f]:g}"]
        worst_r = max(prim["planets"].items(), key=lambda kv: kv[1]["Z_radial_AZ11"])
        worst_p = max(prim["planets"].items(), key=lambda kv: kv[1]["Z_prec_AZ12"])
        label = "PASS" if prim["all_pass"] else "FAIL"
        print(f"  {f}: L* {LSTAR_PC[f]} pc, A {prim['planets']['Mars']['A_ms2']:.3e} m/s^2; worst radial {worst_r[0]} "
              f"Z {worst_r[1]['Z_radial_AZ11']:.4g}; worst precession {worst_p[0]} Z {worst_p[1]['Z_prec_AZ12']:.4g} "
              f"({worst_p[1]['rate_mas_yr']:.4g} mas/yr) -> G3 {label}", flush=True)
        out[f] = dict(label=label, by_Lstar=rows)
    return out


# ===================================================================================================================  G1
def mw_fields(g, Phi):
    dr, dt = g.grad_cells(Phi)
    dz = np.cos(g.t2d) * dr - np.sin(g.t2d) * dt
    dR = np.sin(g.t2d) * dr + np.cos(g.t2d) * dt
    return dz, dR, np.sqrt(dr * dr + dt * dt)


def g1_grade(g, Phi, a0):
    dz, dR, gm = mw_fields(g, Phi)
    R = g.r2d * np.sin(g.t2d); z = g.r2d * np.cos(g.t2d)
    reg = (R <= 25.0) & (z >= 0.02) & (z <= 5.0) & (g.r2d >= 0.1)
    outw = reg & (dz < -1e-3 * gm)
    rel = np.where(reg, dz / np.maximum(gm, 1e-300), np.inf)
    k = int(np.argmin(rel))
    conv = a0 / (2 * math.pi * S.G_SI) / (S.MSUN / PC ** 2)            # dPhi/dz [a0] -> Msun/pc^2 (K_z / 2 pi G)
    p12 = float(g.interp_cells(dz, np.array([12.0]), np.array([0.3]))[0])
    pR0 = float(g.interp_cells(dz, np.array([8.122]), np.array([1.1]))[0])
    return dict(n_region=int(reg.sum()), n_outward=int(outw.sum()),
                min_dz_over_g=float(rel[k]), min_at_Rz=[float(R[k]), float(z[k])],
                dPhidz_12_0p3_Msun_pc2=p12 * conv, K_R0_1p1_Msun_pc2=pR0 * conv,
                label="PASS" if (outw.sum() == 0 and p12 > 0) else "FAIL")


def part_mw(mutate=False, only=None):
    print(f"=== G1 Milky Way vertical-force sign{' (MUTATE: Phi_N - 3(Phi - Phi_N))' if mutate else ''}", flush=True)
    import x5_lib as X                                                   # read-only
    ns = X.load_p4()
    fam = X.Family(ns)
    out = {}
    for f in FOOTS:
        a0 = A0[f]; Mu = S.mass_unit(a0)
        x5 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X5_mw_joint_baryons", f"x5_grid_{f}.json")))
        models = [(k, v) for k, v in ns["BARY"].items()]
        for c in x5["cells"]:
            if c["passes"]:
                models.append((f"X5_{c['sig_b']}_{c['M_bb']:.3g}_{c['R_d']:.4g}", fam.rho(c["sig_b"], c["M_bb"], c["R_d"])[0]))
        if only:
            models = [m for m in models if m[0] in only]
        if mutate:
            best = min((c for c in x5["cells"] if c["passes"]), key=lambda c: c["D"])
            bname = f"X5_{best['sig_b']}_{best['M_bb']:.3g}_{best['R_d']:.4g}"
            models = [m for m in models if m[0] in ("B1_McMillan17", bname)]
        res = {}
        for name, rhof in models:
            t0 = time.time()
            g = ns["mw_grid"](6.6e10 / Mu)
            rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4)
            Mt = 2 * float(np.sum(rho1 * g.vol))
            pr = S.Problem(g, rho1, Mt, 0.0, Lam=LSTAR_PC[f] / 1e3)
            Phi0, res0, _ = pr.solve_aqual()
            Phi0 = Phi0.copy()
            pr.solve(U0=Phi0)
            PhiL, resL = pr.Phi.copy(), pr.res
            row = dict(Mb_Msun=Mt * Mu, res_L0=float(res0), res_L=float(resL))
            if mutate:
                PhiN = pr.solve_newton()
                row["L"] = g1_grade(g, PhiN - 3 * (PhiL - PhiN), a0)
            else:
                row["L"] = g1_grade(g, PhiL, a0)
                row["L0"] = g1_grade(g, Phi0, a0)
                obs = ns["mw_obs"](g, PhiL, a0)
                row["vc_R0_L"] = obs["vc_R0"]; row["chi2_kz_L"] = obs["chi2_kz"]
                if name == "B1_McMillan17" and f == "canonical":
                    K0 = ns["mw_obs"](g, Phi0, a0)["K_R0"]
                    check("K4 P4 reproduction B1 canonical L*=0 K_z(R0)", abs(K0 - 92.3) <= 0.5, f"{K0:.3f} vs 92.3")
                for nm, rr in (("L0", res0), ("L", resL)):
                    check(f"K7 residual {f} {name} {nm}", rr <= 1e-8, f"{rr:.1e}")
            row["solve_s"] = round(time.time() - t0, 1)
            res[name] = row
            L = row["L"]
            print(f"  {f} {name}: outward {L['n_outward']}/{L['n_region']}, min dz/|g| {L['min_dz_over_g']:+.4f} at "
                  f"(R,z)=({L['min_at_Rz'][0]:.2f},{L['min_at_Rz'][1]:.3f}); dPhi/dz(12,0.3) {L['dPhidz_12_0p3_Msun_pc2']:+.2f}; "
                  f"K(R0,1.1) {L['K_R0_1p1_Msun_pc2']:.2f} -> {L['label']}"
                  + ("" if mutate else f"  [L*=0: outward {row['L0']['n_outward']}, {row['L0']['label']}; v_c {row['vc_R0_L']:.1f}]")
                  + f"  ({row['solve_s']} s, RSS {rss_mb():.2f} GB)", flush=True)
        label = "PASS" if all(v["L"]["label"] == "PASS" for v in res.values()) else "FAIL"
        out[f] = dict(label=label, models=res)
        print(f"  {f}: G1 {label}", flush=True)
    if not mutate and not only:
        # K5: X5's best canonical cell at L* = 24 pc
        a0 = A0["canonical"]; Mu = S.mass_unit(a0)
        x5c = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X5_mw_joint_baryons", "x5_grid_canonical.json")))
        best = min((c for c in x5c["cells"] if c["passes"]), key=lambda c: c["D"])          # AMENDMENT A1
        rhof = fam.rho(best["sig_b"], best["M_bb"], best["R_d"])[0]
        g = ns["mw_grid"](6.6e10 / Mu)
        rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4)
        pr = S.Problem(g, rho1, 2 * float(np.sum(rho1 * g.vol)), 0.0, Lam=0.024)
        pr.solve()
        o = ns["mw_obs"](g, pr.Phi, a0)
        check("K5 X5 best canonical cell at L*=24 pc", abs(o["K_R0"] - 76.66) <= 0.5 and abs(o["vc_R0"] - 229.71) <= 0.5,
              f"K_z {o['K_R0']:.3f} (76.66), v_c {o['vc_R0']:.3f} (229.71)")
    return out


# ===================================================================================================================  G2
def dwarf_sample():
    import csv
    rows = {}
    with open(os.path.join(REPO, "real_research", "data", "dsph", "mcconnachie2012_dsph.csv")) as h:
        for d in csv.DictReader(h):
            if d["Name"] in DWARFS:
                rows[d["Name"]] = dict(L=10 ** (-.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3,
                                       obs=float(d["sigma*"]), err=float(d["e_sigma*"]),
                                       MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0)
    assert set(rows) == set(DWARFS)
    return rows


def dwarf_grid(a, M, ge, nper, Nt):
    r_out = S.r_out_for(M, ge, 10 * a)
    return S.Grid(S.log_edges(1e-3 * a, r_out, nper), S.theta_edges(Nt, full=True))


def virial(g, rho, Phi):
    dr, dt = g.grad_cells(Phi)
    m = rho * g.vol
    W = float(np.sum(m * g.r2d * dr))
    Fz = float(np.sum(m * (np.cos(g.t2d) * dr - np.sin(g.t2d) * dt)))
    Fabs = float(np.sum(m * np.sqrt(dr * dr + dt * dt)))
    return W, Fz, Fabs


def solve_dwarf(a, M, ge, Lam, nper, Nt):
    g = dwarf_grid(a, M, ge, nper, Nt)
    rho = g.rho_spherical(S.plummer_M(M, a))
    pr = S.Problem(g, rho, M, ge, Lam=Lam)
    Phi0, res0, _ = pr.solve_aqual()
    Phi0 = Phi0.copy()
    out = dict(L0=virial(g, rho, Phi0), res_L0=float(res0))
    if Lam > 0:
        pr.solve(U0=Phi0)
        out["L"] = virial(g, rho, pr.Phi); out["res_L"] = float(pr.res)
    PhiN = pr.solve_newton()
    out["N"] = virial(g, rho, PhiN)
    out["Mgrid"] = float(np.sum(rho * g.vol))
    return out


def part_dwarfs(mutate=False):
    print(f"=== G2 dwarf scalar virial in a uniform external field{' (MUTATE: W_N - 3(W - W_N))' if mutate else ''}", flush=True)
    D = dwarf_sample()
    out = {}
    if not mutate:
        for f in FOOTS:
            a0 = A0[f]; Mu = S.mass_unit(a0); u2 = a0 * S.KPC / 1e6
            # K1 Newtonian Plummer virial (Draco, Upsilon 2)
            d = D["Draco"]; M = (2 * d["L"] + 1.33 * d["MHI"]) / Mu
            r = solve_dwarf(d["a"], M, 0.0, 0.0, 16, 32)
            sN = r["N"][0] / (3 * r["Mgrid"]) * u2; sA = math.pi * M / (32 * d["a"]) * u2
            check(f"K1 Newtonian Plummer virial {f}", abs(sN / sA - 1) <= 0.01, f"{sN:.5f} vs {sA:.5f} (km/s)^2")
            # K2 deep-MOND isolated AQUAL Plummer: (2/9) sqrt(G M a0)
            Md = 1e-3 / Mu * 1.0; ad = 1.0                              # 1e3 Msun at a = 1 kpc: GM/a^2 << a0
            r = solve_dwarf(ad, Md, 0.0, 0.0, 16, 32)
            sD = r["L0"][0] / (3 * r["Mgrid"]); sM = (2 / 9) * math.sqrt(Md)
            check(f"K2 deep-MOND AQUAL virial {f}", abs(sD / sM - 1) <= 0.02, f"{sD:.6e} vs {sM:.6e} (a0 kpc), GM/a^2 {Md:.1e} a0")
    for f in FOOTS:
        a0 = A0[f]; Mu = S.mass_unit(a0); u2 = a0 * S.KPC / 1e6; Lam = LSTAR_PC[f] / 1e3
        objs = {}
        for name in DWARFS:
            d = D[name]
            rows = []
            for eta in (ETAS if not mutate else [0.0, 0.01]):
                ge = 0.0 if eta == 0 else eta * float(S.nu1(eta))
                t0 = time.time()
                for iu, U in enumerate(UPS):
                    ladder = (not mutate) and (iu in (0, 20, 40))
                    M = (U * d["L"] + 1.33 * d["MHI"]) / Mu
                    r = solve_dwarf(d["a"], M, ge, Lam, 16, 32)
                    W, Fz, Fabs = r["L"]; WN = r["N"][0]; W0 = r["L0"][0]
                    if mutate:
                        W = WN - 3 * (W - WN)
                    row = dict(U=float(U), eta=eta, ge=ge, W=W, W_L0=W0, W_N=WN,
                               s2_L=W / (3 * r["Mgrid"]) * u2, s2_L0=W0 / (3 * r["Mgrid"]) * u2, s2_N=WN / (3 * r["Mgrid"]) * u2,
                               self_force_rel=abs(Fz) / Fabs, res_L=r["res_L"], res_L0=r["res_L0"])
                    if ladder:
                        rb = solve_dwarf(d["a"], M, ge, Lam, 24, 48)
                        row["W_gridB"] = rb["L"][0]; row["s2_L_gridB"] = rb["L"][0] / (3 * rb["Mgrid"]) * u2
                        row["sign_agree"] = bool((rb["L"][0] > 0) == (W > 0))
                        row["rel_gridB"] = abs(rb["L"][0] / W - 1)
                    rows.append(row)
                print(f"  {f} {name} eta {eta:g} (ge {ge:.4g} a0): sigma_W U1/U2/U3 "
                      + " / ".join(f"{math.copysign(math.sqrt(abs(rows[-41 + i]['s2_L'])), rows[-41 + i]['s2_L']):.3f}" for i in (0, 20, 40))
                      + f" km/s; min W {min(x['W'] for x in rows[-41:]):+.3e}; [L*=0 U2 {math.sqrt(max(rows[-21]['s2_L0'], 0)):.3f}]"
                      + f" ({time.time() - t0:.0f} s, RSS {rss_mb():.2f} GB)", flush=True)
            objs[name] = rows
        allrows = [x for v in objs.values() for x in v]
        nneg = sum(1 for x in allrows if x["W"] <= 0)
        lad = [x for x in allrows if "sign_agree" in x]
        lad_ok = all(x["sign_agree"] for x in lad)
        if not mutate:
            mx = max(x["self_force_rel"] for x in allrows if x["eta"] > 0)
            check(f"K3 momentum {f}", mx <= 2e-2, f"max |F_z|/int rho|g| {mx:.2e}")
            mres = max(max(x["res_L"], x["res_L0"]) for x in allrows)
            check(f"K7 dwarf residuals {f}", mres <= 1e-8, f"max {mres:.1e}")
        label = "NO VERDICT" if not lad_ok else ("PASS" if nneg == 0 else "FAIL")
        below_iso = sum(1 for nm, v in objs.items() for x in v
                        if x["eta"] > 0 and x["W"] < next(y["W"] for y in v if y["eta"] == 0 and y["U"] == x["U"]))
        obs_pass = {nm: sorted({x["eta"] for x in v if x["s2_L"] > 0 and abs(math.sqrt(x["s2_L"]) - D[nm]["obs"]) <= 2 * D[nm]["err"]})
                    for nm, v in objs.items()}
        out[f] = dict(label=label, n_config=len(allrows), n_nonpositive=nneg, n_below_isolated=below_iso,
                      ladder_n=len(lad), ladder_sign_agree=lad_ok,
                      ladder_max_rel=max((x["rel_gridB"] for x in lad), default=None),
                      observed_sigma_pass_etas_context=obs_pass, objects=objs)
        print(f"  {f}: {len(allrows)} configs, W <= 0 in {nneg}, below isolated {below_iso}; ladder sign agree {lad_ok} "
              f"(max rel {out[f]['ladder_max_rel']}) -> G2 {label}", flush=True)
    return out


# ===================================================================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="all", choices=["planets", "mw", "dwarfs", "all"])
    ap.add_argument("--mutate", action="store_true")
    ap.add_argument("--tag", default="")
    ap.add_argument("--only", nargs="*", default=None)
    a = ap.parse_args()
    t0 = time.time()
    res = dict(lane="VH1_v3s_health_gates", criteria=CRITERIA, mutate=a.mutate, Lstar_pc=LSTAR_PC, a0=A0)
    parts = ["planets", "mw", "dwarfs"] if a.part == "all" else [a.part]
    for p in parts:
        res[p] = {"planets": part_planets, "mw": lambda m: part_mw(m, a.only), "dwarfs": part_dwarfs}[p](a.mutate)
    res["checks"] = CHECKS
    res["runtime_s"] = round(time.time() - t0, 1); res["peak_rss_GB"] = round(rss_mb(), 3)
    name = f"vh1_{a.part}" + ("_MUTATE" if a.mutate else "") + (f"_{a.tag}" if a.tag else "")
    with open(os.path.join(HERE, name + ".json"), "w") as h:
        json.dump({k: v for k, v in res.items() if k not in ("runtime_s", "peak_rss_GB")}, h, indent=1, sort_keys=True)
        h.write("\n")
    with open(os.path.join(HERE, name + "_runtime.json"), "w") as h:
        json.dump(dict(runtime_s=res["runtime_s"], peak_rss_GB=res["peak_rss_GB"]), h)
    bad = [c for c in CHECKS if not c["passed"]]
    print(f"checks {len(CHECKS) - len(bad)}/{len(CHECKS)} pass; runtime {res['runtime_s']} s; peak RSS {res['peak_rss_GB']} GB", flush=True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
