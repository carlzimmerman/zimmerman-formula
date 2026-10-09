#!/usr/bin/env python3
"""CFG522 -- the Local Group timing miss of CFG515 (d): data re-check (D1-D6), mechanisms (M1 shared catchment, M2 extended-body
mutual force, M3 law between the pair [reference], M4 time dependence [scope + reported bracket]), verdict per FROZEN_CRITERIA.md
(committed alone first, d38a869bc).
CFG515's cfg515_mw.py is executed read-only up to its CFG513 cross-check (it in turn executes CFG513's script read-only): this gives
the Prof class (nu_mono phantom = settled cold energy, numeric edge), the CFG513 radial timing integrator, the Fritz+18 satellites
and CFG515's cell() (the strict statistic).  kappa = 1/2 FITTED; footings never pooled; a0 flat.  External numbers are PROVISIONAL
literature recalls (FROZEN_CRITERIA.md section 1); nothing is downloaded.
MUTATE (CFG522_MUTATE=1): T1 M31 x 0.3, T2 law-on between the halos on top of cold energy, T3 double-counted supply; each must FAIL.
Run: nice -n 10 python3 campaign_fresh_gravity/CFG522_local_group_timing/cfg522_lg_timing.py   (CFG522_MUTATE=1 for the control)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import io, math, json, time, contextlib, hashlib
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
D515 = os.path.join(LANES, "CFG515_census_edge_resolution")
sys.path.insert(0, D515); sys.path.insert(0, LANES)
import cfg515_lib as L                                                       # noqa: E402
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG522_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK, RES = [], {}, {"lane": "CFG522", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
P(f"  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(os.path.join(HERE, 'FROZEN_CRITERIA.md'), 'rb').read()).hexdigest()}")

# ------------------------------------------------------------------ CFG515 (d) machinery, read-only
p515 = os.path.join(D515, "cfg515_mw.py")
src = open(p515).read()
mk = "J513 = json.load("
assert src.count(mk) == 1
_e = os.environ.pop("CFG515_MUTATE", None)
NS = {"__file__": p515, "__name__": "cfg515_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(mk)], "cfg515_ro", "exec"), NS)
if _e is not None:
    os.environ["CFG515_MUTATE"] = _e
Prof, G, FOOTS, GYR, H0, OM_L = NS["Prof"], NS["G"], NS["FOOTS"], NS["GYR"], NS["H0"], NS["OM_L"]
MB_PRIM, MB_HI, MB_M31, D_LG, VR_LG, EVR_LG, T0U = NS["MB_PRIM"], NS["MB_HI"], NS["MB_M31"], NS["D_LG"], NS["VR_LG"], NS["EVR_LG"], NS["T0U"]
cell515 = NS["cell"]
A0 = NS["NS"]["A0"]
nu_mono = NS["NS"]["nu_mono"]
COLD = L.COLD_PER_B
VT_SAL, EVT_SAL = 82.4, 31.2
D_VDM, ED_VDM = 770.0, 40.0


# ------------------------------------------------------------------ fast tabulated two-body machinery
class Pair:
    """MW (extended baryons) + M31 (point baryons), each with its own cold energy profile; G M_eff(d) table for the timing."""

    def __init__(self, foot, Mb_mw, f_mw, Mb_m31, f_m31, mutual=False):
        self.foot = foot
        self.mw = Prof("mw", Mb=Mb_mw, foot=foot, fret=f_mw)
        self.m31 = Prof("m31", Mb=Mb_m31, foot=foot, fret=f_m31, point=True)
        self.M1 = self.mw.Mb_tot() + self.mw.Mcold
        self.M2 = self.m31.Mb_tot() + self.m31.Mcold
        self.ld = np.linspace(-1.5, 3.8, 1400)
        d = 10 ** self.ld
        self.Mb_sc = self.mw.Mb_enc(d) + self.m31.Mb_enc(d)
        self.Mc_sc = self.mw.Mdark(d) + self.m31.Mdark(d)
        self.mutual = mutual
        if mutual:
            ldm = np.linspace(-0.3, 3.6, 160)
            meff = np.array([self.F(10 ** x) * (1 / self.M1 + 1 / self.M2) * (10 ** x) ** 2 / G for x in ldm])
            self.Meff_mut = np.interp(self.ld, ldm, meff)

    def shells(self, prof, n=700):
        r = np.concatenate([[0.0], np.geomspace(1e-2, prof.redge * 1.0000001, n)])
        M = prof.M_enc(np.maximum(r, 1e-12)); M[0] = M[1]                         # mass inside 0.01 kpc placed at the centre
        s = np.concatenate([[0.0], np.sqrt(r[1:-1] * r[2:])]); m = np.concatenate([[M[0]], np.diff(M[1:])])
        return s, m

    def F(self, d):
        """exact rigid-body mutual force of the two spherical bodies at separation d (Newton's theorem, shell-by-shell)."""
        r1, m1 = self.shells(self.mw); s2, m2 = self.shells(self.m31)
        R = r1[:, None]; S = s2[None, :]
        Sp = np.maximum(S, 1e-12)
        ulo = np.maximum(np.abs(d - Sp), R); uhi = d + Sp
        U = lambda u: u - (d * d - Sp * Sp) / u
        K = np.where(ulo < uhi, (U(uhi) - U(np.minimum(ulo, uhi))) / (4 * d * d * Sp), 0.0)
        K = np.where(S == 0, np.where(R < d, 1.0 / d ** 2, 0.0), K)
        assert np.all(np.isfinite(K)) and np.all(np.isfinite(m1)) and np.all(np.isfinite(m2))
        with np.errstate(all="ignore"):                       # Accelerate matmul raises spurious FP flags; inputs checked finite
            out = G * float(np.sum(m1[:, None] * K * m2[None, :]))
        assert math.isfinite(out)
        return out

    def Meff(self, d, tau=0.0, grow=False):
        x = math.log10(max(d, 10 ** self.ld[0]))
        if self.mutual:
            return float(np.interp(x, self.ld, self.Meff_mut))
        mc = float(np.interp(x, self.ld, self.Mc_sc))
        if grow:
            mc *= max(1.0 - tau / T0U, 0.0)
        return float(np.interp(x, self.ld, self.Mb_sc)) + mc


def coll_time(acc, d0, v0, tmax=60.0):
    """CFG513/515 radial timing (time-reversed, Lambda), acc(d, tau)."""
    def rhs(t, y):
        d = max(y[0], 1e-3)
        return [-y[1], acc(d, t) - OM_L * H0 ** 2 * d]
    ev = lambda t, y: y[0] - 0.05
    ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, (0, tmax * GYR), [d0, v0], events=ev, rtol=1e-10, atol=1e-10, max_step=0.05 * GYR)
    if s.t_events[0].size:
        te = s.t_events[0][0]; ye = s.y_events[0][0]
        return te + ye[0] / max(abs(ye[1]), 1e-9) * 0.5
    return tmax * GYR


def peri_time(acc, d0, vr, vt, tmax=60.0):
    """2-D time-reversed orbit of the separation; time back to the first pericentre (after the apocentre)."""
    def rhs(t, y):
        x, yy, vx, vy = y
        r = max(math.hypot(x, yy), 1e-3)
        a = -acc(r, t) / r + OM_L * H0 ** 2
        return [-vx, -vy, -a * x, -a * yy]
    ev = lambda t, y: y[0] * y[2] + y[1] * y[3]          # r * v_r (forward-time velocity): + -> - going back through the pericentre
    ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, (0, tmax * GYR), [d0, 0.0, vr, vt], events=ev, rtol=1e-10, atol=1e-9, max_step=0.05 * GYR)
    return s.t_events[0][0] if s.t_events[0].size else tmax * GYR


def vpred(acc, d0=D_LG, vt=0.0, lo=-900.0, hi=-1.0):
    if vt <= 0.0:
        f = lambda v: coll_time(acc, d0, v) - T0U
    else:
        f = lambda v: peri_time(acc, d0, v, vt) - T0U
    if f(lo) < 0 or f(hi) > 0:
        return float("nan")
    return brentq(f, lo, hi, xtol=1e-5)


def acc_of(pair, grow=False, law=False):
    def a(d, tau=0.0):
        g = G * pair.Meff(d, tau, grow) / d ** 2
        return g * float(nu_mono(g / A0[pair.foot])) if law else g
    return a


def zm(v, vobs=VR_LG, err=EVR_LG):
    return (abs(v) - abs(vobs)) / err if np.isfinite(v) else float("inf")


# ------------------------------------------------------------------ D1: v_r re-derivation (and the GC->M31 unit vector)
def gsr(vh, l, b, D, R0, Vphi, U=11.1, W=7.25):
    lr, br = math.radians(l), math.radians(b)
    nh = np.array([math.cos(br) * math.cos(lr), math.cos(br) * math.sin(lr), math.sin(br)])
    rg = D * nh + np.array([-R0, 0.0, 0.0]); n = rg / np.linalg.norm(rg)
    vsun = np.array([U, Vphi, W])
    return vh * float(nh @ n) + float(vsun @ n), n


def d1():
    out = {}
    v_a, n_a = gsr(-301.0, 121.17, -21.57, D_VDM, 8.29, 239.0 + 12.24)
    out["vdM12_solar"] = v_a
    for R0 in (8.178, 8.277):
        out[f"modern_R0_{R0}"] = gsr(-301.0, 121.17, -21.57, D_VDM, R0, 4.74047 * R0 * 6.411)[0]
    return out, n_a


def frame_vectors():
    _, n = gsr(-301.0, 121.17, -21.57, D_LG, 8.29, 251.24)
    vlmc = np.array([-57.0, -226.0, 221.0])
    v33 = gsr(-180.0, 133.61, -31.33, 794.0, 8.29, 251.24)[0]
    v31 = gsr(-301.0, 121.17, -21.57, D_LG, 8.29, 251.24)[0]
    return float(vlmc @ n), v33 - v31


VLMC_N, DV33 = frame_vectors()
M_LMC = 1.38e11


def full_stats(pair, label, law=False):
    """z_meas (radial), z_full at Salomon+21 v_tan with sigma_D, sigma_vt; z_full,LMC."""
    a = acc_of(pair, law=law)
    v0 = vpred(a, lo=-6000.0)
    vS = vpred(a, vt=VT_SAL, lo=-6000.0)
    vDm, vDp = vpred(a, d0=D_VDM - ED_VDM, vt=VT_SAL, lo=-6000.0), vpred(a, d0=D_VDM + ED_VDM, vt=VT_SAL, lo=-6000.0)
    vTm, vTp = vpred(a, vt=VT_SAL - EVT_SAL, lo=-6000.0), vpred(a, vt=VT_SAL + EVT_SAL, lo=-6000.0)
    sD, sT = abs(vDp - vDm) / 2, abs(vTp - vTm) / 2
    sfull = math.sqrt(EVR_LG ** 2 + sD ** 2 + sT ** 2) if np.isfinite(sD + sT) else float("nan")
    fl = M_LMC / pair.M1
    vobs_lmc = VR_LG - fl * VLMC_N
    r = dict(label=label, M_mw=pair.M1, M_m31=pair.M2, M_tot=pair.M1 + pair.M2, edge_mw=pair.mw.redge, edge_m31=pair.m31.redge,
             v_radial=v0, z_meas=zm(v0), v_vtSal=vS, sigma_D=sD, sigma_vt=sT, sigma_full=sfull,
             z_full=zm(vS, err=sfull), f_LMC=fl, vobs_LMC=vobs_lmc, z_full_LMC=zm(vS, vobs=vobs_lmc, err=sfull))
    # D5 (reported only, radial projection only): M33 with its own census f_ret, barycentre of M31 + M33
    m33 = 8e9 * (1 + COLD / L.fret_census(8e9)[0]); f33 = m33 / (pair.M2 + m33)
    r.update(f_M33=f33, vobs_LMC_M33=vobs_lmc + f33 * DV33, z_full_LMC_M33_reported=zm(vS, vobs=vobs_lmc + f33 * DV33, err=sfull))
    P(f"    [{pair.foot:9s}] {label}: M {pair.M1:.2e}+{pair.M2:.2e}; edges {pair.mw.redge:.0f}/{pair.m31.redge:.0f} kpc; "
      f"v_rad {v0:.1f} (z_meas {r['z_meas']:+.2f}); v(vt 82.4) {vS:.1f}, sigma_full {sfull:.1f} (D {sD:.1f}, vt {sT:.1f}) "
      f"z_full {r['z_full']:+.2f}; LMC f {fl:.3f} -> v_obs {vobs_lmc:.1f}, z_full,LMC {r['z_full_LMC']:+.2f}; "
      f"(reported) +M33 f {f33:.3f} -> v_obs {r['vobs_LMC_M33']:.1f}, z {r['z_full_LMC_M33_reported']:+.2f}")
    return r


def census_ta(Mb):
    f, lMta = L.fret_census(Mb)
    Mta = 10 ** lMta
    R = (3 * Mta / (4 * math.pi * 11.806 * 0.315 * 2.775e11)) ** (1 / 3)              # Mpc/h (CFG416 constants)
    return dict(M_b=Mb, f_ret=f, log10_Mta_Msun_h=lMta, R_ta_kpc=R * 1000 / 0.674, ramp=bool(f > 0.1 + 1e-9))


fM, f31 = L.fret_census(MB_PRIM)[0], L.fret_census(MB_M31)[0]
fLG = L.fret_census(MB_PRIM + MB_M31)[0]
RES["census"] = dict(f_mw=fM, f_m31=f31, f_LG=fLG)

if not MUTATE:
    # ---------------------------------------------------------- controls
    P("\n== Controls")
    k1 = []
    for foot in FOOTS:
        pc = Pair(foot, MB_PRIM, fM, MB_M31, f31); p1 = Pair(foot, MB_PRIM, 1.0, MB_M31, 1.0)
        vc, v1 = vpred(acc_of(pc)), vpred(acc_of(p1))
        k1.append((foot, vc, zm(v1)))
    J515 = json.load(open(os.path.join(D515, "cfg515_mw_results.json")))["rows"]
    check("K1 fast integrator reproduces CFG515 census v and f_ret=1 z (0.5 km/s / 0.3)",
          all(abs(vc - J515["census"][f]["primary"]["v_pred"]) <= 0.5 and abs(z1 + 22.82) <= 0.3 for f, vc, z1 in k1),
          "; ".join(f"{f}: v {vc:.2f} (CFG515 {J515['census'][f]['primary']['v_pred']:.2f}), f=1 z {z1:+.2f}" for f, vc, z1 in k1))
    # K2 Kepler radial cycloid, Lambda = 0: t = sqrt(a^3/GM)(eta - e sin eta) with e = 1 (radial): r = a(1 - cos eta)
    Mk = 4.0e12

    def tk(v, M):
        """radial Kepler cycloid r = a(1 - cos eta), t = sqrt(a^3/GM)(eta - sin eta); approaching branch (eta > pi)."""
        E = 0.5 * v * v - G * M / D_LG
        if E >= 0:
            return float("inf")
        a_ = -G * M / (2 * E)
        eta = 2 * math.pi - math.acos(1 - D_LG / a_)
        return math.sqrt(a_ ** 3 / (G * M)) * (eta - math.sin(eta))

    def rhs0(t, y):
        d = max(y[0], 1e-3); return [-y[1], G * Mk / d ** 2]
    ev = lambda t, y: y[0] - 0.05
    ev.terminal = True; ev.direction = -1

    def ct0(v):
        s = solve_ivp(rhs0, (0, 60 * GYR), [D_LG, v], events=ev, rtol=1e-11, atol=1e-11, max_step=0.05 * GYR)
        if not s.t_events[0].size:
            return 60 * GYR
        te = s.t_events[0][0]; ye = s.y_events[0][0]; return te + ye[0] / abs(ye[1]) * 0.5
    v_num = brentq(lambda v: ct0(v) - T0U, -200, -1, xtol=1e-6)
    v_an = brentq(lambda v: tk(v, Mk) - T0U, -0.999 * math.sqrt(2 * G * Mk / D_LG), -1)
    Mnum = brentq(lambda m: tk(v_num, m) - T0U, 1e12, 2e13)
    check("K2 radial integrator (Lambda = 0, point mass 4e12) vs analytic Kepler cycloid: mass within 0.5%",
          abs(Mnum / Mk - 1) < 5e-3, f"v_num {v_num:.3f}, v_analytic {v_an:.3f}; Kepler mass from v_num {Mnum:.4e} ({(Mnum / Mk - 1) * 100:+.3f}%)")
    pk = Pair("canonical", MB_PRIM, fM, MB_M31, f31)
    Fk = pk.F(20000.0); Fn = G * pk.M1 * pk.M2 / 20000.0 ** 2
    check("K3 mutual-force quadrature: well-separated (d = 20 Mpc) gives G M1 M2/d^2 within 1e-3", abs(Fk / Fn - 1) < 1e-3, f"ratio {Fk / Fn:.6f}")
    a_k = acc_of(pk)
    v_r0, v_r1 = vpred(a_k), vpred(a_k, vt=0.5)
    check("K4 2-D integrator at v_tan = 0.5 km/s reproduces the radial integrator within 0.5 km/s", abs(v_r0 - v_r1) <= 0.5,
          f"radial {v_r0:.2f}, 2-D {v_r1:.2f}")
    D1, n_a = d1()
    check("K5 vdM12 solar motion reproduces v_r = -109.3 within 1.5 km/s (tangential term neglected)", abs(D1["vdM12_solar"] + 109.3) <= 1.5,
          f"{D1['vdM12_solar']:.2f} km/s")

    # ---------------------------------------------------------- D1-D6
    P("\n== D1 v_r re-derivation")
    for k, v in D1.items():
        P(f"    {k}: v_r = {v:.2f} km/s (shift vs -109.3: {v + 109.3:+.2f})")
    d1_issue = any(v + 109.3 < -EVR_LG for k, v in D1.items() if k.startswith("modern"))  # more negative = reduces the census miss
    RES["D1"] = dict(values=D1, data_issue=d1_issue)
    P(f"    D1 data issue: {d1_issue}")

    P("\n== D2 distance (census-individual, radial, z_meas)")
    RES["D2"] = {}
    sig1 = {730.0: True, 752.0: True, 761.0: True, 770.0: True, 785.0: True, 810.0: True}
    for foot in FOOTS:
        pc = Pair(foot, MB_PRIM, fM, MB_M31, f31); a = acc_of(pc)
        RES["D2"][foot] = {}
        for Dd in sig1:
            v = vpred(a, d0=Dd); RES["D2"][foot][str(Dd)] = dict(v=v, z=zm(v))
        P(f"    [{foot}] " + "; ".join(f"D {k}: v {x['v']:.1f} z {x['z']:+.1f}" for k, x in RES["D2"][foot].items()))
    d2_issue = any(abs(x["z"]) <= 3 for f in FOOTS for x in RES["D2"][f].values())
    RES["D2"]["data_issue"] = d2_issue; P(f"    D2 data issue: {d2_issue}")

    P("\n== D3 tangential motion (census-individual, z vs -109.3 +- 4.4)")
    RES["D3"] = {}
    for foot in FOOTS:
        pc = Pair(foot, MB_PRIM, fM, MB_M31, f31); a = acc_of(pc)
        RES["D3"][foot] = {}
        for vt in (17.0, 34.3, 57.0, 82.4, 113.6):
            v = vpred(a, vt=vt); RES["D3"][foot][str(vt)] = dict(v=v, z=zm(v))
        P(f"    [{foot}] " + "; ".join(f"vt {k}: v {x['v']:.1f} z {x['z']:+.1f}" for k, x in RES["D3"][foot].items()))
    d3_issue = all(abs(RES["D3"][f]["82.4"]["z"]) <= 3 for f in FOOTS)
    RES["D3"]["data_issue"] = d3_issue; P(f"    D3 data issue: {d3_issue}")

    P("\n== D4/D5 barycentres (projections on the GC->M31 line)")
    P(f"    v_LMC . n = {VLMC_N:.1f} km/s (LMC moves away from M31 along the line); v_GSR(M33) - v_GSR(M31) = {DV33:+.1f} km/s (radial only)")
    RES["D4_D5"] = dict(vLMC_dot_n=VLMC_N, dv_M33_minus_M31=DV33, M_LMC=M_LMC)

    P("\n== D6 census inputs and turnaround radii (CFG416 constants)")
    D6 = {k: census_ta(m) for k, m in (("MW", MB_PRIM), ("M31", MB_M31), ("MW+M31", MB_PRIM + MB_M31), ("MW7.3e10", MB_HI),
                                       ("MW7.3e10+M31", MB_HI + MB_M31), ("MW+M31+M33+LMC", MB_PRIM + MB_M31 + 8e9 + 3e9), ("M33", 8e9))}
    for k, x in D6.items():
        P(f"    {k:16s}: M_b {x['M_b']:.2e}, f_ret {x['f_ret']:.4f} ({'ramp' if x['ramp'] else 'floor'}), log M_ta {x['log10_Mta_Msun_h']:.3f} [Msun/h], "
          f"R_ta {x['R_ta_kpc']:.0f} kpc")
    RES["D6"] = D6
    pre_M1 = D6["MW"]["R_ta_kpc"] > D_LG or D6["M31"]["R_ta_kpc"] > D_LG
    RES["M1_precondition"] = pre_M1
    P(f"    M1 precondition (a census turnaround sphere contains the other galaxy): {pre_M1}")

    # ---------------------------------------------------------- mechanisms
    P("\n== Census-individual (the miss) and f_ret = 1, full statistics")
    RES["census_individual"], RES["fret_one"] = {}, {}
    for foot in FOOTS:
        RES["census_individual"][foot] = full_stats(Pair(foot, MB_PRIM, fM, MB_M31, f31), "census-individual")
        RES["fret_one"][foot] = full_stats(Pair(foot, MB_PRIM, 1.0, MB_M31, 1.0), "f_ret = 1")

    P(f"\n== M1 shared catchment: f_LG = fret_census(M_b,MW + M_b,M31) = {fLG:.4f}")
    RES["M1"] = {}
    for foot in FOOTS:
        c_ = cell515(foot, fLG, fLG)                                         # CFG515's strict statistic, unchanged
        P(f"    [{foot:9s}] CFG515 cell at f_LG: v {c_['v_pred']:.2f} (z {c_['z']:+.2f}); D {c_['D']:+.2f}; unbound {c_['unbound']}/{c_['n_sat']}; "
          f"edges {c_['edge_mw_kpc']:.0f}/{c_['edge_m31_kpc']:.0f} kpc")
        fs = full_stats(Pair(foot, MB_PRIM, fLG, MB_M31, fLG), "M1 shared")
        fH = L.fret_census(MB_HI + MB_M31)[0]; cH = cell515(foot, fH, fH, Mb=MB_HI)
        fX = L.fret_census(MB_PRIM + MB_M31 + 8e9 + 3e9)[0]; cX = cell515(foot, fX, fX)
        P(f"      reported: MW 7.3e10 -> f_LG {fH:.4f}, v {cH['v_pred']:.2f} (z {cH['z']:+.2f}); +M33+LMC baryons in the census -> f_LG {fX:.4f}, "
          f"v {cX['v_pred']:.2f} (z {cX['z']:+.2f}) [only the catchment value changes]")
        RES["M1"][foot] = dict(strict=c_, full=fs, variant_Mb73=dict(f_LG=fH, v=cH["v_pred"], z=cH["z"]),
                               variant_M33_LMC_baryons=dict(f_LG=fX, v=cX["v_pred"], z=cX["z"]),
                               strict_pass=bool(abs(c_["z"]) <= 3 and c_["D"] <= 3))
    m1_strict = pre_M1 and all(RES["M1"][f]["strict_pass"] for f in FOOTS)
    P(f"    M1 strict pass (both footings): {m1_strict}")

    P("\n== M2 extended-body mutual force")
    RES["M2"] = {}
    for foot in FOOTS:
        pm = Pair(foot, MB_PRIM, fM, MB_M31, f31, mutual=True)
        sc = G * (float(pm.mw.M_enc(np.array([D_LG]))[0]) + float(pm.m31.M_enc(np.array([D_LG]))[0])) / D_LG ** 2
        ex = pm.F(D_LG) * (1 / pm.M1 + 1 / pm.M2)
        P(f"    [{foot}] at 780 kpc exact/shortcut acceleration = {ex / sc:.4f}")
        fs = full_stats(pm, "M2 census-individual, exact mutual force")
        pm1 = Pair(foot, MB_PRIM, fLG, MB_M31, fLG, mutual=True)
        fs1 = full_stats(pm1, "M2 on M1 (reported)")
        RES["M2"][foot] = dict(ratio_at_780=ex / sc, census=fs, on_M1=fs1, strict_pass=bool(abs(fs["z_meas"]) <= 3))
    m2_strict = all(RES["M2"][f]["strict_pass"] for f in FOOTS)

    P("\n== M3 (a) law on between the pair, baryons only, EFE-free (reference, not candidate B)")
    RES["M3"] = {}
    Mb_lg = MB_PRIM + MB_M31
    for foot in FOOTS:
        a0 = A0[foot]
        def a_t(d, tau=0.0, a0=a0):
            g = G * Mb_lg / d ** 2; return g * float(nu_mono(g / a0))
        def a_2b(d, tau=0.0, a0=a0):
            m1, m2 = MB_PRIM, MB_M31; M = m1 + m2
            return (2 / 3) * math.sqrt(G * a0) * (M ** 1.5 - m1 ** 1.5 - m2 ** 1.5) * M / (m1 * m2 * d)
        vt_, v2_ = vpred(a_t, lo=-6000.0), vpred(a_2b, lo=-6000.0)
        RES["M3"][foot] = dict(v_testmass=vt_, z_testmass=zm(vt_), v_deep2body=v2_, z_deep2body=zm(v2_))
        P(f"    [{foot}] test-mass nu_mono: v {vt_:.1f} (z {zm(vt_):+.1f}); deep-MOND two-body: v {v2_:.1f} (z {zm(v2_):+.1f})")

    P("\n== M4 time dependence: a0 flat (identity); reported bracket M_cold(t) ~ t/t0 (census-individual, no verdict weight)")
    RES["M4"] = {}
    for foot in FOOTS:
        pc = Pair(foot, MB_PRIM, fM, MB_M31, f31)
        v = vpred(acc_of(pc, grow=True))
        RES["M4"][foot] = dict(v=v, z=zm(v)); P(f"    [{foot}] v {v:.1f} (z {zm(v):+.1f})")

    P("\n== POST HOC (reported, no verdict weight, not a fit): common f_ret scan, canonical; which totals keep |z_full,LMC| <= 3")
    scan = []
    for fc in (0.08, 0.10, 0.12, 0.14, 0.17, 0.20, 0.25, 0.30, 0.40, 0.55):
        r_ = full_stats(Pair("canonical", MB_PRIM, fc, MB_M31, fc), f"common f_ret {fc}")
        scan.append(dict(f=fc, M_tot=r_["M_tot"], z_meas=r_["z_meas"], z_full=r_["z_full"], z_full_LMC=r_["z_full_LMC"],
                         z_full_LMC_M33=r_["z_full_LMC_M33_reported"]))
    RES["post_hoc_scan_canonical"] = scan

    # ---------------------------------------------------------- verdict
    ci, f1 = RES["census_individual"], RES["fret_one"]
    data_issue = d1_issue or d2_issue or all(abs(ci[f]["z_full"]) <= 3 and abs(ci[f]["z_full_LMC"]) <= 3 for f in FOOTS)
    m1_lmc_ok = all(abs(RES["M1"][f]["full"]["z_full_LMC"]) <= 3 for f in FOOTS)
    m1_full_ok = all(abs(RES["M1"][f]["full"]["z_full"]) <= 3 for f in FOOTS)
    m2_lmc_ok = all(abs(RES["M2"][f]["census"]["z_full_LMC"]) <= 3 for f in FOOTS)
    mutJ = os.path.join(HERE, "cfg522_results_MUTATE.json")
    mut_ok = os.path.exists(mutJ) and json.load(open(mutJ)).get("all_teeth_fail", False)
    if not mut_ok:
        P("    NOTE: MUTATE results missing or teeth not all failing -> a mechanism verdict cannot be granted")
    nd = all(abs(ci[f]["z_full"]) <= 3 and abs(f1[f]["z_full"]) <= 3 for f in FOOTS)
    if data_issue:
        verdict = "DATA-ISSUE"
    elif ((m1_strict and m1_lmc_ok) or (m2_strict and m2_lmc_ok)) and mut_ok:
        verdict = "MECHANISM FOUND"
    elif pre_M1 and not m1_strict and m1_full_ok and m1_lmc_ok and mut_ok:
        verdict = "MECHANISM FOUND, CONDITIONAL ON THE MEASURED TANGENTIAL MOTION"
    elif nd:
        verdict = "NOT DIAGNOSTIC"
    else:
        verdict = "GENUINE TENSION"
    RES["verdict"] = dict(verdict=verdict, data_issue=data_issue, m1_strict=m1_strict, m1_full_ok=m1_full_ok, m1_lmc_ok=m1_lmc_ok,
                          m2_strict=m2_strict, m2_lmc_ok=m2_lmc_ok, mutate_teeth_fail=mut_ok, not_diagnostic=nd)
    P(f"\n== VERDICT: {verdict}")
    P("   " + json.dumps(RES["verdict"]))
else:
    P(f"\n== MUTATE teeth (each must FAIL: |z_meas| > 3 on both footings); f_LG = {fLG:.4f}")
    T = {}
    for foot in FOOTS:
        T.setdefault("T1_M31_x0.3", {})[foot] = full_stats(Pair(foot, MB_PRIM, fLG, 0.3 * MB_M31, fLG), "T1 M31 x0.3")
        T.setdefault("T2_law_on_between_halos", {})[foot] = full_stats(Pair(foot, MB_PRIM, fLG, MB_M31, fLG), "T2 law-on + cold", law=True)
        Mbl = MB_PRIM + MB_M31
        T.setdefault("T3_double_counted_supply", {})[foot] = full_stats(
            Pair(foot, MB_PRIM, fLG * MB_PRIM / Mbl, MB_M31, fLG * MB_M31 / Mbl), "T3 double count")
    teeth = {k: all(abs(v[f]["z_meas"]) > 3 for f in FOOTS) for k, v in T.items()}
    for k, ok in teeth.items():
        check(f"{k} fails the timing", ok, "; ".join(f"{f} z_meas {T[k][f]['z_meas']:+.2f}" for f in FOOTS))
    RES["teeth"] = T; RES["all_teeth_fail"] = all(teeth.values())

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; load-bearing failures {nlb}; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg522_results{SUF}.json"), "w"), indent=1,
          default=lambda o: None if (isinstance(o, float) and o != o) else (bool(o) if isinstance(o, np.bool_) else float(o)))
open(os.path.join(HERE, f"cfg522_lg_timing{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
