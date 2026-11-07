# SV5 iter_2: class C. Sector Jeans scale switched by the AC2q charge Sigma = D.P + 2X. FROZEN CRITERIA

Kappa = 1/2 FITTED; not theory closed. Committed with ../FROZEN_CRITERIA.md, before any script or number.

## Class

v3s's K(Q) sector (n = 1 polytrope, k_J = mu_K; QX3_dust_eos.lean) with mu_K^2 -> mu_K^2(Sigma), any nonincreasing function of
the khronon charge Sigma = D.P + 2X (AC2q's switch variable; QX17: D.P = Pi is the khronon / phantom density). The sector is
stiffer where the charge is larger: dust on the low-charge web, pressure-supported in high-charge hosts. Non-barotropic (the
stiffness depends on P, not on the sector's own density; contrast QX7_cold_switch.lean `kq_cs2_barotropic`).

## Inputs

- Host charge: rho_ph,host(r) = (1/(4 pi G r^2)) d/dr [r^2 (g - g_N)], g = glaw(g_N) of the host baryons, isolated (no EFE:
  generous, EFE lowers the host charge). Hosts: QX10's G5 set (reference 1e10 Msun + top-5 SPARC, exponential discs) and the
  four KiDS lens bins (point masses, log M_b 9.4, 10.45, 10.7, 10.9). Evaluated at r_ta(M_b) (QX10's rule).
  Sigma_*,f = min over hosts of rho_ph,host(r_ta): the HIGHEST threshold at which every host is stiff at its turnaround radius,
  i.e. the member most generous to the web.
- Web charge: rho_ph,web = div_phys[(nu - 1) g_N] / (4 pi G) on iter_1's realisations (same seed, same z grid, footing f).
- 2X enters host and web alike (X/X_bg = 1/(1+Phi)^2, QX7) and is dropped from the comparison (disclosed).

## Gates

- C1 (reported K): rho_ph,host nonincreasing on [R_opt or 10 kpc, r_ta] for every host, so Sigma >= Sigma_* inside r_ta.
- C2 web soft: F_f(z) = mass-weighted (weight max(1 + delta, 0)) fraction of web cells with rho_ph,web >= Sigma_*,f must be
  <= f_line = 1.5 sigma_A,rel at every z of the grid (a stiff fraction F withholds about 2F of the lensing power). FAIL otherwise.
- C3 G5 / G6 / G7: PASS by construction under QX10's convention (sector beyond r_ta is not retained) when C1 holds. The expulsion
  dynamics is NOT EVALUABLE (not run).
- C4 Cassini: rho_ph of the Galaxy at the Sun (point mass 6e10 Msun at 8.2 kpc, law on) >= Sigma_* means no sector in the Solar
  System and AC2q / v3s statics unchanged (C6P inherited). c_T: ARGUED unchanged (a scalar pressure switch adds no (dh)^2 term;
  EQUATIONS 6.2). Not graded beyond that.
- C5 primary CMB: covered by C2 at z >= 10 (the sector must be cold there; QX15).

## Label

NO-GO FOR CLASS C (inside the action, law on the web) if C2 fails on both footings: by monotonicity (Lean) every web cell with
Sigma >= Sigma_* is at least as stiff as the least-charged host at r_ta, so the sector cannot cluster there.
Reported, conditional on A-web (law off on the web, NOT in the action): D.P_web = 0, Sigma_web = 2X <= 2 rho_DE with
rho_DE = 4 a0^2/(G c^2); C2 then passes iff Sigma_* > 2 rho_DE. Reported: AC2q's own sign switch (threshold 0), F_0(z).

## Checks and MUTATE

- K1: deep-MOND point mass, rho_ph 4 pi G r^2 = sqrt(a0 G M) at r = 100 r_M within 1 %.
- MUTATE M1 (switch off: sector soft everywhere): QX10's n = 1 end state at lambda = 1 kpc must FAIL G5 (bites).
- MUTATE M2 (web charge set to 0, the A-web branch): C2 must PASS; bites iff the main C2 fails.
