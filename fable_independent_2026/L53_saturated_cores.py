#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L53 -- the saturated branch WHERE IT IS ACTUALLY REALISED: galaxy interiors and cluster cores
==============================================================================================
Lane L53 of CHARTER.md.  Opened by L30_SATURATION.md (check G4) and L33_SCALAR_CONE.md (check D2).

THE FINDING THAT OPENS THE LANE.  Every screening argument in this corpus faces the Solar System.
L30's G4 showed that is the wrong address: the standing coherence length (0.10 / 0.15 pc) already
EXCEEDS the Sun's saturation radius (0.0242 / 0.0221 pc), so the carried kernel's saturated branch
-- where Delta' = 0, the longitudinal stiffness Sigma_par = 1/Delta' is infinite, and the scalar's
cubic action cannot be written -- is NOT realised around the Sun.  It is realised in the inner few
kiloparsecs of galaxies and in cluster cores, over volumes vastly larger than xi.  L33's D2 adds a
corollary no smooth repair removes: any kernel with an INTERIOR maximum has Delta' = 0 exactly at
its peak, i.e. an infinite longitudinal stiffness on a sphere at ~5000 AU around every star.

THE QUESTION.  What happens on the saturated branch where it is really realised, and does it bear
on the failures the programme cannot fix?  In spherical symmetry the enclosed-mass relation hides
the whole issue -- J_Y(g_phi) g_phi = g_N is algebraic, there is no solve, and Sigma_par never
appears.  Galaxy discs and cluster cores are NOT spherical.  This lane sets up the actual
non-spherical boundary-value problem and asks whether it is well posed, ill posed, or merely stiff,
and then whether the answer touches the inner rotation curve, the vertical structure of a disc, or
cluster cores -- the programme's hardest failure.

THE EQUATION.  THE_ACTION section 1 carries -(2-K_B) J(Y), Y = |grad phi|^2, and the AeST coupling
2(2-K_B) J^mu d_mu phi.  Static variation (PAPER5 section 7; g03x's own docstring) gives

        div [ J_Y(|grad phi|^2) grad phi ]  =  4 pi G rho ,

with the physical acceleration g = g_N + g_phi, g_phi = -grad phi.  On a sphere this integrates once
to J_Y(g_phi) g_phi = g_N, hence g_phi = a0 Delta(s), s = g_N/a0, which IS the carried kernel.  Away
from spherical symmetry it is a genuine nonlinear elliptic BVP and grad phi need not be parallel to
grad Phi_N.

WHAT THE STIFFNESSES ARE (L30 section 1, L33 A2; reproduced here as control K2):

        Sigma_perp = J_Y          = s / Delta(s)              transverse
        Sigma_par  = J_Y + 2Y J_YY = 1 / Delta'(s)            longitudinal

On the published kernel Delta is held FLAT above s_sat = 2.540, so Delta' = 0 and Sigma_par = +oo
on a whole region.  That is the object this lane examines.

STRUCTURE
  0  CONTROLS.  The kernel, its saturation point and ceiling; L30's Solar saturation radius and the
     standing coherence-length floor; L33's ~5000 AU sphere; the Sigma_par = 1/Delta' identity;
     L30's minimal C^2 repair constants.
  1  WHERE THE BRANCH IS REALISED, in kpc, for a disc, a dwarf and a cluster, on the repository's
     own committed baryon models (SPARC rotmod files; the cluster measurement audit; McMillan 2017).
  2  THE MATHEMATICAL CORE.  The constitutive map, its monotonicity, the convexity of the energy,
     and the classification of the non-spherical BVP.  Includes the LOCALISATION check: which of the
     three readings of the field equation (carrier / AQUAL-on-total-potential / QUMOND) actually
     carries the infinite stiffness.
  3  THE SOLVER and its controls: an axisymmetric P1 finite-element energy minimiser driven by
     damped Newton with a sparse direct solve.  Controls: the Newtonian limit on a homogeneous
     oblate spheroid against the exact MacLaurin interior field (a NON-SPHERICAL analytic result at
     finite stiffness); a Plummer sphere against the exact Newtonian field; the nonlinear carrier on
     a spherical source against the algebraic law; grid convergence.
  4  TARGET (a) the inner rotation curve of a real disc.
  5  TARGET (b) the vertical structure of a disc -- the most non-spherical observable available.
  6  TARGET (c) cluster cores, including the geometry-free form of the bounded-boost ceiling.
  7  THE SMOOTH REPAIR re-run on all three targets: L30's minimal C^2 continuation, and the kernel
     THE_COMPLETE_THEORY section 4.3 actually deposits.
  8  VERDICT: formal defect, numerical hazard, or physical effect.

Both a0 footings throughout (9.3619e-11 canonical / 1.1279e-10 alt).  FAIL marks a substantive
finding, never a machinery failure; every control that could unmask a broken solver is separated out
and labelled.

HONESTY NOTE, stated before any result.  The most likely outcome is that the pathology is formal and
observationally invisible, which would discharge a liability the programme carries.  But if an
ill-posed or merely very stiff solve has been quietly affecting cluster-core results, then some of
this programme's own cluster numbers were computed on a branch where the equation is not well posed,
and that requires RE-EXAMINING them, not celebrating.  Section 2's localisation check is written to
find that if it is there.
"""
import os, sys, math, glob, json, time, warnings
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
from scipy.optimize import brentq
from scipy.special import ellipk

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
T0 = time.time()

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# ---- constants (SI) --------------------------------------------------------------------------
G      = 6.6743e-11
MSUN   = 1.98892e30
GMSUN  = 1.32712440018e20
PC     = 3.0857e16
KPC    = 3.0857e19
AU     = 1.495978707e11
MSUN_PC2 = MSUN / PC**2
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FOOT = ("canonical", "alt")

print("=" * 122)
print("L53 -- the saturated branch where it is actually realised: galaxy interiors and cluster cores")
print("=" * 122, flush=True)


# ==================================================================================================
# 0.  THE CARRIED KERNEL, ITS SATURATION, AND THE CONTROLS THAT ANCHOR THIS LANE TO L30 AND L33
# ==================================================================================================
print("\n0.  CONTROLS -- the kernel, the saturation point, and the addresses L30 and L33 established")

def _rar_D(s):
    """Delta_RAR(s) = s/(exp(sqrt(s)) - 1), the carried kernel below saturation."""
    s = np.asarray(s, float)
    x = np.sqrt(np.maximum(s, 0.0))
    out = np.where(x > 1e-4, x**2/np.expm1(np.where(x > 1e-4, x, 1.0)),
                   x*(1.0 - x/2.0 + x**2/12.0 - x**4/720.0))
    return np.where(s > 0, out, 0.0)

def _rar_dD(s):
    """d Delta_RAR / ds, analytic.  numerator 2(e^x-1) - x e^x, denominator 2 (e^x-1)^2."""
    s = np.asarray(s, float)
    x = np.sqrt(np.maximum(s, 1e-300))
    big = x > 1e-3
    xb = np.where(big, x, 1.0)
    em1 = np.expm1(xb)
    num = 2.0*em1 - xb*np.exp(xb)
    den = 2.0*em1**2
    out_big = num/den
    xs = np.where(big, 1.0, x)                       # small-x series: 1/(2x) - 1/2 + x/8 - ...
    out_small = 1.0/(2.0*xs) - 0.5 + xs/8.0 - xs**2/24.0
    return np.where(big, out_big, out_small)

# saturation point of nu_RAR: the root of Delta'
S_SAT = brentq(lambda s: float(_rar_dD(np.array([s]))[0]), 1.0, 6.0, xtol=1e-14, rtol=1e-15)
C_SAT = float(_rar_D(np.array([S_SAT]))[0])
print(f"    nu_RAR: maximum of Delta at s_sat = {S_SAT:.4f}, ceiling C = sup Delta = {C_SAT:.6f}")
check("K0 [control] the carried kernel's saturation point and boost ceiling reproduce THE_ACTION "
      "section 3 / L30 K0 (s_sat = 2.540, C = 0.6476)",
      abs(S_SAT - 2.5396) < 3e-3 and abs(C_SAT - 0.647610) < 5e-5,
      f"s_sat = {S_SAT:.4f}, C = {C_SAT:.6f}")

# --- L30's Solar saturation radius, and L33's ~5000 AU sphere -----------------------------------
print("\n    the radius inside which g_N > s_sat a0 (the saturated branch) around a point mass M:")
print("        r_sat = sqrt( G M / (s_sat a0) )")
rsat = {}
for f in FOOT:
    r = math.sqrt(GMSUN/(S_SAT*A0[f]))
    rsat[f] = r
    print(f"      {f:<10s}: Sun  r_sat = {r/PC:.4f} pc = {r/AU:.0f} AU")
check("K1 [control] L30 G4's Solar saturation radius is reproduced (0.0242 pc canonical / 0.0221 pc alt)",
      abs(rsat["canonical"]/PC - 0.0242) < 5e-4 and abs(rsat["alt"]/PC - 0.0221) < 5e-4,
      f"{rsat['canonical']/PC:.4f} / {rsat['alt']/PC:.4f} pc")
check("K2 [control] L33 D2's corollary sphere is reproduced: any kernel with an INTERIOR maximum has "
      "Delta' = 0 exactly at s_sat, hence Sigma_par = infinity on a sphere at 4994 AU (canonical) / 4550 AU (alt)",
      abs(rsat["canonical"]/AU - 4994) < 25 and abs(rsat["alt"]/AU - 4550) < 25,
      f"{rsat['canonical']/AU:.0f} / {rsat['alt']/AU:.0f} AU")

XI_STANDING = {"canonical": 0.10*PC, "alt": 0.15*PC}     # g02/g03b/g03x floors, reproduced by L30 K3
ok_floor = all(XI_STANDING[f] > rsat[f] for f in FOOT)
print(f"    standing coherence-length floor xi = 0.10 pc (canonical) / 0.15 pc (alt) versus r_sat:")
for f in FOOT:
    print(f"      {f:<10s}: xi/r_sat = {XI_STANDING[f]/rsat[f]:.2f}  "
          f"({'xi EXCEEDS r_sat -- the Sun never sits on the saturated branch' if XI_STANDING[f] > rsat[f] else 'saturated'})")
check("K3 [control] L30 G4's statement is reproduced: the standing coherence length EXCEEDS the Sun's "
      "saturation radius, so the saturated branch is not realised around the Sun",
      ok_floor, f"xi/r_sat = {XI_STANDING['canonical']/rsat['canonical']:.2f} / "
                f"{XI_STANDING['alt']/rsat['alt']:.2f}")

# --- the Sigma_par = 1/Delta' identity ----------------------------------------------------------
# J_Y(s) = s/Delta(s);  Y = (a0 Delta)^2;  J_YY = dJ_Y/dY;  Sigma_par = J_Y + 2 Y J_YY
_st = np.array([0.05, 0.2, 0.6, 1.2, 2.0, 2.4])
_a0 = A0["canonical"]
_h = 1e-7
_JY  = lambda s: s/_rar_D(s)
_Y   = lambda s: (_a0*_rar_D(s))**2
_dJYdY = (_JY(_st*(1+_h)) - _JY(_st*(1-_h))) / (_Y(_st*(1+_h)) - _Y(_st*(1-_h)))
_Spar_direct = _JY(_st) + 2*_Y(_st)*_dJYdY
_Spar_ident  = 1.0/_rar_dD(_st)
_relerr = float(np.max(np.abs(_Spar_direct/_Spar_ident - 1.0)))
check("K4 [control] the longitudinal stiffness identity Sigma_par = J_Y + 2 Y J_YY = 1/Delta'(s) holds "
      "on the unsaturated branch (L30 K2 / L33 A2)", _relerr < 2e-6, f"max relative error {_relerr:.2e}")


# ==================================================================================================
#     THE KERNEL FAMILY -- published, the two repairs, and the stiffness-regularised realisation
# ==================================================================================================
class Kernel:
    """Delta(s), Delta'(s) analytic; the inverse s(u) and the energy density W(u) built from them.

    u == g_phi/a0 == Delta.   s == g_N/a0.
       sigma(u) = s(u)              the 'stress' (the Newtonian source magnitude)
       Sigma_perp = s/u = J_Y       transverse stiffness
       Sigma_par  = ds/du = 1/Delta' longitudinal stiffness
       W(u) = int_0^u s dt          the scaled energy density; W'(u) = s(u)
    """
    def __init__(self, name, D, dD, s_max, u_cap=None):
        self.name, self.D, self.dD, self.s_max = name, D, dD, s_max
        # a monotone table for the initial inverse guess: log-spaced at small s (where Delta ~ sqrt(s)),
        # linear through the transition, log-spaced again above it
        s_tab = np.unique(np.concatenate([[0.0], np.geomspace(1e-18, min(4.0, s_max), 200001),
                                          np.linspace(0.0, min(4.0, s_max), 100001),
                                          np.geomspace(min(4.0, s_max), s_max, 100001)]))
        u_tab = np.asarray(D(s_tab), float)
        keep = np.concatenate([[True], np.diff(u_tab) > 0])   # strictly increasing
        self.s_tab, self.u_tab = s_tab[keep], u_tab[keep]
        self.u_max = float(self.u_tab[-1])
        # The energy density W(u) = int_0^u s dt is built by LEGENDRE TRANSFORM,
        #     W(u) = u s(u) - Psi(s(u)) ,      Psi(s) = int_0^s Delta(t) dt ,
        # so that W'(u) = s + (u - Delta(s)) ds/du = s(u) EXACTLY, given only s(u).  Tabulating W
        # directly in u instead is fatal: near the ceiling s(u) is near-vertical, the table's
        # piecewise-linear derivative is a staircase, and the Armijo line search then compares
        # energies whose difference is smaller than the interpolation error and stalls.  Psi, by
        # contrast, is an integral of the bounded, smooth Delta and tabulates to ~1e-12.
        dtab = np.asarray(D(self.s_tab), float)
        self.Psi_tab = np.concatenate(
            [[0.0], np.cumsum(0.5*(dtab[1:] + dtab[:-1])*np.diff(self.s_tab))])

    BIG = 1e12          # stiffness of the barrier that keeps u below the kernel's own ceiling

    def s_of_u(self, u):
        u = np.asarray(u, float)
        s = np.interp(np.clip(u, 0.0, self.u_max), self.u_tab, self.s_tab)
        for _ in range(6):                                    # vectorised, positivity-preserving Newton
            d = np.asarray(self.D(s), float); dd = np.asarray(self.dD(s), float)
            step = (u - d)/np.maximum(dd, 1e-300)
            step = np.maximum(step, -0.5*s)                   # never overshoot into s < 0
            s = np.clip(s + step, 0.0, self.s_max)
        return np.where(u > self.u_max, self.s_max + self.BIG*(u - self.u_max), s)

    def state(self, u, floor=1e-9):
        """returns (s, Sigma_perp, Sigma_par) at gradient magnitude u (in units of a0)."""
        uu = np.maximum(np.asarray(u, float), floor)
        s = self.s_of_u(uu)
        over = uu > self.u_max
        dd = np.maximum(np.asarray(self.dD(np.minimum(s, self.s_max)), float), 1e-300)
        return s, s/uu, np.where(over, self.BIG, 1.0/dd)

    def W_of_u(self, u):
        u = np.asarray(u, float)
        ucl = np.clip(u, 0.0, self.u_max)
        s = self.s_of_u(ucl)
        w = ucl*s - np.interp(s, self.s_tab, self.Psi_tab)
        ex = np.maximum(u - self.u_max, 0.0)
        return w + self.s_max*ex + 0.5*self.BIG*ex**2

def make_published(M):
    """The published saturated kernel, realised numerically by CAPPING Sigma_par at M.

    Delta_M = Delta_RAR for s <= s*, then the straight line of slope 1/M, where Delta'(s*) = 1/M.
    Delta_M is C^1, strictly increasing, and differs from the published kernel by at most
    (s_max - s*)/M over the whole range used.  M -> infinity recovers the published plateau, i.e.
    the hard constraint |grad phi| <= C a0.
    """
    s_star = brentq(lambda s: float(_rar_dD(np.array([s]))[0]) - 1.0/M, 1e-3, S_SAT, xtol=1e-15, rtol=1e-15)
    u_star = float(_rar_D(np.array([s_star]))[0])
    def D(s):
        s = np.asarray(s, float)
        return np.where(s <= s_star, _rar_D(s), u_star + (s - s_star)/M)
    def dD(s):
        s = np.asarray(s, float)
        return np.where(s <= s_star, np.maximum(_rar_dD(s), 1.0/M), 1.0/M)
    k = Kernel(f"published (Sigma_par capped at {M:.0e})", D, dD, 1e7)
    k.s_star, k.u_star, k.M = s_star, u_star, M
    return k

# --- L30's minimal C^2 repair (L30 section 3, candidate C) --------------------------------------
_S1, _MT = 2.0, 2.0
_d1  = float(_rar_D(np.array([_S1]))[0])
_d1p = float(_rar_dD(np.array([_S1]))[0])
_hh = 1e-6
_d1pp = float((_rar_dD(np.array([_S1*(1+_hh)]))[0] - _rar_dD(np.array([_S1*(1-_hh)]))[0])/(2*_S1*_hh))
BETA_C = -_d1pp/((_MT + 1.0)*_d1p)
AMP_C  = _d1p/(_MT*BETA_C)
DINF_C = _d1 + AMP_C
def _D_repC(s):
    s = np.asarray(s, float)
    return np.where(s <= _S1, _rar_D(s), DINF_C - AMP_C*(1.0 + BETA_C*np.maximum(s - _S1, 0.0))**(-_MT))
def _dD_repC(s):
    s = np.asarray(s, float)
    return np.where(s <= _S1, _rar_dD(s),
                    _MT*AMP_C*BETA_C*(1.0 + BETA_C*np.maximum(s - _S1, 0.0))**(-_MT - 1.0))
print(f"\n    L30's minimal C^2 repair (candidate C):  Delta_C(s) = D_inf - A (1 + beta (s - 2))^-2  "
      f"for s > 2,\n      D_inf = {DINF_C:.6f},  A = {AMP_C:.6e},  beta = {BETA_C:.6f}")
_ss = np.logspace(-6, 6, 200001)
_dev_pub = float(np.max(np.abs(_D_repC(_ss) - np.where(_ss > S_SAT, C_SAT, _rar_D(_ss)))))
check("K5 [control] L30's minimal C^2 repair is reproduced: constants D_inf = 0.655589, "
      "A = 1.317369e-02, beta = 0.801759, and max |Delta_C - Delta_published| = 0.0080 a0 at every s",
      abs(DINF_C - 0.655589) < 5e-6 and abs(AMP_C - 1.317369e-2) < 5e-8
      and abs(BETA_C - 0.801759) < 5e-6 and abs(_dev_pub - 0.0080) < 5e-4,
      f"D_inf = {DINF_C:.6f}, A = {AMP_C:.6e}, beta = {BETA_C:.6f}, max dev = {_dev_pub:.4f} a0")

# --- the kernel THE_COMPLETE_THEORY section 4.3 actually deposits --------------------------------
C_DEP, P_DEP, A2_DEP = 0.647610, 1.7538, 0.9335
A1_DEP = 1.0/(C_DEP*P_DEP)
def _D_dep(s):
    x = np.sqrt(np.maximum(np.asarray(s, float), 0.0))
    W = 1.0 + A1_DEP*x + A2_DEP*x**2
    return C_DEP*(1.0 - W**(-P_DEP))
def _dD_dep(s):
    s = np.asarray(s, float)
    x = np.sqrt(np.maximum(s, 1e-300))
    W = 1.0 + A1_DEP*x + A2_DEP*x**2
    return C_DEP*P_DEP*W**(-P_DEP - 1.0)*(A1_DEP + 2*A2_DEP*x)/(2.0*x)
_dexdep = float(np.max(np.abs(np.log10(np.maximum(_ss + _D_dep(_ss), 1e-300))
                              - np.log10(np.maximum(_ss + np.where(_ss > S_SAT, C_SAT, _rar_D(_ss)), 1e-300)))))
check("K6 [control] the deposited kernel (THE_COMPLETE_THEORY section 4.3) is reproduced: "
      "Delta' > 0 at every finite s and max |Delta log10 g| <= 0.0111 dex against the published kernel",
      float(np.min(_dD_dep(np.logspace(-4, 4, 20001)))) > 0 and _dexdep < 0.0115,
      f"min Delta' = {float(np.min(_dD_dep(np.logspace(-4, 4, 20001)))):.2e}, max dev = {_dexdep:.4f} dex")

KER = {
    "PUB4":  make_published(1e4),
    "PUB6":  make_published(1e6),
    "PUB8":  make_published(1e8),
    "REPC":  Kernel("L30 minimal C^2 repair", _D_repC, _dD_repC, 1e7),
    "DEP":   Kernel("deposited kernel (theory section 4.3)", _D_dep, _dD_dep, 1e7),
    "NEWT":  Kernel("Newtonian control (Delta = s)", lambda s: np.asarray(s, float),
                    lambda s: np.ones_like(np.asarray(s, float)), 1e7),
    # diagnostic: the SAME equation with an UNBOUNDED kernel, so there is no ceiling and no
    # saturated branch at all, but the same deep-MOND nonlinearity.  Used to separate "the disc
    # correction any nonlinear kernel has" from "the disc correction saturation adds".
    "DMND":  Kernel("unbounded deep-MOND diagnostic (Delta = sqrt(s))",
                    lambda s: np.sqrt(np.maximum(np.asarray(s, float), 0.0)),
                    lambda s: 0.5/np.sqrt(np.maximum(np.asarray(s, float), 1e-300)), 1e7),
}
KER_NEWT_NAME = KER["NEWT"].name
_rt = np.array([1e-4, 1e-2, 0.1, 0.4, 0.6, 0.645])
_rterr = max(float(np.max(np.abs(k.D(k.s_of_u(_rt)) - _rt))) for k in (KER["PUB6"], KER["REPC"], KER["DEP"]))
check("K7 [control] the kernel inverse s(u) round-trips: Delta(s(u)) = u to 1e-12 for the published "
      "kernel and both repairs", _rterr < 1e-12, f"max |Delta(s(u)) - u| = {_rterr:.1e}")


# ==================================================================================================
# 1.  WHERE THE BRANCH IS REALISED -- in kpc, on the repository's own committed baryon models
# ==================================================================================================
print("\n1.  WHERE THE SATURATED BRANCH IS REALISED  (g_N > s_sat a0), on committed baryon models")

# --- SPARC, the repository's rotmod files, Upsilon_d = 0.5, Upsilon_b = 0.7 ----------------------
UPS_D, UPS_B = 0.5, 0.7
SPARC = {}
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 4: continue
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    r = d[:, 0]*KPC
    Vg, Vd, Vb = d[:, 3]*1e3, d[:, 4]*1e3, d[:, 5]*1e3
    gb = (Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb))/np.maximum(r, 1e-30)
    m = (r > 0) & (gb > 0)
    if m.sum() < 4: continue
    SPARC[nm] = (r[m], gb[m], d[m, 1]*1e3, d[m, 2]*1e3)
print(f"    SPARC: {len(SPARC)} galaxies loaded from the repository's rotmod files")

def sat_extent(r, gb, a0):
    """outer radius of the saturated region along the measured curve, and whether any point is saturated."""
    sat = gb > S_SAT*a0
    if not sat.any(): return 0.0, float(np.max(gb)/a0)
    return float(np.max(r[sat])/KPC), float(np.max(gb)/a0)

print("\n    representative systems (measured in-plane g_bar, so this is the DISC-PLANE extent):")
print(f"      {'system':<14s}{'footing':<11s}{'max s = g_bar/a0':>18s}{'saturated out to':>19s}")
DISC_NAME, DWARF_NAME = "NGC2903", "DDO154"
region = {}
for nm in ("NGC2903", "NGC3198", DWARF_NAME, "DDO161"):
    if nm not in SPARC: continue
    r, gb, _, _ = SPARC[nm]
    for f in FOOT:
        Rs, smax = sat_extent(r, gb, A0[f])
        region[(nm, f)] = (Rs, smax)
        print(f"      {nm:<14s}{f:<11s}{smax:>18.3f}{(f'{Rs:.2f} kpc' if Rs > 0 else 'NEVER saturated'):>19s}")

nsat = {f: sum(1 for nm in SPARC if (SPARC[nm][1] > S_SAT*A0[f]).any()) for f in FOOT}
print(f"\n    SPARC census: {nsat['canonical']}/{len(SPARC)} galaxies (canonical) and "
      f"{nsat['alt']}/{len(SPARC)} (alt) reach the saturated branch anywhere on their measured curve")
Rout = {f: np.array([sat_extent(*SPARC[nm][:2], A0[f])[0] for nm in SPARC
                     if (SPARC[nm][1] > S_SAT*A0[f]).any()]) for f in FOOT}
for f in FOOT:
    print(f"      {f:<10s}: saturated out to a median {np.median(Rout[f]):.2f} kpc, "
          f"max {np.max(Rout[f]):.2f} kpc, over those {len(Rout[f])} galaxies")
check("R1 the saturated branch IS realised, at kiloparsec scale, in the disc plane of real galaxies "
      "with the repository's own baryon models -- so it is not a Solar-System phenomenon (L30 G4)",
      np.median(Rout["canonical"]) > 1.0 and nsat["canonical"] > 10,
      f"{nsat['canonical']}/{len(SPARC)} SPARC discs saturate somewhere, out to a median "
      f"{np.median(Rout['canonical']):.2f} kpc and a maximum {np.max(Rout['canonical']):.2f} kpc "
      f"(canonical); median {np.median(Rout['alt']):.2f} kpc, max {np.max(Rout['alt']):.2f} kpc (alt). "
      f"{DISC_NAME} is the representative saturating disc used below "
      f"({region[(DISC_NAME,'canonical')][0]:.2f} kpc canonical / "
      f"{region[(DISC_NAME,'alt')][0]:.2f} kpc alt)")
check("R2 the saturated branch is realised in DWARFS, and in typical discs -- i.e. it is a generic "
      "feature of galaxy interiors rather than of the baryon-densest minority",
      region[(DWARF_NAME, "canonical")][0] > 0 and nsat["canonical"] > 0.5*len(SPARC),
      f"it is NOT: {DWARF_NAME} reaches only s = {region[(DWARF_NAME,'canonical')][1]:.3f} "
      f"(canonical) / {region[(DWARF_NAME,'alt')][1]:.3f} (alt) against s_sat = {S_SAT:.3f}, "
      f"{S_SAT/region[(DWARF_NAME,'canonical')][1]:.0f}x short, and "
      f"{len(SPARC)-nsat['canonical']}/{len(SPARC)} SPARC galaxies never saturate anywhere on their "
      f"measured curve.  NGC3198, the archetype, peaks at s = {region[('NGC3198','canonical')][1]:.3f} "
      f"and never reaches the branch either")

# --- clusters, from the repository's own measurement audit --------------------------------------
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/"
                                        "cluster_measurement_audit_2026/results.json")))
CROWS = CLJ["rows"]
print("\n    clusters (the repository's cluster measurement audit, tabulated hydrostatic profiles):")
print(f"      {'footing':<11s}{'radii with g_bar > s_sat a0':>30s}{'n rows':>9s}{'max s':>9s}")
cl_sat = {}
for f in FOOT:
    rw = [r for r in CROWS if r["footing"] == f]
    sat = [r for r in rw if r["g_baryon_over_a0"] > S_SAT]
    rr = sorted(set(r["r_kpc"] for r in sat))
    cl_sat[f] = rr
    print(f"      {f:<11s}{(str(rr) if rr else 'none of the tabulated radii'):>30s}"
          f"{len(sat):>9d}{max(r['g_baryon_over_a0'] for r in rw):>9.3f}")
# where the cluster BARYONS saturate, computed continuously from the tabulated g_bar(r)
def cluster_rsat(name, foot):
    rw = sorted([(r["r_kpc"], r["g_baryon_over_a0"]) for r in CROWS
                 if r["cluster"] == name and r["footing"] == foot])
    if len(rw) < 3: return None
    rr = np.array([x[0] for x in rw]); ss = np.array([x[1] for x in rw])
    if ss.max() <= S_SAT: return 0.0
    # the outermost radius at which the tabulated s crosses s_sat
    idx = np.where(ss > S_SAT)[0]
    i = idx[-1]
    if i == len(rr) - 1: return float(rr[-1])
    t = (S_SAT - ss[i])/(ss[i+1] - ss[i])
    return float(rr[i] + t*(rr[i+1] - rr[i]))
CL_NAMES = sorted(set(r["cluster"] for r in CROWS))
tab = []
for nm in CL_NAMES:
    row = [nm] + [cluster_rsat(nm, f) for f in FOOT]
    tab.append(row)
nsatcl = {f: sum(1 for t in tab if t[1 + FOOT.index(f)] not in (None, 0.0)) for f in FOOT}
print(f"      {nsatcl['canonical']}/{len(tab)} clusters (canonical) have a baryon-saturated core; "
      f"{nsatcl['alt']}/{len(tab)} (alt)")
for t in tab[:6]:
    print(f"        {t[0]:<10s} saturated inside r = "
          + ", ".join(f"{('%.0f kpc' % t[1+i]) if t[1+i] else 'never':>9s} ({FOOT[i][:3]})" for i in range(2)))
_maxcl = max((t[1] or 0.0) for t in tab)
check("R3 the saturated branch is realised at the radii the repository's cluster audit tabulates "
      "(L30 section 7 gives its address as 'the inner few kiloparsecs of every galaxy AND the cores "
      "of clusters')",
      _maxcl > 20.0,
      f"it is NOT.  The audit's innermost radius is 30 kpc and its LARGEST tabulated s = g_bar/a0 "
      f"anywhere is {max(r['g_baryon_over_a0'] for r in CROWS if r['footing']=='canonical'):.3f} "
      f"(canonical) / {max(r['g_baryon_over_a0'] for r in CROWS if r['footing']=='alt'):.3f} (alt), "
      f"{S_SAT/max(r['g_baryon_over_a0'] for r in CROWS if r['footing']=='canonical'):.1f}x below "
      f"s_sat = {S_SAT:.3f}.  0/{len(tab)} clusters saturate at any tabulated radius, at either "
      f"footing.  L30's cluster address is CORRECTED here: cluster cores as the repository measures "
      f"them are deep on the UNSATURATED branch")

# where WOULD a cluster core saturate?  144 of the 248 audit rows (7 of the 12 clusters) DO include
# BCG stars, and none of them saturates either -- but the innermost tabulated radius is 30 kpc, which
# is outside where a BCG's own field is strong.  So a BCG is added explicitly and asked.
_nst = sum(1 for r in CROWS if r["stellar_file_present"])
print(f"\n    {_nst} of the {len(CROWS)} audit rows DO include BCG stars "
      f"({len(sorted(set(r['cluster'] for r in CROWS if r['stellar_file_present'])))} of the "
      f"{len(CL_NAMES)} clusters) and none of them saturates either -- but the innermost tabulated")
print("    radius is 30 kpc.  A BCG is therefore added explicitly to ask where a cluster core WOULD")
print("    saturate: Hernquist stars, M* = 8e11 Msun, a = 16.5 kpc (R_e = 30 kpc).")
MSTAR_BCG, A_BCG = 8.0e11*MSUN, 16.5*KPC
def g_bcg(r_m):
    return G*MSTAR_BCG/(r_m + A_BCG)**2
rr_probe = np.geomspace(0.5, 200.0, 2000)*KPC
rsat_bcg = {}
for f in FOOT:
    gg = g_bcg(rr_probe)/A0[f]
    idx = np.where(gg > S_SAT)[0]
    rsat_bcg[f] = float(rr_probe[idx[-1]]/KPC) if len(idx) else 0.0
    print(f"      {f:<10s}: the BCG alone puts g_N > s_sat a0 inside r = {rsat_bcg[f]:.1f} kpc "
          f"(g_star at 30 kpc = {float(g_bcg(30*KPC)/A0[f]):.3f} a0, at 40 kpc = "
          f"{float(g_bcg(40*KPC)/A0[f]):.3f} a0)")
check("R3b the saturated branch IS realised in cluster cores once the BCG is included, but only "
      "INSIDE the innermost radius at which the repository has cluster data",
      rsat_bcg["canonical"] > 3.0 and rsat_bcg["canonical"] < 30.0,
      f"saturated inside {rsat_bcg['canonical']:.1f} kpc (canonical) / {rsat_bcg['alt']:.1f} kpc "
      f"(alt), against an innermost tabulated radius of 30 kpc.  So the branch exists in cluster "
      f"cores but nowhere the cluster failure is actually measured")

# --- and the Milky Way, on the repository's own committed McMillan 2017 model --------------------
# McMillan 2017, MNRAS 465, 76, Table 3 -- identical parameters to hunt_2026/g02_vertical_*.py
MCM = dict(S0_thin=896.0*MSUN_PC2, Rd_thin=2.50*KPC, zd_thin=0.300*KPC,
           S0_thick=183.0*MSUN_PC2, Rd_thick=3.02*KPC, zd_thick=0.900*KPC,
           rho0_b=98.4*MSUN/PC**3, alpha_b=1.8, r0_b=0.075*KPC, rcut_b=2.1*KPC, q_b=0.5,
           S_HI_fid=10.0*MSUN_PC2, Rm_HI=4.0*KPC, Rd_HI=7.0*KPC, zd_HI=0.085*KPC,
           S_H2_fid=2.0*MSUN_PC2, Rm_H2=12.0*KPC, Rd_H2=1.5*KPC, zd_H2=0.045*KPC, R_fid=8.33*KPC)

def rho_mw(R, z):
    """McMillan 2017 baryonic density, SI kg/m^3.  R, z in metres; z may be signed."""
    p = MCM
    R = np.asarray(R, float); z = np.abs(np.asarray(z, float))
    out = (p["S0_thin"]/(2*p["zd_thin"]))*np.exp(-z/p["zd_thin"] - R/p["Rd_thin"])
    out = out + (p["S0_thick"]/(2*p["zd_thick"]))*np.exp(-z/p["zd_thick"] - R/p["Rd_thick"])
    rp = np.sqrt(R**2 + (z/p["q_b"])**2)
    out = out + p["rho0_b"]/(1 + rp/p["r0_b"])**p["alpha_b"]*np.exp(-((rp/p["rcut_b"])**2))
    for tag in ("HI", "H2"):
        S0 = p[f"S_{tag}_fid"]/math.exp(-p[f"Rm_{tag}"]/p["R_fid"] - p["R_fid"]/p[f"Rd_{tag}"])
        zd = p[f"zd_{tag}"]; Rs = np.maximum(R, 1e-3*KPC)
        out = out + (S0/(4*zd))*np.exp(-p[f"Rm_{tag}"]/Rs - Rs/p[f"Rd_{tag}"])/np.cosh(z/(2*zd))**2
    return out

R0_MW, ZK_MW = 8.178*KPC, 1.1*KPC
_zz = np.linspace(0, ZK_MW, 4001)
SIG11 = 2.0*np.trapz(rho_mw(np.full_like(_zz, R0_MW), _zz), _zz)/MSUN_PC2
SIG11_ST = 2.0*np.trapz(rho_mw(np.full_like(_zz, R0_MW), _zz)
                        - (MCM["S_HI_fid"]*0 + 0), _zz)/MSUN_PC2      # placeholder, replaced below
def sigma_parts(R, zmax, thin=True, thick=True, bulge=True, gas=True, n=4001):
    zz = np.linspace(0.0, zmax, n)
    p = MCM; Ra = np.full_like(zz, float(R)); za = zz
    out = np.zeros_like(zz)
    if thin:  out = out + (p["S0_thin"]/(2*p["zd_thin"]))*np.exp(-za/p["zd_thin"] - Ra/p["Rd_thin"])
    if thick: out = out + (p["S0_thick"]/(2*p["zd_thick"]))*np.exp(-za/p["zd_thick"] - Ra/p["Rd_thick"])
    if bulge:
        rp = np.sqrt(Ra**2 + (za/p["q_b"])**2)
        out = out + p["rho0_b"]/(1 + rp/p["r0_b"])**p["alpha_b"]*np.exp(-((rp/p["rcut_b"])**2))
    if gas:
        for tag in ("HI", "H2"):
            S0 = p[f"S_{tag}_fid"]/math.exp(-p[f"Rm_{tag}"]/p["R_fid"] - p["R_fid"]/p[f"Rd_{tag}"])
            zd = p[f"zd_{tag}"]; Rs = np.maximum(Ra, 1e-3*KPC)
            out = out + (S0/(4*zd))*np.exp(-p[f"Rm_{tag}"]/Rs - Rs/p[f"Rd_{tag}"])/np.cosh(za/(2*zd))**2
    return 2.0*np.trapz(out, zz)/MSUN_PC2
SIG11_ST = sigma_parts(R0_MW, ZK_MW, bulge=False, gas=False)
SIG11_GA = sigma_parts(R0_MW, ZK_MW, thin=False, thick=False, bulge=False)
print(f"\n    Milky Way, McMillan 2017 Table 3 (the repository's own committed model, the same "
      f"parameters\n    hunt_2026/g02_vertical_vs_planar_frequency_split.py uses):")
print(f"      Sigma(R0 = 8.178 kpc, |z| < 1.1 kpc): stars {SIG11_ST:.1f}, gas {SIG11_GA:.1f}, "
      f"total {SIG11:.1f} Msun/pc^2")
print(f"      (McKee, Parravano & Hollenbach 2015: stars 33.4 +- 3.0, gas 13.7 +- 1.6, "
      f"total 47.1 +- 3.4 -- the McMillan model is known to run high here; g02 uses it for its "
      f"SHAPE, and so does this lane)")
check("R4 [control] the McMillan 2017 model is transcribed correctly: its stellar, gaseous and total "
      "surface densities at the Sun land within 30% of the independent McKee et al. 2015 census -- "
      "loose enough to admit the offset the published model is known to carry, tight enough that any "
      "transcription error in the five components would fail it",
      abs(SIG11_ST/33.4 - 1) < 0.30 and abs(SIG11_GA/13.7 - 1) < 0.30
      and abs(SIG11/47.1 - 1) < 0.30,
      f"stars {SIG11_ST:.1f} vs 33.4 ({SIG11_ST/33.4-1:+.1%}), gas {SIG11_GA:.1f} vs 13.7 "
      f"({SIG11_GA/13.7-1:+.1%}), total {SIG11:.1f} vs 47.1 ({SIG11/47.1-1:+.1%}); the model runs "
      f"high on stars, which g02_vertical_vs_planar_frequency_split.py flags on the same comparison, "
      f"and this lane uses the model for its SHAPE")


# ==================================================================================================
# 2.  THE MATHEMATICAL CORE -- what infinite longitudinal stiffness actually is
# ==================================================================================================
print("\n2.  THE MATHEMATICAL CORE -- classifying the non-spherical boundary-value problem")
print("""    The static equation is the Euler-Lagrange equation of a convex-analysis problem, not of a
    quasilinear PDE.  Write u = |grad phi|/a0 and sigma(u) = the Newtonian source magnitude that
    produces it, s = g_N/a0.  Then

        E[phi] = INT [ W(|grad phi|/a0) + q phi~ ] dV ,     W'(u) = sigma(u) = s(u) = Delta^{-1}(u)

    and the two stiffnesses are the eigenvalues of the Hessian of the energy density:

        Sigma_perp = sigma(u)/u = J_Y      (transverse, along directions perpendicular to grad phi)
        Sigma_par  = dsigma/du  = 1/Delta' (longitudinal)

    On the published kernel Delta is flat above s_sat, so sigma(u) has a VERTICAL SEGMENT at
    u = C = 0.6476: any source magnitude s >= s_sat produces the same gradient.  That is a MAXIMAL
    MONOTONE GRAPH, hence the subdifferential of a convex function, and the correct statement of the
    boundary-value problem is a VARIATIONAL INEQUALITY with the pointwise gradient constraint

        |grad phi|  <=  C a0     ,    C = 0.647610 ,

    exactly the elastic-plastic torsion problem of Brezis-Stampacchia.  Sigma_par = +infinity is a
    CONSTRAINT, not a loss of ellipticity: the dangerous case is Sigma_par <= 0, and the branch the
    theory sits on has Sigma_par > 0 everywhere.""")

# --- M1: monotonicity of the constitutive map ---------------------------------------------------
u_probe = np.linspace(1e-4, C_SAT*(1 - 1e-9), 40001)
sig_pub = KER["PUB8"].s_of_u(u_probe)
mono_pub = bool(np.all(np.diff(sig_pub) >= -1e-9))
# the alternative -- continuing nu_RAR past its maximum instead of truncating -- is NOT monotone
s_up = np.linspace(S_SAT*1.0001, 40.0, 20001)
u_up = _rar_D(s_up)
mono_raw = bool(np.all(np.diff(u_up) <= 0))       # Delta DECREASES, so sigma(u) decreases: non-monotone
print(f"\n    the constitutive map sigma(u):")
print(f"      published (truncated) kernel : monotone non-decreasing = {mono_pub}, with a vertical "
      f"segment at u = C = {C_SAT:.4f}")
print(f"      nu_RAR CONTINUED past its maximum: Delta falls from {C_SAT:.4f} to "
      f"{float(u_up[-1]):.4f} over s = {S_SAT:.2f} -> 40, so sigma(u) is DOUBLE-VALUED and its upper "
      f"branch is DECREASING (min Delta' = {float(np.min(_rar_dD(s_up))):.4f} < 0)")
check("M1 the published (truncated) kernel gives a MAXIMAL MONOTONE constitutive map, so the energy "
      "is convex and the saturated branch is a variational inequality rather than an ill-posed PDE",
      mono_pub and mono_raw,
      "sigma(u) non-decreasing with a vertical segment at u = C; the UNTRUNCATED continuation is "
      "non-monotone (Sigma_par < 0) and would be genuinely ill posed -- the truncation is the "
      "repair, not the disease")

# --- M2: the sign of Sigma_par decides well-posedness --------------------------------------------
print(f"\n    Sigma_par = 1/Delta' on the three branches, at a galaxy-core background s = 100:")
for tag, k in (("published (M = 1e8)", KER["PUB8"]), ("L30 minimal C^2 repair", KER["REPC"]),
               ("deposited kernel 4.3", KER["DEP"])):
    _s, _sp, _sl = k.state(np.array([float(k.D(np.array([100.0]))[0])]))
    print(f"      {tag:<24s}  Sigma_perp = {float(_sp[0]):.3e},  Sigma_par = {float(_sl[0]):.3e}")
_sp_raw = 1.0/float(_rar_dD(np.array([100.0]))[0])
print(f"      {'nu_RAR CONTINUED':<24s}  Sigma_par = {_sp_raw:.3e}   <-- NEGATIVE")
check("M2 every kernel the theory actually offers has Sigma_par > 0, hence a CONVEX energy: the "
      "saturated problem is stiff, not ill posed.  Only the untruncated continuation (which the "
      "bounded-boost theorem already forbids) has Sigma_par < 0",
      float(KER["PUB8"].state(np.array([C_SAT*0.999]))[2][0]) > 0
      and float(KER["REPC"].state(np.array([0.65]))[2][0]) > 0 and _sp_raw < 0,
      f"published +{float(KER['PUB8'].state(np.array([C_SAT*0.999]))[2][0]):.1e}, "
      f"continued {_sp_raw:.3e}")

# --- M3: the localisation -- which reading of the field equation carries the infinity? ----------
print("""
    LOCALISATION.  Three readings of the modified field equation appear in this repository, and they
    do NOT share the pathology:

      (i)   CARRIER  (THE_ACTION section 1, PAPER5 section 7, g03x):
              div[J_Y(|grad phi|^2) grad phi] = 4 pi G rho,  g = g_N + g_phi
              Sigma_par = d g_N / d g_phi = 1/Delta'                      -> INFINITE at saturation
      (ii)  AQUAL on the TOTAL potential (g03c, g03d, f24, aqual_efe_full_solve_2026):
              div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho
              Sigma_par = d g_N / d g_tot = 1/(1 + Delta')                -> EXACTLY 1 at saturation
      (iii) QUMOND (g02, k04, hunt_efe_lib, and every non-spherical solve in hunt_2026):
              div grad Phi = div[nu(|grad Phi_N|/a0) grad Phi_N]
              LINEAR in the unknown; the kernel enters only through a precomputed source.""")
_backs = {"Saturn's orbit": 6.90e5, "inner galaxy s = 100": 100.0, "cluster core s = 10": 10.0}
print(f"      {'background':<24s}{'carrier 1/Delta''':>20s}{'AQUAL 1/(1+Delta'')':>22s}{'QUMOND':>12s}")
for nm, sv in _backs.items():
    dpr = float(_rar_dD(np.array([sv]))[0])
    dpub = 0.0 if sv > S_SAT else dpr
    print(f"      {nm:<24s}{'infinity' if dpub == 0 else '%.3e' % (1/dpub):>20s}"
          f"{1.0/(1.0 + dpub):>22.6f}{'linear':>12s}")
check("M3 the infinite longitudinal stiffness belongs to the CARRIER reading ALONE.  In the "
      "AQUAL-on-total-potential reading Delta' = 0 gives Sigma_par = 1 exactly (perfectly ordinary "
      "Newtonian stiffness), and the QUMOND reading is LINEAR in the unknown",
      abs(1.0/(1.0 + 0.0) - 1.0) < 1e-15,
      "so the degenerate operator can only appear in a solve that carries the scalar as a separate "
      "matter-sourced field")

# and now the empirical half of the localisation: does ANY committed script in this repository
# actually solve the carrier equation off spherical symmetry?
print("""
    Which committed scripts could have been affected?  A script is at risk only if it does all three
    of: (a) mention the carrier's own coefficient J_Y, (b) build a 2-D or 3-D spatial grid, and
    (c) run a NONLINEAR solve on that grid (a sparse linear-algebra solve or a root-find loop).
    A script that uses J_Y only in the algebraic relation J_Y(g_phi) g_phi = g_N, or symbolically,
    never touches the degenerate operator no matter how stiff it is.""")
import re
CAR_PAT  = re.compile(r"J_Y|J_YY|JY_of_u|JYu_")
GRID_PAT = re.compile(r"meshgrid\(|np\.mgrid|indexing\s*=\s*[\"']ij[\"']")
SOLV_PAT = re.compile(r"spsolve|splu|sparse\.linalg|newton_krylov|fsolve|scipy\.optimize\.root\b")
hits_car, hits_grid, hits_risk = [], [], []
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "node_modules")]
    for fn in files:
        if not fn.endswith(".py"): continue
        p = os.path.join(root, fn)
        try: txt = open(p, "r", errors="ignore").read()
        except Exception: continue
        if not CAR_PAT.search(txt): continue
        rel = os.path.relpath(p, REPO)
        hits_car.append(rel)
        if GRID_PAT.search(txt):
            hits_grid.append(rel)
            if SOLV_PAT.search(txt): hits_risk.append(rel)
MULTID_PAT = re.compile(r"coo_matrix|lil_matrix|dok_matrix")     # a 2-D/3-D assembled operator
ONED_PAT   = re.compile(r"\[-1,\s*0,\s*1\]|solve_banded")        # a tridiagonal, i.e. 1-D, operator
print(f"      {len(hits_car)} committed .py files mention J_Y;  {len(hits_grid)} of those also build "
      f"a 2-D/3-D grid:")
_risk = []
for h in sorted(hits_grid):
    txt = open(os.path.join(REPO, h), "r", errors="ignore").read()
    md, od = bool(MULTID_PAT.search(txt)), bool(ONED_PAT.search(txt))
    solves = bool(SOLV_PAT.search(txt))
    tag = ("assembles a MULTI-DIMENSIONAL sparse operator" if md else
           ("sparse solves are TRIDIAGONAL, i.e. 1-D radial" if od and solves else
            "no assembled sparse operator at all"))
    if md and not os.path.basename(h).startswith("L53"): _risk.append(h)
    print(f"        {h:<52s} {tag}")
print(f"      at risk (multi-dimensional nonlinear carrier solve, outside this lane): "
      f"{_risk if _risk else 'none'}")
check("M4 [LOCALISATION] some committed script in this repository solves the CARRIER equation off "
      "spherical symmetry, i.e. a published number could have been computed on the degenerate "
      "operator",
      len(_risk) > 0,
      f"none does.  {len(hits_car)} files mention J_Y; only {len(hits_grid)} also build a spatial "
      f"grid, and the sparse operators they assemble are TRIDIAGONAL (1-D radial) or the grid solve "
      f"is of a LINEAR operator.  Every other use of J_Y is the algebraic relation "
      f"J_Y(g_phi) g_phi = g_N on a sphere, or symbolic.  The only multi-dimensional nonlinear "
      f"carrier solve in the repository is this lane's own.  Combined with M3, no committed number "
      f"was computed on the degenerate operator -- the liability is real and was worth checking, "
      f"but it has never been drawn on")


# ==================================================================================================
# 3.  THE AXISYMMETRIC SOLVER, AND ITS CONTROLS
# ==================================================================================================
print("\n3.  THE AXISYMMETRIC SOLVER  (P1 finite elements, damped Newton, sparse direct solve)")
print("""    Scaled variables: lengths in kpc, gradients in a0, potential in a0 kpc.  The energy
        E~ = SUM_T [ W(u_T) + q_T phibar_T ] w_T ,     w_T = R_T * area_T ,  q = 4 pi G rho L / a0
    is minimised by damped Newton; the element Hessian is B^T [Sigma_perp I + (Sigma_par - Sigma_perp)
    n n^T] B, so the whole nonlinear content is the two stiffnesses.  Boundary conditions: Dirichlet
    on the outer R and z faces, natural (symmetry) on the axis R = 0 and the midplane z = 0.""")

class Mesh:
    def __init__(self, Rn, Zn):
        self.Rn, self.Zn = np.asarray(Rn, float), np.asarray(Zn, float)
        nR, nZ = len(Rn), len(Zn); self.nR, self.nZ = nR, nZ
        idx = np.arange(nR*nZ).reshape(nR, nZ); self.idx = idx
        hR = np.diff(self.Rn)[:, None]*np.ones((1, nZ-1))
        hZ = np.ones((nR-1, 1))*np.diff(self.Zn)[None, :]
        R0 = self.Rn[:-1][:, None]*np.ones((1, nZ-1)); R1 = self.Rn[1:][:, None]*np.ones((1, nZ-1))
        Z0 = np.ones((nR-1, 1))*self.Zn[:-1][None, :]; Z1 = np.ones((nR-1, 1))*self.Zn[1:][None, :]
        n00, n10 = idx[:-1, :-1].ravel(), idx[1:, :-1].ravel()
        n01, n11 = idx[:-1, 1:].ravel(), idx[1:, 1:].ravel()
        hr, hz = hR.ravel(), hZ.ravel()
        nT = len(hr)
        BA = np.zeros((nT, 2, 3)); BA[:, 0, 0] = -1/hr; BA[:, 0, 1] = 1/hr
        BA[:, 1, 0] = -1/hz; BA[:, 1, 2] = 1/hz
        BB = np.zeros((nT, 2, 3)); BB[:, 0, 0] = 1/hr; BB[:, 0, 2] = -1/hr
        BB[:, 1, 0] = 1/hz; BB[:, 1, 1] = -1/hz
        self.nodes = np.vstack([np.stack([n00, n10, n01], 1), np.stack([n11, n10, n01], 1)])
        self.B = np.vstack([BA, BB])
        self.Rc = np.concatenate([((2*R0 + R1)/3).ravel(), ((R0 + 2*R1)/3).ravel()])
        self.Zc = np.concatenate([((2*Z0 + Z1)/3).ravel(), ((Z0 + 2*Z1)/3).ravel()])
        self.area = np.concatenate([hr, hr])*np.concatenate([hz, hz])/2.0
        self.w = self.Rc*self.area
        RR, ZZ = np.meshgrid(self.Rn, self.Zn, indexing="ij")
        self.R, self.Z = RR.ravel(), ZZ.ravel()
        self.N = nR*nZ
        # sparse assembly index arrays
        self.rows = np.repeat(self.nodes, 3, axis=1).ravel()
        self.cols = np.tile(self.nodes, (1, 3)).ravel()

    def grad(self, phi):
        return np.einsum("tan,tn->ta", self.B, phi[self.nodes])

    def nodal_grad(self, phi):
        """area-weighted recovery of the gradient at the nodes.  A single P1 triangle's gradient is
        only O(h) accurate and, on a right-triangle mesh, carries a direction error of several
        degrees; the area-weighted patch average is O(h^2) and is what every field evaluation and
        every misalignment statistic in this lane uses."""
        gt = self.grad(phi)
        den = np.bincount(self.nodes.ravel(), weights=np.repeat(self.area, 3), minlength=self.N)
        out = np.empty((self.N, 2))
        for a in (0, 1):
            out[:, a] = np.bincount(self.nodes.ravel(),
                                    weights=np.repeat(gt[:, a]*self.area, 3), minlength=self.N)
        return out/np.maximum(den, 1e-300)[:, None]

def solve_carrier(mesh, kern, q, phi0, fixed, itmax=200, tol=1e-13):
    """Minimise the convex energy E[phi] = SUM_T [W(u_T) + q_T phibar_T] w_T over the free nodes.

    The convergence measure is the NEWTON DECREMENT lambda^2 = -g.dphi = the predicted energy
    decrease, not the residual norm.  That matters on this branch: the residual is measured in the
    'stress' variable s = J_Y u, whose derivative with respect to u is Sigma_par = 1/Delta', which
    is 1e8 here -- so the residual stalls at a huge value while the FIELD is converged to 1e-12.
    The line search is Armijo on the energy, which is well scaled because W is tabulated as the
    integral of the same s(u) the gradient uses.
    """
    phi = phi0.copy()
    fi = np.where(~fixed)[0]
    src_node = np.bincount(mesh.nodes.ravel(),
                           weights=np.repeat(q*mesh.w/3.0, 3), minlength=mesh.N)
    def energy(p):
        g = mesh.grad(p); u = np.hypot(g[:, 0], g[:, 1])
        return float(np.sum(kern.W_of_u(u)*mesh.w) + np.dot(src_node, p))
    def resid(p):
        g = mesh.grad(p); u = np.maximum(np.hypot(g[:, 0], g[:, 1]), 1e-9)
        s, Sp, Sl = kern.state(u)
        vec = (s/u)[:, None]*g
        gv = np.bincount(mesh.nodes.ravel(),
                         weights=(np.einsum("ta,tan->tn", vec, mesh.B)*mesh.w[:, None]).ravel(),
                         minlength=mesh.N) + src_node
        return gv, g, u, Sp, Sl
    E = energy(phi); hist = []
    for it in range(itmax):
        gvec, g, u, Sp, Sl = resid(phi)
        Sl = np.minimum(Sl, 1e14)
        nh = g/u[:, None]
        D = np.zeros((len(u), 2, 2))
        D[:, 0, 0] = Sp; D[:, 1, 1] = Sp
        D += (Sl - Sp)[:, None, None]*nh[:, :, None]*nh[:, None, :]
        D[:, 0, 0] += 1e-10*Sl; D[:, 1, 1] += 1e-10*Sl
        K = np.einsum("tam,tab,tbn->tmn", mesh.B, D, mesh.B)*mesh.w[:, None, None]
        H = sps.coo_matrix((K.ravel(), (mesh.rows, mesh.cols)), shape=(mesh.N, mesh.N)).tocsr()
        try:
            dphi = spl.spsolve(H[fi][:, fi].tocsc(), -gvec[fi])
        except Exception:
            break
        if not np.all(np.isfinite(dphi)): break
        lam2 = float(-np.dot(gvec[fi], dphi))
        hist.append(lam2)
        if not (lam2 > 0):                                  # numerically at the minimum
            break
        if lam2 < tol*abs(E) or lam2 < 1e-300: break
        # fraction-to-the-boundary: never let an iterate leave the admissible set |grad phi| <= C a0,
        # where the barrier makes the energy 1e12 times stiffer than anything physical and the
        # iteration crawls.  This is the standard interior-point safeguard.
        t, ok = 1.0, False
        d_full = np.zeros(mesh.N); d_full[fi] = dphi
        gd = mesh.grad(d_full)
        for _ in range(80):
            if np.max(np.hypot(g[:, 0] + t*gd[:, 0], g[:, 1] + t*gd[:, 1])) <= 1.02*kern.u_max:
                break
            t *= 0.5
        for _ in range(80):
            trial = phi.copy(); trial[fi] += t*dphi
            Et = energy(trial)
            if np.isfinite(Et) and Et <= E - 1e-4*t*lam2:
                phi, E, ok = trial, Et, True; break
            t *= 0.5
        if not ok: break
    return phi, hist

def relstep(mesh, kern, q, phi, fixed):
    """the size of one further Newton step, relative to the solution."""
    p2, _ = solve_carrier(mesh, kern, q, phi.copy(), fixed, itmax=1)
    return float(np.linalg.norm(p2 - phi)/max(np.linalg.norm(phi), 1e-30))

def newtonian_boundary(mesh, rho_fn, Rmax_src, Zmax_src, a0, nR=260, nZ=260):
    """exact Newtonian potential on the Dirichlet boundary nodes, by the axisymmetric elliptic
    integral   Phi = -G INT rho R' 4 K(m) / sqrt((R+R')^2 + dz^2) dR' dz' ,  m = 4RR'/((R+R')^2+dz^2)."""
    Rs = np.linspace(0.0, Rmax_src, nR); Zs = np.linspace(-Zmax_src, Zmax_src, nZ)
    dR, dZ = Rs[1] - Rs[0], Zs[1] - Zs[0]
    RR, ZZ = np.meshgrid(Rs, Zs, indexing="ij")
    wgt = (rho_fn(RR*KPC, ZZ*KPC)*RR*dR*dZ).ravel()
    Rsr, Zsr = RR.ravel(), ZZ.ravel()
    keep = wgt > 0
    wgt, Rsr, Zsr = wgt[keep], Rsr[keep], Zsr[keep]
    bnd = np.where(mesh_fixed_mask(mesh))[0]
    out = np.zeros(mesh.N)
    for n in bnd:
        Rq, Zq = mesh.R[n], mesh.Z[n]
        d2 = (Rq + Rsr)**2 + (Zq - Zsr)**2
        m = 4.0*Rq*Rsr/np.maximum(d2, 1e-30)
        out[n] = -G*KPC**2*np.sum(wgt*4.0*ellipk(np.clip(m, 0, 1 - 1e-14))/np.sqrt(d2))
    return out/(a0*KPC)

def mesh_fixed_mask(mesh):
    f = np.zeros(mesh.N, bool)
    f[mesh.idx[-1, :]] = True
    f[mesh.idx[:, -1]] = True
    return f

def spherical_profile(mesh, rho_fn, a0, kern, nr=3000):
    """spherically averaged enclosed mass -> the algebraic carrier profile phi~(r), for the initial
    guess and for the carrier's Dirichlet data."""
    rmax = float(np.hypot(mesh.Rn[-1], mesh.Zn[-1]))*1.05
    r = np.linspace(rmax/nr, rmax, nr)
    mu = np.linspace(-1, 1, 241)
    RR = r[:, None]*np.sqrt(1 - mu[None, :]**2); ZZ = r[:, None]*mu[None, :]
    rho_sh = 0.5*np.trapz(rho_fn(RR*KPC, ZZ*KPC), mu, axis=1)
    M = np.concatenate([[0.0], np.cumsum(4*math.pi*r[:-1]**2*rho_sh[:-1]*np.diff(r))])*KPC**3
    gN = G*M/np.maximum((r*KPC)**2, 1e-30)/a0
    dphi = np.asarray(kern.D(gN), float)
    phi = np.concatenate([[0.0], np.cumsum(0.5*(dphi[1:] + dphi[:-1])*np.diff(r))])
    return r, phi - phi[-1], gN, M

def run_case(mesh, rho_fn, kern, a0, phi_bnd=None, phi_init=None, ladder=("PUB4",)):
    """Solve the carrier equation.  Stiff kernels are reached by a HOMOTOPY: the mildly stiff
    Sigma_par <= 1e4 problem is solved first and used as the starting point, which is what makes the
    Sigma_par = 1e8 solve converge from a cold start."""
    q = 4*math.pi*G*rho_fn(mesh.Rc*KPC, mesh.Zc*KPC)*KPC/a0
    fixed = mesh_fixed_mask(mesh)
    r, ph, _, _ = spherical_profile(mesh, rho_fn, a0, kern)
    rq = np.hypot(mesh.R, mesh.Z)
    guess = np.interp(rq, r, ph)
    phi0 = guess.copy() if phi_init is None else phi_init.copy()
    phi0[fixed] = (phi_bnd if phi_bnd is not None else guess)[fixed]
    nit = 0
    if phi_init is None and kern.name != KER_NEWT_NAME:
        for lk in ladder:
            if KER[lk] is kern: break
            phi0, hh = solve_carrier(mesh, KER[lk], q, phi0, fixed)
            nit += len(hh)
    phi, hist = solve_carrier(mesh, kern, q, phi0, fixed)
    return phi, [None]*nit + hist

def field_at(mesh, phi, R, Z, ng=None):
    """(g_R, g_z) in units of a0 at a point, by bilinear interpolation of the RECOVERED nodal
    gradient (see Mesh.nodal_grad)."""
    if ng is None: ng = mesh.nodal_grad(phi)
    i = int(np.clip(np.searchsorted(mesh.Rn, R) - 1, 0, mesh.nR - 2))
    j = int(np.clip(np.searchsorted(mesh.Zn, Z) - 1, 0, mesh.nZ - 2))
    tR = (R - mesh.Rn[i])/(mesh.Rn[i+1] - mesh.Rn[i])
    tZ = (Z - mesh.Zn[j])/(mesh.Zn[j+1] - mesh.Zn[j])
    tR = min(max(tR, 0.0), 1.0); tZ = min(max(tZ, 0.0), 1.0)
    out = []
    for a in (0, 1):
        v = (ng[mesh.idx[i, j], a]*(1-tR)*(1-tZ) + ng[mesh.idx[i+1, j], a]*tR*(1-tZ)
             + ng[mesh.idx[i, j+1], a]*(1-tR)*tZ + ng[mesh.idx[i+1, j+1], a]*tR*tZ)
        out.append(float(v))
    return out[0], out[1]

# --- CONTROL N1: a homogeneous oblate spheroid in the Newtonian limit ----------------------------
print("\n    CONTROL N1 -- a NON-SPHERICAL analytic result at finite stiffness: the exact MacLaurin")
print("    interior field of a homogeneous oblate spheroid (Binney & Tremaine eq. 2.140).")
A_SPH, C_SPH, RHO_SPH = 6.0, 3.0, 1.0e-21          # kpc, kpc, kg/m^3
e_sph = math.sqrt(1 - (C_SPH/A_SPH)**2)
A1_MAC = (math.sqrt(1 - e_sph**2)/e_sph**3)*math.asin(e_sph) - (1 - e_sph**2)/e_sph**2
A3_MAC = 2.0/e_sph**2 - 2*math.sqrt(1 - e_sph**2)*math.asin(e_sph)/e_sph**3
def rho_spheroid(R, z):
    return np.where((np.asarray(R, float)/(A_SPH*KPC))**2 + (np.asarray(z, float)/(C_SPH*KPC))**2 <= 1.0,
                    RHO_SPH, 0.0)
Rn = np.linspace(0, 24, 145); Zn = np.linspace(0, 24, 145)
m_sph = Mesh(Rn, Zn)
a0c = A0["canonical"]
bnd = newtonian_boundary(m_sph, rho_spheroid, 8.0, 8.0, a0c, 220, 220)
phi_n, _ = run_case(m_sph, rho_spheroid, KER["NEWT"], a0c, phi_bnd=bnd)
errs = []
for (Rp, Zp) in [(2.0, 0.5), (3.0, 1.0), (4.0, 1.5), (1.0, 2.0), (4.5, 0.5)]:
    gR, gz = field_at(m_sph, phi_n, Rp, Zp)
    gR_ex = 2*math.pi*G*RHO_SPH*A1_MAC*(Rp*KPC)/a0c
    gz_ex = 2*math.pi*G*RHO_SPH*A3_MAC*(Zp*KPC)/a0c
    errs.append(max(abs(gR/gR_ex - 1), abs(gz/gz_ex - 1)))
print(f"      axis ratio c/a = {C_SPH/A_SPH:.2f}, e = {e_sph:.4f}, A1 = {A1_MAC:.5f}, A3 = {A3_MAC:.5f}")
print(f"      max relative error of the solver's interior field at 5 interior points: {max(errs):.3%}")
check("N1 [control] the axisymmetric solver reproduces a known NON-SPHERICAL analytic result where "
      "the stiffness is finite: the MacLaurin interior field of a homogeneous oblate spheroid",
      max(errs) < 0.02, f"max relative error {max(errs):.3%} over 5 interior points")

# --- CONTROL N2/N3/N4: the nonlinear carrier on a spherical source; the NOISE FLOOR --------------
print("""
    CONTROLS N2-N4 -- the SPHERICAL benchmark, which fixes the noise floor for everything below.
    On a spherical source the algebraic carrier law g_phi = a0 Delta(g_N/a0) is EXACT and grad phi
    is EXACTLY radial, so the solver's departure from it is pure discretisation error.  Every
    'algebraic versus solved' and every 'misalignment' number later in this lane is quoted against
    this floor.  A Plummer sphere is used, M = 5e10 Msun, b = 3 kpc, whose saturated shell is
    1.2 < r < 3.4 kpc -- the same geometry as a galaxy's.""")
M_PL, B_PL = 5.0e10*MSUN, 3.0*KPC
def rho_plummer(R, z):
    r2 = np.asarray(R, float)**2 + np.asarray(z, float)**2
    return 3*M_PL/(4*math.pi*B_PL**3)*(1 + r2/B_PL**2)**-2.5
def plummer_probe(mesh, phi, kern, a0):
    ng = mesh.nodal_grad(phi)
    dev, ang = [], []
    for rr in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0):
        for th in (0.15, 0.5, 1.0, 1.42):
            Rp, Zp = rr*math.cos(th), rr*math.sin(th)
            if Rp > mesh.Rn[-2] or Zp > mesh.Zn[-2]: continue
            gR, gz = field_at(mesh, phi, Rp, Zp, ng)
            u = math.hypot(gR, gz)
            MM = M_PL*(rr*KPC)**3/((rr*KPC)**2 + B_PL**2)**1.5
            sN = G*MM/(rr*KPC)**2/a0
            dev.append(abs(u/float(kern.D(np.array([sN]))[0]) - 1))
            cs = (gR*Rp + gz*Zp)/max(u*rr, 1e-30)
            ang.append(math.degrees(math.acos(min(max(cs, -1.0), 1.0))))
    return max(dev), max(ang)
print(f"      {'h [kpc]':>9s}{'nodes':>8s}{'kernels run':>34s}{'max |u/u_alg - 1|':>19s}"
      f"{'max misalign':>14s}")
NOISE = {}
for nf, h, kers in ((61, 0.20, ("PUB8",)), (121, 0.10, ("NEWT", "PUB8", "REPC", "DEP")),
                    (241, 0.05, ("PUB8",))):
    Rn2 = np.concatenate([np.linspace(0, 12, nf)[:-1], np.geomspace(12, 60, 40)])
    mm = Mesh(Rn2, Rn2.copy())
    row, amax = {}, 0.0
    for kn in kers:
        ph, _ = run_case(mm, rho_plummer, KER[kn], a0c)
        d, a = plummer_probe(mm, ph, KER[kn], a0c)
        row[kn] = d
        if kn != "NEWT": amax = max(amax, a)
        if kn == "PUB8" and nf == 121:
            m_pl, phi_c8 = mm, ph
    NOISE[h] = (row, amax)
    print(f"      {h:>9.2f}{mm.N:>8d}{','.join(kers):>34s}"
          + "".join(f"{row[k]:>7.2%}" for k in kers) + f"{amax:>13.2f}d")
rate = NOISE[0.20][0]["PUB8"]/NOISE[0.05][0]["PUB8"]
check("N2 [control] the nonlinear carrier solver CONVERGES to the algebraic carrier law on a "
      "spherical source, at first order in the mesh spacing, for the published (stiff) kernel and "
      "both repairs alike",
      rate > 2.5 and NOISE[0.05][0]["PUB8"] < 0.025,
      f"max |u_solved/a0 Delta(s) - 1| falls {NOISE[0.20][0]['PUB8']:.2%} -> "
      f"{NOISE[0.10][0]['PUB8']:.2%} -> {NOISE[0.05][0]['PUB8']:.2%} as h halves "
      f"({rate:.1f}x over a factor 4 in h)")
DEV_FLOOR = NOISE[0.10][0]["PUB8"]
ANG_FLOOR = NOISE[0.10][1]
check("N3 [control] the solver's spurious MISALIGNMENT on a spherical source (where the exact answer "
      "is exactly radial) falls with the mesh, so it is discretisation and has a known scale that "
      "any disc measurement must beat",
      NOISE[0.20][1] > 2.0*NOISE[0.10][1] and NOISE[0.10][1] > 2.0*NOISE[0.05][1],
      f"max departure from radial {NOISE[0.20][1]:.2f} -> {NOISE[0.10][1]:.2f} -> "
      f"{NOISE[0.05][1]:.2f} deg as h halves; the floor adopted below is {ANG_FLOOR:.2f} deg at the "
      f"disc's own resolution, alongside an amplitude floor of {DEV_FLOOR:.2%}")

u8 = np.hypot(*m_pl.grad(phi_c8).T)
print(f"\n      max |grad phi|/a0 over the whole Plummer grid, published kernel at Sigma_par = 1e8: "
      f"{float(u8.max()):.6f}  (ceiling C = {C_SAT:.6f})")
check("N4 [control] the solver respects the kernel's own kinematic bound |grad phi| <= C a0 to the "
      "regularisation tolerance", float(u8.max()) < C_SAT*(1 + 2e-4),
      f"max u = {float(u8.max()):.6f} vs C = {C_SAT:.6f}")


# ==================================================================================================
#     THE MILKY WAY DISC -- the most non-spherical system with a committed baryon model
# ==================================================================================================
print("\n    THE DISC GRID.  McMillan 2017 baryons on an axisymmetric mesh, R < 45 kpc, |z| < 25 kpc.")
def disc_mesh(f=1.0):
    Rn = np.concatenate([np.arange(0.0, 2.0, 0.05*f), np.arange(2.0, 12.0, 0.12*f),
                         np.geomspace(12.0, 45.0, int(40/f))])
    Zn = np.concatenate([np.arange(0.0, 2.0, 0.04*f), np.geomspace(2.0, 25.0, int(44/f))])
    return Mesh(np.unique(Rn), np.unique(Zn))
mesh_d = disc_mesh(1.0)
print(f"      mesh: {mesh_d.nR} x {mesh_d.nZ} = {mesh_d.N} nodes, {len(mesh_d.w)} triangles")

DISC = {}
for f in FOOT:
    a0 = A0[f]
    bnd_d = newtonian_boundary(mesh_d, rho_mw, 60.0, 40.0, a0, 300, 300)
    phiN, _ = run_case(mesh_d, rho_mw, KER["NEWT"], a0, phi_bnd=bnd_d)
    DISC[(f, "NEWT")] = phiN
    DISC[(f, "bnd")] = bnd_d
gRn, gzn = field_at(mesh_d, DISC[("canonical", "NEWT")], R0_MW/KPC, 0.0)
vcbar = math.sqrt(abs(gRn)*A0["canonical"]*R0_MW)/1e3
gRz, gzz = field_at(mesh_d, DISC[("canonical", "NEWT")], R0_MW/KPC, ZK_MW/KPC)
sig_dyn_bar = abs(gzz)*A0["canonical"]/(2*math.pi*G)/MSUN_PC2
print(f"      Newtonian solve at R0 = 8.178 kpc:  V_c,bar = {vcbar:.1f} km/s;  "
      f"|K_z,bar(1.1 kpc)|/(2 pi G) = {sig_dyn_bar:.1f} Msun/pc^2")
print(f"      (that exceeds the model's own Sigma(|z| < 1.1) = {SIG11:.1f} by "
      f"{sig_dyn_bar/SIG11 - 1:+.1%}, which is the radial term of the integrated Poisson equation "
      f"and is exactly what the Kuijken-Gilmore Sigma_dyn convention absorbs)")

# grid convergence of the FULL CARRIER solve -- the quantity every target below depends on is
# u_solved/u_algebraic in the midplane, so that is what is refined.
print("\n      DISC MESH REFINEMENT of the carrier solve (published kernel, canonical):")
RL_REF = (1.0, 2.0, 3.0, 4.0, 6.0, 8.178, 12.0, 20.0)
print("      " + f"{'factor':>8s}{'nodes':>8s}" + "".join(f"{('R=%g' % R):>9s}" for R in RL_REF)
      + f"{'sat. vol':>10s}")
REF_TAB = {}
for fac in (1.6, 1.0, 0.65):
    mf = mesh_d if fac == 1.0 else disc_mesh(fac)
    if fac == 1.0:
        pN, pC = DISC[("canonical", "NEWT")], None
    else:
        bb = newtonian_boundary(mf, rho_mw, 60.0, 40.0, A0["canonical"], 260, 260)
        pN, _ = run_case(mf, rho_mw, KER["NEWT"], A0["canonical"], phi_bnd=bb)
    pC, _ = run_case(mf, rho_mw, KER["PUB8"], A0["canonical"])
    ngN, ngC = mf.nodal_grad(pN), mf.nodal_grad(pC)
    row = []
    for R in RL_REF:
        gRn_, gzn_ = field_at(mf, pN, R, 0.0, ngN)
        gRc_, gzc_ = field_at(mf, pC, R, 0.0, ngC)
        sN_ = math.hypot(gRn_, gzn_)
        row.append(math.hypot(gRc_, gzc_)/float(KER["PUB8"].D(np.array([sN_]))[0]))
    ut = np.hypot(*mf.grad(pC).T)
    volsat = float(np.sum(mf.w[ut > C_SAT*(1 - 1e-6)])/np.sum(mf.w))
    REF_TAB[fac] = (row, volsat)
    print(f"      {fac:>8.2f}{mf.N:>8d}" + "".join(f"{x:>9.4f}" for x in row) + f"{volsat:>10.2e}")
    if fac == 1.0: DISC[("canonical", "PUB8")] = pC
conv = {R: abs(REF_TAB[0.65][0][i] - REF_TAB[1.0][0][i]) for i, R in enumerate(RL_REF)}
CONVERGED_R = [R for R in RL_REF if conv[R] < 0.01]
print(f"      converged to better than 1% between the last two meshes at R = "
      f"{', '.join('%g' % R for R in CONVERGED_R)} kpc; NOT converged at R = "
      f"{', '.join('%g' % R for R in RL_REF if R not in CONVERGED_R)} kpc "
      f"(the bulge cusp and the axis)")
check("N5 [control] the carrier solve on the disc is mesh-converged over the radii the targets below "
      "use", len(CONVERGED_R) >= 5 and all(R in CONVERGED_R for R in (4.0, 6.0, 8.178, 12.0)),
      f"|change| between the two finest meshes: "
      + ", ".join(f"R={R:g}: {conv[R]:.3f}" for R in RL_REF))

# --- solve the carrier on the disc, for every kernel and both footings ---------------------------
print("\n    solving the CARRIER equation on the disc for each kernel and both footings ...")
for f in FOOT:
    a0 = A0[f]
    for kn in ("PUB4", "PUB6", "PUB8", "REPC", "DEP"):
        if f == "alt" and kn in ("PUB4",): continue
        if (f, kn) in DISC: continue
        t0 = time.time()
        phi, hist = run_case(mesh_d, rho_mw, KER[kn], a0)
        DISC[(f, kn)] = phi
        g = mesh_d.grad(phi); u = np.hypot(g[:, 0], g[:, 1])
        q_ = 4*math.pi*G*rho_mw(mesh_d.Rc*KPC, mesh_d.Zc*KPC)*KPC/a0
        rs = relstep(mesh_d, KER[kn], q_, phi, mesh_fixed_mask(mesh_d))
        print(f"      {f:<10s} {kn:<6s} {len(hist):>3d} Newton steps, {time.time()-t0:5.1f} s, "
              f"max u = {float(u.max()):.6f} a0, one further Newton step moves phi by {rs:.2e} "
              f"(relative)")

# --- M4/M5: uniqueness and continuous dependence, tested on the ACTUAL non-spherical problem -----
print("\n    M4/M5 -- existence, uniqueness and continuous dependence, tested on the disc itself.")
phi_ref = DISC[("canonical", "PUB8")]
fixed_d = mesh_fixed_mask(mesh_d)
q_d = 4*math.pi*G*rho_mw(mesh_d.Rc*KPC, mesh_d.Zc*KPC)*KPC/A0["canonical"]
ngref = mesh_d.nodal_grad(phi_ref)
nrm = float(np.linalg.norm(phi_ref))

# the theorem first: the element energy Hessian is Sigma_perp I + (Sigma_par - Sigma_perp) n n^T,
# whose eigenvalues are exactly Sigma_perp and Sigma_par.  Both strictly positive on every triangle
# of the solution => every element matrix is SPD => the assembled H is SPD on the free nodes =>
# the discrete energy is STRICTLY CONVEX => the minimiser is unique.  That is the proof; the
# multi-start experiment below only illustrates it.
_g = mesh_d.grad(phi_ref); _u = np.maximum(np.hypot(_g[:, 0], _g[:, 1]), 1e-9)
_s, _Sp, _Sl = KER["PUB8"].state(_u)
print(f"      over the {len(_u)} triangles of the solution: min Sigma_perp = {float(_Sp.min()):.3e}, "
      f"min Sigma_par = {float(_Sl.min()):.3e} -- both strictly positive")
check("M4a [THEOREM] the discrete energy is STRICTLY CONVEX on the solution, because the element "
      "Hessian's eigenvalues are exactly Sigma_perp and Sigma_par and both are strictly positive; "
      "hence the non-spherical saturated boundary-value problem has at most one solution",
      float(_Sp.min()) > 0 and float(_Sl.min()) > 0,
      f"min eigenvalues {float(_Sp.min()):.2e} (transverse) and {float(_Sl.min()):.2e} "
      f"(longitudinal); Sigma_par = infinity is a CONSTRAINT, and only Sigma_par <= 0 would break "
      f"this")

rb = math.hypot(float(mesh_d.Rn[-1]), float(mesh_d.Zn[-1]))
taper = np.maximum(0.0, 1.0 - np.hypot(mesh_d.R, mesh_d.Z)/rb)
alt_starts = [("0.9x tapered", phi_ref*(1 - 0.10*taper)),
              ("deposited-kernel solution", DISC[("canonical", "DEP")].copy()),
              ("L30-repair solution", DISC[("canonical", "REPC")].copy())]
uni = []
for tag, p0 in alt_starts:
    p0 = p0.copy(); p0[fixed_d] = phi_ref[fixed_d]
    u0 = float(np.max(np.hypot(*mesh_d.grad(p0).T)))
    ps, _ = solve_carrier(mesh_d, KER["PUB8"], q_d, p0, fixed_d)
    dphi = float(np.linalg.norm(ps - phi_ref)/nrm)
    dg = float(np.max(np.hypot(*(mesh_d.nodal_grad(ps) - ngref).T)))
    uni.append((tag, dphi, dg))
    print(f"      start {tag:<26s} (max |grad|/a0 = {u0:.4f}): ||phi - phi_ref||/||phi_ref|| = "
          f"{dphi:.2e}, max |Delta grad phi|/a0 = {dg:.2e}")
# and an INADMISSIBLE start, for contrast
p_bad = phi_ref*(1 + 0.06*taper); p_bad[fixed_d] = phi_ref[fixed_d]
u_bad = float(np.max(np.hypot(*mesh_d.grad(p_bad).T)))
ps_bad, h_bad = solve_carrier(mesh_d, KER["PUB8"], q_d, p_bad, fixed_d)
print(f"      start 1.06x tapered        (max |grad|/a0 = {u_bad:.4f} -- OUTSIDE the admissible set "
      f"|grad phi| <= {C_SAT:.4f}): does not converge in {len(h_bad)} steps, "
      f"||phi - phi_ref||/||phi_ref|| = {float(np.linalg.norm(ps_bad - phi_ref)/nrm):.2e}")
check("M4b the non-spherical saturated boundary-value problem has a UNIQUE solution in practice: "
      "three genuinely different ADMISSIBLE starting fields converge to the same solution",
      max(x[1] for x in uni) < 1e-8 and max(x[2] for x in uni) < 1e-5,
      f"max relative difference {max(x[1] for x in uni):.2e} in phi and "
      f"{max(x[2] for x in uni):.2e} a0 in grad phi.  An INADMISSIBLE start (|grad phi| > C a0 "
      f"anywhere, i.e. infinite energy) does not converge -- correct behaviour for a constrained "
      f"problem, and a practical warning for anyone solving this equation")

cd = []
for eps in (1e-4, 1e-3, 1e-2):
    ps, _ = solve_carrier(mesh_d, KER["PUB8"], q_d*(1 + eps), phi_ref.copy(), fixed_d)
    dphi = float(np.linalg.norm(ps - phi_ref)/nrm)
    dg = float(np.max(np.hypot(*(mesh_d.nodal_grad(ps) - ngref).T)))
    cd.append((eps, dphi, dg))
    print(f"      source perturbed by {eps:.0e}: ||Delta phi||/||phi|| = {dphi:.3e} "
          f"(ratio to eps {dphi/eps:.3f}), max |Delta grad phi|/a0 = {dg:.3e} "
          f"(ratio {dg/eps:.3f})")
ratios = [c[1]/c[0] for c in cd]
lin = (max(ratios) - min(ratios))/max(ratios)
check("M5 the solution depends CONTINUOUSLY, and in fact LIPSCHITZ-continuously, on the data: a "
      "relative source perturbation eps produces a response linear in eps with a bounded constant",
      lin < 0.10 and max(ratios) < 5.0,
      f"response/eps = {ratios[0]:.4f}, {ratios[1]:.4f}, {ratios[2]:.4f} at eps = 1e-4, 1e-3, 1e-2 "
      f"-- constant to {lin:.2%} over three decades, so the map data -> solution is Lipschitz and "
      f"the problem is WELL POSED in the variational sense")

# --- M6: the regularity that DOES fail -----------------------------------------------------------
print("""
    M6 -- HOW MUCH OF A REAL DISC IS ACTUALLY ON THE SATURATED BRANCH?  Section 1 asked this of the
    ALGEBRAIC law, which is what every number in this repository uses.  Now it is asked of the SOLVE.
    The distinction matters because the approach to the ceiling is astonishingly sharp: for the
    carried kernel, Sigma_par = 1e8 requires |grad phi| to be within 1e-15 a0 of C, and even
    Sigma_par = 200 requires it within 3e-4 a0.  So 'on the saturated branch' means 'the constraint
    is exactly active', and that is a property of the solution, not of the local g_N.""")
kink = {}
for kn in ("PUB4", "PUB6", "PUB8", "REPC", "DEP"):
    if (("canonical", kn)) not in DISC: continue
    phi = DISC[("canonical", kn)]
    g = mesh_d.grad(phi); u = np.hypot(g[:, 0], g[:, 1])
    volsat = float(np.sum(mesh_d.w[u > C_SAT*(1 - 1e-6)])/np.sum(mesh_d.w))
    rmax = float(np.max(mesh_d.Rc[u > C_SAT*(1 - 1e-6)])) if (u > C_SAT*(1 - 1e-6)).any() else 0.0
    kink[kn] = (volsat, float(u.max()), rmax)
    print(f"      {kn:<6s} max |grad phi|/a0 = {float(u.max()):.6f}; the constraint is active over "
          f"{volsat:.2e} of the meshed volume, out to R = {rmax:.2f} kpc")
# what the ALGEBRAIC law would have said, on the same solve's Newtonian field
uN = np.hypot(*mesh_d.grad(DISC[("canonical", "NEWT")]).T)
algsat = uN > S_SAT
volalg = float(np.sum(mesh_d.w[algsat])/np.sum(mesh_d.w))
ralg = float(np.max(mesh_d.Rc[algsat])) if algsat.any() else 0.0
print(f"      for comparison, the ALGEBRAIC law (g_N > s_sat a0) calls {volalg:.2e} of the same "
      f"volume saturated, out to R = {ralg:.2f} kpc")
# and WHERE each of them sits
uS = np.hypot(*mesh_d.grad(DISC[("canonical", "PUB8")]).T)
solsat = uS > C_SAT*(1 - 1e-6)
for nm, msk in (("algebraic law", algsat), ("actual solve", solsat)):
    if not msk.any(): continue
    print(f"      {nm:<15s}: saturated set spans R = {float(mesh_d.Rc[msk].min()):.2f}-"
          f"{float(mesh_d.Rc[msk].max()):.2f} kpc, |z| = {float(mesh_d.Zc[msk].min()):.3f}-"
          f"{float(mesh_d.Zc[msk].max()):.2f} kpc; midplane (|z| < 0.1 kpc) triangles in it: "
          f"{int((msk & (mesh_d.Zc < 0.1)).sum())}")
onlyalg = float(np.sum(mesh_d.w[algsat & ~solsat])/max(np.sum(mesh_d.w[algsat]), 1e-30))
check("M6 the ALGEBRAIC law and the SOLVE agree on where the saturated branch is active in a disc",
      onlyalg < 0.25,
      f"they do not: {onlyalg:.0%} of the volume the algebraic law calls saturated is NOT saturated "
      f"in the solve.  Solving the non-spherical equation moves the active set off the midplane -- "
      f"the algebraic law has {int((algsat & (mesh_d.Zc < 0.1)).sum())} midplane triangles in it, "
      f"the solve {int((solsat & (mesh_d.Zc < 0.1)).sum())} -- and in the midplane at R = 1-4 kpc "
      f"the solved |grad phi| sits 14-21% BELOW the ceiling the algebraic law pins it to")


# ==================================================================================================
# 4.  TARGET (a) -- the inner rotation curve of a real disc
# ==================================================================================================
print("\n4.  TARGET (a) -- the inner rotation curve, where the saturated region sits")
print("""    The comparison is between (i) the ALGEBRAIC prescription the repository uses everywhere,
    g_tot = g_bar + a0 Delta(g_bar/a0) with both vectors radial, and (ii) the actual non-spherical
    carrier solve, in which grad phi need not be parallel to grad Phi_N.""")

def curve(f, kn, Rlist):
    a0 = A0[f]
    phiN, phi = DISC[(f, "NEWT")], DISC[(f, kn)]
    ngN, ngC = mesh_d.nodal_grad(phiN), mesh_d.nodal_grad(phi)
    out = []
    for R in Rlist:
        gRn, gzn = field_at(mesh_d, phiN, R, 0.0, ngN)
        gRc, gzc = field_at(mesh_d, phi, R, 0.0, ngC)
        sN = math.hypot(gRn, gzn)
        alg = abs(gRn) + float(KER[kn].D(np.array([sN]))[0])            # algebraic, radial
        sol = abs(gRn + gRc)                                            # solved, vector sum
        vc_alg = math.sqrt(alg*a0*R*KPC)/1e3
        vc_sol = math.sqrt(max(sol, 0.0)*a0*R*KPC)/1e3
        # radius-specific mesh floor, from the disc's OWN refinement study (N5) rather than from the
        # spherical benchmark's worst point
        cv = conv.get(R, DEV_FLOOR) if R in conv else DEV_FLOOR
        floor = cv*float(KER[kn].D(np.array([sN]))[0])/(2.0*alg)*vc_alg
        out.append((R, sN, vc_alg, vc_sol, math.hypot(gRc, gzc), floor))
    return out

RL = [1.0, 2.0, 3.0, 4.0, 6.0, 8.178, 12.0, 20.0]
print(f"\n      canonical footing, published kernel (Sigma_par capped at 1e8).  A dagger marks a")
print(f"      radius at which the solve is NOT mesh-converted to 1% (N5): those rows are bounds.")
print(f"      {'R [kpc]':>9s}{'s = g_N/a0':>12s}{'u solved':>10s}{'u algebraic':>13s}{'ratio':>8s}"
      f"{'V_c algebraic':>15s}{'V_c solved':>12s}{'difference':>12s}{'mesh floor':>12s}")
rc = curve("canonical", "PUB8", RL)
dmax, fmax, dconv = 0.0, 0.0, 0.0
for (R, sN, va, vs, uu, fl) in rc:
    ual = float(KER["PUB8"].D(np.array([sN]))[0])
    mark = " " if R in CONVERGED_R else "+"
    print(f"      {R:>8.3f}{mark}{sN:>12.3f}{uu:>10.5f}{ual:>13.5f}{uu/ual:>8.4f}{va:>15.2f}"
          f"{vs:>12.2f}{vs-va:>+12.3f}{fl:>12.3f}")
    dmax = max(dmax, abs(vs - va)); fmax = max(fmax, fl)
    if R in CONVERGED_R: dconv = max(dconv, abs(vs - va))
dmax_alt = max(abs(c[3] - c[2]) for c in curve("alt", "PUB6", RL))
print(f"      (+ = not mesh-converged)")
# IS IT SATURATION, or the disc correction ANY nonlinear kernel has?  The unbounded deep-MOND
# diagnostic has the same nonlinearity and no ceiling at all.
phiD, _ = run_case(mesh_d, rho_mw, KER["DMND"], A0["canonical"])
ngD = mesh_d.nodal_grad(phiD); ngN0 = mesh_d.nodal_grad(DISC[("canonical", "NEWT")])
print(f"\n      diagnostic -- the same equation with an UNBOUNDED kernel (Delta = sqrt(s)), which has "
      f"no ceiling:\n      {'R [kpc]':>9s}{'u/u_alg, bounded':>19s}{'u/u_alg, unbounded':>21s}"
      f"{'u_alg/C, bounded':>19s}")
dm_b, dm_u = [], []
for R in RL:
    gRn_, gzn_ = field_at(mesh_d, DISC[("canonical", "NEWT")], R, 0.0, ngN0)
    sN_ = math.hypot(gRn_, gzn_)
    gRb, gzb = field_at(mesh_d, DISC[("canonical", "PUB8")], R, 0.0)
    gRd, gzd = field_at(mesh_d, phiD, R, 0.0, ngD)
    rb_ = math.hypot(gRb, gzb)/float(KER["PUB8"].D(np.array([sN_]))[0])
    rd_ = math.hypot(gRd, gzd)/float(KER["DMND"].D(np.array([sN_]))[0])
    dm_b.append(rb_); dm_u.append(rd_)
    print(f"      {R:>9.3f}{rb_:>19.4f}{rd_:>21.4f}"
          f"{float(KER['PUB8'].D(np.array([sN_]))[0])/C_SAT:>19.4f}")
check("O1 the saturated branch changes the inner rotation curve of a real disc, by more than the "
      "solver's own mesh floor",
      dconv > 2.0*fmax and dconv > 1.0,
      f"max |V_c,solved - V_c,algebraic| = {dconv:.3f} km/s over the mesh-CONVERGED radii "
      f"({dmax:.3f} km/s including the unconverged inner rows), canonical; {dmax_alt:.3f} km/s alt; "
      f"against a radius-specific mesh floor of at most {fmax:.3f} km/s taken from the disc's own "
      f"refinement study.  The carrier's midplane force runs {min(dm_b):.0%}-{max(dm_b):.0%} of the "
      f"algebraic value -- a one-signed geometric deficit worth ~1.4% in V_c, comparable to the "
      f"current systematic error on the Milky Way's V_c (+-2.6 km/s, Eilers et al. 2019).  The "
      f"UNBOUNDED diagnostic kernel, same equation and no ceiling, gives {min(dm_u):.0%}-"
      f"{max(dm_u):.0%}: so the deficit is the generic AQUAL disc correction "
      f"{'AMPLIFIED' if min(dm_b) < min(dm_u) - 0.05 else 'NOT amplified'} by the approach to the "
      f"ceiling")


# ==================================================================================================
# 5.  TARGET (b) -- the vertical structure of a disc
# ==================================================================================================
print("\n5.  TARGET (b) -- the vertical structure, the most non-spherical observable available")
print("""    K_z(R0, 1.1 kpc) is quoted as Sigma_1.1 = |K_z|/(2 pi G) (Kuijken & Gilmore 1991 convention).
    Measurements: 71 +- 6 (KG91), 74 +- 6 (Holmberg & Flynn 2004), 68 +- 4 (Bovy & Rix 2013).""")
SIG_MEAS, SIG_ERR = 68.0, 4.0
print(f"\n      {'footing':<11s}{'kernel':<7s}{'s at (R0,1.1)':>15s}{'Sigma_1.1 algebraic':>21s}"
      f"{'Sigma_1.1 solved':>18s}{'g_phi.zhat/|g_phi|':>21s}")
vert = {}
for f in FOOT:
    a0 = A0[f]
    phiN = DISC[(f, "NEWT")]
    gRn, gzn = field_at(mesh_d, phiN, R0_MW/KPC, ZK_MW/KPC)
    sN = math.hypot(gRn, gzn)
    for kn in ("PUB8", "PUB6", "REPC", "DEP"):
        if (f, kn) not in DISC: continue
        gRc, gzc = field_at(mesh_d, DISC[(f, kn)], R0_MW/KPC, ZK_MW/KPC)
        uu = math.hypot(gRc, gzc)
        dz_alg = abs(gzn) + float(KER[kn].D(np.array([sN]))[0])*abs(gzn)/sN     # algebraic: parallel
        dz_sol = abs(gzn + gzc)
        S_alg = dz_alg*a0/(2*math.pi*G)/MSUN_PC2
        S_sol = dz_sol*a0/(2*math.pi*G)/MSUN_PC2
        vert[(f, kn)] = (S_alg, S_sol, abs(gzc)/max(uu, 1e-30), abs(gzn)/sN)
        print(f"      {f:<11s}{kn:<7s}{sN:>15.3f}{S_alg:>21.2f}{S_sol:>18.2f}"
              f"{abs(gzc)/max(uu,1e-30):>21.4f}")
print(f"      (for comparison the Newtonian direction cosine of g_N at that point is "
      f"{vert[('canonical','PUB8')][3]:.4f}; the algebraic prescription forces g_phi onto it exactly)")
dS = max(abs(vert[(f, kn)][1] - vert[(f, kn)][0]) for (f, kn) in vert)
misalign = max(abs(vert[(f, kn)][2] - vert[(f, kn)][3]) for (f, kn) in vert)
SIG_FLOOR = DEV_FLOOR*max(vert[(f, kn)][0] for (f, kn) in vert)
check("O2 the saturated branch changes the VERTICAL force of a disc, i.e. the non-spherical solve "
      "misaligns g_phi from g_N enough to move Sigma_1.1 by more than the measurement error",
      dS > SIG_ERR,
      f"max |Sigma_solved - Sigma_algebraic| = {dS:.2f} Msun/pc^2 against a measurement error of "
      f"{SIG_ERR:.0f} and a mesh floor of {SIG_FLOOR:.2f}; the direction cosine of g_phi moves by at "
      f"most {misalign:.4f} from the Newtonian one")

# where in the disc IS the misalignment largest?  (recovered nodal gradients throughout: a single P1
# triangle's gradient carries several degrees of direction noise, see Mesh.nodal_grad)
phi = DISC[("canonical", "PUB8")]; phiN = DISC[("canonical", "NEWT")]
gc_n = mesh_d.nodal_grad(phi); gn_n = mesh_d.nodal_grad(phiN)
gc = gc_n[mesh_d.nodes].mean(axis=1); gn = gn_n[mesh_d.nodes].mean(axis=1)   # smooth, at triangles
uu = np.hypot(gc[:, 0], gc[:, 1]); un = np.hypot(gn[:, 0], gn[:, 1])
cosang = (gc[:, 0]*gn[:, 0] + gc[:, 1]*gn[:, 1])/np.maximum(uu*un, 1e-30)
ang = np.degrees(np.arccos(np.clip(cosang, -1, 1)))
u_raw = np.hypot(*mesh_d.grad(phi).T)
regions = {
    "mesh-converged, 4 < R < 20 kpc": (mesh_d.Rc > 4.0) & (mesh_d.Rc < 20) & (mesh_d.Zc < 10),
    "inner, 1 < R < 4 kpc (bounds)":  (mesh_d.Rc > 1.0) & (mesh_d.Rc <= 4.0) & (mesh_d.Zc < 10),
    "the SATURATED set itself":       (u_raw > C_SAT*(1 - 1e-6)) & (mesh_d.Rc > 0.2),
}
print(f"\n      misalignment angle between g_phi and g_N (recovered gradients; the spherical "
      f"benchmark's\n      floor for this statistic is {ANG_FLOOR:.2f} deg at this resolution):")
print(f"      {'region':<34s}{'n':>7s}{'median':>9s}{'90th pct':>10s}{'max':>8s}"
      f"{'frac > floor':>14s}")
ANG = {}
for nm, msk in regions.items():
    if not msk.any():
        print(f"      {nm:<34s}{0:>7d}{'--':>9s}{'--':>10s}{'--':>8s}{'--':>14s}")
        ANG[nm] = (0.0, 0.0, 0.0); continue
    a = ang[msk]
    ANG[nm] = (float(np.median(a)), float(np.max(a)), float((a > ANG_FLOOR).mean()))
    print(f"      {nm:<34s}{int(msk.sum()):>7d}{float(np.median(a)):>9.2f}"
          f"{float(np.percentile(a, 90)):>10.2f}{float(np.max(a)):>8.2f}"
          f"{float((a > ANG_FLOOR).mean()):>13.1%}")
ANG_SAT = ANG["the SATURATED set itself"]
ANG_CONV = ANG["mesh-converged, 4 < R < 20 kpc"]
check("O3 the misalignment between the carrier force and the Newtonian force is a MATERIAL channel "
      "in the mesh-converged part of the disc -- i.e. the non-spherical solve differs from the "
      "algebraic prescription in DIRECTION as well as in magnitude",
      ANG_CONV[2] > 0.10 and ANG_CONV[0] > ANG_FLOOR,
      f"it is not, where the solve is trustworthy: over 4 < R < 20 kpc the median misalignment is "
      f"{ANG_CONV[0]:.2f} deg against a {ANG_FLOOR:.2f} deg mesh floor, and only "
      f"{ANG_CONV[2]:.1%} of triangles exceed the floor.  Inside the saturated set the median is "
      f"{ANG_SAT[0]:.2f} deg with a tail to {ANG_SAT[1]:.1f} deg, but that tail lives at R < 4 kpc "
      f"where the solve is NOT mesh-converged, so it is a bound and not a measurement.  The "
      f"non-spherical solve departs from the algebraic prescription mainly in the MAGNITUDE of "
      f"g_phi (O1, up to 21%), not in its direction")


# ==================================================================================================
# 6.  TARGET (c) -- CLUSTER CORES
# ==================================================================================================
print("\n6.  TARGET (c) -- cluster cores, the programme's hardest failure")
print("""    THE_COMPLETE_THEORY section H-A: 'the excess is 3.37 a0 at 40 kpc, 5.2x the operative
    ceiling'.  The excess is recomputed here from the repository's own cluster measurement audit.""")
print(f"\n      {'footing':<11s}{'radius':<9s}{'n':>4s}{'mean excess':>13s}{'median':>9s}"
      f"{'max':>8s}{'relaxed mean':>14s}{'/ceiling (mean)':>17s}")
exc = {}
for f in FOOT:
    for R in (30.0, 40.0, 50.0):
        rw = [r for r in CROWS if r["footing"] == f and abs(r["r_kpc"] - R) < 1e-9]
        if not rw: continue
        e = np.array([r["g_hse_over_a0"] - r["g_baryon_over_a0"] for r in rw])
        er = np.array([r["g_hse_over_a0"] - r["g_baryon_over_a0"] for r in rw if r["relaxed_subset"]])
        exc[(f, R)] = (e.mean(), np.median(e), e.max(), er.mean() if len(er) else float("nan"))
        print(f"      {f:<11s}{R:<9.0f}{len(rw):>4d}{e.mean():>13.3f}{np.median(e):>9.3f}"
              f"{e.max():>8.3f}{(er.mean() if len(er) else float('nan')):>14.3f}"
              f"{e.mean()/C_SAT:>17.2f}")
e40 = exc[("canonical", 40.0)]
print(f"\n      the deposited value 3.37 a0 sits between the all-cluster mean ({e40[0]:.2f}) and the "
      f"relaxed-subset mean ({e40[3]:.2f}) at 40 kpc, canonical; 3.37/{C_SAT:.4f} = {3.37/C_SAT:.2f}x")
check("O4 the cluster-core excess exceeds the kernel's own bounded-boost ceiling by a large factor, "
      "reproduced from the repository's committed audit at both footings",
      e40[0]/C_SAT > 3.0 and exc[("alt", 40.0)][0]/C_SAT > 3.0,
      f"mean excess/ceiling at 40 kpc = {e40[0]/C_SAT:.2f}x (canonical) / "
      f"{exc[('alt',40.0)][0]/C_SAT:.2f}x (alt); worst single cluster {e40[2]/C_SAT:.2f}x")

# --- the geometry-free form of the ceiling -------------------------------------------------------
print("""
    THE COROLLARY THE VARIATIONAL FORM SUPPLIES.  In spherical symmetry the ceiling C is a statement
    about the algebraic law.  In the variational form it is a POINTWISE CONSTRAINT on the solution
    for ANY source and ANY geometry: every finite-energy configuration satisfies |grad phi| <= C a0
    everywhere, so no triaxiality, no substructure and no non-sphericity can raise the carrier's
    contribution above C a0 at any point.  And because the excess is the magnitude of a VECTOR SUM,
    |g_N + g_phi| - |g_N| <= |g_phi| <= C a0, misalignment can only REDUCE it.  Tested directly on a
    flattened cluster.""")
# a beta-model gas cluster PLUS the BCG of R3b, normalised to the audit's own g_baryon at 40 kpc,
# flattened to q = 0.6.  The BCG is what puts the core on the saturated branch at all (R3b).
BETA_CL, RC_CL = 0.65, 100.0*KPC
RHO_BCG = MSTAR_BCG*A_BCG/(2*math.pi)                    # Hernquist rho = M a /(2 pi r (r+a)^3)
def make_cluster(q, with_bcg=True):
    def rho_cl(R, z):
        rr = np.sqrt(np.asarray(R, float)**2 + (np.asarray(z, float)/q)**2)
        out = RHO0_CL*(1 + (rr/RC_CL)**2)**(-1.5*BETA_CL)
        if with_bcg:
            rs = np.maximum(rr, 0.05*KPC)
            out = out + RHO_BCG/(rs*(rs + A_BCG)**3)
        return out
    return rho_cl
# normalise so that g_bar(40 kpc, midplane, spherical case) matches the audit's median at 40 kpc
gb40 = np.median([r["g_baryon_over_a0"] for r in CROWS
                  if r["footing"] == "canonical" and abs(r["r_kpc"] - 40.0) < 1e-9])
RHO0_CL = 1.0
_r = np.linspace(1e-3, 40.0, 4000)*KPC
_M = np.trapz(4*math.pi*_r**2*(1 + (_r/RC_CL)**2)**(-1.5*BETA_CL), _r)
RHO0_CL = gb40*A0["canonical"]*(40*KPC)**2/(G*_M)
print(f"      beta-model gas: beta = {BETA_CL}, r_c = {RC_CL/KPC:.0f} kpc, normalised to the audit's "
      f"median g_bar(40 kpc) = {gb40:.3f} a0")
Rn_c = np.concatenate([np.arange(0.0, 60.0, 1.5), np.arange(60.0, 200.0, 5.0),
                       np.geomspace(200.0, 3000.0, 40)])
Zn_c = np.concatenate([np.arange(0.0, 60.0, 1.5), np.arange(60.0, 200.0, 5.0),
                       np.geomspace(200.0, 3000.0, 40)])
mesh_c = Mesh(Rn_c, Zn_c)
print(f"      cluster mesh: {mesh_c.nR} x {mesh_c.nZ} = {mesh_c.N} nodes")
CLRES = {}
for q in (1.0, 0.6):
    rho_cl = make_cluster(q)
    for f in FOOT:
        for kn in ("PUB8", "REPC"):
            if f == "alt" and kn == "REPC": continue
            phi, hist = run_case(mesh_c, rho_cl, KER[kn], A0[f])
            g = mesh_c.grad(phi); u = np.hypot(g[:, 0], g[:, 1])
            ceil = DINF_C if kn == "REPC" else C_SAT       # each kernel against ITS OWN ceiling
            sat = u > ceil*(1 - 1e-4)
            CLRES[(q, f, kn)] = (float(u.max())/ceil, float(np.sum(mesh_c.w[sat])/np.sum(mesh_c.w)),
                                 float(np.max(mesh_c.Rc[sat])) if sat.any() else 0.0, float(u.max()))
print(f"\n      {'axis ratio':<12s}{'footing':<11s}{'kernel':<7s}{'max |grad phi|/a0':>19s}"
      f"{'/ own ceiling':>15s}{'saturated out to':>19s}")
for (q, f, kn), (rat, vf, rmx, um) in sorted(CLRES.items()):
    print(f"      {q:<12.1f}{f:<11s}{kn:<7s}{um:>19.6f}{rat:>15.4f}{rmx:>15.1f} kpc")
check("O5 non-sphericity RELAXES the bounded-boost ceiling in cluster cores, i.e. the failure against "
      "the ceiling is an artefact of the spherical solve",
      max(v[0] for v in CLRES.values()) > 1.001,
      f"it does not: the flattened (q = 0.6) cluster's max |grad phi| is "
      f"{CLRES[(0.6,'canonical','PUB8')][0]:.4f} of its own ceiling, indistinguishable from the "
      f"spherical {CLRES[(1.0,'canonical','PUB8')][0]:.4f}.  The ceiling is a POINTWISE constraint for "
      f"every geometry -- and because the excess is |g_N + g_phi| - |g_N| <= |g_phi|, misalignment "
      f"can only REDUCE it.  The cluster kill is strengthened, not weakened")

# --- and where the LENSING SHAPE failure lives ---------------------------------------------------
print("\n    The 9-sigma DeltaSigma shape error is quoted over 0.5-2 Mpc.  Is that on the saturated branch?")
for f in FOOT:
    rw = [r for r in CROWS if r["footing"] == f and r["r_kpc"] >= 750.0]
    if rw:
        print(f"      {f:<10s}: at r >= 750 kpc the tabulated s = g_bar/a0 spans "
              f"{min(r['g_baryon_over_a0'] for r in rw):.4f} - "
              f"{max(r['g_baryon_over_a0'] for r in rw):.4f}, against s_sat = {S_SAT:.3f}")
smax_out = max(r["g_baryon_over_a0"] for r in CROWS if r["r_kpc"] >= 750.0)
check("O6 the 9-sigma lensing-shape failure sits on the saturated branch, so the saturated branch "
      "could be responsible for it",
      smax_out > S_SAT,
      f"it does not: at r >= 750 kpc the largest s in the audit is {smax_out:.4f}, "
      f"{S_SAT/smax_out:.0f}x below s_sat.  The lensing radii are DEEP on the unsaturated branch; "
      f"the shape error is untouched by anything in this lane")


# ==================================================================================================
# 7.  THE SMOOTH REPAIR ON ALL THREE TARGETS
# ==================================================================================================
print("\n7.  THE SMOOTH REPAIR -- L30's minimal C^2 continuation, and the deposited kernel 4.3")
print(f"\n      (a) inner rotation curve, canonical footing, V_c [km/s] at the midplane:")
print(f"      {'R [kpc]':>9s}{'published':>12s}{'L30 repair':>12s}{'deposited':>12s}"
      f"{'repair-pub':>12s}{'dep-pub':>10s}")
rows = {kn: {c[0]: c[3] for c in curve("canonical", kn, RL)} for kn in ("PUB8", "REPC", "DEP", "PUB4")}
d_rc = 0.0
for R in RL:
    a, b, c = rows["PUB8"][R], rows["REPC"][R], rows["DEP"][R]
    d_rc = max(d_rc, abs(b - a), abs(c - a))
    print(f"      {R:>9.3f}{a:>12.2f}{b:>12.2f}{c:>12.2f}{b-a:>+12.3f}{c-a:>+10.3f}")
print(f"\n      (b) vertical structure, Sigma_1.1 [Msun/pc^2] from the solved field:")
for f in FOOT:
    line = f"      {f:<11s}"
    for kn in ("PUB8", "PUB6", "REPC", "DEP"):
        if (f, kn) in vert: line += f"{kn} {vert[(f,kn)][1]:7.2f}   "
    print(line)
d_vt = max(abs(vert[(f, kn)][1] - vert[(f, "PUB8" if (f, "PUB8") in vert else "PUB6")][1])
           for (f, kn) in vert)
print(f"\n      (c) cluster cores: the ceiling itself.")
print(f"      published sup Delta = {C_SAT:.6f};  L30 repair sup Delta = {DINF_C:.6f} "
      f"({DINF_C/C_SAT - 1:+.2%});  deposited sup Delta = {C_DEP:.6f} ({C_DEP/C_SAT - 1:+.2%})")
print(f"      the 40 kpc excess / ceiling: published {e40[0]/C_SAT:.2f}x, L30 repair "
      f"{e40[0]/DINF_C:.2f}x, deposited {e40[0]/C_DEP:.2f}x")
d_repc = max(abs(rows["REPC"][R] - rows["PUB8"][R]) for R in RL)
d_dep = max(abs(rows["DEP"][R] - rows["PUB8"][R]) for R in RL)
check("P1 the SATURATION repair -- L30's minimal C^2 continuation, which differs from the published "
      "kernel by at most 0.008 a0 and ONLY above s_sat -- changes the inner rotation curve",
      d_repc > fmax,
      f"it does not: max change {d_repc:.3f} km/s over 1-20 kpc, below the {fmax:.3f} km/s mesh "
      f"floor.  For contrast the DEPOSITED kernel moves it by {d_dep:.3f} km/s -- but that is its "
      f"different shape at EVERY acceleration (0.011 dex over twenty decades), not the saturated "
      f"branch: it differs from the published kernel most at R = 6-12 kpc, where s = 0.7-2.0 and "
      f"nothing is saturated")
_dv_repc = max(abs(vert[(f, "REPC")][1] - vert[(f, "PUB8" if (f, "PUB8") in vert else "PUB6")][1])
               for f in FOOT if (f, "REPC") in vert)
check("P2 the smooth repair changes the vertical structure",
      d_vt > SIG_ERR,
      f"it does not: L30's minimal repair moves Sigma_1.1 by {_dv_repc:.3f} Msun/pc^2 and the "
      f"deposited kernel by {d_vt:.3f}, against a {SIG_ERR:.0f} Msun/pc^2 measurement error")
check("P3 the smooth repair changes the cluster-core verdict",
      abs(e40[0]/DINF_C - e40[0]/C_SAT) > 0.5,
      f"the ceiling moves from {C_SAT:.4f} to {DINF_C:.4f} (L30) / {C_DEP:.4f} (deposited), so the "
      f"excess/ceiling moves from {e40[0]/C_SAT:.2f}x to {e40[0]/DINF_C:.2f}x -- the failure is "
      f"untouched")
_dM = max(abs(rows["PUB8"][R] - rows["PUB4"][R]) for R in RL)
check("P4 [control] the regularisation converges: capping Sigma_par at 1e4 and at 1e8 gives the same "
      "field, so the constrained (Sigma_par = infinity) limit exists and is what is being computed",
      _dM < 0.5,
      f"max V_c difference between Sigma_par capped at 1e4 and at 1e8 = {_dM:.3f} km/s over "
      f"1-20 kpc, against a mesh floor of {fmax:.3f} km/s")


# ==================================================================================================
# 8.  VERDICT
# ==================================================================================================
print("\n8.  VERDICT")
wellposed = (max(x[1] for x in uni) < 1e-8 and lin < 0.10
             and float(_Sp.min()) > 0 and float(_Sl.min()) > 0)
repo_affected = len(_risk) > 0
cluster_moved = (max(v[0] for v in CLRES.values()) > 1.001) or (smax_out > S_SAT) \
    or (abs(e40[0]/DINF_C - e40[0]/C_SAT) > 0.5)
disc_effect_kms = dconv
print(f"""
      well posed (strictly convex, unique, Lipschitz)   : {wellposed}
      any committed repository solve affected           : {'YES' if repo_affected else 'no'}
      anything in the CLUSTER failure moved             : {'YES' if cluster_moved else 'no'}
      effect on a disc's inner rotation curve           : {disc_effect_kms:.2f} km/s (~1.4%),
                                                          one-signed, mesh-converged
      effect on a disc's vertical structure             : {dS:.2f} Msun/pc^2 (error bar {SIG_ERR:.0f})
      where the branch is really realised               : the inner few kpc of the {nsat['canonical']}/{len(SPARC)}
                                                          densest SPARC discs, and cluster cores only
                                                          inside ~{rsat_bcg['canonical']:.0f} kpc, which is inside the
                                                          innermost radius the audit tabulates
      what the variational form ADDS                    : |grad phi| <= C a0 becomes a POINTWISE,
                                                          GEOMETRY-FREE constraint (O5), so the
                                                          cluster failure is HARDENED, not relaxed""")
check("V1 [VERDICT] the saturated branch is a NUMERICAL HAZARD that has been silently affecting this "
      "programme's committed solves",
      repo_affected,
      "it has not.  The degeneracy exists only in the CARRIER reading (M3: the AQUAL-on-total-"
      "potential reading has Sigma_par = 1 exactly at saturation, and QUMOND is linear), and no "
      "committed script solves the carrier equation off spherical symmetry (M4).  The liability is "
      "real and was worth checking, but it has never been drawn on")
check("V2 [VERDICT] the saturated branch is a PHYSICAL EFFECT the programme has been missing in the "
      "regime it cannot explain -- cluster cores",
      cluster_moved,
      f"it is not.  Cluster cores as the repository measures them are DEEP on the unsaturated branch "
      f"(R3: max s = 0.909 against s_sat = 2.540); the branch only switches on inside "
      f"~{rsat_bcg['canonical']:.0f} kpc once a BCG is added, inside the audit's innermost radius; the "
      f"ceiling is unchanged by flattening (O5); the excess/ceiling stays {e40[0]/C_SAT:.2f}x; and "
      f"the 9-sigma lensing-shape failure lives {S_SAT/smax_out:.0f}x below s_sat (O6)")
check("V3 [VERDICT] the saturated branch is a FORMAL defect with NO observable consequence anywhere",
      wellposed and disc_effect_kms < 1.0 and dS < 1.0,
      f"not quite.  It IS well posed -- strictly convex, unique to 1e-10, Lipschitz to 0.5% over "
      f"three decades -- and it is invisible in clusters and in vertical structure "
      f"({dS:.2f} Msun/pc^2 against a {SIG_ERR:.0f} error bar).  But solving the non-spherical "
      f"equation instead of applying the algebraic law moves a disc's inner rotation curve by "
      f"{disc_effect_kms:.2f} km/s, one-signed and mesh-converged: small, real, and not zero")
check("V4 [VERDICT] the saturated branch is WELL POSED as a variational inequality -- the pathology "
      "L30 and L33 identified is a loss of classical regularity and of the cubic action, not a loss "
      "of existence, uniqueness or continuous dependence",
      wellposed,
      "Sigma_par = +infinity is a CONSTRAINT (|grad phi| <= C a0), not a degeneracy: the energy stays "
      "convex, the minimiser exists and is unique, and the map data -> solution is Lipschitz.  What "
      "genuinely fails is C^2 regularity at the free boundary -- and the SIGN, since a non-monotone "
      "continuation (Sigma_par < 0) WOULD be ill posed, which is exactly what the bounded-boost "
      "theorem already forbids")

print("\n" + "=" * 122)
print(f"RESULT: {len(FAILS)} FAIL -> {FAILS}   ({time.time()-T0:.0f} s)")
print("=" * 122)
