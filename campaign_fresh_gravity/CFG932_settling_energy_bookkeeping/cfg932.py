#!/usr/bin/env python3
"""CFG932: energy bookkeeping of cold-energy settling (theory spine for H-ELS). FROZEN_CRITERIA.md (dce2a2e3d, committed alone first).

Q1  energy accounting of the record's settling (CFG638 = CFG541 E3 drift + CFG544 FIX-2 OU, G9 gravity): 1-D spherical drift-only test
    of the derived identity d(K + W)/dt = P_drift (+ P_bath), two-sided (FIX-1) and one-sided (E5) deficit.
Q2  cost of reaching the law: Delta E = E(settled law profile + baryons) - E(primordial NFW debris + baryons) inside R_x (end of the
    outermost primordial surplus zone); (b) virial energy in the law's potential [primary], (a) self-consistent 1/2 dW, (c) gross local
    transport.  Primordial debris = NFW to r_ta with the native collapse epoch (EPS F 0.2 / 0.05 / 0.01, PS1) from CFG654's native tables.
Q3  eps_req = Delta E / E_avail (SN 1e49 erg per Msun formed + AGN 0.1 M_BH c^2); universal-coupling window over 72 corners.
Q4  M3 expulsion energy E_M3 / E_avail (the code reading is in the README).
K1 analytic NFW / Plummer binding energies; K2 CFG541 MW-like record numbers; K3 virial cross-check.  MUTATE (CFG932_MUTATE=1):
M1 primordial == settled -> Delta E = 0; M2 a0 -> 1e-6 a0 changes the settled profile.  Outputs cfg932[_MUTATE].out / _results[_MUTATE].json.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg932.py   (one core, < 1 GB)
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; no particle; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
from scipy.special import erfcinv

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG932_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []
def log(s=""):
    print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ constants (kpc, Msun, km/s)
GK = 4.30091e-6                                   # kpc (km/s)^2 / Msun
ERG = 1.989e33 * 1e10                             # Msun (km/s)^2 -> erg
C_KMS = 299792.458
FOOT = {"can": 9.3603e-11, "alt": 1.1312e-10}
def a0k(a0_si): return a0_si * 3.0857e19 / 1e6    # m/s^2 -> (km/s)^2 / kpc
FB = 0.15712579897450307                          # record f_b ((1 - f_b)/f_b = 5.364; CFG541 JSON)
E_SN_PER_MSUN = 1e49                              # erg per Msun formed (declared)
RETURN = 0.4                                      # return fraction (declared): M_formed = M*/0.6
ETA_AGN = 0.1                                     # E_AGN = 0.1 M_BH c^2 (declared)
DC, DVIR = 1.686, 18 * math.pi ** 2               # top-hat collapse threshold, virial overdensity (EdS)
H_FRET = 0.674                                    # h used inside CFG416 fret_of (record)

# ------------------------------------------------------------------ native background (CFG654 A1 primary set), read only
NAT = np.load(os.path.join(HERE, "..", "CFG654_independent_inputs", "cfg654_ics_tables_cmb.npz"))
DTJ = json.load(open(os.path.join(HERE, "..", "CFG654_independent_inputs", "cfg654_delta_ta_cmb.json")))
H_NAT = float(NAT["h"]); OMH2 = float(NAT["omega_b"]) + float(NAT["omega_c"]); OM_NAT = OMH2 / H_NAT ** 2
RHOCRIT100 = 3 * 0.1 ** 2 / (8 * math.pi * GK)    # Msun/kpc^3 per h^2  (H = 100 km/s/Mpc = 0.1 km/s/kpc)
RHOM = RHOCRIT100 * OMH2                           # native mean matter density today, Msun/kpc^3
DTA0 = float(DTJ["D"][0]); assert abs(DTJ["z"][0]) < 1e-12
_lk = np.log(NAT["kh"]); _lp = np.log(NAT["Plin0"])
_s = (_lp[-1] - _lp[-50]) / (_lk[-1] - _lk[-50])   # last-decade log slope (power-law extension beyond k_max)
LKX = np.concatenate([_lk, _lk[-1] + np.linspace(0.01, 7.0, 700)])
PX = np.exp(np.concatenate([_lp, _lp[-1] + _s * (LKX[len(_lk):] - _lk[-1])])); KX = np.exp(LKX)
RHOM_H = RHOCRIT100 * 1e9 * OM_NAT                # (Msun/h)/(Mpc/h)^3
def _W(x):
    x = np.asarray(x, float)
    return np.where(x < 1e-3, 1 - x ** 2 / 10, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-300) ** 3)
def _sig_direct(M):
    R = (3 * M * H_NAT / (4 * math.pi * RHOM_H)) ** (1 / 3)
    return math.sqrt(np.trapz(PX * _W(KX * R) ** 2 * KX ** 3, LKX) / (2 * math.pi ** 2))
_LMG = np.linspace(0.0, 17.5, 701); _LSG = np.log([_sig_direct(10 ** x) for x in _LMG])
def sigM(M): return float(np.exp(np.interp(math.log10(M), _LMG, _LSG)))
SIG8 = math.sqrt(np.trapz(PX * _W(KX * 8.0) ** 2 * KX ** 3, LKX) / (2 * math.pi ** 2))
def Dz(z): return float(np.exp(np.interp(-math.log1p(z), NAT["lna"], NAT["lnD"])))
def z_of_D(Dn):
    if Dn >= 1.0: return 0.0
    return brentq(lambda z: Dz(z) - Dn, 0.0, 1e5)

def mfun(x):
    """ln(1+x) - x/(1+x), with its series below x = 1e-3 (no cancellation)."""
    x = np.asarray(x, float)
    xs = np.minimum(x, 1e-3)
    ser = xs ** 2 / 2 - 2 * xs ** 3 / 3 + 3 * xs ** 4 / 4 - 4 * xs ** 5 / 5
    with np.errstate(divide='ignore', invalid='ignore'):
        full = np.log1p(x) - x / (1 + x)
    return np.where(x < 1e-3, ser, full)

def conc(Mta, rule, F=None):
    """c = r_ta / r_s: mean density inside r_s = 18 pi^2 rhobar_m(z_s); z_s from EPS (progenitors > F M_ta) or PS1 (sigma(M_s) D = dc)."""
    m1 = float(mfun(1.0))
    def z_dens(c): return (DTA0 * c ** 3 * m1 / float(mfun(c)) / DVIR) ** (1 / 3) - 1
    def z_coll(c):
        Ms = Mta * m1 / float(mfun(c))
        if rule == "PS1":
            Dn = DC / sigM(Ms)
        else:
            s2 = sigM(F * Mta) ** 2 - sigM(Mta) ** 2
            x = float(erfcinv(Ms / Mta)); Dn = DC / (DC + x * math.sqrt(2 * s2))
        return z_of_D(Dn)
    f = lambda lc: z_dens(math.exp(lc)) - z_coll(math.exp(lc))
    if f(0.0) > 0: return 1.0, True
    return math.exp(brentq(f, 0.0, math.log(1e4), xtol=1e-12)), False

# ------------------------------------------------------------------ baryon components: (M(<r), dM/dr) in kpc / Msun
def plummer(M, a):
    return (lambda r: M * r ** 3 / (r * r + a * a) ** 1.5, lambda r: 3 * M * a * a * r * r / (r * r + a * a) ** 2.5)
def hernquist(M, a):
    return (lambda r: M * r * r / (r + a) ** 2, lambda r: 2 * M * a * r / (r + a) ** 3)
def expsph(M, R):
    def Mf(r):
        x = np.asarray(r, float) / R; xs = np.minimum(x, 1e-3)
        ser = xs ** 2 / 2 - xs ** 3 / 3 + xs ** 4 / 8 - xs ** 5 / 30
        return M * np.where(x < 1e-3, ser, 1 - (1 + x) * np.exp(-x))
    return (Mf, lambda r: M * (r / R) * np.exp(-r / R) / R)
def beta23(Mnorm, rnorm, rc, rtr):
    K = Mnorm / (rnorm / rc - math.atan(rnorm / rc))
    def Mf(r):
        x = np.minimum(np.asarray(r, float), rtr) / rc; xs = np.minimum(x, 1e-3)
        return K * np.where(x < 1e-3, xs ** 3 / 3 - xs ** 5 / 5 + xs ** 7 / 7, x - np.arctan(x))
    def dMf(r):
        x = r / rc; return np.where(r < rtr, K * x * x / (1 + x * x) / rc, 0.0)
    return Mf, dMf, float(Mf(np.array(rtr)))
def combo(parts):
    return (lambda r: sum(p[0](r) for p in parts), lambda r: sum(p[1](r) for p in parts))

def systems():
    S = []
    for nm, Ms, Re, role in (("UFD-c", 5e3, 0.030, "starved"), ("UFD-e", 3e4, 0.240, "starved"),
                             ("Draco-like", 5e5, 0.220, "starved"), ("Fornax-like", 4e7, 0.710, "fornax")):
        p = plummer(Ms, Re)
        S.append(dict(name=nm, role=role, Mb=p[0], dMb=p[1], Mb_tot=Ms, Mstar_in=(lambda R, Ms=Ms: Ms), MBH=0.0,
                      r_obs=1.305 * Re, gaspoor=True))
    st = expsph(2.6e7, 0.6); gs = expsph(3.66e8, 2.0); b = combo([st, gs])
    S.append(dict(name="SPARC-dwarf", role="rotator", Mb=b[0], dMb=b[1], Mb_tot=2.6e7 + 3.66e8, Mstar_in=lambda R: 2.6e7,
                  MBH=0.0, r_obs=5.0, gaspoor=False))
    hq = hernquist(6e10, 2.5)
    S.append(dict(name="MW-like", role="rotator", Mb=hq[0], dMb=hq[1], Mb_tot=6e10, Mstar_in=lambda R: 5e10, MBH=4.3e6,
                  r_obs=8.0, gaspoor=False))
    gM, gdM, gtot = beta23(1e14, 1200.0, 150.0, 2400.0)
    mM, mdM, mtot = beta23(1e13 * 1200.0 / 1200.0, 1200.0, 150.0, 2400.0)
    sc = 1e13 / mtot                                                  # member + ICL stars: 1e13 in total, shaped like the gas
    bcg = hernquist(1.5e12, 30.0)
    memb = (lambda r: sc * mM(r), lambda r: sc * mdM(r))
    cl = combo([(gM, gdM), bcg, memb])
    S.append(dict(name="cluster-core", role="starved", Mb=cl[0], dMb=cl[1], Mb_tot=gtot + 1.5e12 + 1e13,
                  Mstar_in=lambda R: float(bcg[0](np.array(R)) + memb[0](np.array(R))), MBH=None, r_obs=500.0, gaspoor=False))
    return S

def fret_of(lM):                                                      # CFG416 / CFG650 census law (Msun/h)
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def supply(Mb, L):
    g = lambda lM: 10 ** lM - L * Mb / (fret_of(math.log10(10 ** lM * H_FRET)) * FB)
    lM = brentq(g, math.log10(L * Mb), math.log10(L * Mb / (0.09 * FB)) + 0.5, xtol=1e-13)
    Mta = 10 ** lM; fr = fret_of(math.log10(Mta * H_FRET))
    return Mta, fr

# ------------------------------------------------------------------ phantom (CFG541 E7 round rule, nu - 1 = 1/expm1(sqrt y))
def phantom(sysd, a0):
    Mb, dMb = sysd["Mb"], sysd["dMb"]
    def Mph(r):
        r = np.asarray(r, float); s = np.sqrt(GK * Mb(r) / (r * r * a0))
        with np.errstate(over="ignore"):
            return Mb(r) / np.expm1(s)
    def dMph(r):
        r = np.asarray(r, float); m = Mb(r); dm = dMb(r)
        y = GK * m / (r * r * a0); s = np.sqrt(np.maximum(y, 1e-300))
        dy = GK * (dm / (r * r) - 2 * m / r ** 3) / a0
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            f = 1.0 / np.expm1(s)
            fp = -1.0 / (2 * s) / (np.expm1(s) * (-np.expm1(-s)))
            out = dm * f + m * fp * dy
        return np.where(np.isfinite(out), out, 0.0)
    return Mph, dMph

# ------------------------------------------------------------------ integrals on log grids (Simpson in ln r)
def simpson_ln(fr, r1, r2, n=20001):
    """integral_{r1}^{r2} fr(r) dr with Simpson in ln r (n odd)."""
    lr = np.linspace(math.log(r1), math.log(r2), n); r = np.exp(lr); h = lr[1] - lr[0]
    y = fr(r) * r
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))

def W_self(M, dM, R, rlo_frac=1e-10):
    return -GK * simpson_ln(lambda r: M(r) * dM(r) / r, R * rlo_frac, R)

def dW_diff(Mb, dMb, Mcs, dMcs, Mcp, dMcp, R, rlo_frac=1e-10):
    """W_s(<R) - W_p(<R) as one integral (the baryon self-term cancels exactly)."""
    def f(r):
        mb, dmb = Mb(r), dMb(r); ms, dms, mp, dmp = Mcs(r), dMcs(r), Mcp(r), dMcp(r)
        return (mb * (dms - dmp) + dmb * (ms - mp) + (ms * dms - mp * dmp)) / r
    return -GK * simpson_ln(f, R * rlo_frac, R)

def dE_b(Mb, dMb, Mcs, dMcs, Mcp, R, rlo_frac=1e-10):
    """(b): int_0^R (M_p - M_s) * 1/2 [g_law + G M_law'/r] dr  (virial energy in the fixed law potential)."""
    def f(r):
        ml = Mb(r) + Mcs(r); dml = dMb(r) + dMcs(r)
        return (Mcp(r) - Mcs(r)) * 0.5 * (GK * ml / (r * r) + GK * dml / r)
    return simpson_ln(f, R * rlo_frac, R)

def dE_c(Mb, Mcs, Mcp, R, n=40001):
    """(c): gross local transport, int dm max(0, E_law(r_s(m)) - E_law(r_p(m))); also returns the net (= (b), consistency)."""
    r = np.geomspace(R * 1e-9, R, n)
    ml = Mb(r) + Mcs(r); g = GK * ml / r ** 2
    # Phi relative to R: -int_r^R g dr' (cumulative trapezoid from the outside in)
    seg = 0.5 * (g[1:] + g[:-1]) * np.diff(r)
    phi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    Ec = phi + 0.5 * GK * ml / r
    mp = Mcp(r); ms = Mcs(r); Mt = float(Mcp(np.array(R)))
    u = np.concatenate([np.geomspace(1e-12, 1e-3, 4000), np.linspace(1e-3, 1.0, 36001)[1:]]) * Mt
    rp = np.interp(u, mp, r); rs = np.interp(u, ms, r)
    dE = np.interp(np.log(rs), np.log(r), Ec) - np.interp(np.log(rp), np.log(r), Ec)
    return float(np.trapz(np.maximum(dE, 0.0), u)), float(np.trapz(dE, u))

# ------------------------------------------------------------------ one system, one corner
def evaluate(sysd, a0_si, rule, F, L, a0_scale=1.0, identical=False):
    a0 = a0k(a0_si) * a0_scale
    Mb, dMb = sysd["Mb"], sysd["dMb"]
    Lx = L if sysd["gaspoor"] else 1
    Mta, fr = supply(sysd["Mb_tot"], Lx)
    Mcat = (1 - FB) * Mta
    rta = (3 * Mta / (4 * math.pi * DTA0 * RHOM)) ** (1 / 3)
    c, c_flag = conc(Mta, rule, F)
    rs = rta / c; mc = float(mfun(c))
    Mp = lambda r: (1 - FB) * Mta * mfun(np.minimum(r, rta) / rs) / mc
    dMp = lambda r: np.where(r < rta, (1 - FB) * Mta * (r / rs) / (1 + r / rs) ** 2 / (rs * mc), 0.0)
    Mph, dMph = phantom(sysd, a0)
    # r_*: M_ph(<r_*) = M_cat
    hi = rta
    over = float(Mph(np.array(hi))) < Mcat
    rstar = rta if over else brentq(lambda r: float(Mph(np.array(r))) - Mcat, 1e-9 * rta, hi, xtol=1e-14 * rta)
    Ms = lambda r: np.where(r <= rstar, Mph(np.minimum(r, rstar)), Mcat)
    dMs = lambda r: np.where(r <= rstar, dMph(np.minimum(r, rstar)), 0.0)
    if identical:
        Mp, dMp = Ms, dMs
    # monotonic phantom check on the grid
    rg = np.geomspace(1e-6 * sysd["r_obs"], rstar * (1 - 1e-9), 20001)
    mono = bool(np.all(np.diff(Mph(rg)) >= -1e-12 * Mcat))
    D = Mp(rg) - Ms(rg)
    idx = np.where((D[:-1] > 0) & (D[1:] <= 0))[0]
    Rx = None
    if len(idx):
        i = int(idx[-1])
        Rx = brentq(lambda r: float(Mp(np.array(r)) - Ms(np.array(r))), rg[i], rg[i + 1], xtol=1e-14 * rg[i + 1]) if D[i + 1] < 0 else rg[i + 1]
    Msur = float(max(D.max(), 0.0))
    res = dict(M_ta=Mta, f_ret=fr, L=Lx, M_cat=Mcat, r_ta_kpc=rta, c_ta=c, c_noroot=c_flag, r_s_kpc=rs, r_star_kpc=rstar,
               rstar_beyond_rta=over, phantom_monotone=mono, R_x_kpc=Rx, M_surplus_max=Msur)
    if Rx is not None:
        dWa = dW_diff(Mb, dMb, Ms, dMs, Mp, dMp, Rx)
        res["dE_a_erg"] = 0.5 * dWa * ERG
        res["dE_b_erg"] = dE_b(Mb, dMb, Ms, dMs, Mp, Rx) * ERG
        gc, netc = dE_c(Mb, Ms, Mp, Rx)
        res["dE_c_erg"] = gc * ERG; res["dE_c_net_erg"] = netc * ERG
        res["W_s_Rx_erg"] = (W_self(lambda r: Mb(r) + Ms(r), lambda r: dMb(r) + dMs(r), Rx)) * ERG
    else:
        res.update(dE_a_erg=0.0, dE_b_erg=0.0, dE_c_erg=0.0, dE_c_net_erg=0.0, W_s_Rx_erg=None)
    # whole catchment (infall included)
    res["dE_a_tot_erg"] = 0.5 * dW_diff(Mb, dMb, Ms, dMs, Mp, dMp, rta) * ERG
    res["dE_b_tot_erg"] = dE_b(Mb, dMb, Ms, dMs, Mp, rta) * ERG
    # retained-excess diagnostic at r_obs (one-sided minimiser: max(rho_ph, rho_p))
    ro = sysd["r_obs"]
    Mmax = simpson_ln(lambda r: np.maximum(dMph(r), dMp(r)), ro * 1e-10, ro)
    res["X_ret_dex"] = math.log10((float(Mb(np.array(ro))) + Mmax) / (float(Mb(np.array(ro))) + float(Mph(np.array(ro)))))
    res["Mph_robs"] = float(Mph(np.array(ro))); res["Mp_robs"] = float(Mp(np.array(ro))); res["Mb_robs"] = float(Mb(np.array(ro)))
    # available energy
    Rst = max(Rx or 0.0, ro)
    Mst = sysd["Mstar_in"](Rst)
    res["E_SN_erg"] = E_SN_PER_MSUN * Mst / (1 - RETURN)
    # M3 expulsion energy: census non-retained baryons tracing the primordial NFW, lifted to rest at r_ta
    Mexp = max(FB * Mta - sysd["Mb_tot"], 0.0)
    def e_lift(r):
        x = r / rs
        phi = -(GK * Mta / (rs * mc)) * (np.log1p(x) / x - 1 / (1 + c))
        phit = -GK * Mta / rta
        return phit - phi - 0.5 * GK * Mta * mfun(x) / mc / r
    dMn = lambda r: Mta * (r / rs) / (1 + r / rs) ** 2 / (rs * mc)
    res["M_expelled"] = Mexp
    res["E_M3_erg"] = (Mexp / Mta) * simpson_ln(lambda r: dMn(r) * e_lift(r), rta * 1e-10, rta) * ERG
    return res, (Mp, dMp, Ms, dMs, Mph)

# ------------------------------------------------------------------ K1: analytic binding energies
def K1():
    out = {}
    for cc in (10.0, 30.0):
        M, rsv = 1.0, 1.0; rv = cc * rsv; mcv = float(mfun(cc))
        Mf = lambda r: M * mfun(r / rsv) / mcv; dMf = lambda r: M * (r / rsv) / (1 + r / rsv) ** 2 / (rsv * mcv)
        num = W_self(Mf, dMf, rv)
        ana = -(GK * M * M / (2 * rsv * mcv ** 2)) * (1 - 1 / (1 + cc) ** 2 - 2 * math.log1p(cc) / (1 + cc))
        out[f"NFW_c{int(cc)}"] = dict(num=num, ana=ana, rel=abs(num / ana - 1))
    p = plummer(1.0, 1.0)
    num = W_self(p[0], p[1], 1e5, rlo_frac=1e-12); ana = -3 * math.pi * GK / 32
    out["Plummer"] = dict(num=num, ana=ana, rel=abs(num / ana - 1))
    ok = all(v["rel"] < 1e-6 for v in out.values())
    return ok, out

# ------------------------------------------------------------------ K2: CFG541 MW-like record numbers (its own discretisation, SI)
def K2():
    G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
    j = json.load(open(os.path.join(HERE, "..", "CFG541_cold_energy_equations_precise", "cfg541_results.json")))
    rec = j["one_d"]["can"]["MW"]; fb = j["settings"]["f_b"]
    M = 6e10 * MSUN; a0 = 9.3603e-11; fret = 0.1; a_kpc = 2.5
    Mta = M / (fret * fb); Mcat = (1 - fb) * Mta; rta = rec["rta_kpc"] * KPC
    rin = 1e-2 * a_kpc * KPC; rf = np.geomspace(rin, rta, 401); V = 4 * math.pi / 3 * np.diff(rf ** 3)
    ah = a_kpc * KPC; Mbf = M * rf ** 2 / (rf + ah) ** 2
    y = G * Mbf / (rf ** 2 * a0)
    with np.errstate(over="ignore", divide="ignore"):
        Mphf = Mbf / np.expm1(np.sqrt(y))
    rhoph = np.maximum(np.diff(Mphf), 0.0) / V
    rhoc0 = Mcat / (4 * math.pi / 3 * (rta ** 3 - rin ** 3))
    dens = np.maximum(rhoph, rhoc0); cum = np.concatenate([[0.0], np.cumsum(dens * V)])
    i = int(np.searchsorted(cum, Mcat)) - 1; fr_ = (Mcat - cum[i]) / (cum[i + 1] - cum[i])
    rstar = (rf[i] ** 3 + fr_ * (rf[i + 1] ** 3 - rf[i] ** 3)) ** (1 / 3)
    rel_cat = abs(Mcat / M / rec["Mcat_over_Mb"] - 1); rel_r = abs(rstar / KPC / rec["r_analytic_kpc"] - 1)
    # continuous phantom at r_* vs the phantom cell sum (+ phantom inside rin)
    s = math.sqrt(G * M * rstar ** 2 / (rstar + ah) ** 2 / (rstar ** 2 * a0)); Mph_cont = M * rstar ** 2 / (rstar + ah) ** 2 / math.expm1(s)
    cph = Mphf[0] + np.concatenate([[0.0], np.cumsum(np.diff(Mphf))])
    Mph_cells = cph[i] + fr_ * (cph[i + 1] - cph[i])
    rel_ph = abs(Mph_cells / Mph_cont - 1)
    ok = rel_cat <= 1e-9 and rel_r <= 1e-6 and rel_ph <= 1e-3
    return ok, dict(Mcat_over_Mb=Mcat / M, record_Mcat_over_Mb=rec["Mcat_over_Mb"], rel_Mcat=rel_cat,
                    r_star_kpc=rstar / KPC, record_r_star_kpc=rec["r_analytic_kpc"], rel_r_star=rel_r,
                    Mph_cont_over_Mb=Mph_cont / M, Mph_cells_over_Mb=Mph_cells / M, rel_phantom=rel_ph)

# ------------------------------------------------------------------ K3: virial cross-check (direct isotropic Jeans W + K)
def direct_E(Mtot, dMtot, R, n=200001):
    r = np.geomspace(R * 1e-10, R, n)
    m = Mtot(r); dm = dMtot(r); g = GK * m / r ** 2
    W = -GK * np.trapz(m * dm / r, r)
    rho4 = dm                                           # 4 pi r^2 rho
    integrand = (rho4 / (4 * math.pi * r ** 2)) * g     # dP/dr magnitude
    seg = 0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r)
    P = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    K = 1.5 * np.trapz(P * 4 * math.pi * r ** 2, r)
    return W, K

def K3(S, rows):
    out = {}; ok = True
    for nm in ("MW-like", "Draco-like"):
        sysd = [s for s in S if s["name"] == nm][0]
        res, (Mp, dMp, Ms, dMs, _) = rows[nm]
        Mb, dMb = sysd["Mb"], sysd["dMb"]; rta = res["r_ta_kpc"]
        Wp, Kp = direct_E(lambda r: Mb(r) + Mp(r), lambda r: dMb(r) + dMp(r), rta)
        Ws, Ks = direct_E(lambda r: Mb(r) + Ms(r), lambda r: dMb(r) + dMs(r), rta)
        dE_dir = ((Ws + Ks) - (Wp + Kp)) * ERG; dE_vir = res["dE_a_tot_erg"]
        tol = max(1e-2 * abs(dE_vir), 1e-6 * abs(Ws) * ERG)
        good = abs(dE_dir - dE_vir) <= tol
        out[nm] = dict(dE_direct_erg=dE_dir, dE_half_dW_erg=dE_vir, diff=abs(dE_dir - dE_vir), tol=tol, ok=bool(good)); ok &= good
    return ok, out

# ------------------------------------------------------------------ Q1: 1-D spherical drift-only test (G = 1 units)
def drift_test(two_sided, t_end=200.0, maxsteps=3_000_000):
    G = 1.0; N = 400; alpha = 1.0
    rf = np.geomspace(1e-3, 30.0, N + 1); V = 4 * math.pi / 3 * np.diff(rf ** 3); A = 4 * math.pi * rf ** 2
    rc = np.sqrt(rf[1:] * rf[:-1])
    Mbf = rf ** 3 / (rf ** 2 + 1.0) ** 1.5; Mb_in = Mbf[0]; mb = np.diff(Mbf); rhob = mb / V
    a0 = 0.05
    Mphf = Mbf / np.expm1(np.sqrt(Mbf / (rf ** 2 * a0))); rhoph = np.diff(Mphf) / V
    Mcf = 30.0 * mfun(rf / 3.0) / float(mfun(10.0)); mc = np.diff(Mcf).copy(); mc[0] += Mcf[0]
    def W_Phi(mc):
        mt = mb + mc; Sinc = Mb_in + np.cumsum(mt)
        W = -G * float(np.sum((Sinc - 0.5 * mt) * mt / rc))
        tail = np.cumsum((mt / rc)[::-1])[::-1] - mt / rc
        return W, -G * (Sinc / rc + tail)
    # central surplus zone at t = 0: first face where cumulative cold < phantom
    cum0 = np.cumsum(mc)
    below = cum0[:-1] < Mphf[1:N]
    k1 = int(np.argmax(below)) + 1 if below.any() else N
    Mcen0 = float(mc[:k1].sum())
    W0, Phi = W_Phi(mc); t = 0.0; n = 0; Pacc = Pout = Pin = 0.0
    while t < t_end and n < maxsteps:
        rho = mc / V; rhom = rho + rhob
        cin = np.cumsum(mc)[:-1]                                   # cold mass inside internal faces 1..N-1
        if two_sided:
            dpsi = G * (Mphf[1:N] - cin) / rf[1:N] ** 2
        else:
            d = np.maximum(rhoph - rho, 0.0); Md = np.cumsum(d * V)[:-1]
            dpsi = G * Md / rf[1:N] ** 2
        out_dir = dpsi < 0                                         # v = -alpha tau dpsi > 0 -> outward, donor = inner cell
        donor = np.where(out_dir, np.arange(0, N - 1), np.arange(1, N))
        tau = 1.0 / np.sqrt(4 * math.pi * G * np.maximum(rhom[donor], 1e-300))
        v = -alpha * tau * dpsi
        flux = v * rho[donor] * A[1:N]
        act = np.abs(flux) > 0
        if not act.any(): break
        lim = V[donor][act] / (np.abs(v[act]) * A[1:N][act])
        dt = min(0.2 * float(lim.min()), t_end - t)
        dm = flux * dt
        P = dm * (Phi[1:] - Phi[:-1])
        Pacc += float(P.sum()); Pout += float(P[dm > 0].sum()); Pin += float(P[dm < 0].sum())
        mc[:-1] -= dm; mc[1:] += dm
        mc = np.maximum(mc, 0.0)
        _, Phi = W_Phi(mc); t += dt; n += 1
    W1, _ = W_Phi(mc)
    dW = W1 - W0
    inner = slice(0, k1)
    return dict(two_sided=two_sided, t_end=t, steps=n, W0=W0, dW=dW, dW_over_absW0=dW / abs(W0), int_P_dt=Pacc,
                identity_rel=abs(dW - Pacc) / max(abs(dW), 1e-300), int_P_outward=Pout, int_P_inward=Pin,
                central_zone_r=float(rf[k1]), central_mass_t0=Mcen0, central_mass_end=float(mc[inner].sum()),
                mass_err=abs(mc.sum() - (Mcf[-1])) / Mcf[-1])

# ------------------------------------------------------------------ main
def jsonable(x):
    if isinstance(x, dict): return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jsonable(v) for v in x]
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.bool_,)): return bool(x)
    return x

CUSPS = [("PS1", "PS1", None), ("EPS0.2", "EPS", 0.2), ("EPS0.05", "EPS", 0.05), ("EPS0.01", "EPS", 0.01)]
LS = [1, 10, 100]
MBHS = [1e9, 5e9, 2e10]

def window(eps_req, roles, starved):
    lo = max([eps_req[n] for n in eps_req if roles[n] == "rotator"] + [0.0])
    hi = min([eps_req[n] for n in starved])
    hi_c = min(hi, 1.0)
    nonempty = (lo <= 1.0) and (lo < hi) and (lo < hi_c or hi > 1.0)
    return dict(eps_lo=lo, eps_hi=hi, nonempty=bool(nonempty))

def main():
    log("CFG932: energy bookkeeping of cold-energy settling (criteria dce2a2e3d)" + ("  [MUTATE]" if MUT else ""))
    log(f"native: h {H_NAT:.4f}, Omega_m {OM_NAT:.4f}, sigma8(native table) {SIG8:.4f}, Delta_ta(0) {DTA0:.4f}, rhobar_m {RHOM:.3f} Msun/kpc^3")
    S = systems(); RES = {"lane": "CFG932", "mutate": MUT, "criteria": "dce2a2e3d",
                          "settings": dict(kappa=0.5, footings=FOOT, f_b=FB, cold_per_b=(1 - FB) / FB, e_SN=E_SN_PER_MSUN,
                                           return_fraction=RETURN, eta_AGN=ETA_AGN, delta_c=DC, Delta_vir=DVIR, Delta_ta0=DTA0,
                                           h_native=H_NAT, Om_native=OM_NAT, sigma8_native=SIG8)}
    if MUT:
        # M1: primordial == settled -> every Delta E measure = 0 (forced regions r_obs and 0.5 r_*)
        m1 = {}; m1ok = True
        for sysd in S:
            for fk, a0 in FOOT.items():
                res, (Mp, dMp, Ms, dMs, Mph) = evaluate(sysd, a0, "EPS", 0.05, 1, identical=True)
                Mb, dMb = sysd["Mb"], sysd["dMb"]
                for R in (sysd["r_obs"], 0.5 * res["r_star_kpc"]):
                    a = 0.5 * dW_diff(Mb, dMb, Ms, dMs, Mp, dMp, R); b = dE_b(Mb, dMb, Ms, dMs, Mp, R); cg, cn = dE_c(Mb, Ms, Mp, R)
                    Wr = abs(W_self(lambda r: Mb(r) + Ms(r), lambda r: dMb(r) + dMs(r), R))
                    good = max(abs(a), abs(b), abs(cg), abs(cn)) <= 1e-9 * Wr
                    m1[f"{sysd['name']}_{fk}_R{R:.4g}"] = dict(a=a, b=b, c=cg, c_net=cn, absW=Wr, zero=bool(good)); m1ok &= good
                m1[f"{sysd['name']}_{fk}_Rx"] = res["R_x_kpc"]
        # M2: a0 -> 1e-6 a0 changes the settled cold mass inside r_obs by more than x10
        m2 = {}; m2ok = True
        for sysd in S:
            for fk, a0 in FOOT.items():
                Mph, _ = phantom(sysd, a0k(a0)); Mph6, _ = phantom(sysd, a0k(a0) * 1e-6)
                ro = sysd["r_obs"]; x = float(Mph(np.array(ro))); y = float(Mph6(np.array(ro)))
                ratio = x / max(y, 1e-300); good = ratio > 10.0
                m2[f"{sysd['name']}_{fk}"] = {'Mph_robs': x, 'Mph_robs_a0x1e-6': y, 'ratio': ratio, 'changed': bool(good)}; m2ok &= good
        log(f"MUTATE M1 (primordial == settled): every Delta E measure zero to 1e-9 |W|: {'BITES' if m1ok else 'DOES NOT BITE'}")
        for k, v in m1.items():
            if isinstance(v, dict): log(f"  {k:32s} a {v['a']:+.2e} b {v['b']:+.2e} c {v['c']:+.2e} |W| {v['absW']:.3e} zero {v['zero']}")
            else: log(f"  {k:32s} R_x (identical profiles) = {v}")
        log(f"MUTATE M2 (a0 -> 1e-6 a0): settled M_c(<r_obs) changes by > x10 for every system: {'BITES' if m2ok else 'DOES NOT BITE'}")
        for k, v in m2.items(): log(f"  {k:24s} M_ph(<r_obs) {v['Mph_robs']:.3e} -> {v['Mph_robs_a0x1e-6']:.3e}  ratio {v['ratio']:.3e}")
        RES.update(M1=m1, M2=m2, M1_bites=bool(m1ok), M2_bites=bool(m2ok))
        rc = 1 if (m1ok and m2ok) else 0
        RES["exit"] = rc
        json.dump(jsonable(RES), open(os.path.join(HERE, f"cfg932_results{TAG}.json"), "w"), indent=1)
        open(os.path.join(HERE, f"cfg932{TAG}.out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(rc)

    # ---- K1, K2
    k1ok, k1 = K1(); log(f"K1 analytic binding energies (< 1e-6): {'PASS' if k1ok else 'FAIL'}  " +
                         ", ".join(f"{k} rel {v['rel']:.2e}" for k, v in k1.items()))
    k2ok, k2 = K2(); log(f"K2 CFG541 MW-like record: M_cat/M_b {k2['Mcat_over_Mb']:.13f} (rel {k2['rel_Mcat']:.1e}), r_* {k2['r_star_kpc']:.10f} kpc "
                         f"vs {k2['record_r_star_kpc']:.10f} (rel {k2['rel_r_star']:.1e}), phantom cont/cells rel {k2['rel_phantom']:.1e}: {'PASS' if k2ok else 'FAIL'}")
    RES["K1"] = dict(ok=k1ok, **k1); RES["K2"] = dict(ok=k2ok, **k2)

    # ---- Q1 drift tests
    log("Q1 1-D drift-only test (G = 1; Plummer M_b 1, a 1; a0 0.05; NFW cold 30, r_s 3, R_C 30; alpha 1):")
    q1 = {}
    for ts in (True, False):
        d = drift_test(ts); q1["two_sided" if ts else "one_sided"] = d
        log(f"  {'two-sided (FIX-1)' if ts else 'one-sided (E5)  '}: t {d['t_end']:.1f}, steps {d['steps']}, dW/|W0| {d['dW_over_absW0']:+.4e}, "
            f"int P dt {d['int_P_dt']:+.4e} vs dW {d['dW']:+.4e} (identity rel {d['identity_rel']:.2e}); outward {d['int_P_outward']:+.3e}, "
            f"inward {d['int_P_inward']:+.3e}; central zone r < {d['central_zone_r']:.3f}: mass {d['central_mass_t0']:.4f} -> {d['central_mass_end']:.4f}; mass err {d['mass_err']:.1e}")
    t2 = q1["two_sided"]
    ident_ok = t2["identity_rel"] <= 0.02 and q1["one_sided"]["identity_rel"] <= 0.02
    if ident_ok and abs(t2["dW_over_absW0"]) >= 1e-3: q1class = "NON-CONSERVING"
    elif not ident_ok: q1class = "UNDETERMINED"
    else: q1class = "CONSERVING"
    log(f"Q1 CLASS: {q1class} (source: P_drift = int rho_c v_s.grad Phi dV [+ P_bath = int (alpha/tau)(3 rho_c sigma_J^2 - tr Pi) dV]; "
        f"booked to CFG542's dark-energy partner, Q = -rho_c v_s.grad Phi)")
    RES["Q1"] = dict(tests=q1, identity_ok=bool(ident_ok), cls=q1class)

    # ---- Q2/Q3 grid
    roles = {s["name"]: s["role"] for s in S}
    grid = {}; central_rows = {}
    for fk, a0 in FOOT.items():
        for ck, rule, F in CUSPS:
            for L in LS:
                key = f"{fk}|{ck}|L{L}"; grid[key] = {}
                for sysd in S:
                    if (not sysd["gaspoor"]) and L != 1:
                        grid[key][sysd["name"]] = grid[f"{fk}|{ck}|L1"][sysd["name"]]; continue
                    res, prof = evaluate(sysd, a0, rule, F, L)
                    grid[key][sysd["name"]] = res
                    if ck == "EPS0.05" and L == 1: central_rows[(fk, sysd["name"])] = (res, prof)
    # ---- K3 (central corner, canonical)
    k3ok, k3 = K3(S, {nm: central_rows[("can", nm)] for nm in ("MW-like", "Draco-like")})
    log(f"K3 virial cross-check (whole catchment, central corner, can): {'PASS' if k3ok else 'FAIL'}  " +
        ", ".join(f"{k}: direct {v['dE_direct_erg']:.4e} vs 1/2 dW {v['dE_half_dW_erg']:.4e}" for k, v in k3.items()))
    RES["K3"] = dict(ok=k3ok, **k3)

    # ---- windows
    def eps_req_of(row, sysname, MBH, meas):
        dE = row[f"dE_{meas}_erg"]
        Eagn = ETA_AGN * (MBH if sysname == "cluster-core" else (sysd_by[sysname]["MBH"] or 0.0)) * 1.989e33 * (C_KMS * 1e5) ** 2
        Eav = row["E_SN_erg"] + Eagn
        return (dE / Eav if dE > 0 else 0.0), Eav
    sysd_by = {s["name"]: s for s in S}
    SA = ["UFD-c", "UFD-e", "Draco-like", "cluster-core"]; SB = SA + ["Fornax-like"]
    corners = []
    for key, rows in grid.items():
        fk, ck, Lk = key.split("|")
        for MBH in MBHS:
            rec = dict(footing=fk, cusp=ck, L=int(Lk[1:]), MBH=MBH, eps_req={}, E_avail={}, windows={})
            for meas in ("b", "a", "c"):
                er = {}
                for nm, row in rows.items():
                    e, Eav = eps_req_of(row, nm, MBH, meas); er[nm] = e; rec["E_avail"][nm] = Eav
                rec["eps_req"][meas] = er
                rec["windows"][meas] = {"S_A": window(er, roles, SA), "S_B": window(er, roles, SB)}
            corners.append(rec)
    def cls(meas, sset):
        ne = [c["windows"][meas][sset]["nonempty"] for c in corners]
        return ("WINDOW EXISTS" if all(ne) else ("NO WINDOW" if not any(ne) else "BRACKET-DEPENDENT")), int(sum(ne))
    classes = {f"{m}_{s}": cls(m, s) for m in ("b", "a", "c") for s in ("S_A", "S_B")}
    prim, nprim = classes["b_S_A"]
    final = prim
    if prim in ("WINDOW EXISTS", "NO WINDOW") and (classes["a_S_A"][0] != prim or classes["c_S_A"][0] != prim):
        final = "BRACKET-DEPENDENT"
    # per-footing classes (footings never pooled)
    perfoot = {}
    for fk in FOOT:
        ne = [c["windows"]["b"]["S_A"]["nonempty"] for c in corners if c["footing"] == fk]
        perfoot[fk] = ("WINDOW EXISTS" if all(ne) else ("NO WINDOW" if not any(ne) else "BRACKET-DEPENDENT"), int(sum(ne)), len(ne))

    # ---- print central corner
    for fk in FOOT:
        log(f"\nCENTRAL CORNER ({fk}; EPS F 0.05, L 1, cluster M_BH 5e9): per system")
        log(f"  {'system':13s} {'M_ta':>9s} {'f_ret':>5s} {'c_ta':>6s} {'r_s kpc':>8s} {'r_* kpc':>9s} {'R_x kpc':>9s} {'M_sur':>9s} "
            f"{'dE_b erg':>10s} {'dE_a erg':>10s} {'dE_c erg':>10s} {'dEtot_b':>10s} {'E_avail':>9s} {'eps_req b':>9s} {'X_ret':>6s} {'E_M3/Eav':>8s}")
        cc = [c for c in corners if c["footing"] == fk and c["cusp"] == "EPS0.05" and c["L"] == 1 and c["MBH"] == 5e9][0]
        for nm in [s["name"] for s in S]:
            r = grid[f"{fk}|EPS0.05|L1"][nm]; Eav = cc["E_avail"][nm]
            rx = f"{r['R_x_kpc']:.4g}" if r["R_x_kpc"] is not None else "none"
            log(f"  {nm:13s} {r['M_ta']:9.3e} {r['f_ret']:5.2f} {r['c_ta']:6.2f} {r['r_s_kpc']:8.3g} {r['r_star_kpc']:9.4g} {rx:>9s} "
                f"{r['M_surplus_max']:9.3e} {r['dE_b_erg']:10.3e} {r['dE_a_erg']:10.3e} {r['dE_c_erg']:10.3e} {r['dE_b_tot_erg']:10.3e} "
                f"{Eav:9.3e} {cc['eps_req']['b'][nm]:9.2e} {r['X_ret_dex']:+6.3f} {r['E_M3_erg'] / Eav:8.2e}")
        w = cc["windows"]["b"]["S_A"]
        log(f"  window (b, S_A): eps in [{w['eps_lo']:.3e}, {w['eps_hi']:.3e}) -> {'NON-EMPTY' if w['nonempty'] else 'EMPTY'}")
    # ---- bracket summary of eps_req (measure b)
    log("\neps_req (measure b) ranges over all corners, per footing [min, max]; 'n0' = corners with eps_req = 0 (no surplus / net release):")
    for fk in FOOT:
        for nm in [s["name"] for s in S]:
            v = [c["eps_req"]["b"][nm] for c in corners if c["footing"] == fk]
            log(f"  {fk} {nm:13s} [{min(v):.3e}, {max(v):.3e}]  n0 {sum(1 for x in v if x == 0)}/{len(v)}")
    log("\nretained-excess diagnostic X_ret (dex, total mass at r_obs, one-sided minimiser) by cusp x L (canonical):")
    for nm in ("UFD-c", "UFD-e", "Draco-like", "Fornax-like", "SPARC-dwarf", "MW-like", "cluster-core"):
        cells = []
        for ck, _, _ in CUSPS:
            for L in LS:
                cells.append(f"{ck}/L{L} {grid[f'can|{ck}|L{L}'][nm]['X_ret_dex']:+.3f}")
        log(f"  {nm:13s} " + "  ".join(cells))
    log("\nQ3 CLASSES (windows over 72 corners):")
    for k, (cl_, n_) in classes.items(): log(f"  measure {k}: {cl_} ({n_}/72 non-empty)")
    for fk, (cl_, n_, tot) in perfoot.items(): log(f"  footing {fk} (b, S_A): {cl_} ({n_}/{tot})")
    log(f"Q3 CLASS (primary b, S_A, robustness downgrade applied): {final}")
    # flags
    flags = {k: [nm for nm, r in rows.items() if r["rstar_beyond_rta"] or (not r["phantom_monotone"]) or r["c_noroot"]] for k, rows in grid.items()}
    nflag = sum(len(v) for v in flags.values())
    log(f"flags (r_* beyond r_ta, non-monotone phantom, c without root): {nflag} system-corners" + (f" {flags}" if nflag else ""))
    RES.update(grid=grid, corners=corners, Q3=dict(classes={k: dict(cls=v[0], n_nonempty=v[1]) for k, v in classes.items()},
                                                 per_footing={k: dict(cls=v[0], n_nonempty=v[1], n=v[2]) for k, v in perfoot.items()},
                                                 primary=prim, final=final), flags=flags)
    allk = k1ok and k2ok and k3ok
    log(f"\nCONTROLS K1 {'PASS' if k1ok else 'FAIL'}, K2 {'PASS' if k2ok else 'FAIL'}, K3 {'PASS' if k3ok else 'FAIL'}; Q1 identity {'PASS' if ident_ok else 'FAIL'}")
    log("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle; not theory closed.")
    RES["exit"] = 0 if (allk and ident_ok) else 1
    json.dump(jsonable(RES), open(os.path.join(HERE, f"cfg932_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg932{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(RES["exit"])

if __name__ == "__main__":
    main()
