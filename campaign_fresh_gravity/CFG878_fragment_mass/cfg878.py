"""CFG878 -- derive the cold-energy fragment (clump) mass.  Criteria: FROZEN_CRITERIA.md (f39ef2490).
A: full-law isothermal mass vs sigma.  B: the record's own bath (self Jeans dispersion) per dwarf.  C: universal velocity scales.
Run: python3 cfg878.py  (CFG878_MUTATE=1: constant bath).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG878_MUTATE") == "1"; SUF = "_MUTATE" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC, kB, mH = 6.674e-11, 1.989e30, 3.0857e16, 1.380649e-23, 1.6735e-27
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; F_MID = 0.85
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-30))))
deepM = lambda s_kms, a0: 81 * (s_kms * 1e3) ** 4 / (4 * G * a0) / Msun
RES = dict(lane="CFG878", mutate=MUT)

# ---------------- Part A: isothermal sphere under the full law
def sphere(sig, rho0, a0, rmax_pc=3e5):
    s2 = (sig * 1e3) ** 2; rho = rho0 * Msun / PC ** 3; lnr, dl = math.log(1e-3 * PC), 1e-3; r = math.exp(lnr)
    M = 4 / 3 * math.pi * r ** 3 * rho; last = (r, M)
    def d(lr, rho_, M_):
        rr = math.exp(lr); gN = G * M_ / rr ** 2; g = gN * float(nu_e(gN / a0)); return (-rho_ * g * rr / s2, 4 * math.pi * rr ** 3 * rho_)
    while r < rmax_pc * PC and rho > 1e-14 * rho0 * Msun / PC ** 3:
        k1 = d(lnr, rho, M); k2 = d(lnr + dl / 2, rho + dl / 2 * k1[0], M + dl / 2 * k1[1])
        last = (r, M); rho += dl * k2[0]; M += dl * k2[1]; lnr += dl; r = math.exp(lnr)
    slope = math.log(M / last[1]) / math.log(r / last[0])
    return M / Msun, slope
P("CFG878  cold-energy fragment mass" + ("  [MUTATE: constant bath 7.5 km/s]" if MUT else ""))
P("\n== Part A: self-gravitating isothermal clump under the full law (nu_e): M_total / [81 sigma^4/(4 G a0)]")
RES["A"] = {}
for foot, a0 in A0.items():
    for sig in (7.36, 7.53, 8.23):
        row = {}
        for rho0 in (0.01, 0.1, 0.6, 3.0):
            Mt, _ = sphere(sig, rho0, a0); row[rho0] = Mt / deepM(sig, a0)
        RES["A"][f"{foot}|{sig}"] = row
        P(f"  [{foot}] sigma {sig:4.2f} km/s  deep M {deepM(sig, a0):.3e}  f(rho0=0.01/0.1/0.6/3) = " + " / ".join(f"{v:.3f}" for v in row.values()))
ka1 = all(abs(RES["A"][k][0.01] - 1) < 0.06 for k in RES["A"]); Mn, sl = sphere(7.53, 0.1, 1e-20, rmax_pc=1e5)
ka2 = abs(sl - 1) < 0.05
P(f"  K-A1 deep limit (rho0 0.01 within 6% of 1): {'PASS' if ka1 else 'FAIL'};  K-A2 Newtonian run: dlnM/dlnr at edge {sl:.3f} -> {'PASS' if ka2 else 'FAIL'}")
fr = [v for r in RES["A"].values() for v in r.values()]; P(f"  => fragment mass is set by sigma alone: f = {min(fr):.2f}-{max(fr):.2f} over a 300x range of central density")
RES["K_A"] = dict(A1=ka1, A2=ka2, newton_slope=sl)

# ---------------- Part B: the record's own bath
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return None
R872 = json.load(open(os.path.join(LANES, "CFG872_clump_mass_scaling", "cfg872_results.json")))
def bath_sigma(Mb, rh_pc, a0, at=4 / 3):
    a = rh_pc * PC; r = np.geomspace(1e-3 * a, 300 * a, 20000)
    Mb_r = Mb * Msun * r ** 3 / (r ** 2 + a ** 2) ** 1.5; gN = G * Mb_r / r ** 2; g = gN * nu_e(gN / a0)
    Mdyn = g * r ** 2 / G; rho_tot = np.gradient(Mdyn, r) / (4 * np.pi * r ** 2)
    rho_b = 3 * Mb * Msun / (4 * np.pi * a ** 3) * (1 + r ** 2 / a ** 2) ** -2.5; rho_c = np.maximum(rho_tot - rho_b, 0)
    integ = rho_c * g; cum = np.concatenate([np.cumsum(((integ[1:] + integ[:-1]) / 2 * np.diff(r))[::-1])[::-1], [0.0]])
    i = np.searchsorted(r, at * a); return math.sqrt(cum[i] / rho_c[i]) / 1e3, float(np.mean(rho_c[:100] >= 0))
P("\n== Part B: fragments relaxed to the record's own bath (sigma_J of the settled cold energy, CFG544/554)")
s_tst, _ = bath_sigma(1e5, 1000.0, A0["canonical"]); ratio = F_MID * deepM(s_tst, A0["canonical"]) / 1e5
kb1 = abs(ratio / (81 / 16 * F_MID) - 1) < 0.10
P(f"  K-B1 deep test system (M_b 1e5, r_h 1 kpc): sigma_J(r12) {s_tst:.3f} km/s, M_frag/M_b = {ratio:.2f} vs (81/16) f = {81/16*F_MID:.2f} -> {'PASS' if kb1 else 'FAIL'}")
RES["K_B1"] = dict(ratio=ratio, pass_=kb1); RES["B"] = {}
for foot, a0 in A0.items():
    rows = R872[foot]["rows"]; x, y, tab = [], [], []
    for rw in rows:
        nm = rw["name"]; L = LVD[nm]; rh = fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical")); Mb = 10 ** rw["lMs"]
        sj = 7.5 if MUT else bath_sigma(Mb, rh, a0)[0]; Mf = F_MID * deepM(sj, a0)
        x.append(rw["lMs"]); y.append(math.log10(Mf)); tab.append((nm, Mb, rh, sj, Mf, 10 ** rw["lM"]))
    x, y = np.array(x), np.array(y); s_rec, c = np.polyfit(x, y, 1)
    sm, se = R872[foot]["slope"], R872[foot]["slope_err"]; z = abs(s_rec - sm) / se
    cls = "RECORD BATH EXCLUDED" if z >= 3 else ("TENSION" if z >= 2 else "CONSISTENT")
    med = float(np.median([t[4] for t in tab]))
    RES["B"][foot] = dict(s_rec=float(s_rec), s_meas=sm, se_meas=se, z=z, cls=cls, median_Mfrag=med, median_Mcl_meas=R872[foot]["median_Mcl"],
                          rows=[dict(name=t[0], Mb=t[1], rh=t[2], sigma_J=t[3], Mfrag=t[4], Mcl_meas=t[5]) for t in tab])
    P(f"  [{foot}] N {len(tab)}: record-bath slope s_rec = {s_rec:+.3f} vs measured {sm:+.3f} +- {se:.3f}  ({z:.1f} se)  -> {cls}")
    P(f"      median M_frag {med:.2e} vs measured median clump {R872[foot]['median_Mcl']:.2e} Msun")
    for t in sorted(tab, key=lambda q: q[1])[::3]:
        P(f"      {t[0]:16s} M* {t[1]:.1e}  sigma_J {t[3]:5.2f}  M_frag {t[4]:.1e}  (measured clump {t[5]:.1e})")
for nm in ("Fornax", "Leo I"):
    L = LVD[nm]; rh = fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical")); Mb = 2.0 * 10 ** (0.4 * (4.83 - fnum(L["M_V"])))
    sj = bath_sigma(Mb, rh, A0["canonical"])[0]; P(f"  CFG853 check [{nm}] (Ups 2): sigma_J {sj:.2f} km/s -> M_frag {F_MID*deepM(sj, A0['canonical']):.2e} Msun (vs the ~5e6 clump)")

# ---------------- Part C: universal velocity scales from outside the cold sector
P("\n== Part C: universal velocity scales (fixed physics), M_frag = f * 81 sigma^4/(4 G a0), f 0.76-0.95  [POST-HOC comparison]")
th = lambda T, mu: math.sqrt(kB * T / (mu * mH)) / 1e3
cands = {"(i) neutral primordial gas, H-cooling floor 8000 K - 1e4 K (mu 1.22)": (th(8000, 1.22), th(1e4, 1.22)),
         "(ii) ionized gas 8000 K - 1e4 K (mu 0.59)": (th(8000, 0.59), th(1e4, 0.59)),
         "(iii) sigma^2 = a0 L*, L* >= 24 pc (canonical / alt)": (math.sqrt(A0["canonical"] * 24 * PC) / 1e3, math.sqrt(A0["alt"] * 24 * PC) / 1e3)}
RES["C"] = {}
for k, (lo, hi) in cands.items():
    Mlo, Mhi = 0.76 * deepM(lo, A0["canonical"]), 0.95 * deepM(hi, A0["canonical"])
    RES["C"][k] = dict(sigma=[lo, hi], M_canonical=[Mlo, Mhi]); P(f"  {k}: sigma {lo:.2f}-{hi:.2f} km/s -> M_frag {Mlo:.1e}-{Mhi:.1e} Msun (canonical)")
s77 = {f: json.load(open(os.path.join(LANES, "CFG877_finite_cold_clump", "cfg877_results.json")))[f]["sigma"] for f in A0}
lo, hi = cands["(i) neutral primordial gas, H-cooling floor 8000 K - 1e4 K (mu 1.22)"]
hg = all(lo <= s <= hi for s in s77.values())
P(f"  measured clump sigma: CFG877 {s77['canonical']:.2f} / {s77['alt']:.2f} km/s; CFG872 per-dwarf median {R872['canonical']['median_sigma']:.2f} / {R872['alt']['median_sigma']:.2f}")
P(f"  H-GASBATH label (CFG877 sigma inside candidate (i)): {'CONSISTENT (post-hoc)' if hg else 'NOT CONSISTENT'}; (ii) ionized is x{(th(1e4,0.59)/7.53)**4:.1f} too heavy; (iii) is CFG858's coincidence")
RES["H_GASBATH"] = hg
cb, ca = RES["B"]["canonical"]["cls"], RES["B"]["alt"]["cls"]
P(f"\n  PART B CLASS: canonical {cb}; alt {ca}")
if MUT: ok = abs(RES["B"]["canonical"]["s_rec"]) < 0.1; RES["mutate_ok"] = ok; P(f"  MUTATE (constant bath): s_rec {RES['B']['canonical']['s_rec']:+.3f} -> {'responds' if ok else 'FAILED'}")
json.dump(RES, open(os.path.join(HERE, f"cfg878_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg878{SUF}.out"), "w").write("\n".join(OUT) + "\n")

# ---------------- POST-HOC diagnostic (added after the first run; K-B1 as frozen evaluated the deep-limit formula at r12, where the
# settled cold energy is not yet rho ~ r^-2; the analytic limit sigma_J^2 = V_flat^2/2 holds only at r >> r_h)
if not MUT:
    P("\n== POST-HOC diagnostic for K-B1 (disclosed): sigma_J of the deep test system vs radius")
    Vf = (G * 1e5 * Msun * A0["canonical"]) ** 0.25 / 1e3; diag = {}
    for at in (4 / 3, 5, 20, 50):
        sj, _ = bath_sigma(1e5, 1000.0, A0["canonical"], at=at); diag[at] = sj
        P(f"   r = {at:5.2f} r_h: sigma_J {sj:.3f} km/s  (V_flat/sqrt2 = {Vf/math.sqrt(2):.3f})  M_frag/M_b = {F_MID*deepM(sj, A0['canonical'])/1e5:.2f}")
    RES["K_B1_posthoc"] = dict(sigmaJ=diag, Vflat_over_sqrt2=Vf / math.sqrt(2))
    json.dump(RES, open(os.path.join(HERE, f"cfg878_results{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg878{SUF}.out"), "w").write("\n".join(OUT) + "\n")
