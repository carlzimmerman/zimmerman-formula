#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AT1 -- THE ACCELERATION-TRIGGERED CARRIER: the carrier converts where the MOND kernel's own argument is large.  Built on
the halo model, scored at high z (the flagship and RC100), with its decay budget handed to AT2's forest test.

WHY.  Every carrier window on the record fails at high z.  GP5 (70d8070c0) and L356: a carrier still inside galaxies at
z ~ 2.5 moves the flagship deep-MOND Tully-Fisher zero point by +0.82..+1.05 dex (framework 0.00, LCDM +0.33).  L357's
density (virialization) trigger clears galaxies, but as a local trigger it fires in every halo down to 1e8 Msun (its V1).
The vacuum gate that rescued it keeps z >= 2 halos intact, which is GP5's failure again.  What is needed is a trigger that
is MASS-SELECTIVE at high z: it fires in galaxies, not in the web or in minihalos.

THE CONSTRUCTION (a construction: the rule is put in by hand, like every decay channel on the record).
  The carrier X is kernel-invisible (L353): a state of the framework's own field, not a new particle species; the MASS is
  still required.  X converts to a kicked state Y where the kernel's own argument exceeds a threshold y_v.  That argument
  is the bound region's baryonic Newtonian acceleration y_b = |grad w|/a0 (L361):
      Gamma = Gamma_0 Theta(y_b - y_v),   Gamma_0 >> 1/t_dyn,   isotropic kick v_A.
  Because Gamma_0 is fast, a carrier element converts the first time its orbit enters r_v, the radius where y_b = y_v.  In
  steady state this empties the whole LOSS CONE (every orbit with pericentre < r_v), not just the mass inside r_v.  The
  daughter is born at r_v with its orbit's speed there plus the kick.  y_b reaches y_v only where baryons have condensed
  (discs, BCGs, group gas), never in minihalos whose gas stays diffuse: the kernel's own variable supplies the mass
  selection, with no resolution scale.  y_v = 1 (the kernel's own Newtonian/MOND transition) adds no constant; any other
  y_v is one new constant.

METHOD (machinery loaded unedited from committed lanes; three pieces added).
  * Baryons of a halo (added): Moster+13 stellar mass (L320's function) with L356's cold-gas ratio mu = 0.5((1+z)/2)^2
    (x 1/1.5..1.5), in a Hernquist sphere of half-mass radius R_e (van der Wel+14, late types).  The diffuse halo gas is
    left out.  It only raises y_b, so every trigger radius here is a lower bound.
  * Carrier orbits (added): isotropic Jeans NFW (Dutton-Maccio c(M,z); L321's sampling).  The steady-state loss cone and
    the escape fraction of daughters kicked at r_v are tabulated by Monte Carlo on the truncated NFW, V200 = r200 = 1, as
    L357's esc().
  * Retention (added, from L321's pieces): L321/L357's phase-mixed retention (its potential(), frac_inside(), sampling and
    draw order), with decay on entry into r_v.  With r_v -> infinity it IS L321's retained(fd = 1) (control C3).
  * Halo model, L319's linear solver (L357's head, unedited): Sheth-Tormen mass function and bias; the decayed fraction
    that matters for large-scale power is bias-weighted and counts only escaped daughters.
  * The flagship (GP5's definition, unedited: outer radius g_bar = 0.1 a0, Moster-calibrated halos, L320's g_nfw, both
    kernels, both footings, M_b 1e10-1e11, L356's gas range) and RC100 (L320's 100 galaxies, L357 H1's formulas).
GATES (from the record): the flagship |shift| <= 0.10 dex (GP5 F1); L319's forest proxy T^2(k = 5 h/Mpc) at z = 2 and 3,
  >= 0.9952 strict / 0.9 loose (the forest gate of L319/L354/L357/L372/GP4).  The PROXY is a statement about the MATTER power.
  L365's particle-mesh runs show the forest's FLUX power moving <= 1% at z = 3 and <= 5% at z = 2.  In the same runs,
  15-27% of the carrier decays from dense regions, which on the proxy is ~50% of the matter power.  So the forest verdict
  on this carrier is AT2's: the flux observable in the record's particle-mesh machinery, with a relic calibration.
CHECKS
  C1 CONTROL: the loss-cone and escape tables agree with an independent direct Monte Carlo (new seed) at three test points.
  C2 CONTROL: with the carrier retained (GP5's r), the flagship grid reproduces GP5's committed shifts at z = 2.5.
  C3 CONTROL: retained_acc with r_v -> infinity equals L321's retained(fd = 1) to machine precision (identical draws).
  A1 MASS SELECTIVITY: at z = 2 and 3, y_v >= 0.1, both footings, >= 95% of the triggered carrier sits in halos
     >= 1e10.5 Msun; L357's density trigger at its natural threshold (x_v = 30) puts far more below that mass (reported).
  A2 THE FLAGSHIP BY CONSTRUCTION: y_v <= 0.1 with v_A >= 600 km/s keeps the flagship within 0.10 dex at z = 2.5 over
     GP5's full grid (M_b 1e10-1e11, both footings, L356's gas range, both kernels), and at z = 0.5, 1, 1.5, 2.
  A3 THE MATTER PROXY'S PRICE: the A2 cell (y_v = 0.1, v_A = 600) fails L319's proxy even loose.  So does the
     trigger-independent minimum: the optimal removal that clears GP5's flagship population (M_b >= 1e10 at z = 2.5, each
     halo cut to GP5's gate), at every daughter speed 600-3000 km/s (the speeds at which removal clears the flagship
     radius: S1 finds 450 km/s leaves +0.12..+0.21 dex).
  S1 (reported) the design scan: flagship at z = 2.5 and the proxy over (y_v, v_A).
  R1 (reported) RC100 for the natural cell y_v = 1 and the A2 cell.
  B1 (reported) the decay budget F(z) (unweighted triggered, and bias-weighted escaped) handed to AT2.
MUTATE=1: every kick is 0 (the daughter stays on its parent's orbit: a relabelling).  A2 must fail (the flagship keeps its
carrier) and A3 must fail (with no free streaming the proxy costs nothing): rc = 1.

Run from the repository root:  python3 real_research/acceleration_trigger_2026/AT1_acceleration_trigger_highz.py
"""
import os, sys, json, math, time, io, contextlib, warnings
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy.interpolate import RegularGridInterpolator
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "AT1_acceleration_trigger_highz"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "AT1", "mutate": MUTATE, "checks": {}, "numbers": {}}
NTH = int(os.environ.get("AT1_THREADS", "8"))
FAST = os.environ.get("FAST", "0") == "1"                             # smoke test only; never committed


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: every kick is 0 (a relabelling) -- A2 and A3 must FAIL ***")
KMUL = 0.0 if MUTATE else 1.0                                        # multiplies every daughter speed

# ------------------------------------------------------------------------------------------------ L357's head, unedited
P57 = os.path.join(REPO, "real_research", "dark_sector_2026", "L357_virialization_triggered_carrier.py")
_s57 = open(P57).read()
_head57 = _s57.split("# ================================================================================ CONTROLS")[0]
_head57 = _head57.replace('P(__doc__.split("METHOD")[0].strip())', "pass")
os.environ["L357_THREADS"] = "4"
_mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"      # the loaded lane's own MUTATE stays off
L57 = {"__name__": "l357", "__file__": P57}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_head57, L57)
os.environ["MUTATE"] = _mut
h, Om = L57["h"], L57["Om"]
MH, LGM, SIG0, DG, f_st, b_st, DC = L57["MH"], L57["LGM"], L57["SIG0"], L57["DG"], L57["f_st"], L57["b_st"], L57["DC"]
mfn, c_dm14, GK, RHOC0_KPC, Ez2 = L57["mfn"], L57["c_dm14"], L57["GK"], L57["RHOC0_KPC"], L57["Ez2"]
solve_hist, ZG, a_grid, T2_53, _trap, trig57 = L57["solve_hist"], L57["ZG"], L57["a_grid"], L57["T2_53"], L57["_trap"], L57["trig"]
Lm = L57["Lm"]
potential, frac_inside, RG, FB, nfw21, hernquist = Lm["potential"], Lm["frac_inside"], Lm["RG"], Lm["FB"], Lm["nfw"], Lm["hernquist"]
retained_L321 = Lm["retained"]
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KPC_M = 3.0856775814913673e19
A0K = {f_: v_ * KPC_M / 1e6 for f_, v_ in FOOT.items()}              # (km/s)^2 / kpc
P(f"  L357 head loaded (L319 solver, halo model, L321 retention); strict forest proxy threshold {T2_53:.4f}   [{time.time()-T0:.0f}s]")

# ------------------------------------------------------------------------------------------------ L320's top, unedited (as GP5)
P20 = os.path.join(REPO, "real_research", "dark_sector_2026", "L320_carrier_highz_price_rc100.py")
L20 = {"__name__": "l320", "__file__": P20}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P20).read().split("# ------------------------------------------------------------------------------------------------ models")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), L20)
halo_mass, g_nfw, c200_20, nu20, invert, slope_boot = L20["halo_mass"], L20["g_nfw"], L20["c200"], L20["nu"], L20["invert"], L20["slope_boot"]
mstar_over_mh, GAL100, G20, MSUN, KPC = L20["mstar_over_mh"], L20["gal"], L20["G"], L20["MSUN"], L20["KPC"]
_B = {"__name__": "bk1", "__file__": os.path.join(REPO, "real_research", "blind_kernel_2026", "BK1_screened_kernel.py")}
_bs = open(_B["__file__"]).read().split("# ------------------------------------------------------------------ linear LCDM")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(_bs.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), _B)
nu_mono = lambda x: float(_B["nu_mono_arr"](np.array([x]))[0])
P(f"  L320 loaded ({len(GAL100)} RC100 galaxies) and BK1's nu_mono (GP5's second kernel)   [{time.time()-T0:.0f}s]")

# ------------------------------------------------------------------------------------------------ baryons of a halo (added)
VDW = np.array([[0.25, 0.86, 0.25], [0.75, 0.78, 0.22], [1.25, 0.70, 0.22], [1.75, 0.65, 0.23], [2.25, 0.55, 0.22],
                [2.75, 0.51, 0.18]])                                 # van der Wel+14 Table 1, late types: z, log A [kpc], alpha


def Re_kpc(Ms, z):
    """half-mass (projected ~ half-light) radius, R_e = A (M*/5e10)^alpha; beyond z = 2.75 A ~ (1+z)^-0.75 (their fit)."""
    if z <= 2.75:
        la = float(np.interp(z, VDW[:, 0], VDW[:, 1])); al = float(np.interp(z, VDW[:, 0], VDW[:, 2]))
    else:
        la = 0.51 - 0.75 * math.log10((1 + z) / 3.75); al = 0.18
    return 10 ** la * (Ms / 5e10) ** al


def mu_gas(z, fac=1.0):
    return fac * 0.5 * ((1 + z) / 2) ** 2                            # L356's cold-gas-to-star ratio


def galaxy_baryons(Mh, z, mufac=1.0):
    Ms = Mh * mstar_over_mh(Mh, z); Mb = (1 + mu_gas(z, mufac)) * Ms
    return Mb, Re_kpc(Ms, z) / 1.8153                                # Hernquist a = R_e / 1.8153


def r_trigger(Mb, a, yv, a0k):
    """outermost radius [kpc] where the Hernquist sphere's y_b = G M(<r) / (r^2 a0) >= y_v (y_b falls monotonically)."""
    if yv <= 0: return np.inf
    if GK * Mb / a ** 2 / a0k < yv: return 0.0                     # the centre never reaches y_v
    # G Mb / (r + a)^2 = yv a0  ->  r = sqrt(G Mb / (yv a0)) - a
    return max(math.sqrt(GK * Mb / (yv * a0k)) - a, 0.0)


# ------------------------------------------------------------------------------------------------ NFW loss cone + escape (added)
def nfw_phi(x, c):                                                   # truncated NFW, V200 = r200 = 1 (as L357's esc)
    y = np.maximum(x * c, 1e-9); m_c = math.log(1 + c) - c / (1 + c)
    inside = -np.log1p(y) / (np.maximum(x, 1e-12) * m_c) + math.log(1 + c) / m_c - 1.0
    return np.where(x < 1, inside, -1.0 / np.maximum(x, 1e-12))


CG = np.geomspace(2.0, 40.0, 14); XVG = np.geomspace(1e-3, 1.0, 50); UGR = np.linspace(0.0, 8.0, 41)


def lc_draw(c, N, rng):
    m_c = math.log(1 + c) - c / (1 + c)
    M = lambda x: (np.log1p(x * c) - x * c / (1 + x * c)) / m_c
    xg = np.geomspace(1e-5, 1.0, 3000)
    x = np.interp(rng.random(N), M(xg), xg)
    rho = 1.0 / (xg * c * (1 + xg * c) ** 2); gm = M(xg) / xg ** 2
    integ = rho * gm; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(xg)
    s2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / rho
    v = rng.normal(0, 1, (N, 3)) * np.sqrt(np.interp(x, xg, s2))[:, None]
    L = x * np.linalg.norm(v[:, 1:], axis=1); E = 0.5 * (v ** 2).sum(1) + nfw_phi(x, c)
    xs = np.geomspace(1e-5, 1.0, 1500); ph = nfw_phi(xs, c)
    ok = (2 * (E[:, None] - ph[None, :]) * xs[None, :] ** 2 - L[:, None] ** 2) >= 0
    rp = np.minimum(xs[np.argmax(ok, axis=1)], x)
    return x, E, rp


def lc_escape(c, xv, u, x, E, rp):
    lc = rp < xv
    if not lc.any(): return 0.0, 0.0
    xb = np.where(x[lc] <= xv, x[lc], xv)                           # born on entry at xv (in place if the orbit lies inside)
    ve2 = np.maximum(2 * (E[lc] - nfw_phi(xb, c)), 1e-12); vesc2 = -2 * nfw_phi(xb, c)
    if u == 0: return float(lc.mean()), float(np.mean(ve2 > vesc2))
    t = (vesc2 - ve2 - u ** 2) / (2 * np.sqrt(ve2) * u)              # isotropic kick: P(cos theta > t)
    return float(lc.mean()), float(np.mean(np.clip((1 - t) / 2, 0, 1)))


_rng = np.random.default_rng(3)
FLC = np.zeros((len(CG), len(XVG))); FES = np.zeros((len(CG), len(XVG), len(UGR)))
for _ic, _c in enumerate(CG):
    _x, _E, _rp = lc_draw(_c, 30000, _rng)
    for _ixv, _xv in enumerate(XVG):
        for _iu, _u in enumerate(UGR):
            FLC[_ic, _ixv], FES[_ic, _ixv, _iu] = lc_escape(_c, _xv, _u, _x, _E, _rp)
I_LC = RegularGridInterpolator((np.log(CG), np.log(XVG)), FLC, bounds_error=False, fill_value=None)
I_ES = RegularGridInterpolator((np.log(CG), np.log(XVG), UGR), FES, bounds_error=False, fill_value=None)
P(f"  loss-cone and escape tables built (NFW, {len(CG)} x {len(XVG)} x {len(UGR)})   [{time.time()-T0:.0f}s]")


# ------------------------------------------------------------------------------------------------ halo model (L357's, one rule changed)
def trig_acc(z, yv, a0k, mufac=1.0):
    """per halo on L357's mass grid: loss-cone fraction f_lc, x_v = r_v/r200, c, V200 [km/s]."""
    Mh = MH / h; cs = c_dm14(MH, z)
    r200 = (3 * Mh / (4 * np.pi * 200 * RHOC0_KPC * Ez2(z))) ** (1 / 3); V200 = np.sqrt(GK * Mh / r200)
    xv = np.zeros(len(MH))
    for i in range(len(MH)):
        Mb, a = galaxy_baryons(Mh[i], z, mufac)
        xv[i] = min(r_trigger(Mb, a, yv, a0k) / r200[i], 1.0)
    lc = np.where(xv > 0, I_LC(np.stack([np.log(np.clip(cs, CG[0], CG[-1])), np.log(np.maximum(xv, XVG[0]))], 1)), 0.0)
    return np.clip(lc, 0, 1), xv, cs, V200


def F_acc(z, yv, vk, a0k, mufac=1.0, weight="bias", escaped=True):
    s = SIG0 * DG(z); nu = DC / s
    w = f_st(nu) * np.abs(np.gradient(nu, np.log(MH)))
    lc, xv, cs, V200 = trig_acc(z, yv, a0k, mufac)
    if escaped:
        u = np.clip(vk / V200, 0, UGR[-1])
        fe = np.where(xv > 0, I_ES(np.stack([np.log(np.clip(cs, CG[0], CG[-1])), np.log(np.maximum(xv, XVG[0])), u], 1)), 0.0)
    else:
        fe = np.ones(len(MH))
    wb = w * (b_st(nu) if weight == "bias" else 1.0)
    return float(_trap(wb * lc * np.clip(fe, 0, 1), np.log(MH)))


def history_acc(yv, vk, a0k, mufac=1.0, weight="bias", escaped=True):
    Fz = np.array([F_acc(z, yv, vk, a0k, mufac, weight, escaped) for z in ZG])
    assert np.all(np.isfinite(Fz))
    Fz = np.where(Fz < 1e-10, 0.0, Fz)
    Fc = np.maximum.accumulate(Fz[::-1])[::-1]                         # irreversible
    return 1 - np.interp(1 / a_grid - 1, ZG, Fc, right=0.0), Fc


# ------------------------------------------------------------------------------------------------ retention with decay on entry (added)
RGc = np.geomspace(RG[0], RG[-1], 700)


def retained_acc(Mb_fn, M200, c, gates, rv, vk, rhoc, N=10000, seed=5, iters=2):
    N = min(N, 1500) if FAST else N
    """L321's retained() with decay on ENTRY into r_v (steady-state loss cone): retained carrier inside each gate radius,
    relative to the no-decay control on identical draws.  r_v = inf decays every particle in place (= L321, fd = 1)."""
    Mn, r200, rs = nfw21(M200, c, rhoc)
    Mc0 = lambda x: (1 - FB) * Mn(np.minimum(x, r200))
    rng = np.random.default_rng(seed)
    u = rng.random(N) * float(Mc0(r200)); rgrid = np.geomspace(1e-3 * rs, r200, 5000)
    r = np.interp(u, Mc0(rgrid), rgrid); w = float(Mc0(r200)) / N
    g_pre, Phi0 = potential(Mb_fn, Mc0, 0.0, "newtonian")
    rho = np.where(RG < r200, 1.0 / ((RG / rs) * (1 + RG / rs) ** 2), 1e-300)
    integ = rho * g_pre; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    sig2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / np.maximum(rho, 1e-300)
    sig = np.sqrt(np.interp(r, RG, sig2))
    v = rng.normal(0, 1, (N, 3)) * sig[:, None]
    _ = rng.random(N)                                                 # L321's is_d draw (keeps the draw order identical)
    nh = rng.normal(0, 1, (N, 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
    vrad0, vtan0 = v[:, 0], np.linalg.norm(v[:, 1:], axis=1); L0 = r * vtan0
    E0 = 0.5 * (vrad0 ** 2 + vtan0 ** 2) + np.interp(r, RG, Phi0)
    if np.isfinite(rv):
        ph = np.interp(RGc, RG, Phi0)
        ok = (2 * (E0[:, None] - ph[None, :]) * RGc[None, :] ** 2 - L0[:, None] ** 2) >= 0
        rp = np.minimum(RGc[np.argmax(ok, axis=1)], r)
        lc = rp < rv; entry = lc & (r > rv)
    else:
        lc = np.ones(N, bool); entry = np.zeros(N, bool)
    pos_d = np.where(entry, rv if np.isfinite(rv) else 0.0, r)
    vb2 = np.maximum(2 * (E0 - np.interp(pos_d, RG, Phi0)), 0.0)
    vt_e = np.where(entry, L0 / np.maximum(pos_d, 1e-30), 0.0)
    vr_e = -np.sqrt(np.maximum(vb2 - vt_e ** 2, 0.0))
    vvec = np.where(entry[:, None], np.stack([vr_e, vt_e, np.zeros(N)], 1), v)   # in-place decays keep L321's full vector
    vvec = vvec + (lc * vk)[:, None] * nh

    def mass_in(dec):
        pos = pos_d if dec else r
        vv = vvec if dec else v
        vr_, vt_ = vv[:, 0], np.linalg.norm(vv[:, 1:], axis=1); L = pos * vt_
        Mc = Mc0
        for _ in range(iters):
            _, Phi = potential(Mb_fn, Mc, 0.0, "newtonian")
            E = 0.5 * (vr_ ** 2 + vt_ ** 2) + np.interp(pos, RG, Phi)
            probe = np.geomspace(0.02 * rs, 3 * r200, 24)
            prof = np.array([w * frac_inside(E, L, Phi, rg).sum() for rg in probe])
            Mc = (lambda pr=probe, pm=prof: (lambda x: np.interp(np.asarray(x, dtype=float), pr, pm, left=0.0)))()
        _, Phi = potential(Mb_fn, Mc, 0.0, "newtonian")
        E = 0.5 * (vr_ ** 2 + vt_ ** 2) + np.interp(pos, RG, Phi)
        return np.array([w * frac_inside(E, L, Phi, rg).sum() for rg in gates])

    m0 = mass_in(False); m1 = mass_in(True)
    return m1 / np.maximum(m0, 1e-300), float(lc.mean())


# ------------------------------------------------------------------------------------------------ the flagship (GP5's definition)
def flagship_rows(z, yv, vk, mufacs=(1 / 1.5, 1.0, 1.5), feet=("canonical", "alt"), lMbs=(10.0, 10.5, 11.0), ratio_override=None,
                  N=10000):
    """GP5's flagship grid with the carrier's retained fraction inside r_out from retained_acc (decay on entry)."""
    rows = []
    for foot in feet:
        a0 = FOOT[foot]; a0k = A0K[foot]
        for lMb in lMbs:
            Mb = 10 ** lMb
            r_out_m = math.sqrt(G20 * Mb * MSUN / (0.1 * a0)); r_out = r_out_m / KPC
            gb = G20 * Mb * MSUN / r_out_m ** 2
            for mf in mufacs:
                mu = mf * 0.5 * ((1 + z) / 2) ** 2
                Mh = halo_mass(Mb / (1 + mu), z); c = float(c200_20(Mh, z)); rhoc = RHOC0_KPC * Ez2(z)
                a = Re_kpc(Mb / (1 + mu), z) / 1.8153
                rv = r_trigger(Mb, a, yv, a0k)
                if ratio_override is not None:
                    ratio, flc = ratio_override, float("nan")
                else:
                    rr, flc = retained_acc(hernquist(Mb, a), Mh, c, [r_out], rv, vk, rhoc, N=N)
                    ratio = float(rr[0])
                gc = g_nfw(Mh, z, r_out_m) * ratio
                for kern, nuf in (("l320", nu20), ("mono", nu_mono)):
                    g_fw = float(nuf(gb / a0)) * gb
                    rows.append(dict(footing=foot, logMb=lMb, mu_fac=round(mf, 3), kernel=kern, r_out_kpc=r_out, r_v_kpc=rv,
                                     loss_cone=flc, retained=ratio, shift=2 * math.log10((g_fw + gc) / g_fw)))
    return rows


# ================================================================================================ C1-C3
banner("C1-C3  CONTROLS")
_rt = np.random.default_rng(99)
dev1 = []
for c_t, xv_t, u_t in ((4.0, 0.27, 2.5), (8.0, 0.08, 3.5), (15.0, 0.02, 5.0)):
    x_, E_, rp_ = lc_draw(c_t, 40000, _rt)
    lc_d, es_d = lc_escape(c_t, xv_t, u_t, x_, E_, rp_)
    lc_t = float(I_LC([[math.log(c_t), math.log(xv_t)]])[0]); es_t = float(I_ES([[math.log(c_t), math.log(xv_t), u_t]])[0])
    dev1.append(max(abs(lc_d - lc_t), abs(es_d - es_t)))
    P(f"    c {c_t:4.1f} x_v {xv_t:.2f} u {u_t:.1f}: loss cone table {lc_t:.3f} / direct {lc_d:.3f}; escape table {es_t:.3f} / direct {es_d:.3f}")
check("C1 CONTROL: the loss-cone and escape tables agree with an independent direct Monte Carlo (new seed, 40000 draws) "
      "within 0.02 at three test points", f"max |dev| {max(dev1):.4f}", max(dev1) < 0.02, load_bearing=False)
gp5 = json.load(open(os.path.join(REPO, "real_research", "generated_phantom_2026", "GP5_window_at_high_z_results.json")))["numbers"]["F"]
dev2 = []
for key in ("0.95|1200.0|2.5|l320", "0.9|1400.0|2.5|l320"):
    rows = [r_ for r_ in flagship_rows(2.5, 0.1, 0.0, ratio_override=gp5[key]["r"]) if r_["kernel"] == "l320"]
    dev2.append(max(abs(min(r_["shift"] for r_ in rows) - gp5[key]["shift_min"]), abs(max(r_["shift"] for r_ in rows) - gp5[key]["shift_max"])))
check("C2 CONTROL: with GP5's retained fraction the flagship grid reproduces GP5's committed z = 2.5 shifts (min and max, both "
      "window cells) to 1e-9 dex", f"max |dev| {max(dev2):.1e}", max(dev2) < 1e-9, load_bearing=False)
_h = dict(Mb=6e10, M200=1e12, a=3.0)
_c = float(L57["Lm"]["c200_dm14"](_h["M200"]))
ctl_L321 = retained_L321(hernquist(_h["Mb"], _h["a"]), _h["M200"], _c, 30.0, 0.0, "newtonian", 250.0, 1.0, N=4000)[0]
ctl_mine = float(retained_acc(hernquist(_h["Mb"], _h["a"]), _h["M200"], _c, [30.0], np.inf, 250.0, L57["Lm"]["RHO_C0"], N=4000)[0][0])
check("C3 CONTROL: decay on entry with r_v -> infinity is L321's retained(fd = 1) (Milky-Way host, 250 km/s so the retained "
      "fraction is non-trivial, identical draws)", f"L321 {ctl_L321:.6f}, AT1 {ctl_mine:.6f}",
      abs(ctl_L321 - ctl_mine) < 1e-9 and 0.02 < ctl_L321 < 0.98, load_bearing=False)
OUT["numbers"]["controls"] = dict(table_dev=max(dev1), gp5_dev=max(dev2), c3=(ctl_L321, ctl_mine))

# ================================================================================================ A1 mass selectivity
banner("A1  MASS SELECTIVITY: where the carrier converts, by host mass (z = 2, 3)")
A1 = {}
sel_hi = LGM >= 10.5 + math.log10(h)                                 # M_h >= 1e10.5 Msun (grid in Msun/h)
for z in (2.0, 3.0):
    s_ = SIG0 * DG(z); nu_ = DC / s_; w_ = f_st(nu_) * np.abs(np.gradient(nu_, np.log(MH)))
    for foot in FOOT:
        for yv in (0.1, 0.3, 1.0):
            lc, xv, _, _ = trig_acc(z, yv, A0K[foot])
            tot = float(_trap(w_ * lc, np.log(MH))); hi = float(_trap(w_ * lc * sel_hi, np.log(MH)))
            fire = LGM[np.argmax(lc > 1e-3)] - math.log10(h) if (lc > 1e-3).any() else float("nan")
            A1[(z, foot, yv)] = dict(frac_hi=hi / max(tot, 1e-300), F_trig=tot, lowest_firing_logM=fire)
    m57, _, _, _, _ = trig57(z, 30.0, "cleared")
    sel57 = MH >= L57["M_MIN"] * h
    t57 = float(_trap((w_ * m57)[sel57], np.log(MH)[sel57])); h57 = float(_trap((w_ * m57 * sel_hi)[sel57], np.log(MH)[sel57]))
    A1[(z, "L357 density x_v = 30", 0)] = dict(frac_hi=h57 / t57, F_trig=t57)
    P(f"    z = {z}: " + "; ".join(f"{f_[:5]} y_v {yv}: {A1[(z, f_, yv)]['frac_hi']:.3f} of F_trig {A1[(z, f_, yv)]['F_trig']:.3f} "
                                  f"above 1e10.5 (fires from 1e{A1[(z, f_, yv)]['lowest_firing_logM']:.1f})" for f_ in FOOT for yv in (0.1, 0.3, 1.0))
      + f"  || L357 density trigger (x_v = 30): {h57 / t57:.3f} of F_trig {t57:.3f}")
OUT["numbers"]["A1"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in A1.items()}
a1_ok = all(v["frac_hi"] >= 0.95 for k, v in A1.items() if k[2] != 0)
check("A1 MASS SELECTIVITY: at z = 2 and 3, y_v >= 0.1, both footings, >= 95% of the triggered carrier sits in halos >= "
      "1e10.5 Msun (the kernel's argument never reaches y_v in the web or in minihalos)",
      f"min fraction above 1e10.5: {min(v['frac_hi'] for k, v in A1.items() if k[2] != 0):.3f}; L357's density trigger (x_v = 30): "
      f"{A1[(2.0, 'L357 density x_v = 30', 0)]['frac_hi']:.3f} (z = 2), {A1[(3.0, 'L357 density x_v = 30', 0)]['frac_hi']:.3f} (z = 3)",
      a1_ok, "the trigger's variable selects condensed baryons; a density trigger at the particle scale fires in every halo")

# ================================================================================================ S1 design scan at z = 2.5
banner("S1  THE DESIGN SCAN: flagship at z = 2.5 (canonical, L356's central gas) and L319's matter proxy, over (y_v, v_A)")
YVS = [0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0]; VAS = [300.0, 450.0, 600.0, 800.0, 1000.0]


def s1_job(j):
    yv, va = j
    rows = flagship_rows(2.5, yv, va * KMUL, mufacs=(1.0,), feet=("canonical",))
    S, Fc = history_acc(yv, va * KMUL, A0K["canonical"])
    r = solve_hist(S, va * KMUL)
    return j, dict(flag_max=max(abs(r_["shift"]) for r_ in rows), flag=[round(r_["shift"], 3) for r_ in rows if r_["kernel"] == "l320"],
                   t2=r["t2"], t3=r["t3"], S8=r["S8"], Fb=[float(np.interp(z, ZG, Fc)) for z in (3.0, 2.0, 0.0)])


with ThreadPoolExecutor(NTH) as ex:
    S1 = dict(ex.map(s1_job, [(yv, va) for yv in YVS for va in VAS]))
for yv in YVS:
    P(f"    y_v {yv:4.2f}: " + " | ".join(f"v_A {va:4.0f}: flag {S1[(yv, va)]['flag_max']:+.2f} T2 {min(S1[(yv, va)]['t2'], S1[(yv, va)]['t3']):.3f}"
                                         for va in VAS) + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["S1"] = {f"{k[0]}|{k[1]}": v for k, v in S1.items()}
both = [k for k, v in S1.items() if v["flag_max"] <= 0.10 and min(v["t2"], v["t3"]) >= 0.9]
check("S1 (reported) the design scan: flagship at z = 2.5 and L319's matter proxy over (y_v, v_A)",
      f"cells passing the flagship (<= 0.10): {sorted(k for k, v in S1.items() if v['flag_max'] <= 0.10)}; passing the loose proxy: "
      f"{sorted(k for k, v in S1.items() if min(v['t2'], v['t3']) >= 0.9)}; both: {sorted(both)}", True, load_bearing=False)

# ================================================================================================ A2 the flagship by construction
banner("A2  THE FLAGSHIP BY CONSTRUCTION: y_v <= 0.1, v_A >= 600 km/s -- GP5's full grid at z = 2.5, and z = 0.5-2")
A2CELLS = [(0.05, 600.0), (0.1, 600.0), (0.1, 800.0), (0.1, 1000.0)]
A2 = {}


def a2_job(j):
    yv, va, z = j
    mf = (1 / 1.5, 1.0, 1.5) if z == 2.5 else (1.0,)
    return j, flagship_rows(z, yv, va * KMUL, mufacs=mf)


with ThreadPoolExecutor(NTH) as ex:
    for j, rows in ex.map(a2_job, [(yv, va, z) for (yv, va) in A2CELLS for z in (0.5, 1.0, 1.5, 2.0, 2.5)]):
        A2[j] = dict(max_abs=max(abs(r_["shift"]) for r_ in rows), rows=rows)
for (yv, va) in A2CELLS:
    P(f"    y_v {yv}, v_A {va:.0f}: " + "; ".join(f"z {z}: max |shift| {A2[(yv, va, z)]['max_abs']:.3f}" for z in (0.5, 1.0, 1.5, 2.0, 2.5))
      + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["A2"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in A2.items()}
a2_worst = max(v["max_abs"] for v in A2.values())
check("A2 THE FLAGSHIP BY CONSTRUCTION: every cell with y_v <= 0.1 and v_A >= 600 km/s keeps the deep-MOND Tully-Fisher zero "
      "point within 0.10 dex of the framework's 0.00 at z = 2.5 over GP5's full grid (M_b 1e10-1e11, both footings, L356's "
      "gas range, both kernels) and at z = 0.5, 1, 1.5, 2", f"worst |shift| {a2_worst:.3f} dex over {len(A2CELLS)} cells x 5 redshifts",
      a2_worst <= 0.10, "the trigger radius sits at or outside the flagship radius by definition (g_bar = 0.1 a0), and the "
      "loss cone empties the orbits that would carry carrier back inside it")

# ================================================================================================ A3 the matter proxy's price
banner("A3  THE MATTER PROXY'S PRICE: the A2 cell, and the trigger-independent minimum for GP5's flagship population")
Scell, Fcell = history_acc(0.1, 600.0 * KMUL, A0K["canonical"])
rcell = solve_hist(Scell, 600.0 * KMUL)
P(f"    A2 cell (y_v 0.1, v_A 600): F_b(z = 3, 2) {np.interp(3, ZG, Fcell):.3f}/{np.interp(2, ZG, Fcell):.3f} -> T^2(k = 5) z = 3 "
  f"{rcell['t3']:.4f}, z = 2 {rcell['t2']:.4f}")


def opt_table(c, xout, cuts, N=20000, K=64, seed=7):
    rng = np.random.default_rng(seed)
    m_c = math.log(1 + c) - c / (1 + c)
    M = lambda x: (np.log1p(x * c) - x * c / (1 + x * c)) / m_c
    xg = np.geomspace(1e-5, 1.0, 3000)
    x = np.interp(rng.random(N), M(xg), xg)
    rho = 1.0 / (xg * c * (1 + xg * c) ** 2); gm = M(xg) / xg ** 2
    integ = rho * gm; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(xg)
    s2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / rho
    v = rng.normal(0, 1, (N, 3)) * np.sqrt(np.interp(x, xg, s2))[:, None]
    L = x * np.linalg.norm(v[:, 1:], axis=1); E = 0.5 * (v ** 2).sum(1) + nfw_phi(x, c)
    xs = np.geomspace(1e-5, 3.0, 1200); ph = nfw_phi(xs, c)
    vr2 = 2 * (E[:, None] - ph[None, :]) - (L[:, None] / xs[None, :]) ** 2
    pos = vr2 > 0; ip = np.argmax(pos, 1); ia = len(xs) - 1 - np.argmax(pos[:, ::-1], 1)
    rp = xs[np.maximum(ip - 1, 0)]; ra = xs[np.minimum(ia + 1, len(xs) - 1)]
    phi = (np.arange(K) + 0.5) * np.pi / K; rm, D = 0.5 * (ra + rp), 0.5 * (ra - rp)
    rr = rm[:, None] - D[:, None] * np.cos(phi)[None, :]
    v2 = 2 * (E[:, None] - nfw_phi(rr, c)) - (L[:, None] / rr) ** 2
    wgt = D[:, None] * np.sin(phi)[None, :] / np.sqrt(np.maximum(v2, 1e-12))
    fin = (wgt * (rr < xout)).sum(1) / wgt.sum(1)
    order = np.argsort(-fin); cum_in = np.cumsum(fin[order]) / fin.sum(); cum_rm = np.arange(1, N + 1) / N
    return [float(cum_rm[min(np.searchsorted(cum_in, ct), N - 1)]) for ct in cuts]


CUTS = np.array([0.1, 0.3, 0.5, 0.7, 0.8, 0.85, 0.9, 0.93, 0.95, 0.97, 0.99])
CGo = np.array([2.5, 3.5, 5.0, 7.0, 10.0, 15.0]); XOo = np.array([0.03, 0.06, 0.1, 0.15, 0.2, 0.27, 0.35, 0.5])
with ThreadPoolExecutor(NTH) as ex:
    _OT = dict(ex.map(lambda j: (j, opt_table(CGo[j[0]], XOo[j[1]], CUTS)), [(i, k) for i in range(len(CGo)) for k in range(len(XOo))]))
FOPT = np.array([[[_OT[(i, k)][m] for m in range(len(CUTS))] for k in range(len(XOo))] for i in range(len(CGo))])
I_FO = RegularGridInterpolator((np.log(CGo), np.log(XOo), CUTS), FOPT, bounds_error=False, fill_value=None)
P(f"    optimal-removal table built: to cut the inner carrier by 93% a c = 3.5 halo at x_out = 0.27 must lose "
  f"{float(I_FO([[math.log(3.5), math.log(0.27), 0.93]])[0]):.3f} of its carrier   [{time.time()-T0:.0f}s]")


def bound_F(z, a0k, lMb_min=10.0, mufac=1.0, weight="bias"):
    """the trigger-independent minimum: every halo hosting M_b >= 10^lMb_min cut, inside its flagship radius, to GP5's
    gate (the retained fraction that gives a 0.10-dex shift with L320's kernel), by the optimal removal."""
    s = SIG0 * DG(z); nu = DC / s; w = f_st(nu) * np.abs(np.gradient(nu, np.log(MH)))
    Mh = MH / h; cs = c_dm14(MH, z); r200 = (3 * Mh / (4 * np.pi * 200 * RHOC0_KPC * Ez2(z))) ** (1 / 3)
    fo = np.zeros(len(MH)); a0 = a0k * 1e6 / KPC_M
    for i in range(len(MH)):
        Mb, _ = galaxy_baryons(Mh[i], z, mufac)
        if Mb < 10 ** lMb_min: continue
        r_out_m = math.sqrt(G20 * Mb * MSUN / (0.1 * a0)); gb = G20 * Mb * MSUN / r_out_m ** 2
        g_fw = float(nu20(gb / a0)) * gb; gc1 = g_nfw(Mh[i], z, r_out_m)
        r_req = (10 ** 0.05 - 1) * g_fw / gc1
        cut = min(1 - r_req, CUTS[-1]) if r_req < 1 else 0.0          # above 0.99 clipped down (under-counts: conservative)
        if cut <= 0: continue
        xo = float(np.clip(r_out_m / KPC / r200[i], XOo[0], XOo[-1]))
        cc = math.log(float(np.clip(cs[i], CGo[0], CGo[-1])))
        fo[i] = float(I_FO([[cc, math.log(xo), max(cut, CUTS[0])]])[0]) * (min(cut / CUTS[0], 1.0))   # linear below 0.1
    wb = w * (b_st(nu) if weight == "bias" else 1.0)
    return float(_trap(wb * np.clip(fo, 0, 1), np.log(MH)))


BND = {}
VBND = (600.0, 700.0, 800.0, 1000.0, 1500.0, 2000.0, 3000.0)                # the speeds at which removal clears (S1: 450 does not)
for lmin in (10.0, 10.5, 11.0):
    Fm = bound_F(2.5, A0K["canonical"], lmin)
    S_b = np.where(1 / a_grid - 1 <= 2.5, 1 - Fm, 1.0)
    with ThreadPoolExecutor(NTH) as ex:
        t2s = dict(ex.map(lambda vv: (vv, solve_hist(S_b, vv * KMUL)["t2"]), VBND))
    BND[lmin] = dict(F_b_min=Fm, T2_z2=t2s, max_T2=max(t2s.values()))
    P(f"    flagship population M_b >= 1e{lmin}: minimum removal F_b {Fm:.4f} (bias-weighted) at z = 2.5 -> T^2(k = 5, z = 2) "
      + ", ".join(f"{vv:.0f}: {t:.3f}" for vv, t in t2s.items()) + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["A3"] = dict(cell=dict(Fb=[float(np.interp(z, ZG, Fcell)) for z in (3.0, 2.0)], t3=rcell["t3"], t2=rcell["t2"]),
                            bound={str(k): v for k, v in BND.items()})
a3_ok = (min(rcell["t2"], rcell["t3"]) < 0.9) and (BND[10.0]["max_T2"] < 0.9)
check("A3 THE MATTER PROXY'S PRICE: the A2 cell fails L319's proxy even loose (T^2(k = 5) < 0.9 at z = 2 or 3), and so does "
      "the trigger-independent minimum for GP5's flagship population (M_b >= 1e10 at z = 2.5, optimal removal, every "
      "daughter speed 600-3000 km/s)", f"A2 cell: T^2 z = 3 {rcell['t3']:.3f}, z = 2 {rcell['t2']:.3f}; minimum: F_b "
      f"{BND[10.0]['F_b_min']:.4f}, best T^2(z = 2) {BND[10.0]['max_T2']:.3f} (M_b >= 1e10.5: {BND[10.5]['max_T2']:.3f}; "
      f">= 1e11: {BND[11.0]['max_T2']:.3f})", a3_ok,
      "a statement about the MATTER power at k = 5 h/Mpc: clearing the flagship radius at z = 2.5 means moving ~9% of the "
      "bias-weighted mass onto >~ Mpc orbits.  Whether the FOREST sees it is AT2's calibrated flux test (the gas lags a late, "
      "halo-internal removal; L365's runs)")

# ================================================================================================ R1 RC100
banner("R1  RC100 (documentary): the inner dark fraction and the inverted a0(z) slope, natural cell y_v = 1 and the A2 cell")
R1 = {}


def rc_job(j):
    yv, va, gi = j
    g_ = GAL100[gi]; z = g_["z"]; mu = 0.5 * ((1 + z) / 2) ** 2
    Mh = halo_mass(g_["Mb"] / (1 + mu), z); c = float(c200_20(Mh, z)); rhoc = RHOC0_KPC * Ez2(z)
    a = g_["Re"] / KPC / 1.8153
    rv = r_trigger(g_["Mb"], a, yv, A0K["canonical"])
    rr, _ = retained_acc(hernquist(g_["Mb"], a), Mh, c, [g_["Re"] / KPC], rv, va * KMUL, rhoc, N=4000)
    return j, (Mh, float(rr[0]))


with ThreadPoolExecutor(NTH) as ex:
    RCR = dict(ex.map(rc_job, [(yv, va, gi) for (yv, va) in ((1.0, 600.0), (0.1, 600.0)) for gi in range(len(GAL100))]))
zs = [g_["z"] for g_ in GAL100]
fd_data = float(np.median([g_["fdm"] for g_ in GAL100]))
for (yv, va) in ((1.0, 600.0), (0.1, 600.0), ("retained", 0.0)):
    fdm, la = [], []
    for gi, g_ in enumerate(GAL100):
        z = g_["z"]; a0 = FOOT["canonical"]; gb = G20 * 0.5 * g_["Mb"] * MSUN / g_["Re"] ** 2
        if yv == "retained":
            mu = 0.5 * ((1 + z) / 2) ** 2; Mh = halo_mass(g_["Mb"] / (1 + mu), z); ratio = 1.0
        else:
            Mh, ratio = RCR[(yv, va, gi)]
        gc = g_nfw(Mh, z, g_["Re"]) * ratio
        go = nu_mono(gb / a0) * gb + gc; f = 1 - gb / go
        fdm.append(f); la.append(invert(f, go))
    s_, e_, _ = slope_boot(zs, la)
    R1[str((yv, va))] = dict(median_fdm=float(np.nanmedian(fdm)), slope=s_)
    P(f"    {('carrier retained (no trigger)' if yv == 'retained' else f'y_v {yv}, v_A {va:.0f}'):32s}: median f_DM(<R_e) "
      f"{np.nanmedian(fdm):.2f} (data {fd_data:.2f}); inverted slope {s_:+.3f} (data {L20['s_data']:+.3f} +/- {L20['e_data']:.3f})")
OUT["numbers"]["R1"] = R1
check("R1 (documentary) RC100 on the natural cell and the A2 cell", R1, True,
      "RC100's level and trend are calibration-conditional (L331/L332); reported, not gated", load_bearing=False)

# ================================================================================================ B1 the budget for AT2
banner("B1  THE DECAY BUDGET HANDED TO AT2 (canonical footing, L356's central gas)")
B1 = {}
for (yv, va) in ((0.1, 600.0), (0.1, 800.0), (0.05, 600.0), (0.3, 600.0), (1.0, 600.0)):
    _, Ft = history_acc(yv, va, A0K["canonical"], weight="plain", escaped=False)
    _, Fe = history_acc(yv, va, A0K["canonical"], weight="bias", escaped=True)
    B1[f"{yv}|{va}"] = dict(z=ZG.tolist(), F_trig_unweighted=Ft.tolist(), F_b_escaped=Fe.tolist())
    P(f"    y_v {yv}, v_A {va:.0f}: triggered (unweighted) z = 4/3/2/1/0: " + "/".join(f"{np.interp(z, ZG, Ft):.3f}" for z in (4, 3, 2, 1, 0))
      + "; escaped, bias-weighted: " + "/".join(f"{np.interp(z, ZG, Fe):.3f}" for z in (4, 3, 2, 1, 0)))
OUT["numbers"]["B1"] = B1
check("B1 (reported) the decay budget F(z) for AT2's particle-mesh forest test", {k: [round(float(np.interp(z, ZG, v["F_trig_unweighted"])), 4)
                                                                                   for z in (3, 2)] for k, v in B1.items()}, True, load_bearing=False)

# ================================================================================================ verdict
banner("VERDICT")
P(f"""  The acceleration trigger does what it was built for.  Keyed on the kernel's own argument, it converts the carrier only
  where baryons have condensed (A1: >= {min(v['frac_hi'] for k, v in A1.items() if k[2] != 0):.2f} of the triggered carrier in hosts
  above 1e10.5 Msun at z = 2-3), and with y_v <= 0.1 and v_A >= 600 km/s it keeps the flagship prediction flat at every
  redshift (A2: worst {a2_worst:.3f} dex).  With y_v = 1 (no new constant) it brings RC100's inner dark fraction to
  {R1[str((1.0, 600.0))]['median_fdm']:.2f} (data {fd_data:.2f}; carrier retained {R1[str(('retained', 0.0))]['median_fdm']:.2f}).
  The price on L319's MATTER proxy is real and trigger-independent (A3): clearing the flagship radius at z = 2.5 moves
  >= {BND[10.0]['F_b_min']:.3f} of the bias-weighted mass onto >~ Mpc orbits, T^2(k = 5, z = 2) <= {BND[10.0]['max_T2']:.3f}.  The forest,
  however, is measured in the gas's flux, which lags a late, halo-internal removal: AT2 scores it on that observable in
  the record's particle-mesh machinery (L365's rule), with warm-dark-matter relics as a yardstick.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
OUT["runtime_s"] = time.time() - T0
outname = f"{SLUG}_results{'_FAST' if FAST else ''}{'_MUTATE' if MUTATE else ''}.json"   # smoke runs never overwrite the main output
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
