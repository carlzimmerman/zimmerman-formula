"""GD1_route_e_mw_dr4: the flagship's (law + cold dark energy, route E) Milky Way numbers for Gaia DR4.

Route E: gravity Newtonian, the galaxy law emergent from cold dark energy halos Burkert-cored at
rho0 r0 = a0/(2 pi G) (X38; X43's collapse branch is inactive below 10^12.1 / 10^12.4 Msun).
M200 from EM1's committed SPARC relation lgM200 = a + b (lgMb - 10), borrowed, not refit.
Baryons = S3's McMillan 2017 B1 field, recovered from the sealed NFW rival by subtracting its analytic NFW halo
(S3 SEALED_V3_MW_DR4.json, read only). Stars x s over S3's five-value band; footings never pooled.
kappa = 1/2 FITTED. No dark-matter particle. Predictions, not results. Not theory closed.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 gd1_route_e_mw.py [--mutate]
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar

MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

G = 4.30091e-6                       # kpc (km/s)^2 / Msun, as S3
KZU = 2 * math.pi * G * 1e6          # S3's unit: K_z/(2 pi G) in Msun/pc^2
SEAL = json.load(open(os.path.join(REB, "S3_v3_mw_seals", "SEALED_V3_MW_DR4.json")))
X38 = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
EM1 = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
R0 = SEAL["inputs"]["R0_kpc"]
FEET = ("canonical", "alt")
SIG = {f: X38["Sigma_Msun_pc2"][f] * 1e6 for f in FEET}          # Msun/kpc^2
BGS = {t: dict(a=EM1["rows"][t]["R1"]["a"], b=EM1["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
P("GD1_route_e_mw_dr4", "MUTATE (Sigma x 2)" if MUTATE else "normal run")
P("route E: Newtonian + cold dark energy Burkert halo, rho0 r0 = a0/(2 pi G); kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"Sigma_a0 canonical {SIG['canonical']/1e6:.1f} / alt {SIG['alt']/1e6:.1f} Msun/pc^2; R0 {R0} kpc")

# ------------------------------------------------------------------ NFW rival (S3) -> baryon-only field
def nfw(M200, c, h0n=67.7):
    rc = 3 * (h0n / 1e3) ** 2 / (8 * math.pi * G); r200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); rs = r200 / c
    m = math.log(1 + c) - c / (1 + c); rhos = M200 / (4 * math.pi * rs ** 3 * m)
    return lambda r: G * 4 * math.pi * rhos * rs ** 3 * (np.log1p(r / rs) - (r / rs) / (1 + r / rs)) / r ** 2
def B(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def solve_r0(Mtot, Rout, Sig):                                   # X38's A1 compact root
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(pk.x) < math.log(Mtot):
        return math.exp(pk.x), True
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), pk.x, xtol=1e-14)), False
def slope_even(R, V, lo, hi):                                    # S3's definition
    m = (R >= lo - 1e-9) & (R <= hi + 1e-9); return float(np.polyfit(np.log(R[m]), np.log(V[m]), 1)[0])

checks = []
RES = dict(lane="GD1_route_e_mw_dr4", mutate=MUTATE, Sigma_Msun_pc2={f: SIG[f] / 1e6 for f in FEET}, rows={}, checks={})
for sk in sorted(SEAL["NFW_Ou24"]):
    n = SEAL["NFW_Ou24"][sk]; gh = nfw(n["M200"], n["c"])
    Rv = np.array(sorted(float(k[1:]) for k in n["P2_Vc"])); Vt = np.array([n["P2_Vc"][f"R{r:.0f}"] for r in Rv])
    R5 = np.array([30.0, 40, 50, 60]); V5 = np.array([n["P5_Vc"][f"R{r:.0f}"] for r in R5])
    RR = np.concatenate([Rv, R5]); VB2 = np.concatenate([Vt ** 2 - Rv * gh(Rv), V5 ** 2 - R5 * gh(R5)])
    kz_t = n["P3"]["Kz_R0_1p1_over_2piG"]; rr = math.hypot(R0, 1.1)
    kz_b = kz_t - float(gh(np.array([rr]))[0]) * 1.1 / rr / KZU
    rho_b = n["P3"]["rho_tot_R0_Msun_pc3"] - n["P3"]["dark_Msun_pc3"]
    colb = n["P3"]["Sigma_tot_1p1_Msun_pc2"] - n["P3"]["Sigma_dark_1p1_Msun_pc2"]
    # K1: rebuild the rival from the baryon field and match S3's sealed slope (integer grid + 0.5 kpc interp)
    Rg = np.arange(15.0, 27.51, 0.5); vb2g = np.interp(Rg, RR[np.argsort(RR)], VB2[np.argsort(RR)])
    s_nfw = slope_even(Rg, np.sqrt(vb2g + Rg * gh(Rg)), 15, 27.5)
    checks.append(("K1_rebuild_" + sk, abs(s_nfw - n["P2_slope_15_27p5"]) < 2e-3))
    Mb = VB2[RR == 60.0][0] * 60.0 / G                             # spherical estimate of baryon mass inside 60 kpc
    row = dict(Mb_60kpc=Mb, baryon_Kz_R0_1p1=kz_b, rival_slope_rebuilt=s_nfw, rival_slope_sealed=n["P2_slope_15_27p5"])
    for f in FEET:
        for t, bg in BGS.items():
            Sig = SIG[f] * (2.0 if MUTATE else 1.0)
            lM = bg["a"] + bg["b"] * (math.log10(Mb) - 10); M200 = 10 ** lM
            rc = 3 * (100 * bg["h"] / 1e3) ** 2 / (8 * math.pi * G); R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
            r0, sat = solve_r0(M200, R200, Sig)
            gB = lambda r: G * math.pi * Sig * r0 ** 2 * B(r / r0) / r ** 2
            V = lambda R: np.sqrt(np.interp(R, RR[np.argsort(RR)], VB2[np.argsort(RR)]) + R * gB(R))
            kz = kz_b + float(gB(rr)) * 1.1 / rr / KZU
            rho0 = Sig / r0                                          # Msun/kpc^3
            rhoR0 = rho0 / ((1 + R0 / r0) * (1 + (R0 / r0) ** 2)) / 1e9   # Msun/pc^3
            zw = np.linspace(-1.1, 1.1, 441); x = np.hypot(R0, zw) / r0
            col = float(np.trapz(rho0 / ((1 + x) * (1 + x * x)), zw)) / 1e6
            row[f"{f}|{t}"] = dict(lgM200=lM, r0_kpc=r0, saturated=sat, V8=float(V(np.array([R0]))[0]), V20=float(V(np.array([20.0]))[0]),
                                   V60=float(V(np.array([60.0]))[0]), mean_30_60=float(np.mean(V(np.arange(30.0, 60.01, 2.5)))),
                                   slope_15_22=slope_even(Rg, V(Rg), 15, 22), slope_15_27p5=slope_even(Rg, V(Rg), 15, 27.5),
                                   Kz_R0_1p1_over_2piG=kz, rho_dark_R0_Msun_pc3=rhoR0, rho_dark_R0_GeV_cm3=rhoR0 * 37.97,
                                   rho_tot_R0_Msun_pc3=rho_b + rhoR0, Sigma_tot_1p1=colb + col, Sigma_dark_1p1=col,
                                   P6_azimuthal_A=0.0, wide_binary_gamma_v=1.0)
    RES["rows"][sk] = row

# ------------------------------------------------------------------ headline (s = 1, band over s), bg A primary
K = ("V20", "slope_15_22", "slope_15_27p5", "Kz_R0_1p1_over_2piG", "rho_tot_R0_Msun_pc3", "rho_dark_R0_GeV_cm3", "V60", "mean_30_60", "V8", "lgM200", "r0_kpc")
RES["headline"] = {}
for f in FEET:
    for t in BGS:
        h = {}
        for k in K:
            vals = [RES["rows"][sk][f"{f}|{t}"][k] for sk in sorted(RES["rows"])]
            h[k] = dict(central=RES["rows"]["1.000000"][f"{f}|{t}"][k], lo=min(vals), hi=max(vals))
        RES["headline"][f"{f}|{t}"] = h
        P(f"\n[{f} | bg {t}]  lgM200 {h['lgM200']['central']:.2f}, r0 {h['r0_kpc']['central']:.2f} kpc, saturated {any(RES['rows'][s][f'{f}|{t}']['saturated'] for s in RES['rows'])}")
        for k in K[:9]:
            P(f"  {k:<22} {h[k]['central']:9.4f}  ({h[k]['lo']:.4f} – {h[k]['hi']:.4f})")
n1 = SEAL["NFW_Ou24"]["1.000000"]
P(f"\nrival NFW (S3 sealed, s=1): V20 {n1['P2_Vc']['R20']:.1f}, slope 15-27.5 {n1['P2_slope_15_27p5']:+.3f}, Kz {n1['P3']['Kz_R0_1p1_over_2piG']:.1f}, rho_tot {n1['P3']['rho_tot_R0_Msun_pc3']:.3f}, V60 {n1['P5_Vc']['R60']:.1f}")
P(f"baryons only (s=1): Kz {RES['rows']['1.000000']['baryon_Kz_R0_1p1']:.1f} Msun/pc^2; Mb(<60 kpc) {RES['rows']['1.000000']['Mb_60kpc']:.3e} Msun")

# ------------------------------------------------------------------ structural cap + today's data (reported; DR3-era record targets)
Bx = minimize_scalar(lambda x: -float(B(x)) / (2 * x * x), bounds=(0.01, 50), method="bounded")
CAP = -Bx.fun                                                       # max g_halo / (2 pi G Sigma) = max g_halo / a0
A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; KPC = 3.0857e19
ou = np.loadtxt(os.path.join(REB, "..", "real_research", "data", "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14)
OR, OV = ou[:, 0], ou[:, 1]; OE = np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(OR <= 22.0, 0.03, 0.15) * OV)   # S3's error model
VC_E, VC_E_ERR, KZ_BR, KZ_BR_ERR = 229.053, 4.645, 66.4, 2.2                    # X5's targets (Eilers+19; Bovy & Rix 2013)
RES["today"] = dict(cap_g_over_a0=CAP, cap_at_R_over_r0=float(Bx.x))
P(f"\nSTRUCTURAL: an a0-cored Burkert pulls at most {CAP:.4f} a0 anywhere (at R/r0 = {Bx.x:.3f}), for ANY M200")
for f in FEET:
    vcap = math.sqrt(CAP * A0SI[f] * R0 * KPC) / 1e3
    rb = RES["rows"]["1.000000"]; vb = math.sqrt(max(rb[f"{f}|A_c2b_refit"]["V8"] ** 2 - 0, 0))
    hb_ = rb[f"{f}|A_c2b_refit"]
    # rotation curve chi2 vs Ou+24 (S3 error model), s = 1, bg A
    n = SEAL["NFW_Ou24"]["1.000000"]; gh = nfw(n["M200"], n["c"])
    Rv = np.array(sorted(float(k[1:]) for k in n["P2_Vc"])); Vt = np.array([n["P2_Vc"][f"R{r:.0f}"] for r in Rv])
    vb2 = np.interp(OR, Rv, Vt ** 2 - Rv * gh(Rv))
    lM = BGS["A_c2b_refit"]["a"] + BGS["A_c2b_refit"]["b"] * (math.log10(rb["Mb_60kpc"]) - 10)
    r0 = hb_["r0_kpc"]; Sg = SIG[f] * (2.0 if MUTATE else 1.0)
    VE = np.sqrt(vb2 + OR * G * math.pi * Sg * r0 ** 2 * B(OR / r0) / OR ** 2)
    chi2 = float(np.sum(((VE - OV) / OE) ** 2))
    zvc = (hb_["V8"] - VC_E) / VC_E_ERR; zkz = (hb_["Kz_R0_1p1_over_2piG"] - KZ_BR) / KZ_BR_ERR
    vb_need = math.sqrt(VC_E ** 2 - vcap ** 2)
    RES["today"][f] = dict(V_halo_cap_R0=vcap, V_needed_halo_R0=math.sqrt(VC_E ** 2 - (hb_["V8"] ** 2 - (hb_["V8"] ** 2 - float(np.interp(R0, Rv, Vt ** 2 - Rv * gh(Rv)))))),
                           Vbar_R0=math.sqrt(float(np.interp(R0, Rv, Vt ** 2 - Rv * gh(Rv)))), z_vc_R0=zvc, z_Kz=zkz, chi2_Ou24=chi2, N_Ou24=len(OR),
                           baryon_mass_factor_needed=(vb_need ** 2) / float(np.interp(R0, Rv, Vt ** 2 - Rv * gh(Rv))))
    t_ = RES["today"][f]
    P(f"[{f}] halo cap V_h(R0) {vcap:.1f} km/s vs needed {t_['V_needed_halo_R0']:.1f} (Vbar {t_['Vbar_R0']:.1f}); "
      f"v_c(R0) {hb_['V8']:.1f} vs Eilers {VC_E} +- {VC_E_ERR}: z {zvc:+.1f}; Kz {hb_['Kz_R0_1p1_over_2piG']:.1f} vs Bovy&Rix {KZ_BR} +- {KZ_BR_ERR}: z {zkz:+.1f}; "
      f"chi2 vs Ou+24 {chi2:.0f} / {len(OR)}; baryons x{t_['baryon_mass_factor_needed']:.2f} needed at R0 to reach Eilers")

# K2: Newtonian limit (Sigma -> tiny) returns the baryon Kz; K3 Burkert mass at R200 = M200 (non-saturated)
hb = RES["rows"]["1.000000"]["canonical|A_c2b_refit"]
checks.append(("K2_no_saturation", not any(RES["rows"][s][k]["saturated"] for s in RES["rows"] for k in RES["rows"][s] if "|" in k)))
checks.append(("K3_halo_raises_Kz", hb["Kz_R0_1p1_over_2piG"] > RES["rows"]["1.000000"]["baryon_Kz_R0_1p1"]))
checks.append(("K4_sigma_matches_X38", abs(SIG["canonical"] / 1e6 - 106.879) < 0.01 and abs(SIG["alt"] / 1e6 - 129.165) < 0.01))
Rs_ = np.linspace(0.1, 300.0, 30000); Sg_ = SIG["canonical"] * (2.0 if MUTATE else 1.0)
gmax = float(np.max(G * math.pi * Sg_ * hb["r0_kpc"] ** 2 * B(Rs_ / hb["r0_kpc"]) / Rs_ ** 2)) / (2 * math.pi * G * SIG["canonical"])
checks.append(("K5_solved_halo_obeys_cap", gmax <= CAP * (1 + 1e-6)))           # --mutate (Sigma x 2) must FAIL this
P(f"max over R of g_halo / a0 for the solved MW halo (canonical, s=1): {gmax:.4f} (cap {CAP:.4f})")
for k, v in checks:
    P(f"{k}: {'PASS' if v else 'FAIL'}"); RES["checks"][k] = bool(v)
json.dump(RES, open(os.path.join(HERE, f"gd1_route_e_mw_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"gd1_route_e_mw{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v for _, v in checks) else 1)
