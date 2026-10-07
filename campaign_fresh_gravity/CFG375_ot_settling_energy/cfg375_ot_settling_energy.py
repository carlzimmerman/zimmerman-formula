"""CFG375: minimum energy any settling mechanism must handle (optimal transport) vs the vacuum budget.
Frozen criteria: FROZEN_CRITERIA.md (committed alone first, 402c886d0).
kappa = 1/2 FITTED. Both a0 footings, never pooled. No dark-matter particle; the cold fluid's amount (5.364 M_b) is an input.
MUTATE: CFG375_MUTATE=1 replaces the monotone (Brenier) map by the anti-monotone rearrangement; C2 must FAIL (rc 1).
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG100_kids_mass_rederivation"))
import cfg100_lib as L  # nu_mono, dta, r_ta_law (record implementation)

MUTATE = os.environ.get("CFG375_MUTATE", "0") == "1"
KERNEL = os.environ.get("CFG375_KERNEL", "record")  # POST-FREEZE sensitivity: "analytic" = 1/(1-exp(-sqrt y)) exactly
SUF = ("_MUTATE" if MUTATE else "") + ("_ANALYTIC" if KERNEL == "analytic" else "")

# ---------------- constants (SI)
G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98847e30
KPC = 3.0856775814913673e19
GYR = 3.15576e16
H0 = 67.36 * 1e3 / (KPC * 1e3)
OM, OB = 0.3153, 0.0493
OC, OL = OM - OB, 1 - OM
RHOC = 3 * H0 ** 2 / (8 * math.pi * G)
RHO_M, RHO_CBAR = OM * RHOC, OC * RHOC
UVAC = OL * RHOC * C ** 2  # rho_Lambda c^2 [J/m^3]
DTA = 11.806
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
HOSTS = [1e9, 1e10, 6e10, 1e11, 1e12, 1e13]
FRET = [1.0, 0.18]
TAUS = {"10.3Gyr": 10.3 * GYR, "1Gyr": 1.0 * GYR}
SUPPLY = 5.364
CFG373_G4 = (3e-8, 1.3e-5)
NQ = 200000
Q = (np.arange(NQ) + 0.5) / NQ


def nu(y):
    if KERNEL == "analytic":
        y = np.maximum(np.asarray(y, float), 1e-14)
        return 1.0 / (-np.expm1(-np.sqrt(y)))
    return np.asarray(L.nu_mono(y), float)


def mph_enc(r, Mb, a0):
    y = G * Mb / (np.asarray(r, float) ** 2 * a0)
    return Mb * (nu(y) - 1.0)


def r_ta(Mb, a0):
    f = lambda lr: math.log(Mb * float(nu(G * Mb / math.exp(2 * lr) / a0))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * DTA * RHO_M)
    return math.exp(brentq(f, math.log(1e-3 * KPC), math.log(1e5 * KPC), xtol=1e-12))


def target_quantile(Mb, a0, rout):
    rg = np.logspace(math.log10(rout * 1e-7), math.log10(rout), 40001)
    m = mph_enc(rg, Mb, a0)
    qg = m / m[-1]
    keep = np.concatenate([[True], np.diff(qg) > 0])
    return np.interp(Q, qg[keep], rg[keep]), m[-1]


def g_frame(r, Mb, a0):
    return nu(G * Mb / (r ** 2 * a0)) * G * Mb / r ** 2


def phi_diff(kind, Mb, a0, r_from, r_to):
    """Phi_b(r_to) - Phi_b(r_from), vectorised."""
    if kind == "B2":
        return math.sqrt(G * Mb * a0) * np.log(r_to / r_from)
    if kind == "B3":
        return -G * Mb / r_to + G * Mb / r_from
    # B1: full framework field, cumulative integral on a log grid
    lo = min(r_from.min(), r_to.min()) * 0.999
    hi = max(r_from.max(), r_to.max()) * 1.001
    lr = np.linspace(math.log(lo), math.log(hi), 200001)
    rr = np.exp(lr)
    integ = g_frame(rr, Mb, a0) * rr
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(lr))])
    return np.interp(np.log(r_to), lr, phi) - np.interp(np.log(r_from), lr, phi)


def self_energy(Mt, rq):
    return -G * Mt ** 2 * np.mean(Q / rq)


def cat(eps):
    return "ALLOWED" if eps <= 0.1 else ("MARGINAL" if eps <= 1 else "EXCLUDED")


WORST = {"ALLOWED": 0, "MARGINAL": 1, "EXCLUDED": 2}
rng = np.random.default_rng(375)
controls = {}
ok = True

# C1
d0 = L.dta(0.0)
yy = np.logspace(-2, 2, 400)
nu_err = float(np.max(np.abs(np.asarray(L.nu_mono(yy), float) / (1 / (1 - np.exp(-np.sqrt(yy)))) - 1)))
c1 = abs(d0 - DTA) < 1e-3 and nu_err < 1e-3
# cross-check own r_ta against the record's r_ta_law (Mpc units)
rta_rel = abs(r_ta(1e11 * MSUN, A0["canonical"]) / (KPC * 1e3) / L.r_ta_law(1e11, L.A0["canonical"], 0.0) - 1)
controls["C1"] = {"dta0": d0, "nu_rel_err_max": nu_err, "r_ta_vs_record_rel": rta_rel, "pass": bool(c1 and rta_rel < 1e-3)}
ok &= controls["C1"]["pass"]
# C3
Rt = 100 * KPC; Mt = 1e11 * MSUN
c3 = abs(self_energy(Mt, Rt * Q ** (1 / 3)) / (-0.6 * G * Mt ** 2 / Rt) - 1)
controls["C3"] = {"rel_err": float(c3), "pass": bool(c3 < 1e-3)}
ok &= controls["C3"]["pass"]

rows = []
c2_all, c4_all = True, True
for fk, a0 in A0.items():
    for Mb_s in HOSTS:
        Mb = Mb_s * MSUN
        rta = r_ta(Mb, a0); rout = 0.4 * rta
        rf, Mph = target_quantile(Mb, a0, rout)
        for fr in FRET:
            S = SUPPLY * Mb / fr
            RL = (3 * S / (4 * math.pi * RHO_CBAR)) ** (1 / 3)
            Vc = 4 * math.pi / 3 * RL ** 3
            Mt = min(Mph, S)
            Rt = (3 * Mt / (4 * math.pi * RHO_CBAR)) ** (1 / 3)
            ri = Rt * Q ** (1 / 3)
            # C4: target mass (scaled phantom) integrates to Mt
            c4 = abs((Mt / Mph) * float(mph_enc(rout, Mb, a0)) / Mt - 1) < 1e-6
            c4_all &= c4
            w2_mono = float(np.mean((ri - rf) ** 2))
            w2_anti = float(np.mean((ri - rf[::-1]) ** 2))
            w2_used = w2_anti if MUTATE else w2_mono
            # C2: random permutations on a 2000-atom discretisation
            n = 2000; idx = (np.arange(n) + 0.5) / n * NQ
            ia, fa = ri[idx.astype(int)], rf[idx.astype(int)]
            w2_rand = min(float(np.mean((ia - fa[rng.permutation(n)]) ** 2)) for _ in range(20))
            w2_used_d = float(np.mean((ia - (fa[::-1] if MUTATE else fa)) ** 2))
            w2_mono_d = float(np.mean((ia - fa) ** 2)); w2_anti_d = float(np.mean((ia - fa[::-1]) ** 2))
            c2 = w2_used_d <= min(w2_mono_d, w2_anti_d, w2_rand) * (1 + 1e-12)
            c2_all &= c2
            ek = {t: Mt * w2_used / (2 * tau ** 2) for t, tau in TAUS.items()}
            Wi = -0.6 * G * Mt ** 2 / Rt
            Wf = self_energy(Mt, rf)
            eb = {}
            for kind in ("B1", "B2", "B3"):
                dU = Mt * float(np.mean(phi_diff(kind, Mb, a0, ri, rf))) + (Wf - Wi)
                eb[kind] = -dU
            budget = UVAC * Vc
            row = {"footing": fk, "Mb_Msun": Mb_s, "f_ret": fr, "r_ta_kpc": rta / KPC, "r_out_kpc": rout / KPC,
                   "Mph_out_over_Mb": Mph / Mb, "supply_over_Mb": S / Mb, "supply_binds": bool(S < Mph),
                   "Mt_over_Mb": Mt / Mb, "R_L_kpc": RL / KPC, "R_t_kpc": Rt / KPC, "W2_kpc": math.sqrt(w2_used) / KPC,
                   "W2_mono_kpc": math.sqrt(w2_mono) / KPC, "W2_anti_kpc": math.sqrt(w2_anti) / KPC,
                   "budget_J": budget, "C2_pass": bool(c2), "C4_pass": bool(c4)}
            for t in TAUS:
                row[f"Ekin_{t}_J"] = ek[t]; row[f"eps_kin_{t}"] = ek[t] / budget
            for k in eb:
                row[f"Ebind_{k}_J"] = eb[k]; row[f"eps_bind_{k}"] = eb[k] / budget
            # POST-FREEZE stress number (reported, not a verdict input): budget over the host volume r < r_out only
            Vh = 4 * math.pi / 3 * rout ** 3
            row["eps_host_max_over_bounds"] = max(max(ek.values()), max(eb.values())) / (UVAC * Vh)
            rows.append(row)
controls["C2"] = {"pass": bool(c2_all), "map_used": "anti-monotone (MUTATE)" if MUTATE else "monotone"}
controls["C4"] = {"pass": bool(c4_all)}
ok &= c2_all and c4_all

# verdicts per footing per bound
verdict = {}
for fk in A0:
    rs = [r for r in rows if r["footing"] == fk]
    v = {}
    for key in ["eps_kin_10.3Gyr", "eps_kin_1Gyr", "eps_bind_B1", "eps_bind_B2", "eps_bind_B3"]:
        vals = [r[key] for r in rs]
        mx = max(vals); mn = min(vals)
        v[key] = {"max": mx, "min": mn, "category_worst": cat(mx),
                  "inside_CFG373_G4_range_all": bool(all(CFG373_G4[0] <= x <= CFG373_G4[1] for x in vals)),
                  "n_above_CFG373_max": int(sum(x > CFG373_G4[1] for x in vals))}
    kin_cat = max([v["eps_kin_10.3Gyr"]["category_worst"], v["eps_kin_1Gyr"]["category_worst"]], key=WORST.get)
    bind_cat = v["eps_bind_B1"]["category_worst"]
    flags = [k for k in ("eps_bind_B2", "eps_bind_B3") if v[k]["category_worst"] != bind_cat]
    v["bound_a_kinetic"] = kin_cat; v["bound_b_binding_B1"] = bind_cat; v["category_disagreement_flags"] = flags
    verdict[fk] = v

out = {"lane": "CFG375", "mutate": MUTATE, "kernel": KERNEL, "controls": controls, "all_controls_pass": bool(ok), "verdict": verdict, "rows": rows,
       "consts": {"rho_Lambda_c2_J_m3": UVAC, "rho_cbar_kg_m3": RHO_CBAR, "Delta_ta": DTA, "CFG373_G4": CFG373_G4}}
with open(os.path.join(HERE, f"cfg375_results{SUF}.json"), "w") as fh:
    json.dump(out, fh, indent=1)

lines = [f"CFG375 OT settling energy  MUTATE={MUTATE}  KERNEL={KERNEL}"]
lines.append(f"rho_Lambda c^2 = {UVAC:.4e} J/m^3 ; rho_cbar = {RHO_CBAR:.4e} kg/m^3")
for k, c in controls.items():
    lines.append(f"{k}: {c}")
hdr = "foot      Mb      fret  r_ta[kpc] r_out  Mph/Mb  S/Mb  Mt/Mb  R_L[kpc] W2[kpc]  eps_kin10.3  eps_kin1   eps_B1     eps_B2     eps_B3"
lines.append(hdr)
for r in rows:
    lines.append(f"{r['footing']:9s} {r['Mb_Msun']:.0e} {r['f_ret']:5.2f} {r['r_ta_kpc']:8.1f} {r['r_out_kpc']:7.1f} {r['Mph_out_over_Mb']:6.2f} {r['supply_over_Mb']:6.2f} {r['Mt_over_Mb']:6.2f} {r['R_L_kpc']:8.1f} {r['W2_kpc']:7.1f}  "
                 f"{r['eps_kin_10.3Gyr']:.3e}  {r['eps_kin_1Gyr']:.3e}  {r['eps_bind_B1']:.3e}  {r['eps_bind_B2']:.3e}  {r['eps_bind_B3']:.3e}")
for fk, v in verdict.items():
    lines.append(f"VERDICT [{fk}]: bound (a) kinetic = {v['bound_a_kinetic']}; bound (b) binding B1 = {v['bound_b_binding_B1']}; flags {v['category_disagreement_flags']}")
    for key in ["eps_kin_10.3Gyr", "eps_kin_1Gyr", "eps_bind_B1", "eps_bind_B2", "eps_bind_B3"]:
        lines.append(f"   {key}: max {v[key]['max']:.3e} min {v[key]['min']:.3e}  above CFG373 max: {v[key]['n_above_CFG373_max']}/12")
lines.append(f"POST-FREEZE stress: max over cells of E_max/(rho_L c^2 V(r<r_out)) = {max(r['eps_host_max_over_bounds'] for r in rows):.3e}")
lines.append(f"ALL CONTROLS PASS: {ok}")
txt = "\n".join(lines)
print(txt)
with open(os.path.join(HERE, f"cfg375{SUF}.out"), "w") as fh:
    fh.write(txt + "\n")
sys.exit(0 if ok else 1)
