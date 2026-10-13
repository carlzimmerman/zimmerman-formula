#!/usr/bin/env python3
"""CFG652 model library: projected excess surface density DeltaSigma(R) of a group / cluster with given CONDENSED (stars + cold
gas) and HOT-gas masses under
  (a) THEORY v2 (A5 + A6 + A7): the law's round phantom is sourced by the CONDENSED baryons only; supply is the host's own;
      the rest of the supply is unsettled cold energy, collisionless, placed by the CFG637 Method A infall derivation (H-CB);
  (b) CANDIDATE B: the phantom is sourced by ALL retained baryons (condensed + hot); reservoir from the same derivation
      (CFG637: it comes out empty wherever the phantom eats the supply).
Everything except the phantom source is IDENTICAL between (a) and (b): same baryons, same catchment, same supply, same infall.

Declared model inputs (frozen in FROZEN_CRITERIA.md before any data comparison):
  * condensed profile: half in a central galaxy (Hernquist, R_e = 15 kpc), half in members (Hernquist, R_e = 0.5 R_X);
  * hot gas: beta-model beta = 2/3, r_c = 0.234 R_X (CFG543 K4, derived from the on-disk Lovisari table), normalised to
    M_hot(<R_X), extended to 2 R_X and constant beyond (CFG543 G2 geometry); R_X = the X-ray aperture radius (R500 label of
    the X-ray catalogue, used purely as the measured aperture);
  * catchment (one rule spanning the record's two conventions): baryons_cat = max(M_cond / 0.10 [CFG543 P2 progenitor
    containment], (M_cond + M_hot,tot) / 0.90 [CFG634/637 X-COP]); supply = 5.364 x baryons_cat; f_ret = (M_cond +
    M_hot,tot) / baryons_cat; M_ta = baryons_cat / f_b;
  * law: nu_mono (CFG540), footings canonical 9.3603e-11 / alt 1.1312e-10 m s^-2 (CFG4_common), never pooled; a0 flat in z (A4).
Units: kpc, Msun; DeltaSigma in Msun / pc^2. kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory
closed."""
import os, sys, io, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
for d in (LANES, os.path.join(LANES, "CFG637_derived_reservoir"), os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose")):
    if d not in sys.path:
        sys.path.insert(0, d)
import cfg637_lib as L                                       # noqa: E402
import CFG4_common as C4                                     # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import cfg540_bfjr as C540                               # noqa: E402

NU = C540.nu
A0 = {"canonical": C4.A0["canonical"] * L.SI_TO_KPCGYR2, "alt": C4.A0["alt"] * L.SI_TO_KPCGYR2}
COLD_PER_B = 5.364
RE_BCG = 15.0
F_BCG = 0.5
RC_OVER_RX = 0.234
GAS_TRUNC = 2.0
F_COND_FLOOR = 0.10
F_RET_XCOP = 0.90
HERN_RE = 1.8153                     # R_e / a for Hernquist


def hern(r, M, Re):
    a = Re / HERN_RE
    return M * r ** 2 / (r + a) ** 2


def beta_cum(r, Mx, Rx, rc_frac=RC_OVER_RX, trunc=GAS_TRUNC):
    rc = rc_frac * Rx
    f = lambda x: x - np.arctan(x)
    rr = np.minimum(r, trunc * Rx)
    return Mx * f(rr / rc) / f(Rx / rc)


def profiles(Mcond, Mhot, Rx, rg, re_bcg=RE_BCG, f_bcg=F_BCG, re_sat_frac=0.5, gas_trunc=GAS_TRUNC):
    Mc = hern(rg, f_bcg * Mcond, re_bcg) + hern(rg, (1 - f_bcg) * Mcond, re_sat_frac * Rx)
    Mh = beta_cum(rg, Mhot, Rx, trunc=gas_trunc) if Mhot > 0 else 0 * rg
    return Mc, Mh


def catchment(Mcond, Mhot_tot, rule="max"):
    p2 = Mcond / F_COND_FLOOR
    xc = (Mcond + Mhot_tot) / F_RET_XCOP
    bc = {"max": max(p2, xc), "P2": max(p2, Mcond + Mhot_tot), "XCOP": xc}[rule]
    return bc, COLD_PER_B * bc, (Mcond + Mhot_tot) / bc


def system(Mcond, Mhot, Rx, z, foot, model, rule="max", N=1000, hot_as_condensed=False, **kw):
    """Method A derivation for one system and one model ('a' = Theory v2, condensed source; 'b' = candidate B, all baryons).
    hot_as_condensed=True is MUTATE M1 (the hot gas relabelled as condensed: (a) must then reproduce (b))."""
    gt = kw.pop("gas_trunc", GAS_TRUNC)
    pk = {k: kw.pop(k) for k in ("re_bcg", "f_bcg", "re_sat_frac") if k in kw}
    r_obs = np.geomspace(0.5, 6e4, 900)
    Mc, Mh = profiles(Mcond, Mhot, Rx, r_obs, gas_trunc=gt, **pk)
    Mhot_tot = float(Mh[-1])
    bc, supply, fret = catchment(Mcond, Mhot_tot, rule)
    M_ta = bc / L.FB
    core = Mc + Mh
    src = core if (model == "b" or hot_as_condensed) else Mc
    a_obs = 1.0 / (1.0 + z)
    I = L.derive(M_ta, fret, r_obs, core, src, A0[foot], NU, a_obs=a_obs, N=N, **kw)
    s = supply / I.supply_turned                         # gate-unit rescale (CFG637 store(), FROZEN 1 there)
    out = dict(rg=I.rg, Mcore=I.M_core_g, Mset=I.M_set_g, Mres=I.M_res_g * s, Mtot=I.Mtot_g, rta=I.rta,
               x_edge=I.x_edge, supply=supply, fret=fret, M_ta=M_ta, res_frac=I.M_res_tot / I.supply_turned,
               settled_frac=I.drawn / I.supply_turned, scale=s, a_obs=a_obs)
    # bound-region mass used for lensing: core + settled + reservoir (diffuse non-retained baryons and unturned shells are
    # identical in (a) and (b) to the derivation's precision and are reported separately)
    out["Mbound"] = out["Mcore"] + out["Mset"] + out["Mres"]
    out["Mdiff"] = np.maximum(I.Mtot_g - (I.M_core_g + I.M_set_g + I.M_res_g), 0.0)
    return out


def delta_sigma(rg, M3, R_kpc, rmax=None):
    """DeltaSigma(R) [Msun/pc^2] of a spherical mass with cumulative profile M3(<r) on rg (kpc), truncated at rmax."""
    if rmax is not None:
        k = rg <= rmax
        rg, M3 = rg[k], M3[k]
    lr = np.log(rg)
    dM = np.gradient(M3, lr)                              # dM/dln r
    rho = np.maximum(dM, 0) / (4 * math.pi * rg ** 3)
    out = []
    for R in np.atleast_1d(R_kpc):
        if R >= rg[-1]:
            out.append(M3[-1] / (math.pi * R ** 2) / 1e6); continue
        # Sigma(R) = 2 int_R^rmax rho r dr / sqrt(r^2 - R^2), with r = R cosh(u)
        umax = np.arccosh(rg[-1] / R)
        u = np.linspace(0, umax, 600)
        r = R * np.cosh(u)
        rh = np.exp(np.interp(np.log(r), lr, np.log(np.maximum(rho, 1e-300))))
        Sig = 2 * np.trapz(rh * r, u)
        # M2D(<R) = M3(<R) + int_R^rmax 4 pi r^2 rho (1 - sqrt(1 - R^2/r^2)) dr
        rr = np.geomspace(R, rg[-1], 600)
        rh2 = np.exp(np.interp(np.log(rr), lr, np.log(np.maximum(rho, 1e-300))))
        M2 = np.interp(math.log(R), lr, M3) + np.trapz(4 * math.pi * rr ** 2 * rh2 * (1 - np.sqrt(np.maximum(1 - (R / rr) ** 2, 0))), rr)
        out.append((M2 / (math.pi * R ** 2) - Sig) / 1e6)
    return np.array(out)
