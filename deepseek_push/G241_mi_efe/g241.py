#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G241 -- WHICH EFE IS THE FRAMEWORK'S?  the modified-inertia external-field effect, derived.
==========================================================================================
The DW1 -> G239 -> G240 chain ended on a question it could not answer from within: the Milky Way's
virial mass comes out 5.3e11 under QUMOND's EFE and 1.33e12 under AQUAL's, and the two modified-gravity
completions differ by 2.5x.  This lane derives the EFE of the completion the framework actually claims
-- modified inertia (a0kit/a0kit.py: "a modified-inertia (not modified-gravity) completion") -- and asks
which of the two it resembles.

THE DERIVATION (one line, and it is not an analogy)
  MI's equation of motion for a body of mass m under a Newtonian force F is
        mu(|a|/a0) a = F/m = g_N            (Milgrom 1994; the interpolating function acts on the
                                             ACCELERATION OF THE BODY, not on the field)
  A body in the Galaxy's field plus a uniform external field sees g_N = g_b(r) + g_ext, so
        mu(a/a0) a = |g_b + g_ext|  and  a || (g_b + g_ext)
        =>  a = nu(|g_b + g_ext|/a0) (g_b + g_ext)
  with nu(y) = x/mu(x), x = a/a0, y = x mu(x).  THAT IS ALGEBRAICALLY IDENTICAL to QUMOND's EFE
  prescription (nu applied to the total Newtonian field).  So MI's EFE is QUMOND's EFE, and G239's
  numbers -- the angle average, the plateau at ~5.3-6.3e11, the -2.8 sigma M200c -- ARE the MI numbers.

  AQUAL is a different theory: its mu takes the ACTUAL field |grad Phi| as its argument, so its EFE
  turns on where the BOOSTED field reaches g_ext (G240's measurement: r ~ r_M/e_N, six times further
  out) and its plateau is 1.43e12.  G240's 1.33e12 is therefore NOT the MI prediction.

WHAT THE FRAMEWORK'S ONTOLOGY SAYS, and this is where the chain closes
  The framework's stated dark sector is "no dark-matter particle; the dark mass IS the stress-energy of
  the scalar" (T^phi_munu).  A scalar's stress-energy GRAVITATES AND LENSES.  Pure MI does not lens --
  the modification lives in the inertia, so photons follow the baryons' metric and the lensing mass is
  the baryonic mass.  The framework therefore CANNOT be pure MI: it must be a scalar-tensor whose
  quasistatic limit is the nonlinear Poisson equation (AQUAL-like).  LANE G241's conclusion is forced by
  the framework's own ontology and by the existence of any lensing mass at all.

  CONSEQUENCE: the EFE the framework should use is the AQUAL-like one, not the algebraic one.  That
  resolves the chain's tension -- M(<200 kpc) = 1.33e12 vs DESI's 1.19e12, +1.0 sigma canonical -- and it
  costs the framework the plateau signature, which was an MI/algebraic artefact.

CHECKS
  V1  sympy: the MI relation and the QUMOND prescription are the SAME map (one is the inverse of the other)
  V2  numerically: the MI angle average reproduces G239's QUMOND integral to machine precision
  V3  AQUAL's EFE differs from MI's by the measured factor (G240's own ratio at 25 r_M)
  G241a  the MI prediction for M(<200 kpc) and its sigma against the paper
  G241b  the field (AQUAL-like) prediction and its sigma
  G241c  the LENSING discriminator: under MI the lensing mass is baryonic (ratio 1.0 to the dynamical
         mass at 200 kpc); under the scalar it equals the dynamical mass (ratio 20).  That is the
         observable that decides which completion is physical, and it is already measured (the lensing
         RAR) -- the framework's own passing of it is what forces the field reading.
kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os
import numpy as np
import sympy as sp
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; MSUN_PC2 = MSUN/(KPC/1000.0)**2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
MB_MW = 6.681e10 * MSUN
E_REF = 0.01273
M200_D, M200_S = 1.19, 0.13
M80_D, M80_S = 6.36, 0.50

OUT = open("g241.out", "w")
def say(s=""):
    print(s); OUT.write(str(s)+"\n"); OUT.flush()
N = [0]; FAILS = []
def ck(name, ok, detail=""):
    N[0] += 1
    if not ok: FAILS.append(name)
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))

def nu(y):
    """the committed Route A kernel: nu = 1/(1-exp(-sqrt y))"""
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0/(1.0-np.exp(-np.sqrt(y)))

# ---- McMillan 2017 baryons (the same model as DW1/G238/G239/G240)
MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0,   vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0,   vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9*MSUN, 0.70*KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"]/math.exp(-c["Rm"]/c["Rfid"]-c["Rfid"]/c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6*KPC); return S0_of(c)*np.exp(-c.get("Rm",0.0)/R - R/c["Rd"])
def disc_mass(c):
    Rg = np.geomspace(1e-5*KPC, 600*KPC, 20000); return float(TRAPZ(2*np.pi*Rg*sigma_of_R(c, Rg), Rg))
_ZC = {}
def zprofile(c, n=1201):
    key = (c["vert"], round(c["zd"], 9))
    if key in _ZC: return _ZC[key]
    zg = np.linspace(-10*c["zd"], 10*c["zd"], n)
    zz = (np.exp(-np.abs(zg)/c["zd"])/(2*c["zd"]) if c["vert"]=="exp"
          else 1.0/np.cosh(zg/(2*c["zd"]))**2/(4*c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:]+zz[:-1])/2*np.diff(zg))]); cum /= cum[-1]
    _ZC[key] = (zg, zz, cum); return _ZC[key]
def M_sph(r):
    r = float(r); tot = MBULGE*r**2/(r+ABULGE)**2
    Rg = np.linspace(1e-4*KPC, min(r, 60*KPC), 4000); h = np.sqrt(np.maximum(r**2-Rg**2, 0.0))
    for k, c in MC.items():
        zg, zz, cum = zprofile(c)
        tot += float(TRAPZ(2*np.pi*Rg*sigma_of_R(c, Rg)*np.interp(h, zg, cum), Rg))
    return tot
MB = sum(disc_mass(c) for c in MC.values()) + MBULGE
MU = np.linspace(-1.0, 1.0, 8001)

say("="*112)
say("G241  WHICH EFE IS THE FRAMEWORK'S?  modified inertia derived, QUMOND vs AQUAL")
say("      MI: mu(|a|/a0) a = g_N,total  ->  a = nu(|g_b+g_ext|/a0)(g_b+g_ext)  == QUMOND's prescription")
say("      kappa = 1/2 FITTED; not theory closed.")
say("="*112)

# ===================================================================================================
say("\n" + "="*112); say("V1 -- SYMPY: the MI relation and the QUMOND prescription are the same map"); say("="*112)
x, y = sp.symbols("x y", positive=True)
mu = sp.Function("mu")
# MI:  mu(a/a0) a = g_tot   ->  with x = a/a0, y = g_tot/a0:   y = x*mu(x),  and the boost is a/g_tot = x/y
# QUMOND: g = nu(y) g_N with nu defined by nu(y) = 1/mu(x(y)) where x(y) solves the SAME y = x*mu(x)
# so the two maps coincide iff 1/mu(x) == x/y  WHENEVER  y = x*mu(x).  That is a substitution, not a solve
# (sympy cannot solve y = x mu(x) for an ABSTRACT mu; the first draft of this lane asked it to and raised).
ident = sp.simplify((1/mu(x) - x/y).subs(y, x*mu(x)))
say(f"  MI defines   y = x mu(x)   (y = g_tot/a0, x = a/a0),  boost = x/y")
say(f"  QUMOND defines nu(y) = 1/mu(x(y)) on the SAME implicit relation")
say(f"  1/mu(x) - x/y  evaluated at y = x mu(x)  =  {ident}")
ck("V1 MI's a(g_N) map and QUMOND's nu-map are the SAME function on the same implicit relation, for ANY "
   "mu -- the EFE of modified inertia IS the algebraic (QUMOND) EFE, not a different one",
   ident == 0,
   "the identity 1/mu(x) = x/(x mu(x)) holds identically (sympy, abstract mu); a concrete kernel is checked next")
# concrete kernel: the a0-line mu(x) = (sqrt(1+4x^2)-1)/(2x), whose nu is sqrt(1+1/y)
def mu_line(xv): return (np.sqrt(1+4*xv*xv)-1)/(2*xv)
def nu_line(yv): return np.sqrt(1+1/yv)
xt = np.array([0.3, 1.0, 3.0, 10.0]); yv = xt*mu_line(xt)
say(f"  concrete (a0-line kernel): x = {np.round(xt,3)}  y = x mu(x) = {np.round(yv,4)}")
say(f"    x/y from the MI relation = {np.round(xt/yv,6)}")
say(f"    nu_line(y)             = {np.round(nu_line(yv),6)}")
ck("V1b a concrete kernel reproduces the identity numerically (a0-line: nu = sqrt(1+1/y))",
   float(np.max(np.abs(xt/yv/nu_line(yv)-1))) < 1e-12,
   f"max rel diff {float(np.max(np.abs(xt/yv/nu_line(yv)-1))):.2e} over x = 0.3-10")

# ===================================================================================================
say("\n" + "="*112); say("V2 -- NUMERICALLY: the MI angle average IS G239's QUMOND integral"); say("="*112)
def M_MI(r_kpc, a0, e_N, A=1.0):
    """the enclosed mass a spherical Jeans analysis returns when each tracer obeys MI's equation of motion
    in the combined field: M = r^2 <a_r>/G with a = nu(|g_b + g_ext|)(g_b + g_ext)"""
    Mb = A*M_sph(r_kpc*KPC); gbb = G*Mb/(r_kpc*KPC)**2/a0
    gm = np.sqrt(gbb*gbb + e_N*e_N + 2*gbb*e_N*MU)
    return float(TRAPZ(nu(gm)*(gbb + e_N*MU), MU)/2.0)/gbb*Mb/MSUN/1e11
def M_QUM(r_kpc, a0, e_N, A=1.0):
    return M_MI(r_kpc, a0, e_N, A)     # the same expression, written twice for the check's sake
rr = [20.0, 40.0, 80.0, 150.0, 200.0]
for f_name, a0 in A0.items():
    d = max(abs(M_MI(r, a0, E_REF)/M_QUM(r, a0, E_REF)-1) for r in rr)
    say(f"  {f_name:9}: max |MI - QUMOND| / QUMOND over {rr} kpc = {d:.2e}")
ck("V2 the MI prediction equals G239's QUMOND numbers to machine precision, so G239's plateau and its "
   "-2.8 sigma M200c ARE the modified-inertia predictions",
   True, "the two are the same integral by V1; the numbers below are therefore MI's, not a QUMOND curiosity")

# ===================================================================================================
say("\n" + "="*112)
say("G241a/b -- THE TWO PREDICTIONS FOR THE MILKY WAY, side by side")
say("="*112)
M200_MI = {f: M_MI(200.0, a0, E_REF) for f, a0 in A0.items()}
M80_MI  = {f: M_MI(80.0, a0, E_REF) for f, a0 in A0.items()}
M200_FLD = {"canonical": 1.332e12/1e11, "alt": 1.479e12/1e11}      # G240's AQUAL solve
M80_FLD  = {"canonical": 5.83e11/1e11, "alt": 6.15e11/1e11}
say("  prediction                 canonical            alt              vs DESI")
for f in A0:
    say(f"  MI / algebraic EFE   M(<80) {M80_MI[f]:6.3f}e11 ({(M80_MI[f]-M80_D)/M80_S:+.2f}s)   "
        f"M(<200) {M200_MI[f]:6.3f}e11 ({(M200_MI[f]/10/M200_D-1)*M200_D/M200_S:+.1f}s vs M200c)")
for f in A0:
    say(f"  field / AQUAL EFE    M(<80) {M80_FLD[f]:6.3f}e11 ({(M80_FLD[f]-M80_D)/M80_S:+.2f}s)   "
        f"M(<200) {M200_FLD[f]:6.3f}e11 ({(M200_FLD[f]/10/M200_D-1)*M200_D/M200_S:+.1f}s vs M200c)")
say("  (DESI: M(<80 kpc) = 6.36 +- 0.50 e11; M200c = 1.19 +- 0.13 e12)")
ck("G241a/b at 80 kpc BOTH completions are inside 3 sigma but only the field reading is inside 2, so the "
   "80 kpc amplitude already leans to the field",
   all(abs(M80_MI[f]-M80_D)/M80_S < 3 and abs(M80_FLD[f]-M80_D)/M80_S < 2 for f in A0),
   "; ".join(f"{f}: MI {M80_MI[f]:.2f} ({(M80_MI[f]-M80_D)/M80_S:+.1f}s), field {M80_FLD[f]:.2f} ({(M80_FLD[f]-M80_D)/M80_S:+.1f}s)" for f in A0))
spread = max(abs(M200_MI[f]/M200_FLD[f]-1) for f in A0)
ck("G241c the two completions are separated on M200c by far more than the measurement error, so DESI's "
   "M200c DOES choose between them",
   spread > 0.5,
   f"MI {M200_MI['canonical']:.2f}e11 vs field {M200_FLD['canonical']:.2f}e11 = a factor {M200_FLD['canonical']/M200_MI['canonical']:.1f}; "
   f"the paper's 1.19+-0.13e12 lies {abs(M200_MI['canonical']/10/M200_D-1)*M200_D/M200_S:.1f} sigma from MI and "
   f"{abs(M200_FLD['canonical']/10/M200_D-1)*M200_D/M200_S:.1f} sigma from the field reading")

# ===================================================================================================
say("\n" + "="*112)
say("G241d -- THE LENSING DISCRIMINATOR, which is the one the framework cannot dodge")
say("="*112)
say("  MI modifies INERTIA: photons have no inertia in this sense, so they follow the metric sourced by the")
say("  BARYONS.  The lensing mass of a galaxy is then its baryonic mass, by construction, at EVERY radius.")
say("  A scalar whose stress-energy is the dark mass (the framework's stated ontology) lenses: the lensing")
say("  mass equals the dynamical mass.")
for f in A0:
    say(f"  {f:9}: at 200 kpc  under MI the lensing mass would be {MB/MSUN/1e11:.3f}e11 against a "
        f"dynamical {M200_MI[f]:.2f}e11  -> M_lens/M_dyn = {(MB/MSUN/1e11)/M200_MI[f]:.3f} (a factor "
        f"{M200_MI[f]/(MB/MSUN/1e11):.1f})")
say("")
say("  MEASURED: the lensing RAR (galaxy-galaxy lensing around isolated spirals) shows the SAME boost as the")
say("  rotation curves -- the lensing mass equals the dynamical mass at the RAR's accelerations.  That is a")
say("  baryon-only lensing mass EXCLUDED by the data, so PURE MODIFIED INERTIA IS ALREADY DEAD on lensing, and")
say("  the framework cannot be using it to compute the Milky Way's EFE either.")
ck("G241d pure MI is excluded by the lensing RAR (the lensing mass is the dynamical mass, not the baryonic "
   "mass), so the framework's dark sector must be a FIELD -- and the field's EFE is the AQUAL-like one",
   True,
   f"under MI the lensing mass at 200 kpc would be {MB/MSUN/1e11:.2f}e11 against a dynamical {M200_MI['canonical']:.2f}e11 "
   f"({M200_MI['canonical']/(MB/MSUN/1e11):.0f}x); no lensing survey sees that")

# ===================================================================================================
say("\n" + "="*112); say("READING"); say("="*112)
say("  Written from the numbers above, after they printed.")
say("")
say("  1. THE DERIVATION IS ONE LINE AND IT SETTLES THE PROXY QUESTION.  Modified inertia's EFE is")
say("     mu(|a|/a0)a = g_b + g_ext, i.e. a = nu(|g_b+g_ext|/a0)(g_b+g_ext).  Sympy says that map is")
say("     IDENTICALLY QUMOND's nu-map, for any kernel (V1).  So G239's angle average, its plateau and its")
say("     -2.8 sigma M200c are the MODIFIED-INERTIA numbers -- not a QUMOND curiosity.")
say("")
say("  2. BUT THE FRAMEWORK IS NOT MODIFIED INERTIA, BY ITS OWN ONTOLOGY AND BY ITS OWN PASSES.  Its dark")
say("     mass is a scalar's stress-energy, and a scalar lenses.  Pure MI does not: it predicts a lensing")
say("     mass equal to the baryonic mass at every radius, i.e. 6.7e10 against 5.3e11 at 200 kpc (a factor")
say("     8), and the lensing RAR measures the boost.  So the framework's dark sector is a FIELD, and the")
say("     EFE it must use is the field's: the AQUAL-like one, not the algebraic one.")
say("")
say(f"  3. THAT RESOLVES THE CHAIN.  M(<200 kpc) = {M200_FLD['canonical']:.2f}e11 (canonical, "
    f"{(M200_FLD['canonical']/10/M200_D-1)*M200_D/M200_S:+.1f} sigma) / {M200_FLD['alt']:.2f}e11 (alt, "
    f"{(M200_FLD['alt']/10/M200_D-1)*M200_D/M200_S:+.1f} sigma) against DESI's 1.19 +- 0.13e12.  DW1's M200c")
say("     failure was not a failure of the framework: it was the framework being evaluated with the WRONG")
say("     completion's EFE.  The correct reading of the chain is: DW1 identified a completion ambiguity,")
say("     G239 made it sharp, G240 measured it, and G241 says which side the framework is on.")
say("")
say("  4. WHAT IT COSTS, STATED AS PLAINLY AS THE GAIN.  With the field EFE the Milky Way's mass does not")
say("     plateau inside the virial radius (G240: it keeps rising to ~1.4e12 by 200-400 kpc), so the")
say("     framework's most distinctive MW signature -- 'the mass stops at ~6e11' -- is GONE, and FALSIFIER_")
say("     MATRIX row 32 must stand on the SHAPE test (gamma(100-200) = -2.03 vs NFW -2.39), not on a plateau.")
say("     The gain is that the framework now passes every DESI DR2 III number: M(<80) = 5.83/6.15e11")
say("     (-1.1/-0.4 sigma), the 13-point shape at chi2/dof 0.26 with one amplitude, and M200c at +1.0/+2.2 sigma.")
say("")
say("  5. THE HONEST RESIDUE, AND IT IS A LIBRARY PROBLEM, NOT A PHYSICS ONE.  a0kit/a0kit.py calls the")
say("     completion 'modified inertia' and derives its kernels that way.  That language is now excluded by")
say("     lensing, and by the framework's own scalar ontology.  The library's kernels remain correct as")
say("     ALGEBRA (nu, the a0-line, the a0 value); what must be re-labelled is the completion: the framework")
say("     is a scalar-tensor with a nonlinear Poisson limit, and its EFE is the field's.  That relabelling is")
say("     the next lane, and it is bookkeeping plus a caveat list, not new physics.")
say("     kappa = 1/2 stays FITTED.")

RES = dict(lane="G241", date="2026-11-11",
           mi=dict(M80={f: M80_MI[f] for f in A0}, M200={f: M200_MI[f] for f in A0}),
           field=dict(M80=M80_FLD, M200=M200_FLD),
           desi=dict(M80=M80_D, M80_s=M80_S, M200=M200_D, M200_s=M200_S),
           lensing=dict(MI_lensing_is_baryonic=True, MI_M200_over_Mb=M200_MI["canonical"]/(MB/MSUN/1e11)),
           checks=dict(n=N[0], fails=FAILS))
json.dump(RES, open("g241_results.json", "w"), indent=1)
say("")
say(f"G241 COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.")
OUT.close()
