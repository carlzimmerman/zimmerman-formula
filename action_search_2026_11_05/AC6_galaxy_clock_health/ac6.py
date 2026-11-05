"""AC6: is AC2's dark-energy clock healthy inside galaxies? Criteria FROZEN_CRITERIA.md (4ae1062cfc).
Part A: sympy derivation (clock in place of H4's dust). Part B: H4's own AQUAL solver, imported unchanged, parallel over systems.
Run from the repository root: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 action_search_2026_11_05/AC6_galaxy_clock_health/ac6.py
AC6_MUTATE=1 flips the sign of the first-order term (H4's convention) and writes separate outputs.
Kappa = 1/2 FITTED; not theory closed. No dark-matter particle."""
import json, math, os, sys, time, importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("AC6_MUTATE", "0") == "1"
SGN = -1 if MUTATE else 1
TAG = "_MUTATE" if MUTATE else ""
H4P = os.path.join(ROOT, "rebuild_2026_10_22", "H4_v3_saddle_stability", "h4_v3_saddle_stability.py")


def load_h4():
    spec = importlib.util.spec_from_file_location("h4", H4P)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


checks, res, lines = [], {"mutate": MUTATE, "sign_first_order_term": SGN}, []


def log(s=""):
    print(s, flush=True); lines.append(s)


def check(cid, ok, value, thr):
    checks.append({"id": cid, "pass": bool(ok), "value": value, "threshold": thr})
    log(f"  [{'PASS' if ok else 'FAIL'}] {cid}: {value} (line: {thr})")


def part_a():
    import sympy as sp
    from sympy.calculus.euler import euler_equations
    log("A: derivation (sympy)")
    t, x, y, z = X = sp.symbols("t x y z", real=True)
    K, gL, s, muK = sp.symbols("K gamma_L s mu_K", positive=True)
    phi = sp.Function("phi")(*X); sig = sp.Function("sigma")(*X)
    Pf = [sp.Function(f"P{i}")(*X) for i in range(3)]
    rhom = sp.Function("rho_m")(x, y, z); Wf = sp.Function("W"); xs = (x, y, z)
    grad = lambda f: [sp.diff(f, v) for v in xs]
    div = lambda F: sum(sp.diff(F[i], xs[i]) for i in range(3))
    Xi = phi - sp.diff(sig, t) + sum(d ** 2 for d in grad(sig)) / 2
    modP = sp.sqrt(sum(p ** 2 for p in Pf))
    Cl = s ** 2 / 2 * ((1 + sp.diff(sig, t)) ** 2 / (1 + phi) ** 2 - sum(d ** 2 for d in grad(sig)))
    L = (-sum(d ** 2 for d in grad(phi)) / (2 * K) - rhom * phi + sum(Pf[i] * sp.diff(Xi, xs[i]) for i in range(3))
         - Wf(K * modP) - gL / 2 * div(Pf) ** 2 + Cl)
    eqs = euler_equations(L, [phi, sig] + Pf, X)
    rho_t = div(Pf) + s ** 2 * (1 + sp.diff(sig, t)) / (1 + phi) ** 2
    rho_x = div(Pf) + s ** 2
    v = [-d for d in grad(sig)]
    cont = sp.diff(rho_t, t) + div([rho_x * v[i] for i in range(3)])
    r_sig = sp.simplify(sp.expand(eqs[1].lhs + cont))
    rho_grav = s ** 2 * (1 + sp.diff(sig, t)) ** 2 / (1 + phi) ** 3
    r_phi = sp.simplify(sp.expand(eqs[0].lhs - (sum(sp.diff(phi, v_, 2) for v_ in xs) / K - rhom - div(Pf) - rho_grav)))
    check("A1", r_sig == 0 and r_phi == 0,
          f"sigma-EL = -[d_t(divP + s^2(1+sigma_t)/(1+phi)^2) + div((divP + s^2) v)], residual {r_sig}; "
          f"Poisson with clock density s^2(1+sigma_t)^2/(1+phi)^3, residual {r_phi}", "identically 0")
    res["A1"] = {"rho_eff_background": "div P + s^2", "continuity_residual": str(r_sig), "poisson_residual": str(r_phi)}

    k, om, r0, th, ML, MT = sp.symbols("k omega rho_0 theta M_L M_T", positive=True)
    dphi, dsig, dXi, drho = sp.symbols("dphi dsigma dXi drho"); dP = sp.symbols("dP0:3"); dPv = sp.Matrix(dP)
    kh = sp.Matrix([0, 0, 1]); Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hm = K * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T); W2 = sp.Symbol("W2")

    def solve_det(eqs_, unk):
        M = sp.linear_eq_to_matrix(eqs_, unk)[0]
        det = sp.factor(sp.simplify(M.det()))
        return sp.solve(sp.Eq(det.subs(om, sp.sqrt(W2)), 0), W2)

    def clock(gam, sgn):
        Peq = sp.I * k * kh * dXi - gam * k ** 2 * kh * (kh.dot(dPv)) - Hm * dPv
        drt = sp.I * k * kh.dot(dPv) + s ** 2 * (-sp.I * om * dsig - 2 * dphi)
        pois = -k ** 2 * dphi - K * (sp.I * k * kh.dot(dPv) + s ** 2 * (-2 * sp.I * om * dsig - 3 * dphi))
        ce = -sp.I * om * drt + sgn * r0 * k ** 2 * dsig
        be = dXi - (dphi + sp.I * om * dsig)
        return solve_det([pois, ce, be] + list(Peq), [dphi, dsig, dXi] + list(dP))

    def dust(sgn):   # H4 A4's own system, rebuilt (known answer i)
        Peq = sp.I * k * kh * dXi - gL * k ** 2 * kh * (kh.dot(dPv)) - Hm * dPv
        eqs_ = [-k ** 2 * dphi - K * drho, drho - (sp.I * k * kh.dot(dPv) - muK ** 2 * dXi / K),
                -sp.I * om * drho + sgn * r0 * k ** 2 * dsig, dXi - (dphi + sp.I * om * dsig)] + list(Peq)
        return solve_det(eqs_, [dphi, dsig, dXi, drho] + list(dP))

    Mth = 1 / (sp.cos(th) ** 2 / ML + sp.sin(th) ** 2 / MT)
    chi = k ** 2 / (K * Mth + gL * k ** 2) + muK ** 2 / K
    sd = dust(1)
    r_i = sp.simplify(sd[0] - r0 * (k ** 2 / chi - K)) if len(sd) == 1 else "no unique root"
    sc = clock(gL, SGN)
    r_ii = sp.simplify(sc[0].subs(s, 0) - SGN * K * r0 * (Mth - 1 + gL * k ** 2 / K)) if len(sc) == 1 else "n/a"
    uv = sp.simplify(sp.limit(sc[0] / k ** 2, k, sp.oo)) if len(sc) == 1 else None
    r_uv = sp.simplify(uv - SGN * gL * r0 / (1 + gL * s ** 2)) if uv is not None else "n/a"
    ssw = clock(0, SGN)
    uv_sw_k2 = sp.limit(ssw[0] / k ** 2, k, sp.oo) if len(ssw) == 1 else None
    uv_sw = sp.simplify(sp.limit(ssw[0], k, sp.oo)) if len(ssw) == 1 else None
    r_sw = sp.simplify(uv_sw - SGN * K * r0 * (Mth - 1)) if uv_sw is not None else "n/a"
    check("A2", r_i == 0 and r_ii == 0 and len(sc) == 1,
          f"H4 dust system rebuilt minus rho_tau(k^2/chi - K): {r_i}; clock s->0 minus H4 mu_K=0 form: {r_ii}",
          "identically 0")
    check("A3", r_uv == 0, f"clock UV limit omega^2/k^2 = {uv} (minus SGN gamma rho_0/(1+gamma s^2): {r_uv})",
          "identically 0: Gamma ~ k wherever SGN*rho_0 < 0")
    check("A4", uv_sw_k2 == 0 and r_sw == 0,
          f"switched (gamma = 0 where D.P < 0): omega^2/k^2 -> {uv_sw_k2}, omega^2 -> {uv_sw} "
          f"(minus SGN K rho_0 (M_theta - 1): {r_sw})", "k-independent bounded limit")
    res["A"] = {"omega2_clock": str(sc[0]), "uv_over_k2": str(uv), "switched_uv": str(uv_sw)}


A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5
OFFSETS = (0.1, 1.0, 2.0)          # (1 + w)


def build_specs(h4):
    KPC, MPC, MSUN, G_SI = h4.KPC, h4.MPC, h4.MSUN, h4.G_SI
    SYS = {
        "S1_MW-M31": {"L": 780 * KPC, "Mu": 6.0e10, "m": [(1.0, 0.5, 3.0), (1.0e11 / 6.0e10, -0.5, 4.0)], "e": (0, 0.01)},
        "S2_LMC-MW": {"L": 50 * KPC, "Mu": 6.0e10, "m": [(1.0, 0.5, 3.0), (3.0e9 / 6.0e10, -0.5, 1.5)], "e": (0,)},
        "S3_galaxy_pair": {"L": 300 * KPC, "Mu": 5.0e10, "m": [(1.0, 0.5, 3.0), (1.0, -0.5, 3.0)], "e": (0, 0.01)},
        "S4_cluster_pair": {"L": 3 * MPC, "Mu": 1.5e14, "m": [(1.0, 0.5, 300.0), (1.0e14 / 1.5e14, -0.5, 250.0)], "e": (0, 0.01)},
        "S6_single_in_field": {"L": 100 * KPC, "Mu": 6.0e10, "m": [(1.0, 0.0, 3.0)], "e": (0.01,)},
    }
    DISCS = {"S5a_MW_disc": {"Rd": 2.6, "Md": 5e10, "hz": 0.3, "bulge": (1e10, 0.6)},
             "S5b_dwarf_disc": {"Rd": 1.5, "Md": 1e9, "hz": 0.2, "bulge": None}}
    specs, meta = [], {}
    for foot, a0 in h4.A0.items():          # H4's footings (9.36e-11 / 1.13e-10) for the maps, as in H4
        for sname, S in SYS.items():
            a0h = a0 * S["L"] ** 2 / (G_SI * S["Mu"] * MSUN)
            masses = [(M, zc, b * h4.PC * 1e3 / S["L"]) for (M, zc, b) in S["m"]]
            Mtot = sum(M for M, _, _ in masses); zc = sum(M * z_ for M, z_, _ in masses) / Mtot
            for e_ in S["e"]:
                re = math.sqrt(Mtot * a0h) / (e_ * a0h) if e_ > 0 else 0.0
                box = 60.0 if e_ == 0 else max(60.0, 15 * re)
                nm = f"{sname}|{foot}|e{e_}"
                specs.append({"name": nm, "kind": "pair", "deep": False, "masses": masses, "Mtot": Mtot, "zc": zc,
                              "a0h": a0h, "eh": e_, "box": box})
                meta[nm] = {"L_m": S["L"], "Mu_kg": S["Mu"] * MSUN, "foot": foot, "system": sname, "e": e_, "zc": zc,
                            "near_r": (3 * re if e_ > 0 else 2.0) if sname.startswith("S6") or e_ == 0 else max(2.0, 3 * re)}
        for dname, D in DISCS.items():
            L = D["Rd"] * KPC
            a0h = a0 * L ** 2 / (G_SI * D["Md"] * MSUN)
            bulge = (D["bulge"][0] / D["Md"], D["bulge"][1] / D["Rd"]) if D["bulge"] else None
            Mtot = 1.0 + (bulge[0] if bulge else 0.0)
            for e_ in (0, 0.01):
                re = math.sqrt(Mtot * a0h) / (e_ * a0h) if e_ > 0 else 0.0
                box = 200.0 if e_ == 0 else max(200.0, 15 * re)
                nm = f"{dname}|{foot}|e{e_}"
                specs.append({"name": nm, "kind": "disc", "deep": False, "hz": D["hz"] / D["Rd"], "bulge": bulge,
                              "Mtot": Mtot, "zc": 0.0, "a0h": a0h, "eh": e_, "box": box})
                meta[nm] = {"L_m": L, "Mu_kg": D["Md"] * MSUN, "foot": foot, "system": dname, "e": e_, "zc": 0.0,
                            "near_r": 50.0 if e_ == 0 else 3 * re}
    return specs, meta


def worker(spec):
    os.environ["OMP_NUM_THREADS"] = "1"
    return load_h4().run_case(spec)


def stats(lv, M, offset_si, zone):
    conv = M["Mu_kg"] / M["L_m"] ** 3
    rho = lv["rho"] * conv + offset_si
    val = np.isfinite(rho)
    neg = val & (SGN * rho < 0)
    if zone == "near":
        neg &= np.sqrt(lv["RR"] ** 2 + (lv["ZZ"] - M["zc"]) ** 2) < M["near_r"]
    if not neg.any():
        return {"empty": True, "V_m3": 0.0}
    w = lv["V"][neg]; a_ = np.abs(rho[neg]); o_ = np.argsort(a_); cw = np.cumsum(w[o_]) / w.sum()
    return {"empty": False, "V_m3": float(w.sum()) * M["L_m"] ** 3, "median_abs_rho": float(a_[o_][np.searchsorted(cw, 0.5)])}


def part_b():
    import concurrent.futures as cf, multiprocessing as mp
    h4 = load_h4()
    specs, meta = build_specs(h4)
    log(f"B: {len(specs)} maps with H4's solver, parallel")
    t0 = time.time(); out = {}
    with cf.ProcessPoolExecutor(max_workers=12, mp_context=mp.get_context("spawn"), max_tasks_per_child=1) as ex:
        futs = {ex.submit(worker, sp_): sp_["name"] for sp_ in specs}
        for f in cf.as_completed(futs):
            r = f.result(); out[r["name"]] = r
            log(f"  solved {r['name']:34s} ({r['time_s']:.0f} s, child RSS {r['rss_GB']:.2f} GB, t={time.time()-t0:.0f}s)")
    rho_de = {foot: a0 ** 2 / (KAPPA ** 2 * h4.c_SI ** 2 * h4.G_SI) for foot, a0 in A0.items()}
    log(f"  framework-native rho_DE = a0^2/(kappa^2 c^2 G): canonical {rho_de['canonical']:.4e}, alt {rho_de['alt']:.4e} kg/m^3 "
        f"({rho_de['canonical']/h4.MSUN_PC3:.3e} / {rho_de['alt']/h4.MSUN_PC3:.3e} Msun/pc^3)")
    # known answer: H4's own f = 3 dust offset reproduces H4's stored S2 near-zone fine medians
    h4res = json.load(open(H4P.replace(".py", "_results.json")))
    ka = []
    for foot in ("canonical", "alt"):
        nm = f"S2_LMC-MW|{foot}|e0"
        mine = stats(out[nm]["levels"]["fine"], meta[nm], 3 * h4.RHO_K, "near")
        theirs = h4res["regions"][nm]["f3"]["fine"]["near"]
        rel = abs(mine["median_abs_rho"] / theirs["median_abs_rho"] - 1)
        ka.append(rel)
        log(f"  known answer {nm}: median {mine['median_abs_rho']:.6e} vs H4 {theirs['median_abs_rho']:.6e} (rel {rel:.2e})")
    check("B0", max(ka) <= 0.01, f"max rel diff {max(ka):.2e}", "<= 1 % (H4 S2 near-zone fine medians, f = 3)")
    table = {}
    for nm, M in meta.items():
        table[nm] = {}
        for ow in OFFSETS:
            off = ow * rho_de[M["foot"]]
            row = {}
            for zone in ("box", "near"):
                b_ = stats(out[nm]["levels"]["base"], M, off, zone); f_ = stats(out[nm]["levels"]["fine"], M, off, zone)
                if b_["empty"] and f_["empty"]:
                    conv = True
                elif b_["empty"] != f_["empty"]:
                    conv = False
                else:
                    conv = abs(f_["V_m3"] / b_["V_m3"] - 1) <= 0.10 and abs(f_["median_abs_rho"] / b_["median_abs_rho"] - 1) <= 0.10
                row[zone] = {"fine": f_, "base": b_, "converged": conv}
            table[nm][f"1+w={ow}"] = row
    res["B_maps"] = table
    res["rho_DE_kg_m3"] = rho_de
    # verdict rows
    systems = sorted({M["system"] for M in meta.values()})
    summ = {}
    for ow in OFFSETS:
        summ[ow] = {}
        for sysn in systems:
            per = {}
            for foot in A0:
                nms = [nm for nm, M in meta.items() if M["system"] == sysn and M["foot"] == foot]
                neg_conv = [nm for nm in nms if not table[nm][f"1+w={ow}"]["box"]["fine"]["empty"] and table[nm][f"1+w={ow}"]["box"]["converged"]]
                neg_any = [nm for nm in nms if not table[nm][f"1+w={ow}"]["box"]["fine"]["empty"]]
                med = [table[nm][f"1+w={ow}"]["box"]["fine"]["median_abs_rho"] / h4.MSUN_PC3 for nm in neg_any]
                per[foot] = {"neg_converged": neg_conv, "neg_any": neg_any, "median_Msun_pc3": med}
            summ[ow][sysn] = per
            log(f"  1+w={ow:<4} {sysn:20s} canonical: {len(per['canonical']['neg_converged'])}/{len(per['canonical']['neg_any'])} "
                f"conv/neg maps, medians {[f'{m:.1e}' for m in per['canonical']['median_Msun_pc3']]}; alt: "
                f"{len(per['alt']['neg_converged'])}/{len(per['alt']['neg_any'])}")
    res["B_summary"] = {str(k_): v for k_, v in summ.items()}
    ill_2 = [sysn for sysn in systems if summ[2.0][sysn]["canonical"]["neg_converged"] and summ[2.0][sysn]["alt"]["neg_converged"]]
    healthy_01 = all(not summ[0.1][sysn][f]["neg_any"] for sysn in systems for f in A0)
    res["ill_posed_systems_at_1+w=2"] = ill_2
    res["no_region_at_1+w=0.1"] = healthy_01
    # AC2s bounded branch rates (not graded): Gamma_b = sqrt(4 pi G |rho| ((1+x)^2 - 1)) at x = 1 (illustrative), per Gyr
    K4 = 4 * math.pi * h4.G_SI
    rates = {}
    for sysn in ill_2:
        for foot in A0:
            for m_ in summ[2.0][sysn][foot]["median_Msun_pc3"]:
                rates.setdefault(f"{sysn}|{foot}", []).append(math.sqrt(K4 * m_ * h4.MSUN_PC3 * 3.0) * h4.GYR)
    res["AC2s_bounded_efolds_per_Gyr_at_x1"] = rates
    return ill_2, healthy_01


def main():
    T0 = time.time()
    log(f"AC6 (mutate = {MUTATE}); kappa = 1/2 FITTED; not theory closed")
    part_a()
    a_ok = all(c["pass"] for c in checks)
    ill_2, healthy_01 = part_b()
    if not a_ok or not all(c["pass"] for c in checks):
        label = "NO VERDICT (a check failed)"
    elif ill_2:
        label = "AC2 ILL-POSED (unswitched); AC2s bounded"
    elif healthy_01:
        label = "AC2 HEALTHY at this order"
    else:
        label = "UNDECIDED"
    res["label"] = label; res["checks"] = checks; res["runtime_s"] = time.time() - T0
    log(f"LABEL: {label}; systems ill-posed at 1+w=2 on both footings with converged maps: {ill_2}")
    with open(os.path.join(HERE, f"ac6_results{TAG}.json"), "w") as f:
        json.dump(res, f, indent=1, default=str)
    with open(os.path.join(HERE, f"ac6{TAG}.out"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
