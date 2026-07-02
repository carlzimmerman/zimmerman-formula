#!/usr/bin/env python3
"""
ADVERSARIAL VERIFIER script 2 -- INDEPENDENT re-derivation of the KMS/passivity adjudication
(load-bearing computation #2): is the dS horizon a pump or a thermostat?

W1  Footing (canonical): H_L = H0 sqrt(Om_L), Z = sqrt(32pi/3), a0 = c H_L/Z = 9.3624e-11.
W2  T_dS = hbar H_L/(2 pi kB); KMS detailed balance => rho >= 0 (via verifier1 V3).
W3  Passivity in miniature (Pusz-Woronowicz content on 2 levels): thermal state has ZERO
    extractable work (ergotropy 0); inverted state is non-passive (W = w0 dp > 0). A pump IS
    a work source; one KMS bath at one temperature supplies none. The horizon is also the
    COLDEST reservoir in every galactic problem (T_dS << any system T): a sink, not a source.
W4  Galactic band re-derived two ways (50-250 Myr periods; w = g/v at the RAR knee) and the
    full SPARC envelope down to 44 H0. GH in-band occupation: log10 n at band edges/mid and
    at the extreme 44-H0 edge -- spectral emptiness robust to ANY band convention.
W5  Expansion channel (universe is not exact dS): |Hdot|/H0^2 = 1.5 Om_m = 0.4725; adiabatic
    parameter at band; |beta|^2 upper estimate ~ 1e-13, FALLING as w^-4 (monotone: passive
    ordering, no inversion window anywhere).
W6  Raman/difference-frequency generosity bound: Gamma_avail = |beta|^2 * w vs pump-hunt
    minimum 3 H0: shortfall ~ 1e10 even granting full inversion + O(1) coupling.
W7  CMB-vs-horizon free energy: real but 26.3 orders out of band and not the horizon.
W8  Counterfactual (sign structure): an INVERTED line at the horizon's own frequency
    (w_L ~ H0) gives delta_m = A/(w_L^2-w^2) > 0 for A<0 at every galactic frequency:
    ANTI-MOND above the line. MOND sign in-band requires w_L ABOVE the band, where the GH
    weight is the W4 zeros. The horizon cannot pump the MOND sign into galaxies even in
    principle.
W9  Parametric self-pumping door (verifier addition -- lazy-kill audit): the local
    Deser-Levin temperature T(|a|) is CONSTANT on a circular orbit (|a| const), so the
    orbital parametric-modulation channel vanishes identically for the flat-rotation-curve
    systems that define the RAR; for e>0 the payer is the orbit itself (drag, not pump), and
    verifier1-V5 state-blindness covers any Gaussian/parametric drive of a free field anyway.
W10 Gates cross-checks: Saturn numbers, wide-binary frequency, horn-(ii) amplification
    arithmetic, horn-(iii) G-rescale degeneracy, disk-heating |Re/Im| budget.
Exit 0 = all assertions hold.
"""
import numpy as np

ok = []
c, hbar, kB = 2.99792458e8, 1.054571817e-34, 1.380649e-23
Mpc, yr = 3.0856775814913673e22, 3.15576e7
GM_sun, AU = 1.32712440018e20, 1.495978707e11
kpc = Mpc/1e3

# --- W1 footing
H0 = 67.4e3/Mpc
OmL, Omm = 0.685, 0.315
HL = H0*np.sqrt(OmL)
Z = np.sqrt(32*np.pi/3)
a0 = c*HL/Z
assert abs(Z - 5.7888) < 1e-4
assert abs(a0/9.3624e-11 - 1) < 5e-4, a0
ok.append(f"W1 footing: H0={H0:.5e}, H_L={HL:.5e} s^-1, Z={Z:.5f}, a0=cH_L/Z={a0:.5e} m/s^2")

# --- W2 T_dS
T_dS = hbar*HL/(2*np.pi*kB)
assert abs(T_dS/2.198e-30 - 1) < 5e-3, T_dS
ok.append(f"W2: T_dS = {T_dS:.4e} K (Gibbons-Hawking; KMS per Bros-Epstein-Moschella). "
          "KMS => detailed balance => rho>=0 => delta_m>=0 (verifier1 V3): the GH state sits "
          "INSIDE the sign theorem's state clause at every temperature")

# --- W3 passivity/ergotropy in miniature
w0 = 1.0
def ergotropy(p):                       # H = diag(0, w0); passive = populations sorted desc
    E = p[1]*w0
    E_passive = sorted(p, reverse=True)[1]*w0
    return E - E_passive
assert ergotropy([0.73, 0.27]) == 0.0                        # thermal: passive, zero work
assert abs(ergotropy([0.27, 0.73]) - 0.46*w0) < 1e-12        # inverted: work = w0*dp > 0
T_sys_min = 2.7                                              # even the CMB floor
assert T_sys_min/T_dS > 1e29
ok.append(f"W3: thermal state ergotropy = 0 (passive; Pusz-Woronowicz: KMS <=> completely "
          f"passive, single KMS bath => zero cyclic work); inverted state non-passive. And "
          f"T_dS is {T_sys_min/T_dS:.1e}x COLDER than anything galactic: the horizon is the "
          "universe's coldest reservoir -- a SINK (drag), not a free-energy source. "
          "'Permanent free-energy source' conflates energy with free energy: FALSE for exact dS")

# --- W4 band, two independent routes + robustness
w_lo, w_hi = 2*np.pi/(250e6*yr), 2*np.pi/(50e6*yr)           # 50-250 Myr orbital periods
assert abs(w_lo/H0 - 364) < 5 and abs(w_hi/H0 - 1822) < 15
w_knee = [a0/v for v in (250e3, 50e3)]                        # w = g/v at g = a0
assert 150 < w_knee[0]/H0 < 200 and 800 < w_knee[1]/H0 < 900  # 171-857 H0: same band
w_mid = np.sqrt(w_lo*w_hi)
def log10_n(w):                                               # GH occupation, n ~ e^{-2pi w/HL}
    return -(2*np.pi*w/HL)/np.log(10.0)
l_mid, l_lo, l_44 = log10_n(w_mid), log10_n(w_lo), log10_n(44*H0)
assert l_mid < -2600 and l_lo < -1150 and l_44 < -140
# even at the EXTREME slow edge, the needed occupation n >= 3H0/w = 0.068 is missed by >140 orders
assert -l_44 + np.log10(3/44.0) > 140
ok.append(f"W4: band [365,1823] H0 (50-250 Myr) == [171,857] H0 (g=a0 knee, v=50-250 km/s); "
          f"GH log10(n): {l_mid:.0f} (mid), {l_lo:.0f} (slow edge), {l_44:.0f} (extreme 44 H0). "
          "Spectral emptiness is robust to ANY band convention: shortfall >140 orders even at 44 H0")

# --- W5 expansion channel
Hdot = 1.5*Omm                                                # |Hdot|/H0^2, LCDM z=0
adiab_mid = Hdot*H0**2/w_mid**2
nbeta = lambda w: (Hdot*H0**2/(2*w**2))**2
assert abs(Hdot - 0.4725) < 1e-4 and 5e-7 < adiab_mid < 9e-7
assert 1e-13 < nbeta(w_mid) < 2e-13
grid = np.linspace(100, 3000, 300)*H0
assert np.all(np.diff(nbeta(grid)) < 0)                       # falls with w: NO inversion window
ok.append(f"W5: |Hdot|/H0^2 = {Hdot:.4f}; adiabaticity at band {adiab_mid:.2e}; "
          f"|beta|^2 ~ {nbeta(w_mid):.2e} at band mid, monotonically FALLING (w^-4): "
          "passive ordering everywhere -- the real universe's non-dS-ness holds no inversion")

# --- W6 Raman generosity
Gam_need = 3*H0
Gam_avail = nbeta(w_mid)*w_mid                                # full inversion + O(1) coupling GRANTED
short = Gam_need/Gam_avail
assert short > 5e9, short
ok.append(f"W6: difference-frequency loophole at maximal generosity: Gamma_avail = |beta|^2 w = "
          f"{Gam_avail:.2e} s^-1 vs needed 3H0 = {Gam_need:.2e} s^-1: shortfall x{short:.1e} "
          "(>=10 orders); with honest KMS occupations, >900 orders (W4)")

# --- W7 CMB
T_cmb = 2.7255
w_cmb = kB*T_cmb/hbar
assert 26.0 < np.log10(w_cmb/w_mid) < 26.6
assert 1.1e30 < T_cmb/T_dS < 1.4e30
ok.append(f"W7: CMB/horizon T-ratio {T_cmb/T_dS:.2e} (real free energy) but 10^{np.log10(w_cmb/w_mid):.1f} "
          "out of band, tracks the radiation sector (T_CMB ~ (1+z)) not cH_L/Z, and is the "
          "matter sector -- not the horizon")

# --- W8 counterfactual sign structure
A = -1.0                                                      # inverted line strength (sign only)
dm = lambda w, wL: A/(wL**2 - w**2)
for wL in [0.5*H0, 1.0*H0, HL, 3*H0]:
    assert dm(w_mid, wL) > 0                                  # ANTI-MOND at every galactic w
    assert dm(0.3*wL, wL) < 0                                 # MOND sign exists only BELOW the line
# MOND sign in-band requires wL > band top; GH weight there:
assert log10_n(w_hi) < -5800
ok.append("W8: an inverted line at the horizon's own frequency (~H0) gives delta_m > 0 "
          "(ANTI-MOND) at every galactic frequency; the MOND sign in-band needs the line ABOVE "
          f"the band, where GH weight is 10^{log10_n(w_hi):.0f}. Even counterfactually the "
          "horizon cannot pump the MOND sign into galaxies")

# --- W9 parametric self-pump door (verifier addition)
v, r = 120e3, 15*kpc                                          # circular orbit, |a| constant
phases = np.linspace(0, 2*np.pi, 7)
amag = np.full_like(phases, v**2/r)                           # |a(t)| on a circle
T_DL = hbar*np.sqrt(amag**2 + (c*HL)**2)/(2*np.pi*c*kB)
assert np.ptp(T_DL) == 0.0
ok.append("W9: Deser-Levin T(|a|) is exactly CONSTANT on circular orbits => the orbital "
          "parametric-modulation channel is identically zero for flat-rotation-curve systems; "
          "for e>0 the orbit itself pays (drag) and V5 state-blindness covers Gaussian drives: "
          "no lazy kill -- this door is computed shut")

# --- W10 gates cross-checks
g_sat = GM_sun/(9.58*AU)**2
assert abs(a0/(2*g_sat)/7.2e-7 - 1) < 0.02                    # acceleration-gated Saturn tail
w_sat = 2*np.pi/(29.46*365.25*24*3600)
assert 3.0e9 < w_sat/H0 < 3.2e9                               # Saturn 3.1e9 H0: >1e6 x band top
a_wb = 5000*AU                                                # wide binary, ~1 Msun total
w_wb = np.sqrt(GM_sun/a_wb**3)
assert 2.0e5 < w_wb/H0 < 4.0e5                                # ~2.6e5 H0: ~140-170x above band
amp = 1/(1 - 0.9**2)
assert abs(amp - 5.263) < 5e-3 and 0.9*amp > 1.0              # horn (ii): m_eff crosses 0
g_deep = a0/100
mu_deep = np.sqrt(g_deep/(g_deep + a0))
assert abs((1 - mu_deep) - 0.9005) < 1e-3                     # deep-MOND needs |dm|/m ~ 0.90
# horn (iii) G-rescale degeneracy: m(1-eps) v^2/r = G m M/r^2  <=>  v^2 = [G/(1-eps)] M/r
rng = np.random.default_rng(3)
for _ in range(5):
    M, rr, eps = 10**rng.uniform(38, 42), rng.uniform(1, 30)*kpc, rng.uniform(0.05, 0.9)
    v1 = np.sqrt(6.674e-11*M/((1-eps)*rr))
    v2 = np.sqrt((6.674e-11/(1-eps))*M/rr)
    assert abs(v1/v2 - 1) < 1e-12
# disk-heating budget
t_age = 10e9*yr
GamE_max = 0.1/t_age
im_budget = 2*GamE_max/w_mid
ratio = (1 - mu_deep)/im_budget
assert 2.5e-4 < im_budget < 4.5e-4 and ratio > 2.0e3
ok.append(f"W10: Saturn g={g_sat:.2e} => acc-gated |dm|/m = {a0/(2*g_sat):.2e}; Saturn at "
          f"{w_sat/H0:.1e} H0, wide binaries at {w_wb/H0:.1e} H0 (band-gated kernel silent there "
          f"=> gamma->1 falsifier); horn-(ii) amplification x{amp:.2f} => 0.9*{amp:.2f} = "
          f"{0.9*amp:.2f} > 1 (m_eff<=0 shell); G-rescale degeneracy exact; disk heating: "
          f"|Im dm|/m <= {im_budget:.1e} while deep-MOND |Re dm|/m = {1-mu_deep:.2f} => "
          f"|Re/Im| >= {ratio:.1e} => line >= ~1e3 linewidths off-band => trilemma horns (ii)/(iii)")

print("ALL ASSERTIONS PASSED (verifier 2: KMS/thermostat adjudication re-derived independently)")
for line in ok:
    print(" *", line)
