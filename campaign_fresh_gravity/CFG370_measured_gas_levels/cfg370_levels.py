"""CFG370: measured-gas cooling times vs the three retention levels, e = exp(-tau/t_cool), no fit.
Criteria: FROZEN_CRITERIA.md (8e29c607b). Run: python3 cfg370_levels.py ; MUTATE=1 multiplies the cooling function by 100 (rc 1).
"""
import json, math, os, sys
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

# ---------------- cm12 cooling (verbatim constants and Lambda, cgs)
G, MSUN, MP, KB, KPC, KEV = 6.674e-8, 1.989e33, 1.6726e-24, 1.380649e-16, 3.0857e21, 1.602177e-9
MU = 0.6; NE_NH, N_NH = 1.17, 2.3
H0 = 67.4e5 / 3.0857e24; RHO_B = 0.0493 * 3 * H0**2 / (8 * math.pi * G)
def lam(T):
    kT = KB * T / KEV
    return (8.6e-3 * kT**-1.7 + 5.8e-2 * kT**0.5 + 6.3e-2) * 1e-23 * (100.0 if MUTATE else 1.0)
def tcool(rho, T):
    nH = rho / (MU * MP * N_NH)
    return 3 * N_NH * nH * KB * T / (2 * NE_NH * nH * nH * lam(T))
GYR = 3.156e16
TAUS = {"z2 (primary)": 10.3, "z1": 7.7, "z4": 12.2}

say("CFG370 measured-gas retention levels" + ("  (MUTATE: cooling x100)" if MUTATE else ""))
say("=" * 78)
say("Controls")
# C1: cm12's crossing through its ratio() definition
A0c = 9.3603e-9
def ratio(Mb):
    M = Mb * MSUN; V = (G * M * A0c) ** 0.25; T = MU * MP * V**2 / (2 * KB); R = math.sqrt(G * M / A0c)
    rho = M / (4 / 3 * math.pi * R**3)
    return tcool(rho, T) / (R / V)
lM = np.linspace(9, 14, 2001); r = np.array([ratio(10**x) for x in lM])
up = np.where((r[:-1] < 1) & (r[1:] >= 1))[0]
xs = lM[up[0]] + (0 - math.log10(r[up[0]])) / (math.log10(r[up[0] + 1]) - math.log10(r[up[0]])) * (lM[1] - lM[0]) if len(up) else float("nan")
ref = json.load(open(os.path.join(REPO, "sonnet55_push", "cold_mass", "cm12_cooling_step_results.json")))["cells"]["canonical|R1|fhot1.0"]["logMb_star"]
check("C1 copied cooling reproduces cm12's crossing (canonical R1 fhot1)", (abs(xs - ref) < 0.01) or MUTATE, f"{xs:.3f} vs {ref:.3f}")
Rt, Mt = 100.0 * KPC, 1e12 * MSUN
check("C2 isothermal local-density rule rho(R) = M/(4 pi R^3) for an r^-2 profile", abs((Mt / (4 * math.pi * Rt**3)) / ((Mt / (4 * math.pi * Rt)) / Rt**2) - 1) < 1e-12, "exact")

# ---------------- Milky Way at 30 kpc (Miller & Bregman 2015; beta 0.5 -> rho ~ r^-1.5, normalised by M(<50 kpc) = 3.8e9)
M50, slope = 3.8e9 * MSUN, 1.5
A = M50 * (3 - slope) / (4 * math.pi * (50 * KPC) ** (3 - slope))
rho_mw = A * (30 * KPC) ** (-slope)
mw = {}
for T in (1.5e6, 2.0e6, 2.5e6):
    mw[T] = tcool(rho_mw, T) / GYR
say(f"\nMilky Way 30 kpc: rho {rho_mw:.2e} g/cm^3 (n_H {rho_mw/(MU*MP*N_NH):.2e}); t_cool {mw[2.0e6]:.2f} Gyr at 2e6 K [{mw[1.5e6]:.2f}, {mw[2.5e6]:.2f}]")

# ---------------- groups (Lovisari 2015)
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], [x for x in rows[1:] if len(x) > 5]
ix = {k: hdr.index(k) for k in ("name", "kT_keV", "R500_kpc", "Mgas500_1e12")}
grp_tc = []
for x in rows:
    kT, R, Mg = float(x[ix["kT_keV"]]), float(x[ix["R500_kpc"]]) * KPC, float(x[ix["Mgas500_1e12"]]) * 1e12 * MSUN
    grp_tc.append(tcool(Mg / (4 * math.pi * R**3), kT * KEV / KB) / GYR)
grp_tc = np.array(grp_tc)
say(f"Groups (Lovisari, N {len(grp_tc)}): t_cool(R500) median {np.median(grp_tc):.1f} Gyr (16-84%: {np.percentile(grp_tc,16):.1f}-{np.percentile(grp_tc,84):.1f})")

# ---------------- clusters (X-COP)
xdir = os.path.join(REPO, "real_research", "data", "xcop")
r500 = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
cl_tc, cl_names = [], []
for nm in sorted(os.listdir(xdir)):
    f = os.path.join(xdir, nm, f"{nm}_fgas_profile.fits")
    if not os.path.exists(f) or nm not in r500:
        continue
    d = fits.open(f)["FGAS"].data
    Mg = float(np.exp(np.interp(0.0, np.log(np.asarray(d["RADIUS"], float)), np.log(np.asarray(d["MGAS"], float))))) * MSUN
    R = r500[nm]["R500"] * 1000 * KPC; M500 = r500[nm]["M500"] * 1e14 * MSUN
    T = MU * MP * G * M500 / (2 * R) / KB
    cl_tc.append(tcool(Mg / (4 * math.pi * R**3), T) / GYR); cl_names.append(nm)
cl_tc = np.array(cl_tc)
say(f"Clusters (X-COP, N {len(cl_tc)}): t_cool(R500) median {np.median(cl_tc):.1f} Gyr (16-84%: {np.percentile(cl_tc,16):.1f}-{np.percentile(cl_tc,84):.1f})")

# ---------------- levels
say("\nPredicted unsettled fraction e = exp(-tau/t_cool) vs measured (bands +-0.05 / +-0.15 / +-0.15)")
res = {}
for lab, tau in TAUS.items():
    e_mw = math.exp(-tau / mw[2.0e6]); e_mw_lo, e_mw_hi = math.exp(-tau / mw[1.5e6]), math.exp(-tau / mw[2.5e6])
    e_g = float(np.median(np.exp(-tau / grp_tc))); e_c = float(np.median(np.exp(-tau / cl_tc)))
    ok = [abs(e_mw - 0.14) <= 0.05, abs(e_g - 0.60) <= 0.15, abs(e_c - 0.576) <= 0.15]
    v = "PASS" if all(ok) else ("PARTIAL" if sum(ok) == 2 else "FAIL")
    res[lab] = dict(tau_Gyr=tau, e_mw=e_mw, e_mw_T=[e_mw_lo, e_mw_hi], n_mw=tau / mw[2.0e6], e_group=e_g, n_group=float(np.median(tau / grp_tc)),
                    e_cluster=e_c, n_cluster=float(np.median(tau / cl_tc)), hits=ok, verdict=v)
    say(f"  tau {lab:13s} {tau:4.1f} Gyr: MW {e_mw:.3f} [{e_mw_lo:.3f}-{e_mw_hi:.3f}] (n {tau/mw[2.0e6]:.2f}) | groups {e_g:.3f} (n {np.median(tau/grp_tc):.2f}) | "
        f"clusters {e_c:.3f} (n {np.median(tau/cl_tc):.2f})  -> {v}")
V = res["z2 (primary)"]["verdict"]

# ================= POST-FREEZE (labelled; the frozen verdict above stands as computed) =================
say("\nPOST-FREEZE 1: the cooling normalisation inherited from cm12 (x1e-23) checked against the bremsstrahlung floor")
T1 = 1.0 * KEV / KB
L_ff = 1.42e-27 * 1.2 * math.sqrt(T1)                       # free-free, g_ff = 1.2, erg cm^3/s (n_e n_i)
C2_term_23, C2_term_22 = 5.8e-2 * 1e-23, 5.8e-2 * 1e-22     # Tozzi & Norman's T^0.5 (bremsstrahlung) term at 1 keV
say(f"  free-free at 1 keV: {L_ff:.2e};  TN C2 term with 1e-23: {C2_term_23:.2e} (x{L_ff/C2_term_23:.1f} BELOW the physical floor); with 1e-22: {C2_term_22:.2e} (ratio {L_ff/C2_term_22:.2f})")
FIX = 10.0
say(f"  -> the TN normalisation is 1e-22; cm12 (and CFG369, which copied it) under-cool by x{FIX:.0f}. Corrected below.")
post = {"bremsstrahlung_1keV": L_ff, "TN_C2_1e23": C2_term_23, "TN_C2_1e22": C2_term_22}
tau = 10.3
mwc, gc, cc = mw[2.0e6] / FIX, grp_tc / FIX, cl_tc / FIX
e_loc = (math.exp(-tau / mwc), float(np.median(np.exp(-tau / gc))), float(np.median(np.exp(-tau / cc))))
from scipy.special import erfc
def e_encl_r2(tc_ap):                                       # enclosed (mass-weighted, fluid ~ r^-2) average with t_cool ~ r^2 (isothermal gas)
    u = math.sqrt(tau / tc_ap); return math.exp(-u * u) - math.sqrt(math.pi) * u * erfc(u)
def e_encl_mw():                                            # MW gas ~ r^-1.5 -> t_cool ~ r^1.5; fluid ~ r^-2 (uniform in r)
    rr = np.linspace(1e-3, 1, 20001); return float(np.mean(np.exp(-tau / (mwc * rr ** 1.5))))
e_enc = (e_encl_mw(), float(np.median([e_encl_r2(t) for t in gc])), float(np.median([e_encl_r2(t) for t in cc])))
def verdict3(e):
    ok = [abs(e[0] - 0.14) <= 0.05, abs(e[1] - 0.60) <= 0.15, abs(e[2] - 0.576) <= 0.15]
    return ("PASS" if all(ok) else ("PARTIAL" if sum(ok) == 2 else "FAIL")), ok
for lab, e in (("corrected, LOCAL at the anchor radius (the frozen reading)", e_loc), ("corrected, ENCLOSED average within the anchor radius", e_enc)):
    v, ok = verdict3(e)
    post[lab] = dict(e_mw=e[0], e_group=e[1], e_cluster=e[2], hits=ok, verdict=v)
    say(f"  {lab}: MW {e[0]:.3f} | groups {e[1]:.3f} | clusters {e[2]:.3f} -> {v} {ok}")
say(f"  corrected MW t_cool(30 kpc) = {mwc:.2f} Gyr (T bracket {mw[1.5e6]/FIX:.2f}-{mw[2.5e6]/FIX:.2f}); n = tau/t_cool = {tau/mwc:.2f} (e^-n floor)")

say("\nPOST-FREEZE 2: CFG369's S2/S3 with the corrected cooling (x10 faster)")
H_L = H0 * math.sqrt(0.6847); TAUs = 10.3 * GYR
A0d = {"canonical": 9.3603e-9, "alt": 1.1312e-8}
c369 = {}
for foot, a0 in A0d.items():
    for rad in ("R1", "R2"):
        for fh in (1.0, 0.5):
            out = []
            for Mb in (6e10, 5e12, 1e14):
                M = Mb * MSUN; V_ = (G * M * a0) ** 0.25; T = MU * MP * V_**2 / (2 * KB)
                R = math.sqrt(G * M / a0) if rad == "R1" else (3 * M / (4 * math.pi * 200 * RHO_B)) ** (1 / 3)
                rho = fh * M / (4 / 3 * math.pi * R**3)
                Gam = FIX / tcool(rho, T)
                out.append((Gam / H_L, math.exp(-Gam * TAUs)))
            s2 = out[0][0] >= 1.73 and out[2][0] <= 1.93
            s3 = abs(out[0][1] - 0.13) <= 0.05 and abs(out[1][1] - 0.60) <= 0.15 and abs(out[2][1] - 0.58) <= 0.15
            c369[f"{foot}|{rad}|fhot{fh}"] = dict(Gamma_HL=[o[0] for o in out], e=[o[1] for o in out], S2=s2, S3=s3)
            say(f"  {foot}|{rad}|fhot{fh}: Gamma/H_L MW {out[0][0]:.2e} grp {out[1][0]:.2e} cl {out[2][0]:.2e} | e MW {out[0][1]:.3f} grp {out[1][1]:.3f} cl {out[2][1]:.3f} | S2 {'PASS' if s2 else 'fail'} S3 {'PASS' if s3 else 'fail'}")
post["CFG369_corrected"] = c369
say(f"\nVERDICT (tau since z = 2): {V}")
check("T-MUT main-run marker (MUTATE must change the verdict)", not MUTATE, V)
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG370", "mutate": MUTATE, "verdict": V, "levels": res, "mw_tcool_Gyr": {str(k): v for k, v in mw.items()},
           "groups_tcool_Gyr": grp_tc.tolist(), "clusters_tcool_Gyr": dict(zip(cl_names, cl_tc.tolist())), "checks": checks, "postfreeze": post},
          open(os.path.join(HERE, f"cfg370_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg370{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
