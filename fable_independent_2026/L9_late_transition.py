#!/usr/bin/env python3
"""
L9 -- the LATE-TIME TRANSITION: the last flagged escape for the cluster residual.
=================================================================================
L6 closed the screened-force door on a COSMOLOGICAL ORDERING argument: the homogeneous
background sits beyond cluster outskirts in every candidate screening variable, so any
monotone S(X) that unscreens clusters relative to galaxies unscreens the BACKGROUND at least
as much, forcing G_cosmo/G_local >= E(cluster outskirts) = 1.82, which BBN excludes.

L6 explicitly did NOT close ONE escape, and this is that test.  If the field ROLLS, the
background value at nucleosynthesis and the value today are DIFFERENT.  G can be normal at
BBN and enhanced now.  The ordering argument is a statement about a static monotone S(X); it
says nothing about a cosmological history.  So the escape is real -- and it converts the
problem from a screening mechanism into a cosmological history, which must then face the
gates a cosmological history faces.  That is what is computed here.

THE MODEL, stated (minimal: one shape, two parameters).
  G_unscreened(z) = G_0 * g(z),   g(z) = 1 + (F - 1) * sigma(z),
  sigma(z) = [1 - tanh((x - x_t)/W)] / [1 - tanh(-x_t/W)],   x = ln(1+z),  x_t = ln(1+z_t).
  So g(0) = F EXACTLY and g(z -> infinity) = 1 EXACTLY.  Two free parameters: the transition
  redshift z_t and the width W (in ln(1+z)).  F is NOT free: it is the factor the clusters
  require, read from the committed cluster audit below.

  WHY "unscreened".  A purely time-dependent G applying to the solar system too would be
  unobservable AS AN ENHANCEMENT -- everything is measured in units of TODAY's G, so the
  cluster discrepancy would vanish by definition.  The escape has content only as
  time-dependence PLUS screening: the local and galactic value is screened back to G_0 (which
  is what "the locally measured G" means), the cosmological background field value rolls, and
  cluster outskirts are unscreened and feel g(z) G_0.  That is L6's mechanism with the
  ordering constraint relaxed by the roll.  Everything below is in units of G_0.

THE FORK (requirement 5), stated before anything is computed.
  MODEL A -- G_eff enters the FRIEDMANN EQUATION AND the POISSON EQUATION.  This is what any
    scalar-tensor completion gives: the same background field value that sets the fifth-force
    strength also gravitates.  Taken as primary.  It has one exact and non-obvious property,
    derived not asserted: with H^2 = (8 pi g G_0/3) rho_tot and the Poisson source
    4 pi g G_0 rho_m, the factor g CANCELS from the growth SOURCE,
        4 pi G_eff rho_m / H^2 = (3/2) rho_m / rho_tot,
    so a late G-boost does NOT drive growth through the source term at all.  (Verified
    numerically in the control.)  The intuition that a 2-7x G boost drives growth hard is
    therefore WRONG as stated for a consistent model.  Growth still moves, but by a different
    and indirect route: closure at a = 1 reads 1 = F(Omega_m + Omega_r + Omega_Lambda), so
    fixing the measured H0 and the CMB's physical matter density FORCES Omega_Lambda down,
    which raises rho_m/rho_tot and hence the source.  The computation below finds which of
    that and the extra Hubble friction (1/2) dln g/dln a wins, rather than assuming.
  MODEL B -- G_eff enters the POISSON EQUATION ONLY; the background is exactly LambdaCDM.
    This is the phenomenological mu(a) parametrisation.  It is a DIFFERENT AND WEAKER MODEL:
    no action is supplied for it here, it requires the background gravitational effect of the
    rolling field to be cancelled by hand, and it evades BBN and the expansion history BY
    CONSTRUCTION rather than by passing them.  Computed and reported SEPARATELY, labelled
    throughout, and NOT claimed as a live mechanism.

THE CHECKS.  Each of T1-T5 asks whether ANY (z_t, W) on the scanned grid satisfies that gate
ALONE -- so a gate that is individually satisfiable PASSES, and no deficit is manufactured by
picking an unfavourable reference point.  The kill, if there is one, must live in the
INTERSECTION, which is T6.  A PASS on T6 would be the FIRST live mechanism for the cluster
residual in this programme and is the outcome most worth finding.  Nothing here is tuned
toward it or away from it: F comes from the committed audit, every tolerance is set loose,
and the grid is scanned rather than sampled.

  T0 [control]  with g == 1 the growth integrator returns the standard growth factor
                (Carroll-Press-Turner) and f(0) = Omega_m^0.55, the background code reproduces
                Planck's sound horizon and acoustic scale, and the Model-A source cancellation
                is numerically exact;
  T1 [BBN]      some (z_t, W) has g(z = 4e8) = 1 within the conservative bound 20%;
  T2 [CMB]      some (z_t, W) has g(z = 1090) = 1 within 10% (the CMB's own bound on G at
                recombination), with the induced sound-horizon shift reported;
  T3 [growth]   some (z_t, W) gives sigma_8 within 10% of 0.8111 AND RSD f*sigma_8 within
                Delta chi^2 <= 9 of LambdaCDM on the same 7 points;
  T4 [expansion] some (z_t, W) keeps the expansion history on at least ONE self-consistent
                background construction.  Three are offered and all three computed, since the
                model may not buy its expansion history from one normalisation and its growth
                from another: (a) the measured H0 = 67.36 with CMB-fixed physical densities,
                so closure fixes Omega_Lambda; (b) the BEST CASE, h refitted so the acoustic
                scale matches EXACTLY; (c) rho_Lambda held at its LambdaCDM value with H0
                allowed to float.  Conditions on each: Omega_Lambda >= 0, H0 in 60-80
                km/s/Mpc (bracketing Planck and SH0ES), acoustic scale within 0.3% (10x looser
                than Planck's 0.030%), q0 in [-0.75,-0.35], SNe distance-modulus shape within
                0.10 mag rms (3x looser than Pantheon+ systematics), and the BAO distance
                ladder within Delta chi^2 <= 9 on 12 points.  BAO is included because it is
                the only ABSOLUTE distance test here: D_M/r_drag and D_H/r_drag are measured
                against a standard ruler this model does not change (g = 1 before
                recombination), whereas the SNe test marginalises over its zero point and the
                acoustic scale is a single number the refit can always hit;
  T5 [delivers] some (z_t, W) actually DELIVERS the enhancement where the clusters are
                measured: g(z = 0.090) >= 0.9 F at the highest X-COP redshift;
  T6 [verdict]  some (z_t, W) passes T1 AND T2 AND T3 AND T4 AND T5 simultaneously, on BOTH
                a0 footings.  This is the question the lane exists to answer;
  T7 [fork B]   the weaker perturbation-only model survives ITS applicable gates;
  T8 [inherited] whether the roll ALSO supplies the cluster-versus-galaxy contrast, which is
                the SECOND, independent horn on which L6 killed the screened force.  Asked
                because a PASS on T6 would otherwise be over-read: T1-T6 are COSMOLOGICAL
                gates, and L6's overlap horn is not a cosmological statement.
FAIL marks a requirement the stated model does not meet.  Both a0 footings throughout: the
required factor F depends on the footing because the framework's kernel does.

WHAT A PASS ON T6 WOULD AND WOULD NOT MEAN, written down BEFORE the scan so the reading is not
chosen after seeing the answer.  T1-T6 ask exactly what L6 said a late-time transition would
have to face: BBN, the CMB, growth, the expansion history.  A PASS there means the ROLL DOES
DEFEAT L6's COSMOLOGICAL-ORDERING HORN and that the cosmology of such a model is not
immediately excluded -- which is a real and reportable finding.  It would NOT mean the cluster
residual has a mechanism, because L6 killed the screened force on TWO horns and the roll only
addresses one.  The other -- clusters and galaxies overlapping completely in baryon density
while requiring enhancements 12.8 sigma apart -- is a SPATIAL contrast between populations
observed at the same epoch, and a spatially uniform g(z) cannot supply it.  T8 quantifies by
how much.  The verdict of this lane is therefore the PAIR (T6, T8), not T6 alone.

NUMERICAL NOTE, stated because it moved the control: the linear-growth ODE is integrated on a
matter + Lambda background with radiation OMITTED, which is the standard definition of the
linear growth factor and is what Carroll-Press-Turner normalises.  Including radiation in the
growth ODE while starting at z = 999 gives an initial-condition-dependent answer 10% below
CPT (the residual Meszaros drag) and would have made every model look artificially suppressed.
Radiation IS kept everywhere it matters: the sound horizon, the distances, and the closure.
"""
import numpy as np, math, json, os, sys
np.seterr(over="ignore", invalid="ignore", divide="ignore")
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("=" * 124)
print("L9 -- the late-time transition: can a rolling G supply the cluster residual and survive cosmology?")
print("=" * 124, flush=True)

# ---------------------------------------------------------------- fixed external numbers
C_KMS   = 299792.458
Z_BBN   = 4.0e8          # T ~ 0.08 MeV, deuterium formation
Z_REC   = 1089.92        # Planck 2018 (last scattering)
Z_DRAG  = 1059.94        # Planck 2018 (baryon drag), for the BAO standard ruler r_drag
THETA_S = 0.0104109      # Planck 2018 100 theta_* = 1.04109 +/- 0.00031  (0.030% precision)
OM_M    = 0.14304        # omega_m = Omega_m h^2, Planck 2018 (PHYSICAL; fixed at z >> z_t)
OM_B    = 0.02237        # omega_b, Planck 2018 / BBN deuterium
OM_G    = 2.4728e-5      # omega_gamma from T_cmb = 2.7255 K
OM_R    = OM_G*(1 + 0.2271*3.046)     # photons + massless neutrinos
H_FID   = 0.6736         # measured H0/100 (Planck); SH0ES 0.730 -- the gate brackets both
S8_FID  = 0.8111         # Planck 2018 sigma_8
BBN_TOL = 0.20           # conservative |G/G0 - 1| bound at nucleosynthesis (L5/L6 use the same)
CMB_TOL = 0.10           # conservative |G/G0 - 1| bound at recombination
Z_CLUST_MAX = 0.090      # highest redshift in the X-COP sample (A2142); the sample spans 0.047-0.090
H_LO, H_HI  = 0.60, 0.80 # allowed refitted H0/100 -- brackets Planck 0.674 and SH0ES 0.730 with margin
Q0_LO, Q0_HI = -0.75, -0.35
# RSD f*sigma_8 compilation (published; both models scored on the same points)
RSD = np.array([[0.02, 0.428, 0.0465],   # Huterer+2017   SNe peculiar velocities
                [0.15, 0.490, 0.145 ],   # Howlett+2015   SDSS MGS
                [0.38, 0.497, 0.045 ],   # Alam+2017      BOSS DR12
                [0.51, 0.459, 0.038 ],   # Alam+2017      BOSS DR12
                [0.70, 0.473, 0.041 ],   # Bautista+2021  eBOSS LRG
                [0.85, 0.315, 0.095 ],   # de Mattia+2021 eBOSS ELG
                [1.48, 0.462, 0.045 ]])  # Neveux+2020    eBOSS QSO
# BAO, in units of the drag-epoch sound horizon r_drag -- an ABSOLUTE distance ladder, unlike the SNe shape test,
# which marginalises over its zero point.  BOSS DR12 + eBOSS DR16 consensus + 6dFGS + SDSS MGS.  Correlations
# between D_M and D_H at the same redshift are ignored (diagonal errors); the gate is loosened to compensate.
BAO = [("DM", 0.380, 10.234, 0.151), ("DH", 0.380, 24.98, 0.58),      # BOSS DR12
       ("DM", 0.510, 13.366, 0.179), ("DH", 0.510, 22.31, 0.42),      # BOSS DR12
       ("DM", 0.700, 17.86,  0.33 ), ("DH", 0.700, 19.33, 0.53),      # eBOSS LRG
       ("DM", 1.480, 30.69,  0.80 ), ("DH", 1.480, 13.26, 0.55),      # eBOSS QSO
       ("DM", 2.330, 37.6,   1.9  ), ("DH", 2.330,  8.93, 0.28),      # eBOSS Lyman-alpha
       ("DV", 0.106,  2.976, 0.133), ("DV", 0.150,  4.47, 0.17 )]     # 6dFGS, SDSS MGS

# ---------------------------------------------------------------- F, from the committed audit
def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
A0 = CLJ["a0_m_s2"]
FREQ = {}
print("\n  the required late-time factor F, read from the committed cluster audit (not retyped):")
for foot in ("canonical", "alt"):
    a0 = A0[foot]; per = {}
    for rw in CLJ["rows"]:
        if rw.get("footing", "canonical") != foot: continue
        per.setdefault(rw["cluster"], []).append((float(rw["r_kpc"]), float(rw["g_baryon_over_a0"])*a0,
                                                  float(rw["g_hse_over_a0"])*a0))
    Eout, Eall, Nall = [], [], []
    for name, pts in per.items():
        p = np.array(sorted(pts)); gb, gh = p[:, 1], p[:, 2]
        E = gh/(gb + a0*Delta(gb/a0))
        Eout.append(E[-1]); Eall += list(E); Nall += list(gh/gb)
    FREQ[foot] = dict(F=float(np.median(Eout)), F_all=float(np.median(Eall)), F_newt=float(np.median(Nall)),
                      spread=(float(np.min(Eout)), float(np.max(Eout))))
    d = FREQ[foot]
    print(f"    {foot:9s} a0 = {a0:.4e}:  F = g_HSE/g_kernel at the OUTERMOST audited radius, median {d['F']:.3f} "
          f"[{d['spread'][0]:.2f}, {d['spread'][1]:.2f}] over 12 clusters")
    print(f"                              (all audited radii {d['F_all']:.2f};  purely Newtonian g_HSE/g_bar {d['F_newt']:.2f})")
print("    The OUTERMOST-radius value is used as the gate: it is the SMALLEST of the three and therefore the most")
print("    favourable to the model.  The other two are strictly harder and are priced where that matters.", flush=True)

# ---------------------------------------------------------------- the transition
def sigma_x(x, xt, W):
    """normalised roll: sigma(x = 0) = 1 exactly, sigma(x -> inf) = 0 exactly."""
    return (1.0 - np.tanh((x - xt)/W)) / (1.0 + np.tanh(xt/W))
def g_of_x(x, xt, W, F):
    return 1.0 + (F - 1.0)*sigma_x(x, xt, W)
def dlng_dlna(x, xt, W, F):
    """dln g/dln a.  x = ln(1+z) = -ln a, so d/dln a = -d/dx."""
    ch = np.cosh(np.clip((x - xt)/W, -300.0, 300.0))
    dsig = (1.0/(W*ch**2)) / (1.0 + np.tanh(xt/W))       # = -dsigma/dx
    return (F - 1.0)*dsig / g_of_x(x, xt, W, F)

# ---------------------------------------------------------------- background (vectorised over the grid)
def E2(x, oL, xt, W, F):
    """H^2/(100 km/s/Mpc)^2 for MODEL A.  Arguments broadcast."""
    a = np.exp(-x)
    return g_of_x(x, xt, W, F) * (OM_M*a**-3 + OM_R*a**-4 + oL)
def comoving(x_hi, oL, xt, W, F, n=1000):
    """comoving distance (Mpc) from z = 0 to ln(1+z) = x_hi; vectorised over parameter arrays."""
    xs = np.linspace(0.0, x_hi, n); X = xs[None, :]
    H = 100.0*np.sqrt(E2(X, np.atleast_1d(oL)[:, None], np.atleast_1d(xt)[:, None], np.atleast_1d(W)[:, None], F))
    return np.trapz(C_KMS*np.exp(X)/H, xs, axis=1)       # dz = (1+z) dx
def sound_horizon(oL, xt, W, F, n=1600, z_end=Z_REC):
    """r_s (Mpc): integral of c_s/H dz from z_end to z = 1e8.  z_end = Z_REC gives r_*, Z_DRAG gives r_drag."""
    xs = np.linspace(math.log(1 + z_end), math.log(1 + 1e8), n); X = xs[None, :]
    a = np.exp(-X); cs = C_KMS/np.sqrt(3.0*(1.0 + (3.0*OM_B/(4.0*OM_G))*a))
    H = 100.0*np.sqrt(E2(X, np.atleast_1d(oL)[:, None], np.atleast_1d(xt)[:, None], np.atleast_1d(W)[:, None], F))
    return np.trapz(cs*np.exp(X)/H, xs, axis=1)

def age_gyr(oL, xt, Wv, F, n=1200):
    """t0 = integral of da/(a H) from a = 0 to 1, in Gyr."""
    xs = np.linspace(0.0, math.log(1 + 3.0e4), n)          # x = ln(1+z); dt = -dx/H
    H = 100.0*np.sqrt(E2(xs[None, :], np.atleast_1d(oL)[:, None], np.atleast_1d(xt)[:, None],
                         np.atleast_1d(Wv)[:, None], F))   # km/s/Mpc
    return np.trapz(1.0/H, xs, axis=1)*(3.0856775814913673e19/(1e9*3.1557e7))

def bao_chi2(oL, xt, Wv, F):
    """chi^2 of the BAO distance ladder, in units of this model's OWN r_drag."""
    rd = sound_horizon(oL, xt, Wv, F, z_end=Z_DRAG); c2 = np.zeros(np.size(oL))
    for kind, z, val, err in BAO:
        x = math.log(1 + z)
        DM = comoving(x, oL, xt, Wv, F, n=400)
        DH = C_KMS/(100.0*np.sqrt(E2(x, oL, xt, Wv, F)))
        pred = {"DM": DM, "DH": DH, "DV": np.cbrt(z*DM*DM*DH)}[kind]/rd
        c2 += ((pred - val)/err)**2
    return c2

# ---------------------------------------------------------------- linear growth (vectorised RK4 in ln a)
def growth(oL, xt, W, F, modelA=True, a_i=1e-3, N=1200, want_curve=False):
    """d^2 delta/dln a^2 + (2 + dlnH/dln a) ddelta/dln a = S delta, with delta = a at a_i.
       Matter + Lambda background (see the NUMERICAL NOTE in the header)."""
    oL = np.atleast_1d(oL).astype(float); xt = np.atleast_1d(xt).astype(float); W = np.atleast_1d(W).astype(float)
    lo, hi = math.log(a_i), 0.0; h = (hi - lo)/N
    def deriv(la, y):
        d, dp = y; x = -la; a = math.exp(la)
        rm = OM_M*a**-3; br = rm + oL
        if modelA:                                        # g in BOTH Friedmann and Poisson: it cancels from S
            dlnH = 0.5*(dlng_dlna(x, xt, W, F) - 3.0*rm/br)
            S = 1.5*rm/br
        else:                                             # MODEL B: g in Poisson only, LambdaCDM background
            dlnH = 0.5*(-3.0*rm/br)
            S = 1.5*g_of_x(x, xt, W, F)*rm/br
        return np.array([dp, -(2.0 + dlnH)*dp + S*d])
    y = np.array([np.full_like(oL, a_i), np.full_like(oL, a_i)])
    curve = []
    for i in range(N):
        la = lo + i*h
        k1 = deriv(la, y); k2 = deriv(la + h/2, y + h/2*k1)
        k3 = deriv(la + h/2, y + h/2*k2); k4 = deriv(la + h, y + h*k3)
        y = y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        if want_curve: curve.append((lo + (i + 1)*h, y[0].copy(), y[1].copy()))
    return (y[0], y[1]/y[0], curve) if want_curve else (y[0], y[1]/y[0])
def fs8_chi2(curve, s8):
    """chi^2 of f*sigma_8 against RSD for every column of a growth curve."""
    la = np.array([c[0] for c in curve]); D = np.array([c[1] for c in curve]); f = np.array([c[2]/c[1] for c in curve])
    z = np.exp(-la) - 1.0
    pred = f*D/D[-1][None, :]*np.atleast_1d(s8)[None, :]
    chi2 = np.zeros(pred.shape[1])
    for k in range(RSD.shape[0]):
        row = np.array([np.interp(RSD[k, 0], z[::-1], pred[::-1, p]) for p in range(pred.shape[1])])
        chi2 += ((row - RSD[k, 1])/RSD[k, 2])**2
    return chi2

# ================================================================= T0 CONTROL
print("\n  T0 -- control: with g == 1 the machinery must return the standard cosmology.")
oL_fid = H_FID**2 - OM_M - OM_R
xt0 = np.array([math.log(2.0)]); W0 = np.array([0.3])
D_fid, f_fid, cur_fid = growth(np.array([oL_fid]), xt0, W0, 1.0, want_curve=True)
Dova = float(D_fid[0]); f0 = float(f_fid[0])
Om_f, OL_f = OM_M/H_FID**2, oL_fid/H_FID**2
CPT = 2.5*Om_f/(Om_f**(4/7) - OL_f + (1 + Om_f/2)*(1 + OL_f/70))
rs0 = float(sound_horizon(np.array([oL_fid]), xt0, W0, 1.0)[0])
DA0 = float(comoving(math.log(1 + Z_REC), np.array([oL_fid]), xt0, W0, 1.0)[0]); th0 = rs0/DA0
src = [1.5*(Ft*OM_M*0.5**-3)/(Ft*(OM_M*0.5**-3 + oL_fid)) for Ft in (1.0, 2.0, 5.0, 50.0)]
cancel = max(abs(s - src[0]) for s in src)
chi2_fid = float(fs8_chi2(cur_fid, np.array([S8_FID]))[0])
rd0 = float(sound_horizon(np.array([oL_fid]), xt0, W0, 1.0, z_end=Z_DRAG)[0])
t0_fid = float(age_gyr(np.array([oL_fid]), xt0, W0, 1.0)[0])
chi2_bao_fid = 0.0
chi2_bao_fid = float(bao_chi2(np.array([oL_fid]), xt0, W0, 1.0)[0])
print(f"    growth suppression D(a=1)/a = {Dova:.5f}   Carroll-Press-Turner {CPT:.5f}   ({100*abs(Dova/CPT-1):.2f}% apart)")
print(f"    growth rate f(z=0)          = {f0:.5f}   Omega_m^0.55 = {Om_f**0.55:.5f}         ({100*abs(f0/Om_f**0.55-1):.2f}% apart)")
print(f"    sound horizon r_s           = {rs0:.2f} Mpc (Planck 144.43)   comoving D_A(z*) = {DA0:.0f} Mpc (Planck 13872)")
print(f"    acoustic scale 100 theta_*  = {100*th0:.5f} (Planck 1.04109)    ({100*abs(th0/THETA_S-1):.2f}% apart)")
print(f"    drag-epoch sound horizon r_drag = {rd0:.2f} Mpc (Planck 147.09)   ({100*abs(rd0/147.09-1):.2f}% apart)")
print(f"    age of the universe t0      = {t0_fid:.3f} Gyr (Planck 13.797)      ({100*abs(t0_fid/13.797-1):.2f}% apart)")
print(f"    LambdaCDM chi^2: {chi2_fid:.2f} on the {len(RSD)} RSD f*sigma_8 points, "
      f"{chi2_bao_fid:.2f} on the {len(BAO)} BAO points")
print(f"    MODEL-A source cancellation 4 pi G_eff rho_m/H^2: varies by {cancel:.1e} as g runs 1 -> 50 (exact 0 predicted)")
TH_TARGET = th0     # the acoustic scale is compared DIFFERENTIALLY, against THIS code's own LambdaCDM value, so
                    # the 0.07% offset from Planck's absolute number (massless-neutrino approximation, z_* convention)
                    # cancels out of every model/LambdaCDM ratio instead of eating a quarter of the T4 tolerance.
ok0 = (abs(Dova/CPT - 1) < 0.01 and abs(f0/Om_f**0.55 - 1) < 0.03 and abs(th0/THETA_S - 1) < 0.01
       and abs(rs0/144.43 - 1) < 0.01 and cancel < 1e-14 and chi2_fid < 2*len(RSD)
       and abs(rd0/147.09 - 1) < 0.01 and chi2_bao_fid < 2*len(BAO) and abs(t0_fid/13.797 - 1) < 0.01)
# the h-refitter's own control is run below, once refit_h exists; the T0 verdict is issued there.

# ================================================================= the scan
NZT, NW = 81, 45
zt_ax = np.geomspace(1e-2, 3.0e3, NZT); W_ax = np.geomspace(2e-2, 5.0, NW)
ZT, WW = np.meshgrid(zt_ax, W_ax, indexing="ij")
ZTf, WWf = ZT.ravel(), WW.ravel(); xt = np.log(1 + ZTf); Wv = WWf; P = xt.size
ZSN = np.geomspace(0.01, 1.5, 40)
DL_FID = np.array([comoving(math.log(1 + z), np.array([oL_fid]), np.array([0.0]), np.array([1.0]), 1.0, n=600)[0]*(1 + z)
                   for z in ZSN])
def sne_rms(oL, F, xt, Wv, n=500):
    dmu = np.empty((np.size(oL), ZSN.size))
    for j, z in enumerate(ZSN):
        dmu[:, j] = 5*np.log10(comoving(math.log(1 + z), oL, xt, Wv, F, n=n)*(1 + z)/DL_FID[j])
    return np.sqrt(np.mean((dmu - dmu.mean(axis=1, keepdims=True))**2, axis=1))
def q0_of(oL, F, xt, Wv):
    return -1.0 - 0.5*(dlng_dlna(0.0, xt, Wv, F) + (-3*OM_M - 4*OM_R)/(OM_M + OM_R + oL))
def refit_h(F, rs, xt, Wv, n=600, iters=52):
    """BEST CASE for MODEL A: h floated so the acoustic scale matches the target EXACTLY.  theta_s = r_s/D_A is
       monotonically increasing in h (larger h -> larger omega_Lambda -> larger H at low z -> smaller D_A)."""
    n_p = xt.size
    lo = np.full(n_p, math.sqrt(F*(OM_M + OM_R))*(1 + 1e-9)); hi = np.full(n_p, 3.0)
    def th(h): return rs/comoving(math.log(1 + Z_REC), h*h/F - OM_M - OM_R, xt, Wv, F, n=n)
    ok = (th(lo) <= TH_TARGET) & (th(hi) >= TH_TARGET)
    for _ in range(iters):
        mid = 0.5*(lo + hi); m = th(mid) < TH_TARGET      # root is above mid
        lo = np.where(m, mid, lo); hi = np.where(m, hi, mid)
    return 0.5*(lo + hi), ok

def branch(tag, oL, hh, F, xt, Wv, rs):
    """everything that depends on ONE choice of background normalisation (a 'construction').
       oL and hh are per-model arrays; rs is the sound horizon (h-independent at fixed physical densities)."""
    b = {"tag": tag, "oL": oL, "h": hh}
    b["Om"] = np.where(hh > 0, OM_M/hh**2, np.nan); b["OL"] = np.where(hh > 0, oL/hh**2, np.nan)
    b["dtheta"] = rs/comoving(math.log(1 + Z_REC), oL, xt, Wv, F)/TH_TARGET - 1.0
    b["q0"] = q0_of(oL, F, xt, Wv)
    b["sne"] = sne_rms(oL, F, xt, Wv)
    b["dchi2_bao"] = bao_chi2(oL, xt, Wv, F) - chi2_bao_fid
    b["t0"] = age_gyr(oL, xt, Wv, F)
    D, f, cur = growth(oL, xt, Wv, F, modelA=True, want_curve=True)
    b["s8"] = S8_FID*D/D_fid[0]; b["dchi2"] = fs8_chi2(cur, b["s8"]) - chi2_fid; b["f0"] = f
    b["exp_ok"] = ((oL >= 0.0) & np.isfinite(hh) & (hh >= H_LO) & (hh <= H_HI)
                   & (np.abs(b["dtheta"]) <= 0.003) & (b["q0"] >= Q0_LO) & (b["q0"] <= Q0_HI) & (b["sne"] <= 0.10)
                   & (b["dchi2_bao"] <= 9.0))
    b["gro_ok"] = (np.abs(b["s8"]/S8_FID - 1) <= 0.10) & (b["dchi2"] <= 9.0)
    return b

def evaluate(F, xt, Wv):
    """all gates for MODEL A (three background constructions) and MODEL B, on the (z_t, W) arrays given."""
    o = {}; n_p = xt.size
    o["g_bbn"] = g_of_x(math.log(1 + Z_BBN), xt, Wv, F)
    o["g_rec"] = g_of_x(math.log(1 + Z_REC), xt, Wv, F)
    o["g_cl"]  = g_of_x(math.log(1 + Z_CLUST_MAX), xt, Wv, F)
    o["Omega_m_fid"] = OM_M/H_FID**2
    # the sound horizon: fixed physical densities and g = 1 before recombination, so it is essentially construction-blind
    oL_a = np.full(n_p, max(H_FID**2/F - OM_M - OM_R, 0.0))
    rs = sound_horizon(oL_a, xt, Wv, F); o["rs"] = rs
    # ---- (a) the measured H0 = 67.36, physical densities CMB-fixed, closure at a = 1 fixes Omega_Lambda
    o["ok_oL"] = (H_FID**2/F - OM_M - OM_R) >= 0.0
    A = branch("a", oL_a, np.full(n_p, H_FID), F, xt, Wv, rs)
    A["exp_ok"] &= o["ok_oL"]
    # ---- (b) BEST CASE: h refitted so the acoustic scale matches exactly
    hb, br_ok = refit_h(F, rs, xt, Wv)
    hb = np.where(br_ok, hb, np.nan)
    B = branch("b", np.maximum(np.nan_to_num(hb, nan=H_FID)**2/F - OM_M - OM_R, 0.0), hb, F, xt, Wv, rs)
    B["exp_ok"] &= br_ok
    # ---- (c) rho_Lambda held at its LambdaCDM value, H0 allowed to float
    C = branch("c", np.full(n_p, oL_fid), np.full(n_p, math.sqrt(F)*H_FID), F, xt, Wv, rs)
    o["br"] = {"a": A, "b": B, "c": C}
    # ---- MODEL B (perturbations only, exactly LambdaCDM background) -- reported separately, never mixed in
    DB, fB, curB = growth(np.full(n_p, oL_fid), xt, Wv, F, modelA=False, want_curve=True)
    o["s8_B"] = S8_FID*DB/D_fid[0]; o["dchi2_B"] = fs8_chi2(curB, o["s8_B"]) - chi2_fid
    # ---- gates.  T3 and T4 must be met by the SAME construction: a model may not buy its expansion history from
    #      one background normalisation and its growth from another.
    o["T1"] = np.abs(o["g_bbn"] - 1) <= BBN_TOL
    o["T2"] = np.abs(o["g_rec"] - 1) <= CMB_TOL
    o["T3"] = A["gro_ok"] | B["gro_ok"] | C["gro_ok"]
    o["T4"] = A["exp_ok"] | B["exp_ok"] | C["exp_ok"]
    o["T34"] = ((A["gro_ok"] & A["exp_ok"]) | (B["gro_ok"] & B["exp_ok"]) | (C["gro_ok"] & C["exp_ok"]))
    o["T5"] = o["g_cl"] >= 0.9*F
    o["T3_B"] = (np.abs(o["s8_B"]/S8_FID - 1) <= 0.10) & (o["dchi2_B"] <= 9.0)
    o["JOINT"] = o["T1"] & o["T2"] & o["T34"] & o["T5"]
    o["which"] = np.where(A["gro_ok"] & A["exp_ok"], "a", np.where(B["gro_ok"] & B["exp_ok"], "b",
                          np.where(C["gro_ok"] & C["exp_ok"], "c", "-")))
    return o

h_ctrl = float(refit_h(1.0, np.array([rs0]), xt0, W0)[0][0])
print(f"    the h-refitter, run at F = 1, returns h = {h_ctrl:.5f} against the input {H_FID:.5f} "
      f"({100*abs(h_ctrl/H_FID - 1):.3f}% apart)")
ok0 = ok0 and abs(h_ctrl/H_FID - 1) < 0.002
check("T0 [control] with g == 1 the growth integrator, the background code and the h-refitter reproduce the standard "
      "cosmology, and the Model-A source cancellation is exact",
      ok0, f"D/a within {100*abs(Dova/CPT-1):.2f}% of CPT, f(0) within {100*abs(f0/Om_f**0.55-1):.2f}% of Omega_m^0.55, "
           f"theta_* within {100*abs(th0/THETA_S-1):.2f}% of Planck, r_s within {100*abs(rs0/144.43-1):.2f}%, "
           f"r_drag within {100*abs(rd0/147.09-1):.2f}%, t0 within {100*abs(t0_fid/13.797-1):.2f}%, h-refit within {100*abs(h_ctrl/H_FID-1):.3f}%, "
           f"cancellation {cancel:.0e}, LambdaCDM chi^2 {chi2_fid:.1f}/{len(RSD)} RSD and "
           f"{chi2_bao_fid:.1f}/{len(BAO)} BAO")
print("    sigma_8 is NORMALISED, not predicted: every model is CMB-anchored at z = 999 with delta = a and reported as")
print("    sigma_8 = 0.8111 x D_model(1)/D_LCDM(1).  With g == 1 that ratio is 1 identically, so the control is exact.")
print("    The acoustic scale is compared DIFFERENTIALLY throughout (model / this code's own LambdaCDM), so the 0.07%")
print("    absolute offset from Planck cancels rather than eating a quarter of the T4 tolerance.", flush=True)

RES = {}
for foot in ("canonical", "alt"):
    F = FREQ[foot]["F"]; R = evaluate(F, xt, Wv); RES[foot] = R; A, B, C = (R["br"][k] for k in "abc")
    print(f"\n{'-'*124}\n  MODEL A, footing = {foot}:  F = {F:.3f}   grid = {NZT} z_t x {NW} widths = {P} models\n{'-'*124}")
    ceil = H_FID**2/(OM_M + OM_R)
    print(f"    THE ALGEBRAIC CEILING, before any dynamics.  Closure at a = 1 reads 1 = F(Omega_m + Omega_r + Omega_Lambda)")
    print(f"    with the physical densities fixed by the CMB, so at the measured H0, Omega_Lambda = 1/F - Omega_m - Omega_r >= 0")
    print(f"    forces F <= h^2/(omega_m + omega_r) = {ceil:.3f}.  This is a property of F ALONE: (z_t, W) cannot touch it.")
    print(f"      F = {F:5.2f} (outermost radius) -> Omega_Lambda = {A['OL'][0]:+.4f} (LambdaCDM 0.6847); matter is "
          f"{100*OM_M/(OM_M + OM_R + A['oL'][0]):.1f}% of the total energy density (LambdaCDM 31.5%)")
    for lab, Fx in (("all audited radii ", FREQ[foot]["F_all"]), ("purely Newtonian  ", FREQ[foot]["F_newt"])):
        v = 1/Fx - R["Omega_m_fid"] - OM_R/H_FID**2
        print(f"      F = {Fx:5.2f} ({lab})-> Omega_Lambda = {v:+.4f}" +
              ("   ALREADY EXCLUDED at the measured H0: no positive cosmological constant exists" if v < 0 else ""))
    print(f"\n    representative models (construction (a), the measured H0; 'which' names the construction, if any, that")
    print(f"    meets the growth AND expansion gates TOGETHER):")
    print(f"      {'z_t':>8s} {'W':>6s} | {'g(BBN)-1':>9s} {'g(z*)':>7s} {'g(.09)/F':>8s} | {'sigma_8':>7s} {'dchi2':>7s} | "
          f"{'dtheta_*':>9s} {'q0':>7s} {'SNe':>6s} | {'h_refit':>7s} | gates which")
    for ztv, Wv1 in ((0.05, 0.10), (0.15, 0.55), (0.3, 0.30), (0.42, 0.30), (1.0, 0.50), (3.0, 1.00), (30.0, 1.00), (1000.0, 2.00)):
        i = int(np.argmin((np.log(ZTf/ztv))**2 + (np.log(WWf/Wv1))**2))
        gates = "".join(t[-1] if R[t][i] else "." for t in ("T1", "T2", "T3", "T4", "T5"))
        hf = B["h"][i]
        print(f"      {ZTf[i]:8.3g} {WWf[i]:6.3g} | {R['g_bbn'][i]-1:9.2e} {R['g_rec'][i]:7.3f} {R['g_cl'][i]/F:8.3f} | "
              f"{A['s8'][i]:7.4f} {A['dchi2'][i]:+7.1f} | {100*A['dtheta'][i]:+8.2f}% {A['q0'][i]:+7.3f} "
              f"{A['sne'][i]:6.3f} | {('%7.4f' % hf) if np.isfinite(hf) else '   none'} |  {gates}  {R['which'][i]}")
    print(f"      (the 'gates' column shows each gate INDIVIDUALLY; 'which' names the construction meeting the growth AND")
    print(f"       expansion gates TOGETHER, and '-' means no single construction does both -- so '12345' in the gates")
    print(f"       column does NOT by itself make a T6 survivor.)", flush=True)

# ================================================================= T1..T5, each gate alone
print(f"\n{'='*124}\n  the gates, each asked ALONE: is there ANY (z_t, W) on the grid that satisfies it?\n{'='*124}", flush=True)
def cnt(k): return {f: int(RES[f][k].sum()) for f in RES}
n1, n2, n3, n4, n5 = (cnt(k) for k in ("T1", "T2", "T3", "T4", "T5"))
check("T1 [BBN] some (z_t, W) has G_eff = G_0 at nucleosynthesis within the conservative 20% bound",
      all(v > 0 for v in n1.values()),
      ", ".join(f"{f}: {n1[f]}/{P}, best |g-1| = {np.abs(RES[f]['g_bbn']-1).min():.1e}" for f in n1)
      + "  -- passes BY CONSTRUCTION, as the header says; stated explicitly so the construction is honest.  This is "
        "exactly the L6 horn the roll was invoked to escape, and the roll does escape it")
check("T2 [CMB] some (z_t, W) has G_eff = G_0 at recombination within 10%, so the microwave background does not see it",
      all(v > 0 for v in n2.values()),
      ", ".join(f"{f}: {n2[f]}/{P}" for f in n2)
      + f"; the transition must be over by z_t <~ {ZTf[RES['canonical']['T2']].max():.0f} even for the widest roll on the "
        f"grid, and the sound-horizon shift across the passing set is at most "
        f"{100*np.abs(RES['canonical']['rs'][RES['canonical']['T2']]/rs0 - 1).max():.2f}%")
check("T3 [growth] some (z_t, W) keeps sigma_8 within 10% of 0.8111 and the RSD f*sigma_8 within Delta chi^2 <= 9, on "
      "at least one background construction",
      all(v > 0 for v in n3.values()),
      ", ".join(f"{f}: {n3[f]}/{P}, best Delta chi^2_RSD over all constructions "
                f"{min(RES[f]['br'][k]['dchi2'].min() for k in 'abc'):+.2f}" for f in n3))
check("T4 [expansion] some (z_t, W) keeps the expansion history on at least one background construction "
      "(measured H0; h refitted to the acoustic scale; or rho_Lambda held)",
      all(v > 0 for v in n4.values()),
      ", ".join(f"{f}: {n4[f]}/{P} (a: {int(RES[f]['br']['a']['exp_ok'].sum())}, "
                f"b: {int(RES[f]['br']['b']['exp_ok'].sum())}, c: {int(RES[f]['br']['c']['exp_ok'].sum())})" for f in n4))
check("T5 [delivers] some (z_t, W) actually delivers 90% of the enhancement at the highest X-COP redshift z = 0.090",
      all(v > 0 for v in n5.values()), ", ".join(f"{f}: {n5[f]}/{P}" for f in n5))

# ---------------------------------------------------------------- the two hard gates in detail
Rc = RES["canonical"]; Fc = FREQ["canonical"]["F"]; Ac, Bc, Cc = (Rc["br"][k] for k in "abc")
print(f"\n  T3 and T4 in detail (canonical footing, F = {Fc:.3f}).")
print(f"    GROWTH.  The g-cancellation in the source is exact, so the boost does NOT drive growth directly.  What moves")
print(f"    growth is the background normalisation the closure forces, and the two consistent normalisations push it in")
print(f"    OPPOSITE directions -- so growth alone does not uniquely kill the model, and both readings are reported:")
print(f"      (a) measured H0, Omega_Lambda forced to {Ac['OL'][0]:.3f} : sigma_8 in [{Ac['s8'].min():.3f}, {Ac['s8'].max():.3f}] "
      f"-- ENHANCED (the universe is {100*OM_M/(OM_M+OM_R+Ac['oL'][0]):.0f}% matter, so rho_m/rho_tot is larger)")
print(f"      (b) h refitted to the acoustic scale                : sigma_8 in "
      f"[{np.nanmin(Bc['s8']):.3f}, {np.nanmax(Bc['s8']):.3f}]")
print(f"      (c) rho_Lambda held, H0 floats                      : sigma_8 in [{Cc['s8'].min():.3f}, {Cc['s8'].max():.3f}] "
      f"-- SUPPRESSED (the source is LambdaCDM's exactly, so only the extra friction (1/2) dln g/dln a acts)")
print(f"      best RSD Delta chi^2 over every (z_t, W) and every construction: "
      f"{min(Rc['br'][k]['dchi2'].min() for k in 'abc'):+.2f} on {len(RSD)} f*sigma_8 points (gate <= +9.00)")
print(f"    EXPANSION.  At the measured H0, Omega_Lambda = 1/F - Omega_m - Omega_r = {Ac['OL'][0]:.4f} is")
print(f"    (z_t, W)-INDEPENDENT: g(a = 1) = F is fixed by the clusters, and closure at a = 1 does not know when the roll")
print(f"    happened.  The transition parameters cannot buy it back.  The three constructions, all offered to the model:")
print(f"      (a) H0 = 67.36 fixed, densities CMB-fixed : Omega_Lambda = {Ac['OL'][0]:.4f} (measured 0.685); "
      f"d(theta_*) {100*Ac['dtheta'].min():+.2f}% to {100*Ac['dtheta'].max():+.2f}% (gate 0.30%, Planck 0.030%); "
      f"BAO Delta chi^2 {Ac['dchi2_bao'].min():+.1f} to {Ac['dchi2_bao'].max():+.1f};")
print(f"          q0 {Ac['q0'].min():+.3f} to {Ac['q0'].max():+.3f} (SNe -0.55 +/- 0.10); SNe rms "
      f"{Ac['sne'].min():.3f}-{Ac['sne'].max():.3f} mag -- {int(Ac['exp_ok'].sum())}/{P} pass")
_f = np.isfinite(Bc["h"])
print(f"      (b) h refitted, acoustic scale exact      : H0 = {100*np.nanmin(Bc['h']):.1f}-{100*np.nanmax(Bc['h']):.1f} "
      f"km/s/Mpc where a root exists ({int((~_f).sum())}/{P} have NO root at any h: the acoustic scale is unreachable);")
print(f"          there Omega_m = {np.nanmin(Bc['Om']):.3f}-{np.nanmax(Bc['Om']):.3f} and Omega_Lambda = "
      f"{np.nanmin(Bc['OL']):.3f}-{np.nanmax(Bc['OL']):.3f} (measured 0.315, 0.685), BAO Delta chi^2 "
      f"{np.nanmin(Bc['dchi2_bao']):+.1f} to {np.nanmax(Bc['dchi2_bao']):+.1f} -- {int(Bc['exp_ok'].sum())}/{P} pass")
print(f"      (c) rho_Lambda held, H0 floats            : H0 = sqrt(F) x 67.36 = {100*Cc['h'][0]:.1f} km/s/Mpc, against "
      f"67.4-73.0 measured -- {int(Cc['exp_ok'].sum())}/{P} pass")
print(f"      the gate allows the whole band H0 = 60-80 km/s/Mpc, which brackets Planck and SH0ES with margin.")
print(f"    NOT GATED, reported because it is real and adverse: a rolling G also drifts the type-Ia absolute magnitude,")
print(f"    M_B propto -(15/4) log10 G through the Chandrasekhar mass -- {3.75*math.log10(Fc):.2f} mag across the transition,")
print(f"    against a ~0.03 mag systematic floor.  Including it makes T4 strictly worse; it is left out to keep the gate")
print(f"    favourable to the model.  Likewise the SNe check marginalises over an absolute offset, which is favourable.", flush=True)

# ================================================================= T6 verdict
print(f"\n{'='*124}\n  T6 -- the verdict: is there ANY (z_t, W) that passes every gate at once?\n{'='*124}", flush=True)
def margins(F, zf, wf, RR, k, tag):
    br = RR["br"]; who = RR["which"][k]
    print(f"        SURVIVING REGION: z_t in [{zf[k].min():.4g}, {zf[k].max():.4g}], W in [{wf[k].min():.4g}, {wf[k].max():.4g}]"
          f"   ({100*k.size/zf.size:.2f}% of the {tag} box); it survives on construction(s) "
          f"{sorted(set(who.tolist()))}")
    for c in sorted(set(who.tolist())):
        j = k[who == c]; b = br[c]
        print(f"        --- construction ({c}), {j.size} models -- each margin against its OWN gate and against the raw "
              f"measurement precision:")
        print(f"            H0            {100*np.nanmin(b['h'][j]):7.2f}-{100*np.nanmax(b['h'][j]):.2f} km/s/Mpc     "
              f"gate 60-80        measured 67.4 (Planck) / 73.0 (SH0ES)")
        print(f"            Omega_Lambda  {np.nanmin(b['OL'][j]):7.3f}-{np.nanmax(b['OL'][j]):.3f}               "
              f"not gated         measured 0.685   (Omega_m {np.nanmin(b['Om'][j]):.3f}-{np.nanmax(b['Om'][j]):.3f} vs 0.315)")
        print(f"            |dtheta_*|    {100*np.abs(b['dtheta'][j]).min():7.3f}-{100*np.abs(b['dtheta'][j]).max():.3f}%              "
              f"gate 0.300%       Planck 0.030% => "
              f"{np.abs(b['dtheta'][j]).min()/3e-4:.0f}-{np.abs(b['dtheta'][j]).max()/3e-4:.0f} sigma on the raw number")
        print(f"            q0            {b['q0'][j].min():+7.3f} to {b['q0'][j].max():+.3f}            "
              f"gate [{Q0_LO}, {Q0_HI}]  SNe -0.55 +/- 0.10 => "
              f"{min(abs(b['q0'][j]+0.55))/0.10:.1f}-{max(abs(b['q0'][j]+0.55))/0.10:.1f} sigma")
        print(f"            SNe rms       {b['sne'][j].min():7.3f}-{b['sne'][j].max():.3f} mag          "
              f"gate 0.100        Pantheon+ shape systematics ~0.03 mag")
        print(f"            sigma_8       {b['s8'][j].min():7.3f}-{b['s8'][j].max():.3f}               "
              f"gate +/-10%       Planck 0.8111 +/- 0.0060 => "
              f"{abs(b['s8'][j].min()-S8_FID)/0.006:.0f}-{abs(b['s8'][j].max()-S8_FID)/0.006:.0f} sigma")
        print(f"            BAO dchi2     {b['dchi2_bao'][j].min():+7.2f} to {b['dchi2_bao'][j].max():+.2f}            "
              f"gate <= +9.00     ({len(BAO)} points, ABSOLUTE in units of r_drag)")
        print(f"            RSD dchi2     {b['dchi2'][j].min():+7.2f} to {b['dchi2'][j].max():+.2f}            "
              f"gate <= +9.00     ({len(RSD)} f*sigma_8 points)")
        print(f"            g(0.09)/F     {RR['g_cl'][j].min()/F:7.3f}-{RR['g_cl'][j].max()/F:.3f}               "
              f"gate >= 0.900     the enhancement actually delivered at the cluster redshifts")
        print(f"            age t0        {b['t0'][j].min():7.2f}-{b['t0'][j].max():.2f} Gyr        "
              f"NOT GATED         Planck 13.80; oldest globulars ~13.0 +/- 0.4 Gyr")
        print(f"            f(z=0)        {b['f0'][j].min():7.3f}-{b['f0'][j].max():.3f}               "
              f"NOT GATED         LambdaCDM 0.527")

JOINT = {}; REFINED = {}
for f in RES:
    R = RES[f]; F = FREQ[f]["F"]; JOINT[f] = R["JOINT"]; n = int(JOINT[f].sum())
    base = R["T1"] & R["T2"] & R["T5"]
    print(f"    {f:9s} F = {F:.3f}:  {n}/{P} models pass all five")
    print(f"      of the {int(base.sum())} passing BBN + CMB + delivery, {int((base & R['T3']).sum())} also pass growth, "
          f"{int((base & R['T4']).sum())} also pass the expansion history, and {n} pass BOTH ON THE SAME CONSTRUCTION")
    if R["T4"].any():
        print(f"      what does the narrowing: the EXPANSION gate confines z_t to "
              f"[{ZTf[R['T4']].min():.4g}, {ZTf[R['T4']].max():.4g}] and W to "
              f"[{WWf[R['T4']].min():.4g}, {WWf[R['T4']].max():.4g}] -- the roll must still be finishing recently enough")
        print(f"      that its own dln g/dln a term in H(z) stands in for the dark energy the closure took away.  The")
        print(f"      growth gate is broad on its own ({int(R['T3'].sum())}/{P}); it is the requirement that ONE construction meet")
        print(f"      BOTH that cuts {int(R['T4'].sum())} down to {n}.")
    if not n:
        REFINED[f] = None; continue
    i = np.where(JOINT[f])[0]
    print(f"      SURVIVING CELLS on the coarse grid: z_t in [{ZTf[i].min():.4g}, {ZTf[i].max():.4g}], "
          f"W in [{WWf[i].min():.4g}, {WWf[i].max():.4g}]  ({n} of {P})")
    zlo, zhi = ZTf[i].min()/3.0, ZTf[i].max()*3.0; wlo, whi = WWf[i].min()/3.0, WWf[i].max()*3.0
    rz = np.geomspace(zlo, zhi, 61); rw = np.geomspace(wlo, whi, 61)
    RZ, RW = np.meshgrid(rz, rw, indexing="ij"); rzf, rwf = RZ.ravel(), RW.ravel()
    RR = evaluate(F, np.log(1 + rzf), rwf); m = RR["JOINT"]; REFINED[f] = (rzf, rwf, RR)
    print(f"      REFINED scan, {rz.size} x {rw.size} = {rzf.size} models over z_t in [{zlo:.3g}, {zhi:.3g}], "
          f"W in [{wlo:.3g}, {whi:.3g}]: {int(m.sum())} survive")
    if m.any():
        k = np.where(m)[0]; margins(F, rzf, rwf, RR, k, "refined")
        for c in sorted(set(RR["which"][k].tolist())):
            b = RR["br"][c]; strict = m & (np.abs(b["dtheta"]) <= 3e-4)
            print(f"        if the acoustic-scale tolerance on construction ({c}) is set to Planck's ACTUAL precision")
            print(f"        (0.030% rather than the 0.300% this gate allows), the surviving count goes "
                  f"{int(m.sum())} -> {int((m & strict).sum())}.")
    else:
        print(f"        the coarse-grid survivor does NOT survive refinement: a cell on a tolerance corner, not a region.")
check("T6 [verdict] a late-time transition in G_eff, entering the Friedmann and Poisson equations as any scalar-tensor "
      "completion requires, supplies the cluster residual AND survives BBN, the CMB, growth and the expansion history "
      "on the SAME background construction, on BOTH a0 footings",
      all(int(JOINT[f].sum()) > 0 and REFINED[f] is not None and bool(REFINED[f][2]["JOINT"].any()) for f in JOINT),
      ", ".join(f"{f}: {int(JOINT[f].sum())}/{P} coarse"
                + (f", {int(REFINED[f][2]['JOINT'].sum())}/{REFINED[f][2]['JOINT'].size} refined"
                   if REFINED[f] is not None else "") for f in JOINT))

# ================================================================= T7 fork: model B
print(f"\n{'='*124}\n  T7 -- the fork (requirement 5): MODEL B, the enhancement in the PERTURBATIONS ONLY\n{'='*124}")
print("    MODEL B is a strictly WEAKER and DIFFERENT model, labelled as such wherever it appears.  The background")
print("    expansion is held exactly LambdaCDM while the Poisson source is multiplied by g(a).  That is the")
print("    phenomenological mu(a) parametrisation, not a completion: no action is supplied for it here, and the")
print("    background gravitational effect of the rolling field has to be cancelled by hand.  It evades BBN and the")
print("    expansion history BY CONSTRUCTION rather than by passing them, so only CMB, growth and delivery have content.")
JB = {}
for f in RES:
    R = RES[f]; JB[f] = R["T2"] & R["T3_B"] & R["T5"]; n = int(JB[f].sum())
    print(f"    {f:9s} F = {FREQ[f]['F']:.3f}: sigma_8 spans [{R['s8_B'].min():.3f}, {R['s8_B'].max():.3f}] "
          f"(LambdaCDM 0.8111); {n}/{P} models pass CMB + growth + delivery")
    if n:
        i = np.where(JB[f])[0]
        print(f"      SURVIVING REGION (MODEL B): z_t in [{ZTf[i].min():.4g}, {ZTf[i].max():.4g}], "
              f"W in [{WWf[i].min():.4g}, {WWf[i].max():.4g}]; there sigma_8 in "
              f"[{R['s8_B'][i].min():.3f}, {R['s8_B'][i].max():.3f}], Delta chi^2_RSD in "
              f"[{R['dchi2_B'][i].min():+.1f}, {R['dchi2_B'][i].max():+.1f}]")
check("T7 [fork B] the weaker perturbation-only model survives its applicable gates (CMB, growth, delivery at the "
      "cluster redshifts)", all(int(JB[f].sum()) > 0 for f in JB), ", ".join(f"{f}: {int(JB[f].sum())}/{P}" for f in JB))
print("\n  what MODEL B still owes -- stated rather than closed; it is NOT claimed here to be a live mechanism:")
print("    (i)   no action.  A G that gravitates perturbations but not the background is not a scalar-tensor theory; the")
print("          Bianchi identity ties the two and the cancellation must be inserted by hand.  L6's ordering argument was")
print("          defeated here only by the ROLL, and the roll is a BACKGROUND statement.  MODEL B keeps the roll's evasion")
print("          while discarding the roll's background cost, which is exactly why it survives -- and why that survival")
print("          should not be read as a result until an action produces it.")
print("    (ii)  lensing versus dynamics.  MODEL B enhances the dynamical potential by F at cluster outskirts.  If the")
print("          lensing potential is enhanced equally it is a pure G rescaling and inherits every background constraint")
print("          above; if it is not, cluster lensing and hydrostatic masses must disagree by of order F, and they are")
print("          observed to agree to tens of percent.  That gate is not run here.")
print("    (iii) galaxies.  A time-only g(z) is spatially uniform, so MODEL B still needs the SAME screening L6 excluded")
print("          in order to keep galaxies at G_0.  The roll relaxes only L6's BBN-ordering horn, never its OVERLAP horn")
print("          (clusters and galaxies at identical baryon density requiring enhancements 12.8 sigma apart).  MODEL B")
print("          therefore inherits L6's overlap kill unchanged.")
print("    Two further doors this script does NOT close, stated: a NON-MONOTONE g(z), which is a fitted history rather")
print("    than a roll; and a rolling coupling that is not a rescaling of G but an extra clustering component, which is")
print("    dark matter and is closed elsewhere in the programme, not here.")

# ================================================================= growth-gate sensitivity
print(f"\n{'='*124}\n  how robust is the T6 verdict?  the surviving region is set by the GROWTH gate, so vary it and report\n{'='*124}")
print("    The gate as preregistered is Delta chi^2_RSD <= 9 (3 sigma).  Neither loosening nor tightening it is done to")
print("    reach a preferred answer; both are shown so the reader can see where the boundary is.")
print(f"      {'growth gate':>28s} | " + " | ".join(f"{f:>28s}" for f in RES))
for lab, thr in (("Delta chi^2_RSD <= 4  (2 sigma)", 4.0), ("Delta chi^2_RSD <= 9  (3 sigma, THE GATE)", 9.0),
                 ("Delta chi^2_RSD <= 16 (4 sigma)", 16.0), ("Delta chi^2_RSD <= 25 (5 sigma)", 25.0)):
    row = []
    for f in RES:
        R = RES[f]
        g34 = np.zeros(P, bool)
        for c in "abc":
            b = R["br"][c]
            g34 |= (np.abs(b["s8"]/S8_FID - 1) <= 0.10) & (b["dchi2"] <= thr) & b["exp_ok"]
        m = R["T1"] & R["T2"] & R["T5"] & g34
        row.append(f"{int(m.sum()):5d}/{P} of the coarse grid")
    print(f"      {lab:>28s} | " + " | ".join(f"{r:>28s}" for r in row))
print("    The surviving models sit AT the top of the growth gate on every footing, so the T6 PASS is a boundary result,")
print("    not a comfortable one -- and it is reported as a PASS because the gate was fixed before the scan, not after.")

# ================================================================= T8: what the roll does NOT buy
print(f"\n{'='*124}\n  T8 -- the gate this lane's escape was never going to help with, asked and quantified\n{'='*124}")
print("    L6 killed the screened force on TWO independent horns.  The roll was invoked against the first (the")
print("    cosmological ordering: the background must be at least as unscreened as cluster outskirts, forcing")
print("    G_cosmo/G_local >= 1.82 at BBN), and against that horn it works -- T1 passes exactly and by construction.")
print("    The SECOND horn is untouched by any cosmological history: clusters and SPARC galaxies OVERLAP COMPLETELY in")
print("    baryon density yet require enhancements differing at 12.8 sigma, and at the same acceleration clusters need")
print("    2.2-5.1x the boost galaxies are measured to have (L2, L6 -- this lane's own committed results).  That is a")
print("    SPATIAL contrast between two populations observed at essentially the SAME EPOCH.  A g(z) is spatially")
print("    uniform, so the only contrast it can supply between them is the difference in their redshifts.")
D_SP = []
for ln in open(os.path.join(REPO, "real_research/data/SPARC_Lelli2016c.mrt")).read().split("\n")[98:]:
    fl = ln.split()                                        # Galaxy, T, D[Mpc], e_D, ...
    if len(fl) > 3:
        try:
            d = float(fl[2])
            if d > 0: D_SP.append(d)
        except ValueError: pass
D_SP = np.array(D_SP)
assert D_SP.size > 100, f"SPARC distance parse failed ({D_SP.size} rows)"
z_gal = float(np.median(D_SP))*(H_FID*100.0)/C_KMS; z_gal_hi = float(D_SP.max())*(H_FID*100.0)/C_KMS
src = (f"{D_SP.size} galaxies, distances {D_SP.min():.2f}-{D_SP.max():.1f} Mpc, median {np.median(D_SP):.1f} Mpc "
       f"(Hubble flow at h = {H_FID})")
print(f"    SPARC's own redshifts, from the committed catalogue: {src}")
print(f"      => z_gal = {z_gal:.5f} (median), {z_gal_hi:.4f} (most distant); clusters z = 0.047-{Z_CLUST_MAX:.3f}")
REQ_LO, REQ_HI = 2.2, 5.1                                                 # L2/L6: the cluster-over-galaxy boost ratio
roll = {}
for f in RES:
    F = FREQ[f]["F"]
    if REFINED[f] is not None and REFINED[f][2]["JOINT"].any():
        rzf, rwf, RR = REFINED[f]; k = np.where(RR["JOINT"])[0]
        xtk, Wk = np.log(1 + rzf[k]), rwf[k]; tag = "the T6-surviving models"
    else:
        xtk, Wk = xt, Wv; tag = "the whole grid (no T6 survivor)"
    r = g_of_x(math.log(1 + Z_CLUST_MAX), xtk, Wk, F)/g_of_x(math.log(1 + z_gal), xtk, Wk, F)
    roll[f] = (float(r.min()), float(r.max()))
    print(f"    {f:9s}: over {tag}, the roll gives clusters g(z_cl)/g(z_gal) = "
          f"{r.min():.4f}-{r.max():.4f} relative to galaxies")
best = max(v[1] for v in roll.values())
print(f"    The requirement is {REQ_LO}-{REQ_HI}.  The roll supplies at most {best:.4f} -- and because g DECREASES with")
print(f"    redshift while clusters sit at HIGHER redshift than the galaxies, the sign is WRONG: the roll makes clusters")
print(f"    slightly LESS enhanced than galaxies, not more.  It is short by a factor of {REQ_LO/best:.1f}-{REQ_HI/best:.1f}.")
check("T8 [inherited] the roll ALSO supplies the cluster-versus-galaxy contrast, so the spatial screening L6 excluded on "
      "its overlap horn is no longer needed",
      best >= REQ_LO, f"it supplies {best:.4f} against a required {REQ_LO}-{REQ_HI}, in the wrong direction; the two "
                      f"populations are observed {z_gal:.4f} < z < {Z_CLUST_MAX:.3f} apart and no g(z) can separate them. "
                      f"So a T6 PASS clears the COSMOLOGICAL gates only: the model still needs exactly the density-screening "
                      f"L6 excluded at 12.8 sigma, which the roll never addressed")

# ================================================================= parameter-space summary
print(f"\n  SUMMARY OF THE PARAMETER SPACE (canonical footing, F = {Fc:.3f}, {P} models scanned):")
for lab, m in (("BBN alone", Rc["T1"]), ("CMB alone", Rc["T2"]), ("growth alone", Rc["T3"]),
               ("expansion alone", Rc["T4"]), ("delivery alone", Rc["T5"]),
               ("growth+exp, same constr.", Rc["T34"]),
               ("BBN+CMB+delivery", Rc["T1"] & Rc["T2"] & Rc["T5"]),
               ("ALL FIVE (MODEL A)", JOINT["canonical"]), ("MODEL B, its own gates", JB["canonical"])):
    i = np.where(m)[0]
    if i.size: print(f"    {lab:24s}: {i.size:5d}/{P}   z_t in [{ZTf[i].min():.4g}, {ZTf[i].max():.4g}], "
                     f"W in [{WWf[i].min():.4g}, {WWf[i].max():.4g}]")
    else:      print(f"    {lab:24s}: {i.size:5d}/{P}   EMPTY")
print(f"\n{'='*124}\n  THE VERDICT OF THIS LANE, as the pair (T6, T8)\n{'='*124}")
print("  T6 PASSES.  The roll does what L6 said it might: because g(z_BBN) = 1 exactly while g(0) = F, the")
print("  cosmological-ordering horn that closed the screened force is genuinely evaded, and a narrow region of")
print("  (z_t, W) then survives BBN, the CMB, the growth of structure, the expansion history -- acoustic scale, q0,")
print("  the SNe distance-modulus shape and the absolute BAO ladder -- and still delivers the enhancement at the")
print("  redshifts where the clusters are measured.  It survives on ONE construction, (b): h refitted so the acoustic")
print("  scale matches exactly, giving H0 near 68-72 km/s/Mpc with Omega_Lambda near 0.25-0.32.  What makes that")
print("  possible is that the roll's own dln g/dln a term in H(z) partly MIMICS dark energy, so a universe that is")
print("  about half matter by energy density can still reproduce the observed distances.  This is the first mechanism")
print("  in this programme to reach the cluster residual without being excluded by the gate it was proposed against.")
print("  It is a BOUNDARY result and is reported as one: every survivor sits at the top of the growth gate (best RSD")
print("  Delta chi^2 +5.3 canonical, +3.1 alt, against a gate of +9), with sigma_8 = 0.85-0.86 and f(0) = 0.57-0.64")
print("  against LambdaCDM's 0.527.  Tightening the growth gate from 3 sigma to 2 sigma empties the canonical footing")
print("  entirely and leaves 3 models of 3645 on the alt one.")
print()
print("  T8 FAILS, and it is the decisive half.  L6 closed the screened force on TWO horns and the roll addresses only")
print("  one.  The other is that clusters and galaxies overlap completely in baryon density while requiring")
print("  enhancements 12.8 sigma apart -- a SPATIAL contrast between populations observed at z = 0.004 and z = 0.09.")
print("  A spatially uniform g(z) supplies a factor 0.93-0.97 between those epochs, in the WRONG direction, against a")
print("  required 2.2-5.1.  So the late-time transition buys the cosmology and not the mechanism: it still needs the")
print("  density-dependent screening that L6 excluded, and it does not weaken that exclusion by anything.")
print()
print("  Stated as an open door rather than a closure: the surviving cosmology is a real object worth naming.  A model")
print("  with G_cosmo/G_local rolling to about 1.7-1.8 since z ~ 0.1-0.4 is not cosmologically excluded on these gates,")
print("  and it predicts sigma_8 = 0.85-0.86 with H0 = 68-72 -- a sharp, falsifiable pair that current RSD already")
print("  strains and the next generation of growth measurements will settle.  What it does NOT do is explain clusters.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
