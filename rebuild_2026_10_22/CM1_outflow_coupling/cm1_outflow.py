#!/usr/bin/env python3
"""CM1_outflow_coupling (criteria 2ddf43b9b9): gravity-only coupling of impulsive gas outflow to a FORMED converged cusp.
Cold halo = NFW at the c giving CE1's eta 25.94 (X81 a_fit_profile, x_c 0.001), isotropic Eddington DF in the total
potential, spherical-shell self-gravity; SPARC-median baryons (BE1 canonical active set); prescribed gas cycles.
    python3 cm1_outflow.py setup                     # representative galaxy + c + ICs -> cm1_setup.json, cm1_ics.npz
    python3 cm1_outflow.py run STATIC|PRIMARY|BOUND|MUTATE
    python3 cm1_outflow.py grade"""
import json, math, os, sys, signal, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
G_SI, MSUN, KPC, MYR, ERG = 6.674e-11, 1.989e30, 3.0857e19, 3.156e13, 1e-7
N, SEED, NCYC, EPS = 200000, 1, 40, 1e-4
NEED = 21.2 / 25.94
def P(s, out=[]): print(s, flush=True); out.append(s); return out

# X81's fit machinery (script prefix up to its K1)
X81 = os.path.join(REB, "X81_core_convergence", "x80_core_convergence.py"); T81 = open(X81).read()
CUT = "# K1: exact smooth core"; assert T81.count(CUT) == 1
F81 = {"__file__": X81, "__name__": "x81_ro"}; exec(compile(T81.split(CUT)[0], X81, "exec"), F81)
a_fit_profile, BS, M_nfw = F81["a_fit_profile"], F81["BS"], F81["M_nfw"]
eta_a = lambda a: 4 / 3 * a * a / float(BS(a))

def hern_M(r, M, a): return M * r * r / (r + a) ** 2
def hern_P(r, M, a): return -M / (r + a)

def setup():
    # BE1's loader (prefix up to its K2), by-products land in this lane's dir
    B1 = os.path.join(REB, "BE1_baryon_energy_budget", "be1_energy.py"); T1 = open(B1).read()
    T1 = T1.replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {HERE!r}', 1)
    cut = "K2rows = run("; assert T1.count(cut) == 1
    D = {"__file__": B1, "__name__": "be1_ro"}; argv0 = sys.argv; sys.argv = [B1]
    exec(compile(T1.split(cut)[0], B1, "exec"), D); sys.argv = argv0
    GALS, BGS, MSUNE, MPCE, GE = D["GALS"], D["BGS"], D["MSUNE"], D["MPCE"], D["GE"]
    byname = {q["name"]: q for q in GALS}; rep = {}
    for foot in ("canonical", "alt"):
        act = [r for r in D["run"](foot) if r["active"]]; bg = BGS["A_c2b_refit"]
        rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []
        for r in act:
            q = byname[r["name"]]; M200 = 10 ** r["lM200"]; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
            rows.append(dict(M200=M200, R200_kpc=R200 / KPC, fb=10 ** q["lMb"] / M200, fg=1.33 * q["meta"]["MHI"] * 1e9 / M200,
                             rd=q["meta"]["Rdisk"] * KPC / R200, L36=q["meta"]["L36"] * 1e9))
        rep[foot] = {k: float(np.median([w[k] for w in rows])) for k in rows[0]}; rep[foot]["n"] = len(rows)
    # c with eta 25.94 at x_c 0.001 (bisection on the a-grid estimator)
    lo, hi = 3.0, 30.0
    for _ in range(40):
        mid = 0.5 * (lo + hi); e = eta_a(a_fit_profile(M_nfw(mid), 1e-3))
        lo, hi = (mid, hi) if e < 25.94 else (lo, mid)
    c = 0.5 * (lo + hi); S = dict(rep=rep, c=c, eta_c=eta_a(a_fit_profile(M_nfw(c), 1e-3)))
    R = rep["canonical"]; S["tunit_Myr"] = math.sqrt((R["R200_kpc"] * KPC) ** 3 / (G_SI * R["M200"] * MSUN)) / MYR
    S["Eunit_erg"] = G_SI * (R["M200"] * MSUN) ** 2 / (R["R200_kpc"] * KPC) / ERG
    S["a_star"] = 0.70 * R["rd"]; S["Mb"] = R["fb"]; S["Mg"] = R["fg"]
    # cold density: NFW (M(<1) = 1) + slope-continuous exponential taper beyond R200, cut at 3
    mc = math.log1p(c) - c / (1 + c); rs = 1 / c; rd_t = 0.3; slope = -(1 + 3 * c) / (1 + c); epw = slope + 1 / rd_t
    def rho(r):
        r = np.asarray(r, float); rn = 1 / (4 * math.pi * mc) / (r * (rs + r) ** 2)
        r1 = 1 / (4 * math.pi * mc) / (1 * (rs + 1) ** 2)
        return np.where(r <= 1, rn, r1 * r ** epw * np.exp(-(r - 1) / rd_t))
    rg = np.concatenate([[0.0], np.geomspace(1e-6, 3.0, 60001)]); rh = rho(np.maximum(rg, 1e-12))
    Mc = M_nfw(c)(np.minimum(rg, 1.0)) / mc  # exact NFW inside R200, taper integrated outside
    w = rg > 1; dM = 4 * math.pi * 0.5 * (rh[1:] * rg[1:] ** 2 + rh[:-1] * rg[:-1] ** 2) * np.diff(rg)
    Mc[w] += np.cumsum(np.where(w[1:], dM, 0.0))[w[1:]]
    # potential (cold + static baryons with gas at a_star), zero at r = 3
    Mb = S["Mb"]; a = S["a_star"]; Mt = Mc + hern_M(rg, Mb, a)
    gr = Mt / np.maximum(rg, 1e-12) ** 2; gr[0] = 0
    Phi = np.concatenate([[0], np.cumsum(0.5 * (gr[1:] + gr[:-1]) * np.diff(rg))]); Phi -= Phi[-1]
    Psi = -Phi  # >= 0, decreasing outwards
    r_ = rg[1:]; Ps = Psi[1:]; rh_ = rh[1:]
    # Eddington: f(E) = 1/(sqrt8 pi^2) d/dE int_0^E (drho/dPsi) / sqrt(E - Psi) dPsi
    o = np.argsort(Ps); Pso, rho_o = Ps[o], rh_[o]; keep = np.concatenate([[True], np.diff(Pso) > 0]); Pso, rho_o = Pso[keep], rho_o[keep]
    lP = np.log(Pso[1:]); lr = np.log(rho_o[1:]); dlr = np.gradient(lr, lP)
    drho = lambda p: np.interp(np.log(np.maximum(p, Pso[1])), lP, dlr) * np.exp(np.interp(np.log(np.maximum(p, Pso[1])), lP, lr)) / np.maximum(p, Pso[1])
    Eg = np.geomspace(Pso[1] * 1.0001, Pso[-1], 2000); u = np.linspace(0, 1, 801)
    I = np.array([2 * math.sqrt(E) * np.trapz(drho(E - (math.sqrt(E) * u) ** 2), u) for E in Eg])
    f = np.maximum(np.gradient(I, Eg) / (math.sqrt(8) * math.pi ** 2), 0)
    fE = lambda E: np.interp(E, Eg, f, left=0.0, right=f[-1])
    # sample radii from the cold M(r), velocities from v^2 f(Psi - v^2/2)
    rng = np.random.default_rng(SEED); q = rng.random(N) * Mc[-1]; r = np.interp(q, Mc, rg)
    edges = np.geomspace(max(r.min(), 1e-6) * 0.999, 3.0, 801); idx = np.clip(np.searchsorted(edges, r) - 1, 0, 799); v = np.empty(N)
    for b in range(800):
        m = idx == b
        if not m.any(): continue
        psi = float(np.interp(math.sqrt(edges[b] * edges[b + 1]), rg, Psi)); vv = np.linspace(0, math.sqrt(2 * psi), 600)
        p = vv * vv * fE(psi - vv * vv / 2); cdf = np.concatenate([[0], np.cumsum(0.5 * (p[1:] + p[:-1]) * np.diff(vv))])
        v[m] = np.interp(rng.random(m.sum()) * cdf[-1], cdf, vv)
    def iso(n): z = rng.normal(size=(n, 3)); return z / np.linalg.norm(z, axis=1)[:, None]
    pos = iso(N) * r[:, None]; vel = iso(N) * v[:, None]
    np.savez(os.path.join(HERE, "cm1_ics.npz"), pos=pos, vel=vel, mp=Mc[-1] / N)
    xc = float(np.sort(r)[499]); S["xc500"] = xc; S["eta_analytic_xc500"] = eta_a(a_fit_profile(M_nfw(c), xc))
    S["eta_particles_t0"] = eta_p(pos); S["Mcold_total"] = float(Mc[-1])
    json.dump(S, open(os.path.join(HERE, "cm1_setup.json"), "w"), indent=1); P(json.dumps(S, indent=1))

def eta_p(pos, xc=None):
    r = np.sort(np.linalg.norm(pos, axis=1)); n = np.arange(1, len(r) + 1, dtype=float)
    if xc is None: xc = r[499]
    m1 = np.interp(1.0, r, n)
    Mf = lambda x: np.interp(x, r, n) / m1
    return eta_a(a_fit_profile(Mf, xc))

def gas_scale(t, a, tu, mode):
    per, up, dn = (405 if mode == "MUTATE_A1" else 250) / tu, (200 if mode.startswith("MUTATE") else 5) / tu, 200 / tu
    if mode == "STATIC" or t >= NCYC * per: return a
    ph = t % per
    if ph < up: s = (1 - math.cos(math.pi * ph / up)) / 2
    elif ph < up + dn: s = (1 + math.cos(math.pi * (ph - up) / dn)) / 2
    else: s = 0.0
    return a * (1 + 7 * s)

def run(mode):
    S = json.load(open(os.path.join(HERE, "cm1_setup.json"))); I = np.load(os.path.join(HERE, "cm1_ics.npz"))
    pos, vel, mp = I["pos"].copy(), I["vel"].copy(), float(I["mp"]); tu, a = S["tunit_Myr"], S["a_star"]
    Mg = {"STATIC": S["Mg"], "PRIMARY": S["Mg"], "MUTATE": S["Mg"], "MUTATE_A1": S["Mg"], "BOUND": S["Mb"]}[mode]; Ms = S["Mb"] - Mg
    xc = S["xc500"]; dt = 0.5 / tu; per = (405 if mode == "MUTATE_A1" else 250) / tu; nst = int(round(NCYC * per / dt))
    def Pb(r, ag): return hern_P(r, Ms, a) + hern_P(r, Mg, ag)
    def acc(p, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); o = np.argsort(r); rank = np.empty(len(r)); rank[o] = np.arange(len(r))
        M = mp * rank + hern_M(r, Ms, a) + hern_M(r, Mg, ag); return -p * (M / (r * r + EPS * EPS) ** 1.5)[:, None], r
    def energy(p, v, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); rs_ = np.sort(r)
        return 0.5 * mp * float(np.sum(v * v)) - mp * mp * float(np.sum(np.arange(len(rs_)) / np.sqrt(rs_ * rs_ + EPS * EPS))) + mp * float(np.sum(Pb(r, ag)))
    stop = {"x": False}; signal.signal(signal.SIGTERM, lambda *_: stop.update(x=True))
    E0 = energy(pos, vel, a); W = 0.0; marks = []; maxerr = 0.0; t0 = time.time()
    ag = a; A, r = acc(pos, ag)
    marks.append(dict(cycle=0, eta=eta_p(pos, xc), err=0.0))
    for i in range(nst):
        t = i * dt; am = gas_scale(t + dt / 2, a, tu, mode); an = gas_scale(t + dt, a, tu, mode)
        if am != ag: W += mp * float(np.sum(Pb(r, am) - Pb(r, ag))); A, r = acc(pos, am)
        vel += dt / 2 * A; pos += dt * vel; A, r = acc(pos, am); vel += dt / 2 * A
        if an != am: W += mp * float(np.sum(Pb(r, an) - Pb(r, am))); A, r = acc(pos, an)
        ag = an; k = i + 1
        if k % int(round(5 * per / dt)) == 0:
            E = energy(pos, vel, ag); err = abs(E - E0 - W) / abs(E0); maxerr = max(maxerr, err)
            marks.append(dict(cycle=int(round(k * dt / per)), eta=eta_p(pos, xc), err=err, W=W, sec=time.time() - t0)); P(f"{mode} {marks[-1]}")
            json.dump(dict(mode=mode, marks=marks, E0=E0, maxerr=maxerr, done=False), open(os.path.join(HERE, f"cm1_run_{mode}.json"), "w"), indent=1)
        if stop["x"]: P(f"{mode} SIGTERM at step {k}: partial saved"); sys.exit(3)
    json.dump(dict(mode=mode, marks=marks, E0=E0, maxerr=maxerr, W=W, done=True), open(os.path.join(HERE, f"cm1_run_{mode}.json"), "w"), indent=1)

def e_lift(S, Mg):
    """energy to expand Mg from a* to 8a* in the static stars + initial cold halo (+ gas self-energy), code units"""
    a, Ms, c = S["a_star"], S["Mb"] - Mg, S["c"]; mc = math.log1p(c) - c / (1 + c); rs = 1 / c
    rg = np.geomspace(1e-6, 3.0, 200001)
    Pc = -np.log1p(rg / rs) / (mc * rg)  # NFW potential (taper ignored; it only shifts a constant inside r < 1)
    def U(ag):
        dMg = np.diff(hern_M(rg, Mg, ag)); rm = 0.5 * (rg[1:] + rg[:-1])
        return -Mg * Mg / (6 * ag) + float(np.sum(dMg * (hern_P(rm, Ms, a) + np.interp(rm, rg, Pc))))
    return U(8 * a) - U(a)

def grade():
    S = json.load(open(os.path.join(HERE, "cm1_setup.json"))); R = {m: json.load(open(os.path.join(HERE, f"cm1_run_{m}.json"))) for m in ("STATIC", "PRIMARY", "BOUND", "MUTATE")}
    out = P("CM1 outflow coupling (criteria 2ddf43b9b9); kappa = 1/2 FITTED; not theory closed; cold dark energy is a gravitating field, never a particle")
    rc = S["rep"]["canonical"]
    P(f"  representative (canonical, n {rc['n']}): M200 {rc['M200']:.3g} Msun, R200 {rc['R200_kpc']:.0f} kpc, Mb/M200 {rc['fb']:.4f}, Mgas/M200 {rc['fg']:.4f}, Rd/R200 {rc['rd']:.4f}, t_unit {S['tunit_Myr']:.0f} Myr")
    ra = S["rep"]["alt"]; P(f"  [alt, reported] n {ra['n']}: Mb/M200 {ra['fb']:.4f}, Mgas/M200 {ra['fg']:.4f}, Rd/R200 {ra['rd']:.4f}")
    P(f"  cold NFW c {S['c']:.3f} (eta at x_c 0.001: {S['eta_c']:.2f}); x_c(500th) {S['xc500']:.4f}")
    k1a = abs(S["eta_particles_t0"] / S["eta_analytic_xc500"] - 1) <= 0.05
    st = {m["cycle"]: m["eta"] for m in R["STATIC"]["marks"]}
    Rof = lambda m: {k["cycle"]: k["eta"] / st[k["cycle"]] for k in R[m]["marks"] if k["cycle"] in st}
    Rs = {m: Rof(m) for m in R}; last = max(st)
    k1b = 0.97 <= R["STATIC"]["marks"][-1]["eta"] / R["STATIC"]["marks"][0]["eta"] <= 1.03
    k2 = all(R[m]["maxerr"] < 0.01 for m in R); done = all(R[m]["done"] for m in R)
    P(f"K1a particle eta t=0 {S['eta_particles_t0']:.2f} vs analytic at same x_c {S['eta_analytic_xc500']:.2f}: {'PASS' if k1a else 'FAIL'}")
    P(f"K1b STATIC eta drift over {last} cycles: {R['STATIC']['marks'][0]['eta']:.2f} -> {R['STATIC']['marks'][-1]['eta']:.2f}: {'PASS' if k1b else 'FAIL'}")
    P(f"K2 work balance max |E-E0-W|/|E0|: " + ", ".join(f"{m} {R[m]['maxerr']:.1e}" for m in R) + f": {'PASS' if k2 else 'FAIL'}")
    for m in ("PRIMARY", "BOUND", "MUTATE"):
        P(f"  {m}: R by cycle " + ", ".join(f"{k}:{v:.3f}" for k, v in sorted(Rs[m].items())) + f"; net work into cold {R[m].get('W', float('nan')):.3e} (E0 {R[m]['E0']:.3e})")
    Rp, Rb, Rm = Rs["PRIMARY"][last], Rs["BOUND"][last], Rs["MUTATE"][last]
    El = {m: NCYC * e_lift(S, S["Mg"] if m == "PRIMARY" else S["Mb"]) * S["Eunit_erg"] for m in ("PRIMARY", "BOUND")}
    Esn = 0.5 * rc["L36"] / 100 * 1e51; eps = {m: El[m] / Esn for m in El}
    P(f"  E_lift (40 cycles): PRIMARY {El['PRIMARY']:.2e} erg (eps_SN {eps['PRIMARY']:.3f}), BOUND {El['BOUND']:.2e} erg (eps_SN {eps['BOUND']:.3f}); E_SN {Esn:.2e} erg")
    if abs(1 - Rp) < 0.03: mut = "NOT INFORMATIVE (PRIMARY moved R < 0.03)"
    else: mut = "PASS" if abs(1 - Rm) < abs(1 - Rp) else "FAIL"
    sens = abs(1 - Rb) > 0.03
    P(f"MUTATE slow-out R {Rm:.3f} vs PRIMARY {Rp:.3f}: {mut}; BOUND sensitivity |1-R| {abs(1 - Rb):.3f} > 0.03: {'PASS' if sens else 'FAIL'}")
    ok = k1a and k1b and k2 and done and mut != "FAIL"
    if not ok: v = "NOT DECIDED"
    elif Rp <= NEED and eps["PRIMARY"] <= 1: v = "CHANNEL VIABLE"
    elif Rb <= NEED: v = "CHANNEL INSUFFICIENT AT MEASURED GAS"
    else: v = "CHANNEL EXCLUDED IN THIS GEOMETRY"
    P(f"VERDICT (canonical; needed R <= {NEED:.3f}): PRIMARY R {Rp:.3f}, BOUND R {Rb:.3f}: {v}")
    open(os.path.join(HERE, "cm1.out"), "w").write("\n".join(out) + "\n")
    json.dump(dict(setup=S, R=Rs, verdict=v, K1a=k1a, K1b=k1b, K2=k2, mutate=mut, sens=sens, E_lift_erg=El, eps_SN=eps, E_SN_erg=Esn),
              open(os.path.join(HERE, "cm1_results.json"), "w"), indent=1)

def grade_a1():
    """Amendment A1: original verdict rule with the corrected slow control; original outputs untouched."""
    O = json.load(open(os.path.join(HERE, "cm1_results_original.json"))); A = json.load(open(os.path.join(HERE, "cm1_run_MUTATE_A1.json")))
    Rp, Rb = O["R"]["PRIMARY"]["40"], O["R"]["BOUND"]["40"]; es = json.load(open(os.path.join(HERE, "cm1_run_STATIC.json")))["marks"][-1]["eta"]
    W = {m: json.load(open(os.path.join(HERE, f"cm1_run_{m}.json")))["W"] for m in ("PRIMARY", "MUTATE_A1")}
    Ra = {k["cycle"]: k["eta"] / es for k in A["marks"]}; R40 = Ra[40]; k = O["K1a"] and O["K1b"] and O["K2"] and A["maxerr"] < 0.01 and A["done"]
    mut = "NOT INFORMATIVE" if abs(1 - Rp) < 0.03 else ("PASS" if abs(1 - R40) < abs(1 - Rp) else "FAIL")
    if not k or mut == "FAIL": v = "NOT DECIDED"
    elif Rp <= NEED and O["eps_SN"]["PRIMARY"] <= 1: v = "CHANNEL VIABLE"
    elif Rb <= NEED: v = "CHANNEL INSUFFICIENT AT MEASURED GAS"
    else: v = "CHANNEL EXCLUDED IN THIS GEOMETRY"
    out = P("CM1 A1 grade (corrected slow control); kappa = 1/2 FITTED; not theory closed")
    P("  MUTATE_A1 R by cycle " + ", ".join(f"{c}:{r:.3f}" for c, r in sorted(Ra.items())) + f"; work balance {A['maxerr']:.1e}")
    P(f"  net work into cold: PRIMARY {W['PRIMARY']:.3e}, MUTATE_A1 {W['MUTATE_A1']:.3e}")
    P(f"MUTATE_A1 R {R40:.3f} vs PRIMARY {Rp:.3f}: {mut}")
    P(f"VERDICT A1 (needed R <= {NEED:.3f}): PRIMARY R {Rp:.3f} (eps_SN {O['eps_SN']['PRIMARY']:.3f}), BOUND R {Rb:.3f} (eps_SN {O['eps_SN']['BOUND']:.3f}): {v}")
    open(os.path.join(HERE, "cm1_A1.out"), "w").write("\n".join(out) + "\n")
    json.dump(dict(R_A1=Ra, W=W, mutate=mut, verdict=v), open(os.path.join(HERE, "cm1_A1_results.json"), "w"), indent=1)

if __name__ == "__main__":
    run(sys.argv[2]) if sys.argv[1] == "run" else {"setup": setup, "grade": grade, "grade_a1": grade_a1}[sys.argv[1]]()
