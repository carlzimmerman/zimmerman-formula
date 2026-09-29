#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG180_lib.py -- helpers for the CFG180 referee re-derivation of CFG170 (two-epoch gas-ratio test).
Written from CFG180_FROZEN_CRITERIA.md alone (no CFG170 script/out/json open).

SHARED, NOT INDEPENDENT: the KURVS/KROSS/SPARC pipeline is imported read-only from
  campaign_fresh_gravity/CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py   (as M)
  (load_kurvs, load_kross, load_sparc_anchor, per_object, pool, anchor_pool, corr, spec, gbar, gpred, alpha_K, E_of_z; CFG4_common.nu_mono through it).
Independent (this file): the break-even root-finder, intervals, R_law, R_obs, the rule, the mock generator.
"""
import os
import sys
import math
import copy
import importlib

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "data_assembly")):
        return r
    d = HERE
    for _ in range(10):
        if os.path.isdir(os.path.join(d, "data_assembly")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("set ZF_REPO")


REPO = find_repo()
_c165 = os.path.join(REPO, "campaign_fresh_gravity", "CFG165_kurvs_referee")
sys.path.insert(0, _c165)
_mut = os.environ.get("MUTATE")
os.environ["MUTATE"] = "0"          # CFG165's module reads MUTATE at import for its own harness; not ours
M = importlib.import_module("CFG165_referee_kurvs_p4")
if _mut is None:
    os.environ.pop("MUTATE", None)
else:
    os.environ["MUTATE"] = _mut

LN10 = math.log(10.0)
A0 = M.A0
S_PLACE = (0.0, 1.00, 1.42, 1.62, 1.69, 3.00)
MU_LO, MU_HI = 0.01, 30.0
NGRID = 400
LAWS = ("flat", "H")
NAMES = {"flat": "flat", "H": "rival"}


def scrub(s):
    return str(s).replace(REPO, "<repo>").replace(HERE, "<scratch>")


# ------------------------------------------------------------------ samples
_base = {}


def get_kurvs(inc_col="inc_star_deg"):
    k = ("K", inc_col)
    if k not in _base:
        _base[k] = M.load_kurvs(inc_col=inc_col)
    return copy.deepcopy(_base[k])


def get_kross():
    if "R" not in _base:
        _base["R"] = M.load_kross()
    return copy.deepcopy(_base["R"])


def get_anchor():
    if "A" not in _base:
        _base["A"] = M.load_sparc_anchor()
    return _base["A"]


# ------------------------------------------------------------------ one sample's Delta'(mu) curve
class Curve:
    """Delta'(mu), sigma(mu) for both laws of one sample under one prescription; results cached per mu."""

    def __init__(self, S, AS, sp, sp_anchor=None, gas_scale=2.0, anchor_mode="pooled", swap=False, sig_f=None, anchor_floor=True):
        self.anchor_floor = anchor_floor
        self.S, self.AS, self.sp = S, AS, sp
        self.spa = sp_anchor if sp_anchor is not None else sp
        self.gs = gas_scale
        self.anchor_mode = anchor_mode
        self.swap = swap
        self.sig_f = sig_f          # None, or f: sigma_f = sqrt(f^2 raw_err^2 + anchor_err^2)
        self._c = {}
        ap = M.anchor_pool(self.spa, 0.0, "canonical", AS)
        self.am, self.ae, _ = ap["flat"]
        if anchor_mode == "median":
            self.am = ap["median_flat"]
        self.anchor_offset = ap["flat"][0]

    def at(self, mu):
        key = round(float(mu), 12)
        r = self._c.get(key)
        if r is None:
            po = M.per_object(self.S, self.sp, float(mu), 0.0, "canonical", gas_scale=self.gs)
            r = {}
            for law in LAWS:
                m, e, _c = M.pool(po["d_" + law], po["e_" + law])
                if self.sig_f is not None:
                    e_used = math.sqrt((self.sig_f * e) ** 2)      # raw error scaled; anchor floor added below
                    sg = math.sqrt(e_used ** 2 + (self.ae ** 2 if self.anchor_floor else 0.0))
                else:
                    sg = math.sqrt(e ** 2 + self.ae ** 2)
                r[law] = (m - self.am, sg)
            self._c[key] = r
        return r

    def dp(self, mu, law):
        if self.swap:
            law = "H" if law == "flat" else "flat"
        return self.at(mu)[law][0]

    def sg(self, mu, law):
        if self.swap:
            law = "H" if law == "flat" else "flat"
        return self.at(mu)[law][1]


def _first_root(fun, grid, vals):
    """first sign change of vals over grid; returns (root or None, n_sign_changes)"""
    s = np.sign(vals)
    idx = [i for i in range(len(grid) - 1) if s[i] != s[i + 1] and s[i] != 0 and s[i + 1] != 0]
    zero = [i for i in range(len(grid)) if s[i] == 0]
    if zero:
        return float(grid[zero[0]]), len(zero)
    if not idx:
        return None, 0
    i = idx[0]
    return float(brentq(fun, grid[i], grid[i + 1], xtol=1e-12, rtol=1e-12)), len(idx)


def breakeven(cv, law, lo=MU_LO, hi=MU_HI, ngrid=NGRID, conv="A", f=None):
    """Returns dict: mu (central root or None), mu_lo (root of D'=+sigma), mu_hi (root of D'=-sigma), each None when missing;
    lo_open / hi_open flags say the missing edge lies outside [lo, hi]; nroots = # sign changes of the central function.
    conv A: sigma frozen at the central root.  conv B: sigma(mu) recomputed at each mu."""
    grid = np.geomspace(lo, hi, ngrid)
    d = np.array([cv.dp(m, law) for m in grid])
    mu0, nr = _first_root(lambda m: cv.dp(m, law), grid, d)
    out = dict(mu=mu0, mu_lo=None, mu_hi=None, nroots=nr, sigma=None, lo_open=False, hi_open=False)
    if mu0 is None:
        return out
    sig0 = cv.sg(mu0, law)
    out["sigma"] = sig0
    if conv == "A":
        fp = lambda m: cv.dp(m, law) - sig0
        fm = lambda m: cv.dp(m, law) + sig0
    else:
        fp = lambda m: cv.dp(m, law) - cv.sg(m, law)
        fm = lambda m: cv.dp(m, law) + cv.sg(m, law)
    vp = np.array([fp(m) for m in grid])
    vm = np.array([fm(m) for m in grid])
    r_lo, _ = _first_root(fp, grid, vp)
    r_hi, _ = _first_root(fm, grid, vm)
    out["mu_lo"], out["mu_hi"] = r_lo, r_hi
    out["lo_open"] = r_lo is None
    out["hi_open"] = r_hi is None
    return out


def r_law(bU, bK):
    """R_law = mu_be(KURVS)/mu_be(KROSS) with the frozen conservative interval; open sides: lo -> 0, hi -> inf.
    Returns None when a central root is missing."""
    if bU["mu"] is None or bK["mu"] is None:
        return None
    R = bU["mu"] / bK["mu"]
    # R_lo = mu_lo(U)/mu_hi(K); missing mu_lo(U) -> 0 ; missing mu_hi(K) -> R_lo = 0
    if bU["mu_lo"] is None or bK["mu_hi"] is None:
        Rlo = 0.0
    else:
        Rlo = bU["mu_lo"] / bK["mu_hi"]
    if bU["mu_hi"] is None or bK["mu_lo"] is None:
        Rhi = math.inf
    else:
        Rhi = bU["mu_hi"] / bK["mu_lo"]
    # quadrature interval (attack A5); an open side stays open
    q = dict(lo=0.0, hi=math.inf)
    if bU["mu_lo"] is not None and bK["mu_hi"] is not None:
        aU = math.log(bU["mu"] / bU["mu_lo"])
        aK = math.log(bK["mu_hi"] / bK["mu"])
        q["lo"] = R * math.exp(-math.hypot(aU, aK))
    if bU["mu_hi"] is not None and bK["mu_lo"] is not None:
        bUu = math.log(bU["mu_hi"] / bU["mu"])
        bKk = math.log(bK["mu"] / bK["mu_lo"])
        q["hi"] = R * math.exp(math.hypot(bUu, bKk))
    return dict(R=R, lo=Rlo, hi=Rhi, qlo=q["lo"], qhi=q["hi"])


# ------------------------------------------------------------------ R_obs and the rule
DZ_E, DZ_SE, SLOPE_IN = 0.23, 0.52, -0.30
EXP_LIT, SLOPE_LIT, LIT_ALLOW = 2.5, -0.36, 0.20


def robs(zU, zK, logMU, logMK):
    """medians -> dict of brackets"""
    fz = (1 + zU) / (1 + zK)
    dm = logMU - logMK
    mass_in = 10 ** (SLOPE_IN * dm)
    mass_lit = 10 ** (SLOPE_LIT * dm)
    Rin = fz ** DZ_E * mass_in
    def inrep(k):
        return (fz ** (DZ_E - k * DZ_SE) * mass_in, fz ** (DZ_E + k * DZ_SE) * mass_in)
    Rlit = fz ** EXP_LIT * mass_lit
    def litb(a):
        return (Rlit * (1 - a), Rlit * (1 + a))
    return dict(fz=fz, dm=dm, mass_in=mass_in, mass_lit=mass_lit, Rin=Rin, Rlit=Rlit, inrep=inrep, litb=litb)


def disfav_overlap(rl, br, quad=False):
    lo, hi = (rl["qlo"], rl["qhi"]) if quad else (rl["lo"], rl["hi"])
    return bool(lo > br[1] or hi < br[0])


def disfav_literal(rl, br, quad=False):
    lo, hi = (rl["qlo"], rl["qhi"]) if quad else (rl["lo"], rl["hi"])
    R = rl["R"]
    if R > br[1]:
        return bool((R - br[1]) > (R - lo))
    if R < br[0]:
        return bool((br[0] - R) > (hi - R)) if math.isfinite(hi) else False
    return False


# ------------------------------------------------------------------ prescriptions
def sp_scaled(s, **kw):
    return M.spec("P4", scale=float(s), **kw)


def solve_pair(Sk, Su, AS, s, spK=None, spU=None, gsK=2.0, gsU=2.0, anchor_mode="pooled", swap=False, lo=MU_LO, hi=MU_HI,
               ngrid=NGRID, conv="A", sig_f=None, anchor_floor=True):
    """break-evens for both laws in both samples at prescription s.  Returns dict law -> dict(U=..., K=..., R=...)"""
    spK = spK if spK is not None else sp_scaled(s)
    spU = spU if spU is not None else sp_scaled(s)
    cK = Curve(Sk, AS, spK, gas_scale=gsK, anchor_mode=anchor_mode, swap=swap, sig_f=sig_f, anchor_floor=anchor_floor)
    cU = Curve(Su, AS, spU, gas_scale=gsU, anchor_mode=anchor_mode, swap=swap, sig_f=sig_f, anchor_floor=anchor_floor)
    out = {}
    for law in LAWS:
        bU = breakeven(cU, law, lo, hi, ngrid, conv)
        bK = breakeven(cK, law, lo, hi, ngrid, conv)
        out[law] = dict(U=bU, K=bK, R=r_law(bU, bK))
    out["curves"] = (cU, cK)
    return out


def fmtR(r):
    if r is None:
        return "no break-even"
    hi = "open" if not math.isfinite(r["hi"]) else f"{r['hi']:.2f}"
    lo = "open" if r["lo"] <= 0 else f"{r['lo']:.2f}"
    return f"{r['R']:.2f} [{lo}, {hi}]"


def fmtB(b):
    if b["mu"] is None:
        return "no be"
    lo = "<0.01" if b["mu_lo"] is None else f"{b['mu_lo']:.3f}"
    hi = ">30" if b["mu_hi"] is None else f"{b['mu_hi']:.3f}"
    return f"{b['mu']:.3f} [{lo}, {hi}]"


# ------------------------------------------------------------------ mocks
def mock_sample(S, sp, law, mu_true, off_dex, rng, anchor_off, ret_floor=False):
    """new mock generator (CFG180 frozen C): true baryons = catalogue x 10^eps_M; g = 10^(anchor_off + off) * law(g_bar_true);
    V_mock^2 = g R - C(observed sigma), floored at 0.25% of g R; inclination noise and velocity noise added."""
    n = len(S.R)
    Sm = copy.deepcopy(S)
    St = copy.deepcopy(S)
    St.logM = S.logM + rng.normal(0.0, S.mass_err, n)
    gb = M.gbar(St, mu_true, 0.0)
    a = A0["canonical"] * (1.0 if law == "flat" else M.E_of_z(S.z))
    g = M.gpred(gb, a) * 10.0 ** (anchor_off + off_dex)
    Vc2 = g * S.R * M.KPC / 1e6
    C, _ = M.corr(S, sp)
    V2 = Vc2 - C
    floor = 0.0025 * Vc2
    fl = V2 < floor
    V2 = np.where(fl, floor, V2)
    Vt = np.sqrt(V2)
    di = rng.normal(0.0, S.einc)
    Vm = Vt * np.sin(S.inc) / np.sin(S.inc + di)
    Vm = Vm + rng.normal(0.0, S.eV)
    Sm.V = Vm
    if ret_floor:
        return Sm, int(fl.sum())
    return Sm
