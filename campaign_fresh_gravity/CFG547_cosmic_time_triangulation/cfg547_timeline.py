#!/usr/bin/env python3
"""CFG547: cosmic-time triangulation of dark energy, cold energy and galaxy baryons.

Criteria: FROZEN_CRITERIA.md (committed alone first, 55cf38038). On-disk data only: DESI DR2 w0wa chains (read as CFG511),
the RC100 corrected table, CFG303's per-galaxy native baryons. Typical-galaxy scalings are recalled and PROVISIONAL.
kappa = 1/2 FITTED; the cold energy's mass is required. Footings scored separately, never pooled.

Run:   nice -n 10 python3 cfg547_timeline.py                -> cfg547.out, cfg547_results.json, cfg547_timeline.png
       CFG547_MUTATE=1 nice -n 10 python3 cfg547_timeline.py -> cfg547_MUTATE.out, cfg547_results_MUTATE.json
"""
import os, sys, json, math, csv
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CHAINS = os.path.abspath(os.path.join(REPO, "..", "_external_data", "desi_dr2_chains"))
RC100 = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv")
NAT = os.path.join(REPO, "campaign_fresh_gravity", "CFG303_lcdm_free_inputs", "cfg303_rc100_pergalaxy_LCDMFREE.csv")
MUTATE = os.environ.get("CFG547_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = open(os.path.join(HERE, f"cfg547{TAG}.out"), "w")

def P(s=""):
    print(s); OUT.write(s + "\n"); OUT.flush()

# ------------------------------------------------------------------ constants
G = 6.674e-11; C = 2.998e8; KPC = 3.0857e19; MSUN = 1.989e30; GYR = 3.15576e16
H0K = 67.4; H0 = H0K * 1e3 / 3.0857e22; OM = 0.315; OL = 1 - OM
KAPPA = 0.5
FOOT = {"canonical": 9.36e-11, "alt": 1.13e-10}
FB = 1 / (1 + 5.364)
G_KPC = 4.30091e-6; XN = 1.678                       # CFG216 disc_v2 constants
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G)

def nu(y):
    y = np.asarray(y, float)
    return 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))

def E(z):
    return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3 + OL)

def age_gyr(z):
    return 2 / (3 * H0 * math.sqrt(OL)) * np.arcsinh(math.sqrt(OL / OM) * (1 + np.asarray(z, float)) ** -1.5) / GYR

def disc_v2(M, Re, Rr):                               # CFG216 committed thin exponential disc, (km/s)^2
    Rd = Re / XN; y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))

def gbar_si(M, Re, R):                                # m/s^2
    return disc_v2(M, Re, R) / R * 1e6 / KPC

def mu_t18(z, logm):                                  # CFG217 verbatim
    return 10 ** (0.06 - 3.3 * (math.log10(1 + z) - 0.65) ** 2 - 0.41 * (logm - 10.7))

def cpl_f(z, w0, wa):                                 # CFG508 cpl_f, copied
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def wpct(v, wt, qs=(0.16, 0.5, 0.84)):
    o = np.argsort(v); cw = np.cumsum(wt[o]); cw /= cw[-1]
    return [float(np.interp(q, cw, v[o])) for q in qs]

checks = {}
def check(k, ok, msg):
    checks[k] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {k} {msg}")

J = dict(lane="CFG547", criteria_commit="55cf38038", mutate=MUTATE,
         notes="kappa = 1/2 FITTED; cold energy mass required; footings never pooled; scalings PROVISIONAL; not theory closed")
P("CFG547 cosmic-time triangulation" + (" [MUTATE]" if MUTATE else ""))

# ------------------------------------------------------------------ controls K1, K4, K5
P("\n[controls]")
a0c = KAPPA * C * math.sqrt(G * 0.685 * RHOC0)
check("K1", abs(a0c / 9.36e-11 - 1) < 0.005, f"kappa c sqrt(G rho_L) = {a0c:.4e} vs 9.36e-11")
zacc_L = (2 * OL / OM) ** (1 / 3) - 1; zeq_L = (OL / OM) ** (1 / 3) - 1
qfun = lambda z: (OM * (1 + z) ** 3 - 2 * OL) / (2 * E(z) ** 2)
from scipy.optimize import brentq
zacc_num = brentq(qfun, 0, 3); zeq_num = brentq(lambda z: OM * (1 + z) ** 3 - OL, 0, 3)
check("K4", abs(zacc_num - zacc_L) < 1e-3 and abs(zeq_num - zeq_L) < 1e-3, f"Lambda z_acc {zacc_L:.3f}, z_eq {zeq_L:.3f}")
t0 = float(age_gyr(0.0))
check("K5", abs(t0 - 13.80) < 0.15, f"age t(0) = {t0:.3f} Gyr")

# ------------------------------------------------------------------ DESI chains
P("\n[DESI DR2 chains]")
ZD = np.round(np.arange(0, 6.0001, 0.05), 4)
desi = {}
for nm in ("cmb", "pantheonplus", "union3", "desy5"):
    fn1 = os.path.join(CHAINS, nm, "chain.1.txt")
    hdr = open(fn1).readline().lstrip("#").split()
    cols = [hdr.index(c) for c in ("weight", "w", "wa", "omegam")]
    xs = []
    for kk in range(1, 5):
        d = np.loadtxt(os.path.join(CHAINS, nm, f"chain.{kk}.txt"), usecols=cols)
        xs.append(d[int(0.3 * len(d)):])
    x = np.vstack(xs); wt, w0, wa, Om = x[:, 0], x[:, 1], x[:, 2], x[:, 3]
    rr = np.array([wpct(cpl_f(z, w0, wa), wt) for z in ZD])            # rho_DE ratio 16/50/84
    ar = np.array([wpct(np.sqrt(cpl_f(z, w0, wa)), wt) for z in ZD])   # a0 ratio
    mw0, mwa, mOm = wpct(w0, wt)[1], wpct(wa, wt)[1], wpct(Om, wt)[1]
    # chain-median point: z_eq, z_acc
    fz = lambda z: cpl_f(z, mw0, mwa)
    wz = lambda z: mw0 + mwa * z / (1 + z)
    zeq = brentq(lambda z: mOm * (1 + z) ** 3 - (1 - mOm) * fz(z), 0, 5)
    qz = lambda z: mOm * (1 + z) ** 3 + (1 + 3 * wz(z)) * (1 - mOm) * fz(z)
    try:
        zacc = brentq(qz, 0, 5)
    except ValueError:
        zacc = float("nan")
    desi[nm] = dict(n=int(len(wt)), w0=mw0, wa=mwa, Om=mOm, rho_ratio=rr.tolist(), a0_ratio=ar.tolist(), z_eq=zeq, z_acc=zacc,
                    q0_median_point=float(qz(0.0) / 2))
    i25 = int(np.argmin(abs(ZD - 2.5)))
    P(f"  {nm:<13} n={len(wt)} w0={mw0:+.3f} wa={mwa:+.3f} Om={mOm:.3f}  a0(2.5)/a0(0) median {ar[i25,1]:.3f} "
      f"[{ar[i25,0]:.3f},{ar[i25,2]:.3f}]  z_eq {zeq:.3f} z_acc {zacc:.3f}")
ref = dict(pantheonplus=0.827, union3=0.782, desy5=0.798)
i25 = int(np.argmin(abs(ZD - 2.5)))
check("K3", all(abs(desi[n]["a0_ratio"][i25][1] - ref[n]) <= 0.01 for n in ref),
      "DESI a0(2.5)/a0(0) medians vs CFG511 " + ", ".join(f"{n} {desi[n]['a0_ratio'][i25][1]:.3f}/{ref[n]}" for n in ref))
A_med = np.median(np.array([np.array(desi[n]["a0_ratio"])[:, 1] for n in desi]), axis=0)
A_lo = np.min(np.array([np.array(desi[n]["a0_ratio"])[:, 0] for n in desi]), axis=0)
A_hi = np.max(np.array([np.array(desi[n]["a0_ratio"])[:, 2] for n in desi]), axis=0)
R_med = np.median(np.array([np.array(desi[n]["rho_ratio"])[:, 1] for n in desi]), axis=0)
R_lo = np.min(np.array([np.array(desi[n]["rho_ratio"])[:, 0] for n in desi]), axis=0)
R_hi = np.max(np.array([np.array(desi[n]["rho_ratio"])[:, 2] for n in desi]), axis=0)
desi_ratio = lambda z: np.interp(z, ZD, A_med)
J["desi"] = desi
J["desi_envelope"] = dict(z=ZD.tolist(), a0_ratio_med=A_med.tolist(), a0_ratio_lo=A_lo.tolist(), a0_ratio_hi=A_hi.tolist(),
                          rho_ratio_med=R_med.tolist(), rho_ratio_lo=R_lo.tolist(), rho_ratio_hi=R_hi.tolist())

def a0_model(model, z, foot):
    a = FOOT[foot]
    if model == "FLAT": return a * np.ones_like(np.asarray(z, float))
    if model == "DESI": return a * desi_ratio(z)
    if model == "RIVAL": return a * E(z)
    raise ValueError(model)

# ------------------------------------------------------------------ typical galaxies (PROVISIONAL scalings)
VDW = np.array([(0.25, 0.86, 0.25), (0.75, 0.78, 0.22), (1.25, 0.70, 0.22), (1.75, 0.65, 0.23), (2.25, 0.55, 0.22), (2.75, 0.51, 0.18)])
def Re_kpc(z, logm):
    if z < 0.25:
        lA = 0.86 - 0.75 * math.log10((1 + z) / 1.25); al = 0.25
    elif z > 2.75:
        lA = 0.51 - 0.75 * math.log10((1 + z) / 3.75); al = 0.18
    else:
        lA = float(np.interp(z, VDW[:, 0], VDW[:, 1])); al = float(np.interp(z, VDW[:, 0], VDW[:, 2]))
    return 10 ** lA * (10 ** logm / 5e10) ** al

def typical(z, logm, foot, model="FLAT"):
    Re = Re_kpc(z, logm); mu = mu_t18(z, logm); Mb = 10 ** logm * (1 + mu)
    a0 = float(a0_model(model, z, foot))
    g = {k: float(gbar_si(Mb, Re, k * Re)) for k in (1, 2, 3)}
    Rd = Re / XN
    xs = np.linspace(0.02, 40, 8000); gg = gbar_si(Mb, Re, xs * Rd)
    above = np.where(gg >= a0)[0]
    if len(above) == 0:
        frac = 1.0; xcross = 0.0
    else:
        xcross = float(xs[above[-1]]); frac = float((1 + xcross) * math.exp(-xcross))
    fdm = float(1 - 1 / nu(g[1] / a0))
    gobs_Re = float(nu(g[1] / a0) * g[1])
    tff_Re = (math.pi / 2) * math.sqrt(Re * KPC / (2 * gobs_Re)) / GYR
    rM = math.sqrt(G * Mb * MSUN / a0) / KPC
    out = dict(z=z, logMstar=logm, Re_kpc=Re, mu_gas=mu, logMb=math.log10(Mb), a0=a0,
               g_over_a0_1Re=g[1] / a0, g_over_a0_2Re=g[2] / a0, g_over_a0_3Re=g[3] / a0,
               disc_mass_frac_in_law_regime=frac, x_cross_Rd=xcross, fDM_Re=fdm, tff_Re_Gyr=tff_Re, rM_kpc=rM)
    rhom = OM * RHOC0 * (1 + z) ** 3; rhocz = RHOC0 * E(z) ** 2
    for fr in (0.1, 1.0):
        redge = rM / math.log(1 + fr * FB / (1 - FB))
        gN = G * Mb * MSUN / (redge * KPC) ** 2; gob = float(nu(gN / a0) * gN)
        tff_e = (math.pi / 2) * math.sqrt(redge * KPC / (2 * gob)) / GYR
        Mta = Mb / (fr * FB) * MSUN
        rta = (3 * Mta / (4 * math.pi * 5.55 * rhom)) ** (1 / 3) / KPC
        r200 = (3 * Mta / (4 * math.pi * 200 * float(rhocz))) ** (1 / 3) / KPC
        out[f"fret{fr}"] = dict(r_edge_kpc=redge, tff_edge_Gyr=tff_e, logM_ta=math.log10(Mta / MSUN), r_ta_kpc=rta, r200c_kpc=r200,
                                edge_over_rta=redge / rta, edge_over_r200=redge / r200)
    return out

# ------------------------------------------------------------------ TIMELINE (descriptive)
P("\n[TIMELINE] DESCRIPTIVE. z grid 0..6 step 0.25; Lambda background Om 0.315 H0 67.4; scalings PROVISIONAL")
ZT = np.round(np.arange(0, 6.0001, 0.25), 3)
TL = []
for z in ZT:
    Ez = float(E(z)); Hz = H0 * Ez; t = float(age_gyr(z))
    rhoL = OL * RHOC0; rhom = OM * RHOC0 * (1 + z) ** 3
    ODE = OL / Ez ** 2
    row = dict(z=float(z), age_Gyr=t, lookback_Gyr=t0 - t, H_kms_Mpc=H0K * Ez, cH=C * Hz, rho_DE_Lambda=rhoL,
               rho_DE_DESI_ratio_med=float(np.interp(z, ZD, R_med)), rho_DE_DESI_ratio_lo=float(np.interp(z, ZD, R_lo)),
               rho_DE_DESI_ratio_hi=float(np.interp(z, ZD, R_hi)), rho_m=rhom, Omega_DE=ODE,
               a0_DESI_ratio_med=float(desi_ratio(z)), a0_DESI_ratio_lo=float(np.interp(z, ZD, A_lo)),
               a0_DESI_ratio_hi=float(np.interp(z, ZD, A_hi)), a0_RIVAL_ratio=Ez,
               a0_over_cH_canonical=FOOT["canonical"] / (C * Hz), a0_over_cH_alt=FOOT["alt"] / (C * Hz),
               a0_over_cH_tautology=KAPPA * math.sqrt(3 * ODE / (8 * math.pi)), cH_over_2pi=C * Hz / (2 * math.pi))
    row["gal"] = {f"{lm}_{ft}": typical(float(z), lm, ft) for lm in (10.0, 10.7) for ft in FOOT}
    TL.append(row)
P(f"  {'z':>4} {'t/Gyr':>6} {'rhoDE/rhom':>10} {'DESIrho':>7} {'a0/cH':>6} {'taut':>6} | M*=10.7 canon: {'Re':>5} {'mu':>5} "
  f"{'g/a0@Re':>7} {'@2Re':>6} {'@3Re':>6} {'fLaw':>5} {'fDM':>5} {'tffRe/t':>7} {'edge/rta':>8} {'tffE/t':>6} | 10.0: {'g/a0@Re':>7} {'fDM':>5}")
for r in TL:
    g = r["gal"]["10.7_canonical"]; g0 = r["gal"]["10.0_canonical"]
    P(f"  {r['z']:4.2f} {r['age_Gyr']:6.2f} {r['rho_DE_Lambda']/r['rho_m']:10.3f} {r['rho_DE_DESI_ratio_med']:7.3f} "
      f"{r['a0_over_cH_canonical']:6.3f} {r['a0_over_cH_tautology']:6.3f} | {g['Re_kpc']:5.2f} {g['mu_gas']:5.2f} {g['g_over_a0_1Re']:7.2f} "
      f"{g['g_over_a0_2Re']:6.2f} {g['g_over_a0_3Re']:6.2f} {g['disc_mass_frac_in_law_regime']:5.2f} {g['fDM_Re']:5.2f} "
      f"{g['tff_Re_Gyr']/r['age_Gyr']:7.3f} {g['fret0.1']['edge_over_rta']:8.3f} {g['fret0.1']['tff_edge_Gyr']/r['age_Gyr']:6.2f} | "
      f"{g0['g_over_a0_1Re']:7.2f} {g0['fDM_Re']:5.2f}")
P(f"  c H0/2pi = {C*H0/(2*math.pi):.3e}; a0/(cH0) canonical {FOOT['canonical']/(C*H0):.4f}, alt {FOOT['alt']/(C*H0):.4f}; "
  f"tautology kappa sqrt(3 Om_DE/8pi) at z=0 = {KAPPA*math.sqrt(3*OL/(8*math.pi)):.4f}; a0 = cH0/2pi iff Omega_DE = 2/(3 pi kappa^2) = {2/(3*math.pi*KAPPA**2):.3f}")
J["timeline"] = TL
J["tautology_C1"] = dict(a0_over_cH0_canonical=FOOT["canonical"] / (C * H0), a0_over_cH0_alt=FOOT["alt"] / (C * H0),
                         cH0_over_2pi=C * H0 / (2 * math.pi), OmegaDE_for_cH_over_2pi=2 / (3 * math.pi * KAPPA ** 2), label="TAUTOLOGICAL")

# ------------------------------------------------------------------ TEST (b) switch-on
P("\n[TEST b] switch-on epoch z_on: highest z (dz 0.01, z<=6) with g_bar(k Re)/a0(z) <= 1")
ZF = np.round(np.arange(0, 6.0001, 0.01), 3)
zon = {}
for model in ("FLAT", "DESI", "RIVAL"):
    for ft in FOOT:
        for lm in (10.0, 10.7):
            for k in (2, 3):
                vals = []
                for z in ZF:
                    Re = Re_kpc(float(z), lm); Mb = 10 ** lm * (1 + mu_t18(float(z), lm))
                    vals.append(float(gbar_si(Mb, Re, k * Re)) / float(a0_model(model, float(z), ft)) <= 1)
                vals = np.array(vals)
                if vals.all(): v = "> 6 (always in the law's regime)"; vnum = float("inf")
                elif not vals.any(): v = "never"; vnum = float("nan")
                else: vnum = float(ZF[np.where(vals)[0][-1]]); v = f"{vnum:.2f}"
                contiguous = bool(vals.any() and vals[: np.where(vals)[0][-1] + 1].all())
                zon[f"{model}_{ft}_{lm}_{k}Re"] = dict(z_on=vnum, label=v, contiguous_from_z0=contiguous)
for k_, v in zon.items():
    if True:
        P(f"  {k_:<28} z_on = {v['label']:<34} contiguous from z=0: {v['contiguous_from_z0']}")
flat8 = [v["z_on"] for k_, v in zon.items() if k_.startswith("FLAT")]
epochs = dict(Lambda_z_eq=zeq_L, Lambda_z_acc=zacc_L, **{f"{n}_z_eq": desi[n]["z_eq"] for n in desi}, **{f"{n}_z_acc": desi[n]["z_acc"] for n in desi})
def in_win(zr):
    return all(math.isfinite(z) and abs(z - zr) <= 0.15 for z in flat8)
cand = [nm for nm, zr in (("z_eq (Lambda)", zeq_L), ("z_acc (Lambda)", zacc_L)) if in_win(zr)]
verdict_b = "COINCIDENCE CANDIDATE (NOT DERIVED)" if cand else "NO ROBUST EPOCH"
P(f"  dark-energy epochs: " + ", ".join(f"{k_} {v:.3f}" for k_, v in epochs.items()))
P(f"  FLAT z_on (8): {['%.2f' % z if math.isfinite(z) else str(z) for z in flat8]}; spread "
  f"{(max(z for z in flat8 if math.isfinite(z)) - min(z for z in flat8 if math.isfinite(z))) if any(math.isfinite(z) for z in flat8) else float('nan'):.2f}")
P(f"  VERDICT (b): {verdict_b}" + (f" [{', '.join(cand)}]" if cand else ""))
J["test_b"] = dict(z_on=zon, epochs=epochs, flat8=flat8, verdict=verdict_b)

# ------------------------------------------------------------------ TEST (c) descriptive
P("\n[TEST c] DESCRIPTIVE candidates (no data test)")
tc = {}
for lm in (10.0, 10.7):
    for ft in FOOT:
        key = f"{lm}_{ft}"
        e_r = [r["gal"][key]["fret0.1"]["edge_over_rta"] for r in TL]
        s_r = [r["gal"][key]["fret0.1"]["tff_edge_Gyr"] / r["age_Gyr"] for r in TL]
        def cross(arr, lvl=1.0):
            arr = np.array(arr)
            idx = np.where(np.diff(np.sign(arr - lvl)) != 0)[0]
            return [float(np.interp(lvl, [arr[i], arr[i + 1]] if arr[i] < arr[i + 1] else [arr[i + 1], arr[i]],
                                    [ZT[i], ZT[i + 1]] if arr[i] < arr[i + 1] else [ZT[i + 1], ZT[i]])) for i in idx]
        zz = np.array([r["z"] for r in TL]); gR = np.array([r["gal"][key]["g_over_a0_1Re"] for r in TL]); m = zz <= 3
        p = float(np.polyfit(np.log10(1 + zz[m]), np.log10(gR[m]), 1)[0])
        tc[key] = dict(C2_edge_eq_rta_z=cross(e_r), C2_edge_over_rta_z0=e_r[0], C2_edge_over_rta_z6=e_r[-1],
                       C3_tffedge_eq_age_z=cross(s_r), C3_tffedge_over_age_z0=s_r[0], C3_tffedge_over_age_z6=s_r[-1], C4_p=p)
        P(f"  {key:<16} C2 edge/r_ta z0 {e_r[0]:.3f} z6 {e_r[-1]:.3f}, =1 at z {cross(e_r)} | C3 t_ff(edge)/t z0 {s_r[0]:.2f} z6 {s_r[-1]:.2f}, "
          f"=1 at z {cross(s_r)} | C4 g(Re)/a0 propto (1+z)^{p:.2f}")
J["test_c"] = dict(candidates=tc, labels=dict(C1="TAUTOLOGICAL", C2="DESCRIPTIVE", C3="DESCRIPTIVE", C4="DESCRIPTIVE"))

# ------------------------------------------------------------------ TEST (a) RC100
P("\n[TEST a] RC100 dark fraction inside R_e vs z")
rc = {r["idx"]: r for r in csv.DictReader(open(RC100))}
gal = []
for r in csv.DictReader(open(NAT)):
    try:
        z = float(r["z"]); gB = float(r["g_bar_native_B_ms2"]); go = float(r["g_obs_ms2"]); mu = float(r["mu_t18"])
        lm = float(r["logMstar_SED_col6"]); Re = float(r["Re_kpc"]); f1 = float(rc[r["idx"]]["fDM_within_Re"])
    except (ValueError, KeyError):
        continue
    if all(math.isfinite(v) for v in (z, gB, go, mu, lm, Re, f1)):
        gal.append(dict(idx=r["idx"], z=z, gB=gB, go=go, mu=mu, lm=lm, Re=Re, O1=f1, O2=1 - gB / go))
N = len(gal)
z = np.array([g["z"] for g in gal]); gB = np.array([g["gB"] for g in gal]); mu = np.array([g["mu"] for g in gal])
O = dict(O1=np.array([g["O1"] for g in gal]), O2=np.array([g["O2"] for g in gal]))
rec = np.array([gbar_si(10 ** g["lm"] * (1 + g["mu"]), g["Re"], g["Re"]) for g in gal])
check("K2", np.max(np.abs(rec / gB - 1)) < 1e-6,
      f"thin-disc reconstruction of g_bar_native_B, N={N}, max rel dev {np.max(np.abs(rec / gB - 1)):.2e}")
J["K2_max_rel_dev"] = float(np.max(np.abs(rec / gB - 1)))
# POST-FREEZE DIAGNOSTIC (2026-10-09, no verdict weight): K2 as frozen uses the CSV mu_t18 column (4 decimals) and this script's
# kpc = 3.0857e19 m; CFG216 uses 3.0856775814913673e19. Recomputing mu with mu_t18() and using CFG216's kpc isolates the cause.
rec_d = np.array([gbar_si(10 ** g["lm"] * (1 + mu_t18(g["z"], g["lm"])), g["Re"], g["Re"]) for g in gal]) * (KPC / 3.0856775814913673e19)
P(f"  [diag, post-freeze] K2 with mu recomputed by mu_t18() and CFG216's kpc constant: max rel dev {np.max(np.abs(rec_d / gB - 1)):.2e} "
  f"(CSV 7-significant-digit print floor ~5e-7); test (a) reads g_bar_native_B directly, so this does not enter f_pred")
J["K2_diag_postfreeze_max_rel_dev"] = float(np.max(np.abs(rec_d / gB - 1)))
order = np.argsort(z, kind="stable"); bins = np.array_split(order, 4)
zmed = float(np.median(z))
RNG = np.random.default_rng(547); NB = 2000

def fpred(model, foot, zz, gb):
    if model == "NEWTON": return np.zeros_like(gb)
    return 1 - 1 / nu(gb / a0_model(model, zz, foot))

def gscale(dM, dg, tilt=0.0):
    return gB * (10 ** dM + 10 ** (dg + tilt * (z - zmed)) * mu) / (1 + mu)

def ols(x, y):
    return float(np.polyfit(x, y, 1)[0])

models = ["FLAT", "DESI", "RIVAL"] + (["NEWTON"] if MUTATE else [])
boot_idx_bins = [[RNG.choice(b, len(b)) for _ in range(NB)] for b in bins]
boot_idx_all = [RNG.choice(N, N) for _ in range(NB)]
TA = {}
for ft in FOOT:
    for route in ("O1", "O2"):
        y = O[route]
        sO = ols(z, y)
        sO_sig = float(np.std([ols(z[i], y[i]) for i in boot_idx_all]))
        for model in models:
            fp = fpred(model, ft, z, gB)
            rows = []
            for bi, b in enumerate(bins):
                d = float(np.median(y[b]) - np.median(fp[b]))
                sb = float(np.std([np.median(y[i]) - np.median(fp[i]) for i in boot_idx_bins[bi]]))
                meds = [float(np.median(fpred(model, ft, z, gscale(dM, dg))[b])) for dM in (-0.1, 0, 0.1) for dg in (-0.2, 0, 0.2)]
                sys_ = (max(meds) - min(meds)) / 2
                Zb = d / math.sqrt(sb ** 2 + sys_ ** 2) if (sb > 0 or sys_ > 0) else float("inf") * np.sign(d)
                rows.append(dict(bin=bi + 1, z_range=[float(z[b].min()), float(z[b].max())], z_med=float(np.median(z[b])),
                                 med_obs=float(np.median(y[b])), med_pred=float(np.median(fp[b])), diff=d, sig_boot=sb, sys=sys_, Z=Zb))
            sp = ols(z, fp)
            sdiff = float(np.std([ols(z[i], y[i]) - ols(z[i], fp[i]) for i in boot_idx_all]))
            sps = [ols(z, fpred(model, ft, z, gscale(0, 0, t))) for t in (-0.15, 0.15)]
            stilt = abs(sps[1] - sps[0]) / 2
            Zs = (sO - sp) / math.sqrt(sdiff ** 2 + stilt ** 2) if (sdiff > 0 or stilt > 0) else float("inf")
            maxZ = max([abs(r_["Z"]) for r_ in rows] + [abs(Zs)])
            verdict = "TENSION" if maxZ >= 2 else "CONSISTENT"
            TA[f"{ft}|{route}|{model}"] = dict(bins=rows, slope_obs=sO, slope_obs_sig=sO_sig, slope_pred=sp, slope_diff_sig=sdiff,
                                               slope_tilt_sys=stilt, Z_slope=Zs, maxZ=maxZ, verdict=verdict)
            P(f"  {ft:<9} {route} {model:<6} " + " ".join(f"b{r_['bin']}(z{r_['z_med']:.2f}) obs {r_['med_obs']:+.2f} pred {r_['med_pred']:.2f} "
              f"Z {r_['Z']:+.1f} [sb {r_['sig_boot']:.2f} sys {r_['sys']:.2f}]" for r_ in rows)
              + f" | slope obs {sO:+.3f}+-{sO_sig:.3f} pred {sp:+.3f} Z {Zs:+.1f} (tilt {stilt:.3f}) -> {verdict} (max|Z| {maxZ:.1f})")

# decline-follows, diagnosticity, route rule
P("\n  verdicts")
VA = {}
for ft in FOOT:
    res = {}
    for model in models:
        w1 = TA[f"{ft}|O1|{model}"]["verdict"]; w2 = TA[f"{ft}|O2|{model}"]["verdict"]
        res[model] = w1 if w1 == w2 else "ROUTE-DEPENDENT -> NOT DIAGNOSTIC"
    dec = {}
    for route in ("O1", "O2"):
        T = TA[f"{ft}|{route}|FLAT"]
        dec[route] = dict(i_obs_decline=bool(T["slope_obs"] / T["slope_obs_sig"] <= -2), ii_flat_pred_decline=bool(T["slope_pred"] < 0),
                          iii_flat_consistent_O1=bool(TA[f"{ft}|O1|FLAT"]["verdict"] == "CONSISTENT"))
        dec[route]["YES"] = all(dec[route].values())
    pair = {}
    for other in ("RIVAL", "DESI"):
        diag_all = {}
        for route in ("O1", "O2"):
            F = TA[f"{ft}|{route}|FLAT"]["bins"]; Oo = TA[f"{ft}|{route}|{other}"]["bins"]
            diag = [abs(F[i]["med_pred"] - Oo[i]["med_pred"]) > 2 * math.sqrt(F[i]["sig_boot"] ** 2 + F[i]["sys"] ** 2) for i in range(4)]
            seps = [abs(F[i]["med_pred"] - Oo[i]["med_pred"]) for i in range(4)]
            noise = [2 * math.sqrt(F[i]["sig_boot"] ** 2 + F[i]["sys"] ** 2) for i in range(4)]
            fav = None
            if sum(diag) >= 2:
                zF = [abs(F[i]["Z"]) for i in range(4) if diag[i]]; zO = [abs(Oo[i]["Z"]) for i in range(4) if diag[i]]
                if max(zO) >= 3 and max(zF) < 2: fav = "FLAT"
                elif max(zF) >= 3 and max(zO) < 2: fav = other
            diag_all[route] = dict(diagnostic_bins=diag, sep=seps, two_sigma_noise=noise, favoured=fav)
        f1, f2 = diag_all["O1"]["favoured"], diag_all["O2"]["favoured"]
        pv = f"DISCRIMINATING ({f1} favoured)" if (f1 and f1 == f2) else "NOT DIAGNOSTIC"
        pair[f"FLAT_vs_{other}"] = dict(routes=diag_all, verdict=pv)
        P(f"  {ft:<9} FLAT vs {other:<5}: O1 diag bins {diag_all['O1']['diagnostic_bins']} sep {[round(s,3) for s in diag_all['O1']['sep']]} "
          f"2sig {[round(s,3) for s in diag_all['O1']['two_sigma_noise']]}; O2 diag {diag_all['O2']['diagnostic_bins']} -> {pv}")
    VA[ft] = dict(model_verdicts=res, decline_follows=dec, pairs=pair)
    P(f"  {ft:<9} per-model: " + ", ".join(f"{m} {v}" for m, v in res.items()))
    P(f"  {ft:<9} decline follows from compact baryons under fixed a0: O1 {dec['O1']['YES']} {dec['O1']}; O2 {dec['O2']['YES']}")
J["test_a"] = dict(N=N, bins_z=[[float(z[b].min()), float(z[b].max())] for b in bins], table=TA, verdicts=VA)

# ------------------------------------------------------------------ MUTATE
if MUTATE:
    P("\n[MUTATE]")
    M = {}
    for ft in FOOT:
        T = TA[f"{ft}|O1|NEWTON"]
        ok = T["verdict"] == "TENSION" and max(abs(r_["Z"]) for r_ in T["bins"]) >= 3
        M[f"M1_{ft}"] = dict(maxZ_bins=max(abs(r_["Z"]) for r_ in T["bins"]), pass_=bool(ok))
        check(f"M1_{ft}", ok, f"NEWTON on O1 max bin |Z| {M[f'M1_{ft}']['maxZ_bins']:.1f} (need TENSION, >=3)")
    y = O["O1"]; sreal = ols(z, y); sreal_sig = float(np.std([ols(z[i], y[i]) for i in boot_idx_all]))
    rs = np.random.default_rng(547); ss, zs_ = [], []
    for _ in range(200):
        zp = rs.permutation(z); s = ols(zp, y); ss.append(s); zs_.append(s / sreal_sig)
    ss = np.array(ss); zs_ = np.array(zs_)
    sig_real = abs(sreal / sreal_sig) >= 2
    ok2 = bool(np.median(np.abs(ss)) < abs(sreal) / 3 and np.mean(np.abs(zs_) >= 2) <= 0.10)
    M["M2"] = dict(real_slope=sreal, real_sig=sreal_sig, real_significant=bool(sig_real), median_abs_shuffled=float(np.median(np.abs(ss))),
                   frac_shuffled_absZ_ge2=float(np.mean(np.abs(zs_) >= 2)), pass_=ok2)
    check("M2", ok2 if sig_real else True, f"z-shuffle: real O1 slope {sreal:+.3f} ({sreal/sreal_sig:+.1f} sig), median |shuffled| "
          f"{np.median(np.abs(ss)):.3f}, frac |Z|>=2 {np.mean(np.abs(zs_)>=2):.3f}" + ("" if sig_real else " (real slope not significant: reported only)"))
    # M3: FLAT residual pattern on a shuffled set (report)
    zp = np.random.default_rng(548).permutation(z)
    for ft in FOOT:
        fp = fpred("FLAT", ft, zp, gB)
        res3 = [float(np.median(y[b]) - np.median(fp[b])) for b in bins]
        sl = ols(zp, y) - ols(zp, fp)
        M[f"M3_{ft}"] = dict(bin_resid_by_true_z_bins=res3, slope_diff_shuffled=sl)
        P(f"  M3 {ft}: FLAT with shuffled z: bin residuals {[round(v,3) for v in res3]}, slope(obs)-slope(pred) on shuffled z {sl:+.3f}")
    J["mutate"] = M

# ------------------------------------------------------------------ figure (main only)
if not MUTATE:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"; INK2 = "#52514e"
    zf = np.linspace(0, 6, 241); tf = age_gyr(zf)
    fig, ax = plt.subplots(3, 1, figsize=(7.5, 10), sharex=True)
    ax[0].plot(tf, np.full_like(zf, OL * RHOC0), color=S1, lw=2, label="dark energy, Lambda")
    ax[0].fill_between(tf, OL * RHOC0 * np.interp(zf, ZD, R_lo), OL * RHOC0 * np.interp(zf, ZD, R_hi), color=S1, alpha=0.18, lw=0,
                       label="dark energy, DESI DR2 w0wa (4-chain 68% envelope)")
    ax[0].plot(tf, OM * RHOC0 * (1 + zf) ** 3, color=S2, lw=2, label="matter (cold energy + baryons)")
    ax[0].set_yscale("log"); ax[0].set_ylabel("density [kg m$^{-3}$]"); ax[0].legend(fontsize=8, frameon=False)
    for ft, ls in (("canonical", "-"), ("alt", ":")):
        ax[1].plot(tf, np.full_like(zf, FOOT[ft]), color=S1, lw=2, ls=ls, label=f"a0 flat ({ft})")
    ax[1].fill_between(tf, FOOT["canonical"] * np.interp(zf, ZD, A_lo), FOOT["canonical"] * np.interp(zf, ZD, A_hi), color=S1, alpha=0.18, lw=0,
                       label="a0 DESI-tracking (canonical)")
    ax[1].plot(tf, FOOT["canonical"] * E(zf), color=S2, lw=2, label="rival a0 ∝ H(z) (canonical)")
    ax[1].plot(tf, C * H0 * E(zf) / (2 * math.pi), color=INK2, lw=1.5, ls="--", label="c H(z) / 2π")
    ax[1].set_yscale("log"); ax[1].set_ylabel("acceleration [m s$^{-2}$]"); ax[1].legend(fontsize=8, frameon=False)
    for lm, col in ((10.7, S3), (10.0, S4)):
        for k, ls in ((1, "-"), (3, "--")):
            gv = [typical(float(zz), lm, "canonical")[f"g_over_a0_{k}Re"] for zz in zf]
            ax[2].plot(tf, gv, color=col, lw=2, ls=ls, label=f"log M* {lm}, at {k} R_e" if k > 1 else f"log M* {lm}, at R_e")
    ax[2].axhline(1, color=INK2, lw=1); ax[2].set_yscale("log")
    ax[2].set_ylabel("typical g_bar / a0 (flat, canonical)"); ax[2].set_xlabel("cosmic time [Gyr]")
    ax[2].legend(fontsize=8, frameon=False)
    ax[2].text(0.99, 0.02, "sizes and gas fractions PROVISIONAL (van der Wel+14, Tacconi-type)", transform=ax[2].transAxes, ha="right",
               fontsize=7, color=INK2)
    top = ax[0].secondary_xaxis("top", functions=(lambda t: t, lambda t: t))
    zt = [0, 0.5, 1, 2, 3, 6]; top.set_xticks([float(age_gyr(q)) for q in zt]); top.set_xticklabels([str(q) for q in zt]); top.set_xlabel("redshift z")
    for a in ax:
        a.spines[["top", "right"]].set_visible(False); a.grid(alpha=0.2)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "cfg547_timeline.png"), dpi=130)
    P("\n  figure: cfg547_timeline.png")

# ------------------------------------------------------------------ finish
J["checks"] = checks
def conv(o):
    if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [conv(v) for v in o]
    if isinstance(o, (np.floating,)): o = float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, float) and not math.isfinite(o): return str(o)
    return o
json.dump(conv(J), open(os.path.join(HERE, f"cfg547_results{TAG}.json"), "w"), indent=1)
ok = all(checks.values())
P(f"\nchecks: {checks} -> {'ALL PASS' if ok else 'FAILURES'}")
sys.exit(0 if ok else 1)
