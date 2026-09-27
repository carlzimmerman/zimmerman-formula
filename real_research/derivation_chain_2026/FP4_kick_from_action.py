#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP4 -- THE DARK SECTOR AND ITS KICK FROM THE ROOT: can the dark mass be a STATE of the ungated C-H/K core's own fields, and
can the core hand that state the kick that clears galaxies?

WHY.  The scalar kick is wanted, but as built it "falls off the wall": the kick speed (575-675 km/s), its rate and its
trigger were set by hand (L357, L359/L388, AT1-AT4, FK1).  The derivation chain's rule is that nothing below the root is
posited.  The coordinator's redirect (2026-09-26) roots this lane in the UNGATED C-H/K CORE and asks: (A) can the
cosmological dust and the clusters' missing mass be a state of the core's own fields (the clock tau, U, W, L, lambda_0,
and the metric)?  (B) can the kick be DERIVED from them -- energy the clock or the MOND auxiliary sector hands to that state
where g ~ a0 -- and is the ~600 km/s window predicted or only selected?  If not, name the minimal addition and its cost.
It added two requirements: the hand-built windows are knife-edges (mode A alone at 575 km/s fails the flagship at z = 0.5
with 0.149, AT1's 600 km/s keeps every z <= 0.074; Harvey passes only at 575, L389, provisional), so a derived kick must
land inside that sliver without tuning or widen the window; and 575/600 are not targets to fit.

THE ROOT (one action; every equation used below is varied out of it):
    I_core = c^3/(16 pi G) Int d^4x sqrt(-g) { R - 2 Lambda + 2 h^{mn}(D_m U - a_m)(D_n U - a_n)
               + 2 alpha^2 q(h^{mn} D_m W_b D_n W_b / alpha^2) + Int_0^b dz L (d_z W - Delta_h W) + lambda_0 (W_0 - U)
               + alpha_c a_m a^m - c_2 (K - <K>_h)^2 } + GHY + S_matter[g]
  astra's C-H (qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md:95-106), L340's BPS terms with
  beta = 0 (c_T = c), L350's leaf average; kernel q'(s^2) = nu_mono(s) - 1; n_m = -d_m tau / sqrt(X), N = X^(-1/2),
  a_m = D_m ln N, K = div n, alpha = a0/c^2.  Non-relativistic limit (ACTION.md, derived there):
      I_NR = Int dt d^3x { L_kin - rho Phi - [2 grad Phi . grad u - |grad u|^2 - a0^2 q(|grad S u|^2/a0^2)]/(8 pi G) }.
  Constants: G, c, Lambda; a0 = kappa c sqrt(G rho_Lambda) (kappa = 1/2 FITTED); xi; alpha_c; c_2; nu_mono's 0.05.
  Both a0 footings everywhere a number depends on a0: FP0's 9.3603e-11 / 1.1312e-10; the imported machinery's own pair
  9.3619e-11 / 1.1279e-10 (0.02% / 0.3% apart) is used wherever a committed lane's function is called.

PART A -- CAN THE DARK MASS BE A STATE OF THE CORE'S FIELDS?  The core's only propagating fields are the metric (2 tensor
  modes) and the clock (1 scalar, FL1 F1).  Each candidate is derived from the action and then held to the record's
  requirements (XR8's inverse specification: w = 0 at the CMB, cold for the forest, multistreaming, kernel-invisible).
PART B -- CAN THE CORE HAND IT THE KICK?  Every algebraic coupling of a dark density rho_d to an invariant of the core is
  varied: (i) the MOND auxiliary sector's own argument I = |grad S u|^2/a0^2 (the natural scale I = 1 is g_N = a0);
  (ii) the clock's acceleration a_m (a_i = d_i Phi / c^2 in the NR limit); (iii) the clock's expansion K.  The action's own
  reciprocity then bounds what each can hand over.
PART C -- THE DERIVED MECHANISM ON THE GATES.  The strongest kick part B allows is scored with the committed lanes' functions
  (AT1/AT3's retention and flagship, L321's X-COP and galaxies, L360's KiDS at the common cell, MS3's halo-model cosmic
  shear, AT1's escape tables for the forest and S_8, L389's intact-carrier Harvey values), read-only.

CHECKS
  C0 CONTROLS (not load-bearing): L340's printed khronon mode speeds are reproduced from its own block; AT1's committed
     z = 2.5 flagship row (y_v 0.1, v_A 600, canonical, M_b 1e10.5) is reproduced by the loaded machinery; MS3's committed
     intact-carrier cosmic-shear row (1.75 Mpc cap) is reproduced.
  A1 DERIVED: the clock carries no conserved charge.  n_m dn_n/d(d_m tau) = 0 identically, and on FRW the clock's whole
     action is independent of the clock rate tau-dot (reparametrisation invariance), so the clock has no condensate dust --
     contrast AeST's independent aether, whose K(Q) excitation carries rho = Q0 mu^2 u.
  A2 DERIVED: U, W, L and lambda_0 are constrained: with lapse and shift kept, their normal derivatives never appear
     (h^{tt} = h^{tx} = 0), so their kinetic Hessian is identically zero.
  A3 DERIVED: the clock's one mode (L340's block) is gapless, omega^2 = c_2 k^2/(C(2 + 3 c_2)); a gas of its quanta has
     p = rho/3 exactly (radiation, rho ~ a^-4, not the a^-3 dust the CMB needs) and moves at >= 1800 km/s wherever C <= 100
     in L340's window, against the forest's c_s(z = 3) <= 9.5 km/s.
  A4 the metric's own cold state (primordial black holes, a vacuum state of g): not kernel-invisible (it sources u like
     any matter) and not kickable; with its full halo it fails X-COP, the galaxy gate and the flagship.
  A5 VERDICT A: no state of the core's fields can be the dust or the clusters' missing mass; the minimal addition is one
     nearly free complex scalar (2 real propagating fields) with one mass m >= 1.9-5.2e-19 eV, its amount initial data
     (XR8, FL1, L383 committed results loaded).
  B1 DERIVED (reciprocity): varying u in I_NR - rho_d V(I) multiplies the phantom's coefficient by (1 - delta) wherever the
     dark state sits, delta = 8 pi G rho_d V'(I) / (a0^2 (nu - 1)); so the energy per unit mass any such coupling can hand
     over is V <= delta (a0^2/8 pi G) Int q'(I)/rho_d dI, and delta >= 1 reverses the phantom.
  B2 DERIVED: a coupling to the clock's acceleration reads the NR multiplier Phi: the (Phi, u) constraint determinant, which
     is kernel-independent without it (CV3's rule), acquires a zero at delta_N (1 + B) = 1, and a threshold coupling makes
     A = V' + 2 V'' I cos^2(theta) negative for I > 1/3 -- the coupling turns the constraint singular before it can kick.
  B3 DERIVED + LOADED: a coupling to K is spatially blind in bound regions (CV4: |K/3H - 1| <= 4.8e-3), so it cannot push
     the dark state out of anything; a K-gated conversion's speed is the mass splitting, eps/m^2 = v^2/(2c^2 - v^2) (the
     two-body kinematics, symbolic), i.e. FK1's 1.84-2.35e-6 for 575-650 km/s: a constant of the added field.
  B4 DERIVED: for a quasi-isothermal dark halo (rho_d = v_d^2/(4 pi G r^2)) in the deep-MOND limit, B1's bound accumulated
     from the outside in is v_cap^2 = 4 delta (G M_b a0/v_d^2)(r_t/r): at the kernel's natural scale the framework's own
     velocity scale, 2 sqrt(delta) (G M_b a0)^(1/2)/v_d, appears as the CEILING of what the core can hand over, evaluated with
     each host's own baryonic mass.
  B5 THE NUMBERS on real halos (flagship hosts at z = 2.5, KiDS lenses at z = 0.25, the X-COP reference cluster), both
     footings: at the flagship radius every flagship host needs delta_req > 1 (the phantom reversed) to be unbound, and the
     cluster needs a smaller delta_req than the z = 2.5 galaxies (the ordering is backwards: anti-selective).
  B6 THE WINDOW IS NOT PREDICTED: no parameter-free velocity of the core (+ m) lies in 575-675 km/s; the candidates that reach
     it do so only by tuning a declared constant inside its window; (G M a0)^(1/4) lies in it only for M in a 0.28-dex band
     near 1e13 Msun (both footings) -- the group scale at which the gates' galaxy-clearing and cluster-retention edges meet.
  C1 THE DERIVED MECHANISM (the ceiling at delta = 1, the most any coupling can do without reversing the phantom, applied as
     an isotropic kick through AT1's loss-cone retention in three readings -- at the natural scale y = 1, at AT1's
     flagship-passing y_v = 0.1, and an upper bound giving every element entering y_v = 0.1 the full hill height -- with B1's
     reciprocal term (the phantom multiplied by 1 - delta ret where a fraction ret of the halo stays), both footings) clears
     no flagship host: the z = 2.5 zero point stays > 0.10 dex.
  C2-C7 (reported) the same mechanism, with the reciprocal term wherever the machinery can carry it, on X-COP, the z = 0
     galaxies, KiDS (without it: L352's lens model returns the total ESD), cosmic shear (MS3's halo model, with and without
     it), the forest and S_8, and Harvey (by proxy).  Controls: at delta = 0 the reciprocal formulas reproduce the committed
     cl_ratio, gal_shifts and R_of exactly.
  K1 THE KNIFE-EDGE, answered: the derived kick is a host-proportional distribution, below escape in the galaxies and
     relatively largest in the deepest wells; it neither lands in 575-675 where the flagship needs it nor widens the window.
  W  the ledger of the links this lane settles.
HISTORY (stated): the lane was first rooted in THE_COMPLETION's AeST action (the bump A B(Y/a0^2)(Q - Q0)^2); the coordinator's
  redirect re-rooted it in the ungated C-H/K core before any committed run.  The integral form of B1's bound replaced a local
  estimate after a scratch probe showed the halo outskirts dominate it; the reciprocal term was added to the gate scores after a
  low-N smoke run showed it decides X-COP and the z = 0 galaxies.  C4's expectation ("the kept halos are rejected") came from
  that low-N smoke run (+8.8/+13.8) and is recorded, not reworded, where the committed orbit count falsifies it.
MUTATE=1 (both flips are load-bearing): (i) the clock is given a k-essence term P(X) = mu^2 (sqrt(X) - Q0)^2 / 2 (THE_COMPLETION's
  Q-sector transplanted onto the clock's own rate), so its FRW action depends on tau-dot and A1 must FAIL; (ii) the kick is
  the hand-set universal 600 km/s at y_v = 0.1 with no reciprocal term (AT1's A2 cell), so the flagship passes and C1 must
  FAIL.  rc = 1.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP4_kick_from_action.py
"""
import os, sys, io, re, json, math, time, contextlib, warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")                                   # shared machine: at most two workers
for _v in ("AT1_THREADS", "AT3_THREADS", "L357_THREADS"):
    os.environ[_v] = "2"
import numpy as np
import sympy as sp
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FP4_FAST", "0") == "1"                        # smoke test only (fewer orbits); never committed
SLUG = "FP4_kick_from_action" + ("_MUTATE" if MUTATE else "")
T0 = time.time()
NW = 2
OUT = {"lane": "FP4", "mutate": MUTATE, "fast": FAST, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def rd(rel):
    return json.load(open(os.path.join(REPO, rel)))


def elapsed():
    return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: (i) the clock gets P(X) -- A1 must FAIL; (ii) the kick is the hand-set 600 km/s at y_v = 0.1 with no "
      "reciprocal term -- C1 must FAIL ***")

# ------------------------------------------------------------------------------------------------ both footings (FP0's inputs)
c_SI, G_SI = 299792458.0, 6.67430e-11
C_KMS = c_SI / 1e3
MPC_M = 3.0856775814913673e22
MSUN = 1.98847e30
H0_SI = 67.4e3 / MPC_M
OM_L = 0.6847
RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
A0_FP0 = {"canonical": 0.5 * c_SI * math.sqrt(G_SI * OM_L * RHO_CRIT), "alt": 0.5 * c_SI * math.sqrt(G_SI * RHO_CRIT)}
OUT["numbers"]["a0_FP0"] = A0_FP0

# ================================================================================================ the committed machinery
banner("LOADING the committed lanes' machinery (read-only exec; nothing is edited)")
_env_mut, _env_fast = os.environ.get("MUTATE"), os.environ.get("FAST")
os.environ["MUTATE"], os.environ["FAST"] = "0", ("1" if FAST else "0")   # the loaded lanes' own controls stay off
PA3 = os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT3_acceleration_trigger_full_gates.py")
_s3 = open(PA3).read()
_h3 = _s3.split("# ================================================================================================ C1 control")[0]
_h3 = _h3.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
A3 = {"__name__": "at3", "__file__": PA3}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_h3, A3)
A1, L57, Lm = A3["A1"], A3["L57"], A3["Lm"]
retained_acc, r_trigger, r_v_profile = A3["retained_acc"], A3["r_trigger"], A3["r_v_profile"]
flagship_rows, xcop_from_eps, gal_shifts, kids_switched = A3["flagship_rows"], A3["xcop_from_eps"], A3["gal_shifts"], A3["kids_switched"]
hernquist, nfw21, FB, GK = A3["hernquist"], A3["nfw21"], A3["FB"], A3["GK"]
FOOT, A0K = A3["FOOT"], A3["A0K"]
CL, CLREF, cl_mass_fn, GAL = A3["CL"], A3["CLREF"], A3["cl_mass_fn"], A3["GAL"]
M200_KIDS, c200_55, RHOC_ZL, ZL, LOGMS = A3["M200_KIDS"], A3["c200_55"], A3["RHOC_ZL"], A3["ZL"], A3["LOGMS"]
RHO_C0, c200_z0, RHOC0_KPC, Ez2 = A3["RHO_C0"], A3["c200_z0"], A3["RHOC0_KPC"], A3["Ez2"]
galaxy_baryons, Re_kpc, halo_mass, c200_20, g_nfw = A1["galaxy_baryons"], A1["Re_kpc"], A1["halo_mass"], A1["c200_20"], A1["g_nfw"]
nu20, nu_mono_bk1, G20, KPC20 = A1["nu20"], A1["nu_mono"], A1["G20"], A1["KPC"]
trig_acc, I_ES, CG, XVG, UGR, nfw_phi = A1["trig_acc"], A1["I_ES"], A1["CG"], A1["XVG"], A1["UGR"], A1["nfw_phi"]
MH_h, hh, SIG0, DG, f_st, b_st, DC, trap = A1["MH"], A1["h"], A1["SIG0"], A1["DG"], A1["f_st"], A1["b_st"], A1["DC"], A1["_trap"]
c_dm14, MSUN20 = A1["c_dm14"], A1["MSUN"]
nu_core = L57["nu_mono"]                                             # the core's kernel (L340's nu_mono, as L357 builds it)


def nu_rar(y):
    return 1.0 / (-np.expm1(-np.sqrt(np.maximum(np.asarray(y, float), 1e-300))))


def nu_k(s):
    """the core's kernel: nu_mono, which equals nu_RAR's closed form for y <= 2.337 (XC4); the closed form avoids the table's
    clamp below y = 1e-12."""
    s = np.asarray(s, float)
    return np.where(s <= 2.0, nu_rar(s), np.asarray(nu_core(np.maximum(s, 1e-12)), float))


S8_LCDM = float(L57["S8_LCDM"])
P(f"  AT3's head (AT1, L357, L320, BK1, L321, L355, L360) loaded   {elapsed()}")
PMS3 = os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector.py")
MS = {"__name__": "ms3", "__file__": PMS3}
_ms = open(PMS3).read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_ms[:_ms.rindex("# ============================================================================================ C1 control")]
         .replace('P(__doc__.split("CHECKS")[0].strip())', "pass"), MS)
R_of, XLIN, A0_MS3 = MS["R_of"], MS["XLIN"], MS["A0"]
P(f"  MS3's halo model (L363, GP0) loaded: z = 0.5, common cell x_c,eff = {XLIN:.5f}   {elapsed()}")
if _env_mut is None: os.environ.pop("MUTATE", None)
else: os.environ["MUTATE"] = _env_mut
if _env_fast is None: os.environ.pop("FAST", None)
else: os.environ["FAST"] = _env_fast
FEET = ("canonical", "alt")
P(f"  footings: FP0 {A0_FP0['canonical']:.4e} / {A0_FP0['alt']:.4e} m/s^2; the machinery's {FOOT['canonical']:.4e} / {FOOT['alt']:.4e}")

# committed results this lane reads (inputs, not re-derived here; each is checked where it is used)
J = dict(
    L340out=open(os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion.out")).read(),
    L289out=open(os.path.join(REPO, "real_research", "clock_2026", "L289_carrier_requirements.out")).read(),
    AT1=rd("real_research/acceleration_trigger_2026/AT1_acceleration_trigger_highz_results.json")["numbers"],
    MS3=rd("real_research/mond_sector_gate_2026/MS3_cosmic_shear_bound_mond_sector_results.json")["numbers"],
    CV4=rd("real_research/chk_v0_2026/CV4_khronon_K_profile_results.json")["numbers"],
    FK1=rd("real_research/dark_fluid_kick_2026/FK1_kick_as_phase_change_results.json")["numbers"],
    FL1=rd("real_research/dark_fluid_2026/FL1_order_parameter_results.json"),
    XR8=rd("real_research/cross_thread_review_2026_09_26/XR8_nodes_and_polar_form_results.json"),
    L383=rd("real_research/condensate_dust_2026/L383_wave_field_zoom_in_results.json")["numbers"],
    L389=rd("real_research/dark_sector_2026/L389_harvey_same_cell_linear_gate_results.json")["numbers"],
    L390=rd("real_research/dark_sector_2026/L390_kids_resolved_linear_gate_results.json")["numbers"],
)

# ================================================================================================ C0 controls
banner("C0  CONTROLS: the loaded machinery reproduces committed numbers")
_s340 = J["L340out"]
_row = re.search(r"c_s \[km/s\] \(C = 1 / 10 / 100\):\s*(.*)", _s340).group(1)
L340_TABLE = {float(m.group(1)): [float(v) for v in m.group(2).split(",")]
              for m in re.finditer(r"c_2 = ([0-9.]+): ([0-9, ]+)", _row)}
_win = re.search(r"c_2 window:\s*([0-9.e+-]+) < c_2 < ([0-9.]+)", _s340)
C2_MIN, C2_MAX = float(_win.group(1)), float(_win.group(2))
FOREST_CS = float(re.search(r"the forest \(L185\) needs c_s\(z = 3\) <= ([0-9.]+) km/s", J["L289out"]).group(1))

# L340's own block, exec'd from its source, gives the clock's mode (this is A3's derivation; the control is its table)
_src340 = open(os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion.py")).read()
_blk = _src340[_src340.index("def block(C_, eps_, ac_, a2_=0, a3_=0, g_=0):"):_src340.index("M, S = block(C, eps, ac)")]
kS, CS, c2S, acS, wS = sp.symbols("k C c_2 alpha_c omega", real=True)
_ns340 = dict(sp=sp, k=kS, D=-sp.I * wS)
_ns340.update(dict(zip(("psi", "phi", "beta", "U", "R"), sp.symbols("psi phi beta U R"))))
exec(_blk, _ns340)
block340 = _ns340["block"]
_M0, _ = block340(CS, -c2S, 0)
_detp = sp.Poly(sp.expand(_M0.det()), wS)
_cf = {j: _detp.coeff_monomial(wS ** j) for j in range(0, 5)}
W2_mode = sp.simplify(-_cf[0] / _cf[2]) if _cf[4] == 0 else None    # alpha_c = 0: one root in omega^2
cs2_formula = sp.simplify(W2_mode / kS ** 2) if W2_mode is not None else None
_cs_num = lambda c2v, Cv: C_KMS * math.sqrt(float(cs2_formula.subs({c2S: c2v, CS: Cv})))
dev340 = max(abs(_cs_num(c2v, Cv) - ref) / ref for c2v, row in L340_TABLE.items() for Cv, ref in zip((1.0, 10.0, 100.0), row))
check("C0a CONTROL: L340's printed khronon mode speeds (c_2 = 0.00729/0.03/0.0667, C = 1/10/100) are reproduced from L340's own "
      "block (exec'd from its source), within the table's rounding",
      f"omega^2/k^2 = {cs2_formula}; max relative deviation {dev340:.1e} over {sum(len(v) for v in L340_TABLE.values())} entries",
      cs2_formula is not None and dev340 < 2e-3, load_bearing=False)

Lm["A0"] = A0K["canonical"]                                          # AT1's committed run used L321's canonical module value
_ctl = flagship_rows(2.5, 0.1, 600.0, mufacs=(1.0,), feet=("canonical",), lMbs=(10.5,), N=(1500 if FAST else 10000))
_ref = [r_ for r_ in J["AT1"]["A2"]["0.1|600.0|2.5"]["rows"] if r_["footing"] == "canonical" and r_["logMb"] == 10.5
        and abs(r_["mu_fac"] - 1.0) < 1e-9]
dev_at1 = max(abs(a_["shift"] - b_["shift"]) for a_, b_ in zip(sorted(_ctl, key=lambda d: d["kernel"]), sorted(_ref, key=lambda d: d["kernel"])))
check("C0b CONTROL: the loaded retention and flagship machinery reproduces AT1's committed z = 2.5 row (y_v 0.1, v_A 600 km/s, "
      "canonical, M_b 1e10.5, central gas, both kernels)",
      f"shift {[round(r_['shift'], 6) for r_ in _ctl]} vs AT1 {[round(r_['shift'], 6) for r_ in _ref]}; max |dev| {dev_at1:.1e} dex"
      + (" (FAST: fewer orbits, not the committed N)" if FAST else ""), dev_at1 < (5e-2 if FAST else 1e-9), load_bearing=False)
_one = lambda M: 1.0
dev_ms3 = max(abs(max(R_of(XLIN, A0_MS3[f_], 1.75, "door", _one)[0].values()) - J["MS3"]["K1"]["1.75"]["intact"][f_]) for f_ in FEET)
check("C0c CONTROL: MS3's committed intact-carrier cosmic-shear row (1.75 Mpc cap, door convention, both footings) is reproduced",
      f"max |dev| {dev_ms3:.1e}", dev_ms3 < 1e-9, load_bearing=False)
OUT["numbers"]["controls"] = dict(L340_dev=dev340, AT1_dev=dev_at1, MS3_dev=dev_ms3)
P(f"  controls done   {elapsed()}")

# ================================================================================================ A1 the clock carries no charge
banner("A1  THE CLOCK CARRIES NO CONSERVED CHARGE: no condensate dust can be made of the clock")
p = sp.symbols("p0:4", real=True)
Xm = p[0] ** 2 - p[1] ** 2 - p[2] ** 2 - p[3] ** 2                    # X = -eta^{mn} p_m p_n, eta = diag(-1, 1, 1, 1)
n_low = [-p[i] / sp.sqrt(Xm) for i in range(4)]
contraction = [sp.simplify(sum(n_low[m] * sp.diff(n_low[nu], p[m]) for m in range(4))) for nu in range(4)]
pointwise_zero = all(cz == 0 for cz in contraction)
lam_ = sp.symbols("lambda", positive=True)                          # tau -> F(tau): d tau -> F'(tau) d tau
n_scaled = [-(lam_ * p[i]) / sp.sqrt(lam_ ** 2 * Xm) for i in range(4)]
relabel_inv = all(sp.simplify(a_ - b_) == 0 for a_, b_ in zip(n_scaled, n_low))
# FRW with tau = f(t): the clock's normal, expansion and acceleration from the metric (Christoffels computed here)
tt = sp.symbols("t", real=True)
Nf, af = sp.Function("N", positive=True)(tt), sp.Function("a", positive=True)(tt)
fp = sp.symbols("f_p", positive=True)                                # f'(t) > 0: the clock rate
xs = sp.symbols("x1:4", real=True)
crd = [tt, *xs]
gF = sp.diag(-Nf ** 2, af ** 2, af ** 2, af ** 2); giF = gF.inv()
X_frw = sp.simplify(-giF[0, 0] * fp ** 2)
n0 = sp.simplify(-fp / sp.sqrt(X_frw))
nL = sp.Matrix([n0, 0, 0, 0]); nU = giF * nL
sqg = sp.sqrt(-gF.det())
K_frw = sp.simplify(sum(sp.diff(sqg * nU[m], crd[m]) for m in range(4)) / sqg)
Gam = [[[sp.simplify(sum(giF[l, s] * (sp.diff(gF[s, m], crd[nn]) + sp.diff(gF[s, nn], crd[m]) - sp.diff(gF[m, nn], crd[s]))
                         for s in range(4)) / 2) for nn in range(4)] for m in range(4)] for l in range(4)]
cov_n = [[sp.diff(nL[m], crd[nn]) - sum(Gam[l][nn][m] * nL[l] for l in range(4)) for m in range(4)] for nn in range(4)]
acc = [sp.simplify(sum(nU[nn] * cov_n[nn][m] for nn in range(4))) for m in range(4)]
acc2 = sp.simplify(sum(giF[m, m] * acc[m] ** 2 for m in range(4)))
alc, c2x, mu_, Q0_ = sp.symbols("alpha_c c_2 mu Q_0", positive=True)
L_clock = alc * acc2 - c2x * (K_frw - K_frw) ** 2                    # the leaf average <K>_h = K on a homogeneous leaf
L_plain = alc * acc2 - c2x * K_frw ** 2                              # without the leaf average (L350's control)
if MUTATE:
    L_clock = L_clock + mu_ ** 2 * (sp.sqrt(X_frw) - Q0_) ** 2 / 2   # MUTATE (i): a k-essence P(X) on the clock's own rate
dLdfp = sp.simplify(sp.diff(L_clock, fp)); dLplain = sp.simplify(sp.diff(L_plain, fp))
# contrast: AeST's Q-sector (an independent aether A^m = (1/N, 0, 0, 0)): Q = phi-dot / N, rho = Q K'(Q) - K
Qs, Ms_, us = sp.symbols("Q M u", positive=True)
Kq = -Ms_ ** 4 + mu_ ** 2 * (Qs - Q0_) ** 2 / 2
rho_Q = sp.expand((Qs * sp.diff(Kq, Qs) - Kq).subs(Qs, Q0_ + us))
aest_dust = sp.simplify(sp.diff(rho_Q, us).subs(us, 0))
ok_a1 = pointwise_zero and relabel_inv and sp.simplify(sp.diff(n0, fp)) == 0 and dLdfp == 0 and dLplain == 0 \
        and all(a_ == 0 for a_ in acc) and aest_dust != 0
P(f"    n_m dn_n/d(d_m tau) = {contraction}   (the clock's first-derivative current has no density along n)")
P(f"    n_m(F' d tau) = n_m(d tau): {relabel_inv}.  FRW: n_0 = {n0}, K = {K_frw}, a_m = {acc}")
P(f"    dL_clock/d(tau-dot) = {dLdfp} (with the leaf average), {dLplain} (plain -c_2 K^2)"
  + ("   <- MUTATE: P(X) added" if MUTATE else ""))
P(f"    contrast, AeST's independent aether: rho(Q0 + u) = {rho_Q};  d rho/du at u = 0 = {aest_dust} (a dust)")
check("A1 DERIVED: the clock carries no conserved charge -- n_m dn_n/d(d_m tau) = 0 identically, n is invariant under tau -> F(tau), "
      "and on FRW the clock's whole action is independent of the clock rate, so no condensate dust can be made of it "
      "(AeST's independent aether, by contrast, gives rho = Q0 mu^2 u)",
      f"contraction {contraction}; FRW dL/d(tau-dot) = {dLdfp} / {dLplain}; AeST d rho/du = {aest_dust}", ok_a1,
      "C-H/K's clock is its own aether (n is built from tau), so Q = n.d tau = sqrt(X) is pure gauge: THE_COMPLETION's K(Q) dust "
      "has no analogue in the core")
OUT["numbers"]["A1"] = dict(contraction=[str(v) for v in contraction], K=str(K_frw), acc=[str(v) for v in acc],
                            dL=str(dLdfp), dL_plain=str(dLplain), aest=str(aest_dust))

# ================================================================================================ A2 the auxiliaries are constrained
banner("A2  U, W, L AND lambda_0 ARE CONSTRAINED: no normal derivative, zero kinetic Hessian (lapse and shift kept)")
x1, zz = sp.symbols("x z", real=True)
N2 = sp.Function("N", positive=True)(tt, x1); b2 = sp.Function("beta")(tt, x1); gm2 = sp.Function("gamma", positive=True)(tt, x1)
U2 = sp.Function("U")(tt, x1); W2 = sp.Function("W")(tt, x1, zz); Wb2 = sp.Function("W_b")(tt, x1)
L2 = sp.Function("L")(tt, x1, zz); l02 = sp.Function("lambda0")(tt, x1); W02 = sp.Function("W_0")(tt, x1)
g2 = sp.Matrix([[-N2 ** 2 + gm2 * b2 ** 2, gm2 * b2], [gm2 * b2, gm2]]); gi2 = sp.simplify(g2.inv())
nl2 = sp.Matrix([-N2, 0]); nu2 = sp.simplify(gi2 * nl2)
hup = sp.simplify(gi2 + nu2 * nu2.T)
hmix = sp.simplify(sp.eye(2) + (gi2 * nl2) * nl2.T).T                 # h_m^n = delta_m^n + n_m n^n
lnN = sp.log(N2)
a2v = hmix * sp.Matrix([sp.diff(lnN, tt), sp.diff(lnN, x1)])         # a_m = h_m^n d_n ln N
dU2 = sp.Matrix([sp.diff(U2, tt), sp.diff(U2, x1)])
dWb = sp.Matrix([sp.diff(Wb2, tt), sp.diff(Wb2, x1)])
qfun = sp.Function("q")
al_ = sp.symbols("alpha", positive=True)
lap_h = sp.diff(sp.sqrt(gm2) * sp.diff(W2, x1) / gm2, x1) / sp.sqrt(gm2)   # the intrinsic leaf Laplacian (1-D leaf)
dens = N2 * sp.sqrt(gm2) * (2 * ((dU2 - a2v).T * hup * (dU2 - a2v))[0, 0] + 2 * al_ ** 2 * qfun((dWb.T * hup * dWb)[0, 0] / al_ ** 2)
                            + L2 * (sp.diff(W2, zz) - lap_h) + l02 * (W02 - U2))
vel = [sp.Derivative(U2, tt), sp.Derivative(Wb2, tt), sp.Derivative(W2, tt), sp.Derivative(L2, tt), sp.Derivative(l02, tt)]
grads = [sp.simplify(sp.diff(dens, v_)) for v_ in vel]
H_aux = sp.Matrix([[sp.simplify(sp.diff(gr, v2)) for v2 in vel] for gr in grads])
ok_a2 = all(gr == 0 for gr in grads) and H_aux == sp.zeros(len(vel)) and sp.simplify(hup[0, 0]) == 0 and sp.simplify(hup[0, 1]) == 0
P(f"    h^tt = {sp.simplify(hup[0, 0])}, h^tx = {sp.simplify(hup[0, 1])}, h^xx = {sp.simplify(hup[1, 1])}  (lapse N, shift beta, leaf metric gamma)")
P(f"    d(density)/d(U_t, W_b,t, W_t, L_t, lambda0_t) = {grads}")
check("A2 DERIVED: U, W, L and lambda_0 are constrained -- with lapse and shift kept, h^{tt} = h^{tx} = 0, their normal derivatives "
      "never enter the action, and the kinetic Hessian of the auxiliaries is identically zero",
      f"h^tt {sp.simplify(hup[0, 0])}, h^tx {sp.simplify(hup[0, 1])}; first derivatives {grads}; Hessian zero {H_aux == sp.zeros(len(vel))}",
      ok_a2, "they are fixed leaf by leaf by the metric, the clock and the matter (ACTION.md: W forward in z, L backward, no free "
      "endpoint function): they can hold no state of their own")

# ================================================================================================ A3 the clock's one mode
banner("A3  THE CLOCK'S ONE MODE: gapless, radiation-like and fast -- it cannot be the cold dust")
kk2 = sp.symbols("k2", positive=True)
Mk, _ = block340(CS, -c2S, 0)
detk = sp.Poly(sp.expand(Mk.det()), wS)
cfk = {j: detk.coeff_monomial(wS ** j) for j in range(0, 5)}
w2k = sp.simplify(-cfk[0] / cfk[2])
gapless = sp.simplify(sp.diff(w2k / kS ** 2, kS)) == 0 and sp.limit(w2k, kS, 0) == 0
formula_ok = sp.simplify(w2k / kS ** 2 - c2S / (CS * (2 + 3 * c2S))) == 0
_Ma, _ = block340(CS, -c2S, acS)                                      # alpha_c > 0: still one mode, still gapless
_dpa = sp.Poly(sp.expand(_Ma.det()), wS)
cfa = {j: _dpa.coeff_monomial(wS ** j) for j in range(0, 5)}
w2a = sp.simplify(-cfa[0] / cfa[2])
homog = cfa[4] == 0 and cfa[3] == 0 and cfa[1] == 0 and sp.simplify(sp.diff(w2a / kS ** 2, kS)) == 0
ratio_kin = sp.simplify(kS * sp.diff(sp.sqrt(c2S / (CS * (2 + 3 * c2S))) * kS, kS) / (sp.sqrt(c2S / (CS * (2 + 3 * c2S))) * kS))
p_over_rho = sp.Rational(1, 3) * ratio_kin                            # kinetic theory: p = (1/3) Int f k d(omega)/dk, rho = Int f omega
cs_min = _cs_num(C2_MIN, 100.0)
C_star = C2_MIN * C_KMS ** 2 / (FOREST_CS ** 2 * (2 + 3 * C2_MIN))
y_star = math.log(1 + 1 / C_star) ** 2                               # nu_RAR(y) - 1 = C*  (closed form; = nu_mono there)
ok_a3 = formula_ok and gapless and homog and p_over_rho == sp.Rational(1, 3) and cs_min > 100 * FOREST_CS
P(f"    L340's block, alpha_c = 0: omega^2 = {w2k}  (= c_2 k^2/(C(2 + 3 c_2)): {formula_ok}); gapless (omega -> 0 as k -> 0, "
  f"omega/k independent of k): {gapless}")
P(f"    alpha_c > 0: det has only omega^0 and omega^2 terms (one mode), omega^2 = {w2a}: omega/k independent of k: {homog}")
P(f"    a gas of its quanta: k omega'(k)/omega(k) = {ratio_kin} -> p/rho = {p_over_rho} exactly (rho ~ a^-4)")
P(f"    L340's window c_2 in ({C2_MIN:.2e}, {C2_MAX:.3f}): slowest mode where C <= 100 moves at {cs_min:.0f} km/s; the forest needs "
  f"c_s(z = 3) <= {FOREST_CS} km/s (L289/L185): {cs_min / FOREST_CS:.0f}x too fast.  Slow enough only where C >= {C_star:.2e}, "
  f"i.e. y_b <= {y_star:.1e}")
check("A3 DERIVED: the clock's one propagating mode is gapless, omega^2 = c_2 k^2/(C(2 + 3 c_2)) (L340's own block), so a gas of "
      "its quanta has p = rho/3 exactly (radiation, not the a^-3 dust the CMB needs) and moves at >= 1800 km/s wherever C <= 100 "
      "in L340's window -- >= 100x the forest's cold bound",
      f"p/rho = {p_over_rho}; slowest speed {cs_min:.0f} km/s vs forest {FOREST_CS} km/s (x{cs_min / FOREST_CS:.0f}); needs "
      f"C >= {C_star:.1e} (y_b <= {y_star:.1e}) to be cold", ok_a3,
      "the clock also has no conserved charge (A1) and no discrete vacua or winding (its field space is a line), so it has no "
      "Q-balls or topological lumps either: no massive, cold state of the clock exists")
OUT["numbers"]["A3"] = dict(omega2=str(w2k), omega2_alpha_c=str(w2a), p_over_rho=str(p_over_rho), cs_min_kms=cs_min,
                            forest_cs=FOREST_CS, C_star=C_star, y_star=y_star, c2_window=[C2_MIN, C2_MAX])

# ================================================================================================ A4 the metric's cold state
banner("A4  THE METRIC'S OWN COLD STATE (primordial black holes): not kernel-invisible, not kickable")
A4 = {}
for f_ in FEET:
    Lm["A0"] = A0K[f_]
    xr = float(np.median([Lm["cl_ratio"](c_, 1.0, "universal") for c_ in CL]))
    gs = {k_: Lm["gal_shift"](GAL[k_], 1.0, "universal") for k_ in GAL}
    A4[f_] = dict(xcop_ratio=xr, gal_shift=gs)
Lm["A0"] = A0K["canonical"]
_rows_pbh = flagship_rows(2.5, 0.1, 0.0, mufacs=(1.0,), ratio_override=1.0)
A4["flagship_min"] = min(r_["shift"] for r_ in _rows_pbh)
ok_a4 = all(abs(A4[f_]["xcop_ratio"] - 1) > 0.2 and max(A4[f_]["gal_shift"].values()) > 0.06 for f_ in FEET) and A4["flagship_min"] > 0.10
for f_ in FEET:
    P(f"    {f_:9s}: X-COP median M_dyn/M_HSE with the full halo, universal coupling {A4[f_]['xcop_ratio']:.2f} (gate 0.8-1.2); "
      f"galaxy shifts {', '.join(f'{k_} {v_:+.3f}' for k_, v_ in A4[f_]['gal_shift'].items())} dex (gate 0.06)")
P(f"    flagship at z = 2.5 with the halo retained (additive reading, a LOWER bound for a source of u): min shift {A4['flagship_min']:+.2f} dex")
check("A4 the metric's own cold state (PBHs) is cold and multistreams, but it sources u like any matter (not kernel-invisible) and "
      "has no internal energy to convert (not kickable): with its full halo it fails X-COP, the galaxy gate and the flagship",
      f"X-COP {A4['canonical']['xcop_ratio']:.2f}/{A4['alt']['xcop_ratio']:.2f}; worst galaxy shift "
      f"{max(A4['canonical']['gal_shift'].values()):+.3f}/{max(A4['alt']['gal_shift'].values()):+.3f} dex; flagship >= {A4['flagship_min']:+.2f} dex",
      ok_a4, "L321: a carrier that sources the MOND field overshoots the clusters; the flagship needs the carrier gone from galaxies")
OUT["numbers"]["A4"] = A4

# ================================================================================================ A5 verdict A and the minimal addition
banner("A5  VERDICT A: no state of the core's fields is the dust; the minimal addition and its cost")
fl1_f1 = [v_["ok"] for k_, v_ in J["FL1"]["checks"].items() if k_.startswith("F1")]
xr8 = J["XR8"]["numbers"] if "numbers" in J["XR8"] else J["XR8"]
first_nodes = [xr8["census"][k_]["first_node_over_tsc"] for k_ in xr8["census"] if xr8["census"][k_].get("tracks")
               and xr8["census"][k_].get("first_node_over_tsc") is not None]
node_counts = xr8["C1"]
Cfl = J["L383"]["C"]
floors = [v_ for k_, d_ in Cfl.items() if k_.startswith("sigma_dm") for kk_, v_ in d_.items() if kk_.startswith("framework")]
ok_a5 = ok_a1 and ok_a2 and ok_a3 and ok_a4 and all(fl1_f1) and len(first_nodes) > 0 and min(floors) > 1e-19
P(f"    FL1 F1 (committed): V0's scalar block has one propagating mode, the clock: {all(fl1_f1)}")
P(f"    XR8 (committed): every multistreaming continuum's phase winds at nodes -- first node at {min(first_nodes):.3f}-"
  f"{max(first_nodes):.3f} t_sc; converged counts {node_counts}: the phase cannot be the clock")
P(f"    L383 (committed): the wave field's mass floor with the framework's clearing, {min(floors):.2e}-{max(floors):.2e} eV")
check("A5 VERDICT A: no state of the core's fields (metric, clock, U, W, L, lambda_0) can be the cosmological dust or the clusters' "
      "missing mass; the minimal addition is ONE nearly free complex scalar (two real propagating fields) with ONE mass "
      "m >= 1.9-5.2e-19 eV, its amount initial data, kernel-invisible through L353's constrained pair (no new constant)",
      f"A1-A4 {ok_a1 and ok_a2 and ok_a3 and ok_a4}; FL1 F1 {all(fl1_f1)}; XR8 nodes from {min(first_nodes):.2f} t_sc; "
      f"L383 floor {min(floors):.1e}-{max(floors):.1e} eV", ok_a5,
      "the cost: one field (2 real d.o.f.) and one constant (m), plus the amount as an initial condition -- the record's FL1 order "
      "parameter; the requirement 'no new particle species' holds only in the sense XR8 states (a classical field at occupation ~1e77)")

# ================================================================================================ B1 reciprocity
banner("B1  RECIPROCITY: the dark coupling that pushes also rewrites the phantom where the dark state sits")
r = sp.symbols("r", positive=True)
Gs, a0s = sp.symbols("G a_0", positive=True)
u_ = sp.Function("u")(r); Ph = sp.Function("Phi")(r)
rho_ = sp.Function("rho")(r); rhod_ = sp.Function("rho_d")(r)
qf, Vf = sp.Function("q"), sp.Function("V")
I_ = sp.diff(u_, r) ** 2 / a0s ** 2
Lag = r ** 2 * (-rho_ * Ph - (2 * sp.diff(Ph, r) * sp.diff(u_, r) - sp.diff(u_, r) ** 2 - a0s ** 2 * qf(I_)) / (8 * sp.pi * Gs)
                - rhod_ * Vf(I_))
p_u = sp.diff(Lag, sp.diff(u_, r))                                    # u is cyclic: r^2 x (this / r^2) = const = 0 (regular centre)
Phi_p = sp.solve(sp.Eq(p_u, 0), sp.diff(Ph, r))[0]
qprime = sp.diff(qf(I_), sp.diff(u_, r)) / sp.diff(I_, sp.diff(u_, r))
Vprime = sp.diff(Vf(I_), sp.diff(u_, r)) / sp.diff(I_, sp.diff(u_, r))
delta_ = 8 * sp.pi * Gs * rhod_ * Vprime / (a0s ** 2 * qprime)
claimed = sp.diff(u_, r) * (1 + qprime * (1 - delta_))
res_b1 = sp.simplify(Phi_p - claimed)
EL_Phi = sp.simplify(sp.diff(sp.diff(Lag, sp.diff(Ph, r)), r) - sp.diff(Lag, Ph))
poisson = sp.simplify(EL_Phi - (rho_ * r ** 2 - sp.diff(r ** 2 * sp.diff(u_, r), r) / (4 * sp.pi * Gs)))
ok_b1 = res_b1 == 0 and poisson == 0
P(f"    u-equation (first integral, regular centre): Phi' = {sp.simplify(Phi_p)}")
P(f"    = u' [1 + q'(I)(1 - delta)],  delta = 8 pi G rho_d V'(I)/(a0^2 q'(I)):  residual {res_b1};  Phi-equation: grad^2 u = 4 pi G rho "
  f"(residual {poisson}), unchanged")
check("B1 DERIVED (reciprocity): varying u in I_NR - rho_d V(I) multiplies the phantom's coefficient q'(I) = nu - 1 by (1 - delta) "
      "wherever the dark state sits, delta = 8 pi G rho_d V'(I)/(a0^2 (nu - 1)); the energy per unit mass the coupling can hand "
      "over is therefore V <= delta (a0^2/8 pi G) Int q'(I)/rho_d dI, and delta >= 1 reverses the phantom",
      f"residual {res_b1}; Poisson residual {poisson}", ok_b1,
      "the same term that pushes the dark state out screens (delta < 1) or reverses (delta > 1) the MOND phantom around it: a hill "
      "strong enough to unbind a halo must first switch the host's MOND off")

# ================================================================================================ B2 the clock's acceleration
banner("B2  A COUPLING TO THE CLOCK'S ACCELERATION reads the NR multiplier Phi: the constraint turns singular")
kq, rd_, Aq, Bq = sp.symbols("k rho_d A B", real=True)
dPh, du_ = sp.symbols("dPhi du", real=True)
L2q = -(2 * kq ** 2 * dPh * du_ - kq ** 2 * (1 + Bq) * du_ ** 2) / (8 * sp.pi * Gs) - rd_ * Aq * kq ** 2 * dPh ** 2 / a0s ** 2
Hq = sp.hessian(L2q, (dPh, du_))
detq = sp.factor(Hq.det())
det_nocoup = sp.simplify(detq.subs(rd_, 0))
A_zero = sp.solve(sp.Eq(detq, 0), Aq)
Iv, th, Vm = sp.symbols("I theta V_m", positive=True)
Vthr = Vm * Iv / (1 + Iv)                                             # a threshold (step) coupling at the natural scale I = 1
A_dir = sp.simplify(sp.diff(Vthr, Iv) + 2 * sp.diff(Vthr, Iv, 2) * Iv * sp.cos(th) ** 2)
neg_at = sp.solve(sp.Eq(sp.simplify(A_dir.subs(th, 0) * (1 + Iv) ** 3 / Vm), 0), Iv)
ok_b2 = (sp.diff(det_nocoup, Bq) == 0 and det_nocoup != 0 and len(A_zero) == 1
         and sp.simplify(A_zero[0] + a0s ** 2 / (8 * sp.pi * Gs * rd_ * (1 + Bq))) == 0 and neg_at == [sp.Rational(1, 3)])
P(f"    (Phi, u) quadratic block with the coupling -rho_d V(|grad Phi|^2/a0^2), A = V' + 2 V'' I cos^2(theta):")
P(f"    det = {detq};  without the coupling det = {det_nocoup} (kernel-independent: CV3's multiplier rule)")
P(f"    det = 0 at A = {A_zero};  threshold coupling V = V_m I/(1 + I): A(theta = 0) = {sp.simplify(A_dir.subs(th, 0))}, negative for I > {neg_at}")
check("B2 DERIVED: a dark coupling to the clock's acceleration reads the NR multiplier Phi -- the (Phi, u) constraint determinant, "
      "kernel-independent without it (CV3's rule), acquires a zero at 8 pi G rho_d A (1 + B)/a0^2 = -1, and a threshold coupling "
      "has A < 0 along the field for I > 1/3: the constraint turns singular at O(1) strength, before the coupling can kick",
      f"det {detq}; zero at A = {A_zero[0] if A_zero else None}; A < 0 for I > {neg_at}", ok_b2,
      "the same obstruction CV3 found for a gate reading a multiplier; below it, the energy bound is B1's with the Newtonian "
      "coefficient in place of the phantom's")

# ================================================================================================ B3 the clock's expansion
banner("B3  A COUPLING TO THE CLOCK'S EXPANSION K is spatially blind; its kick speed is a constant of the added field")
cv4_rows = J["CV4"]["K3"]["rows"]
max_dK = max(r_["dK_over_3H"] for r_ in cv4_rows)
vv, epsS, mS = sp.symbols("v epsilon m", positive=True)
mH2, mL2 = mS ** 2 + epsS, mS ** 2 - epsS                            # eps Re(Phi^2) splits m^2 -> m^2 +/- eps
v_pair = sp.sqrt(1 - mL2 / mH2)                                      # 2 m_H = 2 gamma m_L (at rest), c = 1
eps_of_v = sp.solve(sp.Eq(v_pair, vv), epsS)[0]
ident = sp.simplify(eps_of_v / mS ** 2 - vv ** 2 / (2 - vv ** 2)) == 0
fk1 = J["FK1"]["K2"]["eps_over_m2"]
dev_fk1 = max(abs(float((vv ** 2 / (2 - vv ** 2)).subs(vv, float(k_) / C_KMS)) / v_ - 1) for k_, v_ in fk1.items())
ok_b3 = max_dK <= 5e-3 and ident and dev_fk1 < 1e-6
P(f"    CV4 (committed): largest |K/3H - 1| at the edges of bound regions {max_dK:.2e} over {len(cv4_rows)} rows: K is a clock of time, not of place")
P(f"    two-body kinematics: eps/m^2 = {sp.simplify(eps_of_v / mS ** 2)} = v^2/(2 - v^2): {ident};  FK1's committed eps/m^2 "
  f"{ {k_: f'{v_:.3e}' for k_, v_ in fk1.items()} } reproduced to {dev_fk1:.1e}")
check("B3 DERIVED + LOADED: a coupling to K cannot push the dark state out of a bound region (K = 3H to <= 4.8e-3 there, CV4), and a "
      "K-gated conversion's speed is the mass splitting, eps/m^2 = v^2/(2c^2 - v^2): FK1's 1.84-2.35e-6 for 575-650 km/s is a "
      "constant of the added field, not of the core", f"max |K/3H - 1| {max_dK:.1e}; identity {ident}; FK1 match {dev_fk1:.1e}", ok_b3,
      "the clock can PAY for a kick (FL2 V3) and can TIME it, but it cannot set its speed or its place")

# ================================================================================================ B4 the ceiling is the BTFR speed
banner("B4  THE CEILING IS THE FRAMEWORK'S OWN VELOCITY SCALE (deep-MOND limit, quasi-isothermal dark halo)")
sI, s1, rr_, vd, Mb_, dl, Rh = sp.symbols("s s' r v_d M_b delta R", positive=True)
# B1's bound, accumulated from the outside in: V(s) = delta (a0^2/8 pi G) Int_0^{s^2} q'(I')/rho(r(I')) dI', I' = s'^2,
# deep MOND q' = nu - 1 -> s'^(-1/2), the halo rho = v_d^2/(4 pi G r'^2) with r'^2 = G M_b/(a0 s')
integrand = s1 ** sp.Rational(-1, 2) * (4 * sp.pi * Gs * (Gs * Mb_ / (a0s * s1)) / vd ** 2) * 2 * s1
V_s = dl * a0s ** 2 / (8 * sp.pi * Gs) * sp.integrate(integrand, (s1, 0, sI))
v2cap = sp.simplify(2 * V_s)
ident_b4 = sp.simplify(v2cap.subs(sI, 1) - 4 * dl * Gs * Mb_ * a0s / vd ** 2) == 0
rt_ = sp.sqrt(Gs * Mb_ / a0s)
v2_r = sp.simplify(v2cap.subs(sI, Gs * Mb_ / (a0s * rr_ ** 2)))
ratio_esc = sp.simplify(v2cap.subs(sI, 1) / (2 * vd ** 2 * (1 + sp.log(Rh / rt_))))   # vs the truncated isothermal escape at r_t
P(f"    2 V_cap/(unit mass) = {v2cap}  (s = g_N/a0);  at radius r: {v2_r}")
P(f"    at the transition radius (s = 1): v_cap^2 = 4 delta (G M_b a0)/v_d^2: {ident_b4};  against the isothermal escape speed "
  f"(halo truncated at R): (v_cap/v_esc)^2 = {ratio_esc}")
check("B4 DERIVED: in the deep-MOND limit with a quasi-isothermal dark halo, B1's ceiling accumulated from the outside in is "
      "v_cap^2 = 4 delta (G M_b a0/v_d^2) (r_t/r): at the kernel's natural scale the framework's own velocity scale, "
      "v_cap(r_t) = 2 sqrt(delta) (G M_b a0)^(1/2)/v_d, appears as the CEILING of what the core can hand over, set by each "
      "host's own baryonic mass and falling as r^(-1/2) outside",
      f"v_cap^2(s) = {v2cap}; (v_cap/v_esc)^2 at r_t = {ratio_esc}", ident_b4,
      "with v_d ~ v_f it is ~2 sqrt(delta) (G M_b a0)^(1/4) against v_esc = v_d sqrt(2(1 + ln R/r_t)): host-proportional, like the "
      "escape speed, so it cannot select galaxies over clusters; B5 prices it on real halos")

# ================================================================================================ the ceiling on real halos
banner("B5  THE CEILING ON REAL HALOS (both footings): what delta each host needs to be unbound")


def nfw_rho(M200, c, rhoc, r):
    Mn, r200, rs = nfw21(M200, c, rhoc)
    rho_s = M200 / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c)))
    return rho_s / ((r / rs) * (1 + r / rs) ** 2), r200, rs


def ceiling(Mb_fn, M200, c, rhoc, a0k, r_on_fac=2.0, fb=None):
    """B1's ceiling for delta = 1 on this host: V_cap(r) = (a0^2/8 pi G) Int_r^{r_on} q'(I) |dI/dr'| / rho_d dr' [(km/s)^2],
    with rho_d the host's UNCLEARED dark halo (1 - f_b) NFW, continued past r200 (lower than the true infall: generous),
    I = s^2, s = G M_b(<r)/(r^2 a0) (the kernel's argument), q' = nu_mono(s) - 1.  Returns (grid, V_cap, v_esc_N, v_c_N)."""
    fb = FB if fb is None else fb
    rho_d, r200, rs = nfw_rho(M200, c, rhoc, 1.0)
    rr = np.geomspace(1e-2, r_on_fac * r200, 6000)
    rho_d = (1 - fb) * nfw_rho(M200, c, rhoc, rr)[0]
    s = GK * Mb_fn(rr) / rr ** 2 / a0k
    I = s ** 2
    qp = nu_k(s) - 1.0
    integ = qp * np.abs(np.gradient(I, rr)) / rho_d
    seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(rr)
    V = a0k ** 2 / (8 * math.pi * GK) * np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    Mn, _, _ = nfw21(M200, c, rhoc)
    Mtot = Mb_fn(rr) + (1 - fb) * Mn(np.minimum(rr, r200))                # the machinery's truncated halo + baryons
    g = GK * Mtot / rr ** 2
    seg_g = 0.5 * (g[1:] + g[:-1]) * np.diff(rr)
    Phi = -(np.concatenate([np.cumsum(seg_g[::-1])[::-1], [0.0]]) + GK * Mtot[-1] / rr[-1])
    return rr, V, np.sqrt(-2 * Phi), np.sqrt(g * rr)


def dreq(host, r):
    rr, V, ve, vc = host
    Vr, ver, vcr = (float(np.interp(r, rr, a_)) for a_ in (V, ve, vc))
    return max(ver ** 2 - vcr ** 2, 0.0) / (2 * Vr), math.sqrt(2 * Vr), ver


HOSTS = {}
for f_ in FEET:
    a0k, a0 = A0K[f_], FOOT[f_]
    for lMb in (10.0, 10.5, 11.0):                                    # GP5/AT1's flagship hosts at z = 2.5, central gas
        z = 2.5; Mb = 10 ** lMb; mu = 0.5 * ((1 + z) / 2) ** 2
        Mh = halo_mass(Mb / (1 + mu), z); c_ = float(c200_20(Mh, z)); rhoc = RHOC0_KPC * Ez2(z)
        a_h = Re_kpc(Mb / (1 + mu), z) / 1.8153
        r_F = math.sqrt(G20 * Mb * MSUN20 / (0.1 * a0)) / KPC20
        HOSTS[(f_, f"flagship 1e{lMb:g}")] = dict(Mb=Mb, a=a_h, M200=Mh, c=c_, rhoc=rhoc, z=z, r_F=r_F,
                                                  r_t=r_trigger(Mb, a_h, 1.0, a0k), r_v01=r_trigger(Mb, a_h, 0.1, a0k),
                                                  Mb_fn=hernquist(Mb, a_h))
    for b in range(4):                                                # the KiDS lenses at z = 0.25
        Mb = 1.3 * 10 ** LOGMS[b]; M200 = M200_KIDS[b]
        HOSTS[(f_, f"KiDS bin {b + 1}")] = dict(Mb=Mb, a=3.0, M200=M200, c=float(c200_55(M200)), rhoc=RHOC_ZL, z=ZL,
                                               r_F=math.sqrt(GK * Mb / (0.1 * a0k)), r_t=r_trigger(Mb, 3.0, 1.0, a0k),
                                               r_v01=r_trigger(Mb, 3.0, 0.1, a0k), Mb_fn=hernquist(Mb, 3.0))
    HOSTS[(f_, "X-COP ref")] = dict(Mb=CLREF["Mb"], a=None, M200=CLREF["M200"], c=CLREF["c"], rhoc=CLREF["rhoc"], z=CLREF["z"],
                                    r_F=CLREF["R500"], r_t=r_v_profile(cl_mass_fn, 1.0, a0k, rmax=5 * CLREF["R500"]),
                                    r_v01=r_v_profile(cl_mass_fn, 0.1, a0k, rmax=5 * CLREF["R500"]), Mb_fn=cl_mass_fn)
B5 = {}
for (f_, name), H in HOSTS.items():
    H["cap"] = ceiling(H["Mb_fn"], H["M200"], H["c"], H["rhoc"], A0K[f_])
    dF, vF, eF = dreq(H["cap"], H["r_F"]); dT, vT, eT = dreq(H["cap"], max(H["r_t"], 1e-2))
    vbtfr = (GK * H["Mb"] * A0K[f_]) ** 0.25
    B5[f"{f_}|{name}"] = dict(r_t=H["r_t"], r_F=H["r_F"], v_cap_rt=vT, v_esc_rt=eT, delta_req_rt=dT, v_cap_rF=vF, v_esc_rF=eF,
                              delta_req_rF=dF, v_btfr=vbtfr, v_cap_over_btfr_rt=vT / vbtfr)
for f_ in FEET:
    P(f"  {f_}:")
    for name in [n_ for (ff, n_) in HOSTS if ff == f_]:
        b_ = B5[f"{f_}|{name}"]
        P(f"    {name:15s} r_t {b_['r_t']:7.1f} kpc: ceiling {b_['v_cap_rt']:6.0f} km/s vs escape {b_['v_esc_rt']:6.0f} -> delta_req "
          f"{b_['delta_req_rt']:7.1f} | r_F {b_['r_F']:7.1f} kpc: ceiling {b_['v_cap_rF']:6.0f} vs escape {b_['v_esc_rF']:6.0f} -> delta_req "
          f"{b_['delta_req_rF']:7.1f} | (G M_b a0)^1/4 {b_['v_btfr']:6.0f} km/s")
fl_req = [B5[f"{f_}|flagship 1e{l_:g}"]["delta_req_rF"] for f_ in FEET for l_ in (10.0, 10.5, 11.0)]
cl_req = [B5[f"{f_}|X-COP ref"]["delta_req_rF"] for f_ in FEET]
anti = all(B5[f"{f_}|X-COP ref"]["delta_req_rF"] < min(B5[f"{f_}|flagship 1e{l_:g}"]["delta_req_rF"] for l_ in (10.0, 10.5, 11.0))
           for f_ in FEET)
ok_b5 = min(fl_req) > 1.0 and anti
check("B5 on real halos, both footings: every flagship host needs delta_req > 1 at the flagship radius (the phantom reversed around "
      "it) to be unbound, and the X-COP cluster needs LESS than any z = 2.5 galaxy -- the ordering is backwards (anti-selective)",
      f"flagship delta_req {min(fl_req):.1f}-{max(fl_req):.1f}; cluster (at R500) {min(cl_req):.1f}-{max(cl_req):.1f}", ok_b5,
      "delta = 1 is the hard ceiling: there the phantom is off wherever the uncleared dark state sits, and beyond it the phantom "
      "reverses.  A coupling strong enough to clear galaxies would clear clusters first -- the wrong order, as L320 found for kicks")
OUT["numbers"]["B5"] = B5

# ================================================================================================ B6 is the window predicted?
banner("B6  IS THE ~600 km/s WINDOW PREDICTED? the core's natural velocities, and the BTFR band")
hbar_eVs = 6.582119569e-16; eV_kg = 1.78266192e-36; PC_M = 3.0856775814913673e16
m_floor = min(floors)
xi_lo, xi_hi = 0.031, 0.1                                              # pc: the Solar-System floor (L340 S1) to the roadmap's upper value
hbar_SI = 1.054571817e-34
census = {}
for f_ in FEET:
    a0 = A0_FP0[f_]
    census[f_] = {
        "c sqrt(c_2) [c_2 window]": (C_KMS * math.sqrt(C2_MIN), C_KMS * math.sqrt(C2_MAX), "declared c_2"),
        "c alpha_c^(1/4) [alpha_c window]": (C_KMS * 9.6e-14 ** 0.25, C_KMS * 3.2e-9 ** 0.25, "declared alpha_c"),
        "tracking speed c_s(C), C in 1..1e4": (_cs_num(C2_MIN, 1e4), _cs_num(C2_MAX, 1.0), "environment C"),
        "sqrt(a0 xi)": (math.sqrt(a0 * xi_lo * PC_M) / 1e3, math.sqrt(a0 * xi_hi * PC_M) / 1e3, "declared xi"),
        "a0 / H0": (a0 / H0_SI / 1e3, a0 / H0_SI / 1e3, "none"),
        "c / Z": (C_KMS / math.sqrt(32 * math.pi / 3), C_KMS / math.sqrt(32 * math.pi / 3), "none"),
        "hbar/(m xi), m >= floor": (0.0, hbar_SI / (m_floor * eV_kg) / (xi_lo * PC_M) / 1e3, "declared m, xi"),
        "(hbar a0/m)^(1/3), m >= floor": (0.0, (hbar_SI / (m_floor * eV_kg) * a0) ** (1 / 3) / 1e3, "declared m"),
    }
WIN = (575.0, 675.0)
reach = {f_: {k_: (lo <= WIN[1] and hi >= WIN[0]) for k_, (lo, hi, _) in census[f_].items()} for f_ in FEET}
free_hit = [k_ for f_ in FEET for k_, (lo, hi, dep) in census[f_].items() if dep == "none" and lo <= WIN[1] and hi >= WIN[0]]
band = {f_: (WIN[0] ** 4 * 1e12 / (G_SI * A0_FP0[f_] * MSUN), WIN[1] ** 4 * 1e12 / (G_SI * A0_FP0[f_] * MSUN)) for f_ in FEET}
v13 = {f_: (G_SI * 1e13 * MSUN * A0_FP0[f_]) ** 0.25 / 1e3 for f_ in FEET}
v14 = {f_: (G_SI * 1e14 * MSUN * A0_FP0[f_]) ** 0.25 / 1e3 for f_ in FEET}
for f_ in FEET:
    P(f"  {f_}:")
    for k_, (lo, hi, dep) in census[f_].items():
        P(f"    {k_:38s} {lo:10.1f} - {hi:10.1f} km/s  (depends on: {dep}){'   <- reaches 575-675' if reach[f_][k_] else ''}")
    P(f"    (G M a0)^(1/4): {v13[f_]:.0f} km/s at 1e13, {v14[f_]:.0f} at 1e14 Msun; inside 575-675 only for M in "
      f"[{band[f_][0]:.2e}, {band[f_][1]:.2e}] Msun ({math.log10(band[f_][1] / band[f_][0]):.2f} dex)")
ok_b6 = len(free_hit) == 0 and all(math.log10(band[f_][1] / band[f_][0]) < 0.3 for f_ in FEET)
check("B6 THE WINDOW IS NOT PREDICTED: no parameter-free velocity of the core (with the dark mass m) lies in 575-675 km/s; the "
      "candidates that reach it need a declared constant tuned inside its window (alpha_c) or an environment variable (C); "
      "(G M a0)^(1/4) lies in it only for M in a 0.28-dex band near 1e13 Msun on either footing",
      f"parameter-free hits {free_hit}; tunable hits {sorted({k_ for f_ in FEET for k_, v_ in reach[f_].items() if v_})}; "
      f"band canonical [{band['canonical'][0]:.2e}, {band['canonical'][1]:.2e}], alt [{band['alt'][0]:.2e}, {band['alt'][1]:.2e}] Msun",
      ok_b6, "the resemblance to (G M a0)^(1/4) at ~1e13 Msun is selection: the gates want a universal speed above the z = 2.5 "
      "galaxies' escape speeds and below the groups'/clusters' retention edge, and in this framework both edges scale as "
      "(G M a0)^(1/4) of their hosts -- they meet at the group scale")
OUT["numbers"]["B6"] = dict(census=census, band=band, v13=v13, v14=v14, free_hit=free_hit)
P(f"  part B done   {elapsed()}")

# ================================================================================================ C the derived mechanism on the gates
banner("C  THE DERIVED MECHANISM ON THE GATES: B1's ceiling at delta = 1 as the kick, with the action's own reciprocal term")
KICK_HAND = 600.0
# The kick: three readings of the hill as a kick through AT1's loss-cone retention (conversion on entry into r_v, isotropic):
#   natural     r_v at the kernel's natural scale (y_b = 1), kick = the ceiling there
#   outer       r_v at AT1's flagship-passing threshold (y_b = 0.1), kick = the ceiling there
#   upper bound r_v at y_b = 0.1, kick = the FULL hill height (the ceiling at the centre): more than any element can get
# The reciprocal term (B1): wherever a fraction ret of the uncleared carrier remains, the phantom is multiplied by
# (1 - DELTA ret), DELTA = 1 at the ceiling.  It enters the flagship, X-COP and galaxy scores below (closed forms); the
# KiDS and cosmic-shear machinery (L360, MS3) cannot carry it and is scored without it (stated at each).
READ = {"natural (y = 1)": (1.0, "rv"), "outer (y = 0.1)": (0.1, "rv"), "upper bound": (0.1, "centre")}
READ2 = ("natural (y = 1)", "upper bound")                            # the two extremes, for the cluster-scale gates
RSEC = "upper bound"                                                  # the most clearing reading, for the gates that want clearing
DELTA = 1.0
if MUTATE:                                                            # MUTATE (ii): the hand-set kick, no reciprocal term
    READ = {"hand-set 600 km/s": (0.1, "hand")}
    READ2 = ("hand-set 600 km/s",)
    RSEC = "hand-set 600 km/s"
    DELTA = 0.0


def kick_for(H, r_v, mode):
    """the derived kick: sqrt(2 V_cap) at delta = 1, at r_v or at the centre (MUTATE (ii): the hand-set 600 km/s)."""
    if mode == "hand":
        return KICK_HAND
    rr, V, _, _ = H["cap"]
    r_ = rr[0] if mode == "centre" else max(r_v, rr[0])
    return math.sqrt(2 * float(np.interp(r_, rr, V)))


NRET = 1500 if FAST else 10000
Gk21, GE_CL, GE_GAL, nu21 = Lm["Gk"], Lm["GE_CL"], Lm["GE_GAL"], Lm["nu"]


def flag_job(job):
    f_, lMb, rname = job
    H = HOSTS[(f_, f"flagship 1e{lMb:g}")]
    yv, mode = READ[rname]
    rv = r_trigger(H["Mb"], H["a"], yv, A0K[f_])
    vk = kick_for(H, rv, mode)
    ratio, flc = retained_acc(H["Mb_fn"], H["M200"], H["c"], [H["r_F"]], rv, vk, H["rhoc"], N=NRET)
    ret = float(ratio[0])
    a0 = FOOT[f_]; r_out_m = H["r_F"] * KPC20
    gb = G20 * H["Mb"] * MSUN20 / r_out_m ** 2; gc = g_nfw(H["M200"], H["z"], r_out_m) * ret
    sh_add, sh_rec = [], []
    for nf in (nu20, nu_mono_bk1):
        nu_ = float(nf(gb / a0))
        sh_add.append(2 * math.log10((nu_ * gb + gc) / (nu_ * gb)))                    # AT1/GP5's additive formula
        sh_rec.append(2 * math.log10((gb + (nu_ - 1) * gb * max(1 - DELTA * ret, 0.0) + gc) / (nu_ * gb)))
    x_over = g_nfw(H["M200"], H["z"], r_out_m) / gb / (float(nu20(gb / a0)) - 1)       # halo force / phantom force at r_F
    return job, dict(r_v=rv, kick=vk, loss_cone=flc, retained=ret, shift_additive=max(sh_add, key=abs),
                     shift=max(sh_rec, key=abs), halo_over_phantom=x_over)


C1 = {}
for f_ in FEET:
    Lm["A0"] = A0K[f_]                                                # the carrier's potential: this footing's baryonic kernel
    with ThreadPoolExecutor(NW) as ex:
        C1.update(dict(ex.map(flag_job, [(f_, l_, rn) for l_ in (10.0, 10.5, 11.0) for rn in READ])))
for (f_, l_, rn), v_ in sorted(C1.items()):
    P(f"    {f_:9s} M_b 1e{l_:<4g} {rn:18s}: r_v {v_['r_v']:6.1f} kpc, kick {v_['kick']:5.0f} km/s, loss cone {v_['loss_cone']:.2f}, "
      f"retained inside r_F {v_['retained']:.3f} -> shift {v_['shift']:+.3f} dex (without the reciprocal term {v_['shift_additive']:+.3f})")
worst_flag = min(abs(v_["shift"]) for v_ in C1.values())
ok_c1 = worst_flag > 0.10
check("C1 the derived mechanism (the delta = 1 ceiling as the kick -- natural scale, outer threshold, and the upper bound that gives "
      "every element the full hill height -- with the reciprocal suppression of the phantom by the kept carrier, both footings) "
      "clears no flagship host: every z = 2.5 zero point stays above the 0.10 dex gate" + (" [MUTATE: the hand-set 600 km/s]" if MUTATE else ""),
      f"smallest |shift| over {len(C1)} cells {worst_flag:.3f} dex; kicks {min(v_['kick'] for v_ in C1.values()):.0f}-"
      f"{max(v_['kick'] for v_ in C1.values()):.0f} km/s; retained {min(v_['retained'] for v_ in C1.values()):.2f}-"
      f"{max(v_['retained'] for v_ in C1.values()):.2f}", ok_c1,
      "framework alone 0.00, LCDM +0.33.  Where the halo stays, the reciprocal term turns the host into Newton + halo.  Smaller "
      "delta only makes it worse: the kick falls as sqrt(delta) (retention rises) and the shift 2 log[(1 + (nu - 1)(1 - delta ret) "
      f"+ x ret)/nu] rises with ret and falls with delta, since the halo's force x exceeds the phantom's at r_F (x/(nu - 1) >= "
      f"{min(v_['halo_over_phantom'] for v_ in C1.values()):.1f})")
OUT["numbers"]["C1"] = {f"{k_[0]}|{k_[1]}|{k_[2]}": v_ for k_, v_ in C1.items()}
P(f"  flagship done   {elapsed()}")


# ------------------------------------------------------------------------------------------------ C2 X-COP, C3 galaxies, C4 KiDS
def xcop_recip(eps, f_, delta):
    """L321's cl_ratio (additive, SW01's EFE rule) with the reciprocal term: g = g_b + (nu - 1) g_b (1 - delta eps) + g_c.
    delta = 0 is exactly the committed cl_ratio (control below)."""
    A0 = A0K[f_]; out = []
    for cl in CL:
        R = cl["R500"]; gb = Gk21 * cl["Mb"] / R ** 2; gc = Gk21 * eps * cl["Mcarr"] / R ** 2
        nu_ = float(nu21(math.sqrt(gb ** 2 + (GE_CL * A0) ** 2) / A0))
        out.append((gb + (nu_ - 1) * gb * max(1 - delta * eps, 0.0) + gc) * R ** 2 / Gk21 / cl["Mhse"])
    med = float(np.median(out))
    return dict(ratio=med, strict=abs(med - 1) <= 0.2, alt=abs(med * (1 - 0.06) - 1) <= 0.2)


def gal_recip(eps, f_, delta):
    """L321's gal_shift (additive) with the reciprocal term; |shift| <= 0.06 dex is the gate.  delta = 0 is the committed one."""
    A0 = A0K[f_]; out = {}
    for kh, e in eps.items():
        host = GAL[kh]; Mn, r200, rs = Lm["nfw"](host["M200"], Lm["c200_dm14"](host["M200"]))
        r = host["rg"]; gb = Gk21 * float(hernquist(host["Mb"], host["a"])(r)) / r ** 2; gc = Gk21 * e * (1 - FB) * float(Mn(r)) / r ** 2
        nu_ = float(nu21(math.sqrt(gb ** 2 + (GE_GAL * A0) ** 2) / A0))
        out[kh] = math.log10((gb + (nu_ - 1) * gb * max(1 - delta * e, 0.0) + gc) / (nu_ * gb))
    return out


def xcop_job(job):
    f_, rn = job
    H = HOSTS[(f_, "X-COP ref")]
    yv, mode = READ[rn]
    rv = r_v_profile(cl_mass_fn, yv, A0K[f_], rmax=5 * CLREF["R500"])
    vk = kick_for(H, rv, mode)
    eps = float(retained_acc(cl_mass_fn, CLREF["M200"], CLREF["c"], [CLREF["R500"]], rv, vk, CLREF["rhoc"],
                             N=(1500 if FAST else 12000))[0][0])
    return job, dict(r_v=rv, kick=vk, eps=eps)


def gal_job(job):
    f_, kh = job
    hst = GAL[kh]; Mb_fn = hernquist(hst["Mb"], hst["a"]); c_ = float(c200_z0(hst["M200"]))
    H = dict(cap=ceiling(Mb_fn, hst["M200"], c_, RHO_C0, A0K[f_]))
    yv, mode = READ[RSEC]
    rv = r_v_profile(Mb_fn, yv, A0K[f_])
    vk = kick_for(H, rv, mode)
    return job, dict(r_v=rv, kick=vk, eps=float(retained_acc(Mb_fn, hst["M200"], c_, [hst["rg"]], rv, vk, RHO_C0, N=NRET)[0][0]))


def kids_job(job):
    f_, b = job
    H = HOSTS[(f_, f"KiDS bin {b + 1}")]
    Mn, r200, rs = nfw21(H["M200"], H["c"], RHOC_ZL)
    pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
    yv, mode = READ[RSEC]
    rv = r_v_profile(H["Mb_fn"], yv, A0K[f_])
    vk = kick_for(H, rv, mode)
    ratio_p, _ = retained_acc(H["Mb_fn"], H["M200"], H["c"], list(pro), rv, vk, RHOC_ZL, N=(1500 if FAST else 8000))
    S05 = float(np.interp(500.0 / hh, pro, ratio_p))
    return job, dict(r_v=rv, kick=vk, pro=pro, ratio=np.asarray(ratio_p), S05=S05)


XC, GA, KD = {}, {}, {}
for f_ in FEET:
    Lm["A0"] = A0K[f_]
    with ThreadPoolExecutor(NW) as ex:
        XC.update(dict(ex.map(xcop_job, [(f_, rn) for rn in READ2])))
        GA.update(dict(ex.map(gal_job, [(f_, kh) for kh in GAL])))
        KD.update(dict(ex.map(kids_job, [(f_, b) for b in range(4)])))
XR, GS, GS0, KS = {}, {}, {}, {}
dev_x, dev_g = 0.0, 0.0
for f_ in FEET:                                                       # serial: the committed functions set the shared A0
    for rn in READ2:
        e_ = XC[(f_, rn)]["eps"]
        committed = xcop_from_eps(e_)[f_]["ratio"]
        Lm["A0"] = A0K[f_]
        dev_x = max(dev_x, abs(xcop_recip(e_, f_, 0.0)["ratio"] - committed))
        XR[(f_, rn)] = xcop_recip(e_, f_, DELTA)
        XR[(f_, rn)]["ratio_committed_formula"] = committed
    eps_g = {kh: GA[(f_, kh)]["eps"] for kh in GAL}
    GS0[f_] = gal_shifts(eps_g)[f_]
    Lm["A0"] = A0K[f_]
    dev_g = max(dev_g, max(abs(gal_recip(eps_g, f_, 0.0)[kh] - GS0[f_][kh]) for kh in GAL))
    GS[f_] = gal_recip(eps_g, f_, DELTA)
    KS[f_] = kids_switched([(KD[(f_, b)]["pro"], KD[(f_, b)]["ratio"]) for b in range(4)])[f_]
check("C2a CONTROL: with delta = 0 this lane's reciprocal X-COP and galaxy formulas reproduce the committed cl_ratio (via AT3's "
      "xcop_from_eps) and L357's gal_shifts on the same retentions", f"max |dev| X-COP {dev_x:.1e}, galaxies {dev_g:.1e}",
      dev_x < 1e-9 and dev_g < 1e-9, load_bearing=False)
for (f_, rn), v_ in sorted(XR.items()):
    P(f"    X-COP {f_:9s} {rn:18s}: kick {XC[(f_, rn)]['kick']:5.0f} km/s at r_v {XC[(f_, rn)]['r_v']:5.0f} kpc, retention in R500 "
      f"{XC[(f_, rn)]['eps']:.3f} -> median M_dyn/M_HSE {v_['ratio']:.2f} (strict {v_['strict']}, 6% non-thermal {v_['alt']}; "
      f"without the reciprocal term {v_['ratio_committed_formula']:.2f})")
for f_ in FEET:
    P(f"    galaxies z = 0 {f_:9s} ({RSEC}): kicks " + ", ".join(f"{kh} {GA[(f_, kh)]['kick']:.0f}" for kh in GAL) + " km/s; retained "
      + ", ".join(f"{kh} {GA[(f_, kh)]['eps']:.2f}" for kh in GAL) + "; shifts " + ", ".join(f"{kh} {v_:+.3f}" for kh, v_ in GS[f_].items())
      + " dex (|shift| <= 0.06; without the reciprocal term " + ", ".join(f"{v_:+.3f}" for v_ in GS0[f_].values()) + ")")
    P(f"    KiDS z = 0.25 {f_:9s} ({RSEC}): kicks " + "/".join(f"{KD[(f_, b)]['kick']:.0f}" for b in range(4)) + " km/s; S(<0.5 Mpc/h) "
      + "/".join(f"{KD[(f_, b)]['S05']:.2f}" for b in range(4)) + f"; Delta chi^2 at the common cell {KS[f_]:+.1f} (gate <= +4; L390's "
      f"decay-off control {J['L390']['controls']['C2'][f_]:+.1f}; the reciprocal term is not modelled in L360's fit)")
if not MUTATE:
    anti_c2 = all(XC[(f_, "upper bound")]["eps"] < min(C1[(f_, l_, "upper bound")]["retained"] for l_ in (10.0, 10.5, 11.0)) for f_ in FEET)
else:
    anti_c2 = False
check("C2 (reported) X-COP, with the reciprocal term: in the upper bound the ceiling clears the reference cluster MORE than it clears "
      "any z = 2.5 flagship galaxy (the anti-selectivity of B5, on the committed machinery); the per-reading gate verdicts are "
      "printed above (the natural reading keeps the halo and switches the phantom off: Newton + halo)",
      {f"{k_[0]}|{k_[1]}": dict(eps=round(XC[k_]['eps'], 3), ratio=round(v_['ratio'], 3), strict=v_['strict'],
                                nonthermal=v_['alt']) for k_, v_ in XR.items()}, anti_c2, load_bearing=False)
gal_in = all(max(abs(v_) for v_ in GS[f_].values()) <= 0.06 for f_ in FEET)
kids_fail = all(KS[f_] > 4 for f_ in FEET)
check(f"C3 (reported) the z = 0 galaxies (L321's three hosts, {RSEC}), with the reciprocal term: every host stays inside the 0.06 dex "
      "band -- the kept halo stands in for the suppressed phantom (the host is Newton + halo, as in LCDM)",
      {f_: {k_: round(v_, 3) for k_, v_ in GS[f_].items()} for f_ in FEET}, gal_in, load_bearing=False)
check(f"C4 (reported) KiDS-1000 at the common switch cell (L360's switched fit, AT3's template, {RSEC}) WITHOUT the reciprocal term "
      "(L352's lens model returns the total ESD and cannot carry it): the kept halos are rejected; WITH it the verdict is OPEN",
      {f_: round(KS[f_], 1) for f_ in FEET}, kids_fail,
      ("as stated" if kids_fail else "FALSIFIED at the committed orbit count (the expectation came from a low-N smoke run, +8.8/+13.8): "
       f"the {RSEC} halos, kept at S(<0.5 Mpc/h) ~0.5-0.8 and mostly outside the core as in L375, pass KiDS without the reciprocal "
       "term; the natural reading keeps ~all of the halo, where L390's decay-off control (+137/+140) applies"), load_bearing=False)
OUT["numbers"]["C2"] = {f"{k_[0]}|{k_[1]}": dict(XC[k_], **XR[k_]) for k_ in XR}
OUT["numbers"]["C3"] = dict(eps={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in GA.items()}, shifts=GS, shifts_without_reciprocal=GS0)
OUT["numbers"]["C4"] = dict(dchi2=KS, S05={f"{k_[0]}|{k_[1]}": v_["S05"] for k_, v_ in KD.items()},
                            kicks={f"{k_[0]}|{k_[1]}": v_["kick"] for k_, v_ in KD.items()})
P(f"  X-COP, galaxies, KiDS done   {elapsed()}")

# ------------------------------------------------------------------------------------------------ the halo-model grid: shear, forest, Harvey
banner("C5-C7  THE HALO-MODEL GRID (hot gas included): cosmic shear (MS3), the forest and S_8, Harvey (group retention)")
GP0 = MS["GP0"]
I_LC = A1["I_LC"]


def grid_kicks(z, yv, f_, rname):
    """per halo on L357's mass grid: baryons = AT1's galaxy (Hernquist) + GP0's observed hot gas, M_hot(<r) = M_hot min(r/R500, 1)
    with R500 = 0.65 r200 (the X-COP reference's shape); the trigger radius where y_b = yv, AT1's loss-cone and escape tables
    at that x_v, and the derived kick of the reading."""
    a0k = A0K[f_]; mode = READ[rname][1]
    rhoc = RHOC0_KPC * Ez2(z)
    cs = np.asarray(c_dm14(MH_h, z), float)
    kick, vesc, xv, V200 = (np.zeros(len(MH_h)) for _ in range(4))
    for i in range(len(MH_h)):
        Mh = MH_h[i] / hh
        r200 = (3 * Mh / (4 * math.pi * 200 * rhoc)) ** (1 / 3); V200[i] = math.sqrt(GK * Mh / r200)
        Mg, a_h = galaxy_baryons(Mh, z)
        Mhot = max(float(GP0.M_bound(Mh, z, "observed")) - float(GP0.M_bound(Mh, z, "galaxy")), 0.0)
        R5 = 0.65 * r200
        Mb_fn = (lambda r, Mg=Mg, a_h=a_h, Mhot=Mhot, R5=R5: hernquist(Mg, a_h)(r) + Mhot * np.clip(np.asarray(r, float) / R5, 0, 1))
        rv = r_v_profile(Mb_fn, yv, a0k, rmax=r200)
        if rv <= 0:
            continue
        xv[i] = min(rv / r200, 1.0)
        H = dict(cap=ceiling(Mb_fn, Mh, float(cs[i]), rhoc, a0k))
        kick[i] = kick_for(H, rv, mode)
        vesc[i] = V200[i] * math.sqrt(-2 * float(nfw_phi(np.array([max(xv[i], 1e-6)]), float(cs[i]))[0]))
    cl = np.log(np.clip(cs, CG[0], CG[-1])); lxv = np.log(np.maximum(xv, XVG[0]))
    lc = np.where(xv > 0, I_LC(np.stack([cl, lxv], 1)), 0.0)
    fe = np.where(xv > 0, I_ES(np.stack([cl, lxv, np.clip(kick / V200, 0, UGR[-1])], 1)), 0.0)
    return dict(lc=np.clip(lc, 0, 1), xv=xv, kick=kick, vesc=vesc, fe=np.clip(fe, 0, 1), V200=V200)


def R_of_recip(xc, a0, rcap, conv, ret, delta):
    """MS3's R_of (worst R over its k grid) with the reciprocal term: each halo's phantom transform is multiplied by
    (1 - delta ret(M)), the suppression B1 derives where a fraction ret(M) of the carrier is kept.  delta = 0 is exactly
    MS3's R_of (control below); the per-halo factor treats the kept fraction as uniform inside the region (an approximation)."""
    KC, LMH, GPm, dn_, bh_, dlnM, RHO = MS["KC"], MS["LMH"], MS["GP0"], MS["dn"], MS["bh"], MS["dlnM"], MS["RHO"]
    P1 = np.zeros_like(KC); X1 = np.zeros_like(KC); B = np.zeros_like(KC); rm = np.zeros_like(KC)
    for lm in LMH:
        M = 10 ** lm; n = float(np.interp(lm, GPm.LM, dn_)); b = float(np.interp(lm, GPm.LM, bh_))
        Mb = float(GPm.M_bound(M, MS["ZS"], "observed")); tr, _ = MS["transform"](M, Mb, xc, a0, rcap, conv); uk = MS["nfw_uk"](M, KC)
        fr = ret(M); tr = tr * max(1 - delta * fr, 0.0)
        P1 += n * tr ** 2 * dlnM / RHO ** 2; B += n * b * tr * dlnM / RHO
        mass_1h = (MS["FB"] + (1 - MS["FB"]) * fr) * M
        rm += n * ((M * uk) ** 2 - (mass_1h * uk) ** 2) * dlnM / RHO ** 2
        X1 += n * mass_1h * uk * tr * dlnM / RHO ** 2
    Pph = P1 + B ** 2 * MS["PLIN"]; Pxm = X1 + MS["I1"] * B * MS["PLIN"]
    R = (MS["PNL"] - rm + 2 * Pxm + Pph) / MS["PNL"]
    return max(float(np.interp(math.log(q * MS["h"]), np.log(KC), R)) for q in MS["KG"])


def F_escaped(gk, z):
    s = SIG0 * DG(z); nu = DC / s
    w = f_st(nu) * np.abs(np.gradient(nu, np.log(MH_h)))
    return float(trap(w * b_st(nu) * gk["lc"] * gk["fe"], np.log(MH_h)))


lgM = np.log10(MH_h / hh)
SH, FOR, HV, GKS = {}, {}, {}, {}
for f_ in FEET:
    for rn in READ2:
        gk05 = grid_kicks(0.5, READ[rn][0], f_, rn)
        keep = 1 - gk05["lc"] * gk05["fe"]
        ret = lambda M, keep=keep: float(np.interp(math.log10(M), lgM, keep))
        SH[(f_, rn)] = {str(cap_): max(R_of(XLIN, A0_MS3[f_], cap_, "door", ret)[0].values()) for cap_ in (math.inf, 1.75)}
        SH[(f_, rn)]["recip_1.75"] = R_of_recip(XLIN, A0_MS3[f_], 1.75, "door", ret, DELTA)
        SH[(f_, rn)]["recip_inf"] = R_of_recip(XLIN, A0_MS3[f_], math.inf, "door", ret, DELTA)
        SH[(f_, rn)]["recip0_dev"] = abs(R_of_recip(XLIN, A0_MS3[f_], 1.75, "door", ret, 0.0) - SH[(f_, rn)]["1.75"])
        SH[(f_, rn)]["keep_1e12_13_14"] = [ret(10 ** lm_) for lm_ in (12.0, 13.0, 14.0)]
        gk04 = grid_kicks(0.4, READ[rn][0], f_, rn)
        keep04 = 1 - gk04["lc"] * gk04["fe"]
        HV[(f_, rn)] = {f"{m_:.0e}": float(np.interp(math.log10(m_), lgM, keep04)) for m_ in (1e13, 1e14, 3e14)}
        GKS[(f_, rn, 0.4)] = gk04
    for z in (3.0, 2.0):
        gkz = grid_kicks(z, READ[RSEC][0], f_, RSEC)
        FOR[(f_, z)] = F_escaped(gkz, z)
        GKS[(f_, RSEC, z)] = gkz
shear_fail = all(SH[k_]["1.75"] > 1.2 for k_ in SH)
shear_recip_ok = all(SH[(f_, READ2[0])]["recip_1.75"] <= 1.2 for f_ in FEET)
dev_shear = max(SH[k_]["recip0_dev"] for k_ in SH)
_b1 = J["AT1"]["B1"]["0.1|600.0"]                                    # AT1's A2 cell: its escaped, bias-weighted budget (handed to AT2)
F_A2 = {z: float(np.interp(z, _b1["z"], _b1["F_b_escaped"])) for z in (3.0, 2.0)}
forest_ok = all(FOR[(f_, z)] <= F_A2[z] for f_ in FEET for z in (3.0, 2.0))   # AT2: that budget moved the forest's flux by <= 1.7%
harvey_intact = J["L389"]["results"]["v575"]["MEAN"]["intact"]
HV_intact = {k_: min(v_.values()) >= 0.9 for k_, v_ in HV.items()}
for (f_, rn), v_ in sorted(SH.items()):
    P(f"    cosmic shear {f_:9s} {rn:18s}: retention at 1e12/1e13/1e14 = " + "/".join(f"{x_:.2f}" for x_ in v_["keep_1e12_13_14"])
      + f"; worst R without the reciprocal term: uncapped {v_['inf']:.2f}, 1.75 Mpc cap {v_['1.75']:.2f} (MS3's intact row "
      f"{J['MS3']['K1']['1.75']['intact'][f_]:.2f}); WITH it: uncapped {v_['recip_inf']:.2f}, 1.75 Mpc cap {v_['recip_1.75']:.2f} (gate 1.2)")
for (f_, z), v_ in sorted(FOR.items()):
    P(f"    forest/S_8   {f_:9s} z = {z}: bias-weighted escaped fraction ({RSEC}) {v_:.4f}  (AT1's committed A2 cell: {F_A2[z]:.3f}, "
      f"whose FLUX moved <= 1.7% in AT2)")
for (f_, rn), v_ in sorted(HV.items()):
    P(f"    Harvey       {f_:9s} {rn:18s}: kept carrier at z = 0.4 in 1e13/1e14/3e14 Msun: " + "/".join(f"{x_:.3f}" for x_ in v_.values())
      + (f" -> intact: the committed intact-carrier excess beta (L389) {', '.join(f'{k_} {x_:+.3f}' for k_, x_ in harvey_intact.items())}"
         if HV_intact[(f_, rn)] else " -> NOT intact: Harvey not scored here (L371's machinery is outside this lane's budget)"))
check("C5a CONTROL: this lane's reciprocal copy of MS3's R_of reproduces MS3's R_of exactly at delta = 0 (same retention)",
      f"max |dev| {dev_shear:.1e}", dev_shear < 1e-9, load_bearing=False)
check("C5 (reported) cosmic shear on MS3's halo model: WITHOUT the reciprocal term the kept halos fail at the KiDS-safe 1.75 Mpc cap in "
      "both readings; WITH it (delta = 1) the kept halos' phantoms are switched off and the natural reading is LCDM-like, within "
      "1.2 at the cap on both footings", {f"{k_[0]}|{k_[1]}": {kk: (round(vv, 3) if not isinstance(vv, list) else [round(x_, 3) for x_ in vv])
                                                               for kk, vv in v_.items() if kk != "recip0_dev"} for k_, v_ in SH.items()},
      shear_fail and shear_recip_ok, load_bearing=False)
check("C6 (reported) the forest and S_8: the derived kick unbinds a few per cent of the bias-weighted carrier at z = 2-3, below AT1's "
      f"A2 budget, which moved the forest's flux by <= 1.7%: they pass, as cold dark matter does (S_8 -> LCDM's {S8_LCDM:.4f})",
      {f"{k_[0]}|{k_[1]}": round(v_, 5) for k_, v_ in FOR.items()}, forest_ok, load_bearing=False)
harvey_ok = all(HV_intact[(f_, READ2[0])] for f_ in FEET) and max(harvey_intact.values()) <= 0.10
check("C7 (reported, a proxy) Harvey: in the natural reading groups and clusters keep >= 90% of the carrier, so the prediction is the "
      "intact carrier's committed excess beta (L389), which passes +0.10; where a reading clears clusters, Harvey is not scored here",
      {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in HV.items()}, harvey_ok, load_bearing=False)
OUT["numbers"]["C5_C7"] = dict(shear={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in SH.items()}, forest={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in FOR.items()},
                               harvey_keep={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in HV.items()}, harvey_intact=harvey_intact)
P(f"  grid done   {elapsed()}")

# ================================================================================================ K1 the knife-edge, answered
banner("K1  THE KNIFE-EDGE: does the derived kick land in 575-675 km/s without tuning, or widen the window?")
dist = {}
for f_ in FEET:
    for key, lo_, hi_ in (((f_, RSEC, 2.0), 10.5, 12.5), ((f_, RSEC, 0.4), 13.0, 14.5)):
        gk = GKS[key]
        sel = (lgM >= lo_) & (lgM <= hi_) & (gk["xv"] > 0)
        k_ = gk["kick"][sel]; e_ = gk["vesc"][sel]
        dist[key] = dict(kick_min=float(k_.min()) if k_.size else float("nan"), kick_max=float(k_.max()) if k_.size else float("nan"),
                         in_window=float(np.mean((k_ >= WIN[0]) & (k_ <= WIN[1]))) if k_.size else float("nan"),
                         ratio_med=float(np.median(k_ / np.maximum(e_, 1e-9))) if k_.size else float("nan"),
                         range=f"1e{lo_:g}-1e{hi_:g}")
for key, d_ in sorted(dist.items()):
    P(f"    {key[0]:9s} z = {key[2]} ({key[1]}): hosts {d_['range']} Msun: derived kick {d_['kick_min']:.0f}-{d_['kick_max']:.0f} km/s, "
      f"fraction inside 575-675 {d_['in_window']:.2f}, median kick / escape at r_v {d_['ratio_med']:.2f}")
gal_ratio = [dist[(f_, RSEC, 2.0)]["ratio_med"] for f_ in FEET]; grp_ratio = [dist[(f_, RSEC, 0.4)]["ratio_med"] for f_ in FEET]
ok_k1 = all(r_ < 1 for r_ in gal_ratio) and all(dist[(f_, RSEC, 2.0)]["in_window"] < 0.05 for f_ in FEET) \
        and all(g_ > h_ for g_, h_ in zip(grp_ratio, gal_ratio))
check("K1 THE KNIFE-EDGE, answered: the derived kick is a host-proportional distribution -- below escape in the z = 2 galaxies "
      "(median kick/escape < 1), almost never inside 575-675 there, and closer to escape in groups and clusters than in galaxies: "
      "it neither lands in the sliver where the flagship needs it nor widens the window",
      {f"{k_[0]}|{k_[1]}|z{k_[2]}": {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v_.items()} for k_, v_ in dist.items()},
      ok_k1, "a window needs a UNIVERSAL speed between the galaxies' and the clusters' escape speeds; the core supplies only "
      "host-proportional energies (largest relative to escape in the deepest wells), so the speed must be a constant of the added "
      "field (B3): FITTED, and the sliver stays a sliver", load_bearing=False)
OUT["numbers"]["K1"] = {f"{k_[0]}|{k_[1]}|{k_[2]}": v_ for k_, v_ in dist.items()}

# ================================================================================================ W the ledger
banner("W  THE LEDGER: what this lane settles (link / status / basis)")
LEDGER = [
    ("L10a", "the dark mass and the clusters' missing mass as a STATE of the core's own fields (g, tau, U, W, L, lambda_0)", "FAILS",
     "A1-A5: the clock has no charge and one gapless mode; the auxiliaries are constrained; the metric's PBHs fail the gates"),
    ("L10b", "the clock carries no conserved charge (n.dn/d(d tau) = 0; FRW action independent of tau-dot)", "DERIVED", "check A1"),
    ("L10c", "U, W, L, lambda_0 are constrained (zero kinetic Hessian with lapse and shift)", "DERIVED", "check A2"),
    ("L10d", "the clock's one mode: omega^2 = c_2 k^2/(C(2 + 3c_2)); its quanta are radiation (p = rho/3) at >= 1800 km/s", "DERIVED", "check A3"),
    ("L10e", "the metric's cold state (primordial black holes): sources u, cannot be kicked; fails X-COP, galaxies, flagship", "FAILS", "check A4"),
    ("L10f", "the minimal addition: one nearly free complex scalar (2 real d.o.f.) + one mass m >= 1.9-5.2e-19 eV; amount = initial data",
     "POSTULATED", "check A5 (XR8, FL1, L383)"),
    ("L10g", "reciprocity: a dark coupling V(I) multiplies the phantom by (1 - delta) where the dark state sits", "DERIVED", "check B1"),
    ("L10h", "a coupling to the clock's acceleration reads the multiplier Phi: the constraint turns singular at O(1) strength", "FAILS", "check B2"),
    ("L10i", "a coupling to the clock's K is spatially blind in bound regions; the kick speed is the splitting eps/m^2 = v^2/(2c^2 - v^2)",
     "FITTED", "check B3 (FK1's eps = 1.84-2.35e-6, set by the 575-650 window)"),
    ("L10j", "the kick velocity scale from the action: only a ceiling, v_cap(r_t) = 2 sqrt(delta) (G M_b a0)^(1/2)/v_d ~ (G M_b a0)^(1/4) "
     "at delta = 1 on real z = 2.5 halos, host-proportional", "DERIVED", "checks B4, B5"),
    ("L10k", "clearing galaxies with the core's own energy: needs delta > 1 (phantom reversed) and is anti-selective (clusters first)",
     "FAILS", "check B5"),
    ("L10l", "the ~600 km/s window: not predicted; (G M a0)^(1/4) in it only for a 0.28-dex band near 1e13 Msun (a selection)", "FITTED", "check B6"),
    ("L10m", "the derived mechanism on the gates (delta = 1, with the reciprocal term): the kept halos switch their phantoms off, so "
     "it passes what LCDM passes (z = 0 galaxies, X-COP in the natural reading, cosmic shear, forest, S_8, Harvey by proxy; KiDS in "
     "the upper bound without the term) and fails the framework's distinctive flagship at z = 2.5 in every reading", "FAILS", "checks C1-C7"),
    ("L10n", "the knife-edge: the derived kick neither lands in 575-675 nor widens the window", "FAILS", "check K1"),
    ("L10o", "derivative/current couplings of the dark state to the core; an acceleration-gated conversion rate's own reciprocal "
     "distortion; the varied region gate's onset (V0, obstructed: CV3/DE12/DE13)", "OPEN", "not computed here"),
]
for k_, what, st, basis in LEDGER:
    P(f"    {k_:5s} {st:10s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane's links", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
_nat = [v_ for k_, v_ in C1.items() if k_[2] == READ2[0]]
P(f"""  A. The dark mass cannot be a state of the ungated C-H/K core.  The clock is its own aether, so it carries no charge and no
  condensate dust (A1); U, W, L and lambda_0 are constrained (A2); the clock's one mode is gapless -- its quanta are radiation
  moving at >= {cs_min:.0f} km/s (A3); the metric's own cold state, primordial black holes, sources the kernel and cannot be kicked,
  and fails X-COP, the galaxies and the flagship (A4).  The minimal addition is ONE nearly free complex scalar (two real fields)
  with ONE mass m >= {min(floors):.1e} eV; its amount is initial data (A5).
  B. The core cannot hand that field the kick.  By the action's own reciprocity (B1) any coupling to the MOND sector that pushes
  the dark state multiplies the phantom around it by (1 - delta); a coupling to the clock's acceleration turns the constraint
  singular first (B2); a coupling to K is blind to place and leaves the speed to a mass splitting (B3).  The ceiling is the
  framework's own velocity, 2 sqrt(delta) (G M_b a0)^(1/2)/v_d at the transition radius (B4) -- on real z = 2.5 halos at
  delta = 1 it is ~(G M_b a0)^(1/4) -- host-proportional and below escape: the flagship hosts would need delta
  {min(fl_req):.0f}-{max(fl_req):.0f} (the phantom reversed), the X-COP cluster only {min(cl_req):.1f}-{max(cl_req):.1f} (B5: anti-selective).
  The ~600 km/s window is not predicted (B6): the gates select a universal speed between galaxy and cluster escape speeds,
  and it resembles (G M a0)^(1/4) at ~1e13 Msun because both edges scale that way.
  C. Scored at delta = 1 with the reciprocal term, the kick ({min(v_['kick'] for v_ in C1.values()):.0f}-{max(v_['kick'] for v_ in C1.values()):.0f} km/s at the flagship hosts) clears no galaxy: the
  flagship fails in every reading (smallest |shift| {worst_flag:.2f} dex).  Where the halo stays, the same coupling switches the
  phantom off, so the host is Newton + halo: the z = 0 galaxies, X-COP (natural reading) and cosmic shear then pass the way LCDM
  passes them, the forest and S_8 pass (a few per cent unbound), Harvey passes by proxy (natural reading), and KiDS passes in the
  upper bound even without the term (its KiDS with the term is not computed).  A MOND-sector kick cannot remove the dark halo;
  at full strength it removes the MOND instead -- and the flagship, the one gate that tells the framework from LCDM, fails.
  The knife-edge is not resolved: the core supplies only host-proportional energies, so a working kick's speed must be a
  constant of the added field (FK1's eps = 1.84-2.35e-6), FITTED to the sliver.  Minimal cost of a working dark sector with a
  kick: one field (two real d.o.f.) and two constants beyond the core -- m (required anyway) and eps (fitted) -- plus FK1's
  trigger rule (lambda, q: declared).""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["runtime_s"] = len(CH), n_fail, time.time() - T0


def _jd(o):
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


outname = f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=_jd)
P(f"\n  {len(CH) - sum(1 for _, ok, _ in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   {elapsed()}")
sys.exit(0 if n_fail == 0 else 1)
