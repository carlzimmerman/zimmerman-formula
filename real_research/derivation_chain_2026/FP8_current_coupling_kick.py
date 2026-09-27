#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP8 -- THE LAST OPEN DOOR FOR THE DARK-SECTOR KICK: couplings of the dark field's CURRENT and DERIVATIVES to the core.

WHY.  FP4 (committed) showed that the ungated C-H/K core cannot carry the dark mass and cannot supply the kick through any
DENSITY coupling -rho_d V(I): by the action's own reciprocity (FP4 B1) the term that pushes the dark state multiplies the
MOND phantom around it by (1 - delta), and at delta = 1 the host is Newton + halo, which fails the z = 2.5 flagship.  FP4's
ledger left one door OPEN (L10o): couplings to the dark field's CURRENT J^m = i(Psi* d^m Psi - Psi d^m Psi*) or its
DERIVATIVES, which might move or heat the dark state without writing on the phantom.  This lane writes the most general
low-order couplings of that kind, varies the action with them, and asks: (1) does any escape the reciprocity bound, and what
is its exact back-reaction on the MOND sector's source; (2) what velocity scale does it produce, from which constants;
(3) where does it act; (4) is it healthy (Minkowski, FRW, static MOND background); (5) the gates for the best one.

THE ROOT (FP4's, varied here exactly as written):
    I = I_core + S_Psi + S_int,   I_core = C-H (ACTION.md:95-106) + alpha_c a^2 - c_2 (K - <K>_h)^2, beta = 0, nu_mono;
    S_Psi = -Int sqrt(-g) [g^{mn} d_m Psi* d_n Psi + m^2 |Psi|^2]   (FP4 L10f, POSTULATED: one complex field, m >= 1.9e-19 eV),
  with L353's constrained pair, so the kernel reads the baryons' Newtonian field and the dark state feels Newtonian gravity
  (the retention machinery below uses exactly that force law).  NR limit of the MOND sector (FP4's I_NR):
    I_NR = Int dt d^3x { L_kin - rho Phi - [2 grad Phi . grad u - |grad u|^2 - a0^2 q(|grad u|^2/a0^2)]/(8 pi G) } + S_int,
  q'(s^2) = nu_mono(s) - 1 (the filter S is at the 0.03-0.1 pc scale and is dropped at halo scales, as in FP4 B1).
  Both a0 footings: FP0's 9.3603e-11 / 1.1312e-10 m/s^2; the imported machinery's pair 9.3619e-11 / 1.1279e-10 is used
  wherever a committed lane's function is called (0.02% / 0.3% apart).

THE CLASS (local, the dark U(1) kept unless stated, at most one derivative on each Psi; chi is any scalar of the core --
U, W_b, I = |grad W_b|^2/alpha^2, tau, ln N, K; e^m = D^m W_b/|D W_b| the MOND field's direction):
  (a) density                   -rho_d V(I)                                     [FP4's class]
  (b) electrostatic current     g (J.n) f(I)                                    (the task's (J.u) f(I))
  (c) gradient current          g J^m d_m chi                                   (the task's J^m d_m(sector field))
  (d) spatial ("rate") current  g J^m h_m^n d_n chi  == -g (J.n)(n.d chi) + (c) (J.a is (d) with chi = ln N)
  (e) magnetic current          g J^m A_m, A spatial with curl A != 0           (e.g. F(I) D_m W_b off spherical symmetry)
  (f) kinetic couplings         -F(I) g^{mn} dPsi* dPsi,  -F(I) n^m n^n dPsi* dPsi,  -G(I) h^{mn} dPsi* dPsi,
                                -G(I) e^m e^n dPsi* dPsi
  (g) U(1)-breaking             f(I) Re Psi^2 (a triggered splitting); eps Re Psi^2 (FK1's kick)
  (h) clock couplings           the same with K, a_m, n_m in place of the MOND sector (FP4 B2/B3 cover their densities)

CHECKS (load-bearing unless marked)
  C0 CONTROLS (not load-bearing): FP4's committed B5 ceilings are reproduced by FP4's own ceiling() exec'd read-only; this
     lane's copy of AT1's retention reproduces AT1's retained_acc on identical draws; the orbit quadrature used for the gains
     is converged (48 vs 400 nodes).
  A1 [sympy] the task's current in the NR limit: J.n = n_d (1 - theta_t/m) (the clock-frame number density), J^i = -n_d v^i.
  A2 [sympy] GAUGE REDUCTION: -|dPsi|^2 + g A.J == -|(d + i g A)Psi|^2 + g^2 A.A |Psi|^2 identically; for A = d chi the
     redefinition Psi -> e^{-i g chi} Psi removes the current coupling exactly, leaving the DENSITY coupling g^2 (d chi)^2 |Psi|^2.
     So (c) is FP4's class at O(g^2); (b) is an electrostatic potential (FP4's class); (e) is a magnetic field.
  A3 [sympy] REST-ENERGY REDUCTION: the dispersion of each kinetic coupling (f); rest energy M/sqrt(A), inertia M sqrt(A)/B,
     speed^2 B/A.  -F(I) g^{mn} dPsi* dPsi is the density coupling V = c^2[(1+F)^(-1/2) - 1] exactly (luminal); a 575-650 km/s
     hill needs |F| = 2.0 x FK1's eps/m^2 -- the same fractional mass shift, now a HILL instead of a splitting.
  A4 [sympy] THE ENERGY-RECIPROCITY IDENTITY (the class-wide theorem): (i) particle level: for L = m v^2/2 - m Phi - W(x, v, t),
     dh/dt = dW/dt|_(x,v) on shell and the part of W linear in v drops out of h (a static current coupling does no work);
     (ii) field level: for any L_int(grad u, d_t grad u, dark fields), -dL_int/dt|_dark = -S . d_t grad u - d_t(Pi . d_t grad u),
     S = dL/d(grad u) - d_t Pi: between two static epochs the energy handed to the dark state is exactly -Int dt d^3x S . d_t grad u,
     and |S| <= delta |P| (P = q' grad u/4 pi G the phantom's flux) bounds it by max(delta) x the MOND sector's field energy for
     a field growing in magnitude (a field that also turns draws on the baryons' motion; B0 allows all their kinetic energy).
  A5 [sympy] THE EXACT BACK-REACTION per member: Euler-Lagrange of I_NR + L_int in spherical symmetry gives
     Phi' = u'(1 + q') + 4 pi G S (residual 0) with S = -2 rho_d V' u'/a0^2 (density), 2 g (d_t n_d) u'/a0^2 (rate), -G' rho_d w^2 u'/a0^2
     (inertia), g j (F + 2 I F') (current).  The rate member's back-reaction is proportional to d_t n_d only.
  B0 THE CLASS-WIDE ENERGY BOUND (numbers, both footings): unbinding the flagship's dark mass inside r_F (retaining the flagship's
     allowed fraction) needs a NET energy input larger than the MOND sector's entire field energy in the host (to 2 r_200), and
     larger than that plus all the baryons' kinetic energy: so by A4 every coupling that supplies it from the MOND sector, at
     any order and with any velocity weighting, must reach delta > 1 where the dark state sits during the clearing.
  B1 LINEAR SPATIAL-CURRENT (MAGNETIC) MEMBERS: no work in a static host (A4); in spherical symmetry pure gauge.  Even with
     every particle's direction re-chosen to minimise its time inside r_F (AT1's retention, its sudden potential iteration),
     the retained dark mass leaves the flagship above 0.10 dex on every host and footing.
  B2 THE WEIGHTED MEMBERS AT THE CEILING (density w = 1, inertia w ~ v^2, anisotropic inertia w ~ v_r^2): with FP4's (generous)
     delta = 1 cap, in both physical switch-on readings (slow: orbit-averaged gains; sudden: gains at a random phase), the
     flagship stays above 0.10 dex on every host and footing -- also when the inertia members' own speed-up inside the region
     is granted (time inside divided by sqrt(1 + G_max)).
  B3 (reported) the ENVELOPE reading (every particle handed the orbit-maximum of its weighted gain, i.e. timed at pericentre,
     unattainable by a population), with FP4's cap and with the health-enforced (Eulerian, delta <= 1 at every time) cap.
  B4 ORDERING: for every weighted member (slow reading, FP4's cap) the X-COP reference cluster keeps LESS of its dark mass
     inside R500 than any flagship host keeps inside r_F (clusters cleared first: anti-selective); the B0 cost ratio agrees.
  B5 THE RATE MEMBER (d): its back-reaction vanishes for a static dark state (A5), so it pays nothing before or after a
     clearing -- but by A4 it pays during the clearing, delta >= the B0 ratio, which is beyond FP5's (N, U) determinant zero
     (H4): the core is ill-posed while it clears.  (Reported: its natural ordering by growth rate, its clock-frame dependence.)
  B6 THE WINDOW IS NOT PREDICTED: no member supplies a universal 575-675 km/s from (a0, rho_Lambda, m): each needs its own
     fitted strength (g, F, G) or scales with its host.
  H1 [sympy] Minkowski: ghost-free iff A > 0, gradient-stable iff B, B + C > 0, speed^2 = (B + C cos^2)/A; per member.
  H2 [sympy] THE WEIGHTING THEOREM: a coupling that hands more energy to faster dark particles without a rest-energy well needs
     d(s^2)/dI > 0: the dark field propagates outside the metric light cone (only the clock's foliation can order it).
  H3 [sympy] FRW: I = 0 there, so every I-member is off; the free field's homogeneous mode has p = 0 exactly (dust).
  H4 [sympy] STATIC MOND BACKGROUND: FP5's committed (N, U) determinant k^4 (2 C_e alpha_c + 2 C_e c_CH + alpha_c c_CH) with the
     reciprocal suppression C_e -> (1 - delta) C_e vanishes at delta* = 1 + alpha_c c_CH/(2 C_e (alpha_c + c_CH)) = 1 + O(1e-9):
     FP4's ceiling delta = 1 is also the core's health boundary; the Psi sector at the ceilings (numbers).
  G1 THE BEST HEALTHY COUPLING is -F(I) g^{mn} dPsi* dPsi (luminal, ghost-free, A3: exactly FP4's density class): its gates are
     FP4's committed delta = 1 rows, loaded read-only -- it FAILS the flagship.
  G2 (reported) THE BEST-CLEARING COUPLING (the superluminal inertia member): X-COP and the z = 0 galaxies from its retention.
  W  the ledger.
HISTORY (stated).  Two bounds were tried in scratch probes and are not used: a per-particle reductio in the potential of the
  successful end state (it double-counts the self-gravity of the departing mass) and a total-energy bound for moving the dark
  mass to a cold shell just outside r_F (vacuous: it lets a hot halo be rearranged into a cold shell, which Liouville forbids).
  The rate member's back-reaction was first estimated with a spurious n_d d_t grad u term; A5's Euler-Lagrange shows it
  cancels exactly.  B0's bound is for UNBINDING (the unbound part ends at E >= 0, so the Liouville loophole does not arise).
  After a smoke run (not committed) three checks were corrected: A5's residual had a sign slip (EL - d_r[r^2 flux], as the
  scratch derivation had it); A3's tolerance was tighter than the O(beta) term it tests (now the exact ratio against its
  series); C0c compared with L321's frac_inside, whose nodes beyond the turning points carry an artificial weight (4% at
  r_F), and is now the quadrature's own convergence.  B0's claim was worded "> 5x"; it is the logical requirement "> 1"
  (the smoke run measured 4.9-8.7 with the baryons' kinetic energy added, 7.2-11.9 without).
MUTATE=1 (both flips load-bearing): (i) A2 claims the current coupling without its diamagnetic term (the naive reading "a
  current coupling is only a current coupling") -- the identity must FAIL; (ii) B1's magnetic member is handed the hand-set
  600 km/s kick (AT1's A2 cell) as if a current coupling could push -- the flagship then passes and B1 must FAIL.  rc = 1.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP8_current_coupling_kick.py
"""
import os, sys, io, re, json, math, time, contextlib, warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")                                   # shared machine: at most two workers
for _v in ("AT1_THREADS", "AT3_THREADS", "L357_THREADS"):
    os.environ[_v] = "2"
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FP8_FAST", "0") == "1"                        # smoke test only (fewer particles); never committed
SLUG = "FP8_current_coupling_kick" + ("_MUTATE" if MUTATE else "")
T0 = time.time()
NW = 2
NPART = 1500 if FAST else 6000
OUT = {"lane": "FP8", "mutate": MUTATE, "fast": FAST, "checks": {}, "numbers": {}, "ledger": []}
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


def elapsed():
    return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: (i) A2 without the diamagnetic term -- A2 must FAIL; (ii) B1's magnetic member handed the hand-set "
      "600 km/s kick -- B1 must FAIL ***")

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
os.environ["MUTATE"], os.environ["FAST"] = "0", "0"                  # the loaded lanes' own controls stay off
PA3 = os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT3_acceleration_trigger_full_gates.py")
_s3 = open(PA3).read()
_h3 = _s3.split("# ================================================================================================ C1 control")[0]
_h3 = _h3.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
A3 = {"__name__": "at3", "__file__": PA3}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_h3, A3)
if _env_mut is None: os.environ.pop("MUTATE", None)
else: os.environ["MUTATE"] = _env_mut
if _env_fast is None: os.environ.pop("FAST", None)
else: os.environ["FAST"] = _env_fast
A1, L57, Lm = A3["A1"], A3["L57"], A3["Lm"]
retained_acc, r_trigger, r_v_profile = A3["retained_acc"], A3["r_trigger"], A3["r_v_profile"]
hernquist, nfw21, FB, GK = A3["hernquist"], A3["nfw21"], A3["FB"], A3["GK"]
FOOT, A0K = A3["FOOT"], A3["A0K"]
CL, CLREF, cl_mass_fn, GAL = A3["CL"], A3["CLREF"], A3["cl_mass_fn"], A3["GAL"]
RHOC0_KPC, Ez2, RHO_C0, c200_z0 = A3["RHOC0_KPC"], A3["Ez2"], A3["RHO_C0"], A3["c200_z0"]
Re_kpc, halo_mass, c200_20, g_nfw = A1["Re_kpc"], A1["halo_mass"], A1["c200_20"], A1["g_nfw"]
nu20, nu_mono_bk1, G20, KPC20, MSUN20 = A1["nu20"], A1["nu_mono"], A1["G20"], A1["KPC"], A1["MSUN"]
nu_core = L57["nu_mono"]
potential, frac_inside, RG = Lm["potential"], Lm["frac_inside"], Lm["RG"]
Gk21, GE_CL, GE_GAL, nu21 = Lm["Gk"], Lm["GE_CL"], Lm["GE_GAL"], Lm["nu"]
FEET = ("canonical", "alt")


def nu_rar(y):
    return 1.0 / (-np.expm1(-np.sqrt(np.maximum(np.asarray(y, float), 1e-300))))


def nu_k(s):
    """the core's kernel (as FP4): nu_mono, equal to nu_RAR's closed form below y = 2.337."""
    s = np.asarray(s, float)
    return np.where(s <= 2.0, nu_rar(s), np.asarray(nu_core(np.maximum(s, 1e-12)), float))


# FP4's own functions, exec'd from its committed source (read-only): the ceiling, and the reciprocal X-COP / galaxy scores
PF4 = os.path.join(HERE, "FP4_kick_from_action.py")
_s4 = open(PF4).read()
NS4 = dict(math=math, np=np, nfw21=nfw21, FB=FB, GK=GK, nu_k=nu_k, A0K=A0K, CL=CL, GAL=GAL, Lm=Lm, hernquist=hernquist,
           Gk21=Gk21, GE_CL=GE_CL, GE_GAL=GE_GAL, nu21=nu21)
exec(_s4[_s4.index("def nfw_rho(M200, c, rhoc, r):"):_s4.index("HOSTS = {}")], NS4)
exec(_s4[_s4.index("def xcop_recip(eps, f_, delta):"):_s4.index("def xcop_job(job):")], NS4)
nfw_rho, ceiling, dreq, xcop_recip, gal_recip = NS4["nfw_rho"], NS4["ceiling"], NS4["dreq"], NS4["xcop_recip"], NS4["gal_recip"]
J4 = json.load(open(os.path.join(HERE, "FP4_kick_from_action_results.json")))
J5 = json.load(open(os.path.join(HERE, "FP5_dof_and_a0_field_results.json")))
JFK1 = json.load(open(os.path.join(REPO, "real_research", "dark_fluid_kick_2026", "FK1_kick_as_phase_change_results.json")))
P(f"  AT3's head (AT1, L357, L320, BK1, L321, L355, L360) and FP4's ceiling/X-COP/galaxy functions loaded   {elapsed()}")
P(f"  footings: FP0 {A0_FP0['canonical']:.4e} / {A0_FP0['alt']:.4e} m/s^2; the machinery's {FOOT['canonical']:.4e} / {FOOT['alt']:.4e}")


# ------------------------------------------------------------------------------------------------ hosts (FP4's definitions)
def flag_host(f_, lMb):
    a0k, a0 = A0K[f_], FOOT[f_]
    z = 2.5; Mb = 10 ** lMb; mu = 0.5 * ((1 + z) / 2) ** 2
    Mh = halo_mass(Mb / (1 + mu), z); c_ = float(c200_20(Mh, z)); rhoc = RHOC0_KPC * Ez2(z)
    a_h = Re_kpc(Mb / (1 + mu), z) / 1.8153
    r_F = math.sqrt(G20 * Mb * MSUN20 / (0.1 * a0)) / KPC20
    H = dict(name=f"flagship 1e{lMb:g}", Mb=Mb, a=a_h, M200=Mh, c=c_, rhoc=rhoc, z=z, gate=r_F, r_t=r_trigger(Mb, a_h, 1.0, a0k),
             Mb_fn=hernquist(Mb, a_h), kind="flagship")
    H["cap"] = ceiling(H["Mb_fn"], Mh, c_, rhoc, a0k)
    r_out_m = r_F * KPC20
    H["gb"] = G20 * Mb * MSUN20 / r_out_m ** 2; H["gcf"] = g_nfw(Mh, z, r_out_m)
    return H


def xcop_host(f_):
    a0k = A0K[f_]
    H = dict(name="X-COP ref", Mb=CLREF["Mb"], a=None, M200=CLREF["M200"], c=CLREF["c"], rhoc=CLREF["rhoc"], z=CLREF["z"],
             gate=CLREF["R500"], r_t=r_v_profile(cl_mass_fn, 1.0, a0k, rmax=5 * CLREF["R500"]), Mb_fn=cl_mass_fn, kind="cluster")
    H["cap"] = ceiling(cl_mass_fn, H["M200"], H["c"], H["rhoc"], a0k)
    return H


def gal_host(f_, kh):
    a0k = A0K[f_]; hst = GAL[kh]; c_ = float(c200_z0(hst["M200"]))
    H = dict(name=kh, Mb=hst["Mb"], a=hst["a"], M200=hst["M200"], c=c_, rhoc=RHO_C0, z=0.0, gate=hst["rg"],
             r_t=r_v_profile(hernquist(hst["Mb"], hst["a"]), 1.0, a0k), Mb_fn=hernquist(hst["Mb"], hst["a"]), kind="galaxy z=0")
    H["cap"] = ceiling(H["Mb_fn"], hst["M200"], c_, RHO_C0, a0k)
    return H


def shift_of(ret, H, f_, delta):
    """FP4's flagship formula (both kernels, largest |shift|): 2 log[(g_b + (nu - 1) g_b (1 - delta ret) + g_c ret)/(nu g_b)]."""
    a0 = FOOT[f_]; gb, gcf = H["gb"], H["gcf"]; out = []
    for nf in (nu20, nu_mono_bk1):
        nu_ = float(nf(gb / a0))
        out.append(2 * math.log10((gb + (nu_ - 1) * gb * max(1 - delta * ret, 0.0) + gcf * ret) / (nu_ * gb)))
    return max(out, key=abs)


def ret_allowed(H, f_, delta):
    """the largest retained fraction inside r_F that keeps |shift| <= 0.10 dex on both kernels."""
    a0 = FOOT[f_]; gb, gcf = H["gb"], H["gcf"]; r_ = []
    for nf in (nu20, nu_mono_bk1):
        nu_ = float(nf(gb / a0)); x_ = gcf / gb
        r_.append(nu_ * (10 ** 0.05 - 1) / (x_ - (nu_ - 1) * delta))
    return min(r_)


def cumint(y, x):
    return np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))])


def q_of_s(s):
    """q(s^2) = Int_0^s (nu(s') - 1) 2 s' ds' -- the MOND sector's own energy function (q' = nu - 1)."""
    s = np.asarray(s, float)
    sg = np.geomspace(1e-9, max(float(np.max(s)), 1e-6) * 1.01, 60000)
    return np.interp(s, sg, cumint((nu_k(sg) - 1.0) * 2 * sg, sg))


FLAG_KEYS = [(f_, l_) for f_ in FEET for l_ in (10.0, 10.5, 11.0)]
HOSTS = {}
for f_, l_ in FLAG_KEYS:
    HOSTS[(f_, f"flagship 1e{l_:g}")] = flag_host(f_, l_)
for f_ in FEET:
    HOSTS[(f_, "X-COP ref")] = xcop_host(f_)
    for kh in GAL:
        HOSTS[(f_, kh)] = gal_host(f_, kh)
P(f"  hosts built: {len(HOSTS)} (6 flagship at z = 2.5, the X-COP reference cluster, L321's three z = 0 galaxies; both footings)   {elapsed()}")

# ================================================================================================ C0 controls
banner("C0  CONTROLS: the loaded machinery reproduces committed numbers")
_b5 = J4["numbers"]["B5"]
dev_b5 = max(abs(dreq(HOSTS[(f_, f'flagship 1e{l_:g}')]["cap"], HOSTS[(f_, f'flagship 1e{l_:g}')]["gate"])[0]
                 - _b5[f"{f_}|flagship 1e{l_:g}"]["delta_req_rF"]) for f_, l_ in FLAG_KEYS)
check("C0a CONTROL: FP4's own ceiling() (exec'd from its committed source) reproduces FP4's committed B5 delta_req at r_F on "
      "all six flagship hosts", f"max |dev| {dev_b5:.1e}", dev_b5 < 1e-9, load_bearing=False)
RGc = np.geomspace(RG[0], RG[-1], 700)


def prep(H, f_, N=None, seed=5):
    """AT1's retained_acc draws (identical order and seed): the (1 - f_b) NFW carrier truncated at r200, isotropic Jeans
    velocities in the Newtonian potential of baryons + carrier.  Returns the sample and the potential."""
    N = NPART if N is None else N
    Mb_fn = H["Mb_fn"]
    Mn, r200, rs = nfw21(H["M200"], H["c"], H["rhoc"])
    Mc0 = lambda x: (1 - FB) * Mn(np.minimum(x, r200))
    rng = np.random.default_rng(seed)
    u = rng.random(N) * float(Mc0(r200)); rgrid = np.geomspace(1e-3 * rs, r200, 5000)
    r = np.interp(u, Mc0(rgrid), rgrid); w = float(Mc0(r200)) / N
    g_pre, Phi0 = potential(Mb_fn, Mc0, 0.0, "newtonian")
    rho = np.where(RG < r200, 1.0 / ((RG / rs) * (1 + RG / rs) ** 2), 1e-300)
    integ = rho * g_pre; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    sig2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / np.maximum(rho, 1e-300)
    v = rng.normal(0, 1, (N, 3)) * np.sqrt(np.interp(r, RG, sig2))[:, None]
    _ = rng.random(N)
    nh = rng.normal(0, 1, (N, 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
    vr0, vt0 = v[:, 0], np.linalg.norm(v[:, 1:], axis=1)
    return dict(H=H, f_=f_, r=r, w=w, v=v, nh=nh, vr0=vr0, vt0=vt0, L0=r * vt0, E0=0.5 * (vr0 ** 2 + vt0 ** 2) + np.interp(r, RG, Phi0),
                Phi0=Phi0, g0=g_pre, Mc0=Mc0, r200=r200, rs=rs, Mb_fn=Mb_fn)


def mass_in(S, vv, Lmin=False, iters=2, nL=9):
    """AT1's retention (its mass_in, sudden potential iteration twice) for velocities vv at the drawn positions; with Lmin
    every particle's velocity DIRECTION is re-chosen (speed kept) to minimise its time inside the gate: the most a
    momentum-only (magnetic) coupling could do."""
    H, r, w = S["H"], S["r"], S["w"]
    vr_, vt_ = vv[:, 0], np.linalg.norm(vv[:, 1:], axis=1); L = r * vt_; spd = np.sqrt(vr_ ** 2 + vt_ ** 2)
    Mc = S["Mc0"]
    for it in range(iters + 1):
        _, Phi = potential(S["Mb_fn"], Mc, 0.0, "newtonian")
        E = 0.5 * spd ** 2 + np.interp(r, RG, Phi)
        if Lmin:
            best, bestL = None, None
            for fL in np.linspace(0.0, 1.0, nL):
                Lt = fL * r * spd
                fr = frac_inside(E, Lt, Phi, H["gate"])
                if best is None:
                    best, bestL = fr, Lt.copy()
                else:
                    m_ = fr < best; best = np.where(m_, fr, best); bestL = np.where(m_, Lt, bestL)
            L = bestL
        if it == iters:
            break
        probe = np.geomspace(0.02 * S["rs"], 3 * S["r200"], 24)
        prof = np.array([w * frac_inside(E, L, Phi, rg).sum() for rg in probe])
        Mc = (lambda pr=probe, pm=prof: (lambda x: np.interp(np.asarray(x, dtype=float), pr, pm, left=0.0)))()
    return float(w * frac_inside(E, L, Phi, H["gate"]).sum())


def scaled(S, e):
    """the gain e (per unit mass) added as kinetic energy along each particle's current velocity."""
    v2 = (S["v"] ** 2).sum(1)
    return S["v"] * np.sqrt(1 + 2 * np.maximum(e, 0.0) / np.maximum(v2, 1e-30))[:, None]


def orbit_avg(E, L, Phi, fns, K=48):
    """time averages and maxima over each orbit (E, L) in Phi of functions f(r, v^2, v_r^2) -- L321's frac_inside quadrature,
    with nodes outside the true turning points given zero weight."""
    N = len(E); avgs = [np.zeros(N) for _ in fns]; maxs = [np.zeros(N) for _ in fns]
    bound = E < 0
    Eb, Lb = E[bound], L[bound]
    vr2 = 2 * (Eb[:, None] - Phi[None, :]) - (Lb[:, None] / RG[None, :]) ** 2
    pos = vr2 > 0
    ip = np.argmax(pos, axis=1); ia = len(RG) - 1 - np.argmax(pos[:, ::-1], axis=1)
    rp = RG[np.maximum(ip - 1, 0)]; ra = RG[np.minimum(ia + 1, len(RG) - 1)]
    ph = (np.arange(K) + 0.5) * np.pi / K
    rm, D = 0.5 * (ra + rp), 0.5 * (ra - rp)
    rr = rm[:, None] - D[:, None] * np.cos(ph)[None, :]
    v2 = 2 * (Eb[:, None] - np.interp(rr, RG, Phi))
    vrr2 = v2 - (Lb[:, None] / rr) ** 2
    ins = vrr2 > 0
    wgt = np.where(ins, D[:, None] * np.sin(ph)[None, :] / np.sqrt(np.maximum(vrr2, 1e-300)), 0.0)
    ws = wgt.sum(1); okw = ws > 0
    for av, mx, fn in zip(avgs, maxs, fns):
        fv = fn(rr, np.maximum(v2, 0.0), np.maximum(vrr2, 0.0))
        av[bound] = np.where(okw, (wgt * fv).sum(1) / np.where(okw, ws, 1.0), fv[:, K // 2])
        mxv = np.where(ins, fv, -np.inf).max(1)
        mx[bound] = np.where(np.isfinite(mxv), mxv, fv[:, K // 2])
    return avgs, maxs


# C0b: this lane's copy of AT1's retention reproduces AT1's retained_acc (decay in place, isotropic 250 km/s kick)
_Hc = HOSTS[("canonical", "flagship 1e10.5")]
_Sc = prep(_Hc, "canonical", N=3000)
_mine = mass_in(_Sc, _Sc["v"] + 250.0 * _Sc["nh"]) / mass_in(_Sc, _Sc["v"])
_at1 = float(retained_acc(_Hc["Mb_fn"], _Hc["M200"], _Hc["c"], [_Hc["gate"]], np.inf, 250.0, _Hc["rhoc"], N=3000)[0][0])
check("C0b CONTROL: this lane's copy of AT1's retention (identical draws, decay in place, isotropic 250 km/s kick) reproduces "
      "AT1's retained_acc on the 1e10.5 flagship host", f"this lane {_mine:.6f}, AT1 {_at1:.6f}, |dev| {abs(_mine - _at1):.1e}",
      abs(_mine - _at1) < 1e-9, load_bearing=False)
_fq = [lambda x, v2, vr2: (x < _Hc["gate"]).astype(float), lambda x, v2, vr2: 0.5 * v2, lambda x, v2, vr2: 0.5 * vr2]
_a48, _ = orbit_avg(_Sc["E0"], _Sc["L0"], _Sc["Phi0"], _fq, K=48)
_a400, _ = orbit_avg(_Sc["E0"], _Sc["L0"], _Sc["Phi0"], _fq, K=400)
dev_q = max(float(abs(np.sum(a_) - np.sum(b_)) / max(abs(np.sum(b_)), 1e-300)) for a_, b_ in zip(_a48, _a400))
_fi = frac_inside(_Sc["E0"], _Sc["L0"], _Sc["Phi0"], _Hc["gate"])
dev_l321 = float(abs(np.sum(_a400[0]) - np.sum(_fi)) / np.sum(_fi))
check("C0c CONTROL: the orbit quadrature used for the gains (48 nodes, zero weight outside the turning points) is converged: "
      "the sample-summed time fraction inside r_F, orbit-averaged v^2 and v_r^2 agree with 400 nodes within 1%",
      f"max relative |dev| {dev_q:.4f}; (reported) L321's frac_inside, whose nodes beyond the turning points carry an artificial "
      f"weight, differs by {dev_l321:.3f} in the time inside r_F", dev_q < 0.01, load_bearing=False)
OUT["numbers"]["controls"] = dict(B5_dev=dev_b5, AT1_dev=abs(_mine - _at1), quad_conv_dev=dev_q, quad_vs_L321=dev_l321)
P(f"  controls done   {elapsed()}")

# ================================================================================================ A1 the current in the NR limit
banner("A1  THE TASK'S CURRENT IN THE NR LIMIT: J.n is the clock-frame number density, J^i the (reversed) number flux")
tS, xS = sp.symbols("t x", real=True)
mS = sp.symbols("m", positive=True)
amp = sp.Function("a", real=True)(tS, xS); thS = sp.Function("theta", real=True)(tS, xS)
Psi_ = sp.exp(-sp.I * mS * tS) * amp * sp.exp(sp.I * thS) / sp.sqrt(2 * mS)
Psic = sp.exp(sp.I * mS * tS) * amp * sp.exp(-sp.I * thS) / sp.sqrt(2 * mS)
dup = lambda F, mu: (-sp.diff(F, tS) if mu == 0 else sp.diff(F, xS))   # d^mu, eta = diag(-1, 1)
Jcur = [sp.simplify(sp.I * (Psic * dup(Psi_, mu) - Psi_ * dup(Psic, mu))) for mu in (0, 1)]
Jn = sp.simplify(-Jcur[0])                                              # n_m = (-1, 0): J.n = -J^0
res_n = sp.simplify(Jn - amp ** 2 * (1 - sp.diff(thS, tS) / mS))
res_f = sp.simplify(Jcur[1] + amp ** 2 * sp.diff(thS, xS) / mS)
check("A1 DERIVED: with Psi = e^{-imt} a e^{i theta}/sqrt(2m), J.n = a^2 (1 - theta_t/m) -> n_d (the number density in the clock "
      "frame) and J^x = -a^2 theta_x/m = -n_d v: a coupling to J.n is a density coupling, a coupling to the spatial J is a "
      "coupling to the dark flux", f"J^0 = {Jcur[0]}; J^x = {Jcur[1]}; residuals {res_n}, {res_f}", res_n == 0 and res_f == 0)

# ================================================================================================ A2 gauge reduction
banner("A2  GAUGE REDUCTION: a current coupling is a charged scalar in an external potential plus a DENSITY coupling")
Pf, Qf = sp.Function("P")(tS, xS), sp.Function("Q")(tS, xS)           # Psi and Psi*, varied independently
A0f, A1f = sp.Function("A_0")(tS, xS), sp.Function("A_1")(tS, xS)
gS, mm = sp.symbols("g m", positive=True)
eta = sp.diag(-1, 1)
dd = lambda F, mu: sp.diff(F, tS) if mu == 0 else sp.diff(F, xS)
Al = [A0f, A1f]
Lfree = -sum(eta[mu, mu] * dd(Qf, mu) * dd(Pf, mu) for mu in (0, 1)) - mm ** 2 * Qf * Pf
Jup = [sp.I * (Qf * eta[mu, mu] * dd(Pf, mu) - Pf * eta[mu, mu] * dd(Qf, mu)) for mu in (0, 1)]
LJ = gS * sum(Al[mu] * Jup[mu] for mu in (0, 1))
DP = [dd(Pf, mu) + sp.I * gS * Al[mu] * Pf for mu in (0, 1)]
DQ = [dd(Qf, mu) - sp.I * gS * Al[mu] * Qf for mu in (0, 1)]
AA = sum(eta[mu, mu] * Al[mu] ** 2 for mu in (0, 1))
claim_A2 = -sum(eta[mu, mu] * DQ[mu] * DP[mu] for mu in (0, 1)) - mm ** 2 * Qf * Pf + gS ** 2 * AA * Qf * Pf
if MUTATE:
    claim_A2 = claim_A2 - gS ** 2 * AA * Qf * Pf                         # MUTATE (i): the naive reading, no diamagnetic term
res_A2 = sp.simplify(sp.expand(Lfree + LJ - claim_A2))
chiS = sp.Function("chi")(tS, xS); Pp, Qp = sp.Function("Pp")(tS, xS), sp.Function("Qp")(tS, xS)
subg = {Pf: sp.exp(-sp.I * gS * chiS) * Pp, Qf: sp.exp(sp.I * gS * chiS) * Qp, A0f: sp.diff(chiS, tS), A1f: sp.diff(chiS, xS)}
Lg = (Lfree + LJ).subs(subg).doit()
tgt_g = (-sum(eta[mu, mu] * dd(Qp, mu) * dd(Pp, mu) for mu in (0, 1)) - mm ** 2 * Qp * Pp
         + gS ** 2 * sum(eta[mu, mu] * dd(chiS, mu) ** 2 for mu in (0, 1)) * Qp * Pp)
res_grad = sp.simplify(sp.expand(Lg - tgt_g))
P(f"    -|dPsi|^2 - m^2|Psi|^2 + g A.J  -  [ -|(d + i g A)Psi|^2 - m^2|Psi|^2 + g^2 A.A |Psi|^2 ] = {res_A2}"
  + ("   <- MUTATE: diamagnetic term dropped" if MUTATE else ""))
P(f"    A = d chi, Psi = e^(-i g chi) Psi':  L - [ -|dPsi'|^2 - m^2 |Psi'|^2 + g^2 (d chi)^2 |Psi'|^2 ] = {res_grad}")
P("    so: (c) g J.d chi is FP4's density class at O(g^2) (m^2 -> m^2 - g^2 (d chi)^2: a WELL for spatial gradients);")
P("        (b) g (J.n) f: A = f n, A.A = -f^2 -> an electrostatic potential g f per particle plus m^2 -> m^2 + g^2 f^2 (healthy);")
P("        (e) spatial A: only B = curl A (magnetic, no work) and E = -d_t A are physical")
check("A2 DERIVED (gauge reduction): -|dPsi|^2 + g A.J == -|(d + igA)Psi|^2 + g^2 A.A |Psi|^2 identically, and for A = d chi the "
      "field redefinition removes the current coupling exactly, leaving the density coupling g^2 (d chi)^2 |Psi|^2"
      + ("  [MUTATE: without the diamagnetic term]" if MUTATE else ""),
      f"identity residual {res_A2}; gradient-reduction residual {res_grad}", res_A2 == 0 and res_grad == 0,
      "a current coupling to a gradient does nothing at O(g) (pure gauge) and is FP4's density class at O(g^2); a coupling to "
      "J.n is an electrostatic potential, i.e. FP4's class; only a curl (magnetic) or a clock-frame rate survives")

# ================================================================================================ A3 rest-energy reduction
banner("A3  REST-ENERGY REDUCTION: the kinetic couplings' dispersion; which are density couplings, which change inertia")
kS, kpS = sp.symbols("k k_par", positive=True)
FS, GSy, beta = sp.symbols("F G beta", real=True)
MEM_KIN = {"isotropic -F(I) g^mn": (1 + FS, 1 + FS, 0), "temporal -F(I) n^m n^n": (1 + FS, 1, 0),
           "spatial -G(I) h^mn": (1, 1 + GSy, 0), "anisotropic -G(I) e^m e^n": (1, 1, GSy)}
A3tab = {}
for nm_, (Aco, Bco, Cco) in MEM_KIN.items():
    om = sp.sqrt((Bco * (kS ** 2 + kpS ** 2) + Cco * kpS ** 2 + mS ** 2) / Aco)     # k: across e, k_par: along e
    Rr = sp.simplify(om.subs({kS: 0, kpS: 0}))
    inv_perp = sp.simplify(sp.diff(om.subs(kpS, 0), kS, 2).subs(kS, 0))
    inv_par = sp.simplify(sp.diff(om.subs(kS, 0), kpS, 2).subs(kpS, 0)) if Cco != 0 else inv_perp
    sp_perp = sp.simplify(sp.limit(om.subs(kpS, 0) ** 2 / kS ** 2, kS, sp.oo))
    sp_par = sp.simplify(sp.limit(om.subs(kS, 0) ** 2 / kpS ** 2, kpS, sp.oo)) if Cco != 0 else sp_perp
    A3tab[nm_] = dict(rest=Rr, inv_inertia_perp=inv_perp, inv_inertia_par=inv_par, speed2_perp=sp_perp, speed2_par=sp_par)
    P(f"    {nm_:28s}: rest energy {Rr}; 1/inertia {inv_perp} (along e: {inv_par}); speed^2 {sp_perp} (along e: {sp_par})")
V_iso = sp.simplify(A3tab["isotropic -F(I) g^mn"]["rest"] / mS - 1)
Fp1 = sp.symbols("Fp1", positive=True)                                  # 1 + F > 0: the ghost-free branch (H1)
iso_is_density = sp.simplify((V_iso - (1 / sp.sqrt(1 + FS) - 1)).subs(FS, Fp1 - 1)) == 0 \
                 and sp.simplify(A3tab["isotropic -F(I) g^mn"]["speed2_perp"] - 1) == 0 \
                 and sp.simplify(A3tab["isotropic -F(I) g^mn"]["speed2_par"] - 1) == 0
F_kick = sp.solve(sp.Eq(1 / sp.sqrt(1 + FS) - 1, beta / 2), FS)[0]
ratio_series = sp.series(-F_kick / (beta / (2 - beta)), beta, 0, 2).removeO()
fk1 = JFK1["numbers"]["K2"]["eps_over_m2"]
F_num = {k_: float(-F_kick.subs(beta, (float(k_) / C_KMS) ** 2)) for k_ in fk1}
F_ratio = {k_: F_num[k_] / v_ for k_, v_ in fk1.items()}
P(f"    isotropic member: V/c^2 = {V_iso} per unit rest mass (a density coupling, luminal); a hill of v^2/2 needs F = {F_kick}; "
  f"|F|/(FK1 eps/m^2) = {ratio_series} + O(beta^2): " + ", ".join(f"{k_} km/s {F_num[k_]:.3e} ({F_ratio[k_]:.4f}x)" for k_ in fk1))
ok_a3 = iso_is_density and sp.simplify(ratio_series - (2 - 5 * beta / 2)) == 0 \
        and all(abs(F_ratio[k_] - (2 - 2.5 * (float(k_) / C_KMS) ** 2)) < 1e-8 for k_ in F_ratio) \
        and sp.simplify(A3tab["spatial -G(I) h^mn"]["rest"] - mS) == 0 and sp.simplify(A3tab["anisotropic -G(I) e^m e^n"]["rest"] - mS) == 0
check("A3 DERIVED (rest-energy reduction): -F(I) g^{mn} dPsi* dPsi is exactly the density coupling V = c^2[(1+F)^(-1/2) - 1] "
      "(rest energy m/sqrt(1+F), luminal); the temporal member shifts the rest energy AND the speed (1/(1+F)); the spatial and "
      "anisotropic members leave the rest energy and change only the inertia; a 575-650 km/s hill needs |F| = 2.0 x FK1's "
      "eps/m^2", f"V_iso = {V_iso}; |F|/(eps/m^2) = {ratio_series}; " + ", ".join(f"{k_}: {F_ratio[k_]:.5f}" for k_ in fk1), ok_a3,
      "the derivative door is the density door with a different name: the kinetic coupling's hill is a rest-mass hill, "
      "FK1's latent heat written as a place-dependent mass, and it pays FP4's reciprocity exactly")
OUT["numbers"]["A3"] = dict(table={k_: {kk: str(vv) for kk, vv in v_.items()} for k_, v_ in A3tab.items()}, F_kick=str(F_kick),
                            F_num=F_num, F_over_FK1=F_ratio)

# ================================================================================================ A4 the energy-reciprocity identity
banner("A4  THE ENERGY-RECIPROCITY IDENTITY: energy reaches the dark state from the MOND sector only through S, its back-reaction")
xP, vP, tP, mP = sp.symbols("x v t m", real=True)
PhiP = sp.Function("Phi")(xP)
W0, W1, W2, W4 = [sp.Function(f"W{i}")(xP, tP) for i in (0, 1, 2, 4)]
Wp = W0 + W1 * vP + W2 * vP ** 2 + W4 * vP ** 4
Lp = mP * vP ** 2 / 2 - mP * PhiP - Wp
pv = sp.diff(Lp, vP)
hP = sp.expand(vP * pv - Lp)
aS = sp.symbols("a", real=True)
a_sol = sp.solve(sp.Eq(sp.diff(pv, xP) * vP + sp.diff(pv, vP) * aS + sp.diff(pv, tP), sp.diff(Lp, xP)), aS)[0]
res_p = sp.simplify(sp.diff(hP, xP) * vP + sp.diff(hP, vP) * a_sol + sp.diff(hP, tP) - sp.diff(Wp, tP))
P(f"    particle: h = {sp.collect(hP, vP)};  dh/dt - dW/dt|_(x,v) on shell = {res_p};  h contains W1: {hP.has(W1)}")
tt_ = sp.symbols("t", real=True)
U1, nD = sp.Function("U1")(tt_), sp.Function("n")(tt_)
y1, y2, y3, y4 = sp.symbols("y1 y2 y3 y4")
Lgen = sp.Function("Lint")(y1, y2, y3, y4)
sub_ = {y1: U1, y2: sp.diff(U1, tt_), y3: nD, y4: sp.diff(nD, tt_)}
Lu_, Pi_ = sp.diff(Lgen, y1).subs(sub_), sp.diff(Lgen, y2).subs(sub_)
S_ = Lu_ - sp.diff(Pi_, tt_)
res_f4 = sp.simplify(sp.expand(-(Lu_ * sp.diff(U1, tt_) + Pi_ * sp.diff(U1, tt_, 2))
                               - (-S_ * sp.diff(U1, tt_) - sp.diff(Pi_ * sp.diff(U1, tt_), tt_))))
Gg, a0g = sp.symbols("G a_0", positive=True)
upS, updS, qpS = sp.symbols("u_p u_pdot q_p", positive=True)
res_b = sp.simplify(qpS * upS / (4 * sp.pi * Gg) * updS - a0g ** 2 * qpS / (8 * sp.pi * Gg) * (2 * upS * updS / a0g ** 2))
P(f"    field: -dL_int/dt|_dark + S u'_t + d/dt(Pi u'_t) = {res_f4}  (S = dL/du' - dPi/dt, Pi = dL/du'_t: generic L_int)")
P(f"    bound: P u'_t - (a0^2 q'/8 pi G) dI/dt = {res_b}  (P = q' u'/4 pi G; u'_t parallel to u')  =>  energy per volume between static")
P("           epochs <= max(delta) (a0^2/8 pi G) q(I): the MOND sector can hand over at most max(delta) x its own field energy")
check("A4 DERIVED (the energy-reciprocity identity): for a particle, dh/dt = dW/dt|_(x,v) and h has no linear-in-v part (a static "
      "current coupling does no work); for any L_int(grad u, d_t grad u, dark fields) the dark state's energy changes as "
      "-S.d_t grad u - d_t(Pi.d_t grad u) with S its source in the MOND sector's equation; with |S| <= delta |P| the energy "
      "handed over between static epochs is <= max(delta) x the MOND field energy (a0^2/8 pi G) Int q(I) for a field growing in "
      "magnitude",
      f"particle residual {res_p} (W1 in h: {hP.has(W1)}); field residual {res_f4}; flux-energy residual {res_b}",
      res_p == 0 and not hP.has(W1) and res_f4 == 0 and res_b == 0,
      "no coupling -- density, current, derivative, rate, any order, any velocity weighting -- can take energy from the MOND "
      "sector without an equal source S in the MOND sector's own equation; couplings only choose WHEN they pay it")

# ================================================================================================ A5 the exact back-reaction per member
banner("A5  THE EXACT BACK-REACTION ON THE MOND SECTOR'S SOURCE, member by member (Euler-Lagrange of I_NR + L_int, spherical)")
rS, tS2 = sp.symbols("r t", positive=True)
gg = sp.symbols("g", positive=True)
uF, PhF = sp.Function("u")(rS, tS2), sp.Function("Phi")(rS, tS2)
rhoF = sp.Function("rho")(rS, tS2)
qF, VF, GcF, FF = sp.Function("q"), sp.Function("V"), sp.Function("Gcoef"), sp.Function("F")
nF, rdF, wF, jF = [sp.Function(s_)(rS, tS2) for s_ in ("n", "rho_d", "w", "j")]
ur = sp.diff(uF, rS)
Ir = ur ** 2 / a0g ** 2
Isym = sp.symbols("I_s", positive=True)
dsub = lambda fn, order=1: sp.diff(fn(Isym), Isym, order).subs(Isym, Ir)
Lcore = -rhoF * PhF - (2 * sp.diff(PhF, rS) * ur - ur ** 2 - a0g ** 2 * qF(Ir)) / (8 * sp.pi * Gg)
MEMS = {
    "density  -rho_d V(I)": (-rdF * VF(Ir), lambda: -2 * rdF * dsub(VF) * ur / a0g ** 2),
    "rate     -g n_d d_t I  (== g J_perp.grad I)": (-gg * nF * sp.diff(Ir, tS2), lambda: 2 * gg * sp.diff(nF, tS2) * ur / a0g ** 2),
    "inertia  -G(I) rho_d w^2/2": (-GcF(Ir) * rdF * wF ** 2 / 2, lambda: -dsub(GcF) * rdF * wF ** 2 * ur / a0g ** 2),
    "current  g j F(I) u'  (J_perp . F grad u)": (gg * jF * FF(Ir) * ur, lambda: gg * jF * (FF(Ir) + 2 * Ir * dsub(FF))),
}
A5res = {}
for nm_, (Lint, Sfun) in MEMS.items():
    eq = euler_equations(rS ** 2 * (Lcore + Lint), [uF, PhF], [rS, tS2])[0]
    ELu = eq.lhs - eq.rhs
    Sx = Sfun()
    flux = (sp.diff(PhF, rS) - ur - dsub(qF) * ur) / (4 * sp.pi * Gg) - Sx
    A5res[nm_] = sp.simplify(sp.expand((ELu - sp.diff(rS ** 2 * flux, rS)).doit()))
    P(f"    {nm_:44s}: S = {sp.simplify(Sx)};  EL - d_r[r^2 flux] = {A5res[nm_]}")
elp = euler_equations(rS ** 2 * Lcore, [uF, PhF], [rS, tS2])[1]
pois = sp.simplify(elp.lhs - elp.rhs - rS ** 2 * (-rhoF + (sp.diff(uF, rS, 2) + 2 * sp.diff(uF, rS) / rS) / (4 * sp.pi * Gg)))
P(f"    Phi-equation: Lap u = 4 pi G rho (residual {pois}), unchanged by every member")
P("    => with a regular centre Phi' = u' (1 + q') + 4 pi G S = u' [1 + q'(1 - delta)], delta = -4 pi G S/(q' u'):")
P("       density: delta = 8 pi G rho_d V'/(a0^2 q')  (FP4 B1);  rate: delta = -8 pi G g d_t n_d/(a0^2 q')  (zero for a static dark state);")
P("       inertia: delta = 8 pi G G' (rho_d w^2/2)/(a0^2 q');  current: S = g j (F + 2 I F'), proportional to the dark current")
check("A5 DERIVED: the Euler-Lagrange equations of I_NR + L_int give Phi' = u'(1 + q') + 4 pi G S for every member (residual 0), "
      "with S = -2 rho_d V' u'/a0^2 (density), 2 g (d_t n_d) u'/a0^2 (rate: the n_d d_t u' terms cancel), -G' rho_d w^2 u'/a0^2 "
      "(inertia), g j (F + 2 I F') (current); the Poisson equation for u is untouched",
      "residuals " + ", ".join(f"{k_.split()[0]} {v_}" for k_, v_ in A5res.items()) + f"; Poisson {pois}",
      all(v_ == 0 for v_ in A5res.values()) and pois == 0,
      "the current and rate members write on the phantom only while the dark state FLOWS (j != 0, d_t n_d != 0): in a static "
      "halo they are silent -- and, by A4, they hand over nothing there either")
P(f"  part A done   {elapsed()}")

# ================================================================================================ B0 the class-wide energy bound
banner("B0  THE CLASS-WIDE ENERGY BOUND: unbinding the flagship's dark mass vs the MOND sector's whole field energy (+ the baryons')")


def energy_budget(H, f_):
    """cost of UNBINDING the dark mass inside the gate beyond the retained core (the innermost ret_allowed fraction, kinetic
    energy set to zero: generous), with self-gravity and the outer halo's potential change counted; against the MOND field
    energy Int (a0^2/8 pi G) q(I) dV to 2 r200 and the baryons' kinetic energy if all on circular orbits (generous)."""
    a0k = A0K[f_]
    Mn, r200, rs = nfw21(H["M200"], H["c"], H["rhoc"])
    r = np.geomspace(1e-4, 2 * r200, 20000)
    rho = np.where(r < r200, (1 - FB) * nfw_rho(H["M200"], H["c"], H["rhoc"], r)[0], 0.0)
    Md = (1 - FB) * Mn(np.minimum(r, r200)); Mb = H["Mb_fn"](r)
    g = GK * (Mb + Md) / r ** 2
    cum = cumint(rho * g, r); sig2 = np.where(rho > 0, (cum[-1] - cum) / np.maximum(rho, 1e-300), 0.0)
    gb = GK * Mb / r ** 2; cb = cumint(gb, r); Phib = -(cb[-1] - cb) - GK * Mb[-1] / r[-1]
    cg = cumint(g, r); Phi = -(cg[-1] - cg) - GK * (Mb[-1] + Md[-1]) / r[-1]
    dV = 4 * math.pi * r ** 2
    K = cumint(1.5 * rho * sig2 * dV, r); Wb = cumint(rho * Phib * dV, r); Ws = cumint(-GK * Md * rho * 4 * math.pi * r, r)
    gate = H["gate"]; Min = float(np.interp(gate, r, Md))
    ret = ret_allowed(H, f_, 1.0) if H["kind"] == "flagship" else 0.1
    Phi_out = -float(cumint(np.where(r >= gate, GK * rho * 4 * math.pi * r, 0.0), r)[-1])
    Mcore = ret * Min; rcore = float(np.interp(Mcore, Md[r <= gate], r[r <= gate]))
    Ein = float(np.interp(gate, r, K) + np.interp(gate, r, Wb) + np.interp(gate, r, Ws)) + Min * Phi_out
    Ecore = float(np.interp(rcore, r, Wb) + np.interp(rcore, r, Ws)) + Mcore * Phi_out
    cost = Ecore - Ein
    s = gb / a0k
    E_mond = float(cumint(a0k ** 2 / (8 * math.pi * GK) * q_of_s(s) * dV, r)[-1])
    dMb = np.gradient(Mb, r)
    K_b = float(cumint(0.5 * dMb * g * r, r)[-1])
    # the Eulerian (average-particle) price inside the gate: the delta the average particle's own escape energy needs
    e_esc = np.maximum(-Phi - 1.5 * sig2, 0.0)
    pref = 8 * math.pi * GK * rho / (a0k ** 2 * np.maximum(q_of_s(s), 1e-300))
    m_ = (r < gate) & (r > 1e-2) & (rho > 0)
    wm = (rho * dV * np.gradient(r))[m_]
    band = (r > 0.1 * gate) & (r < gate) & (rho > 0)
    return dict(cost=cost, E_mond=E_mond, K_b=K_b, ratio=cost / (E_mond + K_b), ratio_mond=cost / E_mond, ret=ret, Min=Min,
                cost_per_mass=cost / ((1 - ret) * Min), delta_esc_mean=float(np.sum((pref * e_esc)[m_] * wm) / np.sum(wm)),
                delta_esc_min=float((pref * e_esc)[band].min()))


EB = {}
for key, H in HOSTS.items():
    if H["kind"] in ("flagship", "cluster"):
        EB[key] = energy_budget(H, key[0])
for (f_, nm_), b_ in EB.items():
    P(f"    {f_:9s} {nm_:15s}: unbinding cost {b_['cost']:.2e} Msun (km/s)^2 ({b_['cost_per_mass']:.0f} (km/s)^2 per unbound Msun, "
      f"core kept {b_['ret']:.3f}); MOND field energy {b_['E_mond']:.2e}, baryon kinetic {b_['K_b']:.2e} -> cost/(both) "
      f"{b_['ratio']:.2f} (cost/MOND {b_['ratio_mond']:.2f}); average-particle delta to escape: mean {b_['delta_esc_mean']:.1f}, "
      f"min over 0.1-1 gate {b_['delta_esc_min']:.1f}")
fl_ratio = [EB[(f_, f"flagship 1e{l_:g}")]["ratio"] for f_, l_ in FLAG_KEYS]
cl_ratio_ = [EB[(f_, "X-COP ref")]["ratio_mond"] for f_ in FEET]
fl_ratio_mond = [EB[(f_, f"flagship 1e{l_:g}")]["ratio_mond"] for f_, l_ in FLAG_KEYS]
ok_b0 = min(fl_ratio) > 1.0
check("B0 DERIVED + NUMBERS (class-wide, any order, any weighting of the NET energy): unbinding the flagship's dark mass inside "
      "r_F down to the flagship's allowed core needs a net energy input larger than the MOND sector's whole field energy (to "
      "2 r200) -- and larger than that plus all the baryons' kinetic energy (a generous allowance for a rotating field) -- on "
      "every host and footing; so by A4 any coupling that supplies it from the MOND sector reaches delta > 1 where the dark state "
      "sits during the clearing (the no-go needs a ratio > 1)",
      f"cost/E_MOND {min(fl_ratio_mond):.2f}-{max(fl_ratio_mond):.2f}; cost/(E_MOND + K_b) {min(fl_ratio):.2f}-{max(fl_ratio):.2f} "
      f"(flagship); cost/E_MOND for X-COP {min(cl_ratio_):.2f}-{max(cl_ratio_):.2f}",
      ok_b0, f"the MOND sector is too soft to be the source: the dark halo inside r_F at z = 2.5 is bound by {min(fl_ratio_mond):.0f}-"
      f"{max(fl_ratio_mond):.0f}x more energy than the whole host's MOND field holds (for clusters the ratio is lower: the same "
      "measure is anti-selective).  Scope: this bounds the NET energy; a pure redistributor (zero net, e.g. a betatron-like "
      "magnetic member) would have to take it from the rest of the halo -- that case is B1's")
OUT["numbers"]["B0"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in EB.items()}
P(f"  B0 done   {elapsed()}")

# ================================================================================================ the retention runs
banner("B1-B4  THE RETENTION RUNS (AT1's machinery; FP4's delta = 1 cap and the health-enforced Eulerian cap)")


def cap_profiles(S):
    """delta = 1 caps on a radial grid.  FP4's (static final state, path-accumulated, density continued past r200 as in FP4's
    ceiling): V (density), G (isotropic inertia, pressure rho sigma^2 in place of rho, x 2/3), G_a = 3 G (anisotropic).
    Eulerian (health-enforced: delta <= 1 at every time where the dark state sits, H4): the same with the local
    density/pressure, V_E = a0^2 q(I)/(8 pi G rho_d), G_E = (2/3) a0^2 q(I)/(8 pi G rho_d sigma^2)."""
    H, f_ = S["H"], S["f_"]; a0k = A0K[f_]
    rr, V, _, _ = H["cap"]
    Mn, r200, rs = nfw21(H["M200"], H["c"], H["rhoc"])
    rho_c = (1 - FB) * nfw_rho(H["M200"], H["c"], H["rhoc"], rr)[0]
    gtr = GK * (H["Mb_fn"](rr) + (1 - FB) * Mn(np.minimum(rr, r200))) / rr ** 2
    ig = rho_c * gtr; cum = cumint(ig, rr)
    pres = (cum[-1] - cum) + rho_c[-1] * gtr[-1] * rr[-1] / 4.0         # rho ~ r^-3, g ~ r^-2 beyond the grid
    s = GK * H["Mb_fn"](rr) / rr ** 2 / a0k; I = s ** 2; qp = nu_k(s) - 1.0; dI = np.abs(np.gradient(I, rr))
    igG = qp * dI / pres; segG = 0.5 * (igG[1:] + igG[:-1]) * np.diff(rr)
    Gr = (2.0 / 3.0) * a0k ** 2 / (8 * math.pi * GK) * np.concatenate([np.cumsum(segG[::-1])[::-1], [0.0]])
    qI = q_of_s(s)
    VE = a0k ** 2 * qI / (8 * math.pi * GK * rho_c)
    GE = (2.0 / 3.0) * a0k ** 2 * qI / (8 * math.pi * GK * pres)
    return dict(rr=rr, V=V, G=Gr, Ga=3 * Gr, VE=VE, GE=GE, GaE=3 * GE)


def gains(S, cp, which="fp4"):
    """per-particle gains of the three weighted members in three readings.  slow: orbit averages (the host's MOND field grows
    over many orbits); sudden: at each particle's drawn phase; envelope: the orbit maximum (pericentre timing)."""
    rr = cp["rr"]
    Vp, Gp, Gap = (cp["V"], cp["G"], cp["Ga"]) if which == "fp4" else (cp["VE"], cp["GE"], cp["GaE"])
    Vf = lambda x: np.interp(x, rr, Vp); Gf = lambda x: np.interp(x, rr, Gp); Gaf = lambda x: np.interp(x, rr, Gap)
    fns = [lambda x, v2, vr2: Vf(x), lambda x, v2, vr2: Gf(x) * 0.5 * v2, lambda x, v2, vr2: Gaf(x) * 0.5 * vr2]
    (aV, aG, aGa), (mV, mG, mGa) = orbit_avg(S["E0"], S["L0"], S["Phi0"], fns)
    r, v2, vr2 = S["r"], S["vr0"] ** 2 + S["vt0"] ** 2, S["vr0"] ** 2
    return {"density": dict(slow=aV, sudden=Vf(r), envelope=np.maximum(mV, Vf(r))),
            "inertia": dict(slow=aG, sudden=Gf(r) * 0.5 * v2, envelope=np.maximum(mG, Gf(r) * 0.5 * v2)),
            "anisotropic": dict(slow=aGa, sudden=Gaf(r) * 0.5 * vr2, envelope=np.maximum(mGa, Gaf(r) * 0.5 * vr2))}


def run_host(key, plan):
    """plan: list of (label, member, reading, capset) plus the special labels 'magnetic' and 'mutate600'."""
    f_, nm_ = key
    H = HOSTS[key]
    S = prep(H, f_)
    m0 = mass_in(S, S["v"])
    cp = cap_profiles(S)
    G_fp4 = {}
    out = {"m0": m0, "Gmax": float(cp["G"][0]), "GmaxE": float(np.max(cp["GE"][cp["rr"] < 3 * H["gate"]])),
           "Vmax": float(cp["V"][0]), "VmaxE": float(np.max(cp["VE"][cp["rr"] < 3 * H["gate"]]))}
    for label, mem, rd_, capset in plan:
        if label == "magnetic":
            out[label] = mass_in(S, S["v"], Lmin=True) / m0
            continue
        if label == "mutate600":
            out[label] = mass_in(S, S["v"] + 600.0 * S["nh"]) / m0
            continue
        if capset not in G_fp4:
            G_fp4[capset] = gains(S, cp, capset)
            out[f"mean_slow_gain|{capset}"] = {mm_: float(np.mean(G_fp4[capset][mm_]["slow"])) for mm_ in G_fp4[capset]}
        out[label] = mass_in(S, scaled(S, G_fp4[capset][mem][rd_])) / m0
    return key, out


PLAN_FLAG = [("magnetic", None, None, None)] + ([("mutate600", None, None, None)] if MUTATE else []) + \
            [(f"{mem}|{rd_}|fp4", mem, rd_, "fp4") for mem in ("density", "inertia", "anisotropic") for rd_ in ("slow", "sudden", "envelope")] + \
            [(f"{mem}|{rd_}|eul", mem, rd_, "eul") for mem in ("density", "inertia", "anisotropic") for rd_ in ("slow", "envelope")]
PLAN_CL = [(f"{mem}|slow|fp4", mem, "slow", "fp4") for mem in ("density", "inertia", "anisotropic")] + [("inertia|envelope|fp4", "inertia", "envelope", "fp4")]
PLAN_GAL = [("density|slow|fp4", "density", "slow", "fp4"), ("inertia|slow|fp4", "inertia", "slow", "fp4")]
jobs = [(k_, PLAN_FLAG) for k_ in HOSTS if HOSTS[k_]["kind"] == "flagship"] + \
       [(k_, PLAN_CL) for k_ in HOSTS if HOSTS[k_]["kind"] == "cluster"] + \
       [(k_, PLAN_GAL) for k_ in HOSTS if HOSTS[k_]["kind"] == "galaxy z=0"]
with ThreadPoolExecutor(NW) as ex:
    RUN = dict(ex.map(lambda j: run_host(*j), jobs))
P(f"  retention runs done ({len(jobs)} hosts, {NPART} particles each)   {elapsed()}")

# ------------------------------------------------------------------------------------------------ B1 magnetic members
banner("B1  LINEAR SPATIAL-CURRENT (MAGNETIC) MEMBERS: no work in a static host; even perfect re-direction leaves the halo")
B1 = {}
for f_, l_ in FLAG_KEYS:
    key = (f_, f"flagship 1e{l_:g}"); H = HOSTS[key]; R_ = RUN[key]
    ret = R_["mutate600"] if MUTATE else R_["magnetic"]
    B1[key] = dict(ret=ret, shift_d0=shift_of(ret, H, f_, 0.0), shift_d1=shift_of(ret, H, f_, 1.0), ret_allowed=ret_allowed(H, f_, 0.0))
    P(f"    {f_:9s} {H['name']:15s}: " + ("hand-set 600 km/s kick (MUTATE)" if MUTATE else "every direction re-chosen (speed kept)")
      + f": retained inside r_F {ret:.3f} (allowed {B1[key]['ret_allowed']:.3f}) -> shift {B1[key]['shift_d0']:+.3f} dex (S = 0: "
      f"no suppression; with delta = 1 it would be {B1[key]['shift_d1']:+.3f})")
b1_min = min(v_["shift_d0"] for v_ in B1.values())
check("B1 DERIVED + NUMBERS: a linear coupling to the spatial current (magnetic, or a gradient: pure gauge) does no work in a static "
      "host (A4: its part of W is linear in v); even re-choosing every particle's direction to minimise its time inside r_F "
      "(AT1's retention, sudden potential iteration) keeps the flagship above 0.10 dex on every host and footing"
      + (" [MUTATE: the hand-set 600 km/s kick]" if MUTATE else ""),
      f"retained {min(v_['ret'] for v_ in B1.values()):.3f}-{max(v_['ret'] for v_ in B1.values()):.3f}; smallest shift {b1_min:+.3f} dex",
      b1_min > 0.10, "in spherical symmetry the member is pure gauge (retention 1); the re-direction floor is the most any "
      "non-spherical (magnetic) field could do, and energy conservation keeps the deep particles inside r_F")
OUT["numbers"]["B1"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in B1.items()}

# ------------------------------------------------------------------------------------------------ B2 weighted members
banner("B2  THE WEIGHTED MEMBERS AT FP4's delta = 1 CAP: slow and sudden switch-on (with the inertia members' own speed-up granted)")
B2 = {}
for f_, l_ in FLAG_KEYS:
    key = (f_, f"flagship 1e{l_:g}"); H = HOSTS[key]; R_ = RUN[key]
    row = {}
    for mem in ("density", "inertia", "anisotropic"):
        Gc = {"density": 0.0, "inertia": R_["Gmax"], "anisotropic": 3 * R_["Gmax"]}[mem]
        for rd_ in ("slow", "sudden"):
            ret = R_[f"{mem}|{rd_}|fp4"]; ret_c = ret / math.sqrt(1 + Gc)
            row[f"{mem}|{rd_}"] = dict(ret=ret, ret_speedup=ret_c, shift=shift_of(ret, H, f_, 1.0), shift_speedup=shift_of(ret_c, H, f_, 1.0))
    B2[key] = row
    P(f"    {f_:9s} {H['name']:15s} (G_max {R_['Gmax']:.2f}): " + "; ".join(
        f"{k_} {v_['ret']:.2f} -> {v_['shift']:+.2f} ({v_['shift_speedup']:+.2f})" for k_, v_ in row.items()))
b2_min = min(v_["shift_speedup"] for row in B2.values() for v_ in row.values())
gain_ratio = [RUN[(f_, f"flagship 1e{l_:g}")]["mean_slow_gain|fp4"][mm_] / RUN[(f_, f"flagship 1e{l_:g}")]["mean_slow_gain|fp4"]["density"]
              for f_, l_ in FLAG_KEYS for mm_ in ("inertia", "anisotropic")]
P(f"    mean slow gain of the inertia members relative to the density member at the same cap: {min(gain_ratio):.2f}-{max(gain_ratio):.2f}")
check("B2 NUMBERS: at FP4's (generous, static) delta = 1 cap the density, inertia and anisotropic-inertia members clear no flagship "
      "host in either physical switch-on reading (slow: orbit-averaged gains; sudden: a random phase), both footings, even with "
      "the inertia members' speed-up inside the region granted (retained time divided by sqrt(1 + G_max))",
      f"smallest shift over 36 cells {b2_min:+.3f} dex (gate 0.10); retained {min(v_['ret'] for r_ in B2.values() for v_ in r_.values()):.2f}"
      f"-{max(v_['ret'] for r_ in B2.values() for v_ in r_.values()):.2f}", b2_min > 0.10,
      f"velocity weighting moves the energy onto the fast particles and raises its total only by the cap's pressure weighting "
      f"({min(gain_ratio):.2f}-{max(gain_ratio):.2f}x the density member's); the reciprocal term then turns the kept halo into "
      "Newton + halo, as in FP4")
OUT["numbers"]["B2"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in B2.items()}
OUT["numbers"]["B2_gain_ratio"] = gain_ratio

# ------------------------------------------------------------------------------------------------ B3 envelopes (reported)
banner("B3  (reported) THE ENVELOPE: every particle handed the orbit maximum of its gain (pericentre timing, unattainable)")
B3 = {}
for f_, l_ in FLAG_KEYS:
    key = (f_, f"flagship 1e{l_:g}"); H = HOSTS[key]; R_ = RUN[key]
    row = {}
    for mem in ("density", "inertia", "anisotropic"):
        for cs in ("fp4", "eul"):
            lab = f"{mem}|envelope|{cs}"
            row[lab] = dict(ret=R_[lab], shift=shift_of(R_[lab], H, f_, 1.0))
        row[f"{mem}|slow|eul"] = dict(ret=R_[f"{mem}|slow|eul"], shift=shift_of(R_[f"{mem}|slow|eul"], H, f_, 1.0))
    B3[key] = row
    P(f"    {f_:9s} {H['name']:15s}: " + "; ".join(f"{k_.replace('|envelope', ' env').replace('|slow', ' slow')} {v_['ret']:.3f}/{v_['shift']:+.3f}"
                                               for k_, v_ in row.items()))
env_pass = sorted({f"{k_[0]}|{k_[1]}|{lab}" for k_, row in B3.items() for lab, v_ in row.items() if abs(v_["shift"]) <= 0.10})
eul_pass = [x_ for x_ in env_pass if x_.endswith("eul")]
env_pass_fp4 = [x_ for x_ in env_pass if x_.endswith("envelope|fp4")]
check("B3 (reported) the envelope reading: which member/host cells pass the flagship when every particle is hit at its orbit's "
      "most favourable phase -- with FP4's cap and with the health-enforced Eulerian cap",
      f"passing cells: {env_pass if env_pass else 'none'}", len(eul_pass) == 0,
      "with FP4's generous cap the (superluminal) inertia envelope clears the heavier hosts; with the cap H4 actually enforces "
      "(delta <= 1 at every time where the dark state sits) no envelope clears any host" if env_pass and not eul_pass else
      "as measured", load_bearing=False)
OUT["numbers"]["B3"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in B3.items()}

# ------------------------------------------------------------------------------------------------ B4 ordering
banner("B4  ORDERING: galaxies vs clusters for every weighted member (slow reading, FP4's cap)")
B4 = {}
for f_ in FEET:
    Rc = RUN[(f_, "X-COP ref")]
    for mem in ("density", "inertia", "anisotropic"):
        fl = [RUN[(f_, f"flagship 1e{l_:g}")][f"{mem}|slow|fp4"] for l_ in (10.0, 10.5, 11.0)]
        B4[f"{f_}|{mem}"] = dict(cluster=Rc[f"{mem}|slow|fp4"], flagship_min=min(fl), flagship_max=max(fl))
        P(f"    {f_:9s} {mem:12s}: X-COP keeps {Rc[f'{mem}|slow|fp4']:.3f} inside R500; the flagship hosts keep {min(fl):.3f}-{max(fl):.3f} inside r_F")
    P(f"    {f_:9s} unbinding cost / MOND field energy: X-COP {EB[(f_, 'X-COP ref')]['ratio_mond']:.2f}, flagship "
      f"{min(EB[(f_, f'flagship 1e{l_:g}')]['ratio_mond'] for l_ in (10.0, 10.5, 11.0)):.2f}-{max(EB[(f_, f'flagship 1e{l_:g}')]['ratio_mond'] for l_ in (10.0, 10.5, 11.0)):.2f}")
anti = all(v_["cluster"] < v_["flagship_min"] for v_ in B4.values()) and \
       all(EB[(f_, "X-COP ref")]["ratio_mond"] < min(EB[(f_, f"flagship 1e{l_:g}")]["ratio_mond"] for l_ in (10.0, 10.5, 11.0)) for f_ in FEET)
check("B4 NUMBERS: every weighted member clears the X-COP reference cluster MORE than any z = 2.5 flagship host (slow reading, both "
      "footings), and the unbinding cost per unit MOND field energy is lower for the cluster: the whole class is anti-selective "
      "(clusters first), the ordering the framework needs is the opposite",
      {k_: {kk: round(vv, 3) for kk, vv in v_.items()} for k_, v_ in B4.items()}, anti,
      "the energy any MOND-sector coupling can hand over scales with the host's MOND field energy per unit dark mass, which is "
      "largest where the halo is diffuse and hot -- the clusters")
OUT["numbers"]["B4"] = B4

# ================================================================================================ B5 the rate member
banner("B5  THE RATE MEMBER g J_perp.grad chi == -g n_d d_t chi: silent in a static halo, pays during the clearing")
# its natural ordering by growth rate (declared, illustrative rates) and its clock-frame dependence
GR = dict(flagship_sSFR_per_Gyr=2.0, cluster_growth_per_Gyr=0.2, zeq0_disc_sSFR_per_Gyr=0.1)    # DECLARED, illustrative
v_host_kms = 300.0                                                                             # a host's speed in the clock frame
b5 = {}
for f_, l_ in FLAG_KEYS:
    H = HOSTS[(f_, f"flagship 1e{l_:g}")]
    t_grow_s = 1.0 / GR["flagship_sSFR_per_Gyr"] * 3.156e16
    b5[f"{f_}|{l_}"] = dict(delta_during_clearing_min=EB[(f_, f"flagship 1e{l_:g}")]["ratio"],
                            advective_over_growth=(v_host_kms * 1e3 / (H["gate"] * 3.0857e19)) * t_grow_s)
delta_star_excess = None
P("    A5: S = 2 g (d_t n_d) u'/a0^2 -- zero before and after a clearing; during it, A4 + B0 force max(delta) >= the B0 ratio")
for k_, v_ in b5.items():
    P(f"    {k_:18s}: delta during the clearing >= {v_['delta_during_clearing_min']:.1f}; a host moving at {v_host_kms:.0f} km/s through the "
      f"clock frame sees an advective n.d chi {v_['advective_over_growth']:.0f}x its growth term at r_F (without tracking)")
P(f"    ordering (declared illustrative growth rates {GR}): the hill per unit I scales with the growth rate -- a z = 2.5 galaxy "
  f"gets {GR['flagship_sSFR_per_Gyr'] / GR['cluster_growth_per_Gyr']:.0f}x a cluster's: the RIGHT order, the class's only member with it")
OUT["numbers"]["B5"] = dict(rows=b5, declared_rates=GR, v_host_kms=v_host_kms)

# ================================================================================================ H health
banner("H1-H4  HEALTH: Minkowski, the weighting theorem, FRW, and the static MOND background")
Aq, Bq, Cq, Mq, thq = sp.symbols("A B C M theta", real=True)
wq = sp.symbols("omega", real=True)
Lq = Aq * wq ** 2 - Bq * kS ** 2 - Cq * kS ** 2 * sp.cos(thq) ** 2 - Mq ** 2        # the quadratic symbol in the clock frame
w2 = sp.simplify((Bq * kS ** 2 + Cq * kS ** 2 * sp.cos(thq) ** 2 + Mq ** 2) / Aq)
speed2 = sp.simplify(sp.limit(w2 / kS ** 2, kS, sp.oo))
H1tab = {"isotropic F": dict(A=1 + FS, B=1 + FS, C=0), "temporal F": dict(A=1 + FS, B=1, C=0), "spatial G": dict(A=1, B=1 + GSy, C=0),
         "anisotropic G": dict(A=1, B=1, C=GSy), "linear current / rate / electrostatic": dict(A=1, B=1, C=0)}
for nm_, d_ in H1tab.items():
    s2_ = sp.simplify(speed2.subs({Aq: d_["A"], Bq: d_["B"], Cq: d_["C"]}))
    d_["speed2"] = s2_
    P(f"    {nm_:38s}: ghost-free iff {d_['A']} > 0; gradient-stable iff {d_['B']} > 0 and {d_['B']} + {d_['C']} > 0; speed^2 = {s2_}")
P("    linear current: m^2 -> m^2 - g^2 A.A (A2): spatial A is tachyonic beyond g|A| = m; electrostatic A = f n gives m^2 + g^2 f^2 (healthy)")
ok_h1 = sp.simplify(speed2 - (Bq + Cq * sp.cos(thq) ** 2) / Aq) == 0
check("H1 DERIVED (Minkowski): the general quadratic member A|d_t Psi|^2 - B|grad Psi|^2 - C|e.grad Psi|^2 - M^2|Psi|^2 is ghost-free "
      "iff A > 0, gradient-stable iff B > 0 and B + C > 0, and propagates at speed^2 (B + C cos^2 theta)/A; the current members are "
      "luminal", {k_: str(v_["speed2"]) for k_, v_ in H1tab.items()}, ok_h1)
Iq = sp.symbols("I", positive=True)
Rq, s2q = sp.Function("R")(Iq), sp.Function("s2")(Iq)
dinv = sp.diff(s2q / Rq, Iq)
res_h2 = sp.simplify(sp.diff(s2q, Iq) - (Rq * dinv + s2q * sp.diff(Rq, Iq) / Rq))
ex_spatial = sp.simplify(sp.diff((1 + GSy) / mS, GSy))                        # s^2/R for the spatial member: kick needs G' > 0
ex_temporal_R = sp.simplify(sp.diff(mS / sp.sqrt(1 + FS), FS))              # temporal: hill needs F' < 0 ...
ex_temporal_s2 = sp.simplify(sp.diff(1 / (1 + FS), FS))                     # ... which raises s^2 = 1/(1+F)
ex_iso = sp.simplify(sp.diff(sp.sqrt(1 + FS) / mS, FS))                     # isotropic: weighting needs F' > 0 = a rest-energy WELL
P(f"    weighting theorem: s2' - [R d(s2/R)/dI + s2 R'/R] = {res_h2}: with R' >= 0 (no well) and d(s2/R)/dI > 0 (faster particles gain "
  f"more), s2' > 0 -- the speed rises above c")
P(f"    spatial G: d(s2/R)/dG = {ex_spatial} > 0 -> kick needs G > 0 -> speed^2 1 + G > 1;  temporal F: dR/dF = {ex_temporal_R} < 0, "
  f"ds2/dF = {ex_temporal_s2} < 0 -> the hill (F < 0) is superluminal;  isotropic F: d(s2/R)/dF = {ex_iso} > 0 needs F' > 0, i.e. a WELL")
check("H2 DERIVED (the weighting theorem): a coupling that hands more energy to faster dark particles without a rest-energy well "
      "needs d(s^2)/dI > 0 -- the dark field propagates outside the metric light cone; the luminal members can weight only "
      "together with a well (c/v)^2 times stronger; so every velocity-weighted kicker is superluminal (ordered only by the "
      "clock's foliation, which the core's instantaneous heat filter already uses)",
      f"identity residual {res_h2}; spatial {ex_spatial}; temporal {ex_temporal_R}, {ex_temporal_s2}; isotropic {ex_iso}",
      res_h2 == 0 and sp.simplify(ex_spatial - 1 / mS) == 0 and sp.simplify(ex_iso * mS * 2 * sp.sqrt(1 + FS) - 1) == 0)
tq = sp.symbols("t", real=True); psi0 = sp.symbols("psi0", positive=True)
Ps_, Pc_ = psi0 * sp.exp(-sp.I * mS * tq), psi0 * sp.exp(sp.I * mS * tq)
p_frw = sp.simplify(sp.diff(Pc_, tq) * sp.diff(Ps_, tq) - mS ** 2 * Pc_ * Ps_)
rho_frw = sp.simplify(sp.diff(Pc_, tq) * sp.diff(Ps_, tq) + mS ** 2 * Pc_ * Ps_)
check("H3 DERIVED (FRW): grad u = 0 on the homogeneous background (FP3 G1b: a0 absent there), so I = 0 and every I-member with "
      "F(0) = G(0) = f(0) = 0 and A(grad u = 0) = 0 is off; the dark field is then free and its homogeneous mode has p = 0 exactly "
      "(dust); K-members are uniform on CMC leaves in bound regions (CV4) and act only as a time-dependent mass",
      f"p = {p_frw}, rho = {rho_frw}", p_frw == 0 and rho_frw == 2 * mS ** 2 * psi0 ** 2)
meas5 = J5["checks"][[k_ for k_ in J5["checks"] if k_.startswith("A3")][0]]["measured"]
detstr = re.search(r"det\(N,U\) = ([^(]*\([^)]*\))", meas5).group(1)
kq, Ce, acS, cCH, dl = sp.symbols("k C_e alpha_c c_CH delta", positive=True)
detNU = sp.sympify(detstr, locals=dict(k=kq, C_e=Ce, alpha_c=acS, c_CH=cCH))
det_d = sp.factor(detNU.subs(Ce, (1 - dl) * Ce))
dstar = sp.solve(sp.Eq(det_d, 0), dl)
excess = sp.simplify(dstar[0] - 1) if dstar else None
ex_num = [float(excess.subs({acS: 3.2e-9, cCH: 2, Ce: c_})) for c_ in (0.3, 1.0, 3.0)] if excess is not None else []
Gcaps = {f"{k_[0]}|{k_[1]}": dict(Gmax_fp4=RUN[k_]["Gmax"], Gmax_eul=RUN[k_]["GmaxE"], speed_fp4=math.sqrt(1 + RUN[k_]["Gmax"]),
                                   speed_aniso_fp4=math.sqrt(1 + 3 * RUN[k_]["Gmax"])) for k_ in RUN if HOSTS[k_]["kind"] == "flagship"}
P(f"    FP5's committed det(N, U) = {detNU}; with C_e -> (1 - delta) C_e: {det_d}; zero at delta = {dstar}")
P(f"    delta* - 1 = {excess} = {', '.join(f'{x_:.1e}' for x_ in ex_num)} at alpha_c = 3.2e-9, c_CH = 2, C_e = 0.3/1/3")
P("    Psi at the ceilings on the flagship hosts: " + "; ".join(f"{k_} G_max {v_['Gmax_fp4']:.2f} -> speed {v_['speed_fp4']:.2f} c "
                                                           f"(anisotropic {v_['speed_aniso_fp4']:.2f} c)" for k_, v_ in Gcaps.items()))
ok_h4 = excess is not None and sp.simplify(excess - acS * cCH / (2 * Ce * (acS + cCH))) == 0 and max(ex_num) < 1e-8
check("H4 DERIVED (static MOND background): FP5's (N, U) determinant with the reciprocal suppression C_e -> (1 - delta) C_e vanishes "
      "at delta* = 1 + alpha_c c_CH/(2 C_e (alpha_c + c_CH)) = 1 + O(1e-9) and is negative beyond: FP4's ceiling delta = 1 is the "
      "core's own health boundary (FP5's positivity), not only the point where the phantom switches off",
      f"det = {det_d}; delta* - 1 = {excess} ({', '.join(f'{x_:.1e}' for x_ in ex_num)})", ok_h4,
      f"so B0's delta >= {min(fl_ratio):.1f} during any MOND-powered clearing is not a phenomenological cost but an ill-posed core; the "
      "density, inertia and rate members pay it in C_e itself (A5), a current member only while the dark state flows")
OUT["numbers"]["H"] = dict(speed2={k_: str(v_["speed2"]) for k_, v_ in H1tab.items()}, det=str(det_d), delta_star=str(dstar),
                           delta_star_excess=ex_num, Psi_at_caps=Gcaps)

# ------------------------------------------------------------------------------------------------ B5 check (needs H4)
b5_min = min(v_["delta_during_clearing_min"] for v_ in b5.values())
check("B5 DERIVED + NUMBERS (the rate member): its back-reaction is 2 g (d_t n_d) u'/a0^2 (A5) -- silent in any static halo, so it "
      "escapes the STATIC reciprocity; but by A4 the energy it hands over passes through that same S, so during the clearing "
      "delta >= the B0 ratio on every flagship host, beyond H4's delta* = 1 + O(1e-9): the core is ill-posed while it clears",
      f"delta during clearing >= {b5_min:.1f} vs delta* - 1 <= {max(ex_num):.1e}", b5_min > 1 + max(ex_num),
      "the one member with the right ordering (its hill tracks each host's growth rate) defers the reciprocity to the epoch of "
      "the clearing instead of removing it.  B0 is the PERMANENT (unbinding) case: holding the dark mass out without unbinding "
      "it lasts only while the host grows, since the hill is g d_t chi.  It is also clock-frame dependent (n.d chi): advective "
      "terms dominate unless the khronon tracks each host to a few per cent")

# ================================================================================================ B6 velocity scales
banner("B6  THE VELOCITY SCALE EACH MEMBER PRODUCES, AND WHERE IT COMES FROM")
b6_fp4 = J4["numbers"]["B6"]
free_hit = b6_fp4["free_hit"]
vs = {}
for f_ in FEET:
    Hs = [HOSTS[(f_, f"flagship 1e{l_:g}")] for l_ in (10.0, 10.5, 11.0)]
    vs[f_] = dict(
        density_ceiling=[math.sqrt(2 * RUN[(f_, h_["name"])]["Vmax"]) for h_ in Hs],
        density_ceiling_eulerian=[math.sqrt(2 * RUN[(f_, h_["name"])]["VmaxE"]) for h_ in Hs],
        xcop_ceiling=math.sqrt(2 * RUN[(f_, "X-COP ref")]["Vmax"]))
    P(f"    {f_:9s}: density-class ceiling (FP4 cap, centre) {', '.join(f'{v_:.0f}' for v_ in vs[f_]['density_ceiling'])} km/s at the flagship "
      f"hosts; Eulerian {', '.join(f'{v_:.0f}' for v_ in vs[f_]['density_ceiling_eulerian'])}; X-COP {vs[f_]['xcop_ceiling']:.0f} km/s (host-proportional)")
P("    inertia members: v^2 ~ G sigma^2 (host-proportional, G fitted); rate member: v^2 = 2 g d_t chi (g fitted, times each host's growth "
  "rate); electrostatic: g f/m (fitted); magnetic: 0; kinetic isotropic: c sqrt|F| with |F| = 2.0 x FK1's eps/m^2 for 575-650 km/s (fitted)")
P(f"    FP4 B6's census of the core's parameter-free velocities (with m): hits in 575-675 km/s: {free_hit if free_hit else 'none'}")
ok_b6 = len(free_hit) == 0 and all(max(vs[f_]["density_ceiling"]) < 575.0 for f_ in FEET)
check("B6 THE WINDOW IS NOT PREDICTED: no member produces a universal 575-675 km/s from (a0, rho_Lambda, m): the ceilings are "
      "host-proportional (below the window at every flagship host), the other members carry their own fitted strength, and FP4's "
      "census has no parameter-free hit", {f_: {k_: ([round(x_) for x_ in v_] if isinstance(v_, list) else round(v_)) for k_, v_ in vs[f_].items()} for f_ in FEET},
      ok_b6, "the ~600 km/s speed remains a constant of the added field (FK1's eps), FITTED")
OUT["numbers"]["B6"] = vs

# ================================================================================================ G gates for the best couplings
banner("G1-G2  THE GATES FOR THE BEST COUPLINGS")
C1 = J4["numbers"]["C1"]; C2 = J4["numbers"]["C2"]; C3 = J4["numbers"]["C3"]; C4 = J4["numbers"]["C4"]; C57 = J4["numbers"]["C5_C7"]
fl_min = min(abs(v_["shift"]) for v_ in C1.values())
G1 = dict(flagship_min_abs_shift=fl_min, xcop={k_: round(v_["ratio"], 3) for k_, v_ in C2.items()},
          galaxies={f_: {k_: round(v_, 3) for k_, v_ in C3["shifts"][f_].items()} for f_ in FEET},
          kids_without_term={f_: round(v_, 1) for f_, v_ in C4["dchi2"].items()},
          shear_with_term={k_: round(v_["recip_1.75"], 3) for k_, v_ in C57["shear"].items()},
          forest_escaped={k_: round(v_, 4) for k_, v_ in C57["forest"].items()},
          harvey_keep={k_: v_ for k_, v_ in C57["harvey_keep"].items()}, harvey_intact=C57["harvey_intact"])
P(f"    G1 the best HEALTHY member -F(I) g^mn dPsi* dPsi (A3: exactly FP4's density class) -- FP4's committed delta = 1 rows:")
P(f"       flagship z = 2.5: smallest |shift| over FP4's 18 cells {fl_min:.3f} dex (gate 0.10) -> FAILS")
P(f"       X-COP (with the reciprocal term) {G1['xcop']} (strict 0.8-1.2: natural passes, upper bound fails)")
P(f"       z = 0 galaxies {G1['galaxies']} (0.06 dex: pass); KiDS without the term {G1['kids_without_term']} (<= +4: pass; with it OPEN)")
P(f"       cosmic shear with the term (1.75 Mpc cap) {G1['shear_with_term']} (<= 1.2: pass); forest/S_8 escaped {G1['forest_escaped']} (pass)")
P(f"       Harvey: kept carrier {G1['harvey_keep']} -> intact-carrier excess beta {G1['harvey_intact']} (natural reading: pass by proxy)")
P("       and with the health-enforced Eulerian cap (H4) the member is weaker still (B3's 'eul' rows): FP4's rows bound it from above")
check("G1 THE BEST HEALTHY COUPLING (-F(I) g^{mn} dPsi* dPsi: luminal, ghost-free for F > -1, exactly FP4's density class by A3) "
      "inherits FP4's committed delta = 1 gate rows: it passes what LCDM passes and FAILS the flagship at z = 2.5 in every reading",
      f"flagship smallest |shift| {fl_min:.3f} dex", fl_min > 0.10,
      "Newton + halo where the halo stays: the framework's distinctive gate is lost exactly as in FP4")
# G2: the best-clearing member (inertia, superluminal): X-COP and the z = 0 galaxies from its own retention
G2 = {}
for f_ in FEET:
    Lm["A0"] = A0K[f_]
    ecl = RUN[(f_, "X-COP ref")]["inertia|slow|fp4"]
    G2[f"{f_}|xcop"] = xcop_recip(ecl, f_, 1.0)
    G2[f"{f_}|xcop"]["eps"] = ecl
    eps_g = {kh: RUN[(f_, kh)]["inertia|slow|fp4"] for kh in GAL}
    G2[f"{f_}|galaxies"] = dict(eps=eps_g, shifts=gal_recip(eps_g, f_, 1.0))
    eps_d = {kh: RUN[(f_, kh)]["density|slow|fp4"] for kh in GAL}
    G2[f"{f_}|galaxies_density"] = dict(eps=eps_d, shifts=gal_recip(eps_d, f_, 1.0))
    P(f"    G2 {f_:9s} inertia member (slow, FP4 cap): X-COP keeps {ecl:.3f} -> median M_dyn/M_HSE {G2[f'{f_}|xcop']['ratio']:.2f} "
      f"(strict {G2[f'{f_}|xcop']['strict']}); z = 0 galaxies keep " + ", ".join(f"{kh} {v_:.2f}" for kh, v_ in eps_g.items())
      + " -> shifts " + ", ".join(f"{kh} {v_:+.3f}" for kh, v_ in G2[f"{f_}|galaxies"]["shifts"].items()) + " dex")
Lm["A0"] = A0K["canonical"]
check("G2 (reported) the best-CLEARING member (the superluminal inertia coupling, slow reading, FP4's cap): X-COP with the "
      "reciprocal term and L321's z = 0 galaxies, from its own retention; the flagship is B2's",
      {k_: (round(v_["ratio"], 3) if "xcop" in k_ else {kk: round(vv, 3) for kk, vv in v_["shifts"].items()}) for k_, v_ in G2.items()},
      all(not G2[f"{f_}|xcop"]["strict"] for f_ in FEET), load_bearing=False)
OUT["numbers"]["G"] = dict(G1=G1, G2=G2)

# ================================================================================================ W the ledger
banner("W  THE LEDGER: what this lane settles (link / status / basis)")
LEDGER = [
    ("L10o.1", "the task's current: J.n = n_d (clock-frame density), J^i = -n_d v^i", "DERIVED", "check A1"),
    ("L10o.2", "gauge reduction: -|dPsi|^2 + gA.J == -|DPsi|^2 + g^2 A.A|Psi|^2; J.d chi is pure gauge at O(g) and FP4's density class at "
     "O(g^2); J.n f is an electrostatic density coupling", "DERIVED", "check A2"),
    ("L10o.3", "kinetic couplings: -F(I) g^mn dPsi*dPsi is the density coupling V = c^2[(1+F)^(-1/2) - 1] (|F| = 2.0 x FK1's eps/m^2 for "
     "575-650 km/s); spatial/anisotropic members change only the inertia", "DERIVED", "check A3"),
    ("L10o.4", "THE ENERGY-RECIPROCITY IDENTITY: the energy any coupling takes from the MOND sector is -Int S.d_t grad u, S its source "
     "in the MOND equation; <= max(delta) x the MOND field energy", "DERIVED", "check A4"),
    ("L10o.5", "exact back-reactions: S = -2 rho_d V' u'/a0^2 (density), 2 g (d_t n_d) u'/a0^2 (rate), -G' rho_d w^2 u'/a0^2 (inertia), "
     "g j (F + 2IF') (current)", "DERIVED", "check A5"),
    ("L10o.6", f"class-wide: unbinding the flagship's dark mass costs {min(fl_ratio_mond):.1f}-{max(fl_ratio_mond):.1f}x the host's whole MOND "
     f"field energy ({min(fl_ratio):.1f}-{max(fl_ratio):.1f}x with the baryons' kinetic energy added): any MOND-powered clearing needs "
     "delta > 1 where the dark state sits (beyond H4's health boundary)", "FAILS", "check B0"),
    ("L10o.7", "linear spatial-current (magnetic) couplings: no work in a static host; the re-direction floor fails the flagship",
     "FAILS", "check B1"),
    ("L10o.8", "velocity-weighted couplings at FP4's delta = 1 cap (density, inertia, anisotropic inertia): fail the flagship in the "
     "slow and sudden readings, both footings", "FAILS", f"check B2 (B3: an unattainable pericentre-timed envelope with FP4's cap "
     f"clears {len(env_pass_fp4)} of 18 member-host cells ({sorted({x_.split('|')[2] for x_ in env_pass_fp4})}); with the health-enforced cap: "
     f"{len(eul_pass)})"),
    ("L10o.9", "ordering: every MOND-sector coupling clears clusters before z = 2.5 galaxies (anti-selective)", "FAILS", "check B4"),
    ("L10o.10", "the rate member g J_perp.grad chi == -g n_d d_t chi: silent in static halos (escapes the static reciprocity), right "
     "ordering by growth rate, but delta >= B0's ratio during the clearing (ill-posed core); clock-frame dependent",
     "FAILS", "checks A5, B5, H4"),
    ("L10o.11", "velocity scale: host-proportional ceilings or a fitted strength per member; the 575-675 km/s window not predicted",
     "FITTED", "check B6"),
    ("L10o.12", "health: current members luminal (tachyonic beyond g|A| = m); every velocity-weighted kicker is superluminal (the "
     "weighting theorem); all I-members off on FRW", "DERIVED", "checks H1-H3"),
    ("L10o.13", "FP4's ceiling delta = 1 is the core's own health boundary: FP5's (N, U) determinant vanishes at delta* = 1 + O(1e-9)",
     "DERIVED", "check H4"),
    ("L10o.14", "the best healthy coupling (-F(I) g^mn dPsi*dPsi) = FP4's density class: passes what LCDM passes, fails the flagship",
     "FAILS", "check G1 (FP4's committed rows)"),
    ("L10o.15", "the honest minimal price of a working kick: FK1's eps (FITTED, eps/m^2 = 1.84-2.35e-6 for 575-650 km/s: energy from "
     "the dark field's own splitting, S = 0) + its trigger's constants (the conversion coupling and gate exponent q, DECLARED) + "
     "the initial misalignment (initial data) + m", "FITTED", "FK1 (committed); this lane's no-go for every MOND-sector source"),
    ("L10o.16", "not scored here: zero-net redistributors in a GROWING host (betatron-like magnetic members, sign-changing weights) "
     "beyond B1's static floor; velocity couplings nonlinear in Psi (outside the low-order class; ill-defined for a multistreaming "
     "wave field); the superluminal members' KiDS / cosmic-shear / forest / Harvey rows (moot: their flagship and X-COP fail); the "
     "rate member's residual clock-frame dipole under khronon tracking", "OPEN", "not computed"),
]
for k_, what, st, basis in LEDGER:
    P(f"    {k_:8s} {st:10s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane's links", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  NO-GO FOR THE CLASS (FP4's last open door, L10o).  No coupling of the dark field's density, current or derivatives to
  the core's MOND sector can hand the dark state the kick's energy without writing on the phantom.  The reason is one
  identity (A4): whatever the coupling, the net energy it takes from the MOND sector is -Int S.d_t grad u, where S is the
  very term it adds to the MOND sector's own equation.  Couplings differ only in WHEN they pay: density and inertia members while the dark state sits
  there (FP4's reciprocity), current members while it flows, the rate member (g J_perp.grad chi == -g n_d d_t chi) only
  during the clearing itself (A5: its S is proportional to d_t n_d).  A gradient current is pure gauge (A2); J.n f is an
  electrostatic density coupling; -F(I)(dPsi)^2 is a rest-mass hill, FP4's class with |F| = 2 x FK1's eps/m^2 (A3); a magnetic
  current does no work in a static host and only redistributes in a growing one (B1).  How much any of them must pay is
  fixed by energy (B0): unbinding the z = 2.5 flagship's dark mass inside r_F costs {min(fl_ratio_mond):.1f}-{max(fl_ratio_mond):.1f}x the whole
  host's MOND field energy ({min(fl_ratio):.1f}-{max(fl_ratio):.1f}x even with all the baryons' kinetic energy added), so the clearing
  needs delta > 1 -- and delta = 1 + O(1e-9) is where FP5's (N, U) determinant changes sign (H4): the core itself goes
  ill-posed.  At FP4's generous delta = 1 cap the velocity-weighted members fail the flagship in both physical readings
  (B2, smallest shift {b2_min:+.2f} dex).  Only an unattainable pericentre-timed envelope with that cap clears any cell:
  {'; '.join(x_.split('|')[0] + ' ' + x_.split('|')[1] + ' (' + x_.split('|')[2] + ')' for x_ in env_pass_fp4) if env_pass_fp4 else 'none'};
  every velocity-weighted quadratic kicker is superluminal (H2), and with the health-enforced cap no envelope clears any
  host.  Every member clears clusters first (B4): the ordering is backwards.  The rate member alone has the right ordering
  (its hill follows each host's growth rate) -- and it pays delta >= {b5_min:.1f} during the clearing.  The best healthy coupling is
  FP4's density class and inherits its gates: it passes what LCDM passes and fails the flagship (G1).  The ~600 km/s window
  is not predicted by any member (B6).
  THE HONEST MINIMAL PRICE: the kick's energy cannot come from the MOND sector; it must come from the dark field itself.
  FK1's U(1)-breaking splitting eps Re Psi^2 (eps/m^2 = 1.84-2.35e-6 for 575-650 km/s, FITTED) has S = 0 by construction,
  plus its trigger's constants (the conversion coupling with its K-gate exponent q, DECLARED), the initial misalignment near
  the heavy axis (initial data), and the dark mass m (required anyway).  Not 'closed' as a theory: FK1's own gates are its
  lanes', not re-derived here.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["runtime_s"] = len(CH), n_fail, time.time() - T0


def _jd(o):
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_,)): return bool(o)
    return str(o)


outname = f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")
OUTDIR = os.environ.get("FP8_FAST_DIR", "") if FAST else HERE              # a smoke run never writes into the lane directory
if OUTDIR:
    json.dump(OUT, open(os.path.join(OUTDIR, outname), "w"), indent=1, default=_jd)
P(f"\n  {len(CH) - sum(1 for _, ok, _ in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   {elapsed()}")
sys.exit(0 if n_fail == 0 else 1)
