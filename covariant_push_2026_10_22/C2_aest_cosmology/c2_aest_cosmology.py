#!/usr/bin/env python3
"""C2_aest_cosmology: AeST-type background, dust abundance, native-H0 map, growth index, tool/data inventory.

Criteria: FROZEN_CRITERIA.md (committed alone first). Deterministic, no network, one thread.
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 c2_aest_cosmology.py      (C2_MUTATE=1 for the mutation)
External inputs are flagged in FROZEN_CRITERIA.md (E-AeST, E-A78, E-886, E-ladder). kappa = 1/2 FITTED.
"""
import os, sys, json, glob, hashlib, importlib.util, math
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
MUT = os.environ.get("C2_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"c2_aest_cosmology{TAG}.out"), "w")
RES, CHK = {"mutate": MUT}, []


def P(s=""):
    print(s); OUT.write(s + "\n")


def check(k, ok, val, thr):
    CHK.append((k, bool(ok)))
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}")


def rel(p):
    return os.path.relpath(p, REPO)


# ------------------------------------------------------------------ K1: Y on FRW, orders eps^0 and eps^1
P("== K1: the a0-carrying invariant Y = q^{mu nu} d_mu phi d_nu phi on FRW + general linear perturbation")
eps, N, a, phid = sp.symbols("epsilon N a phidot", positive=True)
gbar = sp.diag(-N**2, a**2, a**2, a**2)
h = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"h{min(i, j)}{max(i, j)}"))   # symmetric metric perturbation
g = gbar + eps * h
ginv = gbar.inv() - eps * gbar.inv() * h * gbar.inv()                      # O(eps) inverse
Abar = sp.Matrix([1 / N, 0, 0, 0])                                         # unit normal, A^mu
av = sp.Matrix(sp.symbols("a0p a1p a2p a3p"))                              # aether perturbation A^mu
A = Abar + eps * av
norm1 = sp.expand((A.T * g * A)[0, 0] + 1).coeff(eps, 1)                   # unit-norm constraint at O(eps)
a0sol = sp.solve(norm1, av[0])[0]
A = A.subs(av[0], a0sol)
Alow = g * A
dphi = sp.Matrix([phid, 0, 0, 0]) + eps * sp.Matrix(sp.symbols("d0 d1 d2 d3"))   # d_mu phi
q = ginv + (A * A.T)
if MUT:
    q = ginv                                                               # mutation: full metric, not the projector
Y = sp.expand((dphi.T * q * dphi)[0, 0])
Y0 = sp.simplify(Y.coeff(eps, 0))
Y1 = sp.simplify(sp.series(Y, eps, 0, 2).removeO().coeff(eps, 1))
P(f"  Y at eps^0 = {Y0};  Y at eps^1 = {Y1}")
check("K1", Y0 == 0 and Y1 == 0, f"Y0={Y0},Y1={Y1}", "both identically 0")
RES["K1"] = dict(Y0=str(Y0), Y1=str(Y1),
                 meaning="a0 sits in the Y-dependence of F; Y = O(eps^2), so the Y^{3/2} MOND term is O(eps^3): "
                         "absent from the background and from the linear equations")

# ------------------------------------------------------------------ K2: the dust abundance is a free charge
P("== K2: shift-symmetric Q-sector on FRW: what sets the dust abundance")
t = sp.symbols("t")
at, Nt, ph = sp.Function("a")(t), sp.Function("N")(t), sp.Function("phi")(t)
Kf = sp.Function("K")
Qs = sp.Symbol("Q")
L = at**3 * Nt * Kf(ph.diff(t) / Nt)
EL = sp.diff(L, ph) - sp.diff(sp.diff(L, ph.diff(t)), t)                  # Euler-Lagrange for phi
target = -sp.diff(at**3 * sp.Subs(sp.Derivative(Kf(Qs), Qs), Qs, ph.diff(t) / Nt).doit(), t)
eom_res = sp.simplify(EL - target)
rho_N = sp.simplify(-sp.diff(L, Nt) / at**3)                               # energy density from the lapse
rho_target = (Qs * sp.Derivative(Kf(Qs), Qs) - Kf(Qs)).subs(Qs, ph.diff(t) / Nt).doit()
rho_res = sp.simplify((rho_N - rho_target).subs(Nt, 1).doit())
# Higgs-phase K with Lambda: K = -2 Lambda + K2 (Q - Q0)^2 ; K' = I0/a^3
I0, Q0, K2, Lam, a0s, aa = sp.symbols("I_0 Q_0 K_2 Lambda a_0 a", positive=True)
Kq = -2 * Lam + K2 * (Qs - Q0)**2
Qsol = sp.solve(sp.Eq(sp.diff(Kq, Qs), I0 / aa**3), Qs)[0]
rho = sp.expand((Qs * sp.diff(Kq, Qs) - Kq).subs(Qs, Qsol))                # this is 8 pi G~ rho
dust = sp.simplify(rho.coeff(aa, -3))
P(f"  phi EOM residual vs -d/dt(a^3 K'(Q)) = {eom_res};  rho - (Q K' - K) residual = {rho_res}")
P(f"  8 pi G~ rho(a) = {rho}   -> dust coefficient {dust}")
d_I0, d_a0, d_L = sp.diff(dust, I0), sp.diff(dust, a0s), sp.diff(dust, Lam)
ok2 = eom_res == 0 and rho_res == 0 and d_I0 != 0 and d_a0 == 0 and d_L == 0
check("K2", ok2, f"EOMres={eom_res},rhores={rho_res},drho/dI0={d_I0},drho/da0={d_a0},drho/dLam={d_L}",
      "0,0,!=0,0,0")
RES["K2"] = dict(rho_8piG=str(rho), dust_coeff=str(dust), d_dI0=str(d_I0), d_da0=str(d_a0), d_dLambda=str(d_L),
                 verdict="I_0 is the conserved shift charge per comoving volume: an initial datum. Omega_c is FITTED "
                         "(one number, as CDM in LCDM). Nothing in the action ties it to a0 or Lambda.")

# ------------------------------------------------------------------ K3: cosh-K background, dust-share drift
P("== K3: cosh K(Q) (record L137 form; Q0 = K2 = I0 = 1, Z0/Q0 = 1e-3): dust share drift z=1090 -> 0")
Q0n, K2n, I0n, Z0n = 1.0, 1.0, 1.0, 1e-3


def cosh_state(n):
    Z = np.arcsinh(n / (2 * K2n * Z0n))
    Q = Q0n + Z0n * Z
    K = 2 * K2n * Z0n**2 * (np.cosh(Z) - 1.0)
    return Q * n - K, K                                                  # (8piG rho, 8piG P)


def zone(z):
    return I0n * (1 + z)**3


S0 = cosh_state(zone(0))[0] / zone(0)
S1 = cosh_state(zone(1090))[0] / zone(1090)
drift = S1 / S0 - 1
ana = (Z0n / Q0n) * math.log(zone(1090) / zone(0))
w0 = cosh_state(zone(0))[1] / cosh_state(zone(0))[0]
w1090 = cosh_state(zone(1090))[1] / cosh_state(zone(1090))[0]
P(f"  rho a^3 drift (z=1090 vs 0) = {drift:.5f};  analytic (Z0/Q0) ln(n1090/n0) = {ana:.5f};  w(0)={w0:.3e}, w(1090)={w1090:.3e}")
# E(z) effect if the dust share is normalised at z = 0 (E-886 Omega_m, f_c = omega_c/omega_m)
OM886, H886, SH886 = 0.2976015949416498, 0.6856426703851345, 0.005205912421590913
WB886, WC886 = 0.022208778152980592, 0.1170701352888568
fc = WC886 / (WB886 + WC886)
zz = np.array([0.5, 1.0, 2.33, 10, 100, 1090])
dEE = []
for z in zz:
    s = cosh_state(zone(z))[0] / zone(z) / S0
    e_dust = OM886 * (1 + z)**3 + (1 - OM886)
    e_cosh = OM886 * (1 + z)**3 * (1 - fc + fc * s) + (1 - OM886)
    dEE.append(0.5 * (e_cosh / e_dust - 1))
P("  dE/E vs the dust limit at z = " + ", ".join(f"{z:g}: {d:.2e}" for z, d in zip(zz, dEE)))
check("K3", abs(drift / ana - 1) < 0.10, f"{drift:.5f}/{ana:.5f}", "ratio within 10%")
RES["K3"] = dict(drift=drift, analytic=ana, w0=w0, w1090=w1090, dE_over_E=dict(zip(map(float, zz), dEE)),
                 scaling="drift ~ 20.9 (Z0/Q0): omega_c at recombination exceeds omega_c today by this fraction; "
                         "Z0/Q0 is a free parameter of K (POSTULATED in any AeST fit)")

# ------------------------------------------------------------------ K4: G_cosmo = g G_N map
P("== K4: background = GR with G_cosmo = g G_N for every species: BAO ratios and the H0 map")
C_KM = 299792.458
T_CMB = 2.7255
W_G = 2.469e-5 * (T_CMB / 2.7255)**4
W_R = W_G * (1.0 + 0.2271 * 3.044)


def zdrag_eh(wb, wm):
    b1 = 0.313 * wm**-0.419 * (1 + 0.607 * wm**0.674)
    b2 = 0.238 * wm**0.223
    return 1291.0 * wm**0.251 / (1 + 0.659 * wm**0.828) * (1 + b1 * wb**b2)


def model(gfac, wb, wc, wl):
    wm = wb + wc
    Hf = lambda z: 100.0 * math.sqrt(gfac * (wm * (1 + z)**3 + W_R * (1 + z)**4 + wl))
    zd = zdrag_eh(wb, wm)                                                # physical microphysics: g-independent here
    cs = lambda z: C_KM / math.sqrt(3 * (1 + 3 * wb / (4 * W_G) / (1 + z)))
    rd = quad(lambda z: cs(z) / Hf(z), zd, 1e7, limit=400)[0]
    DM = lambda z: quad(lambda x: C_KM / Hf(x), 0, z, limit=200)[0]
    return Hf, rd, DM


WL886 = (H886**2) * (1 - OM886) - W_R                                      # flat at g = 1
zb = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33]
H1, rd1, DM1 = model(1.0, WB886, WC886, WL886)
k4 = {}
worst = 0.0
for gfac in (0.9611, 0.6845):
    Hg, rdg, DMg = model(gfac, WB886, WC886, WL886)
    for z in zb:
        r1 = DMg(z) / rdg / (DM1(z) / rd1) - 1
        r2 = (C_KM / Hg(z) / rdg) / (C_KM / H1(z) / rd1) - 1
        worst = max(worst, abs(r1), abs(r2))
    pred = (gfac if MUT else math.sqrt(gfac)) * H1(0)
    k4[str(gfac)] = dict(H0_model=Hg(0), H0_pred=pred, rd_model=rdg, rd_GR=rd1)
    worst = max(worst, abs(Hg(0) / pred - 1))
    P(f"  g={gfac}: H0_model={Hg(0):.4f}, map={pred:.4f}; r_d {rdg:.3f} vs GR {rd1:.3f} Mpc")
P(f"  worst |residual| over D_M/r_d, D_H/r_d at 7 DESI z and the H0 map = {worst:.2e}")
check("K4", worst < 1e-6, f"{worst:.2e}", "<1e-6")
RES["K4"] = dict(worst_residual=worst, cases=k4,
                 statement="BAO + BBN cannot see g: at fixed physical densities, H(z) and r_d both scale as sqrt(g); "
                           "the native H0 is sqrt(g) times the GR-fit H0. Approximation: z_drag held at its "
                           "microphysical value (the drag rate/H shift with g is neglected).")

# ------------------------------------------------------------------ K5: the BBN-allowed native H0 band
P("== K5: native H0 under the A78 BBN bound G_cosmo/G_N > 0.9611 (E-A78) with the CFG886 GR fit (E-886)")
GMIN = 0.9611
LAD, SLAD = 73.0, 1.0
hi, lo = 100 * H886, 100 * H886 * math.sqrt(GMIN)
s_hi, s_lo = 100 * SH886, 100 * SH886 * math.sqrt(GMIN)
t_lad = ((LAD - hi) / SLAD, (LAD - lo) / SLAD)
t_comb = ((LAD - hi) / math.hypot(SLAD, s_hi), (LAD - lo) / math.hypot(SLAD, s_lo))
OM_A46 = 0.4610                                                           # A46 native Omega_m (Omega_eff = 0.3155)
B_A46 = (2 / 3) * OM_A46                                                  # beta = (2/3) Omega_m at the native Omega_m
beta021 = 2 / (2 + 3 * B_A46)                                             # = 1/(1+Omega_m) = 0.6845
h_b021 = 100 * H886 * math.sqrt(beta021)
P(f"  BBN-allowed native H0 in [{lo:.2f}, {hi:.2f}] km/s/Mpc; ladder 73.0+-1.0: {t_lad[0]:.2f}-{t_lad[1]:.2f} sigma "
  f"(ladder sigma only, E1 convention); {t_comb[0]:.2f}-{t_comb[1]:.2f} sigma (native error added)")
P(f"  the beta = (2/3)Omega_m branch (A42/A46, used by E1): native Omega_m {OM_A46}, beta {B_A46:.4f}, g = {beta021:.4f}, "
  f"H0 = {h_b021:.2f}; A78's line excludes it (Delta N_eff = {-11.1738 * B_A46:.2f}; at A42's beta 0.2109: "
  f"{-11.1738 * 0.21087:.2f}; vs |Delta N_eff| < 0.30)")
check("K5", hi > 60.0, f"{lo:.2f}-{hi:.2f}", "upper end > 60")
RES["K5"] = dict(H0_band=[lo, hi], tension_ladder_only=list(t_lad), tension_combined=list(t_comb),
                 g_beta_native=beta021, beta_native=B_A46, H0_beta_native=h_b021, dNeff_beta_native=-11.1738 * B_A46,
                 dNeff_beta0211=-11.1738 * 0.21087,
                 record_flag="doors_push_2026_10_22/E1_input_audit/README.md L43 (and e1_input_audit.py L104-107): the "
                             "native band 55.0-57.5 and '15.5-18 sigma' use the beta = (2/3)Omega_m background, which A78 "
                             "(committed earlier the same day, dc7cc7e409) excludes at ~8 sigma by BBN")

# ------------------------------------------------------------------ K6: AeST's K_B as the same lever
P("== K6: AeST lever: G~ = (1 - K_B/2) G^_qs (E-AeST). If G_N = G^_qs (OPEN), BBN gives K_B < 2(1 - 0.9611)")
kb = 2 * (1 - GMIN)
P(f"  K_B < {kb:.4f}; and since 0 < K_B < 2, g_AeST = 1 - K_B/2 < 1 can only LOWER the native H0 (never toward 73)")
check("K6", abs(kb - 0.0778) <= 0.001, f"{kb:.4f}", "0.0778+-0.001")
RES["K6"] = dict(KB_max=kb, open_item="G_N vs G^_qs (the lambda_s factor of the AeST Newtonian limit) is not on disk")

# ------------------------------------------------------------------ K7: growth index
P("== K7: linear growth on the dust-limit background (GR growth, source G_cosmo)")


def growth(Om, Eall, src=1.0):
    def rhs(x, y):
        aa_ = math.exp(x)
        E2 = Eall(aa_)
        dlnE = (Eall(aa_ * 1.0001) - Eall(aa_ * 0.9999)) / (2e-4) / (2 * E2)
        om_a = Om * aa_**-3 / E2
        return [y[1], -(2 + dlnE) * y[1] + 1.5 * src * om_a * y[0]]
    x0 = math.log(1e-3)
    sol = solve_ivp(rhs, (x0, 0.0), [1e-3, 1e-3], rtol=1e-10, atol=1e-13)
    D, dD = sol.y[0, -1], sol.y[1, -1]
    return dD / D, D


E886 = lambda aa_: OM886 * aa_**-3 + (1 - OM886)
f886, D886 = growth(OM886, E886)
gam = math.log(f886) / math.log(OM886)
OMA42 = 0.3163
oe = OMA42 / (1 + OMA42)
Eb = lambda aa_: oe * aa_**-3 + (1 - oe)
fb, _ = growth(oe, Eb)
fN, DN = growth(OM886, E886, src=1 / GMIN)                               # variant: Poisson with G_N, background G_cosmo
P(f"  E-886 dust limit: f(0) = {f886:.4f}, gamma = {gam:.4f};  beta=0.21 background (A46/A45): f(0) = {fb:.4f} (A45: 0.452)")
P(f"  variant (OPEN premise: sub-horizon source G_N, background G_cosmo, g = 0.9611): f(0) = {fN:.4f}, "
  f"D(0) ratio = {DN / D886:.4f} (sigma8 +{100 * (DN / D886 - 1):.1f}%)")
check("K7", abs(fb - 0.452) < 0.005, f"{fb:.4f}", "|f-0.452|<0.005")
RES["K7"] = dict(f0=f886, gamma=gam, f0_beta021=fb, f0_variant_GN=fN, D_ratio_variant=DN / D886)

# ------------------------------------------------------------------ K8: CLASS cross-check
P("== K8: CLASS (classy) r_d at E-886 physical densities vs this script's quadrature")
from classy import Class
cl = Class()
cl.set({"h": H886, "omega_b": WB886, "omega_cdm": WC886, "T_cmb": T_CMB, "N_ur": 3.044, "output": ""})
cl.compute()
rd_class = cl.rs_drag()
zd_class = cl.get_current_derived_parameters(["z_d"])["z_d"]
cl.struct_cleanup(); cl.empty()
dr = rd1 / rd_class - 1
P(f"  CLASS {Class.__module__}: r_d = {rd_class:.3f} Mpc (z_d {zd_class:.2f}); quadrature {rd1:.3f} Mpc (EH z_d "
  f"{zdrag_eh(WB886, WB886 + WC886):.2f}); diff {100 * dr:+.2f}%")
P(f"K8-orig {'PASS' if abs(dr) < 0.015 else 'FAIL'} {100 * dr:+.3f}% |diff|<1.5%   (frozen line; reported, superseded by K8b, AMENDMENT A1 post-result)")
rd_b = quad(lambda z: C_KM / math.sqrt(3 * (1 + 3 * WB886 / (4 * W_G) / (1 + z))) / H1(z), zd_class, 1e7, limit=400)[0]
drb = rd_b / rd_class - 1
P(f"  AMENDMENT A1: same quadrature with CLASS's z_d: r_d = {rd_b:.3f} Mpc, diff {100 * drb:+.3f}%")
check("K8b", abs(drb) < 0.015, f"{100 * drb:+.3f}%", "|diff|<1.5% (A1, post-result)")
RES["K8"] = dict(rd_class=rd_class, zd_class=zd_class, rd_quad_EH=rd1, diff_EH=dr, K8_orig_pass=abs(dr) < 0.015,
                 rd_quad_class_zd=rd_b, diff_class_zd=drb,
                 note="frozen K8 FAILED: the uncalibrated Eisenstein-Hu z_d (1020) is 39 below CLASS (1059); "
                      "K4/K5 are unaffected (z_d cancels in the ratios; K5 uses CFG886's fitted h)")

# ------------------------------------------------------------------ K9: inventory
P("== K9: tools and data on disk (no fetch)")


def sha(p, n=16):
    hh = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            hh.update(b)
    return hh.hexdigest()[:n]


def mod_ver(m):
    s = importlib.util.find_spec(m)
    if s is None:
        return None
    mm = __import__(m)
    return getattr(mm, "__version__", "?")


present = {
    "classy (CLASS)": mod_ver("classy"), "camb": mod_ver("camb"), "healpy": mod_ver("healpy"),
    "pyccl (cfg592 venv)": bool(glob.glob(os.path.join(EXT, "cfg592_work", "venv", "lib", "python3*", "site-packages",
                                                     "pyccl"))),
}
data_present = {
    "KiDS-1000 xi+- (fits, cov, n(z))": glob.glob(os.path.join(EXT, "cfg592_work", "kids", "*", "data_fits",
                                                               "xipm_KIDS1000_*.fits")),
    "DES Y3 2pt (xi+-)": glob.glob(os.path.join(EXT, "cfg592_work", "2pt_NG_final_2ptunblind_*.fits")),
    "Planck PR4 lensing bandpowers": glob.glob(os.path.join(EXT, "cmb_lensing_raw", "planck_PR4_lensing", "planckpr4lensing",
                                                            "data_pr4", "*PS1_bandpowers.dat")),
    "Planck PR4 lensing cov": glob.glob(os.path.join(EXT, "cmb_lensing_raw", "planck_PR4_lensing", "planckpr4lensing",
                                                     "data_pr4", "*PS1_cov.dat")),
    "Pantheon+ SNe": glob.glob(os.path.join(REPO, "prep_2026", "sne_lambda", "pantheonplus_full.dat")),
    "Planck 2018 params paper source (1807.06209)": glob.glob(os.path.join(EXT, "cmb_lensing_raw", "planck2018_params",
                                                                           "1807.06209.src")),
    "DESI DR2 chains (LCDM-processed, not data)": glob.glob(os.path.join(EXT, "desi_dr2_chains", "cmb", "chain.1.txt")),
}
inv = {}
okp = True
for k, v in present.items():
    inv[k] = v; okp &= bool(v)
    P(f"  present  {k}: {v}")
for k, v in data_present.items():
    inv[k] = [dict(path=os.path.relpath(p, os.path.join(REPO, "..")), sha16=sha(p)) for p in v]
    okp &= bool(v)
    P(f"  present  {k}: {[d['path'] + ' ' + d['sha16'] for d in inv[k]]}")
# absent items
pat = ["COM_PowerSpect*", "*plik*", "*clik*", "*hillipop*", "*camspec*", "*hi_class*", "*hiclass*", "newRMONDLett*",
       "*2007.00082*"]
pat_A1 = ["COM_PowerSpect*", "plik_*", "clik", "clik_*", "*.clik", "*hillipop*", "*camspec*", "*hi_class*", "*hiclass*",
          "newRMONDLett*", "*2007.00082*"]                                 # A1: '*clik*'/'*plik*' matched 'rclike', 'grouplike', 'multiplikat'
hits_A1 = []
hits = []
skip = {".git", ".claude", "venv", "pysco_venv", "pyautolens_env", ".venv_g035", "node_modules", "__pycache__"}
for root in (EXT, REPO):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in skip and not d.startswith(".venv")]
        for nm in fns + dns:
            low = nm.lower()
            if low.endswith(".pdf") or low.endswith(".png"):
                continue                                                  # figures from the Planck paper source
            if any(glob.fnmatch.fnmatch(low, p.lower()) for p in pat):
                hits.append(os.path.relpath(os.path.join(dp, nm), os.path.join(REPO, "..")))
            if any(glob.fnmatch.fnmatch(low, p.lower()) for p in pat_A1):
                hits_A1.append(os.path.relpath(os.path.join(dp, nm), os.path.join(REPO, "..")))
absent = {"hi_class / AeST-CLASS module": importlib.util.find_spec("hi_class") is None,
          "clik (Planck likelihood code)": importlib.util.find_spec("clik") is None,
          "cobaya": importlib.util.find_spec("cobaya") is None,
          "Planck TT/TE/EE spectra or likelihood files, AeST paper source": len(hits) == 0}
for k, v in absent.items():
    P(f"  absent   {k}: {v}")
if hits:
    P(f"  hits with the frozen patterns ({len(hits)}), first 5: {hits[:5]}")
P(f"K9-orig {'PASS' if okp and all(absent.values()) else 'FAIL'} present={okp},absent={all(absent.values())} all True"
  f"   (frozen line; reported, superseded by K9b, AMENDMENT A1 post-result)")
TT = [hh for hh in hits_A1 if os.path.basename(hh) == "COM_PowerSpect_CMB-TT-full_R3.01.txt"]
other = [hh for hh in hits_A1 if hh not in TT]
ttinfo = {}
if TT:
    tp = os.path.join(REPO, "..", TT[0])
    arr = np.loadtxt(tp)
    ttinfo = dict(path=TT[0], sha16=sha(tp), n_ell=int(arr.shape[0]), lmin=int(arr[0, 0]), lmax=int(arr[-1, 0]),
                  columns="l, Dl, -dDl, +dDl (diagonal errors only; no covariance, no TE/EE)")
    P(f"  A1: PRESENT Planck PR3 TT unbinned spectrum {ttinfo}")
P(f"  A1: other hits with corrected patterns ({len(other)}): {other[:5]}")
check("K9b", okp and absent['hi_class / AeST-CLASS module'] and absent['clik (Planck likelihood code)'] and
      absent['cobaya'] and len(TT) == 1 and len(other) == 0,
      f"present={okp},TT_found={len(TT)},other_hits={len(other)}", "tools absent, 1 TT file, 0 other (A1, post-result)")
RES["K9"] = dict(present=inv, absent=absent, n_hits_orig_patterns=len(hits), hits_orig_patterns_first=hits[:5], hits_A1=hits_A1, planck_TT=ttinfo,
                 K9_orig_pass=bool(okp and all(absent.values())))

# ------------------------------------------------------------------ end
npass = sum(ok for _, ok in CHK)                                         # K8b/K9b replace K8/K9 (AMENDMENT A1)
P(f"C2_AEST_COSMOLOGY COMPLETE: {npass}/{len(CHK)} checks PASS.")
RES["checks"] = dict(CHK)
json.dump(RES, open(os.path.join(HERE, f"c2_aest_cosmology_results{TAG}.json"), "w"), indent=1, default=str)
OUT.close()
sys.exit(0 if npass == len(CHK) else 1)
