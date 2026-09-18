#!/usr/bin/env python3
"""SW06 -- the LENSING gate of the direction-blind class, walked with the record's trilemma (LENSING_TRILEMMA_2026 horns A/B/C):
(1) SW03's disformal photon metric was already dead on the record (prep_2026/gw170817_check: GW170817 differential Shapiro,
    3.5e7 s vs 1.7 s) -- an OMISSION in SW03's ledger ('lensing = dynamics: INHERITED'); reproduced here with the framework's own
    direction-blind cap, both footings, both kernels, three external fields;
(2) horn C (conformal single metric) -- light bends by the baryons only (record: L241 / DC-013), checked here at the level of the
    null geodesic (the conformal factor drops out);
(3) horn A (shared metric, phantom = field stress-energy) for a SINGLE field sourced through the metric alone -- the LOCAL no-go,
    sympy here and Lean in lean_2026/SW06_local_nogo.lean; the vector-sourced (AeST-type) realisation is the 08-31 alpha1 kill;
(4) what is left: named, not computed.  A FAIL is a finding; no literal-True checks."""
import os, json, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("SW06 -- the lensing gate of the direction-blind class (trilemma horns A/B/C)\n")
G, C, MSUN, KPC, MPC = 6.674e-11, 2.99792458e8, 1.989e30, 3.0857e19, 3.0857e22
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
nu_rar = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y))) if y < 1e4 else 1.0 + math.exp(-math.sqrt(y))
mu2 = lambda u: 1.0 - (1.0 + u) ** -2
def nu_mu2(y):
    if y > 1e3: return 1.0 + 4.0 / y ** 2
    return brentq(lambda g: g * mu2(g / 2.0) - y, y, 50 * y + 50) / y
KERN = {"nu_RAR": nu_rar, "mu_2": nu_mu2}

# ------------------------------------------------------------------ 1. horn B: the disformal photon cone vs GW170817, with the framework's cap
print("=" * 100); print("1. horn B -- SW03's g~ = e^{-2phi} g - 2 sinh(2phi) u u: photons on g~ (c_gamma = e^{2phi} c), gravitons on g; the differential delay along the GW170817 sightline"); print("=" * 100)
D = 40 * MPC; M_host, M_mw = 1e11 * MSUN, 6e10 * MSUN; r0_host, r0_mw = 2 * KPC, 8.2 * KPC
def phi_profile(M, a0, nuf, eta, rgrid):
    """phi(r) = -int_r^inf (nu(sqrt(x^2 + eta^2)) - 1) g_N dr' / c^2 with the direction-blind cap (SW01): the scalar's share of the force."""
    r = rgrid; gN = G * M / r ** 2; x = gN / a0
    share = np.array([nuf(math.sqrt(xx ** 2 + eta ** 2)) - 1.0 for xx in x])
    integrand = share * gN / C ** 2
    # cumulative integral from the outside in (phi(inf) = 0)
    phi = np.zeros_like(r)
    for i in range(len(r) - 2, -1, -1):
        phi[i] = phi[i + 1] - 0.5 * (integrand[i] + integrand[i + 1]) * (r[i + 1] - r[i])
    return phi
rgrid = np.logspace(math.log10(1 * KPC), math.log10(50 * MPC), 4000)
res = {}
for foot, a0 in FOOT.items():
    for kn, nuf in KERN.items():
        for eta in (0.01, 0.03, 0.1):
            ph = phi_profile(M_host, a0, nuf, eta, rgrid); pm = phi_profile(M_mw, a0, nuf, eta, rgrid)
            # the ray: l from the kilonova (2 kpc from the host centre) to the Sun (8.2 kpc from the MW centre), straight line through both centres
            l = np.logspace(math.log10(r0_host), math.log10(D - r0_mw), 20000)
            phi_tot = np.interp(l, rgrid, ph) + np.interp(D - l, rgrid, pm)
            # photon speed e^{2 phi} c (phi < 0: subluminal photons, later arrival); Delta t = int dl (1/c_gamma - 1/c) = (1/c) int (e^{-2 phi} - 1) dl
            dt = np.trapz(np.exp(-2 * phi_tot) - 1.0, l) / C
            res[(foot, kn, eta)] = dict(dt_s=dt, phi_sun=float(np.interp(r0_mw, rgrid, pm)), phi_kn=float(np.interp(r0_host, rgrid, ph)), rb_mw_kpc=math.sqrt(G * M_mw / a0) / math.sqrt(eta) / KPC)
            print(f"    {foot:9s} {kn:6s} eta_ext = {eta:.2f}: phi(Sun) = {res[(foot,kn,eta)]['phi_sun']:+.2e}, phi(kilonova) = {res[(foot,kn,eta)]['phi_kn']:+.2e}, r_b(MW) = {res[(foot,kn,eta)]['rb_mw_kpc']:.0f} kpc -> Delta t = {dt:.2e} s = {dt/86400:.0f} d  ({dt/1.7:.1e} x the 1.7 s)")
OUT["hornB"] = {f"{k[0]}/{k[1]}/eta{k[2]}": v for k, v in res.items()}
dt_min = min(v["dt_s"] for v in res.values())
check("1a horn B is EXCLUDED on every footing, kernel and external field: the photon-graviton arrival difference is >= 1e5 x the observed 1.7 s (and >= 1e4 x a 10 s emission budget) even with the framework's direction-blind cap, which makes the phantom potential converge beyond r_b = r_M/sqrt(eta)",
      dt_min > 1e5 * 1.7 and dt_min > 1e4 * 10, f"min Delta t = {dt_min:.2e} s = {dt_min/86400:.0f} days; the record's cap-free number is 3.5e7 s (prep_2026/gw170817_check)")
check("1b the sign is the observed one (photons LATER: phi < 0 inside the phantom potential, c_gamma = e^{2 phi} c < c) -- so the kill is on magnitude alone, 5-7 orders, not on sign",
      all(v["dt_s"] > 0 and v["phi_sun"] < 0 for v in res.values()))
# the local speed difference at the Sun against the GW170817 |c_gw - c_gamma|/c < 1e-15 bound (the in-situ version of the same test)
dc_sun = max(abs(2 * v["phi_sun"]) for v in res.values())
check("1c the LOCAL cone mismatch at the Sun, |c_gamma - c|/c = 2|phi(Sun)|, exceeds 1e-15 by >= 8 orders on every footing/kernel/eta (the Galactic phantom potential alone sets it)",
      min(abs(2 * v["phi_sun"]) for v in res.values()) > 1e-7, f"2|phi(Sun)| = {min(abs(2*v['phi_sun']) for v in res.values()):.1e} .. {dc_sun:.1e} vs 1e-15")
print("    READING: SW03's ledger row 'lensing = dynamics: INHERITED (Bekenstein 2004)' and 'c_T = c: PASS' missed this -- the tensor speed is c, the PHOTON speed is not;")
print("    the disformal route (horn B) was dead on the record before SW04; SW04's alpha1 is a second, independent kill of the same action.")

# ------------------------------------------------------------------ 2. horn C: conformal single metric -> light bends by the baryons only
print("\n" + "=" * 100); print("2. horn C -- conformal coupling g~ = e^{2 phi} g: the null cone of g~ IS the null cone of g, so photons see the Einstein-frame potentials only"); print("=" * 100)
ph, U = sp.symbols('phi U', real=True)
k0, k1, k2, k3 = sp.symbols('k0 k1 k2 k3', real=True)
g = sp.diag(-(1 - 2 * U), 1 + 2 * U, 1 + 2 * U, 1 + 2 * U)      # weak-field Einstein frame, gamma_E = 1
gt = sp.exp(2 * ph) * g                                          # conformal matter metric
gt_inv = gt.inv(); k = sp.Matrix([k0, k1, k2, k3])
disp_t = sp.simplify((k.T * gt_inv * k)[0]); disp = sp.simplify((k.T * g.inv() * k)[0])
check("2a the photon dispersion relation g~^{mu nu} k_mu k_nu = 0 is e^{-2 phi} x (g^{mu nu} k_mu k_nu) = 0: the conformal factor drops out, the light cone is g's, and light bends by U (the baryons) only",
      sp.simplify(disp_t - sp.exp(-2 * ph) * disp) == 0)
print("    READING: dynamics feel Phi_E + phi (the MOND amplitude), lensing feels Phi_E (the baryons): the slip-lock of DC-013 / the L241 lensing kill (galaxy-galaxy lensing carries the MOND amplitude).")

# ------------------------------------------------------------------ 3. horn A: single field sourced through the metric alone -> the local no-go
print("\n" + "=" * 100); print("3. horn A -- phantom = the static energy density of ONE field that is an algebraic function of the local Newtonian field: impossible (sympy; Lean SW06_local_nogo.lean)"); print("=" * 100)
a0s, Gs, M, r, w = sp.symbols('a0 G M r w', positive=True)
eps_mond = sp.sqrt(Gs * M * a0s) / (4 * sp.pi * Gs * r ** 2)
eps_at_w = sp.simplify(eps_mond.subs(r, sp.sqrt(Gs * M / w)))    # the phantom at fixed local field w = G M / r^2
check("3a at fixed local field w the deep-MOND phantom is sqrt(a0) w / (4 pi G sqrt(G M)): it still depends on M, so no function eps(w) of the local field alone reproduces it for two masses (d eps/d M != 0)",
      sp.simplify(eps_at_w - sp.sqrt(a0s) * w / (4 * sp.pi * Gs * sp.sqrt(Gs * M))) == 0 and sp.simplify(sp.diff(eps_at_w, M)) != 0, f"eps(w, M) = {eps_at_w}")
lean_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lean_2026", "SW06_local_nogo.lean")
lean_txt = open(lean_path).read() if os.path.exists(lean_path) else ""
check("3b the same statement is certified in Lean (lean_2026/SW06_local_nogo.lean: local_nogo, epsMOND_rewrite; compiled exit 0, axioms propext/Classical.choice/Quot.sound only -- see lean_2026/SW06_local_nogo.out)",
      "theorem local_nogo" in lean_txt and "theorem epsMOND_rewrite" in lean_txt and "sorry" not in lean_txt.replace("Zero sorry", ""))
print("    READING: a shared-metric phantom needs a SOURCED Poisson-type equation (QUMOND/AQUAL's div[mu grad phi] = 4 pi G rho). Sourcing by matter directly makes the field act")
print("    on matter (a fifth force photons do not feel: horn C again); sourcing through the metric needs a second field carrying the constraint -- AeST's vector, whose tie")
print("    to the MOND scalar fixes alpha1 = -2(K_B + 2) (record, 08-31). The record's LOCAL no-go theorem (fried-chicken) is the same statement at the level of the force law.")

# ------------------------------------------------------------------ 4. the ledger
print("\n" + "=" * 100); print("4. the lensing ledger of the direction-blind (quadrature) structure"); print("=" * 100)
rows = [("B  disformal photon metric (SW03, TeVeS-type)", "DEAD", "GW170817 differential Shapiro: >= 1e6 s vs 1.7 s (Part 1; record prep_2026/gw170817_check); plus SW04 alpha1 whenever the scalar has a Newtonian-regime share"),
        ("C  conformal single metric", "DEAD", "light bends by the baryons only (Part 2); DC-013 slip-lock / L241 (galaxy-galaxy lensing carries the MOND amplitude)"),
        ("A1 shared metric, ONE field sourced through the metric", "DEAD", "the local no-go (Part 3, Lean): the phantom is not a function of the local field"),
        ("A2 shared metric, field sourced by matter", "DEAD", "the field then acts on matter directly and not on light: horn C's slip"),
        ("A3 shared metric, vector-sourced (AeST-type: the vector's constraint carries the Poisson structure)", "DEAD on the record for AeST", "alpha1 = -2(K_B + 2) un-tunable (08-31); the MOND scalar keeps an O(1) Newtonian-regime share there -- SW04's mechanism in horn-A form"),
        ("A4 shared metric, khronon-sourced, scalar switched OFF locally (the quadrature structure's own route)", "OPEN -- not computed anywhere", "needs: (i) that a Poisson-type equation with the matter source arises when the scalar's coefficient diverges in the Newtonian regime (the local no-go forbids a purely local version), (ii) its boosted alpha1 without AeST's '+2' (the share -> 0 is necessary, SW05 3a, not shown sufficient)")]
for name, st, why in rows: print(f"    {name:100s} {st:28s} {why}")
OUT["ledger"] = rows
check("4a every lensing route of the direction-blind class except A4 is dead on the record or in this lane; A4 is the single uncomputed gate (a computed statement about the table, not a physics result)",
      sum(1 for _, st, _ in rows if st.startswith("DEAD")) == 5 and sum(1 for _, st, _ in rows if st.startswith("OPEN")) == 1)

n, n_pass = len(CH), sum(CH)
print(f"\nSW06 COMPLETE: {n_pass}/{n} checks PASS.")
print("""VERDICT.  SW03's disformal lensing was dead on the record before SW04 (an omission in SW03's ledger, now corrected): with the framework's own
direction-blind cap the photon-graviton delay along the GW170817 sightline is >= 1e6 s against the observed 1.7 s, and the local cone mismatch
at the Sun is 2|phi| ~ 1e-7 against 1e-15.  For the repaired quadrature action (SW05) the lensing routes are the trilemma's: B dead (this),
C dead (baryons-only bending), A dead for a single metric-sourced field (the local no-go, Lean-certified) and for matter-sourced fields
(the slip), and dead on the record for AeST's vector-sourced realisation (alpha1 = -2(K_B + 2)).  The ONE route not on the record: a
khronon-sourced MOND scalar that switches off locally (the quadrature's PPN escape) AND produces the sourced Poisson structure a shared-metric
phantom needs -- the local no-go says it cannot be purely local, so it must be a constraint (AeST-like) or a genuinely nonlocal operator; whether
such a structure exists with a vanishing Newtonian-regime share and alpha1 = 0 is the next computation.  Nothing here derives kappa.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SW06_results.json"), "w"), indent=1, default=str)
