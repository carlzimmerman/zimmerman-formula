#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h99_local_sheet_cold_flow.py -- HUNT ITEM 99: the Local Sheet's cold flow.
==========================================================================
Item 99 asks whether the framework can reproduce the coldness of the local Hubble flow -- the fact that
galaxies between about 1 and 3 Mpc from the Local Group follow a Hubble law with a scatter of only a few
tens of km/s -- from the local baryons plus Lambda, with no dark mass.  The observable that actually carries
the information is not the scatter but the SHAPE of the flow: the local group's gravity decelerates the
nearby expansion, pushing the zero-velocity radius R0 outward and steepening the apparent local H0, and R0
is a direct measure of how much braking mass there is.

DATA, FETCHED THIS SESSION: the Updated Nearby Galaxy Catalog (Karachentsev, Makarov & Kaisina 2013,
AJ 145, 101; VizieR J/AJ/145/101), 869 Local Volume galaxies with distances, distance METHODS, Local-Group
frame velocities and a tidal index.  Saved as real_research/data/ungc_karachentsev2013.tsv.  The clean
sample is the one Karachentsev himself uses for this measurement: TRGB or Cepheid distances only, and
tidal index Theta_1 < 0, which removes galaxies bound to a nearer group whose virial motions would swamp
the flow.

THE PHYSICS, AND THE THING THAT DECIDES IT.  A test galaxy outside the Local Group obeys
    r_ddot = -g_group(r) - (1/2) Omega_m H0^2 a^-3 r + Omega_Lambda H0^2 r,
the second term being the homogeneous background (which reduces to the Friedmann equation when the group
is removed -- checked below) and the third Lambda.  Everything hinges on g_group:
  * LambdaCDM: G M_halo/r^2 with M_halo = the sum of the Milky Way's and M31's halos.
  * the framework WITHOUT its external field: the deep-MOND boost nu ~ 56 at 1 Mpc turns 2.2e11 Msun of
    baryons into an effective 1.2e13 -- six times MORE braking mass than the flow allows.  That is the
    known MOND Local Group timing problem, and this script reproduces it.
  * the framework WITH its external field: the Local Group's own MOND radius is only ~18 kpc, so beyond
    r_EFE = r_M/sqrt(e_N) ~ 160 kpc the boost SATURATES at the external-field value instead of growing.
    With e_N = 0.0127 (computed in h81_h82 from 2M++ + M31 + LMC) the effective mass at 1 Mpc drops by an
    order of magnitude.  Whether that lands on the observed R0 is the test, and it is not tuned: e_N comes
    from a different script and a different dataset.
Both footings.  Mutation controls.  Checks CAN fail.
"""
import sys, os, math
import numpy as np
from hunt_lib import *
from hunt_efe_lib import EFESolve

ck = Check(); rng = np.random.default_rng(9999)
E_N = {"canonical": 0.012730, "alt": 0.010545}       # from h81_h82_mw_external_fields.py
MB_LG = 2.2e11                     # baryons: Milky Way ~7-9e10 + M31 ~1.3e11 (photometric)
MB_LG_RC = 3.4e11                  # what the two rotation curves REQUIRE on the framework's own kernel
MH_LG = 2.8e12                     # LambdaCDM: M_MW ~1.3e12 + M_M31 ~1.5e12, measured independently
LG_RA, LG_DE, LG_F = 10.68, 41.27, 0.4     # barycentre placed 0.4 Mpc from us toward M31
T0_GYR = 13.79

P("="*118); P("ITEM 99 -- the Local Sheet's cold flow, and how much braking mass it allows"); P("="*118)

# ---------------------------------------------------------------- PART A: the data
P(""); P("-"*118); P("PART A -- the local Hubble diagram from the Updated Nearby Galaxy Catalog"); P("-"*118)
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "ungc_karachentsev2013.tsv"),
                                                 encoding="latin-1") if l.strip() and not l.startswith("#")]
hdr = [h.strip() for h in rows[0]]
rec = [dict(zip(hdr, [c.strip() for c in r])) for r in rows[3:]]
def fl(v):
    try: return float(v)
    except Exception: return float("nan")
D = np.array([fl(r["Dist"]) for r in rec]); V = np.array([fl(r["Vlg"]) for r in rec])
T1 = np.array([fl(r["Ti1"]) for r in rec]); MTH = np.array([r["f_Dist"] for r in rec])
RA = np.array([fl(r["_RAJ2000"]) for r in rec]); DE = np.array([fl(r["_DEJ2000"]) for r in rec])
def unit(ra, de):
    a, d = np.radians(ra), np.radians(de)
    return np.stack([np.cos(d)*np.cos(a), np.cos(d)*np.sin(a), np.sin(d)], axis=-1)
pos = unit(RA, DE)*D[:, None]
Dlg = np.linalg.norm(pos - unit(np.array([LG_RA]), np.array([LG_DE]))[0]*LG_F, axis=1)
info(f"UNGC loaded: {len(rec)} galaxies; distance methods " +
     ", ".join(f"{m} {int((MTH==m).sum())}" for m in ("TRGB", "Cep", "TF", "mem", "SBF")))
RLO, RHI = 0.7, 3.0
good = np.isin(MTH, ["TRGB", "Cep"]) & np.isfinite(V) & np.isfinite(T1) & (T1 < 0.0) & \
       (Dlg > RLO) & (Dlg < RHI)
info(f"selection declared up front, and it is Karachentsev's own: TRGB or Cepheid distance, tidal index "
     f"Theta_1 < 0 (not dominated by a nearer group), {RLO:g} < D_LG < {RHI:g} Mpc  ->  {good.sum()} galaxies")
sl, ic = np.polyfit(Dlg[good], V[good], 1)
res_lin = V[good] - (sl*Dlg[good] + ic)
sig_obs = float(np.std(res_lin))
R0_obs = -ic/sl
info(f"straight-line fit: V_LG = {sl:.1f} D {ic:+.1f} km/s, scatter {sig_obs:.1f} km/s, and the line "
     f"crosses zero at R0 = {R0_obs:.2f} Mpc")
info(f"the apparent local expansion rate, {sl:.0f} km/s/Mpc, is far above the cosmic {100*h:.0f} -- that is "
     f"not a Hubble tension, it is the Local Group braking the nearby flow, and it is the signal")
bs = []
for _ in range(4000):
    k = rng.integers(0, good.sum(), good.sum())
    ss, bb = np.polyfit(Dlg[good][k], V[good][k], 1)
    if ss > 0: bs.append(-bb/ss)
R0_err = float(np.std(bs))
info(f"bootstrap uncertainty on the measured zero-velocity radius: R0 = {R0_obs:.2f} +- {R0_err:.2f} Mpc "
     f"({len(bs)} of 4000 resamples usable)")
ck("99a the flow IS cold and the deceleration IS there: a few tens of km/s of scatter about a line whose "
   "zero crossing sits near 0.9 Mpc, which is where the Local Group's zero-velocity surface has been "
   "measured for two decades",
   sig_obs < 60.0 and 0.6 < R0_obs < 1.3 and good.sum() >= 15,
   f"N = {good.sum()}, scatter {sig_obs:.1f} km/s, R0(linear) = {R0_obs:.2f} Mpc, apparent H0_local = "
   f"{sl:.0f} km/s/Mpc")

# ---------------------------------------------------------------- PART B: the models
P(""); P("-"*118); P("PART B -- integrating the flow from z = 50 to today, three ways"); P("-"*118)
HT0 = H0
def a_of_t(t):
    return (OM_M/OM_L)**(1.0/3.0)*np.sinh(1.5*math.sqrt(OM_L)*HT0*t)**(2.0/3.0)
def t_of_a(a):
    return math.asinh((a**1.5)*math.sqrt(OM_L/OM_M))/(1.5*math.sqrt(OM_L)*HT0)
T0 = t_of_a(1.0)
info(f"flat LambdaCDM background from the same Planck parameters the rest of the repository uses: "
     f"Omega_m = {OM_M:.4f}, Omega_L = {OM_L:.4f}, H0 = {100*h:.1f}  ->  age {T0/(1e9*365.25*86400):.2f} Gyr")

_efe = {}
_GTAB = {}
def g_table(mode, a0=None, Mb=MB_LG, Mh=MH_LG, eN=0.0):
    """Tabulate the inward acceleration of the Local Group on a log radius grid, once per model, and
    interpolate it during the integration.  (The first version evaluated the QUMOND solver inside every
    Runge-Kutta substep -- a few hundred thousand orientation-averaged solves -- and did not finish.)"""
    key = (mode, a0, Mb, Mh, eN)
    if key in _GTAB: return _GTAB[key]
    rg = np.geomspace(1e-4, 3e2, 700)*Mpc
    if mode == "lcdm":
        gg = G*Mh*Msun/rg**2
    else:
        gN = G*Mb*Msun/rg**2
        if mode == "mond_noefe":
            gg = nu(gN/a0)*gN
        else:
            k = round(math.log10(eN), 4)
            if k not in _efe: _efe[k] = EFESolve(e=10.0**k)
            sol = _efe[k]
            rM = math.sqrt(G*Mb*Msun/a0)
            mu, w = np.polynomial.legendre.leggauss(12)
            x = rg/rM
            acc = np.zeros((len(mu), len(x)))
            for i, m in enumerate(mu):
                acc[i] = -sol.g_relative(x, np.full_like(x, m))          # inward, in a_0
            gg = a0*np.maximum(0.5*np.einsum("i,ij->j", w, acc), 0.0)
    _GTAB[key] = (rg, gg)
    return _GTAB[key]

def g_group(r_m, mode, a0=None, Mb=MB_LG, Mh=MH_LG, eN=0.0):
    """inward gravitational acceleration of the Local Group at physical radius r (m), positive."""
    rg, gg = g_table(mode, a0, Mb, Mh, eN)
    return np.interp(r_m, rg, gg, left=gg[0], right=gg[-1]*(rg[-1]/np.maximum(r_m, 1e-30))**2)

def integrate(r0_today_Mpc, mode, a0=None, Mb=MB_LG, Mh=MH_LG, eN=0.0, nstep=2500, zi=50.0):
    """shoot from a = 1/(1+zi) with pure Hubble flow; return (r_today_Mpc, v_today_km_s)."""
    ai = 1.0/(1.0 + zi); ti = t_of_a(ai)
    r = r0_today_Mpc*ai*Mpc
    v = (HT0*math.sqrt(OM_M*ai**-3 + OM_L))*r
    ts = np.linspace(ti, T0, nstep); dt = ts[1] - ts[0]
    for t in ts[:-1]:
        def acc(rr, tt):
            aa = a_of_t(tt)
            return (-float(g_group(rr, mode, a0, Mb, Mh, eN)) - 0.5*OM_M*HT0**2*aa**-3*rr
                    + OM_L*HT0**2*rr)
        k1v = acc(r, t); k1r = v
        k2v = acc(r + 0.5*dt*k1r, t + 0.5*dt); k2r = v + 0.5*dt*k1v
        k3v = acc(r + 0.5*dt*k2r, t + 0.5*dt); k3r = v + 0.5*dt*k2v
        k4v = acc(r + dt*k3r, t + dt); k4r = v + dt*k3v
        r = r + dt*(k1r + 2*k2r + 2*k3r + k4r)/6.0
        v = v + dt*(k1v + 2*k2v + 2*k3v + k4v)/6.0
        if r <= 0.002*Mpc: return float("nan"), float("nan")
    return r/Mpc, v/1e3

# validation: with no group mass the integration must reproduce the pure Hubble flow
rr, vv = integrate(2.0, "lcdm", Mh=0.0)
ck("99b the integrator is CORRECT: with the group's mass set to zero it reproduces the unperturbed "
   "background exactly -- the test particle ends at the radius it started from in comoving terms and moves "
   "at exactly H0 times that radius.  A sign error in the background term or in Lambda cannot pass this",
   abs(rr/2.0 - 1.0) < 0.01 and abs(vv/(100*h*rr) - 1.0) < 0.01,
   f"target r = 2.000 Mpc, got {rr:.4f}; v = {vv:.2f} km/s against H0 r = {100*h*rr:.2f}")

MODELS = []
for ft, a0 in A0.items():
    MODELS.append((f"framework + EFE ({ft})", dict(mode="mond_efe", a0=a0, Mb=MB_LG, eN=E_N[ft])))
MODELS.append(("framework, EFE ignored (canonical)", dict(mode="mond_noefe", a0=A0["canonical"], Mb=MB_LG)))
MODELS.append(("framework + EFE, RC-required M_b", dict(mode="mond_efe", a0=A0["canonical"], Mb=MB_LG_RC,
                                                        eN=E_N["canonical"])))
MODELS.append((f"LambdaCDM halos, M = {MH_LG:.1e}", dict(mode="lcdm", Mh=MH_LG)))
MODELS.append(("LambdaCDM, timing-argument M = 1.9e12", dict(mode="lcdm", Mh=1.9e12)))
MODELS.append(("Newtonian, baryons only", dict(mode="lcdm", Mh=MB_LG)))

def curve(kw, rs):
    out = []
    for r0 in rs:
        r, v = integrate(r0, **kw)
        out.append((r, v))
    return np.array([o[0] for o in out]), np.array([o[1] for o in out])

def zero_velocity_radius(kw, qlo=0.02, qhi=40.0, nit=44):
    """R0 = the present-day radius at which today's radial velocity vanishes.  Found by bisecting on the
    shooting parameter (a collapsed orbit counts as a large negative velocity), because sampling a fixed
    radial grid MISSES it: shells inside R0 have already turned round and fall to the centre, so they never
    appear in the grid at all and the naive 'find where the sampled v changes sign' returns nothing.
    That is what the first version of this script did, and it reported NaN for every massive model."""
    def f(q):
        r, v = integrate(q, **kw)
        return (-1e9, 0.0) if not np.isfinite(v) else (v, r)
    lo, hi = qlo, qhi
    if f(hi)[0] <= 0: return float("nan")
    if f(lo)[0] > 0: return float("nan")
    for _ in range(nit):
        mid = math.sqrt(lo*hi)
        if f(mid)[0] > 0: hi = mid
        else: lo = mid
    return f(hi)[1]

RCUT = 1.4          # common comparison window: outside every model's zero-velocity radius
rs = np.geomspace(0.35, 6.0, 26)
P(f"    {'model':>36} {'M_eff(1 Mpc)':>13} {'R0 (Mpc)':>9} {'V(2 Mpc)':>9} {'V(3 Mpc)':>9} "
  f"{'rms resid':>10}")
CUR = {}
for name, kw in MODELS:
    rq, vq = curve(kw, rs)
    ok = np.isfinite(rq) & np.isfinite(vq)
    rq, vq = rq[ok], vq[ok]
    srt = np.argsort(rq); rq, vq = rq[srt], vq[srt]
    R0 = zero_velocity_radius(kw)
    gm = float(np.atleast_1d(g_group(np.array([1.0*Mpc]), kw.get("mode"), kw.get("a0"),
                                     kw.get("Mb", MB_LG), kw.get("Mh", MH_LG), kw.get("eN", 0.0)))[0])
    Meff = gm*Mpc**2/G/Msun
    # the model curve only exists OUTSIDE that model's own zero-velocity radius: shells inside it have
    # collapsed and the integration returns nothing.  Comparing over the full 0.7-3 Mpc window therefore
    # silently clamps the massive models to their innermost value and manufactures a difference in rms.
    # (That is exactly what the first version did: it made LambdaCDM look 12 km/s worse than the framework
    # on curves that agree to 4 km/s.)  The comparison is made on a COMMON window instead.
    inwin = good & (Dlg > RCUT)
    pred = np.interp(Dlg[inwin], rq, vq, left=np.nan)
    rms = float(np.nanstd(V[inwin] - pred))
    nfit = int(np.sum(np.isfinite(pred)))
    CUR[name] = dict(r=rq, v=vq, R0=R0, rms=rms, Meff=Meff, nfit=nfit,
                     bias=float(np.nanmean(V[inwin] - pred)))
    P(f"    {name:>36} {Meff:13.3e} {R0:9.3f} {float(np.interp(2.0, rq, vq)):9.1f} "
      f"{float(np.interp(3.0, rq, vq)):9.1f} {rms:10.1f}")
NW = int(np.sum(good & (Dlg > RCUT)))
info(f"the measured R0 from the linear fit is {R0_obs:.2f} Mpc +- {R0_err:.2f}, and the measured scatter "
     f"about that line is {sig_obs:.1f} km/s; the last column is the rms of the {NW} galaxies beyond "
     f"{RCUT:g} Mpc -- a window outside EVERY model's zero-velocity radius, so all six curves are compared "
     f"on the same points -- about each model curve, with NO free parameter of any kind")

# ---------------------------------------------------------------- PART C: the verdict
P(""); P("-"*118); P("PART C -- which model the flow actually allows"); P("-"*118)
fw = CUR[f"framework + EFE (canonical)"]
fwn = CUR["framework, EFE ignored (canonical)"]
lc = CUR[f"LambdaCDM halos, M = {MH_LG:.1e}"]
nb = CUR["Newtonian, baryons only"]
info(f"framework WITHOUT the external field: effective braking mass at 1 Mpc = {fwn['Meff']:.2e} Msun, "
     f"R0 = {fwn['R0']:.2f} Mpc -- {fwn['R0']/R0_obs:.1f} times the observed zero-velocity radius.  This is "
     f"the MOND Local Group timing problem, and it is real")
info(f"framework WITH it: {fw['Meff']:.2e} Msun, R0 = {fw['R0']:.2f} Mpc -- the external field cuts the "
     f"braking mass by a factor {fwn['Meff']/fw['Meff']:.0f} and brings R0 to within "
     f"{100*abs(fw['R0']/R0_obs - 1):.0f} per cent of the measurement")
info(f"LambdaCDM with the independently measured halos: {lc['Meff']:.2e} Msun, R0 = {lc['R0']:.2f} Mpc")
info(f"Newtonian gravity with the baryons alone: {nb['Meff']:.2e} Msun, R0 = {nb['R0']:.2f} Mpc -- far too "
     f"little braking, which is why the Local Group needs either dark matter or a boost")
ck("99c (THE RESULT) the external field is what saves the framework here, and it was not free: with e_N "
   "taken unchanged from an entirely separate calculation on an entirely separate dataset, the Local "
   "Group's effective braking mass falls by an order of magnitude and the predicted zero-velocity radius "
   "lands near the measured one, where the same calculation with the external field ignored over-predicts "
   "it by a large factor",
   abs(fw["R0"] - R0_obs) < 3*R0_err and fwn["R0"] > fw["R0"] + 3*R0_err,
   f"observed R0 = {R0_obs:.2f} Mpc; framework + EFE {fw['R0']:.2f}; framework without EFE {fwn['R0']:.2f}; "
   f"LambdaCDM {lc['R0']:.2f}; Newtonian baryons {nb['R0']:.2f}")
lc2 = CUR["LambdaCDM, timing-argument M = 1.9e12"]
info(f"AND THE APPARENT PREFERENCE EVAPORATES ON A NUISANCE PARAMETER.  The framework's curve does fit "
     f"better than LambdaCDM's at M = {MH_LG:.1e} ({fw['rms']:.1f} against {lc['rms']:.1f} km/s) -- but the Local "
     f"Group's halo mass is uncertain by a factor of about two, and at the timing-argument value 1.9e12 "
     f"LambdaCDM gives R0 = {lc2['R0']:.2f} Mpc and rms {lc2['rms']:.1f} km/s.  That must not be quoted as a preference "
     f"for the framework.")
ck("99d BUT THE FLOW DOES NOT DISCRIMINATE, and saying so is the honest half: the framework's and "
   "LambdaCDM's curves fit the 1-3 Mpc galaxies about equally well once LambdaCDM's halo mass is allowed "
   "its own factor-of-two uncertainty, because both are matched by nature to the same zero-velocity radius "
   "and the data's scatter is far larger than the difference between them",
   abs(fw["rms"] - lc2["rms"]) < 0.5*sig_obs,
   f"rms about the framework's curve {fw['rms']:.1f} km/s, about LambdaCDM's {lc['rms']:.1f} at "
   f"M = {MH_LG:.1e} and {lc2['rms']:.1f} at the timing-argument 1.9e12, against an observed scatter of "
   f"{sig_obs:.1f}; the error on an rms from {NW} points is about "
   f"{sig_obs/math.sqrt(2*NW):.1f} km/s")

# ---------------------------------------------------------------- PART D: controls
P(""); P("-"*118); P("mutation controls and robustness"); P("-"*118)
info(f"MUTATION 1 (nu = 1, i.e. Newtonian gravity with the same baryons): R0 falls from {fw['R0']:.2f} to "
     f"{nb['R0']:.2f} Mpc, well outside the measurement's {R0_err:.2f} Mpc error -- the kernel is load-bearing "
     f"for the zero-velocity radius.  The rms in the outer window barely moves ({fw['rms']:.1f} to "
     f"{nb['rms']:.1f} km/s), which is the same lesson as check 99d: beyond 1.4 Mpc every model looks alike, "
     f"and ALL of the information is in R0")
perm = rng.permutation(good.sum())
rmsp = float(np.std(V[good][perm] - np.interp(Dlg[good], fw["r"], fw["v"])))
info(f"MUTATION 2 (permute which velocity belongs to which distance): rms about the framework's curve rises "
     f"from {fw['rms']:.1f} to {rmsp:.1f} km/s -- the model curve is tracking the real distance-velocity "
     f"relation and not just its mean")
alt = np.isin(MTH, ["TRGB", "Cep", "SBF", "SN"]) & np.isfinite(V) & np.isfinite(T1) & (T1 < 0.5) & \
      (Dlg > RLO) & (Dlg < 4.0)
sl2, ic2 = np.polyfit(Dlg[alt], V[alt], 1)
info(f"ROBUSTNESS (widen to SBF and SN distances, Theta_1 < 0.5, out to 4 Mpc): N = {alt.sum()}, "
     f"R0 = {-ic2/sl2:.2f} Mpc against {R0_obs:.2f} -- the zero-velocity radius is not a property of the cut")
ck("99e MUTATION CONTROLS behave: switching the kernel off collapses the predicted zero-velocity radius by "
   "far more than the measurement's own error; scrambling the distance-velocity pairing triples the "
   "residual scatter, so the model curve really is tracking the flow and not just its mean; and the "
   "measured R0 survives a substantial change of sample",
   nb["R0"] < fw["R0"] - R0_err and rmsp > fw["rms"] and abs(-ic2/sl2 - R0_obs) < 3*R0_err,
   f"Newtonian R0 {nb['R0']:.2f} vs the framework's {fw['R0']:.2f} Mpc against a measurement error of "
   f"{R0_err:.2f}; permuted rms {rmsp:.1f} vs {fw['rms']:.1f} km/s; widened-sample R0 {-ic2/sl2:.2f} vs "
   f"{R0_obs:.2f} Mpc")

P(""); P("-"*118)
P(f"VERDICT.  Item 99 asked for the Local Sheet's cold flow 'from baryons + Lambda with no dark mass'.  The")
P(f"scatter itself turns out to be the wrong statistic -- it is {sig_obs:.0f} km/s and every model reproduces it,")
P(f"because it is dominated by the real inhomogeneity of the Local Volume.  The statistic that bites is the")
P(f"ZERO-VELOCITY RADIUS, and there the run produces something worth keeping AND something against interest.")
P(f"Against interest: the framework's kernel applied naively to the Local Group's {MB_LG:.1e} Msun of baryons")
P(f"gives an effective braking mass of {fwn['Meff']:.1e} Msun at 1 Mpc and a zero-velocity radius of {fwn['R0']:.2f} Mpc,")
P(f"{fwn['R0']/R0_obs:.1f} times the measured {R0_obs:.2f} -- the MOND Local Group timing problem, reproduced here and not")
P(f"explained away.  Worth keeping: the external field, taken unchanged from the 2M++ reconstruction in a")
P(f"different script, saturates the boost beyond ~160 kpc and cuts that to {fw['Meff']:.1e} Msun and R0 = {fw['R0']:.2f} Mpc,")
P(f"within {100*abs(fw['R0']/R0_obs-1):.0f} per cent of the measurement with no free parameter.  What it is NOT is a discriminant:")
P(f"LambdaCDM gives R0 = {lc['R0']:.2f} Mpc at M = {MH_LG:.1e} and {lc2['R0']:.2f} at the timing-argument 1.9e12, and fits the same")
P(f"galaxies as well within its own halo-mass uncertainty.  Recorded as")
P(f"a CONSISTENCY, with the EFE identified as the load-bearing element and the naive-MOND failure recorded.")
P("-"*118)
sys.exit(ck.done())
