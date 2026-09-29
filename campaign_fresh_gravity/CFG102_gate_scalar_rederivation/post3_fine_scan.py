"""POST-HOC (NOT in cfg102_frozen.py; labelled as such): a FINE (m2, mu) scan asking whether any point passes stable AND T AND F AND S,
because the declared half-decade grid can straddle isolated zero-crossings of the (signed) flagship / Sun potentials.
m2: 61 log-spaced values 1e-16 .. 1e-8 (7.5 per decade); mu = f x mu_uni(m2), f in FACS; both chi0 boundary conditions (Dirichlet, Neumann).
Bars as frozen: T = 24/24 edges within 10%; F = |Phi_F| <= 0.1 v_f^2 and |F|/g_M <= 0.023; S = |Phi_Sun| <= 0.1 v_f^2; stable = all 24 layers, t-windows."""
import os, sys, math, json, multiprocessing as mp
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cfg102_common import *

LAYERS = {key(z, Mb, f): Layer(z, Mb, f) for (z, Mb, f) in GAL}
KEYS = list(LAYERS)
GF = cost_setup(*FLAG)
GS = cost_setup(SUN[0], SUN[1], SUN[2])
M2S = [10 ** (-16 + 8 * i / 60) for i in range(61)]
FACS = (1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 30.0, 100.0)


def work(m2):
    mus = [LAYERS[k].mu_min(m2) for k in KEYS]
    if any(v is None for v in mus):
        return m2, None
    mu_u = max(mus)
    out = []
    for f in FACS:
        mu = mu_u * f
        for bc in ("D", "N"):
            free = (bc == "N")
            st = 0
            n10 = 0
            for k in KEYS:
                L = LAYERS[k]
                chi, info = L.chi0(mu, m2, free=free)
                cf = L.chi0_on(chi, L.fine)
                chi2, _ = L.chi0(mu * (1 + 1e-6), m2, free=free)
                st += int(stable_all(L.fine, L.chi0_on(chi2, L.fine), mu * (1 + 1e-6), m2))
                e = L.edge_chi(chi)
                n10 += int(e is not None and abs(e / L.r_edge_t - 1) <= 0.10)
            chiF, iF = solve_chi0(GF, mu, m2, free=free)
            fc = flagship_costs(GF, phi_chi(GF, iF, m2))
            chiS, iS = solve_chi0(GS, mu, m2, free=free)
            sc = sun_cost(GS, phi_chi(GS, iS, m2), SUN[3])
            out.append(dict(m2=m2, f=f, bc=bc, mu=mu, stable=st, n10=n10, phiF=fc["phi_over_vf2"], forceF=fc["force_over_gM"], phiSun=sc,
                            T=n10 == 24, F=(abs(fc["phi_over_vf2"]) <= 0.1 and abs(fc["force_over_gM"]) <= 0.023), S=abs(sc) <= 0.1,
                            conv=bool(iF["converged"] and iS["converged"])))
    return m2, out


if __name__ == "__main__":
    ctx = mp.get_context("fork")
    with ctx.Pool(min(14, os.cpu_count() or 4)) as pool:
        res = pool.map(work, M2S, chunksize=1)
    rows = [r for m2, o in res if o for r in o]
    print(f"m2 values with a stable mu <= 1e34 on all layers: {sum(1 for m2, o in res if o)} / {len(M2S)}; points evaluated: {len(rows)}")
    for bc in ("D", "N"):
        R = [r for r in rows if r["bc"] == bc]
        st = [r for r in R if r["stable"] == 24]
        print(f"\nBC = {bc}: points {len(R)}; stable(24/24) {len(st)}")
        for lab, cond in (("T", lambda r: r["T"]), ("F", lambda r: r["F"]), ("S", lambda r: r["S"]), ("T&F", lambda r: r["T"] and r["F"]), ("T&S", lambda r: r["T"] and r["S"]),
                          ("F&S", lambda r: r["F"] and r["S"]), ("T&F&S", lambda r: r["T"] and r["F"] and r["S"])):
            sel = [r for r in st if cond(r)]
            print(f"   stable AND {lab:6s}: {len(sel):4d}" + (f"   e.g. m2 range {min(r['m2'] for r in sel):.2e}..{max(r['m2'] for r in sel):.2e}" if sel else ""))
        # closest approach: minimise the max of the bar ratios among stable & T points
        cand = [r for r in st if r["T"]]
        if cand:
            def ratio(r):
                return max(abs(r["phiF"]) / 0.1, abs(r["forceF"]) / 0.023, abs(r["phiSun"]) / 0.1)
            best = min(cand, key=ratio)
            print(f"   stable & T point with the smallest worst bar-ratio: m2 = {best['m2']:.3e}, f = {best['f']}: Phi_F {best['phiF']:+.3g}, F/gM {best['forceF']:+.3g}, Sun {best['phiSun']:+.3g}; worst ratio {ratio(best):.3g}")
        # sign changes along f = 1
        f1 = sorted([r for r in R if r["f"] == 1.0], key=lambda r: r["m2"])
        for nm in ("phiF", "forceF", "phiSun"):
            zs = [(a["m2"], b["m2"]) for a, b in zip(f1[:-1], f1[1:]) if a[nm] * b[nm] < 0]
            print(f"   f = 1: sign changes of {nm} between m2 = " + ", ".join(f"{a:.2e}-{b:.2e}" for a, b in zs))
    json.dump(rows, open(os.path.join(HERE, "cfg102_post3_results.json"), "w"), default=str)
