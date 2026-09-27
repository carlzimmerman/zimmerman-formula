#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG4 (part 2 of 5) -- WHERE THE LAW MUST SWITCH OFF, AND WHICH SWITCH CRITERION THE DATA ALLOW.  The galaxy law of part 1
must be ON in bound galaxies (SPARC), around isolated KiDS lenses out to ~1 Mpc at z = 0.25, and in z = 2.5 discs (flat
a0(z), the framework's distinctive prediction); it must be OFF in the linear web at z < 0.64 (CMB lensing, XR26), in the
z = 2-3 IGM (the Lyman-alpha forest) and in the Solar System (FP17's threshold-mass theorem).  This lane puts every
candidate criterion -- the field strength (the record's 'yield'), a length, a mass, a local density, the bound-versus-
expanding state of the flow (turnaround; the energy form of 'bound'; virialised) and their combinations -- against every
region at once, with the region variables computed, and scores the survivors in the record's own pipelines.

THE BASE.  a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED, flat in z; footings 9.3603e-11 / 1.1312e-10 m/s^2 (FP0).
The law: g = nu(g_bar/a0) g_bar with the kernels of part 1 (P2, nu_mono).  Nothing here imports a published theory as a
base; the switch criteria are stated as properties of the matter flow and of the region, not of any theory.

THE RECORD'S MACHINERY, READ-ONLY (exec'd from the committed files, writes refused):
  * XR26_cmb.py (the hub's CMB lane): CAMB/CLASS at the Planck 2018 best fit, FP13's growth yardstick (FP9/FP6 inside),
    the Limber C_L^phiphi, Planck 2018 VIII's MV band powers and amplitudes.  Its patched-CLASS build, its C section and its
    L3-L5 are NOT re-run.
  * FP17_screening_without_xi.py up to its V section: the threshold-mass theorem (the Solar System's switch).
  * FP1_static_sector.py's KiDS-1000 machinery (Brouwer et al. 2021 isolated lenses, four stellar-mass bins, full covariance,
    M_b profiled per bin, the linear 2-halo template) with FP20's EXACT projector swapped in (FP20_esd_projection_fix.py).
    esd_of_M, DE8's esd_from_mlens and L352's project_M2 are NOT used anywhere.
  * CLASS 3.3.4 for the linear spectra of the web and the IGM (FP6's T_EH98 carries an h-units error; not used for new work).

PRE-DECLARED (written before any run of this script):
  H1 CONTROLS.  (a) XR26's committed lensing numbers are reproduced exactly by its own code: LCDM chi^2 = 10.15 and pull
     -0.39 sigma (8-400), the headline chain amplitude 1.1492 (linear base, +4.93 sigma) and 2.1344 (halofit), the phantom
     budget f* = 0.62 / 0.18; (b) FP17's threshold window is reproduced exactly: the heat-filter window as a threshold mass
     a0 xi^2/G = 0.40-6.72e6 Msun (canonical) / 0.58-8.12e6 (alt), the compactness gap C 2.91e-12 .. 3.71e-9, the length
     window 0.021-84 pc; (c) FP20's corrected KiDS base (isolated P2, FP1 E's machinery, exact projector) chi^2 = 139.800 /
     133.948 is reproduced to < 1e-3.  EXPECT TRUE.
  H2 THE KiDS REACH.  With the phantom sharply truncated at a fixed physical radius r_t (M_b profiled, as the record), KiDS
     tolerates (d chi^2 <= +9 against the untruncated law) only r_t >~ 1 Mpc without a 2-halo term; a 2-halo term (A <= 2)
     lowers the floor.  UNCERTAIN in size.
  H3 THE SEPARABILITY TABLE.  In the space of region variables: the field strength y, a length, a mass and a local
     overdensity each FAIL to separate every ON region from every OFF region; the bound state (enclosed overdensity above
     the turnaround value Delta_ta(z)) separates the web, the IGM, galaxies, KiDS and the z = 2.5 discs, and fails only the
     Solar System, which a threshold mass M_* in FP17's window repairs.  EXPECT TRUE.
  H4 [HEADLINE] THE SURVIVING SWITCH.  'ON iff the region is bound (turned around, Delta(<r) >= Delta_ta(z)) AND its mass
     exceeds M_*' passes every region: CMB lensing (the unbound linear web carries no phantom: Planck's 8-400 amplitude is
     LCDM's, within 2 sigma of 1.011 +- 0.028), the forest (the unbound IGM carries none), KiDS (the phantom truncated at each
     lens's own turnaround radius stays within d chi^2 <= +9), the z = 2.5 discs (ON at r_F) and the Solar System (M_* in
     FP17's window).  EXPECT TRUE.
  H5 THE VIRIALISED VARIANT.  'ON only inside the virial radius' FAILS KiDS without a 2-halo term.  EXPECT TRUE (reported).
  H6 THE LEAK (reported, an estimate).  If the law's phantom in the bound sub-regions of the web ADDS to the cold component
     there, the Press-Schechter turned-around fraction f_ta(k, z) of the linear web's phantom enters CMB lensing: expected to
     cost a sizeable fraction of XR26's excess (the answer decides whether the bound regions' phantom may add to, or must
     replace, the cold component -- part 5's question).  UNCERTAIN.
MUTATE=1 removes the switch from the web: the law acts on the linear web as the chain's H_S separator lets it (XR26's
headline).  The headline H4 must FAIL (rc = 1) on the CMB-lensing requirement.

DISCLOSURES.  (1) Debug runs: the first MUTATE run lacked the x-scan (H2c); it was added and both runs repeated; the x-scan's
window finder first returned 'inf' on a non-monotone scan and was replaced by a two-edged window before the committed runs.
(2) K4 and H7 were ADDED AFTER the committed-form runs, when lane CFG0 (running in parallel) reported that 'a turnaround switch
fails KiDS' from the record's h72 bounds.  Before adding them a scratch check (not committed) re-ran the x-scan with the
photometric masses FIXED and one coherent offset: the edge at x = 0.6-1.0 r_ta fit better than the unbounded phantom by
d chi^2 ~ 10-19, and the profiled masses had moved by <= 0.1 dex.  K4 reproduces h72; H7 shows the two statements concern
different edges.  No other check, threshold or number changed.

SCOPE.  Linear-theory yardsticks (XR26's for the controls and the leak; CLASS spectra for the region variables); spherical
top-hat collapse in the Planck LCDM background for Delta_ta(z) and delta_ta,lin(z); Bryan & Norman 1998's Delta_vir(z);
KiDS scored at the record's lead grade (isolated lenses, M_b profiled per bin, the record's linear 2-halo template).  No
particle-mesh or N-body run.  The Solar System rows are FP17's.

Run from the repository root:  python3 campaign_fresh_gravity/CFG4_switch.py      (MUTATE=1 for the control run)
"""
import os
import sys
import math
import json
import time
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG4_common as C
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erfc
from scipy.interpolate import RectBivariateSpline

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
R = C.Run("CFG4_switch")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("PRE-DECLARED")[0].strip())
P("\nPRE-DECLARED" + __doc__.split("PRE-DECLARED")[1].split("SCOPE.")[0].rstrip())
if C.MUTATE:
    P("\n  *** MUTATE=1: the switch is removed from the web (the law acts on the linear web as XR26's headline) -- H4 must FAIL ***")
A0 = C.A0
KIDS_TOL = 9.0

# ================================================================================================ K1 XR26
banner("K1  CONTROL: XR26's lensing pipeline (exec'd read-only from its committed source) reproduces its committed numbers")
t1 = time.time()
XR26 = os.path.join(C.HUB, "XR26_cmb.py")
X = C.exec_slices(XR26, [(None, "class _Tee:"),
                         ('OUT = {"lane": "XR26"', "P(__doc__.strip())"),
                         ("# ================================================================================================ inputs (published, committed)",
                          "# ================================================================================================ the patched CLASS"),
                         ('banner("K  CONTROLS', "cam = cres.get_cmb_power_spectra"),
                         ("# ---- FP13's (H_S) growth yardstick", "# ---- re-lensing with CAMB"),
                         ("# ================================================================================================ L late-time lensing",
                          "# L3/L4 the lensed spectra")], name="xr26_readonly")[0]
J26 = json.load(open(os.path.join(C.HUB, "XR26_cmb_results.json")))["numbers"]
HEAD = X["HEAD"]
L2x = X["L2"]["8-400"]
rows_c = J26["L2"]["8-400"]["rows"]
lin_now, nl_now = L2x["rows"][(HEAD, "lin")], L2x["rows"][(HEAD, "NL")]
lin_ref, nl_ref = rows_c[f"{HEAD} || lin"], rows_c[f"{HEAD} || NL"]
d_amp = max(abs(lin_now["amp"] - lin_ref["amp"]), abs(nl_now["amp"] - nl_ref["amp"]))
d_chi = max(abs(L2x["chi2_lcdm"] - J26["L2"]["8-400"]["chi2_lcdm"]), abs(lin_now["chi2"] - lin_ref["chi2"]))
d_f = max(abs(X["FSTAR"][b] - J26["L2b"]["f_star"][b]) for b in ("lin", "NL"))
P(f"    reproduced ({time.time() - t1:.0f} s): LCDM chi^2 = {L2x['chi2_lcdm']:.4f} (committed {J26['L2']['8-400']['chi2_lcdm']:.4f}), pull "
  f"{L2x['pull_lcdm']:+.3f}; headline amplitude linear base {lin_now['amp']:.6f} (committed {lin_ref['amp']:.6f}, pull {lin_now['pull']:+.2f}), "
  f"halofit {nl_now['amp']:.6f} (committed {nl_ref['amp']:.6f}); f* = {X['FSTAR']['lin']:.4f} / {X['FSTAR']['NL']:.4f} (committed "
  f"{J26['L2b']['f_star']['lin']:.4f} / {J26['L2b']['f_star']['NL']:.4f})")
check("K1 CONTROL: XR26's committed lensing numbers are reproduced exactly by its own code (exec'd read-only): LCDM chi^2 and pull, "
      "the headline amplitude on the linear and halofit bases, and the phantom budget f*",
      f"max |d amp| {d_amp:.1e}, max |d chi^2| {d_chi:.1e}, max |d f*| {d_f:.1e}; amplitudes {lin_now['amp']:.4f} / {nl_now['amp']:.4f}",
      d_amp < 1e-9 and d_chi < 1e-6 and d_f < 1e-9)
R.num("K1", dict(chi2_lcdm=L2x["chi2_lcdm"], pull_lcdm=L2x["pull_lcdm"], amp_lin=lin_now["amp"], amp_NL=nl_now["amp"],
                 pull_lin=lin_now["pull"], pull_NL=nl_now["pull"], f_star=X["FSTAR"], seconds=time.time() - t1))

# ================================================================================================ K2 FP17
banner("K2  CONTROL: FP17's threshold-mass theorem (exec'd read-only up to its V section) reproduces its committed window")
t2 = time.time()
FP17 = os.path.join(C.CHAIN, "FP17_screening_without_xi.py")
F17 = C.exec_slices(FP17, [(None, 'banner("V  (a) VAINSHTEIN')], name="fp17_readonly")[0]
J17 = json.load(open(os.path.join(C.CHAIN, "FP17_screening_without_xi_results.json")))["numbers"]
win_now = F17["WIN_M"]; win_ref = J17["M3"]["window_Msun"]
dev17 = max(abs(win_now[f][i] / win_ref[f][i] - 1) for f in C.FOOTS for i in (0, 1))
dev17 = max(dev17, abs(F17["C_sun_max"] / J17["M2"]["C_sun_max"] - 1), abs(F17["M_gal_min"] / J17["M2"]["M_gal_min"] - 1),
            max(abs(F17["LLEN"][f][i] / J17["M2"]["length_window_pc"][f][i] - 1) for f in C.FOOTS for i in (0, 1)))
C_gal_min = min(v[0] for v in F17["Cgal"].values())
P(f"    reproduced ({time.time() - t2:.0f} s): M_* window {win_now['canonical'][0]:.3f}-{win_now['canonical'][1]:.4e} Msun (canonical), "
  f"{win_now['alt'][0]:.3f}-{win_now['alt'][1]:.4e} (alt); compactness gap C {F17['C_sun_max']:.3e} .. {C_gal_min:.3e}; smallest SPARC "
  f"enclosed baryonic mass at the Sun's y {F17['M_gal_min']:.3e} Msun; length window {F17['LLEN']['canonical'][0]:.4f}-"
  f"{F17['LLEN']['canonical'][1]:.2f} pc")
check("K2 CONTROL: FP17's committed threshold window is reproduced exactly (the M_* window a0 xi^2/G on both footings, the compactness "
      "gap, the smallest SPARC enclosed mass at the Sun's y, the length window)", f"max relative deviation {dev17:.1e}", dev17 < 1e-12)
MSTAR_WIN = {f: tuple(win_now[f]) for f in C.FOOTS}
R.num("K2", dict(Mstar_window=MSTAR_WIN, C_sun_max=F17["C_sun_max"], C_gal_min=C_gal_min, M_gal_min=F17["M_gal_min"],
                 length_window_pc=F17["LLEN"], y_range=F17["y_lo"] if "y_lo" in F17 else None))

# ================================================================================================ K3 KiDS with the exact projector
banner("K3  CONTROL: FP1 E's KiDS-1000 machinery with FP20's exact projector reproduces FP20's corrected isolated P2 base")
t3 = time.time()
GK = {"np": np, "math": math, "os": os, "REPO": C.REPO, "G_SI": 6.67430e-11, "_trap": C._trap}
GK = C.exec_slices(os.path.join(C.CHAIN, "FP1_static_sector.py"),
                   [("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")], ns=GK, name="fp1_kids")[0]
FIX = C.ESDFix(GK["rrK"], GK["Rp"], GK["PCm2"], GK["MS"])
RRK, RPK, MPCK, MSK = GK["rrK"], GK["Rp"], GK["MPCm"], GK["MS"]
LM, NPB = GK["LM"], GK["npb"]
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
GN = 6.67430e-11


def kids_chi2(Mfun, foot, Amax=0.0, full=False):
    """chi^2 of the KiDS isolated lenses (FP1 E / L355 conventions: M_b profiled per bin over LM, optional linear 2-halo with
    amplitude in [0, Amax]); Mfun(Mb_kg, a0) returns the enclosed total mass on GK's r-grid; FP20's exact projector."""
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, A0[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    out = GK["kfit"]({foot: T}, foot, W0, Amax)
    return out if full else out[0]


def M_law(kfun):
    def f_(Mb, a0):
        y = GN * Mb / RRK ** 2 / a0
        return Mb * kfun(y)
    return f_


BASE = {(f, k): kids_chi2(M_law(kf), f) for f in C.FOOTS for k, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono))}
BASE2H = {(f, k): kids_chi2(M_law(kf), f, 2.0) for f in C.FOOTS for k, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono))}
NEWT = {f: kids_chi2(lambda Mb, a0: Mb * np.ones_like(RRK), f) for f in C.FOOTS}
P(f"    isolated law chi^2 (60 points, M_b profiled, exact projector): P2 {BASE[('canonical', 'P2')]:.3f} / {BASE[('alt', 'P2')]:.3f}; "
  f"nu_mono {BASE[('canonical', 'nu_mono')]:.3f} / {BASE[('alt', 'nu_mono')]:.3f}; with the 2-halo (A <= 2): P2 "
  f"{BASE2H[('canonical', 'P2')]:.3f} / {BASE2H[('alt', 'P2')]:.3f}; Newton (baryons only) {NEWT['canonical']:.1f} ({time.time() - t3:.0f} s)")
k3 = abs(BASE[("canonical", "P2")] - 139.800) < 1e-3 and abs(BASE[("alt", "P2")] - 133.948) < 1e-3
check("K3 CONTROL: FP1 E's KiDS machinery (exec'd read-only) with FP20's exact projector reproduces FP20's corrected isolated P2 base "
      "chi^2 139.800 / 133.948 (FP20 R7, the FP14/FP17 K rows)", f"{BASE[('canonical', 'P2')]:.4f} / {BASE[('alt', 'P2')]:.4f}", k3)
R.num("K3", dict(base={f"{k[0]}|{k[1]}": v for k, v in BASE.items()}, base_2h={f"{k[0]}|{k[1]}": v for k, v in BASE2H.items()},
                 newton=NEWT))

# ================================================================================================ collapse thresholds
banner("D  THE BOUND-STATE THRESHOLDS: spherical top-hat collapse in the Planck LCDM background (turnaround), the energy form, virial")
hK = GK["hK"]; OMK = GK["OmK"]; OLK = GK["OLK"]
H0K = 100 * hK * 1e3 / C.MPC


def tophat_turnaround(z_ta):
    """(1 + delta_NL at turnaround, delta_lin at turnaround) for a top-hat turning around at z_ta (growing-mode ICs)."""
    a_i = 1e-3
    H = lambda a: H0K * math.sqrt(OMK / a ** 3 + OLK)
    # background time -> scale factor
    def bg(t, y):
        return [y[0] * H(y[0])]

    def shell(d_i):
        Ri = 1.0
        Hi = H(a_i)
        Mfac = 0.5 * OMK * H0K ** 2 / a_i ** 3 * (1 + d_i) * Ri ** 3            # G M = (4 pi/3) G rho R^3 = 0.5 Om H0^2 a^-3 R^3
        def rhs(t, y):
            R_, V_, a_ = y
            return [V_, -Mfac / R_ ** 2 + OLK * H0K ** 2 * R_, a_ * H(a_)]
        ev = lambda t, y: y[1]
        ev.terminal = True; ev.direction = -1
        t_i = 2.0 / (3.0 * Hi)
        sol = solve_ivp(rhs, (t_i, t_i + 5e18), [Ri, Hi * Ri * (1 - d_i / 3.0), a_i], events=ev, rtol=1e-10, atol=1e-14,
                        max_step=1e16)
        if not sol.t_events[0].size:
            return None
        R_ta, _, a_ta = sol.y_events[0][0]
        return a_ta, (1 + d_i) * (Ri / R_ta) ** 3 * (a_ta / a_i) ** 3

    a_t = 1.0 / (1.0 + z_ta)
    d_i = brentq(lambda d: (shell(d) or (1e9, 0))[0] - a_t, 1.2e-3, 0.2, xtol=1e-12)
    a_ta, one_plus = shell(d_i)
    # linear growth D(a) from the growing mode (normalised at a_i with D ~ a)
    solD = solve_ivp(lambda N_, Y: [Y[1], 1.5 * OMK / math.exp(3 * N_) / (OMK / math.exp(3 * N_) + OLK) * Y[0]
                                    - (2 - 1.5 * OMK / math.exp(3 * N_) / (OMK / math.exp(3 * N_) + OLK)) * Y[1]],
                     (math.log(a_i), math.log(a_ta)), [1.0, 1.0], rtol=1e-10, atol=1e-14)
    d_lin = d_i * solD.y[0][-1]
    return one_plus, d_lin


def omega_m(z):
    return OMK * (1 + z) ** 3 / (OMK * (1 + z) ** 3 + OLK)


def delta_vir_mean(z):
    x = omega_m(z) - 1.0
    return (18 * math.pi ** 2 + 82 * x - 39 * x * x) / omega_m(z)               # Bryan & Norman 1998, relative to the mean


ZS = (0.0, 0.25, 0.5, 0.64, 2.0, 2.5, 3.0)
DTA = {z: tophat_turnaround(z) for z in ZS}
for z in ZS:
    P(f"    z = {z:4.2f}: turnaround 1 + delta_NL = {DTA[z][0]:.3f}, delta_lin = {DTA[z][1]:.4f}; energy-bound Delta = 1/Omega_m = "
      f"{1 / omega_m(z):.3f}; virial Delta_vir/Omega_m = {delta_vir_mean(z):.1f} (mean-density units)")
check("D1 (reported) the bound-state thresholds: the top-hat turnaround contrast approaches the EdS 5.55 (delta_lin 1.06) at high z "
      "and grows toward z = 0 as Lambda acts; the energy form and the virial contrast bracket it",
      "; ".join(f"z={z}: {DTA[z][0]:.2f}/{DTA[z][1]:.3f}" for z in ZS),
      abs(DTA[3.0][0] - 5.55) < 0.25 and abs(DTA[3.0][1] - 1.06) < 0.03, load_bearing=False)
R.num("D1", {str(z): dict(one_plus_delta_ta=DTA[z][0], delta_lin_ta=DTA[z][1], delta_E=1 / omega_m(z), delta_vir_mean=delta_vir_mean(z))
             for z in ZS})

# ================================================================================================ H2 the KiDS reach
banner("H2  THE KiDS REACH: the phantom truncated at a fixed radius, and at each lens's own bound radii (turnaround, energy, virial)")
ZL = GK["ZL"]
RHOM_ZL = GK["rho_m_z"] * MSK / C.MPC ** 3                                     # kg/m^3 at z_l = 0.25 (physical)


def M_trunc_fixed(kfun, rt_mpc):
    def f_(Mb, a0):
        M = M_law(kfun)(Mb, a0)
        Mt = np.interp(rt_mpc * MPCK, RRK, M)
        return np.where(RRK <= rt_mpc * MPCK, M, Mt)
    return f_


def r_bound(M, Delta):
    """radius [m] where the enclosed mean density of M(r) falls to Delta x the mean matter density at z_l (first crossing)."""
    D = M / (4.0 / 3.0 * math.pi * RRK ** 3 * RHOM_ZL)
    k = np.where(D < Delta)[0]
    if not len(k) or k[0] == 0:
        return RRK[-1] if not len(k) else RRK[0]
    i = k[0]
    return float(math.exp(np.interp(math.log(Delta), [math.log(D[i]), math.log(D[i - 1])], [math.log(RRK[i]), math.log(RRK[i - 1])])))


def M_trunc_bound(kfun, Delta):
    def f_(Mb, a0):
        M = M_law(kfun)(Mb, a0)
        rt = r_bound(M, Delta)
        Mt = np.interp(rt, RRK, M)
        return np.where(RRK <= rt, M, Mt)
    return f_


RT_SCAN = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0, 3.0, 5.0)
SCAN = {}
for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        for A in (0.0, 2.0):
            SCAN[(f, kn, A)] = [kids_chi2(M_trunc_fixed(kf, rt), f, A) - BASE[(f, kn)] for rt in RT_SCAN]


def floor_of(v):
    v = np.asarray(v)
    ok = v <= KIDS_TOL
    if ok.all():
        return RT_SCAN[0]
    if not ok[-1]:
        return float("inf")
    j = int(np.max(np.where(~ok)[0]))
    x0, x1, y0, y1 = math.log(RT_SCAN[j]), math.log(RT_SCAN[j + 1]), v[j], v[j + 1]
    return float(math.exp(x0 + (KIDS_TOL - y0) * (x1 - x0) / (y1 - y0)))


FLOOR = {k: floor_of(v) for k, v in SCAN.items()}
for k, v in SCAN.items():
    P(f"    {k[0]:9s} {k[1]:8s} 2-halo A <= {k[2]:.0f}: d chi^2 vs the untruncated isolated law at r_t = " +
      ", ".join(f"{rt:g}: {d:+.1f}" for rt, d in zip(RT_SCAN, v)) + f"  -> KiDS floor r_t >= {FLOOR[k]:.2f} Mpc")
h2 = all(0.5 <= FLOOR[(f, k, 0.0)] <= 2.0 for f in C.FOOTS for k in ("P2", "nu_mono"))
check("H2 (reported; pre-declared UNCERTAIN in size) THE KiDS REACH: with the phantom sharply truncated at a fixed physical radius, "
      "KiDS (d chi^2 <= +9 against the untruncated law, M_b profiled) needs r_t of order 1 Mpc without a 2-halo term",
      "; ".join(f"{k[0][:3]}/{k[1]}/A{k[2]:.0f}: r_t >= {v:.2f} Mpc" for k, v in FLOOR.items()), h2, load_bearing=False)
R.num("H2", dict(scan={f"{k[0]}|{k[1]}|A{k[2]:.0f}": v for k, v in SCAN.items()}, r_t=RT_SCAN,
                 floor={f"{k[0]}|{k[1]}|A{k[2]:.0f}": v for k, v in FLOOR.items()}))

# the bound radii of the KiDS lenses and the truncation at them
DEF = {"turnaround": DTA[0.25][0], "energy": 1.0 / omega_m(0.25), "virial": delta_vir_mean(0.25), "200m": 200.0}
BOUNDS = {}
for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        for dn, Dv in DEF.items():
            for A in (0.0, 2.0):
                chi, pars = kids_chi2(M_trunc_bound(kf, Dv), f, A, full=True)
                BOUNDS[(f, kn, dn, A)] = chi - BASE[(f, kn)]
RADII = {}
for lm in (10.0, 10.5, 11.0, 11.5):
    Mb = 10 ** lm * MSK
    for f in C.FOOTS:
        M = M_law(C.nu_p2)(Mb, A0[f])
        RADII[(f, lm)] = {dn: r_bound(M, Dv) / MPCK for dn, Dv in DEF.items()}
for (f, lm), v in RADII.items():
    P(f"    {f:9s} log M_b = {lm:.1f} (P2 phantom, z = 0.25): r_turnaround {v['turnaround']:.2f} Mpc, r_energy {v['energy']:.2f}, "
      f"r_virial {v['virial']:.3f}, r_200m {v['200m']:.3f} Mpc")
for k, v in BOUNDS.items():
    if k[3] == 0.0:
        P(f"    {k[0]:9s} {k[1]:8s} truncated at r_{k[2]:10s}: d chi^2 {v:+8.2f} (no 2-halo), {BOUNDS[(k[0], k[1], k[2], 2.0)]:+8.2f} "
          f"(2-halo A <= 2)")
R.num("H2b", dict(d_chi2={f"{k[0]}|{k[1]}|{k[2]}|A{k[3]:.0f}": v for k, v in BOUNDS.items()},
                  radii={f"{k[0]}|{k[1]}": v for k, v in RADII.items()}, thresholds=DEF))


def kfit_full(Mfun, foot, Amax=0.0):
    """the record's kfit logic (FP1 E / L355), re-typed only to also return each bin's profiled log M_b; checked equal to kfit."""
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, A0[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    blk = np.tensordot(W0, T, axes=(0, 0))
    mods, lms, amps = [], [], []
    for b in range(4):
        bb = None
        for im in range(len(LM)):
            mk = blk[im, b]
            A = 0.0
            if Amax > 0:
                t2 = GK["T2H"][b]; wv = 1 / GK["Sd"][b] ** 2
                A = float(np.clip(np.sum(wv * t2 * (GK["Ed"][b] - mk)) / np.sum(wv * t2 * t2), 0.0, Amax))
                mk = mk + A * t2
            c__ = float(np.sum(((GK["Ed"][b] - mk) / GK["Sd"][b]) ** 2))
            if bb is None or c__ < bb[0]:
                bb = (c__, mk, LM[im], A)
        mods.append(bb[1]); lms.append(float(bb[2])); amps.append(bb[3])
    dv = np.concatenate(GK["Ed"]) - np.concatenate(mods)
    return float(dv @ GK["Ci"] @ dv), lms, amps


def M_trunc_xta(kfun, x):
    """the phantom truncated at x times the lens's own turnaround radius (z_l = 0.25, the top-hat Delta_ta)."""
    def f_(Mb, a0):
        M = M_law(kfun)(Mb, a0)
        rt = x * r_bound(M, DTA[0.25][0])
        Mt = np.interp(rt, RRK, M)
        return np.where(RRK <= rt, M, Mt)
    return f_


chk_full, LMB, _ = kfit_full(M_law(C.nu_p2), "canonical")
P(f"    re-typed kfit reproduces the record's: {chk_full:.6f} vs {BASE[('canonical', 'P2')]:.6f}; the bins' profiled log M_b (P2, "
  f"canonical, untruncated) = {LMB}")
XS = (0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.25, 1.5)
XSCAN = {}
for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        for A in (0.0, 2.0):
            XSCAN[(f, kn, A)] = [kids_chi2(M_trunc_xta(kf, x), f, A) - BASE[(f, kn)] for x in XS]


def xwindow(v):
    """the contiguous passing window (d chi^2 <= +9) around the scan's minimum, edges interpolated linearly in x."""
    v = np.asarray(v)
    j0 = int(np.argmin(v))
    if v[j0] > KIDS_TOL:
        return (float("inf"), float("-inf"))
    lo = j0
    while lo > 0 and v[lo - 1] <= KIDS_TOL:
        lo -= 1
    hi = j0
    while hi < len(v) - 1 and v[hi + 1] <= KIDS_TOL:
        hi += 1
    x_lo = XS[0] if lo == 0 else float(XS[lo - 1] + (KIDS_TOL - v[lo - 1]) * (XS[lo] - XS[lo - 1]) / (v[lo] - v[lo - 1]))
    x_hi = float("inf") if hi == len(v) - 1 else float(XS[hi] + (KIDS_TOL - v[hi]) * (XS[hi + 1] - XS[hi]) / (v[hi + 1] - v[hi]))
    return (x_lo, x_hi)


XFLOOR = {k: xwindow(v) for k, v in XSCAN.items()}
for k, v in XSCAN.items():
    P(f"    {k[0]:9s} {k[1]:8s} 2-halo A <= {k[2]:.0f}: truncation at x r_ta: " + ", ".join(f"{x:g}: {d:+.1f}" for x, d in zip(XS, v))
      + f"  -> KiDS window x in [{XFLOOR[k][0]:.2f}, {XFLOOR[k][1]:.2f}]; best x = {XS[int(np.argmin(v))]:g} ({min(v):+.1f})")
R.num("H2c", dict(x=XS, scan={f"{k[0]}|{k[1]}|A{k[2]:.0f}": v for k, v in XSCAN.items()},
                  x_floor={f"{k[0]}|{k[1]}|A{k[2]:.0f}": v for k, v in XFLOOR.items()}, lens_logMb_P2_canonical=LMB,
                  kfit_retyped_check=chk_full))
check("H2c (reported) the KiDS reach in units of each lens's own turnaround radius: the smallest x with d chi^2 <= +9 when the phantom "
      "is cut at x r_ta (the number part 5's budget is set against), and the window's upper edge",
      "; ".join(f"{k[0][:3]}/{k[1]}/A{k[2]:.0f}: x in [{v[0]:.2f}, {v[1]:.2f}]" for k, v in XFLOOR.items()),
      abs(chk_full - BASE[("canonical", "P2")]) < 1e-9, load_bearing=False)
h5 = all(BOUNDS[(f, k, "virial", 0.0)] > KIDS_TOL for f in C.FOOTS for k in ("P2", "nu_mono"))
check("H5 (reported) THE VIRIALISED VARIANT FAILS KiDS without a 2-halo term: the phantom cut at each lens's own virial radius costs "
      "d chi^2 > +9 on both footings for both kernels",
      "; ".join(f"{f[:3]}/{k}: {BOUNDS[(f, k, 'virial', 0.0)]:+.1f} (2h {BOUNDS[(f, k, 'virial', 2.0)]:+.1f})" for f in C.FOOTS
                for k in ("P2", "nu_mono")), h5, load_bearing=False)

# ================================================================================================ H7 the two kinds of edge (h72)
banner("H7  TWO KINDS OF EDGE: a RESPONSE edge (the boost returns to 1: the phantom's enclosed mass stops gravitating; the record's "
       "h72) vs a DENSITY edge (the phantom's density ends: its enclosed mass keeps gravitating as 1/r^2)")
t7 = time.time()
H72 = os.path.join(C.REPO, "hunt_2026", "h72_where_the_boost_ends.py")
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
HN = C.exec_slices(H72, [(None, 'P(""); P("4. mutation control')], name="h72_readonly")[0]
sys.path.pop(0)
out72 = open(os.path.join(C.REPO, "hunt_2026", "h72_where_the_boost_ends.out")).read()
ref72 = {}
import re as _re
for foot_ in ("canonical", "alt"):
    m_ = _re.search(foot_ + r"\s+3-sigma lower bounds on r_end: bin 1: > ([0-9.]+) Mpc, bin 2: > ([0-9.]+) Mpc, bin 3: > ([0-9.]+) Mpc, "
                    r"bin 4: > ([0-9.]+) Mpc", out72)
    ref72[foot_] = [float(m_.group(i)) for i in range(1, 5)]
now72 = {f: [HN["lims"][(f, b)] for b in (1, 2, 3, 4)] for f in ("canonical", "alt")}
k72 = all(abs(round(now72[f][i], 2) - ref72[f][i]) < 1e-9 for f in now72 for i in range(4))
P(f"    h72 (exec'd read-only): 3-sigma lower bounds on a RESPONSE edge: canonical {[round(v, 2) for v in now72['canonical']]} Mpc, alt "
  f"{[round(v, 2) for v in now72['alt']]} (committed {ref72['canonical']} / {ref72['alt']})")
check("K4 CONTROL: the record's h72 (hunt_2026/h72_where_the_boost_ends.py, exec'd read-only up to its mock section) reproduces its "
      "committed 3-sigma lower bounds on where the boost ends: > 1.67 / 2.07 / 3.44 / 2.77 Mpc in the four Brouwer bins, both footings",
      f"{now72} vs {ref72}", k72)
# the density edge in h72's own convention (Fig-9 RAR, fixed photometric masses, one coherent amplitude): the boost FREEZES at r_e
gb0, radH, MbH, binsH = HN["gb0"], HN["rad"], HN["Mb"], HN["bins"]
nuH, profH, chiH = HN["nu"], HN["profileA"], HN["chi2_of"]


def model_edge(b, a0, A, r_e):
    y = gb0 / a0
    ye = (HN["G"] * MbH[b] / (r_e * HN["Mpc"]) ** 2) / a0 if np.isfinite(r_e) else 0.0
    return nuH(np.maximum(y, ye)) * gb0 * 10 ** A


E72 = {}
for foot_, a0_ in HN["A0"].items():
    for b in (1, 2, 3, 4):
        m = np.zeros(60, bool); m[15 * (b - 1):15 * b] = True
        cb, _ = profH(lambda A: {bb: model_edge(bb, a0_, A, np.inf) for bb in binsH}, m)
        lim = 0.0
        for r_e in np.geomspace(0.1, 30.0, 80):
            c_, _ = profH(lambda A, re=r_e: {bb: model_edge(bb, a0_, A, re) if bb == b else model_edge(bb, a0_, A, np.inf) for bb in binsH}, m)
            if c_ - cb > 9.0:
                lim = r_e
        E72[(foot_, b)] = lim
P("    the DENSITY edge in the same convention (the boost frozen at its value at r_e): 3-sigma lower bounds on r_e: " +
  "; ".join(f"{f}: " + ", ".join(f"bin {b} > {E72[(f, b)]:.2f}" for b in (1, 2, 3, 4)) for f in ("canonical", "alt")) + " Mpc")
# the fixed-mass ESD scan (exact projector): h72's photometric masses and one coherent offset (prior (dA/0.3)^2), the density edge at x r_ta
LOGM72 = [10.0, 10.45, 10.7, 10.9]; FG72 = [0.5, 0.3, 0.2, 0.15]
LMB72 = [math.log10(10 ** l_ * (1 + f_)) for l_, f_ in zip(LOGM72, FG72)]


def esd_bin(b, lm, a0, x, A2h, kf=C.nu_p2):
    Mb = 10 ** lm * MSK
    M = M_law(kf)(Mb, a0)
    if x is not None:
        rt = x * r_bound(M, DTA[0.25][0])
        M = np.where(RRK <= rt, M, np.interp(rt, RRK, M))
    return np.interp(GK["Rd"][b], RPK / MPCK, FIX(M, Mb)) + A2h * GK["T2H"][b]


def chi2_fixed(x, A2h, foot_="canonical", kf=C.nu_p2):
    best = None
    for dA in np.linspace(-0.3, 0.5, 81):
        dv = np.concatenate(GK["Ed"]) - np.concatenate([esd_bin(b, LMB72[b] + dA, A0[foot_], x, A2h, kf) for b in range(4)])
        c_ = float(dv @ GK["Ci"] @ dv) + (dA / 0.3) ** 2
        if best is None or c_ < best[0]:
            best = (c_, dA)
    return best


FIXS = {}
for foot_ in C.FOOTS:
    base_ = chi2_fixed(None, 0.0, foot_)
    for x in (1.5, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3):
        for A2h in (0.0, 1.0):
            c_, dA = chi2_fixed(x, A2h, foot_)
            FIXS[(foot_, x, A2h)] = (c_ - base_[0], dA)
    FIXS[(foot_, "base")] = base_
    P(f"    fixed photometric masses (h72's bins), exact projector, {foot_}: untruncated chi^2 {base_[0]:.1f} (offset {base_[1]:+.2f} dex); density "
      "edge at x r_ta: " + ", ".join(f"x {x}: {FIXS[(foot_, x, 0.0)][0]:+.1f} / 2h {FIXS[(foot_, x, 1.0)][0]:+.1f}" for x in (1.5, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3)))
P(f"    ({time.time() - t7:.0f} s)")
resp_ta = {f: [now72[f][b - 1] for b in (1, 2, 3, 4)] for f in now72}
h7 = (all(FIXS[(f, 1.0, 0.0)][0] <= KIDS_TOL for f in C.FOOTS) and all(E72[(f, b)] < now72[f][b - 1] for f in now72 for b in (1, 2, 3, 4)))
check("H7 (reported; added after CFG0 named h72's bounds, disclosed) THE TWO KINDS OF EDGE: a RESPONSE edge (the boost returns to 1) "
      "must lie beyond h72's 1.7-3.4 Mpc, but a DENSITY edge (the phantom's density ends, its enclosed mass keeps gravitating) is "
      "allowed much further in -- with the photometric masses FIXED (h72's convention, exact projector) an edge at the turnaround radius "
      "costs d chi^2 <= +9 against the unbounded phantom on both footings",
      "; ".join(f"{f}: response > {[round(v, 2) for v in now72[f]]} Mpc, density > {[round(E72[(f, b)], 2) for b in (1, 2, 3, 4)]} Mpc; "
                f"fixed-mass x=1 {FIXS[(f, 1.0, 0.0)][0]:+.1f}, x=0.6 {FIXS[(f, 0.6, 0.0)][0]:+.1f}, x=0.4+2h {FIXS[(f, 0.4, 1.0)][0]:+.1f}"
                for f in C.FOOTS), h7, load_bearing=False,
      reading="CFG0's 'a turnaround switch fails KiDS' is the response edge (h72's model); the target's edge is a density edge -- "
              "the field outside it is Newtonian from the enclosed (baryons + phantom) mass.  A construction whose switch acts on the "
              "field law itself (a response gate) fails KiDS; one that confines the phantom's SOURCE density passes")
R.num("H7", dict(h72_response_bounds=now72, h72_committed=ref72, density_edge_bounds={f"{k[0]}|b{k[1]}": v for k, v in E72.items()},
                 fixed_mass_scan={f"{k[0]}|x{k[1]}|A{k[2]}" if len(k) == 3 else f"{k[0]}|base": v for k, v in FIXS.items()},
                 photometric_logMb=LMB72))

# ================================================================================================ region variables
banner("V  THE REGION VARIABLES: field strength, length, mass, local and enclosed overdensity, flow state -- for every region")
cl = X["cl_fid"]; hF = X["H_FID"]
BG = cl.get_background()
OM0 = cl.Omega_m(); OB0 = cl.Omega_b()
RHOC0 = 3 * (100 * hF * 1e3 / C.MPC) ** 2 / (8 * math.pi * C.G_SI)


def rho_m(z):
    return OM0 * RHOC0 * (1 + z) ** 3


def delta2(k_h, z):
    """dimensionless linear power at k [h/Mpc], z (CLASS)."""
    k = k_h * hF
    return k ** 3 * cl.pk_lin(k, z) / (2 * math.pi ** 2)


def sigma_R(Rh, z):
    return cl.sigma(Rh / hF, z)                                                   # R in Mpc/h -> Mpc


def y_mode(k_h, z, a0, baryons=True):
    """the per-mode physical field of a linear mode (the record's per-mode reading) in units of a0; baryons-only if asked."""
    kphys = k_h * hF * (1 + z) / C.MPC
    g = 4 * math.pi * C.G_SI * rho_m(z) * math.sqrt(delta2(k_h, z)) / kphys
    return g * (OB0 / OM0 if baryons else 1.0) / a0


REG = {}
# web: z <= 0.64, k = 0.1-1 h/Mpc
web = []
for z in (0.0, 0.25, 0.5, 0.64):
    for kh in (0.1, 0.3, 1.0):
        Rh = 1.0 / kh
        s = sigma_R(Rh, z)
        web.append(dict(z=z, k=kh, R_phys_Mpc=Rh / hF / (1 + z), M=rho_m(z) * 4 / 3 * math.pi * (Rh / hF / (1 + z) * C.MPC) ** 3 / C.MSUN,
                        sigma=s, f_ta=float(erfc(DTA[min(ZS, key=lambda q: abs(q - z))][1] / (math.sqrt(2) * s))),
                        y_b={f: y_mode(kh, z, A0[f]) for f in C.FOOTS}, y_all={f: y_mode(kh, z, A0[f], False) for f in C.FOOTS}))
REG["web"] = web
# forest: z = 2, 3; k = 1-20 h/Mpc (the proxy's k_F = 10-20 and its k_par range)
igm = []
for z in (2.0, 2.5, 3.0):
    for kh in (1.0, 5.0, 10.0, 20.0):
        Rh = 1.0 / kh
        s = sigma_R(Rh, z)
        igm.append(dict(z=z, k=kh, R_phys_Mpc=Rh / hF / (1 + z), M=rho_m(z) * 4 / 3 * math.pi * (Rh / hF / (1 + z) * C.MPC) ** 3 / C.MSUN,
                        sigma=s, f_ta=float(erfc(DTA[min(ZS, key=lambda q: abs(q - z))][1] / (math.sqrt(2) * s))),
                        y_b={f: y_mode(kh, z, A0[f]) for f in C.FOOTS}, y_all={f: y_mode(kh, z, A0[f], False) for f in C.FOOTS}))
REG["forest"] = igm
for w in web:
    w["f_ta"] = float(erfc(DTA[min(ZS, key=lambda q: abs(q - w['z']))][1] / (math.sqrt(2) * w["sigma"])))
for nm_, rows in (("web (z <= 0.64)", web), ("IGM (z = 2-3)", igm)):
    for r_ in rows:
        P(f"    {nm_:16s} z = {r_['z']:4.2f} k = {r_['k']:5.1f} h/Mpc: R_phys {r_['R_phys_Mpc']:7.3f} Mpc, M {r_['M']:.2e} Msun, sigma(R) "
          f"{r_['sigma']:.3f}, PS turned-around fraction {r_['f_ta']:.3f}; per-mode y (baryons) {r_['y_b']['canonical']:.2e} / all matter "
          f"{r_['y_all']['canonical']:.2e} (canonical)")
# ON regions: SPARC points (P2, canonical best Upsilon from part 1 if available)
GAL = C.load_sparc()
U_c = 0.70
sp = dict(y=[], r_kpc=[], M=[], Denc=[])
for g in GAL:
    vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U_c * g["Vdisk"] ** 2 + 1.4 * U_c * g["Vbul"] ** 2
    rr = g["R"] * C.KPC
    gb = vb2 * 1e6 / rr
    m = gb > 0
    y = gb[m] / A0["canonical"]
    Mb = gb[m] * rr[m] ** 2 / C.G_SI
    Mt = C.nu_p2(y) * Mb
    sp["y"] += list(y); sp["r_kpc"] += list(g["R"][m]); sp["M"] += list(Mb / C.MSUN)
    sp["Denc"] += list(Mt / (4 / 3 * math.pi * rr[m] ** 3 * rho_m(0.0)))
for k in sp:
    sp[k] = np.array(sp[k])
REG["sparc"] = dict(y=[float(sp["y"].min()), float(sp["y"].max())], r_kpc=[float(sp["r_kpc"].min()), float(sp["r_kpc"].max())],
                    M=[float(sp["M"].min()), float(sp["M"].max())], Denc_min=float(sp["Denc"].min()))
P(f"    SPARC (P2, Upsilon 0.70, canonical): y {REG['sparc']['y'][0]:.2e}-{REG['sparc']['y'][1]:.1f}; r {REG['sparc']['r_kpc'][0]:.2f}-"
  f"{REG['sparc']['r_kpc'][1]:.0f} kpc; enclosed M_b {REG['sparc']['M'][0]:.2e}-{REG['sparc']['M'][1]:.2e} Msun; smallest enclosed "
  f"overdensity (law's total mass / mean matter) {REG['sparc']['Denc_min']:.2e}")
# KiDS at the reach: y, local and enclosed overdensity at r = FLOOR (canonical, P2, no 2-halo), for the bins' mass range
rK = FLOOR[("canonical", "P2", 0.0)] if math.isfinite(FLOOR[("canonical", "P2", 0.0)]) else 1.0
kid = []
for lm in (10.0, 10.5, 11.0, 11.5):
    Mb = 10 ** lm * C.MSUN
    for f in C.FOOTS:
        r = rK * C.MPC
        y = C.G_SI * Mb / r ** 2 / A0[f]
        Mt = C.nu_p2(y) * Mb
        e_ = 1e-4
        dM = (C.nu_p2(C.G_SI * Mb / (r * (1 + e_)) ** 2 / A0[f]) * Mb * 1 - C.nu_p2(C.G_SI * Mb / (r * (1 - e_)) ** 2 / A0[f]) * Mb) / (2 * e_ * r)
        rho_loc = dM / (4 * math.pi * r ** 2)
        kid.append(dict(lm=lm, foot=f, r_Mpc=rK, y=float(y), M=float(Mt / C.MSUN), Denc=float(Mt / (4 / 3 * math.pi * r ** 3 * RHOM_ZL)),
                        dloc=float(rho_loc / RHOM_ZL)))
REG["kids"] = kid
for r_ in kid:
    if r_["foot"] == "canonical":
        P(f"    KiDS lens log M_b = {r_['lm']:.1f} at the reach r = {r_['r_Mpc']:.2f} Mpc (z = 0.25): y {r_['y']:.2e}, total M {r_['M']:.2e} Msun, "
          f"enclosed overdensity {r_['Denc']:.1f} (turnaround {DTA[0.25][0]:.2f}), local 1 + delta {r_['dloc']:.2f}")
# the z = 2.5 discs (the flagship: g_bar = 0.1 a0)
disc = []
for lm in (10.0, 11.0):
    Mb = 10 ** lm * C.MSUN
    for f in C.FOOTS:
        rF = math.sqrt(C.G_SI * Mb / (0.1 * A0[f]))
        Mt = C.nu_p2(0.1) * Mb
        disc.append(dict(lm=lm, foot=f, rF_kpc=rF / C.KPC, Denc=float(Mt / (4 / 3 * math.pi * rF ** 3 * rho_m(2.5))), y=0.1, M=float(Mt / C.MSUN)))
REG["discs"] = disc
for r_ in disc:
    P(f"    z = 2.5 disc log M_b = {r_['lm']:.0f} ({r_['foot']}): r_F = {r_['rF_kpc']:.1f} kpc, enclosed overdensity {r_['Denc']:.2e} "
      f"(turnaround {DTA[2.5][0]:.2f}, virial {delta_vir_mean(2.5):.0f})")
# the Solar System (FP17 M1)
REG["solar"] = dict(r_AU=[float(F17["r_lo_AU"]), float(F17["r_hi_AU"])], y=[float(F17["y_lo"]), float(F17["y_hi"])], M=1.0)
P(f"    Solar System (FP17 M1): Q2 made at r = {REG['solar']['r_AU'][0]:.0f}-{REG['solar']['r_AU'][1]:.0f} AU, y_N {REG['solar']['y'][0]:.2f}-"
  f"{REG['solar']['y'][1]:.1f}, M = 1 Msun, bound")
R.num("V", REG)

# ================================================================================================ H3 separability
banner("H3  THE SEPARABILITY TABLE: can a threshold on each variable put every ON region on one side and every OFF region on the other?")
foot = "canonical"
kidf = [r_ for r_ in kid if r_["foot"] == foot]
# system (baryonic) masses of the ON systems
Mb_sparc = []
for g in GAL:
    if g["meta"]:
        Mb_sparc.append(U_c * g["meta"]["L36"] * 1e9 + 1.33 * g["meta"]["MHI"] * 1e9)
Mb_sparc = np.array(Mb_sparc)
MSYS_ON = [float(Mb_sparc.min()), 10 ** 11.5]
# the IGM's high-density tail at the Jeans scale (lognormal, 97.5th percentile of 1 + delta)
sJ = max(r_["sigma"] for r_ in igm if r_["k"] >= 10)
sln = math.sqrt(math.log(1 + sJ ** 2))
igm_hi = math.exp(-0.5 * sln ** 2 + 1.96 * sln)
tab = []
# (1) field strength (the record's 'yield'); the field-energy density g^2/(8 pi G) against rho_Lambda c^2 is the same variable
yon = min(REG["sparc"]["y"][0], min(r_["y"] for r_ in kidf), 0.1)
yoff = max(max(w["y_b"][foot] for w in web), max(w["y_b"][foot] for w in igm))
sep1 = yon > yoff
ss1 = REG["solar"]["y"][1] < yon
tab.append(("field strength y = g_bar/a0 (the 'yield'; equivalently g^2/8piG against rho_Lambda c^2)", "ON iff y >= y_th",
            f"ON needs y_th <= {yon:.2e} (KiDS at the reach); the web/IGM modes' own field reaches {yoff:.2e}; the Sun's Q2 region "
            f"(y = {REG['solar']['y'][0]:.1f}-{REG['solar']['y'][1]:.0f}) would be ON", sep1, ss1))
# (2) length band
r_on_lo, r_on_hi = REG["sparc"]["r_kpc"][0] * 1e-3, rK
igm_r = [min(r_["R_phys_Mpc"] for r_ in igm), max(r_["R_phys_Mpc"] for r_ in igm)]
sep2 = (igm_r[1] < r_on_lo) or (igm_r[0] > r_on_hi)
ss2 = REG["solar"]["r_AU"][1] * 1.495978707e11 / C.MPC < r_on_lo
tab.append(("length r", "ON iff r_min <= r <= r_max",
            f"ON needs r in [{r_on_lo * 1e3:.2f} kpc, {r_on_hi:.2f} Mpc]; the IGM's forest scales {igm_r[0] * 1e3:.0f}-{igm_r[1] * 1e3:.0f} kpc "
            f"(physical) lie inside; the Sun's Q2 region lies below r_min (FP17's length key)", sep2, ss2))
# (3) system mass band
igm_M = [min(r_["M"] for r_ in igm), max(r_["M"] for r_ in igm)]
web_M = min(r_["M"] for r_ in web)
sep3 = (igm_M[1] < MSYS_ON[0] or igm_M[0] > MSYS_ON[1]) and web_M > max(r_["M"] for r_ in kidf)
ss3 = 1.0 < MSYS_ON[0]
tab.append(("system mass M", "ON iff M_* <= M <= M_max",
            f"ON systems span M_b {MSYS_ON[0]:.1e}-{MSYS_ON[1]:.1e} Msun (KiDS totals to {max(r_['M'] for r_ in kidf):.1e}); the IGM's "
            f"forest-scale masses {igm_M[0]:.1e}-{igm_M[1]:.1e} fall inside, the web's >= {web_M:.1e} overlap KiDS's totals", sep3, ss3))
# (4) local overdensity
don = min(r_["dloc"] for r_ in kidf)
sep4 = don > igm_hi and don > 1 + max(w["sigma"] for w in web)
tab.append(("local overdensity 1 + delta (total)", "ON iff 1 + delta >= t",
            f"ON needs t <= {don:.2f} (KiDS at the reach); the IGM's 97.5% tail at the Jeans scale reaches {igm_hi:.2f} (lognormal, "
            f"sigma {sJ:.2f}); the Sun's surroundings are dense (ON)", sep4, False))
# (5) bound: enclosed overdensity >= the turnaround contrast
Dk = min(r_["Denc"] for r_ in kidf)
web_typ = max(1 + w["sigma"] for w in web if w["z"] <= 0.64)
igm_typ = max(1 + r_["sigma"] for r_ in igm)
sep5 = (Dk >= DTA[0.25][0]) and (REG["sparc"]["Denc_min"] >= DTA[0.0][0]) and (min(r_["Denc"] for r_ in disc) >= DTA[2.5][0]) \
    and (web_typ < DTA[0.0][0]) and (igm_typ < DTA[3.0][0])
tab.append(("bound state: enclosed overdensity Delta(<r) >= Delta_ta(z) (turned around; flow converging)", "ON iff Delta >= Delta_ta(z)",
            f"ON: KiDS at the reach {Dk:.1f} >= {DTA[0.25][0]:.2f}; SPARC >= {REG['sparc']['Denc_min']:.1e}; discs >= "
            f"{min(r_['Denc'] for r_ in disc):.1e}.  OFF: the linear web's 1-sigma enclosed contrast <= {web_typ:.2f} and the IGM's at the "
            f"Jeans scale <= {igm_typ:.2f}, below Delta_ta (their turned-around fractions ARE bound structure, where the law belongs).  The Sun "
            f"is bound (ON)", sep5, False))
# (6) bound AND system mass >= M_*
mlo = {f: max(1.0, MSTAR_WIN[f][0]) for f in C.FOOTS}
ss6 = all(mlo[f] < MSTAR_WIN[f][1] <= MSYS_ON[0] for f in C.FOOTS)
tab.append(("bound AND system mass M_b >= M_* (FP17's window)", "ON iff Delta >= Delta_ta(z) and M_b >= M_*",
            f"as the row above; the Sun (1 Msun) is OFF for any M_* in (1, {MSTAR_WIN['canonical'][1]:.2e}] (canonical) / (1, "
            f"{MSTAR_WIN['alt'][1]:.2e}] (alt), below SPARC's smallest galaxy (M_b {MSYS_ON[0]:.1e})", sep5, ss6))
for name, rule, why, sep_, ss_ in tab:
    verdict = "SEPARATES ALL" if (sep_ and ss_) else ("fails the Sun only" if sep_ else "FAILS")
    P(f"    {verdict:18s} {name}\n                       rule: {rule}\n                       {why}")
h3 = (not any(t[3] and t[4] for t in tab[:4])) and (not any(t[3] for t in tab[:4])) and tab[4][3] and (not tab[4][4]) \
    and tab[5][3] and tab[5][4]
check("H3 THE SEPARABILITY TABLE: field strength, length, mass and local overdensity each FAIL to separate the ON regions from the web "
      "and the IGM; the bound state (Delta(<r) >= Delta_ta(z)) separates everything except the Solar System, and bound AND M_b >= M_* "
      "separates everything", "; ".join(f"{t[0].split(':')[0].split('(')[0].strip()[:30]}: web/IGM {'ok' if t[3] else 'x'}, Sun "
                                        f"{'ok' if t[4] else 'x'}" for t in tab), h3)
R.num("H3", [dict(criterion=t[0], rule=t[1], why=t[2], separates_web_igm=t[3], separates_sun=t[4]) for t in tab])
R.num("H3_masses", dict(ON_system_Mb=MSYS_ON, igm_M=igm_M, web_M_min=web_M, igm_hi_1pd=igm_hi))

# ================================================================================================ H4 the surviving switch in the pipelines
banner("H4  THE SURVIVING SWITCH IN THE RECORD'S PIPELINES: CMB lensing, the forest, KiDS, the z = 2.5 discs, the Solar System")
LA = X["LENS_AMP"]["8-400"]
if C.MUTATE:
    amp_switch, pull_switch, chi_switch = lin_now["amp"], lin_now["pull"], lin_now["chi2"]
    P("    [MUTATE] no switch in the web: the law acts on the linear web as XR26's headline (H_S) lets it")
else:
    bp_l = X["bandpowers"](lambda ll: np.ones_like(ll, float), "8-400")
    w8 = 1 / np.array([b_[3] for b_ in X["PL18_MV"]["8-400"]]) ** 2
    amp_switch = float(np.sum(w8 * bp_l / bp_l) / np.sum(w8))
    pull_switch = (amp_switch - LA[0]) / LA[1]
    chi_switch = L2x["chi2_lcdm"]
P(f"    CMB lensing: the unbound linear web carries no phantom -> B(k, z) = 1 on every linear mode -> amplitude {amp_switch:.4f} relative "
  f"to the Planck best fit (Planck 2018 VIII: {LA[0]} +- {LA[1]}), pull {pull_switch:+.2f} sigma, chi^2 {chi_switch:.2f} over 9 bins")
cmb_ok = abs(amp_switch - LA[0]) <= 2 * LA[1]
# the leak (reported): the turned-around fraction of the linear web's phantom, added (XR26's amp_for_f with f -> f_ta(k, z))
GR_, GL_, ZL_, KHF_ = X["GROW"][HEAD], X["GL"], X["Z_L"], X["KHF"]


def f_ta_kz(kh, z):
    zz = min(ZS, key=lambda q: abs(q - z)) if z <= 3.0 else 3.0
    s = cl.sigma((1.0 / min(kh, 20.0)) / hF, z)
    return float(erfc(DTA[zz][1] / (math.sqrt(2) * s)))


FTA = np.array([[f_ta_kz(kh, z_) for kh in KHF_] for z_ in ZL_])


def amp_leak(base="lin", scale=1.0):
    Bz = np.array([((1 + scale * FTA[i] * GR_[round(z_, 6)][1]) * GR_[round(z_, 6)][0] / GL_[round(z_, 6)][0]) ** 2 for i, z_ in enumerate(ZL_)])
    ib = RectBivariateSpline(np.array(ZL_), np.log(KHF_), Bz, kx=1, ky=1)
    Rr = X["limber_pp"](base, lambda k_h, z_: np.where(z_ > ZL_[-1], 1.0, ib(np.minimum(z_, ZL_[-1]), np.log(np.clip(k_h, KHF_[0], KHF_[-1])),
                                                                              grid=False))) / X["LIMB_FID"][base]
    bp_c = X["bandpowers"](lambda ll: np.interp(ll, X["L_G"], Rr), "8-400")
    bp_l = X["bandpowers"](lambda ll: np.ones_like(ll, float), "8-400")
    w = 1 / np.array([b_[3] for b_ in X["PL18_MV"]["8-400"]]) ** 2
    return float(np.sum(w * bp_c / bp_l) / np.sum(w))


LEAK = {b: amp_leak(b) for b in ("lin", "NL")}
P(f"    the leak (reported; the law's phantom in the web's turned-around sub-regions ADDED, XR26's conservative 'growth held' form): "
  f"f_ta at z = 0.25: k = 0.1/0.3/1 h/Mpc -> {f_ta_kz(0.1, 0.25):.3f}/{f_ta_kz(0.3, 0.25):.3f}/{f_ta_kz(1.0, 0.25):.3f}; amplitude "
  f"{LEAK['lin']:.4f} (linear base, pull {(LEAK['lin'] - LA[0]) / LA[1]:+.2f}) / {LEAK['NL']:.4f} (halofit, pull {(LEAK['NL'] - LA[0]) / LA[1]:+.2f})")
check("H6 (reported; an estimate) THE LEAK: if the phantom of the web's bound sub-regions ADDS to the cold component there, Planck's "
      "8-400 amplitude moves by the printed amount (XR26's own conservative 'growth held at f = 1' form, f -> f_ta(k, z))",
      f"linear base {LEAK['lin']:.4f} (pull {(LEAK['lin'] - LA[0]) / LA[1]:+.2f}), halofit {LEAK['NL']:.4f} (pull {(LEAK['NL'] - LA[0]) / LA[1]:+.2f})",
      abs(LEAK["lin"] - LA[0]) <= 2 * LA[1], load_bearing=False,
      reading="whether the bound regions' phantom may ADD to the cold component or must REPLACE it is the bookkeeping question of "
              "part 5; replacing it leaves the lensing mass of every halo LCDM's (the switch then costs nothing on CMB lensing)")
# the forest: the unbound IGM carries no phantom
if C.MUTATE:
    forest_dev = float("nan")
    P("    [MUTATE] the forest is not re-scored without the switch here (FP9 I4 / FP6 B4: the law acting in the IGM fails the proxy)")
else:
    forest_dev = 0.0
P(f"    the forest: the unbound IGM carries no phantom -> the linear forest proxy (FP6's definition) deviates by {forest_dev} from LCDM; "
  f"the PS turned-around fraction at the Jeans scale (k = 10-20 h/Mpc, z = 2-3) is {min(r_['f_ta'] for r_ in igm if r_['k'] >= 10):.2f}-"
  f"{max(r_['f_ta'] for r_ in igm if r_['k'] >= 10):.2f} of the mass (the saturated, masked or halo-bound absorbers)")
forest_ok = (forest_dev == 0.0)
# KiDS at each lens's own turnaround radius
kids_ta = {(f, k): BOUNDS[(f, k, "turnaround", 0.0)] for f in C.FOOTS for k in ("P2", "nu_mono")}
kids_ok = all(v <= KIDS_TOL for v in kids_ta.values())
P("    KiDS with the phantom truncated at each lens's own turnaround radius (no 2-halo): " +
  ", ".join(f"{k[0][:3]}/{k[1]} {v:+.2f}" for k, v in kids_ta.items()))
# the flagship
disc_ok = all(r_["Denc"] >= delta_vir_mean(2.5) for r_ in disc)
P(f"    the z = 2.5 discs: r_F = {min(r_['rF_kpc'] for r_ in disc):.1f}-{max(r_['rF_kpc'] for r_ in disc):.1f} kpc lies inside the virialised "
  f"body (enclosed overdensity >= {min(r_['Denc'] for r_ in disc):.1e} > Delta_vir) -> ON; the law's zero-point shift at the flagship: 0 dex")
ss_ok = ss6
P(f"    the Solar System: a system-mass threshold M_* in (1, {MSTAR_WIN['canonical'][1]:.2e}] Msun (canonical) turns the Sun's own "
  "phantom off (FP17: a mass, or the equivalent length xi ~ sqrt(G M_*/a0), is the ONLY local discriminant; FP17's heat-filter "
  f"window read as a0 xi^2/G starts at {MSTAR_WIN['canonical'][0]:.2f} Msun because a smooth filter at 0.6 r_M(Sun) already suffices)")
h4 = cmb_ok and forest_ok and kids_ok and disc_ok and ss_ok
check("H4 [HEADLINE] THE SURVIVING SWITCH 'bound (Delta >= Delta_ta(z)) AND M >= M_*' passes every region: CMB lensing (Planck 8-400 "
      "within 2 sigma), the forest (proxy deviation 0), KiDS (d chi^2 <= +9 with the phantom cut at each lens's own turnaround radius), "
      "the z = 2.5 discs (ON) and the Solar System (M_* window non-empty)",
      f"CMB amplitude {amp_switch:.4f} (pull {pull_switch:+.2f}); forest {forest_dev}; KiDS " +
      "/".join(f"{v:+.1f}" for v in kids_ta.values()) + f"; discs {disc_ok}; M_* window {MSTAR_WIN['canonical'][0]:.2f}-{MSTAR_WIN['canonical'][1]:.1e}",
      h4)
R.num("H4", dict(cmb_amp=amp_switch, cmb_pull=pull_switch, cmb_chi2=chi_switch, leak=LEAK, forest_dev=forest_dev,
                 kids_turnaround={f"{k[0]}|{k[1]}": v for k, v in kids_ta.items()}, discs_on=disc_ok, Mstar_window=MSTAR_WIN,
                 no_switch_amp=dict(lin=lin_now["amp"], NL=nl_now["amp"], pull_lin=lin_now["pull"])))

# ================================================================================================ W ledger
banner("W  THE LEDGER: part 2 (the switch)")
R.ledger("S1", "CONSTRAINT", f"KiDS reach: phantom to r_t >= {FLOOR[('canonical', 'P2', 0.0)]:.2f} / {FLOOR[('alt', 'P2', 0.0)]:.2f} Mpc "
         f"(no 2-halo), >= {FLOOR[('canonical', 'P2', 2.0)]:.2f} / {FLOOR[('alt', 'P2', 2.0)]:.2f} Mpc (2-halo A <= 2)", "H2")
R.ledger("S2", "CONSTRAINT", f"CMB lensing: the unbound linear web carries no phantom (XR26: with it, {lin_now['amp']:.3f}, "
         f"{lin_now['pull']:+.1f} sigma)", "K1, H4")
R.ledger("S3", "CONSTRAINT", f"Solar System: the Sun's own phantom off; threshold mass M_* in [{MSTAR_WIN['canonical'][0]:.2f}, "
         f"{MSTAR_WIN['canonical'][1]:.2e}] / [{MSTAR_WIN['alt'][0]:.2f}, {MSTAR_WIN['alt'][1]:.2e}] Msun (FP17)", "K2")
R.ledger("S4", "DERIVED", "the switch: ON iff bound (enclosed overdensity >= the top-hat turnaround contrast Delta_ta(z), "
         f"{DTA[0.25][0]:.2f} at z = 0.25) AND M >= M_*; y, length, mass and local density alone fail", "H3, H4")
R.ledger("S5", "OPEN", f"bookkeeping of the bound regions' phantom vs the cold component: added -> CMB lensing leak {LEAK['lin']:.3f} "
         f"(lin) / {LEAK['NL']:.3f} (halofit); replaced -> LCDM's lensing (part 5)", "H6")
check("W (reported) the ledger of part 2", f"{len(R.OUT['ledger'])} rows", True, load_bearing=False)
sys.exit(R.finish())
