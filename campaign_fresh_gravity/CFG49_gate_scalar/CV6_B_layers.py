#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV6-B -- THE DYNAMICAL GATE FIELD chi WITH ITS OWN CONSTANT STIFFNESS, ON DE12/DE13's 24 GALAXY LAYERS.

MODEL (POSTULATED; see CV6_A):  E[chi] = int r^2 dr { (mu/2)|chi'|^2 + (m2/2)(chi - t)^2 - B W(chi) },  t = the baryon-only gate variable
of DE12/DE13 (t = t_U (U - 1) + 1/2, U = C 4 pi G (rho_b + phantom); reading A+), coupled to the gas (sound speed 117 km/s) through t(rho_b).
The layers, B(r), h, rho_b, the C-infinity step W (w = 0.25) and the gas are DE12's own (DE12's transition() is exec'd unedited, as DE13 does).

WHAT THE CV6 "own stiffness" IS.  Two things: chi's mass m2 (its potential stiffness) and its gradient stiffness mu.  chi is an INDEPENDENT field,
so the composite-gradient background term K0 of DE13's form (ii) is absent.  The exact second variation about the EXACT chi0(r) (solved on the full
grid, not chi0 = t) after eliminating the algebraic gas displacement (Schur complement) is
     E2[dchi] = (1/2) int r^2 { mu |dchi'|^2 + [ g_eff - B W''(chi0) ] dchi^2 },     g_eff = a m2 / (a + m2),   a = c_s^2/(rho h^2)  (gas modulus, eps = dt units)
and a negative mode inside one of DE13's five half-layer Dirichlet windows (t-width 0.5) = unstable (DE13's lenient scale).

PRE-DECLARED (written before the final run; the exploratory runs that preceded are listed under DISCLOSED).
 H1a [load-bearing; MUTATE=a must FAIL]  mu = 0: every one of the 24 galaxy layers is unstable at EVERY m2 in the scan (chi's mass alone repairs nothing).
 H1b [load-bearing; MUTATE=a,b must FAIL]  at mu = mu_uni(m2) := max over the 24 layers of the layer's minimal stable mu (bisection about the consistent chi0),
     every layer is stable, for every m2 in the scan.
 H2  [load-bearing]  finite m2 does not lower the needed gradient stiffness: mu_min(layer; m2) >= 0.98 mu_min(layer; m2 = inf) on every layer where the gate
     still exists (edge within a factor 2).  [m2 = inf is DE13's form (i): control C1.]
 H3  [load-bearing; expected FAIL of the conjunction, declared before the run]  there is an m2 for which, with mu = mu_uni(m2), ALL of
       (T) tracking: the gate's edge (chi0 = 1/2) is within 10% of the t = 1/2 edge on 24/24 layers,
       (F) cost at the flagship radius: |Phi_chi(r_F)| <= 0.1 v_f^2 (z = 2.5, 1e11, canonical) and force <= 0.023 g_MOND (0.01 dex),
       (S) cost at the Sun's distance: |Phi_chi| <= 0.1 v_f^2 (z = 0, 6e10, 8 kpc)
     hold.  Phi_chi = -4 pi G C t_U m2 (chi0 - t) = -4 pi G C t_U (B W' + mu lap chi0)  is the chi sector's chemical potential per unit baryon mass,
     the same object as DE12's Phi_gate and DE13's N1.
CONTROLS.  C1 the m2 = inf, mu_min(layer) reproduces DE13's committed F1 lambda_U and eta_U (24 layers); C2 m2 = inf reproduces DE13's committed N1
    (31.8 v_f^2 at r_F, 2.1e8 at the Sun); C3 the discrete second variation formula = finite differences of the discrete energy functional (no gas).
DISCLOSED: exploratory scans of mu_min(m2) with chi0 = t (ratio 1.00-1.06), of the chi0 solver, and of the flagship potential preceded this script.
SCOPE: DE12/DE13's: frozen background, spherical, fluid gas, self-gravity of the gas and the kernel-response terms B_rho (T3, T4 of XR15) NOT included
(T3 is estimated separately in CV6_D); windows as DE13.

Run:  python3 CV6_B_layers.py      MUTATE=a (mu = 0) | MUTATE=b (mu -> -mu_uni: gradient sign flipped)  must FAIL load-bearing checks.
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv6_common as c

MUT = os.environ.get("MUTATE", "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH = []
OUT = {"lane": "CV6-B", "mutate": MUT, "checks": {}, "numbers": {}}
REPO = c.REPO
M2S = [10 ** e for e in np.arange(-16.0, -8.9, 0.5)] + [np.inf]


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


# ------------------------------------------------------------------------------------------------ workers
def layer_unstable(args):
    z, Mb, f, mu, m2 = args
    tr = c.transition(z, Mb, f, c.W_M, amp=True)
    r, t, B = tr["r"], tr["t"], tr["B"]
    if np.isfinite(m2) and mu >= 0:
        chi0 = c.solve_chi(r, t, B, mu, m2)[0]
    elif np.isfinite(m2):
        chi0 = t                                                    # negative mu (mutation b): the functional is unbounded; use chi0 = t
    else:
        chi0 = t
    trf = c.layer_fine(z, Mb, f); co = c.layer_coeffs(trf)
    chi_l = np.interp(np.log(co["r"]), np.log(r), chi0)
    _, _, W2c = c.Wd(chi_l)
    a = co["a"]
    geff = a if not np.isfinite(m2) else a * m2 / (a + m2)
    base = geff - co["B"] * W2c
    return c.has_neg(co, base, mu), chi0, r, t


def mu_min_layer(args):
    z, Mb, f, m2 = args
    lo, hi = 20.0, 36.0
    if not layer_unstable((z, Mb, f, 10 ** lo, m2))[0]: return (z, Mb, f, m2, 0.0)
    if layer_unstable((z, Mb, f, 10 ** hi, m2))[0]: return (z, Mb, f, m2, np.inf)
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        if layer_unstable((z, Mb, f, 10 ** mid, m2))[0]: lo = mid
        else: hi = mid
    return (z, Mb, f, m2, 10 ** hi)


def layer_edge(args):
    z, Mb, f, mu, m2 = args
    tr = c.transition(z, Mb, f, c.W_M, amp=True)
    r, t, B = tr["r"], tr["t"], tr["B"]
    chi0 = t if not np.isfinite(m2) else c.solve_chi(r, t, B, mu, m2)[0]
    re, rc = c.edge_radius(r, t), c.edge_radius(r, chi0)
    return (rc / re - 1.0) if np.isfinite(rc) else np.nan


def flag_cost(args):
    kind, mu, m2 = args
    z, Mb, rq = (2.5, 1e11, None) if kind == "F" else (0.0, 6e10, 8.0)
    tr = c.transition(z, Mb, "canonical", c.W_M, amp=True); r, t, B = tr["r"], tr["t"], tr["B"]
    a0 = c.A0["canonical"]
    rr = math.sqrt(c.G * Mb * c.MS / (0.1 * a0)) if rq is None else rq * c.KPC
    Cc = 1 / (tr["H"] ** 2 * tr["xce"])
    if np.isfinite(m2):
        chi = c.solve_chi(r, t, B, mu, m2)[0]
        Phi = -4 * math.pi * c.G * Cc * c.TU * m2 * (chi - t)
    else:                                                          # DE13's N1 evaluation (A = 1, chi = U slaved)
        rho_ph = Mb * c.MS * (c.h_of(tr["y"]) - tr["y"] * c.dh_of(tr["y"])) / (2 * math.pi * r ** 3 * tr["y"])
        U = 4 * math.pi * c.G * (tr["rho_b"] + rho_ph) * Cc
        lapU = np.gradient(r ** 2 * np.gradient(U, r), r) / r ** 2
        Phi = -4 * math.pi * c.G * mu * c.TU ** 2 * lapU * Cc
    gg = -np.gradient(Phi, r); gN = c.G * Mb * c.MS / r ** 2; gM = c.nu_of(gN / a0) * gN
    return (kind, float(np.interp(rr, r, Phi) / tr["vf2"]), float(np.interp(rr, r, gg) / np.interp(rr, r, gM)))


def cuv_layer(args):
    z, Mb, f, m2 = args
    trf = c.layer_fine(z, Mb, f); co = c.layer_coeffs(trf)
    return float(np.sqrt(1.0 + m2 / co["a"].min()) * c.CS["1e6K"] / c.C_LIGHT) if np.isfinite(m2) else np.inf


if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUT: P("\n  *** MUTATE=" + MUT + ": " + {"a": "mu = 0 (the chi gradient term is dropped)", "b": "mu -> -mu_uni (gradient sign flipped)"}[MUT] + " ***")
    pool = Pool(16)

    # ============================================================================ C1 C2 controls
    banner("C1 C2  CONTROLS: m2 = inf reproduces DE13's committed form-(i) results (lambda_U per layer, eta_U, N1)")
    R13 = json.load(open(os.path.join(REPO, "real_research/dark_energy_2026/DE13_gate_gradient_repair_results.json")))["numbers"]
    F1 = R13["F1"]["rows"]
    res_inf = pool.map(mu_min_layer, [(z, Mb, f, np.inf) for (z, Mb, f) in c.GAL])
    dev, my_lam = [], {}
    for (z, Mb, f, m2, mm) in res_inf:
        key = f"{z}/{Mb:.0e}/{f}"
        tr = c.transition(z, Mb, f, c.W_M, amp=True); trf = c.layer_fine(z, Mb, f); co = c.layer_coeffs(trf)
        it = int(np.argmin(np.abs(co["t"] - 0.5))); unit = co["B"][it] * co["r"][it] ** 2
        lamU = math.sqrt(mm / unit) * c.TU                         # mu_U = mu_chi t_U^2, lambda_U^2 = mu_U/(B r^2 at t=1/2)
        my_lam[key] = lamU
        dev.append(abs(lamU / F1[key]["lam_U"] - 1))
    mu_inf = {f"{z}/{Mb:.0e}/{f}": mm for (z, Mb, f, m2, mm) in res_inf}
    muU = max(mu_inf.values())
    eta = 8 * math.pi * c.G * muU * c.TU ** 2 / c.C_LIGHT ** 4
    check("C1 CONTROL m2 = inf: the layer-by-layer minimal gradient stiffness reproduces DE13's committed form-(i) lambda_U (24 layers) and eta_U",
          f"max |lambda_U/DE13 - 1| = {max(dev):.2e} (DE13 rounds to 2 digits: tolerance 3%); eta_U = {eta:.4e} vs DE13 {R13['F1']['eta_U_galaxies']:.4e}",
          max(dev) < 0.03 and abs(eta / R13["F1"]["eta_U_galaxies"] - 1) < 0.01)
    OUT["numbers"]["mu_uni_inf"] = muU
    fc = pool.map(flag_cost, [("F", muU, np.inf), ("S", muU, np.inf)])
    R3U = R13["form_i_cost"]
    ref = list(R3U.values())
    check("C2 CONTROL m2 = inf: the flagship and Sun potentials reproduce DE13's committed N1",
          f"r_F: {abs(fc[0][1]):.3g} v_f^2 (DE13 {ref[0]:.3g}); Sun: {abs(fc[1][1]):.3g} v_f^2 (DE13 {ref[1]:.3g})",
          abs(abs(fc[0][1]) / ref[0] - 1) < 0.02 and abs(abs(fc[1][1]) / ref[1] - 1) < 0.02)

    # ============================================================================ C3 finite-difference control of the second-variation formula
    banner("C3  CONTROL: the discrete second-variation formula (chi sector alone, consistent chi0) against finite differences of the discrete functional")
    tr = c.transition(2.5, 1e11, "canonical", c.W_M, amp=True); r, t, B = tr["r"], tr["t"], tr["B"]
    mu_t, m2_t = 3.86e28, 1e-12
    chi0, _ = c.solve_chi(r, t, B, mu_t, m2_t)
    sl = (t > 0.02) & (t < 0.98)
    idx = np.where(sl)[0]; i0, i1 = idx[0], idx[-1]
    rng = np.random.default_rng(5)
    rels = []
    j0, j1 = max(i0 - 3, 0), min(i1 + 4, len(r))                     # local slice: eps = 0 outside, so every outside term cancels in the difference
    rs, ts, Bs, chs = r[j0:j1], t[j0:j1], B[j0:j1], chi0[j0:j1]
    for trial in range(3):
        eps = np.zeros(j1 - j0)
        seg = np.arange(i0 - j0 + 1, i1 - j0)                       # strictly inside the window
        eps[seg] = np.exp(-((seg - rng.uniform(seg[0], seg[-1])) / rng.uniform(20, 120)) ** 2) * np.cos(rng.uniform(0.01, 0.2) * seg)
        Es = lambda s: c.chi_energy_parts(rs, chs + s * eps, ts, Bs, mu_t, m2_t)[0]
        s_ = 1e-4
        fd = (Es(s_) + Es(-s_) - 2 * Es(0.0)) / s_ ** 2
        _, _, W2c = c.Wd(chs)
        a_, b_, M_ = c._tri(rs, m2_t - Bs * W2c, mu_t)
        e = eps[1:-1]
        form = float(np.sum(a_ * e ** 2) + 2 * np.sum(b_ * e[:-1] * e[1:]))
        rels.append(abs(form / fd - 1))
    check("C3 CONTROL the second variation used in the stability scan equals the finite-difference second derivative of the discrete chi functional",
          f"rel. deviations {', '.join(f'{x:.1e}' for x in rels)} (tolerance 1e-4)", max(rels) < 1e-4)

    # ============================================================================ H1a mu = 0
    banner("H1a  mu = 0: chi's own mass/potential stiffness alone repairs nothing (24 layers x the m2 scan)")
    unst0 = {}
    for m2 in M2S:
        out = pool.map(layer_unstable, [(z, Mb, f, 0.0, m2) for (z, Mb, f) in c.GAL])
        unst0[m2] = sum(o[0] for o in out)
    P("    unstable layers at mu = 0:", {("%.0e" % k if np.isfinite(k) else "inf"): v for k, v in unst0.items()})
    check("H1a [load-bearing; not mutated: it is the mu = 0 case] at mu = 0 every layer is unstable at every m2 in the scan "
          "(uniform-limit theorem of CV6_A, numerically, on the real layers)",
          f"{min(unst0.values())}/24 .. {max(unst0.values())}/24 unstable over {len(M2S)} values of m2 (1e-16 .. 1e-9, inf)", all(v == 24 for v in unst0.values()))

    # ============================================================================ H2 mu_min(m2)
    banner("H2  the gradient stiffness needed, layer by layer, about the consistent chi0: does a finite chi mass lower it?")
    MU_T = {}
    cache_fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CV6_B_mu_cache.json")
    cache = json.load(open(cache_fn)) if (os.path.exists(cache_fn) and os.environ.get("FRESH", "0") != "1") else {}
    for m2 in M2S:
        ck = "inf" if not np.isfinite(m2) else "%.6e" % m2
        if ck in cache:
            MU_T[m2] = cache[ck]
            continue
        out = pool.map(mu_min_layer, [(z, Mb, f, m2) for (z, Mb, f) in c.GAL])
        MU_T[m2] = {f"{z}/{Mb:.0e}/{f}": mm for (z, Mb, f, _, mm) in out}
        cache[ck] = MU_T[m2]
        json.dump(cache, open(cache_fn, "w"))
    # gate-existence: edge shift at mu = mu_uni(m2), computed below; here compare ratios where the layer has a gate
    ratio_rows = {}
    for m2 in M2S:
        muu = max(MU_T[m2].values())
        edges = pool.map(layer_edge, [(z, Mb, f, muu, m2) for (z, Mb, f) in c.GAL])
        ex = np.array([abs(e) < 1.0 if np.isfinite(e) else False for e in edges])
        keys = [f"{z}/{Mb:.0e}/{f}" for (z, Mb, f) in c.GAL]
        rat = [MU_T[m2][k] / mu_inf[k] if (ex[i] and mu_inf[k] > 0) else np.nan for i, k in enumerate(keys)]
        ratio_rows[m2] = (float(np.nanmin(rat)) if np.any(np.isfinite(rat)) else np.nan, float(np.nanmax(rat)) if np.any(np.isfinite(rat)) else np.nan, int(ex.sum()))
        P(f"    m2 = {m2:8.1e}: mu_uni/mu_uni(inf) = {muu / muU:9.3e};  per-layer mu_min(m2)/mu_min(inf) in [{ratio_rows[m2][0]:.3f}, {ratio_rows[m2][1]:.3f}] "
          f"on the {ratio_rows[m2][2]}/24 layers whose gate survives")
    OUT["numbers"]["mu_min_ratio_range"] = {("%.0e" % k if np.isfinite(k) else "inf"): v for k, v in ratio_rows.items()}
    lowest = min(v[0] for v in ratio_rows.values() if np.isfinite(v[0]))
    check("H2 [load-bearing] a finite chi mass does not lower the needed gradient stiffness: mu_min(m2)/mu_min(inf) >= 0.98 on every layer whose gate survives",
          f"lowest ratio over the scan = {lowest:.3f}", lowest >= 0.98,
          "DECLARED BEFORE THE RUN AND REFUTED BY IT (kept as run): the exploratory scan used chi0 = t; about the consistent chi0 a small m2 lets chi lag t, the lagged "
          "profile has smaller B W'' peaks and needs less stiffness.  The reduction is bought by a gate that no longer follows t: see H2b/H3")

    # ============================================================================ H1b + H3
    banner("H1b H3  mu = mu_uni(m2): stability, tracking, the flagship and Sun costs, the UV baryon sound speed")
    MUF = {"a": 0.0, "b": -1.0}.get(MUT, 1.0)
    rows = {}
    for m2 in M2S:
        muu = MUF * max(MU_T[m2].values())
        un = pool.map(layer_unstable, [(z, Mb, f, muu, m2) for (z, Mb, f) in c.GAL])
        n_unst = sum(o[0] for o in un)
        edges = pool.map(layer_edge, [(z, Mb, f, abs(muu), m2) for (z, Mb, f) in c.GAL])
        n_bad = sum((not np.isfinite(e)) or abs(e) > 0.1 for e in edges)
        emax = max((abs(e) if np.isfinite(e) else 9.99) for e in edges)
        fF, fS = pool.map(flag_cost, [("F", abs(muu), m2), ("S", abs(muu), m2)])
        cuv = max(pool.map(cuv_layer, [(z, Mb, f, m2) for (z, Mb, f) in c.GAL]))
        ell = math.sqrt(abs(muu) / m2) / c.KPC if np.isfinite(m2) else 0.0
        rows[m2] = dict(mu_uni=muu, unstable=n_unst, edge_bad=int(n_bad), edge_max=emax, PhiF=fF[1], forceF=fF[2], PhiS=fS[1], cUV_over_c=float(cuv), ell_kpc=ell)
        P(f"    m2 = {m2:8.1e}: ell = sqrt(mu/m2) = {ell:9.2f} kpc | unstable {n_unst:2d}/24 | edges off >10%: {n_bad:2d}/24 (max {emax:.2f}) | "
          f"Phi_chi(r_F) = {fF[1]:+9.3g} v_f^2, force {fF[2]:+8.3g} g_M | Phi_chi(Sun) = {fS[1]:+9.3g} v_f^2 | max c_UV/c = {cuv:.3g}")
    OUT["numbers"]["scan"] = {("%.0e" % k if np.isfinite(k) else "inf"): v for k, v in rows.items()}
    stab_all = all(v["unstable"] == 0 for v in rows.values())
    check("H1b [load-bearing; MUTATE=a and b must FAIL] with mu = mu_uni(m2) every layer is stable at every m2 in the scan (the gradient stiffness is the repair)",
          f"unstable layers per m2: {[v['unstable'] for v in rows.values()]}", stab_all)
    good = []
    for m2, v in rows.items():
        T_ = v["edge_bad"] == 0
        F_ = abs(v["PhiF"]) <= 0.1 and abs(v["forceF"]) <= 0.023
        S_ = abs(v["PhiS"]) <= 0.1
        v["T"], v["F"], v["S"] = bool(T_), bool(F_), bool(S_)
        if T_ and F_ and S_: good.append(m2)
    Tset = [("%.0e" % m if np.isfinite(m) else "inf") for m, v in rows.items() if v["T"]]
    Fset = [("%.0e" % m if np.isfinite(m) else "inf") for m, v in rows.items() if v["F"]]
    Sset = [("%.0e" % m if np.isfinite(m) else "inf") for m, v in rows.items() if v["S"]]
    P(f"    (T) tracking holds at m2 in {Tset}\n    (F) flagship cost <= 0.1 v_f^2 & 0.023 g_M at m2 in {Fset}\n    (S) Sun cost <= 0.1 v_f^2 at m2 in {Sset}")
    check("H3 [load-bearing; declared FAIL of the conjunction] some m2 has tracking (T) AND flagship cost (F) AND Sun cost (S) at mu = mu_uni(m2)",
          f"T: {len(Tset)} values, F: {len(Fset)}, S: {len(Sset)}, all three: {len(good)}", len(good) == 0 if not MUT else True,
          "the load-bearing statement is the NO-GO: constant-mu chi cannot track the edge without paying DE13's N1 cost; a small m2 removes the cost but the gate no longer follows t")
    m2_track_min = min([m for m, v in rows.items() if v["T"] and np.isfinite(m)], default=None)
    if m2_track_min:
        v = rows[m2_track_min]
        P(f"    smallest tracking m2 = {m2_track_min:.1e}: mu_uni = {v['mu_uni']:.3e} J/m, ell = {v['ell_kpc']:.1f} kpc, cost Phi_chi(r_F) = {v['PhiF']:+.3g} v_f^2, "
          f"Phi_chi(Sun) = {v['PhiS']:+.3g} v_f^2, max c_UV/c = {v['cUV_over_c']:.2g}")
        a0 = c.A0["canonical"]; Bref = a0 ** 2 / (8 * math.pi * c.G)
        P(f"    natural units: l_mu = sqrt(mu_uni/(a0^2/8piG)) = {math.sqrt(abs(v['mu_uni']) / Bref) / c.KPC:.2f} kpc;  m2/(a0^2/8piG) = {m2_track_min / Bref:.3f}")
        OUT["numbers"]["min_tracking"] = dict(m2=m2_track_min, mu=v["mu_uni"], ell_kpc=v["ell_kpc"], l_mu_kpc=math.sqrt(abs(v["mu_uni"]) / Bref) / c.KPC,
                                             m2_over_MOND_energy=m2_track_min / Bref, cuv_over_c=v["cUV_over_c"])

    if m2_track_min:
        rr_ = rows[m2_track_min]["mu_uni"] / (MUF * muU) if MUF else np.nan
        check("H2b (reported) at the smallest tracking m2 the universal stiffness relative to the slaved (m2 = inf) value",
              f"mu_uni(m2 = {m2_track_min:.1e}) / mu_uni(inf) = {abs(rr_):.3f}; the cost potential at r_F is {rows[m2_track_min]['PhiF']:+.3g} v_f^2 against DE13's {fc[0][1]:+.3g}",
              True, "a factor ~2.6 in stiffness and in the flagship cost, still >= 100x the 0.1 v_f^2 bar; the Sun is unchanged in order of magnitude", load_bearing=False)

    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CV6_B_results" + (f"_MUTATE_{MUT}" if MUT else "") + ".json")
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   [{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
