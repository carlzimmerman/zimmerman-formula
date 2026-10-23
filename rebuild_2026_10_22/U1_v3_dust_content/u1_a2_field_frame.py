#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
U1 AMENDMENT A2: the field-galaxy frame.  Does v3 keep the held phantom (and so the RAR) for isolated field galaxies?
Criteria: FROZEN_CRITERIA.md, AMENDMENT A2 (616ad70e96).  kappa = 1/2 FITTED; footings never pooled.

Run (repository root):  OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/U1_v3_dust_content/u1_a2_field_frame.py
Mutate:                 U1_MUTATE=1 ...  (the hold kernel is removed: dust feels its full own gravity, s == 1; F1 and F2 must FAIL)
"""
import os, sys, json, math, time, csv, glob, resource, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1")
if sys.platform == "darwin" and os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, MallocMediumZone="0"))
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
warnings.filterwarnings("ignore", category=RuntimeWarning)

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
MUT = os.environ.get("U1_MUTATE", "0") == "1"
SFX = "_MUTATE" if MUT else ""
OUT, CHK = [], {}
RES = dict(lane="U1_v3_dust_content/A2_field_frame", mutate=MUT, amendment="616ad70e96", numbers={})


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, val, thr, note=""):
    CHK[name] = dict(ok=bool(ok), value=str(val), threshold=str(thr), note=note)
    P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}  {note}")


A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
KPC = 3.0857e19
P("=" * 116)
P("U1 A2: the field-galaxy frame (held phantom vs relative velocity to the local khronon flow)" + ("   *** MUTATE: no hold kernel ***" if MUT else ""))
P("=" * 116)

# ------------------------------------------------------------------------------------------------ F1 (sympy)
P("\n--- F1: linear baryon-dust differential acceleration on FRW ---")
k, a, mu, G4 = sp.symbols("k a mu fourpiG", positive=True)
drt, drb = sp.symbols("drho_tau drho_b", real=True)
Xi_k = -G4 * a ** 2 * drt / (k ** 2 + a ** 2 * mu ** 2)                 # (lap - a^2 mu^2) Xi = 4piG a^2 drho_tau
if MUT:
    Xi_k = sp.Integer(0)                                                # mutate: no hold, dust feels its whole own potential
Phi_tau = -G4 * a ** 2 * drt / k ** 2
Phi = -G4 * a ** 2 * (drb + drt) / k ** 2
acc_b = Phi                                                             # baryons feel Phi
acc_t = Phi - Xi_k                                                      # dust feels psi
diff_ = sp.simplify(acc_b - acc_t)
s_ = k ** 2 / (k ** 2 + a ** 2 * mu ** 2)
f1a = sp.simplify(diff_ - s_ * Phi_tau)
lim_hi = sp.limit(sp.simplify(diff_ / Phi_tau), k, sp.oo)
lead_lo = sp.simplify(sp.series(sp.simplify(diff_ / Phi_tau), k, 0, 3).removeO())
ok_f1 = f1a == 0 and lim_hi == 1 and sp.simplify(lead_lo - k ** 2 / (a ** 2 * mu ** 2)) == 0
check("F1", ok_f1, f"(acc_b - acc_dust) - s*Phi_tau = {f1a}; k>>a mu: ratio -> {lim_hi}; k<<a mu: ratio ~ {lead_lo}", "0; 1; k^2/(a mu)^2",
      "differential acceleration = s grad(Phi_tau): full on k >> a muK, suppressed (k/a muK)^2 on k << a muK (co-flow)")

# ------------------------------------------------------------------------------------------------ F2 (linear relative velocity)
P("\n--- F2: linear rms baryon-dust relative velocity at z = 0 (v3 two-fluid, J_x/BSK2 kernel) ---")
from classy import Class


def make_E(Om, h, rad=True):
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda aa: math.sqrt(Om * aa ** -3 + Or * aa ** -4 + OL)), Or


def two_fluid(kk, mu_h, Om, Ob, h, a_i=1e-3):
    """F3's two-fluid sub-horizon ODE (copy); returns (db, db', dt, dt') at a = 1, ' = d/dln a.  mu_h None -> s = 1."""
    Ek, _ = make_E(Om, h, True); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)

    def s_of(aa):
        if mu_h is None or MUT:
            return np.ones(n)
        x2 = (kk / (aa * mu_h)) ** 2
        return 1.0 / (1.0 + x2)

    def rhs(x, st):
        aa = math.exp(x); E = Ek(aa); eps = 1e-6
        dlnE = (math.log(Ek(aa * math.exp(eps))) - math.log(Ek(aa * math.exp(-eps)))) / (2 * eps)
        dens = 1.5 * aa ** -3 / E ** 2
        db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
        src_b = dens * (Ob * db + OK * dk); src_k = dens * (Ob * db + OK * dk * s_of(aa))
        return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE) * gk + src_k])
    st0 = np.concatenate([np.full(n, a_i)] * 4)
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12)
    y_ = sol.y[:, -1]
    return y_[:n], y_[n:2 * n], y_[2 * n:3 * n], y_[3 * n:]


def class_pk(wb, wc, h, lnA, ns, tau):
    c = Class(); c.set({"omega_b": wb, "omega_cdm": wc, "h": h, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau, "N_ur": 3.044,
                        "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0})
    c.compute()
    KS = np.geomspace(1e-4, 50.0, 1500)
    Pk = np.array([c.pk_lin(kv * h, 0.0) for kv in KS]) * h ** 3
    s8 = c.sigma8(); c.struct_cleanup(); c.empty()
    return KS, Pk, s8


W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
F3R = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json")))
pA = F3R["K2"]["A_c2b_refit"]["params"]; pB = F3R["K2"]["B_cfg886_bg"]["params"]
# reproduce F3 K4 bsk2_ai0.001 on background A
KSA, PkA, _ = class_pk(pA["omega_b"], pA["omega_cdm"], pA["h"], pA["lnAs"], pA["n_s"], pA["tau"])
OmA = (pA["omega_b"] + pA["omega_cdm"]) / pA["h"] ** 2; ObA = pA["omega_b"] / pA["h"] ** 2
KT = np.geomspace(1e-3, 3.0, 36)
mu_ref = F3R["K4"]["BS24_Eq39_edge_100kpc"]["mu_hMpc"]
db, _, dt_, _ = two_fluid(KT, mu_ref, OmA, ObA, pA["h"]); dbi, _, dti, _ = two_fluid(KT, None, OmA, ObA, pA["h"])
T_ = (ObA * db + (OmA - ObA) * dt_) / (ObA * dbi + (OmA - ObA) * dti)
Tf = np.interp(np.log(KSA), np.log(KT), T_, left=T_[0], right=T_[-1])
sig = lambda Pk, KS, T=None: math.sqrt(np.trapz((Pk if T is None else Pk * T ** 2) * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))
r8 = sig(PkA, KSA, Tf) / sig(PkA, KSA)
ref8 = F3R["K4"]["BS24_Eq39_edge_100kpc"]["bsk2_ai0.001"]["sigma8_ratio"]
P(f"   reproduction: sigma8 ratio at mu {mu_ref:.5f} h/Mpc = {r8:.5f} (F3 K4 {ref8:.5f})")
# model B
KSB, PkB, s8B = class_pk(pB["omega_b"], pB["omega_cdm"], pB["h"], pB["lnAs"], pB["n_s"], pB["tau"])
hB = pB["h"]; OmB = (pB["omega_b"] + pB["omega_cdm"]) / hB ** 2; ObB = pB["omega_b"] / hB ** 2
KV = np.geomspace(1e-4, 50.0, 400)
dbi, gbi, dti, gti = two_fluid(KV, None, OmB, ObB, hB)
Dinf = (ObB * dbi + (OmB - ObB) * dti) / OmB                           # dust-limit total growth at a = 1 (normalises P_lin)
Plin = np.interp(np.log(KV), np.log(KSB), PkB)
MUS = {"BS24_own_0.015637/Mpc": 0.015637 / hB, "cap_14.8h/Mpc": 14.8, "M1_411h/Mpc": 411.0}
KMAX = (0.3, 1.0, 10.0, 50.0)
F2 = {}
ok_f2 = True
for lab, mu_h in MUS.items():
    db, gb, dt_, gt = two_fluid(KV, mu_h, OmB, ObB, hB)
    vb = 100.0 * gb / Dinf / KV                                       # km/s per unit delta_lin (H0 = 100 h km/s/Mpc, k in h/Mpc)
    vr = 100.0 * (gb - gt) / Dinf / KV
    share = (gb - gt) / gb
    row = dict(mu_hMpc=mu_h, share_at_k={str(kk_): float(np.interp(math.log(kk_), np.log(KV), share)) for kk_ in (0.01, 0.1, 1.0, 10.0)})
    for km in KMAX:
        sel = KV <= km
        row[f"sigma_b_kmax{km}"] = float(math.sqrt(np.trapz(Plin[sel] * vb[sel] ** 2 * KV[sel] ** 2, KV[sel]) / (2 * math.pi ** 2)))
        row[f"sigma_rel_kmax{km}"] = float(math.sqrt(np.trapz(Plin[sel] * vr[sel] ** 2 * KV[sel] ** 2, KV[sel]) / (2 * math.pi ** 2)))
    F2[lab] = row
    ok_f2 &= all(np.isfinite(v) for kk_, v in row.items() if kk_.startswith("sigma"))
    P(f"   {lab:22s} mu {mu_h:9.4f} h/Mpc: " + "; ".join(f"k<={km}: sigma_b {row[f'sigma_b_kmax{km}']:6.1f}, sigma_rel {row[f'sigma_rel_kmax{km}']:7.2f} km/s"
                                                       for km in KMAX))
    P(f"   {'':22s} share of baryon velocity not carried by dust (delta_b'-delta_tau')/delta_b' at k = 0.01/0.1/1/10 h/Mpc: "
      + "/".join(f"{v:.3f}" for v in row["share_at_k"].values()))
vbc0 = 30.0 / 1021.0
P(f"   post-recombination streaming today (EXTERNAL, ~30 km/s at z~1020, decaying as 1/a): {vbc0:.3f} km/s")
ok_rep = abs(r8 / ref8 - 1) <= 1e-3
check("F2", ok_rep and ok_f2, f"F3 K4 reproduced {r8:.5f} vs {ref8:.5f} ({abs(r8 / ref8 - 1):.1e}); all cells finite {ok_f2}", "<= 1e-3", "")
RES["numbers"]["F2"] = dict(reproduction=dict(mine=r8, F3=ref8), cells=F2, sigma8_B_dustlimit=s8B, vbc_today=vbc0)

# ------------------------------------------------------------------------------------------------ F3 (SPARC hold radii)
P("\n--- F3: SPARC hold radii: V_hold = sqrt(2) V_bar (Upsilon_d 0.5, Upsilon_b 0.7; spherical approximation) ---")
UD, UB = 0.5, 0.7
GALS = {}
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    arr = np.array([[float(x) for x in l.split()[:6]] for l in open(fn) if l.strip() and not l.startswith("#")])
    R, Vo, eV, Vg, Vd, Vb = arr.T
    Vbar2 = np.abs(Vg) * Vg + UD * Vd ** 2 + UB * Vb ** 2
    GALS[nm] = dict(R=R, Vo=Vo, Vbar2=Vbar2)
VREL = (1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 600.0)
allV = np.concatenate([np.sqrt(2 * np.maximum(g["Vbar2"], 0)) for g in GALS.values()])
F3 = dict(N_gal=len(GALS), N_pts=int(allV.size), Vhold_percentiles={str(p_): float(np.percentile(allV, p_)) for p_ in (1, 5, 25, 50, 75, 95)},
          Vhold_last_median=float(np.median([math.sqrt(2 * max(g["Vbar2"][-1], 0)) for g in GALS.values()])), by_Vrel={})
for V in VREL:
    lost = float(np.mean(allV < V))
    rf = []
    for g in GALS.values():
        ok_ = np.sqrt(2 * np.maximum(g["Vbar2"], 0)) >= V
        rf.append(float(g["R"][ok_][-1] / g["R"][-1]) if ok_.any() else 0.0)
    F3["by_Vrel"][str(V)] = dict(frac_points_not_held=lost, median_rf_over_Rlast=float(np.median(rf)), frac_gal_rf_below_half_Rlast=float(np.mean(np.array(rf) < 0.5)))
    P(f"   V_rel {V:5.0f} km/s: RAR points not held {lost:6.3f}; median r_f/R_last {np.median(rf):.3f}; galaxies with r_f < R_last/2 {np.mean(np.array(rf) < 0.5):.3f}")
P(f"   V_hold percentiles (1/5/25/50/75/95 %): " + ", ".join(f"{v:.1f}" for v in F3["Vhold_percentiles"].values()) + f" km/s; median at the last point {F3['Vhold_last_median']:.1f}")
check("F3", len(GALS) == 175, f"{len(GALS)} galaxies, {allV.size} points", "175", "a0-free")
RES["numbers"]["F3"] = F3


# ------------------------------------------------------------------------------------------------ F4 (environment)
def law(gN):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN))


P("\n--- F4: acceleration criterion: RAR points with g_obs < g_e (dust cannot follow if the surroundings are held) ---")
env = {r["galaxy"].strip(): r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv")))}
GE_CHAE = 1.2e-10
mu_cap_phys = 14.8 * 0.6856                                            # 1/Mpc physical
s_1Mpc = (2 * math.pi / 1.0) ** 2 / ((2 * math.pi / 1.0) ** 2 + mu_cap_phys ** 2)   # kernel for a D = 1 Mpc mode at the cap
F4 = {}
for f in FOOTS:
    a0 = A0[f]; tot = 0; held = 0; unheld = 0; ngal = 0
    for nm, r in env.items():
        if nm not in GALS:
            continue
        ngal += 1
        lne = 0.5 * (float(r["log_eN_maxclu"]) + float(r["log_eN_noclu"]))
        ge = float(law(10 ** lne * GE_CHAE / a0)) * a0
        g = GALS[nm]; gobs = (g["Vo"] * 1e3) ** 2 / (g["R"] * KPC)
        tot += gobs.size; held += int(np.sum(gobs < ge)); unheld += int(np.sum(gobs < s_1Mpc * ge))
    F4[f] = dict(N_gal=ngal, N_pts=tot, frac_held_surroundings=held / tot, frac_unheld_cap_1Mpc=unheld / tot, s_1Mpc_cap=s_1Mpc)
    P(f"   [{f}] {ngal} galaxies, {tot} points: g_obs < g_e at {held / tot:.3f} of points (held surroundings); "
      f"{unheld / tot:.4f} with the field x s = {s_1Mpc:.3f} (unheld, D = 1 Mpc, cap)")
check("F4", all(F4[f]["N_gal"] > 0 for f in FOOTS), "computed", "computed", "")
RES["numbers"]["F4"] = F4

# ------------------------------------------------------------------------------------------------ F5 (Ursa Major)
P("\n--- F5: a moving-member class: SPARC Ursa Major members (distance method 4) ---")
MASTER = {r["name"]: r for r in csv.DictReader(open(os.path.join(DATA, "sparc_master_clean.csv")))}
ENVT = {r["name"]: r for r in csv.DictReader(open(os.path.join(DATA, "sparc_a0_environment_table.csv")))}
uma = [n for n, r in MASTER.items() if r["fD"] == "4" and n in GALS]
cz = np.array([float(ENVT[n]["cz_kms"]) for n in uma if n in ENVT])
sig_los = float(np.std(cz, ddof=1)); Vu = math.sqrt(3) * sig_los
F5 = dict(N_members=len(uma), N_cz=int(cz.size), sigma_los=sig_los, V_rel=Vu, footings={})
for f in FOOTS:
    a0 = A0[f]
    bins = np.linspace(-2.5, 1.0, 15)

    def offs(names, beyond):
        x, yv = [], []
        for nm in names:
            g = GALS[nm]; R = g["R"] * KPC
            ok_ = g["Vbar2"] > 0
            gbar = g["Vbar2"] * 1e6 / R; gobs = (g["Vo"] * 1e3) ** 2 / R
            vh = np.sqrt(2 * np.maximum(g["Vbar2"], 0))
            sel = ok_ & ((vh < Vu) if beyond else np.ones_like(ok_))
            x.append(np.log10(gbar[sel] / a0)); yv.append(np.log10(gobs[sel] / (law(gbar[sel] / a0) * a0)))
        return np.concatenate(x) if x else np.array([]), np.concatenate(yv) if yv else np.array([])
    xu, yu = offs(uma, True)
    xo, yo = offs([n for n in GALS if n not in uma], False)
    # matched-bin comparison: mean offset of UMa points beyond r_f minus the non-UMa mean in the same g_bar bin
    d = []
    for i in range(len(bins) - 1):
        su = (xu >= bins[i]) & (xu < bins[i + 1]); so = (xo >= bins[i]) & (xo < bins[i + 1])
        if su.sum() and so.sum() > 5:
            d += list(yu[su] - np.mean(yo[so]))
    d = np.array(d)
    newton_gap = float(np.mean([np.log10(law(10 ** xx) / 10 ** xx) for xx in xu])) if xu.size else float("nan")
    F5["footings"][f] = dict(N_pts_beyond_rf=int(xu.size), frac_member_points_beyond_rf=float(xu.size / max(1, sum(int(np.sum(GALS[n]['Vbar2'] > 0)) for n in uma))),
                             mean_offset_vs_field=float(np.mean(d)) if d.size else float("nan"),
                             se=float(np.std(d, ddof=1) / math.sqrt(d.size)) if d.size > 1 else float("nan"),
                             Newton_prediction_offset=-newton_gap)
    P(f"   [{f}] {len(uma)} members ({cz.size} with cz), sigma_LOS {sig_los:.0f} km/s -> V_rel {Vu:.0f} km/s; "
      f"{xu.size} member points beyond r_f ({F5['footings'][f]['frac_member_points_beyond_rf']:.2f} of their points); "
      f"their RAR offset vs field points in the same g_bar bins {F5['footings'][f]['mean_offset_vs_field']:+.3f} +- {F5['footings'][f]['se']:.3f} dex "
      f"(a dust-free member would sit at {-newton_gap:+.3f} dex)")

    # [A4, post-result, REPORTED] The count above selects member points with V_hold < V_rel at ANY radius. The frozen F5
    # wording is "their points beyond r_f"; read literally, r_f = the last radius with V_hold >= V_rel (0 if none) and the
    # points are R > r_f. Both readings, each with per-point and per-galaxy statistics (points within a galaxy are
    # correlated, so the per-point se understates the error). Nothing above is changed.
    def sel_pts(nm, mode):
        g = GALS[nm]; ok_ = g["Vbar2"] > 0; vh = np.sqrt(2 * np.maximum(g["Vbar2"], 0))
        if mode == "any_radius":
            return ok_ & (vh < Vu)
        rf = float(g["R"][vh >= Vu][-1]) if np.any(vh >= Vu) else 0.0
        return ok_ & (g["R"] > rf)
    n_member_pts = sum(int(np.sum(GALS[n]["Vbar2"] > 0)) for n in uma)
    A4 = {}
    for mode in ("any_radius", "beyond_rf"):
        dp, npn, gal_d, gal_n = [], [], [], []
        npts = 0
        for nm in uma:
            g = GALS[nm]; s_ = sel_pts(nm, mode); R = g["R"][s_] * KPC
            npts += int(s_.sum())
            if not s_.any():
                continue
            gbar = g["Vbar2"][s_] * 1e6 / R; gobs = (g["Vo"][s_] * 1e3) ** 2 / R
            xx = np.log10(gbar / a0); yy = np.log10(gobs / (law(gbar / a0) * a0))
            nn_all = list(-np.log10(law(10 ** xx) / 10 ** xx))
            npn += nn_all
            dd = []
            for i in range(len(bins) - 1):
                su = (xx >= bins[i]) & (xx < bins[i + 1]); so = (xo >= bins[i]) & (xo < bins[i + 1])
                if su.sum() and so.sum() > 5:
                    dd += list(yy[su] - np.mean(yo[so]))
            dp += dd
            if dd:
                gal_d.append(float(np.mean(dd))); gal_n.append(float(np.mean(nn_all)))
        dp, gal_d = np.array(dp), np.array(gal_d)
        se_p = float(np.std(dp, ddof=1) / math.sqrt(dp.size)); se_g = float(np.std(gal_d, ddof=1) / math.sqrt(gal_d.size))
        A4[mode] = dict(N_pts=npts, frac_member_points=npts / max(1, n_member_pts), N_matched_pts=int(dp.size),
                        per_point=dict(mean=float(np.mean(dp)), se=se_p, Newton=float(np.mean(npn)),
                                       z_from_Newton=float((np.mean(dp) - np.mean(npn)) / se_p)),
                        per_galaxy=dict(N_gal=int(gal_d.size), mean=float(np.mean(gal_d)), se=se_g, Newton=float(np.mean(gal_n)),
                                        z_from_Newton=float((np.mean(gal_d) - np.mean(gal_n)) / se_g)))
    A4["any_radius_reproduces_count_above"] = float(abs(A4["any_radius"]["per_point"]["mean"] - F5["footings"][f]["mean_offset_vs_field"]))
    F5["footings"][f]["A4"] = A4
    P(f"   [{f}] [A4] the count above is V_hold < V_rel at ANY radius; the frozen wording 'beyond r_f' read literally is R > the last "
      f"radius with V_hold >= V_rel (reported; any-radius per-point mean reproduced to {A4['any_radius_reproduces_count_above']:.1e}):")
    for mode in ("any_radius", "beyond_rf"):
        q = A4[mode]; pp = q["per_point"]; pg = q["per_galaxy"]
        P(f"      {mode:10s}: {q['N_pts']} points ({q['frac_member_points']:.3f} of members' points); per point {pp['mean']:+.4f} +- {pp['se']:.4f} dex "
          f"vs Newton {pp['Newton']:+.3f} ({pp['z_from_Newton']:.1f} se); per galaxy {pg['mean']:+.4f} +- {pg['se']:.4f} dex vs Newton "
          f"{pg['Newton']:+.3f} ({pg['z_from_Newton']:.1f} se, {pg['N_gal']} galaxies)")
check("F5", len(uma) > 0 and cz.size > 2, "computed", "computed", "")
RES["numbers"]["F5"] = F5

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("F6", rss < 1.0, f"{rss:.3f} GB", "< 1 GB", "peak RSS")
npass = sum(v["ok"] for v in CHK.values())
P(f"\nU1_A2_FIELD_FRAME COMPLETE: {npass}/{len(CHK)} checks PASS.  ({time.time() - T0:.0f} s)")
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, f"u1_a2_field_frame_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"u1_a2_field_frame{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
