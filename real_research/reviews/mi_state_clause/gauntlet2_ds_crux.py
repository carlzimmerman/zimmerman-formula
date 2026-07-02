#!/usr/bin/env python3
"""
GAUNTLET ITEM 2 -- THE CRUX: is the dS horizon a pump or a thermostat?

Adjudicated head-on, with numbers:
  (a) Gibbons-Hawking static-patch state is KMS at T_dS = hbar*H_L/(2 pi k_B c ... ) --
      KMS is EXACTLY the passivity clause (gauntlet1 A5/B1: KMS => rho>=0 => delta_m>=0).
      A single KMS bath at one temperature has ZERO extractable work (Pusz-Woronowicz 1978
      passivity theorem; Kelvin-Planck). "Permanent free-energy source" is thermodynamically
      FALSE for exact dS: free energy requires a second reservoir or a non-KMS state.
  (b) Spectral emptiness in-band: GH occupation at the galactic band w ~ 700 H0 is
      n = 1/(e^{2 pi w/H_L} - 1) ~ 10^-2000 -- the horizon bath has NOTHING to deliver at
      the frequencies where the MOND kernel must act, inverted or not.
  (c) Expansion-driven non-equilibrium (the real universe is not exact dS): adiabaticity at
      the band is |Hdot|/w^2 ~ 1e-6; adiabatic-basis occupations |beta|^2 <~ (Hdot/2w^2)^2
      ~ 1e-13, and they DECREASE with w => no inversion => passive sign anyway (and by
      gauntlet1-C, for linear coupling to a free field the sign is state-blind REGARDLESS).
  (d) Raman/difference-frequency loophole (quadratic coupling): a gap Delta = w1-w2 in-band
      requires the UPPER mode at w1 >= Delta = 700 H0, where occupations are the (b)/(c)
      numbers; max gain rate ~ n*w is >= 9 orders below the pump-hunt's own minimum
      Gamma >= 3 H0. KILLED both ways (honest generosity shown).
  (e) The real free energy in the cosmos (CMB at 2.7 K vs T_dS): band mismatch 26 orders;
      and it is the MATTER sector, not the horizon.
  (f) Accelerated-worldline horizon flux (Deser-Levin): thermal ALONG the worldline =>
      worldline-KMS => passive => Unruh DRAG (anti-MOND direction), not gain.
Exit 0 = all assertions hold.
"""
import numpy as np

ok = []

# constants (SI)
c     = 2.99792458e8
hbar  = 1.054571817e-34
kB    = 1.380649e-23
Mpc   = 3.0856775814913673e22
yr    = 3.155814954e7   # Julian-ish year, s (not load-bearing at this precision)

# framework footing (canonical): H0 = 67.4, Omega_L = 0.685, Z = sqrt(32 pi/3)
H0  = 67.4e3/Mpc
OmL = 0.685
HL  = H0*np.sqrt(OmL)
Z   = np.sqrt(32*np.pi/3)
a0  = c*HL/Z
assert abs(a0 - 9.36e-11) < 0.01e-11, a0
ok.append(f"footing: H0={H0:.4e} s^-1, H_L={HL:.4e} s^-1, Z={Z:.4f}, a0=cH_L/Z={a0:.4e} m/s^2 (canonical 9.36e-11)")

# (a) T_dS and the single-bath work statement
T_dS = hbar*HL/(2*np.pi*kB)
assert 1e-31 < T_dS < 1e-29
ok.append(f"(a) T_dS = hbar*H_L/(2 pi k_B) = {T_dS:.3e} K. GH state = KMS at T_dS "
          "(Gibbons-Hawking 1977; Bros-Epstein-Moschella). KMS => rho>=0 (gauntlet1 B1) => "
          "delta_m>=0. Pusz-Woronowicz: NO cyclic work from a single KMS bath => "
          "'the horizon is a permanent free-energy source' is FALSE for exact dS.")

# (b) in-band spectral emptiness of the GH bath
w_band_lo, w_band_hi = 2*np.pi/(250e6*yr), 2*np.pi/(50e6*yr)   # 50-250 Myr orbits
w_mid = np.sqrt(w_band_lo*w_band_hi)
x_lo, x_mid = 2*np.pi*w_band_lo/HL, 2*np.pi*w_mid/HL           # hbar w/(kB T_dS) = 2 pi w/H
log10_n_mid = -x_mid/np.log(10.0)                               # n ~ e^{-x}
log10_n_lo  = -x_lo/np.log(10.0)
assert w_band_lo/H0 > 300 and w_band_hi/H0 < 2000
assert log10_n_mid < -1900 and log10_n_lo < -900
ok.append(f"(b) band = [{w_band_lo:.2e},{w_band_hi:.2e}] s^-1 = [{w_band_lo/H0:.0f},{w_band_hi/H0:.0f}] H0; "
          f"GH occupation at band: log10 n = {log10_n_mid:.0f} (mid), {log10_n_lo:.0f} (slow edge). "
          "The horizon bath is spectrally EMPTY in-band by >900 orders of magnitude.")

# (c) expansion-driven non-equilibrium at the band (the universe is not exact dS)
Om_m = 1 - OmL
Hdot_over_H2 = 1.5*Om_m           # |Hdot|/H^2 at z=0 (LCDM)
adiab = Hdot_over_H2*H0**2/w_mid**2
n_beta = (Hdot_over_H2*H0**2/(2*w_mid**2))**2   # |beta|^2 upper estimate, smooth expansion
assert adiab < 1e-5 and n_beta < 1e-12
ok.append(f"(c) |Hdot|/H0^2 = {Hdot_over_H2:.3f}; adiabaticity at band |Hdot|/w^2 = {adiab:.1e}; "
          f"|beta|^2 <~ {n_beta:.1e}, and it FALLS with w (no inversion anywhere) => even the "
          "non-dS expansion holds a PASSIVE-ordered, nearly-empty state in-band; and for LINEAR "
          "coupling to a free field the dissipation kernel is state-blind anyway (gauntlet1-C).")

# (d) difference-frequency (Raman) loophole: gap in band needs upper mode >= band frequency
# |w1 - w2| = Delta and w1,w2 > 0  =>  max(w1,w2) >= Delta.  (arithmetic identity)
Delta = w_mid
w1 = Delta + 0.0  # the minimal upper mode
assert max(w1, w1 - Delta) >= Delta
Gamma_needed = 3*H0                                  # pump-hunt R2 minimum
Gamma_avail_generous = n_beta*w_mid                  # O(1) coupling, full inversion granted
shortfall = Gamma_needed/Gamma_avail_generous
assert shortfall > 1e8
ok.append(f"(d) Raman loophole: an in-band gap needs occupation at w >= 700 H0; granting the "
          f"(c) occupations FULL inversion and O(1) coupling: Gamma_avail ~ n*w = "
          f"{Gamma_avail_generous:.2e} s^-1 vs Gamma_needed = 3 H0 = {Gamma_needed:.2e} s^-1 -- "
          f"shortfall x{shortfall:.1e} (>=9 orders). With the honest KMS numbers the shortfall "
          "is >900 orders. No expansion channel pumps the band.")

# (e) the real cosmic free energy (CMB vs T_dS) is 26 orders out of band and not the horizon
T_cmb = 2.7255
w_cmb = kB*T_cmb/hbar
band_miss = np.log10(w_cmb/w_mid)
assert 25 < band_miss < 28
ok.append(f"(e) CMB-vs-horizon gradient is real free energy (T_CMB/T_dS ~ {T_cmb/T_dS:.1e}) but "
          f"w_CMB/w_band = 10^{band_miss:.1f}: 26 orders out of band, no down-conversion "
          "mechanism, amplitude would track the radiation sector not cH_L/Z -- and it is not "
          "'the dS horizon' pumping.")

# (f) accelerated worldline: Deser-Levin temperature is thermal ALONG the worldline
g_gal = a0    # deep-MOND-edge orbit
T_DL  = hbar*np.sqrt(g_gal**2 + (c*HL)**2)/(2*np.pi*c*kB)
assert T_DL < 1e-28
ok.append(f"(f) Deser-Levin T(a0) = {T_DL:.2e} K -- a THERMAL (worldline-KMS) spectrum: "
          "detailed balance along the orbit => passive => the only energy flow is orbit->bath "
          "(Unruh drag, anti-MOND direction). The DL structure supplies the a0~cH_L SCALE and "
          "the right VARIABLE (acceleration), but as a thermostat, not a pump.")

# the adjudication inequality: what the pump needs vs what the horizon has, side by side
ok.append("(g) ADJUDICATION: pump-hunt spec needs power at 362-1810 H0 with T-odd coupling at "
          "Gamma >= 3 H0; the horizon has (i) zero extractable work at one temperature (KMS), "
          "(ii) 10^-2000 occupation in-band, (iii) no inversion channel (free-field linear "
          "coupling is state-blind; expansion occupations fall with w). The dS horizon is a "
          "THERMOSTAT. The pump-hunt's kill of the thermal dS bath STANDS; the cartography's "
          "'the dS horizon IS the pump' does not survive contact with its own premise "
          "(GH thermality) -- the very thermality that makes T_dS ~ a0/c work as a SCALE is "
          "what forbids it from being a PUMP.")

print("ALL ASSERTIONS PASSED (gauntlet 2)")
for line in ok:
    print(" *", line)
