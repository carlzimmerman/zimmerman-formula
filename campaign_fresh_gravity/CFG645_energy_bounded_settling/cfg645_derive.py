#!/usr/bin/env python3
"""CFG645 derivation (FROZEN_CRITERIA.md, 21b7b0857): energy-bounded settling H-EB.

S1 point-mass R(y) control vs CFG635; S2 astra receiver_capacity exact channel for BOTH signs (sympy + ODE); D1 settled amount vs mass
(CFG556 halo machinery executed from its committed source, inherited context ingredients as in CFG556), export E_V / E_Phi, global
capacity C_rest = rho_DE c^2 V_ta, Xi = C/E_Phi, EB-L removal, eta_crit; D2-D4 labels; T5 KiDS magnitude-and-sign bound; T6 growth
proxy (CONTEXT ONLY) for EB-R / EB-L / EB-eta boundary; local-reaction flag.  MUTATE: CFG645_MUTATE=1 -> *_MUTATE outputs
(M-inf: capacity -> inf reproduces CFG556 primary; M0: capacity -> 0; Mc: cap x 1e-3).
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG645_energy_bounded_settling/cfg645_derive.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE); sys.path.insert(0, LANES)
try:
    os.nice(10)
except OSError:
    pass
import cfg645_lib as L                                                       # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                                 # noqa: E402
MUTATE = os.environ.get("CFG645_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK = [], {}
RES = {"lane": "CFG645", "script": "cfg645_derive", "criteria": "21b7b0857", "mutate": MUTATE}
FOOTS = ("canonical", "alt")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run from")[0].strip())
nu_exp = C4.nu_rar
nu_mono = C4.nu_mono

# ===================================================================================== S1
P("\n== S1 point-mass R(y) = rho_ph V_c^2/(rho_DE c^2) (finite differences of the profile) vs CFG635")
yy = np.geomspace(1e-6, 1e4, 4001)
Rexp, Rmono = L.point_mass_R(yy, nu_exp), L.point_mass_R(yy, nu_mono)
deep = L.KAPPA ** 2 * yy / (4 * math.pi)
d4 = float(L.point_mass_R(np.array([1e-4]), nu_exp)[0] / (L.KAPPA ** 2 * 1e-4 / (4 * math.pi)) - 1)
d6 = float(L.point_mass_R(np.array([1e-6]), nu_exp)[0] / (L.KAPPA ** 2 * 1e-6 / (4 * math.pi)) - 1)
ipk = int(np.argmax(np.where(yy > 1, Rexp, 0)))
y1 = float(brentq(lambda v: L.point_mass_R(np.array([v]), nu_mono)[0] - 1.0, 5, 1e4))
check("S1a deep limit kappa^2 y/(4 pi) to 1e-3 at y = 1e-4 (frozen tolerance)", abs(d4) <= 1e-3, f"rel dev {d4:+.2e} (analytic next order +sqrt(y)/2 = +5.0e-03)")
check("S1a' (post-freeze, disclosed) same at y = 1e-6, tolerance 1e-3", abs(d6) <= 1e-3, f"rel dev {d6:+.2e}", lb=False)
check("S1b exponential-kernel peak 0.43 +- 0.01 near y ~ 24", abs(Rexp[ipk] - 0.43) <= 0.01 and 18 <= yy[ipk] <= 30, f"peak {Rexp[ipk]:.4f} at y {yy[ipk]:.1f}")
check("S1c repaired nu_mono R = 1 at y = 36 +- 2", abs(y1 - 36) <= 2, f"y(R=1) = {y1:.2f}")
g_star = math.sqrt(4 * math.pi) / L.KAPPA
P(f"  deep-regime boundary R = 1 at g* = sqrt(4 pi)/kappa a0 = {g_star:.3f} a0 (outside the deep regime: the kernels set where R = 1)")
P(f"  R at g = 0.05 a0 (KiDS RAR upper edge, deep): {L.KAPPA ** 2 * 0.05 ** 2 / (4 * math.pi):.2e};  at y = 1: exp {float(np.interp(1, yy, Rexp)):.3f}")
RES["S1"] = dict(dev_y1e4=d4, dev_y1e6=d6, exp_peak=float(Rexp[ipk]), exp_peak_y=float(yy[ipk]), mono_y_R1=y1, g_star_over_a0=g_star)

# ===================================================================================== S2
P("\n== S2 astra receiver_capacity exact channel, both signs of D (export: D < 0)")
t, m, D, A, Lr, x = sp.symbols("t m D A L x", real=True)
X = sp.Function("X")(t)
# implicit solution (A - X)/(L - X) = (A/L) exp(2 m D (A - L) t); differentiate implicitly
F = sp.log((A - X) / (Lr - X)) - sp.log(A / Lr) - 2 * m * D * (A - Lr) * t
dX = sp.solve(sp.diff(F, t), sp.diff(X, t))[0]
ode_res = sp.simplify(dX - 2 * m * D * (Lr - X) * (A - X))
pi0, q = sp.symbols("pi0 q", real=True)
# energy: E = D q + pi^2/2 with pi^2 = pi0^2 - 2 D x; qdot = m pi^2 (A - x), pidot = -m pi D (A - x)
pi_ = sp.sqrt(pi0 ** 2 - 2 * D * x)
Edot = sp.simplify(D * m * pi_ ** 2 * (A - x) + pi_ * (-m * pi_ * D * (A - x)))
check("S2a sympy: implicit solution satisfies xdot = 2 m D (L - x)(A - x) for either sign of D", ode_res == 0, f"residual {ode_res}")
check("S2b sympy: E = D q + pi^2/2 conserved by the bracket flow", Edot == 0, f"dE/dt = {Edot}")


def chan(pi02, Dv=-1.0, Av=1.0, mv=1.0, tmax=60.0):
    def f(_, s):
        xq, p = s
        return [mv * p * p * (Av - xq), -mv * p * Dv * (Av - xq)]
    sol = solve_ivp(f, (0, tmax), [0.0, math.sqrt(pi02)], rtol=1e-10, atol=1e-13, dense_output=True)
    tt = np.linspace(0, tmax, 6001); xs = sol.sol(tt)[0]
    th = float(tt[np.argmax(xs >= 0.5 * Av)]) if xs[-1] >= 0.5 * Av else float("nan")
    return float(xs[-1]), th


S2 = {}
for p2 in (1e-6, 1e-2, 1.0, 0.0):
    xe, th = chan(p2); S2[str(p2)] = dict(x_end_over_A=xe, t_half=th)
    P(f"  export D = -1, A = 1, m = 1: pi0^2 = {p2:g} -> x(60)/A = {xe:.6f}, t_half = {th:.3f}")
imp = {str(p2): chan(p2, Dv=+1.0)[0] for p2 in (0.5, 2.0, 4.0)}
P("  import D = +1 (astra's case): pi0^2 = 0.5 / 2 / 4 -> x(60)/A = " + " / ".join(f"{imp[k]:.4f}" for k in imp) + "  (endpoint min(A, L), L = pi0^2/2D)")
binary = all(abs(S2[k]["x_end_over_A"] - 1) < 1e-4 for k in ("1e-06", "0.01", "1.0")) and abs(S2["0.0"]["x_end_over_A"]) < 1e-12
check("S2c export channel: x -> A for every pi0 != 0, x = 0 for pi0 = 0 (BINARY endpoint)", binary,
      ", ".join(f"{k}: {S2[k]['x_end_over_A']:.6f}" for k in S2))
lag = S2["1e-06"]["t_half"] - S2["1.0"]["t_half"]
P(f"  pi0 sets only a lag: t_half(1e-6) - t_half(1) = {lag:.2f} (logarithmic in pi0); the amount does not depend on pi0 or m")
RES["S2"] = dict(export=S2, import_endpoints=imp, binary=binary, lag=lag)
RES["D3"] = dict(label="BINARY" if binary else "NOT BINARY",
                 note="exact Lambda (w = -1): pi0 = 0 -> nothing settles; any pi0 != 0 -> full target; pi0 is a free initial datum that only sets a lag")
P(f"  D3 EB-K label: {RES['D3']['label']}")

# ===================================================================================== CFG556 machinery (executed from committed source)
P("\n== D1 settled amount vs mass (CFG556 machinery executed read-only from its source up to its run block)")
S556 = open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")).read()
pre = S556[:S556.index("# ------------------------------------------------------------------ run")]
NS = dict(__file__=os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py"), __name__="cfg556_ro")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre, "cfg556_ro", "exec"), NS)
G = NS["G"]; h = NS["h"]; A0MPC = NS["A0MPC"]; FB = NS["FB"]


def settled_parts(hb, foot):
    """B's cen-edge profile pieces (same arithmetic as CFG556 frame_profile edge='cen', mode='normal')."""
    r, MF, inf = NS["frame_profile"](hb, foot, edge="cen")
    re = inf["re"]; Mb = inf["Mb"]; a0 = A0MPC[foot]
    mb = NS["baryon_cum"](hb, Mb, r, re)
    y = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
    Min = np.where(r > 0, mb * NS["nu_k"](y), 0.0)
    S = np.where(r <= re, Min - mb, np.interp(re, r, Min - mb))
    return r, MF, inf, mb, S


def phys_profile(hb, foot):
    """physical units: r [Mpc], masses [Msun], G [Mpc (km/s)^2/Msun], a0 [(km/s)^2/Mpc]."""
    r, MF, inf, mb, S = settled_parts(hb, foot)
    rp = r / h; MFp = MF / h; mbp = mb / h; Sp = S / h
    return r, rp, MFp, mbp, Sp, inf


def e_full(rp, MFp, rta):
    """e_V, e_Phi on the full grid (r = 0 node takes the first interior value)."""
    eV, ePhi = L.e_profiles(rp[1:], MFp[1:], G, rta)
    return np.concatenate([[eV[0]], eV]), np.concatenate([[ePhi[0]], ePhi])


def eb_case(hb, foot, mode, emode="Phi", fac=1.0, C=None):
    """returns (MF_new [h units], info): settled part capped, removed mass returned to the drained shell (mass inside r_ta conserved)."""
    r, rp, MFp, mbp, Sp, inf = phys_profile(hb, foot)
    a0 = A0MPC[foot]; rta_p = hb["rta"] / h
    eV, ePhi = e_full(rp, MFp, rta_p)
    e = eV if emode == "V" else ePhi
    if mode == "R" and C is None:
        C = L.rho_de_c2(a0, G) * 4 / 3 * math.pi * rta_p ** 3
    Sc, rem, ci = L.cap_cum(rp, Sp, e, a0, G, fac=fac, mode=mode, C=C)
    remt = float(rem[-1])
    ML = NS["M_L"](hb, r) / h
    rout = inf.get("rout", inf["re"]) / h
    iout = np.searchsorted(rp, rout)
    Mta = hb["Mta"] / h
    if rout < rta_p * (1 - 1e-9) and ML[iout] < Mta * (1 - 1e-12):
        sh = np.where(rp > rout, (ML - ML[iout]) / (Mta - ML[iout]), 0.0)
    else:
        sh = ML / Mta
    MFn = MFp - rem + remt * np.clip(sh, 0, 1)
    return MFn * h, dict(removed_tot=remt, settled=float(Sp[-1]), info=ci, r_ta=rta_p, eV=eV, ePhi=ePhi, rp=rp, Sp=Sp, MFp=MFp, mbp=mbp)


MSEL = [1e11, 3e11, 1e12, 3e12, 1e13, 1e14, 1e15]
D1 = {}
for foot in FOOTS:
    a0 = A0MPC[foot]; rde = L.rho_de_c2(a0, G)
    D1[foot] = {}
    P(f"\n  [{foot}] rho_DE c^2 = a0^2/(kappa^2 G) = {rde:.4e} Msun (km/s)^2 / Mpc^3")
    P("   M200m[Msun/h] logMta  fret  M_set/Mta  Vf[km/s]  E_V/(MsVf2) E_Phi/(MsVf2)   C_rest/E_Phi   eta_crit  | EB-L removed frac (V / Phi)  band0.2-0.5rta (V / Phi)  bind r/rta (Phi)  g/a0 at bind")
    for M in MSEL:
        hb = NS["halo_basics"](M)
        r, rp, MFp, mbp, Sp, inf = phys_profile(hb, foot)
        rta = hb["rta"] / h; Mb = inf["Mb"] / h
        Vf2 = math.sqrt(G * Mb * a0)
        eV, ePhi = e_full(rp, MFp, rta)
        dS = np.diff(Sp)
        EV = float(np.sum(dS * 0.5 * (eV[1:] + eV[:-1])))
        EP = float(np.sum(dS * 0.5 * (ePhi[1:] + ePhi[:-1])))
        Crest = rde * 4 / 3 * math.pi * rta ** 3
        Ms = float(Sp[-1])
        out = dict(M200m=M, logMta=math.log10(hb["Mta"] / h), fret=inf["fret"], Mset_over_Mta=Ms / (hb["Mta"] / h), Vf=math.sqrt(Vf2),
                   EV_over_MsVf2=EV / (Ms * Vf2), EPhi_over_MsVf2=EP / (Ms * Vf2), Xi=Crest / EP, eta_crit=EP / Crest, re_over_rta=inf["re"] / hb["rta"])
        for em in ("V", "Phi"):
            MFn, ci = eb_case(hb, foot, "L", emode=em)
            rpp = ci["rp"]; band = (rpp >= 0.2 * rta) & (rpp <= 0.5 * rta)
            # removed inside the band relative to settled mass in the band
            _, rem, inf2 = L.cap_cum(rpp, ci["Sp"], ci["eV"] if em == "V" else ci["ePhi"], a0, G, mode="L")
            ib = np.where(band)[0]
            if len(ib) > 1:
                rb = (rem[ib[-1]] - rem[ib[0]]) / max(ci["Sp"][ib[-1]] - ci["Sp"][ib[0]], 1e-300)
            else:
                rb = 0.0
            out[f"L{em}_removed_frac"] = ci["removed_tot"] / Ms
            out[f"L{em}_band_removed_frac"] = float(rb)
            out[f"L{em}_bind_r_over_rta"] = [None if inf2["bind_lo"] is None else inf2["bind_lo"] / rta, None if inf2["bind_hi"] is None else inf2["bind_hi"] / rta]
            if inf2["bind_hi"] is not None:
                gg = G * np.interp(inf2["bind_hi"], rpp, ci["MFp"]) / inf2["bind_hi"] ** 2 / a0
                gl = G * np.interp(inf2["bind_lo"], rpp, ci["MFp"]) / inf2["bind_lo"] ** 2 / a0
                out[f"L{em}_bind_g_over_a0"] = [float(gg), float(gl)]
                # local-reaction flag (astra local_sink_reaction): |d(rho_set e)/dr| / (rho_tot g) at the outer binding radius
                e_ = ci["eV"] if em == "V" else ci["ePhi"]
                with np.errstate(divide="ignore", invalid="ignore"):
                    rho_s = np.gradient(ci["Sp"], rpp) / (4 * math.pi * rpp ** 2)
                    rho_t = np.gradient(ci["MFp"], rpp) / (4 * math.pi * rpp ** 2)
                    u = rho_s * e_; du = np.gradient(u, rpp)
                j = int(np.searchsorted(rpp, inf2["bind_hi"]))
                out[f"L{em}_reaction_ratio"] = float(abs(du[j]) / (rho_t[j] * G * ci["MFp"][j] / rpp[j] ** 2))
            else:
                out[f"L{em}_bind_g_over_a0"] = None; out[f"L{em}_reaction_ratio"] = None
        D1[foot][f"{M:.0e}"] = out
        bp = out["LPhi_bind_r_over_rta"]; bg = out["LPhi_bind_g_over_a0"]
        P(f"   {M:8.0e}   {out['logMta']:6.2f}  {out['fret']:.2f}   {out['Mset_over_Mta']:.3f}    {out['Vf']:7.1f}   {out['EV_over_MsVf2']:8.3f}   {out['EPhi_over_MsVf2']:8.3f}"
          f"     {out['Xi']:10.3e}   {out['eta_crit']:.2e} | {out['LV_removed_frac']:.2e} / {out['LPhi_removed_frac']:.2e}   "
          f"{out['LV_band_removed_frac']:.1e} / {out['LPhi_band_removed_frac']:.1e}   "
          + (f"{bp[0]:.1e}-{bp[1]:.1e}" if bp[0] is not None else "none") + "   " + (f"{bg[0]:.1f}-{bg[1]:.1f}" if bg else "-"))
RES["D1"] = D1

# D2 / D4
Xi_min = min(D1[f][k]["Xi"] for f in FOOTS for k in D1[f])
lab2 = "INERT (capacity never binds; EB-R = candidate B)" if Xi_min >= 10 else ("BINDS (scored as a new profile)" if Xi_min < 1 else "MARGINAL")
etas = {f: [D1[f][k]["eta_crit"] for k in D1[f]] for f in FOOTS}
spread = {f: max(etas[f]) / min(etas[f]) for f in FOOTS}
lab4 = "KNOB (mass-dependent effect)" if all(s > 3 for s in spread.values()) else "KNOB"
P(f"\n  D2 EB-R: min Xi = C_rest/E_Phi over all masses, both footings = {Xi_min:.3e} -> {lab2}")
P(f"  D4 EB-eta: eta_crit spread (max/min over the D1 masses) = {spread['canonical']:.1f} / {spread['alt']:.1f} -> {lab4}")
RES["D2"] = dict(Xi_min=Xi_min, label=lab2); RES["D4"] = dict(eta_crit=etas, spread=spread, label=lab4)
bandmax = max(D1[f][k][f"L{em}_band_removed_frac"] for f in FOOTS for k in D1[f] for em in ("V", "Phi"))
P(f"  EB-L: largest removed fraction of settled mass inside 0.2-0.5 r_ta, any mass, either e bracket, both footings: {bandmax:.2e}")
RES["EBL_band_removed_max"] = bandmax

# ===================================================================================== T5 KiDS bound
P("\n== T5 KiDS isolated lenses: magnitude-and-sign bound (innermost RAR bin g_obs = 5e-12 m s^-2)")
LZ = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
Mg_pct = np.percentile(LZ["Mgal"], [5, 50, 95])
GS, MS, KPC = C4.G_SI, C4.MSUN, C4.KPC
RHO_M_SI = L.OM * 3 * (67.36e3 / (1e3 * KPC)) ** 2 / (8 * math.pi * GS)
T5 = {}
for foot in FOOTS:
    a0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}[foot]
    T5[foot] = {}
    for pc, Mg in zip((5, 50, 95), Mg_pct):
        M = Mg * MS
        for kn, nu in (("nu_mono", nu_mono), ("exp", nu_exp)):
            Rmin = brentq(lambda R: float(nu(GS * M / R ** 2 / a0)) * GS * M / R ** 2 - 5e-12, 1e-3 * KPC, 1e5 * KPC)
            Mlaw = 5e-12 * Rmin ** 2 / GS
            Mta = M / (0.10 * FB); rta = L.r_ta_of(Mta, RHO_M_SI)
            remV, _ = L.point_mass_removed(M, a0, GS, nu, Rmin, "V")
            remP, _ = L.point_mass_removed(M, a0, GS, nu, Rmin, "Phi", r_ta=rta, Mtot_outer=Mta)
            T5[foot][f"p{pc}|{kn}"] = dict(logMgal=math.log10(Mg), Rmin_kpc=Rmin / KPC, delta_V=remV / Mlaw, delta_Phi=remP / Mlaw)
            P(f"  [{foot}] log M_gal {math.log10(Mg):.2f} ({kn:7s}): R_min {Rmin / KPC:6.1f} kpc; removed / M_law(<R_min): e_V {remV / Mlaw:.2e}, e_Phi {remP / Mlaw:.2e}")
dmax = {f: max(max(v["delta_V"], v["delta_Phi"]) for v in T5[f].values()) for f in FOOTS}
lab5 = {f: ("UNCHANGED (FAIL, = CFG529 record)" if dmax[f] <= 1e-3 else "WORSE (removal deepens the recorded inner-bin deficit)") for f in FOOTS}
P(f"  T5 EB-L label: canonical {lab5['canonical']} (max delta {dmax['canonical']:.1e}); alt {lab5['alt']} (max delta {dmax['alt']:.1e}). "
  "EB-R inert -> record (census edge FAILS f30, both footings).")
RES["T5"] = dict(rows=T5, delta_max=dmax, label=lab5, EBR_label="UNCHANGED (FAIL, = CFG529 record)")

# ===================================================================================== T6 growth proxy (CONTEXT ONLY)
P("\n== T6 growth proxy, CFG556 halo model (CONTEXT ONLY): R = 1 + (P_F,ta - P_L,ta)/P_L,std")
HB, KK, W_M, RHO_M = NS["HB"], NS["KK"], NS["W_M"], NS["RHO_M"]
Ustd = NS["U_std"](); Pstd = NS["spectra_std"](Ustd)[0]
Ulta, _ = NS["U_set"](lambda hb: NS["frame_profile"](hb, "canonical", mode="lta")); Plta = NS["spectra_ta"](Ulta)[0]
J556 = json.load(open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))
W8 = NS["_W8"]


def t6(fn):
    U = np.empty((len(HB), len(KK)))
    for i, hb in enumerate(HB):
        r, Mc = fn(hb); U[i] = NS["U_of"](r, Mc, KK)
    PF = NS["spectra_ta"](U)[0]; R = 1 + (PF - Plta) / Pstd
    w8 = W8(KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
    s8 = math.sqrt(NS["s8_of"](Pstd) ** 2 + np.trapz((PF - Plta) * w8, KK)) / NS["s8_of"](Pstd)
    return dict(R03=float(np.interp(0.3, KK, R)), R1=float(np.interp(1.0, KK, R)), s8_ratio=s8)


def mf_case(mode, emode="Phi", fac=1.0, Cfun=None):
    def fn(hb, foot):
        if mode == "inf":
            r, MF, _ = NS["frame_profile"](hb, foot, edge="cen"); return r, MF
        C = Cfun(hb, foot) if Cfun else None
        r = NS["frame_profile"](hb, foot, edge="cen")[0]
        MFn, _ = eb_case(hb, foot, mode, emode=emode, fac=fac, C=C)
        return r, MFn
    return fn


T6 = {}
cases = [("B (capacity inf)", "inf", "Phi", 1.0), ("EB-R", "R", "Phi", 1.0), ("EB-L e_V", "L", "V", 1.0), ("EB-L e_Phi", "L", "Phi", 1.0)]
if MUTATE:
    cases = [("M-inf (capacity inf)", "inf", "Phi", 1.0), ("M0 (capacity 0)", "zero", "Phi", 1.0), ("Mc EB-L e_Phi cap x 1e-3", "L", "Phi", 1e-3)]
for foot in FOOTS:
    T6[foot] = {}
    for nm, mode, em, fac in cases:
        fn = mf_case(mode, em, fac)
        o = t6(lambda hb, fn=fn: fn(hb, foot)); T6[foot][nm] = o
        P(f"  [{foot}] {nm:26s} R(k=0.3) {o['R03']:.3f}  R(k=1) {o['R1']:.3f}  sigma8 ratio {o['s8_ratio']:.4f}")
    ref = J556["cases"][f"{foot}|census|cen"]
    k0 = "B (capacity inf)" if not MUTATE else "M-inf (capacity inf)"
    dd = max(abs(T6[foot][k0]["R1"] - ref["R_at"]["1.0"]), abs(T6[foot][k0]["R03"] - ref["R_at"]["0.3"]))
    check(f"S3/M-inf [{foot}] capacity -> inf reproduces CFG556 primary R(k=0.3), R(k=1) (1e-9)", dd <= 1e-9,
          f"{T6[foot][k0]['R03']:.9f}/{ref['R_at']['0.3']:.9f}, {T6[foot][k0]['R1']:.9f}/{ref['R_at']['1.0']:.9f}")


def t6_label(o, base):
    exc0 = base["R1"] - 1; exc = o["R1"] - 1
    if exc <= 0.10 and o["R1"] >= 0.90:
        return "REMOVES"
    if exc0 > 0 and (exc0 - exc) / exc0 >= 0.25:
        return "REDUCES"
    return "UNCHANGED"


if not MUTATE:
    lab6 = {}
    for nm in ("EB-R", "EB-L e_V", "EB-L e_Phi"):
        labs = {f: t6_label(T6[f][nm], T6[f]["B (capacity inf)"]) for f in FOOTS}
        cut = {f: (T6[f]["B (capacity inf)"]["R1"] - T6[f][nm]["R1"]) / (T6[f]["B (capacity inf)"]["R1"] - 1) for f in FOOTS}
        lab6[nm] = dict(labels=labs, excess_cut=cut)
        P(f"  T6 {nm}: {labs['canonical']} / {labs['alt']} (k = 1 excess cut {cut['canonical']:.2e} / {cut['alt']:.2e})")
    RES["T6_labels"] = lab6

    # ------------------------------------------------------------ reported only: EB-eta boundary (one evaluation, no scan)
    P("\n== reported only: EB-eta boundary eta_gal = max eta_crit over M200m <= 3e12 (smallest eta keeping galaxy halos fully settled)")
    ETA = {}
    for foot in FOOTS:
        eg = max(D1[foot][f"{M:.0e}"]["eta_crit"] for M in MSEL if M <= 3e12)
        a0 = A0MPC[foot]
        Cf = lambda hb, eg=eg, a0=a0: eg * L.rho_de_c2(a0, G) * 4 / 3 * math.pi * (hb["rta"] / h) ** 3
        fr = {}
        for M in MSEL:
            hb = NS["halo_basics"](M)
            _, ci = eb_case(hb, foot, "R", emode="Phi", C=Cf(hb))
            fr[f"{M:.0e}"] = 1 - ci["removed_tot"] / ci["settled"]
        o = t6(lambda hb: mf_case("R", "Phi", 1.0, Cfun=lambda hb_, f_=foot: Cf(hb_))(hb, foot))
        ETA[foot] = dict(eta_gal=eg, settled_fraction=fr, T6=o, T6_label=t6_label(o, T6[foot]["B (capacity inf)"]))
        P(f"  [{foot}] eta_gal = {eg:.3e}; settled fraction of B's amount: " + ", ".join(f"{k} {v:.3f}" for k, v in fr.items()))
        P(f"  [{foot}] T6 at eta_gal: R(k=0.3) {o['R03']:.3f}  R(k=1) {o['R1']:.3f}  sigma8 ratio {o['s8_ratio']:.4f} -> {ETA[foot]['T6_label']} (reported, KNOB)")
    RES["EB_eta_boundary"] = ETA
RES["T6"] = T6

# ===================================================================================== MUTATE teeth (derive side)
if MUTATE:
    teeth = {}
    for foot in FOOTS:
        b = T6[foot]["M-inf (capacity inf)"]; z = T6[foot]["M0 (capacity 0)"]; c = T6[foot]["Mc EB-L e_Phi cap x 1e-3"]
        teeth[foot] = dict(M0_dR1=z["R1"] - b["R1"], Mc_dR1=c["R1"] - b["R1"])
        P(f"  [{foot}] M0 changes R(k=1) by {z['R1'] - b['R1']:+.3f}; Mc by {c['R1'] - b['R1']:+.3f}")
    RES["teeth_T6"] = teeth

RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"] and c["load_bearing"])
P(f"\n{sum(1 for c in CHK.values() if c['ok'])}/{len(CHK)} checks pass ({nf} load-bearing failures); elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg645_derive_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg645_derive{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0)
