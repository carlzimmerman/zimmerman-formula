#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f29 -- the coherence-length law made concrete: one parameter, one machinery, every scale it touches.

THE LAW (static limit, the only new ingredient is one length xi):
        nabla^2 Phi_N        = 4 pi G rho_b                          (Newton, from the baryons)
        Phi~                 = S_xi * Phi_N                          (the Newtonian potential smoothed over xi)
        nabla^2 Phi          = nabla . [ nu(|grad Phi~|/a_0) grad Phi~ ]   (QUMOND on the smoothed field; nu = the framework's kernel)
with S_xi a Gaussian filter of width xi (a Helmholtz filter (1 - xi^2 nabla^2)^-1 behaves the same way; both make a point
source's field harmonic inside xi).  For sources that vary on scales >> xi it IS QUMOND.  For a point source it removes
the phantom from inside xi.  Equivalently: the phantom density is the QUMOND phantom of a source that has been spread
over xi.  This is what a medium with a healing length does; the closure programme's localised version (a dynamical
filter field, Theorem 8) is not what is written here -- Phi~ is a constraint, and whether it can remain one in a
covariant host is the question handed to the field-theory lead at the end.

WHAT IS COMPUTED, all from ONE phantom-density quadrature (axisymmetric, source + uniform Newtonian external field):
  1. Validation: xi -> 0 reproduces the committed DHF quadrupole (f23 section 6, q = 0.2748 canonical at the solar
     circle) and a spherical source has zero quadrupole.
  2. The Solar System: Q_2(xi)/ceiling for xi = 0.01 .. 30 pc, both footings; the smallest xi that clears Cassini.
  3. Wide binaries: the pair's phantom monopole inside the separation s as a function of xi; gamma_v(xi) scaled from the
     framework's pre-registered 1.21; the xi above which Gaia DR4 sees Newton (gamma_v < 1.02) and the xi below which
     it cannot tell the two apart.
  4. Globular clusters: the four outer-halo rows of the ledger, each with its own external field; the fraction F of
     the MOND+EFE boost the data require (from B_MOND, B_EFE, B_Newton) and the xi each implies.
  5. Dwarf spheroidals and discs: that xi in the range the clusters imply leaves them untouched (F > 0.9, > 0.99).
  6. The three elliptic equations written out for the lead's constraint-chain machinery.
Every check can fail.  Scope: a static one-parameter law; not a relativistic theory; the GC source is a Gaussian
matched to a Plummer half-mass radius; the wide-binary number is a ratio scaled to the pre-registration, not a
re-derivation of its pipeline.
"""
import os, sys, math
import numpy as np
from scipy.special import erf
from scipy.optimize import brentq
from scipy import integrate
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *
from u10_ledger import ledger

ck = Check()
PC = 3.0857e16; GM_SUN = 6.6743e-11*1.98892e30
GEXT_OBS, SGEXT = 2.32e-10, 0.16e-10
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27
PREF = lambda a0: 1.5*a0**1.5/math.sqrt(GM_SUN)
def nu_rar(y): return 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-30))))
def solve_eN(et): return brentq(lambda e: float(nu_rar(e))*e - et, 1e-9, et*1.5, xtol=1e-14)

# --------------------------------------------------------------- the phantom-density machinery
NR, NT = 1400, 241
def phantom(M, w, gN_ext, a0, rmin, rmax):
    """QUMOND phantom density of a Gaussian source (mass M, width w) in a uniform NEWTONIAN external field gN_ext (z-axis),
    on a log-r x theta grid.  Returns r, theta, rho_ph (kg/m^3).  rho_ph = -div[(nu-1) g_N] / 4 pi G,  g_N = g_ext zhat + g_s(r) rhat."""
    r = np.geomspace(rmin, rmax, NR); th = np.linspace(0.0, math.pi, NT)
    R, TH = np.meshgrid(r, th, indexing="ij")
    x = R/(math.sqrt(2)*w); Menc = M*(erf(x) - math.sqrt(2/math.pi)*(R/w)*np.exp(-R**2/(2*w*w)))
    small = R < 0.05*w                                    # cubic series where the two terms cancel catastrophically
    Menc = np.where(small, M*math.sqrt(2/math.pi)*(R/w)**3/3.0*(1 - 0.3*(R/w)**2), Menc)
    gs = -G*Menc/R**2                                     # inward
    gr = gN_ext*np.cos(TH) + gs; gt = -gN_ext*np.sin(TH)
    f = nu_rar(np.hypot(gr, gt)/a0) - 1.0
    Fr = R**2*f*gr; Ft = np.sin(TH)*f*gt
    dFr = np.gradient(Fr, r, axis=0)/R**2
    dFt = np.gradient(Ft, th, axis=1)/(R*np.maximum(np.sin(TH), 1e-12))
    dFt[:, 0] = dFt[:, 1]; dFt[:, -1] = dFt[:, -2]        # polar rows: sin -> 0, use the neighbour
    return r, th, -(dFr + dFt)/(4*math.pi*G)
def quadrupole(r, th, rho):
    """interior l = 2 coefficient at the origin: Phi_2 = -G r^2 P2 I2, I2 = 2 pi int int rho P2 r^-1 sin(th) dth dr.
    The repository's frozen convention (NORMALIZATION_LOCK; aqual_solver_2026 V2 anchored to Blanchet-Novak 2011's
    published 3.8e-26) is |Q2| = 3 |c2| a0/R_M with c2 the r^2 P2 coefficient of Phi, i.e. Q2 = 3 G I2."""
    P2 = 0.5*(3*np.cos(th)**2 - 1)
    inner = integrate.trapezoid(rho*P2[None, :]*np.sin(th)[None, :], th, axis=1)
    return 3*G*2*math.pi*integrate.trapezoid(inner/r, r)
def enclosed(r, th, rho, s):
    """phantom monopole mass inside radius s."""
    inner = integrate.trapezoid(rho*np.sin(th)[None, :], th, axis=1)*2*math.pi*r**2
    m = r <= s
    return integrate.trapezoid(inner[m], r[m])

P("=" * 118); P("f29 -- the coherence-length law: one parameter, one machinery"); P("=" * 118)
# --------------------------------------------------------------- 1. validation
P("\n1.  validation at xi -> 0 against the committed quadrupole, and the spherical null")
a0c = A0["canonical"]; eta = GEXT_OBS/a0c; eN = solve_eN(eta)*a0c
rM = math.sqrt(GM_SUN/a0c)
info(f"Sun: r_M = {rM/PC:.3f} pc; solar-circle field {GEXT_OBS:.2e} (observed) -> Newtonian external field {eN:.3e} m/s^2 = {eN/a0c:.3f} a_0")
r, th, rho = phantom(1.98892e30, 1e-3*rM, eN, a0c, 1e-4*rM, 1e4*rM)
Q2_0 = abs(quadrupole(r, th, rho)); Q2_ref = 0.2748*PREF(a0c)
ck("V1 the point-mass limit of this quadrature reproduces the committed DHF quadrupole (f23: q = 0.2748 at the solar "
   "circle, canonical) to 5 per cent -- an independent implementation (phantom density + interior multipole) of the "
   "same physics", abs(Q2_0/Q2_ref - 1) < 0.05, f"this file {Q2_0:.3e} vs committed {Q2_ref:.3e} s^-2, ratio {Q2_0/Q2_ref:.3f}")
r0, th0, rho0 = phantom(1.98892e30, 1e-3*rM, 0.0, a0c, 1e-4*rM, 1e4*rM)
ck("V2 with no external field the phantom is spherical and the quadrupole vanishes (P2 orthogonality)",
   abs(quadrupole(r0, th0, rho0)) < 1e-3*Q2_0, f"|Q2(g_ext = 0)| / Q2(solar) = {abs(quadrupole(r0, th0, rho0))/Q2_0:.1e}")
Mph_tot = enclosed(r0, th0, rho0, 1e3*rM)
info(f"total phantom mass of the isolated Sun inside 1000 r_M: {Mph_tot/1.98892e30:.2f} M_sun (deep-MOND growth ~ sqrt(a_0/G M) r, as it should)")

# --------------------------------------------------------------- 2. the Solar System vs xi
P("\n2.  the Solar-System quadrupole against the coherence length")
XIS = np.array([0.003, 0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.2, 0.3, 0.5, 1.0, 3.0, 10.0, 30.0])*PC
Q2 = {}
for foot, a0 in A0.items():
    eNf = solve_eN(GEXT_OBS/a0)*a0
    row = []
    for xi in XIS:
        r, th, rho = phantom(1.98892e30, xi, eNf, a0, min(1e-4*rM, 1e-3*xi), max(1e4*rM, 1e3*xi))
        row.append(abs(quadrupole(r, th, rho)))
    Q2[foot] = np.array(row)
P(f"    {'xi [pc]':>8s} {'Q2/ceiling can':>15s} {'Q2/ceiling alt':>15s} {'suppression can':>16s}")
for i, xi in enumerate(XIS):
    P(f"    {xi/PC:8.2f} {Q2['canonical'][i]/Q2_CEIL:15.4f} {Q2['alt'][i]/Q2_CEIL:15.4f} {Q2['canonical'][i]/Q2['canonical'][0]:16.2e}")
def xi_cross(foot, level):
    q = Q2[foot]/level;
    for i in range(1, len(XIS)):
        if q[i-1] >= 1 > q[i]:
            return math.exp(np.interp(0.0, [math.log(q[i]), math.log(q[i-1])], [math.log(XIS[i]), math.log(XIS[i-1])]))
    return float("nan")
xi_min = {f: xi_cross(f, Q2_CEIL) for f in A0}; xi_1s = {f: xi_cross(f, Q2_CEN + Q2_SIG) for f in A0}
info(f"smallest xi that clears the Park 2026 two-sigma ceiling: canonical {xi_min['canonical']/PC:.2f} pc, alt {xi_min['alt']/PC:.2f} pc; "
     f"to sit within one sigma of the central value: {xi_1s['canonical']/PC:.2f} / {xi_1s['alt']/PC:.2f} pc")
ck("S1 the Solar System needs only a SUB-PARSEC coherence length: the quadrupole falls below the Cassini ceiling for xi "
   "under 1 pc on both footings, and by xi = 3 pc it is below one per cent of the ceiling",
   all(xi_min[f] < PC for f in A0) and all(Q2[f][XIS == 3*PC][0] < 0.01*Q2_CEIL for f in A0),
   f"xi_min = {xi_min['canonical']/PC:.2f} / {xi_min['alt']/PC:.2f} pc; Q2(3 pc)/ceiling = {Q2['canonical'][XIS == 3*PC][0]/Q2_CEIL:.1e}")
slope = np.polyfit(np.log(XIS[XIS > 0.5*PC]), np.log(Q2["canonical"][XIS > 0.5*PC]), 1)[0]
ck("S2 the suppression is the geometric one: for xi >> r_M the quadrupole falls as xi^-3 (the phantom moved from r_M "
   "to xi), slope between -2.5 and -3.5", -3.5 < slope < -2.5, f"d ln Q2 / d ln xi = {slope:.2f} over 0.5-30 pc")
ipk = int(np.argmax(Q2["canonical"]))
ck("S3 THE LAW HAS A HARD LOWER EDGE: smoothing the Sun over LESS than its MOND radius r_M = 0.039 pc makes the "
   "quadrupole LARGER (the source's transition region moves inward, where the r^-3 weighting is strongest); the maximum "
   "is several times the point-mass value, so xi between ~0.003 and ~0.03 pc is worse than no smoothing at all",
   Q2["canonical"][ipk] > 3*Q2_0*1.5 and XIS[ipk] < rM, f"maximum {Q2['canonical'][ipk]/(Q2_0*1.5):.1f}x the point-mass value at xi = {XIS[ipk]/PC:.3f} pc = {XIS[ipk]/rM:.2f} r_M")

# --------------------------------------------------------------- 3. wide binaries
P("\n3.  wide binaries: the pair's phantom monopole inside the separation, and gamma_v(xi)")
Mpair = 2*1.98892e30; rMp = math.sqrt(G*Mpair/a0c)
SEPS = np.array([0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.15])*PC          # 1 to 30 kAU: the Gaia wide-binary range
r, th, rho = phantom(Mpair, 1e-3*rMp, eN, a0c, 1e-4*rMp, 1e4*rMp)
phi0 = {s_: enclosed(r, th, rho, s_)/Mpair for s_ in SEPS}              # unsmoothed: the framework's own law
info(f"pair of 2 M_sun in the solar-circle field: r_M(pair) = {rMp/PC:.3f} pc = {rMp/PC*206265:.0f} AU; internal field equals the external at s = {math.sqrt(G*Mpair/eN)/PC*206265:.0f} AU")
info("unsmoothed phantom monopole inside s / pair mass: " + ", ".join(f"{s_/PC*206265/1e3:.0f} kAU: {phi0[s_]:.3f}" for s_ in SEPS))
# gamma_v: the pre-registered 1.21 is the boost where the phantom monopole has saturated (s >= 0.1 pc); scale linearly in the monopole
GV0 = 1.21; K = (GV0**2 - 1)/phi0[SEPS[-2]]
gv = lambda ph: math.sqrt(1 + K*max(ph, 0.0))
GV = {}
P(f"    {'xi [pc]':>8s} " + " ".join(f"{'gv('+format(s_/PC*206265/1e3,'.0f')+'kAU)':>10s}" for s_ in SEPS))
for xi in np.concatenate([[0.0], XIS]):
    if xi == 0.0: ph = phi0
    else:
        r, th, rho = phantom(Mpair, xi, eN, a0c, min(1e-4*rMp, 1e-3*xi), max(1e4*rMp, 1e3*xi))
        ph = {s_: enclosed(r, th, rho, s_)/Mpair for s_ in SEPS}
    GV[xi] = {s_: gv(ph[s_]) for s_ in SEPS}
    P(f"    {xi/PC:8.2f} " + " ".join(f"{GV[xi][s_]:10.3f}" for s_ in SEPS))
kAU = lambda s_: s_/PC*206265/1e3
ck("W0 sanity: the UNSMOOTHED law already has a separation dependence -- Newtonian inside the radius where the pair's own "
   "field exceeds the external one (~8 kAU) and the full pre-registered boost beyond ~10 kAU.  This check pins the method: "
   "gamma_v(2 kAU) < 1.05 and gamma_v(20 kAU) within 0.02 of 1.21",
   GV[0.0][SEPS[1]] < 1.05 and abs(GV[0.0][SEPS[-2]] - 1.21) < 0.02, f"gamma_v(2 kAU) = {GV[0.0][SEPS[1]]:.3f}, (6 kAU) = {GV[0.0][SEPS[3]]:.3f}, (20 kAU) = {GV[0.0][SEPS[-2]]:.3f}")
xi_c = XIS[XIS >= max(xi_min.values())][0]                          # the smallest tabulated xi that clears Cassini on both footings
ck("W1 THE CASSINI <-> WIDE-BINARY LOCK IS BROKEN BY A LENGTH: at the smallest xi that clears Cassini the pre-registered "
   "boost at 20-30 kAU SURVIVES (gamma_v > 1.15) while the Solar-System quadrupole is gone.  The repository's lock assumed "
   "a screening keyed on the external-field strength; a screening keyed on length separates the two, because the "
   "quadrupole is weighted by r^-3 around the Sun while the binary boost is the phantom monopole inside the separation",
   GV[xi_c][SEPS[-2]] > 1.15 and Q2["canonical"][XIS == xi_c][0] < Q2_CEIL,
   f"xi = {xi_c/PC:.2f} pc: Q2/ceiling = {Q2['canonical'][XIS == xi_c][0]/Q2_CEIL:.2f} / {Q2['alt'][XIS == xi_c][0]/Q2_CEIL:.2f}, gamma_v(20 kAU) = {GV[xi_c][SEPS[-2]]:.3f}")
ck("W2 (THE NEW PREDICTION) the coherence length moves the wide-binary KNEE outward: at 6 kAU the unsmoothed law is already "
   "boosted (gamma_v > 1.12) while the Cassini-minimal xi keeps it near Newton (gamma_v < 1.06); by 20-30 kAU both agree.  "
   "Gaia DR4 binned in separation (the 4-10 kAU bins) distinguishes them; a flat 1.00 or a flat 1.2 fits neither",
   GV[0.0][SEPS[3]] > 1.12 and GV[xi_c][SEPS[3]] < 1.06 and GV[xi_c][SEPS[-1]] > 1.15,
   f"at 6 kAU: framework {GV[0.0][SEPS[3]]:.3f} vs xi = {xi_c/PC:.2f} pc {GV[xi_c][SEPS[3]]:.3f}; at 30 kAU: {GV[0.0][SEPS[-1]]:.3f} vs {GV[xi_c][SEPS[-1]]:.3f}")
ck("W3 and for xi >= 0.3 pc the binaries are Newtonian at every separation up to 30 kAU: the large-xi regime (the one the "
   "globular clusters point to) predicts a flat gamma_v = 1.00 in DR4",
   all(GV[xi][s_] < 1.02 for xi in XIS if xi >= 0.3*PC for s_ in SEPS), f"max gamma_v over s <= 30 kAU at xi >= 0.3 pc: {max(GV[xi][s_] for xi in XIS if xi >= 0.3*PC for s_ in SEPS):.4f}")

# --------------------------------------------------------------- 4. globular clusters
P("\n4.  the four outer-halo globular clusters: the fraction of the MOND+EFE boost the data require, and the xi it implies")
rows_iso = {r_["name"]: r_ for r_ in ledger("canonical", "iso")}; rows_efe = {r_["name"]: r_ for r_ in ledger("canonical", "published")}
GC = {}
P(f"    {'cluster':9s} {'r_h [pc]':>8s} {'M_enc':>9s} {'e_N':>6s} {'B_MOND':>7s} {'B_EFE':>7s} {'B_Newt':>7s} {'F_req':>7s} {'xi implied':>12s}")
for nm in ("pal4", "pal14", "ngc2419", "pal3"):
    ri, re_ = rows_iso[nm], rows_efe[nm]
    BN = ri["B"] + math.log10(float(nu_rar(ri["y"]))); boost_obs = 10**BN; boost_mond = 10**(BN - re_["B"])
    Freq = (boost_obs - 1)/(boost_mond - 1)
    rh = ri["r"]; M = ri["M_enc"]*2.0                      # M_enc at r_h ~ half the mass for a Plummer-like profile
    w0 = 0.65*rh; gext = ri["x_ext"]*a0c                   # the ledger's x_ext is the Newtonian external field / a_0
    r_, th_, rho_ = phantom(M, w0, gext, a0c, 1e-3*rh, 1e3*rh); Mb0 = enclosed(r_, th_, rho_, rh)
    def Fxi(xi):
        w = math.sqrt(w0*w0 + xi*xi); r2, t2, p2 = phantom(M, w, gext, a0c, 1e-3*rh, max(1e3*rh, 1e2*w)); return enclosed(r2, t2, p2, rh)/Mb0
    xis = np.geomspace(0.1*rh, 300*rh, 25); Fs = np.array([Fxi(x_) for x_ in xis])
    xi_imp = float("nan") if Freq <= Fs.min() or Freq >= Fs.max() else math.exp(np.interp(-Freq, -Fs, np.log(xis)))
    GC[nm] = dict(rh=rh, Freq=Freq, xi=xi_imp, Fs=Fs, xis=xis)
    P(f"    {nm:9s} {rh/PC:8.1f} {M/1.989e30:9.2e} {ri['x_ext']:6.3f} {ri['B']:+7.3f} {re_['B']:+7.3f} {BN:+7.3f} {Freq:+7.3f} "
      + (f"{xi_imp/PC:9.0f} pc" if not math.isnan(xi_imp) else ("   > " + f"{xis[-1]/PC:.0f} pc (Newton or below)" if Freq <= Fs.min() else "  < " + f"{xis[0]/PC:.0f} pc")))
three = [GC[n]["xi"] for n in ("pal14", "ngc2419")]
ck("G1 the three Newtonian-side globulars want a coherence length of tens of parsecs or more (Pal 4 a lower bound, Pal 14 "
   "and NGC 2419 finite values within a factor of three of each other), and Pal 3 wants a much smaller one: the "
   "globular-cluster rung MEASURES xi if three of the four are trusted, and Pal 3 is the discordant row",
   all(not math.isnan(x_) for x_ in three) and max(three)/min(three) < 3.0 and (math.isnan(GC["pal4"]["xi"]) or GC["pal4"]["xi"] > 10*PC)
   and (math.isnan(GC["pal3"]["xi"]) or GC["pal3"]["xi"] < min(three)),
   "; ".join(f"{n}: {GC[n]['xi']/PC:.0f} pc" if not math.isnan(GC[n]["xi"]) else f"{n}: out of range" for n in GC))
XI_GC = math.exp(np.mean([math.log(x_) for x_ in three]))
info(f"geometric mean of the two finite values: xi_GC ~ {XI_GC/PC:.0f} pc")

# --------------------------------------------------------------- 5. dwarfs and discs untouched
P("\n5.  what xi ~ xi_GC leaves untouched")
def F_system(M, rh_, gext, xi, R):
    w0_ = 0.65*rh_; r_, t_, p_ = phantom(M, w0_, gext, a0c, 1e-3*rh_, 1e3*max(rh_, xi)); m0 = enclosed(r_, t_, p_, R)
    w = math.sqrt(w0_*w0_ + xi*xi); r2, t2, p2 = phantom(M, w, gext, a0c, 1e-3*rh_, 1e3*max(rh_, xi)); return enclosed(r2, t2, p2, R)/m0
F_dsph = F_system(3e5*1.989e30, 220*PC, 0.01*a0c, XI_GC, 220*PC)
F_disc = F_system(5e10*1.989e30, 3000*PC, 0.02*a0c, XI_GC, 3000*PC)
ck("D1 a Draco-like dwarf spheroidal (r_h = 220 pc) keeps more than 70 per cent of its MOND+EFE boost at xi = xi_GC "
   "(a 0.1-0.15 dex reduction, inside the dwarf rung's own prescription spread), and a 3 kpc disc keeps more than 99 "
   "per cent: the length the globulars point to does not touch the discs and only trims the dwarfs", F_dsph > 0.7 and F_disc > 0.99, f"F(dSph) = {F_dsph:.3f}, F(disc) = {F_disc:.4f} at xi = {XI_GC/PC:.0f} pc")

# --------------------------------------------------------------- 6. the equations for the lead
P("\n6.  handed to the field-theory lead: the static system whose constraint chain decides whether xi costs a degree of freedom")
P("      (i)   nabla^2 Phi_N = 4 pi G rho_b")
P("      (ii)  (1 - xi^2 nabla^2) Phi~ = Phi_N            [Helmholtz filter; the Gaussian used above is its smooth cousin]")
P("      (iii) nabla^2 Phi = nabla . [ nu(|grad Phi~|/a_0) grad Phi~ ]")
P("    Three elliptic equations, no time derivatives.  (ii) is what Theorem 8 localised into a dynamical field and killed;")
P("    here it is a CONSTRAINT.  The question for the Dirac chain: with Phi~ a constrained variable, is the finite-k static")
P("    block still 0 propagating DOF (as your two-field block was), and does the k -> 0 sector survive a background?")
P(f"    Numbers to hold it to: xi >= {max(xi_min.values())/PC:.2f} pc (Cassini; and NOT below ~0.03 pc, where smoothing makes it worse); two regimes:")
P(f"      small xi (0.03-0.1 pc): Cassini passes, wide binaries keep the boost at 20 kAU with a knee near xi, globulars stay MOND (f13's +0.3 dex remains);")
P(f"      large xi (~{XI_GC/PC:.0f} pc, from 3 of 4 globulars): Cassini passes, wide binaries Newtonian at all separations, dwarfs trimmed by 0.1-0.15 dex, discs untouched.")
P("    Gaia DR4 binned in separation, and the outer-halo globulars, decide between them.")
sys.exit(ck.done())
