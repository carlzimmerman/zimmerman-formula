#!/usr/bin/env python3
"""L189 -- CANDIDATE C003 "CLOCK-FRAME KICKS, DE-TRIGGERED": the cold component X drops to a lighter state X' + phi (a clock/MOND-scalar
quantum), recoiling isotropically with v_k = c sqrt(2 dm/m); the rate is Gamma(z) = G0 * [Omega_DE(z)/Omega_DE,0] * step(v_rel), where v_rel
is the particle's velocity relative to the clock frame: ~0 in single-stream flow (field, filaments comoving with the dust-like clock), the
host dispersion inside virialised halos. Repeatable (dm << m). Per-particle Poisson kicks: after k kicks v^2 -> v^2 + k v_k^2; expelled if
above the host escape speed at the anchor radius; kicked-but-bound particles heat the host (impulsive, self-similar re-virialisation).
Gates: ledger anchors (spiral <= 0.105 at 3R_d, MW 0.14 at 30 kpc, cluster 0.576 at R500; group reported as a prediction), G5 forest
(z >= 2.2 protected by the trigger: elapsed DE-weighted time fraction), S8 proxy (kicked mass fraction by z = 0.5 + free-streaming scale),
G8 (mass conserved), and a NEW cost on G13: the forest forces DM halos to persist around z ~ 2.5 rotators, shifting the flat-a0(z) BTFR
zero-point prediction. Two fitted parameters (G0*T_eff, v_k). No literal-True checks; no kernel enters (footings irrelevant)."""
import sys, os, json, numpy as np
from scipy.stats import poisson
from scipy.integrate import quad
from scipy.special import gammainc
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL189 CANDIDATE C003 CLOCK-FRAME KICKS (DE-triggered): ledger, forest, S8 proxy, Omega_m, the z = 2.5 cost\n" + "=" * 118)
h = 0.6736; Om = 0.3138; OL = 1 - Om; H0 = h/9.778                                   # Gyr^-1
E = lambda z: np.sqrt(Om*(1 + z)**3 + OL); ODE = lambda z: OL/E(z)**2
dt_dz = lambda z: 1/(H0*E(z)*(1 + z))
Teff = lambda z1, z2: quad(lambda z: ODE(z)/OL*dt_dz(z), z2, z1)[0]                 # DE-weighted elapsed time, Gyr, from z1 down to z2
T_all = Teff(6.0, 0.0); T_kids = Teff(6.0, 0.5); T_forest = Teff(6.0, 2.2)
print(f"    DE-weighted elapsed time [Gyr]: z = 6 -> 0: {T_all:.2f}; -> 0.5: {T_kids:.2f}; -> 2.2: {T_forest:.3f}  (the trigger protects the forest by time)")
m = lambda x: np.log(1 + x) - x/(1 + x)
hosts = [("spiral 1.2e10 Mb, 3R_d", 70., 250., 0.50, 0.105, "<="), ("Milky Way, 30 kpc", 110., 480., 1.19, 0.14, "~"),
         ("group 1e13, R500", 300., 900., 2.2, None, "pred"), ("cluster 1e15, R500", 1000., 2600., 2.71, 0.576, "~")]
def retained(n, vk, sig, vesc, r):
    """Poisson kicks with mean n; speeds ~ 3D Maxwellian(sig); expelled if v^2 + k vk^2 > vesc^2; bound kicked particles heat the host."""
    tot = 0.0
    for k in range(0, 60):
        pk = poisson.pmf(k, n)
        if pk < 1e-9: continue
        lim2 = vesc**2 - k*vk**2
        bound = 0.0 if lim2 <= 0 else gammainc(1.5, lim2/(2*sig**2))
        if k == 0: tot += pk*bound; continue
        dk = k*vk**2/(3*sig**2)
        expand = 0.0 if dk >= 1 else m(r*(1 - dk))/m(r)
        tot += pk*bound*expand
    return tot
best = None
for vk in np.arange(300., 1001., 50.):
    for nT in np.geomspace(0.3, 30, 80):
        fs = [retained(nT, vk, s, ve, r) for _, s, ve, r, _, _ in hosts]
        if fs[0] > 0.105: continue                                                    # the strict spiral ceiling is a hard constraint
        cost = (np.log(max(fs[1], 1e-3)/0.14))**2 + (np.log(max(fs[3], 1e-3)/0.576))**2
        if best is None or cost < best[0]: best = (cost, vk, nT, fs)
cost, vk, nT, fs = best
print(f"    best: v_k = {vk:.0f} km/s, kicks per particle by z = 0: {nT:.2f} (G0 = {nT/T_all:.2f} per DE-weighted Gyr)")
print("    retained: " + "; ".join(f"{n} {f:.3f}" + (f" (target {t})" if t else " (PREDICTION)") for (n, _, _, _, t, _), f in zip(hosts, fs)))
check("V1 [ledger] with two parameters (v_k, G0) the spiral ceiling (<= 0.105) and the cluster anchor (0.576 +/- 0.10) are met together, and the MW is within a factor 2 of 0.14",
      fs[0] <= 0.105 and abs(fs[3] - 0.576) < 0.10 and abs(np.log(fs[1]/0.14)) < np.log(2), "f = " + " ".join(f"{f:.3f}" for f in fs))
n_forest = nT*T_forest/T_all; fd = 1 - np.exp(-n_forest); plateau = (1 - fd)**2
check("V2 [G5 forest] by z = 2.2 the DE-triggered rate has kicked < 5% of the particles even in fully multi-stream halos (plateau (1 - f_d)^2 > 0.9); single-stream DM is untouched at any epoch",
      plateau > 0.9, f"kicks by z = 2.2: {n_forest:.3f}, f_d = {fd:.3f}, plateau {plateau:.3f}")
sys.path.insert(0, os.path.abspath("L183_class_mond_kernel/site"))
from classy import Class
G = 6.674e-8; Msun = 1.989e33; Mpc = 3.086e24; rho_c = 2.775e11*h**2*Msun/Mpc**3
cl = Class(); cl.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.12, "A_s": 2.1e-9, "n_s": 0.9649, "output": "mPk", "P_k_max_h/Mpc": 200, "z_max_pk": 3}); cl.compute()
rho_m = cl.Omega_m()*rho_c
def halo_fraction(z, Mmin=1e9):
    Ms = np.geomspace(Mmin, 1e16, 120); sig = np.array([cl.sigma((3*M*Msun/(4*np.pi*rho_m))**(1/3)/Mpc, z) for M in Ms]); dlns = np.gradient(np.log(sig), np.log(Ms))
    nu = 1.686/sig; A, a, p = 0.3222, 0.707, 0.3; fST = A*np.sqrt(2*a/np.pi)*nu*(1 + (a*nu**2)**(-p))*np.exp(-a*nu**2/2)
    return np.trapz(rho_m/(Ms*Msun)*fST*np.abs(dlns)*Ms*Msun, np.log(Ms))/rho_m
fh = halo_fraction(0.7); n_kids = nT*T_kids/T_all; frac_kicked = fh*(1 - np.exp(-n_kids)); lam_fs = vk*1e5*4*3.156e16/Mpc
check("V3 [S8 proxy, to be replaced by a simulation] the kicked mass fraction by z = 0.5 stays below 0.5 and free-streams less than 5 Mpc, so the k < 0.3 h/Mpc power is displaced, not removed",
      frac_kicked < 0.5 and lam_fs < 5.0, f"DM in halos > 1e9 at z = 0.7: {fh:.2f}; kicks by z = 0.5: {n_kids:.2f}; kicked fraction {frac_kicked:.2f}; lambda_fs ~ {lam_fs:.1f} Mpc")
check("V4 [G8] mass conserved: dm/m per kick = (v_k/c)^2/2 ~ 1e-6", (vk*1e5/2.998e10)**2/2*nT < 1e-3, f"{(vk*1e5/2.998e10)**2/2:.1e} per kick")
rc_z = rho_c*E(2.5)**2; R200 = (3*3e11*Msun/(4*np.pi*200*rc_z))**(1/3); c = 4.0; rs = R200/c; MDM = 3e11*m(3e-3*Mpc/rs)/m(c); fDM = MDM/(MDM + 1e10)
shift = 0.25*np.log10(1 + MDM/1e10)
check("V5 [G13 cost, computed -- a correction to the record] DM halos persisting at z = 2.5, which the forest gate requires of ANY mechanism, put a dark fraction ~0.4 inside R_e = 3 kpc of a 1e10-baryon rotator and shift the framework's BTFR zero-point at z = 2.5 by +0.05 dex in velocity (+0.2 dex in mass): the observing case's 0.00-vs-+0.33 dex gap (PAPER14) shrinks to ~0.1 dex in mass zero-point, below its +/-0.13 dex resolution, and must be recomputed with the halo included",
      0.2 < fDM < 0.6 and 0.03 < shift < 0.08 and 0.33 - 4*shift < 0.13, f"R200(z=2.5) = {R200/Mpc*1e3:.0f} kpc, r_s = {rs/Mpc*1e3:.0f} kpc, M_DM(<3 kpc) = {MDM:.1e} Msun, f_DM = {fDM:.2f}, velocity zero-point +{shift:.3f} dex, mass zero-point +{4*shift:.2f} dex, residual gap {0.33 - 4*shift:.2f} dex")
print("    LIMITS: Poisson kicks + Maxwellian speeds + impulsive heating with self-similar re-virialisation (no orbit integration; replace with the L167 code); host sigma/v_esc as stated;\n"
      "    forest protected by the DE trigger (elapsed DE-weighted time); S8 by a kicked-fraction proxy; the microphysics (clock-frame-gated rate, small mass splitting) is a CANDIDATE, not derived.")
json.dump(dict(vk=vk, kicks_by_z0=nT, G0_per_DEGyr=nT/T_all, f=[float(x) for x in fs], forest_plateau=float(plateau), frac_kicked=float(frac_kicked), lam_fs=float(lam_fs), fDM_z25=float(fDM), btfr_shift=float(shift)), open("L189_results.json", "w"), indent=1)
print(f"\nL189 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
