"""CFG102-B: the declared (mu, m2) scan of cfg102_frozen.py: mu_min per layer, mu_uni(m2), H1a, H1b, H2, H3, costs, UV speed, edges.
Run: python3 cfg102_b_scan.py      MUTATE=a (mu = 0 in the mu_uni role) | MUTATE=b (mu -> -mu_uni) must FAIL H1b (rc = 1)."""
import os, sys, math, json, hashlib, multiprocessing as mp
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cfg102_common import *

MUT = os.environ.get("MUTATE", "")
SUF = (("_MUTATE_" + MUT) if MUT else "") + ("_BCN" if FREE_DEFAULT else "")
R = Rep("B" + SUF)
P0 = print
P = R.P
P("frozen doc sha256:", hashlib.sha256(open(os.path.join(HERE, "cfg102_frozen.py"), "rb").read()).hexdigest())
if MUT:
    P(f"  *** MUTATE={MUT} ***")
P("chi0 boundary condition:", "NEUMANN (post-hoc variant)" if FREE_DEFAULT else "Dirichlet (declared main)")
M2S = [10 ** (-16 + 0.5 * i) for i in range(17)]          # 1e-16 .. 1e-8, half decades
LAYERS = {key(z, Mb, f): Layer(z, Mb, f) for (z, Mb, f) in GAL}
KEYS = list(LAYERS)
GF = cost_setup(*FLAG)
GS = cost_setup(SUN[0], SUN[1], SUN[2])
mu_inf = json.load(open(os.path.join(HERE, "cfg102_a_results.json")))["mu_inf"]      # my own control run's per-layer m2 = inf values


def task1(args):
    m2, k = args
    L = LAYERS[k]
    out = {}
    out["mu_min_cons"] = L.mu_min(m2)
    out["mu_min_slaved"] = L.mu_min(m2, "slaved")
    # H1a: mu = 0
    chi, info = L.chi0(0.0, m2)
    cf = L.chi0_on(chi, L.fine)
    out["mu0_nneg"] = max_neg(L.fine, cf, 0.0, m2)
    out["mu0_conv"] = info["converged"]
    # monotonicity probes around mu_min
    mm = out["mu_min_cons"]
    if mm is not None:
        out["above_stable"] = [bool(L.stable(mm * f, m2)) for f in (1.001, 3.0, 10.0, 100.0, 1e3)]
        out["below_stable"] = [bool(L.stable(mm * f, m2)) for f in (0.9, 0.5, 0.1, 0.01)]
    return (m2, k, out)


def task2(args):
    m2, mu, k = args
    L = LAYERS[k]
    out = {}
    mu_used = {"": mu, "a": 0.0, "b": -mu}[MUT]
    chi, info = L.chi0(mu, m2)
    out["conv"] = info["converged"]; out["merit"] = info["merit"]; out["strict"] = info["strict_layer_rel"]
    re_ = L.edge_chi(chi)
    out["edge_ratio"] = None if re_ is None else re_ / L.r_edge_t - 1.0
    # H1b: stability at (1 + 1e-6) mu (or the mutated value); chi0 is re-solved at the value used
    mu_chk = mu_used * (1 + 1e-6) if mu_used > 0 else mu_used
    out["stable_at_mu"] = bool(L.stable(mu_chk, m2)) if mu_used != 0.0 else bool(L.stable(0.0, m2))
    inl = (L.full.t > 0) & (L.full.t < 1)
    fi = (L.fine.t > 0) & (L.fine.t < 1)
    out["uv_layer"] = uv_speed(L.fine, m2, fi)
    out["uv_full"] = uv_speed(L.full, m2)
    return (m2, k, out)


if __name__ == "__main__":
    ctx = mp.get_context("fork")
    RES = {}
    with ctx.Pool(min(14, os.cpu_count() or 4)) as pool:
        t1 = pool.map(task1, [(m2, k) for m2 in M2S for k in KEYS], chunksize=1)
        S1 = {}
        for m2, k, o in t1:
            S1.setdefault(m2, {})[k] = o
        MU = {}
        for m2 in M2S:
            vals = [S1[m2][k]["mu_min_cons"] for k in KEYS]
            MU[m2] = None if any(v is None for v in vals) else max(vals)
        t2 = pool.map(task2, [(m2, MU[m2], k) for m2 in M2S if MU[m2] for k in KEYS], chunksize=1)
    S2 = {}
    for m2, k, o in t2:
        S2.setdefault(m2, {})[k] = o

    P("\nm2 [Pa]     mu_uni [J/m]   set by                  l=sqrt(mu/m2)  edges<=10%  Phi_F/vf2   F/gM       Phi_Sun/vf2   UVspeed[c]  conv")
    ROW = {}
    for m2 in M2S:
        if not MU[m2]:
            P(f"{m2:9.2e}  no stable mu <= 1e34 on some layer"); continue
        mu = MU[m2]
        kset = max(KEYS, key=lambda k: S1[m2][k]["mu_min_cons"])
        edges = [S2[m2][k]["edge_ratio"] for k in KEYS]
        n10 = sum(1 for e in edges if e is not None and abs(e) <= 0.10)
        chiF, infoF = solve_chi0(GF, mu, m2)
        PhiF = phi_chi(GF, infoF, m2)
        fc = flagship_costs(GF, PhiF)
        chiS, infoS = solve_chi0(GS, mu, m2)
        sc = sun_cost(GS, phi_chi(GS, infoS, m2), SUN[3])
        uvl = max(S2[m2][k]["uv_layer"] for k in KEYS)
        uvf = max(S2[m2][k]["uv_full"] for k in KEYS)
        uvF = uv_speed(GF, m2)
        T = n10 == 24
        F_ = abs(fc["phi_over_vf2"]) <= 0.1 and abs(fc["force_over_gM"]) <= 0.023
        S_ = abs(sc) <= 0.1
        conv = all(S2[m2][k]["conv"] for k in KEYS) and infoF["converged"] and infoS["converged"]
        ell_kpc = math.sqrt(mu / m2) / KPC
        ROW[m2] = dict(mu_uni=mu, set_by=kset, ell_kpc=ell_kpc, n_edges_10=n10, edges=edges, phiF=fc["phi_over_vf2"], forceF=fc["force_over_gM"],
                       rF_kpc=fc["rF_kpc"], phiSun=sc, uv_layer=uvl, uv_full=uvf, uv_flag=uvF, T=T, F=F_, S=S_, converged=conv,
                       stable_uni=all(S2[m2][k]["stable_at_mu"] for k in KEYS),
                       mu0_all_unstable=all(S1[m2][k]["mu0_nneg"] > 0 for k in KEYS),
                       mu0_conv=all(S1[m2][k]["mu0_conv"] for k in KEYS),
                       strict_max=max(S2[m2][k]["strict"] for k in KEYS),
                       merit_max=max(S2[m2][k]["merit"] for k in KEYS),
                       flag_info=infoF, sun_info=infoS,
                       mu_min_cons={k: S1[m2][k]["mu_min_cons"] for k in KEYS}, mu_min_slaved={k: S1[m2][k]["mu_min_slaved"] for k in KEYS},
                       monotone_above={k: S1[m2][k].get("above_stable") for k in KEYS}, monotone_below={k: S1[m2][k].get("below_stable") for k in KEYS})
        P(f"{m2:9.2e}  {mu:11.4e}   {kset:22s}  {ell_kpc:9.2f}     {n10:2d}/24    {fc['phi_over_vf2']:+10.4g}  {fc['force_over_gM']:+9.4g}  {sc:+11.4g}   {uvl:8.3g}    {conv}")

    # --------------------------------------------------------------------------------------- checks
    P("\nCHECKS")
    h1a = all(ROW[m2]["mu0_all_unstable"] for m2 in ROW)
    R.check("H1a [load-bearing] mu = 0: all 24 layers unstable at every scanned m2",
            f"{sum(ROW[m2]['mu0_all_unstable'] for m2 in ROW)}/{len(ROW)} m2 values; mu=0 chi0 solves converged on all: {all(ROW[m2]['mu0_conv'] for m2 in ROW)}", h1a)
    h1b = all(ROW[m2]["stable_uni"] for m2 in ROW) and len(ROW) == len(M2S)
    R.check("H1b [load-bearing] at mu = mu_uni(m2) (1.000001x) every layer stable, every scanned m2",
            f"{sum(ROW[m2]['stable_uni'] for m2 in ROW)}/{len(M2S)} m2 values", h1b)
    # H2
    viol, n_h2 = [], 0
    for m2 in ROW:
        for k in KEYS:
            e = ROW[m2]["edges"][KEYS.index(k)]
            if e is None or not (0.5 <= 1 + e <= 2.0):
                continue
            n_h2 += 1
            ratio = ROW[m2]["mu_min_cons"][k] / mu_inf[k]
            if ratio < 0.98:
                viol.append((m2, k, ratio))
    minr = min((ROW[m2]["mu_min_cons"][k] / mu_inf[k], m2, k) for m2 in ROW for k in KEYS
               if ROW[m2]["edges"][KEYS.index(k)] is not None and 0.5 <= 1 + ROW[m2]["edges"][KEYS.index(k)] <= 2.0)
    R.check("H2 [reported] mu_min(layer; m2) >= 0.98 mu_min(layer; inf) on layers with edge within a factor 2",
            f"{n_h2} (m2, layer) pairs; violations {len(viol)}; lowest ratio {minr[0]:.3f} at m2 = {minr[1]:.1e}, {minr[2]}", not viol, load_bearing=False)
    nT = sum(ROW[m2]["T"] for m2 in ROW); nF = sum(ROW[m2]["F"] for m2 in ROW); nS = sum(ROW[m2]["S"] for m2 in ROW)
    nall = sum(ROW[m2]["T"] and ROW[m2]["F"] and ROW[m2]["S"] for m2 in ROW)
    R.check("H3 [reported] exists an m2 with T and F and S", f"T: {nT} values, F: {nF}, S: {nS}, all three: {nall}  (of {len(ROW)} scanned)", nall > 0, load_bearing=False)
    R.check("C5b solver converged (merit <= 1e-8) on every layer, flagship and Sun solve at every scanned (m2, mu_uni)",
            f"all converged: {all(ROW[m2]['converged'] for m2 in ROW)}; worst merit {max(ROW[m2]['merit_max'] for m2 in ROW):.1e}; "
            f"worst strict in-layer relative residual {max(ROW[m2]['strict_max'] for m2 in ROW):.1e} (diagnostic)",
            all(ROW[m2]["converged"] for m2 in ROW))
    # monotonicity of stability in mu
    nb = sum(1 for m2 in ROW for k in KEYS if ROW[m2]["monotone_above"][k] and not all(ROW[m2]["monotone_above"][k]))
    nbl = sum(1 for m2 in ROW for k in KEYS if ROW[m2]["monotone_below"][k] and any(ROW[m2]["monotone_below"][k]))
    R.check("M1 [reported] stability is monotone in mu on the probes: unstable above mu_min (x1.001..1e3): "
            f"{nb} violations; stable below mu_min (x0.9..0.01): {nbl} violations", "(bisection assumes this)", nb == 0 and nbl == 0, load_bearing=False)
    nlb = R.finish(bool(MUT))
    json.dump(dict(m2s=M2S, mu_uni={str(k): v for k, v in MU.items()}, rows={str(k): v for k, v in ROW.items()},
                   checks=[(n, ok, lb) for n, ok, lb in R.checks], keys=KEYS), open(os.path.join(HERE, f"cfg102_b_results{SUF}.json"), "w"), indent=1, default=str)
    sys.exit(1 if nlb else 0)
