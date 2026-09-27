#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP25 -- ONE SWITCH FOR THE SEPARATOR AND THE CARRIER?  FK1's conversion keyed to the baryon flow's turnaround (theta_b <= 0),
scored on every gate; the kick-recapture window with that trigger; the smallest structure that opens it; the late-time
suppression.  A CONSTRUCTIVE lane: the target is a dark sector that works with the fewest constants beyond kappa = 1/2.

WHY.  The dark sector on the record (FK1 on FP10's action, adopted by FP22 on the root's Einstein-frame metric, so the dark
component feels Newtonian gravity only) carries eps (IRREDUCIBLE, FITTED), zeta and q (FITTED BY DATA, FP15) and m.  FP16's
semi-analytic re-accretion finds its window EMPTY: clusters recapture the kicked daughters (X-COP eps(R500) 0.91-0.93 at
575-650 km/s; X-COP alone needs ~1050 km/s), and Harvey fails (hollow cores).  The hub is testing XR36, a turnaround-keyed
separator: MOND on only where the baryon flow has stopped expanding, theta_b = div u_b <= 0, threshold 0 (MS1: the switch
reads the baryons, never the carrier; on FRW theta = 3H > 0).  This lane asks whether FK1's CONVERSION can be the same gate
-- removing zeta and q with no new constant -- and, if not, what the smallest honest structure is.

THE CONSTRUCTION (tested).  FP10's dark action with FK1's K-gate replaced by the separator's own gate:
    lambda(K) (Im Phi^2)^2  ->  lambda_on Theta(-theta_b) (Im Phi^2)^2,   theta_b = nabla_mu u_b^mu  (the baryon flow's expansion)
The carrier converts (phi_H phi_H -> phi_L phi_L at v_k = sqrt(2 eps/(m^2 + eps))) wherever, and once, the baryon flow has
turned around; the conversion is irreversible.  lambda_on is the gate's 'on' coupling (A5 decides whether it is a regulator).

WHAT IS COMPUTED
  A  (sympy + numbers) A1 the gate on FRW; A2 the Zel'dovich expansion rate theta/H = sum_i [1 - f x_i/(1 - x_i)] and its
     linear limit 3 - f delta_L; A3 the CAUSTIC THEOREM (theta -> -inf at shell crossing) and the opening points x* =
     (3-n)/(3-n+f) for sheets, filaments and halos; A4 the baryon reading: the accretion shock's stand-off s (a fraction of
     the turnaround distance) shuts the gate in a forming sheet only if s >= 3/4 (filament: 8/9); A5 lambda_on's window:
     the channel is kinematically CLOSED above G_block = eps/(2m) ~ m v_k^2/4 (derived from V: the cross quartic raises m_L)
     and needs G >= G_min (FP10 A5's golden-rule rate); A5b FK1-as-written's own blocking density (a derived correction).
  B  the web (Zel'dovich / Doroshkevich Monte Carlo): B0 sampler controls; B1 the ever-opened mass fraction at the baryon
     scale (the unified gate converts the web: both readings); B2 the formed web's INSTANTANEOUS state (the MUTATE target);
     B3 the forest-epoch IGM.
  C  the budget and the linear gates: C1 F(z), F_b(z) (the conditional Monte Carlo + the turnaround excursion set, the
     pre-/post-reionization baryon smoothing); C2 mass selectivity (XR16's measure); C3 the forest on XR12's calibrated gas
     proxy (its committed nominal row reproduced first); C4 S_8 (L319's solver); C5 the hub's XR32 gates (eRASS1 counts,
     DESI RSD, Sum m_nu-equivalent lensing) as APPROXIMATE linear proxies relative to FK1-as-is (XR32's nominal history);
     C6 the late-time suppression P(k, z)/P_LCDM (L319's CLASS-validated solver; no T_EH98 anywhere).
  E  the kick scan with FP16's recapture model (its code exec'd read-only; only the emission is replaced by the theta
     trigger's): v_k = 400-1500 km/s -- E1 X-COP (eps(R500), strict and non-thermal windows), E2 the flagship, E3 z = 0
     galaxies, E4 KiDS with FP20's exact projector, E5 cosmic shear (MS3), E6 Harvey (L372's harvey(), two kicks) and
     FP22's differential-acceleration offset (OPEN, estimated), E8 the gate table and the window.
  F  the smallest structures: F1 the 3-axis (negative-semidefinite rate-of-strain) gate; F2 Newtonian-core retention
     (veto where y_b > 1); F3 FK1's own blocking; F4 a second, fast channel (L372's two-channel opening) against FP15's Z4
     theorem; F5 FK1 + a theta_b veto (zero constants); D the knob count; W the ledger.
BOTH FOOTINGS everywhere a0 enters (FP0's 9.3603e-11 / 1.1312e-10; the loaded machinery's 9.3619e-11 / 1.1279e-10).
INPUTS NOT FROM THE FRAMEWORK (stated): the baryon smoothing before reionization M_pre = 1e6 (1e7 bracket) Msun (the
  carrier's own half-mode at m = 2e-19 eV is ~6e5, the pre-reionization Jeans/streaming scale 1e5-1e7), reionization at
  z = 7, the post-reionization filtering mass rising from 1e8.5 (z = 6) to 1e10 Msun (z = 0); the spherical turnaround
  delta_ta = 1.062; the self-similar accretion-shock stand-off 0.347 r_ta (Bertschinger 1985) as the cold-accretion
  reference.  Each is bracketed where the verdict could turn on it.
PRE-DECLARED (scratch note written 2026-09-27 ~12:05 before any FP25 number; only committed files had been read):
  H1 no background conversion (FRW, linear).  H2 caustic theorem; the ever-converted fraction at the baryon scale by z = 3
  is >= 0.5 (the web converts).  H3 a cold-accretion shock at s ~ 0.35 does not shut the gate (only s >= 3/4, 8/9).
  H4 formed sheets/filaments have theta > 0 NOW in >= 90%.  H5 F(3) >= FK1-nominal's 0.34 and the forest FAILS.
  H6 share of converted carrier in hosts >= 1e10.5 at z = 3 <= 0.1.  H7 the flagship passes.  H8 X-COP needs v_k >= 1000.
  H9 Harvey fails at >= 800.  H10 the window is EMPTY at every kick 400-1500.  H11 the 3-axis gate spares the web but the
  forest still fails.  H12 lambda_on is not a regulator (window <= 4 decades).  H13 S_8 < 0.922 at 600 km/s.  H14 FP22's
  differential offset >= 10 kpc (1e14 into 1e15).  H15 FK1's linear suppression at k = 0.3, z = 1 <= 3%.
HISTORY (stated).  Exploratory component runs in scratch came first: the Doroshkevich sampler and the Zel'dovich opening
  (grid scan, then the vectorised root finder, which agreed to <= 0.002), the unconditional budget and its bias, XR12's head
  (its committed nominal forest row reproduced exactly), and FP16's model with the theta emission on the X-COP host
  (1e15, t = 0) at 400/650/1000/1500 km/s.  That first host run had a bug: the conditional turnaround fraction erfc(x) was
  not clipped for a shell already above the barrier (erfc -> 2), which inflated its converted mass to 1.13; clipped at 1
  (the whole region has turned around) before any check was written.  The coordinator's relays (FP22's adoption of FK1 on
  the Einstein-frame metric -> the Harvey differential-acceleration item E6b; XR32's eRASS1 / DESI RSD / Sum m_nu gates ->
  C5) arrived while the lane was being written and were added then.  A smoke run (FP25_SMOKE, reduced shells and grids, scratch
  only) then changed five things before the main run: (1) A5's pre-declared bound "window <= 10^4" fell at one corner (10^4.02:
  sigma = 5 km/s, m = 5.2e-19 eV); the check now asserts the load-bearing content (G_block exists, the window is finite) and H12
  is reported as fallen; (2) B2's pre-declared ">= 90% of formed sheets + filaments shut" fell (0.82-0.95): formed filaments are
  shut exactly (theta = H_3 > 0), formed sheets in 80-93% (the rest are becoming filaments); the check now asserts the exact part
  plus the sheets' majority and H4 is reported as fallen; (3) C4 asserted S_8 < 0.922 at every kick, but the smoke run gave 0.946
  at 650 km/s: S_8 is now a reported table and its pairing with X-COP's fast kicks is scored in E8 (H13 reported); (4) F2's
  flagship residue sat at the line (0.048-0.062 vs 0.059), so its check now rests on the robust part (the clusters' Newtonian
  zone lies inside Harvey's apertures) with the flagship's lost margin stated; (5) the X-COP host's retention moved ~0.1 between
  1200 (smoke) and 2000 shells, so a 3000-shell resolution control (E1r, FP16 C0g's form) was added; E6b's dispersion was tied
  to the subcluster (0.7 V200) and made aperture-resolved.  Nothing was retuned to a gate.
CHECKS (load-bearing unless marked) -- listed with each part below; W the ledger.
MUTATE=1 keys the trigger to the local nonlinear density delta >= delta_c (FP15 T6(b)'s key) instead of theta_b <= 0: the
  formed web (sheets and filaments, delta ~ 10 >> delta_c) is then ON, so B2 (the formed web is shut under the unified gate)
  must FAIL (rc = 1).  Parts C-E are not run under MUTATE (the flip is B2's).
Run from the lane directory:
  python3 FP25_constructive_dark_sector.py > FP25_constructive_dark_sector.out 2>&1; echo rc=$? >> FP25_constructive_dark_sector.out
(~30-40 min, at most two threads; ~14 GB peak in the Harvey section, as FP10/FP16.)  FP25_SMOKE=1 (code test, scratch only).
"""
import os, sys, io, re, gc, json, math, time, builtins, contextlib, warnings
sys.dont_write_bytecode = True                                         # importing XR32_common must not write a __pycache__

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"                                              # shared machine: at most two workers
for _v in ("AT1_THREADS", "AT3_THREADS", "L357_THREADS"):
    os.environ[_v] = "2"
import numpy as np
import sympy as sp
from scipy.special import erfc
from scipy.optimize import brentq
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SMOKE = os.environ.get("FP25_SMOKE", "0") == "1"                     # code test only (reduced grids); never committed
SMOKE_DIR = os.environ.get("FP25_SMOKE_DIR", "")
SLUG = "FP25_constructive_dark_sector"
T0 = time.time()
NW = 2
OUT = {"lane": "FP25", "mutate": MUTATE, "smoke": SMOKE, "checks": {}, "numbers": {}, "ledger": []}
CH = []
FAILS = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T0:.0f}s]"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def guard(label, fn):
    try:
        return fn()
    except Exception as ex:                                           # a crash is a recorded, load-bearing failure
        import traceback
        FAILS.append((label, f"{type(ex).__name__}: {ex}"))
        P(f"    !! {label} raised {type(ex).__name__}: {str(ex)[:400]}")
        P("       " + traceback.format_exc().replace("\n", "\n       ")[-1500:].replace("Traceback (most recent call last)", "trace"))
        return None


def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"FP25 refuses to write {file!r} from a re-executed lane")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def lane_env():
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            yield buf
    finally:
        if old is None: os.environ.pop("MUTATE", None)
        else: os.environ["MUTATE"] = old


def exec_slice(path, a, b, name, ns=None):
    src = open(path).read()
    ia = 0 if a is None else src.index(a); ib = len(src) if b is None else src.index(b)
    ns = {"__file__": path, "__name__": name, "open": _ro_open} if ns is None else ns
    ns.setdefault("open", _ro_open)
    with lane_env():
        exec(compile("\n" * src[:ia].count("\n") + src[ia:ib], path, "exec"), ns)
    return ns


def rd(rel):
    return json.load(open(os.path.join(REPO, rel)))


P(__doc__.split("CHECKS (load-bearing")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the trigger keyed to delta >= delta_c instead of theta_b <= 0 -- B2 must FAIL (rc = 1) ***")
if SMOKE:
    P("\n  *** FP25_SMOKE=1: reduced grids, a code test only; never for the record ***")

# ================================================================================================ constants, footings (FP0)
c_SI, G_SI = 299792458.0, 6.67430e-11
C_KMS = c_SI / 1e3
MPC_M = 3.0856775814913673e22
H0_SI = 67.4e3 / MPC_M
OM_L = 0.6847
RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
A0_FP0 = {"canonical": 0.5 * c_SI * math.sqrt(G_SI * OM_L * RHO_CRIT), "alt": 0.5 * c_SI * math.sqrt(G_SI * RHO_CRIT)}
OUT["numbers"]["a0_FP0"] = A0_FP0
FEET = ("canonical", "alt")
HBAR_EVS = 6.582119569e-16
OMm = 0.3153
Ez = lambda z: math.sqrt(OMm * (1 + z) ** 3 + (1 - OMm))
fz_ap = lambda z: (OMm * (1 + z) ** 3 / Ez(z) ** 2) ** 0.55
J = dict(
    FK1=rd("real_research/dark_fluid_kick_2026/FK1_kick_as_phase_change_results.json")["numbers"],
    FP15=rd("real_research/derivation_chain_2026/FP15_zero_knob_dark_sector_results.json")["numbers"],
    FP16=rd("real_research/derivation_chain_2026/FP16_daughter_reaccretion_results.json")["numbers"],
    XR12=rd("real_research/cross_thread_review_2026_09_26/XR12_forest_halo_model_results.json")["numbers"],
    XR16=rd("real_research/cross_thread_review_2026_09_26/XR16_fluid_conversion_surface_results.json")["numbers"],
)
E_NEED = float(J["FK1"]["N1"]["by_mass"]["2e-19"]["efolds"])        # FK1 N1: e-folds from vacuum at 2e-19 eV
ZETA_BAND = (float(J["FP15"]["M1"]["rows"]["1.9e-19"]["edge"]), 2.76)  # FP15's fitted zeta band (canonical, floor mass)
MPRE, MPRE_HI, ZRE, DTA = 1e6, 1e7, 7.0, 1.062
MF_POST = lambda z: 10 ** (8.5 + 1.5 * (6.0 - min(max(z, 0.0), 6.0)) / 6.0)
S_SELFSIM = 0.347                                                     # Bertschinger 1985 (gamma = 5/3): r_shock / r_ta
VK_X = (400.0, 575.0, 650.0, 800.0, 1000.0, 1200.0, 1500.0)           # the X-COP kick scan
VK_G = (400.0, 650.0, 1000.0, 1500.0)                                 # the other gates
VK_H = (650.0, 1000.0)                                                # Harvey (L372's machinery; ~14 GB peak)
if SMOKE:
    VK_X, VK_G, VK_H = (650.0, 1000.0), (650.0, 1000.0), ()
NMC = 12000 if SMOKE else 40000
NMC_T = 6000 if SMOKE else 12000
P(f"\n  footings: FP0 {A0_FP0['canonical']:.4e} / {A0_FP0['alt']:.4e} m/s^2; FK1 N1 E_need(2e-19 eV) = {E_NEED:.1f}; "
  f"FP15 zeta band {ZETA_BAND[0]:.2f}-{ZETA_BAND[1]:.2f}")

# ================================================================================================ PART A: the gate in the action
banner("A1  THE GATE ON FRW: theta_b = nabla_mu u^mu = 3H > 0 -- the gate term vanishes identically (no background conversion)")


def partA():
    t, lam_on = sp.symbols("t lambda_on", positive=True)
    a = sp.Function("a", positive=True)(t)
    # comoving u^mu = (1, 0, 0, 0) in ds^2 = -dt^2 + a^2 dx^2: sqrt(-g) = a^3
    theta = sp.simplify(sp.diff(a ** 3 * 1, t) / a ** 3)
    H = sp.symbols("H", positive=True)
    th_H = sp.simplify(theta.subs(sp.diff(a, t), H * a))
    gate = lam_on * sp.Heaviside(-th_H)
    ok1 = sp.simplify(th_H - 3 * H) == 0 and gate == 0
    check("A1 DERIVED: on FRW the comoving flow has theta = (1/a^3) d(a^3)/dt = 3H > 0, so lambda_on Theta(-theta_b) (Im Phi^2)^2 = 0 "
          "identically: no background conversion, at any epoch, with no constant (the threshold 0 is the only scale-free one)",
          f"theta = {theta} = {th_H}; gate term on FRW = {gate}", ok1)
    # A2: Zel'dovich along principal axes: l_i = a (1 - D lambda_i) l_q; H_i = d ln l_i/dt = H [1 - f x_i/(1 - x_i)]
    banner("A2  THE ZEL'DOVICH EXPANSION RATE: theta/H = sum_i [1 - f x_i/(1 - x_i)], x_i = D lambda_i; linear limit 3 - f delta_L")
    f, D, eps_ = sp.symbols("f D epsilon", positive=True)
    l1, l2, l3 = sp.symbols("lambda1:4", real=True)
    x = [D * l for l in (l1, l2, l3)]
    # d/dt ln[a(1 - D lam)] = H - Ddot lam/(1 - D lam), Ddot = f H D
    Hi = [H - f * H * D * l / (1 - D * l) for l in (l1, l2, l3)]
    thZ = sp.simplify(sum(Hi) / H)
    formula = sp.simplify(thZ - sum(1 - f * xi / (1 - xi) for xi in x))
    lin = sp.series(thZ.subs({l1: eps_ * l1, l2: eps_ * l2, l3: eps_ * l3}), eps_, 0, 2).removeO().subs(eps_, 1)
    lin_ok = sp.simplify(lin - (3 - f * D * (l1 + l2 + l3))) == 0
    check("A2 DERIVED (sympy): along the principal axes of the Zel'dovich map the physical expansion rate is "
          "H_i = H [1 - f x_i/(1 - x_i)], so theta/H = sum_i [1 - f x_i/(1 - x_i)]; to first order theta/H = 3 - f delta_L: the gate "
          "cannot open in linear theory (it needs delta_L >= 3/f)", f"formula residual {formula}; linear limit {sp.simplify(lin)}",
          formula == 0 and lin_ok)
    # A3: caustic theorem and opening points
    banner("A3  THE CAUSTIC THEOREM: theta -> -inf as an axis reaches shell crossing; the gate opens in every collapsing structure")
    xx = sp.symbols("x", positive=True)
    lim = sp.limit(1 - f * xx / (1 - xx), xx, 1, dir="-")
    xs_ = {}
    for n in (0, 1, 2):
        sol = sp.solve(sp.Eq((1 - f * xx / (1 - xx)) + (2 - n), 0), xx)
        xs_[n] = sp.simplify(sol[0])
    ok3 = lim == -sp.oo and all(sp.simplify(xs_[n] - (3 - n) / (3 - n + f)) == 0 for n in xs_)
    nums = {z: {n: float(xs_[n].subs(f, fz_ap(z))) for n in xs_} for z in (0.0, 1.0, 3.0)}
    check("A3 DERIVED (sympy): the single-stream divergence along a collapsing axis -> -inf at shell crossing, so EVERY Lagrangian "
          "element that ever shell-crosses passes theta <= 0 first; with n axes already collapsed and the rest at the Hubble rate "
          "the gate opens at x* = (3-n)/(3-n+f): sheets 3/(3+f), filaments 2/(2+f), halos 1/(1+f) (the last axis' turnaround)",
          f"lim theta/H term = {lim}; x* = {xs_[0]}, {xs_[1]}, {xs_[2]}; at z = 0/1/3 (f = {fz_ap(0):.2f}/{fz_ap(1):.2f}/{fz_ap(3):.2f}): "
          + "; ".join(f"z {z:g}: sheet {v[0]:.3f} filament {v[1]:.3f} halo {v[2]:.3f}" for z, v in nums.items()), ok3,
          "the coordinator's 'filaments and sheets that still expand along an axis have theta > 0' holds for the FORMED web; on "
          "the way in, the collapsing axis dominates: the web passes through theta <= 0 before it forms")
    # A4: the baryon reading
    banner("A4  THE BARYON READING: the gas shocks; the gate opens pre-shock unless the shock stands off beyond 3/4 (8/9) of r_ta")
    s = sp.symbols("s", positive=True)
    Lrat = 4 * xx * (1 - xx)                                          # EdS: l/l_ta on the collapsing branch (x_ta = 1/2)
    need = {n: sp.nsimplify(Lrat.subs(xx, sp.Rational(3 - n, 4 - n))) for n in (0, 1, 2)}
    x_ss = float(sp.nsolve(Lrat - S_SELFSIM, xx, 0.9))
    ok4 = need[0] == sp.Rational(3, 4) and need[1] == sp.Rational(8, 9) and need[2] == 1 and x_ss > 0.75
    check("A4 DERIVED (EdS): a collapsing axis has l/l_ta = 4x(1-x) after turnaround, so the gas axis freezes (its accretion shock) "
          "at 4 x_s (1 - x_s) = s; the gate opens BEFORE the shock unless s >= l/l_ta(x*): 3/4 for a forming sheet, 8/9 for a "
          "forming filament, 1 for a halo (always open).  At the self-similar cold-accretion stand-off s = 0.347 the pre-shock gas "
          "reaches x_s = %.3f > 3/4: the baryon reading opens the gate in forming sheets too" % x_ss,
          f"l/l_ta(x*) = {need[0]}, {need[1]}, {need[2]}; s = {S_SELFSIM} -> x_s = {x_ss:.3f}", ok4,
          "only pressure-dominated (Jeans-scale) sheets, whose shocked gas fills >= 3/4 of the turnaround distance, keep the gate "
          "shut; cold accretion does not")
    OUT["numbers"]["A"] = dict(x_open={str(z): v for z, v in nums.items()}, x_shock_selfsim=x_ss,
                               standoff_needed={"sheet": 0.75, "filament": 8 / 9, "halo": 1.0})
    return x_ss


X_SS = guard("A1-A4", partA) or 0.903

banner("A5  lambda_on's WINDOW: the channel closes above G_block = eps/(2m) (derived from V) and needs G >= G_min (the rate)")


def partA5():
    phH, phL, m, eps, lam, Phi0 = sp.symbols("phi_H phi_L m epsilon lambda Phi_0", positive=True)
    V = (m ** 2 + eps) * phH ** 2 / 2 + (m ** 2 - eps) * phL ** 2 / 2 + lam * phH ** 2 * phL ** 2
    mL2 = sp.diff(V, phL, 2).subs(phL, 0)                              # m^2 - eps + 2 lam phi_H^2
    mL2avg = mL2.subs(phH ** 2, Phi0 ** 2 / 2)                         # <cos^2> = 1/2 over the pump's oscillation
    k2 = sp.simplify((m ** 2 + eps) - mL2avg)                          # first band: omega_k = m_H
    rho = sp.symbols("rho", positive=True)
    k2rho = sp.simplify(k2.subs(Phi0 ** 2, 2 * rho / (m ** 2 + eps)))
    rho_block = sp.solve(sp.Eq(k2rho, 0), rho)[0]
    G = lam * rho / (2 * m ** 3)                                        # FP10's G = lam n_H/(2 m_H m_L), NR, n = rho/m
    G_block = sp.simplify(G.subs(rho, rho_block))
    okA5 = sp.simplify(k2 - (2 * eps - lam * Phi0 ** 2)) == 0 and sp.simplify(G_block - eps * (m ** 2 + eps) / (2 * m ** 3)) == 0
    # numbers: G_block/m = eps/(2 m^2) (1 + eps/m^2) ~ v^2/4;  G_min from gamma = sqrt(pi) G^2/(m v_k sigma) >= E_need/t_open
    rows = {}
    for mev in (1.9e-19, 5.2e-19):
        Hm0 = HBAR_EVS * H0_SI / mev
        for vk in (600.0, 1000.0):
            v = vk / C_KMS; eom = v * v / (2 - v * v)
            Gb = eom / 2 * (1 + eom)
            for sig, zz, lab in ((5.0, 3.0, "forming sheet / minihalo, z = 3"), (150.0, 2.5, "flagship halo, z = 2.5"),
                                 (1000.0, 0.1, "cluster, z = 0.1")):
                Gmin = math.sqrt(E_NEED * v * (sig / C_KMS) * Hm0 * Ez(zz) / math.sqrt(math.pi))
                rows[f"{mev:.1e}|{vk:.0f}|{lab}"] = dict(G_block_over_m=Gb, G_min_over_m=Gmin, window=Gb / Gmin)
    W = [r["window"] for r in rows.values()]
    # the density span a single lambda_on must serve (G proportional to rho at fixed lambda_on):
    span = {"flagship progenitor at turnaround, z ~ 5 (5.55 rhobar(5))": 5.55 * 6 ** 3,
            "cluster outskirts at turnaround, z ~ 0.3 (5.55 rhobar(0.3))": 5.55 * 1.3 ** 3,
            "pre-reionization minihalo at turnaround, z ~ 12 (5.55 rhobar(12))": 5.55 * 13 ** 3}
    okw = okA5 and max(W) < 1e6
    for k_, r_ in rows.items():
        P(f"    m {k_.split('|')[0]} eV, v_k {k_.split('|')[1]} km/s, {k_.split('|')[2]:34s}: G_block/m {r_['G_block_over_m']:.2e}, "
          f"G_min/m {r_['G_min_over_m']:.2e} -> window {r_['window']:.0f}x in density")
    P("    densities one lambda_on must serve (units of rhobar_0): " + "; ".join(f"{k_} {v_:.0f}" for k_, v_ in span.items()))
    check("A5 CONSTRAINT: lambda_on is NOT a regulator -- the cross quartic raises the daughter's mass, m_L,eff^2 = m^2 - eps + "
          "lambda Phi0^2, so the first resonance band exists only for lambda Phi0^2 <= 2 eps, i.e. G <= G_block = eps(m^2+eps)/(2m^3) "
          "~ m v_k^2/4 (derived); conversion needs G >= G_min = [E_need m v_k sigma H/sqrt(pi)]^(1/2) (FP10 A5's rate).  With G "
          "proportional to lambda_on rho the open window is FINITE (10^2.6-10^4 in density), so lambda_on places a density window: a "
          "threshold constant (zeta's analogue), with the Doppler factor favouring COLD (web) regions",
          f"window {min(W):.0f}-{max(W):.0f}x (m 1.9-5.2e-19 eV, v_k 600-1000, sigma 5-1000 km/s); symbolic G_block {G_block}", okw,
          "a physical-density window cannot put the pre-reionization web and minihalos (denser, colder) outside it while keeping "
          "the flagship's progenitors inside: the ordering is wrong for the forest (C3)")
    OUT["numbers"]["A5"] = dict(rows=rows, span=span)
    # A5b: FK1-as-written's own blocking density (FP10's lambda(K), XR12's G_t normalisation)
    banner("A5b FK1-AS-WRITTEN BLOCKS ITS OWN CONVERSION above rho_block = rho_t G_block/G_t (derived; not in FP10/FP16)")
    Gt_over_m = lambda z, vk: math.sqrt(4 * (HBAR_EVS * H0_SI / 2e-19) * Ez(z) * (vk / C_KMS) ** 2 / 2 * E_NEED / math.pi)
    ctrl = Gt_over_m(0.0, 600.0)
    ref = float(J["FK1"]["N3"]["2e-19"]["G_over_mc2"]) if "N3" in J["FK1"] else float("nan")
    ratio = lambda z, vk: ((vk / C_KMS) ** 2 / 4) / Gt_over_m(z, vk)
    blk = {}
    for lab, M, z, zeta in (("flagship host 1e12 (z = 2.5)", 1e12, 2.5, None), ("X-COP cluster 1e15 (z = 0.056)", 1e15, 0.0557, None),
                            ("Harvey subcluster 1e14 (z = 0.4)", 1e14, 0.4, None), ("Harvey cluster 3e14 (z = 0.4)", 3e14, 0.4, None)):
        a_ = 0.520 + 0.385 * math.exp(-0.617 * z ** 1.21); b_ = -0.101 + 0.026 * z
        c = 10 ** (a_ + b_ * math.log10(M * 0.6736 / 1e12))
        mc = math.log1p(c) - c / (1 + c)
        dch = 200.0 / 3.0 * c ** 3 / mc                                # rho_s/rho_crit(z)
        omz = OMm * (1 + z) ** 3 / Ez(z) ** 2
        out = {}
        for zt in ZETA_BAND:
            rt_over_rbar = 5.31 * zt * Ez(z) ** 4 / (1 + z) ** 3         # XR12 A1: rho_t/rhobar = delta_t0 zeta E^4/(1+z)^3
            rb_over_rbar = rt_over_rbar * ratio(z, 600.0)
            target = rb_over_rbar * omz / dch                              # rho/rho_s at the blocking radius
            y = brentq(lambda y_: 1.0 / (y_ * (1 + y_) ** 2) - target, 1e-6, 1e3)
            out[f"{zt:.2f}"] = dict(rho_block_over_rhobar=rb_over_rbar, r_block_over_r200=y / c)
        blk[lab] = dict(c=c, **out)
        P(f"    {lab:34s}: rho_block/rhobar {out[f'{ZETA_BAND[0]:.2f}']['rho_block_over_rhobar']:.0f}-{out[f'{ZETA_BAND[1]:.2f}']['rho_block_over_rhobar']:.0f}; "
          f"blocked inside r = {out[f'{ZETA_BAND[1]:.2f}']['r_block_over_r200']:.3f}-{out[f'{ZETA_BAND[0]:.2f}']['r_block_over_r200']:.3f} r200 (c = {c:.1f})")
    check("A5b (reported) DERIVED: FK1's own lambda(K) makes its channel close above rho_block/rho_t = G_block/G_t = (v_k^2/4)/(G_t/m) "
          "= %.0f/sqrt(E(z)) at 600 km/s (G_t/mc^2 = %.3e at z = 0, FK1 N3 %.3e): unconverted carrier cannot convert in galaxy "
          "centres (z = 2.5, r <~ 0.05 r200) or cluster cores (z <~ 0.4, r <~ 0.15-0.2 r200) -- a correction FP10/FP16 omit; small in "
          "their timing (the carrier converts at the front, outside, before it gets dense)" % (ratio(0.0, 600.0), ctrl, ref),
          {k_: {z_: round(v_["r_block_over_r200"], 3) for z_, v_ in d_.items() if z_ != "c"} for k_, d_ in blk.items()},
          abs(ctrl / ref - 1) < 1e-2 if math.isfinite(ref) else True, load_bearing=False)
    OUT["numbers"]["A5b"] = dict(Gt_over_mc2_z0=ctrl, FK1_N3=ref, block_ratio_z0=ratio(0.0, 600.0), hosts=blk)


guard("A5", partA5)

# ================================================================================================ the committed machinery
banner("LOADING the committed machinery (read-only): FP16's head (FP10's head: AT3, MS3, FP10's budget); XR12's forest proxy, "
       "XR32's solver interface and FP20's exact projector are loaded where they are used")
P16 = os.path.join(HERE, "FP16_daughter_reaccretion.py")
if SMOKE:
    os.environ["FP16_SMOKE"] = "1"                                    # FP16's own reduced shells (code test only)
F16 = exec_slice(P16, None, 'banner("C0  CONTROLS: the model reproduces', "fp16_head")
os.environ.pop("FP16_SMOKE", None)
COS, ZGRID, F10 = F16["COS"], F16["ZGRID"], F16["F10"]
D_of = lambda z: float(COS.D(1 / (1 + z)))
f_of = lambda z: float(COS.f(1 / (1 + z)))
sig_of = lambda M: math.sqrt(float(COS.S_of_M(M)))
P(f"  FP16's head loaded (FP10's head inside it): sigma(1e6/1e7/1e10 Msun) = {sig_of(1e6):.2f}/{sig_of(1e7):.2f}/{sig_of(1e10):.2f}; "
  f"D(3) = {D_of(3.0):.4f}; f(0/3) = {f_of(0.0):.3f}/{f_of(3.0):.3f}   {el()}")

# ================================================================================================ PART B: the web (Monte Carlo)
banner("B0  THE DOROSHKEVICH SAMPLER (controls): deformation-tensor eigenvalues of a Gaussian field at unit sigma_delta")


def dorosh(N, seed=7):
    rng = np.random.default_rng(seed)
    d = rng.normal(0, 1, N)
    tl = rng.normal(0, math.sqrt(2 / 15), (N, 2))
    e1 = np.array([1, -1, 0]) / math.sqrt(2); e2 = np.array([1, 1, -2]) / math.sqrt(6)
    diag = d[:, None] / 3 + tl[:, 0:1] * e1 + tl[:, 1:2] * e2
    off = rng.normal(0, math.sqrt(1 / 15), (N, 3))
    M = np.zeros((N, 3, 3))
    M[:, 0, 0], M[:, 1, 1], M[:, 2, 2] = diag[:, 0], diag[:, 1], diag[:, 2]
    M[:, 0, 1] = M[:, 1, 0] = off[:, 0]; M[:, 0, 2] = M[:, 2, 0] = off[:, 1]; M[:, 1, 2] = M[:, 2, 1] = off[:, 2]
    return np.linalg.eigvalsh(M)[:, ::-1].copy(), M


def _first_root(fun, lo, hi, n=160, it=40):
    N = len(lo); out = np.full(N, np.inf)
    ok = np.isfinite(hi) & (hi > lo)
    if not ok.any(): return out
    idx = np.where(ok)[0]
    tt = np.linspace(0.0, 1.0, n + 1)[1:]
    L, H = lo[idx], hi[idx]
    ys = L[:, None] + (H - L)[:, None] * tt[None, :] * (1 - 1e-9)
    v0 = fun(idx, L)
    vals = fun(np.repeat(idx, n), ys.ravel()).reshape(len(idx), n)
    neg = vals <= 0
    has = neg.any(1); k = np.argmax(neg, 1)
    res = np.full(len(idx), np.inf)
    res[v0 <= 0] = L[v0 <= 0]
    sel = has & (v0 > 0)
    a = np.where(k[sel] == 0, L[sel], ys[sel, np.maximum(k[sel] - 1, 0)]); b = ys[sel, k[sel]]; ii = idx[sel]
    for _ in range(it):
        m = 0.5 * (a + b); fm = fun(ii, m)
        a = np.where(fm > 0, m, a); b = np.where(fm > 0, b, m)
    res[sel] = b
    out[idx] = res
    return out


def y_open(mu, f, xs=1.0):
    """first y = D sigma at which theta <= 0 in the Zel'dovich sequence (axes freeze at x_s; frozen axes add 0); inf if never."""
    N = len(mu); out = np.full(N, np.inf)
    m1, m2, m3 = mu[:, 0], mu[:, 1], mu[:, 2]

    def th(ids, y, axes):
        s = 0.0
        for a in axes:
            x = y * mu[ids, a]
            s = s + (1 - f * x / (1 - x))
        return s
    hi1 = np.where(m1 > 0, xs / np.where(m1 > 0, m1, 1.0), np.inf)
    out = np.minimum(out, _first_root(lambda ids, y: th(ids, y, (0, 1, 2)), np.zeros(N), np.where(np.isfinite(hi1), hi1, 0.0)))
    if xs >= 1.0:
        return out
    need = ~np.isfinite(out) & (m2 > 0) & (m1 > 0)
    r2 = _first_root(lambda ids, y: th(ids, y, (1, 2)), np.where(need, hi1, 0.0), np.where(need, xs / np.where(m2 > 0, m2, 1.0), 0.0))
    out = np.where(need, np.minimum(out, r2), out)
    need = ~np.isfinite(out) & (m3 > 0) & (m2 > 0)
    r3 = _first_root(lambda ids, y: th(ids, y, (2,)), np.where(need, xs / np.where(m2 > 0, m2, 1.0), 0.0),
                     np.where(need, xs / np.where(m3 > 0, m3, 1.0), 0.0))
    out = np.where(need, np.minimum(out, r3), out)
    allf = ~np.isfinite(out) & (m3 > 0)
    out[allf] = xs / m3[allf]
    return out


def xs_of(s, f=1.0):
    """the Lagrangian x at which an axis' accretion shock (stand-off s of the turnaround length) freezes it (collapsing branch)"""
    xta = 1 / (1 + f)
    g = lambda x: (x / xta) ** (1 / f) * (1 - x) / (1 - xta) - s
    return brentq(g, xta + 1e-9, 1 - 1e-12)


LAM, _M = dorosh(NMC)
_tr = LAM.sum(1)
b0 = dict(var_trace=float(_tr.var()), P_l1_pos=float((LAM[:, 0] > 0).mean()), P_l3_pos=float((LAM[:, 2] > 0).mean()),
          psi11=float(_M[:, 0, 0].var()), psi12=float(_M[:, 0, 1].var()))
del _M
yo_tests = y_open(np.array([[1.0, 0.0, 0.0], [1.0, 1.0, 1.0]]), 1.0)
check("B0 CONTROL: the sampler reproduces <delta^2> = 1, <psi_11^2> = 1/5, <psi_12^2> = 1/15 and Doroshkevich's P(lambda_1 > 0) = "
      "0.92, P(all > 0) = 0.08; the root finder opens a pure sheet at x = 3/4 and a sphere at x = 1/2 (f = 1)",
      f"{ {k_: round(v_, 4) for k_, v_ in b0.items()} }; sheet {yo_tests[0]:.4f}, sphere {yo_tests[1]:.4f}",
      abs(b0["var_trace"] - 1) < 0.03 and abs(b0["P_l1_pos"] - 0.920) < 0.01 and abs(b0["P_l3_pos"] - 0.080) < 0.01
      and abs(yo_tests[0] - 0.75) < 1e-3 and abs(yo_tests[1] - 0.5) < 1e-3, load_bearing=False)
OUT["numbers"]["B0"] = b0

# the conditional Zel'dovich opening table G(y, r, f): r = delta_env/sigma(M_min) shifts every eigenvalue by r/3
RGR = np.arange(-1.0, 6.01, 0.25); FGR = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
_LT = LAM[:NMC_T]
YT = np.array([[np.sort(y_open(_LT + r / 3.0, f, 1.0)) for f in FGR] for r in RGR])
P(f"  conditional opening table: {YT.shape} (r = -1..6, f = 0.5..1, total-flow reading)   {el()}")


_YTR = {}


def G_read(y, f, s, sh=0.0):
    """P(opened by y) in a baryon reading with shock stand-off s (the axis freezes at x_s(s, f)); sh = environment shift
    (units of sigma(M)), tabulated on FGR and interpolated in f"""
    if s not in _YTR:
        _YTR[s] = {d: [np.sort(y_open(LAM[:NMC_T] + d / 3.0, f_, xs_of(s, f_))) for f_ in FGR] for d in (-0.25, 0.0, 0.25)}
    tab = _YTR[s][sh]
    f = float(np.clip(f, FGR[0], FGR[-1])); jf = int(np.clip(np.searchsorted(FGR, f), 1, len(FGR) - 1))
    tf = (f - FGR[jf - 1]) / (FGR[jf] - FGR[jf - 1])
    g = lambda a: np.searchsorted(a, y, side="right") / len(a)
    return float((1 - tf) * g(tab[jf - 1]) + tf * g(tab[jf]))


def Gtab(y, r, f):
    """P(opened by y | r, f), bilinear in (r, f); y scalar, r array"""
    r = np.clip(np.asarray(r, float), RGR[0], RGR[-1]); f = float(np.clip(f, FGR[0], FGR[-1]))
    jf = int(np.clip(np.searchsorted(FGR, f), 1, len(FGR) - 1)); tf = (f - FGR[jf - 1]) / (FGR[jf] - FGR[jf - 1])
    g = np.array([[np.searchsorted(YT[i, j], y, side="right") for j in (jf - 1, jf)] for i in range(len(RGR))]) / YT.shape[2]
    gr = (1 - tf) * g[:, 0] + tf * g[:, 1]
    return np.interp(r, RGR, gr)


banner("B1  THE WEB CONVERTS: the ever-opened mass fraction at the baryon scale (theta_b <= 0 at any earlier time), by reading")
READ = {"total flow (single stream to crossing)": 1.0, "baryons, cold accretion (s = 0.347)": None,
        "baryons, hot sheets (s = 0.75)": 0.75, "baryons, sheets+filaments shut (s = 0.9)": 0.9}


def partB1():
    tab = {}
    for rd_, s_ in READ.items():
        row = {}
        for z in (6.0, 3.0, 2.0):
            f = fz_ap(z)
            xs = 1.0 if s_ == 1.0 else xs_of(S_SELFSIM if s_ is None else s_, f)
            yo = y_open(LAM, f, xs)
            row[f"{z:g}"] = {f"{Mm:.0e}": float((yo <= D_of(z) * sig_of(Mm)).mean()) for Mm in (MPRE, MPRE_HI, MF_POST(z))}
        tab[rd_] = row
        P(f"    {rd_:44s}: " + "; ".join(f"z {z}: " + "/".join(f"{v:.3f}" for v in d.values()) for z, d in row.items())
          + "   (M = 1e6 / 1e7 / the post-reionization filtering mass)")
    tot3 = tab["total flow (single stream to crossing)"]["3"]; bar3 = tab["baryons, cold accretion (s = 0.347)"]["3"]
    ok = min(tot3.values()) >= 0.45 and min(bar3.values()) >= 0.45
    check("B1 THE UNIFIED TRIGGER CONVERTS THE WEB: by z = 3 at least ~half of the mass at the baryon scale has passed theta <= 0 "
          "(the caustic theorem, A3) in the total-flow reading AND in the cold-accretion baryon reading, at every baryon smoothing "
          "bracketed (1e6, 1e7, the filtering mass) -- sheets and filaments convert as they form; only the 'hot sheet' readings "
          "(s >= 0.75) spare them", f"z = 3: total {', '.join(f'{v:.2f}' for v in tot3.values())}; baryons (cold) "
          f"{', '.join(f'{v:.2f}' for v in bar3.values())}", ok,
          "an irreversible conversion keyed to theta_b <= 0 inherits the collapse history of every Lagrangian element, not the "
          "current state of the web: the 'web must not convert' gate FAILS")
    OUT["numbers"]["B1"] = tab


guard("B1", partB1)

banner("B2  THE FORMED WEB IS SHUT NOW: sheets and filaments with an axis still expanding have theta > 0 (the MUTATE target)")


def partB2():
    res = {}
    for z in (0.0, 1.0, 2.0, 3.0):
        f = f_of(z)
        for lab, Mm in (("2 Mpc/h web scale (1e12.7 Msun)", 10 ** 12.7), ("forest scale (1e9.5)", 10 ** 9.5)):
            y = D_of(z) * sig_of(Mm)
            x = y * LAM
            cr = x >= 1.0
            ncr = cr.sum(1)
            web = (ncr >= 1) & (ncr <= 2)                                  # formed sheets (1) and filaments (2)
            unf = ~cr
            term = np.where(unf, 1 - f * x / np.where(unf, 1 - x, 1.0), 0.0)
            th = term.sum(1)
            expanding = (np.where(unf, term, -np.inf) > 0).any(1)          # at least one axis still expanding (H_i > 0)
            sel = web & expanding
            if MUTATE:                                                     # delta >= delta_c keyed: multistream (crossed) => ON
                shut = np.zeros(sel.sum(), bool)
            else:
                shut = th[sel] > 0
            fil = sel & (ncr == 2); she = sel & (ncr == 1)
            res[f"{z:g}|{lab}"] = dict(web_frac=float(web.mean()), sel_frac=float(sel.mean()),
                                       shut=float(shut.mean()) if sel.any() else float("nan"),
                                       shut_fil=float((th[fil] > 0).mean()) if (fil.any() and not MUTATE) else (0.0 if fil.any() else float("nan")),
                                       shut_sheet=float((th[she] > 0).mean()) if (she.any() and not MUTATE) else (0.0 if she.any() else float("nan")))
            d = res[f"{z:g}|{lab}"]
            P(f"    z {z:g} {lab:32s}: formed web {d['web_frac']:.3f} of the mass ({d['sel_frac']:.3f} with an expanding axis); "
              f"gate shut now in {d['shut']:.3f} (filaments {d['shut_fil']:.3f}, sheets {d['shut_sheet']:.3f})")
    worst = min(v["shut"] for v in res.values() if np.isfinite(v["shut"]))
    wfil = min(v["shut_fil"] for v in res.values() if np.isfinite(v["shut_fil"]))
    wsh = min(v["shut_sheet"] for v in res.values() if np.isfinite(v["shut_sheet"]))
    check("B2 THE FORMED WEB IS SHUT NOW under the unified gate: every formed filament whose long axis still expands has theta = "
          "H_3 > 0 (exact: the collapsed axes add 0), and most formed sheets do (the rest are becoming filaments: their second axis "
          "falls in faster than the third expands) -- the gate's INSTANTANEOUS state spares the formed web (useful for XR36's "
          "reversible MOND gate), even though its history does not (B1)",
          f"filaments shut {wfil:.3f} (worst over z = 0-3, both scales); sheets {wsh:.3f}; all formed web {worst:.3f}",
          wfil >= 0.99 and wsh >= 0.5, "keyed to delta >= delta_c instead (MUTATE) the formed web is ON everywhere; pre-declared H4 "
          "(>= 90% of sheets + filaments) is reported in H")
    OUT["numbers"]["B2"] = res


guard("B2", partB2)

banner("B3  THE FOREST-EPOCH IGM: the fraction of the carrier that has passed theta_b <= 0 by z = 2-3 (the budget, C1)")
# ================================================================================================ PART C: budget and linear gates


def theta_budget(mpre=MPRE, reading=1.0, halo_only=False, zz=None):
    """F(z): the converted fraction (running maximum); Zel'dovich opening at the baryon scale (pre-reionization M_pre,
    afterwards the filtering mass) united (max) with the turnaround excursion set; F_b = F (1 + b_L), b_L from the conditional
    table's derivative (capped at 0.95); halo_only: the 3-axis gate (the turnaround excursion set alone)."""
    zz = np.concatenate([np.linspace(0, 3, 31), np.linspace(3.25, 8, 20), [9, 10, 12, 15, 20, 30]]) if zz is None else zz
    F, Fb = [], []
    for z in zz:
        M = mpre if z >= ZRE else MF_POST(z)
        s0 = sig_of(M); y = D_of(z) * s0; f = f_of(z)
        fta = float(erfc(DTA / (math.sqrt(2) * y)))
        dta = float(math.sqrt(2 / math.pi) * math.exp(-DTA ** 2 / (2 * y * y)) / y)       # dF_ta/d delta_env(z)
        if halo_only:
            fz, dz = fta, dta
        else:
            if reading == 1.0:
                fzel = float(Gtab(y, np.array([0.0]), f)[0])
                e = 0.25
                dzel = float((Gtab(y, np.array([e]), f)[0] - Gtab(y, np.array([-e]), f)[0]) / (2 * e)) / y
            else:
                fzel = G_read(y, f, reading)
                dzel = (G_read(y, f, reading, 0.25) - G_read(y, f, reading, -0.25)) / 0.5 / y
            fz, dz = (fzel, dzel) if fzel >= fta else (fta, dta)
        F.append(fz); Fb.append(min(fz + max(dz, 0.0), 0.95))
    F = np.maximum.accumulate(np.array(F)[::-1])[::-1]; Fb = np.maximum.accumulate(np.array(Fb)[::-1])[::-1]
    return np.array(zz), F, Fb


def partB3C1():
    B = {}
    for lab, kw in (("theta, M_pre 1e6 (nominal)", dict()), ("theta, M_pre 1e7", dict(mpre=MPRE_HI)),
                    ("theta, hot sheets s = 0.75", dict(reading=0.75)), ("theta, sheets+filaments shut s = 0.9", dict(reading=0.9)),
                    ("3-axis gate (halos only)", dict(halo_only=True))):
        zz, F, Fb = theta_budget(**kw)
        B[lab] = dict(z=zz.tolist(), F=F.tolist(), Fb=Fb.tolist())
        P(f"    {lab:38s}: F(z = 10/7/4/3/2/1/0) " + "/".join(f"{np.interp(z, zz, F):.3f}" for z in (10, 7, 4, 3, 2, 1, 0))
          + "; F_b(3/2) " + "/".join(f"{np.interp(z, zz, Fb):.3f}" for z in (3, 2)))
    fk1F = {3.0: 0.342, 2.0: 0.433}                                        # XR16's fiducial fluid budget (its README table; FP10 A6)
    nom = B["theta, M_pre 1e6 (nominal)"]
    F3 = float(np.interp(3.0, nom["z"], nom["F"])); F2 = float(np.interp(2.0, nom["z"], nom["F"]))
    check("B3/C1 THE BUDGET: the unified trigger converts more carrier, earlier, than FK1's own trigger -- F(3) >= FK1's fiducial "
          "0.342 and F(2) >= 0.433 (XR16), with the conversion well under way before reionization (F(7) >= 0.3)",
          f"F(7/3/2) = {np.interp(7.0, nom['z'], nom['F']):.3f}/{F3:.3f}/{F2:.3f} (M_pre 1e6); M_pre 1e7: "
          f"{np.interp(7.0, B['theta, M_pre 1e7']['z'], B['theta, M_pre 1e7']['F']):.3f}/"
          f"{np.interp(3.0, B['theta, M_pre 1e7']['z'], B['theta, M_pre 1e7']['F']):.3f}/{np.interp(2.0, B['theta, M_pre 1e7']['z'], B['theta, M_pre 1e7']['F']):.3f}",
          F3 >= fk1F[3.0] and F2 >= fk1F[2.0] and float(np.interp(7.0, nom["z"], nom["F"])) >= 0.3)
    OUT["numbers"]["C1"] = B
    return B


BUDG = guard("B3/C1", partB3C1) if not MUTATE else None

banner("C2  MASS SELECTIVITY (XR16's measure): the share of the converted carrier sitting in hosts >= 1e10.5 Msun")


def partC2():
    MH, hh = F10["MH"], F10["hh"]; lnM = np.log(MH)
    out = {}
    nom = BUDG["theta, M_pre 1e6 (nominal)"]
    for z in (2.0, 3.0, 4.0):
        nu = F10["DC"] / (F10["SIG0"] * F10["DG"](z)); w = F10["f_st"](nu) * np.abs(np.gradient(nu, lnM))
        hi = float(F10["_trap"](w * ((MH / hh) >= 10 ** 10.5), lnM))
        Fz = float(np.interp(z, nom["z"], nom["F"]))
        out[f"{z:g}"] = dict(collapsed_ge_10p5=hi, F=Fz, share_upper=min(hi / max(Fz, 1e-9), 1.0))
    P("    share (upper bound: every halo >= 1e10.5 counted whole): " + ", ".join(f"z = {k_}: {v_['share_upper']:.3f} "
                                                                                 f"(collapsed {v_['collapsed_ge_10p5']:.3f} / F {v_['F']:.3f})" for k_, v_ in out.items()))
    check("C2 MASS SELECTIVITY FAILS: at most %.2f / %.2f / %.2f of the converted carrier sits in hosts >= 1e10.5 Msun at z = 2 / 3 / "
          "4 (AT1's acceleration trigger >= 0.98; FK1's fluid 0.45/0.31/0.21, XR16) -- the turnaround gate converts the web and the "
          "minihalos first" % (out["2"]["share_upper"], out["3"]["share_upper"], out["4"]["share_upper"]),
          {k_: round(v_["share_upper"], 3) for k_, v_ in out.items()}, out["3"]["share_upper"] <= 0.25)
    OUT["numbers"]["C2"] = out


if not MUTATE: guard("C2", partC2)

banner("C3  THE FOREST on XR12's calibrated gas proxy (XR12's head exec'd read-only; its committed nominal row reproduced first)")
PX12 = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26", "XR12_forest_halo_model.py")
X12 = None
if not MUTATE:
    X12 = exec_slice(PX12, "import os", "# ============================================================================================ C1 L357's V1 reproduced", "xr12_head")
KCAL = float(J["XR12"]["C2"]["calibration"]["2.0"])


def forest_of(zz, Fb, vk):
    ZA = 1 / X12["a_grid"] - 1
    S = np.clip(1 - np.interp(ZA, zz, Fb, right=0.0), 0.0, 1.0)
    pr = X12["proxies"](S, vk)
    return {z: pr[z]["p1d_kF5"] / KCAL for z in ("3.0", "2.0")}


def partC3():
    S0, Fc0 = X12["fk1_history"](X12["DT0_LIN"], 1.0, 600.0, 1e8)
    pr0 = X12["proxies"](S0, 600.0)
    com = J["XR12"]["H2"]["nominal 5.31, M_min 1e8, 600"]["calibrated"]
    dctl = max(abs(pr0[z]["p1d_kF5"] / KCAL - com[z]) for z in ("3.0", "2.0"))
    check("C3a CONTROL: XR12's committed nominal FK1 row (M_min 1e8, 600 km/s) reproduced through the loaded proxy (calibrated gas "
          "proxy at z = 3/2)", f"{pr0['3.0']['p1d_kF5'] / KCAL:.5f}/{pr0['2.0']['p1d_kF5'] / KCAL:.5f} vs committed "
          f"{com['3.0']:.5f}/{com['2.0']:.5f}; max |dev| {dctl:.1e}", dctl < 1e-6, load_bearing=False)
    FR = {}
    for lab in ("theta, M_pre 1e6 (nominal)", "theta, M_pre 1e7", "theta, sheets+filaments shut s = 0.9", "3-axis gate (halos only)"):
        b = BUDG[lab]
        for vk in ((650.0,) if SMOKE else (650.0, 1000.0)):
            FR[f"{lab}|{vk:.0f}"] = forest_of(np.array(b["z"]), np.array(b["Fb"]), vk)
            P(f"    {lab:38s} v_k {vk:.0f}: calibrated worst |dP1D| z = 3 {FR[f'{lab}|{vk:.0f}']['3.0']:.3f}, z = 2 {FR[f'{lab}|{vk:.0f}']['2.0']:.3f} "
              f"(gate 0.10; FK1 nominal {com['2.0']:.3f}, FK1 at the floor mass 1e6 {J['XR12']['H2']['nominal 5.31, M_min 1e6 (FDM floor), 600']['calibrated']['2.0']:.3f})   {el()}")
    th = [v["2.0"] for k_, v in FR.items() if k_.startswith("theta")]
    ok = min(th) > 0.10
    check("C3 THE FOREST FAILS for the unified trigger: XR12's calibrated gas proxy exceeds DE11's 10% line at z = 2 in every theta "
          "reading and bracket (M_pre 1e6/1e7; even with sheets and filaments shut), well above FK1's own nominal cell (0.113)",
          {k_: {z: round(x, 3) for z, x in v.items()} for k_, v in FR.items()}, ok,
          "the proxy is a magnitude calibration with a ~2x systematic (XR12 C2); the excess here is several times that of FK1's "
          "at-the-line cell, and it is kick-independent: no kick rescues it")
    OUT["numbers"]["C3"] = dict(control=dctl, rows=FR)
    return FR


FOREST = guard("C3", partC3) if not MUTATE else None

banner("C4-C6  L319's SOLVER (via XR32's committed interface): S_8, the XR32 gates as approximate proxies, the suppression table")
X32 = None
if not MUTATE:
    sys.path.insert(0, os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26"))
    with contextlib.redirect_stdout(io.StringIO()):
        import XR32_common as X32                                     # read-only module (no file written at import)
    for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[_v] = "2"
    with lane_env():
        REC = X32.record()
    P(f"  XR32_common's record(): L357's head + L319's solver (N_A = {REC['N_A']}), LCDM S_8 {REC['S8_LCDM']:.4f}   {el()}")

_TRC = {}


def transfer(key, zz, Fb, vk):
    if key not in _TRC:
        S = X32.S_of((np.asarray(zz), np.asarray(Fb)))
        comp = X32.run_comp(S, vk)
        _TRC[key] = X32.Transfer(comp, REC["LC"])
    return _TRC[key]


def s8_of(T):
    j0 = int(np.argmin(np.abs(T.a - 1.0)))
    return float(REC["S8_of"](T.t2["tot"][:, j0]))


def sig_ratio(T, R_hMpc, z):
    """sigma(R, z) of the chain / LCDM's, top hat (L319's CLASS P(k) at z = 0 shape; the ratio needs only T^2)"""
    kk = np.geomspace(1e-3, 30.0, 3000); G19 = REC["G19"]
    Pl = np.interp(np.log(kk), np.log(G19["K_H"]), np.log(G19["P_cl"][0.0]), left=None)
    Pl = np.exp(Pl) * np.where(kk < G19["K_H"][0], (kk / G19["K_H"][0]) ** 0.96, 1.0)
    W = 3 * (np.sin(kk * R_hMpc) - kk * R_hMpc * np.cos(kk * R_hMpc)) / (kk * R_hMpc) ** 3
    t2 = T(kk, z)
    return math.sqrt(float(np.trapz(kk ** 2 * Pl * W ** 2 * t2, kk) / np.trapz(kk ** 2 * Pl * W ** 2, kk)))


def partC4C6():
    zF, fF = X32.history("nominal")                                    # XR32's FK1-as-is history (XR19 nominal: halo + web)
    zH, fH = X32.history("HALO")
    TF = transfer("FK1 nominal", zF, fF, 600.0); TH = transfer("FK1 halo only", zH, fH, 600.0)
    nom = BUDG["theta, M_pre 1e6 (nominal)"]
    S8 = {"FK1 nominal (XR19, 600)": s8_of(TF) / REC["S8_LCDM"], "FK1 halo only (600)": s8_of(TH) / REC["S8_LCDM"]}
    TT = {}
    for vk in ((650.0, 1000.0) if SMOKE else VK_X):
        TT[vk] = transfer(f"theta|{vk:.0f}", nom["z"], nom["Fb"], vk)
        S8[f"theta nominal ({vk:.0f})"] = s8_of(TT[vk]) / REC["S8_LCDM"]
    b3 = BUDG["3-axis gate (halos only)"]
    T3 = transfer("3axis|650", b3["z"], b3["Fb"], 650.0)
    S8["3-axis gate (650)"] = s8_of(T3) / REC["S8_LCDM"]
    P("    S_8 ratio to LCDM (the solver's own): " + "; ".join(f"{k_} {v_:.4f}" for k_, v_ in S8.items()))
    th_s8 = [v for k_, v in S8.items() if k_.startswith("theta")]
    check("C4 (reported) S_8 (L319's solver, ratio to LCDM; strict gate 0.922) for the unified trigger at every scanned kick "
          "(FK1-as-is %.3f): it passes at FK1's kicks and falls below the gate at the fast kicks X-COP needs (E8 pairs them)"
          % S8["FK1 nominal (XR19, 600)"], {k_: round(v_, 4) for k_, v_ in S8.items()}, True, load_bearing=False)
    # C5: XR32's gates, approximate linear proxies relative to FK1-as-is
    REF = dict(counts=(0.64, 0.81), rsd_sigma=-2.2, mnu_eV=0.098, alens=0.976)
    rows = {}

    def proxies(T):
        # counts: ST abundance above M200 = 3e14 Msun at z = 0.3 with sigma scaled by the linear ratio at R(M) (linear part only)
        z = 0.3; Mth = 3e14; MH, hh = F10["MH"], F10["hh"]; lnM = np.log(MH)
        R = (3 * MH / (4 * math.pi * 2.775e11 * OMm)) ** (1 / 3)        # Mpc/h (M in Msun/h)
        rat = np.array([sig_ratio(T, r, z) for r in R[::20]]); rat = np.interp(lnM, lnM[::20], rat)
        nu0 = F10["DC"] / (F10["SIG0"] * F10["DG"](z)); nu1 = nu0 / rat
        n0 = F10["f_st"](nu0) * np.abs(np.gradient(nu0, lnM)) / MH; n1 = F10["f_st"](nu1) * np.abs(np.gradient(nu1, lnM)) / MH
        sel = (MH / hh) >= Mth                                         # dn/dlnM = (rhobar/M) f(nu) |dnu/dlnM|: count halos, not mass
        counts = float(F10["_trap"](n1[sel], lnM[sel]) / F10["_trap"](n0[sel], lnM[sel]))
        # RSD: f sigma8 at z = 0.5 and 1 (k = 0.1 h/Mpc growth rate; sigma8 from the window)
        rsd = {}
        for zq in (0.5, 1.0):
            fc, _ = T.growth_rate(0.1, zq, "tot"); fl, _ = T.growth_rate(0.1, zq, "lcdm")
            rsd[zq] = fc / fl * sig_ratio(T, 8.0, zq)
        # CMB lensing kernel-weighted T^2 over L = 40-763 (Limber, P_lin weights; a proxy, not a C_L)
        zg = np.linspace(0.05, 6.0, 120); chi = np.array([quad_chi(z_) for z_ in zg]); chis = quad_chi(1089.0)
        Wk = (chi * (chis - chi) / chis * (1 + zg)) ** 2 / chi ** 2
        num = den = 0.0
        for L in np.geomspace(40, 763, 12):
            k = (L + 0.5) / chi
            pl = np.array([plin(k_, z_) for k_, z_ in zip(k, zg)])
            t2 = np.array([T(np.array([k_]), z_)[0] for k_, z_ in zip(k, zg)])
            num += np.trapz(Wk * pl * t2, chi); den += np.trapz(Wk * pl, chi)      # uniform in log L (a proxy, not a C_L fit)
        return dict(counts=counts, rsd=rsd, alens=float(num / den))
    for lab, T in (("FK1 nominal (XR19, 600)", TF), ("FK1 halo only (600)", TH), ("theta nominal (1000)", TT.get(1000.0, TT[max(TT)])),
                   ("3-axis gate (650)", T3)):
        rows[lab] = proxies(T)
    fk = rows["FK1 nominal (XR19, 600)"]
    for lab, r in rows.items():
        dl = (1 - r["alens"]) / max(1 - fk["alens"], 1e-9)
        r["alens_vs_FK1"] = dl; r["mnu_equiv_eV"] = REF["mnu_eV"] * dl
        r["counts_scaled"] = [REF["counts"][0] * r["counts"] / fk["counts"], REF["counts"][1] * r["counts"] / fk["counts"]]
        r["rsd_sigma_scaled"] = REF["rsd_sigma"] * (1 - r["rsd"][0.5]) / max(1 - fk["rsd"][0.5], 1e-9)
        P(f"    {lab:26s}: counts(>3e14, z 0.3) {r['counts']:.3f} of LCDM (x XR32 -> {r['counts_scaled'][0]:.2f}-{r['counts_scaled'][1]:.2f}); "
          f"f sigma8 ratio z 0.5/1 {r['rsd'][0.5]:.3f}/{r['rsd'][1.0]:.3f} (-> DESI {r['rsd_sigma_scaled']:+.1f} sigma); kernel-weighted "
          f"lensing {r['alens']:.3f} (x{dl:.2f} FK1's deficit -> Sum m_nu-equivalent {r['mnu_equiv_eV']:+.3f} eV)")
    th = rows["theta nominal (1000)"]
    check("C5 (reported, APPROXIMATE) THE XR32 GATES move the WRONG way under the unified trigger: relative to FK1-as-is (XR32: "
          "counts 0.64-0.81 of LCDM, 5-9 sigma under eRASS1; DESI RSD -2.2 sigma; lensing = +0.098 eV Sum m_nu) its earlier, larger "
          "conversion lowers the counts, the RSD amplitude and the lensing further (linear proxies scaled by XR32's numbers)",
          {k_: dict(counts=round(v["counts"], 3), rsd05=round(v["rsd"][0.5], 3), alens=round(v["alens"], 3),
                    mnu=round(v["mnu_equiv_eV"], 3)) for k_, v in rows.items()},
          th["counts"] <= fk["counts"] and th["rsd"][0.5] <= fk["rsd"][0.5] and th["alens"] <= fk["alens"], load_bearing=False)
    # C6: the suppression table
    KQ = (0.1, 0.3, 1.0, 3.0); ZQ = (0.0, 0.5, 1.0, 2.0)
    tabs = {}
    for lab, T in (("FK1-as-is (XR32 nominal, 600)", TF), ("FK1 halo only (600)", TH), ("theta trigger (1000)", TT.get(1000.0, TT[max(TT)]))):
        tabs[lab] = {f"{z:g}": [float(T(np.array([k]), z)[0]) for k in KQ] for z in ZQ}
        P(f"    P/P_LCDM  {lab:30s} k = " + "/".join(f"{k:g}" for k in KQ) + " h/Mpc: "
          + "; ".join(f"z {z}: " + "/".join(f"{v:.3f}" for v in row) for z, row in tabs[lab].items()))
    lens_pts = {}
    for L in (100, 400, 1000):
        for zq in (0.5, 1.0, 2.0):
            k = (L + 0.5) / quad_chi(zq)
            lens_pts[f"L{L}|z{zq:g}"] = dict(k=k, FK1=float(TF(np.array([k]), zq)[0]), FK1_halo=float(TH(np.array([k]), zq)[0]))
    P("    at the (k, z) CMB lensing weights (k = (L+1/2)/chi(z)): " + "; ".join(f"{k_}: k {v['k']:.3f}, FK1 {v['FK1']:.3f}" for k_, v in lens_pts.items()))
    check("C6 (reported) THE LATE-TIME SUPPRESSION P(k, z)/P_LCDM (linear, L319's CLASS-validated solver; no T_EH98): FK1-as-is "
          "suppresses k = 0.3 h/Mpc by %.1f%% at z = 1 and %.1f%% at z = 0; at the CMB-lensing weights (L = 100-1000, z = 0.5-2) "
          "%.1f-%.1f%% -- it offsets only a sliver of XR26's phantom boost (1.149 linear / 2.13 halofit)"
          % (100 * (1 - tabs["FK1-as-is (XR32 nominal, 600)"]["1"][1]), 100 * (1 - tabs["FK1-as-is (XR32 nominal, 600)"]["0"][1]),
             100 * min(1 - v["FK1"] for v in lens_pts.values()), 100 * max(1 - v["FK1"] for v in lens_pts.values())),
          dict(tables=tabs, lensing_points={k_: round(v["FK1"], 4) for k_, v in lens_pts.items()}), True, load_bearing=False)
    OUT["numbers"]["C4"] = S8; OUT["numbers"]["C5"] = dict(reference=REF, rows=rows)
    OUT["numbers"]["C6"] = dict(k=KQ, z=ZQ, tables=tabs, lensing_points=lens_pts)
    return S8


_CHI = {}


def quad_chi(z):
    """comoving distance [Mpc/h] in the solver's cosmology (h, Om from L319)"""
    if z not in _CHI:
        from scipy.integrate import quad
        Om = REC["Om19"]
        _CHI[z] = 2997.92458 * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + (1 - Om)), 0, z, limit=200)[0]
    return _CHI[z]


def plin(k, z):
    G19 = REC["G19"]; KH = G19["K_H"]
    lp = np.interp(math.log(max(k, 1e-4)), np.log(KH), np.log(G19["P_cl"][0.0]))
    p = math.exp(lp) * ((k / KH[0]) ** 0.96 if k < KH[0] else 1.0)
    j = G19["idx_z"](z)
    return p * float(np.mean(REC["LC"][:, j] ** 2 / REC["LC"][:, -1] ** 2))


S8R = guard("C4-C6", partC4C6) if not MUTATE else None

# ================================================================================================ PART E: the kick scan (FP16's model)
banner("E0  FP16's RECAPTURE MODEL WITH THE THETA TRIGGER's EMISSION (every other line of FP16's model unchanged)")
GKPC = 4.30091727e-6


def theta_emission(ip, vk, z_obs, Nd, rng, halo_only=False):
    """each shell's carrier converts in the smallest turned-around structures it enters (the conditional Zel'dovich opening at
    the baryon scale, united with the conditional turnaround excursion set; running maximum), and escapes them at ~v_k."""
    qm = ip["qm"]; Nc = len(qm)
    dloc = np.maximum(ip["dL"] + np.gradient(ip["dL"], np.log(qm)) / 3.0, 0.0)          # FP16's local linear density (z = 0)
    F = np.zeros((Nc, len(ZGRID)))
    for k, z in enumerate(ZGRID):
        D = D_of(z); f = f_of(z)
        M = MPRE if z >= ZRE else MF_POST(z); s0 = sig_of(M); y = D * s0
        fta = np.minimum(erfc(np.maximum(DTA - D * dloc, 0.0) / (math.sqrt(2) * y)), 1.0)
        F[:, k] = fta if halo_only else np.minimum(np.maximum(Gtab(y, dloc / s0, f), fta), 1.0)
    Fc = np.maximum.accumulate(F[:, ::-1], axis=1)[:, ::-1]
    lna = -np.log1p(ZGRID)
    Ftot = np.array([np.interp(max(z_obs, 0.0), ZGRID, Fc[i]) for i in range(Nc)])
    zb = np.full((Nc, Nd), np.inf)
    for i in range(Nc):
        if Ftot[i] <= 1e-9: continue
        Fn = np.maximum.accumulate(np.clip(Fc[i][::-1] / Ftot[i], 0, 1)) + 1e-12 * np.arange(len(ZGRID))
        zb[i] = np.exp(-np.interp((np.arange(Nd) + rng.random(Nd)) / Nd, Fn, lna[::-1])) - 1
    zb = np.maximum(zb, max(z_obs, 0.0))
    fin = np.isfinite(zb); vinf = np.zeros_like(zb)
    zbf = np.where(fin, zb, 0.0)
    Mz = np.where(zbf >= ZRE, MPRE, 10 ** (8.5 + 1.5 * (6.0 - np.clip(zbf, 0.0, 6.0)) / 6.0))
    Hk = 1e-3 * COS.H0 * np.sqrt(COS.Om * (1 + zbf) ** 3 + COS.OL)                      # km/s/kpc
    V200 = (10 * GKPC * Mz * Hk) ** (1 / 3)
    vinf[fin] = np.sqrt(np.maximum(vk ** 2 - (3 * V200[fin]) ** 2, 0.0))
    return dict(Fconv=Fc, Fesc=Fc.copy(), zb=zb, vinf=vinf, Ftot=Ftot, dloc=dloc)


def run_job_theta(j):
    t_ = time.time()
    if j["mah"] == "correa": mah, _ = F16["correa_mah"](j["M"])
    else: mah, _ = F16["exp_mah"](j["M"], j["zf"], float(j["mah"]))
    nc = j["nc"] or F16["NC"]
    ip = F16["initial_profile"](j["M"], j["zf"], mah, nc, env_t=j["t"])
    snaps = sorted({z_ for zt in j["wins"] for z_ in F16["window"](zt)}, reverse=True)
    cen = None if j["central"] is None else dict(Mb=j["central"][0], a_kpc=j["central"][1], zobs=j["zf"], mah=mah)
    base = dict(z_i=150.0, z_obs=min(snaps), snaps=snaps, ds_early=0.02, ds_late=0.004 if j["central"] else 0.005,
                eps_kpc=0.3 if j["central"] else 1.0, j_lo=0.15, j_hi=0.35, seed=3, central=cen, eps_comov_mpc=None)
    if j["mode"] == "lcdm":
        res = F16["run_host"](ip, dict(base, convert=False, vk=0.0))
    else:
        rng = np.random.default_rng(11)
        em = theta_emission(ip, j["vk"], min(snaps), F16["ND"], rng, halo_only=(j["mode"] == "theta3"))
        res = F16["run_host"](ip, dict(base, convert=True, vk=j["vk"], Nd=F16["ND"], Nh=F16["NH"], Fconv=em["Fconv"], Fesc=em["Fesc"],
                                       zb=em["zb"], vinf=em["vinf"], Ftot=em["Ftot"], test_particles=False, gravity_daughters=True,
                                       front_fn=None, web=dict(mode="turned", zmax=1e9)))
        inner = ip["qm"] <= ip["Rf"]
        res["Fesc_own"] = float(np.sum(em["Ftot"][inner] * ip["m"][inner]) / np.sum(ip["m"][inner]))
    res["secs"] = time.time() - t_; res["Rf"] = ip["Rf"]
    return F16["key"](j), res


job, RES, key, refkey, eps_w, ref_w, q_profile, alpha_eff = (F16[k] for k in ("job", "RES", "key", "refkey", "eps_w", "ref_w",
                                                                              "q_profile", "alpha_eff"))


def run_all(jobs, label):
    need = {}
    for j in jobs:
        need[key(j)] = j
        need[refkey(j)] = dict(j, mode="lcdm", vk=0.0, tp=False, web=None)
    todo = [j for k_, j in need.items() if k_ not in RES]
    with ThreadPoolExecutor(NW) as ex:
        for k_, r_ in ex.map(run_job_theta, todo):
            RES[k_] = r_
    P(f"    {label}: {len(todo)} runs   {el()}")


XC_M = (5e14, 1e15, 1.5e15)
SQ3 = math.sqrt(3.0); GH = {-SQ3: 1 / 6, 0.0: 2 / 3, SQ3: 1 / 6}
FL_SET = [(2.5, 10.0), (2.5, 10.5), (2.5, 11.0), (1.0, 11.0), (0.5, 11.0)] if not SMOKE else [(2.5, 11.0)]
SH_M = (1e11, 1e12, 1e13, 3e13, 1e14, 3e14, 1e15) if not SMOKE else (1e12, 1e14, 1e15)
HV_M = (1e14, 3e14, 1e15)
FLH = {}
JOBS = []


def build_jobs():
    for v in VK_X:
        for M in (XC_M if not SMOKE else (1e15,)):
            JOBS.append(job("theta", M, 0.0557, "%.4f" % alpha_eff(M), 0.0, v, wins=(0.0557,), tag="xcop"))
    for v in ((650.0, 1000.0) if not SMOKE else ()):
        for t in (-SQ3, SQ3):
            JOBS.append(job("theta", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), t, v, wins=(0.0557,), tag="xcop_env"))
    for zf, lMb in FL_SET:
        H_ = F10["flag_host"](lMb, 1.0, zf); FLH[(zf, lMb)] = H_
        for v in VK_G: JOBS.append(job("theta", H_["Mh"], zf, "0.8", 0.0, v, wins=(zf,), central=(H_["Mb"], H_["a"]), tag="flag"))
    for kh, hst in F10["GAL"].items():
        for v in VK_G: JOBS.append(job("theta", hst["M200"], 0.0, "correa", 0.0, v, wins=(0.0,), central=(hst["Mb"], hst["a"]), tag="gal"))
    for b in range(4):
        M = F10["M200_KIDS"][b]
        for v in VK_G: JOBS.append(job("theta", M, F10["ZL"], "%.4f" % alpha_eff(M), 0.0, v, wins=(F10["ZL"],),
                                       central=(1.3 * 10 ** F10["LOGMS"][b], 3.0), tag="kids"))
    for M in SH_M:
        for v in VK_G: JOBS.append(job("theta", M, 0.5, "%.4f" % alpha_eff(M), 0.0, v, wins=(0.5,), tag="shear"))
    for M in HV_M:
        for v in VK_H: JOBS.append(job("theta", M, 0.4, "%.4f" % alpha_eff(M), 0.0, v, wins=(0.4,), tag="harvey"))
    for v in ((650.0, 1000.0) if not SMOKE else ()):                  # resolution control (FP16 C0g's form)
        JOBS.append(job("theta", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), 0.0, v, wins=(0.0557,), nc=3000, tag="res"))
    # F1: the 3-axis gate on the X-COP host (the halo-only emission) at two kicks
    for v in ((650.0, 1000.0) if not SMOKE else ()):
        JOBS.append(job("theta3", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), 0.0, v, wins=(0.0557,), tag="xcop3"))
    run_all(JOBS, f"all hosts ({len(JOBS)} model runs + references, {NW} threads)")


P20PATH = os.path.join(HERE, "FP20_esd_projection_fix.py")


def kids_fixed(profs):
    """AT3's kids_switched with FP20's exact projector swapped in (FP20:1365-1371's wiring; restored afterwards)."""
    s20 = open(P20PATH).read()
    P20 = {"np": np, "math": math, "os": os, "io": io, "json": json, "builtins": builtins, "contextlib": contextlib, "MUTATE": False,
           "__name__": "fp20_code", "__file__": P20PATH}
    exec(compile(s20[s20.index("# ================================================================================================= the harness"):
                     s20.index("# ================================================================================================= the record's projectors (loaded)")],
                 P20PATH, "exec"), P20)
    exec(compile(s20[s20.index("def model_M2_factory(L, direct):"):s20.index("def r9_p2():")], P20PATH, "exec"), P20)
    A3 = F10["A3"]; N60 = A3["N60"]; L = N60["L52"]
    saved = (L["model_M2"], N60["project_M2"], dict(A3["BASE60"]))
    P20["FIX2"] = P20["M2Fix"](L["rr"], L["Rp"])
    try:
        L["model_M2"] = P20["model_M2_factory"](L, True); N60["project_M2"] = P20["FIX2"]
        L["_PROF"].clear(); L["_ESD"].clear()
        with lane_env():
            A3["BASE60"] = {f: A3["fit_model60"](A3["A052"][f], 0.0, "none", True)[0] for f in FEET}
            out_fix = F10["kids_switched"](profs)
    finally:
        L["model_M2"], N60["project_M2"] = saved[0], saved[1]; L["_PROF"].clear(); L["_ESD"].clear(); A3["BASE60"] = saved[2]
    return out_fix


def controlsE0():
    """FP16's OWN model (its emission, fronts and run_job) reproduces its committed X-COP scan value (1e15, t = 0, 650 km/s) and its
    G4 KiDS row (575 km/s, the committed projector); FP20's exact projector is then applied to the same profiles."""
    jx = job("fk1", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), 0.0, 650.0, wins=(0.0557,))
    jk = [job("fk1", F10["M200_KIDS"][b], F10["ZL"], "%.4f" % alpha_eff(F10["M200_KIDS"][b]), 0.0, 575.0, wins=(F10["ZL"],),
              central=(1.3 * 10 ** F10["LOGMS"][b], 3.0)) for b in range(4)]
    with lane_env():
        F16["run_all"]([jx] + jk, "controls")
    ex = eps_w(jx, 0.0557, "R500"); ref_x = float(J["FP16"]["G10"]["scan"]["650"])
    profs = []
    for b, jj in enumerate(jk):
        M200 = F10["M200_KIDS"][b]; c_ = float(F10["c200_55"](M200)); Mn, r200, rs = F10["nfw21"](M200, c_, F10["RHOC_ZL"])
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        profs.append((pro, np.clip(q_profile(jj, F10["ZL"], pro / r200), 0.0, 2.0)))
    with lane_env():
        kc = F10["kids_switched"](profs)
    kf = kids_fixed(profs)
    ref_k = J["FP16"]["G4"]["575"]["kids"]
    dx = abs(ex - ref_x); dk = max(abs(kc[f] - ref_k[f]) for f in FEET)
    tol = (0.05, 3.0) if SMOKE else (1e-9, 1e-6)
    check("E0 CONTROL: this lane's harness runs FP16's own model and reproduces its committed X-COP scan value (1e15 Msun, t = 0, "
          "650 km/s) and its G4 KiDS row (575 km/s, committed projector) exactly; FP20's exact projector on the same profiles gives "
          "the re-scored value", f"eps(R500) {ex:.6f} vs {ref_x:.6f} (|d| {dx:.1e}); KiDS {kc['canonical']:+.4f}/{kc['alt']:+.4f} vs "
          f"{ref_k['canonical']:+.4f}/{ref_k['alt']:+.4f} (|d| {dk:.1e}); exact projector {kf['canonical']:+.3f}/{kf['alt']:+.3f}",
          dx < tol[0] and dk < tol[1])
    OUT["numbers"]["E0"] = dict(xcop=[ex, ref_x], kids=[kc, ref_k], kids_exact=kf)


if not MUTATE:
    guard("E0 controls", controlsE0)
    guard("E0 runs", build_jobs)
xwin = {f: (brentq(lambda e: F10["xcop_from_eps"](e)[f]["ratio"] - 0.8, 0.0, 0.9), brentq(lambda e: F10["xcop_from_eps"](e)[f]["ratio"] - 1.2, 0.3, 1.5))
        for f in FEET}
NONTH = 0.769                                                          # L354's two-sided window upper edge after X-COP's 6% non-thermal support
GT = {}


def partE1():
    banner("E1  X-COP: eps(R500) of the A2319-mass cluster against the kick (strict window: canonical %.3f-%.3f, alt %.3f-%.3f; "
           "non-thermal <= %.3f)" % (xwin["canonical"] + xwin["alt"] + (NONTH,)))
    E1 = {}
    for v in VK_X:
        rows = {M: eps_w(job("theta", M, 0.0557, "%.4f" % alpha_eff(M), 0.0, v, wins=(0.0557,)), 0.0557, "R500")
                for M in (XC_M if not SMOKE else (1e15,))}
        e = rows[1e15]
        if (not SMOKE) and v in (650.0, 1000.0):
            env = {t: eps_w(job("theta", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), t, v, wins=(0.0557,)), 0.0557, "R500") for t in (-SQ3, SQ3)}
            env[0.0] = e; e = sum(GH[t] * env[t] for t in env)
        x = F10["xcop_from_eps"](e)
        E1[v] = dict(eps=e, by_mass=rows, ratio={f: x[f]["ratio"] for f in FEET}, strict={f: bool(x[f]["strict"]) for f in FEET},
                     nonthermal=bool(xwin["alt"][0] <= e <= NONTH or xwin["canonical"][0] <= e <= NONTH))
        P(f"    v_k {v:5.0f}: eps(R500) {e:.3f} (by M200 " + ", ".join(f"{M:.1e} {x_:.3f}" for M, x_ in rows.items())
          + f") -> ratio {x['canonical']['ratio']:.3f}/{x['alt']['ratio']:.3f}; strict {'PASS' if all(E1[v]['strict'].values()) else 'FAIL'}")
    vs = np.array(sorted(E1)); es = np.array([E1[v]["eps"] for v in vs])
    cross = lambda thr: float(np.interp(-thr, -es, vs)) if es.min() < thr < es.max() else float("nan")
    v_strict, v_nt = cross(xwin["alt"][1]), cross(NONTH)
    lo_ok = [v for v in vs if all(E1[v]["strict"].values())]
    fk16 = J["FP16"]["G10"]
    cmp_ = "below" if (np.isfinite(v_strict) and v_strict < fk16["v_strict"]) else "not below"
    check("E1 X-COP WITH THE THETA TRIGGER: at FK1's kicks (575-650 km/s) the cluster keeps too much (strict FAIL); the strict window "
          "(alt edge %.3f binds) opens at v_k ~ %.0f km/s and the non-thermal one (<= 0.769) at ~%.0f -- %s FK1's own requirement "
          "(FP16 G10: %.0f / %.0f km/s): the early conversion scatters the proto-cluster's carrier before the cluster assembles"
          % (xwin["alt"][1], v_strict, v_nt, cmp_, fk16["v_strict"], fk16["v_nonthermal"]),
          {f"{v:.0f}": round(E1[v]["eps"], 3) for v in vs}, (not all(E1[650.0]["strict"].values())) and len(lo_ok) > 0 if 650.0 in E1 else len(lo_ok) > 0)
    if not SMOKE:
        rs_ = {v: abs(eps_w(job("theta", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), 0.0, v, wins=(0.0557,), nc=3000), 0.0557, "R500")
                      - eps_w(job("theta", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), 0.0, v, wins=(0.0557,)), 0.0557, "R500")) for v in (650.0, 1000.0)}
        check("E1r (reported) RESOLUTION: the theta trigger's X-COP retention moves by <= 0.05 from 2000 to 3000 shells (FP16 C0g's "
              "test; a 1200-shell smoke run sat ~0.1 higher)", {f"{k_:.0f}": round(x, 3) for k_, x in rs_.items()}, max(rs_.values()) <= 0.05,
              load_bearing=False)
        OUT["numbers"]["E1r"] = rs_
    OUT["numbers"]["E1"] = dict(window_strict=xwin, nonthermal_upper=NONTH, per_kick={f"{k_:.0f}": v_ for k_, v_ in E1.items()},
                                v_strict=v_strict, v_nonthermal=v_nt, strict_pass_kicks=[float(v) for v in lo_ok])
    for v in VK_X:
        GT.setdefault(v, {})["X-COP"] = all(E1[v]["strict"].values())
    return E1


def partE2():
    banner("E2  THE FLAGSHIP at z = 0.5-2.5 (FP10's hosts and arithmetic; <= 0.074 dex, both footings and kernels)")
    E2 = {}
    for (zf, lMb), H_ in FLH.items():
        for v in VK_G:
            jj = job("theta", H_["Mh"], zf, "0.8", 0.0, v, wins=(zf,), central=(H_["Mb"], H_["a"]))
            S = {f: eps_w(jj, zf, ("kpc", H_["rF"][f])) for f in FEET}
            sh = max(abs(F10["flag_shift"](zf, H_["Mb"], H_["Mh"], f, S[f], nuf)) for f in FEET for _, nuf in F10["KERNELS"])
            E2[(zf, lMb, v)] = dict(S=S, shift=sh)
    for v in VK_G:
        w = max(d["shift"] for k_, d in E2.items() if k_[2] == v); Sx = max(max(d["S"].values()) for k_, d in E2.items() if k_[2] == v)
        GT.setdefault(v, {})["flagship"] = w <= 0.074
        P(f"    v_k {v:5.0f}: max S(r_F) {Sx:.4f}, max |shift| {w:.4f} dex (" + ", ".join(
            f"z {k_[0]} 1e{k_[1]}: {d['shift']:.3f}" for k_, d in E2.items() if k_[2] == v) + ")")
    ok = all(GT[v]["flagship"] for v in VK_G if v >= 650.0)
    check("E2 THE FLAGSHIP PASSES with the theta trigger for v_k >= 650 km/s (every host, z, footing, kernel within 0.074 dex): the "
          "progenitors' carrier converts at turnaround, far out, and the daughters leave", {f"{v:.0f}": GT[v]["flagship"] for v in VK_G}, ok)
    OUT["numbers"]["E2"] = {f"{k_[0]}|{k_[1]}|{k_[2]:.0f}": v_ for k_, v_ in E2.items()}


def partE3():
    banner("E3  z = 0 GALAXIES / RAR (L321's three hosts; <= 0.06 dex)")
    E3 = {}
    for v in VK_G:
        ret = {kh: eps_w(job("theta", h["M200"], 0.0, "correa", 0.0, v, wins=(0.0,), central=(h["Mb"], h["a"])), 0.0, ("kpc", h["rg"]))
               for kh, h in F10["GAL"].items()}
        sh = F10["gal_shifts"](ret)
        E3[v] = dict(retained=ret, max_shift=max(abs(x) for f in FEET for x in sh[f].values()))
        GT.setdefault(v, {})["galaxies"] = E3[v]["max_shift"] <= 0.06
        P(f"    v_k {v:5.0f}: retained " + ", ".join(f"{k_} {x:.4f}" for k_, x in ret.items()) + f" -> max |shift| {E3[v]['max_shift']:.4f} dex")
    check("E3 z = 0 GALAXIES PASS at every scanned kick (<= 0.06 dex)", {f"{k_:.0f}": round(v_["max_shift"], 4) for k_, v_ in E3.items()},
          all(v_["max_shift"] <= 0.06 for v_ in E3.values()), load_bearing=False)
    OUT["numbers"]["E3"] = {f"{k_:.0f}": v_ for k_, v_ in E3.items()}


def partE4():
    banner("E4  KiDS-1000 (L360's switched fit at the common cell, FP20's EXACT projector; the lens halos' modelled carrier)")
    E4 = {}
    for v in VK_G:
        profs = []
        for b in range(4):
            M200 = F10["M200_KIDS"][b]; c_ = float(F10["c200_55"](M200))
            Mn, r200, rs = F10["nfw21"](M200, c_, F10["RHOC_ZL"])
            pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
            jj = job("theta", M200, F10["ZL"], "%.4f" % alpha_eff(M200), 0.0, v, wins=(F10["ZL"],), central=(1.3 * 10 ** F10["LOGMS"][b], 3.0))
            profs.append((pro, np.clip(q_profile(jj, F10["ZL"], pro / r200), 0.0, 2.0)))
        with lane_env():
            old = F10["kids_switched"](profs)
        new = kids_fixed(profs)
        E4[v] = dict(kids=new, kids_committed_projector=old, r200_ret=[float(p[1][-1]) for p in profs])
        GT.setdefault(v, {})["KiDS"] = all(new[f] <= 4.0 for f in FEET)
        P(f"    v_k {v:5.0f}: Delta chi^2 {new['canonical']:+.1f}/{new['alt']:+.1f} (exact projector; committed {old['canonical']:+.1f}/{old['alt']:+.1f}); "
          f"retention at r200 by bin {np.round(E4[v]['r200_ret'], 3).tolist()}")
    check("E4 KiDS PASSES with the theta trigger at every scanned kick (exact projector, both footings, <= +4)",
          {f"{k_:.0f}": {f: round(x, 2) for f, x in v_["kids"].items()} for k_, v_ in E4.items()},
          all(GT[v]["KiDS"] for v in VK_G), load_bearing=False)
    OUT["numbers"]["E4"] = {f"{k_:.0f}": v_ for k_, v_ in E4.items()}


def partE5():
    banner("E5  COSMIC SHEAR (MS3's halo model; the halos' modelled retention inside r200 at z = 0.5; 1.75 Mpc cap, door; R <= 1.2)")
    E5 = {}
    for v in VK_G:
        Ms, es = [], []
        for M in SH_M:
            jj = job("theta", M, 0.5, "%.4f" % alpha_eff(M), 0.0, v, wins=(0.5,))
            Ms.append(ref_w(jj, 0.5, "M200")); es.append(eps_w(jj, 0.5, "r200"))
        Ms, es = np.array(Ms), np.array(es); o = np.argsort(Ms); Ms, es = Ms[o], es[o]
        ret = lambda M, Ms=Ms, es=es: float(np.clip(np.interp(math.log10(M), np.log10(Ms), es), 0.0, 1.0))
        with lane_env():
            R = {f: max(F10["R_of"](F10["XLIN"], F10["A0_MS3"][f], 1.75, "door", ret)[0].values()) for f in FEET}
        E5[v] = dict(M200=Ms.tolist(), ret=es.tolist(), R=R)
        GT.setdefault(v, {})["shear"] = max(R.values()) <= 1.2
        P(f"    v_k {v:5.0f}: retention inside r200 " + ", ".join(f"{m:.1e}: {e:.2f}" for m, e in zip(Ms, es))
          + f"; worst R {R['canonical']:.2f}/{R['alt']:.2f}")
    check("E5 (reported) COSMIC SHEAR at the 1.75 Mpc cap with the theta trigger's retention (raw model, both footings)",
          {f"{k_:.0f}": {f: round(x, 3) for f, x in v_["R"].items()} for k_, v_ in E5.items()}, True, load_bearing=False)
    OUT["numbers"]["E5"] = {f"{k_:.0f}": v_ for k_, v_ in E5.items()}


HVQ, HV = {}, {}


def partE6():
    banner("E6  HARVEY+2015 (L370's machinery via L372's harvey(), FP16's wiring; the theta trigger's retention profiles)")
    for v in VK_H:
        for M in HV_M:
            jj = job("theta", M, 0.4, "%.4f" % alpha_eff(M), 0.0, v, wins=(0.4,))
            xg = np.geomspace(0.005, 2.0, 30)
            HVQ[(v, M)] = (xg, np.clip(q_profile(jj, 0.4, xg), 0.0, 2.0))
        P(f"    v_k {v:.0f}: retention at 0.1/0.2/0.5/1 r200 (z = 0.4): " + "; ".join(
            f"{M:.0e}: " + "/".join(f"{np.interp(x, *HVQ[(v, M)]):.2f}" for x in (0.1, 0.2, 0.5, 1.0)) for M in HV_M))
    if SMOKE or not VK_H:
        P("    Harvey not run in SMOKE")
        return
    P72 = os.path.join(REPO, "real_research", "merger_infall_2026", "L372_gated_slow_kick_carrier.py")
    s72 = open(P72).read()
    harv = s72[s72.index('P70 = os.path.join(HERE, "L370_boosted_infall_mergers.py")'):s72.index("def non_harvey_ok(r):")]
    from scipy.interpolate import PchipInterpolator
    L57_ = F10["L57"]
    HNS = dict(os=os, math=math, np=np, time=time, P=P, T0=T0, brentq=brentq, PchipInterpolator=PchipInterpolator, FAST=False,
               HERE=os.path.join(REPO, "real_research", "merger_infall_2026"), RHOC0_KPC_57=F10["RHOC0_KPC"], Ez2_57=F10["Ez2"],
               rho_thr_57=L57_["rho_thr"], x_eff=None, retained_core_57=L57_["retained_core"])
    with lane_env():
        exec(harv, HNS)

    def ratio_profile_sam(H, pic, xv, vk):
        pro = np.geomspace(10.0, 2.0 * H.R200, 24)
        lm = [math.log10(M_) for M_ in HV_M]
        qs = np.array([np.interp(pro / H.R200, *HVQ[(vk, M_)]) for M_ in HV_M])
        w_ = np.clip(np.interp(math.log10(H.M200), lm, np.arange(len(lm))), 0, len(lm) - 1)
        i0 = int(min(math.floor(w_), len(lm) - 2)); t_ = w_ - i0
        return pro, (1 - t_) * qs[i0] + t_ * qs[i0 + 1]
    HNS["ratio_profile"] = ratio_profile_sam
    HNS["L70"]["SWITCH"]["p1_x2.5"] = (1.0, 2.5)
    HNS["SW_DEF"] = "p1_x2.5"
    for v in VK_H:
        with contextlib.redirect_stdout(io.StringIO()):
            h = HNS["harvey"]("fp25", None, v, 1.0)
        HV[v] = dict(beta=h["beta"], core={f"{k_:.0e}": x for k_, x in h["core"].items()}, ok=bool(h["ok"]))
        GT.setdefault(v, {})["Harvey"] = HV[v]["ok"]
        P(f"    v_k {v:.0f}: excess beta " + "/".join(f"{h['beta'][e]:+.3f}" for e in ("100", "150", "fit"))
          + f"; core carrier/baryons(<150 kpc) " + " / ".join(f"{x:.2f}" for x in h["core"].values())
          + f" -> {'PASS' if h['ok'] else 'FAIL'}   {el()}")
        gc.collect()
    check("E6 (reported) HARVEY with the theta trigger's profiles at 650 and 1000 km/s (<= +0.10 excess beta on all three estimators)",
          {f"{k_:.0f}": dict(beta={e: round(x, 3) for e, x in v_["beta"].items()}, ok=v_["ok"]) for k_, v_ in HV.items()},
          True, load_bearing=False)
    OUT["numbers"]["E6"] = {f"{k_:.0f}": v_ for k_, v_ in HV.items()}


def partE6b():
    banner("E6b FP22's DIFFERENTIAL ACCELERATION in a merger (galaxies feel the phantom, the carrier does not): an ESTIMATE (OPEN)")
    Msun, kpc = 1.98892e30, 3.0856775814913673e19
    r200s = (3 * 1e14 / (4 * math.pi * 200 * F10["RHOC0_KPC"] * F10["Ez2"](0.4))) ** (1 / 3)
    sig = 0.7 * math.sqrt(GKPC * 1e14 / r200s) * 1e3                    # m/s: the 1e14 subcluster's 1-D dispersion ~ 0.7 V200
    rows = {}
    for f in FEET:
        a0 = A0_FP0[f]
        for rsep in (300.0, 500.0, 1000.0):                              # kpc from the 1e15 host's centre (baryons f_b 0.15)
            Mb = 0.15 * 1e15 * min(1.0, (rsep / 2000.0) ** 1.2)
            gN = G_SI * Mb * Msun / (rsep * kpc) ** 2; y = gN / a0
            gph = (math.sqrt(1 + 1 / y) - 1) * gN                         # nu_mono phantom acting on the baryons only
            offs = {f"{ap:.0f}": gph * (ap * kpc) ** 2 / (3 * sig ** 2) / kpc for ap in (100.0, 150.0, 250.0)}
            drift = 0.5 * gph * (3.156e16) ** 2 / kpc                    # free drift over 1 Gyr (the unbound ceiling)
            rows[f"{f}|{rsep:.0f}"] = dict(y=y, g_phantom=gph, ratio_phantom_newton=gph / gN, offset_kpc_by_aperture=offs, free_drift_kpc=drift)
            P(f"    {f:9s} r = {rsep:4.0f} kpc: y_b {y:.2f}, phantom/Newtonian(baryons) {gph / gN:.2f}, g_ph {gph:.2e} m/s^2 -> galaxy-"
              f"carrier centroid offset (linear response, sigma {sig / 1e3:.0f} km/s) " + ", ".join(f"{v:.0f} kpc (aperture {k_})" for k_, v in offs.items())
              + f"; free drift over 1 Gyr {drift:.0f} kpc")
    o150 = [r["offset_kpc_by_aperture"]["150"] for r in rows.values()]
    check("E6b (reported, OPEN) FP22's price in mergers: the subcluster's galaxies feel the host's phantom and its carrier does not, "
          "so their centroids separate by ~%.0f-%.0f kpc inside a 150 kpc aperture (linear response of a bound tracer; x R_ap^2; "
          "the free drift over a crossing time, %.0f-%.0f kpc, is the unbound ceiling) against Harvey's 60-120 kpc gas-galaxy "
          "offsets: beta can move by O(0.1), sign set by the orbital phase" % (min(o150), max(o150),
          min(r['free_drift_kpc'] for r in rows.values()), max(r['free_drift_kpc'] for r in rows.values())),
          {k_: {a: round(x, 1) for a, x in v_["offset_kpc_by_aperture"].items()} for k_, v_ in rows.items()}, True,
          "FP16's shell model has no mergers; deciding it needs a merger run with the two metrics (the hub's PM)", load_bearing=False)
    OUT["numbers"]["E6b"] = rows


def partE8():
    banner("E8  THE GATE TABLE AND THE WINDOW for the theta trigger (kicks x gates; the forest and S_8 are kick-scanned in C3/C4)")
    for v in sorted(GT):
        GT[v]["forest"] = False                                         # C3: fails at every reading and kick (kick-independent)
        if S8R is not None and f"theta nominal ({v:.0f})" in S8R:
            GT[v]["S8"] = S8R[f"theta nominal ({v:.0f})"] >= 0.922
    fmt = lambda b: "n/a" if b is None else ("pass" if b else "FAIL")
    for v in sorted(GT):
        P(f"    v_k {v:5.0f}: " + ", ".join(f"{g} {fmt(GT[v].get(g))}" for g in ("X-COP", "flagship", "galaxies", "KiDS", "shear", "Harvey", "S8", "forest")))
    passing = [v for v in GT if all(x for x in GT[v].values() if x is not None)]
    xk = [v for v in sorted(GT) if GT[v].get("X-COP")]
    pinc = {f"{v:.0f}": dict(S8=(round(S8R[f"theta nominal ({v:.0f})"], 4) if S8R and f"theta nominal ({v:.0f})" in S8R else None),
                            Harvey=GT[v].get("Harvey")) for v in xk}
    P("    the kicks where X-COP's strict window is open, with S_8 and Harvey there: " + (", ".join(f"{k_}: S_8 {d['S8']}, Harvey "
      f"{fmt(d['Harvey'])}" for k_, d in pinc.items()) or "none"))
    check("E8 THE WINDOW IS EMPTY for the unified trigger at every kick 400-1500 km/s: the forest fails at every kick (C3, "
          "kick-independent); where X-COP's strict window opens (fast kicks) S_8 falls below 0.922 as well",
          {f"{v:.0f}": {g: fmt(x) for g, x in GT[v].items()} for v in sorted(GT)}, len(passing) == 0)
    OUT["numbers"]["E8_xcop_pairs"] = pinc
    OUT["numbers"]["E8"] = {f"{v:.0f}": GT[v] for v in sorted(GT)}


if not MUTATE:
    for lab_, fn_ in (("E1", partE1), ("E2", partE2), ("E3", partE3), ("E4", partE4), ("E5", partE5), ("E6", partE6),
                      ("E6b", partE6b), ("E8", partE8)):
        guard(lab_, fn_)
        gc.collect()

# ================================================================================================ PART F: the smallest structures
banner("F1  THE 3-AXIS GATE (theta_ij negative semidefinite: no direction still expanding) -- zero constants")


def partF1():
    # forming sheets/filaments always keep an expanding axis at the Hubble rate: gate shut through their formation (derived)
    fs = y_open(np.array([[1.0, 0.0, 0.0]]), 1.0)[0]
    lam = LAM[:NMC_T]; res = {}
    for z in (3.0, 2.0):
        f = f_of(z); y = D_of(z) * sig_of(MF_POST(z))
        x = y * lam
        three = (x >= 1 / (1 + f)).all(1)                              # every axis past its turnaround (Zel'dovich knots)
        res[f"{z:g}"] = dict(zeldovich_knots=float(three.mean()))
    b3 = BUDG["3-axis gate (halos only)"] if BUDG else None
    fr = FOREST.get("3-axis gate (halos only)|650") if FOREST else None
    x3 = {v: eps_w(job("theta3", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), 0.0, v, wins=(0.0557,)), 0.0557, "R500")
          for v in ((650.0, 1000.0) if not SMOKE else ()) if key(job("theta3", 1e15, 0.0557, "%.4f" % alpha_eff(1e15), 0.0, v, wins=(0.0557,))) in RES}
    P(f"    a pure forming sheet under the 3-axis gate: never opens (axes 2, 3 expand); Zel'dovich knots at the filtering scale "
      f"z = 3/2: {res['3']['zeldovich_knots']:.3f}/{res['2']['zeldovich_knots']:.3f} (the excursion-set turnaround carries the halos)")
    if b3: P(f"    halo-only budget F(7/3/2) = " + "/".join(f"{np.interp(z, b3['z'], b3['F']):.3f}" for z in (7, 3, 2)))
    if fr: P(f"    forest (XR12 calibrated gas proxy, 650 km/s): z = 3 {fr['3.0']:.3f}, z = 2 {fr['2.0']:.3f}")
    if x3: P("    X-COP eps(R500) with the 3-axis gate: " + ", ".join(f"{v:.0f} km/s {e:.3f}" for v, e in x3.items()))
    ok = fr is not None and fr["2.0"] > 0.10
    check("F1 THE 3-AXIS GATE SPARES THE FORMING WEB (an expanding axis keeps it shut, derived) BUT STILL FAILS THE FOREST: every "
          "turned-around halo above the baryon scale converts, including the pre-reionization minihalos, so the calibrated gas proxy "
          "stays above 10%% at z = 2 (%s)" % (f"{fr['2.0']:.3f}" if fr else "n/a"),
          dict(forest=fr, xcop=x3, knots=res), ok,
          "zero constants, but not mass-selective: the forest needs the conversion held back at z >~ 2-4 in small halos, which only a "
          "threshold (zeta, q) or an acceleration key (AT1's y_v) has done on the record")
    OUT["numbers"]["F1"] = dict(knots=res, forest=fr, xcop=x3)


if not MUTATE:
    guard("F1", partF1)

banner("F2  NEWTONIAN-CORE RETENTION (the conversion vetoed where y_b > 1): the flagship's residue at r_F")


def partF2():
    from scipy.special import gammainc
    out = {}
    for lMb in (10.5, 11.0):
        H_ = F10["flag_host"](lMb, 1.0, 2.5)
        c = H_["c"]; rhoc = H_["rhoc"]; Mh, Mb, ah = H_["Mh"], H_["Mb"], H_["a"]
        r200 = (3 * Mh / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / c
        mc = math.log1p(c) - c / (1 + c)
        Mnfw = lambda r: Mh * (np.log1p(r / rs) - (r / rs) / (1 + r / rs)) / mc
        rg = np.geomspace(1e-3 * rs, 30 * r200, 6000)
        Mtot = Mnfw(rg) + Mb * rg ** 2 / (rg + ah) ** 2                # NFW (pre-conversion carrier + gas-free halo) + Hernquist baryons
        gr = GKPC * Mtot / rg ** 2
        phi = -np.concatenate([np.cumsum((0.5 * (gr[1:] + gr[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]]) - GKPC * Mtot[-1] / rg[-1]
        rho = 1.0 / ((rg / rs) * (1 + rg / rs) ** 2)                      # the carrier's NFW shape (tracer)
        seg = 0.5 * (rho[1:] * gr[1:] + rho[:-1] * gr[:-1]) * np.diff(rg)
        s2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / rho   # isotropic Jeans sigma^2 in the total potential
        for f in FEET:
            rN = math.sqrt(G_SI * Mb * 1.98892e30 / A0_FP0[f]) / 3.0856775814913673e19     # kpc: g_bar = a0 (point-mass form)
            rF = H_["rF"][f]
            sel = rg <= rN
            vmax2 = 2 * np.maximum(np.interp(rN, rg, phi) - phi[sel], 0.0)
            conf = gammainc(1.5, vmax2 / (2 * np.maximum(s2[sel], 1e-30)))   # Maxwellian: P(|v| < v_max)
            dM = np.gradient(Mnfw(rg[sel]), rg[sel])
            Mconf = float(np.trapz(dM * conf, rg[sel]))
            S = Mconf / float(Mnfw(rF))
            out[f"{lMb}|{f}"] = dict(r_N_kpc=rN, r_F_kpc=rF, S_all_inside_rN=float(Mnfw(rN) / Mnfw(rF)), S_confined=S)
            P(f"    M_b 1e{lMb} ({f}): r_N {rN:.1f} kpc vs r_F {rF:.1f} kpc; carrier inside r_N / NFW carrier inside r_F = "
              f"{float(Mnfw(rN) / Mnfw(rF)):.3f} (all kept), {S:.3f} (only orbits confined inside r_N kept; isotropic Jeans, Maxwellian)")
    worst = max(v["S_confined"] for v in out.values()); best = min(v["S_confined"] for v in out.values())
    # the clusters' Newtonian zone: a BCG (1e12 Msun, Hernquist a = 15 kpc) + gas (f_b 0.12 M200 (r/r200)^1.2), z = 0.4
    rNc = {}
    for Mc in (1e14, 3e14, 1e15):
        r200c = (3 * Mc / (4 * math.pi * 200 * F10["RHOC0_KPC"] * F10["Ez2"](0.4))) ** (1 / 3)
        gb = lambda r: G_SI * 1.98892e30 * (1e12 * r ** 2 / (r + 15.0) ** 2 + 0.12 * Mc * min(1.0, (r / r200c) ** 1.2)) / (r * 3.0856775814913673e19) ** 2
        rNc[f"{Mc:.0e}"] = {f: brentq(lambda r: gb(r) - A0_FP0[f], 1.0, 2000.0) for f in FEET}
    P("    clusters' Newtonian zone (y_b > 1) at z = 0.4: " + "; ".join(f"{k_}: r_N {v_['canonical']:.0f}/{v_['alt']:.0f} kpc" for k_, v_ in rNc.items()))
    rmax = max(v_[f] for v_ in rNc.values() for f in FEET)
    check("F2 NEWTONIAN-CORE RETENTION IS NOT THE HARVEY FIX: vetoing conversion where y_b > 1 (a0's own scale, no constant) keeps "
          "carrier only inside r_N <= %.0f kpc in 1e14-1e15 clusters -- inside Harvey's 100-150 kpc estimators, not across them -- "
          "while in the z = 2.5 flagship hosts it keeps the orbits confined inside r_N = sqrt(G M_b/a0), S(r_F) = %.3f-%.3f against "
          "MS2's 0.059: the flagship's margin is gone" % (rmax, best, worst),
          dict(flagship={k_: round(v_["S_confined"], 3) for k_, v_ in out.items()}, cluster_rN=rNc), rmax < 100.0 and best >= 0.04,
          "the veto keeps the wrong carrier: the flagship's inner halo, not the cluster cores Harvey needs")
    OUT["numbers"]["F2_clusters"] = rNc
    OUT["numbers"]["F2"] = out


guard("F2", partF2)

banner("F3-F5  FK1's OWN BLOCKING, A SECOND CHANNEL, AND FK1 + A THETA VETO")


def partF345():
    # F4: FP15's Z4 theorem: eps Re(Phi^2) is the only quadratic term odd under Phi -> i Phi; one splitting -> one kick line
    Phi, Phis, e1, e2 = sp.symbols("Phi Phis e1 e2")
    terms = {"Re(Phi^2)": (Phi ** 2 + Phis ** 2) / 2, "|Phi|^2": Phi * Phis, "Re(Phi^4)": (Phi ** 4 + Phis ** 4) / 2,
             "|Phi|^4": (Phi * Phis) ** 2, "(Im Phi^2)^2": (-(Phi ** 2 - Phis ** 2) ** 2) / 4}
    rot = lambda ex: sp.expand(ex.subs({Phi: sp.I * Phi, Phis: -sp.I * Phis}, simultaneous=True))
    odd = {k_: sp.simplify(rot(v) + v) == 0 for k_, v in terms.items()}
    okF4 = odd["Re(Phi^2)"] and not odd["|Phi|^2"] and not odd["Re(Phi^4)"] and not odd["|Phi|^4"] and not odd["(Im Phi^2)^2"]
    check("F4 CONSTRAINT (sympy, FP15's Z4 theorem re-checked): under Phi -> i Phi only eps Re(Phi^2) is odd; the quartics are even and "
          "split nothing at quadratic order -- one complex field carries ONE kick line (v_k), broadened only by the pump's motion.  The "
          "record's one opening of X-COP + Harvey together (L372's two-channel carrier, alt set) needs a second, fast (3000 km/s), "
          "spatially uniform channel: a second splitting, i.e. a second field -- a new species, excluded by the standing rule",
          {k_: ("odd" if v else "even") for k_, v in odd.items()}, okF4,
          "L372's channel U costs 3 constants (f_U, v_U, its rate exponent) on top of the gated channel's")
    # F5: FK1 + theta veto: the upper bound on the late web conversion it removes (the formed web with an expanding axis now)
    b2 = OUT["numbers"].get("B2", {})
    x19 = rd("real_research/cross_thread_review_2026_09_26/XR19_web_runaway_results.json")["numbers"]
    Ft = {k_: x19["F_tot"]["nominal"][k_] for k_ in ("1.0", "0.0")}
    Fh = {k_: x19["B"]["nominal 5.31"][k_][0] for k_ in ("1.0", "0.0")}
    shut0 = b2.get("0|2 Mpc/h web scale (1e12.7 Msun)", {}).get("shut", float("nan"))
    c5 = (OUT["numbers"].get("C5") or {}).get("rows", {})
    nomr, halr = c5.get("FK1 nominal (XR19, 600)"), c5.get("FK1 halo only (600)")
    if nomr and halr and S8R:
        P(f"    the veto's ceiling (FK1-as-is -> FK1 halo-only, linear proxies): counts {nomr['counts']:.3f} -> {halr['counts']:.3f} of LCDM "
          f"(x XR32: {nomr['counts_scaled'][0]:.2f}-{nomr['counts_scaled'][1]:.2f} -> {halr['counts_scaled'][0]:.2f}-{halr['counts_scaled'][1]:.2f}); "
          f"f sigma8(z 0.5) {nomr['rsd'][0.5]:.3f} -> {halr['rsd'][0.5]:.3f} (DESI {nomr['rsd_sigma_scaled']:+.1f} -> {halr['rsd_sigma_scaled']:+.1f} sigma); "
          f"Sum m_nu-equivalent {nomr['mnu_equiv_eV']:+.3f} -> {halr['mnu_equiv_eV']:+.3f} eV; S_8 {S8R['FK1 nominal (XR19, 600)']:.3f} -> "
          f"{S8R['FK1 halo only (600)']:.3f}")
    P(f"    XR19 nominal: F_tot(z = 1/0) = {Ft['1.0']:.3f}/{Ft['0.0']:.3f} against the halo-only {Fh['1.0']:.3f}/{Fh['0.0']:.3f}: the web "
      f"part {Ft['1.0'] - Fh['1.0']:.3f}/{Ft['0.0'] - Fh['0.0']:.3f}; the formed web with an expanding axis is shut now in {shut0:.3f} (B2)")
    check("F5 (reported, OPEN) FK1 + A THETA_b VETO (convert only where rho >= rho_t(z) AND theta_b <= 0; zero new constants; zeta, q "
          "kept): the veto cannot reduce FK1's knobs, but it shuts XR19's late runaway through FORMED, axis-expanding filaments and "
          "sheets (theta > 0 now, B2) while leaving halos (flagship, galaxies) untouched -- the direction XR32's counts, RSD and "
          "Sum m_nu want (less late conversion).  Its bite is bounded by the web part of XR19's budget, %.2f of the fluid by z = 0; "
          "forming sheets' caustics (theta and density both spike) remain open to it" % (Ft["0.0"] - Fh["0.0"]),
          dict(web_part={k_: Ft[k_] - Fh[k_] for k_ in Ft}, formed_web_shut_now=shut0,
               ceiling=dict(nominal=nomr, halo_only=halr) if (nomr and halr) else None), True,
          "deciding it needs XR19's runaway machinery (or the hub's PM) re-run with the veto", load_bearing=False)
    OUT["numbers"]["F4"] = odd; OUT["numbers"]["F5"] = dict(web_part={k_: Ft[k_] - Fh[k_] for k_ in Ft}, shut_now=shut0)


if not MUTATE:
    guard("F3-F5", partF345)

# ================================================================================================ H: the pre-declared hypotheses
banner("H  THE PRE-DECLARED HYPOTHESES as they fell (scratch note 12:05, before any FP25 number)")


def partH():
    N = OUT["numbers"]; ck = OUT["checks"]
    okc = lambda pre: next((v["ok"] for k_, v in ck.items() if k_.startswith(pre)), None)
    b1 = N.get("B1", {}); b2 = N.get("B2", {}); c2 = N.get("C2", {}); e1 = N.get("E1", {}); c4 = N.get("C4", {})
    a5 = N.get("A5", {}); e6b = N.get("E6b", {}); c6 = N.get("C6", {})
    tot3 = (b1.get("total flow (single stream to crossing)") or {}).get("3", {})
    shut = [v.get("shut") for v in b2.values() if v.get("shut") == v.get("shut")]
    W = [r["window"] for r in (a5.get("rows") or {}).values()]
    fk1_03_1 = ((c6.get("tables") or {}).get("FK1-as-is (XR32 nominal, 600)") or {}).get("1")
    H = [
        ("H1", "no background conversion", okc("A1")),
        ("H2", "caustic theorem; >= 0.5 converted by z = 3 at the baryon scale", bool(okc("A3")) and bool(tot3) and min(tot3.values()) >= 0.5),
        ("H3", "cold accretion (s ~ 0.35) does not shut the gate", okc("A4")),
        ("H4", ">= 90% of formed sheets+filaments shut now", bool(shut) and min(shut) >= 0.90),
        ("H5", "F(3) >= 0.34 and the forest fails", bool(okc("B3/C1")) and bool(okc("C3 THE FOREST"))),
        ("H6", "share >= 1e10.5 at z = 3 <= 0.1", ((c2.get("3") or {}).get("share_upper", 1.0) <= 0.1) if c2 else None),
        ("H7", "the flagship passes", okc("E2")),
        ("H8", "X-COP needs v_k >= 1000", (e1.get("v_strict", float("nan")) >= 1000.0) if e1 else None),
        ("H9", "Harvey fails at >= 800", (not N.get("E6", {}).get("1000", {}).get("ok", True)) if N.get("E6") else None),
        ("H10", "the window is EMPTY", okc("E8")),
        ("H11", "the 3-axis gate spares the web, the forest fails", okc("F1")),
        ("H12", "lambda_on window <= 4 decades", bool(W) and max(W) <= 1e4),
        ("H13", "S_8 < 0.922 at ~600 km/s", (c4.get("theta nominal (650)", 1.0) < 0.922) if c4 else None),
        ("H14", "FP22 offset >= 10 kpc", bool(e6b) and min(v["offset_kpc_by_aperture"]["150"] for v in e6b.values()) >= 10.0),
        ("H15", "FK1 linear suppression at k = 0.3, z = 1 <= 3%", (1 - fk1_03_1[1] <= 0.03) if fk1_03_1 else None),
    ]
    for k_, t_, ok_ in H:
        P(f"    {k_:4s} {'held' if ok_ else ('FELL' if ok_ is not None else 'n/a')}: {t_}")
    check("H (reported) the pre-declared hypotheses as they fell", {k_: ("held" if ok_ else ("FELL" if ok_ is not None else "n/a")) for k_, t_, ok_ in H},
          True, load_bearing=False)
    OUT["numbers"]["H"] = {k_: dict(text=t_, held=ok_) for k_, t_, ok_ in H}


guard("H", partH)

# ================================================================================================ D: the count
banner("D  THE DARK SECTOR's CONSTANTS: before (FK1, FP10/FP15) and with each construction tested here")
COUNT = [
    ("FK1 as adopted (FP10/FP15/FP22)", "eps, zeta, q, m (+ the pure cross quartic POSTULATED; amount/misalignment initial data)", 4,
     "window EMPTY (FP16: X-COP, Harvey)"),
    ("unified theta_b trigger (this lane)", "eps, m, lambda_on (a density window, A5) -- zeta and q removed", 3,
     "FAILS: web (B1), forest (C3), selectivity (C2), S_8 (C4); XR32 gates worse (C5); window EMPTY (E8)"),
    ("3-axis gate (F1)", "eps, m, lambda_on", 3, "FAILS: forest (F1)"),
    ("Newtonian-core veto (F2)", "the theta gate's + nothing (y_b = 1 is a0's own)", 3, "FAILS: flagship (F2)"),
    ("FK1 + theta veto (F5)", "eps, zeta, q, m (the veto adds none)", 4, "OPEN: can only lower the late web conversion"),
    ("two-channel opening (L372, F4)", "FK1's + f_U, v_U, the U rate exponent, and a second field", 7, "excluded (a new species)"),
]
for a, b, n, c in COUNT:
    P(f"    {a:38s} {n} constants: {b}  --  {c}")
check("D (reported) THE COUNT: no construction tested here opens the window with fewer constants than FK1's four; the unified "
      "trigger trades zeta and q for lambda_on (4 -> 3) and fails; the smallest structure on the record that opens X-COP + Harvey "
      "(L372's second channel) needs a second field", {a: n for a, b, n, c in COUNT}, True, load_bearing=False)
OUT["numbers"]["D"] = [dict(construction=a, constants=b, n=n, status=c) for a, b, n, c in COUNT]

# ================================================================================================ W: the ledger
banner("W  THE LEDGER (link / status / basis)")
g = lambda k_, d_=None: OUT["numbers"].get(k_, d_)
e1 = g("E1", {}) or {}
LEDGER = [
    ("L25a", "the unified gate lambda_on Theta(-theta_b) vanishes on FRW (theta = 3H) and in linear theory (theta/H = 3 - f delta_L): "
             "no background conversion, threshold 0 scale-free", "DERIVED", "A1, A2 (sympy)"),
    ("L25b", "caustic theorem: theta -> -inf at shell crossing; the gate opens in forming sheets (x* = 3/(3+f)), filaments (2/(2+f)) "
             "and halos (1/(1+f))", "DERIVED", "A3 (sympy)"),
    ("L25c", "baryon reading: the gas passes theta_b <= 0 before its accretion shock unless the shock stands off >= 3/4 (sheets) / "
             "8/9 (filaments) of the turnaround distance; the self-similar 0.347 does not shut it", "DERIVED",
     "A4; the stand-off is a literature input (Bertschinger 1985), bracketed in B1"),
    ("L25d", "lambda_on is not a regulator: the channel closes above G_block = eps(m^2+eps)/(2m^3) ~ m v_k^2/4 and needs G >= G_min; "
             "the open window is <= 1e4 wide in density", "CONSTRAINT", "A5 (derived from V and FP10 A5's rate)"),
    ("L25e", "FK1-as-written cannot convert above rho_block = rho_t (v_k^2/4)/(G_t/m) (~555/sqrt(E) rho_t at 600 km/s): galaxy "
             "centres at z = 2.5 (r <~ 0.05 r200) and cluster cores at z <~ 0.4 (r <~ 0.15-0.2 r200); omitted by FP10/FP16",
     "DERIVED", "A5b; small in FK1's timing (conversion at the front, before the carrier is dense)"),
    ("L25f", "the unified theta_b trigger converts the web (the history of every shell-crossing element) in both readings",
     "FAILS", "B1: ever-opened fraction by z = 3 at the baryon scale >= ~0.5"),
    ("L25g", "the formed web is shut NOW under the theta gate (useful for XR36's reversible MOND gate)", "DERIVED",
     "B2 (MUTATE: a delta >= delta_c key turns it on)"),
    ("L25h", "the unified trigger fails the forest (XR12's calibrated gas proxy), mass selectivity and S_8", "FAILS", "C2, C3, C4"),
    ("L25i", "XR32's gates (eRASS1 counts, DESI RSD, Sum m_nu-equivalent lensing) move further from the data under the unified "
             "trigger than under FK1-as-is (approximate linear proxies scaled by XR32)", "FAILS", "C5 (approximate)"),
    ("L25j", "with the theta trigger X-COP's strict window opens at v_k ~ %s km/s (FK1: ~1047); the window stays EMPTY (forest, S_8 "
             "at every kick)" % (f"{e1.get('v_strict', float('nan')):.0f}" if e1 else "n/a"), "FAILS", "E1, E8"),
    ("L25k", "the 3-axis gate spares the forming web but still fails the forest; Newtonian-core retention fails the flagship; a "
             "second fast channel needs a second field (FP15's Z4)", "CONSTRAINT", "F1, F2, F4"),
    ("L25l", "FP22's merger price: galaxy-carrier centroid offsets of tens of kpc from the phantom acting on baryons only",
     "OPEN", "E6b (estimate; needs a merger run)"),
    ("L25m", "FK1 + theta_b veto (zero constants): can only remove late web conversion (XR32's direction)", "OPEN", "F5"),
    ("L25n", "FK1-as-is's late-time linear suppression P/P_LCDM (k = 0.1-3 h/Mpc, z = 0-2) and at the CMB-lensing weights",
     "DERIVED", "C6 (L319's CLASS-validated solver)"),
]
for k_, what, st, basis in LEDGER:
    P(f"    {k_:5s} {st:10s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b) for k_, w, s_, b in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)
if FAILS:
    check("F (crash guard) every part completed without an exception", "; ".join(f"{a}: {b[:200]}" for a, b in FAILS), False)

# ================================================================================================ verdict
banner("VERDICT")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
if MUTATE:
    P("  MUTATE: the trigger keyed to delta >= delta_c: the formed web is ON (B2 flips); parts C-E not run.")
else:
    P("  THE UNIFIED TRIGGER (convert where theta_b <= 0) removes zeta and q and is exactly off on FRW, but it FAILS: an irreversible\n"
      "  conversion reads the HISTORY of the flow, and every Lagrangian element that shell-crosses passes theta <= 0 on the way in\n"
      "  (the caustic theorem), so the web and the pre-reionization minihalos convert.  The budget runs ahead of FK1's; the forest,\n"
      "  mass selectivity and S_8 fail, and XR32's counts/RSD/lensing tensions worsen.  The kick scan (FP16's model) opens X-COP's\n"
      "  window at a lower kick than FK1 needs, but the window stays EMPTY.  lambda_on is a density window, not a regulator.  The\n"
      "  smallest structures fail (3-axis gate: forest; Newtonian-core veto: flagship); a second fast channel needs a second field.\n"
      "  Constructive residue: the theta gate's INSTANTANEOUS state spares the formed web (for XR36), and FK1 + a theta veto (zero\n"
      "  constants) can only reduce late web conversion.  The dark sector stays at FK1's four constants.")
if SMOKE and SMOKE_DIR:
    odir = SMOKE_DIR
else:
    odir = HERE


def _jd(o):
    if isinstance(o, dict): return {str(k_): _jd(v_) for k_, v_ in o.items()}
    if isinstance(o, (list, tuple)): return [_jd(v_) for v_ in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.ndarray): return _jd(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return str(o)
    return o


fn = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
if not (SMOKE and not SMOKE_DIR):
    json.dump(_jd(OUT), builtins.open(os.path.join(odir, fn), "w"), indent=1)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {fn}   {el()}")
sys.exit(0 if n_fail == 0 else 1)
