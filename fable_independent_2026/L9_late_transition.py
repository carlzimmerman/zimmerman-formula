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
  T4 [expansion] some (z_t, W) keeps the expansion history.  Two constructions, either may
                pass: (a) at the measured H0 = 67.36 with CMB-fixed physical densities --
                Omega_Lambda >= 0, acoustic scale within 0.3% (10x looser than Planck's
                0.030%), q0 in [-0.75, -0.35], SNe distance-modulus shape within 0.10 mag rms
                (3x looser than Pantheon+ systematics); or (b) the BEST CASE, h refitted to
                match Planck's acoustic scale EXACTLY, landing in H0 = 60-80 km/s/Mpc with
                the same q0 and SNe conditions;
  T5 [delivers] some (z_t, W) actually DELIVERS the enhancement where the clusters are
                measured: g(z = 0.090) >= 0.9 F at the highest X-COP redshift;
  T6 [verdict]  some (z_t, W) passes T1 AND T2 AND T3 AND T4 AND T5 simultaneously, on BOTH
                a0 footings.  This is the question the lane exists to answer;
  T7 [fork B]   the weaker perturbation-only model survives ITS applicable gates.
FAIL marks a requirement the stated model does not meet.  Both a0 footings throughout: the
required factor F depends on the footing because the framework's kernel does.

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
Z_REC   = 1089.92        # Planck 2018
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
def sound_horizon(oL, xt, W, F, n=1600):
    """r_s (Mpc): integral of c_s/H dz from z_rec to z = 1e8."""
    xs = np.linspace(math.log(1 + Z_REC), math.log(1 + 1e8), n); X = xs[None, :]
    a = np.exp(-X); cs = C_KMS/np.sqrt(3.0*(1.0 + (3.0*OM_B/(4.0*OM_G))*a))
    H = 100.0*np.sqrt(E2(X, np.atleast_1d(oL)[:, None], np.atleast_1d(xt)[:, None], np.atleast_1d(W)[:, None], F))
    return np.trapz(cs*np.exp(X)/H, xs, axis=1)

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
def fs8_chi2(curve, s8, zref):
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
chi2_fid = float(fs8_chi2(cur_fid, np.array([S8_FID]), None)[0])
print(f"    growth suppression D(a=1)/a = {Dova:.5f}   Carroll-Press-Turner {CPT:.5f}   ({100*abs(Dova/CPT-1):.2f}% apart)")
print(f"    growth rate f(z=0)          = {f0:.5f}   Omega_m^0.55 = {Om_f**0.55:.5f}         ({100*abs(f0/Om_f**0.55-1):.2f}% apart)")
print(f"    sound horizon r_s           = {rs0:.2f} Mpc (Planck 144.43)   comoving D_A(z*) = {DA0:.0f} Mpc (Planck 13872)")
print(f"    acoustic scale 100 theta_*  = {100*th0:.5f} (Planck 1.04109)    ({100*abs(th0/THETA_S-1):.2f}% apart)")
print(f"    LambdaCDM chi^2 on the {len(RSD)} RSD f*sigma_8 points: {chi2_fid:.2f}")
print(f"    MODEL-A source cancellation 4 pi G_eff rho_m/H^2: varies by {cancel:.1e} as g runs 1 -> 50 (exact 0 predicted)")
ok0 = (abs(Dova/CPT - 1) < 0.01 and abs(f0/Om_f**0.55 - 1) < 0.03 and abs(th0/THETA_S - 1) < 0.01
       and abs(rs0/144.43 - 1) < 0.01 and cancel < 1e-14 and chi2_fid < 2*len(RSD))
check("T0 [control] with g == 1 the growth integrator and background code reproduce the standard cosmology, and the "
      "Model-A source cancellation is exact",
      ok0, f"D/a within {100*abs(Dova/CPT-1):.2f}% of CPT, f(0) within {100*abs(f0/Om_f**0.55-1):.2f}% of Omega_m^0.55, "
           f"theta_* within {100*abs(th0/THETA_S-1):.2f}%, r_s within {100*abs(rs0/144.43-1):.2f}%, "
           f"cancellation {cancel:.0e}, LambdaCDM RSD chi^2 {chi2_fid:.1f}/{len(RSD)}")
print("    sigma_8 is NORMALISED, not predicted: every model is CMB-anchored at z = 999 with delta = a and reported as")
print("    sigma_8 = 0.8111 x D_model(1)/D_LCDM(1).  With g == 1 that ratio is 1 identically, so the control is exact.", flush=True)

# ================================================================= the scan
NZT, NW = 81, 45
zt_ax = np.geomspace(1e-2, 3.0e3, NZT); W_ax = np.geomspace(2e-2, 5.0, NW)
ZT, WW = np.meshgrid(zt_ax, W_ax, indexing="ij")
ZTf, WWf = ZT.ravel(), WW.ravel(); xt = np.log(1 + ZTf); Wv = WWf; P = xt.size
ZSN = np.geomspace(0.01, 1.5, 40)
DL_FID = np.array([comoving(math.log(1 + z), np.array([oL_fid]), np.array([0.0]), np.array([1.0]), 1.0, n=600)[0]*(1 + z)
                   for z in ZSN])
def sne_rms(oL, F, n=500):
    dmu = np.empty((np.size(oL), ZSN.size))
    for j, z in enumerate(ZSN):
        dmu[:, j] = 5*np.log10(comoving(math.log(1 + z), oL, xt, Wv, F, n=n)*(1 + z)/DL_FID[j])
    return np.sqrt(np.mean((dmu - dmu.mean(axis=1, keepdims=True))**2, axis=1))
def q0_of(oL, F):
    return -1.0 - 0.5*(dlng_dlna(0.0, xt, Wv, F) + (-3*OM_M - 4*OM_R)/(OM_M + OM_R + oL))
def refit_h(F, rs, n=600, iters=48):
    """BEST CASE for MODEL A: h floated so the acoustic scale matches Planck EXACTLY.
       theta_s = r_s/D_A is monotonically increasing in h (larger h -> larger omega_Lambda -> larger H -> smaller D_A)."""
    lo = np.full(P, math.sqrt(F*(OM_M + OM_R))*(1 + 1e-9)); hi = np.full(P, 2.0)
    def th(h): return rs/comoving(math.log(1 + Z_REC), h*h/F - OM_M - OM_R, xt, Wv, F, n=n)
    lo_ok = th(lo) <= THETA_S; hi_ok = th(hi) >= THETA_S
    for _ in range(iters):
        mid = 0.5*(lo + hi); m = th(mid) < THETA_S
        lo = np.where(m, mid, lo); hi = np.where(m, mid, hi)
    return 0.5*(lo + hi), (lo_ok & hi_ok)

def evaluate(F):
    o = {}
    o["g_bbn"] = g_of_x(math.log(1 + Z_BBN), xt, Wv, F)
    o["g_rec"] = g_of_x(math.log(1 + Z_REC), xt, Wv, F)
    o["g_cl"]  = g_of_x(math.log(1 + Z_CLUST_MAX), xt, Wv, F)
    # ---- construction (a): the measured H0, physical densities from the CMB, closure at a = 1
    oLa = H_FID**2/F - OM_M - OM_R
    o["OmegaL_a"] = oLa/H_FID**2; o["Omega_m"] = OM_M/H_FID**2; o["ok_oL"] = oLa >= 0.0
    oLv = np.full(P, max(oLa, 0.0))
    rs = sound_horizon(oLv, xt, Wv, F); o["rs"] = rs
    o["dtheta"] = rs/comoving(math.log(1 + Z_REC), oLv, xt, Wv, F)/THETA_S - 1.0
    o["q0_a"] = q0_of(oLv, F); o["sne_a"] = sne_rms(oLv, F)
    A_ok = (o["ok_oL"] & (np.abs(o["dtheta"]) <= 0.003) & (o["q0_a"] >= Q0_LO) & (o["q0_a"] <= Q0_HI)
            & (o["sne_a"] <= 0.10))
    # ---- construction (b): the BEST CASE -- h refitted to Planck's acoustic scale exactly
    hb, br_ok = refit_h(F, rs)
    oLb = np.maximum(hb*hb/F - OM_M - OM_R, 0.0)
    o["h_fit"] = np.where(br_ok, hb, np.nan); o["Om_fit"] = OM_M/hb**2; o["OL_fit"] = oLb/hb**2
    o["q0_b"] = q0_of(oLb, F); o["sne_b"] = sne_rms(oLb, F)
    B_ok = (br_ok & (hb >= H_LO) & (hb <= H_HI) & (o["q0_b"] >= Q0_LO) & (o["q0_b"] <= Q0_HI) & (o["sne_b"] <= 0.10))
    o["A_ok"] = A_ok; o["B_ok"] = B_ok
    # ---- growth, MODEL A (on construction (a), the one at the measured H0)
    D, f, cur = growth(oLv, xt, Wv, F, modelA=True, want_curve=True)
    o["s8"] = S8_FID*D/D_fid[0]; o["dchi2"] = fs8_chi2(cur, o["s8"], None) - chi2_fid
    # ---- growth, MODEL B (perturbations only, LambdaCDM background)
    DB, fB, curB = growth(np.full(P, oL_fid), xt, Wv, F, modelA=False, want_curve=True)
    o["s8_B"] = S8_FID*DB/D_fid[0]; o["dchi2_B"] = fs8_chi2(curB, o["s8_B"], None) - chi2_fid
    # ---- gates
    o["T1"] = np.abs(o["g_bbn"] - 1) <= BBN_TOL
    o["T2"] = np.abs(o["g_rec"] - 1) <= CMB_TOL
    o["T3"] = (np.abs(o["s8"]/S8_FID - 1) <= 0.10) & (o["dchi2"] <= 9.0)
    o["T4"] = A_ok | B_ok
    o["T5"] = o["g_cl"] >= 0.9*F
    o["T3_B"] = (np.abs(o["s8_B"]/S8_FID - 1) <= 0.10) & (o["dchi2_B"] <= 9.0)
    return o

RES = {}
for foot in ("canonical", "alt"):
    F = FREQ[foot]["F"]; R = evaluate(F); RES[foot] = R
    print(f"\n{'-'*124}\n  MODEL A, footing = {foot}:  F = {F:.3f}   grid = {NZT} z_t x {NW} widths = {P} models\n{'-'*124}")
    ceil = H_FID**2/(OM_M + OM_R)
    print(f"    THE ALGEBRAIC CEILING, before any dynamics.  Closure at a = 1 reads 1 = F(Omega_m + Omega_r + Omega_Lambda)")
    print(f"    with the physical densities fixed by the CMB, so Omega_Lambda = 1/F - Omega_m - Omega_r >= 0 forces")
    print(f"    F <= h^2/(omega_m + omega_r) = {ceil:.3f}.  This is a property of F alone: (z_t, W) cannot touch it.")
    print(f"      F = {F:5.2f} (outermost radius) -> Omega_Lambda = {R['OmegaL_a']:+.4f} (LambdaCDM 0.6847); matter is "
          f"{F*R['Omega_m']*100:.1f}% of the total energy density (LambdaCDM 31.5%)")
    for lab, Fx in (("all audited radii ", FREQ[foot]["F_all"]), ("purely Newtonian  ", FREQ[foot]["F_newt"])):
        v = 1/Fx - R["Omega_m"] - OM_R/H_FID**2
        print(f"      F = {Fx:5.2f} ({lab})-> Omega_Lambda = {v:+.4f}" +
              ("   ALREADY EXCLUDED: no positive cosmological constant exists" if v < 0 else ""))
    print(f"    (the alternative reading -- keep rho_Lambda at its LambdaCDM value and let H0 float -- gives")
    print(f"     H0 = sqrt(F) x 67.36 = {math.sqrt(F)*67.36:.1f} km/s/Mpc, against 67.4-73.0 measured.)")
    print(f"\n    representative models:")
    print(f"      {'z_t':>8s} {'W':>6s} | {'g(BBN)-1':>9s} {'g(z*)':>7s} {'g(.09)/F':>8s} | {'sigma_8':>7s} {'dchi2RSD':>8s} | "
          f"{'dtheta_*':>9s} {'q0':>7s} {'SNe rms':>7s} {'h_refit':>7s} | gates")
    for ztv, Wv1 in ((0.05, 0.10), (0.15, 0.55), (0.3, 0.30), (1.0, 0.50), (3.0, 1.00), (30.0, 1.00), (300.0, 1.00), (1000.0, 2.00)):
        i = int(np.argmin((np.log(ZTf/ztv))**2 + (np.log(WWf/Wv1))**2))
        gates = "".join(t[-1] if R[t][i] else "." for t in ("T1", "T2", "T3", "T4", "T5"))
        hf = R["h_fit"][i]
        print(f"      {ZTf[i]:8.3g} {WWf[i]:6.3g} | {R['g_bbn'][i]-1:9.2e} {R['g_rec'][i]:7.3f} {R['g_cl'][i]/F:8.3f} | "
              f"{R['s8'][i]:7.4f} {R['dchi2'][i]:+8.1f} | {R['dtheta'][i]*100:+8.2f}% {R['q0_a'][i]:+7.3f} "
              f"{R['sne_a'][i]:7.3f} {('%7.3f' % hf) if np.isfinite(hf) else '   none'} | {gates}")
    print(f"      (gates column: the digit is shown when that gate PASSES at this point, '.' when it fails)", flush=True)

# ================================================================= T1..T5, each gate alone
print(f"\n{'='*124}\n  the gates, each asked ALONE: is there ANY (z_t, W) on the grid that satisfies it?\n{'='*124}", flush=True)
def cnt(k): return {f: int(RES[f][k].sum()) for f in RES}
n1, n2, n3, n4, n5 = (cnt(k) for k in ("T1", "T2", "T3", "T4", "T5"))
check("T1 [BBN] some (z_t, W) has G_eff = G_0 at nucleosynthesis within the conservative 20% bound",
      all(v > 0 for v in n1.values()),
      ", ".join(f"{f}: {n1[f]}/{P}, best |g-1| = {np.abs(RES[f]['g_bbn']-1).min():.1e}" for f in n1)
      + "  -- passes BY CONSTRUCTION, as the header says; stated explicitly so the construction is honest, "
        "and note this is exactly the L6 horn the roll was invoked to escape")
z2max = {f: (ZTf[RES[f]["T2"]].max() if RES[f]["T2"].any() else float("nan")) for f in RES}
rs_sh = {f: (100*np.abs(RES[f]["rs"][RES[f]["T2"]]/rs0 - 1).max() if RES[f]["T2"].any() else float("nan")) for f in RES}
check("T2 [CMB] some (z_t, W) has G_eff = G_0 at recombination within 10%, so the microwave background does not see it",
      all(v > 0 for v in n2.values()),
      ", ".join(f"{f}: {n2[f]}/{P}" for f in n2)
      + f"; the transition must be over by z_t <~ {z2max['canonical']:.0f} even for the widest roll on the grid, and the "
        f"induced sound-horizon shift across the passing set is at most {rs_sh['canonical']:.2f}%")
check("T3 [growth] some (z_t, W) keeps sigma_8 within 10% of 0.8111 and the RSD f*sigma_8 within Delta chi^2 <= 9",
      all(v > 0 for v in n3.values()),
      ", ".join(f"{f}: {n3[f]}/{P}, sigma_8 spans [{RES[f]['s8'].min():.3f}, {RES[f]['s8'].max():.3f}], "
                f"best Delta chi^2_RSD {RES[f]['dchi2'].min():+.1f}" for f in n3))
check("T4 [expansion] some (z_t, W) keeps the expansion history, on either construction (measured H0, or h refitted "
      "to the acoustic scale)",
      all(v > 0 for v in n4.values()),
      ", ".join(f"{f}: {n4[f]}/{P} (construction a: {int(RES[f]['A_ok'].sum())}, refit b: {int(RES[f]['B_ok'].sum())})"
                for f in n4))
check("T5 [delivers] some (z_t, W) actually delivers 90% of the enhancement at the highest X-COP redshift z = 0.090",
      all(v > 0 for v in n5.values()), ", ".join(f"{f}: {n5[f]}/{P}" for f in n5))

# ---------------------------------------------------------------- the two hard gates in detail
Rc = RES["canonical"]; Fc = FREQ["canonical"]["F"]
print(f"\n  T3 and T4 in detail (canonical footing, F = {Fc:.3f}):")
print(f"    GROWTH.  The g-cancellation in the source is exact, so the boost does NOT drive growth directly.  What drives")
print(f"    it is the closure-forced collapse of Omega_Lambda from 0.685 to {Rc['OmegaL_a']:.3f}: the universe becomes")
print(f"    {Fc*Rc['Omega_m']*100:.0f}% matter by energy density instead of 31.5%, so rho_m/rho_tot -- the growth source -- rises,")
print(f"    and that beats the extra Hubble friction (1/2) dln g/dln a.  Net: growth is ENHANCED, not suppressed.")
print(f"      sigma_8 spans [{Rc['s8'].min():.3f}, {Rc['s8'].max():.3f}] vs 0.8111; f*sigma_8 Delta chi^2 spans "
      f"[{Rc['dchi2'].min():+.1f}, {Rc['dchi2'].max():+.1f}] on {len(RSD)} points")
print(f"      the sigma_8 band alone is passable ({int((np.abs(Rc['s8']/S8_FID-1)<=0.10).sum())}/{P} models); it is the RSD")
print(f"      f*sigma_8 shape that is not, with a best Delta chi^2 of {Rc['dchi2'].min():+.1f} -- and the direction is toward MORE")
print(f"      growth, while weak lensing already prefers LESS.")
print(f"    EXPANSION.  Omega_Lambda = 1/F - Omega_m - Omega_r = {Rc['OmegaL_a']:.4f} is (z_t, W)-INDEPENDENT, because")
print(f"    g(a=1) = F is fixed by the clusters and closure at a = 1 does not know when the roll happened.")
print(f"      acoustic-scale shift d(theta_*)/theta_*  : {100*Rc['dtheta'].min():+.2f}% to {100*Rc['dtheta'].max():+.2f}%   "
      f"(Planck measures it to 0.030%; the gate allows 0.3%)")
print(f"      deceleration parameter q0               : {Rc['q0_a'].min():+.3f} to {Rc['q0_a'].max():+.3f}   (SNe: -0.55 +/- 0.10)")
print(f"      SNe distance-modulus rms, offset removed: {Rc['sne_a'].min():.3f} to {Rc['sne_a'].max():.3f} mag   "
      f"(Pantheon+ shape systematics ~0.03; the gate allows 0.10)")
hf = Rc["h_fit"]; fin = np.isfinite(hf)
print(f"      BEST CASE, h refitted to Planck's theta_* exactly: H0 = "
      f"{100*np.nanmin(hf):.1f} to {100*np.nanmax(hf):.1f} km/s/Mpc over the grid ({int((~fin).sum())}/{P} models have NO")
print(f"      solution at all -- theta_* is unreachable at this F).  Measured H0 is 67.4 (Planck) to 73.0 (SH0ES); the")
print(f"      gate allows the whole band 60-80.  At the refit, Omega_m = {np.nanmin(Rc['Om_fit']):.2f}-{np.nanmax(Rc['Om_fit']):.2f}")
print(f"      and Omega_Lambda = {np.nanmin(Rc['OL_fit']):.2f}-{np.nanmax(Rc['OL_fit']):.2f}, against 0.315 and 0.685 measured.")
print(f"    NOT GATED, reported because it is real and adverse: a rolling G also drifts the type-Ia absolute magnitude,")
print(f"    M_B propto -(15/4) log10 G through the Chandrasekhar mass, giving {3.75*math.log10(Fc):.2f} mag across the transition.")
print(f"    Including it makes T4 strictly worse; it is left out to keep the gate favourable to the model.", flush=True)

# ================================================================= T6 verdict
print(f"\n{'='*124}\n  T6 -- the verdict: is there ANY (z_t, W) that passes every gate at once?\n{'='*124}", flush=True)
JOINT = {}
for f in RES:
    R = RES[f]; JOINT[f] = R["T1"] & R["T2"] & R["T3"] & R["T4"] & R["T5"]; n = int(JOINT[f].sum())
    base = R["T1"] & R["T2"] & R["T5"]
    print(f"    {f:9s} F = {FREQ[f]['F']:.3f}:  {n}/{P} models pass all five")
    print(f"      of the {int(base.sum())} models passing BBN + CMB + delivery, {int((base & R['T3']).sum())} also pass growth "
          f"and {int((base & R['T4']).sum())} also pass the expansion history; both together: {n}")
    if n:
        i = np.where(JOINT[f])[0]
        print(f"      SURVIVING REGION: z_t in [{ZTf[i].min():.4g}, {ZTf[i].max():.4g}], W in [{WWf[i].min():.4g}, {WWf[i].max():.4g}]")
        for j in i[:6]:
            print(f"        z_t = {ZTf[j]:.4g}, W = {WWf[j]:.4g}: sigma_8 {R['s8'][j]:.4f}, dchi2 {R['dchi2'][j]:+.1f}, "
                  f"dtheta {100*R['dtheta'][j]:+.3f}%, q0 {R['q0_a'][j]:+.3f}, SNe {R['sne_a'][j]:.3f}, "
                  f"g(0.09)/F {R['g_cl'][j]/FREQ[f]['F']:.3f}, h_refit {R['h_fit'][j]:.3f}")
check("T6 [verdict] a late-time transition in G_eff, entering the Friedmann and Poisson equations as any scalar-tensor "
      "completion requires, supplies the cluster residual AND survives BBN, the CMB, growth and the expansion history",
      all(int(JOINT[f].sum()) > 0 for f in JOINT),
      ", ".join(f"{f}: {int(JOINT[f].sum())}/{P}" for f in JOINT)
      + "; the expansion-history gate depends on F alone, not on (z_t, W), because g(a=1) = F is fixed by the clusters -- "
        "so no transition redshift and no width can reach it")

# ================================================================= T7 fork: model B
print(f"\n{'='*124}\n  T7 -- the fork (requirement 5): MODEL B, the enhancement in the PERTURBATIONS ONLY\n{'='*124}")
print("    MODEL B is a strictly WEAKER and DIFFERENT model, and is labelled as such wherever it appears.  The background")
print("    expansion is held exactly LambdaCDM while the Poisson source is multiplied by g(a).  That is the")
print("    phenomenological mu(a) parametrisation, not a completion: no action is supplied for it here, and the background")
print("    gravitational effect of the rolling field has to be cancelled by hand.  It evades BBN and the expansion history")
print("    BY CONSTRUCTION rather than by passing them, so only the CMB, growth and delivery gates have content.")
JB = {}
for f in RES:
    R = RES[f]; JB[f] = R["T2"] & R["T3_B"] & R["T5"]; n = int(JB[f].sum())
    print(f"    {f:9s} F = {FREQ[f]['F']:.3f}: sigma_8 spans [{R['s8_B'].min():.3f}, {R['s8_B'].max():.3f}] "
          f"(LambdaCDM 0.8111); {n}/{P} models pass CMB + growth + delivery")
    if n:
        i = np.where(JB[f])[0]
        print(f"      SURVIVING REGION (MODEL B): z_t in [{ZTf[i].min():.4g}, {ZTf[i].max():.4g}], "
              f"W in [{WWf[i].min():.4g}, {WWf[i].max():.4g}]")
        print(f"        there: sigma_8 in [{R['s8_B'][i].min():.3f}, {R['s8_B'][i].max():.3f}], "
              f"Delta chi^2_RSD in [{R['dchi2_B'][i].min():+.1f}, {R['dchi2_B'][i].max():+.1f}]")
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

# ================================================================= parameter-space summary
print(f"\n  SUMMARY OF THE PARAMETER SPACE (canonical footing, F = {Fc:.3f}, {P} models scanned):")
for lab, m in (("BBN alone", Rc["T1"]), ("CMB alone", Rc["T2"]), ("growth alone", Rc["T3"]),
               ("expansion alone", Rc["T4"]), ("delivery alone", Rc["T5"]),
               ("BBN+CMB+delivery", Rc["T1"] & Rc["T2"] & Rc["T5"]),
               ("+ growth", Rc["T1"] & Rc["T2"] & Rc["T5"] & Rc["T3"]),
               ("+ expansion", Rc["T1"] & Rc["T2"] & Rc["T5"] & Rc["T4"]),
               ("ALL FIVE (MODEL A)", JOINT["canonical"]), ("MODEL B, its gates", JB["canonical"])):
    i = np.where(m)[0]
    if i.size: print(f"    {lab:20s}: {i.size:5d}/{P}   z_t in [{ZTf[i].min():.4g}, {ZTf[i].max():.4g}], "
                     f"W in [{WWf[i].min():.4g}, {WWf[i].max():.4g}]")
    else:      print(f"    {lab:20s}: {i.size:5d}/{P}   EMPTY")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
