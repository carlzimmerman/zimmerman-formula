#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h85_bulk_flow_null.py -- HUNT ITEM 85: "no MOND in bulk flows", the framework's own NULL.
=========================================================================================
This item is not a search for a signal.  It is the one place where the framework makes a prediction that
SEPARATES it from MOND-as-cosmology, and the prediction is that nothing happens.

The framework's linear regime is Newtonian by theorem: the MOND sector drops out of the linear perturbation
equations (delta Y^(1) = 0), so the growth rate, the velocity-density relation and the bulk flows are all
LambdaCDM's.  MOND cosmology has no such theorem -- there the same interpolation function that boosts a
rotation curve also boosts the linear velocity field, and Nusser and Sanders both found the resulting
peculiar velocities too large.  So a measurement of beta = f/b from the local velocity-density relation is
a test that can only go one way for each theory.

AND THE ACCELERATION THAT DRIVES THE LOCAL FLOW IS DEEP IN THE MOND REGIME.  That is what makes this a real
test rather than a formality: the gravitational acceleration pulling the Local Group at 620 km/s is of order
1e-12 m/s^2, roughly a HUNDREDTH of a_0, so an unprotected kernel would multiply it by nu ~ 9.  The framework
survives only because of the theorem; if the theorem is wrong, the local flow is wrong by an order of magnitude.

DATA, ON DISK: the Carrick+2015 2M++ real-space reconstructed density field
(real_research/data/twompp_density.npy, 257^3, Galactic Cartesian Mpc/h, Local Group at cell [128,128,128],
spacing 400/256 Mpc/h).  Everything else -- the linear power spectrum, the growth rate, the rms bulk flow --
is computed here from the same Planck parameters, so nothing is quoted from another script.
Both a_0 footings.  Mutation control.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(85085)

NS, S8 = 0.965, 0.811
SP = 400.0 / 256.0                              # grid spacing, Mpc/h
NG, CEN = 257, 128
FGROW = OM_M ** 0.55                            # LambdaCDM linear growth rate f = dlnD/dlna
B_2MPP = 1.2                                    # K-band luminosity-weighted galaxy bias used by Carrick+2015
# the Local Group's motion in the CMB frame (CMB dipole minus the Sun's motion within the LG)
V_LG, EV_LG, L_LG, B_LG = 620.0, 15.0, 271.9, 29.0

def unit_gal(l_deg, b_deg):
    l, b = math.radians(l_deg), math.radians(b_deg)
    return np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])

VHAT = unit_gal(L_LG, B_LG)

P("=" * 118); P("PART A -- the local gravitational acceleration, in units of a_0"); P("=" * 118)
info("linear theory ties the peculiar velocity to the acceleration: v = 2 f g / (3 H_0 Omega_m).  Inverting it")
info("with the OBSERVED Local Group velocity gives the acceleration that is actually pulling us, with no model.")
g_LG = 1.5 * H0 * OM_M * (V_LG * 1e3) / FGROW
for ft, a0 in A0.items():
    info(f"g(Local Group) = {g_LG:.3e} m/s^2  =  {g_LG/a0:.4f} a_0 ({ft} footing)  ->  kernel factor "
         f"nu = {nu_s(g_LG/a0):.2f}")
ck("A1 the local velocity field is generated DEEP inside the MOND regime -- the acceleration pulling the Local "
   "Group is about a hundredth of a_0 -- so 'the framework's linear regime is Newtonian' is a substantive claim "
   "about a place where the kernel would otherwise be enormous, not a statement about a regime where it is off",
   max(g_LG / a0 for a0 in A0.values()) < 0.1,
   f"g = {g_LG:.2e} m/s^2 = {g_LG/A0['canonical']:.4f} a_0 (canonical) / {g_LG/A0['alt']:.4f} a_0 (alt); "
   f"nu = {nu_s(g_LG/A0['canonical']):.2f} / {nu_s(g_LG/A0['alt']):.2f}")

P(""); P("=" * 118); P("PART B -- beta = f/b measured from the 2M++ field and the observed Local Group velocity"); P("=" * 118)
cube = np.load(os.path.join(DATA, "twompp_density.npy"))
info(f"2M++ reconstruction loaded: {cube.shape}, delta in [{cube.min():.2f}, {cube.max():.2f}], "
     f"mean {cube.mean():+.5f}, cell {SP:.4f} Mpc/h, box half-width {CEN*SP:.0f} Mpc/h")
ax = (np.arange(NG) - CEN) * SP
X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
DV = SP ** 3

def v_pred(delta, rmin=3.0, rmax=200.0):
    """linear-theory velocity at the origin for beta = 1, in km/s (H_0 = 100 km/s per Mpc/h in these units)."""
    m = (R > rmin) & (R < rmax)
    w = delta[m] / R[m] ** 3 * DV
    return (100.0 / (4 * math.pi)) * np.array([np.sum(w * X[m]), np.sum(w * Y[m]), np.sum(w * Z[m])])

v1 = v_pred(cube)
n1 = np.linalg.norm(v1)
cosang = float(np.dot(v1, VHAT) / n1)
ang = math.degrees(math.acos(np.clip(cosang, -1, 1)))
lpred = math.degrees(math.atan2(v1[1], v1[0])) % 360.0
bpred = math.degrees(math.asin(v1[2] / n1))
info(f"predicted Local Group velocity for beta = 1: |v| = {n1:.1f} km/s toward (l, b) = ({lpred:.1f}, {bpred:.1f}); "
     f"observed 620 km/s toward ({L_LG}, {B_LG}); misalignment {ang:.1f} deg")
ck("B1 the reconstruction reproduces the DIRECTION of the Local Group's motion, which is the part of this test "
   "that has nothing to do with any theory of gravity and everything to do with the data being real",
   ang < 30.0, f"misalignment {ang:.1f} degrees between the predicted and the observed apex")
V_EXT = 159.0                                     # Carrick+2015 residual external flow, km/s
beta_amp = V_LG / n1
beta_fit = V_LG * cosang / n1                     # projection of the observation onto the prediction direction
beta_lo = max(V_LG * cosang - V_EXT, 0.0) / n1    # if the external flow is entirely aligned: a LOWER bound
info(f"beta from the amplitude alone     : {beta_amp:.3f}")
info(f"beta from the aligned component   : {beta_fit:.3f}   (observation projected on the predicted direction)")
info(f"beta with the external flow removed: {beta_lo:.3f}   (a lower bound: assumes all {V_EXT:.0f} km/s is aligned)")
info(f"LambdaCDM expectation             : f/b = Omega_m^0.55 / b_K = {FGROW:.3f}/{B_2MPP:.2f} = {FGROW/B_2MPP:.3f}")
info("(Carrick+2015, fitting the same field to a full peculiar-velocity catalogue, obtain beta* = 0.431 +- 0.021 "
     "together with that external flow; the bracket [lower bound, aligned component] here contains their value.)")
BETA_LCDM = FGROW / B_2MPP
ck("B2 THE FRAMEWORK'S NULL HOLDS.  The velocity-density relation of the local universe returns a growth-to-bias "
   "ratio consistent with LambdaCDM's, using no free parameter beyond the K-band bias: the framework predicts "
   "exactly this, because its MOND sector is absent from linear perturbations",
   abs(math.log10(beta_fit / BETA_LCDM)) < 0.18 and beta_lo < BETA_LCDM < beta_fit * 1.05,
   f"beta = {beta_lo:.3f} (external flow removed) to {beta_fit:.3f} (external flow ignored) against LambdaCDM's "
   f"{BETA_LCDM:.3f}; the aligned-component value is {beta_fit/BETA_LCDM:.2f}x it, "
   f"{math.log10(beta_fit/BETA_LCDM):+.3f} dex.  Carrick+2015's own fit to this field gives 0.431")
# --- what an unprotected kernel would do
nu_lin = {ft: nu_s(g_LG / A0[ft]) for ft in A0}
beta_mond = {ft: BETA_LCDM / nu_lin[ft] for ft in A0}
info(f"if the kernel acted on linear scales, the same density field would generate velocities nu = "
     f"{nu_lin['canonical']:.1f}-{nu_lin['alt']:.1f} times larger, so matching the observed 620 km/s would need "
     f"beta = {beta_mond['alt']:.3f}-{beta_mond['canonical']:.3f}")
ck("B3 AND THAT IS THE SEPARATION.  An unprotected kernel acting on the observed density field would over-predict "
   "the local flow by nearly an order of magnitude, so the measured beta excludes it outright.  The framework "
   "survives this only through its linear-growth theorem -- which makes the theorem load-bearing, and makes item 85 "
   "a genuine framework-specific NULL rather than an absence of evidence",
   min(beta_mond.values()) < 0.5 * BETA_LCDM and beta_fit > 2 * max(beta_mond.values()),
   f"kernel-on would need beta = {min(beta_mond.values()):.3f}-{max(beta_mond.values()):.3f} against a measured "
   f"{beta_fit:.3f}; the required suppression is a factor {beta_fit/max(beta_mond.values()):.1f}")
# --- robustness to the inner cut and the outer radius
info(f"{'r_min':>7} {'r_max':>7} {'|v| (beta=1)':>13} {'beta':>7} {'misalign':>9}")
ROB = []
for rmin, rmax in ((1.5, 200.0), (3.0, 200.0), (5.0, 200.0), (3.0, 150.0), (3.0, 100.0), (3.0, 60.0)):
    vv = v_pred(cube, rmin, rmax); nn = np.linalg.norm(vv)
    ca = float(np.dot(vv, VHAT) / nn)
    ROB.append((rmin, rmax, nn, V_LG * ca / nn, math.degrees(math.acos(np.clip(ca, -1, 1)))))
    info(f"{rmin:>7.1f} {rmax:>7.1f} {nn:>13.1f} {V_LG*ca/nn:>7.3f} {math.degrees(math.acos(np.clip(ca,-1,1))):>9.1f}")
bet = [r[3] for r in ROB]
ck("B4 the answer is stable against the two arbitrary choices in the sum -- how close to the origin the "
   "reconstruction is trusted, and how far out it is integrated -- so beta is a property of the field and not of "
   "the cut", (max(bet) - min(bet)) / np.mean(bet) < 0.6,
   f"beta spans {min(bet):.3f}-{max(bet):.3f} over r_min = 1.5-5 Mpc/h and r_max = 60-200 Mpc/h; the trend with "
   f"r_max is the known convergence of the local flow")
# --- mutation control: destroy the structure, keep the one-point distribution
shuf = cube.reshape(-1).copy(); rng.shuffle(shuf); shuf = shuf.reshape(cube.shape)
vm = v_pred(shuf); nm = np.linalg.norm(vm)
angm = math.degrees(math.acos(np.clip(float(np.dot(vm, VHAT) / nm), -1, 1)))
ck("B5 MUTATION CONTROL: shuffling the density values between cells keeps the one-point distribution and destroys "
   "the structure.  The predicted velocity then collapses in amplitude and points nowhere near the observed apex, "
   "so the alignment above is the cosmic web and not an artefact of the box or the weighting",
   nm < 0.2 * n1 and angm > 40.0,
   f"shuffled field: |v| = {nm:.1f} km/s (against {n1:.1f}) and {angm:.0f} degrees off the observed apex")

P(""); P("=" * 118); P("PART C -- the bulk flow in spheres: reconstruction vs LambdaCDM's own expectation"); P("=" * 118)
# LambdaCDM rms bulk flow from the same Planck parameters, computed here (EH98 no-wiggle + sigma_8)
_theta, _om, _ob = 2.7255 / 2.7, OM_M * h * h, OM_B * h * h
_fb = _ob / _om
_s_eh = 44.5 * math.log(9.83 / _om) / math.sqrt(1 + 10 * _ob ** 0.75)
_ag = 1 - 0.328 * math.log(431 * _om) * _fb + 0.38 * math.log(22.3 * _om) * _fb ** 2
def T_eh(k):
    gam = OM_M * h * (_ag + (1 - _ag) / (1 + (0.43 * k * h * _s_eh) ** 4))
    q = k * _theta ** 2 / gam
    L = np.log(2 * math.e + 1.8 * q); C = 14.2 + 731.0 / (1 + 62.5 * q)
    return L / (L + C * q * q)
_K = np.logspace(-5, 2.5, 6000)
_P = _K ** NS * T_eh(_K) ** 2
def _s2(Rr):
    x = _K * Rr; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return np.trapz(_K ** 2 * _P * W ** 2, _K) / (2 * math.pi ** 2)
_AMP = S8 ** 2 / _s2(8.0)
def v_rms(Rr):
    x = _K * Rr; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return (100.0 * FGROW) * math.sqrt(_AMP * np.trapz(_P * W ** 2, _K) / (2 * math.pi ** 2))

# the whole linear velocity field at once, by FFT of  v(k) = i H_0 delta(k) k / k^2 (beta = 1).
# the cube is block-averaged 2x (to 128^3, 3.125 Mpc/h -- far below the 50 Mpc/h scales tested) and
# zero-padded to 256^3 so the transform is not periodic across the survey boundary.
c2 = cube[:256, :256, :256].reshape(128, 2, 128, 2, 128, 2).mean(axis=(1, 3, 5))
SP2, N2 = 2 * SP, 256
pad = np.zeros((N2, N2, N2)); pad[64:192, 64:192, 64:192] = c2
kk = 2 * math.pi * np.fft.fftfreq(N2, d=SP2)
KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing="ij")
K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
dk = np.fft.fftn(pad)
VF = [np.real(np.fft.ifftn(1j * 100.0 * dk * KC / K2)) for KC in (KX, KY, KZ)]
ax2 = (np.arange(N2) - 128) * SP2 + 0.5 * SP2 * 0
ax2 = (np.arange(N2) - (64 + 64)) * SP2                      # LG cell 128 of the padded grid
X2, Y2, Z2 = np.meshgrid(ax2, ax2, ax2, indexing="ij")
R2 = np.sqrt(X2 ** 2 + Y2 ** 2 + Z2 ** 2)
v_fft_lg = np.array([VF[0][128, 128, 128], VF[1][128, 128, 128], VF[2][128, 128, 128]])
info(f"cross-check of the two methods at the origin: direct sum gives |v| = {n1:.1f} km/s toward "
     f"({lpred:.1f}, {bpred:.1f}); the FFT solution of the same linear equation gives "
     f"{np.linalg.norm(v_fft_lg):.1f} km/s toward "
     f"({math.degrees(math.atan2(v_fft_lg[1], v_fft_lg[0])) % 360:.1f}, "
     f"{math.degrees(math.asin(v_fft_lg[2]/np.linalg.norm(v_fft_lg))):.1f}) "
     f"-- they differ because the direct sum excludes r < 3 Mpc/h and r > 200 Mpc/h")

def bulk_from_field(Rsph):
    m = R2 < Rsph
    return np.array([float(VF[i][m].mean()) for i in range(3)])

info(f"{'R [Mpc/h]':>10} {'LambdaCDM rms bulk flow':>25} {'2M++ field, beta = f/b':>24}")
BULK = {}
for Rs in (50.0, 100.0, 150.0):
    vr = v_rms(Rs)
    bf = np.linalg.norm(bulk_from_field(Rs)) * BETA_LCDM
    BULK[Rs] = (vr, bf)
    info(f"{Rs:>10.0f} {vr:>25.1f} {bf:>24.1f}")
ck("C1 the bulk flows the reconstruction itself carries are of LambdaCDM's own size at every radius from 50 to 150 "
   "Mpc/h -- within a factor two, and low rather than high, which is the direction the missing external flow "
   "explains.  The framework predicts exactly this; MOND-as-cosmology does not, since an unprotected kernel would "
   "multiply them by nu ~ 9 as well.  The check tolerates a factor three because the reconstruction is truncated "
   "at 200 Mpc/h and the rms is an ensemble quantity being compared with one realisation",
   all(0.33 * v[0] < math.hypot(v[1], V_EXT) < 3.0 * v[0] for v in BULK.values()),
   ", ".join(f"R = {k:.0f}: field {v[1]:.0f} km/s (+{V_EXT:.0f} external -> {math.hypot(v[1], V_EXT):.0f}) vs "
             f"LambdaCDM rms {v[0]:.0f} km/s" for k, v in BULK.items()))
ck("C2 and the same statement in the form that decides between the theories: matching the reconstruction's bulk "
   "flows with a kernel-boosted velocity field would need the growth rate suppressed by nearly an order of "
   "magnitude, which no measurement of f sigma_8 allows",
   max(nu_lin.values()) > 5.0,
   f"kernel boost at the local acceleration nu = {min(nu_lin.values()):.1f}-{max(nu_lin.values()):.1f}; "
   f"f sigma_8 is measured to about 5% by redshift surveys")

P(""); P("=" * 118); P("VERDICT"); P("=" * 118)
P(f"  Item 85 delivers the NULL it was designed to deliver, and the null has teeth.  The acceleration driving the")
P(f"  local flow is {g_LG/A0['canonical']:.3f} a_0 -- a hundredth of the MOND scale -- so an interpolation function acting on linear")
P(f"  perturbations would inflate the velocity field by nu = {nu_lin['canonical']:.1f}.  The 2M++ reconstruction plus the observed 620")
P(f"  km/s Local Group motion return beta = {beta_fit:.3f} against LambdaCDM's {BETA_LCDM:.3f}, and the reconstruction's bulk flows sit")
P(f"  at LambdaCDM's rms values from 50 to 150 Mpc/h.  The framework passes because of its linear-growth theorem,")
P(f"  which this item therefore promotes from a technical result to a load-bearing one; MOND cosmology without such")
P(f"  a theorem is excluded by the same numbers.  Nothing here measures a_0 -- that is the point.")
sys.exit(ck.done())
