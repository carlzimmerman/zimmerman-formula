#!/usr/bin/env python3
"""CFG368 -- does DESI DR2 prefer an energy flow between the cold fluid and the vacuum, and which way?  Frozen: FROZEN_CRITERIA.md (e8fb8e08c).
a0(z) = kappa c sqrt(G rho_vac(z)) tracks the vacuum (owner correction 10-06).  Q > 0: cold -> vacuum.
CPL projection and chain loader copied from CFG360 (DECLARED, PROVISIONAL).  CFG368_MUTATE=1 sets Q = 0 (separate outputs)."""
import os, json, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
CHAINS = os.path.abspath(os.path.join(ROOT, "..", "_external_data", "desi_dr2_chains"))
MUTATE = os.environ.get("CFG368_MUTATE", "0") == "1"; SLUG = "cfg368_cold_de_flow" + ("_MUTATE" if MUTATE else "")
h = 0.674; om_c, om_b, om_r = 0.1200, 0.02237, 4.18e-5
Oc, Ob, Or = om_c / h**2, om_b / h**2, om_r / h**2
A_INI = 1e-4; ZFIT = np.linspace(0, 2.5, 126)
LOG, CH, OUT = [], [], {"lane": "CFG368", "frozen": "e8fb8e08c", "mutate": MUTATE, "forms": {}}


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok, v=""):
    CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")


def solve(form, p):
    """densities in rho_crit0, N = ln a.  y = (rho_vac, rho_c).  Q into vacuum from cold."""
    p = 0.0 if MUTATE else p
    def run(rv_ini, dense=False):
        def f(N, y):
            rv, rc = y; a = math.exp(N); E = math.sqrt(max(Or * a**-4 + Ob * a**-3 + rc + rv, 1e-30))
            q = {"F1": p * rv / E, "F2": p * rc / E, "F3": p * rv, "F4": p * rc}[form]   # Q/(H rho_crit0): d/dN = Q/H
            return [q, -3 * rc - q]
        def stall(N, y):                       # E^2 -> 0 (a turnaround / negative-density branch): stop, the branch is unphysical
            a = math.exp(N); return Or * a**-4 + Ob * a**-3 + y[1] + y[0] - 1e-6
        stall.terminal = True
        return solve_ivp(f, [math.log(A_INI), 0.0], [rv_ini, Oc * A_INI**-3], rtol=1e-10, atol=1e-14, dense_output=dense, method="LSODA", events=stall)
    def resid(rv):
        s = run(rv)
        if s.status == 1:                      # stalled before today: E^2 fell to ~0, i.e. too little density -> negative residual
            return -1.0
        return Or + Ob + s.y[0, -1] + s.y[1, -1] - 1.0
    lo, hi = -5.0, 10.0
    try:
        rv0 = brentq(resid, lo, hi, xtol=1e-13)
    except ValueError:
        return None
    sol = run(rv0, dense=True)
    return None if sol.status == 1 else sol


def cpl(sol):
    rv1, rc1 = sol.sol(0.0); Om = Ob + rc1
    a = 1 / (1 + ZFIT); Y = np.array([sol.sol(n) for n in np.log(a)])
    E2 = Or * a**-4 + Ob * a**-3 + Y[:, 1] + Y[:, 0]
    if np.any(E2 <= 0):
        return None
    rde = E2 - Om * a**-3 - Or * a**-4; ODE = 1 - Om - Or
    def r(q):
        w0, wa = q; fde = a**(-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
        return 0.5 * np.log(np.maximum(Om * a**-3 + Or * a**-4 + ODE * fde, 1e-30)) - 0.5 * np.log(E2)
    fit = least_squares(r, [-1.0, 0.0], xtol=1e-14, ftol=1e-14, gtol=1e-14)
    return float(fit.x[0]), float(fit.x[1]), float(Om), float(rde.min()), float(Y[:, 0].min()), float(np.abs(fit.fun).max())


def load_chain(name):
    d = os.path.join(CHAINS, name); hdr = open(os.path.join(d, "chain.1.txt")).readline().lstrip("#").split()
    iw, iw0, iwa = hdr.index("weight"), hdr.index("w"), hdr.index("wa"); rows = []
    for k in range(1, 5):
        x = np.loadtxt(os.path.join(d, f"chain.{k}.txt")); x = x[int(0.3 * len(x)):]; rows.append(x[:, [iw, iw0, iwa]])
    x = np.vstack(rows); wt = x[:, 0]
    return np.average(x[:, 1:], axis=0, weights=wt), np.cov(x[:, 1:].T, aweights=wt)


chains = {nm: load_chain(nm) for nm in ("cmb", "pantheonplus", "union3", "desy5")}
for nm, (mu, cov) in chains.items():
    P(f"  chain {nm:12s}: <w0> {mu[0]:+.3f} +- {math.sqrt(cov[0,0]):.3f}, <wa> {mu[1]:+.3f} +- {math.sqrt(cov[1,1]):.3f}")
chi2 = lambda mu, cov, w0, wa: float((np.array([w0, wa]) - mu) @ np.linalg.solve(cov, np.array([w0, wa]) - mu))

s0 = solve("F1", 0.0); c0 = cpl(s0)
check("K1 zero flow -> (w0, wa) = (-1, 0) to 1e-6 and omega_c unchanged", abs(c0[0] + 1) < 1e-6 and abs(c0[1]) < 1e-6 and abs(s0.sol(0.0)[1] - Oc) < 1e-9,
      f"(w0+1 = {c0[0]+1:+.2e}, wa = {c0[1]:+.2e}, d omega_c = {s0.sol(0.0)[1] - Oc:+.2e})")
X0 = {k: chi2(*chains[k], -1.0, 0.0) for k in chains}
P("  LCDM chi2 cmb/PP/U3/DY5 = " + "/".join(f"{X0[k]:.2f}" for k in chains))
GRID = np.linspace(-0.5, 0.5, 41)
SN = ("pantheonplus", "union3", "desy5")
any_pref = False
for form, lab in (("F1", "Gamma H0 rho_vac  [tied to dark energy]"), ("F2", "Gamma H0 rho_c"), ("F3", "xi H rho_vac  [tied to H, critical density]"), ("F4", "xi H rho_c")):
    rows = []
    for p in GRID:
        s = solve(form, float(p))
        if s is None:
            continue
        c = cpl(s)
        if c is None:
            continue
        x = {k: chi2(*chains[k], c[0], c[1]) for k in chains}
        rows.append(dict(p=float(p), w0=c[0], wa=c[1], Om=c[2], rde_min=c[3], rvac_min=c[4], cpl_resid=c[5], chi2=x, sol=s))
    P(f"  {form}: {len(rows)} of {len(GRID)} grid points solved")
    if not rows:
        OUT["forms"][form] = dict(label=lab, solved=0); continue
    best = min(rows, key=lambda r: sum(r["chi2"][k] for k in SN))
    dchi = {k: X0[k] - best["chi2"][k] for k in chains}
    pref = all(dchi[k] >= 4 for k in SN); any_pref |= pref
    s = best["sol"]; rv0 = s.sol(0.0)[0]
    a0z = {z: float(math.sqrt(max(s.sol(math.log(1 / (1 + z)))[0], 0) / rv0)) for z in (1.0, 2.0, 2.5)}
    dcold = float(s.sol(0.0)[1] / Oc - 1)
    direction = "cold -> vacuum (cold fluid decays into dark energy)" if best["p"] > 0 else ("vacuum -> cold" if best["p"] < 0 else "none")
    edge = best["p"] in (GRID[0], GRID[-1])
    OUT["forms"][form] = dict(label=lab, best_p=best["p"], at_grid_edge=bool(edge), w0=best["w0"], wa=best["wa"], Om_obs=best["Om"], chi2=best["chi2"],
                              dchi2_vs_LCDM=dchi, preferred=bool(pref), direction=direction, a0_ratio=a0z, cold_comoving_change=dcold,
                              rho_vac_min=best["rvac_min"], rho_de_eff_min=best["rde_min"], cpl_resid=best["cpl_resid"])
    P(f"\n  {form} {lab}: best p = {best['p']:+.3f}{' (GRID EDGE)' if edge else ''} -> {direction}")
    P(f"     (w0, wa)_eff = ({best['w0']:+.3f}, {best['wa']:+.3f}), Om_obs {best['Om']:.4f}; dchi2 vs LCDM cmb/PP/U3/DY5 = " + "/".join(f"{dchi[k]:+.2f}" for k in chains)
      + f"; DESI-PREFERRED: {pref}")
    P(f"     a0(z)/a0(0) = sqrt(rho_vac ratio): z1 {a0z[1.0]:.3f}, z2 {a0z[2.0]:.3f}, z2.5 {a0z[2.5]:.3f}  (record M-DEC ~0.87 at z2); cold comoving change since a=1e-4: {dcold:+.3%}; "
      f"min rho_vac {best['rvac_min']:+.3f}, min rho_DE,eff {best['rde_min']:+.3f}, CPL resid {best['cpl_resid']:.1e}")
verdict = "OPEN DOOR CONFIRMED" if any_pref else "OPEN DOOR NOT SUPPORTED"
OUT["verdict"] = verdict
P(f"\n{'MUTATE ' if MUTATE else ''}VERDICT: {verdict}")
if MUTATE:
    check("MUTATE: every dchi2 = 0 and NOT SUPPORTED", all(abs(v) < 1e-6 for f in OUT["forms"].values() for v in f["dchi2_vs_LCDM"].values()) and not any_pref)
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
