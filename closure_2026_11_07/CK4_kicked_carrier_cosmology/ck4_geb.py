#!/usr/bin/env python3
"""CK4 row GEB (FROZEN_CRITERIA.md section 1): EB1's A2744-QSO1 timing gate with the cold parent (cold dark energy) clustering.
Halo mass M_h = M_clump (1 + omega_d/omega_b), M_clump = 10 M_seed of baryons; Newtonian spherical collapse (delta_c 1.686)
on top-hat sigma(M_h, z) of the cold reference linear power (QX3 iter2 / QX7 iter_4 CLASS model, exec'd read-only as CE2);
nu_req = smallest nu in {1..5} with t(z_coll) <= t_seed; seed time as EB1 (Eddington, eps 0.1, M_seed 1e5).
Footing-independent: a0 does not enter (Newtonian cold collapse), stated once for both footings.
    python3 ck4_geb.py                 -> ck4_geb.json / ck4_geb.out
    CK4_MUTATE=1 python3 ck4_geb.py    -> ck4_geb_MUTATE.json / .out (cold parent made non-clustering: sigma x omega_b/(omega_b+omega_d); must FAIL)
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = os.environ.get("CK4_MUTATE", "0") == "1"; TAG = "ck4_geb_MUTATE" if MUT else "ck4_geb"; OUT = []
NOTE = "kappa = 1/2 FITTED; not theory closed"
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ---------------------------------------------------------------- constants (as EB1)
G0 = 6.67430e-11; C = 299792458.0; MPC = 3.0856775814913673e22; MYR = 3.15576e13; CKM = C / 1e3
T_SAL = 6.6524587e-29 * C / (4 * math.pi * G0 * 1.67262192e-27) / MYR   # Myr, EB1's formula (the "450.7 Myr")
DELTA_C = 1.686; NUS = [1, 2, 3, 4, 5]
QSO1_Z = 7.0451; LOGM_GRADED = [7.7, 6.9]; LOGM_ALL = [7.7, 7.6, 6.9]; SEEDS = [1e2, 1e4, 1e5, 1e6]; EPS = [0.1, 0.2]
PRIMARY = dict(eps=0.1, seed=1e5)

def label(nu_req, t_seed):
    if t_seed <= 0: return "NO (age)"
    if nu_req is None: return "NO"
    return "EASY" if nu_req <= 2 else ("RARE" if nu_req <= 4 else "EXTREME")

# ---------------------------------------------------------------- cold reference (QX7 iter_4 prefix, read-only, as CE2)
I4 = os.path.join(REPO, "closure_2026_11_06", "QX7_unified_cold_switch", "iter_4_late_evaporation", "qx7_iter4.py")
s4 = open(I4).read(); c4 = s4.index("RES = dict(tag=TAG")
argv0 = sys.argv; sys.argv = [I4]; N4 = {"__file__": I4, "__name__": "qx7_iter4_reused"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(s4[:c4], I4, "exec"), N4)
sys.argv = argv0
N3 = N4["N3"]; MC = N3["M"]; h = float(N4["h"])
pars = dict(MC.pars)
omb = pars["omega_b"]; omd = pars["omega_cdm"]
Om_b0 = float(N3["Om_b0"]); Om_d0 = float(N3["Om_d0"]); rho_m0 = float(N3["rho_m0"])   # Msun/Mpc^3 (QX3's GMSUN)
P(f"CK4 GEB{' MUTATE' if MUT else ''}: cold reference CLASS model (QX3 iter2 / QX7 iter_4); the cold component is cold dark energy (cold parent)")
P(f"  N3 pars: {pars}")
P(f"  h {h} (N4) / {MC.h()} (MC); omega_b {omb}; omega_d (CLASS omega_cdm slot) {omd:.8f}; N3 Om_b0 {Om_b0:.8f} Om_d0 {Om_d0:.8f}"
  f" (x h^2: {Om_b0*h*h:.6f}, {Om_d0*h*h:.6f}); rho_m0 {rho_m0:.6e} Msun/Mpc^3; MC P_k_max {pars['P_k_max_1/Mpc']} /Mpc, z_max_pk {pars['z_max_pk']}")
ratio_dm = omd / omb

# ---------------------------------------------------------------- extended-k CLASS model (identical parameters, larger P_k_max / z_max_pk)
from classy import Class
KMAX_EXT = 1500.0; ZMAX_EXT = 60.0
pe = dict(pars); pe["P_k_max_1/Mpc"] = KMAX_EXT; pe["z_max_pk"] = ZMAX_EXT
ME = Class(); ME.set(pe); ME.compute()
rep = {}
for k in (0.1, 1.0):
    for z in (0.0, 7.0451):
        a_ = MC.pk_lin(k, z); b_ = ME.pk_lin(k, z); rep[f"k{k}_z{z}"] = dict(MC=a_, ME=b_, rel=abs(b_ / a_ - 1))
rep_ok = all(v["rel"] <= 1e-4 for v in rep.values())
P(f"  MC's k range ends at {pars['P_k_max_1/Mpc']} /Mpc < needed ~300-1000 /Mpc: recomputed CLASS with identical parameters, P_k_max {KMAX_EXT}, z_max_pk {ZMAX_EXT}")
P("  reproduction of MC.pk_lin: " + "; ".join(f"{k_} rel {v['rel']:.2e}" for k_, v in rep.items()) + f" -> {'PASS' if rep_ok else 'FAIL'} (1e-4)")

KG = np.logspace(-5, math.log10(KMAX_EXT * 0.999), 3000)
_PK = {}
def pk_arr(z, model=ME):
    key = (id(model), round(z, 10))
    if key not in _PK:
        _PK[key] = np.array([model.pk_lin(float(k), float(z)) for k in KG])
    return _PK[key]

def W(x):
    x = np.asarray(x, float); out = np.empty_like(x); s = x < 1e-3
    out[s] = 1 - x[s] ** 2 / 10; xs = x[~s]; out[~s] = 3 * (np.sin(xs) - xs * np.cos(xs)) / xs ** 3; return out

def sigma_R(R, z, kcut=None, model=ME):
    """top-hat sigma, R in Mpc, k in 1/Mpc, trapezoid in ln k."""
    pk = pk_arr(z, model); kk = KG
    if kcut is not None: m = kk <= kcut; kk = kk[m]; pk = pk[m]
    integ = kk ** 3 * pk * W(kk * R) ** 2 / (2 * math.pi ** 2)
    return math.sqrt(np.trapz(integ, np.log(kk)))

def R_of_M(M): return (3 * M / (4 * math.pi * rho_m0)) ** (1 / 3)
MUTF = (omb / (omb + omd)) if MUT else 1.0
def sigma_M(M, z): return sigma_R(R_of_M(M), z) * MUTF

# ---------------------------------------------------------------- background clock
def t_MC(z):
    """t(z) in Myr = int_0^a da / (a H), H from MC.Hubble (1/Mpc); a < 1e-8 piece from radiation domination."""
    a = 1 / (1 + z)
    f = lambda lna: 1.0 / MC.Hubble(1 / math.exp(lna) - 1)
    lo = math.log(1e-8); Hlo = MC.Hubble(1e8 - 1); tlo = 0.5 / Hlo              # t = 1/(2H) in radiation era
    val = quad(f, lo, math.log(a), epsabs=0, epsrel=1e-10, limit=400)[0] + tlo
    return val * MPC / C / MYR          # MC.Hubble is H/c in 1/Mpc, so val is in Mpc; / c -> s

# independent check: analytic E(a) with CLASS's own Omegas
Om_m_C = MC.Omega0_m(); Om_r_C = MC.Omega_r() if hasattr(MC, "Omega_r") else None
Om_L_C = 1 - Om_m_C - Om_r_C
H0s = h * 100e3 / MPC
def t_an(z):
    a = 1 / (1 + z)
    return quad(lambda x: 1.0 / (x * H0s * math.sqrt(Om_r_C / x ** 4 + Om_m_C / x ** 3 + Om_L_C)), 0, a, epsabs=0, epsrel=1e-11, limit=400)[0] / MYR

t_obs = t_MC(QSO1_Z); t_obs_an = t_an(QSO1_Z)
t_ok = abs(t_obs / t_obs_an - 1) <= 1e-3
P(f"  clock: t(z) = int da/(aH) with H = MC.Hubble (CLASS background, radiation + massless nu included). t(7.0451) = {t_obs:.3f} Myr;"
  f" independent quad on analytic E(a) (Om_m {Om_m_C:.6f}, Om_r {Om_r_C:.4e}, Om_L {Om_L_C:.6f}) {t_obs_an:.3f} Myr; rel {abs(t_obs/t_obs_an-1):.1e} -> {'PASS' if t_ok else 'FAIL'} (1e-3)")
P(f"  T_sal (EB1 formula) {T_SAL:.3f} Myr; t_E(eps 0.1) {T_SAL*0.1/0.9:.3f} Myr")

# ---------------------------------------------------------------- K1 sigma8
s8_mine = sigma_R(8.0 / h, 0.0); s8_MC = MC.sigma8(); s8_ME = ME.sigma8()
K1 = dict(sigma8_mine=s8_mine, sigma8_MC=s8_MC, sigma8_ME=s8_ME, rel=abs(s8_mine / s8_MC - 1))
K1["pass_"] = bool(K1["rel"] <= 1e-3)
P(f"K1 sigma8: mine {s8_mine:.6f} vs MC.sigma8() {s8_MC:.6f} (extended model {s8_ME:.6f}); rel {K1['rel']:.2e} -> {'PASS' if K1['pass_'] else 'FAIL'} (1e-3)")

# ---------------------------------------------------------------- K2 EB1 seed-time arithmetic on EB1's own B2 background
HE = 0.6736; OMB_E = 0.02237 / HE ** 2; OMR_E = 4.18e-5 / HE ** 2; OFLD_E = 0.2504; OL_E = 1 - OMB_E - OFLD_E - OMR_E
H0E = 100e3 * HE / MPC
def t_eb1(z):
    a = 1 / (1 + z)
    return quad(lambda x: 1.0 / (x * H0E * math.sqrt(OMR_E / x ** 4 + (OMB_E + OFLD_E) / x ** 3 + OL_E)), 0, a, epsabs=0, epsrel=1e-11, limit=400)[0] / MYR
tE1 = T_SAL * 0.1 / 0.9
t_obs_eb1 = t_eb1(QSO1_Z); ts77 = t_obs_eb1 - tE1 * math.log(10 ** 7.7 / 1e5); ts69 = t_obs_eb1 - tE1 * math.log(10 ** 6.9 / 1e5)
K2 = dict(t_obs=t_obs_eb1, t_seed_77=ts77, t_seed_69=ts69, eb1=dict(t_obs=771.4, t_seed_77=460.2, t_seed_69=552.4))
K2["pass_"] = bool(abs(t_obs_eb1 - 771.4) <= 0.1 and abs(ts77 - 460.2) <= 0.1 and abs(ts69 - 552.4) <= 0.1)
P(f"K2 EB1 B2 arithmetic: t_obs {t_obs_eb1:.2f} (771.4), t_seed 7.7 {ts77:.2f} (460.2), 6.9 {ts69:.2f} (552.4) -> {'PASS' if K2['pass_'] else 'FAIL'} (0.1 Myr)")

# ---------------------------------------------------------------- sigma, z_coll, t_coll
def z_coll(M, nu):
    """collapse epoch = largest z with nu*sigma(M,z) >= delta_c (first time the peak reaches delta_c); pk_lin at z."""
    g = lambda z: nu * sigma_M(M, z) - DELTA_C
    if g(0.0) < 0: return None
    if g(ZMAX_EXT - 1e-6) >= 0: return float("inf")
    return brentq(g, 0.0, ZMAX_EXT - 1e-6, xtol=1e-6)

# sigma convergence on the primary halo
Mh_prim = 10 * PRIMARY["seed"] * (1 + ratio_dm)
conv = dict(full=sigma_M(Mh_prim, 0.0), half=sigma_R(R_of_M(Mh_prim), 0.0, kcut=KMAX_EXT / 2) * MUTF)
conv["rel"] = abs(conv["half"] / conv["full"] - 1)
P(f"  M_h(primary) = 1e6 x (1 + {ratio_dm:.5f}) = {Mh_prim:.5e} Msun, R_L {R_of_M(Mh_prim):.5f} Mpc; sigma(z=0) {conv['full']:.5f},"
  f" with k cut at {KMAX_EXT/2:g} /Mpc {conv['half']:.5f} (rel {conv['rel']:.1e}){' [MUTATE factor %.5f applied]' % MUTF if MUT else ''}")

table = {}
for Ms in SEEDS:
    Mc = 10 * Ms; Mh = Mc * (1 + ratio_dm); row = {}
    for nu in NUS:
        zc = z_coll(Mh, nu)
        tc = None if zc is None else (0.0 if zc == float("inf") else t_MC(zc))
        row[str(nu)] = dict(z_coll=zc, t_coll_Myr=tc)
    table[f"{Ms:.0e}"] = dict(M_clump=Mc, M_h=Mh, R_L_Mpc=R_of_M(Mh), sigma_z0=sigma_M(Mh, 0.0), sigma_z7=sigma_M(Mh, QSO1_Z), rows=row)
P("-- z_coll / t_coll table (cols nu 1..5)")
for Ms, v in table.items():
    P(f"   M_seed {Ms}: M_h {v['M_h']:.3e} sigma0 {v['sigma_z0']:.4f} sigma(7.05) {v['sigma_z7']:.4f}: " +
      "  ".join(("none" if r["z_coll"] is None else f"z {r['z_coll']:.2f}/{r['t_coll_Myr']:.0f} Myr") for r in v["rows"].values()))

gate = {}
for eps in EPS:
    tE = T_SAL * eps / (1 - eps)
    for lm in LOGM_ALL:
        for Ms in SEEDS:
            ts = t_obs - tE * math.log(10 ** lm / Ms); rows = table[f"{Ms:.0e}"]["rows"]
            nu_req = None; zc = None
            if ts > 0:
                for nu in NUS:
                    r = rows[str(nu)]
                    if r["t_coll_Myr"] is not None and r["t_coll_Myr"] <= ts: nu_req = nu; zc = r["z_coll"]; break
            ts_eb1 = t_obs_eb1 - tE * math.log(10 ** lm / Ms)
            gate[f"eps{eps}|logM{lm}|seed{Ms:.0e}"] = dict(t_obs_Myr=t_obs, t_seed_Myr=ts, t_obs_EB1_Myr=t_obs_eb1, t_seed_EB1bg_Myr=ts_eb1,
                                                         M_h=table[f"{Ms:.0e}"]["M_h"], nu_req=nu_req, z_coll=zc, label=label(nu_req, ts),
                                                         graded=bool(eps == PRIMARY["eps"] and Ms == PRIMARY["seed"] and lm in LOGM_GRADED))
P("-- seed time and nu_req (all cells; graded = eps 0.1, seed 1e5, logM 7.7 and 6.9)")
for k_, g in gate.items():
    P(f"   {k_}: t_seed {g['t_seed_Myr']:.1f} Myr (EB1 bg {g['t_seed_EB1bg_Myr']:.1f}), nu_req {g['nu_req']}, z_coll "
      f"{'-' if g['z_coll'] is None else round(g['z_coll'], 3)}, {g['label']}{'  <- GRADED' if g['graded'] else ''}")

# ---------------------------------------------------------------- daughters: upper bound on the converted fraction at z 7.05 (Sheth-Tormen)
def F_ST(Mmin, z):
    A, p, q = 0.3222, 0.3, 0.707
    nu0 = DELTA_C / sigma_M(Mmin, z)
    f = lambda nu: A * math.sqrt(2 * q / math.pi) * (1 + (q * nu * nu) ** (-p)) * math.exp(-q * nu * nu / 2)
    return quad(f, nu0, np.inf, limit=200)[0]
dau = {f"{Mm:.0e}": F_ST(Mm, QSO1_Z) for Mm in (1e10, 1e11, 1e12)}
dau_enter = dau["1e+11"] > 1e-3
P("  daughters: Sheth-Tormen F(>M_min, z 7.0451) (upper bound on converted, hence on escaped, fraction): " +
  ", ".join(f"M_min {k} {v:.3e}" for k, v in dau.items()) + f"; primary M_min 1e11 {'EXCEEDS' if dau_enter else 'below'} 1e-3"
  + (" -> daughters would enter (not handled here; flag)" if dau_enter else " -> daughters do not enter GEB"))

# ---------------------------------------------------------------- label
g77 = gate["eps0.1|logM7.7|seed1e+05"]; g69 = gate["eps0.1|logM6.9|seed1e+05"]
checks_ok = K1["pass_"] and K2["pass_"] and rep_ok and t_ok
gpass = all(g["label"] in ("EASY", "RARE") for g in (g77, g69))
LAB = ("PASS" if gpass else "FAIL") if checks_ok else "NO VERDICT"
P(f"GEB{' MUTATE' if MUT else ''} label (footing-independent; Newtonian cold collapse, a0 does not enter): {LAB}"
  f"  [logM 7.7: nu_req {g77['nu_req']} {g77['label']}; logM 6.9: nu_req {g69['nu_req']} {g69['label']}]")
if MUT: P(f"MUTATE bite: {'YES (FAIL as required)' if LAB == 'FAIL' else 'NO (did not bite)'}")
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 2 if sys.platform == "darwin" else 1024)
P(f"peak RSS {peak:.0f} MB. {NOTE}")

RES = dict(tag=TAG, mutate=MUT, mutate_factor=MUTF, label=LAB, footing="independent (Newtonian cold collapse; a0 does not enter)",
           pars_N3=pars, h=h, omega_b=omb, omega_d=omd, Om_b0=Om_b0, Om_d0=Om_d0, rho_m0=rho_m0,
           ext_model=dict(P_k_max=KMAX_EXT, z_max_pk=ZMAX_EXT, reproduction=rep, pass_=rep_ok),
           clock=dict(method="int da/(aH), H = MC.Hubble", t_obs=t_obs, t_obs_analytic=t_obs_an, pass_=t_ok, T_sal=T_SAL),
           K1=K1, K2=K2, sigma_conv=conv, table=table, gate=gate, daughters_F_ST_z7=dau, daughters_enter=dau_enter,
           primary=dict(logM77=g77, logM69=g69), peak_rss_MB=peak,
           disclosures=["MC P_k_max 12 /Mpc too short; CLASS recomputed with N3's parameters, P_k_max 1500, z_max_pk 60",
                        "z_coll = largest z (earliest epoch) with nu sigma(M_h, z) >= 1.686, sigma from pk_lin at z (scale-dependent growth kept)",
                        "rho_m0 = N3's (baryons + cold parent); Lagrangian radius on total matter",
                        "T_sal from EB1's constants formula",
                        "daughters bounded by Sheth-Tormen F(>M_min) at z 7.0451, not by the CK4 production solver"],
           note=NOTE)
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
