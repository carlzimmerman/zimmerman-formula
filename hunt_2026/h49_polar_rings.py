#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h49_polar_rings.py -- HUNT ITEM 49: polar-ring galaxies.
========================================================
The item as written: "ring speed from the disc's baryons in MOND (flattened phantom); ring faster than the disc by
the predicted ratio; ratio within 10% for 5+ systems."

TWO THINGS HAVE TO BE SEPARATED, and the item conflates them.

  (1) THE RING-VERSUS-DISC RATIO AT THE SAME RADIUS.  This is the quantity the polar-ring literature uses to measure
      dark-halo flattening (Sackett & Sparke 1994; Iodice et al. 2003), and the framework makes a SIGN-DEFINITE
      prediction about it: the phantom dark matter of a disc is itself FLATTENED TOWARD THE DISC, so at radii where
      the mass distribution still matters the polar circular speed is LOWER than the equatorial one, not higher.
      The item states the opposite ("ring faster than the disc"), which is the observers' inference about the HALO,
      not the framework's prediction about the phantom.  PART 1 computes the real number with a three-dimensional
      QUMOND solve, and it comes out on the low side, so THE ITEM'S PREDICTION AS WRITTEN IS WITHDRAWN and replaced
      by the computed one.  The ring-versus-disc data needed to test it are NOT machine-readable (PART 0).

  (2) THE ONE PREDICTION THAT IS BOTH SHARP AND TESTABLE FROM PUBLIC DATA.  In the framework the field far from any
      baryonic distribution becomes spherical, g -> sqrt(G M_b a_0)/r, whatever shape the baryons have.  A polar
      ring at 1.5-3 optical radii therefore has NOTHING to measure about halo shape: it must sit on the SAME
      baryonic Tully-Fisher relation, with the SAME a_0, as an ordinary disc.  That is a zero-parameter statement
      and it is exactly what a dark halo of adjustable flattening does not make.  PART 2 tests it on the HI survey
      of polar-ring galaxies (Huchtmeier 1997, VizieR J/A+A/319/401, fetched this session), using the QUMOND
      finite-radius correction computed in PART 1 rather than the bare asymptotic formula.

Both footings.  Newtonian baryons and a spherical NFW halo computed beside the framework.  Mutation controls.
Checks CAN fail.
"""
import sys, math, os
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(4949)
H0_KMS = 67.4
MB_SUN = 5.44                 # absolute B magnitude of the Sun
UPS_B = 1.5                   # stellar M/L in B for an early-type host; scanned in PART 2
W_TURB = 22.0                 # km/s, turbulent broadening subtracted from W20 (Verheijen 2001 convention)
CZ_MIN = 1500.0               # km/s, below this a flow distance is not trustworthy

# =====================================================================================================================
# PART 1 -- the prediction, from a three-dimensional QUMOND solve
# =====================================================================================================================
# QUMOND:  div( grad Phi ) = div[ nu(|grad Phi_N|/a_0) grad Phi_N ].
# So: (a) solve Poisson for the baryons -> Phi_N, g_N = -grad Phi_N;
#     (b) build h = nu(|g_N|/a_0) g_N;  the effective source is rho_eff = div(h)/(4 pi G);
#     (c) solve Poisson again for rho_eff -> Phi, g = -grad Phi.
# Both Poisson solves use the Hockney-Eastwood zero-padded FFT convolution, which gives ISOLATED (not periodic)
# boundary conditions.  The algebraic shortcut g = nu(g_N/a_0) g_N is exact only in spherical, cylindrical or plane
# symmetry; a disc-plus-polar-ring has none of those, which is why the full solve is done here.

class Poisson3D:
    """Isolated-boundary Poisson solver by zero-padded FFT convolution with the 1/r Green's function."""
    def __init__(self, n, h):
        self.n, self.h = n, h
        m = 2*n
        i = np.arange(m); i = np.minimum(i, m - i)            # wrap-around distance in cells
        X, Y, Z = np.meshgrid(i, i, i, indexing="ij")
        r = h*np.sqrt(X.astype(np.float64)**2 + Y**2 + Z**2)
        r[0, 0, 0] = 0.5*h                                    # standard one-cell softening
        self.gk = np.fft.rfftn(-G/r); del r, X, Y, Z
    def solve(self, rho):
        """rho on the inner n^3 grid (SI kg/m^3) -> potential on the same grid (SI J/kg)."""
        m = 2*self.n
        pad = np.zeros((m, m, m)); pad[:self.n, :self.n, :self.n] = rho
        phi = np.fft.irfftn(np.fft.rfftn(pad)*self.gk, s=(m, m, m))*self.h**3
        return phi[:self.n, :self.n, :self.n]

def grad3(f, h):
    return np.gradient(f, h, edge_order=2)

def div3(fx, fy, fz, h):
    return np.gradient(fx, h, axis=0, edge_order=2) + np.gradient(fy, h, axis=1, edge_order=2) + \
           np.gradient(fz, h, axis=2, edge_order=2)

def interp3(F, coords, x0, h):
    """Trilinear interpolation of grid field F at physical coords (..., 3), grid origin x0, spacing h."""
    t = (np.asarray(coords, float) - x0)/h
    i0 = np.floor(t).astype(int); f = t - i0
    n = F.shape[0]; i0 = np.clip(i0, 0, n - 2)
    out = np.zeros(t.shape[:-1])
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = ((1 - f[..., 0]) if dx == 0 else f[..., 0]) * \
                    ((1 - f[..., 1]) if dy == 0 else f[..., 1]) * \
                    ((1 - f[..., 2]) if dz == 0 else f[..., 2])
                out += w*F[i0[..., 0] + dx, i0[..., 1] + dy, i0[..., 2] + dz]
    return out

class Model:
    """Baryons on a cube: an exponential host disc in the x-y plane plus a polar ring annulus in the x-z plane."""
    def __init__(self, n=128, L_kpc=100.0):
        self.n = n; self.L = L_kpc*kpc; self.h = 2*self.L/n; self.x0 = -self.L
        ax = self.x0 + (np.arange(n) + 0.5)*self.h
        self.X, self.Y, self.Z = np.meshgrid(ax, ax, ax, indexing="ij")
        self.R = np.sqrt(self.X**2 + self.Y**2)               # cylindrical radius about the disc axis (z)
        self.r = np.sqrt(self.X**2 + self.Y**2 + self.Z**2)
        self.Rpol = np.sqrt(self.X**2 + self.Z**2)            # radius within the polar (x-z) plane
        self.solver = Poisson3D(n, self.h)
    def rho_disc(self, M, Rd_kpc, hz_kpc):
        Rd = Rd_kpc*kpc; hz = hz_kpc*kpc
        f = np.exp(-self.R/Rd)*np.exp(-np.abs(self.Z)/hz)
        return f*(M*Msun/(f.sum()*self.h**3))
    def rho_ring(self, M, Rring_kpc, w_kpc):
        Rr = Rring_kpc*kpc; w = w_kpc*kpc
        f = np.exp(-0.5*((self.Rpol - Rr)/w)**2)*np.exp(-0.5*(self.Y/w)**2)
        return f*(M*Msun/(f.sum()*self.h**3))
    def rho_point(self, M):
        rho = np.zeros_like(self.X); c = self.n//2
        rho[c, c, c] = M*Msun/self.h**3
        return rho
    def rho_nfw(self, M200, c200):
        rho_c = 3*(H0_KMS*1e3/Mpc)**2/(8*math.pi*G)
        R200 = (3*M200*Msun/(4*math.pi*200*rho_c))**(1/3.)
        rs = R200/c200
        m = lambda t: np.log1p(t) - t/(1 + t)
        rho_s = M200*Msun/(4*math.pi*rs**3*m(c200))
        x = np.maximum(self.r, 0.5*self.h)/rs
        return rho_s/(x*(1 + x)**2)
    def field(self, rho_b, a0=None, extra_rho=None):
        """Returns (gx, gy, gz) in SI.  a0=None -> pure Newtonian on rho_b (+extra_rho)."""
        rho_tot = rho_b if extra_rho is None else rho_b + extra_rho
        phiN = self.solver.solve(rho_tot)
        gx, gy, gz = [-c for c in grad3(phiN, self.h)]
        del phiN
        if a0 is None:
            return gx, gy, gz
        gN = np.sqrt(gx**2 + gy**2 + gz**2)
        w = nu(gN/a0)
        # QUMOND is  laplacian(Phi) = div[ nu grad(Phi_N) ] = -div[ nu g_N ], and the solver takes 4 pi G rho_eff
        # on the right-hand side, so rho_eff = -div(nu g_N)/(4 pi G).  (Dropping the minus sign makes the total
        # field point outward and every circular speed come out as exactly zero -- which is how the sign error in
        # the first run of this script announced itself.)
        rho_eff = -div3(w*gx, w*gy, w*gz, self.h)/(4*math.pi*G)
        del gN, w, gx, gy, gz
        phi = self.solver.solve(rho_eff); del rho_eff
        return [-c for c in grad3(phi, self.h)]
    def v_equatorial(self, gxyz, r_kpc):
        """Circular speed in the DISC plane (z = 0, azimuth-averaged) [km/s]."""
        gx, gy, gz = gxyz; out = []
        ph = np.linspace(0, 2*math.pi, 24, endpoint=False)
        for rk in np.atleast_1d(r_kpc):
            r = rk*kpc
            pts = np.stack([r*np.cos(ph), r*np.sin(ph), np.zeros_like(ph)], axis=-1)
            gr = (interp3(gx, pts, self.x0, self.h)*np.cos(ph) + interp3(gy, pts, self.x0, self.h)*np.sin(ph))
            out.append(math.sqrt(max(-float(np.mean(gr))*r, 0.0))/1e3)
        return np.array(out)
    def v_polar(self, gxyz, r_kpc):
        """Circular speed in the POLAR (x-z) plane at spherical radius r, averaged around the ring [km/s].
        v^2 = <-r g_r>, the standard definition used to compare a polar ring with the host disc."""
        gx, gy, gz = gxyz; out = []
        th = np.linspace(0, 2*math.pi, 24, endpoint=False)
        for rk in np.atleast_1d(r_kpc):
            r = rk*kpc
            pts = np.stack([r*np.sin(th), np.zeros_like(th), r*np.cos(th)], axis=-1)
            gr = (interp3(gx, pts, self.x0, self.h)*np.sin(th) + interp3(gz, pts, self.x0, self.h)*np.cos(th))
            out.append(math.sqrt(max(-float(np.mean(gr))*r, 0.0))/1e3)
        return np.array(out)

P("="*122); P("PART 0 -- is the ring-versus-disc kinematic table available?"); P("="*122)
info("The item points at Iodice et al. 2003 (A&A 404, 921) and Khoperskov.  Checked this session on the VizieR CfA")
info("mirror: J/A+A/404/921 returns no table -- that paper was never deposited at CDS.  The SDSS-based Polar Ring")
info("Catalogue (Moiseev et al. 2011, J/MNRAS/418/244) IS there but carries only positions, r magnitudes and a")
info("systemic velocity: no rotation curves.  Combes et al. 2013 (J/A+A/554/A11) adds CO spectra and systemic")
info("velocities, again no ring-versus-disc rotation.  So the ratio the item asks for cannot be measured from")
info("machine-readable data here.  What IS deposited is an HI survey of the Whitmore et al. 1990 Polar Ring")
info("Catalogue objects with 20% line widths (J/A+A/319/401), and that is what PART 2 uses.")
ck("49a NOT RUNNABLE AS POSED -- the per-system ring and disc rotation velocities the item needs are not in any "
   "machine-readable archive reachable from here.  The polar-ring catalogues that ARE deposited carry photometry "
   "and systemic velocities only.  A data-availability result, not a null",
   True, "VizieR J/A+A/404/921 empty; J/MNRAS/418/244 and J/A+A/554/A11 carry no rotation velocities; "
         "J/A+A/319/401 carries HI 20% line widths and is used in PART 2")

P(""); P("="*122); P("PART 1 -- what the framework actually predicts, from a 3-D QUMOND solve"); P("="*122)
N_GRID, L_BOX = 128, 100.0
mod = Model(n=N_GRID, L_kpc=L_BOX)
info(f"grid {N_GRID}^3 over +/-{L_BOX:.0f} kpc (cell {2*L_BOX/N_GRID:.2f} kpc), isolated-boundary FFT Poisson, "
     f"Route A kernel nu(y) = 1/(1-exp(-sqrt(y)))")

# --- validation: a point mass must reproduce the algebraic MOND solution exactly (spherical symmetry, no curl field)
M_PT = 5e10
gpt = mod.field(mod.rho_point(M_PT), a0=A0["canonical"])
rr = np.array([15.0, 25.0, 40.0, 60.0])
v_num = mod.v_equatorial(gpt, rr)
gN_an = G*M_PT*Msun/(rr*kpc)**2
v_an = np.sqrt(nu(gN_an/A0["canonical"])*gN_an*(rr*kpc))/1e3
info(f"{'r [kpc]':>9} {'v numeric':>11} {'v analytic':>11} {'ratio':>8}   (point mass, spherical: the solver must "
     f"reproduce the closed form)")
for a, b, c_ in zip(rr, v_num, v_an):
    info(f"{a:9.0f} {b:11.2f} {c_:11.2f} {b/c_:8.4f}")
err_pt = float(np.max(np.abs(v_num/v_an - 1)))
del gpt
ck("49b solver validation: in spherical symmetry QUMOND reduces exactly to v^2 = nu(g_N/a_0) g_N r, so the "
   "three-dimensional solve must reproduce the closed form.  If it does not, nothing else in PART 1 means anything",
   err_pt < 0.03, f"maximum error over r = 15-60 kpc: {100*err_pt:.2f}%")

# --- the configuration: an S0 host disc plus a massive polar ring, the standard PRG geometry
M_DISC, RD, HZ = 3.0e10, 3.0, 0.5          # Msun, kpc, kpc -- an S0 host
M_RING, R_RING, W_RING = 1.0e10, 20.0, 3.0  # Msun, kpc, kpc -- the ring, gas-rich and at 6-7 disc scale lengths
rho_d = mod.rho_disc(M_DISC, RD, HZ)
rho_r = mod.rho_ring(M_RING, R_RING, W_RING)
MB_TOT = M_DISC + M_RING
info("")
info(f"configuration: exponential host disc M = {M_DISC:.1e} Msun, R_d = {RD} kpc, h_z = {HZ} kpc (x-y plane);")
info(f"               polar ring M = {M_RING:.1e} Msun at R = {R_RING} kpc, width {W_RING} kpc (x-z plane)")

radii = np.array([8.0, 12.0, 16.0, 20.0, 25.0, 30.0, 40.0, 55.0, 70.0])
RES = {}
for ft, a0 in A0.items():
    g_all = mod.field(rho_d + rho_r, a0=a0)
    RES[(ft, "both")] = (mod.v_equatorial(g_all, radii), mod.v_polar(g_all, radii)); del g_all
    g_dsk = mod.field(rho_d, a0=a0)
    RES[(ft, "disconly")] = (mod.v_equatorial(g_dsk, radii), mod.v_polar(g_dsk, radii)); del g_dsk
g_newt = mod.field(rho_d + rho_r, a0=None)
RES[("newton", "both")] = (mod.v_equatorial(g_newt, radii), mod.v_polar(g_newt, radii)); del g_newt
# The fair alternative: a SPHERICAL NFW halo normalised so that its EQUATORIAL rotation speed at the ring radius
# equals the framework's.  Same observable rotation curve in the disc plane, different answer in the polar plane --
# which is the only way to ask whether a polar ring can tell the two apart.  Bisected, not guessed.
v_target = float(RES[("canonical", "both")][0][list(radii).index(R_RING)])
lo, hi = 10.0, 13.5
for _ in range(14):
    mid_ = 0.5*(lo + hi)
    gtest = mod.field(rho_d + rho_r, a0=None, extra_rho=mod.rho_nfw(10**mid_, 10.0))
    vt = float(mod.v_equatorial(gtest, [R_RING])[0]); del gtest
    if vt < v_target: lo = mid_
    else: hi = mid_
M200 = 10**(0.5*(lo + hi))
g_nfw = mod.field(rho_d + rho_r, a0=None, extra_rho=mod.rho_nfw(M200, 10.0))
RES[("nfw", "both")] = (mod.v_equatorial(g_nfw, radii), mod.v_polar(g_nfw, radii)); del g_nfw
info(f"the spherical NFW comparison halo is M200 = {M200:.2e} Msun, c = 10, bisected so that its equatorial speed "
     f"at r = {R_RING:.0f} kpc matches the framework's {v_target:.1f} km/s "
     f"(it gives {RES[('nfw','both')][0][list(radii).index(R_RING)]:.1f})")

info("")
info(f"{'r [kpc]':>8} | {'framework (disc+ring)':>28} | {'framework (disc only)':>28} | "
     f"{'Newton baryons':>22} | {'Newton + spherical NFW':>24}")
info(f"{'':>8} | {'v_eq':>8}{'v_pol':>8}{'ratio':>8}   | {'v_eq':>8}{'v_pol':>8}{'ratio':>8}   | "
     f"{'v_eq':>7}{'v_pol':>7}{'ratio':>7}  | {'v_eq':>8}{'v_pol':>8}{'ratio':>7}")
for i, rk in enumerate(radii):
    a_eq, a_po = RES[("canonical", "both")]; b_eq, b_po = RES[("canonical", "disconly")]
    c_eq, c_po = RES[("newton", "both")]; d_eq, d_po = RES[("nfw", "both")]
    info(f"{rk:8.0f} | {a_eq[i]:8.1f}{a_po[i]:8.1f}{a_po[i]/a_eq[i]:8.3f}   | "
         f"{b_eq[i]:8.1f}{b_po[i]:8.1f}{b_po[i]/b_eq[i]:8.3f}   | "
         f"{c_eq[i]:7.1f}{c_po[i]:7.1f}{c_po[i]/c_eq[i]:7.3f}  | "
         f"{d_eq[i]:8.1f}{d_po[i]:8.1f}{d_po[i]/d_eq[i]:7.3f}")

i_ring = list(radii).index(R_RING)
ratio_fw = float(RES[("canonical", "both")][1][i_ring]/RES[("canonical", "both")][0][i_ring])
ratio_do = float(RES[("canonical", "disconly")][1][i_ring]/RES[("canonical", "disconly")][0][i_ring])
ratio_nw = float(RES[("newton", "both")][1][i_ring]/RES[("newton", "both")][0][i_ring])
ratio_nfw = float(RES[("nfw", "both")][1][i_ring]/RES[("nfw", "both")][0][i_ring])
ck("49c 🔴 THE ITEM'S PREDICTION IS WITHDRAWN AND REPLACED.  The item says the framework predicts the ring FASTER "
   "than the disc.  It does not: the phantom of a disc is flattened TOWARD the disc, so at the ring's radius the "
   "polar circular speed is BELOW the equatorial one.  'Ring faster than disc' is the observers' inference about a "
   "dark halo flattened toward the polar plane, and it is the OPPOSITE of what the framework says",
   ratio_fw < 1.0 and ratio_do < 1.0,
   f"at r = {R_RING:.0f} kpc: v_pol/v_eq = {ratio_fw:.3f} for the disc+ring baryons and {ratio_do:.3f} for the host "
   f"disc alone; Newtonian baryons give {ratio_nw:.3f}; a spherical NFW halo matched to the same equatorial speed "
   f"gives {ratio_nfw:.3f}")
ck("49c2 ⚠ AND THE DISCRIMINANT IS SMALLER THAN THE ITEM'S OWN BAR.  Against a spherical halo matched to the same "
   "equatorial rotation speed -- the fair comparison -- the framework's extra polar-plane suppression is a few per "
   "cent, not the 10% the hunt list set as the pass threshold.  So even with perfect ring-and-disc data, 'ratio "
   "within 10% for 5+ systems' would not decide anything; the measurement has to be good to about 2%",
   abs(ratio_fw - ratio_nfw) < 0.10,
   f"framework {ratio_fw:.3f} against a matched spherical halo {ratio_nfw:.3f}: a discriminant of "
   f"{100*abs(ratio_fw-ratio_nfw):.1f}% in velocity, against the item's 10% bar")

# --- the asymptotic BTFR limit and the finite-radius correction that PART 2 needs
v_btfr = {ft: (G*MB_TOT*Msun*a0)**0.25/1e3 for ft, a0 in A0.items()}
f_ring = {ft: float(RES[(ft, "both")][1][i_ring]/v_btfr[ft]) for ft in A0}
f_eq = {ft: float(RES[(ft, "both")][0][i_ring]/v_btfr[ft]) for ft in A0}
info("")
for ft in A0:
    info(f"{ft:10}: (G M_b a_0)^(1/4) = {v_btfr[ft]:.1f} km/s;  v_pol({R_RING:.0f} kpc) = "
         f"{RES[(ft,'both')][1][i_ring]:.1f} km/s  ->  f_ring = {f_ring[ft]:.3f};  "
         f"v_eq = {RES[(ft,'both')][0][i_ring]:.1f} -> f_eq = {f_eq[ft]:.3f}")
far = RES[("canonical", "both")]
info(f"at r = {radii[-1]:.0f} kpc the two planes have converged to {far[1][-1]/far[0][-1]:.3f} of each other and to "
     f"{far[1][-1]/v_btfr['canonical']:.3f} of the asymptotic BTFR speed -- the field goes spherical, as it must.")
ck("49d THE PREDICTION THAT IS TESTABLE: a polar ring must sit on the ORDINARY baryonic Tully-Fisher relation with "
   "the ordinary a_0, because the framework's field becomes spherical far from any baryon distribution whatever its "
   "shape.  The finite-radius correction at a realistic ring radius is small and is computed here rather than "
   "assumed, so PART 2 uses a number and not the bare asymptote.  A dark halo of adjustable flattening makes no "
   "such prediction -- which is precisely why the literature uses polar rings to MEASURE halo shape",
   0.75 < f_ring["canonical"] < 1.15 and abs(far[1][-1]/far[0][-1] - 1) < 0.10,
   f"f_ring = v_pol(R_ring)/(G M_b a_0)^(1/4) = {f_ring['canonical']:.3f} (canonical), {f_ring['alt']:.3f} (alt); "
   f"the two planes agree to {100*abs(far[1][-1]/far[0][-1]-1):.1f}% by r = {radii[-1]:.0f} kpc")

# --- resolution control
mod2 = Model(n=96, L_kpc=L_BOX)
g2 = mod2.field(mod2.rho_disc(M_DISC, RD, HZ) + mod2.rho_ring(M_RING, R_RING, W_RING), a0=A0["canonical"])
r2 = float(mod2.v_polar(g2, [R_RING])[0]/mod2.v_equatorial(g2, [R_RING])[0])
f2 = float(mod2.v_polar(g2, [R_RING])[0]/v_btfr["canonical"])
del g2, mod2
ck("M1 resolution control: the item-71 lesson was that a coarse grid can invent (or hide) the answer, so the whole "
   "of PART 1 is recomputed at 96^3 and must give the same numbers",
   abs(r2 - ratio_fw) < 0.03 and abs(f2 - f_ring["canonical"]) < 0.03,
   f"96^3 vs 128^3: v_pol/v_eq {r2:.3f} vs {ratio_fw:.3f}; f_ring {f2:.3f} vs {f_ring['canonical']:.3f}")

# --- mutation control: with a_0 x 100 the ring speed must move by the predicted 0.5 dex, and with nu = 1 the
#     configuration must collapse onto the Newtonian answer
g_big = mod.field(rho_d + rho_r, a0=100*A0["canonical"])
v_big = float(mod.v_polar(g_big, [R_RING])[0]); del g_big
v_now = float(RES[("canonical", "both")][1][i_ring])
ck("M2 mutation control: a_0 x 100 must raise the ring speed by 0.5 dex in the deep-MOND part of the answer.  It "
   "cannot be the full 0.5 because at 20 kpc the ring is not fully in the deep regime -- the measured shift is the "
   "check that the solver is responding to a_0 at all and by roughly the right amount",
   0.15 < math.log10(v_big/v_now) < 0.50,
   f"log10(v_ring(100 a_0)/v_ring(a_0)) = {math.log10(v_big/v_now):+.3f} (deep-MOND limit +0.500, Newtonian limit 0)")
del rho_d, rho_r

# =====================================================================================================================
P(""); P("="*122); P("PART 2 -- the polar-ring BTFR on real data"); P("="*122)
# =====================================================================================================================
info("Huchtmeier 1997, 'HI survey of polar ring galaxies II' (VizieR J/A+A/319/401 table1), fetched this session to")
info("real_research/data/prg_huchtmeier1997_hi_table1.tsv: Whitmore et al. 1990 Polar Ring Catalogue identifier,")
info("total blue magnitude, HI flux, HI systemic velocity and the 20% line width, for 44 objects.")
info("PRC classes: A = kinematically CONFIRMED polar ring; B = good candidate; C = possible candidate;")
info("             D = possibly related object (mergers, peculiars -- not polar rings).")
info("THE LOAD-BEARING ASSUMPTION, stated up front: in a polar-ring galaxy the HI lies overwhelmingly in the RING,")
info("not in the gas-poor early-type host, so W20 measures the RING's rotation.  That is the standard reading of")
info("these observations and it is why the survey was done; it is also what makes this a test of item 49 at all.")
info("The ring is assumed edge-on (sin i = 1), which is how PRC objects are recognised.  Any i < 90 deg would raise")
info("the inferred rotation speed, so every velocity below is a LOWER bound.")

rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "prg_huchtmeier1997_hi_table1.tsv"),
                                                 encoding="latin-1") if l.strip() and not l.startswith("#")]
hdr = [h.strip() for h in rows[0]]
def _f(v):
    try: return float(v)
    except Exception: return float("nan")
recs = []
for r in rows[3:]:
    d = {hdr[i]: (r[i].strip() if i < len(r) else "") for i in range(len(hdr))}
    w20, bt, shi, vhi = _f(d["dv20"]), _f(d["BT"]), _f(d["SHI"]), _f(d["VHI"])
    if not (np.isfinite(w20) and np.isfinite(bt) and np.isfinite(shi) and np.isfinite(vhi)): continue
    if vhi < CZ_MIN: continue
    cls = d["PRC"][:1]
    D = vhi/H0_KMS
    MHI = 2.356e5*D**2*shi
    MB_abs = bt - 5*math.log10(D) - 25.0
    LB = 10**(0.4*(MB_SUN - MB_abs))
    wc = math.sqrt(max(w20**2 - (2*W_TURB)**2, 1.0))
    recs.append(dict(prc=d["PRC"], name=d["Name"], cls=cls, mtype=d["MType"], D=D, w20=w20, vrot=wc/2.0,
                     MHI=MHI, LB=LB))
info("")
info(f"{'PRC':6}{'name':12}{'type':6}{'D [Mpc]':>9}{'W20':>7}{'V_ring':>8}{'M_HI [1e9]':>12}{'L_B [1e9]':>11}")
for r_ in sorted(recs, key=lambda z: z["cls"]):
    info(f"{r_['prc']:6}{r_['name']:12}{r_['mtype']:6}{r_['D']:9.1f}{r_['w20']:7.0f}{r_['vrot']:8.1f}"
         f"{r_['MHI']/1e9:12.2f}{r_['LB']/1e9:11.2f}")
gold = [r_ for r_ in recs if r_["cls"] in ("A", "B")]
info(f"objects with W20, B magnitude, HI flux and cz > {CZ_MIN:.0f} km/s: {len(recs)};  "
     f"of those PRC class A or B (confirmed + good candidates): {len(gold)}")
ck("49e UNDERPOWERED ON THE GOLD SAMPLE, and this is the item's real limit.  The hunt list asks for 5 or more "
   "systems agreeing to 10%.  The number of KINEMATICALLY CONFIRMED or good-candidate polar rings with a published "
   "HI line width, a blue magnitude and a usable flow distance in the whole deposited literature is smaller than "
   "that.  The extended sample below is dominated by PRC classes C and D, which are candidates and 'related "
   "objects' (mergers and peculiars), not polar rings",
   len(gold) < 5,
   f"{len(gold)} class A+B objects against the {len(recs)} total; the rest are class C ({sum(1 for r_ in recs if r_['cls']=='C')}) "
   f"and class D ({sum(1 for r_ in recs if r_['cls']=='D')})")

# --- the BTFR test
def offsets(sample, ups, a0, fcorr):
    lv, lp = [], []
    for r_ in sample:
        Mb = 1.33*r_["MHI"] + ups*r_["LB"]
        vp = fcorr*(G*Mb*Msun*a0)**0.25/1e3
        lv.append(math.log10(r_["vrot"])); lp.append(math.log10(vp))
    return np.array(lv) - np.array(lp)

info("")
info(f"the framework's parameter-free prediction: V_ring = f_ring x (G M_b a_0)^(1/4) with f_ring from PART 1, "
     f"M_b = 1.33 M_HI + Upsilon_B L_B")
info(f"{'sample':>16}{'N':>4}{'footing':>12}{'Ups_B':>8}{'median offset [dex]':>22}{'rms':>8}")
OFF = {}
for name, sample in (("PRC A+B", gold), ("all classes", recs)):
    for ft, a0 in A0.items():
        for ups in (0.8, 1.5, 3.0):
            o = offsets(sample, ups, a0, f_ring[ft])
            OFF[(name, ft, ups)] = o
            info(f"{name:>16}{len(sample):4d}{ft:>12}{ups:8.1f}{float(np.median(o)):16.3f}      "
                 f"{float(np.std(o)):8.3f}")

# --- what the framework REQUIRES of the stellar M/L (the item-76 inversion, applied to polar rings)
info("")
info("inverted: with a_0 fixed by Lambda, the ring speed and the HI mass PREDICT the host's stellar M/L")
for name, sample in (("PRC A+B", gold), ("all classes", recs)):
    for ft, a0 in A0.items():
        ups_req = []
        for r_ in sample:
            Mreq = (r_["vrot"]*1e3/f_ring[ft])**4/(G*a0)/Msun
            ups_req.append((Mreq - 1.33*r_["MHI"])/r_["LB"])
        ups_req = np.array(ups_req)
        info(f"  {name:>12} {ft:>10}: required Upsilon_B = median {np.median(ups_req):6.2f}, "
             f"16-84 pct [{np.percentile(ups_req,16):.2f}, {np.percentile(ups_req,84):.2f}], "
             f"{int(np.sum(ups_req < 0))}/{len(ups_req)} negative (i.e. the HI alone already over-predicts)")
        if name == "PRC A+B" and ft == "canonical": UPS_REQ_GOLD = ups_req

o_gold = OFF[("PRC A+B", "canonical", UPS_B)]
o_all = OFF[("all classes", "canonical", UPS_B)]
med_g, rms_g = float(np.median(o_gold)), float(np.std(o_gold))
med_a, rms_a = float(np.median(o_all)), float(np.std(o_all))
sem_g = rms_g/math.sqrt(max(len(o_gold), 1))
lpred_all = np.array([math.log10(f_ring["canonical"]*(G*(1.33*r_["MHI"] + UPS_B*r_["LB"])*Msun*A0["canonical"])**0.25/1e3)
                      for r_ in recs])
lobs_all = np.array([math.log10(r_["vrot"]) for r_ in recs])
spread_pred, spread_obs = float(np.std(lpred_all)), float(np.std(lobs_all))
info("")
info(f"THE LEVER, before any conclusion is drawn from the numbers above: across these {len(recs)} objects the "
     f"PREDICTED velocity varies by only {spread_pred:.3f} dex (rms), because M_b spans "
     f"{np.log10(np.array([1.33*r_['MHI'] + UPS_B*r_['LB'] for r_ in recs])).ptp():.2f} dex and the BTFR compresses "
     f"that by a factor of four.  The OBSERVED velocities scatter by {spread_obs:.3f} dex.  A Tully-Fisher "
     f"correlation cannot be detected when the signal is {spread_pred/spread_obs:.2f} of the scatter.")
ck("49f 🔴 AGAINST INTEREST -- THE BTFR TEST IS NOT A TEST ON THIS SAMPLE.  The offset can be quoted, but the "
   "sample cannot demonstrate the Tully-Fisher correlation: the predicted velocity varies over a range two and a "
   "half times smaller than the observed scatter, because taking a fourth root of a 1.3 dex mass range leaves "
   "almost no lever.  What follows is therefore a ZERO-POINT statement -- the mean ratio of measured to predicted "
   "speed -- and not a demonstration that polar rings obey the relation",
   spread_pred < 0.7*spread_obs,
   f"predicted-velocity spread {spread_pred:.3f} dex against an observed scatter of {spread_obs:.3f} dex; "
   f"zero point: PRC A+B (N = {len(o_gold)}, canonical, Upsilon_B = {UPS_B}) median offset {med_g:+.3f} dex "
   f"({100*(10**med_g - 1):+.0f}% in velocity), s.e.m. {sem_g:.3f}; all {len(o_all)} objects "
   f"{med_a:+.3f} +/- {rms_a/math.sqrt(len(o_all)):.3f} dex")

# --- the control: the same law on ordinary discs
gals = load_sparc()
lv_s = np.array([math.log10(g["Vflat"]) for g in gals if g["Vflat"] > 0])
lm_s = np.array([math.log10(g["Mb"]) for g in gals if g["Vflat"] > 0])
lp_s = np.array([math.log10((G*10**m*Msun*A0["canonical"])**0.25/1e3) for m in lm_s])
o_s = lv_s - lp_s
info("")
info(f"CONTROL -- the same zero-parameter BTFR on {len(o_s)} ordinary SPARC discs (V_flat, M_b = 0.5 L_3.6 + 1.33 "
     f"M_HI, no f_ring correction because V_flat is already the asymptote): median offset {np.median(o_s):+.3f} dex, "
     f"rms {np.std(o_s):.3f}")
info("CAVEAT ON THAT COMPARISON, because it is not as clean as it looks: the polar rings carry a B-band stellar "
     "mass with Upsilon_B assumed and the SPARC discs a 3.6-micron one with Upsilon = 0.5, so the two zero points "
     "sit in different M/L systems and their agreement is partly a coincidence of those two choices.  What is "
     "robust is the SIZE of the difference relative to the polar-ring scatter, not its being near zero.")
ck("49g the comparison that matters is not to zero but to ORDINARY DISCS analysed with the same law.  A polar ring "
   "offset that matches the disc offset means the ring behaves like a disc of the same baryonic mass, which is the "
   "framework's claim; a difference between them is the signal the item was after",
   abs(med_g - float(np.median(o_s))) < 0.15,
   f"polar rings {med_g:+.3f} dex vs SPARC discs {float(np.median(o_s)):+.3f} dex -- a difference of "
   f"{med_g - float(np.median(o_s)):+.3f} dex, against a polar-ring s.e.m. of {sem_g:.3f} and a polar-ring rms of "
   f"{rms_g:.3f}")

# --- mutation controls on PART 2
P(""); P("-"*122); P("MUTATION CONTROLS on PART 2"); P("-"*122)
o_x100 = offsets(recs, UPS_B, 100*A0["canonical"], f_ring["canonical"])
ck("M3 mutation control: a_0 x 100 must move the BTFR offset by exactly 0.5 dex (v ~ a_0^1/4).  If the offset does "
   "not respond, 49f is measuring nothing",
   abs((float(np.median(o_all)) - float(np.median(o_x100))) - 0.5) < 0.02,
   f"median offset {float(np.median(o_all)):+.3f} -> {float(np.median(o_x100)):+.3f} dex, a shift of "
   f"{float(np.median(o_all)) - float(np.median(o_x100)):+.3f} (predicted +0.500)")
def scramble_ratio(idx):
    sub = [recs[i] for i in idx]
    pm = rng.permutation(len(sub))
    o_r = offsets(sub, UPS_B, A0["canonical"], f_ring["canonical"])
    o_s = offsets([dict(sub[i], vrot=sub[pm[i]]["vrot"]) for i in range(len(sub))], UPS_B,
                  A0["canonical"], f_ring["canonical"])
    return float(np.std(o_s))/float(np.std(o_r))
ratio_obs = float(np.mean([scramble_ratio(np.arange(len(recs))) for _ in range(60)]))
ratio_bs = np.array([scramble_ratio(rng.integers(0, len(recs), len(recs))) for _ in range(200)])
# under a PERFECT relation the scramble removes the full covariance: var(o_scr) = var(o) + 2 var(pred)
ratio_perfect = math.sqrt(1 + 2*spread_pred**2/rms_a**2)
ck("M4 mutation control, AND IT IS THE ONE THAT SIZES 49f: scrambling which rotation speed belongs to which galaxy "
   "must inflate the residual scatter by a known amount if the relation is really there.  The observed inflation "
   "sits between 'no relation at all' and 'the relation holds exactly', and its bootstrap error covers both -- so "
   "this control cannot tell the two apart either.  Everything in PART 2 is a zero point, not a relation",
   abs(ratio_obs - 1.0) < 3*float(np.std(ratio_bs)) or abs(ratio_obs - ratio_perfect) < 3*float(np.std(ratio_bs)),
   f"rms of the offset inflates from {rms_a:.3f} dex to {ratio_obs*rms_a:.3f} dex on scrambling, a ratio of "
   f"{ratio_obs:.3f} +/- {float(np.std(ratio_bs)):.3f} (bootstrap) against 1.000 for no relation and "
   f"{ratio_perfect:.3f} for an exact one")
lv_r = np.array([math.log10(r_["vrot"]) for r_ in recs])
lm_r = np.array([math.log10(1.33*r_["MHI"] + UPS_B*r_["LB"]) for r_ in recs])
sl_r = float(np.polyfit(lm_r, lv_r, 1)[0])
n_b = 400; sls = []
for _ in range(n_b):
    j = rng.integers(0, len(recs), len(recs))
    sls.append(float(np.polyfit(lm_r[j], lv_r[j], 1)[0]))
esl = float(np.std(sls))
ck("M5 estimator control, same verdict from the other direction: the framework's BTFR has slope exactly 1/4 in "
   "log V vs log M_b.  The measured slope is consistent with 1/4 -- and equally consistent with ZERO, i.e. with no "
   "relation at all.  Two independent controls therefore say the same thing: this sample cannot test the relation, "
   "only its zero point",
   abs(sl_r - 0.25) < 3*esl and abs(sl_r)/esl < 3.0,
   f"measured d log V_ring / d log M_b = {sl_r:.3f} +/- {esl:.3f} (bootstrap): {abs(sl_r-0.25)/esl:.1f} sigma from "
   f"the predicted 0.250 and {abs(sl_r)/esl:.1f} sigma from zero")

# --- estimator validation against the paper's own derived quantities
t2rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "prg_huchtmeier1997_derived_table2.tsv"),
                                                   encoding="latin-1") if l.strip() and not l.startswith("#")]
h2 = [x.strip() for x in t2rows[0]]
pub = {}
for r in t2rows[3:]:
    dd = {h2[i]: (r[i].strip() if i < len(r) else "") for i in range(len(h2))}
    pub[dd["PRC"]] = (_f(dd["MHI"]), _f(dd["LB"]))
dm, dl, H0_PAPER = [], [], 75.0
for r_ in recs:
    if r_["prc"] not in pub: continue
    mhi_p, lb_p = pub[r_["prc"]]
    if not (np.isfinite(mhi_p) and np.isfinite(lb_p) and mhi_p > 0 and lb_p > 0): continue
    s = (H0_KMS/H0_PAPER)**2                      # both M_HI and L_B scale as D^2
    dm.append(math.log10(r_["MHI"]*s/(mhi_p*1e9))); dl.append(math.log10(r_["LB"]*s/(lb_p*1e9)))
ck("M6 estimator validation on the paper's own numbers: this script recomputes M_HI from the HI flux and L_B from "
   "the blue magnitude and its own distance, rather than taking the catalogue's derived columns.  Rescaled to the "
   "paper's Hubble constant those recomputations must reproduce its published values, or the whole of PART 2 is "
   "built on an arithmetic error",
   len(dm) >= 8 and abs(float(np.median(dm))) < 0.06 and abs(float(np.median(dl))) < 0.10,
   f"N = {len(dm)} objects in both tables: median log10(mine/published) = {float(np.median(dm)):+.3f} for M_HI and "
   f"{float(np.median(dl)):+.3f} for L_B after rescaling from H0 = {H0_KMS} to the paper's {H0_PAPER:.0f}")

P(""); P("-"*122)
info("SYSTEMATICS, stated plainly:")
info(" 1. THE RING/HOST GAS SPLIT.  If part of the HI sits in the host rather than the ring, W20 mixes two")
info("    kinematic systems and V_ring is wrong in an uncontrolled direction.  Single-dish data cannot separate")
info("    them; resolved HI synthesis maps can, and exist for a handful of objects only.")
info(" 2. INCLINATION.  sin i = 1 is assumed.  Any real inclination raises V_ring, so the offsets above are")
info("    LOWER bounds on the ring speed and the framework's requirement is at its easiest here.")
info(" 3. B-band magnitudes are not extinction-corrected in this table and PRC hosts are seen through their own")
info("    rings.  Under-corrected extinction lowers L_B, lowers M_b, and lowers the predicted velocity.")
info(f" 4. Upsilon_B is the wall, exactly as in items 2/65/66/76: over 0.8 to 3.0 the predicted velocity moves by")
info(f"    {0.25*math.log10(3.0/0.8):.3f} dex when the stars dominate, which is the size of the whole signal.")
info(" 5. flow distances from cz/H0 with no peculiar-velocity model; the cz > 1500 km/s cut keeps this near 10%,")
info("    which is 0.05 dex in M_b at fixed flux and 0.012 dex in the predicted velocity.")
info(" 6. PRC classes C and D are candidates and related objects, NOT confirmed polar rings.  Any statement made")
info("    on the 'all classes' sample is a statement about peculiar galaxies in general.")
P("")
info("WHAT WOULD MAKE ITEM 49 DECISIVE:")
info(" 1. resolved HI or ionised-gas rotation curves for both components of 5+ confirmed polar rings -- these")
info("    exist in the literature (NGC 4650A and a handful of others) but are not deposited anywhere machine-")
info("    readable, which is finding 49a.  With them, PART 1's v_pol/v_eq prediction becomes a 3-sigma test.")
info(" 2. the SIGN is the whole point and it is free of every systematic above: the framework says the polar")
info("    plane rotates SLOWER than the disc plane at the same radius, a dark halo flattened toward the polar")
info("    plane says faster.  A single well-measured system with both curves settles the direction.")
sys.exit(ck.done())
