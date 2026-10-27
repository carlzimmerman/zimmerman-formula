#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g02v_adversarial_mi_argument_refutation.py
=================================================================================================
ADVERSARIAL VERIFICATION of g02_vertical_vs_planar_frequency_split.py.

THE CLAIM UNDER TEST (g02, checks V6b/V6c and SUMMARY items 3, 4, 7):
    "The vertical-versus-planar split in the Milky Way disc does NOT discriminate modified GRAVITY
     from modified INERTIA.  A full QUMOND solve with the framework's own Route A kernel and
     algebraic modified inertia predict the same vertical/planar force ratio to about 1%
     (S_MG = 1.0111/1.0118, S_MI = 0.9990/0.9989, |dS| = 0.0121 against sigma(S) = 0.1208
     -> 0.10 sigma), far inside the measurement error."

WHAT THIS SCRIPT DOES.  Three separate attacks, each with numbered checks that can fail:

  W1  INDEPENDENT RECOMPUTATION OF THE NEWTONIAN INPUTS.  g02's forces come from a Hankel-space
      axisymmetric solver.  This script recomputes |g_R|(R0,0), |g_R|(R0,1.1), |g_z|(R0,1.1) for the
      SAME McMillan 2017 mass model by a completely different method -- the ray form

          g(r0) = G Int dOmega n_hat Int_0^inf ds rho(r0 + s n_hat)

      in which the 1/s^2 of the Green's function cancels against the s^2 of the volume element, so
      the field point's own singularity never appears.  Validated first on Miyamoto-Nagai, where the
      forces are known analytically.  If g02's Q is wrong, the whole statistic is wrong.

  W2  WHAT THE 0.10 SIGMA ACTUALLY MEASURES.  Every "modified-inertia" arm g02 puts within 1% of the
      QUMOND arm -- the algebraic map, the orbit average A1, and the frequency gate A2 in the part of
      its window that matters -- takes as its kernel argument the LOCAL FIELD MAGNITUDE |g_N| at the
      evaluation point.  g02's own V5a records that this quantity differs by 0.38% between (R0,0) and
      (R0,1.1 kpc).  Any prescription whose only input is |g_N| at a point is an ALGEBRAIC MODIFIED-
      GRAVITY relation, not a modified-inertia one: it has no access to the trajectory.  This section
      shows the reported arm-vs-arm separation is numerically identical to the QUMOND phantom's
      departure from the algebraic MOND relation, S_MG / S_MI,alg = 1.012 -- i.e. g02 has measured
      full modified gravity against ALGEBRAIC modified gravity, and the fork does not enter.

  W3  A MODIFIED-INERTIA PRESCRIPTION THAT IS NOT A LOCAL-FIELD MAP, AND WHAT IT PREDICTS.  In
      Milgrom's modified inertia (1994, Ann.Phys. 229, 384; 2011, arXiv:1111.1611) the modification
      is a functional of the whole trajectory, and the theory is fixed on CIRCULAR orbits by the
      exact relation mu(a/a0) a = g_N with a = Omega^2 R -- the argument is the orbit's OWN
      acceleration, not the ambient field magnitude.  Carrying that same rule to the other periodic
      motion available at the Sun -- the vertical oscillation, whose own (Newtonian) acceleration at
      its turning point is the restoring force |g_z,bar(R0,z_max)|, NOT the quadrature sum of the
      radial and vertical fields -- gives an MI arm with

          S_A4 = nu(|g_z,bar(R0,1.1)|/a0) / nu(|g_R,bar(R0,0)|/a0)

      This is a prescription, exactly like g02's A1/A2/A3, and it is stated as one.  It is however
      the prescription that follows the one place where MI is not free -- its circular-orbit
      normalisation -- rather than the place where MI is defined not to look.  It moves the arm
      separation by a factor of ~20, and it lies INSIDE g02's own A3 bracket at p = -1.41, an
      exponent that is NOT free: p = ln[(z_max/R0)(nu_z/Omega)^2] / ln(nu_z/Omega) is fixed by two
      measured numbers.  g02's SUMMARY item 7 -- "only a trajectory dependence far stronger than
      anything the framework contains ... the framework supplies no such exponent" -- is what fails.

  W4  A SEPARATE, SMALLER DEFECT: the four Sigma_1.1 determinations are combined as though all four
      were the Kuijken-Gilmore quantity |K_z(1.1)|/(2 pi G).  Nitschai+ 2021 quote the INTEGRATED
      surface density Sigma(R0,|z|<1.1 kpc) = Int rho dz, which for the same mass model is 13% SMALLER
      than |K_z|/(2 pi G) because of the radial term in the integrated Poisson equation.  Mixing the
      two conventions biases S_obs LOW -- i.e. it manufactures part of the "common offset" that g02
      reports at 2.5-3.1 sigma.  This does not touch the arm-vs-arm verdict; it is recorded because a
      manufactured deficit is as much a defect as a manufactured win.

  W5  MUTATION CONTROLS.

BOTH a0 FOOTINGS throughout.  Checks that FAIL are the point.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, Check, G, P, Msun, info, kpc, nu_s  # noqa: E402

PC = kpc / 1000.0
MSUN_PC2 = Msun / PC**2
TWO_PI_G = 2.0 * math.pi * G

C = Check()
np.seterr(over="ignore", divide="ignore", invalid="ignore")


def banner(t: str) -> None:
    P("\n" + "=" * 104)
    P("  " + t)
    P("=" * 104)


# --- g02's own reported numbers, transcribed from g02_vertical_vs_planar_frequency_split.out ------
G02 = dict(
    gR0=1.2302e-10, gzK=5.3437e-11, gz_over_gR_at_K=0.480, gNK=1.2349e-10,
    Q=2.3022, sig_lnQ=0.1340, S_obs=0.6417, S_err=0.1208,
    S_MG={"canonical": 1.0111, "alt": 1.0118},
    S_MIalg={"canonical": 0.9990, "alt": 0.9989},
    Omega=9.0748e-16, nu_z=1.6345e-15, q=1.801,
    sig_model_col=54.03,                       # Int rho dz, |z|<1.1 kpc, McMillan 2017 at R0
)
R0 = 8.178 * kpc                               # GRAVITY Collaboration 2019, A&A 625, L10
ZK = 1.1 * kpc

# --- the SAME McMillan 2017 (MNRAS 465, 76, Table 3) mass model g02 uses, transcribed verbatim ----
MCM = dict(
    S0_thin=896.0 * MSUN_PC2, Rd_thin=2.50 * kpc, zd_thin=0.300 * kpc,
    S0_thick=183.0 * MSUN_PC2, Rd_thick=3.02 * kpc, zd_thick=0.900 * kpc,
    rho0_b=98.4 * Msun / PC**3, alpha_b=1.8, r0_b=0.075 * kpc, rcut_b=2.1 * kpc, q_b=0.5,
    S_HI_fid=10.0 * MSUN_PC2, Rm_HI=4.0 * kpc, Rd_HI=7.0 * kpc, zd_HI=0.085 * kpc,
    S_H2_fid=2.0 * MSUN_PC2, Rm_H2=12.0 * kpc, Rd_H2=1.5 * kpc, zd_H2=0.045 * kpc,
    R_fid=8.33 * kpc,
)


def rho_disc_gas(R, z):
    """thin + thick + HI + H2 (everything smooth; the cusped bulge is handled separately)."""
    p = MCM
    R = np.asarray(R, float)
    z = np.abs(np.asarray(z, float))
    out = (p["S0_thin"] / (2 * p["zd_thin"])) * np.exp(-z / p["zd_thin"] - R / p["Rd_thin"]) \
        + (p["S0_thick"] / (2 * p["zd_thick"])) * np.exp(-z / p["zd_thick"] - R / p["Rd_thick"])
    for tag in ("HI", "H2"):
        S0 = p[f"S_{tag}_fid"] / math.exp(-p[f"Rm_{tag}"] / p["R_fid"] - p["R_fid"] / p[f"Rd_{tag}"])
        zd = p[f"zd_{tag}"]
        Rs = np.maximum(R, 1e-3 * kpc)
        out = out + (S0 / (4 * zd)) * np.exp(-p[f"Rm_{tag}"] / Rs - Rs / p[f"Rd_{tag}"]) \
            / np.cosh(z / (2 * zd)) ** 2
    return out


def rho_bulge(R, z):
    p = MCM
    rp = np.sqrt(np.asarray(R, float) ** 2 + (np.asarray(z, float) / p["q_b"]) ** 2)
    return p["rho0_b"] / (1 + rp / p["r0_b"]) ** p["alpha_b"] * np.exp(-((rp / p["rcut_b"]) ** 2))


# =================================================================================================
banner("W1  INDEPENDENT RECOMPUTATION OF THE NEWTONIAN FORCES -- a different method entirely")
# =================================================================================================
P(r"""  THE RAY IDENTITY.  With r = r0 + s n_hat the Newtonian field is

      g(r0) = G Int rho(r) (r - r0)/|r - r0|^3 dV = G Int dOmega n_hat Int_0^inf ds rho(r0 + s n_hat)

  because dV = s^2 ds dOmega cancels the 1/s^2.  There is NO singularity at the field point even when
  the field point sits inside the mass, and no Hankel transform, no k grid and no Bessel function
  appears anywhere -- so this shares no failure mode with g02's solver.  The only numerical care
  needed is that for a thin disc the ray integral has a 1/|cos theta| ridge at theta = pi/2 (rays
  running along the plane), so cos theta is graded as A sinh(v).""")


def ray_field(rho_fn, Rf, zf, nmu=600, nphi=128, ns=2400, smax=400 * kpc, A=0.004, chunk=25):
    """g_R, g_z at (Rf, zf) by the ray identity.  Field point on the +x axis; g_y = 0 by symmetry."""
    vmax = math.asinh(1.0 / A)
    v = np.linspace(-vmax, vmax, nmu)
    mu = A * np.sinh(v)                                   # cos theta, graded near 0
    dmu_dv = A * np.cosh(v)
    wv = np.empty_like(v)
    wv[1:-1] = 0.5 * (v[2:] - v[:-2])
    wv[0] = 0.5 * (v[1] - v[0])
    wv[-1] = 0.5 * (v[-1] - v[-2])
    wmu = wv * dmu_dv                                     # weights for Int dmu
    phi = np.linspace(0.0, math.pi, nphi)                 # symmetric in phi -> [0,pi], doubled
    wphi = np.empty_like(phi)
    wphi[1:-1] = 0.5 * (phi[2:] - phi[:-2])
    wphi[0] = 0.5 * (phi[1] - phi[0])
    wphi[-1] = 0.5 * (phi[-1] - phi[-2])
    wphi = 2.0 * wphi
    s = np.geomspace(1e-5 * kpc, smax, ns)
    ws = np.empty_like(s)
    ws[1:-1] = 0.5 * (s[2:] - s[:-2])
    ws[0] = 0.5 * (s[1] - s[0]) + s[0]
    ws[-1] = 0.5 * (s[-1] - s[-2])
    st = np.sqrt(np.maximum(1.0 - mu**2, 0.0))
    gx = gz = 0.0
    for a in range(0, nmu, chunk):
        b = min(a + chunk, nmu)
        nx = (st[a:b, None] * np.cos(phi)[None, :])[:, :, None]     # (m, p, 1)
        ny = (st[a:b, None] * np.sin(phi)[None, :])[:, :, None]
        nz = mu[a:b, None, None] * np.ones((1, nphi, 1))
        X = Rf + s[None, None, :] * nx
        Y = s[None, None, :] * ny
        Z = zf + s[None, None, :] * nz
        F = np.einsum("mps,s->mp", rho_fn(np.sqrt(X * X + Y * Y), Z), ws)
        W = wmu[a:b, None] * wphi[None, :]
        gx += float(np.sum(W * F * nx[:, :, 0]))
        gz += float(np.sum(W * F * nz[:, :, 0]))
    return G * gx, G * gz


def mn_rho_cyl(R, z, M, a, b):
    zt = np.sqrt(z**2 + b**2)
    return (b**2 * M / (4 * math.pi)) * (a * R**2 + (a + 3 * zt) * (a + zt) ** 2) \
        / ((R**2 + (a + zt) ** 2) ** 2.5 * zt**3)


def mn_forces(R, z, M, a, b):
    zt = math.sqrt(z**2 + b**2)
    den = (R**2 + (a + zt) ** 2) ** 1.5
    return -G * M * R / den, -G * M * z * (a + zt) / (zt * den)


MMN, aMN, bMN = 5.0e10 * Msun, 3.0 * kpc, 0.3 * kpc
P("\n  W1a  validation on Miyamoto-Nagai (M=5e10 Msun, a=3 kpc, b=0.3 kpc -- as thin as the MW disc):")
P(f"      {'R,z [kpc]':<15}{'gR ray':>14}{'gR exact':>14}{'err':>9}{'gz ray':>14}{'gz exact':>14}{'err':>9}")
worst = 0.0
for Rt, zt_ in ((8.178, 0.0), (8.178, 1.1), (4.0, 1.1)):
    gr, gz = ray_field(lambda R, z: mn_rho_cyl(R, z, MMN, aMN, bMN), Rt * kpc, zt_ * kpc)
    gra, gza = mn_forces(Rt * kpc, zt_ * kpc, MMN, aMN, bMN)
    er = abs(gr / gra - 1)
    ez = abs(gz / gza - 1) if gza != 0 else abs(gz) / abs(gra)
    worst = max(worst, er, ez)
    P(f"      {Rt:5.2f},{zt_:5.2f}   {gr:14.4e}{gra:14.4e}{er:9.3%}{gz:14.4e}{gza:14.4e}{ez:9.3%}")
C("W1a the independent ray solver reproduces the exact Miyamoto-Nagai forces to better than 1%, so "
  "it is fit to audit g02's Hankel solver", worst < 0.01, f"worst error {worst:.3%}")


def rho_full(R, z):
    return rho_disc_gas(R, z) + rho_bulge(R, z)


gR0_ray, _ = ray_field(rho_full, R0, 0.0)
gRK_ray, gzK_ray = ray_field(rho_full, R0, ZK)
Q_ray = abs(gR0_ray) / abs(gzK_ray)
P(f"\n  W1b  the McMillan 2017 model at the Sun, ray solver vs g02's Hankel solver:")
P(f"      {'quantity':<26}{'ray':>14}{'g02':>14}{'diff':>10}")
for tag, mine, theirs in (("|g_R|(R0, 0)", abs(gR0_ray), G02["gR0"]),
                          ("|g_R|(R0, 1.1 kpc)", abs(gRK_ray), G02["gzK"] / G02["gz_over_gR_at_K"]),
                          ("|g_z|(R0, 1.1 kpc)", abs(gzK_ray), G02["gzK"]),
                          ("Q = |g_R|(0)/|g_z|(1.1)", Q_ray, G02["Q"])):
    P(f"      {tag:<26}{mine:14.4e}{theirs:14.4e}{mine/theirs-1:+10.2%}")
C("W1c g02's Newtonian shape number Q is CONFIRMED by an independent solver to better than 2% -- the "
  "attack that follows is NOT about the mass model's forces", abs(Q_ray / G02["Q"] - 1) < 0.02,
  f"ray Q = {Q_ray:.4f} vs g02 Q = {G02['Q']:.4f} ({Q_ray/G02['Q']-1:+.2%})")

gNK_ray = math.hypot(gRK_ray, gzK_ray)
C("W1d and so is the fact g02 leans on hardest -- |g_N| at the two evaluation points agrees to well "
  "under 1%, because the vertical pull is only ~0.48 of the radial one and adds in quadrature",
  abs(gNK_ray / abs(gR0_ray) - 1) < 0.01,
  f"|g_N|(R0,1.1)/|g_N|(R0,0) = {gNK_ray/abs(gR0_ray):.5f}; |g_z|/|g_R| = "
  f"{abs(gzK_ray)/abs(gRK_ray):.3f}")


# =================================================================================================
banner("W2  WHAT THE 0.10 SIGMA ACTUALLY MEASURES -- both 'arms' read the same local scalar")
# =================================================================================================
P(r"""  Write out the three arms g02 finds to agree:

      MI algebraic      S = nu(|g_N|(R0,1.1)/a0) / nu(|g_N|(R0,0)/a0)
      MI orbit-avg A1   S = nu(<|g_N|>_orbit/a0)  / nu(|g_N|(R0,0)/a0)
      MI gate A2        S = [1+|G(w_v)|(nu(|g_N|(R0,1.1)/a0)-1)] / [1+|G(w_r)|(nu(|g_N|(R0,0)/a0)-1)]

  Every one of them takes |g_N| AT A POINT as the kernel's argument.  A theory whose prediction is a
  function of the local field magnitude is an ALGEBRAIC MODIFIED-GRAVITY relation; it cannot know
  which trajectory the particle is on, which is the one thing modified INERTIA is defined to know
  (Milgrom 1994; 2011, arXiv:1111.1611).  For A2 the point is sharper still: over the committed and
  upper thirds of its omega_c window |G| -> 1 at BOTH frequencies and the gate collapses exactly onto
  the algebraic map, so its 'scan over four decades' is a scan over a region where the assumption is
  inert.  The consequence is arithmetic:""")

ratio_c = G02["S_MG"]["canonical"] / G02["S_MIalg"]["canonical"]
ratio_a = G02["S_MG"]["alt"] / G02["S_MIalg"]["alt"]
P(f"\n      S_MG / S_MI,algebraic = {ratio_c:.4f} (canonical), {ratio_a:.4f} (alt)")
P(f"      i.e. g02's whole arm-vs-arm separation, {abs(G02['S_MG']['canonical']-G02['S_MIalg']['canonical']):.4f}, "
  f"IS the QUMOND phantom's departure from the algebraic\n      MOND relation g = nu(|g_N|/a0) g_N in "
  f"a flattened source -- a known ~1% disc effect that exists\n      entirely INSIDE modified gravity "
  f"(g02's own M2 shows it goes to zero for a spherical source).")
C("W2a *** the quantity g02 reports as the modified-GRAVITY / modified-INERTIA separation is "
  "numerically the full-QUMOND vs ALGEBRAIC-MOND difference: both of its arms are functions of the "
  "same local |g_N|, which its own V5a records as differing by 0.38% between the two evaluation "
  "points, so the 0.10 sigma is guaranteed before any physics enters ***",
  abs(ratio_c - 1) < 0.02 and abs(ratio_a - 1) < 0.02,
  f"S_MG/S_MI,alg = {ratio_c:.4f} / {ratio_a:.4f}; g02's M2 drives the same quantity to "
  f"{1.00480:.5f} for a sphere")

P("\n  A2's window, checked: |G(w)| = 1/sqrt(1+(w/omega_c)^2) at w = Omega and w = nu_z.")
OMC = dict(lo=2.0e-15, committed=1.782e-14, hi=1.0e-11)
inert = []
for tag, oc in OMC.items():
    Gr = 1.0 / math.sqrt(1 + (G02["Omega"] / oc) ** 2)
    Gv = 1.0 / math.sqrt(1 + (G02["q"] * G02["Omega"] / oc) ** 2)
    inert.append(min(Gr, Gv))
    P(f"      omega_c {tag:<10} |G(Omega)| = {Gr:.4f}, |G(nu_z)| = {Gv:.4f}")
C("W2b two thirds of the gate's 'theory-allowed window' have |G| > 0.99 at BOTH frequencies, i.e. the "
  "gate is switched OFF there and its agreement with the algebraic map is definitional, not a result",
  sum(1 for x in inert if x > 0.99) >= 2, f"min |G| per decade tier = {[round(x,4) for x in inert]}")


# =================================================================================================
banner("W3  AN MI PRESCRIPTION THAT IS NOT A LOCAL-FIELD MAP -- and what it does to the verdict")
# =================================================================================================
P(r"""  MI IS NORMALISED ON CIRCULAR ORBITS BY ITS OWN ACCELERATION, NOT BY THE AMBIENT FIELD.  The one
  place Milgrom's modified inertia is not free is the circular orbit, where the exact relation is
  mu(a/a0) a = g_N with a = Omega^2 R: the kernel's argument is the acceleration OF THAT MOTION.  At
  the Sun the circular motion's Newtonian acceleration is |g_R,bar(R0,0)| -- there is no vertical
  component in it at all.  The vertical oscillation is the OTHER periodic motion available at the same
  place, and its own Newtonian acceleration at the turning point is the restoring force
  |g_z,bar(R0,z_max)|.  Carrying the circular-orbit rule across to it gives

      ARM A4 (modal argument):  S = nu(|g_z,bar(R0,1.1)|/a0) / nu(|g_R,bar(R0,0)|/a0)

  g02 instead feeds the vertical arm |g_N| = sqrt(g_R^2 + g_z^2), which is dominated by the RADIAL
  field that the vertical oscillation never samples.  That single choice -- not any physics -- is what
  makes its MI arm agree with its MG arm to 0.1%.  A4 is a PRESCRIPTION, with exactly the status of
  g02's A1/A2/A3, and it is labelled as one here.  Two further readings of the same idea are carried
  so the reader sees the spread rather than one favourable point.""")

gR0, gzK, gNK = abs(gR0_ray), abs(gzK_ray), gNK_ray
a_vert_dyn = ZK * G02["nu_z"] ** 2         # z_max * nu_z^2 with g02's own (boosted) nu_z
P(f"\n  the three candidate arguments for the VERTICAL motion at R0 (a0-canonical units in brackets):")
P(f"      |g_N|(R0,1.1) = sqrt(g_R^2+g_z^2)  = {gNK:.4e}  [y = {gNK/A0['canonical']:.3f}]   <- g02's choice")
P(f"      |g_z,bar|(R0,1.1) = restoring force = {gzK:.4e}  [y = {gzK/A0['canonical']:.3f}]   <- A4")
P(f"      z_max nu_z^2 (g02's own nu_z)       = {a_vert_dyn:.4e}  [y = {a_vert_dyn/A0['canonical']:.3f}]   <- A4'")
P(f"      radial motion:  |g_R,bar|(R0,0)     = {gR0:.4e}  [y = {gR0/A0['canonical']:.3f}]")

rows = []
for f, a0 in A0.items():
    nr = nu_s(gR0 / a0)
    S_alg = nu_s(gNK / a0) / nr
    S_A4 = nu_s(gzK / a0) / nr
    S_A4p = nu_s(a_vert_dyn / a0) / nr
    S_MG = G02["S_MG"][f]
    rows.append((f, a0, S_alg, S_A4, S_A4p, S_MG))

P(f"\n  {'footing':<12}{'S_MG (g02)':>12}{'S_MI alg':>11}{'S_A4':>9}{'S_A4prime':>11}"
  f"{'|dS| A4':>10}{'sigma':>8}{'|dS| A4p':>10}{'sigma':>8}")
sep_A4, sep_A4p = [], []
for f, a0, S_alg, S_A4, S_A4p, S_MG in rows:
    d4, d4p = abs(S_MG - S_A4), abs(S_MG - S_A4p)
    sep_A4.append(d4 / G02["S_err"])
    sep_A4p.append(d4p / G02["S_err"])
    P(f"  {f:<12}{S_MG:12.4f}{S_alg:11.4f}{S_A4:9.4f}{S_A4p:11.4f}{d4:10.4f}"
      f"{d4/G02['S_err']:8.2f}{d4p:10.4f}{d4p/G02['S_err']:8.2f}")

sep_claimed = abs(G02["S_MG"]["canonical"] - G02["S_MIalg"]["canonical"]) / G02["S_err"]
P(f"\n  g02's claimed arm-vs-arm separation: {sep_claimed:.2f} sigma.  A4: {min(sep_A4):.2f}-{max(sep_A4):.2f} "
  f"sigma.  A4': {min(sep_A4p):.2f}-{max(sep_A4p):.2f} sigma.")
C("W3a *** THE CLAIM 'the two arms predict the same ratio to about 1%' DOES NOT SURVIVE a "
  "modified-inertia prescription that keeps MI's own circular-orbit normalisation instead of "
  "substituting the ambient field: A4 splits the arms by 27-29%, more than 20x the 1.2% claimed ***",
  min(sep_A4) > 4 * sep_claimed,
  f"A4 separation {min(sep_A4):.2f}-{max(sep_A4):.2f} sigma against the claimed {sep_claimed:.2f} sigma")
C("W3b and even the most conservative reading of the same idea (A4', which uses the boosted vertical "
  "frequency and so partly re-imports the radial field) still splits the arms by several times the "
  "claimed amount", min(sep_A4p) > 3 * sep_claimed,
  f"A4' separation {min(sep_A4p):.2f}-{max(sep_A4p):.2f} sigma")
C("W3c ATTEMPTED AND HONESTLY FAILED: A4 does not reach a 3-sigma arm-vs-arm separation either, so "
  "this refutation establishes that g02's laboratory has SOME discriminating power, not that it "
  "decides the fork", max(sep_A4) > 3.0,
  f"best A4 separation {max(sep_A4):.2f} sigma -- FAILING THIS IS PART OF THE VERDICT: the honest "
  f"reading is 'up to ~2.4 sigma', not '0.10 sigma, structurally undecidable'")

# --- the A3 exponent is NOT free ------------------------------------------------------------------
q = G02["q"]
p_A4 = math.log(gzK / gNK) / math.log(q)
p_A4p = math.log(a_vert_dyn / gNK) / math.log(q)
P(f"""
  AND IT LIES INSIDE g02's OWN A3 BRACKET.  A3 writes y_eff = (w/Omega)^p (|g_N|/a0) and g02 scans
  p in [-2,+2], then dismisses the whole family in SUMMARY item 7 because "the framework supplies no
  such exponent".  But A4 is A3 at
        p = ln(|g_z,bar| / |g_N|) / ln(nu_z/Omega) = {p_A4:+.3f}        (A4)
        p = ln(z_max nu_z^2 / |g_N|) / ln(nu_z/Omega) = {p_A4p:+.3f}     (A4')
  and that exponent is not a free parameter: it is fixed by the two measured numbers z_max/R0 and
  nu_z/Omega together with the disc's own force ratio.  g02's scan already CONTAINS the refuting
  case -- its p = -1 row reads S = 1.186, 1.5 sigma from its own MG arm -- and rejects it only by
  the assertion that no exponent of order one is motivated.""")
C("W3d *** the exponent that refutes the null is INSIDE g02's own scanned bracket, so the null rests "
  "entirely on the assertion that |p| ~ 1 is unmotivated -- and A4 motivates it from MI's "
  "circular-orbit normalisation, the one part of MI that is not free ***",
  -2.0 <= p_A4 <= 2.0, f"p(A4) = {p_A4:+.3f}, inside the scanned [-2,+2]")

# --- internal consistency with the fork's own motivation -------------------------------------------
P(f"""
  AN INTERNAL-CONSISTENCY POINT, which is the strongest form of this objection.  The fork exists in
  this repository (F08_F10_THE_COHERENCE_FORK.md, f09) because rotation-supported systems land on the
  kernel and pressure-supported ones do not -- a pattern that can only be explained by a modification
  which reads the ORBIT.  g02's 'MI algebraic' arm is a function of the local field alone; applied to
  a dwarf spheroidal it returns exactly what modified gravity returns, and therefore cannot produce
  the rotation/pressure split that motivated the fork in the first place.  An MI arm that cannot
  reproduce the observation the fork was opened to explain is not a representative of the MI side.""")
C("W3e the arm g02 calls 'modified inertia' predicts, for any system, exactly the algebraic "
  "modified-gravity answer, so it cannot reproduce the rotation-vs-pressure split (f09) that the fork "
  "was opened over -- it is not a representative of the MI side of the fork it is being used to close",
  abs(G02["S_MIalg"]["canonical"] - 1) < 0.01,
  f"S_MI,alg = {G02['S_MIalg']['canonical']:.4f}, i.e. indistinguishable from 'no split at all'")


# =================================================================================================
banner("W4  A SEPARATE DEFECT -- two different quantities are averaged as one Sigma_1.1")
# =================================================================================================
zz = np.linspace(0.0, ZK, 4001)
col = 2.0 * float(np.trapz(rho_full(np.full_like(zz, R0), zz), zz)) / MSUN_PC2
kz_over = gzK / TWO_PI_G / MSUN_PC2
P(f"""
  For the SAME McMillan model at R0, the two quantities that the literature both writes 'Sigma_1.1'
  are not equal, because the integrated Poisson equation carries a radial term:

      Int rho dz over |z| < 1.1 kpc          = {col:6.2f} Msun/pc^2   (a surface DENSITY)
      |K_z(1.1 kpc)| / (2 pi G)              = {kz_over:6.2f} Msun/pc^2   (a FORCE, the Kuijken-Gilmore
                                                              1991 convention g02 assumes for all four)
      ratio                                  = {kz_over/col:6.3f}

  Kuijken & Gilmore 1991 and Holmberg & Flynn 2004 quote the force quantity.  Nitschai, Eilers,
  Neumayer, Cappellari & Rix 2021 (ApJ 916, 112) quote 'the surface density within |z| <= 1.1 kpc' from
  a Jeans mass model -- an integrated density.  Averaging the two conventions as if they were one
  quantity pushes S_obs DOWN by of order {kz_over/col-1:.0%} on whichever entries are densities.""")
P(f"      g02's own model column, for cross-reference: {G02['sig_model_col']:.2f} Msun/pc^2 "
  f"(this script: {col:.2f})")
S_obs_fix = G02["S_obs"] * (1 + 0.25 * (kz_over / col - 1))     # one of four entries re-expressed
P(f"      re-expressing ONE of the four entries in the force convention moves S_obs from "
  f"{G02['S_obs']:.4f} to {S_obs_fix:.4f},\n      i.e. the 'common offset' from "
  f"{(G02['S_obs']-G02['S_MIalg']['canonical'])/G02['S_err']:+.2f} sigma to "
  f"{(S_obs_fix-G02['S_MIalg']['canonical'])/G02['S_err']:+.2f} sigma.")
C("W4a the two conventions differ by more than 10% for this mass model, so mixing them is a real "
  "error, not a rounding one", abs(kz_over / col - 1) > 0.10, f"ratio {kz_over/col:.3f}")
C("W4b and the error runs AGAINST the framework -- it inflates the 2.5-3.1 sigma common offset g02 "
  "reports -- so it is a manufactured deficit, which this repository's working rule forbids as firmly "
  "as a manufactured win", S_obs_fix > G02["S_obs"],
  f"corrected S_obs = {S_obs_fix:.4f} > reported {G02['S_obs']:.4f}")
C("W4c NOT RUN AS A KILL: this script has not read Nitschai+ 2021's definition off the paper, only "
  "off its abstract wording as transcribed in g02's own header ('Sigma(R0,|z|<=1.1kpc)'), so the "
  "size of the correction is flagged, not asserted", False,
  "marked not-run: the convention of each of the four determinations must be checked against the "
  "papers before any number here is used")


# =================================================================================================
banner("W5  MUTATION CONTROLS")
# =================================================================================================
gR_lo, gz_lo = ray_field(rho_full, R0, 0.05 * kpc)
S_A4_lo = nu_s(abs(gz_lo) / A0["canonical"]) / nu_s(gR0 / A0["canonical"])
S_alg_lo = nu_s(math.hypot(gR_lo, gz_lo) / A0["canonical"]) / nu_s(gR0 / A0["canonical"])
P(f"\n  M1 vanishing-amplitude mutation: evaluate the vertical arm at z_max = 0.05 kpc instead of "
  f"1.1 kpc.\n     |g_z| there = {abs(gz_lo):.4e} (vs {gzK:.4e}); S_A4 = {S_A4_lo:.4f}, "
  f"S_algebraic = {S_alg_lo:.4f}")
C("M1 as the vertical amplitude goes to zero the A4 argument goes to zero and its S runs AWAY from "
  "1, while the local-field arm stays pinned at 1 -- the two prescriptions are genuinely different "
  "functions of the trajectory and not a re-parametrisation of each other",
  abs(S_A4_lo - 1) > 3 * abs(S_alg_lo - 1),
  f"|S_A4-1| = {abs(S_A4_lo-1):.3f} vs |S_alg-1| = {abs(S_alg_lo-1):.4f}")
C("M1b AGAINST THIS SCRIPT'S OWN INTEREST -- A4's PATHOLOGY, STATED OUTRIGHT.  Taken literally to "
  "small amplitude A4 sends nu_vert to infinity, because a low-amplitude vertical mode has a "
  "vanishing acceleration of its own whatever the ambient field.  A real time-nonlocal MI does not "
  "decompose a trajectory into independent modes and would not do this.  So A4 is a BRACKET, not a "
  "theory -- exactly the status of g02's A1/A2/A3 -- and this refutation does NOT claim A4 is right; "
  "it claims the null is prescription-dependent and therefore not a statement about the fork",
  S_A4_lo < 1.5, f"A4 at z_max = 0.05 kpc gives S = {S_A4_lo:.3f}, which is unphysical -- FAILING "
  f"THIS CHECK IS THE HONEST LIMIT OF THIS REFUTATION")

a0_tiny = 1e-18
S_A4_newt = nu_s(gzK / a0_tiny) / nu_s(gR0 / a0_tiny)
S_alg_newt = nu_s(gNK / a0_tiny) / nu_s(gR0 / a0_tiny)
P(f"  M2 Newtonian mutation (a0 = {a0_tiny:.0e}): S_A4 = {S_A4_newt:.6f}, S_algebraic = "
  f"{S_alg_newt:.6f}")
C("M2 with the kernel switched off BOTH prescriptions return 1, so the A4 split is produced by the "
  "kernel and not by the substitution of arguments",
  abs(S_A4_newt - 1) < 5e-3 and abs(S_alg_newt - 1) < 5e-3,
  f"|S_A4-1| = {abs(S_A4_newt-1):.2e}, |S_alg-1| = {abs(S_alg_newt-1):.2e}")

gR_sph, gz_sph = ray_field(lambda R, z: 1e-24 * np.exp(-np.sqrt(R**2 + z**2) / (3 * kpc)), R0, ZK)
r_here = math.hypot(R0, ZK)
C("M3 the ray solver returns a strictly radial field for a spherical source, so the vertical/radial "
  "decomposition it feeds the arms is not an artefact of the ray grading",
  abs((gz_sph / gR_sph) / (ZK / R0) - 1) < 0.02,
  f"gz/gR = {gz_sph/gR_sph:.5f} against z/R = {ZK/R0:.5f} (r = {r_here/kpc:.3f} kpc)")


# =================================================================================================
banner("VERDICT")
# =================================================================================================
P(f"""
  1. THE ARITHMETIC IS RIGHT AND THE MASS MODEL IS RIGHT.  An independent ray-integral solver, which
     shares no machinery with g02's Hankel code, reproduces Q to {abs(Q_ray/G02['Q']-1):.2%} and confirms that |g_N| at
     (R0,0) and (R0,1.1 kpc) agree to {abs(gNK/gR0-1):.2%}.  Nothing in this refutation is a numerical dispute.

  2. THE INFERENCE IS NOT RIGHT.  All three MI arms that agree with the QUMOND arm take the LOCAL
     FIELD MAGNITUDE as the kernel's argument.  That is an algebraic modified-GRAVITY relation.  The
     reported separation is arithmetically the full-QUMOND / algebraic-MOND difference,
     S_MG/S_MI,alg = {ratio_c:.4f}, a known ~1% disc effect that lives entirely inside modified gravity and
     that g02's own M2 mutation drives to zero for a spherical source.  The 0.10 sigma is a property
     of the parametrisation, not a measurement about the fork.

  3. AN MI PRESCRIPTION THAT KEEPS MI'S OWN CIRCULAR-ORBIT NORMALISATION SPLITS THE ARMS BY 20x MORE.
     Feeding the vertical motion its own restoring force |g_z,bar| instead of the quadrature sum gives
     S = {rows[0][3]:.3f} (canonical) / {rows[1][3]:.3f} (alt) against the MG arm's {G02['S_MG']['canonical']:.3f} / {G02['S_MG']['alt']:.3f}: a separation of
     {min(sep_A4):.2f}-{max(sep_A4):.2f} sigma rather than 0.10 sigma.  It sits at p = {p_A4:+.2f} inside g02's own A3 bracket, and
     that exponent is fixed by z_max/R0 and nu_z/Omega -- it is not a free parameter that the
     framework 'does not supply'.

  3b. AND WHAT IS WRONG WITH A4, SAID BY THIS SCRIPT AND NOT LEFT FOR A REFEREE.  M1b shows A4 sends
     nu_vert to infinity as the vertical amplitude goes to zero, which no real time-nonlocal theory
     would do.  A4 is therefore a BRACKET, not a theory.  The refutation does not need it to be a
     theory: point 2 stands on its own, and A4 only has to be as defensible as g02's own A1/A2/A3 to
     show that the 0.10 sigma is a property of the prescription rather than of the fork.

  4. WHAT SURVIVES OF g02.  The narrow statement -- QUMOND and the ALGEBRAIC local map predict the
     same S to 1% -- survives and is confirmed here.  The headline generalisation -- that the
     vertical/planar split does not discriminate modified gravity from modified inertia, and cannot
     be made to, 'for a reason that is structural' -- does not.  The honest statement is that the
     split discriminates MG from a trajectory-argument MI at about 2.4 sigma today, which is the same
     strength as f09's rotation/pressure hint, and that the obstruction is the {G02['sig_lnQ']:.0%} baryon SHAPE
     systematic rather than a structural degeneracy between the two theories.

  5. AND A SECOND, SMALLER DEFECT.  Two different quantities are averaged as one Sigma_1.1: the
     Kuijken-Gilmore force |K_z|/(2 pi G) and an integrated column Int rho dz, which differ by
     {kz_over/col-1:.0%} for this mass model.  The mixture biases S_obs LOW and so INFLATES the common offset
     g02 reports at 2.5-3.1 sigma.  Flagged, not asserted: the four papers' conventions have to be
     read off the papers before the size of the correction is quoted.""")

P("")
sys.exit(C.done())
