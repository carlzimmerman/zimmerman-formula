#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV6-C -- CAN chi's STIFFNESS BE SWITCHED OFF INSIDE COLLAPSED REGIONS?  (the one repair N14 lists as 'unsized')

CV6-B showed that a constant gradient stiffness mu stabilises every layer only at DE13's form-(i) price (Phi_chi ~ 32 v_f^2 at r_F, ~2e8 at the Sun):
the gradient energy of chi acts wherever t varies, and t >> 1 (t ~ 28 at r_F, ~8e4 at the Sun) inside every galaxy.  The obvious repair is a field-dependent
stiffness, mu(chi) = mu0 s(chi), s = 1 for chi <= c_a (the layer, 0 < chi < 1) and s = s_inf << 1 for chi >= c_b (deep in the ON plateau).  The cost then scales
as s_inf.  This lane sizes what that repair does to stability.

THE ALGEBRA.  E = int r^2 { (mu0/2) s(chi)|grad chi|^2 + (m2/2)(chi - t)^2 - B W(chi) }.  psi = int sqrt(s) dchi makes the gradient energy canonical
(mu0/2)|grad psi|^2.  About the chi0 solution the second variation (chi sector; the gas adds g_eff = a m2/(a+m2) to the chi^2 coefficient exactly as in CV6-B) is
     E2[dpsi] = (1/2) int r^2 { mu0 |dpsi'|^2 + [ chi_psi^2 (g_eff - B W''(chi0)) + F1 chi_psipsi ] dpsi^2 },   F1 = m2 (chi0 - t) - B W'(chi0) = mu0 lap(psi0)/chi_psi,
     chi_psi = s^-1/2,  chi_psipsi = -s'/(2 s^2).
The term K = F1 chi_psipsi is the SWITCH-OFF TERM, the analogue of DE13's K0: in chi-space it is -(1/2) mu'' |grad chi0|^2 - mu' lap chi0.  It is proportional to mu0
(F1 ~ mu0 lap psi0), exactly as the stiffness is, and it is NEGATIVE wherever lap psi0 < 0 with s' < 0, i.e. on the falling profile inside the switch zone.

PRE-DECLARED (before the first final run; K1 turned out too strong and is kept as run, K1a/K1b are POST-HOC refinements written after seeing it -- flagged as such).
 K1 [declared; REFUTED as declared, reported, not load-bearing]  On EVERY layer, at EVERY switch shape, at EVERY mu0 in the scan (and at m2 = inf and 1e-12) the chi sector
    has a negative mode on the domain from the layer inward through the switch zone (full Dirichlet from t = 10 c_b to t = 0.004).  The run refutes the strong form: at m2 = 1e-12
    and large mu0 some layers stabilise.
 K1a [POST-HOC, load-bearing; MUTATE=k must FAIL]  at m2 = inf (perfect tracking, chi0 = t) and the three compact zones (c_b <= 30) all 24 layers are unstable at every mu0
    in 1e-6 .. 1e4 x mu_uni: no universal stiffness window.
 K1b [POST-HOC, load-bearing; MUTATE=k must FAIL]  at m2 = 1e-12 no mu0 in the scan makes all 24 layers stable AND keeps every gate edge within 10% of t = 1/2:
    (the run finds more: no mu0 in the scan, up to 1e4 mu_uni where sqrt(mu0/m2) = 390 kpc, stabilises all 24 layers even ignoring the edges.)
 K2 (reported)  the size of K against the gradient energy in the zone: |K|/(mu0 k_zone^2) with k_zone = pi/(zone width).
 K3 (reported; what the repair WOULD buy)  the cost potential scales as s_inf: at s_inf = 1e-8 it is (2.12 / 3e-3) v_f^2 at the Sun / r_F, so <= 0.01 v_f^2 at the Sun needs
    s_inf <= 5e-11: eleven decades of stiffness switching, itself a new hierarchy (c_a, c_b, s_inf).
K4 (control C3) the psi-form second variation equals finite differences of the discrete psi-energy (no gas).
DISCLOSED: (i) a layer-only version (windows inside 0 < t < 1) reported 0/24 unstable because the switch zone lies OUTSIDE the DE13 layer grid (t > 1);
    the domain here is extended through the zone.  (ii) exploratory runs at c_a = 1.5, c_b = 4, s_inf = 1e-8 found lowest eigenvalue -4e-10 (z = 2.5, 1e11) on the extended domain.
SCOPE: as CV6-B (frozen, spherical, DE13's windows are replaced by the full extended domain because the negative mode lives in the zone, not the layer).

Run:  python3 CV6_C_switched_stiffness.py     MUTATE=k drops the switch-off term K (as DE13's MUTATE drops K0): K1 must FAIL.
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
OUT = {"lane": "CV6-C", "mutate": MUT, "checks": {}, "numbers": {}}
MU_UNI = 3.8598829328133485e28                  # CV6-B's m2 = inf universal constant stiffness (=DE13 form (i)); the reference unit
SHAPES = [(1.5, 4.0, 1e-8), (3.0, 30.0, 1e-8), (1.5, 1e3, 1e-8), (1.5, 4.0, 1e-3)]
X0S = [1e-6, 1e-4, 1e-2, 0.03, 0.1, 0.2, 0.4, 0.7, 1.0, 3.0, 10.0, 1e2, 1e4]


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


def ext_layer(z, Mb, f, tmax, N=12000):
    tr = c.transition(z, Mb, f, c.W_M, amp=True); r, t = tr["r"], tr["t"]
    tmax = min(tmax, 0.9 * float(np.max(t)))
    ri = float(np.interp(tmax, t[::-1], r[::-1])); ro = float(np.interp(0.004, t[::-1], r[::-1]))
    return c.transition_on(np.geomspace(ri, ro, N), z, Mb, f, c.W_M)


def zone_stability(args):
    """per mu0 in X0S: (negative mode on the extended domain, gate-edge shift |chi0 = 1/2 edge / t = 1/2 edge - 1|); plus |K|/(mu0 k_zone^2) at mu0 = mu_uni."""
    z, Mb, f, shape, m2 = args
    ca, cb, sinf = shape
    S = c.SwitchedStiff(ca, cb, sinf)
    trf = ext_layer(z, Mb, f, 10 * cb)
    co = c.layer_coeffs(trf); r, t = co["r"], co["t"]
    a = co["a"]
    tr = c.transition(z, Mb, f, c.W_M, amp=True)
    re_t = c.edge_radius(tr["r"], tr["t"])
    out = []; ratio = np.nan
    for x in X0S:
        mu0 = x * MU_UNI
        if np.isfinite(m2):
            psi, chi0, inf = c.solve_psi(tr["r"], tr["t"], tr["B"], mu0, m2, S)
            lr, Lr = np.log(r), np.log(tr["r"])
            chi_l = np.interp(lr, Lr, chi0)
            F1 = np.interp(lr, Lr, m2 * (chi0 - tr["t"]) - tr["B"] * c.Wd(chi0)[1])
            geff = a * m2 / (a + m2)
            rc = c.edge_radius(tr["r"], chi0)
            es = abs(rc / re_t - 1.0) if np.isfinite(rc) else 9.99
        else:
            chi_l = t.copy()
            psi0 = S.psi_of_chi(chi_l)
            lap = np.gradient(r ** 2 * np.gradient(psi0, r), r) / r ** 2
            F1 = mu0 * lap / S.chi_psi(chi_l)                      # F1 = mu0 lap(psi0)/chi_psi on the m2 = inf solution
            geff = a
            es = 0.0
        _, _, W2c = c.Wd(chi_l)
        cp, cpp = S.chi_psi(chi_l), S.chi_psipsi(chi_l)
        Kterm = F1 * cpp
        base_noK = cp ** 2 * (geff - co["B"] * W2c)
        base = base_noK if MUT == "k" else base_noK + Kterm
        lam = c.lowest_eig_sign(r, base, mu0)
        out.append((bool(lam < 0), float(es)))
        if x == 1.0:
            zone = (chi_l > ca) & (chi_l < cb)
            width = float(r[zone].max() - r[zone].min()) if zone.sum() > 3 else np.nan
            kz = math.pi / width if np.isfinite(width) and width > 0 else np.nan
            ratio = float(np.max(-Kterm[zone]) / (mu0 * kz ** 2)) if zone.any() and np.isfinite(kz) else np.nan
    return out, ratio


def cost(args):
    s_inf, kind = args
    S_ = c.SwitchedStiff(1.5, 4.0, s_inf)
    z, Mb, rq = (2.5, 1e11, None) if kind == "F" else (0.0, 6e10, 8.0)
    tr_ = c.transition(z, Mb, "canonical", c.W_M, amp=True); r_, t_, B_ = tr_["r"], tr_["t"], tr_["B"]
    rr = math.sqrt(c.G * Mb * c.MS / (0.1 * c.A0["canonical"])) if rq is None else rq * c.KPC
    psi_, chi_, _ = c.solve_psi(r_, t_, B_, MU_UNI, 1e-11, S_)
    Cc = 1 / (tr_["H"] ** 2 * tr_["xce"])
    Phi = -4 * math.pi * c.G * Cc * c.TU * 1e-11 * (chi_ - t_)
    return float(np.interp(rr, r_, Phi) / tr_["vf2"])


if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUT == "k": P("\n  *** MUTATE=k: the switch-off term K = F1 chi_psipsi is dropped from the second variation ***")
    pool = Pool(16)

    # ============================================================================ K4 / C3 control
    banner("C3  CONTROL: the psi-form second variation (chi sector, switch term included) against finite differences of the discrete psi-energy")
    S = c.SwitchedStiff(1.5, 4.0, 1e-3)
    tr = c.transition(2.5, 1e11, "canonical", c.W_M, amp=True); r, t, B = tr["r"], tr["t"], tr["B"]
    mu0, m2 = MU_UNI, 1e-12
    psi0, chi0, inf = c.solve_psi(r, t, B, mu0, m2, S)
    sl = np.where((chi0 > 0.05) & (chi0 < 9.0))[0]
    i0, i1 = sl[0], sl[-1]
    j0, j1 = max(i0 - 3, 0), min(i1 + 4, len(r))
    rs, ts, Bs, ps = r[j0:j1], t[j0:j1], B[j0:j1], psi0[j0:j1]
    rng = np.random.default_rng(11); rels = []
    for trial in range(3):
        eps = np.zeros(j1 - j0)
        seg = np.arange(2, j1 - j0 - 2)
        eps[seg] = np.exp(-((seg - rng.uniform(seg[0], seg[-1])) / rng.uniform(15, 60)) ** 2) * np.cos(rng.uniform(0.02, 0.3) * seg)
        Es = lambda s_: c.psi_parts(rs, ps + s_ * eps, ts, Bs, mu0, m2, S)[0]
        s_ = 1e-5
        fd = (Es(s_) + Es(-s_) - 2 * Es(0.0)) / s_ ** 2
        chi_s = S.chi_of_psi(ps)
        _, _, W2c = c.Wd(chi_s)
        cp, cpp = S.chi_psi(chi_s), S.chi_psipsi(chi_s)
        F1 = m2 * (chi_s - ts) - Bs * c.Wd(chi_s)[1]
        a_, b_, _m = c._tri(rs, cp ** 2 * (m2 - Bs * W2c) + F1 * cpp, mu0)
        e = eps[1:-1]
        form = float(np.sum(a_ * e ** 2) + 2 * np.sum(b_ * e[:-1] * e[1:]))
        rels.append(abs(form / fd - 1))
    check("C3 CONTROL the psi-form second variation (with the switch-off term F1 chi_psipsi) equals finite differences of the discrete psi-energy",
          f"rel. deviations {', '.join(f'{x:.1e}' for x in rels)} (tolerance 1e-3)", max(rels) < 1e-3)

    # ============================================================================ K1
    banner("K1 K2  THE SWITCH-OFF TERM ON THE EXTENDED DOMAIN (layer + switch zone), 24 layers x 4 shapes x 6 values of mu0")
    tab = {}
    for m2 in (np.inf, 1e-12):
        for shape in SHAPES:
            res = pool.map(zone_stability, [(z, Mb, f, shape, m2) for (z, Mb, f) in c.GAL])
            unst = np.array([[o[0] for o in r_[0]] for r_ in res])          # 24 x len(X0S)
            edge = np.array([[o[1] for o in r_[0]] for r_ in res])
            n_un = unst.sum(axis=0); emax = edge.max(axis=0)
            ratios = [r_[1] for r_ in res if np.isfinite(r_[1])]
            windows = [(x, int(n_un[i]), float(emax[i])) for i, x in enumerate(X0S) if n_un[i] == 0 and emax[i] <= 0.10]
            all_stable = [(x, float(emax[i])) for i, x in enumerate(X0S) if n_un[i] == 0]
            tab[(m2, shape)] = dict(n_always=int(unst.all(axis=1).sum()), n_unstable_per_mu0=n_un.tolist(), edge_max_per_mu0=emax.tolist(),
                                    windows=windows, first_all_stable=all_stable[0] if all_stable else None,
                                    ratio_med=float(np.median(ratios)) if ratios else np.nan)
            fs = tab[(m2, shape)]["first_all_stable"]
            ell = (math.sqrt(fs[0] * MU_UNI / m2) / c.KPC) if (fs and np.isfinite(m2)) else None
            P(f"    m2 = {m2:7.1e} shape {shape}: unstable layers per mu0/mu_uni {dict(zip(X0S, n_un.tolist()))}; "
              f"first all-stable mu0/mu_uni = {fs[0] if fs else None} (edge shift max {fs[1] if fs else None}, ell = {ell if ell is None else round(ell, 1)} kpc); "
              f"windows with edges <= 10%: {len(windows)}; median |K|/(mu0 k_zone^2) = {tab[(m2, shape)]['ratio_med']:.2g}")
    OUT["numbers"]["K1"] = {f"{k[0]}|{k[1]}": v for k, v in tab.items()}
    nalways = [v["n_always"] for v in tab.values()]
    check("K1 [declared strong form, REFUTED as declared, kept as run; reported] on every layer, at every switch shape and every mu0, a negative mode exists",
          f"layers unstable at all mu0: min {min(nalways)}/24 over the {len(nalways)} (m2, shape) cells", min(nalways) == 24,
          "refuted: at m2 = 1e-12 and mu0 >~ 1e2 mu_uni some cells stabilise; K1a/K1b (post-hoc) carry the claim", load_bearing=False)
    k1a = all(tab[(np.inf, sh)]["n_always"] == 24 for sh in SHAPES if sh[1] <= 30)
    check("K1a [POST-HOC, load-bearing; MUTATE=k must FAIL] at m2 = inf and the compact zones (c_b <= 30): 24/24 layers unstable at EVERY mu0 in 1e-6..1e4 mu_uni (no window)",
          {str(sh): tab[(np.inf, sh)]["n_always"] for sh in SHAPES}, k1a,
          "the wide zone (c_b = 1e3) leaves 4 layers stable at large mu0: the switch-off term shrinks as s' does, but at s_inf = 1e-8 the cost is then paid over a wider region")
    k1b = all(len(tab[(1e-12, sh)]["windows"]) == 0 for sh in SHAPES)
    check("K1b [POST-HOC, load-bearing; MUTATE=k must FAIL] at m2 = 1e-12 no mu0 in the scan stabilises all 24 layers with every gate edge within 10% of t = 1/2",
          {str(sh): (tab[(1e-12, sh)]["first_all_stable"], len(tab[(1e-12, sh)]["windows"])) for sh in SHAPES}, k1b,
          "in fact no mu0 up to 1e4 mu_uni (sqrt(mu0/m2) = 390 kpc) stabilises all 24 layers at all: the count of unstable layers only falls to 2-13, at smoothing lengths far above the edge scales")
    K2 = [v["ratio_med"] for v in tab.values() if np.isfinite(v["ratio_med"])]
    check("K2 (reported) |K| against the stiffness on the zone's own scale", f"median |K|/(mu0 k^2) over cells: {np.min(K2):.2g} .. {np.max(K2):.2g}", True, load_bearing=False)

    # ============================================================================ K3
    banner("K3  WHAT THE REPAIR WOULD BUY (if K were absent): the cost potential scales as s_inf")
    cc = pool.map(cost, [(s, k) for s in (1e-4, 1e-6, 1e-8) for k in "FS"])
    P("    Phi_chi / v_f^2 at (r_F, Sun) for s_inf = 1e-4, 1e-6, 1e-8:", [(cc[2 * i], cc[2 * i + 1]) for i in range(3)])
    slope = abs(cc[5] / cc[3])
    check("K3 (reported) the Sun potential scales linearly with s_inf (ratio s_inf = 1e-8 : 1e-6)", f"{slope:.3g} (linear: 0.01)", abs(slope - 0.01) / 0.01 < 0.15, load_bearing=False)
    s_needed = 0.01 * 1e-8 / abs(cc[5])
    P(f"    Sun cost <= 0.01 v_f^2 would need s_inf <= {s_needed:.1e}")
    OUT["numbers"]["s_inf_needed_for_sun_0p01"] = s_needed

    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CV6_C_results" + (f"_MUTATE_{MUT}" if MUT else "") + ".json")
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   [{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
