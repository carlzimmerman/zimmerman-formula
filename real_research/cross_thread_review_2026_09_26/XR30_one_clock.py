#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR30 -- ONE CLOCK OR TWO?  The derivation chain carries two global time structures: the khronon's constant-mean-curvature
(CMC) foliation (FP14: c_2 -> oo turns the leaf-averaged term into the multiplier term -2 mu (K - <K>_h), so every leaf has
K = <K>_h) and the Henneaux-Teitelboim (HT) unimodular clock (XR20 T1: Lambda -> Lambda(x) plus 2 Lambda d_m T^m, with
alpha = alpha(Lambda), so d Lambda = 0 is a field equation, Lambda is conjugate to the four-volume time T, and
a0 = kappa c sqrt(G rho_Lambda) holds on every solution).  Can the two be merged into one term?  If they can, what changes
(field content, the Dirac count, PPN, FRW, the York/CMC G_eff = 2G kill, the a0 tie)?  If they cannot, why not, and what is
the minimal honest content?

kappa = 1/2 is FITTED (equivalently Z = 5.7888) and is never derived here.  Both a0 footings are carried wherever a0
enters: canonical 9.3603e-11 and alt 1.1312e-10 m/s^2.  No new constant is adopted: every candidate below that needs one
is reported as needing it and is not adopted.

THE ACTION VARIED HERE (per 1/16 pi G, c = 1; FP14's zero-knob root at lambda = 0 plus XR20's T1 term):
  I = Int sqrt(-g) { R - 2 Lambda(x) + alpha_c a^2 - 2 mu (K - <K>_h) + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi
                     - 2 alpha(Lambda)^2 J_P2(h^mn D_m phi D_n phi / alpha(Lambda)^2) + heat pair } + 2 Int Lambda d_m T^m + S_m[g],
  alpha(Lambda) = kappa sqrt(Lambda/8 pi),  K = nabla.n on the khronon's leaves,  <K>_h = Int sqrt(h) K / Int sqrt(h).

LITERATURE (read before the hypotheses were written; cited in XR30_README.md): Henneaux-Teitelboim 1989 and Unruh 1989
(Lambda conjugate to the four-volume time); Kuchar 1991 (the four-volume time labels only equivalence classes of
hypersurfaces enclosing zero four-volume -- it needs a separate hypertime); York 1972 (mean curvature conjugate to the
3-volume); Gomes-Gryb-Koslowski 2011 and Barbour-Koslowski-Mercati 2014 (shape dynamics: a volume-preserving CMC constraint
plus ONE global Hamiltonian constraint; a cosmological constant is an extra input there); Gryb-Thebault 2012 ('unimodular
shape dynamics': the unimodular pair ADDED to shape dynamics' single global Hamiltonian constraint); Afshordi 2009,
Bhattacharyya et al. 2018, Gomes-Guariento 2017 (the cuscuton: CMC leaves with K tied to the scalar; with a linear
potential the scalar is a multiplier pinning K to a constant K_0; the homogeneous cuscuton on a CMC foliation carries one
global degree of freedom and acts as a time-dependent cosmological constant).

PRE-DECLARED (written into this docstring before any code of this lane was run; the expectations come from the reading
above and pencil-and-paper algebra, not from any script output):
  H1  SAME FOLIATION?  The HT term is invariant under T^m -> T^m + d_n omega^{mn} (omega antisymmetric), so only the charge
      T[Sigma] is physical and HT carries no foliation of its own (Kuchar's equivalence classes).  On the khronon's leaves
      T(tau) is monotone (dT/dtau = Int N sqrt(h)(1 - eps F) > 0), so "the HT time's foliation is the khronon's" holds only as
      a gauge choice (T - tau fixes the khronon's global reparametrization).  EXPECT TRUE: a relabeling, not a merger.
  H2  ONE TERM, Lambda == f(K).  2 f(K)(d_m T^m - sqrt(-g)) alone gives K spatially constant AND d f(K) = 0, but T^0's
      equation then freezes York time: on FRW with dust K = K_0 at all times, H(z) = const, against E(z) = 1.322, 1.791,
      3.769, 8.294 at z = 0.5, 1, 2.5, 5.  At k != 0 about Minkowski it is FP14's CMC multiplier in other variables.
      EXPECT TRUE (this merger FAILS on FRW).
  H3  OTHER ONE-TERM MERGERS.  (a) mu == beta sqrt(Lambda) (beta new): HT forces delta Lambda = 0, so delta mu = 0; the
      constant-mu term is a total derivative (sqrt(-g) K = d_m(sqrt(-g) n^m)); the linear theory is FP14's block at c_2 = 0,
      whose scalar is frozen (omega^2 prop. to c_2 = 0; FP5 B4).  (b) T^m == l sqrt(-g) n^m (l new; the linear-potential
      cuscuton's form): Lambda's equation pins K = 1/l and Lambda(t) is no longer constant.  EXPECT both FAIL.
  H4  THE GLOBAL PART.  The mu-term is invariant under mu N -> mu N + c(t) and Int sqrt(h)(K - <K>_h) = 0 identically: the
      CMC condition has NO global part and the multiplier's zero mode is pure gauge.  HT's physical content is purely global
      (Lambda_0 conserved, T its clock).  A conserved momentum cannot be a function of the York clock: on dust FRW
      dK/dt = -12 pi G rho_m N != 0.  The only conserved combination of the CMC leaf data is the Friedmann (global
      Hamiltonian) combination K^2/3 - 8 pi G rho_m = Lambda, i.e. Lambda itself.  EXPECT TRUE.
  H5  ONE GLOBAL CONSTRAINT.  A single global multiplier c(t) can impose K = <K>_h only through the positive square
      Int N sqrt(h)(K - <K>_h)^2 = 0 (FP14's c_2 made a global multiplier).  That constraint is irregular: its fluctuation
      drops out of the quadratic action, which becomes FP14's finite-c_2 block with c_2 = c-bar undetermined, and the
      forceless condition delta K = 0 then removes the scalar (it carries delta K != 0) and admits no time-dependent source.
      EXPECT: not FP14's regular CMC limit -> FAILS.  (A single global pair CAN give d Lambda = 0: the global HT form
      2 Lambda_0 (T-dot - Int N sqrt(h)) on the khronon's leaves; expected equivalent to the local HT.)
  H6  THE COMBINED (UNMERGED) COUNT.  FP14 core + HT: at k != 0 det(combined) = const x det(FP14 multiplier block) (the HT
      sector sets delta Lambda = 0), so FP14's local count holds (3 modes at lambda = 0); globally HT adds one pair
      (Lambda_0, T).  On a periodic-lattice model of the trace sector: physical phase-space dimension 2 N_L with HT, 2 N_L - 2
      without; HT's spatial constraints first class, the CMC constraints second class, the mu and phi zero modes and the
      global reparametrization first class; no tertiary constraints.  The merged Lambda == f(K) model has the same count but
      frozen K.  EXPECT TRUE.
  H7  PPN / FRW / THE YORK-CMC KILL WITH HT ADDED.  The combined FRW perturbations are FP14 C1b's (G_eff/G = 2/(2 - alpha_c),
      no slip, delta Lambda = 0 at k != 0); the static and equal-time responses equal FP14's, and the Newtonian-limit
      coupling is G/(1 - alpha_c/2), not 2G: the kill stays evaded.  EXPECT TRUE.
  H8  THE a0 TIE.  a0 = (kappa/sqrt(24 pi)) c^2 K_inf with K_inf = sqrt(3 Lambda) IS the canonical footing, and the same
      coefficient on today's York time K_0 = 3 H_0/c gives the alt footing's number.  Tying a0 to K_inf is, on shell, the
      HT tie (K_inf^2/3 = Lambda_obs, the global constraint's value); a constant matter vacuum energy shifts HT's Lambda by a
      total derivative, so reading Lambda_obs (= K_inf^2/3) is a choice of variable, not new physics.  Tying a0 to the
      local York time (the CMC leaf value, exactly leaf-uniform by mu's equation) gives a0 proportional to H(z): the rival.
      EXPECT TRUE.
  VERDICT EXPECTED: NO MERGE.  Minimal honest content: two structures -- the khronon's CMC foliation (a local constraint
      family whose global part is pure gauge) and one global HT pair (Lambda_0, T) living on that foliation (the pairing the
      literature calls unimodular shape dynamics).  a0 stays tied through Lambda_0 (= K_inf^2/3 on shell), not York time.
MUTATE=1: the headline tie reads the CMC leaf's York time K(z) = 3 H(z)/c instead of the conserved HT quantity:
HEADLINE-FLAT must FAIL (rc = 1).  Every other check is unchanged by the mutation.
"""
# (the docstring above is the pre-declaration.  The CHECKS text below was written after it and after the scratch development
#  probes disclosed in XR30_README.md, and before the first run of this file.)
DOC_CHECKS = r"""
CHECKS
  C1 CONTROL XR20 T1, reproduced from XR20's own source (read-only slices): the inputs (a0, rho_Lambda, Lambda, kappa, eps), the
     unimodular-clock table (12 numbers), the vacuum table (4 numbers) and the five T1a-T1e measured strings, all EXACTLY equal
     to XR20's committed JSON.
  C2 CONTROL FP14's Dirac count and York/CMC check, reproduced from FP14's own source (read-only slices): K1, L2, C1 and C2
     measured strings EXACTLY equal to FP14's committed JSON (K1's timing field aside); the det line and the Dirac bookkeeping
     line (22 - 2x6 - 4 = 6 -> 3 modes) found verbatim in FP14's committed .out; FP5 A3's count formula gives N_phys = 3.
  C3 CONTROL FP14 C1b (FRW, the multiplier) re-run through FP2's machinery: FP14's committed C1b numbers EXACTLY.
  M1 MINISUPERSPACE, the combined action on FRW: the CMC term vanishes identically on a homogeneous leaf (and on any leaf,
     Sum_j v_j (K_j - <K>) = 0 and mu N -> mu N + c(t) is an exact symmetry); HT gives Lambda-dot = 0 and T-dot = N a^3;
     Friedmann is GR + Lambda_0; sqrt(-g) R = -6 a adot^2/N + a total derivative (sympy, from the metric).
  M2 YORK TIME IS A CLOCK, Lambda IS CONSERVED: on dust FRW dK/dt = -12 pi G rho_m (N = 1), Q = K^2/3 - 8 pi G rho_m = Lambda_0
     on shell, K -> K_inf = sqrt(3 Lambda_0).
  M3 MERGER MB (one term 2 f(K)(T-dot - N a^3), f a generic cubic): T's equation forces dK/dt = 0; with K = K_0 the lapse
     equation is solved by the clock rate for ANY dust and the scale-factor equation is then identically satisfied: H(z) = const,
     E(z) = 1 against the LCDM E(z) -> this merger FAILS FRW.
  M4 MERGER MA (T^m = l sqrt(-g) n^m, the linear-cuscuton form): K = 1/l (a new constant) and Lambda(t) = 1/(3 l^2) - 8 pi G rho_m
     (not constant; with l set by today it reaches zero at z = Omega_m^(-1/3) - 1) -> FAILS.
  M5 HT HAS NO FOLIATION (H1): d_m d_n omega^{mn} = 0 in 3+1 (the 3-form gauge); 1+1 Stokes: T[S2] - T[S1] = the four-volume
     between them, and a visibly different hypersurface enclosing zero four-volume has the same T (Kuchar's equivalence
     classes); on the khronon's FRW leaves dT/dtau = N a^3 > 0 (a monotone relabeling).
  F1 FRW + PERTURBATIONS (FP2's machinery + FP14's multiplier + HT): T^x's equation forces delta Lambda_k = 0 (k != 0); the
     delta Lambda equation is the clock; with delta Lambda = 0 all eight remaining equations EQUAL FP14 C1b's; G_eff/G =
     2/(2 - alpha_c), no slip.
  L0 CONTROL: this lane's extended Minkowski block (FP14's unitary-gauge construction, copied) reproduces FP14's committed
     multiplier det string exactly.
  L1 COMBINED BLOCK (multiplier + HT with generic delta Lambda couplings): det = -4 x det(FP14 multiplier block); D's row forces
     delta Lambda = 0; with delta Lambda = 0 the five FP14 equations are unchanged (so every response FP14 C2 scored is
     unchanged); the static Newtonian-limit lapse response is 2/(2 - alpha_c) of GR's, not 2 (the York/CMC 2G).
  L2 MB LOCALLY: det(MB) = f_1^2 det(FP14 multiplier block): at k != 0 the merged term IS FP14's multiplier in other variables.
  L3 MC (mu = mubar + b_1 delta Lambda): the constant-mubar term adds nothing to the field equations (a total derivative);
     det(MC) = -4 det(FP14 c_2 block at c_2 = 0) = ... omega^2 (...): at lambda = 0 the khronon scalar is frozen (omega = 0) -> FAILS.
  L4 SQ (one global multiplier, positive square): its fluctuation is absent at quadratic order; the quadratic action is FP14's
     c_2 block at c_2 = cbar (undetermined); the scalar mode and a time-dependent forced response both carry delta K != 0, which
     the forceless constraint forbids -> irregular, FAILS.
  D1 LATTICE (the trace sector of the actual action on a periodic leaf, N_L = 3, 4; MOND-free): physical phase-space dimension
     2 N_L (combined), 2 N_L - 2 (core without HT), 2 N_L (no CMC term: mu adds nothing), 2 N_L (global HT pair), 2 N_L (MB);
     constraint surface and consistency residuals < 1e-10; singular-value gaps > 1e10.
  D1m the same with the MOND scalar phi (lambda = 0, alpha(Lambda) read from the HT momentum): combined 2 N_L, core 2 N_L - 2.
  D2 CLASSES: HT's spatial constraints and pi_X first class (their bracket rows vanish); the CMC constraints second class (their
     bracket block with pi_mu has rank N_L - 1); the mu zero-mode generator Sum_j pi_mu_j/N_j, the lapse scaling Sum_j N_j pi_N_j
     and the global Hamiltonian G = Sum_j N_j dH/dN_j first class.
  D3 GLOBAL STRUCTURE: {T_tot, G} != 0 (T - tau is an admissible gauge for the khronon's global reparametrization); p_T is
     conserved exactly while dKbar/dt != 0 (York time ticks); in MB dK_j/dt = 0 (frozen).
  A1 THE FOOTING IDENTITY: a0_can = (kappa/sqrt(24 pi)) c^2 K_inf, K_inf = sqrt(3 Lambda); a0_alt = the same coefficient x c^2 K_0,
     K_0 = 3 H_0/c -- both to 1e-12 against FP0's committed values.
  A2 K_inf AND THE VACUUM: a constant matter vacuum energy is absorbed into HT's Lambda by a field redefinition that changes the
     action by a total derivative (identical field equations), so alpha(Lambda) vs alpha(Lambda_obs) is a choice; K_inf^2 =
     3 Lambda_obs; the Gryb-Thebault large-volume global constraint 2 Lambda - (3/8) P^2 = 0 is K^2 = 3 Lambda.
  A3 THE LOCAL YORK TIME IS EXACTLY LEAF-UNIFORM on the CMC root: mu's equation is N sqrt(h)(K - <K>) = 0 whatever else the
     action contains (a K-dependent MOND coupling included).
  HEADLINE-FLAT the tie read from the conserved combination of the leaf data, Q = K^2/3 - 8 pi G rho_m (= Lambda_0 = K_inf^2/3
     on shell): a0(z)/a0(0) = 1 at z = 0.5, 1, 2.5, 5, 1100 on both footings, uniform on the leaf.  MUTATE=1 reads K(z) alone.
  W  the ledger.
"""
import os, re, sys, io, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
from itertools import combinations_with_replacement
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.integrate import quad, dblquad
from scipy.optimize import brentq, fsolve

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR30_one_clock"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()


class _Tee:
    """the script writes its own .out: everything printed goes to the terminal and to the file."""

    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()

    def close(self):
        self._f.close()


TEE = _Tee(TXT)
sys.stdout = TEE
OUT = {"lane": "XR30", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 114 + "\n" + t + "\n" + "=" * 114)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def src_slice(path, start, end):
    s_ = open(path, encoding="utf-8").read()
    i = s_.index(start)
    return s_[i:s_.index(end, i)]


def el_exprs(L, funcs, vars_):
    """Euler-Lagrange expressions for EVERY field, zeros kept (sympy's euler_equations drops identically trivial ones)."""
    ders = L.atoms(sp.Derivative)
    order = max(len(d.variables) for d in ders) if ders else 0
    out = []
    for f in funcs:
        eq = sp.diff(L, f)
        for i in range(1, order + 1):
            for p_ in combinations_with_replacement(vars_, i):
                eq = eq + sp.S.NegativeOne ** i * sp.diff(sp.diff(L, sp.diff(f, *p_)), *p_)
        out.append(eq)
    return out


P(__doc__.strip())
P(DOC_CHECKS.strip())
if MUTATE:
    P("\n  *** MUTATE=1: the headline tie reads the CMC leaf's York time K(z) = 3 H(z)/c instead of the conserved quantity; "
      "HEADLINE-FLAT must FAIL ***")

# ================================================================================================ inputs
c_SI, G_SI = 299792458.0, 6.67430e-11
MPC = 3.0856775814913673e22
H0_KMS, OM_L, OM_M = 67.4, 0.6847, 0.3153                                  # FP0's canonical pair
fp0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))
A0 = {"canonical": fp0["numbers"]["a0_canonical"], "alt": fp0["numbers"]["a0_rho_total"]}
H0 = H0_KMS * 1e3 / MPC
rho_c = 3 * H0 ** 2 / (8 * math.pi * G_SI)
rho_L = OM_L * rho_c
LAM_SI = 8 * math.pi * G_SI * rho_L / c_SI ** 2
KAPPA = 0.5                                                                  # FITTED (Z = 5.7888), never derived here
E_of = lambda z: math.sqrt(OM_M * (1 + z) ** 3 + OM_L)
ZS = [0.5, 1.0, 2.5, 5.0, 1100.0]
P(f"\n  inputs (FP0): a0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2; Lambda = {LAM_SI:.4e} 1/m^2; "
  f"kappa = 1/2 (fitted)")

# ================================================================================================ C controls
banner("C   CONTROLS: XR20 T1, FP14's Dirac count and York/CMC check, FP14's FRW limit -- reproduced from their own sources")
tC = time.time()
# C1 XR20 T1
XR20 = os.path.join(HERE, "XR20_a0_lambda_tie.py")
rec20 = {}


def _check20(name, measured, ok, reading="", load_bearing=True):
    rec20[name.split()[0]] = dict(measured=str(measured), ok=bool(ok))
    return ok


ns20 = dict(os=os, re=re, json=json, math=math, np=np, sp=sp, euler_equations=euler_equations, CHAIN=CHAIN,
            P=lambda *a: None, banner=lambda t: None, check=_check20, OUT={"numbers": {}}, MUTATE=False)
exec(compile(src_slice(XR20, "def num_zero(", "P(__doc__.strip())"), XR20, "exec"), ns20)
exec(compile(src_slice(XR20, "# ================================================================================================ inputs",
                       "# (2) the C-H core's nu_mono"), XR20, "exec"), ns20)
ns20["s_"] = sp.symbols("s", positive=True)
exec(compile(src_slice(XR20, "# ================================================================================================ T1 unimodular (HT)",
                       "# ================================================================================================ T2 four-form (BT)"),
             XR20, "exec"), ns20)
com20 = json.load(open(os.path.join(HERE, "XR20_a0_lambda_tie_results.json")))
cm20 = {k.split()[0]: v for k, v in com20["checks"].items()}
n20 = ns20["OUT"]["numbers"]
c1_inputs = n20["inputs"] == com20["numbers"]["inputs"]
c1_clock = {f: {str(k): v for k, v in c_.items()} for f, c_ in n20["T1_clock"].items()} == com20["numbers"]["T1_clock"]
c1_vac = {str(k): v for k, v in n20["T1_vacuum"].items()} == com20["numbers"]["T1_vacuum"]
c1_str = {k: rec20[k]["measured"] == cm20[k]["measured"] and rec20[k]["ok"] == cm20[k]["ok"] for k in ("T1a", "T1b", "T1c", "T1d", "T1e")}
EPS = ns20["EPS"]
P("    XR20 T1 clock (kappa^2/8pi) F at y = 1e-3 ... 100 (canonical): " + ", ".join(f"{v:.2e}" for v in n20["T1_clock"]["canonical"].values()))
check("C1 CONTROL XR20 T1 reproduced EXACTLY from XR20's own source (read-only slices): inputs, the unimodular-clock table, the "
      "vacuum table, and the T1a-T1e measured strings (incl. T1c's lattice count: rank 4, 2 phase-space dimensions)",
      f"inputs {c1_inputs}; clock {c1_clock}; vacuum {c1_vac}; strings {c1_str}",
      c1_inputs and c1_clock and c1_vac and all(c1_str.values()))
OUT["numbers"]["C1"] = dict(clock=n20["T1_clock"], eps=EPS)

# C2 FP14 C1 (Dirac count) and C2 (York/CMC), plus K1 and L2
FP14 = os.path.join(CHAIN, "FP14_zero_knob_core.py")
rec14, outs14 = {}, []


def _check14(name, measured, ok, load_bearing=True, reading=None):
    rec14[name.split()[0]] = dict(measured=str(measured), ok=bool(ok))
    return ok


fp7 = json.load(open(os.path.join(CHAIN, "FP7_aqual_type_repair_results.json")))
n14 = dict(os=os, re=re, json=json, math=math, np=np, sp=sp, euler_equations=euler_equations, time=time, fp7=fp7,
           P=lambda *a: outs14.append(" ".join(str(x_) for x_ in a)), banner=lambda t: None, check=_check14, OUT={"numbers": {}},
           MUTATE=False, TERM="leaf", HERE=CHAIN, el=lambda: "", load_json=lambda nm_: json.load(open(os.path.join(CHAIN, nm_))))


def run14(start, end):
    exec(compile(src_slice(FP14, start, end), FP14, "exec"), n14)


run14("# ============================================================================================================ the Minkowski block",
      "# ============================================================================================================ K controls")
run14("tK = time.time()", "# K2: FP9's machinery")
run14("# L2: health and mode count at lambda = 0", "# L3: exact zero field")
run14("# L4: every FP7/FP9 gate at lambda = 0", "alpha2_M = sympify_fp(")
run14("# C1 Minkowski: the multiplier block", "# C1b FRW")
run14("# C2 York/CMC", "# C3: tracking")
com14 = json.load(open(os.path.join(CHAIN, "FP14_zero_knob_core_results.json")))
cm14 = {k.split()[0]: v for k, v in com14["checks"].items()}
strip_t = lambda s_: re.sub(r"; \(\d+\.\d s\)$", "", s_)
c2_eq = {k: strip_t(rec14[k]["measured"]) == strip_t(cm14[k]["measured"]) and rec14[k]["ok"] and cm14[k]["ok"] for k in ("K1", "L2", "C1", "C2")}
out14 = open(os.path.join(CHAIN, "FP14_zero_knob_core.out"), encoding="utf-8").read()
det_line = [l_ for l_ in outs14 if l_.strip().startswith("det (c_2 -> oo form)")]
dirac_line = [l_ for l_ in outs14 if "UV khronon speed^2" in l_]
c2_lines = bool(det_line) and det_line[0].strip() in out14 and bool(dirac_line) and dirac_line[0].strip() in out14
fp5 = json.load(open(os.path.join(CHAIN, "FP5_dof_and_a0_field_results.json")))
nh = sp.Symbol('n', positive=True, integer=True)
Nphys5 = sp.simplify((12 + 2 + 6 + 2 + 2 * (nh + 1) + 2 * nh + 2 - 2 * 6 - (2 + 2 + 2 * (nh + 1) + 2 * nh + 2)) / 2)
fp5_A3 = [v for k, v in fp5["checks"].items() if k.startswith("A3")][0]["measured"]
count14 = (22 - 2 * 6 - 4) // 2
P(f"    FP14 C1 measured: {rec14['C1']['measured']}")
P(f"    FP14 C2 measured: {rec14['C2']['measured'][:160]} ...")
P(f"    FP14's bookkeeping: metric + lapse/shift + multiplier 22 - 2 x 6 (first class) - 4 (second class) = 6 -> {count14} modes; "
  f"FP5 A3's formula: N_phys = {Nphys5} for every heat-point number n")
check("C2 CONTROL FP14's Dirac count and York/CMC check reproduced EXACTLY from FP14's own source (read-only slices): K1, L2, C1 and "
      "C2 measured strings equal the committed JSON (K1's timing aside), the det line and the Dirac bookkeeping line are verbatim "
      "in FP14's committed .out, and FP5 A3's count formula gives N_phys = 3",
      f"strings {c2_eq}; .out lines {c2_lines}; FP14 count {count14}; FP5 N_phys {Nphys5} (committed: 'N_phys = 3' in A3: "
      f"{'N_phys = 3' in fp5_A3})", all(c2_eq.values()) and c2_lines and count14 == 3 and Nphys5 == 3 and "N_phys = 3" in fp5_A3)

# C3 FP14 C1b through FP2's machinery
run14("# K3: FP2's FRW machinery", "# K4: FP1's direct QUMOND")
run14("# C1b FRW", "# C2 York/CMC")
c3_ok = n14["OUT"]["numbers"]["C1b"] == com14["numbers"]["C1b"]
check("C3 CONTROL FP14 C1b (the multiplier on FRW) re-run through FP2's committed machinery: FP14's committed C1b numbers EXACTLY",
      f"dict equal {c3_ok}: G_eff {n14['OUT']['numbers']['C1b']['Geff']}, slip {n14['OUT']['numbers']['C1b']['slip']}, "
      f"mu eq/Q {n14['OUT']['numbers']['C1b']['mu_eq_over_Q']}", c3_ok)
P(f"    ({time.time() - tC:.1f} s)")

# ================================================================================================ M minisuperspace
banner("M   MINISUPERSPACE: the combined action on FRW, York time vs Lambda, and the one-term mergers")
t_ = sp.Symbol('t', real=True)
a_, N_, T_, Lam_ = [sp.Function(n_)(t_) for n_ in ('a', 'N', 'T', 'Lambda')]
Gs, ms, K0s, ells, Lam0s = sp.symbols('G m K_0 ell Lambda_0', positive=True)
ad = sp.diff(a_, t_)
Kfrw = 3 * ad / (a_ * N_)
sqg_ = N_ * a_ ** 3
L_R = -6 * a_ * ad ** 2 / N_
L_dust = -16 * sp.pi * Gs * ms * N_
# sqrt(-g) R from the metric
tt, xx, yy, zz = sp.symbols('tt xx yy zz')
aa_, NN_ = sp.Function('a')(tt), sp.Function('N')(tt)
g4 = sp.diag(-NN_ ** 2, aa_ ** 2, aa_ ** 2, aa_ ** 2); gi4 = g4.inv(); X4 = [tt, xx, yy, zz]
Gam = [[[sum(gi4[l, s] * (sp.diff(g4[s, m], X4[n]) + sp.diff(g4[s, n], X4[m]) - sp.diff(g4[m, n], X4[s])) for s in range(4)) / 2
         for n in range(4)] for m in range(4)] for l in range(4)]
Ric = lambda m, n: sum(sp.diff(Gam[l][m][n], X4[l]) - sp.diff(Gam[l][m][l], X4[n]) + sum(Gam[l][l][s] * Gam[s][m][n] - Gam[l][n][s] * Gam[s][m][l]
                                                                                        for s in range(4)) for l in range(4))
R4 = sp.simplify(sum(gi4[m, n] * Ric(m, n) for m in range(4) for n in range(4)))
m1_R = sp.simplify(NN_ * aa_ ** 3 * R4 - (-6 * aa_ * sp.diff(aa_, tt) ** 2 / NN_ + sp.diff(6 * aa_ ** 2 * sp.diff(aa_, tt) / NN_, tt))) == 0
L_comb = L_R - 2 * Lam_ * sqg_ + 2 * Lam_ * sp.diff(T_, t_) + L_dust        # the CMC term is identically zero on a homogeneous leaf
ELc = dict(zip(("a", "N", "T", "Lambda"), [sp.simplify(e_) for e_ in el_exprs(L_comb, [a_, N_, T_, Lam_], [t_])]))
fr_c = sp.solve(ELc["N"].subs(N_, 1), ad ** 2)[0]
NLs = 5
vS = sp.symbols(f'v0:{NLs}', positive=True); KS = sp.symbols(f'K0:{NLs}'); NS = sp.symbols(f'N0:{NLs}', positive=True)
muS = sp.symbols(f'mu0:{NLs}'); cS = sp.Symbol('c')
KbarS = sum(vS[i] * KS[i] for i in range(NLs)) / sum(vS)
leafsum = sp.simplify(sum(vS[i] * (KS[i] - KbarS) for i in range(NLs)))
cmc_term = lambda mm: sum(-2 * mm[i] * NS[i] * vS[i] * (KS[i] - KbarS) for i in range(NLs))
zero_mode = sp.simplify(cmc_term([muS[i] + cS / NS[i] for i in range(NLs)]) - cmc_term(muS))
m1_ok = (m1_R and sp.simplify(ELc["T"] + 2 * sp.diff(Lam_, t_)) == 0 and sp.simplify(ELc["Lambda"] - (2 * sp.diff(T_, t_) - 2 * N_ * a_ ** 3)) == 0
         and sp.simplify(fr_c - (8 * sp.pi * Gs * ms + Lam_ * a_ ** 3) / (3 * a_)) == 0 and leafsum == 0 and zero_mode == 0)
P(f"    EL(T) = {ELc['T']};  EL(Lambda) = {ELc['Lambda']};  Friedmann: adot^2 = {fr_c}")
P(f"    any leaf: Sum_j v_j (K_j - <K>) = {leafsum};  change of the CMC term under mu_j -> mu_j + c/N_j: {zero_mode}")
check("M1 THE COMBINED ACTION ON FRW: sqrt(-g) R = -6 a adot^2/N + a total derivative (from the metric); the CMC term vanishes on a "
      "homogeneous leaf and, on ANY leaf, has no global part (Sum_j v_j (K_j - <K>) = 0 identically) and an exact zero-mode "
      "symmetry mu N -> mu N + c(t): its multiplier's zero mode is pure gauge; HT gives Lambda-dot = 0 and T-dot = N a^3; "
      "Friedmann is GR + Lambda_0",
      f"R identity {m1_R}; leaf sum {leafsum}; zero-mode change {zero_mode}; EL(T) = {ELc['T']}", m1_ok,
      "the CMC condition's global part is EMPTY; HT's content is purely global -- the two live in complementary sectors")
# M2
EL2 = [sp.simplify(e_) for e_ in el_exprs(L_R - 2 * Lam0s * sqg_ + L_dust, [a_, N_], [t_])]
add2 = sp.solve(EL2[1].subs(N_, 1), ad ** 2)[0]
addd = sp.solve(EL2[0].subs(N_, 1).doit(), sp.diff(a_, t_, 2))[0]
Kn = Kfrw.subs(N_, 1)
dKdt = sp.factor(sp.simplify(sp.expand(sp.diff(Kn, t_).subs(sp.diff(a_, t_, 2), addd)).subs(ad ** 2, add2)))
Qsh = sp.simplify(sp.expand(Kn ** 2 / 3 - 8 * sp.pi * Gs * ms / a_ ** 3).subs(ad ** 2, add2))
As_ = sp.Symbol('A', positive=True)
Kinf_sym = sp.limit(3 * sp.sqrt(add2.subs(a_, As_)) / As_, As_, sp.oo)
m2_ok = (sp.simplify(dKdt + 12 * sp.pi * Gs * ms / a_ ** 3) == 0 and sp.simplify(Qsh - Lam0s) == 0
         and sp.simplify(Kinf_sym - sp.sqrt(3 * Lam0s)) == 0)
P(f"    dust FRW (N = 1): dK/dt = {dKdt};  Q = K^2/3 - 8 pi G rho_m on shell = {Qsh};  K_inf = {Kinf_sym}")
check("M2 YORK TIME IS A CLOCK, Lambda IS CONSERVED: on dust FRW dK/dt = -12 pi G rho_m (never zero while rho_m > 0), while "
      "Lambda-dot = 0; the only conserved combination of the leaf data is the Friedmann (global Hamiltonian) one, "
      "Q = K^2/3 - 8 pi G rho_m = Lambda_0; K -> K_inf = sqrt(3 Lambda_0) as rho_m -> 0",
      f"dK/dt = {dKdt}; Q = {Qsh}; K_inf = {Kinf_sym}", m2_ok,
      "a conserved momentum (Lambda_0) cannot be a function of a ticking clock (K): any identification Lambda == F(K) either "
      "freezes K or makes F constant (M3)")
# M3 MB
c1s, c2s, c3s = sp.symbols('c1 c2 c3')
fK = lambda k: c1s * k + c2s * k ** 2 + c3s * k ** 3
L_MB = L_R + 2 * fK(Kfrw) * (sp.diff(T_, t_) - sqg_) + L_dust
ELMB = [sp.simplify(e_) for e_ in el_exprs(L_MB, [a_, N_, T_], [t_])]
fac_T = sp.factor(ELMB[2])
aan = sp.exp(K0s * t_ / 3)
sub_ans = lambda ex: sp.simplify(ex.subs(N_, 1).doit().subs(a_, aan).doit())
Td_sol = sp.solve(sub_ans(ELMB[1]), sp.diff(T_, t_))
eA = sub_ans(ELMB[0])
eA = sp.simplify(eA.subs(sp.diff(T_, t_, 2), sp.diff(Td_sol[0], t_)).subs(sp.diff(T_, t_), Td_sol[0])) if Td_sol else None
eT = sub_ans(ELMB[2])
E_LCDM = {z: E_of(z) for z in ZS[:4]}
m3_ok = bool(Td_sol) and eA == 0 and eT == 0 and ms in sp.sympify(Td_sol[0]).free_symbols
P(f"    EL(T) = {fac_T}")
P(f"    with K = K_0 (a = exp(K_0 t/3), N = 1): T-dot = {Td_sol[0] if Td_sol else None};  EL(a) -> {eA};  EL(T) -> {eT}")
P("    so H = K_0/3 at every z for ANY dust: E(z) = 1, against LCDM E(z) = " + ", ".join(f"{v:.3f}" for v in E_LCDM.values())
  + " at z = 0.5, 1, 2.5, 5")
check("M3 MERGER MB (ONE term 2 f(K)(T-dot - N a^3) replacing both mu and HT, f a generic cubic): T's equation is proportional to "
      "f'(K) dK/dt, so K is frozen; with K = K_0 the lapse equation is solved by the clock rate (the dust is absorbed into T-dot) "
      "and the scale-factor equation is then identically satisfied -- H = K_0/3 at every z for any dust.  This merger FAILS FRW "
      "(E(z) = 1 vs 1.322 / 1.791 / 3.769 / 8.294)",
      f"T-dot absorbs m: {m3_ok}; EL(a) under K = K_0: {eA}", m3_ok,
      "the only one-term merger that keeps both local structures pays with York time: the CMC leaf value becomes HT's conserved "
      "momentum (compare the linear-potential cuscuton, whose multiplier pins K = K_0)")
OUT["numbers"]["M3"] = dict(T_dot=str(Td_sol[0]) if Td_sol else None, E_LCDM=E_LCDM)
# M4 MA
L_MA = L_R + 2 * Lam_ * (sp.diff(ells * a_ ** 3, t_) - sqg_) + L_dust
ELMA = dict(zip(("a", "N", "Lambda"), [sp.simplify(e_) for e_ in el_exprs(L_MA, [a_, N_, Lam_], [t_])]))
Ksol = sp.simplify(sp.solve(ELMA["Lambda"], ad)[0])
K_MA = sp.simplify(3 * Ksol / (a_ * N_))
Lsol = sp.simplify(sp.solve(ELMA["N"].subs(ad, Ksol), Lam_)[0])
z_zero = OM_M ** (-1.0 / 3.0) - 1.0
m4_ok = sp.simplify(K_MA - 1 / ells) == 0 and sp.simplify(Lsol - (1 / (3 * ells ** 2) - 8 * sp.pi * Gs * ms / a_ ** 3)) == 0
P(f"    MA: Lambda's equation gives K = {K_MA}; the lapse equation gives Lambda(t) = {Lsol}")
check("M4 MERGER MA (T^m = l sqrt(-g) n^m, the linear-cuscuton form of the HT term): Lambda's equation pins K = 1/l (a NEW constant) "
      "and the lapse equation makes Lambda(t) = 1/(3 l^2) - 8 pi G rho_m, not constant: with l set today, Lambda falls to zero at "
      f"z = Omega_m^(-1/3) - 1 = {z_zero:.3f} and a0 = alpha(Lambda) is undefined beyond -> FAILS",
      f"K = {K_MA}; Lambda(t) = {Lsol}", m4_ok)
# M5 HT has no foliation
Y4 = sp.symbols('y0:4')
om_ = {}
for i in range(4):
    for j in range(i + 1, 4):
        om_[(i, j)] = sp.Function(f'w{i}{j}')(*Y4)
        om_[(j, i)] = -om_[(i, j)]
div2 = sp.simplify(sum(sp.diff(om_[(m, n)], Y4[n], Y4[m]) for m in range(4) for n in range(4) if m != n))
T0f = lambda tt_, x: tt_ + 0.3 * math.sin(x) * tt_ ** 2
T1f = lambda tt_, x: 0.2 * math.cos(x) * tt_
rho_ = lambda tt_, x: 1 + 0.4 * math.sin(x) * tt_                          # d_t T0 + d_x T1
Tq_ = lambda f, fp: quad(lambda x: T0f(f(x), x) - fp(x) * T1f(f(x), x), 0, 2 * math.pi, epsabs=1e-13, epsrel=1e-13)[0]
f1, f1p = (lambda x: 0.4 + 0.1 * math.sin(x)), (lambda x: 0.1 * math.cos(x))
f2, f2p = (lambda x: 0.7 + 0.15 * math.cos(2 * x)), (lambda x: -0.3 * math.sin(2 * x))
stokes = Tq_(f2, f2p) - Tq_(f1, f1p) - dblquad(lambda tt_, x: rho_(tt_, x), 0, 2 * math.pi, f1, f2, epsabs=1e-12, epsrel=1e-12)[0]
g_ = lambda x: math.sin(x) + 0.5 * math.cos(3 * x)
vol_ = lambda cc: dblquad(lambda tt_, x: rho_(tt_, x), 0, 2 * math.pi, f1, lambda x: f1(x) + 0.2 * g_(x) + cc, epsabs=1e-12, epsrel=1e-12)[0]
c_zero = brentq(vol_, -0.3, 0.3, xtol=1e-14)
f3, f3p = (lambda x: f1(x) + 0.2 * g_(x) + c_zero), (lambda x: f1p(x) + 0.2 * (math.cos(x) - 1.5 * math.sin(3 * x)))
dev3 = max(abs(f3(x) - f1(x)) for x in np.linspace(0, 2 * math.pi, 400))
dT3 = Tq_(f3, f3p) - Tq_(f1, f1p)
dTdtau = sp.simplify(sp.solve(ELc["Lambda"], sp.diff(T_, t_))[0])
m5_ok = div2 == 0 and abs(stokes) < 1e-10 and abs(dT3) < 1e-10 and dev3 > 0.1 and sp.simplify(dTdtau - N_ * a_ ** 3) == 0
P(f"    3+1: d_m d_n omega^mn = {div2};  1+1: T[S2] - T[S1] - (four-volume between) = {stokes:.1e};  a surface displaced by up to "
  f"{dev3:.3f} but enclosing zero four-volume: T[S3] - T[S1] = {dT3:.1e};  on the FRW leaves dT/dtau = {dTdtau}")
check("M5 HT CARRIES NO FOLIATION (H1): the HT term is invariant under T^m -> T^m + d_n omega^{mn} (d_m d_n omega^{mn} = 0 in 3+1), "
      "T[S2] - T[S1] is the four-volume between the two surfaces (Stokes, 1+1), and a visibly different surface enclosing zero "
      "four-volume has the same T -- the four-volume time labels equivalence classes, not a foliation (Kuchar 1991).  On the "
      "khronon's leaves dT/dtau = N a^3 > 0: T is a monotone RELABELING of the CMC leaves, a gauge choice of the khronon's global "
      "reparametrization, not a merger", f"3-form identity {div2 == 0}; Stokes {stokes:.1e}; zero-volume deformation {dev3:.3f} -> "
      f"dT {dT3:.1e}; dT/dtau = {dTdtau}", m5_ok)

# ================================================================================================ F FRW + perturbations
banner("F   FRW + PERTURBATIONS: FP2's machinery + FP14's multiplier + the HT sector (delta Lambda, T^t, T^x)")
tF = time.time()
G2 = n14["G2"]
e_, tq, xq, a_t, rb = G2["e"], G2["tq"], G2["xq"], G2["a"], G2["rb"]
alc, Gc, Lam = G2["alc"], G2["Gc"], G2["Lam"]
Phi, Psi, Bq, Eq_, piq, th, dq = G2["FIELDS"]
mu1 = n14["mu1"]
Lq, Tt, Tx = [sp.Function(s_)(tq, xq) for s_ in ('dLambda', 'Tt', 'Tx')]
Tbar = sp.Function('Tbar')(tq)
LamF = Lam + e_ * Lq
Lt = sp.expand(G2["ser"](G2["sqg4"] * (G2["R4"] - 2 * LamF + alc * G2["aa4"]) - 2 * e_ * mu1 * G2["sqg4"] * G2["dK_leaf"]
                         + 16 * sp.pi * Gc * G2["Ldust"] + 2 * LamF * (sp.diff(Tbar + e_ * Tt, tq) + sp.diff(e_ * Tx, xq))))
L1f, L2f = Lt.coeff(e_, 1), Lt.coeff(e_, 2)
flF = G2["FIELDS"] + [mu1, Lq, Tt, Tx]
nmF = [F.func.__name__ for F in flF]
bgF = [sp.simplify(ee) for ee in el_exprs(L1f, flF, [tq, xq])]
kF = sp.Symbol('k', positive=True)
ampF = {F: sp.Function(F.func.__name__ + 'k')(tq) for F in flF}
rbs, adds = n14["rbs"], n14["adds"]


def fourierF(ex):
    for F in flF:
        ex = ex.subs(F, ampF[F] * sp.exp(sp.I * kF * xq))
    return sp.expand(sp.simplify(ex.doit() * sp.exp(-sp.I * kF * xq)))


def bgsubF(ex):
    ex = ex.subs({ampF[Bq]: 0, ampF[Eq_]: 0}).doit()
    ex = ex.subs(sp.diff(a_t, tq, 3), sp.diff(adds, tq)).subs(sp.diff(a_t, tq, 2), adds).subs(rb, rbs)
    ex = ex.subs(sp.diff(a_t, tq, 2), adds)
    return sp.expand(sp.simplify(ex))


EgF = [bgsubF(fourierF(ee)) for ee in el_exprs(L2f, flF, [tq, xq])]
Eg8, names8, amp8 = n14["Eg8"], n14["names8"], n14["amp8"]
sameF = {}
for nme in names8:
    mine = EgF[nmF.index(nme)].subs(ampF[Lq], 0).doit()
    mine = mine.subs({ampF[F]: amp8[F] for F in G2["FIELDS"] + [mu1]}).subs(kF, n14["kF"])
    sameF[nme] = sp.simplify(mine - Eg8[names8.index(nme)]) == 0
GeffF, slipF = G2["qs_mu"](dict(Eg=[EgF[nmF.index(F.func.__name__)].subs(ampF[Lq], 0) for F in G2["FIELDS"]], amp=ampF, k=kF, rbs=rbs))
f1_ok = (sp.simplify(bgF[nmF.index("dLambda")] - (2 * sp.diff(Tbar, tq) - 2 * a_t ** 3)) == 0 and bgF[nmF.index("mu")] == 0
         and sp.simplify(EgF[nmF.index("Tx")] + 2 * sp.I * kF * ampF[Lq]) == 0 and all(sameF.values())
         and sp.simplify(GeffF - 2 / (2 - alc)) == 0 and sp.simplify(slipF - 1) == 0)
P(f"    background: EL(dLambda) = {bgF[nmF.index('dLambda')]} (the clock, T-bar-dot = a^3), EL(mu) = {bgF[nmF.index('mu')]} (mu-bar gauge)")
P(f"    perturbations: EL(T^t)_k = {EgF[nmF.index('Tt')]};  EL(T^x)_k = {EgF[nmF.index('Tx')]}  ->  delta Lambda_k = 0 (k != 0);  "
  f"EL(dLambda)_k = {sp.factor(EgF[nmF.index('dLambda')])}")
P(f"    with delta Lambda_k = 0, equations == FP14 C1b's: {sameF};  G_eff/G = {sp.factor(GeffF)}, slip {slipF}  ({time.time() - tF:.1f} s)")
check("F1 FRW + PERTURBATIONS OF THE COMBINED ROOT: T^x's equation forces delta Lambda_k = 0 on every k != 0 mode, delta Lambda's "
      "equation is the unimodular clock, the multiplier's background is pure gauge, and with delta Lambda = 0 all eight remaining "
      "linear equations EQUAL FP14 C1b's: G_eff/G = 2/(2 - alpha_c), no slip -- HT adds nothing to FRW growth",
      f"clock {bgF[nmF.index('dLambda')]}; equations equal {all(sameF.values())}; G_eff/G {sp.factor(GeffF)}; slip {slipF}", f1_ok)

# ================================================================================================ L Minkowski block
banner("L   THE LINEAR BLOCK ABOUT MINKOWSKI (FP14's unitary-gauge construction, extended by the HT sector and the mergers)")
tL = time.time()
ttm, xxm, yym, zzm = sp.symbols('t x y z', real=True)
X3m = (xxm, yym, zzm)
eb = sp.Symbol('e_b')
alm, c2m, Cph, lmm, sgm = sp.symbols('alpha_c c_2 C_phi lambda sigma', real=True)
mL, gph, f1c, mub, b1, cbar = sp.symbols('m_L g_phi f_1 mubar b_1 cbar', real=True)
nf, pf, Bf, Sf, Ff, Mf, Lf, Df = [sp.Function(s_)(ttm, xxm, yym, zzm) for s_ in ('n', 'psi', 'B', 'S', 'phi', 'mu', 'dLambda', 'D')]
kq_, wq_ = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AF, AM, AL, AD = sp.symbols('A_n A_psi A_B A_S A_phi A_mu A_L A_D')
AMP = {"n": An, "psi": Ap, "B": AB, "S": AS, "phi": AF, "mu": AM, "dLambda": AL, "D": AD}


def block(form):
    """FP14's unitary_block (copied, same conventions) extended: 'c2', 'mult' (FP14's), 'comb' = mult + HT (Lambda = e dLambda,
    d_m T^m = 1 + e D with D the 3-form-gauge-invariant divergence, plus generic couplings m_L dLambda^2/2 and g_phi dLambda d_z phi
    for the alpha(Lambda) terms), 'MB' = 2 f(K)(d_m T^m - sqrt(-g)) with f = f_1 K, 'MC' = mu == mubar + b_1 dLambda with HT,
    'MCbar' = the constant-mubar term alone."""
    Nl = sp.exp(eb * nf)
    gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
    gin = gam.inv()
    Ni = [eb * (sp.diff(Bf, X3m[0]) + Sf), eb * sp.diff(Bf, X3m[1]), eb * sp.diff(Bf, X3m[2])]
    Gm3 = [[[sum(gin[a2, d2] * (sp.diff(gam[d2, b2], X3m[c2_]) + sp.diff(gam[d2, c2_], X3m[b2]) - sp.diff(gam[b2, c2_], X3m[d2]))
                 for d2 in range(3)) / 2 for c2_ in range(3)] for b2 in range(3)] for a2 in range(3)]
    DN = [[sp.diff(Ni[j], X3m[i]) - sum(Gm3[q][i][j] * Ni[q] for q in range(3)) for j in range(3)] for i in range(3)]
    Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], ttm) - DN[i][j] - DN[j][i]) / (2 * Nl))
    Kup = gin * Kij * gin
    KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
    trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))

    def Ric3(b2, c2_):
        return sum(sp.diff(Gm3[a2][b2][c2_], X3m[a2]) - sp.diff(Gm3[a2][b2][a2], X3m[c2_]) +
                   sum(Gm3[a2][a2][d2] * Gm3[d2][b2][c2_] - Gm3[a2][c2_][d2] * Gm3[d2][b2][a2] for d2 in range(3)) for a2 in range(3))
    R3 = sum(gin[b2, c2_] * Ric3(b2, c2_) for b2 in range(3) for c2_ in range(3))
    ai = [sp.diff(sp.log(Nl), xi_) for xi_ in X3m]
    aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
    Fi = [sp.diff(eb * Ff, xi_) for xi_ in X3m]
    Xi = [sgm * Fi[i] for i in range(3)]
    chassis = 2 * (2 - alm) * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3)) - (2 - alm) * sum(
        gin[i, j] * Xi[i] * Xi[j] for i in range(3) for j in range(3))
    Jquad = -2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3))
    ndphi = (sp.diff(eb * Ff, ttm) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
    sqg = Nl * sp.exp(-3 * eb * pf)
    flds, kin, extra = [nf, pf, Bf, Sf, Ff], 0, 0
    if form == "c2":
        kin = -c2m * trK ** 2
    elif form in ("mult", "comb"):
        kin = -2 * eb * Mf * trK
        flds.append(Mf)
    if form in ("comb", "MC"):
        extra = 2 * eb * Lf * (1 + eb * Df - sqg) + mL * eb ** 2 * Lf ** 2 / 2 + gph * eb * Lf * sp.diff(eb * Ff, zzm)
        flds += [Lf, Df]
    if form == "MC":
        kin = -2 * (mub + eb * b1 * Lf) * trK
    if form == "MCbar":
        kin = -2 * mub * trK
    if form == "MB":
        extra = 2 * f1c * trK * (1 + eb * Df - sqg)
        flds.append(Df)
    Lfull = sqg * (KK - trK ** 2 + R3 + alm * aa + kin + chassis + Jquad + 2 * lmm * ndphi ** 2) + extra
    L2_ = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
    phs = sp.exp(sp.I * (kq_ * zzm - wq_ * ttm))
    fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Ff: AF * phs, Mf: AM * phs, Lf: AL * phs, Df: AD * phs}
    ELk = [sp.expand(sp.simplify(e2.subs(fsub).doit() / phs)) for e2 in el_exprs(L2_, flds, [ttm, xxm, yym, zzm])]
    return dict(zip([f_.func.__name__ for f_ in flds], ELk))


def mmat(E, order):
    return sp.Matrix([[sp.expand(sp.diff(E[r_], AMP[c_])) for c_ in order] for r_ in order])


EB = {fm: block(fm) for fm in ("c2", "mult", "comb", "MB", "MC", "MCbar")}
det_mult = sp.factor(sp.expand(mmat(EB["mult"], ["psi", "n", "B", "phi", "mu"]).det(method='berkowitz')))
det_c2 = sp.factor(sp.expand(mmat(EB["c2"], ["psi", "n", "B", "phi"]).det(method='berkowitz')))
l0_ok = bool(det_line) and f"det (c_2 -> oo form) = {det_mult};" in det_line[0]
check("L0 CONTROL this lane's extended block (FP14's unitary-gauge construction, copied) reproduces FP14's committed multiplier "
      "determinant string exactly", f"det = {det_mult}", l0_ok)
Mcomb = mmat(EB["comb"], ["psi", "n", "B", "phi", "mu", "dLambda", "D"])
det_comb = sp.factor(sp.expand(Mcomb.det(method='berkowitz')))
r_comb = sp.simplify(det_comb / det_mult)
same_eq = {k_: sp.simplify(EB["comb"][k_].subs(AL, 0) - EB["mult"][k_]) == 0 for k_ in ("n", "psi", "B", "phi", "mu")}
D_only = [k_ for k_ in EB["comb"] if EB["comb"][k_].has(AD)]
Jsrc = sp.Symbol('J')
keys5 = ["n", "psi", "B", "phi", "mu"]
sol0 = sp.solve([EB["mult"][k_].subs(wq_, 0) - (Jsrc if k_ == "n" else 0) for k_ in keys5[:4]], [An, Ap, AB, AF], dict=True)[0]
nJ = sp.simplify(sol0[An] / Jsrc)
GN_ratio = sp.factor(sp.simplify(sp.limit(nJ, Cph, sp.oo) / sp.limit(sp.limit(nJ, Cph, sp.oo), alm, 0)))
l1_ok = (r_comb == -4 and all(same_eq.values()) and D_only == ["dLambda"] and sp.simplify(EB["comb"]["D"] - 2 * AL) == 0
         and sp.simplify(GN_ratio - 2 / (2 - alm)) == 0 and n14["static_mond"] and n14["same_inf"] and n14["efe_blind"])
P(f"    combined: det = {r_comb} x det(FP14 multiplier);  E_D = {EB['comb']['D']};  A_D only in {D_only};  "
  f"equations at A_L = 0 == FP14's: {same_eq}")
P(f"    static lapse response n/J = {nJ};  Newtonian limit (C_phi -> oo) relative to alpha_c = 0: {GN_ratio}  (York/CMC: 2)")
check("L1 THE COMBINED BLOCK (FP14's multiplier + HT, generic delta Lambda couplings m_L, g_phi): det = -4 x det(FP14), D's row forces "
      "delta Lambda = 0, and with delta Lambda = 0 FP14's five equations are unchanged -- so the count (deg_omega 4; 2 at lambda = 0), "
      "the health, and every response FP14 C2 scored (static MOND pole, equal-time part c_2-blind and EFE-blind) carry over; the "
      "static Newtonian-limit coupling is 2/(2 - alpha_c) of GR's, not the York/CMC 2: THE KILL STAYS EVADED",
      f"det ratio {r_comb}; equations unchanged {all(same_eq.values())}; G_N/G = {GN_ratio}; FP14 C2 flags (reproduced) static "
      f"{n14['static_mond']}, equal-time {n14['same_inf']}, EFE-blind {n14['efe_blind']}", l1_ok)
Mmb = mmat(EB["MB"], ["psi", "n", "B", "phi", "D"])
r_MB = sp.simplify(sp.factor(sp.expand(Mmb.det(method='berkowitz'))) / det_mult)
check("L2 MB LOCALLY: det(MB) = f_1^2 x det(FP14 multiplier block) -- at k != 0 the merged single term IS FP14's CMC multiplier in "
      "other variables (mu <-> -f_1 (D - delta sqrt(-g))); its failure is purely global (M3: the zero mode freezes York time)",
      f"det ratio {r_MB}", sp.simplify(r_MB - f1c ** 2) == 0)
tot_der = [sp.simplify(EB["MCbar"][k_] - EB["c2"][k_].subs(c2m, 0)) for k_ in ("n", "psi", "B", "phi")]
det_MC = sp.factor(sp.expand(mmat(EB["MC"], ["psi", "n", "B", "phi", "dLambda", "D"]).det(method='berkowitz')))
det_c20 = sp.factor(det_c2.subs(c2m, 0))
r_MC = sp.simplify(det_MC / det_c20)
w_c20 = sp.factor(det_c20.subs(lmm, 0))
deg_c20 = sp.degree(sp.Poly(sp.numer(sp.together(w_c20)), wq_), wq_)
roots_c20 = sp.solve(sp.numer(sp.together(w_c20)), wq_)
l3_ok = all(v_ == 0 for v_ in tot_der) and r_MC == -4 and roots_c20 == [0]
P(f"    MC: the constant-mubar term's contribution to the field equations: {tot_der};  det(MC) = {r_MC} x det(c_2 = 0) = "
  f"{r_MC} x {det_c20};  at lambda = 0: {w_c20} -> omega roots {roots_c20}")
check("L3 MC (the multiplier made the HT field, mu = mubar + b_1 delta Lambda; b_1 needs a NEW constant): HT forces delta Lambda = 0, "
      "so delta mu = 0; the constant-mubar term is a total derivative (sqrt(-g) K = d_m(sqrt(-g) n^m); no field-equation change); "
      "the block is FP14's c_2 = 0 block, whose only scalar root at lambda = 0 is omega = 0: the khronon is FROZEN (FP5 B4's "
      "exceptional surface) and the CMC condition is lost -> FAILS",
      f"total derivative {all(v_ == 0 for v_ in tot_der)}; det ratio {r_MC}; lambda = 0 roots {roots_c20}", l3_ok)
# L4 SQ
e2_, dc_, K1_, ds_ = sp.symbols('e2 dc K1 ds')
sq2 = sp.expand(-(cbar + e2_ * dc_) * (1 + e2_ * ds_) * (e2_ * K1_) ** 2).coeff(e2_, 2)
Kform = sp.expand(EB["mult"]["mu"])
Mc2 = mmat(EB["c2"], ["psi", "n", "B", "phi"])
det_c2x = sp.expand(Mc2.det(method='berkowitz'))
sq_rows = []
for pars in (dict(alpha_c=sp.Rational(1, 3), C_phi=sp.Rational(1, 5), sigma=sp.Rational(7, 10), cbar=sp.Rational(3, 2), k=1),
             dict(alpha_c=sp.Rational(1, 100), C_phi=sp.Rational(3, 1), sigma=sp.Rational(1, 2), cbar=sp.Rational(1, 20), k=2)):
    sub = {alm: pars["alpha_c"], Cph: pars["C_phi"], sgm: pars["sigma"], c2m: pars["cbar"], kq_: pars["k"], lmm: 0}
    roots = [r_ for r_ in sp.solve(det_c2x.subs(sub), wq_) if r_.is_real and r_ > 0]
    for w0 in roots:
        vec = list(Mc2.subs(sub).subs(wq_, w0).nullspace()[0])
        dK = complex(sp.N(Kform.subs(sub).subs(wq_, w0).subs(dict(zip([Ap, An, AB, AF], vec))).subs(AM, 0)))
        nrm = math.sqrt(sum(abs(complex(sp.N(v_))) ** 2 for v_ in vec))
        solv = Mc2.subs(sub).subs(wq_, sp.Rational(3, 7)).LUsolve(sp.Matrix([0, 1, 0, 0]))
        dKf = complex(sp.N(Kform.subs(sub).subs(wq_, sp.Rational(3, 7)).subs(dict(zip([Ap, An, AB, AF], list(solv)))).subs(AM, 0)))
        sq_rows.append(dict(pars={k_: str(v_) for k_, v_ in pars.items()}, omega=float(w0), dK_mode_over_norm=abs(dK) / nrm,
                            dK_forced_over_J=abs(dKf)))
for r_ in sq_rows:
    P(f"    SQ at {r_['pars']}: scalar root omega = {r_['omega']:.4f}, |delta K|/|mode| = {r_['dK_mode_over_norm']:.3f}; forced at "
      f"omega = 3/7: |delta K/J| = {r_['dK_forced_over_J']:.3f}")
l4_ok = (not sq2.has(dc_)) and sp.simplify(sq2 + cbar * K1_ ** 2) == 0 and all(r_["dK_mode_over_norm"] > 1e-3 and r_["dK_forced_over_J"] > 1e-3
                                                                              for r_ in sq_rows)
check("L4 SQ (ONE GLOBAL multiplier c(t) with Int N sqrt(h)(K - <K>)^2 = 0, the only global way to impose CMC): its fluctuation is "
      f"ABSENT at quadratic order (the second-order term is {sq2}); the quadratic action is FP14's c_2 block at c_2 = cbar, a value "
      "no equation fixes (the knob FP14 eliminated returns); the scalar mode and a time-dependent forced response both carry "
      "delta K != 0, which the forceless constraint forbids: irregular, not FP14's regular CMC limit -> FAILS",
      "; ".join(f"|dK|/|mode| {r_['dK_mode_over_norm']:.3f}, forced {r_['dK_forced_over_J']:.3f}" for r_ in sq_rows), l4_ok)
OUT["numbers"]["L"] = dict(det_comb_ratio=str(r_comb), GN_ratio=str(GN_ratio), det_MB_ratio=str(r_MB), det_MC_ratio=str(r_MC),
                           c2_zero_lambda0=str(w_c20), SQ=sq_rows)
P(f"    ({time.time() - tL:.1f} s)")

# ================================================================================================ D the Dirac analysis on a lattice
banner("D   THE DIRAC ANALYSIS: the trace sector of the actual action on a periodic leaf of N_L sites (sympy + exact brackets, numeric rank)")
tD = time.time()


def Jp2(s):
    return -sp.log(1 - 2 * sp.sqrt(s)) / 4 - sp.sqrt(s) / 2 - s / 2


def build_lattice(model, NL, mond, alc_val=0.3, w_val=0.2):
    """the root's trace sector on a periodic leaf: sqrt(h) = v_j, N_j, K_j = v-dot_j/(N_j v_j), <K> = Sum v_j K_j / Sum v_j, h^xx = v^(-2/3);
    L = Sum_j N_j v_j [-(2/3) K_j^2 - 2 mu_j (K_j - <K>) + w h (dln v)^2 + alpha_c h (dln N)^2 + (2 - alpha_c) h (2 dln N - dphi) dphi
        - 2 alpha(Lambda_j)^2 J_P2(h dphi^2/alpha^2)] + 2 Lambda_j (T-dot_j + X_j - X_(j-1) - N_j v_j) - d_j N_j   (d_j: dust);
    models: 'comb' (FP14 core + HT), 'core' (no HT, Lambda a constant), 'noCMC' (comb without the mu term), 'globalHT' (one global
    pair 2 Lambda_0 (T-dot - Sum N v) instead of the local HT fields), 'MB' (Lambda_j == f(K_j) = K_j^2/3, no mu).  phi (lambda = 0)
    is included when mond is True; alpha = kappa sqrt(Lambda/8 pi) reads the HT momentum (p_T = 2 Lambda)."""
    J = range(NL)
    v = sp.symbols(f'v0:{NL}', positive=True); Nn = sp.symbols(f'N0:{NL}', positive=True)
    mu = sp.symbols(f'mu0:{NL}'); Tq = sp.symbols(f'T0:{NL}'); Xq = sp.symbols(f'X0:{NL}'); ph = sp.symbols(f'phi0:{NL}')
    vd = sp.symbols(f'vd0:{NL}'); Td = sp.symbols(f'Td0:{NL}')
    pv = sp.symbols(f'pv0:{NL}'); pN = sp.symbols(f'pN0:{NL}'); pmu = sp.symbols(f'pmu0:{NL}'); pT = sp.symbols(f'pT0:{NL}')
    pX = sp.symbols(f'pX0:{NL}'); pph = sp.symbols(f'pphi0:{NL}')
    Tg, pTg = sp.symbols('Tg pTg')
    dm = sp.symbols(f'd0:{NL}', positive=True)
    Lam0 = sp.Symbol('Lambda0', positive=True)
    alc_, w_ = sp.Float(alc_val), sp.Float(w_val)
    V = sum(v)
    K = [vd[i] / (Nn[i] * v[i]) for i in J]
    Kbar = sum(vd[i] / Nn[i] for i in J) / V
    h = [v[i] ** sp.Rational(-2, 3) for i in J]
    nx = lambda i: (i + 1) % NL
    aN = [sp.log(Nn[nx(i)]) - sp.log(Nn[i]) for i in J]
    dv = [sp.log(v[nx(i)]) - sp.log(v[i]) for i in J]
    dph = [ph[nx(i)] - ph[i] for i in J]
    LamS = {'comb': [pT[i] / 2 for i in J], 'noCMC': [pT[i] / 2 for i in J], 'globalHT': [pTg / 2 for i in J],
            'core': [Lam0 for i in J], 'MB': [None for i in J]}[model]

    def U(i, Lam_i):
        u = w_ * h[i] * dv[i] ** 2 + alc_ * h[i] * aN[i] ** 2
        if mond:
            al = KAPPA * sp.sqrt(Lam_i / (8 * sp.pi))
            u += (2 - alc_) * h[i] * (2 * aN[i] - dph[i]) * dph[i] - 2 * al ** 2 * Jp2(h[i] * dph[i] ** 2 / al ** 2)
        return u
    kinL = sum(Nn[i] * v[i] * (-sp.Rational(2, 3) * K[i] ** 2) for i in J)
    if model in ('comb', 'core', 'globalHT'):
        kinL += sum(Nn[i] * v[i] * (-2 * mu[i] * (K[i] - Kbar)) for i in J)
    q_vel, moms = list(vd), list(pv)
    if model == 'MB':
        kinL += sum(2 * (K[i] ** 2 / 3) * (Td[i] + Xq[i] - Xq[(i - 1) % NL] - Nn[i] * v[i]) for i in J)
        q_vel += list(Td); moms += list(pT)
    potL = sum(Nn[i] * v[i] * U(i, LamS[i]) for i in J) - sum(dm[i] * Nn[i] for i in J)
    eqs = [sp.Eq(moms[k_], sp.diff(kinL, q_vel[k_])) for k_ in range(len(q_vel))]
    if model == 'MB':
        sol = {vd[i]: Nn[i] * v[i] * sp.sqrt(sp.Rational(3, 2) * pT[i]) for i in J}      # p_T = (2/3) K^2, expanding branch
        sol.update(sp.solve([e_.subs(sol) for e_ in eqs[:NL]], list(Td), dict=True)[0])
    else:
        sol = sp.solve(eqs, q_vel, dict=True)[0]
    Hc = (sum(moms[k_] * q_vel[k_] for k_ in range(len(q_vel))) - kinL).subs(sol) - potL
    if model in ('comb', 'noCMC'):
        Hc += sum(2 * LamS[i] * Nn[i] * v[i] for i in J) - sum(2 * LamS[i] * (Xq[i] - Xq[(i - 1) % NL]) for i in J)
    if model == 'globalHT':
        Hc += 2 * LamS[0] * sum(Nn[i] * v[i] for i in J)
    if model == 'core':
        Hc += sum(2 * Lam0 * Nn[i] * v[i] for i in J)
    Q, Pm, prim = list(v) + list(Nn), list(pv) + list(pN), list(pN)
    if model in ('comb', 'core', 'globalHT'):
        Q += list(mu); Pm += list(pmu); prim += list(pmu)
    if model in ('comb', 'noCMC', 'MB'):
        Q += list(Tq) + list(Xq); Pm += list(pT) + list(pX); prim += list(pX)
    if model == 'globalHT':
        Q += [Tg]; Pm += [pTg]
    if mond:
        Q += list(ph); Pm += list(pph); prim += list(pph)
    conj = dict(zip(Pm, Q))
    sec = [-sp.diff(Hc, conj[p_]) for p_ in prim]
    return dict(Hc=Hc, Q=Q, P=Pm, prim=prim, sec=sec, v=v, N=Nn, mu=mu, pv=pv, pT=pT, pmu=pmu, pN=pN, pX=pX, pph=pph, T=Tq, ph=ph,
                dm=dm, Lam0=Lam0, pTg=pTg, Tg=Tg, K=K, Kbar=Kbar, sol=sol, NL=NL, model=model, mond=mond)


def surface_point(M, Kbar_val=0.8, P0=1.0, seed=3):
    """a point on the constraint surface: primaries 0, HT momenta uniform, CMC gauge <mu N> = 0 (mu_j = -(p_v,j + 4 Kbar/3)/2), the
    lapse and phi equations solved (fsolve from the phi = ln N lock), York time Kbar (or K_0 for MB) chosen, Lambda_0 solved."""
    NL, model = M["NL"], M["model"]
    rng = np.random.default_rng(seed)
    vv = 1.0 + 0.3 * rng.random(NL); NN = 1.0 + 0.005 * rng.standard_normal(NL); dd = 0.2 + 0.3 * rng.random(NL)
    pt = {M["v"][i]: vv[i] for i in range(NL)}
    pt.update({M["N"][i]: NN[i] for i in range(NL)}); pt.update({M["dm"][i]: dd[i] for i in range(NL)})
    for z_ in M["Q"] + M["P"]:
        pt.setdefault(z_, 0.0)
    P0u, Kbu = sp.Symbol('P0u'), sp.Symbol('Kbu')
    unk = list(M["pv"]) + ([P0u] if model in ('comb', 'noCMC', 'MB') else []) + ([M["pTg"]] if model == 'globalHT' else []) + \
        ([Kbu] if model == 'core' else []) + (list(M["ph"][1:]) if M["mond"] else [])
    subsP = {M["pT"][i]: P0u for i in range(NL)} if model in ('comb', 'noCMC', 'MB') else {}
    lapse = [M["sec"][M["prim"].index(p_)] for p_ in M["pN"]]
    mondeq = [M["sec"][M["prim"].index(p_)] for p_ in M["pph"]][1:] if M["mond"] else []
    fixed = {z_: pt[z_] for z_ in list(M["v"]) + list(M["N"]) + list(M["dm"])}
    fixed[M["ph"][0]] = 0.0
    Kb = Kbu if model == 'core' else sp.Float(Kbar_val)
    musub = {M["mu"][i]: -(M["pv"][i] + sp.Rational(4, 3) * Kb) / 2 for i in range(NL)} if model in ('comb', 'core', 'globalHT') else {}
    eqs = [e_.subs(subsP).subs(musub).subs(fixed) for e_ in lapse + mondeq]
    if model in ('comb', 'core', 'globalHT'):
        eqs.append(sum(M["pv"][i] * fixed[M["N"][i]] * fixed[M["v"][i]] for i in range(NL))
                   + sp.Rational(4, 3) * Kb * sum(fixed[M["N"][i]] * fixed[M["v"][i]] for i in range(NL)))
    if model == 'MB':
        eqs.append(P0u - sp.Rational(2, 3) * sp.Float(Kbar_val) ** 2)
    if model == 'noCMC':
        eqs.append(P0u - P0)
    if model == 'core':
        eqs = [e_.subs(M["Lam0"], P0 / 2) for e_ in eqs]
    rest = {z_: 0.0 for z_ in M["Q"] + M["P"] if z_ not in unk and z_ not in fixed and z_ not in musub}
    eqs = [e_.subs(rest) for e_ in eqs]
    f = sp.lambdify([unk], eqs, 'numpy')
    x0 = [-1.0] * NL + [Kbar_val if model == 'core' else P0] + ([math.log(NN[i] / NN[0]) for i in range(1, NL)] if M["mond"] else [])
    sol, info, ier, msg = fsolve(lambda y: np.array(f(y), dtype=float), x0, full_output=True, xtol=1e-14)
    vals = dict(zip(unk, sol))
    pt.update({k_: v_ for k_, v_ in vals.items() if k_ not in (P0u, Kbu)})
    if model in ('comb', 'noCMC', 'MB'):
        pt.update({M["pT"][i]: vals[P0u] for i in range(NL)})
    Kbv = vals[Kbu] if model == 'core' else Kbar_val
    if model in ('comb', 'core', 'globalHT'):
        pt.update({M["mu"][i]: -(pt[M["pv"][i]] + 4.0 / 3.0 * Kbv) / 2 for i in range(NL)})
    if model == 'core':
        pt[M["Lam0"]] = P0 / 2
    return pt, float(np.abs(np.array(f(sol), dtype=float)).max()), Kbv


def analyse(M, pt, tol=1e-9, extra=None):
    """constraint surface residual, ranks of the constraint Jacobian and of the Poisson-bracket matrix (first/second class),
    the physical phase-space dimension 2n - 2 FC - SC, the consistency (no tertiary constraint) residual, and brackets of named
    combinations (extra: {name: phase-space function})."""
    par = {d_: pt[d_] for d_ in M["dm"]}
    if M["model"] == 'core':
        par[M["Lam0"]] = pt[M["Lam0"]]
    Z = M["Q"] + M["P"]; n = len(M["Q"])
    chi = [sp.sympify(c_).subs(par) for c_ in M["prim"] + M["sec"]]
    Hc = M["Hc"].subs(par)
    x = [pt[z_] for z_ in Z]
    grad = lambda F_: np.array(sp.lambdify(Z, sp.Matrix([sp.diff(F_, z_) for z_ in Z]), 'numpy')(*x), dtype=float).ravel()
    Jm = np.array(sp.lambdify(Z, sp.Matrix([[sp.diff(c_, z_) for z_ in Z] for c_ in chi]), 'numpy')(*x), dtype=float)
    hg = grad(Hc)
    Om = np.block([[np.zeros((n, n)), np.eye(n)], [-np.eye(n), np.zeros((n, n))]])
    with np.errstate(all='ignore'):
        Mb = Jm @ Om @ Jm.T
        chiH = Jm @ (Om @ hg)
    finite = bool(np.isfinite(Jm).all() and np.isfinite(hg).all() and np.isfinite(Mb).all() and np.isfinite(chiH).all())
    res = float(np.abs(np.array(sp.lambdify(Z, sp.Matrix(chi), 'numpy')(*x), dtype=float)).max())
    sJ = np.linalg.svd(Jm, compute_uv=False); sM = np.linalg.svd(Mb, compute_uv=False)
    rJ = int((sJ > tol * sJ[0]).sum()); rM = int((sM > tol * sM[0]).sum())
    npr = len(M["prim"])
    u = np.linalg.lstsq(Mb[:, :npr], -chiH, rcond=None)[0]
    cons = float(np.abs(Mb[:, :npr] @ u + chiH).max())
    out = dict(n=n, nconstr=len(chi), rankJ=rJ, SC=rM, FC=rJ - rM, dims=2 * n - 2 * (rJ - rM) - rM, surface_res=res, consistency_res=cons,
               gapJ=float(sJ[rJ - 1] / max(sJ[rJ], 1e-300)) if rJ < len(sJ) else float('inf'),
               gapM=float(sM[rM - 1] / max(sM[rM], 1e-300)) if rM < len(sM) else float('inf'), finite=finite)
    pfl = np.zeros(2 * n)
    with np.errstate(all='ignore'):
        for a_i, p_ in enumerate(M["prim"]):                              # + u_a {z, phi_a}
            pfl += u[a_i] * (Om @ grad(sp.sympify(p_)))
    with np.errstate(all='ignore'):
        zdot = Om @ hg + pfl
    out["finite"] = out["finite"] and bool(np.isfinite(zdot).all()) and bool(np.isfinite(u).all())
    out["zdot"] = dict(zip([str(z_) for z_ in Z], zdot))
    if extra:
        for nm_, F_ in extra.items():
            gF = grad(sp.sympify(F_).subs(par))
            with np.errstate(all='ignore'):
                brk = Jm @ (Om @ gF)
            out["finite"] = out["finite"] and bool(np.isfinite(brk).all()) and bool(np.isfinite(gF).all())
            out[nm_ + "_bracket_max"] = float(np.abs(brk).max())
            out[nm_ + "_dot"] = float(gF @ zdot)
            out[nm_ + "_grad"] = gF
    out["Jm"], out["Mb"], out["Z"], out["chi"] = Jm, Mb, Z, chi
    return out


LAT = {}
for mond in (False, True):
    for model in ('comb', 'core', 'noCMC', 'globalHT') + (('MB',) if not mond else ()):
        for NL in (3, 4):
            M = build_lattice(model, NL, mond)
            pt, fres, Kbv = surface_point(M)
            extra = {}
            if model in ('comb', 'core', 'globalHT'):
                extra["Kbar"] = sum(M["v"][i] * (-sp.Rational(3, 4)) * (M["pv"][i] + 2 * M["mu"][i] - 2 * sum(
                    M["mu"][k_] * M["N"][k_] * M["v"][k_] for k_ in range(NL)) / (M["N"][i] * sum(M["v"]))) for i in range(NL)) / sum(M["v"])
                extra["mu_zero"] = sum(M["pmu"][i] / M["N"][i] for i in range(NL))
            if model in ('comb', 'noCMC', 'MB'):
                extra["pT0"] = M["pT"][0]
                extra["T_tot"] = sum(M["T"])
            if model == 'MB':
                extra["K0site"] = sp.sqrt(sp.Rational(3, 2) * M["pT"][0])
            extra["lapse_scaling"] = sum(M["N"][i] * M["pN"][i] for i in range(NL))
            extra["Hc"] = M["Hc"]                               # the canonical Hamiltonian: homogeneous of degree 1 in the lapse
            r = analyse(M, pt, extra=extra)
            if model in ('comb', 'noCMC', 'MB'):
                r["T_G"] = float(sum(r["Hc_grad"][len(M["Q"]) + M["P"].index(M["pT"][i])] for i in range(NL)))   # {T_tot, H} = dH/dp_T
                r["NV"] = float(sum(pt[M["N"][i]] * pt[M["v"][i]] for i in range(NL)))
            if model in ('comb', 'core', 'globalHT'):
                idx_k = [M["prim"].index(p_) for p_ in M["pmu"]]
                idx_K = [len(M["prim"]) + M["prim"].index(p_) for p_ in M["pmu"]]
                r["cmc_block_rank"] = int(np.linalg.matrix_rank(r["Mb"][np.ix_(idx_K, idx_k)], tol=1e-9))
            if model in ('comb', 'noCMC', 'MB'):
                idx_C = [len(M["prim"]) + M["prim"].index(p_) for p_ in M["pX"]] + [M["prim"].index(p_) for p_ in M["pX"]]
                r["HT_rows_max"] = float(np.abs(r["Mb"][idx_C, :]).max())
            LAT[(model, NL, mond)] = r
            P(f"    {model:9s} phi={'yes' if mond else 'no ':3s} N_L={NL}: phase space {2 * r['n']:2d}, constraints {r['nconstr']:2d} (independent "
              f"{r['rankJ']:2d}), SC {r['SC']:2d}, FC {r['FC']:2d} -> physical dimension {r['dims']:2d} (2 N_L = {2 * NL}); residuals: surface "
              f"{r['surface_res']:.0e}, consistency {r['consistency_res']:.0e}; rank gaps {min(r['gapJ'], r['gapM']):.0e}; finite {r['finite']}")
expect = {'comb': 0, 'core': -2, 'noCMC': 0, 'globalHT': 0, 'MB': 0}
d1_ok = all(r["dims"] == 2 * k_[1] + expect[k_[0]] and r["surface_res"] < 1e-10 and r["consistency_res"] < 1e-10 and r["finite"]
            and min(r["gapJ"], r["gapM"]) > 1e10 for k_, r in LAT.items() if not k_[2])
d1m_ok = all(r["dims"] == 2 * k_[1] + expect[k_[0]] and r["surface_res"] < 1e-10 and r["consistency_res"] < 1e-10 and r["finite"]
             and min(r["gapJ"], r["gapM"]) > 1e10 for k_, r in LAT.items() if k_[2])
check("D1 THE LATTICE COUNT (MOND-free trace sector, N_L = 3 and 4): physical phase-space dimension 2 N_L for the combined root, 2 N_L - 2 "
      "for the core without HT (HT adds exactly ONE global pair), 2 N_L with no CMC term at all (the multiplier adds no degree of "
      "freedom -- FP14's 'same count'), 2 N_L for ONE global pair 2 Lambda_0 (T-dot - Sum N v) (the local HT fields are not needed on "
      "the khronon's leaves), and 2 N_L for the merged MB; every constraint surface and consistency condition solved to < 1e-10 "
      "(no tertiary constraints), rank gaps > 1e10",
      "; ".join(f"{k_[0]}/{k_[1]}: {r['dims']}" for k_, r in LAT.items() if not k_[2]), d1_ok)
check("D1m THE SAME WITH THE MOND SCALAR (lambda = 0, auxiliary; alpha read from the HT momentum, so the MOND sector feeds the clock): "
      "the counts are unchanged -- combined 2 N_L, core 2 N_L - 2, no-CMC 2 N_L, global pair 2 N_L; the phi zero mode is one more "
      "first-class constraint (FP14 L1's shift symmetry)", "; ".join(f"{k_[0]}/{k_[1]}: {r['dims']} (FC {r['FC']}, SC {r['SC']})"
                                                                   for k_, r in LAT.items() if k_[2]), d1m_ok)
rc4 = LAT[('comb', 4, False)]
d2_ok = (rc4["HT_rows_max"] < 1e-10 and rc4["cmc_block_rank"] == 3 and rc4["mu_zero_bracket_max"] < 1e-10
         and rc4["lapse_scaling_bracket_max"] < 1e-10 and rc4["consistency_res"] < 1e-10 and rc4["FC"] == 2 * 4 + 2 and rc4["SC"] == 4 * 4 - 4)
P(f"    combined, N_L = 4: HT constraint + pi_X bracket rows max {rc4['HT_rows_max']:.0e}; CMC block {{K_j - <K>, pi_mu_k}} rank "
  f"{rc4['cmc_block_rank']} (= N_L - 1); brackets of Sum pi_mu/N {rc4['mu_zero_bracket_max']:.0e}, Sum N pi_N "
  f"{rc4['lapse_scaling_bracket_max']:.0e}; the global Hamiltonian H_T = H_c + u.phi (second-class multipliers solved): brackets "
  f"= the consistency residual {rc4['consistency_res']:.0e}")
check("D2 THE CLASSES DO NOT MATCH: HT's spatial constraints and pi_X are FIRST class (their bracket rows vanish identically: no "
      "constraint depends on T or X), the CMC constraints are SECOND class (their bracket block with pi_mu has rank N_L - 1, full on "
      "the non-zero modes), and the mu zero mode (Sum pi_mu/N), the lapse scaling and the global Hamiltonian H_T = H_c + u.phi are "
      "first class.  "
      "A first-class family cannot be identified with a second-class one (the rank of the bracket matrix is a canonical invariant): "
      "the local parts cannot be one term, and the CMC's global part is pure gauge while HT's is a physical pair",
      f"HT rows {rc4['HT_rows_max']:.0e}; CMC rank {rc4['cmc_block_rank']}; FC {rc4['FC']} = 2 N_L + 2, SC {rc4['SC']} = 4 N_L - 4", d2_ok)
rmb = LAT[('MB', 4, False)]
rcm = LAT[('comb', 4, True)]
P(f"    with the MOND scalar (combined, N_L = 4): {{T_tot, H}}/Sum N v = {rcm['T_G'] / rcm['NV']:.6f} -- the unimodular clock's MOND "
  f"correction (XR20 T1b's 1 - (kappa^2/8 pi) F, on the lattice)")
OUT["numbers"]["D3_clock_mond"] = rcm["T_G"] / rcm["NV"]
d3_ok = (abs(rc4["T_G"] / rc4["NV"] - 1) < 1e-10 and abs(rc4["pT0_dot"]) < 1e-12 and abs(rc4["Kbar_dot"]) > 1e-3 and abs(rmb["pT0_dot"]) < 1e-12
         and abs(rmb["K0site_dot"]) < 1e-12)
P(f"    combined: {{T_tot, H}} = {rc4['T_G']:.4f} (Sum N v = {rc4['NV']:.4f}); p_T-dot = {rc4['pT0_dot']:.0e}; Kbar-dot = {rc4['Kbar_dot']:.4f};  "
  f"MB: p_T-dot = {rmb['pT0_dot']:.0e}, K-dot = {rmb['K0site_dot']:.0e}")
check("D3 THE GLOBAL STRUCTURE: {T_tot, H} = Sum N v != 0 (the four-volume rate), so T - tau is an admissible gauge for the khronon's global reparametrization (the "
      "four-volume time can LABEL the CMC leaves); on the constraint surface p_T (= 2 Lambda_0) is conserved exactly while the York "
      "clock Kbar ticks; in the merged MB the site values of K are frozen",
      f"{{T_tot, H}} {rc4['T_G']:.4f} (Sum N v {rc4['NV']:.4f}); p_T-dot {rc4['pT0_dot']:.0e}; Kbar-dot {rc4['Kbar_dot']:.4f}; MB K-dot {rmb['K0site_dot']:.0e}", d3_ok)
OUT["numbers"]["D"] = {f"{k_[0]}|NL={k_[1]}|phi={k_[2]}": {kk: (float(vv) if isinstance(vv, (float, np.floating)) else vv)
                                                            for kk, vv in r.items() if kk in ("n", "nconstr", "rankJ", "SC", "FC", "dims",
                                                                                              "surface_res", "consistency_res", "T_G",
                                                                                              "pT0_dot", "Kbar_dot", "K0site_dot")}
                       for k_, r in LAT.items()}
P(f"    ({time.time() - tD:.1f} s)")

# ================================================================================================ A the a0 tie
banner("A   THE a0 TIE: K_inf, K_0, the vacuum, and the local York time")
coef = KAPPA / math.sqrt(24 * math.pi)
K_inf = math.sqrt(3 * LAM_SI)
K_now = 3 * H0 / c_SI
a0_Kinf, a0_Know = coef * c_SI ** 2 * K_inf, coef * c_SI ** 2 * K_now
a1_ok = abs(a0_Kinf / A0["canonical"] - 1) < 1e-12 and abs(a0_Know / A0["alt"] - 1) < 1e-12
P(f"    (kappa/sqrt(24 pi)) = {coef:.6f};  K_inf = sqrt(3 Lambda) = {K_inf:.5e} 1/m -> a0 = {a0_Kinf:.6e};  K_0 = 3 H_0/c = {K_now:.5e} 1/m -> "
  f"a0 = {a0_Know:.6e};  K_0/K_inf = {K_now / K_inf:.5f} = 1/sqrt(Omega_Lambda)")
check("A1 THE FOOTING IDENTITY: the canonical a0 is (kappa/sqrt(24 pi)) c^2 K_inf with K_inf = sqrt(3 Lambda) the asymptotic York time, and "
      "the alt a0 is the same coefficient on today's York time K_0 = 3 H_0/c -- an algebraic identity (kappa stays FITTED; nothing is "
      "derived): applied at every z, the alt reading IS the rival a0 proportional to H(z)",
      f"canonical {a0_Kinf:.6e} vs FP0 {A0['canonical']:.6e}; alt {a0_Know:.6e} vs FP0 {A0['alt']:.6e}", a1_ok)
OUT["numbers"]["A1"] = dict(coef=coef, K_inf=K_inf, K_0=K_now, a0_Kinf=a0_Kinf, a0_K0=a0_Know)
# A2: the vacuum shift is a total derivative; Gryb-Thebault's large-volume constraint
tv, xv = sp.symbols('t x', real=True)
LamV, T0V, T1V, gV = sp.Function('Lambda')(tv, xv), sp.Function('T0')(tv, xv), sp.Function('T1')(tv, xv), sp.Function('g', positive=True)(tv, xv)
rv, Gv = sp.symbols('rho_vac G', positive=True)
Lv1 = gV * (-2 * LamV - 16 * sp.pi * Gv * rv) + 2 * LamV * (sp.diff(T0V, tv) + sp.diff(T1V, xv))
Lv2 = (gV * (-2 * LamV) + 2 * LamV * (sp.diff(T0V, tv) + sp.diff(T1V, xv))).subs(LamV, LamV + 8 * sp.pi * Gv * rv)
diffL = sp.expand(Lv1 - Lv2)
el_diff = [sp.simplify(e_) for e_ in el_exprs(diffL, [LamV, T0V, T1V, gV], [tv, xv])]
Kg, Lg = sp.symbols('K Lambda_g', positive=True)
hdet = sp.Symbol('sqrt_h', positive=True)
pi_trace = hdet * (Kg - 3 * Kg)                                           # h_ij pi^ij for pi^ij = sqrt(h)(K^ij - K h^ij), K_ij = (K/3) h_ij
Pgt = sp.Rational(2, 3) * pi_trace / hdet
gt = sp.solve(sp.Eq(2 * Lg - sp.Rational(3, 8) * Pgt ** 2, 0), Kg)
a2_ok = all(e_ == 0 for e_ in el_diff) and sp.simplify(diffL + 16 * sp.pi * Gv * rv * (sp.diff(T0V, tv) + sp.diff(T1V, xv))) == 0 and \
    gt == [sp.sqrt(3) * sp.sqrt(Lg)]
P(f"    L(Lambda) + vacuum - L(Lambda' = Lambda + 8 pi G rho_vac) = {sp.factor(diffL)};  its Euler-Lagrange terms: {el_diff}")
P(f"    Gryb-Thebault H_gl = 2 Lambda - (3/8) P^2 (P = (2/3) <h_ij pi^ij>/<sqrt h> = {sp.simplify(Pgt)}) vanishes at K = {gt}")
check("A2 K_inf AND THE VACUUM: a constant matter vacuum energy is absorbed into HT's Lambda by the field redefinition Lambda' = "
      "Lambda + 8 pi G rho_vac, which changes the action by -16 pi G rho_vac d_m T^m (a total derivative: identical field equations); so "
      "whether alpha reads Lambda or Lambda_obs = Lambda' (= K_inf^2/3, what K_inf sees) is a CHOICE in the action, not new physics -- "
      "XR20 T1e's caveat is that choice.  The leading large-volume global Hamiltonian of unimodular shape dynamics, 2 Lambda - (3/8) P^2, "
      "vanishes exactly at K = sqrt(3 Lambda)", f"total derivative {all(e_ == 0 for e_ in el_diff)}; H_gl root K = {gt}", a2_ok)
# A3: the local York time is exactly leaf-uniform on the CMC root, whatever else the action contains
NA = 4
vA = sp.symbols(f'v0:{NA}', positive=True); NA_ = sp.symbols(f'N0:{NA}', positive=True); vdA = sp.symbols(f'vd0:{NA}'); muA = sp.symbols(f'mu0:{NA}')
KA = [vdA[i] / (NA_[i] * vA[i]) for i in range(NA)]
KbA = sum(vdA[i] / NA_[i] for i in range(NA)) / sum(vA)
Wf = sp.Function('W')
L_A3 = sum(NA_[i] * vA[i] * (-2 * muA[i] * (KA[i] - KbA) + Wf(KA[i], vA[i], NA_[i])) for i in range(NA))   # W: anything, K-dependent too
a3 = [sp.simplify(sp.diff(L_A3, muA[i]) + 2 * NA_[i] * vA[i] * (KA[i] - KbA)) for i in range(NA)]
check("A3 THE LOCAL YORK TIME IS EXACTLY LEAF-UNIFORM ON THE CMC ROOT: mu appears only in the CMC term, so its equation is "
      "N sqrt(h)(K - <K>) = 0 whatever else the action contains (a K-dependent MOND coupling included): a tie to the local K has NO "
      "local variation on FP14's root (XR20 T3c's estimate scales to zero exactly), and fails only through K(z) = 3 H(z)/c",
      f"dL/dmu_j + 2 N_j v_j (K_j - <K>) = {a3}", all(e_ == 0 for e_ in a3))

# ================================================================================================ HEADLINE-FLAT
banner("HEADLINE-FLAT  the tie on the combined root's FRW solutions" + ("  [MUTATE: the tie reads the leaf's York time K(z)]" if MUTATE else ""))
import mpmath as mpm
mpm.mp.dps = 50
H0m, OMm, OLm, cm = mpm.mpf(H0_KMS) * 1000 / mpm.mpf(MPC), mpm.mpf('0.3153'), mpm.mpf('0.6847'), mpm.mpf(c_SI)
Gm = mpm.mpf(G_SI)
rho_cm = 3 * H0m ** 2 / (8 * mpm.pi * Gm)
LAMm = 8 * mpm.pi * Gm * OLm * rho_cm / cm ** 2
Kz = lambda z: 3 * H0m * mpm.sqrt(OMm * (1 + z) ** 3 + OLm) / cm                      # the CMC leaf value on the root's FRW (= GR + Lambda_0)
rhom = lambda z: OMm * rho_cm * (1 + z) ** 3
Qz = lambda z: Kz(z) ** 2 / 3 - 8 * mpm.pi * Gm * rhom(z) / cm ** 2                # the conserved combination (M2): Lambda_0 on shell
zs_h = [0.0] + ZS
a0z = {}
for foot in A0:
    if not MUTATE:
        a0z[foot] = {z: float(mpm.mpf(A0[foot]) * mpm.sqrt(Qz(z) / Qz(0))) for z in zs_h}
    else:
        a0z[foot] = {z: float(mpm.mpf(A0[foot]) * Kz(z) / Kz(0)) for z in zs_h}
ratio = {foot: {z: a0z[foot][z] / a0z[foot][0.0] for z in zs_h} for foot in A0}
Qdev = max(abs(float(Qz(z) / LAMm) - 1) for z in zs_h)
flat_ok = all(abs(ratio[f][z] - 1) < 1e-12 for f in A0 for z in zs_h) and all(abs(a0z[f][0.0] / A0[f] - 1) < 1e-12 for f in A0)
for foot in A0:
    P(f"    {foot:9s} a0(z)/a0(0) at z = 0.5, 1, 2.5, 5, 1100: " + ", ".join(f"{ratio[foot][z]:.6f}" for z in ZS)
      + f"  (a0(0) = {a0z[foot][0.0]:.6e})")
P(f"    Q(z) = K(z)^2/3 - 8 pi G rho_m(z) against Lambda_0 over z = 0..1100: max |Q/Lambda - 1| = {Qdev:.1e} (50-digit arithmetic)")
check("HEADLINE-FLAT the tie read from the conserved combination of the CMC leaf data, Q = K^2/3 - 8 pi G rho_m (= Lambda_0 = K_inf^2/3 on "
      "shell, the global constraint's value): a0(z)/a0(0) = 1 at z = 0.5, 1, 2.5, 5, 1100 on both footings, to 1e-12, and uniform on "
      "every leaf (a leaf-global quantity)",
      "; ".join(f"{f}: " + ", ".join(f"{ratio[f][z]:.6f}" for z in ZS) for f in A0), flat_ok,
      "the tie survives through the conserved Lambda_0, which K_inf merely re-expresses" if not MUTATE else
      "MUTATE: reading the York clock K(z) alone ties a0 to the expansion rate -- the rival a0 proportional to H(z), XR20 T3")
OUT["numbers"]["headline"] = dict(ratio={f: {str(z): v for z, v in r_.items()} for f, r_ in ratio.items()},
                                  a0={f: {str(z): v for z, v in r_.items()} for f, r_ in a0z.items()}, Q_dev=Qdev)

# ================================================================================================ W ledger
banner("W   THE LEDGER")
ledger = [
    ("X30-merge", "the khronon's CMC foliation and the HT unimodular clock CANNOT be merged into one term: the CMC family is local and "
     "second class with a pure-gauge global part; HT's local family is first class and its content is one global conserved pair; "
     "a conserved momentum cannot be the York clock (dK/dt = -12 pi G rho_m)", "DERIVED", "M1, M2, D1-D3, L1-L4"),
    ("X30-fol", "'the HT time's foliation is the khronon's' holds only as a relabeling: HT has no foliation (3-form gauge, Kuchar's "
     "equivalence classes); T - tau is an admissible gauge for the khronon's global reparametrization", "DERIVED", "M5, D3"),
    ("X30-MB", "the only one-term merger that keeps both local structures, 2 f(K)(d_m T^m - sqrt(-g)), is FP14's multiplier at k != 0 "
     "but freezes York time: H(z) = const for any dust", "FAILS (FRW)", "M3, L2, D1, D3"),
    ("X30-MA", "T^m = l sqrt(-g) n^m (the linear-cuscuton form): K pinned to 1/l (new constant), Lambda(t) drifts to zero at z = 0.47",
     "FAILS", "M4"),
    ("X30-MC", "mu = beta sqrt(Lambda) (new constant): the CMC condition is lost, the khronon frozen (FP14's c_2 = 0 block)", "FAILS", "L3"),
    ("X30-SQ", "one global multiplier on Int N sqrt(h)(K - <K>)^2: irregular (no reaction force, c_2 returns undetermined, the scalar "
     "mode and time-dependent sources excluded)", "FAILS", "L4"),
    ("X30-count", "the combined root: FP14's local count (2 tensor + 1 khronon scalar at lambda = 0; det x -4) + ONE global pair "
     "(Lambda_0, T); lattice: 2 N_L vs 2 N_L - 2 without HT; classes as D2", "DERIVED", "L1, D1, D2"),
    ("X30-global", "on the khronon's leaves one global pair 2 Lambda_0 (T-dot - Int N sqrt(h)) does everything the local HT fields do "
     "(same count; the MOND sector feeds its clock)", "DERIVED", "D1 (globalHT), D1m"),
    ("X30-kill", "with HT added, FRW growth (G_eff/G = 2/(2 - alpha_c), no slip), the static Newtonian coupling (not 2G) and every "
     "response FP14 C2 scored are unchanged: the York/CMC kill stays evaded; PPN unchanged (HT is metric-free, XR20 T1d)",
     "DERIVED", "F1, L1, C2, C3"),
    ("X30-a0", "a0 stays TIED through the conserved Lambda_0 (= Q = K_inf^2/3 on shell); the K_inf reading is T1 re-expressed, not a "
     "new tie; the local York time is exactly leaf-uniform on the CMC root but gives the rival a0(z) ~ H(z)", "TIED (as XR20 T1)",
     "A1-A3, HEADLINE-FLAT; kappa FITTED"),
    ("X30-foot", "canonical a0 = (kappa/sqrt(24 pi)) c^2 K_inf and alt a0 = the same coefficient on K_0 = 3 H_0/c (an identity)",
     "IDENTITY", "A1"),
    ("X30-vac", "XR20 T1e's vacuum caveat is a choice of which variable alpha reads (the shift is a total derivative)", "READING", "A2"),
]
for row in ledger:
    OUT["ledger"].append(dict(id=row[0], claim=row[1], status=row[2], evidence=row[3]))
    P(f"    {row[0]:10s} {row[2]:18s} {row[1]}  --  {row[3]}")

# ================================================================================================ verdict
banner("VERDICT")
P("  NO MERGE.  The CMC foliation and the unimodular clock are two structures, and they fit together rather than fuse:\n"
  "  - the CMC multiplier is a LOCAL second-class constraint family whose global part is pure gauge (mu N -> mu N + c(t));\n"
  "  - HT's local constraints are first class (gauge) and its content is ONE global pair (Lambda_0, T), which on the khronon's\n"
  "    leaves can be written as a single global term; T labels the CMC leaves (a gauge choice), it defines none (Kuchar 1991);\n"
  "  - every single-term merger fails: Lambda == f(K) freezes York time (H(z) = const), the flux form pins K = 1/l and lets Lambda\n"
  "    drift, mu == beta sqrt(Lambda) loses the CMC condition and freezes the khronon, and one global squared constraint is irregular.\n"
  "  Combined (not merged): FP14's local count + one global pair; FRW growth, the static coupling and the York/CMC evasion unchanged.\n"
  "  The a0 tie stays XR20's T1: a0 reads the conserved Lambda_0 = K_inf^2/3; K_inf adds nothing new, and the local York time gives\n"
  "  the rival a0 ~ H(z).  The literature's 'unimodular shape dynamics' (Gryb-Thebault 2012) is the same pairing.\n"
  "  kappa = 1/2 stays FITTED; nothing here derives it.  The closure target stays open.")
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; time {time.time() - T_START:.0f} s")
OUT["verdict"] = dict(pass_=sum(1 for _, ok, _ in CH if ok), total=len(CH), load_bearing_failures=nlb, time_s=time.time() - T_START)
json.dump(OUT, open(JSN, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(JSN)} and {os.path.basename(TXT)}")
TEE.flush(); sys.stdout = sys.__stdout__; TEE.close()
sys.exit(1 if nlb else 0)
