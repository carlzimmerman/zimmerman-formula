#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR16 (the FK2 lane) -- THE DARK FLUID'S OWN CONVERSION SURFACE: does the fluid's phi_H phi_H -> phi_L phi_L conversion
clear the flat-a0 flagship radius by z = 2.5, and is its early conversion budget safe for the Lyman-alpha forest?

WHY.  FK1 (c2e1fa119) builds the kick inside the dark fluid's order parameter: a U(1)-breaking splitting eps/m^2 =
1.84-2.35e-6 (v_k = 575-650 km/s), a pure cross quartic lambda(K)(Im Phi^2)^2, the coupling vacuum-gated through K
(q = 1.75), Bose-stimulated, so the trigger is the fluid's OWN density (n^2).  FL2 (e96b71eb0) puts it in V0's dark slot.
The flat-a0 flagship at z = 2.5 tolerates a retained carrier fraction S <= 0.059 at r_F (MS2 on DE4's galaxy; M_b = 1e11
canonical is the worst host).  The record's particle-mesh residue at z = 2 is S = 0.063-0.075 (L388): the row is 'not
established'.  AT1 (dd1d6a0d6) scores a hand-put acceleration trigger on the halo model; this lane puts the fluid's own
conversion surface into AT1's machinery.

THE DESIGN (supplied by the session that built FK1; implemented here, not re-derived).
  * Conversion depth (per E_need e-folds):  S_c(r) = (2 C H/pi) Int_r^inf (rho_c/rho_bg)^2 D dr'/sigma(r').
    Spontaneous ignition where S_c >= 1; a stimulated front where S_c >= 1/E_need (E_need 60-180, FK1 N1).
    rho_bg = delta_t(z) rho_bar_carrier, delta_t = 2.5 E^2/(1.5 Omega_m(z)) (the linear cell's threshold, carrier reading).
    C ~ 1 (broadband prefactor), bracketed 0.3-3.  D = exp(-(Delta v/sigma)^2/2), Delta v = v_k - sqrt(v_k^2 - 2 Delta Phi).
    The front depends on K = C E_need only: the design's six corners are K = 18, 54, 60, 180, 540.
  * Method: AT1's machinery, exec'd from the committed file only up to 'NFW loss cone + escape (added)' and from
    'retention with decay on entry (added)' through flagship_rows (its main and tables are NOT run); r_v = the fluid's
    surface.  AT1's retained_acc decays everything inside r_v IN PLACE (L388-like).  In the fluid's history the interior
    converted earlier, in smaller progenitors: the z = 2.5 state drops the in-place population that escaped then and keeps
    only the daughters converting on entry at the surface, GATED by a progenitor check -- a mass accretion history
    M(z) = M(2.5) exp(-alpha (z - 2.5)), alpha = dlnM/dz magnitude 0.8 (0.6-1.0); the epoch z_pass the front passes r_F;
    the INTACT progenitor's v_esc(r_F) at z_pass against v_k (G1: escaped iff v_esc < v_k).
  * Part B: the early conversion budget F(z) over the halo mass function, minihalos down to the fluid's own scale
    (m >= 2e-19 eV), scored against the budget AT2 put through the particle mesh (no particle-mesh run here).
IMPLEMENTATION CHOICES (declared; each is the conservative side for the verdict it feeds).
  * The carrier density is AT1's truncated NFW, (1 - f_b) rho_NFW(r < r200): no infall region, so S_c(r200) = 0 and the
    front lies inside r200 -- a SMALLER front, i.e. a later passage of r_F in a bigger progenitor (pessimistic for A) and a
    smaller budget (optimistic for 'the budget is large', i.e. conservative for B).
  * sigma(r) in S_c is the untruncated isotropic Jeans dispersion (baryons + untruncated carrier): larger than the
    truncated one near r200, so again a smaller front.
  * The retained fraction is scored in TWO readings of the potential's response: AT1's own self-consistent iteration
    (iters = 2: the potential drops as the carrier leaves) and the INTACT halo held fixed (iters = 0: the daughters feel
    the pre-conversion potential).  The truth for a front that sweeps out over Gyr lies between; the load-bearing
    flagship checks require BOTH.
  * G2 (a refinement, reported): each in-place particle converted when the front reached its pericentre r_p; it is kept
    with weight 1 - P_esc, P_esc = L357's escape table at u = v_k/v_esc,prog(r_p, z_pass(r_p)), s = sigma_prog/v_esc,prog;
    kept daughters are then treated in place at z = 2.5 (pessimistic: the z = 2.5 well is deeper).
  * Halo concentration: AT1's Dutton-Maccio c(M, z) with a floor c >= 3 (simulated concentrations flatten at c ~ 3-4 at
    high peak height; D-M is fitted to z <= 5 and its extrapolation gives c < 1 for small halos at z > 6).  The floor
    binds only for halos below ~1e11 Msun at z >~ 4.5 (the M_b = 1e10 hosts' progenitors meet r_F there); the gate
    without it is reported (F2).

PRE-DECLARED (written 2026-09-26 22:45 in the session's scratch notes, before any XR16 number was computed).
  H-A1: with conversion at the fluid's surface and the in-place population dropped where the intact progenitor's
        v_esc(r_F) at the front's passage is below v_k, S at r_F <= 0.059 and the GP5 flagship |shift| <= 0.10 dex for
        M_b = 1e10-1e11, both footings, L356's gas range, both kernels, over C, E_need, alpha, v_k 600 (575).  EXPECT TRUE.
  H-A2: the in-place population kept (no early escape, L388-like) at the same surface: S at r_F > 0.059 and/or
        |shift| > 0.10, the flagship FAILS (designer: S ~ 0.1-0.2).  EXPECT TRUE.
  H-B:  the fluid's early conversion budget exceeds the budget AT2 scored (AT1's A2 cell, F_trig 0.052/0.083 at z = 3/2),
        so AT2's <= 0.33%/<= 1.7% flux result does not carry over.  EXPECT TRUE.
  AFTER THE EXPLORATORY COMPONENT RUN (not committed: the fronts at z = 2.5, the passages, and ~75 retention calls on the
  M_b = 1e11 and 1e11.5 hosts -- in place, surface-only, the intact-potential reading and G2, v_k 575-600): the in-place S
  at M_b = 1e11 came out 0.006-0.010 in AT1's self-consistent reading and 0.12-0.21 with the intact potential held fixed.
  H-A2 is therefore kept as pre-declared and reported as it falls (T1).  The one change made after that run makes A1
  STRICTER: the pass must hold in BOTH readings of the potential's response (it was pre-declared for AT1's reading only).
CHECKS
  C1 CONTROL: r_v = AT1's y_v = 0.1 trigger radius, through this lane's copy of retained_acc and flagship arithmetic,
     reproduces AT1's committed A2 rows at z = 2.5, v_A = 600 EXACTLY (36 rows).
  C2 CONTROL: the copy with no gate is bit-identical to AT1's retained_acc at the fluid's surface (identical draws).
  C3 CONTROL: the depth integral: a singular isothermal sphere with D -> 1 against the closed form, and the D factor against
     adaptive quadrature.
  C4 CONTROL: v_esc from L321's potential (truncated NFW + Hernquist) against the closed form.
  C5 CONTROL: AT2's own functions (band_dev, forest_D, l365_rule, exec'd from its source text; its main is not run)
     reproduce AT2's committed F4 table (L365's runs) and its cells' rule values from the committed flux power.
  F1 THE SURFACE AT z = 2.5: r_F lies inside the fluid's stimulated front for every host and K (reported: x_s = r_s/r200,
     the spontaneous-ignition radius for C = 0.3-3).
  F2 THE PASSAGE (reported): z_pass(r_F) and the intact progenitor's v_esc(r_F); fronts monotone in time; the cusp ignites
     at every progenitor epoch; alpha_crit for the worst record host.
  A1 = H-A1 (strict): S <= 0.059 and |shift| <= 0.10 on the record's grid (M_b 1e10-1e11) with G1, over K = 18-540,
     alpha = 0.6-1.0, v_k = 575-600, both footings, the gas range, both kernels, in BOTH potential readings.
  A2 THE EARLY-ESCAPE STEP ITSELF: at every cell where the progenitor gate escapes, including the M_b = 1e11.5 hosts that
     in-place conversion leaves loaded, S <= 0.059 and |shift| <= 0.10 in both readings.
  T1 = H-A2 (pre-declared, reported as it falls): the in-place reading fails the flagship on the record's grid, in AT1's
     own (self-consistent) reading.
  A3 (reported) G2, the per-particle refinement.  A4 (reported) the M_b = 1e11.5 extension, cell by cell.
  B1 = H-B: F_conv(z = 3, 2) exceeds AT1's A2-cell budget even at the most favourable corner (K = 18, the record's
     M_min = 1e8 Msun cut, which removes more small halos than any allowed fluid mass).
  B2 (reported) a conservative forest bound from the committed particle-mesh responses (sparsest-first to densest-first).
  B3 (reported flag) the design's stimulated criterion in the Hubble flow (the web), which this halo model does not score.
MUTATE=1: the in-place population is kept (no early escape: G1 and G2 keep every in-place daughter).  A1 and A2 must FAIL
(the intact-potential reading gives the L388-like S; the 1e11.5 hosts keep their carrier): rc = 1.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR16_fluid_conversion_surface.py
Single-threaded; ~50 min; peak memory ~3 GB (AT1's retention machinery).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy.integrate import quad
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SMOKE = os.environ.get("XR16_SMOKE", "0") == "1"                     # reduced grids for a code test; never committed
OUTDIR = os.environ.get("XR16_OUTDIR", HERE) if SMOKE else HERE
SLUG = "XR16_fluid_conversion_surface"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR16", "mutate": MUTATE, "smoke": SMOKE, "checks": {}, "numbers": {}}
EXPECT = dict(A1=True, A2=True, T1=True, B1=True)                    # pre-declared (docstring)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)
def el(): return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the in-place population is kept (no early escape); A1 and A2 must FAIL ***")
if SMOKE: P("\n  *** XR16_SMOKE=1: reduced grids, code test only, output not for the record ***")

# ================================================================================================ AT1's machinery (as designed)
PAT1 = os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT1_acceleration_trigger_highz.py")
_src = open(PAT1).read()
_M1 = "# ------------------------------------------------------------------------------------------------ NFW loss cone + escape (added)"
_M2 = "# ------------------------------------------------------------------------------------------------ retention with decay on entry (added)"
_M3 = "# ================================================================================================ C1-C3"
assert _src.count(_M1) == 1 and _src.count(_M2) == 1 and _src.count(_M3) == 1, "AT1 section markers changed"
_head = _src.split(_M1)[0]
assert _head.count('P(__doc__.split("CHECKS")[0].strip())') == 1
_head = _head.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")           # exec() has no module docstring
_tail = _M2 + _src.split(_M2)[1].split(_M3)[0]
_saved = {k_: os.environ.get(k_) for k_ in ("MUTATE", "FAST")}
os.environ["MUTATE"] = "0"; os.environ["FAST"] = "0"                   # AT1's own switches stay off
A = {"__name__": "at1", "__file__": PAT1}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_head, A)
    exec(_tail, A)
for k_, v_ in _saved.items():
    if v_ is None: os.environ.pop(k_, None)
    else: os.environ[k_] = v_
assert A["FAST"] is False and A["MUTATE"] is False
nfw21, potential, frac_inside, RG, RGc, FB = A["nfw21"], A["potential"], A["frac_inside"], A["RG"], A["RGc"], A["FB"]
hernquist, GK, RHOC0_KPC, Ez2, Om, h = A["hernquist"], A["GK"], A["RHOC0_KPC"], A["Ez2"], A["Om"], A["h"]
c200_20, halo_mass, Re_kpc, galaxy_baryons, r_trigger = A["c200_20"], A["halo_mass"], A["Re_kpc"], A["galaxy_baryons"], A["r_trigger"]
retained_acc, FOOT, A0K, G20, MSUN, KPC = A["retained_acc"], A["FOOT"], A["A0K"], A["G20"], A["MSUN"], A["KPC"]
g_nfw, nu20, nu_mono = A["g_nfw"], A["nu20"], A["nu_mono"]
MH, LGM, SIG0, DG, DC, f_st, b_st, c_dm14, _trap = A["MH"], A["LGM"], A["SIG0"], A["DG"], A["DC"], A["f_st"], A["b_st"], A["c_dm14"], A["_trap"]
PESC = A["L57"]["PESC"]; UGmax, SGmin, SGmax = float(A["L57"]["UG"][-1]), float(A["L57"]["SGR"][0]), float(A["L57"]["SGR"][-1])
P(f"\n  AT1 loaded as designed (head to 'NFW loss cone + escape', then 'retention with decay on entry' through flagship_rows); "
  f"h = {h}, Om = {Om:.4f}, f_b = {FB}   {el()}")

# ================================================================================================ constants of this lane
Z0 = 2.5
KS = (18.0, 54.0, 60.0, 180.0, 540.0)                                # K = C E_need at the design's corners
K_OF = {(0.3, 60): 18.0, (0.3, 180): 54.0, (1.0, 60): 60.0, (1.0, 180): 180.0, (3.0, 60): 180.0, (3.0, 180): 540.0}
CS = (0.3, 1.0, 3.0)
ALPHAS = (0.6, 0.8, 1.0)
VKS_RET = (575.0, 600.0)                                              # retention runs (650 kicks harder: gate reported)
VKS_GATE = (575.0, 600.0, 650.0)
LMBS = (10.0, 10.5, 11.0, 11.5); LMB_RECORD = (10.0, 10.5, 11.0)
MUFACS = (1 / 1.5, 1.0, 1.5)
FEET = ("canonical", "alt")
S_MAX, SHIFT_MAX = 0.059, 0.10
C_FLOOR = 3.0
ZP = np.round(np.arange(Z0, 20.0 + 1e-9, 0.1), 4)                     # progenitor epochs
N_RET = 10000
K_G2 = (18.0, 60.0)
if SMOKE:
    KS = (18.0, 180.0); ALPHAS = (0.6, 1.0); VKS_RET = (600.0,); LMBS = (11.0, 11.5); LMB_RECORD = (11.0,)
    MUFACS = (1 / 1.5,); ZP = np.round(np.arange(Z0, 12.0 + 1e-9, 0.25), 4); N_RET = 2000; K_G2 = (18.0,)
    K_OF = {k_: v_ for k_, v_ in K_OF.items() if v_ in KS}


def Hz(z): return 0.1 * h * math.sqrt(Ez2(z))                        # km/s/kpc
def rho_bar_m(z): return Om * RHOC0_KPC * (1 + z) ** 3                # Msun/kpc^3
def Om_z(z): return Om * (1 + z) ** 3 / Ez2(z)
def delta_t(z): return 2.5 * Ez2(z) / (1.5 * Om_z(z))                 # the linear cell's threshold, carrier reading
def mfn(x): return np.log1p(x) - x / (1 + x)
def conc(M, z): return max(float(c200_20(M, z)), C_FLOOR)            # M in Msun


def halo_prof(Mh, c, z, Mb, a):
    """the intact halo: AT1's truncated NFW carrier + Hernquist baryons (Phi on RG, AT1's potential) and the untruncated
    isotropic Jeans dispersion of the NFW tracer (baryons + untruncated carrier)."""
    rhoc = RHOC0_KPC * Ez2(z)
    Mn, r200, rs = nfw21(Mh, c, rhoc)
    Mc0 = lambda x: (1 - FB) * Mn(np.minimum(x, r200))
    _, Phi = potential(hernquist(Mb, a), Mc0, 0.0, "newtonian")
    gu, _ = potential(hernquist(Mb, a), lambda x: (1 - FB) * Mn(x), 0.0, "newtonian")
    rho = 1.0 / ((RG / rs) * (1 + RG / rs) ** 2)
    integ = rho * gu; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    sig2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / rho
    rho_s = Mh / (4 * math.pi * rs ** 3 * float(mfn(c)))
    return dict(Mh=Mh, c=c, z=z, Mb=Mb, a=a, r200=r200, rs=rs, rho_s=rho_s, Phi=Phi, sig=np.sqrt(np.maximum(sig2, 1e-30)))


def depth(r, q2, sig, Phi, H, vk):
    """S_c(r_i)/C = (2H/pi) Int_{r_i}^{r_max} q^2 D dr'/sigma, q = rho/rho_bg, on an ascending grid (trapezoid in ln r)."""
    n = len(r)
    f = q2 / sig * r                                                  # integrand per d ln r
    dPhi = Phi[None, :] - Phi[:, None]                                # [i, j] = Phi_j - Phi_i
    dv = vk - np.sqrt(np.maximum(vk ** 2 - 2 * dPhi, 0.0))
    W = f[None, :] * np.exp(-0.5 * (dv / sig[None, :]) ** 2)
    seg = 0.5 * (W[:, 1:] + W[:, :-1]) * np.diff(np.log(r))[None, :]
    seg = np.where(np.arange(n - 1)[None, :] >= np.arange(n)[:, None], seg, 0.0)
    return 2 * H / math.pi * seg.sum(1)


def depth_halo(H_, vk, n_in=400):
    r200, rs = H_["r200"], H_["rs"]
    r = np.unique(np.concatenate([np.geomspace(1e-3 * rs, r200, n_in), r200 * (1 - np.geomspace(1e-4, 0.3, 80))]))
    r = r[(r > 0) & (r <= r200)]
    q = H_["rho_s"] / ((r / rs) * (1 + r / rs) ** 2) / (delta_t(H_["z"]) * rho_bar_m(H_["z"]))   # (1 - f_b) cancels
    return r, depth(r, q ** 2, np.interp(r, RG, H_["sig"]), np.interp(r, RG, H_["Phi"]), Hz(H_["z"]), vk)


def front(r, S, thr):
    """outermost radius with S >= thr (linear in S between the bracketing grid points)."""
    ok = S >= thr
    if not ok.any(): return 0.0
    i = int(np.where(ok)[0].max())
    if i == len(r) - 1: return float(r[-1])
    t = (S[i] - thr) / max(S[i] - S[i + 1], 1e-300)
    return float(r[i] + min(max(t, 0.0), 1.0) * (r[i + 1] - r[i]))


def host(lMb, mf, z=Z0):
    """AT1's flagship host (flagship_rows' own lines)."""
    Mb = 10 ** lMb; mu = mf * 0.5 * ((1 + z) / 2) ** 2
    Mh = halo_mass(Mb / (1 + mu), z); c = float(c200_20(Mh, z)); rhoc = RHOC0_KPC * Ez2(z)
    a = Re_kpc(Mb / (1 + mu), z) / 1.8153
    return dict(lMb=lMb, mf=mf, Mb=Mb, Mh=Mh, c=c, rhoc=rhoc, a=a)


def r_flag(Mb, foot):
    r_out_m = math.sqrt(G20 * Mb * MSUN / (0.1 * FOOT[foot])); return r_out_m, r_out_m / KPC


def flag_shift(z, Mb, Mh, foot, S, nuf):                             # AT1 flagship_rows' arithmetic, unchanged
    a0 = FOOT[foot]
    r_out_m = math.sqrt(G20 * Mb * MSUN / (0.1 * a0))
    gb = G20 * Mb * MSUN / r_out_m ** 2
    gc = g_nfw(Mh, z, r_out_m) * S
    g_fw = float(nuf(gb / a0)) * gb
    return 2 * math.log10((g_fw + gc) / g_fw)


KERNELS = (("l320", nu20), ("mono", nu_mono))


def retained_fluid(Mb_fn, M200, c, gates, rv, vk, rhoc, keep=None, N=10000, seed=5, iters=2):
    """AT1's retained_acc (committed lines, copied), plus per-particle weights on the IN-PLACE decays (keep: (r, r_p) ->
    [0, 1]; None = AT1's retained_acc exactly) and the potential-response reading (iters = 2 AT1's; 0 = intact halo)."""
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
        del ok
    else:
        lc = np.ones(N, bool); entry = np.zeros(N, bool); rp = np.zeros(N)
    pos_d = np.where(entry, rv if np.isfinite(rv) else 0.0, r)
    vb2 = np.maximum(2 * (E0 - np.interp(pos_d, RG, Phi0)), 0.0)
    vt_e = np.where(entry, L0 / np.maximum(pos_d, 1e-30), 0.0)
    vr_e = -np.sqrt(np.maximum(vb2 - vt_e ** 2, 0.0))
    vvec = np.where(entry[:, None], np.stack([vr_e, vt_e, np.zeros(N)], 1), v)   # in-place decays keep L321's full vector
    vvec = vvec + (lc * vk)[:, None] * nh
    inpl = lc & ~entry
    wk = None if keep is None else np.where(inpl, np.clip(keep(r, rp), 0.0, 1.0), 1.0)

    def mass_in(dec):
        pos = pos_d if dec else r
        vv = vvec if dec else v
        vr_, vt_ = vv[:, 0], np.linalg.norm(vv[:, 1:], axis=1); L = pos * vt_
        tot = (lambda f: w * f.sum()) if (wk is None or not dec) else (lambda f: w * (wk * f).sum())
        Mc = Mc0
        for _ in range(iters):
            _, Phi = potential(Mb_fn, Mc, 0.0, "newtonian")
            E = 0.5 * (vr_ ** 2 + vt_ ** 2) + np.interp(pos, RG, Phi)
            probe = np.geomspace(0.02 * rs, 3 * r200, 24)
            prof = np.array([tot(frac_inside(E, L, Phi, rg)) for rg in probe])
            Mc = (lambda pr=probe, pm=prof: (lambda x: np.interp(np.asarray(x, dtype=float), pr, pm, left=0.0)))()
        _, Phi = potential(Mb_fn, Mc, 0.0, "newtonian")
        E = 0.5 * (vr_ ** 2 + vt_ ** 2) + np.interp(pos, RG, Phi)
        return np.array([tot(frac_inside(E, L, Phi, rg)) for rg in gates])

    m0 = mass_in(False); m1 = mass_in(True)
    return m1 / np.maximum(m0, 1e-300), float(lc.mean()), dict(n_inplace=int(inpl.sum()), n_entry=int(entry.sum()),
                                                                kept_inplace=(float(wk[inpl].sum()) if wk is not None else float(inpl.sum())))


# ================================================================================================ C1-C5 controls
banner("C1-C5  CONTROLS")
at1 = json.load(open(os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT1_acceleration_trigger_highz_results.json")))
ref_rows = at1["numbers"]["A2"]["0.1|600.0|2.5"]["rows"]
mine = []
for foot in FEET:
    for lMb in (10.0, 10.5, 11.0):
        for mf in (1 / 1.5, 1.0, 1.5):
            if SMOKE and not (lMb == 11.0 and mf == 1 / 1.5): continue
            H0_ = host(lMb, mf)
            rv = r_trigger(H0_["Mb"], H0_["a"], 0.1, A0K[foot])
            _, r_out = r_flag(H0_["Mb"], foot)
            rr, flc, _ = retained_fluid(hernquist(H0_["Mb"], H0_["a"]), H0_["Mh"], H0_["c"], [r_out], rv, 600.0, H0_["rhoc"], N=10000)
            for kern, nuf in KERNELS:
                mine.append(dict(footing=foot, logMb=lMb, mu_fac=round(mf, 3), kernel=kern, r_out_kpc=r_out, r_v_kpc=rv,
                                 loss_cone=flc, retained=float(rr[0]), shift=flag_shift(Z0, H0_["Mb"], H0_["Mh"], foot, float(rr[0]), nuf)))
P(f"    C1 rows computed   {el()}")
ref_use = [r_ for r_ in ref_rows if any(r_["footing"] == m_["footing"] and r_["logMb"] == m_["logMb"] and r_["mu_fac"] == m_["mu_fac"]
                                        and r_["kernel"] == m_["kernel"] for m_ in mine)]
dev1 = 0.0
for m_ in mine:
    r_ = [x_ for x_ in ref_use if x_["footing"] == m_["footing"] and x_["logMb"] == m_["logMb"] and x_["mu_fac"] == m_["mu_fac"]
          and x_["kernel"] == m_["kernel"]][0]
    dev1 = max(dev1, *(abs(float(m_[k_]) - float(r_[k_])) for k_ in ("retained", "shift", "r_v_kpc", "loss_cone", "r_out_kpc")))
check("C1 CONTROL: r_v = AT1's y_v = 0.1 trigger radius, through this lane's copy of retained_acc and flagship arithmetic, "
      "reproduces AT1's committed A2 rows at z = 2.5, v_A = 600 (retained, shift, r_v, loss cone, r_out) exactly",
      f"{len(mine)} rows (of {len(ref_rows)} committed), max |dev| {dev1:.1e}", dev1 == 0.0 and len(mine) == (4 if SMOKE else 36),
      load_bearing=False)

Ht = host(11.0, 1 / 1.5); Hp = halo_prof(Ht["Mh"], Ht["c"], Z0, Ht["Mb"], Ht["a"])
_r, _S = depth_halo(Hp, 600.0); rv_t = front(_r, _S, 1 / 60.0)
_gt = [r_flag(Ht["Mb"], f_)[1] for f_ in FEET]
ra_, _ = retained_acc(hernquist(Ht["Mb"], Ht["a"]), Ht["Mh"], Ht["c"], _gt, rv_t, 600.0, Ht["rhoc"], N=N_RET)
rf_, _, _ = retained_fluid(hernquist(Ht["Mb"], Ht["a"]), Ht["Mh"], Ht["c"], _gt, rv_t, 600.0, Ht["rhoc"], N=N_RET)
dev2 = float(np.max(np.abs(ra_ - rf_)))
check("C2 CONTROL: the copy with no gate is bit-identical to AT1's retained_acc at the fluid's surface (M_b 1e11, gas x1/1.5, "
      "K = 60, both footings' r_F, identical draws)", f"AT1 {ra_}, copy {rf_}, max |dev| {dev2:.1e}", dev2 == 0.0, load_bearing=False)

# C3: the depth integral
H_t = 0.3; sig_t = 150.0; r0_t, q0_t = 10.0, 3.0; Rt = 300.0
rt = np.geomspace(0.5, Rt, 600)
q2_t = (q0_t * (r0_t / rt) ** 2) ** 2
Phi_iso = 2 * sig_t ** 2 * np.log(rt / r0_t)
S_num = depth(rt, q2_t, np.full_like(rt, sig_t), Phi_iso, H_t, 1e9)
S_ana = 2 * H_t / math.pi * (q0_t * r0_t ** 2) ** 2 * (rt ** -3 - Rt ** -3) / (3 * sig_t)
dev3a = float(np.max(np.abs(S_num[:-20] / S_ana[:-20] - 1)))
S_num_D = depth(rt, q2_t, np.full_like(rt, sig_t), Phi_iso, H_t, 600.0)
dev3b = 0.0
for i_ in (50, 250, 450):
    ri = rt[i_]
    fq = lambda lr: (q0_t * (r0_t / math.exp(lr)) ** 2) ** 2 / sig_t * math.exp(lr) * math.exp(
        -0.5 * ((600.0 - math.sqrt(max(600.0 ** 2 - 4 * sig_t ** 2 * (lr - math.log(ri)), 0.0))) / sig_t) ** 2)
    ex = 2 * H_t / math.pi * quad(fq, math.log(ri), math.log(Rt), limit=400, epsabs=0, epsrel=1e-10)[0]
    dev3b = max(dev3b, abs(S_num_D[i_] / ex - 1))
check("C3 CONTROL: the depth integral -- a singular isothermal sphere with D -> 1 against (2H/pi) q0^2 r0^4 (r^-3 - R^-3)/(3 sigma), "
      "and with D at v_k = 600 against adaptive quadrature (three radii)", f"max rel dev {dev3a:.1e} (closed form), {dev3b:.1e} (with D)",
      dev3a < 2e-3 and dev3b < 2e-3, load_bearing=False)

# C4: escape speed
_Mn, _r200, _rs = nfw21(Ht["Mh"], Ht["c"], Ht["rhoc"]); _mc = float(mfn(Ht["c"]))
dev4 = 0.0
for rq in (0.5, 3.0, 12.0, 40.0, 100.0, 300.0):
    x = rq / _r200
    phin = (-math.log1p(x * Ht["c"]) / (x * _mc) + math.log1p(Ht["c"]) / _mc - 1.0) if x < 1 else -1.0 / x
    ve_ana = math.sqrt(-2 * ((1 - FB) * GK * Ht["Mh"] / _r200 * phin - GK * Ht["Mb"] / (rq + Ht["a"])))
    ve_num = math.sqrt(-2 * float(np.interp(rq, RG, Hp["Phi"])))
    dev4 = max(dev4, abs(ve_num / ve_ana - 1))
check("C4 CONTROL: v_esc from L321's potential (AT1's intact halo: truncated NFW carrier + Hernquist) against the closed form at "
      "0.5-300 kpc", f"max rel dev {dev4:.1e}", dev4 < 2e-3, load_bearing=False)

# C5: AT2's functions on the committed flux power
PAT2 = os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT2_forest_flux_calibrated.py")
_s2 = open(PAT2).read()
_fns = "import math\nimport numpy as np\n" + _s2[_s2.index("BANDS = "):_s2.index("\n", _s2.index("BANDS = "))] + "\n"
for _nm in ("def band_dev", "def forest_D", "def l365_rule"):
    _i = _s2.index(_nm); _j = _s2.index("\n\n\n", _i); _fns += _s2[_i:_j] + "\n\n\n"
F2NS = {}
exec(_fns, F2NS)
at2 = json.load(open(os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT2_forest_flux_calibrated_results.json")))["numbers"]
at2m = json.load(open(os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT2_forest_flux_calibrated_results_MUTATE.json")))["numbers"]
l365 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L365_virialization_triggered_carrier_results.json")))["numbers"]["runs"]
dev5 = 0.0
for rk, rv_ in at2["F4"].items():
    dv = F2NS["band_dev"](l365[rk], l365["lcdm"])
    fm = max(abs(x_) for x_ in dv["3.0"] + dv["2.0"])
    dev5 = max(dev5, abs(F2NS["l365_rule"](l365[rk], l365["lcdm"]) - rv_["l365_rule"]), abs(fm - rv_["flux_max"]),
               abs(F2NS["forest_D"](dv) - rv_["D"]))
for src_, runs_ in ((at2, at2["runs65"]), (at2m, at2m["runs65"])):
    for ck, cv in src_["F12"]["cells"].items():
        rr_ = runs_[f"acc{ck}"]
        dev5 = max(dev5, abs(F2NS["l365_rule"](rr_, runs_["lcdm"]) - cv["l365_rule"]))
check("C5 CONTROL: AT2's own band_dev / forest_D / l365_rule (exec'd from its source text; its main is not run) reproduce its committed "
      "F4 table from L365's committed flux power, and its cells' rule values (densest-first and its MUTATE, sparsest-first)",
      f"{len(at2['F4'])} L365 runs + {2 * len(at2['F12']['cells'])} AT2 cells, max |dev| {dev5:.1e}", dev5 < 1e-12, load_bearing=False)
OUT["numbers"]["controls"] = dict(C1_rows=len(mine), C1_dev=dev1, C2=[ra_.tolist(), rf_.tolist()], C3=[dev3a, dev3b], C4=dev4, C5=dev5)

# ================================================================================================ F1 the surface at z = 2.5
banner("F1  THE FLUID'S SURFACE AT z = 2.5: stimulated front (K = C E_need) and spontaneous ignition (C), against r_F")
HOSTS = {}
for lMb in LMBS:
    for mf in MUFACS:
        H0_ = host(lMb, mf); Hp_ = halo_prof(H0_["Mh"], H0_["c"], Z0, H0_["Mb"], H0_["a"])
        rF = {f_: r_flag(H0_["Mb"], f_)[1] for f_ in FEET}
        fr = {}
        for vk in VKS_GATE:
            r_, S_ = depth_halo(Hp_, vk)
            fr[vk] = dict(rv={K: front(r_, S_, 1 / K) for K in KS}, ign={C: front(r_, S_, 1 / C) for C in CS}, S_rmin=float(S_[0]))
        H0_.update(prof=Hp_, rF=rF, fr=fr)
        HOSTS[(lMb, mf)] = H0_
        f6 = fr[600.0]
        P(f"    M_b 1e{lMb:<4} gas x{mf:.2f}: M_h {H0_['Mh']:.2e}, c {H0_['c']:.2f}, r200 {Hp_['r200']:6.1f} kpc; r_F/r200 "
          f"{rF['canonical'] / Hp_['r200']:.3f} (canonical) {rF['alt'] / Hp_['r200']:.3f} (alt); front r_s/r200 "
          + " ".join(f"K{K:.0f} {f6['rv'][K] / Hp_['r200']:.3f}" for K in KS) + "; spontaneous r/r200 "
          + " ".join(f"C{C} {f6['ign'][C] / Hp_['r200']:.3f}" for C in CS) + f"; S_c(r_min) {f6['S_rmin']:.1e}")
f1_ok = all(H0_["rF"][f_] < H0_["fr"][vk]["rv"][K] for H0_ in HOSTS.values() for f_ in FEET for vk in VKS_GATE for K in KS)
f1_ign = all(H0_["rF"][f_] < H0_["fr"][vk]["ign"][0.3] for H0_ in HOSTS.values() for f_ in FEET for vk in VKS_GATE)
OUT["numbers"]["F1"] = {f"{k_[0]}|{round(k_[1], 3)}": dict(Mh=v_["Mh"], c=v_["c"], r200=v_["prof"]["r200"], rF=v_["rF"],
                                                          front={str(vk): {str(K): x_ for K, x_ in d_["rv"].items()} for vk, d_ in v_["fr"].items()},
                                                          ignition={str(vk): {str(C): x_ for C, x_ in d_["ign"].items()} for vk, d_ in v_["fr"].items()},
                                                          S_rmin=v_["fr"][600.0]["S_rmin"]) for k_, v_ in HOSTS.items()}
check("F1 THE SURFACE: at z = 2.5 the flagship radius lies inside the fluid's stimulated front for every host (M_b 1e10-1e11.5, gas "
      "range), footing, K = 18-540 and v_k = 575-650", f"all inside: {f1_ok}; inside even the spontaneous region at C = 0.3: {f1_ign}; "
      f"front r_s/r200 {min(H_['fr'][vk]['rv'][K] / H_['prof']['r200'] for H_ in HOSTS.values() for vk in VKS_GATE for K in KS):.3f}-"
      f"{max(H_['fr'][vk]['rv'][K] / H_['prof']['r200'] for H_ in HOSTS.values() for vk in VKS_GATE for K in KS):.3f}; r_F/r200 "
      f"{min(H_['rF'][f_] / H_['prof']['r200'] for H_ in HOSTS.values() for f_ in FEET):.3f}-{max(H_['rF'][f_] / H_['prof']['r200'] for H_ in HOSTS.values() for f_ in FEET):.3f}",
      f1_ok, "the truncated profile puts the front just inside r200 (S_c(r200) = 0 by construction); with an infall region it "
      "would lie beyond.  The carrier at r_F has converted by z = 2.5 in every host: what remains is the daughters' retention")
P(f"    {el()}")

# ================================================================================================ F2 the passage
banner("F2  THE PASSAGE: when the front passed r_F in the main progenitor (M ~ exp(-alpha (z - 2.5))), and the intact progenitor's v_esc there")


class Prog:
    """the intact main progenitor on ZP: fronts r_s(z; v_k, K), Phi(RG) and sigma(RG) at every epoch."""

    def __init__(self, H0_, al, vks=VKS_GATE, floor=True):
        self.z = ZP; self.rs = {vk: {K: np.zeros(len(ZP)) for K in KS} for vk in vks}
        self.Phi = np.zeros((len(ZP), len(RG))); self.sig = np.zeros((len(ZP), len(RG))); self.r200 = np.zeros(len(ZP))
        self.Srmin = np.inf
        for iz, z in enumerate(ZP):
            M = H0_["Mh"] * math.exp(-al * (z - Z0))
            c = conc(M, z) if floor else float(c200_20(M, z))
            if iz == 0: c = H0_["c"]                                  # the host itself at z = 2.5
            Mbz, az = (H0_["Mb"], H0_["a"]) if iz == 0 else galaxy_baryons(M, z, H0_["mf"])
            Hq = halo_prof(M, c, z, Mbz, az)
            self.Phi[iz], self.sig[iz], self.r200[iz] = Hq["Phi"], Hq["sig"], Hq["r200"]
            for vk in vks:
                r_, S_ = depth_halo(Hq, vk, n_in=300)
                self.Srmin = min(self.Srmin, float(S_[0]))
                for K in KS: self.rs[vk][K][iz] = front(r_, S_, 1 / K)

    def mono(self):
        return all(bool(np.all(np.diff(a_) <= 1e-9)) for d_ in self.rs.values() for a_ in d_.values())

    def passage(self, rq, vk, K):
        """z_pass (first epoch with r_s >= r), the intact progenitor's v_esc and sigma there; r below the z = ZP[-1] front
        -> ZP[-1] (converted earlier still)."""
        rq = np.atleast_1d(np.asarray(rq, float)); rs = self.rs[vk][K]
        zp = np.interp(rq, rs[::-1], self.z[::-1])                    # rs decreases with z
        zp = np.where(rq <= rs[-1], self.z[-1], np.where(rq >= rs[0], self.z[0], zp))
        i = np.clip(np.searchsorted(self.z, zp, side="right") - 1, 0, len(self.z) - 2)
        t = np.clip((zp - self.z[i]) / (self.z[i + 1] - self.z[i]), 0.0, 1.0)
        j = np.clip(np.searchsorted(RG, rq) - 1, 0, len(RG) - 2); s = np.clip((rq - RG[j]) / (RG[j + 1] - RG[j]), 0.0, 1.0)
        bil = lambda T: (1 - t) * ((1 - s) * T[i, j] + s * T[i, j + 1]) + t * ((1 - s) * T[i + 1, j] + s * T[i + 1, j + 1])
        return zp, np.sqrt(np.maximum(-2 * bil(self.Phi), 0.0)), bil(self.sig)


PROG, GATE = {}, {}
for (lMb, mf), H0_ in HOSTS.items():
    for al in ALPHAS:
        pg = Prog(H0_, al); PROG[(lMb, mf, al)] = pg
        for vk in VKS_GATE:
            for K in KS:
                for f_ in FEET:
                    zp, ve, _ = pg.passage(H0_["rF"][f_], vk, K)
                    GATE[(lMb, mf, al, vk, K, f_)] = dict(z_pass=float(zp[0]), v_esc=float(ve[0]), escaped=bool(ve[0] < vk))
    rowsum = []
    for al in ALPHAS:
        g_ = [GATE[(lMb, mf, al, 600.0, K, f_)] for K in KS for f_ in FEET]
        rowsum.append(f"alpha {al}: z_pass {min(x_['z_pass'] for x_ in g_):.1f}-{max(x_['z_pass'] for x_ in g_):.1f}, v_esc(r_F) "
                      f"{min(x_['v_esc'] for x_ in g_):.0f}-{max(x_['v_esc'] for x_ in g_):.0f}")
    P(f"    M_b 1e{lMb:<4} gas x{mf:.2f} (v_k 600, K 18-540, both footings): " + "; ".join(rowsum) + f"   {el()}")
mono_all = all(pg.mono() for pg in PROG.values()); ign_min = min(pg.Srmin for pg in PROG.values())
rec_gate = [v_ for k_, v_ in GATE.items() if k_[0] in LMB_RECORD and k_[3] in (575.0, 600.0)]
g115 = [v_ for k_, v_ in GATE.items() if k_[0] == 11.5 and k_[3] in (575.0, 600.0)]
P(f"    fronts grow monotonically in physical radius with time in every progenitor: {mono_all}; the cusp ignites at every epoch "
  f"(min S_c(r_min) = {ign_min:.1e}, x C = 0.3 -> {0.3 * ign_min:.1e} >= 1)")
P(f"    record grid (M_b 1e10-1e11), v_k 575-600: v_esc(r_F) at the passage {min(x_['v_esc'] for x_ in rec_gate):.0f}-{max(x_['v_esc'] for x_ in rec_gate):.0f} km/s, "
  f"z_pass {min(x_['z_pass'] for x_ in rec_gate):.1f}-{max(x_['z_pass'] for x_ in rec_gate):.1f}; escaped at {sum(x_['escaped'] for x_ in rec_gate)}/{len(rec_gate)} cells")
if g115:
    P(f"    M_b 1e11.5: v_esc(r_F) {min(x_['v_esc'] for x_ in g115):.0f}-{max(x_['v_esc'] for x_ in g115):.0f} km/s; escaped at "
      f"{sum(x_['escaped'] for x_ in g115)}/{len(g115)} cells")
P(f"    at v_k = 650: escaped at {sum(v_['escaped'] for k_, v_ in GATE.items() if k_[3] == 650.0 and k_[0] in LMB_RECORD)}/"
  f"{sum(1 for k_ in GATE if k_[3] == 650.0 and k_[0] in LMB_RECORD)} record-grid cells and "
  f"{sum(v_['escaped'] for k_, v_ in GATE.items() if k_[3] == 650.0 and k_[0] == 11.5)}/{sum(1 for k_ in GATE if k_[3] == 650.0 and k_[0] == 11.5)} M_b 1e11.5 cells")
# no concentration floor (the record's pure extrapolation) at the central cell
nof = {}; AL_MID = ALPHAS[len(ALPHAS) // 2]; K_MID = 60.0 if 60.0 in KS else KS[0]
for (lMb, mf), H0_ in HOSTS.items():
    pg0 = Prog(H0_, AL_MID, vks=(600.0,), floor=False)
    for f_ in FEET:
        nof[(lMb, mf, f_)] = float(pg0.passage(H0_["rF"][f_], 600.0, K_MID)[1][0])
dnof = max(abs(nof[(k_[0], k_[1], f_)] - GATE[(k_[0], k_[1], AL_MID, 600.0, K_MID, f_)]["v_esc"]) for k_ in HOSTS for f_ in FEET)
P(f"    without the c >= 3 floor (alpha {AL_MID}, K {K_MID:.0f}, v_k 600): v_esc(r_F) changes by at most {dnof:.1f} km/s   {el()}")
# alpha_crit: the slowest growth at which the worst record host's daughters still escape (K = 18, v_k = 575)
worst = max(((k_[0], k_[1]) for k_ in HOSTS if k_[0] in LMB_RECORD),
            key=lambda k_: max(GATE[(k_[0], k_[1], ALPHAS[0], 575.0 if 575.0 in VKS_GATE else 600.0, KS[0], f_)]["v_esc"] for f_ in FEET))
vk_w = 575.0


def worst_ve(al):
    pg_ = Prog(HOSTS[worst], al, vks=(vk_w,))
    return max(float(pg_.passage(HOSTS[worst]["rF"][f_], vk_w, KS[0])[1][0]) for f_ in FEET)


lo_a, hi_a = 0.02, ALPHAS[0]
if worst_ve(lo_a) < vk_w:
    a_crit = f"< {lo_a}"
else:
    for _ in range(3 if SMOKE else 9):
        mid = 0.5 * (lo_a + hi_a)
        lo_a, hi_a = (lo_a, mid) if worst_ve(mid) < vk_w else (mid, hi_a)
    a_crit = f"{hi_a:.3f}"
P(f"    alpha_crit (worst record host M_b 1e{worst[0]} gas x{worst[1]:.2f}, K {KS[0]:.0f}, v_k 575): the daughters escape for "
  f"dlnM/dz magnitude >= {a_crit}   {el()}")
OUT["numbers"]["F2"] = dict(gate={"|".join(str(round(x_, 3)) if isinstance(x_, float) else str(x_) for x_ in k_): v_ for k_, v_ in GATE.items()},
                            monotone=mono_all, ignition_min=ign_min, no_floor_max_dv=dnof, alpha_crit=a_crit, worst_host=list(worst))
check("F2 (reported) THE PASSAGE: fronts monotone in time; the cusp ignites at every progenitor epoch; z_pass(r_F) and v_esc(r_F)",
      f"monotone {mono_all}; min S_c(r_min) {ign_min:.1e}; record grid v_esc(r_F) {min(x_['v_esc'] for x_ in rec_gate):.0f}-"
      f"{max(x_['v_esc'] for x_ in rec_gate):.0f} km/s at z_pass {min(x_['z_pass'] for x_ in rec_gate):.1f}-{max(x_['z_pass'] for x_ in rec_gate):.1f} "
      f"({sum(x_['escaped'] for x_ in rec_gate)}/{len(rec_gate)} escaped); alpha_crit {a_crit}", mono_all and 0.3 * ign_min >= 1,
      load_bearing=False)

# ================================================================================================ the retention grid
banner("A  RETENTION AT r_F (z = 2.5): in place (AT1's rule) and surface-only (the in-place population gone), two potential readings")
RET = {}
for (lMb, mf), H0_ in HOSTS.items():
    Mb_fn = hernquist(H0_["Mb"], H0_["a"]); gates = [H0_["rF"][f_] for f_ in FEET]
    for vk in VKS_RET:
        for K in KS:
            rv = H0_["fr"][vk]["rv"][K]
            d_ = {}
            for rd, it in (("self", 2), ("intact", 0)):
                s_in, flc, inf_in = retained_fluid(Mb_fn, H0_["Mh"], H0_["c"], gates, rv, vk, H0_["rhoc"], N=N_RET, iters=it)
                s_en, _, inf_en = retained_fluid(Mb_fn, H0_["Mh"], H0_["c"], gates, rv, vk, H0_["rhoc"], N=N_RET, iters=it,
                                                 keep=lambda r_, rp_: np.zeros_like(r_))
                d_[rd] = dict(inplace=dict(zip(FEET, s_in.tolist())), surface=dict(zip(FEET, s_en.tolist())))
            d_.update(rv=rv, loss_cone=flc, n_inplace=inf_in["n_inplace"], n_entry=inf_in["n_entry"])
            RET[(lMb, mf, vk, K)] = d_
        P(f"    M_b 1e{lMb:<4} gas x{mf:.2f} v_k {vk:.0f}: in place S (self / intact) "
          + " ".join(f"K{K:.0f} {RET[(lMb, mf, vk, K)]['self']['inplace']['canonical']:.4f}/{RET[(lMb, mf, vk, K)]['intact']['inplace']['canonical']:.4f}" for K in KS)
          + "; surface-only " + " ".join(f"{RET[(lMb, mf, vk, K)]['self']['surface']['canonical']:.4f}/{RET[(lMb, mf, vk, K)]['intact']['surface']['canonical']:.4f}" for K in KS)
          + f" (canonical)   {el()}")
OUT["numbers"]["RET"] = {f"{k_[0]}|{round(k_[1], 3)}|{k_[2]}|{k_[3]}": v_ for k_, v_ in RET.items()}

# ------------------------------------------------------------------------------------------------ G1 rows
ROWS = []
for (lMb, mf, vk, K), d_ in RET.items():
    H0_ = HOSTS[(lMb, mf)]
    for al in ALPHAS:
        for f_ in FEET:
            g_ = GATE[(lMb, mf, al, vk, K, f_)]
            use = "inplace" if (MUTATE or not g_["escaped"]) else "surface"
            for rd in ("self", "intact"):
                S = d_[rd][use][f_]
                sh = {kn: flag_shift(Z0, H0_["Mb"], H0_["Mh"], f_, S, nuf) for kn, nuf in KERNELS}
                ROWS.append(dict(lMb=lMb, mf=round(mf, 3), vk=vk, K=K, alpha=al, foot=f_, reading=rd, escaped=g_["escaped"], used=use,
                                 z_pass=g_["z_pass"], v_esc_pass=g_["v_esc"], S=S, shift_l320=sh["l320"], shift_mono=sh["mono"]))
OUT["numbers"]["G1_rows"] = ROWS


def worst_of(rows):
    return (max(r_["S"] for r_ in rows), max(max(abs(r_["shift_l320"]), abs(r_["shift_mono"])) for r_ in rows)) if rows else (float("nan"), float("nan"))


rec = [r_ for r_ in ROWS if r_["lMb"] in LMB_RECORD]
S_rec, sh_rec = worst_of(rec)
S_rec_self, sh_rec_self = worst_of([r_ for r_ in rec if r_["reading"] == "self"])
S_rec_int, sh_rec_int = worst_of([r_ for r_ in rec if r_["reading"] == "intact"])
P("\n    G1 (the design's gate) on the record's grid, worst over gas x1/1.5-1.5, both footings, K, alpha, v_k, both kernels:")
for lMb in LMB_RECORD:
    for rd in ("self", "intact"):
        s_, h_ = worst_of([r_ for r_ in rec if r_["lMb"] == lMb and r_["reading"] == rd])
        P(f"      M_b 1e{lMb:<4} ({rd:6s} potential): max S at r_F {s_:.5f}, max |shift| {h_:.4f} dex")
esc_rows = [r_ for r_ in ROWS if r_["escaped"]]
S_esc, sh_esc = worst_of(esc_rows)
e115 = [r_ for r_ in esc_rows if r_["lMb"] == 11.5]
S_e115, sh_e115 = worst_of(e115)
a1 = (S_rec <= S_MAX) and (sh_rec <= SHIFT_MAX)
check("A1 = H-A1 (strict): on the record's grid (M_b 1e10-1e11, gas x1/1.5-1.5, both footings, both kernels) with the design's "
      "progenitor gate, S at r_F <= 0.059 and |shift| <= 0.10 dex over K = 18-540, alpha = 0.6-1.0, v_k = 575-600, in BOTH "
      "readings of the potential's response", f"max S {S_rec:.5f} (self-consistent {S_rec_self:.5f}, intact {S_rec_int:.5f}); "
      f"max |shift| {sh_rec:.4f} dex (self {sh_rec_self:.4f}, intact {sh_rec_int:.4f}); gate escaped at "
      f"{sum(r_['escaped'] for r_ in rec)}/{len(rec)} rows", a1 == EXPECT["A1"],
      "the front passed r_F at z ~ 4-7 when the progenitor's v_esc(r_F) was below the kick; the surface daughters at ~r200 "
      "escape; nothing at r_F is left to retain")
a2 = bool(esc_rows) and (S_esc <= S_MAX) and (sh_esc <= SHIFT_MAX) and (bool(e115) if 11.5 in LMBS else True)
check("A2 THE EARLY-ESCAPE STEP: at every cell where the progenitor gate escapes -- including the M_b = 1e11.5 hosts that in-place "
      "conversion leaves loaded -- S at r_F <= 0.059 and |shift| <= 0.10 dex in both readings",
      f"{len(esc_rows)} escaped rows: max S {S_esc:.5f}, max |shift| {sh_esc:.4f}; of them M_b 1e11.5: {len(e115)} rows, max S "
      f"{S_e115:.5f}, max |shift| {sh_e115:.4f}", a2 == EXPECT["A2"],
      "what the step removes is exactly the retained carrier the in-place reading leaves (MUTATE keeps it)")
inpl_rec = {rd: max(RET[k_][rd]["inplace"][f_] for k_ in RET if k_[0] in LMB_RECORD for f_ in FEET) for rd in ("self", "intact")}
inpl_sh = {rd: max(max(abs(flag_shift(Z0, HOSTS[(k_[0], k_[1])]["Mb"], HOSTS[(k_[0], k_[1])]["Mh"], f_, RET[k_][rd]["inplace"][f_], nuf))
                       for kn, nuf in KERNELS) for k_ in RET if k_[0] in LMB_RECORD for f_ in FEET) for rd in ("self", "intact")}
t1 = inpl_rec["self"] > S_MAX or inpl_sh["self"] > SHIFT_MAX
check("T1 = H-A2 (pre-declared, reported as it falls): the in-place population kept (AT1's rule at the fluid's surface, no early "
      "escape) fails the flagship on the record's grid in AT1's own self-consistent reading (designer: S ~ 0.1-0.2)",
      f"in place, record grid: max S {inpl_rec['self']:.4f} / max |shift| {inpl_sh['self']:.3f} dex (self-consistent, AT1's reading); "
      f"{inpl_rec['intact']:.4f} / {inpl_sh['intact']:.3f} dex (intact potential held fixed)", t1 == EXPECT["T1"],
      "in AT1's machinery the daughters born in place escape once the converted carrier's own mass has left the well; the "
      "designer's L388-like S appears only if the intact well is held fixed", load_bearing=False)
OUT["numbers"]["A_summary"] = dict(record=dict(S=S_rec, shift=sh_rec, S_self=S_rec_self, S_intact=S_rec_int), escaped=dict(S=S_esc, shift=sh_esc),
                                   e115=dict(S=S_e115, shift=sh_e115, n=len(e115)), inplace_record=inpl_rec, inplace_record_shift=inpl_sh)
P(f"    {el()}")

# ------------------------------------------------------------------------------------------------ A3 G2 per-particle
banner("A3  (reported) G2: each in-place particle kept with 1 - P_esc at the front's passage of its pericentre (v_k 600)")
G2 = {}
for (lMb, mf), H0_ in HOSTS.items():
    Mb_fn = hernquist(H0_["Mb"], H0_["a"]); gates = [H0_["rF"][f_] for f_ in FEET]
    for K in K_G2:
        rv = H0_["fr"][600.0]["rv"][K]
        for al in ALPHAS:
            pg = PROG[(lMb, mf, al)]

            def keep(r_, rp_, pg=pg, K=K):
                if MUTATE: return np.ones_like(r_)
                _, ve, sg = pg.passage(rp_, 600.0, K)
                ve = np.maximum(ve, 1e-3)
                return 1.0 - PESC(np.stack([np.clip(600.0 / ve, 0.0, UGmax), np.clip(sg / ve, SGmin, SGmax)], -1))

            out_ = {}
            for rd, it in (("self", 2), ("intact", 0)):
                s_, _, inf_ = retained_fluid(Mb_fn, H0_["Mh"], H0_["c"], gates, rv, 600.0, H0_["rhoc"], keep=keep, N=N_RET, iters=it)
                out_[rd] = dict(zip(FEET, s_.tolist())); out_["kept_frac"] = inf_["kept_inplace"] / max(inf_["n_inplace"], 1)
            G2[(lMb, mf, K, al)] = out_
    P(f"    M_b 1e{lMb:<4} gas x{mf:.2f}: G2 S at r_F (self/intact, canonical) " + " ".join(
        f"K{K:.0f} a{al}: {G2[(lMb, mf, K, al)]['self']['canonical']:.4f}/{G2[(lMb, mf, K, al)]['intact']['canonical']:.4f}"
        for K in K_G2 for al in ALPHAS) + f"; in-place kept fraction <= {max(G2[(lMb, mf, K, al)]['kept_frac'] for K in K_G2 for al in ALPHAS):.3f}   {el()}")
OUT["numbers"]["G2"] = {f"{k_[0]}|{round(k_[1], 3)}|{k_[2]}|{k_[3]}": v_ for k_, v_ in G2.items()}
g2_rec = max(v_[rd][f_] for k_, v_ in G2.items() if k_[0] in LMB_RECORD for rd in ("self", "intact") for f_ in FEET)
g2_115 = [v_[rd][f_] for k_, v_ in G2.items() if k_[0] == 11.5 for rd in ("self", "intact") for f_ in FEET]
check("A3 (reported) G2, the per-particle refinement: S at r_F", f"record grid max {g2_rec:.5f}; M_b 1e11.5 "
      + (f"{min(g2_115):.4f}-{max(g2_115):.4f}" if g2_115 else "n/a"), True, load_bearing=False)

# ------------------------------------------------------------------------------------------------ A4 the 1e11.5 extension
banner("A4  (reported) THE M_b = 1e11.5 EXTENSION under G1: cell by cell")
A4 = {}
for mf in MUFACS:
    rows_ = [r_ for r_ in ROWS if r_["lMb"] == 11.5 and abs(r_["mf"] - round(mf, 3)) < 1e-9]
    if not rows_: continue
    npass = sum(1 for r_ in rows_ if r_["S"] <= S_MAX and max(abs(r_["shift_l320"]), abs(r_["shift_mono"])) <= SHIFT_MAX)
    A4[round(mf, 3)] = dict(M_h=HOSTS[(11.5, mf)]["Mh"], n=len(rows_), n_pass=npass, S_max=max(r_["S"] for r_ in rows_),
                            shift_max=max(max(abs(r_["shift_l320"]), abs(r_["shift_mono"])) for r_ in rows_),
                            v_esc_pass=[min(r_["v_esc_pass"] for r_ in rows_), max(r_["v_esc_pass"] for r_ in rows_)])
    P(f"    gas x{mf:.2f} (M_h {A4[round(mf, 3)]['M_h']:.2e}): {npass}/{len(rows_)} rows pass; v_esc(r_F) at passage "
      f"{A4[round(mf, 3)]['v_esc_pass'][0]:.0f}-{A4[round(mf, 3)]['v_esc_pass'][1]:.0f} km/s; worst S {A4[round(mf, 3)]['S_max']:.3f}, "
      f"worst |shift| {A4[round(mf, 3)]['shift_max']:.3f} dex")
OUT["numbers"]["A4"] = {str(k_): v_ for k_, v_ in A4.items()}
check("A4 (reported) M_b = 1e11.5 (outside MS2's flagship grid) under G1", {k_: f"{v_['n_pass']}/{v_['n']} pass" for k_, v_ in A4.items()},
      True, load_bearing=False)

# ================================================================================================ B the early conversion budget
banner("B  THE EARLY CONVERSION BUDGET F(z): every halo's own cusp, the fluid's front, minihalos to the fluid's scale")
ZB = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0] if not SMOKE else [2.0, 3.0, 4.0, 6.0, 10.0]
M22 = {"2e-19 eV": 2000.0, "1e-18 eV": 1e4}


def supp_fdm(M, m22):                                                 # Schive+2016 halo-mass-function suppression
    M0 = 1.6e10 * m22 ** (-4.0 / 3.0)
    return (1 + (M / M0) ** -1.1) ** -2.2


def r_core(M, z, m22):                                                # Schive+2014 soliton radius [kpc]
    om = Om_z(z); zeta = lambda o: (18 * math.pi ** 2 + 82 * (o - 1) - 39 * (o - 1) ** 2) / o
    return 1.6 / m22 * (1 + z) ** -0.5 * (zeta(om) / zeta(Om)) ** (-1 / 6) * (M / 1e9) ** (-1 / 3)


CUTS = {"fluid m = 2e-19 eV": lambda M: supp_fdm(M, M22["2e-19 eV"]), "fluid m = 1e-18 eV": lambda M: supp_fdm(M, M22["1e-18 eV"]),
        "grid floor 1.5e5 Msun (heavier m)": lambda M: np.ones_like(M), "record M_min = 1e8 (most favourable)": lambda M: (M >= 1e8).astype(float)}
BZ = {}
ign_fail = 0; ign_min_B = np.inf; IGN_FAIL = []; HI_SPLIT = {}
for z in ZB:
    s = SIG0 * DG(z); nu = DC / s
    w = f_st(nu) * np.abs(np.gradient(nu, np.log(MH))); bb = b_st(nu)
    Mh_ = MH / h
    fconv = {K: np.zeros(len(MH)) for K in KS}; pesc = {K: np.zeros(len(MH)) for K in KS}
    for i in range(len(MH)):
        if w[i] < 1e-12: continue
        c = max(float(c_dm14(MH[i], z)), C_FLOOR)
        Mb, a = galaxy_baryons(Mh_[i], z, 1.0)
        Hq = halo_prof(Mh_[i], c, z, Mb, a)
        r_, S_ = depth_halo(Hq, 600.0, n_in=260)
        rc = max(r_core(Mh_[i], z, M22["2e-19 eV"]), r_[0])
        s_c = float(np.interp(math.log(rc), np.log(r_), S_))
        ign_min_B = min(ign_min_B, 0.3 * s_c)
        if 0.3 * s_c < 1: ign_fail += 1; IGN_FAIL.append((z, float(Mh_[i])))
        ve = np.sqrt(np.maximum(-2 * np.interp(r_, RG, Hq["Phi"]), 1e-6)); sg = np.interp(r_, RG, Hq["sig"])
        pe = PESC(np.stack([np.clip(600.0 / ve, 0.0, UGmax), np.clip(sg / ve, SGmin, SGmax)], -1))
        dm = Hq["rho_s"] / ((r_ / Hq["rs"]) * (1 + r_ / Hq["rs"]) ** 2) * r_ ** 3              # dM / d ln r
        for K in KS:
            rsK = front(r_, S_, 1 / K)
            fconv[K][i] = float(mfn(rsK / Hq["rs"]) / mfn(c)) if (rsK > 0 and 0.3 * s_c >= 1) else 0.0
            sel = r_ <= rsK
            pesc[K][i] = float(_trap((dm * pe)[sel], np.log(r_[sel])) / max(_trap(dm[sel], np.log(r_[sel])), 1e-300)) if sel.sum() > 1 else 1.0
    _Kf = 60.0 if 60.0 in KS else KS[0]; _sp = CUTS["fluid m = 2e-19 eV"](Mh_)
    HI_SPLIT[z] = float(_trap(w * fconv[_Kf] * _sp * (Mh_ >= 10 ** 10.5), np.log(MH)) / max(_trap(w * fconv[_Kf] * _sp, np.log(MH)), 1e-300))
    BZ[z] = {}
    for cn, cf in CUTS.items():
        sp = cf(Mh_)
        for K in KS:
            BZ[z][(cn, K)] = dict(F=float(_trap(w * fconv[K] * sp, np.log(MH))), Fb_esc=float(_trap(w * bb * fconv[K] * pesc[K] * sp, np.log(MH))),
                                  coll=float(_trap(w * sp, np.log(MH))))
    P(f"    z = {z:4.1f}: converted fraction of the carrier F(z) [m = 2e-19 eV; K 18/60/540] "
      + "/".join(f"{BZ[z][('fluid m = 2e-19 eV', K)]['F']:.3f}" for K in KS if K in (18.0, 60.0, 540.0))
      + f"  (collapsed above the fluid's scale {BZ[z][('fluid m = 2e-19 eV', KS[0])]['coll']:.3f}); record cut 1e8, K 18: "
      f"{BZ[z][('record M_min = 1e8 (most favourable)', KS[0])]['F']:.3f}   {el()}")
HIST = {}
for key in BZ[ZB[0]]:
    Fi = np.array([BZ[z][key]["F"] for z in ZB]); Fb = np.array([BZ[z][key]["Fb_esc"] for z in ZB])
    order = np.argsort(ZB)[::-1]                                      # from high z to low z
    zs_desc = np.array(ZB)[order]
    run_F = np.maximum.accumulate(Fi[order]); run_Fb = np.maximum.accumulate(Fb[order])      # irreversible
    HIST[key] = {float(z_): (float(a_), float(b_)) for z_, a_, b_ in zip(zs_desc, run_F, run_Fb)}
at1B1 = at1["numbers"]["B1"]["0.1|600.0"]
zb1 = np.array(at1B1["z"]); ft1 = np.array(at1B1["F_trig_unweighted"]); fe1 = np.array(at1B1["F_b_escaped"])
AT1F = {z_: float(np.interp(z_, zb1, ft1)) for z_ in (4.0, 3.0, 2.0)}; AT1Fb = {z_: float(np.interp(z_, zb1, fe1)) for z_ in (4.0, 3.0, 2.0)}
P("\n    the running (irreversible) budget, unweighted converted fraction F and bias-weighted escaped F_b, at z = 4 / 3 / 2:")
for cn in CUTS:
    for K in KS:
        if K not in (KS[0], 60.0, KS[-1]): continue
        hh = HIST[(cn, K)]
        P(f"      {cn:38s} K {K:4.0f}: F {hh[4.0][0]:.3f}/{hh[3.0][0]:.3f}/{hh[2.0][0]:.3f}; F_b,esc {hh[4.0][1]:.3f}/{hh[3.0][1]:.3f}/{hh[2.0][1]:.3f}")
P(f"      AT1's A2 cell (y_v 0.1, v_A 600; what AT2 scored): F_trig {AT1F[4.0]:.3f}/{AT1F[3.0]:.3f}/{AT1F[2.0]:.3f}; "
  f"F_b,esc {AT1Fb[4.0]:.3f}/{AT1Fb[3.0]:.3f}/{AT1Fb[2.0]:.3f}")
P(f"    ignition at the soliton core (m = 2e-19 eV, C = 0.3): fails in {ign_fail} halo evaluations"
  + (f" (z = {sorted(set(z_ for z_, _ in IGN_FAIL))}, M_h {min(m_ for _, m_ in IGN_FAIL):.1e}-{max(m_ for _, m_ in IGN_FAIL):.1e} Msun; counted "
     f"unconverted)" if IGN_FAIL else "") + f"; min C S_c(r_core) {ign_min_B:.1e}")
P("    mass selectivity (fiducial m = 2e-19 eV, K = 60): the share of the converted carrier in hosts >= 1e10.5 Msun is "
  + ", ".join(f"{HI_SPLIT[z_]:.3f} (z = {z_:g})" for z_ in (4.0, 3.0, 2.0) if z_ in HI_SPLIT) + "  [AT1's acceleration trigger: >= 0.98 at z = 2-3]")
fav = HIST[("record M_min = 1e8 (most favourable)", KS[0])]; fid = HIST[("fluid m = 2e-19 eV", 60.0 if 60.0 in KS else KS[0])]
b1 = fav[3.0][0] > AT1F[3.0] and fav[2.0][0] > AT1F[2.0]
OUT["numbers"]["B"] = dict(inst={str(z_): {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in d_.items()} for z_, d_ in BZ.items()},
                           history={f"{k_[0]}|{k_[1]}": {str(z_): v_ for z_, v_ in d_.items()} for k_, d_ in HIST.items()},
                           AT1_A2cell=dict(F_trig=AT1F, F_b_esc=AT1Fb), ignition_fail=ign_fail, ignition_min=ign_min_B,
                           ignition_fail_where=IGN_FAIL, share_above_1e10p5={str(z_): v_ for z_, v_ in HI_SPLIT.items()})
check("B1 = H-B: the fluid's early conversion budget exceeds the one AT2 scored (AT1's A2 cell) at z = 3 and 2 even at the most "
      "favourable corner (K = 18, the record's M_min = 1e8 cut)",
      f"most favourable F(4/3/2) = {fav[4.0][0]:.3f}/{fav[3.0][0]:.3f}/{fav[2.0][0]:.3f} ({fav[3.0][0] / AT1F[3.0]:.1f}x / {fav[2.0][0] / AT1F[2.0]:.1f}x "
      f"AT1's {AT1F[3.0]:.3f}/{AT1F[2.0]:.3f}); fiducial (m = 2e-19 eV, K = 60) {fid[4.0][0]:.3f}/{fid[3.0][0]:.3f}/{fid[2.0][0]:.3f}",
      b1 == EXPECT["B1"], "the gate's threshold in rho_crit(z) units, (5/3) E^2 = 15 / 35 / 66 at z = 2 / 3 / 4, lies below every "
      "halo's mean density (200 rho_crit) for z <~ 6: at z <~ 4 every halo above the fluid's scale converts almost whole, so the "
      "budget tracks the collapsed fraction, not the massive hosts")

# ------------------------------------------------------------------------------------------------ B2 the forest bound
banner("B2  (reported) A CONSERVATIVE FOREST BOUND from the committed particle-mesh responses (no particle-mesh run here)")
resp = []                                                             # (label, rule/F(2), bandmax/F(2), F(2))
for ck, cv in at2["F12"]["cells"].items():
    if ck.endswith("|600.0"): resp.append((f"AT2 densest {ck}", cv["l365_rule"] / cv["decayed"][1], cv["flux_max_z2"] / cv["decayed"][1], cv["decayed"][1]))
for ck, cv in at2m["F12"]["cells"].items():
    if ck.endswith("|600.0"): resp.append((f"AT2 sparsest {ck}", cv["l365_rule"] / cv["decayed"][1], cv["flux_max_z2"] / cv["decayed"][1], cv["decayed"][1]))
for rk, rv_ in at2["F4"].items():
    if int(rk.split("_v")[1]) <= 700: resp.append((f"L365 {rk}", rv_["l365_rule"] / rv_["decayed"][1], rv_["flux_max"] / rv_["decayed"][1], rv_["decayed"][1]))
rlo, rhi = min(x_[1] for x_ in resp), max(x_[1] for x_ in resp)
Fmax_committed = max(x_[3] for x_ in resp)
proj = {key: (HIST[key][2.0][0] * rlo, HIST[key][2.0][0] * rhi) for key in ((("record M_min = 1e8 (most favourable)", KS[0])),
                                                                        (("fluid m = 2e-19 eV", 60.0 if 60.0 in KS else KS[0])))}
for x_ in resp: P(f"      {x_[0]:28s}: F(2) {x_[3]:.3f}; L365 rule per unit F(2) {x_[1]:.3f}; band max per unit F(2) {x_[2]:.3f}")
for key, (lo_, hi_) in proj.items():
    P(f"    projected L365 rule at z = 2 for {key[0]}, K {key[1]:.0f} (F(2) = {HIST[key][2.0][0]:.3f}): {lo_:.3f}-{hi_:.3f} (gate 0.10)")
P(f"    the largest committed particle-mesh budget is F(2) = {Fmax_committed:.3f}: every projection above is an EXTRAPOLATION")
OUT["numbers"]["B2"] = dict(responses=resp, rule_per_F2=[rlo, rhi], F2_max_committed=Fmax_committed,
                            projection={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in proj.items()})
check("B2 (reported) the forest bound: AT2's regime does not carry over; the projected L365 rule at the fluid's F(2)",
      {f"{k_[0]}|K{k_[1]:.0f}": f"{v_[0]:.3f}-{v_[1]:.3f}" for k_, v_ in proj.items()}, True, load_bearing=False)

# ------------------------------------------------------------------------------------------------ B3 the web flag
banner("B3  (reported flag) THE DESIGN'S STIMULATED CRITERION IN THE HUBBLE FLOW: gain (rho/rho_bg)^2 E_need >= 1 e-fold")
B3 = {}
for En in (60.0, 180.0):
    zz = np.linspace(0.0, 6.0, 6001); dts = np.array([delta_t(z_) for z_ in zz])
    zbg = float(zz[np.argmax(dts >= math.sqrt(En))]) if (dts >= math.sqrt(En)).any() else float("nan")
    B3[En] = dict(delta_stim={z_: delta_t(z_) / math.sqrt(En) - 1 for z_ in (2.0, 3.0, 4.0)},
                  delta_stim_3efold={z_: delta_t(z_) * math.sqrt(3 / En) - 1 for z_ in (2.0, 3.0, 4.0)}, z_mean_stimulable_below=zbg)
    P(f"    E_need {En:.0f}: the web meets the stimulated criterion above delta = " + ", ".join(f"{B3[En]['delta_stim'][z_]:.2f} (z = {z_:.0f})" for z_ in (2.0, 3.0, 4.0))
      + f" [3 e-folds: " + ", ".join(f"{B3[En]['delta_stim_3efold'][z_]:.2f}" for z_ in (2.0, 3.0, 4.0)) + f"]; the MEAN density meets it below z = {zbg:.2f}")
OUT["numbers"]["B3"] = {str(k_): v_ for k_, v_ in B3.items()}
check("B3 (reported flag) the stimulated criterion in the Hubble flow reaches filament densities at z = 2-4 and the mean density "
      "at low z; the halo model above does not score the web", {k_: v_["z_mean_stimulable_below"] for k_, v_ in B3.items()}, True,
      "whether seeds from converted halos actually drive a front through the web (the gain needed is ln(pump/seed), not 1) is "
      "not computed here; if it does, F(z) above is a LOWER bound", load_bearing=False)

# ================================================================================================ verdict
banner("VERDICT")
P(f"""  PART A (the flagship at z = 2.5).  The fluid's stimulated front sits at {min(H_['fr'][vk]['rv'][K] / H_['prof']['r200'] for H_ in HOSTS.values() for vk in VKS_GATE for K in KS):.2f}-{max(H_['fr'][vk]['rv'][K] / H_['prof']['r200'] for H_ in HOSTS.values() for vk in VKS_GATE for K in KS):.2f} r200 in every flagship host,
  far outside r_F.  In the main progenitor the front passed r_F at z = {min(x_['z_pass'] for x_ in rec_gate):.1f}-{max(x_['z_pass'] for x_ in rec_gate):.1f}, when the intact progenitor's
  v_esc(r_F) was {min(x_['v_esc'] for x_ in rec_gate):.0f}-{max(x_['v_esc'] for x_ in rec_gate):.0f} km/s (M_b 1e10-1e11), below every kick in 575-650: the in-place population left then.
  With the design's gate the retained carrier at r_F on the record's grid is S <= {S_rec:.5f} (both potential readings), the
  flagship shift <= {sh_rec:.4f} dex: {'PASS' if (S_rec <= S_MAX and sh_rec <= SHIFT_MAX) else 'FAIL'} against S <= 0.059 and 0.10 dex{' (MUTATE: the in-place population kept)' if MUTATE else ''}.
  The trap: kept in place, S = {inpl_rec['self']:.4f} in AT1's self-consistent reading but {inpl_rec['intact']:.3f} with the intact well held
  fixed -- the designer's L388-like number.  The early escape is what makes the pass independent of that unresolved response.
  M_b = 1e11.5 (outside MS2's grid): {', '.join(f"gas x{k_}: {v_['n_pass']}/{v_['n']}" for k_, v_ in A4.items())} rows pass; its progenitor's v_esc(r_F) reaches
  {max((v_['v_esc_pass'][1] for v_ in A4.values()), default=float('nan')):.0f} km/s.
  PART B (the forest).  Not mass-selective: by z = 3 / 2 the fluid has converted F = {fid[3.0][0]:.2f} / {fid[2.0][0]:.2f} of the carrier (m = 2e-19 eV,
  K = 60; >= {fav[3.0][0]:.2f} / {fav[2.0][0]:.2f} at the most favourable corner), {fav[3.0][0] / AT1F[3.0]:.0f}x / {fav[2.0][0] / AT1F[2.0]:.0f}x AT1's cell that AT2 scored.  AT2's
  <= 0.33% / 1.7% does not carry over; the committed responses project an L365 rule of {min(v_[0] for v_ in proj.values()):.2f}-{max(v_[1] for v_ in proj.values()):.2f} at z = 2
  (an extrapolation past the committed F(2) <= {Fmax_committed:.2f}).  Forest: NOT established; a particle-mesh run with this budget is the
  owner's call.  Flag: the design's stimulated criterion reaches filament densities at z = 2-4 (B3).""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["expect"], OUT["runtime_s"] = len(CH), n_fail, EXPECT, time.time() - T0
fn = os.path.join(OUTDIR, f"{SLUG}_results{'_SMOKE' if SMOKE else ''}{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: (o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating,)) else str(o))))
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}   {el()}")
sys.exit(0 if n_fail == 0 else 1)
