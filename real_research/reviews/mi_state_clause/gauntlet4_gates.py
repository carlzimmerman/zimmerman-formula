#!/usr/bin/env python3
"""
GAUNTLET ITEM 4 -- GATES: Cassini, universality, energy bookkeeping.
Plus the gauntlet's sharpest new product: the LINE-PLACEMENT TRILEMMA for any linear
pumped kernel + saturation (the frequency-gating vs acceleration-gating wall).

G1 CASSINI: worldline-MI has no slip field by construction => gamma_MI = 1 exactly vs
   Bertotti+ 2003 gamma-1 = (2.1+/-2.3)e-5: PASS. Both gatings safe at Saturn:
   acceleration-gated |delta_m|/m = a0/(2 g_Sat) = 7.2e-7 (below ranging leverage on gamma);
   band-gated: Saturn at 3.1e9 H0 (>=1e6 x band top) => kernel OFF => 0. But note the two
   gatings DISAGREE about what Saturn should see -- the realization must choose.

G2 TRILEMMA (universality + stability + shape simultaneously):
   Horn (i)  gain line IN band (w_L in 44-3008 H0): 1/(w_L^2-w^2) changes sign across the
             band => MOND-signed inside/below, ANTI-MOND above, divergence at w_L: the RAR
             is one-signed at 0.11 dex across the whole domain => killed (this is the
             pump-hunt's R_flip kill, reproduced for the horizon-pump kernel).
   Horn (ii) line ABOVE band but below the top of the populated frequency ladder
             (comets/binaries/planets occupy 1e3-1e10 H0 continuously): systems just below
             w_L see the shift AMPLIFIED (x5.3 at w=0.9 w_L) => m_eff <= 0 shell (unbound/
             runaway zone) + anti-MOND shell above w_L: unobserved => killed.
   Horn (iii) line above EVERYTHING (w_L > 1e14 H0 pulsar band): every system sees the SAME
             delta_m => uniform inertia rescale == G-rescale (sympy: m(1-eps)a = GmM/r^2
             <=> a = [G/(1-eps)]M/r^2) => locally unobservable, NO acceleration dependence,
             NO RAR curvature => the MOND phenomenology VANISHES. Also: a circular orbit is
             a pure tone at w_orb -- Fourier power at w_L is exactly 0 (harmonic n = w_L/w_orb
             needs (v/c)^n ~ 1e-300 suppression) => saturation NEVER ENGAGES => no
             amplitude-dependence can rescue horn (iii).
   => a LINEAR pumped kernel is frequency-gated; the data demand acceleration-gating;
      converting w-gating to a-gating needs in-band nonlinear engagement = horn (i).

G3 ENERGY BOOKKEEPING: in-band gain anti-damps orbits: Gamma_E = w(-Im dm)/(2m)
   (gauntlet1-D3). Disk longevity (thin disks survive ~10 Gyr) => Gamma_E <= 0.1/t_age
   => |Im dm|/m <= 3.0e-4 at band mid while deep-MOND needs |Re dm|/m ~ 0.90
   (g = a0/100) => |Re/Im| >= 3.0e3 => detuning >= 1.5e3 linewidths => the line is
   off-band => horn (ii)/(iii) of the trilemma. And in exact dS NOTHING pays (gauntlet2a:
   single-KMS-bath, zero extractable work); if the matter sector pays, the pump is not
   the horizon.
Exit 0 = all assertions hold.
"""
import numpy as np
import sympy as sp

ok = []

c = 2.99792458e8
Mpc = 3.0856775814913673e22
yr = 3.155814954e7
H0 = 67.4e3/Mpc
HL = H0*np.sqrt(0.685)
Z = np.sqrt(32*np.pi/3)
a0 = c*HL/Z
GM_sun = 1.32712440018e20

# ---------------- G1 Cassini
r_sat = 9.58*1.495978707e11
g_sat = GM_sun/r_sat**2
dm_acc = a0/(2*g_sat)                       # acceleration-gated MI correction at Saturn
w_sat = 2*np.pi/(29.46*yr*1.0e0)            # Saturn orbital angular frequency... (29.46 yr)
w_sat = 2*np.pi/(29.46*365.25*24*3600)
band_top = 3008*H0                          # pump-hunt honest full RAR domain
assert dm_acc < 1e-6
assert w_sat/band_top > 1e5
gamma_cassini = 2.3e-5                      # Bertotti+ 2003 1-sigma
ok.append(f"G1: gamma_MI = 1 exactly (no slip field on a worldline route) vs Cassini "
          f"|gamma-1| <= {gamma_cassini:.1e}: PASS by construction. Saturn numbers: "
          f"acceleration-gated |dm|/m = {dm_acc:.2e}; band-gated = 0 (w_Sat = {w_sat/H0:.2e} H0 "
          f"= {w_sat/band_top:.1e} x band top). NOTE the two gatings disagree at Saturn "
          "(7e-7 vs 0) -- the realization must pick one; both pass Cassini-gamma, but only "
          "band-gating also predicts the wide-binary gamma->1 falsifier.")

# ---------------- G2 trilemma
# horn (i): sign change of the shift across the band for an in-band line
wL = 700*H0
band = np.array([44, 3008])*H0
shift = lambda w, wl: 1.0/(wl**2 - w**2)     # sign carrier of delta_m(w) for a line at wl
s_lo, s_hi = shift(band[0], wL), shift(band[1], wL)
assert s_lo*s_hi < 0
ok.append(f"G2(i): in-band line (w_L=700 H0): shift sign at band edges = ({np.sign(s_lo):+.0f}, "
          f"{np.sign(s_hi):+.0f}) -- MOND-signed below the line, ANTI-MOND above, divergence at "
          "w_L; SPARC RAR is one-signed at 0.11 dex across 44-3008 H0 (Lelli+ 2017): KILLED "
          "(pump-hunt R_flip kill, reproduced for the horizon-pump kernel).")

# horn (ii): amplification just below an above-band line + anti-MOND shell above it
amp_09 = abs(shift(0.9*wL, wL))/abs(shift(0.0, wL))     # |dm(0.9 wL)|/|dm(0)|
assert abs(amp_09 - 1/(1 - 0.81)) < 1e-9                # = 5.26
dm_band_deep = 0.90                                     # |Re dm|/m needed at g = a0/100
assert dm_band_deep*amp_09 > 1.0                        # m_eff crosses ZERO below the line
# populated ladder: wide binaries P ~ 1e3 yr .. 1e8 yr and comets fill 1e3-1e9 H0
P1, P2 = 1e3*yr, 1e8*yr
w_bin_hi, w_bin_lo = 2*np.pi/P1/H0, 2*np.pi/P2/H0
assert w_bin_lo < 3e3 and w_bin_hi > 5e7
ok.append(f"G2(ii): line above band but below the populated ladder: shift amplified x{amp_09:.2f} "
          f"at w=0.9 w_L => with in-band |dm|/m = {dm_band_deep} the m_eff<=0 shell is crossed "
          f"(0.90 x 5.26 = {dm_band_deep*amp_09:.2f} > 1) => unbound/runaway zone at orbital "
          f"periods near 2pi/w_L, plus an anti-MOND shell above; binaries+comets populate "
          f"[{w_bin_lo:.0f}, {w_bin_hi:.1e}] H0 continuously -- no such shell exists: KILLED.")

# horn (iii): line above everything => uniform dm => G-rescale degeneracy (sympy) + pure tone
eps, m_, a_, G_, M_, r_ = sp.symbols('epsilon m a G M r', positive=True)
lhs = sp.Eq(m_*(1 - eps)*a_, G_*m_*M_/r_**2)
sol_a = sp.solve(lhs, a_)[0]
assert sp.simplify(sol_a - (G_/(1 - eps))*M_/r_**2) == 0
# flatness: for w_L = 1e14 H0, spread of dm across 1 H0..3e9 H0 (Saturn):
wL3 = 1e14*H0
spread = abs(shift(3.09e9*H0, wL3) - shift(1*H0, wL3))/abs(shift(1*H0, wL3))
assert spread < 1e-8
# pure tone: circular orbit x(t) = R e^{i w t}: Fourier support = {w_orb} exactly;
# reaching w_L needs harmonic n with amplitude ~ (v/c)^n:
n_harm = wL3/(700*H0)
log10_amp = n_harm*np.log10(1e-3)                       # v/c ~ 1e-3 galactic
assert log10_amp < -1e10
ok.append(f"G2(iii): line above everything (w_L=1e14 H0): dm spread across ALL systems < "
          f"{spread:.1e} => uniform inertia deficit == G-rescale (sympy-exact: a = G/(1-eps) "
          f"M/r^2) => locally UNOBSERVABLE, no a-dependence, no RAR curvature -- the MOND "
          f"phenomenology vanishes. Saturation cannot rescue it: a circular orbit is a pure "
          f"tone at w_orb; power at w_L via harmonic n = {n_harm:.1e} is suppressed by "
          f"10^{log10_amp:.1e} = zero. KILLED.")

# horn (iv): the CONTINUUM wriggle -- a broadband inverted profile spanning the band.
# Re dm(w) = P.int w(w')/(w'^2-w^2) dw' with w(w') = -w0 (inverted, flat on [w1,w2]):
# P.V. primitive: int dx/(x^2-a^2) = (1/2a) ln|(x-a)/(x+a)|
def pv_flat(w, w1, w2):
    return (1.0/(2*w))*(np.log(abs((w2 - w)/(w2 + w))) - np.log(abs((w1 - w)/(w1 + w))))
w1b, w2b = 44.0, 3008.0                      # units of H0
re_100  = -1.0*pv_flat(100.0,  w1b, w2b)     # w0=1
re_1000 = -1.0*pv_flat(1000.0, w1b, w2b)
im_100  = -np.pi/(2*100.0)                   # Im dm = -pi w(w)/(2w), inverted
assert re_100 < 0 and re_1000 > 0            # Re dm FLIPS SIGN inside the band
assert abs(re_100/im_100) < 1.0              # and where it is MOND-signed, |Re|<|Im|
ok.append(f"G2(iv): continuum gain spanning the band: Re dm flips sign INSIDE the band "
          f"(Re(100 H0) = {re_100:.3e} w0 < 0, Re(1000 H0) = {re_1000:+.3e} w0 > 0 -- P.V. "
          f"balance point) AND where MOND-signed |Re/Im| = {abs(re_100/im_100):.2f} < 1 "
          "(no detuning hierarchy) => heating bound (G3) violated by >3 orders. The "
          "continuum escape from horn (i) is closed: in-band weight is P.V.-suppressed in "
          "Re and direct in Im.")

# horn (v): pump the horizon's OWN modes (~1 H0, the only place it has spectral weight):
# inverted weight BELOW the band => for in-band w > w_L: dm = A/(w_L^2-w^2), A<0 =>
# denominator<0 => dm > 0 = ANTI-MOND at every galaxy.
wL_h = 1.0*H0
dm_sign_inband = -1.0/(wL_h**2 - (700*H0)**2)   # A=-1
assert dm_sign_inband > 0
ok.append("G2(v): even granting the impossible -- a population-inverted mode AT the horizon "
          "frequency (~1 H0, the only band where dS has weight) -- the dispersive shift it "
          "produces IN the galactic band (w >> w_L) is dm = A/(w_L^2-w^2) > 0 for A<0: "
          "ANTI-MOND. Gain BELOW the band gives the wrong sign ABOVE it. The horizon cannot "
          "pump the MOND sign into galaxies from its own frequency, period.")

ok.append("G2 verdict: linear pumped kernels are FREQUENCY-gated; the RAR demands "
          "ACCELERATION-gating (same a0 at every radius/system, one-signed); converting "
          "w-gating to a-gating requires the nonlinearity to engage AT the orbital band = "
          "horn (i)/(iv) = killed. The trilemma (+ the two wriggles iv, v) closes: no "
          "placement of the gain spectrum reproduces MOND phenomenology while passing the "
          "system surveys.")

# ---------------- G3 energy bookkeeping / heating bound
t_age = 13.8e9*yr
w_mid = np.sqrt(44*3008)*H0*np.sqrt(1.0)     # geometric band mid ~364 H0; use 700 H0 canonical
w_mid = 700*H0
GammaE_max = 0.1/t_age                       # disk-longevity tolerance (10% energy per age)
Im_dm_max = 2*GammaE_max/w_mid               # Gamma_E = w*(-Im dm)/(2m)
Re_needed = 0.90
ratio = Re_needed/Im_dm_max
assert 1e3 < ratio < 1e5
ok.append(f"G3: heating: Gamma_E = w|Im dm|/(2m) <= 0.1/t_age => |Im dm|/m <= "
          f"{Im_dm_max:.2e} at 700 H0, while deep-MOND needs |Re dm|/m ~ {Re_needed} => "
          f"|Re/Im| >= {ratio:.1e} => detuning >= {ratio/2:.0e} linewidths => the gain line "
          "must sit far off-band => G2 horns (ii)/(iii). In exact dS nothing pays at all "
          "(single-KMS bath, zero extractable work, gauntlet2a); if the matter sector pays, "
          "the pump is by definition not the dS horizon. Energy bookkeeping FAILS for the "
          "horizon-pump reading; it survives only as the pump-hunt's unoccupied spec "
          "(universal field, T-odd band-limited coupling, Gamma >= 3 H0 ~ secular cost "
          "4.6 Gyr -- friction-signed, i.e. DISSIPATIVE phase-pinning, NOT gain).")

# the friction-vs-gain sign tension, stated sharply:
ok.append("G3b: NOTE the internal tension in the merged claim: the pump-hunt spec needs "
          "T-odd FRICTION (Gamma >= +3 H0, energy orbit->bath) to pin phase (R2), while the "
          "inverted-bath route needs GAIN (energy bath->orbit) to make delta_m < 0. One "
          "kernel must be dissipative at the phase-pinning frequencies and amplifying in the "
          "mass-shift integral simultaneously -- not impossible for a structured rho(w) with "
          "both signs, but nothing exhibited so far provides it; the merged document's two "
          "requirements currently point in opposite thermodynamic directions.")

print("ALL ASSERTIONS PASSED (gauntlet 4)")
for line in ok:
    print(" *", line)
