#!/usr/bin/env python3
"""TM1_tethered_medium: PAPER49's tethered medium (its exact action) scored on six hard rows.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (committed alone first, 167976b20a).
Run:   OMP_NUM_THREADS=1 nice -n 15 python3 tm1_tethered_medium.py            -> .out, _results.json (exit 0 iff all checks pass)
       OMP_NUM_THREADS=1 nice -n 15 python3 tm1_tethered_medium.py --mutate   -> _MUTATE.out, _results_MUTATE.json (must exit 1)
Inputs are read only (record sources exec'd from their text, data loaded from their files); nothing is downloaded.
kappa = 1/2 FITTED.  Footings canonical / alt, never pooled.  Cold energy is a medium of real rest mass, no particle.
Not "theory closed".  Nothing here says the data favour the framework.
"""
import os, sys, io, re, csv, json, math, time, shutil, hashlib, resource, subprocess, tempfile, warnings
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.dirname(HERE)
REPO = os.path.dirname(REB)
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
T0 = time.time()
OUTL, CHECKS = [], {}
RES = dict(lane="TM1_tethered_medium", criteria="167976b20a", mutate=MUT, checks=CHECKS, rows={})
FEET = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KPC = 3.0857e19
FC = 5.364                                    # Omega_c / Omega_b (measured)
FBN = 1.0 / (1.0 + FC)


def P(s=""):
    OUTL.append(str(s)); print(s, flush=True)


def check(k, ok, val, thr, what=""):
    CHECKS[k] = dict(ok=bool(ok), value=str(val), line=str(thr), what=what)
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} :: {thr}  ({what})")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


def cut(txt, a, b):
    i = txt.index(a); j = txt.index(b, i); return txt[i:j]


P("=" * 118)
P("TM1_tethered_medium: PAPER49's tethered medium scored on the hardest rows" + ("   [MUTATE]" if MUT else ""))
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled; not theory closed")
P("=" * 118)
SRC = {k: os.path.join(REPO, v) for k, v in dict(
    paper="qwen_claude_field_theory/papers_2026/PAPER49_why_cold_energy_settles_2026.tex",
    ag6c="argon_push/AG6C_relativistic_completion/ag6c_s0_saddle.py",
    f1="rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores.py",
    x2="rebuild_2026_10_22/X2_cluster_outskirts/x2_cluster_outskirts.py",
    x2npz="rebuild_2026_10_22/X2_cluster_outskirts/x2_replay_percluster.npz",
    x2json="rebuild_2026_10_22/X2_cluster_outskirts/x2_cluster_outskirts_results.json",
    d6="doors_push_2026_10_22/D6_u_mechanism/d6_u_mechanism.py",
    d6npz="doors_push_2026_10_22/D6_u_mechanism/d6_selfsim_tables.npz",
    f3="rebuild_2026_10_22/F3_growth_audit/f3_growth_audit.py",
    f3json="rebuild_2026_10_22/F3_growth_audit/f3_growth_audit_results.json",
    z2csv="rebuild_2026_10_22/Z2_satellite_systematics/z2_per_system.csv",
    z2json="rebuild_2026_10_22/Z2_satellite_systematics/z2_satellite_systematics_results.json",
    p4="rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py",
    p4json="rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles_results.json").items()}
RES["source_sha256_16"] = {k: sha(v) for k, v in SRC.items()}
P("sources (sha256/16): " + ", ".join(f"{k} {v}" for k, v in RES["source_sha256_16"].items()))

# =====================================================================================================================
# S1-S6: the action, symbolically
# =====================================================================================================================
P("\n=== S: PAPER49's action, symbolically (sympy) ===")
u, s_, a0s, Ks, gs, gam = sp.symbols("u s a0 K g gamma", positive=True)
W_full = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / Ks
W_rem = W_full - u ** 2 / (2 * Ks)
W_used = W_full if MUT else W_rem                                   # M1: W_full in place of W_rem (double counts the quadratic)
dW_ok = sp.simplify(Ks * sp.diff(W_rem, u) - u ** 2 / (a0s - u)) == 0 and sp.simplify(Ks * sp.diff(W_full, u) - a0s * u / (a0s - u)) == 0
ser = sp.series(W_used, u, 0, 5).removeO()
lead = sp.simplify(ser - u ** 3 / (3 * a0s * Ks) - u ** 4 / (4 * a0s ** 2 * Ks))
check("S1", dW_ok and lead == 0, f"K W_rem' = u^2/(a0-u): {dW_ok}; series(W used) = {sp.simplify(ser)}",
      "series == u^3/(3 a0 K) + u^4/(4 a0^2 K) (no u^2 term)", "W_rem starts at cubic order: no linear tether force about P = 0")

# S2: Euler-Lagrange in 1D (planar, P > 0) and the rest state
x = sp.symbols("x", real=True)
Phi = sp.Function("Phi")(x); Pf = sp.Function("P")(x); rb = sp.Function("rho_b")(x)
Wf = sp.Lambda(u, W_used)
L1 = -(sp.diff(Phi, x) - Ks * Pf) ** 2 / (2 * Ks) - rb * Phi - Wf(Ks * Pf) - gam / 2 * sp.diff(Pf, x) ** 2
EL = sp.euler_equations(L1, [Phi, Pf], x)
eqPhi = sp.simplify(EL[0].lhs); eqP = sp.simplify(EL[1].lhs)
poisson_ok = sp.simplify(eqPhi - (sp.diff(Phi, x, 2) - Ks * sp.diff(Pf, x)) / Ks + rb) == 0 or \
    sp.simplify(eqPhi + (sp.diff(Phi, x, 2) - Ks * sp.diff(Pf, x)) / Ks - rb) == 0
R_of = lambda uu: uu ** 2 / (a0s - uu)
Peq_target = (sp.diff(Phi, x) - Ks * Pf) - R_of(Ks * Pf) + gam * sp.diff(Pf, x, 2)
peq_ok = sp.simplify(eqP - Peq_target) == 0 or sp.simplify(eqP + Peq_target) == 0
u_rest = a0s * gs / (a0s + gs)
gN_rest = sp.simplify(R_of(u_rest))
rest_ok = sp.simplify(gN_rest - gs ** 2 / (gs + a0s)) == 0 and sp.simplify((gs - u_rest) - gN_rest) == 0
check("S2", poisson_ok and peq_ok and rest_ok, f"Poisson {poisson_ok}; P-eq {peq_ok}; rest g_N = {gN_rest}",
      "lap Phi = K(rho_b + div P); (grad Phi - K P) - R(u) + gamma lap P = 0; g_N = g^2/(g + a0)", "field equations and the n = 1 rest state")
RES["S2"] = dict(EL_Phi=str(eqPhi), EL_P=str(eqP), rest_gN=str(gN_rest))

# S3: self-gravity of the tethered medium.  1D: Phi' = K (M_b(x) + P) + c  ->  force on the medium element
Mb_ = sp.Function("M_b")(x); c0 = sp.symbols("c0")
dPhi = Ks * (Mb_ + Pf) + c0
force = (dPhi - Ks * Pf) - sp.diff(W_used, u).subs(u, Ks * Pf) * Ks           # gamma-term omitted (gradient, not self-gravity)
pp = sp.symbols("p", positive=True)
dF_dP = sp.limit(sp.diff(force.subs(Pf, pp), pp), pp, 0)
# 3D linear, longitudinal Fourier mode
k_, rhok, PL = sp.symbols("k rho_k P_L")
Phik = -Ks * (rhok + sp.I * k_ * PL) / k_ ** 2
gNL = sp.simplify(sp.I * k_ * Phik - Ks * PL)
dgN = sp.simplify(sp.diff(gNL, PL))
check("S3", dF_dP == 0 and dgN == 0, f"1D d(force)/dP at P->0 = {dF_dP}; 3D longitudinal (grad Phi - K P)_L = {gNL}, d/dP_L = {dgN}",
      "both == 0", "the tethered medium feels no self-gravity and no linear tether force (D-T on PAPER49's own action)")
RES["S3"] = dict(dF_dP_1D=str(dF_dP), gN_L=str(gNL))

# S4: PAPER49's static P-equation == D10's stiffened equation (curl-free P), Lambda = L*
pv = sp.symbols("p", positive=True); Ls = sp.symbols("Lstar", positive=True)
rhs_paper = Ks * (a0s * pv / Ks) + R_of(a0s * pv)                    # K|P| + R(u), u = a0 p
rhs_d10 = a0s * pv / (1 - pv)
gamma_val = Ks * Ls ** 2 / 2
lhs_coeff = sp.simplify(gamma_val * a0s / Ks / a0s)                  # gamma lap P = (gamma a0/K) lap p ; divide by a0
X, Y, Z = sp.symbols("X Y Z", real=True); chi = sp.Function("chi")(X, Y, Z)
pvec = [sp.diff(chi, v) for v in (X, Y, Z)]
divp = sum(sp.diff(pvec[i], v) for i, v in enumerate((X, Y, Z)))
lap_vs_graddiv = all(sp.simplify(sum(sp.diff(pvec[i], v, 2) for v in (X, Y, Z)) - sp.diff(divp, (X, Y, Z)[i])) == 0 for i in range(3))
s4 = sp.simplify(rhs_paper - rhs_d10) == 0 and sp.simplify(lhs_coeff - Ls ** 2 / 2) == 0 and lap_vs_graddiv
check("S4", s4, f"K|P| + R = a0 p/(1-p): {sp.simplify(rhs_paper - rhs_d10) == 0}; stiffness coefficient {lhs_coeff}; lap p = grad div p (curl-free): {lap_vs_graddiv}",
      "identical to D10: grad Phi + (Lambda^2/2) grad div p = p/(1-|p|), Lambda = L*", "Z2's V3S and P4's T1 rows are this action's rest state")

# S5: kinetic matrices (ghost test).  Completion: L_kin = rho_b xi_b'^2/2 + rho_c xi_c'^2/2  (P = -rho_c xi_c)
rb0, rc0 = sp.symbols("rho_b0 rho_c0", positive=True)
xb_d, xc_d = sp.symbols("xidot_b xidot_c")
Lkin = rb0 * xb_d ** 2 / 2 + rc0 * xc_d ** 2 / 2
Hk = sp.hessian(Lkin, (xb_d, xc_d))
ev_k = list(Hk.eigenvals().keys())
blt = sp.Matrix([[1, 1], [1, 0]]); ev_blt = sorted([float(e) for e in blt.eigenvals().keys()])
ghost_free = all(sp.simplify(e).is_positive for e in ev_k)
check("S5", ghost_free and blt.det() == -1 and abs(ev_blt[0] + 0.618034) < 1e-5,
      f"completion kinetic eigenvalues {ev_k}; BLT [[1,1],[1,0]] det {blt.det()} eig {[round(e, 6) for e in ev_blt]}",
      "completion positive definite; BLT det -1 (Z1 K1)", "PAPER49 + forced kinetic term has no ghost; BLT has one")
# gradient sector of the medium: L2 = rho_c xi'^2/2 - (gamma/2) rho_c^2 k^2 xi^2  ->  omega^2 = gamma rho_c k^2
om2 = sp.symbols("omega2")
w2 = sp.solve(sp.Eq(rc0 * om2, gam * rc0 ** 2 * k_ ** 2), om2)[0]
RES["S5"] = dict(kinetic_eigs=[str(e) for e in ev_k], BLT_eigs=ev_blt, medium_omega2=str(w2), note="omega^2 = gamma rho_c k^2 >= 0: gradient-stable")
P(f"   medium gradient sector: omega^2 = {w2} >= 0 (gradient-stable); c_s^2 = gamma rho_c = 2 pi G rho_c L*^2")

# S6: EdS growth exponent of the completed linear system
fb = sp.Rational(1000, 6364); fcs = 1 - fb
lam = sp.symbols("lambda")
Mgr = sp.Matrix([[fb, fcs], [fb, fcs if MUT else 0]])               # M2 (mutate): the medium given full self-gravity
lam_max = max(float(e) for e in Mgr.eigenvals().keys())
pexp = sp.symbols("p_exp")
p_grow = max(float(r) for r in sp.solve(pexp ** 2 + pexp / 2 - sp.Rational(3, 2) * sp.nsimplify(lam_max, rational=False), pexp))
check("S6", abs(p_grow - 0.610) <= 0.005, f"growing exponent p = {p_grow:.4f} (largest eigenvalue {lam_max:.4f})", "0.610 +- 0.005 (CFG938)",
      "delta ~ a^p in EdS with the medium feeling only the baryons")
RES["S6"] = dict(p=p_grow, lambda_max=lam_max)

# =====================================================================================================================
# ROW 1: growth on FRW with F3's machinery
# =====================================================================================================================
P("\n=== ROW 1: growth on FRW (forced minimal completion; F3's growth_ratio, exec'd read-only) ===")
TF3 = open(SRC["f3"]).read()
NS3 = {"np": np, "math": math, "solve_ivp": solve_ivp}
exec(cut(TF3, "def make_E(", "# ------------------------------------------------------------------ K0b"), NS3)
growth_ratio = NS3["growth_ratio"]
F3J = json.load(open(SRC["f3json"]))
BGS = {}
for tag in ("A_c2b_refit", "B_cfg886_bg"):
    pr = F3J["K2"][tag]["params"]; h = pr["h"]; Om = F3J["K2"][tag]["Om"]; Ob = pr["omega_b"] / h ** 2
    BGS[tag] = dict(h=h, Om=Om, Ob=Ob)
KT = np.geomspace(1e-3, 3.0, 36)
ref = F3J["K4"]["BSK2_floor_1100"]["bsk2_ai0.001"]["T_at_k"]
bA = BGS["A_c2b_refit"]
Tchk = growth_ratio(KT, 1.1e3, bA["Om"], bA["Ob"], bA["h"], "bsk2", 1e-3)
dF3 = max(abs(float(Tchk[::5][i]) - v) for i, v in enumerate(ref.values()))
check("F3a", dF3 <= 1e-4, f"max |dT| = {dF3:.2e} over {len(ref)} k", "<= 1e-4", "F3's growth_ratio reproduces F3's committed K4 BSK2_floor_1100 transfer")
MU_TETHER = 1e-12        # s = 1/(1 + (k/(a mu))^2) -> 0: the tethered medium has no self-gravity (S3)
R1 = {}
for tag, b in BGS.items():
    for ai in (1e-3, 1e-4):
        T = growth_ratio(KT, MU_TETHER, b["Om"], b["Ob"], b["h"], "bsk2", ai)
        R1[f"{tag}|ai{ai:g}"] = dict(sigma8_ratio=float(np.mean(T)), T_min=float(T.min()), T_max=float(T.max()))
        P(f"   {tag:12s} a_i {ai:g}: delta_m / delta_m(dust) = {np.mean(T):.4f} (k-spread {T.max() - T.min():.1e}; scale-free, so sigma8/sigma8,dust = this)")
cs_kms = {L: math.sqrt(2 * math.pi * G * FC * 0.0224 * 1.8785e-26) * L * 3.0857e16 / 1e3 for L in (24.0, 1000.0)}
P(f"   stiffness sound speed today c_s = sqrt(2 pi G rho_c) L*: {cs_kms[24.0]*1e3:.2f} m/s (24 pc), {cs_kms[1000.0]*1e3:.1f} m/s (1 kpc): "
  "Jeans-like cut only at k ~ 1/L*, far beyond sigma8 scales (not included; it only lowers growth)")
r1min = min(v["sigma8_ratio"] for v in R1.values())
r1_class = "PASS" if (ghost_free and r1min >= 0.95) else "FAIL"
RES["rows"]["1_growth"] = dict(
    paper_as_written="NOT COMPUTABLE: PAPER49's Lagrangian has no time derivative of P or of the medium, no background and no "
                     "relativistic completion (L60 lists the completion as not derived). Missing: the medium's inertia, the FRW "
                     "background of P (P = 0 by isotropy), how u = K|P| behaves in the linear universe, and a metric sector.",
    completion="L = rho_b|xi_b'|^2/2 + rho_c|xi_c'|^2/2 + PAPER49's L, P = -rho_c xi_c (forced: real rest mass, d_t P = -j)",
    health=dict(ghost_free=ghost_free, gradient="omega^2 = gamma rho_c k^2 >= 0"),
    growth_exponent_EdS=p_grow, sigma8_over_dust=R1, cs_today_kms=cs_kms,
    record_parent="CFG938 covariant parent: Hadamard ILL-POSED on FRW (CFG961, WT-02); growth a^0.694 (CFG941). Not re-derived.",
    record_limit="CFG944: the always-on tether's argument reaches the u = a0 wall at z >= 84, so linear theory with u << a0 fails "
                 "earlier; at the wall the medium cannot displace further, which can only lower its growth.",
    cls=r1_class)
P(f"   ROW 1 class: {r1_class} (min sigma8/sigma8,dust {r1min:.4f} vs line 0.95; healthy {ghost_free})")

# =====================================================================================================================
# ROW 2: satellites (Z2's committed per-system data; rest state = V3S by S4)
# =====================================================================================================================
P("\n=== ROW 2: satellites with real cold mass ===")
rows = [r for r in csv.DictReader(open(SRC["z2csv"]))]
Z2J = json.load(open(SRC["z2json"]))
fl = lambda v: float(v) if v not in ("", "None", "nan") else float("nan")
R2 = {}
for f in FEET:
    rr = [r for r in rows if r["footing"] == f]
    clean = [r for r in rr if r["pm"] == "True" and fl(r["q_V3S"]) < 0.5 and fl(r["ell"]) < 0.5 and r["grad_flag"] != "True" and fl(r["N_q"]) >= 10]
    med = float(np.median([fl(r["Delta_V3S"]) for r in clean])) if clean else float("nan")
    ok = [r for r in rr if np.isfinite(fl(r["x_e"])) and np.isfinite(fl(r["M_V"]))]
    Xm = np.column_stack([np.ones(len(ok)), np.log10([fl(r["x_e"]) for r in ok]), [fl(r["M_V"]) for r in ok]])
    lb = np.array([fl(r["lb0"]) for r in ok]); pred = lb - np.array([fl(r["Delta_V3S"]) for r in ok])
    b_pred = float(np.linalg.lstsq(Xm, pred, rcond=None)[0][1]); b_dat = float(np.linalg.lstsq(Xm, lb, rcond=None)[0][1])
    R2[f] = dict(clean_names=[r["name"] for r in clean], clean_median=med, N_clean=len(clean), N_slope=len(ok), slope_pred=b_pred, slope_data=b_dat)
    P(f"   [{f}] clean (C1-C4) N {len(clean)} {[r['name'] for r in clean]}: median Delta_V3S {med:+.3f}; "
      f"slope on log x_e | M_V (N {len(ok)}): V3S prediction {b_pred:+.3f}, data {b_dat:+.3f}")
check("Z2a", abs(R2["canonical"]["clean_median"] - 0.900) <= 0.05, f"{R2['canonical']['clean_median']:+.3f}", "+0.900 +- 0.05",
      "Z2's clean-subset V3S excess reproduced from its per-system CSV (canonical)")
check("Z2b", abs(R2["canonical"]["slope_pred"] + 0.55) <= 0.05 and abs(R2["canonical"]["slope_data"] + 0.05) <= 0.05,
      f"pred {R2['canonical']['slope_pred']:+.3f}, data {R2['canonical']['slope_data']:+.3f}", "-0.55 / -0.05 +- 0.05",
      "Z2's host-field slopes at fixed M_V reproduced (canonical)")
# scored numbers: Z2's committed bootstrap values (README L19-L28, L100-L103)
Z2S = dict(canonical=dict(clean=(0.900, 0.213, 6), c2c4=(1.169, 0.146, 19)), alt=dict(clean=(0.787, 0.235, 5), c2c4=(1.162, 0.150, 19)))
SLOPE_DATA = (-0.05, 0.19)
r2cls = {}
for f in FEET:
    c = Z2S[f]["clean"] if Z2S[f]["clean"][2] >= 6 else Z2S[f]["c2c4"]
    ex_ok = abs(c[0]) <= 2 * c[1]
    sl_ok = abs(R2[f]["slope_pred"] - SLOPE_DATA[0]) <= 2 * SLOPE_DATA[1]
    r2cls[f] = "PASS" if (ex_ok and sl_ok) else "FAIL"
    R2[f].update(scored_excess=c, excess_within_2sd=ex_ok, slope_within_2sd=sl_ok, cls=r2cls[f],
                 subset="clean C1-C4" if Z2S[f]["clean"][2] >= 6 else "C2-C4 only (clean TOO FEW)")
    P(f"   [{f}] scored excess {c[0]:+.3f} +- {c[1]:.3f} ({R2[f]['subset']}): within 2 sd {ex_ok}; predicted slope {R2[f]['slope_pred']:+.2f} "
      f"vs data {SLOPE_DATA[0]:+.2f} +- {SLOPE_DATA[1]}: within 2 sd {sl_ok} -> {r2cls[f]}")
RES["rows"]["2_satellites"] = dict(
    per_footing=R2, cls="FAIL" if "FAIL" in r2cls.values() else "PASS",
    self_binding="NO. S3: the tethered medium's self-gravity cancels exactly in PAPER49's own action (and W_rem has no quadratic "
                 "term, S1), so a satellite's tethered cold mass exerts no pull on itself or on other tethered medium (CFG941 D-T). "
                 "Its rest state is fixed pointwise by the total baryonic Newtonian field (host + satellite): stiffened AQUAL with "
                 "the host's EFE (S4) = Z2's V3S row. Dynamically the label-free tether hovers in the host (CFG945 Theorem S; "
                 "CFG941 delta-a/g_host 1.02-1.11; stars leave it in 9-106 Myr), which drives the system to the dust-free limit "
                 "(Z2 V3D, +1.88 dex C2-C4). Contrast: U1 T3 (held dust weightless) and O1 (epsilon = 1) say the same for v3; "
                 "Y1's P-medium binds only because its tether is finite (and it loses the law).",
    dust_free_limit=dict(canonical=(1.880, 0.097), alt=(1.885, 0.100)))
P(f"   ROW 2 class: {RES['rows']['2_satellites']['cls']}")

# =====================================================================================================================
# ROW 3: cluster cores with untethered cold energy (self-similar collisionless infall, no NFW)
# =====================================================================================================================
P("\n=== ROW 3: cluster cores, untethered cold energy (postulate U), self-similar infall profile ===")
TF1 = open(SRC["f1"]).read(); TX2 = open(SRC["x2"]).read()
NSF = {"np": np, "os": os, "sys": sys, "REPO": REPO, "_trap": np.trapz, "PchipInterpolator": PchipInterpolator}
exec(cut(TF1, "G = 6.674e-11", "# ---------------------------------------------------------------- sources"), NSF)
exec(cut(TF1, "EDGES = np.logspace", "def gather("), NSF)
exec(cut(TF1, "RG = np.logspace(-3", "# SIS self-test (K4)"), NSF)
NSF.update(RG=NSF["RG"], RF=NSF["RF"], UU=NSF["UU"], MPC=MPC, MSUN=MSUN, math=math)
exec(cut(TX2, "def project_floor(", "# ============================================================== gas profiles"), NSF)
exec(cut(TX2, "def gas(", "# ============================================================== EFE"), NSF)
RG, RC, BANDS = NSF["RG"], NSF["RC"], NSF["BANDS"]; RM = RG * MPC
DM, DA_lcdm, g_aqual_sph = NSF["DM"], NSF["DA_lcdm"], NSF["g_aqual_sph"]
project_floor, offset_floor, dsig_from_sig, at_bins, gas = (NSF[k] for k in ("project_floor", "offset_floor", "dsig_from_sig", "at_bins", "gas"))
KG_PC2 = NSF["KG_PC2"]
X = np.load(SRC["x2npz"]); N = len(X["z"])
CL = [dict(z=float(X["z"][i]), Mgas500=float(X["Mgas500"][i]), R500=float(X["R500"][i]), off_deg=float(X["off_deg"][i])) for i in range(N)]
order = np.argsort(X["ra"]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N) * 30 // N
ALL = np.ones(N, bool)
_q = np.quantile(X["Mgas500"], [1 / 3, 2 / 3]); TID = np.digitize(X["Mgas500"], _q); TERC = {f"T{t+1}": TID == t for t in range(3)}
HK = ("h0672", "h0686"); HV = {"h0672": 0.672, "h0686": 0.686}; HI = {"h070": 0, "h0672": 1, "h0686": 2}
DAT = {}
for hk in HK:
    i = HI[hk]; Et = X["E"][:, i]; W = np.where(Et < 1e8, 1 / Et ** 2, 0)
    B = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=X["D"][:, i] * B[None, :], W=W)


def A_band(D, Pm, W, sel):
    return {b: float((W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum()) for b, j in BANDS.items()}


def jk(D, Pm, W, sel=ALL):
    full = A_band(D, Pm, W, sel)
    reps = [A_band(D, Pm, W, sel & (PATCH != p)) for p in range(30) if (sel & (PATCH != p)).sum() < sel.sum()]
    return {b: (full[b], float(np.sqrt((len(reps) - 1) / len(reps) * np.sum((np.array([r[b] for r in reps]) - np.mean([r[b] for r in reps])) ** 2)))) for b in full}


# self-similar tables (D6, read-only) and the SSb re-solve
SSz = np.load(SRC["d6npz"], allow_pickle=True); SS = SSz["SS"].item()
s1 = SS["1.0000"]
check("SSa", abs(s1["lsp"] - 0.364) <= 0.01 and all(abs(s["M_at_1"] - 1) <= 1e-4 for s in SS.values()),
      f"lambda_sp(eps=1) {s1['lsp']:.4f}; M(1) {[round(float(s['M_at_1']), 6) for s in SS.values()]}", "0.364 +- 0.01; 1 +- 1e-4",
      "D6 self-similar tables (Bertschinger caustic, normalisation)")
CACHE = os.path.join(HERE, "tm1_selfsim_resolve_2x.npz")          # AMENDMENT A1: written by tm1_selfsim_resolve.py (2x tau_max)
SS3 = np.load(CACHE, allow_pickle=True)["SS"].item() if os.path.exists(CACHE) else None
P(f"   SSb: re-solved tables {'loaded from ' + os.path.basename(CACHE) if SS3 else 'MISSING -> row 3 PROVISIONAL on D6 tables'}")
LGT = np.geomspace(0.02, 1.0, 60)
ssb = {}
for k_ in (SS if SS3 else []):
    a = np.interp(np.log(LGT), np.log(SS[k_]["lg"]), SS[k_]["M"]); b = np.interp(np.log(LGT), np.log(SS3[k_]["lg"]), SS3[k_]["M"])
    ssb[k_] = dict(maxrel=float(np.max(np.abs(b / a - 1))), conv=float(SS3[k_]["last_err"]), slope_in_2x=float(SS3[k_]["slope_in"]),
                   lsp_2x=float(SS3[k_]["lsp"]))
ssb_ok = bool(ssb) and all(v["maxrel"] <= 0.05 for v in ssb.values())
ss_conv = bool(ssb) and all(v["conv"] <= 0.02 for v in ssb.values())
check("SSb", ssb_ok, "; ".join(f"eps {k_}: max|dM/M| {v['maxrel']:.3f} (2x conv {v['conv']:.4f}, slope(0.01-0.03) {v['slope_in_2x']:.3f})" for k_, v in ssb.items()),
      "<= 5 % on lambda in [0.02, 1] (A1: 2x tau_max)", "self-similar profile converged in tau_max")
PROVISIONAL = SS3 is None
TABLES = SS if (ssb_ok or PROVISIONAL) else SS3
RES["SSb"] = dict(per_eps=ssb, used="D6" if (ssb_ok or PROVISIONAL) else "re-solved 2x", provisional=PROVISIONAL, row3_computable=bool(ssb_ok or ss_conv or PROVISIONAL))

W_B = 0.0224; RHO_C100 = 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G); DTA = (3 * math.pi / 4) ** 2


def Mss(lmb, tab):
    lg, M = tab["lg"], tab["M"]; lmb = np.asarray(lmb, float)
    out = np.exp(np.interp(np.log(np.clip(lmb, lg[0], 1.0)), np.log(lg), np.log(M)))
    s0 = math.log(M[1] / M[0]) / math.log(lg[1] / lg[0])
    out = np.where(lmb < lg[0], M[0] * (np.maximum(lmb, 1e-30) / lg[0]) ** max(s0, 0.05), out)
    return np.where(lmb >= 1.0, 1.0, out)


def r_ta_of(Mb_kg, z):
    """catchment fixed point: M_ta = 6.364 M_b(< r_ta); r_ta from the EdS turnaround overdensity on the native mean density."""
    rhom = (1 + FC) * W_B * RHO_C100 * (1 + z) ** 3; Mta = (1 + FC) * Mb_kg[-1]
    for _ in range(60):
        rta = (3 * Mta / (4 * math.pi * DTA * rhom)) ** (1 / 3) / MPC
        Mta_new = (1 + FC) * float(np.interp(min(rta, RG[-1]), RG, Mb_kg))
        if abs(Mta_new / Mta - 1) < 1e-10: break
        Mta = Mta_new
    return rta, Mta


def model(cl, foot, hk, comp=None, tab=None, cold_mult=1.0):
    h = HV[hk]; a0 = A0[foot]; q = (float(DM(cl["z"], h)) / (1 + cl["z"])) / DA_lcdm(cl["z"])
    Mg500 = cl["Mgas500"] * q ** 2.5; R500 = cl["R500"] * q
    Mg, rho_g = gas(Mg500, R500, "G0"); Mst = 0.20 * Mg; Mb = Mg + Mst
    ex = {}
    if comp is None:
        g = g_aqual_sph(G * Mb / RM ** 2, a0)
    else:
        rta, Mta = r_ta_of(Mb, cl["z"]); shape = Mss(RG / rta, tab)
        supply = cold_mult * FC * Mta / (1 + FC)
        if comp == "U0":
            Mc = supply * shape; g = G * (Mb + Mc) / RM ** 2
        else:
            src = Mst if comp == "U1" else Mb
            gl = g_aqual_sph(G * src / RM ** 2, a0); Mph = gl * RM ** 2 / G - src
            Mph_ta = float(np.interp(rta, RG, Mph)); Mc = max(0.0, supply - Mph_ta) * shape
            g = gl + G * ((Mg if comp == "U1" else 0.0) + Mc) / RM ** 2
            ex["phantom_over_supply_at_rta"] = Mph_ta / supply
        ex.update(rta=rta, Mta=Mta / MSUN, Mcold_05=float(np.interp(0.5, RG, Mc)) / MSUN, Mb_05=float(np.interp(0.5, RG, Mb)) / MSUN)
    ML = g * RM ** 2 / G
    rho = np.gradient(ML, RM) / (4 * np.pi * RM ** 2)
    Sig = project_floor(rho); d = np.radians(cl["off_deg"]) * float(DM(cl["z"], h)) / (1 + cl["z"])
    So = offset_floor(Sig, d); Pm = at_bins(dsig_from_sig(So)) / KG_PC2
    return Pm, ex


def stack(foot, hk, **kw):
    Pm = np.empty((N, 8)); EX = []
    for i, cl in enumerate(CL):
        p, e = model(cl, foot, hk, **kw); Pm[i] = p; EX.append(e)
    return Pm, EX


def score(Pm, hk):
    d = DAT[hk]; out = {"ALL": jk(d["D"], Pm, d["W"])}
    for t, sel in TERC.items(): out[t] = jk(d["D"], Pm, d["W"], sel)
    return out


def passes(sc):
    return all(abs(sc[s][b][0] - 1) <= 2 * sc[s][b][1] for s in ("ALL", "T1", "T2", "T3") for b in ("MID", "OUTER"))


# X2a: the no-cold law reproduces X2's committed C0 terciles
X2J = json.load(open(SRC["x2json"]))["terciles"]["C0"]
LAWSC = {}; dx2 = 0.0
for f in FEET:
    for hk in HK:
        Pm, _ = stack(f, hk); sc = score(Pm, hk); LAWSC[f"{f}|{hk}"] = sc
        for t in ("T1", "T2", "T3"):
            for b in ("MID", "OUTER"):
                dx2 = max(dx2, abs(sc[t][b][0] - X2J[t]["boost"][f"{f}|{hk}"][b]["A"]))
        P(f"   law (no cold) {f:9s} {hk}: ALL MID {sc['ALL']['MID'][0]:.3f}+-{sc['ALL']['MID'][1]:.3f} OUT {sc['ALL']['OUTER'][0]:.3f} | "
          + " ".join(f"{t} {sc[t]['MID'][0]:.2f}/{sc[t]['OUTER'][0]:.2f}" for t in ("T1", "T2", "T3")))
check("X2a", dx2 <= 0.005, f"max |dA| {dx2:.2e}", "<= 0.005", "my cluster model (law on baryons) reproduces X2's committed C0 tercile table")
RES["rows"]["3_clusters_law_reference"] = LAWSC
R3 = {}
cm = 2.0 if MUT else 1.0                                           # M3: cold mass doubled (reported)
row3_ok = bool(ssb_ok or ss_conv or PROVISIONAL)
if row3_ok:
    for comp in ("U0", "U1", "U2"):
        for k_, tab in TABLES.items():
            for f in (("canonical",) if comp == "U0" else FEET):
                for hk in HK:
                    Pm, EX = stack(f, hk, comp=comp, tab=tab, cold_mult=cm); sc = score(Pm, hk)
                    key = f"{comp}|eps{k_}|{f}|{hk}"
                    meta = dict(rta_median=float(np.median([e["rta"] for e in EX])), Mcold05_median=float(np.median([e["Mcold_05"] for e in EX])),
                                Mb05_median=float(np.median([e["Mb_05"] for e in EX])))
                    if comp != "U0": meta["phantom_over_supply_median"] = float(np.median([e["phantom_over_supply_at_rta"] for e in EX]))
                    R3[key] = dict(score=sc, pass_cell=passes(sc), meta=meta)
                    P(f"   {key:28s}: ALL MID {sc['ALL']['MID'][0]:.3f}+-{sc['ALL']['MID'][1]:.3f} OUT {sc['ALL']['OUTER'][0]:.3f}+-{sc['ALL']['OUTER'][1]:.3f} | "
                      + " ".join(f"{t} {sc[t]['MID'][0]:.2f}+-{sc[t]['MID'][1]:.2f}/{sc[t]['OUTER'][0]:.2f}+-{sc[t]['OUTER'][1]:.2f}" for t in ("T1", "T2", "T3"))
                      + f" -> {'PASS' if R3[key]['pass_cell'] else 'fail'}  [r_ta {meta['rta_median']:.2f} Mpc, M_cold(<0.5) {meta['Mcold05_median']:.2e}"
                      + (f", phantom/supply at r_ta {meta['phantom_over_supply_median']:.2f}" if comp != "U0" else "") + "]")
                    if rss() > 0.95: P("RSS guard"); sys.exit(3)
    rcls = {}
    for comp in ("U0", "U1", "U2"):
        for f in (("canonical",) if comp == "U0" else FEET):
            per_eps = [all(R3[f"{comp}|eps{k_}|{f}|{hk}"]["pass_cell"] for hk in HK) for k_ in TABLES]
            rcls[f"{comp}|{f}"] = "EXPLAINS" if all(per_eps) else ("CONDITIONAL(eps)" if any(per_eps) else "FAILS")
    r3_class = {"EXPLAINS": "CONDITIONAL", "CONDITIONAL(eps)": "CONDITIONAL", "FAILS": "FAIL"}[rcls["U0|canonical"]]
else:
    rcls = {}; r3_class = "NOT COMPUTABLE"
RES["rows"]["3_clusters"] = dict(cells=R3, reading_class=rcls, cls=r3_class, cold_mult=cm,
                                 paper_own_test="CFG815: PAPER49's expelled-gas freeing rule FAILS on 318 eRASS1 (MID tercile 1.64, Z +4.6; P profile)")
P(f"   reading classes: {rcls}")
P(f"   ROW 3 class: {r3_class} (U0 = PAPER49 L52 literally; postulates U and C)")

# =====================================================================================================================
# ROW 6 (fit first) and ROW 4: SPARC
# =====================================================================================================================
P("\n=== ROW 6: SPARC RAR (rest state = n = 1 law; P4's loader and rule) ===")
TP4 = open(SRC["p4"]).read()
NS4 = {"np": np, "os": os, "math": math, "DATA": os.path.join(REPO, "real_research", "data")}
exec(cut(TP4, "KPC_S = 3.0857e19", "def chi2_offset("), NS4)
GALS = NS4["load_sparc_own"](); gal_arrays = NS4["gal_arrays"]; UPS = NS4["UPS"]; KPC_S = NS4["KPC_S"]


def nu_law(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    if MUT: return np.sqrt(0.5 + np.sqrt(0.25 + 1 / y ** 2))         # M4: standard mu = x/sqrt(1+x^2)
    return 0.5 + np.sqrt(0.25 + 1 / y)


P4J = json.load(open(SRC["p4json"]))["tiles"]["T1"]
R6 = {}; FITS = {}
for f in FEET:
    a0 = A0[f]; num = den = 0.0; Us = []; FITS[f] = {}; GN = np.zeros(len(UPS)); GD = np.zeros(len(UPS))
    for q in GALS:
        GB, GO, OK, Wt = gal_arrays(q, UPS)
        gb = np.where(OK, GB, 1.0)
        r = np.where(OK, np.log10(np.where(OK, GO, 1.0)) - np.log10(nu_law(gb / a0) * gb), 0.0)
        Wm = np.where(OK, Wt[:, None], 0.0)
        GN += (Wm * r * r).sum(0); GD += Wm.sum(0)
        mse = (Wm * r * r).sum(0) / np.maximum(Wm.sum(0), 1e-300); i = int(np.argmin(mse))
        num += (Wm[:, i] * r[:, i] ** 2).sum(); den += Wm[:, i].sum(); Us.append(UPS[i]); FITS[f][q["name"]] = float(UPS[i])
    jg = int(np.argmin(GN / GD)); best = (float(GN[jg] / GD[jg]), float(UPS[jg]))      # global Upsilon (CFG695 S2)
    R6[f] = dict(rms_perUps=math.sqrt(num / den), U_median=float(np.median(Us)), U_q=[float(v) for v in np.percentile(Us, [16, 84])],
                 rms_global=math.sqrt(best[0]), U_global=best[1], N=len(GALS))
    R6[f]["line"] = bool(R6[f]["rms_perUps"] <= 0.110 and 0.50 <= R6[f]["U_median"] <= 0.80)
    P(f"   [{f}] per-galaxy Upsilon: rms {R6[f]['rms_perUps']:.5f} dex, median Upsilon {R6[f]['U_median']:.2f} -> line {'PASS' if R6[f]['line'] else 'FAIL'}; "
      f"global Upsilon: rms {R6[f]['rms_global']:.5f} @ {R6[f]['U_global']:.2f}")
dP4 = max(abs(R6[f]["rms_perUps"] - P4J["footings"][f]["iso_perUps"]["rms"]) for f in FEET)
check("P4a", dP4 <= 2e-4 and len(GALS) == 175, f"max |d rms| {dP4:.1e} (N {len(GALS)})", "<= 2e-4", "P4's iso_perUps rms reproduced on both footings")
k5 = P4J["K5_reproduction"]
dk5 = max(abs(R6[f]["rms_global"] - k5[f]["rms"]) for f in FEET); uk5 = all(abs(R6[f]["U_global"] - k5[f]["U"]) < 1e-9 for f in FEET)
check("P4b", dk5 <= 1e-4 and uk5, f"max |d rms| {dk5:.1e}; Upsilon equal {uk5}", "<= 1e-4; equal", "CFG695 S2 (global Upsilon) reproduced")
r6_class = "CONDITIONAL" if any(R6[f]["line"] for f in FEET) else "FAIL"
RES["rows"]["6_sparc"] = dict(per_footing=R6, cls=r6_class,
                              chi2_line="P4: FAIL on both footings (63-64 % of galaxies at p >= 0.001 vs 90 %; family-generic)",
                              settling="POSTULATE S; CFG939 derived the law state by phase mixing for a spherical single medium only "
                                       "(44 % of infall mass ejected); no derivation for discs or with supply")
P(f"   ROW 6 class: {r6_class} (settling is a postulate; line per footing: {[R6[f]['line'] for f in FEET]})")

P("\n=== ROW 4: capacity in isolated galaxies (own supply 5.364 M_b; catchment multiplier reported) ===")
R4 = {}
for f in FEET:
    a0 = A0[f]; nfail = 0; npts = nfail_pts = 0; mults = []; mults_dat = []; nfail_dat = 0; rel_edge = []
    for q in GALS:
        U = FITS[f][q["name"]]; m = q["meta"]
        Mb = (U * m["L36"] + 1.33 * m["MHI"]) * 1e9
        GB, GO, OK, _ = gal_arrays(q, np.array([U])); ok = OK[:, 0]
        R = q["R"][ok] * KPC_S; gb = GB[ok, 0]; go = GO[ok, 0]
        if len(R) == 0: continue
        gl = nu_law(gb / a0) * gb
        Mph = (gl - gb) * R ** 2 / G / MSUN; Mdat = (go - gb) * R ** 2 / G / MSUN
        cap = FC * Mb
        mult = float(Mph.max() / cap); multd = float(max(Mdat.max(), 0) / cap)
        mults.append(mult); mults_dat.append(multd)
        nfail += mult > 1; nfail_dat += multd > 1; npts += len(R); nfail_pts += int((Mph > cap).sum())
        rM = math.sqrt(G * Mb * MSUN / a0) / KPC_S
        rel_edge.append(float(q["R"][ok][-1] / rM))
    ng = len(mults)
    R4[f] = dict(N=ng, f_gal=nfail / ng, f_pts=nfail_pts / npts, f_gal_data=nfail_dat / ng,
                 mult_q=[float(v) for v in np.percentile(mults, [50, 84, 95, 100])],
                 Rlast_over_rM_q=[float(v) for v in np.percentile(rel_edge, [50, 84, 95, 100])])
    R4[f]["own_class"] = "PASS" if R4[f]["f_gal"] <= 0.05 else ("FAIL" if R4[f]["f_gal"] > 0.20 else "CONDITIONAL")
    P(f"   [{f}] N {ng}: law phantom > 5.364 M_b in {nfail} galaxies (f_gal {R4[f]['f_gal']:.3f}; f_pts {R4[f]['f_pts']:.3f}); "
      f"data-side {nfail_dat} (f {R4[f]['f_gal_data']:.3f}); catchment multiplier needed (median/84/95/max) "
      + "/".join(f"{v:.2f}" for v in R4[f]["mult_q"]) + "; R_last/r_M (median/84/95/max) " + "/".join(f"{v:.1f}" for v in R4[f]["Rlast_over_rM_q"])
      + f" -> own reading {R4[f]['own_class']}")
own = [R4[f]["own_class"] for f in FEET]
own_cls = "FAIL" if "FAIL" in own else ("CONDITIONAL" if "CONDITIONAL" in own else "PASS")
r4_class = "PASS" if own_cls == "PASS" else "CONDITIONAL"
RES["rows"]["4_capacity"] = dict(per_footing=R4, own_reading_class=own_cls, cls=r4_class,
                                 lensing="CFG801: own-supply edge excluded by KiDS isolated-galaxy lensing (dchi2 +197 within 0.31 Mpc)",
                                 deep_edge="deep regime: M_ph(<r) ~ r sqrt(M_b a0/G), so own supply ends at r ~ 5.364 r_M (+ the Newtonian core)")
P(f"   ROW 4 class: {r4_class} (own reading {own_cls}; catchment = postulate C)")

# =====================================================================================================================
# ROW 5: saddle positivity (AG6C's script run as a read-only copy)
# =====================================================================================================================
P("\n=== ROW 5: saddle positivity (AG6C S0.4 run as a copy in a scratch directory) ===")
SCR = tempfile.mkdtemp(prefix="tm1_ag6c_copy_"); cp = os.path.join(SCR, "ag6c_s0_saddle.py"); shutil.copy(SRC["ag6c"], cp)
envr = dict(os.environ, OMP_NUM_THREADS="1")
pr_ = subprocess.run([sys.executable, cp], cwd=SCR, env=envr, capture_output=True, text=True, timeout=1200)
txt = open(os.path.join(SCR, "ag6c_s0_saddle.out")).read() if os.path.exists(os.path.join(SCR, "ag6c_s0_saddle.out")) else pr_.stdout
RES["ag6c_copy_exit"] = pr_.returncode
m02 = re.search(r"mid-plane C\(R = 0\.2\) : ([+-][0-9.]+) \(h\) vs ([+-][0-9.]+) \(h/2\)", txt)
C02 = (float(m02.group(1)), float(m02.group(2))) if m02 else (float("nan"), float("nan"))
check("AGa", m02 is not None and all(abs(c + 0.240) <= 0.01 for c in C02), f"C(0.2 d) = {C02[0]:+.5f} (h) / {C02[1]:+.5f} (h/2)", "-0.240 +- 0.01",
      "AG6C's mid-plane phantom density at R = 0.2 d reproduced")
rho_c = FC * W_B * RHO_C100
FID = dict(MW_M31=(8e10, 0.77), cluster_pair=(2e13, 5.0))
R5 = dict(rho_c_mean=rho_c, C02=C02, ratio={})
for nm, (M, d) in FID.items():
    for f in FEET:
        rph = C02[0] * math.sqrt(G * M * MSUN * A0[f]) / (G * (d * MPC) ** 2)
        R5["ratio"][f"{nm}|{f}"] = rph / rho_c
cols = re.findall(r"(F\d_[A-Za-z0-9_-]+)\s+(canonical|alt)\s*: min rho_ph = ([-0-9.e+]+) kg/m\^3 = ([-0-9.]+) rhobar_c; mid-plane negative column \(AQUAL\) ([-0-9.]+) Msun/pc\^2, unsuppliable by a rho>=0 medium ([-0-9.]+)", txt)
R5["fiducials_AG6C"] = [dict(pair=c[0], footing=c[1], min_ratio=float(c[3]), neg_column=float(c[4]), unsuppliable=float(c[5])) for c in cols]
check("AGb", abs(R5["ratio"]["MW_M31|canonical"] + 89) <= 5 and abs(R5["ratio"]["cluster_pair|canonical"] + 33) <= 2,
      f"MW-M31 {R5['ratio']['MW_M31|canonical']:.1f}, cluster {R5['ratio']['cluster_pair|canonical']:.1f} (alt {R5['ratio']['MW_M31|alt']:.1f} / {R5['ratio']['cluster_pair|alt']:.1f})",
      "-89 +- 5 / -33 +- 2 (canonical)", "PAPER49's -89x / -33x mean cold density at R = 0.2 d")
R5["stiffness_bound_L1kpc"] = {nm: (1.0 / (0.05 * d * 1e3)) ** 2 for nm, (M, d) in FID.items()}
for c in R5["fiducials_AG6C"]:
    P(f"   {c['pair']:18s} {c['footing']:9s}: min rho_ph {c['min_ratio']:.1f} rhobar_c; AQUAL negative column {c['neg_column']:.2f}, unsuppliable {c['unsuppliable']:.2f} Msun/pc^2")
P(f"   stiffness cannot fill the pancake: (L*/0.05d)^2 at L* = 1 kpc = {R5['stiffness_bound_L1kpc']['MW_M31']:.1e} (MW-M31), {R5['stiffness_bound_L1kpc']['cluster_pair']:.1e} (cluster)")
R5["observability"] = "AG7: Epps & Hudson 2017 pairs give box S/N 0.30, optimal strip 0.87 (canonical primary); 3 sigma needs ~2.7e5 pairs (x12). NOT TESTABLE NOW."
R5["cls"] = "FAIL" if min(R5["ratio"].values()) < -1 else "PASS"
RES["rows"]["5_saddle"] = R5
P(f"   ROW 5 class: {R5['cls']} (rho_bar + div P < 0 by {-min(R5['ratio'].values()):.0f}x at the worst fiducial; the law must fail in the saddle band)")

# =====================================================================================================================
# summary
# =====================================================================================================================
P("\n=== SUMMARY ===")
CL_ = {"1 growth on FRW": r1_class, "2 satellites": RES["rows"]["2_satellites"]["cls"], "3 cluster cores (U0)": r3_class,
       "4 capacity": r4_class, "5 saddle positivity": R5["cls"], "6 SPARC RAR": r6_class}
for k_, v in CL_.items(): P(f"   {k_:24s}: {v}")
resolves = (r1_class == "PASS" and RES["rows"]["2_satellites"]["cls"] == "PASS" and r6_class != "FAIL")
RES["summary"] = dict(classes=CL_, resolves_law_vs_clumping=resolves,
                      postulates=["T tether only to condensed baryons at low speed", "C catchment supply", "S settling / rest state reached",
                                  "U untethered collisionless cold energy in hot-gas systems", "self-similar infall initial condition (row 3)"],
                      fitted=["kappa = 1/2", "L* (bounded 24 pc - ~1 kpc)", "Omega_c/Omega_b = 5.364 (measured)"])
P(f"   resolves the law-versus-clumping split: {resolves}")
nfail = sum(not c["ok"] for c in CHECKS.values())
P(f"\nchecks: {len(CHECKS) - nfail}/{len(CHECKS)} PASS; run time {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
RES.update(runtime_s=time.time() - T0, peak_rss_GB=rss())
open(os.path.join(HERE, f"tm1_tethered_medium{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
json.dump(RES, open(os.path.join(HERE, f"tm1_tethered_medium_results{TAG}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
sys.exit(0 if nfail == 0 else 1)
