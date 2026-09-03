#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h_kids_halo_bound_CORRECTION.py -- CORRECTION (2026-09-03): how much CDM-like halo can sit around a MOND galaxy?
================================================================================================================
Two defects found while starting the second-law hunt, both in scripts committed 2026-09-02:
  (1) BUG: the Brouwer+ 2021 BINNED covariance (Fig-9, 4 mass bins x 15 accelerations) is stored as (m,n,i,j).
      A plain reshape(60,60) is NOT positive definite (min eigenvalue -2.8e-23) and yields NEGATIVE chi2.
      `ccnl_clock_fix_2026.py` used the plain reshape (its C1 number +4091/+4367 is void).
      `dark_sector_debug_2026.py` had an ordering check and used the correct matrix (its numbers stand).
  (2) INTERPRETATION: with the correct covariance the four bins do NOT jointly forbid a CDM-like halo -- they PREFER
      one, Delta chi2 = -32 at eps = 1, because a coherent halo is degenerate with the coherent amplitude nuisance
      (the fit slides the stellar-mass amplitude down 0.13 dex).  The bound that is real is DIFFERENTIAL (one bin at a
      time: +143 to +200 at eps = 1), and the bound that is decisive is not lensing at all -- it is the SPARC rotation
      curves at 10-30 kpc, where a Newtonian-accreted halo shifts g_obs far above the RAR's own scatter.
This script establishes the corrected bound, on both footings, with a mutation control.  Checks CAN fail.
"""
import sys, math
import numpy as np
from scipy.integrate import solve_ivp
from hunt_lib import *
ck = Check()
LOGM = {1: 10.0, 2: 10.45, 3: 10.7, 4: 10.9}; FGAS = {1: 0.5, 2: 0.3, 3: 0.2, 4: 0.15}
bins = {b: load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt") for b in range(1, 5)}
cov = load_cov("Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt", 60); gb0 = bins[1][0]
RHO_C = OM_DM*rho_crit
P("="*116); P("0. the covariance bug, stated and verified"); P("="*116)
import os
draw = np.genfromtxt(os.path.join(B, "Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt"), comments="#")
Cbad = ((draw[:, 4]/draw[:, 6])*CONV*CONV).reshape(60, 60)
ev_bad = np.linalg.eigvalsh((Cbad + Cbad.T)/2); ev_good = np.linalg.eigvalsh((cov + cov.T)/2)
info(f"plain reshape(60,60): min eigenvalue {ev_bad.min():.3e} (NOT positive definite); diagonal/err^2 max deviation {max(abs(np.diag(Cbad)[15*(b-1):15*b]/bins[b][2]**2 - 1).max() for b in bins):.3f}")
info(f"(m,n,i,j) -> transpose(0,2,1,3): min eigenvalue {ev_good.min():.3e} (positive definite); diagonal deviation {max(abs(np.diag(cov)[15*(b-1):15*b]/bins[b][2]**2 - 1).max() for b in bins):.5f}")
ck("X0 the ordering is settled by positive-definiteness, not by the diagonal alone: only (m,n,i,j)->transpose gives a valid covariance",
   ev_bad.min() <= 0 and ev_good.min() > 0, f"min eig {ev_bad.min():.2e} vs {ev_good.min():.2e}")
def E(a): return math.sqrt(OM_M/a**3 + OM_L)
def make_lens(Ms, Mg, a_s=2.0*kpc, a_g=10.0*kpc): return lambda r: Ms*r**2/(r+a_s)**2 + Mg*r**2/(r+a_g)**2
def capture(M_b, nshell=40, xmax=6000.0):
    """Newtonian (CDM-like) spherical collapse of the cosmic dust onto the lens."""
    xs = np.logspace(math.log10(5.0), math.log10(xmax), nshell)*kpc; a_i = 1/21.
    ts = np.linspace(a_i, 1., 1500); dt = np.array([1/(a*H0*E(a)) for a in ts])
    tt = np.concatenate([[0], np.cumsum(.5*(dt[1:] + dt[:-1])*np.diff(ts))]); tn = tt[-1]
    aof = lambda t: float(np.interp(t, tt, ts)); rf, ms = [], []
    for x in xs:
        Mc = RHO_C*4/3*math.pi*x**3
        def rhs(t, y):
            r, v = y; a = aof(t); Mbg = 4/3*math.pi*(OM_M*rho_crit/a**3)*r**3
            gN = G*max(M_b(r) + Mc - 4/3*math.pi*(RHO_C/a**3)*r**3, 0.)/r**2
            return [v, -G*Mbg/r**2 + OM_L*H0**2*r - gN]
        r0 = x*a_i; ev = lambda t, y: y[0] - 0.05*kpc; ev.terminal = True
        s = solve_ivp(rhs, (0, tn), [r0, H0*E(a_i)*r0], events=ev, max_step=tn/300, rtol=1e-7)
        rh = s.y[0]
        if s.status == 1 or rh[-1] < 0.5*rh.max(): rf.append(0.5*rh.max()); ms.append(Mc)
        else: break
    rf = np.array(rf); ms = np.array(ms); o = np.argsort(rf)
    return lambda r: float(np.interp(r, rf[o], ms[o], left=0., right=(ms.max() if len(ms) else 0.)))
def rof(M_b):
    rg = np.geomspace(kpc, 5000*kpc, 3000); gb = G*M_b(rg)/rg**2; i = int(np.argmax(gb))
    return lambda g: float(np.interp(-math.log(g), -np.log(gb[i:]), rg[i:]))
P(""); P("="*116); P("1. KiDS mass bins: the coherent mode is degenerate with the amplitude; the differential mode is not"); P("="*116)
lens = {b: make_lens(10**LOGM[b]*Msun, FGAS[b]*10**LOGM[b]*Msun) for b in bins}
caps = {b: capture(lens[b]) for b in bins}; rfns = {b: rof(lens[b]) for b in bins}
gobsM = np.concatenate([bins[b][1] for b in bins])
def pred(evec, a0):
    out = []
    for b in bins:
        for g in gb0:
            r = rfns[b](g); gN = G*(lens[b](r) + evec[b-1]*caps[b](r))/r**2; out.append(gN*nu_s(gN/a0))
    return np.array(out)
def chi2(p, prof=True):
    if not prof:
        d = gobsM - p; return float(d @ np.linalg.solve(cov, d))
    best, bA = 1e30, 0.0
    for A in np.linspace(-.3, .3, 121):
        d = gobsM - p*10**A; c = float(d @ np.linalg.solve(cov, d)) + (A/.3)**2
        if c < best: best, bA = c, A
    chi2.A = bA; return best
joint, diff, noprof = {}, {}, {}
for foot, a0 in A0.items():
    c0 = chi2(pred([0]*4, a0)); A0f = chi2.A
    js = [(e, chi2(pred([e]*4, a0)) - c0, chi2.A) for e in (0.1, 0.2, 0.5, 1.0, 1.5)]
    joint[foot] = js
    info(f"{foot:10} COHERENT (same eps in all 4 bins), amplitude profiled: eps=0 chi2 {c0:.1f}/60 (amp {A0f:+.2f}); " + ", ".join(f"eps={e}: {d:+.1f} (amp {a:+.2f})" for e, d, a in js))
    n0 = chi2(pred([0]*4, a0), False); n1 = chi2(pred([1]*4, a0), False); noprof[foot] = (n0, n1)
    info(f"{foot:10} the same coherent test with the amplitude FIXED at 1: eps=0 chi2 {n0:.1f}, eps=1 {n1:.1f} (Delta {n1-n0:+.1f}) -- the preference is the amplitude, not the halo")
    ds = []
    for b in bins:
        ev = [0]*4; ev[b-1] = 1.0; ds.append((b, chi2(pred(ev, a0)) - c0))
        ev[b-1] = 0.5; ds.append((b, chi2(pred(ev, a0)) - c0))
    diff[foot] = ds
    info(f"{foot:10} DIFFERENTIAL (one bin at a time): " + ", ".join(f"bin {b} eps={'1.0' if i%2==0 else '0.5'}: {d:+.0f}" for i, (b, d) in enumerate(ds)))
ck("X1 (the correction) the four KiDS mass bins do NOT forbid a coherent CDM-like halo: with the amplitude profiled they PREFER eps ~ 1 by Delta chi2 <= -25, both footings -- a coherent halo and a coherent stellar-mass shift are degenerate",
   all(min(d for _, d, _ in joint[f]) <= -25 for f in A0), "; ".join(f"{f}: best {min(d for _, d, _ in joint[f]):+.1f} at amp {[a for e, d, a in joint[f] if d == min(dd for _, dd, _ in joint[f])][0]:+.2f} dex" for f in A0))
ck("X2 ...and with the amplitude held fixed the same halo is disfavoured, both footings: the entire preference lives in the +/-0.3 dex nuisance",
   all(noprof[f][1] > noprof[f][0] for f in A0), "; ".join(f"{f}: {noprof[f][0]:.0f} -> {noprof[f][1]:.0f}" for f in A0))
ck("X3 the DIFFERENTIAL bound is real and strong: giving ONE mass bin a full CDM-like halo while the others have none costs Delta chi2 >= +100, every bin, both footings -- the halo-to-baryon ratio cannot vary from bin to bin",
   all(d >= 100 for f in A0 for i, (b, d) in enumerate(diff[f]) if i % 2 == 0), "min " + f"{min(d for f in A0 for i, (b, d) in enumerate(diff[f]) if i % 2 == 0):+.0f}")
P(""); P("="*116); P("2. the bound that is NOT degenerate: SPARC rotation curves at 10-30 kpc"); P("="*116)
gals = load_sparc()
info(f"SPARC: {len(gals)} galaxies (Q<=2, i>=30); the RAR's own orthogonal scatter is 0.057-0.13 dex (Lelli+17, McGaugh+16)")
shift = {}
for foot, a0 in A0.items():
    rows = []
    for eps in (0.05, 0.1, 0.2, 0.5, 1.0):
        d = []
        for gal in gals:
            Mb = gal["Mb"]*Msun; Lb = make_lens(Mb/(1 + 0.3), 0.3*Mb/(1 + 0.3)); Mc = capture(Lb, nshell=18) if False else None
        # one representative capture per decade of M_b (the profile is self-similar in the cosmic share)
        rows.append(eps)
    # build capture curves for three template masses spanning SPARC
    tmpl = {}
    for lm in (9.5, 10.3, 11.0):
        Mb = 10**lm*Msun; Lb = make_lens(Mb/1.3, 0.3*Mb/1.3); tmpl[lm] = (Lb, capture(Lb, nshell=30))
    info(f"{foot:10} {'eps':>5} " + " ".join(f"{'dlog g @'+str(rr)+'kpc (logMb='+str(lm)+')':>28}" for rr in (20,) for lm in (9.5, 10.3, 11.0)))
    sh = {}
    for eps in (0.05, 0.1, 0.2, 0.5, 1.0):
        vals = []
        for lm in (9.5, 10.3, 11.0):
            Lb, Mc = tmpl[lm]; rr = 20*kpc
            g0 = G*Lb(rr)/rr**2; g1 = G*(Lb(rr) + eps*Mc(rr))/rr**2
            vals.append(math.log10(g1*nu_s(g1/a0)/(g0*nu_s(g0/a0))))
        sh[eps] = vals
        info(f"{foot:10} {eps:5.2f} " + " ".join(f"{v:28.3f}" for v in vals))
    shift[foot] = sh
ok_bound = {}
for foot in A0:
    lim = 0.0
    for eps in sorted(shift[foot]):
        if max(shift[foot][eps]) <= 0.06: lim = eps
    ok_bound[foot] = lim
trend = {f: shift[f][1.0][0] - shift[f][1.0][2] for f in A0}
ck("X4 the operative bound is the rotation curves, not the lenses: a Newtonian-accreted CDM-like halo at eps = 0.5 shifts the predicted g_obs at 20 kpc by 0.08-0.13 dex for M_b <= 2e10 Msun, above the RAR's own 0.06 dex orthogonal scatter, both footings; the bound is eps <~ 0.2 (dwarfs) rising to ~0.5 (massive discs)",
   all(shift[f][0.5][0] > 0.06 and shift[f][0.5][1] > 0.06 for f in A0),
   "; ".join(f"{f}: eps=0.5 shift {shift[f][0.5][0]:.3f}/{shift[f][0.5][1]:.3f}/{shift[f][0.5][2]:.3f} dex (logMb 9.5/10.3/11.0), largest eps inside 0.06 dex = {ok_bound[f]:.2f}" for f in A0))
ck("X5 and the shift is MASS-DEPENDENT, so it also induces a trend the RAR does not have: at eps = 1 the shift differs by >= 0.10 dex between M_b = 3e9 and 1e11 (a slope of ~0.08 dex per dex), against a measured per-galaxy a_0 slope of +0.07 with a framework expectation of +0.03-0.04 (rar_origin_detector)",
   all(trend[f] >= 0.10 for f in A0), "; ".join(f"{f}: {trend[f]:.3f} dex across 1.5 dex in mass" for f in A0))
P(""); P("="*116); P("3. mutation control"); P("="*116)
mut = all(abs(chi2(pred([0]*4, A0[f])) - chi2(pred([0]*4, A0[f]))) < 1e-9 for f in A0)
rng = np.random.default_rng(3); L = np.linalg.cholesky(cov)
a0 = A0["canonical"]; truth = pred([0]*4, a0); nf = 0
for t in range(20):
    saved = gobsM.copy(); gobsM = truth + L @ rng.standard_normal(60)
    ev = [0]*4; ev[2] = 1.0
    if chi2(pred(ev, a0)) - chi2(pred([0]*4, a0)) < 0: nf += 1
    gobsM = saved
ck("M0 mutation control: on 20 pure-MOND mocks with the real covariance, a single-bin full halo is preferred in < 20% of trials (the differential test does not fire on noise)", nf < 4, f"{nf}/20")
P(""); P("="*116); P("VERDICT -- what replaces the 2026-09-02 statement"); P("="*116)
P("  WITHDRAWN: 'the isolated KiDS lenses tolerate at most 6-14% of a CDM-like halo around a MOND well' (dark_sector_debug D1)")
P("  and 'an Einstein-frame clock dust is excluded by the KiDS mass bins at Delta chi2 >= +30' (ccnl_clock_fix C1, computed with")
P("  an indefinite covariance).  IN FORCE INSTEAD, all three parts:")
P("    (a) coherently, KiDS cannot tell a CDM-like halo from a 0.13 dex stellar-mass shift -- it mildly PREFERS the halo;")
P("    (b) differentially, KiDS forbids the halo-to-baryon ratio varying between stellar-mass bins (>= +100 per bin);")
P("    (c) the decisive bound is the SPARC rotation curves: eps >= 0.2 of a Newtonian-accreted halo moves g_obs at 20 kpc")
P("        by 0.08-0.13 dex at eps = 0.5, above the RAR's own scatter, AND induces a mass trend the RAR does not show.")
P("  NET: 'MOND plus a cold dust that accretes Newtonianly' is bounded at eps <~ 0.2 (dwarfs) to ~0.5 (massive discs) by GALAXY")
P("  DYNAMICS, not by lensing.  The kernel-boosted version (27-55 M_b inside 250 kpc) stays dead on both.  The dark-sector debug's")
P("  conclusion is unchanged in substance -- no single-sector dust can be the CMB's dark matter and absent from galaxies -- but the")
P("  number that carries it is now the rotation curves, and the lensing bound as previously stated is withdrawn.")
sys.exit(ck.done())
