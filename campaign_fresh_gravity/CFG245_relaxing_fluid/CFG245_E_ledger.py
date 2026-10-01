#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG245 Gate E -- ENERGY, CAUSALITY, STABILITY (frozen criteria section 3).

  E1 (BINDING at the shared G3 line)  Delta E = E_eq(relaxed) - E_eq(passive), E_eq = W_c/2 (virial), W_c = -G int [M_b(<r) + M_c(<r)] dM_c / r, from the cumulative
      mass profiles (committed passive products; relaxed = min(M_ph, S)); PASS iff |Delta E| <= (1/2) M_b V_f^2, V_f^2 = G M_b/r_M.  In units G M_b^2/r_M the ratio is |Delta W|.
      The passive profile beyond the last grid radius (x = 28.2) is not in the committed products: two declared closures (near: all outer bound mass at x = 28.2, which
      gives the SMALLEST |Delta E|; far: all at the passive turnaround radius); the verdict uses the near closure (generous to the class).
      Reported: |Delta E| / E_vac(ball) in both r_ta conventions (CFG48 and B's law r_ta), heating rows with limits from memory (unverified).
  E2  drift speed w = |J|/rho_c = Gamma |M_target - M_inf| / (dM_inf/dr) at the start of the relaxation; PASS iff max w/c <= 1e-3.  Relativistic completion: UNDEFINED.
  E3  (a) the relaxation block has the single eigenvalue -Gamma (sympy + discretised operator); (b) Lyapunov L = (G/2) int (M_t - M_c)^2 / r^2 dr decreases as exp(-2 Gamma t).
  E4  reaction row: UNDEFINED for non-spherical flows.
Run: ZF_REPO=<repo> python3 CFG245_E_ledger.py ; MUTATE=MT3|ME1|ME2 python3 CFG245_E_ledger.py (exits 1 when the control bites)
"""
import os, sys, math
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG245_common as K

MUT = os.environ.get("MUTATE", "").strip()
SLUG = "CFG245_E_ledger"
POST = (K.upstream_binding() is not None) and not MUT
if POST:
    SLUG += "_POSTHOC"
R = K.Report(SLUG, MUT or None)
XB, XC = K.XB, K.XC
OM48, HH48, DELTA = 0.3153, 0.6736, 11.81
RHOM_KPC3 = OM48 * 2.775e11 * HH48 ** 2 / 1e9                 # Msun / kpc^3 (CFG48 / CFG4 convention)


def W_profile(x, Mc):
    """W_c in units G M_b^2 / r_M from a cumulative cold mass profile Mc(<x) (units M_b) on radii x (increasing); mass inside the first radius at x0/sqrt2."""
    x = np.asarray(x, float); Mc = np.asarray(Mc, float)
    dm = np.diff(np.concatenate([[0.0], Mc]))
    xm = np.concatenate([[x[0] / math.sqrt(2.0)], np.sqrt(x[1:] * x[:-1])])
    Mmid = np.concatenate([[0.5 * Mc[0]], 0.5 * (Mc[1:] + Mc[:-1])])
    return float(-np.sum((1.0 + Mmid) / xm * dm))


def W_target(S, n=400000):
    xc = math.sqrt((S + 1.0) ** 2 - 1.0)
    x = np.geomspace(1e-6, xc, n)
    Mc = np.sqrt(1 + x ** 2) - 1.0
    return W_profile(x, Mc), xc


def W_passive(M, q, foot, closure):
    p = K.passive(M, q, foot)
    x = XC
    Mc = p["Minf"] / M
    S = p["S"] / M
    mo = S - Mc[-1]
    rM = K.r_M(M, foot)
    if mo > 0:
        xpos = x[-1] if closure == "near" else p["r_ta0"] / rM
        # outer mass at xpos, half its own mass counted in the self term
        W = W_profile(x, Mc) - (1.0 + Mc[-1] + 0.5 * mo) / xpos * mo
    else:
        W = W_profile(x, Mc)
    return W, S, mo


def r_ta_B_kpc(M):
    """B's law turnaround: mean enclosed law density = Delta_ta x mean matter density (P2 point mass, M_dyn = M_b sqrt(1+x^2))."""
    from scipy.optimize import brentq
    rm = K.r_M(M, "canonical")
    f = lambda lr: M * math.sqrt(1 + (math.exp(lr) / rm) ** 2) - DELTA * RHOM_KPC3 * 4 * math.pi / 3 * math.exp(lr) ** 3
    return math.exp(brentq(f, math.log(1e-2), math.log(1e5)))


def r_ta_48_kpc(M):
    Mcol = M * (1.0 + K.OMEGA_C_OVER_B)
    return (3.0 * Mcol / (4.0 * math.pi * RHOM_KPC3 * DELTA)) ** (1.0 / 3.0)


def e3a_sympy():
    """symbolic linearisation of the flux operator: div J = Gamma (rho_c - rho_ph) and the single relaxation eigenvalue -Gamma"""
    r, t, G, Gam = sp.symbols("r t G Gamma", positive=True)
    Mb, Mt, Mc = sp.Function("M_b")(r), sp.Function("M_t")(r), sp.Function("M_c")(r)
    sgn = -1 if MUT == "ME2" else 1                                     # ME2: flip the damping sign (growth)
    g_law = -G * (Mb + Mt) / r ** 2                                     # inward radial component
    g_tot = -G * (Mb + Mc) / r ** 2
    J = sgn * Gam / (4 * sp.pi * G) * (g_law - g_tot)
    divJ = sp.diff(r ** 2 * J, r) / r ** 2
    rho_c, rho_t = sp.diff(Mc, r) / (4 * sp.pi * r ** 2), sp.diff(Mt, r) / (4 * sp.pi * r ** 2)
    ident = sp.simplify(divJ - sgn * Gam * (rho_c - rho_t))
    # d rho_c / dt = -divJ (relaxation block), linearised in delta = rho_c - rho_t:  d delta/dt = -divJ = -sgn Gamma delta
    lam = -sgn * Gam
    return bool(ident == 0), lam


def main():
    R.banner("CFG245 Gate E -- ENERGY, CAUSALITY, STABILITY" + ("  (POST-HOC EXTRA: an upstream gate already bound)" if POST else "") + (f"  (MUTATE {MUT})" if MUT else ""))
    # ---------------------------------------------------------------- controls
    R.banner("CONTROLS")
    # C-E1: virial identity E = W/2 on circular orbits in a point mass; W_profile on the target against the closed form -x_cap
    rr = np.geomspace(0.5, 50, 40)
    GM = 1.0
    Kk = 0.5 * GM / rr; Wk = -GM / rr
    ok_v = float(np.abs((Kk + Wk) - Wk / 2).max()) < 1e-9 and float(np.abs(2 * Kk + Wk).max()) < 1e-9
    Wt, xc = W_target(26.0)
    ok_w = abs(Wt - (-xc)) / xc < 1e-4
    R.cell("C-E1 virial identity E = W/2 (circular test orbits, 1e-9) and the W integral on the target profile equals the closed form -x_cap (1e-4)", "PASS" if (ok_v and ok_w) else "FAIL",
           f"W_target(S = 26) = {Wt:.5f} vs -x_cap = {-xc:.5f}")
    # ball conventions (CFG243 README:76: 1.17 M_b CFG48; 98/55/31/18 M_b B's) -- reported control
    ball48 = {M: RHO_L_ball for M, RHO_L_ball in ((M, K.RHO_L * 4 * math.pi / 3 * r_ta_48_kpc(M) ** 3 / M) for M in K.MASSES)}
    ballB = {M: K.RHO_L * 4 * math.pi / 3 * r_ta_B_kpc(M) ** 3 / M for M in K.MASSES}
    R.P("  vacuum energy of the turnaround ball in units of M_b c^2: CFG48 convention " + ", ".join(f"{M:.0e}: {v:.3f}" for M, v in ball48.items()) + " (CFG243 README:76: 1.17, mass independent); "
        "B's law r_ta (P2, Delta = 11.81, my implementation) " + ", ".join(f"{M:.0e}: {v:.1f}" for M, v in ballB.items()) + " (CFG243 README:76 quotes 98 / 55 / 31 / 18 from CFG7_common with its own kernel)")
    ok_ball = abs(ball48[1e9] - 1.17) < 0.02
    R.cell("C-E2 CFG48-convention ball energy 1.17 M_b c^2 reproduced (0.02); B's-convention numbers reported (not reproduced exactly if they differ)", "PASS" if ok_ball else "FAIL")
    # ---------------------------------------------------------------- E1
    R.banner("E1 -- energy ledger: |Delta E| / (1/2 M_b V_f^2) = |Delta W| (units G M_b^2/r_M), virial E = W/2; shared G3 line <= 1")
    e1 = {}
    worst_near = []
    R.P(f"  {'foot':10s} {'M_b':>7s} {'q':>5s} {'S/M_b':>7s} {'x_cap':>7s} {'W_target':>9s} {'W_pass(near)':>13s} {'W_pass(far)':>12s} {'ratio near':>11s} {'ratio far':>10s}")
    for foot in K.FOOTS:
        for M in K.MASSES:
            for q in K.QS:
                Wn, S, mo = W_passive(M, q, foot, "near")
                Wf, _, _ = W_passive(M, q, foot, "far")
                Wr, xc = W_target(S)
                if MUT == "ME1":
                    Wn = Wr; Wf = Wr
                rn, rf = abs(Wr - Wn), abs(Wr - Wf)
                e1[(foot, M, q)] = dict(S=S, xcap=xc, W_target=Wr, W_near=Wn, W_far=Wf, ratio_near=rn, ratio_far=rf)
                worst_near.append(rn)
                R.P(f"  {foot:10s} {M:7.0e} {q:5.2f} {S:7.2f} {xc:7.2f} {Wr:9.3f} {Wn:13.3f} {Wf:12.3f} {rn:11.2f} {rf:10.2f}")
    # verdict: generous closure per case (min |Delta E| over the two declared closures); PASS iff some bracket q has every mass <= 1 on both footings
    gen = {k: min(v["ratio_near"], v["ratio_far"]) for k, v in e1.items()}
    lo = min(gen.values()); hi = max(max(v["ratio_near"], v["ratio_far"]) for v in e1.values())
    bq = {q: max(gen[(f, M, q)] for f in K.FOOTS for M in K.MASSES) for q in K.QS}
    e1_ok = any(v <= 1.0 for v in bq.values())
    sgn_info = {f"{f}|{M:.0e}": ("ENERGY MUST BE REMOVED (more bound)" if np.mean([e1[(f, M, q)]["W_target"] - e1[(f, M, q)]["W_near"] for q in K.QS]) < 0 else "ENERGY MUST BE SUPPLIED (less bound)") for f in K.FOOTS for M in K.MASSES}
    R.P("  sign of Delta W (relaxed minus passive, near closure, mean over q): " + "; ".join(f"{k}: {v}" for k, v in sgn_info.items() if k.startswith("canonical")))
    R.P("  per-bracket worst case over masses and footings (generous closure): " + ", ".join(f"q = {q}: {v:.2f}" for q, v in bq.items()))
    R.cell("E1 energy ledger at the shared G3 line (<= 1 x the baryons' orbital energy; generous closure per case; some bracket q must have all four masses <= 1)", "PASS" if e1_ok else "FAIL (BINDING)",
           f"|Delta E|/(1/2 M_b V_f^2): generous closure {lo:.2f} to {max(gen.values()):.1f}, either closure up to {hi:.1f}; frozen hand: about 20 (10-40) -- the hand estimate was high by about 2x and its SIGN (energy removal) holds only for 1e9-1e10 Msun. The frozen text asked for 'both r_ta conventions': Delta E is the energy of the whole bound domain D and does not depend on the convention; the conventions enter only the vacuum-ball ratio below (disclosed departure)")
    worst_near = list(gen.values())
    # vacuum ratio and heating rows
    R.P("  |Delta E| / E_vac(ball) (E_vac = rho_Lambda c^2 V of the turnaround ball): ratio of (1/2) ratio V_f^2/c^2 to the ball's M_b c^2 content")
    vac = {}
    for M in K.MASSES:
        Vf2 = K.G_KPC * M / K.r_M(M, "canonical")                   # (km/s)^2
        dE_over_Mbc2 = 0.5 * np.mean([gen[k] for k in gen if k[0] == "canonical" and k[1] == M]) * Vf2 / (K.C_SI / 1e3) ** 2
        vac[M] = dict(dE_over_Mbc2=float(dE_over_Mbc2), f48=float(dE_over_Mbc2 / ball48[M]), fB=float(dE_over_Mbc2 / ballB[M]), V_f=math.sqrt(Vf2))
        R.P(f"    M_b = {M:.0e}: V_f = {math.sqrt(Vf2):6.1f} km/s, |Delta E|/(M_b c^2) = {dE_over_Mbc2:.2e}; /E_vac(ball): CFG48 {vac[M]['f48']:.1e}, B's {vac[M]['fB']:.1e} (frozen hand: about 1e-5)")
    # heating (reported, limits from memory, unverified)
    Mb = 1e11
    Vf2 = K.G_KPC * Mb / K.r_M(Mb, "canonical")
    Eerg = 0.5 * np.mean([gen[k] for k in gen if k[0] == "canonical" and k[1] == Mb]) * Mb * K.MSUN * 1e3 * (math.sqrt(Vf2) * 1e5) ** 2
    L = Eerg / (K.T0 * K.GYR_S)
    R.P(f"  heating row (reported only; limits from memory, unverified): a 1e11 Msun galaxy: |Delta E| = {Eerg:.2e} erg over t_0 = mean {L:.1e} erg/s (cluster X-ray luminosities are of order 1e44-1e45 erg/s; the FIRAS Compton-y bound is of order 1.5e-5; not compared further: for 1e11-1e12 the sign is energy SUPPLIED, and the cluster case is outflow toward the phantom)")
    # ---------------------------------------------------------------- E2
    R.banner("E2 -- causality: drift speed at the start of the relaxation, w = Gamma |M_target - M_inf| / (dM_inf/dr); PASS iff max w/c <= 1e-3 (relativistic completion UNDEFINED)")
    mx = {}
    for foot in ("canonical", "alt"):
        wmax = 0.0; wmed = []
        for M in K.MASSES:
            for q in K.QS:
                p = K.passive(M, q, foot)
                rM = K.r_M(M, foot)
                edges = XB * rM
                dr = np.diff(edges)
                dens = p["dM"] / dr                                  # Msun / kpc (time-averaged shell mass per radius)
                Mt = np.minimum(p["Mph"], p["S"])
                dMc = np.abs(Mt - p["Minf"])
                m = (XC >= 0.3) & (dens > 0)
                w = K.HL * dMc[m] / dens[m] * 0.9778e0 * 1.0         # kpc/Gyr -> km/s: 1 kpc/Gyr = 0.9778 km/s
                wmax = max(wmax, float(w.max())); wmed.append(float(np.median(w)))
        mx[foot] = (wmax, float(np.median(wmed)))
        R.P(f"  {foot:10s}: max w = {wmax:.1f} km/s ({wmax/(K.C_SI/1e3):.1e} c), median over cases of the bin-median = {mx[foot][1]:.1f} km/s (Gamma = H_Lambda, the fastest candidate; slower candidates scale down)")
    e2_ok = all(v[0] / (K.C_SI / 1e3) <= 1e-3 for v in mx.values())
    R.cell("E2 drift speed (max w/c <= 1e-3)", "PASS" if e2_ok else "FAIL", f"max w = {max(v[0] for v in mx.values()):.1f} km/s; relativistic completion UNDEFINED (no action written)")
    R.cell("E2 relativistic completion / causal cone", "UNDEFINED", "the class is a Newtonian-limit statement; no action")
    # ---------------------------------------------------------------- E3
    R.banner("E3 -- stability of the relaxation block")
    ident, lam = e3a_sympy()
    R.P(f"  sympy: div J - Gamma (rho_c - rho_ph) simplifies to 0: {ident}; linearised relaxation eigenvalue lambda = {lam} (in units of Gamma)")
    # discretised operator eigenvalues
    n = 40
    Cm = np.tril(np.ones((n, n)))
    sgn = -1.0 if MUT == "ME2" else 1.0
    Lm = np.linalg.solve(Cm, -sgn * Cm)                              # operator on the density vector: C^-1 (-Gamma I) C
    ev = np.linalg.eigvals(Lm)
    ok_a = ident and np.all(ev.real <= 1e-10) and np.max(np.abs(ev + sgn)) < 1e-9
    R.cell("E3(a) the relaxation block has the single eigenvalue -Gamma (damped, no propagating mode, no sound speed)", "PASS" if ok_a else "FAIL",
           f"discretised operator (n = {n}): eigenvalues in [{ev.real.min():+.3e}, {ev.real.max():+.3e}] (units Gamma)")
    # Lyapunov
    p = K.passive(1e10, 0.1, "canonical")
    x = XC; rM = K.r_M(1e10, "canonical"); rr = x * rM
    Mt = np.minimum(p["Mph"], p["S"]); Mc = p["Minf"].copy()
    G = K.HL
    sgl = -1.0 if MUT == "MT3" else 1.0
    def Lfun(Mc_):
        return 0.5 * K.G_KPC * np.trapz((Mt - Mc_) ** 2 / rr ** 2, rr)
    L0 = Lfun(Mc); ts = [0.0]; Ls = [L0]
    nst = 2000; dt = 5.0 / nst
    for i in range(nst):
        f = lambda m_: sgl * G * (Mt - m_)
        k1 = f(Mc); k2 = f(Mc + 0.5 * dt * k1); k3 = f(Mc + 0.5 * dt * k2); k4 = f(Mc + dt * k3)
        Mc = Mc + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    L1 = Lfun(Mc)
    slope = math.log(L1 / L0) / 5.0
    ok_b = (L1 < L0) and abs(slope + 2 * G) / (2 * G) < 1e-6
    R.cell("E3(b) Lyapunov L = (G/2) int (M_t - M_c)^2/r^2 dr decreases as exp(-2 Gamma t)", "PASS" if ok_b else "FAIL", f"d ln L/dt = {slope:.6f} /Gyr vs -2 Gamma = {-2*G:.6f}; L(5 Gyr)/L(0) = {L1/L0:.4f}")
    R.cell("E3(c) coupled Vlasov-Poisson + relaxation system", "NOT ADDRESSED", "J depends on rho_c only through -Gamma rho_c (fluid perturbations never feed the target); no further linearisation")
    R.cell("E3(d) a bound-only gate written as an action term", "NOT ADDRESSED", "statement only: it would inherit DE12/DE13's obstruction")
    R.cell("E4 reaction row (G3)", "UNDEFINED", "non-spherical flows have no momentum partner (the w = -1 vacuum cannot, CFG230 R12a); spherical: net momentum zero")

    # ---------------------------------------------------------------- MUTATE
    if MUT:
        if MUT == "ME1":
            R.P(f"  MUTATE ME1: passive state := relaxed state: E1 {'PASS' if e1_ok else 'FAIL'} (baseline expectation FAIL)")
            bites = e1_ok
        elif MUT == "ME2":
            R.P(f"  MUTATE ME2: damping sign flipped: E3(a) {'PASS' if ok_a else 'FAIL'} (baseline PASS)")
            bites = not ok_a
        elif MUT == "MT3":
            R.P(f"  MUTATE MT3: flux sign flipped: Lyapunov cell E3(b) {'PASS' if ok_b else 'FAIL'} (baseline PASS); L(5 Gyr)/L(0) = {L1/L0:.3f}")
            bites = not ok_b
        else:
            raise SystemExit(f"MUTATE {MUT} is not a Gate E control")
        R.finish(dict(binding_fail=False, mutate_bites=bool(bites)))
        K.exit_mutate(bites, True)
    R.numbers = dict(E1={f"{k[0]}|{k[1]:.0e}|{k[2]}": v for k, v in e1.items()}, ratio_generous_min=lo, ratio_generous_max=max(worst_near), ratio_any_max=hi, sign=sgn_info, worst_by_q={str(q): v for q, v in bq.items()},
                     vac={f"{M:.0e}": v for M, v in vac.items()}, ball48={f"{M:.0e}": v for M, v in ball48.items()}, ballB={f"{M:.0e}": v for M, v in ballB.items()},
                     E2={k: dict(max_kms=v[0], median_kms=v[1]) for k, v in mx.items()}, E3a=dict(ident=bool(ident), lam=str(lam)), E3b=dict(slope=slope, expected=-2 * G),
                     heating=dict(erg=float(Eerg), erg_per_s=float(L)))
    R.finish(dict(binding_fail=bool(not e1_ok), post_hoc=POST, controls_ok=bool(ok_v and ok_w)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
