#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""hunt_efe_lib.py -- a QUMOND external-field solver shared by hunt items 74, 75, 81, 82, 83, 98.
(predictions_2026/SECOND_LAW_HUNT_2026.md; run this file directly for its own validation suite, exit 0 = clean.)

WHY THIS EXISTS.  The one-line "algebraic" external-field prescription everyone reaches for first,

    g_rel(x) = nu(|g_N,b(x) + g_N,ext|/a0) (g_N,b(x) + g_N,ext)  -  nu(e) g_N,ext          [NOT a solution]

is not a solution of any MOND field equation, and it fails in a specific and violent way: it leaves a
UNIFORM residual force of order nu(e) e a0 = a0 sqrt(e) inside the galaxy, because the first term boosts
the external field only by nu(y) ~ 1 where the internal field is strong.  At e = 0.01 that is 0.1 a0
against a 0.37 a0 outer disc -- a ~30% lopsidedness where real discs are lopsided at ~10%.  The same
prescription applied to the solar system inside the Milky Way's ~2 a0 field predicts a uniform a0/2
anomalous acceleration that planetary ephemerides exclude by three orders of magnitude.  This module
solves QUMOND instead, and V4 below MEASURES that uniform residual rather than assuming it either way.

WHAT IS SOLVED.  QUMOND:  lap(phi) = div[ nu(|grad phi_N|/a0) grad phi_N ],  g = -grad phi.  With
g_N = g_N,baryon + g_N,ext and g_N,ext UNIFORM, the uniform piece contributes nothing to the source (its
divergence vanishes) and enters only through the boundary condition phi -> -nu(e) g_N,ext . x.  Since
g_N = -grad(phi_N) gives div g_N = -4 pi G rho, the phantom source is

    4 pi G rho_ph = - div[ (nu(|g_N|/a0) - 1) g_N ]

(the minus sign is derived, not guessed: the first version of this module dropped it and V1 failed by a
factor 1.7, so V1 is kept precisely so that a sign error cannot pass silently).

GEOMETRY.  Baryons = point mass M.  Lengths in the MOND radius r_M = sqrt(GM/a0), accelerations in a0, so
g_N,b(r) = -1/r^2 and the WHOLE problem has ONE parameter, e = g_N,ext/a0.  g_ext points along +z, the
configuration is axisymmetric about it, rho_ph is expanded in Legendre polynomials in mu = cos(theta) and
each multipole is integrated with the exact radial Green's function.  (A Plummer baryon sphere was tried
first and had to be abandoned: its central field VANISHES, which manufactures a second, inner stagnation
sphere at r = e/Y that no affordable grid resolves, and the l=1 integral then returns garbage that varies
by a factor 10 with the baryon scale.  Recorded because it looked like physics -- an "extra pull on the
centre of mass" -- and was not.)

WHAT THE ROTATION CURVE MEASURES: the acceleration of a star relative to the galaxy's own centre of mass,
g_rel(x) = g_N,b(x) + g_ph(x) - g_ph(0).  V4 finds g_ph(0) = 0 to 1e-5 a0 across e = 0.001-0.3, i.e. the
centre of mass falls at exactly the external MOND field nu(e) g_N,ext and there is NO uniform residual.

ANALYTIC FAR-FIELD CHECK (V2/V3, derived here so the validation has teeth).  Linearising QUMOND about a
uniform external field for a point mass, with L(e) = d ln nu / d ln y at y = e:

    lap(phi) = nu(e)[ 4 pi G rho + L d^2 phi_N,b/dz^2 ],   d^2(-GM/r)/dz^2 = -2GM P_2(mu)/r^3 + (4 pi GM/3) delta^3
    =>  phi = -nu(e)(GM/r)[ 1 + L/3 - (L/3) P_2(mu) ]
    =>  g_r/g_N,b,r -> nu(e)[1 + L/3 - (L/3) P_2(mu)]   and   M_ph/M_b -> (nu(e)-1) + nu(e) L(e)/3.

The naive M_ph -> (nu(e)-1) M_b is WRONG by 22-30%: it misses the delta-function trace of the anisotropic
term.  V3 tests the corrected form.
"""
import math
import numpy as np

G = 6.674e-11
Msun = 1.989e30
kpc = 3.0857e19
Mpc = 3.0857e22


def nu(y):
    y = np.maximum(np.asarray(y, dtype=float), 1e-14)
    return 1.0/(1.0 - np.exp(-np.sqrt(y)))


def nu_s(y):
    y = max(float(y), 1e-14)
    return 1.0/(1.0 - math.exp(-math.sqrt(y)))


def dlnnu_dlny(y):
    """L(y) = d ln nu / d ln y for Route A; L -> -1/2 deep-MOND, -> 0 Newtonian."""
    y = np.maximum(np.asarray(y, dtype=float), 1e-14)
    s = np.sqrt(y); ex = np.exp(-s)
    return -0.5*s*ex/(1.0 - ex)


class EFESolve:
    """QUMOND point mass in a uniform external Newtonian field of strength e = g_N,ext/a0.
    Lengths in r_M = sqrt(GM/a0); accelerations in a0; g_ext along +z."""

    def __init__(self, e, nr=3000, nth=200, lmax=16, rmin=1e-3, rmax=1e5):
        self.e = float(e); self.lmax = int(lmax)
        self.r = np.geomspace(rmin, rmax, nr)
        x, w = np.polynomial.legendre.leggauss(nth)
        self.mu = x; self.w = w
        R = self.r[:, None]; MU = self.mu[None, :]
        ST = np.sqrt(np.maximum(1.0 - MU**2, 0.0))
        gr = -1.0/R**2 + self.e*MU
        gt = 0.0*R - self.e*ST
        f = nu(np.sqrt(gr**2 + gt**2)) - 1.0
        hr = f*gr; ht = f*gt
        div = np.gradient(R**2*hr, self.r, axis=0)/R**2
        div = div - np.gradient(ST*ht, self.mu, axis=1)/R
        self.src = -div                                      # = 4 pi G rho_ph
        self.rho_ph = self.src/(4*np.pi)                     # in units a0/(G r_M) -- Sigma_M = a0/(2 pi G)
        self._solve()
        self.u = self._uniform()

    def _solve(self):
        r = self.r
        self.phi_l = []; self.dphi_l = []
        for l in range(self.lmax+1):
            Pl = np.polynomial.legendre.Legendre.basis(l)(self.mu)
            sl = (2*l+1)/2.0*np.sum(self.src*Pl[None, :]*self.w[None, :], axis=1)
            f1 = sl*r**(l+2); f2 = sl*r**(1.0-l)
            I1 = np.concatenate([[0.0], np.cumsum(0.5*(f1[1:]+f1[:-1])*np.diff(r))])
            I2t = np.concatenate([[0.0], np.cumsum(0.5*(f2[1:]+f2[:-1])*np.diff(r))])
            phi = -(I1/r**(l+1) + r**l*(I2t[-1] - I2t))/(2*l+1.0)
            self.phi_l.append(phi); self.dphi_l.append(np.gradient(phi, r))
        self.phi_l = np.array(self.phi_l); self.dphi_l = np.array(self.dphi_l)

    def _uniform(self):
        return float(-self.dphi_l[1][0])

    def g_phantom(self, r, mu):
        r = np.asarray(r, float); mu = np.asarray(mu, float)
        gr = np.zeros(np.broadcast(r, mu).shape); gt = np.zeros_like(gr)
        st = np.sqrt(np.maximum(1.0 - mu**2, 0.0))
        for l in range(self.lmax+1):
            Pl = np.polynomial.legendre.Legendre.basis(l); dPl = Pl.deriv()
            p = np.interp(r, self.r, self.phi_l[l])
            dp = np.interp(r, self.r, self.dphi_l[l])
            gr = gr - dp*Pl(mu)
            gt = gt - (p/r)*(st*dPl(mu))
        return gr, gt

    def g_relative(self, r, mu):
        """Radial star-minus-centre field in units of a0 (negative = inward)."""
        return -1.0/np.asarray(r, float)**2 + self.g_phantom(r, mu)[0] - self.u*np.asarray(mu, float)

    def enclosed_phantom(self, r):
        r = np.asarray(r, float)
        return np.interp(r, self.r, self.dphi_l[0])*r**2

    def disc_curve(self, y_target, gamma_deg, npsi=720):
        """Circular speed round a ring of a disc whose NORMAL makes angle gamma with g_ext.
        Returns (psi, v/v_isolated, r0).  psi = 0 is the in-plane direction of g_ext."""
        r0 = 1.0/math.sqrt(y_target)                       # g_N,b = 1/r^2 = y
        g = math.radians(gamma_deg)
        psi = np.linspace(0.0, 2*np.pi, npsi, endpoint=False)
        mu = math.sin(g)*np.cos(psi)
        gin = -self.g_relative(np.full_like(mu, r0), mu)
        v = np.sqrt(np.maximum(gin, 0.0)*r0)
        return psi, v/math.sqrt(nu_s(y_target)*y_target*r0), r0

    def disc_mean(self, y_target, gamma_deg, npsi=720):
        return float(self.disc_curve(y_target, gamma_deg, npsi)[1].mean())

    def disc_asym(self, y_target, gamma_deg, npsi=720):
        """A = 2(v_toward - v_away)/(v_toward + v_away) across the in-plane field direction."""
        psi, v, _ = self.disc_curve(y_target, gamma_deg, npsi)
        a = v[0]; b = v[npsi//2]
        return float(2*(a - b)/(a + b))


def algebraic_relative(y, e, mu):
    """The FOIL: the algebraic prescription's radial relative field, in a0 (negative = inward)."""
    gr = -y + e*mu
    gt = -e*math.sqrt(max(1.0 - mu*mu, 0.0))
    m = math.hypot(gr, gt)
    return nu_s(m)*gr - nu_s(e)*e*mu


if __name__ == "__main__":
    import sys
    fails = []

    def ck(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
        if not ok:
            fails.append(name)

    print("VALIDATION of the QUMOND external-field solver (hunt_efe_lib.py)")
    s0 = EFESolve(e=1e-9, lmax=4)
    rt = np.array([0.3, 1.0, 3.0, 10.0, 30.0])
    gr = -1.0/rt**2 + s0.g_phantom(rt, np.zeros_like(rt))[0]
    gN = 1.0/rt**2
    err = float(np.max(np.abs(gr/(-nu(gN)*gN) - 1.0)))
    ck("V1 e->0 recovers the EXACT isolated point-mass QUMOND field g = nu(g_N/a0) g_N (dropping the minus "
       "sign in the phantom source fails this by 1.7x)", err < 0.005,
       f"max relative error {err:.5f} over r/r_M = 0.3-30, i.e. g_bar/a0 = 11 down to 0.0011")

    for e in (0.01, 0.1, 0.5):
        s = EFESolve(e=e)
        L = float(dlnnu_dlny(np.array([e]))[0]); n = nu_s(e)
        rf = 30.0/math.sqrt(e)                            # y/e = 1/900
        gNf = 1.0/rf**2
        got = float(-1.0/rf**2 + s.g_phantom(np.array([rf]), np.array([0.0]))[0][0])
        tgt = -n*gNf*(1.0 + L/3.0 + L/6.0)
        ep = abs(got/tgt - 1.0)
        ck(f"V2 (e={e}) the far field reproduces the analytic linearised QUMOND EFE "
           f"g_r/g_N,b -> nu(e)[1 + L/3 - (L/3)P_2(mu)], perpendicular to the field", ep < 0.02,
           f"solver {got:.5e} vs analytic {tgt:.5e}, relative error {ep:.4f} at y/e = {gNf/e:.2e}")
        mp = float(s.enclosed_phantom(np.array([rf]))[0])
        tg = (n - 1.0) + n*L/3.0
        ck(f"V3 (e={e}) the enclosed phantom mass tends to the CORRECTED (nu-1) + nu L/3, not the naive (nu-1)",
           abs(mp/tg - 1.0) < 0.05,
           f"M_ph/M_b = {mp:.4f} vs corrected {tg:.4f}; the naive (nu-1) = {n-1.0:.4f} is "
           f"{100*abs(tg-(n-1))/tg:.0f}% off")

    print("\n  V4 -- the uniform residual, SOLVED not assumed, against the algebraic prescription's leftover:")
    umax = 0.0
    for ee in (0.001, 0.003, 0.01, 0.03, 0.1, 0.3):
        s = EFESolve(e=ee)
        umax = max(umax, abs(s.u)/(nu_s(ee)*ee))
        print(f"    e = {ee:6.3f}:  solved g_ph(0) = {s.u:+.3e} a0    algebraic leftover nu(e) e = "
              f"{nu_s(ee)*ee:.4e} a0    ratio {abs(s.u)/(nu_s(ee)*ee):.5f}")
    ck("V4 the algebraic prescription's uniform residual is an ARTIFACT: the solved phantom leaves NO uniform "
       "force at the centre, so the centre of mass falls at exactly the external MOND field nu(e) g_N,ext",
       umax < 1e-3, f"|g_ph(0)|/(nu(e)e) < {umax:.2e} over e = 0.001-0.3")

    print("\n  reference table -- azimuthally averaged v/v_isolated (what a tilted-ring fit returns):")
    print(f"    {'e':>7} {'y=g_bar/a0':>11} {'gamma=0':>9} {'gamma=45':>9} {'gamma=90':>9} {'dex(0-90)':>10} {'|A|(g=90)':>10}")
    for ee in (0.003, 0.01, 0.03, 0.1):
        s = EFESolve(e=ee)
        for y in (0.3, 0.1, 0.03):
            v = [s.disc_mean(y, g) for g in (0, 45, 90)]
            print(f"    {ee:7.3f} {y:11.3f} {v[0]:9.5f} {v[1]:9.5f} {v[2]:9.5f} "
                  f"{math.log10(v[0]/v[2]):+10.5f} {abs(s.disc_asym(y, 90)):10.4f}")
    print(f"\nRESULT: {len(fails)} FAIL" + (f" -> {fails}" if fails else ""))
    sys.exit(1 if fails else 0)
