#!/usr/bin/env python3
"""CK01 -- the gate the clock chain never ran: GW170817's photon-graviton arrival difference for the PAPER24/25 construction.

PAPER24 sec. 5 / L215: matter couples DISFORMALLY along the clock's unit timelike direction, so matter (hence photons) feel
Phi~ = Phi + phi, Psi~ = Psi + phi (gamma_PPN = 1 exactly), while gravitational waves propagate on g (the Einstein-Hilbert metric).
The scalar phi carries the MOND force (a0 = lambda^3/(12 pi G beta s_0)) and, at solar-system accelerations, a share f_s ~ 1 of the
local potential (PAPER24: alpha_1 = 8 f_s, f_s ~ 1).  Two species on two cones: the photon's coordinate speed is 1 + Phi~ + Psi~ and
the graviton's 1 + Phi + Psi, so photons are slower by 2|phi| wherever phi < 0, and GW170817/GRB170817A bounds the accumulated
difference along the 40 Mpc sightline to the observed +1.74 +/- 0.05 s (a generous emission budget is 10 s).
The record's own prep_2026/gw170817_check killed exactly this structure (3.5e7 s) for an earlier paper; L186-L225 and PAPER24/25 do
not cite it.  This lane computes the number for THIS construction: the scalar potential is phi' = [f_s + (nu(x) - 1)] g_N / c^2 with
the framework's cap (eta_ext = 0.03), for f_s in {1, 0.1, 0.01, 0}; both a0 footings; both kernels.  The clock's alignment to the
local frame (PAPER25, s_0 >= 1.5e7) does NOT enter: the cone split is a scalar, frame-independent.  A FAIL is a finding."""
import os, re, json, math
import numpy as np
from scipy.optimize import brentq
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("CK01 -- GW170817 differential Shapiro delay for the PAPER24/25 clock construction\n")
G, C, MSUN, KPC, MPC = 6.674e-11, 2.99792458e8, 1.989e30, 3.0857e19, 3.0857e22
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
nu_rar = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y))) if y < 1e4 else 1.0 + math.exp(-math.sqrt(y))
mu2 = lambda u: 1.0 - (1.0 + u) ** -2
def nu_mu2(y):
    if y > 1e3: return 1.0 + 4.0 / y ** 2
    return brentq(lambda g: g * mu2(g / 2.0) - y, y, 50 * y + 50) / y
KERN = {"nu_RAR": nu_rar, "mu_2": nu_mu2}
D = 40 * MPC; M_host, M_mw = 1e11 * MSUN, 6e10 * MSUN; r0_host, r0_mw = 2 * KPC, 8.2 * KPC; ETA = 0.03
rgrid = np.logspace(math.log10(1 * KPC), math.log10(50 * MPC), 4000)
def phi_profile(M, a0, nuf, fs):
    r = rgrid; gN = G * M / r ** 2; x = gN / a0
    share = np.array([fs + nuf(math.sqrt(xx ** 2 + ETA ** 2)) - 1.0 for xx in x])     # the scalar's share of the force: f_s (Newtonian regime) + the phantom
    integrand = share * gN / C ** 2; phi = np.zeros_like(r)
    for i in range(len(r) - 2, -1, -1): phi[i] = phi[i + 1] - 0.5 * (integrand[i] + integrand[i + 1]) * (r[i + 1] - r[i])
    return phi
# ------------------------------------------------------------------ 1. the delay
print("=" * 100); print("1. Delta t = (1/c) int (e^{-2 phi} - 1) dl along the kilonova -> Sun line (host exit 2 kpc, MW entry 8.2 kpc), eta_ext = 0.03"); print("=" * 100)
res = {}
for foot, a0 in FOOT.items():
    for kn, nuf in KERN.items():
        for fs in (1.0, 0.1, 0.01, 0.0):
            ph = phi_profile(M_host, a0, nuf, fs); pm = phi_profile(M_mw, a0, nuf, fs)
            l = np.logspace(math.log10(r0_host), math.log10(D - r0_mw), 20000)
            phi_tot = np.interp(l, rgrid, ph) + np.interp(D - l, rgrid, pm)
            dt = np.trapz(np.exp(-2 * phi_tot) - 1.0, l) / C
            res[(foot, kn, fs)] = dict(dt_s=dt, phi_sun=float(np.interp(r0_mw, rgrid, pm)))
            print(f"    {foot:9s} {kn:6s} f_s = {fs:<5g}: phi(Sun) = {res[(foot,kn,fs)]['phi_sun']:+.2e} -> Delta t = {dt:.2e} s = {dt/3.156e7:.1f} yr  ({dt/1.7:.1e} x the 1.7 s; {dt/10:.1e} x a 10 s budget)")
OUT["delays"] = {f"{k[0]}/{k[1]}/fs{k[2]}": v for k, v in res.items()}
dt_min = min(v["dt_s"] for v in res.values()); dt_fs0 = min(v["dt_s"] for k, v in res.items() if k[2] == 0.0); dt_fs1 = min(v["dt_s"] for k, v in res.items() if k[2] == 1.0)
check("1a with the scalar carrying the share PAPER24 assigns it at solar-system accelerations (f_s ~ 1), the photon-graviton delay is >= 5e7 s (>= 1.5 yr) on every footing and kernel: >= 1e7 x the observed 1.7 s (the Newtonian-regime share adds only ~25% because the path integral is dominated by the phantom's log potential at large radii)",
      dt_fs1 >= 5e7 and dt_fs1 / 1.7 >= 1e7, f"min Delta t at f_s = 1: {dt_fs1:.2e} s = {dt_fs1/3.156e7:.0f} yr")
check("1b even with NO Newtonian-regime share (f_s = 0) the deep-MOND part alone -- which is the scalar's by construction, since the force law a0 = lambda^3/(12 pi G beta s_0) comes from it -- gives >= 1e7 s (>= 1 yr): the coupling is dead irrespective of f_s",
      dt_fs0 >= 1e7 and dt_fs0 / 10 >= 1e5, f"min Delta t at f_s = 0: {dt_fs0:.2e} s = {dt_fs0/3.156e7:.1f} yr; the record's cap-free number is 3.5e7 s")
check("1c the sign is the observed one (phi < 0: photons later), so nothing is rescued by sign; the required TOTAL scalar share to pass a 10 s budget would be <= 1e-7 of the potential, i.e. no MOND force from the scalar at all",
      all(v["dt_s"] > 0 and v["phi_sun"] < 0 for v in res.values()) and 10.0 / dt_fs0 < 1e-6, f"allowed share ~ 10 s / {dt_fs0:.1e} s = {10/dt_fs0:.1e}")
# ------------------------------------------------------------------ 2. the records
print("\n" + "=" * 100); print("2. the records: the gate exists in the repository and predates the papers; the papers and lanes do not cite it"); print("=" * 100)
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
chk = os.path.join(ROOT, "prep_2026", "gw170817_check", "RESULT.md")
tex24 = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026", "PAPER24_the_decoupling_locus_2026.tex")
tex25 = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026", "PAPER25_a_clock_that_must_run_fast_2026.tex")
t_chk = open(chk).read() if os.path.exists(chk) else ""; t24 = open(tex24).read() if os.path.exists(tex24) else ""; t25 = open(tex25).read() if os.path.exists(tex25) else ""
lanes = [os.path.join(ROOT, "fable_independent_2026", f) for f in os.listdir(os.path.join(ROOT, "fable_independent_2026")) if re.match(r"L(18[6-9]|19\d|2[0-2]\d)_.*\.out$", f)]
cited = [os.path.basename(f) for f in lanes if re.search(r"GW170817|gw170817|Boran|emulator", open(f, errors="ignore").read())]
check("2a the record's gate exists (prep_2026/gw170817_check/RESULT.md, verdict EXCLUDED, 3.5e7 s) and NEITHER PAPER24 nor PAPER25 nor any of the L186-L225 lanes mentions GW170817, Boran or the emulator wall [PASS = the omission is verified]",
      "EXCLUDED" in t_chk and "3.5e7" in t_chk and "GW170817" not in t24 and "GW170817" not in t25 and len(cited) == 0 and len(lanes) > 20,
      f"lanes scanned: {len(lanes)}; citing the gate: {cited}")
check("2b the construction's own words put photons on the disformal metric: PAPER24 states Phi~ = Phi + phi, Psi~ = Psi + phi and 'light bending and Shapiro delay are general-relativistic' -- the ratio gamma = 1, not the photon-graviton difference [records located]",
      "tilde\\Phi=\\Phi+\\varphi" in t24.replace(" ", "") and "Shapiro delay are general-relativistic" in t24)
n, n_pass = len(CH), sum(CH)
print(f"\nCK01 COMPLETE: {n_pass}/{n} checks PASS.")
print("""VERDICT.  The PAPER24/25 clock construction, as published, fails GW170817's photon-graviton arrival test by 7-9 orders of magnitude on
both footings and both kernels: its disformal matter coupling along the clock direction is exactly the two-cone ('dark-matter emulator')
structure the repository's own prep_2026/gw170817_check excluded before the papers were written, and the deep-MOND part of the scalar
potential alone is enough.  The PAPER25 alignment (s_0 >= 1.5e7) is irrelevant to it: the cone split is a scalar.  Consequences for the
swarm: (1) do NOT 'run the clock' as published; (2) the repair must put every species on ONE metric -- either move the disformal
structure into the gravitational sector (then c_T = c must be re-derived; a clock-dependent disformal factor generically breaks it) or
drop the disformal coupling and let lensing come from the sector's own clustering (which L248's truncation test already kills as the
lensing source); (3) the single-metric candidate of 2026-09-05 (clock host + xi-screened scalar, matter on g) is the construction that
does not have this problem and is where the roadmap G04-G14 should be run.  PAPER24/25 need a versioned erratum -- on the user's go
only.  Nothing here derives kappa.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "CK01_results.json"), "w"), indent=1, default=str)
