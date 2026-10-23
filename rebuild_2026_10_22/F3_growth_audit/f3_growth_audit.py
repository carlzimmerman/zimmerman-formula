#!/usr/bin/env python3
"""F3_growth_audit (FROZEN_CRITERIA.md, committed alone first): the growth / cosmic-shear failures (CFG555/556/596) and the
growth no-go, re-audited against the covariant screened theory (THEORY_V3_DRAFT: BS Khronon + J_x + K(Q) dust).

  OMP_NUM_THREADS=1 nice -n 15 python3 f3_growth_audit.py              -> f3_growth_audit.out, f3_growth_audit_results.json
  F3_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 f3_growth_audit.py  -> *_MUTATE.out / *_MUTATE.json (exit 1 = teeth bite)

No PM simulation. KiDS likelihood = the CFG592 library part, exec'd unchanged (as CFG596 does). Linear P(k) = vanilla CLASS
(the dust limit). kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys, json, math, glob, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("F3_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
OUT, RES, CHK = [], {"lane": "F3_growth_audit", "date": "2026-10-22", "mutate": MUT}, {}
T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")

# ------------------------------------------------------------------ the record's KiDS likelihood (CFG592 library, unchanged)
SRC = os.path.join(CFG, "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
SURV, Pmat, fit, support_mask, subset, nuis_spec = G["SURV"], G["Pmat"], G["fit"], G["support_mask"], G["subset"], G["nuis_spec"]
LN, ZG, BG = G["LN"], G["ZG"], G["BG"]
KIDS = SURV["KiDS"]
from scipy.stats import chi2 as CH
P("F3_growth_audit" + (" [MUTATE]" if MUT else "") + ": kappa = 1/2 FITTED; footings never pooled; no PM run; CLASS dust limit; CFG592 KiDS library unchanged")

# ------------------------------------------------------------------ K0: reproduce CFG596 canonical (P0 S0, P1 RES) on KiDS
W596 = os.path.join(G["EXT"], "cfg596_work")
def load596(job): return json.load(open(glob.glob(os.path.join(W596, job, "cfg596_*.json"))[0]))
F, S = load596("P1"), load596("P0")
ZK = {0.0: "z0", 0.5: "z0.5", 1.0: "z1"}
k596 = np.array(F["snap"]["z0"]["k"]); N596, L596 = int(F["np"]), float(F["L"])
run596 = dict(k=k596, k_lo=float(k596[0]), k_hi=float(math.pi * N596 / (4 * L596)), B=np.ones_like(k596),
              nodes={z: ((np.array(F["snap"][key]["P"]) if MUT else np.array(F["snap"][key]["P_grav"])),
                         np.array(S["snap"][key]["P"])) for z, key in ZK.items()})
PS0 = Pmat(run596, "S0"); PF = Pmat(run596, "F")
f_sup = support_mask(KIDS, run596, PS0); D596 = subset(KIDS, KIDS["pubkeep"] & (f_sup >= 0.9))
s0, fF = fit(KIDS, D596, PS0), fit(KIDS, D596, PF)
ref = json.load(open(os.path.join(CFG, "CFG596_lean_pm_1024", "cfg596_native_results.json")))["runs"]["L100_N1024_canonical"]["surveys"]["KiDS"]
r0 = (ref["fits"]["IA"]["S0"]["chi2"], ref["fits"]["IA"]["F"]["chi2"], ref["dchi2"])
m0 = (s0["chi2"], fF["chi2"], fF["chi2"] - s0["chi2"])
dev0 = max(abs(a - b) for a, b in zip(m0, r0))
pS0 = float(CH.sf(s0["chi2_data"], D596["N"]))
RES["K0"] = dict(N_kept=D596["N"], chi2_S0=m0[0], chi2_F=m0[1], dchi2=m0[2], record=r0, max_dev=dev0, p_S0=pS0,
                 B_at={str(kk): float(np.interp(math.log(kk), np.log(k596), np.array(F["snap"]["z0"]["P_grav"]) / np.array(F["snap"]["z0"]["P"])))
                       for kk in (0.3, 0.5, 1.0, 2.0)})
check("K0", dev0 <= 0.05, f"S0 {m0[0]:.2f} F {m0[1]:.2f} dchi2 {m0[2]:+.2f} (N {D596['N']}; record {r0[0]:.2f}/{r0[1]:.2f}/{r0[2]:+.2f}; max|dev| {dev0:.2e})", "max|dev|<=0.05")

# ------------------------------------------------------------------ K1: symbolic identities
import sympy as sp
Y, a0s, Q, mu = sp.symbols("Y a_0 Q mu", positive=True)
y = sp.sqrt(Y) / a0s
J = (sp.Rational(2, 3) * Y ** sp.Rational(3, 2) / a0s) if MUT else (-2 * a0s ** 2 * (y - sp.log(1 + y)))   # MUTATE: AeST-like J ~ Y^{3/2}
Jp0 = sp.limit(sp.diff(J, Y), Y, 0, "+")
one_plus = sp.simplify(1 + sp.diff(J, Y))
K1i = (Jp0 == -1)
K = mu ** 2 * (Q - 1) ** 2
rho8 = Q * sp.diff(K, Q) - K                         # 8 pi G rho / c^4
cs2 = sp.diff(K, Q) / (Q * sp.diff(K, Q, 2))
kJ2 = sp.simplify((rho8 / 2) / cs2)                   # 4 pi G rho / c_s^2 (c = 1)
K1ii_orig = sp.simplify(kJ2 - mu ** 2 * Q ** 2) == 0 and sp.simplify(cs2 - (Q - 1) / Q) == 0
# AMENDMENT A1 (post-result, FROZEN_CRITERIA.md): the frozen identity k_J^2 = mu^2 Q^2 was an algebra slip (it used rho ~ Q K').
# The exact identity is k_J^2 = mu^2 Q(Q+1)/2, which -> mu^2 as Q_bar -> 1 (dust limit). The frozen line is kept and printed as K1-orig.
K1ii = (sp.simplify(kJ2 - mu ** 2 * Q * (Q + 1) / 2) == 0 and sp.simplify(cs2 - (Q - 1) / Q) == 0
        and sp.limit(kJ2, Q, 1) == mu ** 2)
RES["K1"] = dict(Jprime_at_0=str(Jp0), one_plus_Jprime=str(one_plus), cs2=str(sp.simplify(cs2)), kJ2=str(kJ2),
                 K1_orig_pass=bool(K1i and K1ii_orig),
                 meaning="(i) 1 + J_x'(0) = 0: on FRW (Y = 0) the lapse-gradient (Newtonian) coefficient vanishes, so v3's linear "
                         "growth is GR's only where the K(Q) dust term dominates (k < a mu_K); C2's gamma = 0.555 is AeST's (J ~ Y^3/2, J'(0) = 0). "
                         "(ii) the BS dust Jeans wavenumber equals the static mass to O(Q_bar - 1): k_J^2 = mu_K^2 Q(Q+1)/2 (physical), comoving ~ a mu_K.")
P(f"K1-orig {'PASS' if (K1i and K1ii_orig) else 'FAIL'} k_J^2 = {kJ2} (frozen: == mu^2 Q^2 exactly; superseded by AMENDMENT A1, post-result)")
check("K1", bool(K1i and K1ii), f"J'(0) = {Jp0}; 1+J' = {one_plus}; c_s^2 = {sp.simplify(cs2)}; k_J^2 = {kJ2} -> mu^2 at Q=1",
      "J'(0) == -1 and k_J^2 == mu^2 Q(Q+1)/2 exactly (A1)")

# ------------------------------------------------------------------ growth solvers
from scipy.integrate import solve_ivp, quad
def make_E(Om, h, rad=True):
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL)), Or
def f_growth_gr(Om):
    """C2 K7 analogue: GR linear growth on flat dust + Lambda, f(z = 0)."""
    E2 = lambda a: Om * a ** -3 + 1 - Om
    def rhs(x, s):
        a = math.exp(x); dlnE = -1.5 * Om * a ** -3 / E2(a)
        return [s[1], -(2 + dlnE) * s[1] + 1.5 * Om * a ** -3 / E2(a) * s[0]]
    a_i = 1e-3; sol = solve_ivp(rhs, [math.log(a_i), 0.0], [a_i, a_i], rtol=1e-10, atol=1e-14)
    return sol.y[1, -1] / sol.y[0, -1]

def growth_ratio(kk, mu_h, Om, Ob, h, kernel="jeans", a_i=1e-3, rad=True):
    """two-fluid sub-horizon growth (baryons Newtonian at every k; BS dust kernel s(x), x = k/(a mu)); returns
    delta_m(k, a = 1) / delta_m(mu -> inf).  Vectorised over kk (h/Mpc)."""
    Ek, Or = make_E(Om, h, rad); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)
    def s_of(a, mu):
        if mu is None: return np.ones(n)
        x2 = (kk / (a * mu)) ** 2
        return (1.0 - x2) if kernel == "jeans" else 1.0 / (1.0 + x2)
    def solve(mu):
        def rhs(x, st):
            a = math.exp(x); E = Ek(a); eps = 1e-6
            dlnE = (math.log(Ek(a * math.exp(eps))) - math.log(Ek(a * math.exp(-eps)))) / (2 * eps)
            dens = 1.5 * a ** -3 / E ** 2
            db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
            src_b = dens * (Ob * db + OK * dk); src_k = dens * (Ob * db + OK * dk * s_of(a, mu))
            return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE) * gk + src_k])
        st0 = np.concatenate([np.full(n, a_i), np.full(n, a_i), np.full(n, a_i), np.full(n, a_i)])
        sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12)
        y_ = sol.y[:, -1]; return (Ob * y_[:n] + OK * y_[2 * n:3 * n]) / Om
    return solve(mu_h) / solve(None)

# ------------------------------------------------------------------ K0b: reproduce BSK2 (its cosmology, a_i = 1e-4, BSK2 kernel)
bsk = json.load(open(os.path.join(REPO, "real_research", "bs_khronon_2026", "BSK2_frw_dust_results.json")))
def find_num(d, keys):
    out = {}
    def walk(x, p=""):
        if isinstance(x, dict):
            for k_, v in x.items(): walk(v, p + "." + k_)
        elif isinstance(x, (int, float)) and any(t in p.lower() for t in keys): out[p] = x
    walk(d); return out
bsk_nums = find_num(bsk, ("ratio", "floor", "mu"))
RES["K0b_BSK2_record_numbers"] = bsk_nums

# sigma8 machinery on an EH-free CLASS P(k) (set below); for BSK2 reproduction BSK2's own power-law x EH is not on disk,
# so the ratio is taken on CLASS P(k) at BSK2's densities (shape difference stated).
from classy import Class
def class_run(wb, wc, h, lnA, ns, tau=0.0544, zs=(0.0,)):
    c = Class(); c.set({"omega_b": wb, "omega_cdm": wc, "h": h, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau, "N_ur": 3.044,
                        "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0})
    c.compute(); return c
KS = np.geomspace(1e-4, 50.0, 1500)
def pk0(c, h):   # (Mpc/h)^3 at k in h/Mpc, z = 0, linear
    return np.array([c.pk_lin(k * h, 0.0) for k in KS]) * h ** 3
W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
def sig8(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(np.trapz(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))
KT = np.geomspace(1e-3, 3.0, 36)
def sig8_ratio(Pk, mu_h, Om, Ob, h, kernel, a_i):
    T = growth_ratio(KT, mu_h, Om, Ob, h, kernel, a_i)
    Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8(Pk, Tf) / sig8(Pk), T

hB = 0.674; ObB, OmB = 0.049, 0.316
cB = class_run(ObB * hB ** 2, (OmB - ObB) * hB ** 2, hB, 3.044, 0.965); PkB = pk0(cB, hB)
EV = 5.067730469559e6; mu_bs24 = EV * 1e-31 * 3.08568e22 / hB
rB24, _ = sig8_ratio(PkB, mu_bs24, OmB, ObB, hB, "bsk2", 1e-4)
rB_floor, _ = sig8_ratio(PkB, 1.1e3, OmB, ObB, hB, "bsk2", 1e-4)
RES["K0b"] = dict(ratio_bs24=rB24, ratio_at_floor_1100=rB_floor, mu_bs24_hMpc=mu_bs24)
okb = abs(rB24 / 0.037 - 1) <= 0.10 and abs(rB_floor - 0.80) <= 0.08
check("K0b", okb, f"BS24 mu {mu_bs24:.4f} h/Mpc: ratio {rB24:.4f} (BSK2 0.037); mu 1.1e3: ratio {rB_floor:.3f} (BSK2 gate edge 0.80)", "|r/0.037-1|<=0.10 and |r(1.1e3)-0.80|<=0.08")

# ------------------------------------------------------------------ K0c + K2: dust-limit linear predictions
c2b = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb_results.json")))["P5"]["lcdm_refit"]
wbA, wcA, thA, lnAA, nsA, tauA = c2b["params"]; hA = c2b["chi2"]["H0"] / 100.0
c2r = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2_aest_cosmology_results.json")))
OM886, H886 = 0.2976015949416498, 0.6856426703851345      # C2 c2_aest_cosmology.py L115 (E-886)
fK7 = f_growth_gr(OM886); fK7_rec = c2r["K7"]["f0"]
MODELS = {}
for tag, (wb, wc, h, lnA, ns, tau) in {"A_c2b_refit": (wbA, wcA, hA, lnAA, nsA, tauA),
                                       "B_cfg886_bg": (wbA, OM886 * H886 ** 2 - wbA, H886, lnAA, nsA, tauA)}.items():
    c = class_run(wb, wc, h, lnA, ns, tau); Om = (wb + wc) / h ** 2
    Pk = pk0(c, h); s8_own = sig8(Pk); s8_cl = c.sigma8()
    fz0 = c.scale_independent_growth_factor_f(0.0)
    Dz = np.array([c.scale_independent_growth_factor(z) for z in ZG]) / c.scale_independent_growth_factor(0.0)
    MODELS[tag] = dict(c=c, h=h, Om=Om, Ob=wb / h ** 2, Pk=Pk, Dz=Dz, s8=s8_cl, s8_own=s8_own, S8=s8_cl * math.sqrt(Om / 0.3), f0=fz0,
                       par=dict(omega_b=wb, omega_cdm=wc, h=h, lnAs=lnA, n_s=ns, tau=tau))
fB_class = MODELS["B_cfg886_bg"]["f0"]
okc = abs(fK7 - fK7_rec) <= 1e-3 and abs(fB_class / fK7 - 1) <= 0.01
RES["K0c"] = dict(f0_this=fK7, f0_C2K7=fK7_rec, f0_CLASS_B=fB_class)
check("K0c", okc, f"f(0) GR solver {fK7:.4f} vs C2 K7 {fK7_rec:.4f}; CLASS (B, with radiation/baryons) {fB_class:.4f}", "|df|<=1e-3 and CLASS within 1%")
s8_PM = 0.811; S8_PM = s8_PM * math.sqrt(G["Om"] / 0.3)
RES["K2"] = {t: dict(params=m["par"], Om=m["Om"], sigma8=m["s8"], S8=m["S8"], sigma8_own_integral=m["s8_own"], f0=m["f0"]) for t, m in MODELS.items()}
RES["K2"]["C_PM_IC"] = dict(sigma8=s8_PM, Om=G["Om"], S8=S8_PM, note="engine EH IC normalisation (Planck-2018 LCDM), reference only")
ok2 = all(abs(m["s8_own"] / m["s8"] - 1) <= 1e-3 for m in MODELS.values())
check("K2", ok2, "; ".join(f"{t}: sigma8 {m['s8']:.4f}, Om {m['Om']:.4f}, S8 {m['S8']:.4f}" for t, m in MODELS.items()) + f"; PM IC S8 {S8_PM:.4f}", "own sigma8 integral vs CLASS <= 1e-3")

# ------------------------------------------------------------------ K3: linear model vs raw KiDS xi+- on linear-dominated points
def lin_Pmat(m, bg):
    chi = BG[bg][0]; KK = (LN[:, None] + 0.5) / chi[None, :]
    P0 = np.exp(np.interp(np.log(np.clip(KK, KS[0], KS[-1])), np.log(KS), np.log(m["Pk"])))
    return P0 * (m["Dz"][None, :] ** 2)
K3 = {}
OM_LIB, DZG_LIB = G["Om"], G["DZG"].copy()
for tag, m in MODELS.items():
    bg = "NAT_" + tag; BG[bg] = G["background"](m["Om"])
    G["Om"] = m["Om"]; G["DZG"] = m["Dz"]                     # projection prefactor + IA growth on the model's own background
    Pm = lin_Pmat(m, bg)
    K3[tag] = {}
    for klin in (0.2, 0.3):
        runL = dict(k_lo=1e-5, k_hi=klin)
        f_l = support_mask(KIDS, runL, Pm, bg=bg); D = subset(KIDS, KIDS["pubkeep"] & (f_l >= 0.9))
        if D["N"] < 10:
            K3[tag][str(klin)] = dict(N_kept=D["N"], cls="NOT DIAGNOSTIC"); continue
        base = fit(KIDS, D, Pm, bg=bg); pval = float(CH.sf(base["chi2_data"], D["N"]))
        # amplitude measurement: chi2_min(A) on a grid, parabola around the minimum (not a model knob)
        AG_ = np.linspace(0.3, 1.7, 15); c2 = np.array([fit(KIDS, D, Pm * A, bg=bg)["chi2"] for A in AG_])
        i = int(np.argmin(c2)); i = min(max(i, 1), len(AG_) - 2)
        fine = np.linspace(AG_[i - 1], AG_[i + 1], 9); c2f = np.array([fit(KIDS, D, Pm * A, bg=bg)["chi2"] for A in fine])
        pc = np.polyfit(fine, c2f, 2); Ahat = -pc[1] / (2 * pc[0]); sA = 1 / math.sqrt(pc[0]) if pc[0] > 0 else float("inf")
        c2hat = float(np.polyval(pc, Ahat))
        cls = "NOT DIAGNOSTIC" if sA > 0.3 else ("TENSION" if abs(Ahat - 1) > 2 * sA else "CONSISTENT")
        K3[tag][str(klin)] = dict(N_kept=D["N"], chi2_min=base["chi2"], chi2_data=base["chi2_data"], p=pval, A_IA=base["A_IA"],
                                  A_hat=Ahat, sigma_A=sA, chi2_at_A_hat=c2hat, dchi2_pred_vs_Ahat=base["chi2"] - c2hat,
                                  S8_pred=m["S8"], S8_data_lin=m["S8"] * math.sqrt(max(Ahat, 0)), S8_data_sigma=m["S8"] * sA / (2 * math.sqrt(max(Ahat, 1e-9))),
                                  cls=cls, A_grid=list(map(float, AG_)), chi2_grid=list(map(float, c2)))
        P(f"  K3 {tag} k_lin {klin}: N_kept {D['N']}, chi2_min {base['chi2']:.2f} (data p {pval:.3f}), A_hat {Ahat:.3f} +- {sA:.3f} "
          f"-> S8_data(lin) {m['S8'] * math.sqrt(max(Ahat, 0)):.3f} vs S8_pred {m['S8']:.3f}; class {cls}")
G["Om"], G["DZG"] = OM_LIB, DZG_LIB
RES["K3"] = K3
check("K3", all(v.get("N_kept", 0) >= 0 for d in K3.values() for v in d.values()),
      "; ".join(f"{t}@{k}: {v['cls']}" for t, d in K3.items() for k, v in d.items()), "computed (class is a result)")

# ------------------------------------------------------------------ K4: BS dust at finite mu_K on background A
mA = MODELS["A_c2b_refit"]; hA_ = mA["h"]
mu_100kpc = 10.0 / hA_                    # mu^-1 = 100 kpc physical today -> 10 /Mpc -> h/Mpc
K4 = {}
for lab, mu_h in (("BS24_Eq39_edge_100kpc", mu_100kpc), ("BSK2_floor_1100", 1.1e3), ("BS24_scale", mu_bs24)):
    K4[lab] = dict(mu_hMpc=mu_h)
    for kern in ("jeans", "bsk2"):
        for a_i in (1e-3, 1e-4):
            if kern == "jeans" and (3.0 / (a_i * mu_h)) > 3000:
                K4[lab][f"{kern}_ai{a_i:g}"] = None; continue      # too many Jeans oscillations to integrate; BSK2 kernel reported instead
            r_, T_ = sig8_ratio(mA["Pk"], mu_h, mA["Om"], mA["Ob"], hA_, kern, a_i)
            K4[lab][f"{kern}_ai{a_i:g}"] = dict(sigma8_ratio=r_, sigma8=r_ * mA["s8"], T_at_k={str(round(k_, 3)): float(t_) for k_, t_ in zip(KT[::5], T_[::5])})
    P(f"  K4 {lab} (mu {mu_h:.4g} h/Mpc): " + "; ".join(f"{k_} {v['sigma8_ratio']:.4f}" for k_, v in K4[lab].items() if isinstance(v, dict)))
rinf, _ = sig8_ratio(mA["Pk"], 1e9, mA["Om"], mA["Ob"], hA_, "bsk2", 1e-3)
RES["K4"] = K4; RES["K4"]["mu_inf_ratio"] = rinf
check("K4", abs(rinf - 1) <= 1e-4, f"mu->inf ratio {rinf:.6f}", "|r-1|<=1e-4")

# ------------------------------------------------------------------ K5: the mu_K window
from scipy.optimize import brentq
def mu_min(kern, a_i, target=0.95):
    g = lambda lm: sig8_ratio(mA["Pk"], 10 ** lm, mA["Om"], mA["Ob"], hA_, kern, a_i)[0] - target
    return 10 ** brentq(g, 1.5, 6.0, xtol=1e-3)
MU = {"jeans_ai0.001": mu_min("jeans", 1e-3), "bsk2_ai0.001": mu_min("bsk2", 1e-3), "bsk2_ai0.0001": mu_min("bsk2", 1e-4)}
mu_max = mu_100kpc
win = {k_: dict(mu_min_hMpc=v, inv_mu_min_kpc_phys=1e3 / (v * hA_), gap_factor=v / mu_max, window_empty=bool(v > mu_max)) for k_, v in MU.items()}
RES["K5"] = dict(mu_max_hMpc_BS24_Eq39=mu_max, windows=win)
check("K5", True, "; ".join(f"{k_}: mu_min {v['mu_min_hMpc']:.0f} h/Mpc (1/mu {v['inv_mu_min_kpc_phys']:.2f} kpc) = {v['gap_factor']:.0f}x mu_max {mu_max:.1f}" for k_, v in win.items()), "computed")

# ------------------------------------------------------------------ K6: the EFE price (1D AQUAL, mu = x/(1+x), a0 units)
gN_in, g_ext = 0.01, 0.11
g_iso = (gN_in + math.sqrt(gN_in ** 2 + 4 * gN_in)) / 2; boost_iso = g_iso / gN_in
boost_efe = (1 + g_ext) ** 2 / (g_ext * (2 + g_ext))
ratio6 = boost_efe / boost_iso
RES["K6"] = dict(gN_in=gN_in, g_ext=g_ext, boost_isolated=boost_iso, boost_in_field=boost_efe, ratio=ratio6, dex=math.log10(ratio6),
                 note="1D (along-field) AQUAL; 3D direction-averaged values differ by O(1) factors; the point is existence and sign")
check("K6", abs(ratio6 - 1) > 0.10, f"boost isolated {boost_iso:.2f}, in g_ext {g_ext} a0: {boost_efe:.2f}; ratio {ratio6:.3f} ({math.log10(ratio6):+.2f} dex)", "|ratio-1|>0.10")

# ------------------------------------------------------------------ CFG555 decomposition (read only, for verdict (a))
src = json.load(open(os.path.join(CFG, "CFG555_growth_on_gravitating_field", "cfg555_srccheck.json")))["425_R3_can_512"]
RES["CFG555_decomposition_R3_512"] = dict(k=src["k_at_max"], r_grav=src["r_grav"], r_part=src["r_part"], Psrc=src["Psrc_over_PS0"],
                                          twoPcross=src["twoPcross_over_PS0"],
                                          source_carried_share_of_excess=(src["Psrc_over_PS0"] + src["twoPcross_over_PS0"]) / (src["r_grav"] - 1))
P(f"  CFG555 R3 512^3 at k {src['k_at_max']:.3f}: r_grav {src['r_grav']:.3f} = particles {src['r_part']:.3f} + source auto {src['Psrc_over_PS0']:.3f} + cross {src['twoPcross_over_PS0']:.3f}; "
  f"source-carried share of the excess {RES['CFG555_decomposition_R3_512']['source_carried_share_of_excess']:.2f}")

# ------------------------------------------------------------------ close
for m in MODELS.values(): m["c"].struct_cleanup(); m["c"].empty()
npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
import resource
RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
P(f"F3_GROWTH_AUDIT COMPLETE: {npass}/{ntot} checks PASS.  ({RES['runtime_s']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB)")
def clean(x):
    if isinstance(x, dict): return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.floating, np.integer)): return x.item()
    if isinstance(x, np.bool_): return bool(x)
    return x
json.dump(clean(RES), open(os.path.join(HERE, f"f3_growth_audit_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"f3_growth_audit{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)
