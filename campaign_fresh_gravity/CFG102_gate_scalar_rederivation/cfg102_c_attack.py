"""CFG102-C: the ATTACK items A1-A6 of cfg102_frozen.py (all reported, none load-bearing).  Needs cfg102_b_results.json (the main scan)."""
import os, sys, math, json, hashlib, multiprocessing as mp
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cfg102_common import *

R = Rep("C")
P = R.P
P("frozen doc sha256:", hashlib.sha256(open(os.path.join(HERE, "cfg102_frozen.py"), "rb").read()).hexdigest())
SUF = "_BCN" if FREE_DEFAULT else ""
P("chi0 boundary condition:", "NEUMANN (post-hoc variant)" if FREE_DEFAULT else "Dirichlet (declared main)")
B = json.load(open(os.path.join(HERE, f"cfg102_b_results{SUF}.json")))
KEYS = B["keys"]
ROWS = {float(k): v for k, v in B["rows"].items()}
M2S = sorted(ROWS)
mu_inf = json.load(open(os.path.join(HERE, "cfg102_a_results.json")))["mu_inf"]
LAYERS = {key(z, Mb, f): Layer(z, Mb, f) for (z, Mb, f) in GAL}
GF = cost_setup(*FLAG)
GS = cost_setup(SUN[0], SUN[1], SUN[2])

# --------------------------------------------------------------------------- A1 / A2 / A3 from the scan
P("\nA1  per-layer mu_min [J/m] (consistent chi0) at m2 = 1e-12, 1e-16, and the m2 = inf control; and who sets mu_uni")
m12, m16 = 1e-12, 1e-16
close = lambda x: min(M2S, key=lambda v: abs(math.log10(v) - math.log10(x)))
m12, m16 = close(1e-12), close(1e-16)
P(f"    {'layer':24s} {'m2=1e-12':>12s} {'m2=1e-16':>12s} {'m2=inf':>12s}   ratio(1e-12/inf)")
for k in KEYS:
    P(f"    {k:24s} {ROWS[m12]['mu_min_cons'][k]:12.4e} {ROWS[m16]['mu_min_cons'][k]:12.4e} {mu_inf[k]:12.4e}   {ROWS[m12]['mu_min_cons'][k] / mu_inf[k]:.4f}")
P("    layer setting mu_uni per m2:  " + "; ".join(f"{m:.0e}: {ROWS[m]['set_by']}" for m in M2S))
sets = {}
for m in M2S:
    sets[ROWS[m]["set_by"]] = sets.get(ROWS[m]["set_by"], 0) + 1
P("    tally:", sets)

P("\nA2  chi0 = t (slaved, same g_eff) vs consistent chi0: mu_uni ratio per m2")
for m in M2S:
    ms = max(v for v in ROWS[m]["mu_min_slaved"].values())
    mc = max(v for v in ROWS[m]["mu_min_cons"].values())
    per = [ROWS[m]["mu_min_slaved"][k] / ROWS[m]["mu_min_cons"][k] for k in KEYS]
    P(f"    m2 = {m:8.1e}: mu_uni(slaved)/mu_uni(consistent) = {ms / mc:.4f};  per layer {min(per):.3f}..{max(per):.3f}")

P("\nA3  tracking tolerance: layers within tol of the t-edge, per m2 (chi0 = 1/2 radius / t = 1/2 radius - 1)")
TOLS = (0.10, 0.20, 0.30, 0.50, 1.00)
P("    m2        " + "  ".join(f"<={int(t * 100):3d}%" for t in TOLS) + "   no-crossing")
for m in M2S:
    e = ROWS[m]["edges"]
    P(f"    {m:8.1e}  " + "  ".join(f"{sum(1 for x in e if x is not None and abs(x) <= t):5d}" for t in TOLS) + f"   {sum(1 for x in e if x is None)}")
for t in TOLS:
    ok = [m for m in M2S if sum(1 for x in ROWS[m]['edges'] if x is not None and abs(x) <= t) == 24]
    P(f"    smallest scanned m2 with 24/24 within {int(t * 100)}%: {min(ok) if ok else 'none'}")
P(f"    layers failing the 10% line at m2 = {m16:.0e} (signed edge error r_chi/r_t - 1):")
for k, e in zip(KEYS, ROWS[m16]["edges"]):
    if e is None or abs(e) > 0.10:
        P(f"       {k:24s} {('none' if e is None else f'{e:+.3f}')}")
P("    layers failing the 10% line at m2 = 1e-12:", [k for k, e in zip(KEYS, ROWS[m12]["edges"]) if e is None or abs(e) > 0.10])


# --------------------------------------------------------------------------- A4 the plane, extended
def task_mu(args):
    m2, k = args
    return (m2, k, LAYERS[k].mu_min(m2))


FACS = (1.0, 2.0, 5.0, 10.0, 100.0)


def task_pt(args):
    m2, mu, k, f = args
    L = LAYERS[k]
    chi, info = L.chi0(mu * f, m2)
    e = L.edge_chi(chi)
    st = bool(L.stable(mu * f * (1 + 1e-6), m2))
    return (m2, f, k, st, None if e is None else e / L.r_edge_t - 1.0, info["converged"])


M2X = [10.0 ** e for e in range(-30, -7)]            # 1e-30 .. 1e-8 decade steps (EXTENSION beyond the declared 1e-16 floor)
if __name__ == "__main__":
    ctx = mp.get_context("fork")
    with ctx.Pool(min(14, os.cpu_count() or 4)) as pool:
        mus = pool.map(task_mu, [(m2, k) for m2 in M2X for k in KEYS], chunksize=1)
        MUX = {}
        for m2, k, v in mus:
            MUX.setdefault(m2, {})[k] = v
        MUU = {m2: (None if any(v is None for v in MUX[m2].values()) else max(MUX[m2].values())) for m2 in M2X}
        pts = pool.map(task_pt, [(m2, MUU[m2], k, f) for m2 in M2X if MUU[m2] for k in KEYS for f in FACS], chunksize=1)
    PT = {}
    for m2, f, k, st, e, cv in pts:
        PT.setdefault((m2, f), []).append((k, st, e, cv))
    P("\nA4  the (m2, mu) plane: mu = f x mu_uni(m2), 24 layers; m2 from 1e-30 (EXTENSION) to 1e-8")
    P("    m2        mu_uni       f     stable  edges<=10%  Phi_F/vf2   F/gM        Phi_Sun/vf2   T  F  S   ALL")
    nall = 0
    ROWX = []
    for m2 in M2X:
        if not MUU[m2]:
            P(f"    {m2:8.1e}  no stable mu <= 1e34"); continue
        for f in FACS:
            mu = MUU[m2] * f
            lst = PT[(m2, f)]
            nst = sum(1 for _, s, _, _ in lst if s)
            n10 = sum(1 for _, _, e, _ in lst if e is not None and abs(e) <= 0.10)
            chiF, iF = solve_chi0(GF, mu, m2)
            fc = flagship_costs(GF, phi_chi(GF, iF, m2))
            chiS, iS = solve_chi0(GS, mu, m2)
            sc = sun_cost(GS, phi_chi(GS, iS, m2), SUN[3])
            T = n10 == 24; F_ = abs(fc["phi_over_vf2"]) <= 0.1 and abs(fc["force_over_gM"]) <= 0.023; S_ = abs(sc) <= 0.1
            allp = (nst == 24) and T and F_ and S_
            nall += allp
            ROWX.append(dict(m2=m2, f=f, mu=mu, stable=nst, n10=n10, phiF=fc["phi_over_vf2"], forceF=fc["force_over_gM"], phiSun=sc, T=T, F=F_, S=S_, ALL=allp,
                             conv=iF["converged"] and iS["converged"] and all(c for *_, c in lst)))
            if f in (1.0, 100.0) or allp:
                P(f"    {m2:8.1e}  {MUU[m2]:10.3e}  {f:5.0f}  {nst:2d}/24    {n10:2d}/24    {fc['phi_over_vf2']:+10.3e}  {fc['force_over_gM']:+10.3e}  {sc:+11.3e}   {int(T)}  {int(F_)}  {int(S_)}   {int(allp)}")
    P(f"    points (m2, f) passing stable AND T AND F AND S: {nall} of {len(ROWX)}")
    P("    points passing stable AND F AND S (ignoring tracking): " + str(sum(1 for r in ROWX if r['stable'] == 24 and r['F'] and r['S'])))
    P("    points passing stable AND T (tracking): " + str(sum(1 for r in ROWX if r['stable'] == 24 and r['T'])))
    tail = [r for r in ROWX if r["f"] == 1.0 and r["m2"] <= 1e-16]
    if len(tail) >= 4:
        xs = np.log10([r["m2"] for r in tail]); ys = np.log10([abs(r["phiSun"]) for r in tail]); yf = np.log10([abs(r["phiF"]) for r in tail])
        P(f"    log-log slope of |Phi_Sun| vs m2 for m2 <= 1e-16 (f = 1): {np.polyfit(xs, ys, 1)[0]:.3f}; of |Phi_F|: {np.polyfit(xs, yf, 1)[0]:.3f}")
    okS = [r["m2"] for r in ROWX if r["f"] == 1.0 and r["S"]]
    okF = [r["m2"] for r in ROWX if r["f"] == 1.0 and r["F"]]
    P(f"    (f = 1) largest m2 meeting S: {max(okS) if okS else 'none'}; largest m2 meeting F: {max(okF) if okF else 'none'}; "
      f"smallest m2 meeting T (10%): {min([r['m2'] for r in ROWX if r['f'] == 1.0 and r['T']] or [float('nan')])}")

    # ----------------------------------------------------------------------- A5 window choice
    P("\nA5  window choice: stability of mu_uni(m2) and the minimal mu with (i) t-windows (declared), (ii) windows in chi0, (iii) the full domain")

    def stable_chiwin(L, mu, m2):
        chi, _ = L.chi0(mu, m2)
        idx = np.where((chi > 0.004) & (chi < 0.996))[0]
        if len(idx) < 10:
            return None
        ri, ro = L.full.r[idx.min()], L.full.r[idx.max()]
        Gf = Grid(transition_on(np.geomspace(ri, ro, 8000), L.z, L.Mb, L.foot, W_M))
        cf = np.interp(Gf.lnr, L.full.lnr, chi)
        return stable_all(Gf, cf, mu, m2, fieldvals=cf)

    def stable_full(L, mu, m2):
        chi, _ = L.chi0(mu, m2)
        Gd = L.full
        mask = np.ones(Gd.N, bool)
        dg, of, wt = win_matrix(Gd, chi, mu, m2, mask)
        return is_pd(dg, of, wt)

    def bis(fn, L, m2, lo=20.0, hi=34.0, n=22):
        if not fn(L, 10 ** hi, m2):
            return None
        for _ in range(n):
            mid = 0.5 * (lo + hi)
            if fn(L, 10 ** mid, m2):
                hi = mid
            else:
                lo = mid
        return 10 ** hi

    def task5(args):
        m2, k = args
        L = LAYERS[k]
        mu = ROWS[m2]["mu_uni"]
        return (m2, k, stable_chiwin(L, mu * (1 + 1e-6), m2), stable_full(L, mu * (1 + 1e-6), m2),
                bis(lambda L_, mu_, m2_: bool(stable_chiwin(L_, mu_, m2_)), L, m2), bis(stable_full, L, m2))
    with ctx.Pool(min(14, os.cpu_count() or 4)) as pool:
        r5 = pool.map(task5, [(m2, k) for m2 in (m12, m16) for k in KEYS], chunksize=1)
    for m2 in (m12, m16):
        rr = [x for x in r5 if x[0] == m2]
        mu_t = ROWS[m2]["mu_uni"]
        chiw = [x[4] for x in rr]; full = [x[5] for x in rr]
        P(f"    m2 = {m2:.0e}: mu_uni(t-windows) = {mu_t:.4e}; stable at that mu under chi0-windows on {sum(1 for x in rr if x[2])}/24 "
          f"(no chi0 layer on {sum(1 for x in rr if x[2] is None)}), full domain {sum(1 for x in rr if x[3])}/24")
        P(f"         mu_uni(chi0-windows) = {max([c for c in chiw if c] or [float('nan')]):.4e} ({sum(1 for c in chiw if c is None)} layers None); "
          f"mu_uni(full domain) = {max([c for c in full if c] or [float('nan')]):.4e}")

    # ----------------------------------------------------------------------- A6 Neumann
    P("\nA6  chi0 boundary condition: Dirichlet (declared) vs Neumann (free ends), mu = mu_uni(Dirichlet)")
    for m2 in (m12, m16):
        mu = ROWS[m2]["mu_uni"]
        out = {}
        for lab, free in (("Dirichlet", False), ("Neumann", True)):
            chiF, iF = solve_chi0(GF, mu, m2, free=free)
            fc = flagship_costs(GF, phi_chi(GF, iF, m2))
            chiS, iS = solve_chi0(GS, mu, m2, free=free)
            sc = sun_cost(GS, phi_chi(GS, iS, m2), SUN[3])
            out[lab] = (fc["phi_over_vf2"], fc["force_over_gM"], sc, iF["converged"] and iS["converged"])
            P(f"    m2 = {m2:.0e} {lab:9s}: Phi_F/vf2 = {fc['phi_over_vf2']:+.4g}, F/gM = {fc['force_over_gM']:+.4g}, Phi_Sun/vf2 = {sc:+.4g}, converged {out[lab][3]}")
    json.dump(dict(mu_uni_ext={str(k): v for k, v in MUU.items()}, plane=ROWX), open(os.path.join(HERE, f"cfg102_c_results{SUF}.json"), "w"), indent=1, default=str)
