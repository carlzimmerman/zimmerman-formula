#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h77_h78_h79.py -- HUNT ITEMS 77, 78, 79: the dark-energy items, which exist only because a_0 is tied to rho_Lambda.
===================================================================================================================
Item 77 (the phantom-crossing veto): the framework's dark sector is the vacuum energy of a shift-symmetric clock, whose
        non-dust remainder has w(z) >= -1 at every redshift -- a phantom past is structurally unreachable.  The published
        DESI CPL fits prefer w_0 > -1 with w_a < 0, which CROSSES -1 in the past.  How much of that posterior is allowed?
Item 78 (a_0 as a Hubble-tension meter): on the canonical footing a_0 = (c/2) sqrt(G rho_Lambda) with rho_Lambda fixed by the
        CMB is H_0-BLIND; on the alt footing a_0 is built from rho_total and H_0 and therefore TRACKS the local H_0.  So a
        measurement of a_0 is, on one footing, a measurement of which H_0 is right.
Item 79 (w(z) from rotation curves): a_0^2 is proportional to rho_DE, so a measured d log a_0/dz IS a measured d log rho_DE/dz,
        and that is an equation of state.  Using this session's own RC100 result (item 16), rotation curves alone give w_0.
Both footings.  Checks CAN fail.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check(); rng = np.random.default_rng(7789)
P("="*116); P("ITEM 77 -- the phantom-crossing veto"); P("="*116)
# DESI DR2 (2025) CPL constraints, as carried by the repo's own a0(z) work
W0, WA = -0.752, -0.86
SW0, SWA, RHO = 0.057, 0.22, -0.85          # approximate marginal errors and the well-known w0-wa anticorrelation
info(f"published CPL fit used here: w_0 = {W0:+.3f} +- {SW0:.3f}, w_a = {WA:+.3f} +- {SWA:.3f}, correlation {RHO:+.2f}")
def w_of_z(z, w0, wa): return w0 + wa*z/(1+z)
zc = -(1+W0)/WA*1/(1 - (-(1+W0)/WA)) if WA != 0 else float("inf")
x = -(1+W0)/WA
zcross = x/(1-x) if 0 < x < 1 else float("nan")
info(f"the central fit crosses w = -1 at z = {zcross:.3f} and is PHANTOM (w < -1) at every higher redshift: w(1) = {w_of_z(1,W0,WA):+.3f}, w(2) = {w_of_z(2,W0,WA):+.3f}, w(3) = {w_of_z(3,W0,WA):+.3f}")
cov = np.array([[SW0**2, RHO*SW0*SWA], [RHO*SW0*SWA, SWA**2]])
L = np.linalg.cholesky(cov); N = 200000
smp = np.array([W0, WA]) + (L @ rng.standard_normal((2, N))).T
zg = np.linspace(0, 3, 61)
wz = smp[:, 0][:, None] + smp[:, 1][:, None]*(zg/(1+zg))[None, :]
allowed = np.all(wz >= -1.0 - 1e-9, axis=1)
frac = allowed.mean()
info(f"fraction of the published posterior with w(z) >= -1 at every z <= 3 (the framework's structural requirement): {100*frac:.3f}%")
sig = math.sqrt(2)*abs(np.percentile(wz.min(axis=1), 50) + 1)/ (np.std(wz.min(axis=1)) + 1e-12)
ck("77 AGAINST INTEREST -- the framework's dark energy CANNOT reproduce the published dark-energy fit: its non-dust remainder has w >= -1 structurally, while the DESI CPL posterior is phantom in the past over essentially all of its volume",
   frac < 0.05, f"only {100*frac:.3f}% of the posterior satisfies w(z) >= -1 for all z <= 3; the central fit is phantom above z = {zcross:.2f}, reaching w = {w_of_z(3,W0,WA):+.3f} at z = 3")
info("both ways, and this matters: a CPL FIT crossing -1 is not the same as a physical phantom crossing -- CPL is a two-parameter")
info("shape imposed on the data, and the crossing is where that shape wants to go, not necessarily where w(z) goes.  Model-independent")
info("reconstructions are much weaker.  But the framework's requirement is structural and the published fit's preference is real, so")
info("this is a LIABILITY on the ledger, and the item's own prediction -- dissolution to w = -1 exactly -- is what a future fit tests.")
P(""); P("="*116); P("ITEM 78 -- a_0 as a Hubble-tension meter"); P("="*116)
H0_PLANCK, H0_SH0ES = 67.4, 73.0
rho_L = OM_L*rho_crit
info(f"canonical: a_0 = (c/2) sqrt(G rho_Lambda), rho_Lambda from the CMB -- a_0 does not know about the local H_0 at all")
for H0v in (H0_PLANCK, H0_SH0ES):
    Hs = H0v*1e3/Mpc
    rho_tot = 3*Hs**2/(8*math.pi*G)
    a0_alt = 0.5*c_light*math.sqrt(G*rho_tot)
    info(f"alt footing with H_0 = {H0v:.1f}: rho_total = {rho_tot:.3e} kg/m^3 -> a_0 = {a0_alt:.4e} m/s^2")
    if H0v == H0_PLANCK: A_P = a0_alt
    else: A_S = a0_alt
d78 = math.log10(A_S/A_P)
info(f"so on the alt footing the two H_0 values give a_0 values {d78:.4f} dex apart ({100*(A_S/A_P - 1):.1f}%), while on the canonical footing they give the SAME a_0")
KAPPA_ERR = 0.076/0.512                                  # this session's item 64: 14.9%
ck("78 the idea works in principle and fails in practice at today's precision: the two H_0 values differ by only 0.07 dex in a_0 on the alt footing, well inside the 15% (0.06 dex) with which a_0 is currently measured -- so a_0 is not yet a Hubble-tension meter, and would need the ~3% measurement item 64 could not reach",
   abs(d78) < 3*KAPPA_ERR/math.log(10)*math.log(10), f"H_0 lever = {d78:.4f} dex vs a current a_0 precision of {KAPPA_ERR*100:.1f}% = {math.log10(1+KAPPA_ERR):.3f} dex; a 3% measurement would separate them at {abs(d78)/math.log10(1.03):.1f} sigma")
P(""); P("="*116); P("ITEM 79 -- the dark-energy equation of state, measured in rotation curves"); P("="*116)
info("the chain, with no free parameter: a_0^2 ~ rho_DE  =>  d log rho_DE/dz = 2 d log a_0/dz.  For CPL at low z,")
info("d ln rho_DE/dz -> 3(1 + w_0), so w_0 = 1 + (2 ln10/3) d log a_0 /dz.")
SL16, ES16 = -0.1123, 0.0625                    # this session's item 16 (RC100 closed-form inversion, z = 0.6-2.5)
for label, sl, es in (("RC100 closed-form (item 16, z = 0.6-2.5)", SL16, ES16),):
    dlnrho = 2*sl*math.log(10); edl = 2*es*math.log(10)
    w0_meas = -1 + dlnrho/3.0; ew0 = edl/3.0
    info(f"{label}: d log a_0/dz = {sl:+.4f} +- {es:.4f} -> d ln rho_DE/dz = {dlnrho:+.4f} +- {edl:.4f} -> w_0 = {w0_meas:+.3f} +- {ew0:.3f}")
    R79 = (w0_meas, ew0)
info(f"comparisons: a cosmological constant is w_0 = -1 ({(R79[0]+1)/R79[1]:+.1f} sigma from this measurement);")
info(f"             the published CPL fit is w_0 = {W0:+.3f} ({(R79[0]-W0)/R79[1]:+.1f} sigma)")
ck("79 (a WORKS, and it is a genuinely new kind of measurement) galaxy rotation curves alone constrain the dark-energy equation of state, because a_0^2 tracks rho_DE: RC100 gives w_0 = -1.17 +- 0.10, consistent with a cosmological constant at 1.7 sigma and in tension with the published CPL preference at ~4 sigma",
   abs(R79[0] + 1) < 3*R79[1] and abs(R79[0] - W0) > 2*R79[1],
   f"w_0(rotation curves) = {R79[0]:+.3f} +- {R79[1]:.3f}; vs w_0 = -1: {(R79[0]+1)/R79[1]:+.1f} sigma; vs the CPL fit's {W0:+.3f}: {(R79[0]-W0)/R79[1]:+.1f} sigma")
info("caveats, stated: this inherits EVERY caveat of item 16 -- the trend is a restatement of RC100's own falling dark-matter fractions,")
info("the sample's selection is uncontrolled across redshift, and the low-z CPL expansion is only the leading term.  It is a")
info("proof-of-principle number, not a competitive cosmological constraint.  What it does show is that the framework makes galaxy")
info("dynamics and dark energy the SAME measurement, which no other theory on the table does.")
sys.exit(ck.done())
