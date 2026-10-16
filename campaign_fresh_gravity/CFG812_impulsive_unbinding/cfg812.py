#!/usr/bin/env python3
"""CFG812 (FROZEN_CRITERIA.md 39f34ed7f): H-UB = CFG809 split H-EX + impulsive unbinding of freed cold energy; H-EX - free cold energy from EXPELLED gas; CFG727 machinery with the census f_ret(M_ta)
catchment (fixed point) and the all-retained tethered source. Derived from CFG727 (H-HT): Bookkeeping = CFG721's condensed source (supply 5.364 x catchment; tethered = condensed-source law phantom within supply;
free = the rest, CFG637 Method A). New here: the DECLARED stellar placement (BCG Hernquist R_e = 0.015 R_X, catalogue BCG mass
where present, members rho ~ r^-2.5 over 0.1-1 R_X; brackets R_e x0.5/x2, slope -2/-3).
Stages (CFG727_MODE): erass | accept | efeds | score (work files in ../_external_data/cfg727_work). T-K KiDS is read from CFG721's
stored condensed-source rows (identical construction; predetermined FAIL, addendum). Run ONLY after T1x.
kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg812_work")
W721 = os.path.join(EXT, "cfg721_work"); os.makedirs(WORK, exist_ok=True)
for d in (LANES, os.path.join(LANES, "CFG637_derived_reservoir"), os.path.join(LANES, "CFG652_hot_group_discriminator"),
          os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose")):
    sys.path.insert(0, d)
try:
    os.nice(10)
except OSError:
    pass
import cfg637_lib as L                                              # noqa: E402
import CFG4_common as C4                                            # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import cfg652_model as M652                                     # noqa: E402
MODE = os.environ.get("CFG812_MODE", "score")
MUT = os.environ.get("CFG727_MUTATE", "0") == "1"
T0 = time.time(); LOG = []
N_SH = 600


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def nu_s(y):                                                         # CFG695 / CFG720: g_N = g^2/(g + a0)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


KERN = {"mono": C4.nu_mono, "s": nu_s}
# ADDENDUM c5c6894a6 (H-OF2): tethered phantom capped at mean Sigma <= a0/(pi G)  <=>  (nu - 1) <= 1/y
KCAP = {k + "_cap": (lambda y, f=f: np.minimum(f(y), 1.0 + 1.0 / np.maximum(np.asarray(y, float), 1e-300))) for k, f in KERN.items()}
KALL = dict(KERN, **KCAP)
A0SI = {"canonical": C4.A0["canonical"], "alt": C4.A0["alt"]}
FEET = ("canonical", "alt")
CASES = [("s", f, "EX") for f in FEET] + [("mono", f, "EX") for f in FEET] + [("s", "canonical", "ALL")]


class InfallEX(L.Infall):
    """CFG809: settling capped at the RETAINED share of the turned cold energy (cold_turned x f_ret); the expelled share stays free."""
    def core_set(self, r, rta, Mret_turned, cold_turned, draw=True):
        return super().core_set(r, rta, Mret_turned, cold_turned * self.fret, draw)


UNBIND = os.environ.get("CFG812_NO_UNBIND", "0") != "1"


class InfallUB(InfallEX):
    """CFG812: final profile in the potential WITHOUT the expelled (diffuse) baryons; residual cold elements with no outer
    turning point inside the grid under that potential are unbound and dropped."""
    def final_profile(self, nr=500, ntheta=160):
        import math as _m
        G_, OL_, H0_ = L.G, L.OL, L.H0
        rta = self.rta
        rg = np.geomspace(1e-3, 4.0, nr) * rta
        Mc, mph, target, xe = self.core_set(None, rta, self.Mret_t, self.cold_t)
        fset = min(1.0, self.drawn / target) if target > 0 else 0.0
        Mfix = np.interp(rg / rta, self.x_core, Mc + fset * mph, left=0.0)
        self.M_core_g = np.interp(rg / rta, self.x_core, Mc, left=0.0)
        self.M_set_g = np.interp(rg / rta, self.x_core, fset * mph, left=0.0)
        mg = np.where(self.turned, (0.0 if UNBIND else 1.0) * self.m_bdiff + self.m_cold, self.dm)
        o = np.argsort(self.r)
        Msh = np.interp(rg, self.r[o], np.cumsum(mg[o]), left=0.0)
        Mtot = Mfix + Msh
        g = G_ * Mtot / rg ** 2 - OL_ * H0_ ** 2 * rg
        Phi = np.zeros(nr)
        Phi[-1] = -G_ * Mtot[-1] / rg[-1] - 0.5 * OL_ * H0_ ** 2 * rg[-1] ** 2
        seg = 0.5 * (g[1:] + g[:-1]) * np.diff(rg)
        Phi[:-1] = Phi[-1] - np.cumsum(seg[::-1])[::-1]
        self.rg, self.Mtot_g, self.Phi_g = rg, Mtot, Phi
        res = np.where(self.turned & (self.m_cold > 0))[0]
        lrg = np.log(rg)
        Mres = np.zeros(nr); Etot = 0.0; mb = 0.0; mall = 0.0
        th = (np.arange(ntheta) + 0.5) / ntheta * _m.pi
        for i in res:
            ri, vi, j2, m = self.r[i], self.v[i], self.j2[i], self.m_cold[i]
            mall += m
            Pe = np.interp(np.log(max(ri, rg[0])), lrg, Phi) + 0.5 * j2 / ri ** 2
            E = 0.5 * vi ** 2 + Pe
            f = E - (Phi + 0.5 * j2 / rg ** 2)
            ki = int(np.searchsorted(rg, ri)); ki = min(max(ki, 1), nr - 1)
            below = np.where(f[:ki] < 0)[0]; above = np.where(f[ki:] < 0)[0]
            if not len(above) and UNBIND:
                continue                                              # unbound under the shallower potential: leaves
            mb += m
            Etot += m * E
            if len(below):
                k = below[-1]; rp = rg[k] + (rg[k + 1] - rg[k]) * (-f[k]) / (f[k + 1] - f[k])
            else:
                rp = rg[0]
            if len(above):
                k = ki + above[0] - 1; ra = rg[k] + (rg[k + 1] - rg[k]) * f[k] / (f[k] - f[k + 1])
            else:
                ra = rg[-1]
            ra = max(ra, ri); rp = min(rp, ri)
            rr = rp + (ra - rp) * 0.5 * (1 - np.cos(th))
            ff = np.maximum(E - (np.interp(np.log(rr), lrg, Phi) + 0.5 * j2 / rr ** 2), 0.0)
            vr = np.sqrt(2 * ff); drdth = (ra - rp) * 0.5 * np.sin(th)
            w = np.where(vr > 0, drdth / np.maximum(vr, 1e-30), 0.0)
            if w.sum() <= 0:
                Mres += m * (rg >= ri); continue
            cw = np.cumsum(w) / w.sum()
            Mres += m * np.interp(rg, rr, cw, left=0.0, right=1.0)
        self.M_res_g = Mres; self.E_res = Etot
        self.M_res_tot = float(mb); self.bound_frac = (mb / mall) if mall > 0 else 1.0
        return self


def derive_ex(M_ta, fret, r_obs, Mcore_obs, Msrc_obs, a0, nu, a_obs=1.0, tol=0.01, **kw):
    _orig = L.Infall
    L.Infall = InfallUB
    try:
        return L.derive(M_ta, fret, r_obs, Mcore_obs, Msrc_obs, a0, nu, a_obs=a_obs, tol=tol, **kw)
    finally:
        L.Infall = _orig


def fret_of(lM):                                                      # CFG416 / CFG556 census, verbatim
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def catch_ex(Mc_tot, Mhot_tot):
    """H-EX catchment: bc = max(Mc/0.10, retained/f_ret(M_ta)), M_ta = bc/f_b (fixed point)."""
    ret = Mc_tot + Mhot_tot; f = 0.9
    for _ in range(200):
        bc = max(Mc_tot / M652.F_COND_FLOOR, ret / f)
        fn = fret_of(math.log10(bc / L.FB))
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    bc = max(Mc_tot / M652.F_COND_FLOOR, ret / f)
    return bc, M652.COLD_PER_B * bc, ret / bc


def placement(variant):
    re_fac = {"Re0.5": 0.5, "Re2": 2.0}.get(variant, 1.0)
    slope = {"sl-2": -2.0, "sl-3": -3.0}.get(variant, -2.5)
    return re_fac, slope


def cond_profile(r, Mstar, Rx, variant, Mbcg=None):
    """declared stellar placement: BCG Hernquist R_e = 0.015 R_X x re_fac (catalogue mass if given, else half), members rho ~ r^slope on 0.1-1 R_X."""
    re_fac, sl = placement(variant)
    mb = 0.5 * Mstar if (Mbcg is None or not np.isfinite(Mbcg) or Mbcg <= 0) else min(float(Mbcg), Mstar)
    bcg = M652.hern(r, mb, 0.015 * Rx * re_fac)
    r1, r2 = 0.1 * Rx, Rx
    q = sl + 3.0
    f = (lambda x: np.log(x)) if abs(q) < 1e-9 else (lambda x: x ** q)
    rr = np.clip(r, r1, r2)
    mem = (Mstar - mb) * (f(rr) - f(r1)) / (f(r2) - f(r1))
    return bcg + mem


def run_system(r_obs, Mcond, Mhot, z, foot, kern, variant, N=N_SH):
    """CFG721 condensed-source bookkeeping (variant ALL = all-baryon source, the M0 control)."""
    p = 1.0
    Mhot_tot = float(Mhot[-1]); Mc_tot = float(Mcond[-1])
    if variant == "EX":
        bc, supply, fret = catch_ex(Mc_tot, Mhot_tot)
    else:
        bc = max(p * Mc_tot / M652.F_COND_FLOOR, (Mc_tot + Mhot_tot) / M652.F_RET_XCOP)
        supply = M652.COLD_PER_B * bc; fret = (Mc_tot + Mhot_tot) / bc
    M_ta = bc / L.FB
    core = Mcond + Mhot
    I = (derive_ex if variant == "EX" else L.derive)(M_ta, fret, r_obs, core, (core if variant in ("ALL", "EX") else Mcond), A0SI[foot] * L.SI_TO_KPCGYR2, KALL[kern], a_obs=1.0 / (1.0 + z), N=N)
    s = supply / I.supply_turned
    cons = abs(I.drawn + I.M_res_tot - I.supply_turned) / I.supply_turned
    meta = dict(rta=I.rta, x_edge=I.x_edge, supply=supply, fret=fret, M_ta=M_ta, res_frac=I.M_res_tot / I.supply_turned,
                settled_frac=I.drawn / I.supply_turned, cons=cons, bound_frac=getattr(I, 'bound_frac', 1.0), turned=I.M_turned / M_ta, variant=variant)
    return I.rg, I.M_core_g, I.M_set_g * s, I.M_res_g * s, meta


def rx_of(Mhot):                                                     # eRASS1 catalogue Mgas500-R500 power law (aperture only), kpc
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    p = np.polyfit(np.log10(d["mg"]), np.log10(d["R500"]), 1)
    return 1000.0 * 10 ** (p[0] * np.log10(Mhot) + p[1]), p


R_OBS = np.geomspace(0.5, 6e4, 900)



# ============================================================================================ cluster projection (CFG686/687 code)
G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KG = MSUN / (3.0857e16) ** 2
RGRID = np.logspace(-3, np.log10(30), 3000); U_GRID = np.linspace(0, 1, 4001)
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1])


def sigma_proj(rhoL, r, R):                       # CFG686 RUN3, with a floor so a truncated density projects as zero beyond r_ta
    umax = np.arccosh(r[-1] / R); u = U_GRID * umax; rr = R * np.cosh(u)
    rho_u = np.exp(np.interp(np.log(rr), np.log(r), np.log(np.maximum(rhoL, 1e-300))))
    return 2 * np.trapz(rho_u * rr * MPC, u)


def dsig_from_M(ML_msun):
    """CFG687 law() projection for a cumulative mass on RGRID (Mpc grid, Msun) -> DeltaSigma at RC (Msun/pc^2)."""
    ML = ML_msun * MSUN; r = RGRID
    rhoL = np.gradient(ML, r * MPC) / (4 * np.pi * (r * MPC) ** 2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4 * np.pi * (r[r > R] * MPC) ** 2 * rhoL[r > R] * (1 - np.sqrt(1 - (R / r[r > R]) ** 2)), r[r > R] * MPC) for R in RC])
    return (M2 / (np.pi * (RC * MPC) ** 2) - Sig) / KG


def law_M(Mb_msun, foot, kern):
    gb = G * Mb_msun * MSUN / (RGRID * MPC) ** 2
    return Mb_msun * KALL[kern](gb / A0SI[foot])


def cluster_runs(Mg_rgrid, fs, z, Rx_kpc, Mbcg=None):
    rk = RGRID * 1000.0
    mg = np.interp(R_OBS, rk, Mg_rgrid, left=0.0, right=Mg_rgrid[-1])
    out = {"M0": {}}
    for kern in KERN:
        for foot in FEET:
            out["M0"][f"{kern}|{foot}"] = dsig_from_M(law_M(Mg_rgrid * (1 + fs), foot, kern))   # CFG687/686 reproduction control
    for kern, foot, v in CASES:
        mc = cond_profile(R_OBS, fs * Mg_rgrid[-1], Rx_kpc, v, Mbcg)
        MbR = np.interp(rk, R_OBS, mc + mg)
        rg, Mcore, Mset, Mres, meta = run_system(R_OBS, mc, mg, z, foot, kern, v)
        setR = np.interp(rk, rg, Mset, left=0.0, right=Mset[-1]); resR = np.interp(rk, rg, Mres, left=0.0, right=Mres[-1])
        out[f"{kern}|{foot}|{v}"] = dict(base=dsig_from_M(MbR + setR), res=dsig_from_M(resR) if meta["res_frac"] > 0 else np.zeros(8), meta=meta)
    return out


# ============================================================================================ eRASS1 (CFG687)
if MODE == "erass":
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    res = []
    for i in range(len(d["mg"])):
        R5, mgas = float(d["R500"][i]), float(d["mg"][i])
        r = RGRID; rc = 0.15 * R5; shape = (1 + (r / rc) ** 2) ** (-1.0); shape[r > 3.0] = 0      # beta = 2/3
        dm = 4 * np.pi * (r * MPC) ** 2 * shape; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]
        Mg = Mm * (mgas / np.interp(R5, r, Mm))                                                  # Msun (CFG687 normalisation)
        o = cluster_runs(Mg, 0.20, float(d["z"][i]), R5 * 1000.0)
        res.append(o)
        if (i + 1) % 10 == 0:
            P(f"  eRASS1 {i + 1}/{len(d['mg'])} ({time.time() - T0:.0f} s); last free/supply (s, can) {o['s|canonical|EX']['meta']['res_frac']:.3f}")
            np.save(os.path.join(WORK, "erass_partial.npy"), np.array(res, dtype=object), allow_pickle=True)
    np.save(os.path.join(WORK, "erass.npy"), np.array(res, dtype=object), allow_pickle=True)


# ============================================================================================ ACCEPT (CFG686)
if MODE == "accept":
    from scipy.interpolate import PchipInterpolator
    c = 2.998e8; MP = 1.6726e-27
    zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]   # CFG686 verbatim
    DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DMb = np.sqrt(7.942 ** 3 / (0.295 * DHb))
    pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54 / 0.70
    DM = lambda z: pch(np.minimum(np.asarray(z, float), 2.33)) * RD
    prof = {}
    for l in open(os.path.join(EXT, "cfg686_inputs", "accept", "all_profiles.dat")):
        if l.startswith("#"): continue
        p = l.split()
        try: prof.setdefault(p[0], []).append([float(x) for x in p[1:14]])
        except ValueError: pass
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))["clusters"]
    res = []
    for cl in C686:                                                 # CFG686 law_dsigma gas construction, verbatim (beta_shift 0)
        Pp = np.array(prof[cl["key"]]); Pp = Pp[np.argsort(Pp[:, 0])]; rin, rout, ne = Pp[:, 0], Pp[:, 1], Pp[:, 2]
        ok_ = ne > 0; rin, rout, ne = rin[ok_], rout[ok_], ne[ok_]
        zl = cl["z"]; zz = np.linspace(0, zl, 400); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7); DA_acc = np.trapz(1 / E, zz) * c / (70e3 / MPC) / MPC / (1 + zl)
        q = (float(DM(zl)) / (1 + zl)) / DA_acc; rin, rout, ne = rin * q, rout * q, ne * q ** -0.5
        rm = 0.5 * (rin + rout); rho = 1.17 * MP * ne * 1e6
        half = rm >= np.exp(0.5 * (np.log(rm[0]) + np.log(rm[-1]))); b0 = -np.polyfit(np.log(rm[half]), np.log(rho[half]), 1)[0]
        flag = not (b0 >= 1.5); b = 2.0 if flag else b0
        r = RGRID; rho_g = np.interp(r, rm, rho, left=rho[0], right=np.nan)
        out_ = r > rm[-1]; rho_g[out_] = rho[-1] * (r[out_] / rm[-1]) ** (-b); rho_g[r > 3.0] = 0.0
        Mg = np.r_[0, np.cumsum(0.5 * (4 * np.pi * (r[1:] * MPC) ** 2 * rho_g[1:] + 4 * np.pi * (r[:-1] * MPC) ** 2 * rho_g[:-1]) * np.diff(r) * MPC)] / MSUN
        Rx = 1000.0                                                     # fixed point R_X = rx_of(M_gas(<R_X)) (addendum)
        for _ in range(30):
            Rx = float(rx_of(max(float(np.interp(Rx / 1000.0, RGRID, Mg)), 1e10))[0])
        o = cluster_runs(Mg, 0.20, zl, Rx); o["name"] = cl["name"]
        res.append(o)
        P(f"  ACCEPT {cl['name']}: R_X {Rx:.0f}; free/supply (s, can) {o['s|canonical|EX']['meta']['res_frac']:.3f}")
    np.save(os.path.join(WORK, "accept.npy"), np.array(res, dtype=object), allow_pickle=True)
# ============================================================================================ eFEDS (CFG652 model (a) with peak factor p)
def efeds_system(Mcond, Mhot, Rx, z, foot, kern, variant, Mbcg=None, N=600):
    """CFG652 model (a) machinery with the declared stellar placement (catalogue BCG mass where present)."""
    r_obs = np.geomspace(0.5, 6e4, 900)
    _, Mh = M652.profiles(Mcond, Mhot, Rx, r_obs, gas_trunc=2.0)
    Mc = cond_profile(r_obs, Mcond, Rx, variant, Mbcg)
    Mhot_tot = float(Mh[-1])
    bc, supply, fret = (catch_ex(Mcond, Mhot_tot) if variant == "EX" else M652.catchment(Mcond, Mhot_tot))
    M_ta = bc / L.FB
    I = (derive_ex if variant == "EX" else L.derive)(M_ta, fret, r_obs, Mc + Mh, ((Mc + Mh) if variant in ("ALL", "EX") else Mc), M652.A0[foot], KALL[kern], a_obs=1.0 / (1.0 + z), N=N)
    s_ = supply / I.supply_turned
    return dict(rg=I.rg, Mbound=I.M_core_g + I.M_set_g + I.M_res_g * s_, rta=I.rta, res_frac=I.M_res_tot / I.supply_turned)


if MODE == "efeds":
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz"))
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); n = len(I0["z"])
    out = {}
    for kern, foot, p in CASES:
        arr = np.full((n, len(RCg)), np.nan); rf = np.full(n, np.nan)
        for i in range(n):
            if I0["Mcond"][i] <= 0: continue
            o = efeds_system(I0["Mcond"][i], I0["Mhot"][i], I0["Rx_kpc"][i], I0["z"][i], foot, kern, p, I0["Mbcg"][i])
            arr[i] = M652.delta_sigma(o["rg"], o["Mbound"], RCg, rmax=o["rta"]); rf[i] = o["res_frac"]
        out[f"{kern}|{foot}|{p}"] = arr; out[f"rf|{kern}|{foot}|{p}"] = rf
        P(f"  eFEDS {kern} {foot} {p} done; median free/supply {np.nanmedian(rf):.3f} ({time.time() - T0:.0f} s)")
    np.savez(os.path.join(WORK, "efeds_models.npz"), **{k.replace("|", "__"): v for k, v in out.items()})

# ============================================================================================ score
if MODE == "score":
    from scipy.stats import chi2 as CHI2
    RES = {"lane": "CFG812", "criteria": "39f34ed7f"}
    CHK = {}

    def check(name, ok, msg):
        CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

    P(__doc__.split("Stages")[0].strip())
    key = lambda kern, foot, mode: f"{kern}|{foot}|{mode}"
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    ER = list(np.load(os.path.join(WORK, "erass.npy"), allow_pickle=True))
    D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
    order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
    A_of = lambda sel, Pm: {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}

    def jk(fun):
        full = fun(np.ones(n, bool)); reps = [fun(patch != p_) for p_ in range(30)]
        return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}
    rel = np.median(np.abs(np.array([o["M0"]["mono|canonical"] for o in ER]) / d["PL"] - 1), axis=0)
    check("M0 eRASS1 plain law reproduces CFG687 PL", rel.max() <= 0.01, f"max {rel.max():.2e}")
    c1 = max(o[k_]["meta"]["cons"] for o in ER for k_ in o if isinstance(o[k_], dict) and "meta" in o[k_])
    check("C1 supply = settled + free (eRASS1)", c1 < 1e-9, f"max rel {c1:.1e}")
    TR = {}
    P("\n== eRASS1 318 (jackknife 30): pass |A_MID-1| < 2 sig AND |A_OUTER-1| < 2 sig")
    for kern, foot, mode in CASES:
        k = key(kern, foot, mode)
        Ph = np.array([o[k]["base"] + o[k]["res"] for o in ER]); A = jk(lambda s_: A_of(s_, Ph))
        zm, zo = (A["MID"][0] - 1) / A["MID"][1], (A["OUTER"][0] - 1) / A["OUTER"][1]
        mgv = d["mg"]; qq = np.quantile(mgv, [1 / 3, 2 / 3]); TS = [mgv <= qq[0], (mgv > qq[0]) & (mgv <= qq[1]), mgv > qq[1]]
        terc = []
        for t_ in TS:
            full_ = A_of(t_, Ph)["MID"]; reps_ = [A_of(t_ & (patch != p_), Ph)["MID"] for p_ in range(30)]
            sg_ = float(np.sqrt(29 / 30 * np.sum((np.array(reps_) - np.mean(reps_)) ** 2))); terc.append((float(full_), sg_, float((full_ - 1) / sg_)))
        tok = all(abs(t[2]) < 3 for t in terc)
        TR[k] = dict(A=A, Z_mid=zm, Z_outer=zo, terciles=terc, pass_=bool(abs(zm) < 2 and abs(zo) < 2 and tok))
        P(f"  {k:20s}: A INNER {A['INNER'][0]:.2f}+-{A['INNER'][1]:.2f} MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f} (Z {zm:+.1f}) OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f} (Z {zo:+.1f}) | terciles MID " + " ".join(f"{t[0]:.2f}+-{t[1]:.2f}(Z{t[2]:+.1f})" for t in terc) + f" -> {'PASS' if TR[k]['pass_'] else 'FAIL'}")
    ER721 = list(np.load(os.path.join(EXT, "cfg721_work", "erass.npy"), allow_pickle=True))
    PA = np.array([o["s|canonical|all"]["base"] + o["s|canonical|all"]["res"] for o in ER721]); A721 = A_of(np.ones(n, bool), PA)
    A0v = A_of(np.ones(n, bool), np.array([o[key("s", "canonical", "ALL")]["base"] + o[key("s", "canonical", "ALL")]["res"] for o in ER]))
    P(f"  MUTATE M0 (all-baryon source) vs CFG721 'all' (different stellar placement, so approximate): MID {A0v['MID']:.3f} vs {A721['MID']:.3f}, OUTER {A0v['OUTER']:.3f} vs {A721['OUTER']:.3f}")
    Pt = np.array([o[key("s", "canonical", "EX")]["base"] for o in ER]); A1 = A_of(np.ones(n, bool), Pt)
    P(f"  MUTATE M1 (free removed, tethered only): MID {A1['MID']:.3f} vs primary {TR[key('s', 'canonical', 'EX')]['A']['MID'][0]:.3f}")
    sup = np.array([o[key("s", "canonical", "EX")]["meta"]["supply"] for o in ER]); perm = np.random.default_rng(727).permutation(n)
    resd = np.array([o[key("s", "canonical", "EX")]["res"] for o in ER]); Psh = Pt + resd[perm] * (sup / sup[perm])[:, None]
    Ash = A_of(np.ones(n, bool), Psh)
    P(f"  MUTATE M2 (free component shuffled across clusters): MID {Ash['MID']:.3f}, OUTER {Ash['OUTER']:.3f}")
    RES["T_R"] = TR
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
    cls = C686["clusters"]; AC = list(np.load(os.path.join(WORK, "accept.npy"), allow_pickle=True))
    D_ = np.nan_to_num(np.array([x["dsig"] for x in cls])); E_ = np.array([x["err"] for x in cls]); W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)

    def bandA(Pm, sel):
        o_ = {}
        for b, j in BANDS.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * Pm[sel][:, j]).sum(); o_[b] = num / den if den != 0 else np.nan
        return o_
    TA = {}
    P("\n== ACCEPT 8 (bootstrap 1000, seed 1); pass |A_OUTER-1| < 2 sig")
    for kern, foot, mode in CASES:
        k = key(kern, foot, mode); Pm = np.array([o[k]["base"] + o[k]["res"] for o in AC])
        A = bandA(Pm, np.arange(len(cls))); rb = np.random.default_rng(1)
        boots = [bandA(Pm, rb.integers(0, len(cls), len(cls))) for _ in range(1000)]
        sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}; zo = (A["OUTER"] - 1) / sig["OUTER"]
        TA[k] = dict(A={b: [float(A[b]), sig[b]] for b in BANDS}, Z_outer=float(zo), pass_=bool(abs(zo) < 2))
        P(f"  {k:20s}: A INNER {A['INNER']:.2f} MID {A['MID']:.2f} OUTER {A['OUTER']:.2f}+-{sig['OUTER']:.2f} (Z {zo:+.1f}) -> {'PASS' if TA[k]['pass_'] else 'FAIL'}")
    RES["T_A"] = TA
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz")); D0 = np.load(os.path.join(W652, "cfg652_esd.npz")); EM = np.load(os.path.join(WORK, "efeds_models.npz"))
    keep = I0["Mcond"] > 0
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); USE = (RCg >= 50) & (RCg <= 1000); NPATCH = 30
    Dd = {k: (D0[k][keep] if k in ("WG", "WX", "WW", "NN", "pg") else D0[k]) for k in D0.files}

    def esd(sel_g, sel_r):
        Wg = Dd["WW"][sel_g].sum(0); Wr = Dd["rWW"][sel_r].sum(0)
        g = Dd["WG"][sel_g].sum(0) / np.where(Wg > 0, Wg, np.nan); r = Dd["rWG"][sel_r].sum(0) / np.where(Wr > 0, Wr, np.nan)
        boost = (Dd["NN"][sel_g].sum(0) / max(sel_g.sum(), 1)) / (Dd["rNN"][sel_r].sum(0) / max(sel_r.sum(), 1))
        return boost * g - r

    def model_stack(arr, sel_g):
        Wm = Dd["WW"][sel_g]
        return (Wm * arr[sel_g]).sum(0) / np.where(Wm.sum(0) > 0, Wm.sum(0), np.nan)
    allg = np.ones(int(keep.sum()), bool); allr = np.ones(len(Dd["rz"]), bool)
    vals = np.array([esd(Dd["pg"] != p_, Dd["pr"] != p_)[USE] for p_ in range(NPATCH)]); mv = vals.mean(0)
    C = (NPATCH - 1) / NPATCH * (vals - mv).T @ (vals - mv); nb = int(USE.sum()); Ci = np.linalg.inv(C) * (NPATCH - nb - 2) / (NPATCH - 1)
    obs = esd(allg, allr); TE = {}
    P("\n== eFEDS 131; pass chi2 p >= 0.01")
    for kern, foot, mode in CASES:
        k = key(kern, foot, mode); ms = model_stack(EM[k.replace("|", "__")][keep], allg); dd = obs[USE] - ms[USE]
        ch = float(dd @ Ci @ dd); pv = float(CHI2.sf(ch, nb)); TE[k] = dict(chi2=ch, p=pv, pass_=bool(pv >= 0.01))
        P(f"  {k:20s}: chi2 {ch:.1f}/{nb} p {pv:.3g} -> {'PASS' if pv >= 0.01 else 'FAIL'}")
    RES["T_E"] = TE
    P("\n== KiDS early - late: NOT SCORED here (rule changes galaxy-scale supply; separate T-K rerun needed; stated in criteria)")
    P("\n== VERDICT (nu_s; PASS = eRASS1 (incl. terciles) + ACCEPT + eFEDS on >= 1 footing; PARTIAL = two of three)")
    best = 0
    for foot in FEET:
        k = key("s", foot, "EX"); r3 = [TR[k]["pass_"], TA[k]["pass_"], TE[k]["pass_"]]
        P(f"  {foot}: eRASS1 {r3[0]}, ACCEPT {r3[1]}, eFEDS {r3[2]}"); best = max(best, sum(r3))
    V = "PASS" if best == 3 else ("PARTIAL" if best == 2 else "FAIL")
    kA = key("s", "canonical", "ALL")
    P(f"  K1 ALL control: eRASS1 MID {TR[kA]['A']['MID'][0]:.3f} (CFG727 1.40), ACCEPT OUTER {TA[kA]['A']['OUTER'][0]:.3f} (0.92), eFEDS chi2 {TE[kA]['chi2']:.1f} (29.4)")
    bf_ = np.array([o[key("s", "canonical", "EX")]["meta"].get("bound_frac", 1.0) for o in ER]); mgv_ = d["mg"]; qq_ = np.quantile(mgv_, [1 / 3, 2 / 3])
    P("  bound fraction of freed cold energy, median per gas tercile: " + " / ".join(f"{np.median(bf_[t_]):.3f}" for t_ in (mgv_ <= qq_[0], (mgv_ > qq_[0]) & (mgv_ <= qq_[1]), mgv_ > qq_[1])))
    P(f"  -> {V}")
    RES["verdict"] = V; RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg812_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg812.out"), "w").write("\n".join(LOG) + "\n")

if MODE != "score":
    open(os.path.join(HERE, f"cfg812_{MODE}.log"), "w").write("\n".join(LOG) + f"\nelapsed {time.time() - T0:.0f} s\n")
