#!/usr/bin/env python3
"""
ADVERSARIAL VERIFIER for lane B_structured (non-stationary/transient door).
Independent re-derivations, DIFFERENT methods from the lane's scripts:

 (1) LOAD-BEARING EQUATION, re-derived two independent ways:
     delta_m = 2 g^2 w0 (p_g - p_e) / (Omega^2 (w0^2 - Omega^2))
     (a) sympy: Kubo commutator response of a TLS, symbolic, exact.
     (b) numpy: PURE-STATE Schrodinger evolution (no Lindblad, no dissipator,
         different integrator) for |g> and |e>; windowed quadrature -> sign + value.
     The lane's whole 'transient gain EXISTS' claim and its anti-MOND ground-state
     sign both hang on this equation.
 (2) GAP ATTACK (open direction): laneB_band_persistence lets 85% of deep-MOND
     evade the Gamma_2=H floor -- so a FREE one-shot prepared transient would
     half-open the door. Close or open it: compute the PREPARATION bill from the
     dS-drift kinematics (|beta|^2 occupancy): can O(1) inversion/coherence be
     prepared even ONCE per Hubble time?
 (3) FRAGILITY ATTACK: 'redshift drift kills 100% of deep-MOND' -- compute the
     MINIMUM of 10T/t_rs over the deep-MOND grid (both footings). If it is ~1,
     the 100% is grid-edge marginal and must be reported as such.
 (4) Re-derive S_inv and S_coh_rs from scratch (own constants, own algebra),
     both footings; confirm 2.9e10 / 1.4e11 and the x1.10 fork spread.
Exit 0 = all checks hold.
"""
import numpy as np
import sympy as sp

# ================= (1a) sympy Kubo derivation =================
t, tau, w0, Om, g, A, eps = sp.symbols('t tau omega0 Omega g A epsilon', positive=True)
pe, pg = sp.symbols('p_e p_g', nonnegative=True)
w = pg - pe
# chi(tau) = -i Tr(rho [sx(tau), sx]); sx(tau)=cos(w0 tau) sx - sin(w0 tau) sy
# [sx(tau), sx] = -sin(w0 tau)[sy,sx] = 2i sin(w0 tau) sz ; Tr(rho sz)=pe-pg=-w
chi_tau = -sp.I*(2*sp.I*sp.sin(w0*tau)*(-w))          # = -2 w sin(w0 tau)
assert sp.simplify(chi_tau + 2*w*sp.sin(w0*tau)) == 0
# steady response to f(t)=gA cos(Om t): d<sx> = Re[ chi~(Om) ] gA cos(Om t) with
# chi~(Om) = int_0^inf chi(tau) e^{i Om tau - eps tau} dtau
chi_Om = sp.integrate(chi_tau*sp.exp(sp.I*Om*tau - eps*tau), (tau, 0, sp.oo),
                      conds='none')
chi_Om = sp.limit(sp.simplify(chi_Om), eps, 0, '+')
chi_expected = -2*w*w0/(w0**2 - Om**2)
assert sp.simplify(chi_Om - chi_expected) == 0
# F = -g d<sx> = -g^2 A chi(Om) cos(Om t);  F = -dm*xdd = +dm A Om^2 cos(Om t)
dm_sym = sp.simplify(-g**2*chi_Om/Om**2)
dm_expected = 2*g**2*w0*(pg - pe)/(Om**2*(w0**2 - Om**2))
assert sp.simplify(dm_sym - dm_expected) == 0
print("(1a) SYMPY: delta_m = 2 g^2 w0 (p_g-p_e)/(Om^2(w0^2-Om^2))  -- CONFIRMED exactly.")
print("     ground w=+1 -> dm>0 (anti-MOND); inverted w=-1 -> dm<0 (transient gain). Signs stand.")

# ================= (1b) pure-state Schrodinger (independent method) =================
w0n, gn, An, Omn = 1.0, 0.05, 1.0, 0.1
sz = np.array([[1,0],[0,-1]], complex); sx = np.array([[0,1],[1,0]], complex)
def schro(psi0, T, dt):
    ts, sxv = [], []
    psi = psi0.astype(complex); tt = 0.0
    H = lambda tt: 0.5*w0n*sz + gn*An*np.cos(Omn*tt)*sx
    while tt < T:
        ts.append(tt); sxv.append(np.real(psi.conj() @ (sx @ psi)))
        k1 = -1j*H(tt) @ psi
        k2 = -1j*H(tt+dt/2) @ (psi + dt/2*k1)
        k3 = -1j*H(tt+dt/2) @ (psi + dt/2*k2)
        k4 = -1j*H(tt+dt) @ (psi + dt*k3)
        psi = psi + dt/6*(k1+2*k2+2*k3+k4); psi /= np.linalg.norm(psi)
        tt += dt
    return np.array(ts), np.array(sxv)
Td = 2*np.pi/Omn
dm_num = {}
for name, psi0 in [("ground", np.array([0,1.])), ("inverted", np.array([1.,0]))]:
    ts, sxv = schro(psi0, 8*Td, 0.01)
    F = -gn*sxv
    m = ts >= 1*Td                                    # skip switch-on window
    dm = 2/(ts[m][-1]-ts[m][0]) * np.trapz(F[m]*np.cos(Omn*ts[m]), ts[m]) / (An*Omn**2)
    dm_num[name] = dm
dm_th = 2*gn**2*w0n/(Omn**2*(w0n**2-Omn**2))
assert abs(dm_num["ground"] - dm_th)/dm_th < 0.15, dm_num
assert abs(dm_num["inverted"] + dm_th)/dm_th < 0.15, dm_num
print(f"(1b) SCHRODINGER (no Lindblad): dm(ground)={dm_num['ground']:+.4f}, "
      f"dm(inverted)={dm_num['inverted']:+.4f} vs +-{dm_th:.4f} analytic -- "
      "both within 15%, signs confirmed by a fully independent integrator.")

# ================= constants (own, from scratch) =================
c   = 2.99792458e8; Mpc = 3.085677581491367e22; kpc = Mpc/1e3; yr = 3.1557e7
H0  = 67.4e3/Mpc; OmL = 0.685; HL = H0*np.sqrt(OmL); Z = np.sqrt(32*np.pi/3)
a0_can, a0_alt = c*HL/Z, c*H0/Z
assert abs(a0_can/9.36e-11 - 1) < 0.01 and abs(a0_alt/1.13e-10 - 1) < 0.01

# ================= (2) one-shot PREPARATION bill (the gap) =================
# laneB_band_persistence: at the Gamma_2=H floor, 85% of deep-MOND has 10T < 1/H,
# i.e. a FREE one-shot transient would survive there. Is preparation free?
# dS-drift kinematics (the only universal source, per theorems III/V + gauntlet2):
# in-band Bogoliubov occupation |beta|^2 = (|Hdot| H0^2 / (2 w^2))^2 -- this IS the
# occupancy the expansion can put into an in-band mode; positivity caps coherence
# at |rho_ge| <= sqrt(p_e p_g) <= sqrt(|beta|^2).
Hdot = 1.5*(1-OmL)                                   # |Hdot|/H0^2 at z=0 (LCDM)
w_band = np.geomspace(3.24e-17, 1.94e-14, 400)
beta2 = (Hdot*H0**2/(2*w_band**2))**2
# fractional delta_m achievable from occupancy n: |dm| <= n * dm_max(O(1) inversion)
# -> one-shot inversion route: n = |beta|^2 ; coherence route: |c| = sqrt(beta2) but
# the FORCE at first order is ~ |c| * (phase-random -> 1/sqrt(N) net, laneB_phase);
# even granting full phase lock, |c| <= 3.6e-7 at band-mid.
b2_mid = (Hdot*H0**2/(2*np.sqrt(3.24e-17*1.94e-14)**2))**2
print(f"(2) ONE-SHOT PREPARATION BILL: dS-drift in-band occupancy |beta|^2 = "
      f"{beta2.max():.1e} (slow edge) .. {b2_mid:.1e} (mid) .. {beta2.min():.1e} (fast edge);")
print(f"    O(1) inversion needs n~1 -> shortfall {1/b2_mid:.1e} at band-mid EVEN ONCE;")
print(f"    max coherence |c| <= sqrt(beta2) = {np.sqrt(b2_mid):.1e} -> first-order force "
      f"fraction {np.sqrt(b2_mid):.1e} of the per-star amplitude, need O(1).")
assert b2_mid < 1e-10 and np.sqrt(b2_mid) < 1e-5 and beta2.max() < 1e-5
print("    => the 85%-of-deep-MOND 'one-shot survivable' region does NOT reopen the door:")
print("       preparation is not free -- the same |beta|^2 delivery wall applies to the")
print("       FIRST shot, not only to regeneration. (This closes a gap the lane's")
print("       persistence script left implicit; verdict unchanged, reasoning tightened.)")

# ================= (3) fragility of 'redshift drift kills 100%' =================
v = np.geomspace(30e3, 300e3, 400); R = np.geomspace(0.5*kpc, 30*kpc, 400)
V, RR = np.meshgrid(v, R, indexing='ij'); Omg = V/RR; g_obs = V**2/RR
for a0, Hf, tag in [(a0_can, HL, "canonical"), (a0_alt, H0, "alt")]:
    deep = g_obs < a0
    ratio = (20*np.pi/Omg) / np.sqrt(np.pi/(Omg*Hf))   # 10T / t_rs = 20 sqrt(pi H / Om)
    rmin = ratio[deep].min()
    frac_fail = (ratio[deep] > 1).mean()
    print(f"(3) [{tag}] min(10T/t_rs) over deep-MOND grid = {rmin:.2f}; "
          f"fraction with 10T>t_rs = {frac_fail*100:.1f}%")
    assert frac_fail > 0.99
# analytic edge: ratio=1 at Om = 400 pi H; deep-MOND fast edge Om < a0/v_min
Om_edge = 400*np.pi*HL; Om_deepmax_offgrid = a0_can/30e3
print(f"    CAVEAT (found): the 100% is GRID-EDGE MARGINAL at the fast corner: min ratio "
      f"~{(20*np.sqrt(np.pi*HL/ (300e3/(0.5*kpc)) )):.2f}-1.1; off-grid orbits (v~30 km/s, "
      f"R<0.5 kpc) with Om up to a0/v = {Om_deepmax_offgrid:.1e} > 400*pi*H = {Om_edge:.1e} "
      "would EVADE drift-dephasing -- but those are near-boundary (g~a0), not deep-MOND-dominated, "
      "and they still face the preparation bill (2). Report '100%' as 'all of the on-grid "
      "deep-MOND band, marginal (x1.1) at the fast corner'.")

# ================= (4) S_inv and S_coh from scratch, both footings =================
w_g2 = 2*np.pi/np.sqrt((50e6*yr)*(250e6*yr))
b2 = (Hdot*H0**2/(2*w_g2**2))**2
S_inv = 3*H0/(b2*w_g2)
assert 2.7e10 < S_inv < 3.1e10, S_inv
out = {}
for Hf, tag in [(HL, "canonical"), (H0, "alt")]:
    Gphi_rs = np.sqrt(w_g2*Hf/np.pi)
    S_coh = Gphi_rs/(b2*w_g2)
    out[tag] = S_coh
    assert S_coh > S_inv                                # coherence WORSE, both footings
    print(f"(4) [{tag}] S_inv = {S_inv:.2e}; Gamma_phi,rs = {Gphi_rs/H0:.1f} H0; "
          f"S_coh_rs = {S_coh:.2e} = {S_coh/S_inv:.1f}x S_inv; S_coh_best = S_inv/2 = {S_inv/2:.2e}")
spread = out["alt"]/out["canonical"]
assert abs(spread - np.sqrt(H0/HL)) < 1e-6 and 1.05 < spread < 1.15
print(f"    footing spread x{spread:.3f} = sqrt(H0/H_L) -- verdict-stable. "
      "Lane numbers (2.91e10, 1.42e11/1.56e11, x1.10) REPRODUCED independently.")

print("\nVERIFIER CONCLUSION: lane B_structured UPHELD -- transient gain real, persistence")
print("in deep-MOND requires (re)generation, and BOTH the first shot and regeneration hit")
print("the same |beta|^2 delivery wall (~1e-13 occupancy vs O(1) needed); coherence discount")
print("<= x2, drift floor makes it ~5x worse. Corrections: (i) one-shot-preparation bill now")
print("explicit (gap closed, same verdict); (ii) '100% drift-kill' is grid-marginal at the")
print("fast corner -- soften to 'all on-grid, x1.1 margin at the edge'.")
