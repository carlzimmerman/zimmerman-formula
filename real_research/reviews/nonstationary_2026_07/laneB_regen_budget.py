#!/usr/bin/env python3
"""
LANE B, TASK 3 -- REGENERATION POWER BUDGET: IS COHERENCE CHEAPER THAN INVERSION?

The one-shot transient dies (laneB_band_persistence): the deep-MOND band needs
continuous regeneration. The ONLY universal free-energy source is the real
universe's drift from exact dS (established: horizon itself = KMS thermostat with
in-band occupation < 1e-900; CMB is 26 orders out of band). This script computes,
with Planck/DESI-era numbers and BOTH a0 footings:

 (A) benchmark: reproduce the INVERSION-route pump shortfall (mi_state_clause/
     gauntlet2 construction): S_inv = Gamma_needed/Gamma_avail = 3H0/(|beta|^2 w)
     ~ 2.9e10 at the 50-250 Myr band, and its spread across the FULL Omega=v/R band
     (|beta|^2 ~ (Hdot/2w^2)^2 falls as w^-4 => S rises as w^3).
 (B) exact Lindblad-spectrum fact: coherences decay at Gamma_2 = Gamma_1/2 + Gamma_phi
     >= Gamma_1/2 (verified from superoperator eigenvalues, not assumed), and
     |rho_ge| <= sqrt(p_e p_g): holding coherence |c| REQUIRES holding population
     p_e >= |c|^2. So the coherence route inherits the inversion route's occupancy
     bill, discounted by AT MOST the factor Gamma_2/Gamma_1 >= 1/2.
 (C) pure-dephasing floor: an in-band mode riding the expansion detunes at
     Gamma_phi,rs ~ sqrt(w H/pi) (redshift drift) -- at band-mid this is ~15 H0,
     making the coherence route ~5x MORE expensive than inversion, not less.
 (D) stored-energy scale: locked-response energy u_lock ~ f v^2/2 per kg (adopted
     from kernel-lane d2_pump_energetics, which this reproduces); the coherent-state
     version of the same kernel needs the same order of quanta (|c|^2 <= p_e).
 (E) raw-energy generosity layer: even the raw local DE-drift draw only covers the
     leak with O(1) headroom in a disk; the 10-orders wall is DELIVERY (in-band
     spectral emptiness), which coherence does not touch.
Exit 0 = all assertions hold.
"""
import numpy as np

c   = 2.99792458e8
hbar= 1.054571817e-34
Mpc = 3.0856775814913673e22
kpc = Mpc/1e3
yr  = 3.1557e7
Msun= 1.989e30
pc  = kpc/1e3

H0  = 67.4e3/Mpc
OmL = 0.685; Omm = 1-OmL
HL  = H0*np.sqrt(OmL)
Z   = np.sqrt(32*np.pi/3)
a0_can, a0_alt = c*HL/Z, c*H0/Z
assert abs(a0_can-9.36e-11)<1e-13 and abs(a0_alt-1.13e-10)<1e-12
ok = [f"footings: a0_can=cH_L/Z={a0_can:.3e}, a0_alt=cH0/Z={a0_alt:.3e} m/s^2 "
      f"(ratio {a0_alt/a0_can:.3f}); H0={H0:.3e}/s, H_L={HL:.3e}/s"]

# ---------------- (A) inversion benchmark + band spread ----------------
Hdot = 1.5*Omm                                   # |Hdot|/H0^2, LCDM z=0
nbeta = lambda w: (Hdot*H0**2/(2*w**2))**2       # expansion-channel occupation (upper est.)
G_need = 3*H0                                    # R2 pump floor (kernel lane)
w_g2 = 2*np.pi/np.sqrt((50e6*yr)*(250e6*yr))     # gauntlet2 band-mid
S_inv_g2 = G_need/(nbeta(w_g2)*w_g2)
assert 2.5e10 < S_inv_g2 < 3.5e10, S_inv_g2      # the established ~2.9e10, reproduced
w_lo, w_hi = 30e3/(30*kpc), 300e3/(0.5*kpc)      # full Omega=v/R band
w_mid = np.sqrt(w_lo*w_hi)
S_lo, S_mid, S_hi = (G_need/(nbeta(w)*w) for w in (w_lo, w_mid, w_hi))
ok.append(f"(A) INVERSION benchmark reproduced: S_inv = 3H0/(|beta|^2 w) = {S_inv_g2:.2e} "
          f"at the 50-250 Myr band (the established ~2.9e10). Across the full band "
          f"(S ~ w^3): {S_lo:.1e} (slow edge) / {S_mid:.1e} (mid) / {S_hi:.1e} (fast edge).")

# ---------------- (B) coherence decay >= half population decay (exact) ----------------
sz = np.array([[1,0],[0,-1]], complex); sm = np.array([[0,0],[1,0]], complex)
def liouvillian(w0, G1, Gphi):
    I = np.eye(2); H = 0.5*w0*sz
    L = -1j*(np.kron(H, I) - np.kron(I, H.T))
    for Lk in [np.sqrt(G1)*sm, np.sqrt(Gphi/2)*sz]:
        L += (np.kron(Lk, Lk.conj())
              - 0.5*np.kron(Lk.conj().T@Lk, I) - 0.5*np.kron(I, (Lk.conj().T@Lk).T))
    return L
for G1, Gphi in [(1.0, 0.0), (1.0, 0.7), (0.3, 2.0)]:
    ev = np.linalg.eigvals(liouvillian(5.0, G1, Gphi))
    coh = ev[np.abs(ev.imag) > 1.0]               # coherence pair rotates at +-w0
    pop = ev[(np.abs(ev.imag) < 1e-9) & (np.abs(ev.real) > 1e-9)]
    G2 = -coh.real.mean(); G1_meas = -pop.real.mean()
    assert abs(G1_meas - G1) < 1e-9 and abs(G2 - (G1/2 + Gphi)) < 1e-9
ok.append("(B) exact Liouvillian spectrum: population rate = Gamma_1, coherence rate = "
          "Gamma_1/2 + Gamma_phi >= Gamma_1/2 (verified, 3 parameter sets). With "
          "|rho_ge| <= sqrt(p_e p_g) (positivity), holding coherence |c| requires holding "
          "p_e >= |c|^2: the coherence route pays the SAME occupancy bill, discount <= x2.")

# ---------------- (C) dephasing floor from redshift drift ----------------
res = {}
for Hf, tag in [(HL, "canonical(H_L)"), (H0, "alt(H0)")]:
    Gphi_rs = np.sqrt(w_g2*Hf/np.pi)              # phase slip pi/2 in t_rs=sqrt(pi/(w H))
    S_coh_best = S_inv_g2/2                       # Gamma_2 = Gamma_1/2, zero pure dephasing
    S_coh_rs   = Gphi_rs/(nbeta(w_g2)*w_g2)       # with the redshift-drift floor
    res[tag] = (Gphi_rs/H0, S_coh_best, S_coh_rs)
    ok.append(f"(C) [{tag}] Gamma_phi,rs = sqrt(w_mid H/pi) = {Gphi_rs/H0:.1f} H0 "
              f">> 3 H0 -> S_coh = {S_coh_rs:.2e} ({S_coh_rs/S_inv_g2:.1f}x WORSE than "
              f"inversion); absolute best case (no pure dephasing at all): "
              f"S_coh >= S_inv/2 = {S_coh_best:.2e}")
    assert S_coh_rs > S_inv_g2 and S_coh_best > 1e10
spread = res["alt(H0)"][2]/res["canonical(H_L)"][2]
ok.append(f"(C) footing spread on S_coh_rs: x{spread:.2f} (sqrt(H0/H_L)) -- verdict-stable; "
          f"S_coh in [{res['canonical(H_L)'][1]:.1e} (impossible best case), "
          f"{res['alt(H0)'][2]:.1e} (with the drift floor)] across all forks.")

# ---------------- (D) stored energy scale (reproduce d2, compare coherent version) ----------------
f = 0.5; v = 220e3
u_lock_kg = f*v**2/2                              # J per kg, locked kernel response
P_inv_kg  = 3*H0*u_lock_kg                        # leak at 3H0
assert abs(P_inv_kg - 7.99e-8)/7.99e-8 < 0.02     # d2_pump_energetics: 7.99e-8 W/kg
quanta_kg = u_lock_kg/(hbar*w_g2)
ok.append(f"(D) locked-response energy {u_lock_kg:.1e} J/kg = {quanta_kg:.1e} quanta/kg at "
          f"band-mid (d2 kernel-lane: 1.3e59 -- consistent); P_inv = 3H0*u_lock = "
          f"{P_inv_kg:.2e} W/kg. Coherent version: same order of quanta (|c|^2 <= p_e), "
          f"leak at Gamma_2 -> P_coh in [{P_inv_kg/2:.1e} (best), "
          f"{P_inv_kg*res['canonical(H_L)'][0]/3:.1e} (drift floor)] W/kg.")

# ---------------- (E) raw-energy generosity layer ----------------
rho_c  = 3*H0**2/(8*np.pi*6.674e-11)
u_DE   = OmL*rho_c*c**2
draw   = u_DE*H0                                  # max homogeneous draw, W/m^3
rho_disk = 0.1*Msun/pc**3                         # local disk mass density
avail_disk = draw/rho_disk                        # W per kg of disk baryons
headroom = avail_disk/P_inv_kg
assert 1 < headroom < 5, headroom
ok.append(f"(E) raw local energy: DE-drift draw u_DE*H0 = {draw:.2e} W/m^3 over disk "
          f"rho = {rho_disk:.1e} kg/m^3 -> {avail_disk:.2e} W/kg vs P_inv {P_inv_kg:.1e} "
          f"-> headroom only x{headroom:.1f} IN-DISK (cosmic-mean headroom ~5e7, d2). "
          "Raw energy is marginal but not the wall; the wall is DELIVERY: the drift's "
          "in-band occupation |beta|^2 ~ 1e-13 is a KINEMATIC property of the expansion, "
          "identical whether the target state is populated or coherent.")

ok.append("VERDICT (task 3): coherence is NOT cheaper than inversion in any way that matters. "
          "Best conceivable discount = x2 (Gamma_2 = Gamma_1/2, zero pure dephasing, "
          "phase-conspiracy ignored); with the unavoidable redshift-drift dephasing of "
          "horizon-tied in-band modes the coherence route is ~5x MORE expensive. "
          "Shortfall: S_coh ~ 1.5e10 (impossible best) to ~1.6e11 (drift floor), both "
          "footings, vs S_inv ~ 2.9e10. Same pump wall, same 10 orders.")

print("ALL ASSERTIONS PASSED (laneB regeneration budget)")
for line in ok: print(" *", line)
