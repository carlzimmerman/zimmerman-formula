#!/usr/bin/env python3
"""
RFX1 -- the measured LMC reflex (travel) velocity against a force-law-free momentum bound, in the framework's own
Milky Way field. Criteria: FROZEN_CRITERIA.md (sha256 in FREEZE_STAMP.txt), written before this script was run.
Usage: python3 -I -B rfx1.py <path to MWS_BHB.fits>
Writes rfx1.out (main), rfx1_mut.out (mutations, separate), rfx1_results.json. No times in any output.
Copied (not imported; nothing outside this folder is executed):
  - census baryons M_parts, nu_fw, g_model, the log-grid field table: closure_2026_11_12/LMC1_lmc_pull_on_halo_stars/
    lmc1_core.py (itself from RAW1's raw1_model.py and MWJ1's mwj1.py).
  - LMC today (published K13 inputs, astropy transform), load(), build(), prof_interval(), sgr_matrix(),
    sgr_lat_lon(), frame_affine(): closure_2026_11_12/LMC1_lmc_pull_on_halo_stars/lmc1.py (from RAW1's raw1.py).
Known-answer checks K1, K2, K4 first; the script stops before any label if one fails.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_k] = "1"
import sys, json, math
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianRepresentation, CartesianDifferential
from astropy.coordinates.matrix_utilities import rotation_matrix
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__))
FITS = sys.argv[1] if len(sys.argv) > 1 else None

OUT = open(os.path.join(HERE, "rfx1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 100); say(t); say("=" * 100)
FAIL = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAIL.append(name)
def stop_if_failed():
    if FAIL:
        say("\nKNOWN-ANSWER CHECK FAILED: " + ", ".join(FAIL) + ". Stopping before any label. Lane label: NO LABEL.")
        OUT.close(); sys.exit(2)

# ------------------------------------------------------------------ constants and field (copied from lmc1_core.py)
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
MYR = 3.15576e13
KMS = 1.0e3 * MYR / KPC
ACC = MYR ** 2 / KPC
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
MSTAR_CENSUS = 5.49e10
MSTAR_RC = {"canonical": 7.08e10, "alt": 6.42e10}
MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0, vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
STARS = ("thin", "thick")
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def zcum(c, n=1201):
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp" else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:] + zz[:-1]) / 2 * np.diff(zg))]); return zg, cum / cum[-1]
_MS = {}
def M_parts(r_kpc):
    key = float(r_kpc)
    if key not in _MS:
        r = key * KPC; st = MBULGE * r ** 2 / (r + ABULGE) ** 2; gs = 0.0
        Rg = np.linspace(1e-4 * KPC, min(r, 60 * KPC), 4000); h = np.sqrt(np.maximum(r ** 2 - Rg ** 2, 0.0))
        for k, c in MC.items():
            zg, cum = zcum(c); m = float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg) * np.interp(h, zg, cum), Rg))
            if k in STARS: st += m
            else: gs += m
        _MS[key] = (st, gs)
    return _MS[key]
def nu_fw(y): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))
RTAB = np.logspace(math.log10(0.5), math.log10(2.0e4), 700)
_TAB = None
def _tab():
    global _TAB
    if _TAB is None:
        st = np.array([M_parts(r)[0] if r <= 200 else np.nan for r in RTAB]); gs = np.array([M_parts(r)[1] if r <= 200 else np.nan for r in RTAB])
        last = np.where(RTAB <= 200)[0][-1]; st[last + 1:] = st[last]; gs[last + 1:] = gs[last]
        _TAB = (st, gs)
    return _TAB
def g_model(r_kpc, footing):
    """framework census field (lmc1_core.g_model, model 'FW_census'), m/s^2"""
    r = np.asarray(r_kpc, float); rm = r * KPC
    st, gs = _tab()
    Ms = np.interp(np.log(r), np.log(RTAB), st); Mg = np.interp(np.log(r), np.log(RTAB), gs)
    gb = G * (Ms + Mg) / rm ** 2
    return nu_fw(gb / A0[footing]) * gb
def M_b(r_kpc):
    s, g = M_parts(r_kpc); return (s + g) / MSUN

class Field:
    """g(r) and Phi(r) on a log grid (lmc1_core.Field); scalar access for the two-body integrators."""
    def __init__(self, footing):
        self.lr = np.linspace(math.log(0.5), math.log(2.0e4), 20001)
        self.g = g_model(np.exp(self.lr), footing) * ACC
        rr = np.exp(self.lr); seg = 0.5 * (self.g[1:] + self.g[:-1]) * np.diff(rr)
        self.phi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
        self.lr0 = float(self.lr[0]); self.dlr = float(self.lr[1] - self.lr[0])
        self.gl = self.g.tolist(); self.pl = self.phi.tolist(); self.n = len(self.gl)
    def _ix(self, r):
        t = (math.log(max(r, 0.5)) - self.lr0) / self.dlr; i = min(int(t), self.n - 2); return i, t - i
    def gs(self, r):
        i, f = self._ix(r); return self.gl[i] + f * (self.gl[i + 1] - self.gl[i])
    def phis(self, r):
        # linear in log r between nodes, consistent with gs to second order
        i, f = self._ix(r); return self.pl[i] + f * (self.pl[i + 1] - self.pl[i])

# ------------------------------------------------------------------ LMC today (lmc1.py lines 133-137)
R0, ZSUN, VSUN = 8.122, 20.8, (12.9, 245.6, 7.78)
gc_frame = Galactocentric(galcen_distance=R0 * u.kpc, z_sun=ZSUN * u.pc, galcen_v_sun=CartesianDifferential(list(VSUN) * u.km / u.s))
lmc = SkyCoord(ra=78.76 * u.deg, dec=-69.19 * u.deg, distance=49.59 * u.kpc, pm_ra_cosdec=1.910 * u.mas / u.yr,
               pm_dec=0.229 * u.mas / u.yr, radial_velocity=262.2 * u.km / u.s, frame="icrs").transform_to(gc_frame)
XL0 = np.array([lmc.x.to_value(u.kpc), lmc.y.to_value(u.kpc), lmc.z.to_value(u.kpc)])
VL0 = np.array([lmc.v_x.to_value(u.km / u.s), lmc.v_y.to_value(u.km / u.s), lmc.v_z.to_value(u.km / u.s)])
SPEED_ERR = 24.0

DT = 0.1; TCAP = 6000.0; NCAP = int(round(TCAP / DT))
FIELDS = {ft: Field(ft) for ft in ("canonical", "alt")}

def lb(v):
    v = np.asarray(v, float); a = float(np.linalg.norm(v))
    return math.degrees(math.atan2(v[1], v[0])), math.degrees(math.asin(v[2] / a))
def sep(l1, b1, l2, b2):
    l1, b1, l2, b2 = map(math.radians, (l1, b1, l2, b2))
    c = math.sin(b1) * math.sin(b2) + math.cos(b1) * math.cos(b2) * math.cos(l1 - l2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))

# ------------------------------------------------------------------ the relative orbit, backward, to the last apocentre
def back_orbit(F, mL, mMW, vscale=1.0, vsign=1.0, energy=False):
    """d'' = -(1 + mL/mMW) g(|d|) d_hat, integrated back from today (KDK leapfrog, step DT). Returns the state at the
    last apocentre (first max of |d| after the first min), the pericentre speed, and flags."""
    q = 1.0 + (mL / mMW if mMW > 0 else 0.0)
    x = [float(c) for c in XL0]; v = [float(c) * KMS * vscale * vsign for c in VL0]
    h = -DT
    def acc(x):
        r = math.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2]); s = -q * F.gs(r) / r
        return [s * x[0], s * x[1], s * x[2]], r
    a, r = acc(x)
    rs_prev = r; phase = 0; vperi = None; rperi = None; tperi = None; out = None
    E0 = 0.5 * sum(c * c for c in v) + q * F.phis(r); dEmax = 0.0
    prev = (list(x), list(v), r)
    for k in range(1, NCAP + 1):
        v = [v[i] + 0.5 * h * a[i] for i in range(3)]
        x = [x[i] + h * v[i] for i in range(3)]
        a, r = acc(x)
        v = [v[i] + 0.5 * h * a[i] for i in range(3)]
        if energy:
            E = 0.5 * sum(c * c for c in v) + q * F.phis(r); dEmax = max(dEmax, abs(E / E0 - 1))
        if phase == 0 and r > prev[2] and k > 1:          # first minimum passed: the last pericentre at step k-1
            phase = 1; rperi = prev[2]; vperi = math.sqrt(sum(c * c for c in prev[1])) / KMS; tperi = -(k - 1) * DT
        elif phase == 1 and r < prev[2] and not energy:   # first maximum after it: the last apocentre at step k-1
            out = dict(x=prev[0], v=prev[1], r=prev[2], t=-(k - 1) * DT, capped=False, steps=k - 1); break
        prev = (list(x), list(v), r)
        if energy and k == NCAP: break
    if out is None:
        out = dict(x=list(x), v=list(v), r=r, t=-NCAP * DT, capped=True, steps=NCAP)
    out.update(rperi=rperi, vperi=vperi, tperi=tperi, dEmax=dEmax)
    return out

_MEMO = {}
def bound(F, mL, mMW, vscale=1.0, vsign=1.0):
    key = (id(F), mL, mMW, vscale, vsign)
    if key not in _MEMO: _MEMO[key] = _bound(F, mL, mMW, vscale, vsign)
    return _MEMO[key]
def _bound(F, mL, mMW, vscale=1.0, vsign=1.0):
    o = back_orbit(F, mL, mMW, vscale, vsign)
    mu = mL / (mMW + mL)
    vnow = VL0 * vscale * vsign; vapo = np.array(o["v"]) / KMS
    dv = vnow - vapo; VB = -mu * dv
    Babs = 2 * mu * (o["vperi"] if o["vperi"] is not None else float(np.linalg.norm(vnow)))
    l, b = lb(VB)
    return dict(mu=mu, dv=dv.tolist(), dv_mag=float(np.linalg.norm(dv)), VB=VB.tolist(), B=float(np.linalg.norm(VB)),
                Babs=Babs, l=l, b=b, apo_r=o["r"], apo_t=o["t"], capped=o["capped"], rperi=o["rperi"], vperi=o["vperi"],
                tperi=o["tperi"], vapo=vapo.tolist(), xapo=o["x"], steps=o["steps"], mL=mL, mMW=mMW)

def sigma_B(F, mL, mMW, mass_err=None, key="B"):
    s = 1.0 + SPEED_ERR / float(np.linalg.norm(VL0))
    lo = bound(F, mL, mMW, vscale=2.0 - s)[key]; hi = bound(F, mL, mMW, vscale=s)[key]
    parts = dict(speed=0.5 * abs(hi - lo))
    if mass_err is not None:
        eL, eM = mass_err
        parts["m_L"] = 0.5 * abs(bound(F, mL * (1 + eL), mMW)[key] - bound(F, mL * (1 - eL), mMW)[key])
        parts["m_MW"] = 0.5 * abs(bound(F, mL, mMW * (1 + eM))[key] - bound(F, mL, mMW * (1 - eM))[key])
    return math.sqrt(sum(p * p for p in parts.values())), parts

# ------------------------------------------------------------------ measurements (PROVISIONAL; SOURCES.md)
PRIMARY = dict(name="Petersen & Penarrubia 2021 (40-120 kpc)", v=32.0, e=4.0, l=56.0, b=-34.0, el=9.0, eb_up=10.0, eb_dn=9.0)
OTHERS = [
    dict(name="Yaaqib+ 2024 50+ kpc", v=40.0, e=7.0, l=38.0, b=-37.0),
    dict(name="Yaaqib+ 2024 40-50 kpc", v=23.0, e=7.0, l=64.0, b=-47.0),
    dict(name="Chandra+ 2024 at 100 kpc", v=37.0, e=9.0, l=-80.0, b=-59.0),
    dict(name="Chandra+ 2024 at 120 kpc (model endpoint)", v=47.0, e=12.0, l=None, b=None),
    dict(name="Bystrom+ 2025 DESI BHB >50 kpc", v=34.0, e=10.6, l=-72.7, b=-52.9),
    dict(name="Li+ 2026 DESI DR2 50-120 kpc", v=24.0, e=3.8, l=-34.8, b=-37.8),
    dict(name="Li+ 2026 DESI DR2 50-60 kpc", v=18.1, e=3.6, l=-87.6, b=-48.8),
    dict(name="Li+ 2026 DESI DR2 60-80 kpc", v=20.0, e=4.4, l=-14.3, b=-41.6),
    dict(name="Li+ 2026 DESI DR2 80-120 kpc", v=44.0, e=5.4, l=-28.3, b=-23.8),
]
def zval(vm, em, B, sB): return (vm - B) / math.sqrt(em * em + sB * sB)
def word(z): return "REFLEX EXCEEDS THE BOUND" if z >= 2.0 else "REFLEX WITHIN THE BOUND"
def k3(l, b):
    dl = (l - PRIMARY["l"] + 180.0) % 360.0 - 180.0; db = b - PRIMARY["b"]
    sb = PRIMARY["eb_up"] if b > PRIMARY["b"] else PRIMARY["eb_dn"]
    chi = math.hypot(dl / PRIMARY["el"], db / sb); return chi, chi <= 3.0

RES = dict()
# ================================================================== K1
sec("K1 the LMC today (as LMC1 built it)")
rL = float(np.linalg.norm(XL0)); vL = float(np.linalg.norm(VL0))
check("K1 r_GC", abs(rL - 49.08) <= 0.01, f"{rL:.4f} kpc vs 49.08; position {np.round(XL0, 3).tolist()}")
check("K1 speed", abs(vL - 320.1) <= 0.1, f"{vL:.3f} km/s vs 320.1; velocity {np.round(VL0, 2).tolist()}")
lv, bv = lb(-VL0)
say(f"  reported: direction opposite to the LMC's present velocity (l, b) = ({lv:.1f}, {bv:.1f}); {sep(lv, bv, PRIMARY['l'], PRIMARY['b']):.1f} deg from the published apex")
MB200 = M_b(200.0)
check("census baryons M_b(<200 kpc) ~ 6.68e10 (within 1 per cent)", abs(MB200 / 6.68e10 - 1) < 0.01, f"{MB200:.4e} Msun")
st200, gs200 = M_parts(200.0); say(f"  census stars {st200 / MSUN:.4e}, census gas {gs200 / MSUN:.4e} Msun")
GAS_CENSUS = gs200 / MSUN

# ================================================================== K4
sec("K4 energy conservation of the relative-orbit integrator (static field, test-particle LMC, 6 Gyr back)")
for ft, F in FIELDS.items():
    o = back_orbit(F, 0.0, 1.0, energy=True)
    check(f"K4 {ft}", o["dEmax"] < 1e-6, f"max |dE/E| {o['dEmax']:.2e} over {o['steps'] * DT:.0f} Myr")
stop_if_failed()

# ================================================================== readings: primary masses
M_L_R1 = 3.2e9 + 3.1e8 + 5.6e8
R1_VAR = {"(a) LMC alone": (3.2e9, None), "(b) plus all Stream/Bridge/Leading Arm gas": (M_L_R1 + 2.0e9 * 1.33, None),
          "(c) MW rc stellar mass + census gas": (M_L_R1, "rc"), "(d) MW plus hot gas <50 kpc": (M_L_R1, "hot")}
R1_REP = {"Stream neutral gas only (reported)": (M_L_R1 + 4.87e8 * 1.33, None)}
def mMW_R1(ft, kind=None):
    if kind == "rc": return MSTAR_RC[ft] + GAS_CENSUS
    if kind == "hot": return MB200 + 3.846e9
    return MB200
def mdyn(ft, rc): return float(g_model(rc, ft)) * (rc * KPC) ** 2 / G / MSUN

# ================================================================== K2
sec("K2 two-body integration in an inertial frame (separate code path), and force-free far tracers")
def twobody_check(F, mL, mMW, B):
    """from the last apocentre forward to today: two bodies, equal and opposite forces m_L g(|d|)."""
    mu = mL / (mL + mMW)
    d = np.array(B["xapo"], float); vrel = np.array(B["vapo"], float) * KMS
    xM = -mu * d; xL = (1 - mu) * d; vM = -mu * vrel; vL_ = (1 - mu) * vrel
    xM = xM.tolist(); xL = xL.tolist(); vM = vM.tolist(); vL_ = vL_.tolist()
    vM0 = list(vM); P0 = [mMW * vM[i] + mL * vL_[i] for i in range(3)]
    def forces(xM, xL):
        dd = [xL[i] - xM[i] for i in range(3)]; r = math.sqrt(sum(c * c for c in dd)); gg = F.gs(r) / r
        aL = [-gg * dd[i] for i in range(3)]; aM = [(mL / mMW) * gg * dd[i] for i in range(3)]
        return aM, aL
    aM, aL = forces(xM, xL); dPmax = 0.0; pscale = mL * math.sqrt(sum(c * c for c in vL_)) + 1e-300
    for k in range(B["steps"]):
        vM = [vM[i] + 0.5 * DT * aM[i] for i in range(3)]; vL_ = [vL_[i] + 0.5 * DT * aL[i] for i in range(3)]
        xM = [xM[i] + DT * vM[i] for i in range(3)]; xL = [xL[i] + DT * vL_[i] for i in range(3)]
        aM, aL = forces(xM, xL)
        vM = [vM[i] + 0.5 * DT * aM[i] for i in range(3)]; vL_ = [vL_[i] + 0.5 * DT * aL[i] for i in range(3)]
        P = [mMW * vM[i] + mL * vL_[i] for i in range(3)]
        dPmax = max(dPmax, math.sqrt(sum((P[i] - P0[i]) ** 2 for i in range(3))) / pscale)
    dVM = (np.array(vM) - np.array(vM0)) / KMS
    VB = np.array(B["VB"])
    rel = float(np.linalg.norm(dVM - VB) / np.linalg.norm(VB))
    dnow = np.array(xL) - np.array(xM)
    # force-free tracers, moving with the Milky Way's velocity at the apocentre, placed around the MW centre
    rng = np.random.default_rng(7); Nt = 2000
    cth = rng.uniform(-1, 1, Nt); ph = rng.uniform(0, 2 * np.pi, Nt); rr = rng.uniform(200, 400, Nt); sth = np.sqrt(1 - cth ** 2)
    n0 = np.vstack([sth * np.cos(ph), sth * np.sin(ph), cth]).T
    T = B["steps"] * DT
    xt = -mu * d[None, :] + rr[:, None] * n0 + np.array(vM0)[None, :] * T      # force-free drift to today
    vt = np.repeat(np.array(vM0)[None, :], Nt, 0)
    rel_pos = xt - np.array(xM)[None, :]; nn = rel_pos / np.linalg.norm(rel_pos, axis=1)[:, None]
    vlos = np.einsum("ij,ij->i", (vt - np.array(vM)[None, :]) / KMS, nn)
    A = np.hstack([np.ones((Nt, 1)), nn]); co, *_ = np.linalg.lstsq(A, vlos, rcond=None)
    trav = -co[1:]
    relt = float(np.linalg.norm(trav - VB) / np.linalg.norm(VB))
    return dPmax, rel, relt, float(np.linalg.norm(dnow - XL0)), dVM

PRIM = {}
for ft, F in FIELDS.items():
    for rd in ("R1", "R2"):
        mL, mMW = (M_L_R1, MB200) if rd == "R1" else (2.5e10, mdyn(ft, 40.0))
        B = bound(F, mL, mMW); PRIM[(rd, ft)] = B
        dP, rel, relt, dpos, dVM = twobody_check(F, mL, mMW, B)
        check(f"K2 momentum {rd} {ft}", dP < 1e-8, f"max |dP| / (m_L |v_L|) {dP:.2e}")
        check(f"K2 MW velocity change = V_B {rd} {ft}", rel < 1e-4, f"relative difference {rel:.2e}; dV_MW {np.round(dVM, 3).tolist()} vs V_B {np.round(B['VB'], 3).tolist()}; today's separation reproduced to {dpos:.2e} kpc")
        check(f"K2 far tracers' travel velocity = V_B {rd} {ft}", relt < 1e-4, f"relative difference {relt:.2e}")
stop_if_failed()

# ================================================================== primary bounds, K3, labels
sec("Primary bounds (B_first = mu |v_rel(now) - v_rel(last apocentre)|), K3, labels")
say(f"Primary measurement: {PRIMARY['name']}: {PRIMARY['v']} +/- {PRIMARY['e']} km/s toward ({PRIMARY['l']}, {PRIMARY['b']}) (PROVISIONAL)")
LAB = {}
def describe(B): return (f"m_L {B['mL']:.3e}, m_MW {B['mMW']:.4e}, mu {B['mu']:.5f}; last pericentre {B['rperi']:.2f} kpc at {B['tperi']:.1f} Myr, "
                         f"v_peri {B['vperi']:.1f}; last apocentre {B['apo_r']:.1f} kpc at {B['apo_t']:.0f} Myr{' (CAPPED at 6 Gyr)' if B['capped'] else ''}; "
                         f"|v_apo| {np.linalg.norm(B['vapo']):.1f}; |dv| {B['dv_mag']:.1f} km/s; B_first {B['B']:.2f} toward ({B['l']:.1f}, {B['b']:.1f}); B_abs {B['Babs']:.2f}")
for rd in ("R1", "R2"):
    for ft, F in FIELDS.items():
        B = PRIM[(rd, ft)]
        say(f"\n{rd} {ft}: " + describe(B))
        sB, parts = sigma_B(F, B["mL"], B["mMW"], (0.25, 0.10) if rd == "R1" else None)
        sBa, _ = sigma_B(F, B["mL"], B["mMW"], (0.25, 0.10) if rd == "R1" else None, key="Babs")
        say(f"   sigma_B {sB:.2f} (" + ", ".join(f"{k} {v:.2f}" for k, v in parts.items()) + f"); sigma of B_abs {sBa:.2f}")
        chi, ok3 = k3(B["l"], B["b"])
        say(f"   K3 direction: {sep(B['l'], B['b'], PRIMARY['l'], PRIMARY['b']):.1f} deg from the published apex; chi {chi:.2f} (<= 3 passes) -> {'PASS' if ok3 else 'FAIL'}")
        z = zval(PRIMARY["v"], PRIMARY["e"], B["B"], sB)
        say(f"   z = ({PRIMARY['v']} - {B['B']:.2f}) / sqrt({PRIMARY['e']}^2 + {sB:.2f}^2) = {z:.3f} -> {word(z)}")
        w0 = word(z); flips = []; rows = []
        # variants
        if rd == "R1":
            for nm, (mLv, kind) in list(R1_VAR.items()) + list(R1_REP.items()):
                mMWv = mMW_R1(ft, kind); Bv = bound(F, mLv, mMWv); sv, _ = sigma_B(F, mLv, mMWv, (0.25, 0.10))
                zv = zval(PRIMARY["v"], PRIMARY["e"], Bv["B"], sv); rep = "reported" in nm
                rows.append((nm, Bv["B"], sv, zv, word(zv), rep, Bv["l"], Bv["b"]))
                if word(zv) != w0 and not rep: flips.append(nm)
        else:
            for rc in (30.0, 50.0, 80.0):
                mMWv = mdyn(ft, rc); Bv = bound(F, 2.5e10, mMWv); sv, _ = sigma_B(F, 2.5e10, mMWv)
                zv = zval(PRIMARY["v"], PRIMARY["e"], Bv["B"], sv); nm = f"r_c {rc:.0f} kpc (m_MW {mMWv:.3e})"
                rows.append((nm, Bv["B"], sv, zv, word(zv), False, Bv["l"], Bv["b"]))
                if word(zv) != w0: flips.append(nm)
            for mLv in (1.6e10, 4.0e10):
                Bv = bound(F, mLv, B["mMW"]); sv, _ = sigma_B(F, mLv, B["mMW"])
                zv = zval(PRIMARY["v"], PRIMARY["e"], Bv["B"], sv); nm = f"M_eff {mLv:.1e}"
                rows.append((nm, Bv["B"], sv, zv, word(zv), False, Bv["l"], Bv["b"]))
                if word(zv) != w0: flips.append(nm)
        zA = zval(PRIMARY["v"], PRIMARY["e"], B["Babs"], sBa)
        rows.append(("B_abs in place of B_first", B["Babs"], sBa, zA, word(zA), False, None, None))
        if word(zA) != w0: flips.append("B_abs in place of B_first")
        for m in OTHERS:
            zm = zval(m["v"], m["e"], B["B"], sB); nm = f"measurement: {m['name']} {m['v']} +/- {m['e']}"
            dsep = sep(B["l"], B["b"], m["l"], m["b"]) if m["l"] is not None else None
            rows.append((nm, B["B"], sB, zm, word(zm), False, dsep, None))
            if word(zm) != w0: flips.append(nm)
        for nm, Bv, sv, zv, wv, rep, l_, b_ in rows:
            extra = ""
            if nm.startswith("measurement") and l_ is not None: extra = f"; its apex is {l_:.0f} deg from the bound's direction"
            elif l_ is not None: extra = f"; direction ({l_:.1f}, {b_:.1f})"
            say(f"   variant {nm}: B {Bv:.2f} +/- {sv:.2f}, z {zv:.3f} -> {wv}{' (reported, no flip power)' if rep else ''}{extra}")
        lab = "NOT EVALUABLE" if not ok3 else (w0 + (", FRAGILE" if flips else ""))
        say(f"   ==> {rd} {ft}: {lab}")
        if flips: say("       flipped by: " + "; ".join(flips))
        # reported: mu required
        mu_req = PRIMARY["v"] / B["dv_mag"]; mL_need = mu_req / (1 - mu_req) * B["mMW"]
        say(f"   reported: mu required by the primary measurement {mu_req:.5f}; inertial m_L needed at this m_MW {mL_need:.3e} Msun "
            f"(inventory: LMC 3.2e9, LMC+SMC {M_L_R1:.3e}, plus all Stream gas {M_L_R1 + 2.66e9:.3e}; R2 bracket 1.6e10-4e10)")
        LAB[f"{rd}/{ft}"] = dict(label=lab, z=z, B=B["B"], sigma_B=sB, sigma_parts=parts, Babs=B["Babs"], sigma_Babs=sBa,
                                 chi_K3=chi, K3=ok3, flips=flips, mu_req=mu_req, mL_needed=mL_need, primary=B,
                                 variants=[dict(name=r[0], B=r[1], sigma=r[2], z=r[3], word=r[4], reported=r[5]) for r in rows])
RES["labels"] = LAB

# ================================================================== mutations
MUT = open(os.path.join(HERE, "rfx1_mut.out"), "w")
def msay(s): print("[MUT] " + s); MUT.write(s + "\n"); MUT.flush()
msay("RFX1 mutations (FROZEN_CRITERIA.md section 8).")
MR = {}
for ft, F in FIELDS.items():
    L = LAB[f"R1/{ft}"]; B3 = bound(F, 3 * M_L_R1, MB200); s3, _ = sigma_B(F, 3 * M_L_R1, MB200, (0.25, 0.10))
    z3 = zval(PRIMARY["v"], PRIMARY["e"], B3["B"], s3); bites = (word(z3) != word(L["z"])) or abs(z3 - L["z"]) >= 2
    msay(f"M1 R1 {ft}: m_L x 3 = {3 * M_L_R1:.3e}: B {B3['B']:.2f} +/- {s3:.2f}, z {z3:.3f} ({word(z3)}) vs primary z {L['z']:.3f}: bites {bites}")
    MR[f"M1/{ft}"] = dict(B=B3["B"], z=z3, bites=bool(bites))
for rd in ("R1", "R2"):
    for ft, F in FIELDS.items():
        B = PRIM[(rd, ft)]; Bm = bound(F, B["mL"], B["mMW"], vsign=-1.0)
        s = sep(Bm["l"], Bm["b"], B["l"], B["b"]); chi, ok3 = k3(Bm["l"], Bm["b"]); bites = (s > 90.0) and not ok3
        msay(f"M2 {rd} {ft}: velocity reversed: apex ({Bm['l']:.1f}, {Bm['b']:.1f}), {s:.1f} deg from the unmutated apex; K3 chi {chi:.2f} ({'passes' if ok3 else 'fails'}); "
             f"last apocentre {Bm['apo_r']:.1f} kpc at {Bm['apo_t']:.0f} Myr{' CAPPED' if Bm['capped'] else ''}; B {Bm['B']:.2f}: bites {bites}")
        MR[f"M2/{rd}/{ft}"] = dict(l=Bm["l"], b=Bm["b"], sep=s, chi=chi, bites=bool(bites))
msay("M3 BORROWED masses (standard-model literature), CONTEXT ONLY, no label:")
for ft, F in FIELDS.items():
    for mMW in (1.0e12, 1.3e12):
        Bm = bound(F, 1.5e11, mMW); sm, _ = sigma_B(F, 1.5e11, mMW)
        zm = zval(PRIMARY["v"], PRIMARY["e"], Bm["B"], sm)
        verdict = "bound at or above the measurement" if zm <= 0 else ("below the measurement but within 2 sigma" if zm < 2 else "BOUND TOO TIGHT: below the measurement by >= 2 sigma")
        msay(f"   {ft} m_L 1.5e11, m_MW {mMW:.1e}: mu {Bm['mu']:.4f}, apocentre {Bm['apo_r']:.1f} kpc at {Bm['apo_t']:.0f} Myr{' CAPPED' if Bm['capped'] else ''}, "
             f"B_first {Bm['B']:.2f} +/- {sm:.2f} toward ({Bm['l']:.1f}, {Bm['b']:.1f}), z {zm:.3f}: {verdict}")
        MR[f"M3/{ft}/{mMW:.1e}"] = dict(B=Bm["B"], z=zm, verdict=verdict)
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()
RES["mutations"] = MR
say("\nMutations (rfx1_mut.out): " + "; ".join(f"{k} bites {v['bites']}" for k, v in MR.items() if "bites" in v))

# ================================================================== own stars (reported, no label)
sec("Reported: own stars (DESI DR1 BHB, RAW1's sample and bins): travel velocity along the bound's direction")
def prof_interval(nll, lo, hi):
    res = minimize_scalar(nll, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-6))
    xb, nb = res.x, res.fun
    def side(direction):
        step = max(abs(xb) * 0.02, 1e-3); x = xb
        for _ in range(200):
            xn = x + direction * step
            if (direction < 0 and xn < lo) or (direction > 0 and xn > hi): return (lo if direction < 0 else hi)
            if nll(xn) - nb > 0.5:
                return brentq(lambda t: nll(t) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-6)
            x = xn; step *= 1.3
        return lo if direction < 0 else hi
    return xb, side(-1), side(+1), nb
def sgr_matrix():
    D = rotation_matrix((180 + 3.75) * u.deg, "z"); Cm = rotation_matrix((90 - 13.46) * u.deg, "x")
    Bm = rotation_matrix((180 + 14.111534) * u.deg, "z"); A = np.diag([1., 1., -1.])
    return A @ Bm @ Cm @ D
def sgr_lat_lon(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    x = np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)])
    xs = sgr_matrix() @ x
    return np.degrees(np.arctan2(xs[1], xs[0])) % 360.0, np.degrees(np.arcsin(np.clip(xs[2], -1, 1)))
def frame_affine(R0, zsun):
    gc = Galactocentric(galcen_distance=R0 * u.kpc, z_sun=zsun * u.pc, galcen_v_sun=CartesianDifferential([0, 0, 0] * u.km / u.s))
    def tr(xyz):
        c = SkyCoord(CartesianRepresentation(np.asarray(xyz, float).T * u.kpc), frame="icrs").transform_to(gc)
        return np.vstack([c.x.to_value(u.kpc), c.y.to_value(u.kpc), c.z.to_value(u.kpc)]).T
    p0 = tr(np.zeros((1, 3)))[0]; Rm = (tr(np.eye(3)) - p0).T
    return p0, Rm
def load():
    h = fits.open(FITS, memmap=False)
    rv, fm = h["RVTAB"].data, h["FIBERMAP"].data
    return dict(tid=np.asarray(rv["TARGETID"]), tid_fm=np.asarray(fm["TARGETID"]), primary=np.asarray(rv["PRIMARY"]).astype(bool),
                vrad=np.asarray(rv["VRAD"], float), verr=np.asarray(rv["VRAD_ERR"], float),
                ra=np.asarray(rv["TARGET_RA"], float), dec=np.asarray(rv["TARGET_DEC"], float),
                dist=np.asarray(fm["DIST"], float), g=np.asarray(fm["MAG_DERED_G"], float), Mg=np.asarray(fm["ABS_MAG_G"], float))
def build(D):
    m = D["primary"] & np.isfinite(D["vrad"]) & (D["verr"] > 0) & (D["dist"] > 0) & np.isfinite(D["g"]) & np.isfinite(D["Mg"])
    idx = np.where(m)[0]
    ra, dec = np.radians(D["ra"][idx]), np.radians(D["dec"][idx]); d = D["dist"][idx]
    p0, Rm = frame_affine(R0, ZSUN)
    n = np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T @ Rm.T
    pos = p0 + d[:, None] * n; r = np.linalg.norm(pos, axis=1)
    vgsr = D["vrad"][idx] + n @ np.array(VSUN)
    c = SkyCoord(ra=D["ra"][idx] * u.deg, dec=D["dec"][idx] * u.deg, frame="icrs").galactic
    lam, bet = sgr_lat_lon(c.l.deg, c.b.deg)
    keep = (np.abs(bet) >= 15.0) & (r >= 20.0) & (r < 80.0) & (np.abs(vgsr) <= 400.0)
    k = np.where(keep)[0]
    return dict(r=r[k], n=n[k], vgsr=vgsr[k], verr=D["verr"][idx][k])
OWN = None
if FITS is None:
    say("  no FITS path given: own-stars item not run")
else:
    S = build(load())
    BINS = [(20.0, 30.0), (30.0, 40.0), (40.0, 55.0), (55.0, 80.0)]
    bsel = [(S["r"] >= a) & (S["r"] < b) for a, b in BINS]; counts = [int(m.sum()) for m in bsel]
    ok5 = counts == [865, 264, 241, 125]
    say(f"  [{'PASS' if ok5 else 'FAIL'}] K5 counts {counts} (stops only this item)")
    if ok5:
        def unit(l, b):
            l, b = math.radians(l), math.radians(b); return np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])
        dirs = {"bound R1 canonical": np.array(PRIM[("R1", "canonical")]["VB"]) / PRIM[("R1", "canonical")]["B"],
                "published apex (56, -34)": unit(56.0, -34.0)}
        OWN = {}
        for dn, uu in dirs.items():
            rows = []
            for (a, b), m in zip(BINS, bsel):
                v = S["vgsr"][m]; e = S["verr"][m]; p = S["n"][m] @ uu
                def nll_T(T):
                    vv = v + T * p
                    def nll_s(sg):
                        var = sg * sg + e * e; mu_ = np.sum(vv / var) / np.sum(1 / var)
                        return 0.5 * np.sum((vv - mu_) ** 2 / var + np.log(var))
                    return minimize_scalar(nll_s, bounds=(1.0, 400.0), method="bounded", options=dict(xatol=1e-6)).fun
                Tb, lo, hi, _ = prof_interval(nll_T, -300.0, 300.0)
                prng = float(np.std(p))
                rows.append(dict(bin=f"{a:.0f}-{b:.0f}", T=float(Tb), lo=float(lo), hi=float(hi), h=float(0.5 * (hi - lo)), n=int(m.sum()), spread_u_dot_n=prng))
                say(f"  {dn}: bin {a:.0f}-{b:.0f} kpc (n {int(m.sum())}): T = {Tb:+.1f} [{lo:+.1f}, {hi:+.1f}] km/s; rms of u.n {prng:.3f}")
            OWN[dn] = rows
RES["own_stars"] = OWN

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float): return float(f"{o:.10g}")
    return o
json.dump(clean(RES), open(os.path.join(HERE, "rfx1_results.json"), "w"), indent=1)
sec("LABELS (summary)")
for k, v in LAB.items():
    say(f"  {k}: {v['label']}  (B_first {v['B']:.2f} +/- {v['sigma_B']:.2f}, z {v['z']:.3f}; K3 chi {v['chi_K3']:.2f})")
say("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
