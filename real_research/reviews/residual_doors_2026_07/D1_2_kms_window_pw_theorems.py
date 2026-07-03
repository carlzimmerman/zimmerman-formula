#!/usr/bin/env python3
"""
D1_2: THE THEOREM ROUTE FOR INTERACTING FIELDS -- BW/KMS + WINDOWS, AND
      WHAT PUSZ-WORONOWICZ DOES *NOT* CLOSE
========================================================================
Lane D1, part 2 of 4. Convention (matches Theorem VI): for a stationary
pull-back W(tau-tau') with spectral function S(nu) >= 0 (Bochner),
   W(u) = int dnu/2pi e^{-i nu u} S(nu),
the windowed response at detector gap omega is
   F(omega) = int int chi chi' e^{-i omega(tau-tau')} W(tau-tau')
            = int dnu/2pi S(nu) |chihat(omega + nu)|^2 ,  chihat = FT of chi.
Excitation = F(omega>0); emission = F(-omega). Windowing = smearing of S
by the window power spectrum |chihat|^2.

(a) BISOGNANO-WICHMANN (uniform acceleration, ANY Wightman QFT):
The Minkowski vacuum restricted to the Rindler wedge is KMS at
T_U = a/2pi with respect to the boost -- an axiomatic theorem (Wightman
axioms only), INTERACTING FIELDS INCLUDED. Hence along a uniformly
accelerated worldline the pulled-back W is stationary with
   S(nu) = e^{-beta nu} S(-nu),  beta = 2pi/a   (detailed balance).

MONOTONE-WINDOW LEMMA (proved below, verified numerically): if |chihat|^2
is even and non-increasing in |k| (Gaussian windows qualify), then for
ANY KMS spectral function and ANY window length,
   F(omega) <= F(-omega)  for all omega > 0.
Proof: F(-w)-F(w) = int_0^inf dnu/2pi [S(-nu)-S(nu)] *
       [|chihat(w-nu)|^2 - |chihat(w+nu)|^2]; both brackets are >= 0
       (first by beta>0 detailed balance, second by monotonicity since
       |w-nu| <= w+nu). QED.
=> Windowed detailed balance SURVIVES for interacting fields on uniform
trajectories: NO inversion, window or no window. Leg (iii) CLOSED here.

The SAME decomposition with vacuum-type S (supported nu >= 0, spectrum
condition) gives F(w) <= F(-w) for INERTIAL trajectories of ANY
interacting theory: |chihat(w+nu)|^2 <= |chihat(nu-w)|^2 for nu,w > 0.

(b) HARD WINDOWS: the lemma needs monotone |chihat|^2. A boxcar window
(sinc sidelobes) CAN produce F(w) > F(-w) -- quantified below: it is a
switching artifact, needs a narrow-line spectrum + a sinc ZERO landing on
the emission side, is absent for any KMS/vacuum CONTINUUM tested, and
dies with window length. The switching agent supplies the quanta.

(c) PUSZ-WORONOWICZ, honestly: PW says the vacuum of any QFT is passive
-- no work extraction by CYCLIC UNITARIES acting on the field alone. A
detector dragged on a NON-UNIFORM trajectory is an externally DRIVEN open
system: the agent moving it supplies work (the Unruh effect itself
excites detectors!). PW therefore does NOT forbid detector population
inversion on non-uniform trajectories. THE THEOREM ROUTE DOES NOT CLOSE
NON-UNIFORM INTERACTING TRAJECTORIES -- that corner goes to computation
(D1_3: exact KL reduction + relativistic scan; D1_4: interacting lattice).
Any inversion found there is agent-pumped (drive-photon Raman/Stokes
class), i.e. exactly the pump channel Theorem VI already prices
(pump shortfall x2.9e10), not a violation of vacuum passivity.
"""
import numpy as np

chihatsq_gauss = lambda k, T: 2 * np.pi * T ** 2 * np.exp(-k ** 2 * T ** 2)
chihatsq_box = lambda k, T: T ** 2 * np.sinc(k * T / (2 * np.pi)) ** 2

def F_resp(omega, S, nu, T, win=chihatsq_gauss):
    return np.trapz(S * win(omega + nu, T), nu) / (2 * np.pi)

print(__doc__)
print("=" * 72)
print("(a) windowed-KMS lemma, numerical verification (Gaussian window)")
print("=" * 72)
nu = np.linspace(-60, 60, 24001)
worst = -np.inf
for beta in [0.3, 1.0, 3.0]:
    # three KMS spectra: 1+1-like, 3+1-like, and a 'lumpy' generic one
    S11 = nu / (1 - np.exp(-beta * nu)); S11[np.abs(nu) < 1e-12] = 1 / beta
    S31 = nu ** 3 / (1 - np.exp(-beta * nu)); S31[np.abs(nu) < 1e-12] = 0.0
    Q = np.exp(-(np.abs(nu) - 3) ** 2) + 0.5 * np.exp(-(np.abs(nu) - 8) ** 2 / 4)
    Slump = np.exp(beta * nu / 2) * Q * np.exp(-nu ** 2 / 200)
    for Sname, S in [("S~nu(1+1)", S11), ("S~nu^3(3+1)", S31),
                     ("lumpy-KMS", Slump)]:
        assert np.all(S >= -1e-12)
        for T in [0.2, 1.0, 5.0]:
            for w in np.linspace(0.1, 8, 25):
                r = F_resp(w, S, nu, T) / F_resp(-w, S, nu, T)
                worst = max(worst, r - 1)
        # infinite-window limit recovers exact detailed balance
        w0 = 2.0; Tbig = 40.0
        r_inf = F_resp(w0, S, nu, Tbig) / F_resp(-w0, S, nu, Tbig)
        print(f"  beta={beta:4.1f} {Sname:12s}: max[F(w)/F(-w) - 1] so far ="
              f" {worst: .2e};  T={Tbig:.0f}: ratio={r_inf:.5f} vs "
              f"e^-bw={np.exp(-beta * w0):.5f}")
assert worst < 1e-9, "windowed KMS detailed-balance inequality violated?!"
print("PASS: F(w) <= F(-w) for every KMS spectrum, every Gaussian window")
print("      length, every w>0 -- and -> e^{-beta w} as T -> inf.")
print("=> By Bisognano-Wichmann this holds for ANY INTERACTING Wightman QFT")
print("   on uniformly accelerated worldlines, windowed or not. CLOSED.")

print()
print("=" * 72)
print("(b) hard-window (boxcar) artifact: when CAN windowed 'inversion' occur")
print("=" * 72)
# continuum spectra: boxcar never inverted on the tested grid
worst_box = -np.inf
for beta in [0.5, 2.0]:
    S11 = nu / (1 - np.exp(-beta * nu)); S11[np.abs(nu) < 1e-12] = 1 / beta
    for T in [0.5, 2.0, 8.0]:
        for w in np.linspace(0.1, 8, 40):
            r = F_resp(w, S11, nu, T, chihatsq_box) / \
                F_resp(-w, S11, nu, T, chihatsq_box)
            worst_box = max(worst_box, r - 1)
print(f"  KMS continuum + boxcar: max[F(w)/F(-w) - 1] = {worst_box: .3e}"
      f"  (no inversion)")
# vacuum-type gapped continuum (KL slice, inertial): boxcar
Svac = np.where(nu >= 2.0, np.sqrt(np.clip(nu ** 2 - 4.0, 0, None)), 0.0)
worst_vac = -np.inf
for T in [0.5, 2.0, 8.0]:
    for w in np.linspace(0.1, 8, 40):
        r = F_resp(w, Svac, nu, T, chihatsq_box) / \
            F_resp(-w, Svac, nu, T, chihatsq_box)
        worst_vac = max(worst_vac, r - 1)
print(f"  gapped vacuum continuum (m=2) + boxcar: max = {worst_vac: .3e}")
# NARROW LINE + boxcar: inversion by sinc-zero placement (the artifact)
nu0, sig = 3.0, 0.02
Sline = np.exp(-(nu - nu0) ** 2 / (2 * sig ** 2))
print("  narrow line at nu0=3 + boxcar, w chosen so (nu0-w)T/2 = pi (sinc zero):")
for T in [2.0, 4.0, 8.0, 16.0]:
    w = nu0 - 2 * np.pi / T
    if w <= 0:
        continue
    r = F_resp(w, Sline, nu, T, chihatsq_box) / \
        F_resp(-w, Sline, nu, T, chihatsq_box)
    rg = F_resp(w, Sline, nu, T) / F_resp(-w, Sline, nu, T)
    print(f"    T={T:5.1f}, w={w:5.3f}:  boxcar F(w)/F(-w) = {r:9.3f}   "
          f"(same w, GAUSSIAN window: {rg:.2e})")
print("  => 'inversion' exists ONLY for (narrow line) x (hard switching):")
print("     sidelobe leakage; the switching supplies the quanta; the Gaussian")
print("     window kills it outright; QFT vacua/KMS baths are CONTINUA and")
print("     show none. This is the class Theorem VI's coherence discount and")
print("     window accounting already covers.")

print()
print("D1_2 VERDICT: uniform trajectories = CLOSED for interacting fields")
print("(BW + monotone-window lemma, all window lengths); inertial = CLOSED")
print("(spectrum condition, same lemma). PW does NOT close non-uniform")
print("trajectories (agent supplies work) -- computation required: D1_3/D1_4.")
