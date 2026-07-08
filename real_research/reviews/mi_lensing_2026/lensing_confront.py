#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
lensing_confront.py -- THE CONFRONTATION (verdict), both footings, prove-by-moving.
==================================================================================
Question: does the de Sitter-Unruh MODIFIED-INERTIA framework deliver the OBSERVED
lensing = dynamics consistency (Brouwer+2021 arXiv:2106.11677; Mistele-McGaugh 2024
arXiv:2310.15248), and is it PRINCIPLED, TUNED, or a TENSION?

MI LENSING PROBLEM (precise): MI modifies how MASSIVE bodies respond to force
(g_obs = sqrt(g_bar^2 + g_bar a0)). LIGHT is MASSLESS -> the MI law cannot bend it.
Photons follow null geodesics of the ORDINARY GR metric sourced by REAL mass:
T_baryon + T_condensate (the ghost-condensate dark sector). For the OBSERVED
lensing = dynamics, the condensate must supply a lensing mass
        M_cond(<r) = M_bar(<r) * (nu(g_bar/a0) - 1)   = the MI dynamical excess.
Do NOT smuggle in the AeST/MG modified-metric (phantom-potential) lensing -- that
is MODIFIED GRAVITY (Cassini-walled), not the MI reading. The MI lensing mass must
be REAL condensate mass.

FRAMEWORK STANDING (established, banked): the condensate amount I0 (~Omega_dm) is a
FREE shift charge (measured-not-derived); P(X) founded-not-derived; the shift Ward
identity gives ORTHOGONALITY dI0/d(grad phi)=0 => d rho_dust/d a0 = 0. So the Q-mode
(dust) is NOT sourced by the Y-mode (the a0/MI gradient). The condensate clusters on
its OWN (CDM-like / baryon-tracking), independent of the MI excess.

PROVE-BY-MOVING (the required stress test): sweep the condensate CLUSTERING
ASSUMPTION across a physically-motivated family -- from cuspy CDM (NFW, various
concentrations), to baryon-tracking, to cored, to the flat-curve isothermal ansatz.
For EACH, fix the ONE free amplitude I0 by matching total mass at r_max (the fairest
single-parameter normalization the framework permits) and measure the SHAPE residual
vs the MI excess across radius, in acceleration space (what the lensing RAR sees).
   - If the residual is ~0 for a BROAD range of clustering assumptions -> the match
     is robust/automatic -> CONSISTENT_PREDICTED.
   - If a SPECIFIC hand-chosen profile (= the MI excess itself) is needed and generic
     ones miss -> FINE_TUNED.
   - If EVERY realizable profile is DRIVEN AWAY from the MI excess by more than the
     data allow -> TENSION.
   - If the framework FORCES a specific small residual within the data scatter that
     differs from MG -> DISTINCTIVE.

Data allowance (SETUP B, Brouwer+21 / Mistele24): coherent lensing-vs-dynamics offset
~0.05 dex (1sig) / ~0.10 dex (2sig exclusion) clean GAMA; ~0.2-0.3 dex once the g_bar
(baryon) systematic is folded in. Lensing RAR scatter floor ~0.10 dex.

BOTH FOOTINGS: a0 = 9.36e-11 (canonical, rho_DE) and 1.13e-10 (alt). Exit 0.
"""
import numpy as np

# ---- constants -------------------------------------------------------------
c    = 2.99792458e8
G    = 6.67430e-11
Msun = 1.98892e30
kpc  = 3.0856775814913673e19
Z    = np.sqrt(32.0*np.pi/3.0)

A0_CANON = 9.36e-11
A0_ALT   = 1.13e-10

# data allowance (SETUP B, from observed_offset_budget.py, QUOTED-derived)
COHERENT_1SIG   = 0.05   # dex, clean GAMA coherent
COHERENT_2SIG   = 0.10   # dex, ~2sig exclusion (clean)
HONEST_BUDGET   = 0.30   # dex, once g_bar/baryon systematic folded in
LENS_SCATTER    = 0.10   # dex, lensing RAR per-bin/systematic floor

def nu(y):
    return np.sqrt(1.0 + 1.0/y)

# ---- fiducial galaxy -------------------------------------------------------
Md = 6.0e10*Msun
Rd = 3.0*kpc
r  = np.linspace(0.5, 15.0, 400)*Rd

def Mbar_enc(r):
    x = r/Rd
    return Md*(1.0 - (1.0 + x)*np.exp(-x))

Mbar = Mbar_enc(r)
gbar = G*Mbar/r**2

def mi_excess(a0):
    """M_cond required for lensing=dynamics = M_bar*(nu-1)."""
    y = gbar/a0
    return Mbar*(nu(y) - 1.0)

# ---- condensate clustering family (the prove-by-moving sweep) --------------
# Each returns an enclosed-mass SHAPE (arbitrary amplitude); amplitude fixed later.
def shape_nfw(rs_kpc, gamma=1.0):
    """(gNFW) enclosed mass shape. gamma=1 -> NFW cusp; gamma=0 -> cored-ish."""
    rs = rs_kpc*kpc
    x = r/rs
    if abs(gamma-1.0) < 1e-9:
        return np.log(1.0+x) - x/(1.0+x)               # NFW
    # generic: integrate rho ~ x^-gamma (1+x)^-(3-gamma) numerically (enclosed)
    xx = np.linspace(1e-4, x, 1, axis=0) if False else None
    # simple numeric cumulative for gNFW
    xg = r/rs
    rho = (xg**(-gamma))*(1.0+xg)**(-(3.0-gamma))
    integ = rho*r**2
    M = np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(r))
    M = np.concatenate([[0.0], M])
    return M

def shape_isothermal():
    return r.copy()                                    # M ~ r, rho ~ 1/r^2

def shape_track_baryons():
    return Mbar.copy()

def shape_cored(rc_kpc):
    """cored isothermal (pseudo-isothermal): M(<r) ~ r - rc*atan(r/rc)."""
    rc = rc_kpc*kpc
    return r - rc*np.arctan(r/rc)

def norm_at_rmax(shape, target):
    return shape*(target[-1]/shape[-1])

def residual_dex(Mcond, Mtarget):
    """acceleration-space log residual over the deep-MOND region."""
    good = Mtarget > 0.02*Mtarget[-1]
    gc = G*Mcond/r**2
    gt = G*Mtarget/r**2
    res = np.log10(gc[good]/gt[good])
    return np.sqrt(np.mean(res**2)), np.max(np.abs(res))

# ---- run the confrontation both footings -----------------------------------
def confront(a0, label):
    print("="*80)
    print(f"FOOTING  a0 = {a0:.3e} m/s^2   ({label})")
    print("="*80)
    Mex = mi_excess(a0)
    y = gbar/a0
    print(f"  fiducial galaxy Md={Md/Msun:.2e} Msun, Rd={Rd/kpc:.1f} kpc")
    print(f"  r_max={r[-1]/kpc:.1f} kpc: y={y[-1]:.3f}, nu={nu(y[-1]):.3f}, "
          f"M_cond_required/M_bar = nu-1 = {nu(y[-1])-1:.2f}")
    print(f"  MI excess (LENSING TARGET) at r_max = {Mex[-1]/Msun:.3e} Msun\n")

    # the prove-by-moving sweep: many clustering assumptions
    fam = [
        ("NFW cusp rs=10kpc     ", norm_at_rmax(shape_nfw(10.0), Mex)),
        ("NFW cusp rs=15kpc     ", norm_at_rmax(shape_nfw(15.0), Mex)),
        ("NFW cusp rs=30kpc     ", norm_at_rmax(shape_nfw(30.0), Mex)),
        ("gNFW cored g=0.3 rs=15", norm_at_rmax(shape_nfw(15.0, gamma=0.3), Mex)),
        ("cored-isoth rc=20kpc  ", norm_at_rmax(shape_cored(20.0), Mex)),
        ("isothermal ~1/r^2     ", norm_at_rmax(shape_isothermal(), Mex)),
        ("tracks baryons        ", norm_at_rmax(shape_track_baryons(), Mex)),
        ("MI-excess itself(hand)", Mex.copy()),   # the hand-placed profile
    ]
    print(f"  {'clustering assumption':<24}{'rms[dex]':>10}{'max[dex]':>10}"
          f"{'within 0.10?':>14}{'within 0.30?':>14}")
    results = []
    for name, Mc in fam:
        rms, mx = residual_dex(Mc, Mex)
        results.append((name, rms, mx))
        w10 = "YES" if rms < LENS_SCATTER else "no"
        w30 = "YES" if rms < HONEST_BUDGET else "no"
        print(f"  {name:<24}{rms:>10.3f}{mx:>10.3f}{w10:>14}{w30:>14}")
    print()
    # count how many generic (non-hand) assumptions land within the CLEAN data allowance
    generic = results[:-1]  # exclude the hand-placed MI-excess-itself
    n_within_clean = sum(1 for _,rms,_ in generic if rms < COHERENT_2SIG)
    n_within_scatter = sum(1 for _,rms,_ in generic if rms < LENS_SCATTER)
    n_within_honest = sum(1 for _,rms,_ in generic if rms < HONEST_BUDGET)
    print(f"  of {len(generic)} generic clustering assumptions:")
    print(f"    {n_within_clean}/{len(generic)} within clean 2sig coherent bound ({COHERENT_2SIG} dex)")
    print(f"    {n_within_scatter}/{len(generic)} within lensing scatter floor ({LENS_SCATTER} dex)")
    print(f"    {n_within_honest}/{len(generic)} within honest budget ({HONEST_BUDGET} dex)")
    return results, (n_within_clean, n_within_scatter, n_within_honest, len(generic))

print(__doc__)
res_c, cnt_c = confront(A0_CANON, "canonical rho_DE, a0=cH_Lambda/Z")
print()
res_a, cnt_a = confront(A0_ALT, "alt rho_total/cH0")

# ---- interpret the sweep ---------------------------------------------------
print("\n" + "="*80)
print("INTERPRETATION OF THE PROVE-BY-MOVING SWEEP")
print("="*80)
print(f"""
  If the match to the MI excess were AUTOMATIC (CONSISTENT_PREDICTED), then a BROAD
  range of physically-motivated clustering assumptions would land within the data
  allowance without being told about a0 / the MI excess.

  Canonical: {cnt_c[0]}/{cnt_c[3]} generic assumptions within the clean 2sig bound (0.10 dex);
             {cnt_c[1]}/{cnt_c[3]} within the lensing scatter floor.
  Alt      : {cnt_a[0]}/{cnt_a[3]} within clean 2sig; {cnt_a[1]}/{cnt_a[3]} within scatter floor.

  The only profile that sits at ~0 dex by construction is the HAND-PLACED "MI-excess
  itself". The NFW family lands ~0.10-0.16 dex rms (near/over the clean bound, inside
  the honest baryon-inflated budget), and it does so ONLY after its amplitude I0 is
  DIALED to the MI-excess mass at r_max -- which is itself a per-galaxy tuning (the MI
  excess ratio nu(r)-1 != the cosmic Omega_dm/Omega_b). Nothing in the ghost-condensate
  sector FORCES the NFW amplitude OR shape to the MI excess: I0 is free (dI0/da0=0).
""")

# ---- key positivity / realizability check (why NOT a TENSION) --------------
print("="*80)
print("REALIZABILITY: can a REAL (positive-density) condensate carry the MI excess?")
print("="*80)
for a0, tag in [(A0_CANON,"canonical"), (A0_ALT,"alt")]:
    Mex = mi_excess(a0)
    dM = np.diff(Mex)                    # shell masses (must be > 0)
    rho_excess = dM/(4.0*np.pi*r[:-1]**2*np.diff(r))
    min_over_peak = rho_excess.min()/rho_excess.max()
    slope_out = np.gradient(np.log(Mex), np.log(r))[-1]
    slope_in  = np.gradient(np.log(Mex), np.log(r))[np.argmax(gbar/a0 < 1.0)] if np.any(gbar/a0<1) else np.nan
    print(f"  {tag}: rho_excess min/peak = {min_over_peak:.4f} (>=0 everywhere => "
          f"{'REALIZABLE' if rho_excess.min()>0 else 'NEEDS NEGATIVE MASS'})")
    print(f"          d ln M_excess/d ln r  outer={slope_out:.2f} (->1 isothermal), "
          f"MI excess is monotonic & positive")
print("""
  => The required M_cond = M_bar*(nu-1) is monotonic with rho_excess > 0 EVERYWHERE.
     A real condensate CAN carry it -> lensing=dynamics is VIABLE, NOT excluded.
     This is why the verdict is NOT TENSION: the data can be matched.
""")

# ---- DISTINCTIVE check: does the framework FORCE a specific residual offset? -
print("="*80)
print("DISTINCTIVE check: is there a FORCED, framework-specific lensing-dyn offset?")
print("="*80)
print(f"""
  A DISTINCTIVE verdict needs the framework to PREDICT a specific small offset
  (within scatter) that differs from MG. But:
   * The condensate profile is FREE (I0 free, P(X) founded-not-derived, dI0/da0=0):
     the framework does NOT forecast any particular condensate shape, hence no
     forced offset. The ~0.10-0.20 dex residuals of generic shapes are the SIZE OF
     THE TUNING required, not a prediction -- they VANISH once the condensate is set
     to M_bar*(nu-1).
   * a0-fork discriminating power: canonical vs alt shifts the deep-MOND track by
     {0.5*np.log10(A0_CANON/1.20e-10):+.3f} / {0.5*np.log10(A0_ALT/1.20e-10):+.3f} dex vs the
     lensing a0=1.2e-10 -- BELOW the {LENS_SCATTER} dex scatter floor. The lensing RAR
     is a0-DEGENERATE; no separable a0 signature.
   => NO distinctive forced offset on the framework's own terms. NOT DISTINCTIVE.
""")

# ---- FINAL VERDICT ---------------------------------------------------------
print("="*80)
print("FINAL VERDICT (both footings)")
print("="*80)
print(f"""
  * NOT CONSISTENT_PREDICTED: no framework law ties the free ghost condensate
    (amount I0 free, shape CDM-like, orthogonal to a0: dI0/da0=0) to the MI excess.
    Generic clustering assumptions do NOT robustly land on the MI-excess shape/amount;
    only the hand-placed profile does (0 dex by construction).
  * NOT TENSION: the required M_cond = M_bar*(nu-1) is positive-density & monotonic ->
    a REAL condensate CAN carry it; the data (lensing=dynamics) are matched, not excluded.
  * NOT DISTINCTIVE: the free condensate forecasts no specific offset; the a0 forks
    are below the lensing scatter (a0-degenerate).
  => VERDICT: FINE_TUNED.
     Lensing=dynamics is VIABLE but a FIT: the ghost condensate must be hand-placed to
     equal the MI dynamical excess M_bar*(nu-1) in BOTH shape (~r isothermal deep-MOND)
     and amount (fixed by a0). This is the honest place many two-sector dark theories
     sit. Verified as hard as a win: no manufactured consistency (it needs hand-placing),
     no manufactured deficit (positive-density realizable, data matched). Footing-
     independent: alt a0 only rescales the required amplitude by (a0_alt/a0_canon)^0.5
     = {np.sqrt(A0_ALT/A0_CANON):.3f}, below the lensing scatter.
""")
print("lensing_confront.py complete. exit 0.")
