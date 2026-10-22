#!/usr/bin/env python3
"""E1_input_audit -- are the doors-push verdicts and the screened theory's record inputs free of hidden LCDM or
standard-MOND assumptions?  Clean-substitute sensitivities S1-S7 of FROZEN_CRITERIA.md.

Run:     OMP_NUM_THREADS=1 nice -n 10 python3 e1_input_audit.py
Mutate:  E1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 e1_input_audit.py   (native a0 with 2 pi in place of Z: K1 fails)

Other lanes' scripts are exec'd READ-ONLY: their source text is run up to a marker that precedes any file write
(D7b via D7c's own loader, D7c, D6), and the one place D6 could write (np.savez of its tables) is patched out.
kappa = 1/2 FITTED.  Footings never pooled.  Cold energy, no particle.  Not theory closed.
"""
import os, sys, json, math, re, time, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("E1_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
LANE = "E1_INPUT_AUDIT"
OUT, CHECKS = [], []
RES = {"lane": LANE, "mutate": MUT}
T0 = time.time()


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def check(cid, ok, value, thr, label):
    CHECKS.append(dict(id=cid, pass_=bool(ok), value=str(value), threshold=str(thr), label=label))
    P(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr} :: {label}")


def R(*p):
    return os.path.join(ROOT, *p)


def J(*p):
    return json.load(open(R(*p)))


def exec_until(path, marker, patches=(), name="ro"):
    """exec another lane's source text up to `marker` (read-only), return its namespace."""
    src = open(path).read()
    assert marker in src, (path, marker)
    src = src.split(marker)[0]
    for a, b in patches:
        assert a in src, (path, a)
        src = src.replace(a, b)
    argv = sys.argv
    sys.argv = [path]
    ns = {"__file__": path, "__name__": name}
    cwd = os.getcwd()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, "exec"), ns)
    finally:
        sys.argv = argv
        os.chdir(cwd)
    return ns


# ================================================================================ constants (all listed)
C_SI = 2.99792458e8
MPC = 3.0856775814913673e22
Z = 2 * math.sqrt(8 * math.pi / 3)                 # 5.78881 (never ~21)
ZU = 2 * math.pi if MUT else Z                     # MUTATE: wrong divisor
H0_PL, OL_PL = 67.4, 0.685                         # Planck 2018 LCDM (the record's footing inputs) [EXT, LCDM fit]
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10                # BRIEF rule 3
A0_CAN_X, A0_ALT_X = 9.3603e-11, 1.1312e-10        # CFG4/FP0 exact footing values


def a0_of_H(H):                                    # a0 = c H / Z  (H in km/s/Mpc)
    return C_SI * H * 1e3 / MPC / ZU


P(f"{LANE}  (kappa = 1/2 FITTED; footings never pooled; not theory closed){'  [MUTATE: 2 pi for Z]' if MUT else ''}")

# ================================================================================ S1 framework-native background
P("\n=== S1  framework-native background: what a0 is when H0 comes from the model's own background (A46, CFG886)")
a46 = J("deepseek_push", "DS_FINAL_2026_10_21", "A46_cosmology_fit", "a46_results.json")["numbers"]
c886 = J("campaign_fresh_gravity", "CFG886_ratio_fret_without_planck", "cfg886_results.json")["T2a"]["primary"]
h886, om886 = c886["h"]["mean"], c886["Om"]["mean"]
HN = {"A46_2pt": 100 * a46["model2"]["h"], "A46_3pt": a46["H0_model"], "A46_map": a46["H0_map"],
      "CFG886_BAO+BBN": 100 * h886 * math.sqrt(1 - om886)}
A0N = {k: a0_of_H(v) for k, v in HN.items()}
H_L_PL = H0_PL * math.sqrt(OL_PL)                  # Planck H_Lambda = H0 sqrt(Omega_L)
k1 = max(abs(A0N["A46_2pt"] / a46["model2"]["a0"] - 1), abs(A0N["A46_3pt"] / a46["model3"]["a0"] - 1),
         abs(A0N["A46_map"] / a46["a0_map"] - 1))
check("K1", k1 < 1e-6, f"{k1:.2e}", "<1e-6", "native a0 = cH0/Z reproduces A46's own a0 entries (2pt, 3pt, map)")
k2 = abs(C_SI * H_L_PL * 1e3 / MPC / Z / A0_CAN - 1)
check("K2", k2 < 2e-3, f"{k2:.2e}", "<2e-3", "canonical footing = c H0 sqrt(Omega_L)/Z at Planck (67.4, 0.685)")
for k, v in HN.items():
    P(f"  {k:15s}: H0,native = {v:7.3f} km/s/Mpc -> a0 = {A0N[k]:.4e}  ({100 * (A0N[k] / A0_CAN_X - 1):+.2f}% vs canonical "
      f"9.3603e-11, {100 * (A0N[k] / A0_ALT_X - 1):+.2f}% vs alt 1.1312e-10)")
NAT_LO, NAT_HI = min(A0N.values()), max(A0N.values())
NAT_C = A0N["A46_3pt"]                             # central native value (A46 3-pt fit, the record's quoted 9.53e-11)
P(f"  native band a0 in [{NAT_LO:.4e}, {NAT_HI:.4e}]  (canonical {100 * (NAT_LO / A0_CAN_X - 1):+.1f}% .. "
  f"{100 * (NAT_HI / A0_CAN_X - 1):+.1f}%; alt {100 * (NAT_HI / A0_ALT_X - 1):+.1f}% .. {100 * (NAT_LO / A0_ALT_X - 1):+.1f}%)")
P(f"  Planck H_Lambda = {H_L_PL:.3f}; the native H0 IS the LCDM H0*sqrt(Omega_L) (A46 map h = h_L sqrt(1-Om_L)), so the canonical "
  f"footing is the background-invariant one; the alt footing (cH0/Z at 67.4) does not exist in the native background")
P(f"  A46 cost of keeping H0 = 67.4 (alt footing): dchi2 = {a46['dchi2_h0_2pt']:.1f} (2pt) / {a46['dchi2_h0_3pt']:.1f} (3pt)")
SH0ES = (73.0, 1.0)                                # as used on disk: A51 a51_checks.py H0_SH0ES, SIG_H0_SH0ES
gapH = {k: (SH0ES[0] - v) / SH0ES[1] for k, v in HN.items()}
P(f"  NOTE: the native H0 band {min(HN.values()):.1f}-{max(HN.values()):.1f} sits {min(gapH.values()):.1f}-{max(gapH.values()):.1f} "
  f"sigma below the local-ladder 73.0 +- 1.0 used on disk (A51); Planck-LCDM's 67.4 sits {(73 - 67.4) / 1.0:.1f} sigma below it")
RES["S1"] = dict(H0_native=HN, a0_native=A0N, band=[NAT_LO, NAT_HI], central=NAT_C, H_Lambda_Planck=H_L_PL,
                 shift_vs_canonical_pct=[100 * (NAT_LO / A0_CAN_X - 1), 100 * (NAT_HI / A0_CAN_X - 1)],
                 shift_vs_alt_pct=[100 * (NAT_HI / A0_ALT_X - 1), 100 * (NAT_LO / A0_ALT_X - 1)],
                 dchi2_alt_2pt=a46["dchi2_h0_2pt"], dchi2_alt_3pt=a46["dchi2_h0_3pt"],
                 sigma_below_SH0ES=gapH, SH0ES_on_disk=SH0ES)

# ================================================================================ S2 kappa in the native background
P("\n=== S2  kappa measurements re-expressed in the native background (kappa_nat = a0 Z / (2 c H0,native))")
# record values (quoted): CFG493 kappa_Lambda (DE convention, rho_L Planck); A51/A71/A81 kappa_P3 (rho_crit at 67.4)
KREC = {"CFG493 (kappa_DE)": (0.417, 0.095, "DE"), "A51 (kappa_P3)": (0.371, 0.119, "P3"),
        "A71 (kappa_P3)": (0.3777, 0.1207, "P3"),
        "A81 (kappa_P3)": (0.37808124619485783, 0.12081732631600586, "P3")}
S2 = {}
for k, (kap, sk, conv) in KREC.items():
    Href = H_L_PL if conv == "DE" else H0_PL
    rows = {}
    for nk, H in HN.items():
        f = Href / H
        kn, skn = kap * f, sk * f
        rows[nk] = dict(kappa=kn, sigma=skn, z_half=(0.5 - kn) / skn, z_thermal=(Z / (4 * math.pi) - kn) / skn)
    z0 = (0.5 - kap) / sk
    zr = [r["z_half"] for r in rows.values()]
    S2[k] = dict(record=kap, sigma=sk, convention=conv, z_half_record=z0, native=rows,
                 dz_half_max=max(abs(z - z0) for z in zr))
    P(f"  {k:18s} record {kap:.4f} +- {sk:.4f} (1/2 at {z0:+.2f} sigma) -> native "
      + ", ".join(f"{nk} {r['kappa']:.4f} ({r['z_half']:+.2f})" for nk, r in rows.items()))
# the A51 coherent-floor H0 term: 12.5% half-span (56.8/67.4/73.0) collapses in the native background
hs = 0.5 * (max(HN.values()) - min(HN.values())) / np.mean(list(HN.values()))
fl_old = math.sqrt(0.21 ** 2 + 0.161 ** 2 + 0.125 ** 2 + 0.10 ** 2)
fl_new = math.sqrt(0.21 ** 2 + 0.161 ** 2 + hs ** 2 + 0.10 ** 2)
P(f"  A51 coherent floor: H0 term 12.5% -> {100 * hs:.1f}% half-span of the native band; total {100 * fl_old:.1f}% -> {100 * fl_new:.1f}%")
RES["S2"] = dict(kappas=S2, A51_H0_halfspan_native=hs, A51_floor_old=fl_old, A51_floor_native=fl_new,
                 note="kappa_P3 and kappa_DE coincide in the native background (A46: Lambda_bare/Lambda_obs = 1.038)")

# ================================================================================ S5 D7b / D7c at the native a0
P("\n=== S5  Q2 (D7b solver) and SPARC (AG4b pipeline) at the native a0, via D7c's own code (read-only exec)")
t = time.time()
D7C = R("doors_push_2026_10_22", "D7c_q2_rar_gate", "d7c_q2_rar_gate.py")
NS7 = exec_until(D7C, "FIT = {f: {k: fit_all(nu, A0S[f]) for k, nu in LAWS.items()} for f in C.FOOTS}", name="d7c_ro")
d7c = J("doors_push_2026_10_22", "D7c_q2_rar_gate", "d7c_q2_rar_gate_results.json")
LAWS, NAMED, EL = NS7["LAWS"], NS7["NAMED"], NS7["EL"]
H_HI, HEES = NS7["H_HI"], NS7["HEES"]
A0Q = NS7["A0Q"]
NATK = {"nat_lo": NAT_LO, "nat_c": NAT_C, "nat_hi": NAT_HI}
for k, v in NATK.items():
    A0Q[k] = v                                     # Q2_law reads A0Q[foot] at call time
q25 = NS7["Q2_law"](LAWS["beta=2.5"], "canonical", "E0")[0]
fit_all, paired_z, chi_z = NS7["fit_all"], NS7["paired_z"], NS7["chi_z"]
FITc = {k: fit_all(LAWS[k], NS7["A0S"]["canonical"]) for k in list(NAMED) + ["beta=2.5"]}
z25 = min(paired_z(FITc[y][0], FITc["beta=2.5"][0])[2] for y in NAMED)
k3 = (abs(q25 / d7c["Q2"]["beta=2.5"]["canonical"]["Q2"]["E0"] - 1), abs(z25 - d7c["SPARC"]["canonical"]["beta=2.5"]["worst_z"]))
check("K3", k3[0] < 1e-6 and k3[1] < 0.02, f"{k3[0]:.1e},{k3[1]:.1e}", "<1e-6,<0.02",
      "D7c reproduced: Q2(beta=2.5, canonical, E0) and SPARC worst paired z (beta=2.5, canonical)")


def law_row(name, foot_q, a0s, fit_cache):
    vals = [NS7["Q2_law"](LAWS[name], foot_q, e)[0] for e in EL]
    hees = "PASS" if all(HEES[0] - 2 * HEES[1] <= v <= H_HI for v in vals) else (
        "FAIL" if not any(HEES[0] - 2 * HEES[1] <= v <= H_HI for v in vals) else "E-DEPENDENT")
    if name not in fit_cache:
        fit_cache[name] = fit_all(LAWS[name], a0s)
    zs = {y: paired_z(fit_cache[y][0], fit_cache[name][0])[2] for y in NAMED if y != name}
    cs = {y: chi_z(fit_cache[y][1], fit_cache[name][1])[1] for y in NAMED if y != name}
    wz, wc = min(zs.values()), min(cs.values())
    return dict(Q2=dict(zip(EL, vals)), max_over_Hees=max(vals) / H_HI, Hees=hees,
                sigma_Hees_max=(max(vals) - HEES[0]) / HEES[1], SPARC_worst_z=wz, SPARC=("PASS" if wz > -2 else "FAIL"),
                S1_worst_z=wc, S1=("PASS" if wc > -2 else "FAIL"), both=(hees == "PASS" and wz > -2))


S5 = {}
SEL = ["L", "Q", "M", "S", "R"] + [f"beta={b:g}" for b in NS7["B_GRID"]] + [f"n={n:g}" for n in NS7["N_GRID"]]
for k, a0v in NATK.items():
    cache = {}
    for y in NAMED:
        cache[y] = fit_all(LAWS[y], a0v)
    S5[k] = {"a0": a0v, "laws": {nm: law_row(nm, k, a0v, cache) for nm in SEL}}
    passers = [nm for nm, r in S5[k]["laws"].items() if r["both"]]
    s1c = [nm for nm in passers if S5[k]["laws"][nm]["S1"] == "FAIL"]
    S5[k]["passers_primary"] = passers
    S5[k]["passers_S1_contradicts"] = s1c
    S5[k]["outcome_native"] = ("NO LAW PASSES BOTH" if not passers else
                               ("UNDECIDED (S1 contradicts the primary for " + ", ".join(s1c) + ")" if s1c else
                                "A LAW PASSES BOTH: " + ", ".join(passers)))
    L = S5[k]["laws"]["L"]
    P(f"  [{k} a0={a0v:.4e}] canonical law L: Q2 max/Hees-2sigma {L['max_over_Hees']:.2f} ({L['Hees']}); "
      f"passers (Hees all E + SPARC primary z>-2): {passers or 'none'} -> {S5[k]['outcome_native']}")
    for nm in ("beta=2.5", "beta=3", "beta=6", "n=2", "n=8"):
        r = S5[k]["laws"][nm]
        P(f"     {nm:8s}: Q2/Hees2s max {r['max_over_Hees']:.3f} [{r['Hees']}] SPARC z {r['SPARC_worst_z']:+.2f} [{r['SPARC']}] "
          f"S1 z {r['S1_worst_z']:+.2f}")
# SPS prior centre of the per-galaxy Upsilon (AG4b: log 0.5 +- 0.10 dex) moved +-0.2 dex, native central a0
LU0_0 = NS7["LU0"]
S5["ups_prior_shift"] = {}
for dl in (-0.2, +0.2):
    NS7["LU0"] = LU0_0 + dl
    NS7["LU"] = NS7["LU0"] + np.linspace(-0.5, 0.5, 201)
    NS7["UG"] = 10 ** NS7["LU"]
    cache = {y: fit_all(LAWS[y], NAT_C) for y in NAMED}
    rows = {nm: law_row(nm, "nat_c", NAT_C, cache) for nm in ("L", "Q", "beta=2.5", "beta=3", "beta=6")}
    S5["ups_prior_shift"][f"{dl:+.1f}"] = rows
    P(f"  [native c, Upsilon prior centre {dl:+.1f} dex] SPARC worst z: " + ", ".join(
        f"{nm} {r['SPARC_worst_z']:+.2f}" for nm, r in rows.items()))
NS7["LU0"] = LU0_0
NS7["LU"] = LU0_0 + np.linspace(-0.5, 0.5, 201)
NS7["UG"] = 10 ** NS7["LU"]
S5["D7c_record_outcome"] = d7c["outcome"]
RES["S5_D7b_D7c"] = S5
P(f"  (S5 took {time.time() - t:.0f} s)")

# D2 gamma_v: interpolation in ln a0 at fixed g_ext between D2's two footings (orientation-averaged, 20 kAU)
d2 = J("doors_push_2026_10_22", "D2_wide_binary_fork", "d2_wide_binary_fork_results.json")["gamma_table"]
S5b = {}
for gx in ("PREREG_primary", "PREREG_alt"):
    gc, ga = d2[f"canonical|{gx}|20"]["avg"], d2[f"alt|{gx}|20"]["avg"]
    sl = (ga - gc) / math.log(A0_ALT / A0_CAN)
    S5b[gx] = {k: gc + sl * math.log(v / A0_CAN) for k, v in NATK.items()}
    S5b[gx]["record_canonical"], S5b[gx]["record_alt"] = gc, ga
    P(f"  D2 gamma_v(20 kAU, {gx}) [interpolated in ln a0]: canonical {gc:.4f}, alt {ga:.4f} -> native "
      + ", ".join(f"{k} {S5b[gx][k]:.4f}" for k in NATK))
RES["S5_D2_gamma_interp"] = S5b

# ================================================================================ S3/S4 CFG820 globular floor
P("\n=== S3/S4  CFG820's L* floor (estimator verbatim from cfg820.py via D8) under SPS M/L +-0.2 dex, native a0,"
  " and its standard-MOND machinery (nu_RAR + algebraic EFE) replaced by the canonical law")
G8, Msun8, kpc8, PC8 = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
MW_MB, WID = 6.0e10, 0.15                         # CFG332 constants (MW point mass is an SPS-based baryonic mass)
GC = J("campaign_fresh_gravity", "CFG332_globulars_three_routes", "cfg332_globulars_results.json")["clusters"]
PRIM = [g for g in GC if g["name"] != "Pal 3"]    # CFG334: Pal 3 excluded (binaries explain)
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000])
ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
KB, M_P = 1.380649e-23, 1.67262192369e-27


def nu_rar(y): y = max(float(y), 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))
def nu_law(y): y = max(float(y), 1e-12); return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))


def Sfun(s):
    if s <= 0.01: return s / 2
    if s >= 1000: return 1 - 1 / s
    return float(np.interp(math.log(s), np.log(ST_s), ST_S))


def make_chi2(ups=1.6, nu=nu_rar, efe=True):
    vU = (math.log(10) * WID / 2) ** 2

    def pred(g, a0, Lst):
        M = ups * g["LV"]
        sN = math.sqrt(G8 * M * Msun8 / (6.0 * (4.0 / 3.0) * g["rhl"] * PC8)) / 1e3
        y = G8 * (ups * g["LV"] * Msun8 / 2) / ((4.0 / 3.0) * g["rhl"] * PC8) ** 2 / a0
        if efe:
            y = y + G8 * MW_MB * Msun8 / (g["RGC"] * kpc8) ** 2 / a0
        B = nu(y)
        if Lst is None: return sN
        rM = math.sqrt(G8 * M * Msun8 / a0) / PC8; lg = Lst ** 2 / (2 * rM); s = (4.0 / 3.0) * g["rhl"] / lg
        return sN * math.sqrt(1 + Sfun(s) * (B - 1))

    def chi2(a0, L):
        return sum((math.log(g["so"]) - math.log(pred(g, a0, L))) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU) for g in PRIM)
    return chi2


GRID = np.geomspace(5.75, 3000, 400)
FINE = np.geomspace(1.0, 400, 40001)


def floor(chi2, a0):
    cg = np.array([chi2(a0, L) for L in GRID]); cmin = min(cg.min(), chi2(a0, None))
    L95g = float(GRID[cg - cmin <= 3.84].min())
    sel = (FINE > 0.5 * L95g) & (FINE < 1.6 * L95g)
    cf = np.array([chi2(a0, L) for L in FINE[sel]]); cminf = min(cmin, cf.min())
    ok = FINE[sel][cf - cminf <= 3.84]
    return L95g, float(ok.min()), cminf


ref820 = J("campaign_fresh_gravity", "CFG820_stiffness_from_globulars", "cfg820_results.json")
c820 = make_chi2()
k4 = []
for f, a0 in (("canonical", A0_CAN_X), ("alt", A0_ALT_X)):
    k4.append(abs(floor(c820, a0)[0] / ref820[f"primary (no Pal 3)|{f}"]["L95"] - 1))
check("K4", max(k4) < 5e-3, f"{max(k4):.2e}", "<5e-3", "CFG820 L*_95 reproduced on its own grid, both footings")
sig_th = math.sqrt(KB * 1e4 / (1.22 * M_P))      # A76 thermal sigma (1e4 K, mu 1.22)
VAR = {"record (nu_RAR+EFE, Ups 1.6)": dict(ups=1.6, nu=nu_rar, efe=True),
       "Ups_V -0.2 dex": dict(ups=1.6 * 10 ** -0.2, nu=nu_rar, efe=True),
       "Ups_V +0.2 dex": dict(ups=1.6 * 10 ** 0.2, nu=nu_rar, efe=True),
       "canonical law nu_L + same EFE": dict(ups=1.6, nu=nu_law, efe=True),
       "canonical law nu_L, no EFE (isolated)": dict(ups=1.6, nu=nu_law, efe=False),
       "nu_RAR, no EFE (isolated)": dict(ups=1.6, nu=nu_rar, efe=False)}
A0SET = {"canonical": A0_CAN_X, "alt": A0_ALT_X, "native_lo": NAT_LO, "native_c": NAT_C, "native_hi": NAT_HI}
S3 = {}
for vk, kw in VAR.items():
    ch = make_chi2(**kw)
    S3[vk] = {}
    for ak, a0 in A0SET.items():
        if vk != "record (nu_RAR+EFE, Ups 1.6)" and ak in ("native_lo", "native_hi"):
            continue
        L95g, L95f, cmin = floor(ch, a0)
        Lth = sig_th ** 2 / a0 / PC8
        dth = ch(a0, Lth) - cmin
        S3[vk][ak] = dict(L95_grid=L95g, L95_fine=L95f, L_thermal=Lth, dchi2_thermal=dth,
                          thermal_class=("EXCLUDED at 95%" if dth > 3.84 else "allowed"))
    P(f"  {vk:38s}: " + "; ".join(f"{ak} L95 {v['L95_fine']:.2f} pc, thermal {v['L_thermal']:.2f} pc dchi2 {v['dchi2_thermal']:.2f}"
                                    f" [{v['thermal_class']}]" for ak, v in S3[vk].items()))
RES["S3_S4_CFG820"] = S3

# D8b: Stilp sigma_m2 statistics -> L* = sigma^2/a0 at the native a0 vs the floor at the same a0
d8b = J("doors_push_2026_10_22", "D8b_sigma_universality", "d8b_sigma_universality_results.json")
SIGS = {"sigma_m2 median": 9.30, "sigma_m2 5th pct": 7.81, "sigma_m2 min (DDO 125)": 7.00, "sigma_central median": 7.70}
P("  D8b at native a0 (floor = record CFG820 estimator at the same a0): " + "; ".join(
    f"{k} -> L* {(s * 1e3) ** 2 / NAT_C / PC8:.1f} pc" for k, s in SIGS.items())
  + f"; floor {S3['record (nu_RAR+EFE, Ups 1.6)']['native_c']['L95_fine']:.2f} pc")
RES["S3_D8b_native"] = {k: (s * 1e3) ** 2 / NAT_C / PC8 for k, s in SIGS.items()}
RES["S3_D8b_record_floor_pc"] = d8b.get("cfg820_floor_pc")

# ================================================================================ S6/S3 D6 u: native h, SPS, r_sp
P("\n=== S6  D6's u inputs: LCDM distances (h = 0.70) -> native h, SPS M* +-0.2 dex, NFW r_sp machinery bracket")
t = time.time()
D6 = R("doors_push_2026_10_22", "D6_u_mechanism", "d6_u_mechanism.py")
NS6 = exec_until(D6, "TM = tercile_masks()", patches=[("np.savez(TAB", "(lambda *a, **k: None)(TAB")], name="d6_ro")
src6 = open(D6).read()
qa = "#" + src6.split("# ============================================================================== Q3a")[1].split("Q3A = {}")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(qa, D6, "exec"), NS6)
umid0 = NS6["UD"]["canonical"]["MID"][0]
ug0 = NS6["u_gal"](NS6["galaxy_parts"]("canonical", 0.0))[0]
check("K5", abs(umid0 - 0.47157) < 1e-3 and abs(ug0 - 0.660) < 0.002, f"{umid0:.5f},{ug0:.4f}",
      "0.47157+-1e-3, 0.660+-0.002", "D6 reproduced: cluster u_MID and KiDS u_gal (canonical)")
S6 = {"u_MID_record": umid0, "u_gal_record": ug0}
# (a) SPS M* +-0.2 dex on u_gal
S6["u_gal_sps_full"] = {f"{d:+.1f}": {ft: dict(zip(("u", "sigma"), NS6["u_gal"](NS6["galaxy_parts"](ft, d))))
                                       for ft in ("canonical", "alt")} for d in (-0.2, 0.2)}
for v in S6["u_gal_sps_full"].values():
    for r_ in v.values():
        r_["z_vs_0p4716"] = (r_["u"] - 0.4716) / r_["sigma"]
S6["u_gal_sps"] = {d: {ft: r_["u"] for ft, r_ in v.items()} for d, v in S6["u_gal_sps_full"].items()}
P(f"  u_gal (canonical/alt) record {ug0:.3f}/{NS6['u_gal'](NS6['galaxy_parts']('alt', 0.0))[0]:.3f}; M* -0.2 dex: "
  f"{S6['u_gal_sps']['-0.2']['canonical']:.3f}/{S6['u_gal_sps']['-0.2']['alt']:.3f}; +0.2 dex: "
  f"{S6['u_gal_sps']['+0.2']['canonical']:.3f}/{S6['u_gal_sps']['+0.2']['alt']:.3f}; z vs 0.4716 at -0.2 dex: "
  f"{S6['u_gal_sps_full']['-0.2']['canonical']['z_vs_0p4716']:+.2f}/{S6['u_gal_sps_full']['-0.2']['alt']['z_vs_0p4716']:+.2f}")
# (b) native h on u_gal: R -> sR, ESD -> ESD/s, M* -> s^2 M*, s = 0.70/h_native (B21 is h70, flat LCDM Om 0.2793)
R0_, Y0_, S0_, CG0, ZK0 = NS6["R_"].copy(), NS6["Y_"].copy(), NS6["S_"].copy(), NS6["CG"].copy(), list(NS6["ZK"])
S6["u_gal_native_h"] = {}
for hk, H in (("A46_3pt", HN["A46_3pt"]), ("A46_map", HN["A46_map"]), ("A46_2pt", HN["A46_2pt"]),
              ("Planck_67.4", 67.4), ("SH0ES_73.0", 73.0)):
    s = 70.0 / H
    NS6["R_"], NS6["Y_"], NS6["S_"], NS6["CG"] = R0_ * s, Y0_ / s, S0_ / s, CG0 / s ** 2
    NS6["ZK"] = [z + 2 * math.log10(s) for z in ZK0]
    NS6["A0"]["native"] = a0_of_H(H)
    row = {}
    for ft in ("canonical", "native"):
        u, su = NS6["u_gal"](NS6["galaxy_parts"](ft, 0.0))
        row[ft] = dict(u=u, sigma=su, z_vs_0p4716=(u - 0.4716) / su)
    S6["u_gal_native_h"][hk] = dict(s=s, **row)
    P(f"  u_gal at native h ({hk}, s = {s:.3f}): a0 canonical {row['canonical']['u']:.3f} +- {row['canonical']['sigma']:.3f} "
      f"({row['canonical']['z_vs_0p4716']:+.1f} sigma vs 0.4716); a0 native {row['native']['u']:.3f} ({row['native']['z_vs_0p4716']:+.1f})")
NS6["R_"], NS6["Y_"], NS6["S_"], NS6["CG"], NS6["ZK"] = R0_, Y0_, S0_, CG0, ZK0
NS6["A0"].pop("native", None)
# (c) cluster u_MID: native h on the CFG687 stack (R500 -> sR500, Mgas -> s^2.5 Mgas, bins -> sRC, D,E -> /s) and f_s +-0.2 dex
baryon, dsigma, rho_of, NU, G, MPCd = NS6["baryon"], NS6["dsigma"], NS6["rho_of"], NS6["NU"], NS6["G"], NS6["MPC"]
RM, W0, D0, E0, MID, ALL = NS6["RM"], NS6["W"], NS6["D"], NS6["E"], NS6["MID"], NS6["ALL"]
R500, MG, RC0, NCL = NS6["R500"], NS6["MG"], NS6["RC"], NS6["NCL"]


def u_mid_stack(a0, s=1.0, fs=0.20, step=1):
    idx = np.arange(0, NCL, step)
    PLs, PNs = np.zeros((NCL, 8)), np.zeros((NCL, 8))
    for i in idx:
        Mb = baryon(R500[i] * s, MG[i] * s ** 2.5, fs=fs); gb = G * Mb / RM ** 2
        ML = gb * NU(gb / a0) * RM ** 2 / G
        PLs[i] = dsigma(ML, rho_of(ML), RC0 * s); PNs[i] = dsigma(Mb, rho_of(Mb), RC0 * s)
    m = np.zeros(NCL, bool); m[idx] = True
    Wm, Dm = W0 * s ** 2, D0 / s
    num = (Wm[m][:, MID] * (PLs[m][:, MID] - PNs[m][:, MID])).sum()
    den = (Wm[m][:, MID] * (Dm[m][:, MID] - PNs[m][:, MID])).sum()
    return float(num / den)


base = u_mid_stack(A0_CAN_X)
S6["u_MID_recomputed"] = base
S6["u_MID_variants"] = {}
for lab, kw in (("native h (A46_3pt) + native a0", dict(a0=NAT_C, s=70.0 / HN["A46_3pt"])),
                ("h = 0.674 (Planck), canonical a0", dict(a0=A0_CAN_X, s=70.0 / 67.4)),
                ("h = 0.730 (SH0ES), canonical a0", dict(a0=A0_CAN_X, s=70.0 / 73.0)),
                ("native h (A46_2pt) + native a0", dict(a0=NAT_LO, s=70.0 / HN["A46_2pt"])),
                ("native a0 only", dict(a0=NAT_C)),
                ("f_s 0.20 -> -0.2 dex", dict(a0=A0_CAN_X, fs=0.20 * 10 ** -0.2)),
                ("f_s 0.20 -> +0.2 dex", dict(a0=A0_CAN_X, fs=0.20 * 10 ** 0.2))):
    S6["u_MID_variants"][lab] = u_mid_stack(**kw)
S6["du_MID_dlnh"] = (S6["u_MID_variants"]["h = 0.730 (SH0ES), canonical a0"] - S6["u_MID_variants"]["h = 0.674 (Planck), canonical a0"]) / math.log(73.0 / 67.4)
P(f"  d u_MID / d ln h (canonical a0, 0.674 -> 0.730) = {S6['du_MID_dlnh']:+.3f}")
P(f"  u_MID (canonical) recomputed {base:.4f} (D6 0.4716 +- 0.0362): " + "; ".join(
    f"{k} {v:.4f} ({(v - base) / 0.0362:+.2f} sigma)" for k, v in S6["u_MID_variants"].items()))
# (d) r_sp machinery (NFW c = 4.5, r_sp = 0.83 r200m) bracket in D6's H-VR profile test, eps = 1, canonical
SS = NS6["SS"]; s1 = SS[f"{1.0:.4f}"]
xt, ut = NS6["u_table"](s1, "H-VR")
RSP0 = NS6["RSPi"].copy()
stats = __import__("scipy").stats
S6["HVR_rsp_bracket"] = {}
for fr in (1.0, 0.8, 1.25):
    NS6["RSPi"] = RSP0 * fr
    Dp = NS6["cluster_model"]("canonical", xt, ut, s1["lsp"])
    mstk = NS6["STK"](ALL, Dp); r = NS6["DSTK"] - mstk; chi2 = float(r @ NS6["CINV"] @ r)
    plf = NS6["PL"]; PN = NS6["PN"]
    num = (W0[:, MID] * (plf[:, MID] - PN[:, MID])).sum(); den = (W0[:, MID] * (Dp[:, MID] - PN[:, MID])).sum()
    S6["HVR_rsp_bracket"][f"{fr:g}"] = dict(u_MID=float(num / den), chi2=chi2, p=float(stats.chi2.sf(chi2, 8)))
    P(f"  H-VR eps=1 canonical, r_sp x {fr:g}: u_MID {num / den:.3f}, chi2 {chi2:.1f}/8 (p {stats.chi2.sf(chi2, 8):.1e})")
NS6["RSPi"] = RSP0
RES["S6_D6"] = S6
P(f"  (S6 took {time.time() - t:.0f} s)")

# ================================================================================ S7 Omega_c/Omega_b
P("\n=== S7  Omega_c/Omega_b = 5.3643 (Planck LCDM fit) -> CFG886 Planck-free values, on A18's R_req = 5.552 +- 0.427")
RREQ = (5.552, 0.427)
S7 = {}
for lab, (v, sv) in (("Planck 5.3643", (5.3643, 0.0)), ("CFG886 (a) BAO+BBN", (5.272, 0.218)),
                     ("CFG886 (b) SH0ES", (6.122, 0.321))):
    zz = (RREQ[0] - v) / math.hypot(RREQ[1], sv)
    S7[lab] = dict(ratio=v, sigma=sv, z_Rreq_minus_ratio=zz, u_scale=5.3643 / v)
    P(f"  {lab:20s}: R_req - ratio = {zz:+.2f} sigma; a u defined per unit 5.3643 rescales by {5.3643 / v:.4f}")
RES["S7"] = S7

# ================================================================================ K6 ledger
P("\n=== K6  ledger completeness")
LED = os.path.join(HERE, "INPUT_LEDGER.md")
CLASSES = {"RAW", "FRAMEWORK-NATIVE", "SURVEY-CALIBRATION", "LCDM-PROCESSED", "STANDARD-MOND-MACHINERY"}
VERD = ["D1", "D2", "D4", "D5", "D6", "D7", "D7b", "D7c", "D8", "D8b"]
rows, bad = [], []
if os.path.exists(LED):
    for line in open(LED):
        if not re.match(r"^\| I\d+ ", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            bad.append(cells[0]); continue
        rid, inp, cls, src, used = cells[:5]
        cls_ok = cls.replace("ΛCDM", "LCDM").split()[0] in CLASSES if cls else False
        paths = re.findall(r"`([^`]+)`", src)
        p_ok = bool(paths) and all(os.path.exists(R(p.split(":")[0])) for p in paths)
        if not (cls_ok and p_ok):
            bad.append(rid)
        rows.append((rid, cls, used))
covered = {v: any(re.search(rf"\b{re.escape(v)}\b", u) for _, _, u in rows) for v in VERD}
k6 = bool(rows) and not bad and all(covered.values())
check("K6", k6, f"rows={len(rows)} bad={bad} uncovered={[v for v, c in covered.items() if not c]}", "all classed, paths exist, all verdicts covered",
      "INPUT_LEDGER.md complete")
RES["ledger"] = dict(n_rows=len(rows), bad=bad, covered=covered)

# ================================================================================ close
npass = sum(c["pass_"] for c in CHECKS)
RES["checks"] = CHECKS
RES["runtime_s"] = time.time() - T0
P(f"\n{LANE} COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"e1_input_audit_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"e1_input_audit{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
