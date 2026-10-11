"""CFG591 library (FROZEN_CRITERIA.md section 1): the CFG556 halo-model namespace at observation epoch z, and CFG557's alpha-free
finite-age supply ceiling s_c*(M_ta, z) on that epoch's halo grid.

CFG556's source is exec'd read-only up to its run block; ONLY the epoch inputs are overridden (linear amplitude D(z)^2, Tinker08
z-evolution, Duffy08 (1+z)^-1.01, Delta_ta(z), 200 rho_crit(z) for r200c, Moster13 z-evolution, a0 -> a0/(1+z)^2 in comoving units so
r_M, r_e and y are the physical ones).  CFG557's frame_profile_sc and CFG559's frame_profile_kin are exec'd verbatim (source text
extracted from cfg559_tests.py) in the same namespace.  Lengths comoving Mpc/h, k comoving h/Mpc, rho_m comoving.
kappa = 1/2 FITTED; footings never pooled; flat a0 (w = -1: a0 the same at every z); cold energy mass required; not theory closed."""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
D557 = os.path.join(LANES, "CFG557_settling_catchment_derived")
D559 = os.path.join(LANES, "CFG559_kinetic_settled_profile")
for _p in (D557, D559):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import cfg557_lib as L          # noqa: E402
import cfg559_lib as K9         # noqa: E402
A0_BASE = dict(L.A0MPC)

ZNODES = [0.0, 0.25, 0.5, 0.75, 1.0]
FOOTS = ("canonical", "alt")
P556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
P559T = os.path.join(D559, "cfg559_tests.py")
JD = json.load(open(os.path.join(D557, "cfg557_derive_results.json")))

DE = None          # None = w = -1 (frozen primary); dict(w0=, wa=) = ADDENDUM 1 DESI-tracking variant (set by cfg591_desi.activate)
def fDE(z):
    """rho_DE(z)/rho_DE(0); 1 for the primary."""
    if DE is None:
        return 1.0
    w0, wa = DE["w0"], DE["wa"]
    return (1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))

_EP = {}
def epoch(z):
    if z not in _EP:
        _EP[z] = L.Epoch(z)
    return _EP[z]
DODE0 = None
def delta_ta(z):
    """Delta_ta(z) = 11.81 x Delta_ODE(z) / Delta_ODE(0) (anchored to CFG556's z = 0 value)."""
    global DODE0
    if DODE0 is None:
        DODE0 = epoch(0.0).Delta_ta
    return 11.81 * epoch(z).Delta_ta / DODE0, epoch(z).Delta_ta


def namespace(z):
    """CFG556 namespace at epoch z with the frame_profile_sc / frame_profile_kin sources exec'd in it."""
    src = open(P556).read(); cut = src.index("# ------------------------------------------------------------------ run")
    H = {"__file__": P556, "__name__": "cfg556_ro_z"}
    _e = os.environ.pop("CFG556_MUTATE", None)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:cut], "cfg556_ro", "exec"), H)
    if _e is not None:
        os.environ["CFG556_MUTATE"] = _e
    a = 1.0 / (1.0 + z); zp = 1.0 + z
    Om, OL = H["Om"], 1.0 - H["Om"]
    # --- linear amplitude
    Dz = L.Dgrow(a) / L.Dgrow(1.0)
    H["_PK"] = H["_PK"] * Dz ** 2
    # --- sigma(M, z), Tinker08 z-evolution, Tinker10 bias
    SIG = H["sigma_R"](H["RM"]); LM = H["LM"]; MM = H["MM"]; RHO_M = H["RHO_M"]; DC = H["DC"]
    dlns = np.gradient(np.log(SIG), LM * math.log(10))
    alpha_b = 10 ** (-(0.75 / math.log10(200.0 / 75.0)) ** 1.2)
    At, at, bt = 0.186 * zp ** -0.14, 1.47 * zp ** -0.06, 2.57 * zp ** -alpha_b
    fT = At * ((SIG / bt) ** -at + 1) * np.exp(-1.19 / SIG ** 2)
    NDLNM = fT * RHO_M / MM * (-dlns)
    NUP = DC / SIG
    A10, a10, B10, b10, C10, c10 = (H[k] for k in ("A10", "a10", "B10", "b10", "C10", "c10"))
    BIAS = 1 - A10 * NUP ** a10 / (NUP ** a10 + DC ** a10) + B10 * NUP ** b10 + C10 * NUP ** c10
    W_M = NDLNM * H["DLM"]
    A_MISS = 1.0 - float(np.sum(W_M * BIAS * MM)) / RHO_M
    H.update(SIG=SIG, dlns=dlns, fT=fT, NDLNM=NDLNM, NUP=NUP, BIAS=BIAS, W_M=W_M, A_MISS=A_MISS)
    # --- concentration, Delta_ta, r200c at 200 rho_crit(z), Moster13(z), a0 in comoving units
    DTA, DODE = delta_ta(z)
    Omz = Om * zp ** 3 / (Om * zp ** 3 + OL * fDE(z))
    m_nfw = H["m_nfw"]; r200m = H["r200m"]
    def conc(M): return 10.14 * (M / 2e12) ** -0.081 * zp ** -1.01
    def halo_basics(M):
        c = conc(M); r2 = r200m(M); mc = m_nfw(c)
        xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - DTA / 200.0, 1.0, 50.0, xtol=1e-12)
        xc = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - 1.0 / Omz, 0.05, 1.0, xtol=1e-12)
        return dict(M=M, c=c, r200=r2, rs=r2 / c, mc=mc, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc, r200c=xc * r2, M200c=M * m_nfw(c * xc) / mc)
    zz = z / (1.0 + z); hh = H["h"]
    def mstar(hb):
        M = hb["M200c"] / hh; M1 = 10 ** (11.590 + 1.195 * zz)
        N, be, ga = 0.0351 - 0.0247 * zz, 1.376 - 0.826 * zz, 0.608 + 0.329 * zz
        ms = M * 2 * N / ((M / M1) ** -be + (M / M1) ** ga)
        return ms * hh
    H["A0MPC_PHYS"] = dict(H["A0MPC"])
    if DE is not None:                                   # ADDENDUM 1: a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE(0))
        H["A0MPC_PHYS"] = {f: v * math.sqrt(fDE(z)) for f, v in H["A0MPC_PHYS"].items()}
    H["A0MPC"] = {f: v / zp ** 2 for f, v in H["A0MPC_PHYS"].items()}
    H.update(conc=conc, halo_basics=halo_basics, mstar=mstar, DTA=DTA, Omz=Omz)
    HB = [halo_basics(M) for M in MM]
    H["HB"] = HB; H["MTA"] = np.array([hb["Mta"] for hb in HB]); H["PL"] = H["P_lin"](H["KK"])
    H["NORM_TA"] = float(np.sum(W_M * BIAS * H["MTA"])) / RHO_M
    H.update(Z=z, Dz=Dz, Delta_ODE=DODE, alpha_b=alpha_b)
    # --- CFG557 frame_profile_sc + CFG559 frame_profile_kin, verbatim source from cfg559_tests.py
    t = open(P559T).read(); i0 = t.index("def frame_profile_sc"); i1 = t.index("\nUstd = U_std()")
    H["K9"] = K9
    exec(compile(t[i0:i1], "cfg559_tests_frame_profiles", "exec"), H)
    return H


def sc_grid(H, foot, z):
    """CFG557 alpha-free free-fall ceiling s_c* on the epoch grid (census baryons); z = 0 -> CFG557's stored grid."""
    if z == 0.0 and DE is None:
        g = JD["grid"][foot]
        assert np.allclose(g["log10_Mta"], np.log10(H["MTA"]), atol=1e-10, rtol=0)
        return np.array(g["ff"], float)
    return sc_grid_compute(H, foot, z)


def sc_grid_compute(H, foot, z):
    E = epoch(z); out = []
    base = dict(A0_BASE)
    L.A0MPC = {f: v * math.sqrt(fDE(z)) for f, v in base.items()}
    for hb in H["HB"]:
        Mta = hb["Mta"]; f = L.fret_of(math.log10(Mta)); Mb = f * L.FB * Mta
        out.append(L.s_catch(E, Mta, Mb, foot, math.inf, mah=E.mah(Mta)))
    L.A0MPC = base
    return np.array(out)
