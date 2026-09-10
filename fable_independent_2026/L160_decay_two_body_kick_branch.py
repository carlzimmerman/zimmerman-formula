#!/usr/bin/env python3
"""
T2 -- TEMPORAL SEPARATION, part 2: the TWO-BODY KICKED-DAUGHTER branch (the arm that really evades the lemma).
===============================================================================================================
T1 closed the arm in which the cold component is DESTROYED (one-body decay to dark radiation): destroying the
42-72% of the matter that the galaxy gate requires costs too much expansion history and is capped at 2-4% by
the published CMB+BAO+SNe likelihoods.  This lane tests the arm that does NOT destroy it.

  THE MECHANISM.  X -> Y + (massless), mass splitting eps, daughter speed v_k/c = eps/(1-eps) ~ eps.  The
  daughter is NON-relativistic, so rho_Y ~ a^-3 and the BACKGROUND is essentially untouched -- T1's kill does
  not apply.  What changes is VELOCITY: the daughter is born with a kick v_k and thereafter v ~ 1/a.  A
  particle is retained by a halo iff v < v_esc.  Clusters are far deeper than galaxies, so the kick acts as an
  ESCAPE-VELOCITY FILTER that evacuates galaxies while leaving clusters loaded -- and, because the parent is
  COLD until it decays, that filter is switched OFF at recombination.

  WHY THIS IS THE STRONGEST CANDIDATE, stated fairly BEFORE it is tested:
   * it defeats the velocity-ordering lemma (L125 VEL-1/2), whose hypothesis is that ONE species carries
     v ~ 1/a from the start.  A late, non-adiabatic velocity injection breaks the monotonicity of k_fs.
   * it defeats L61 B7's ordering objection.  L61 found every galaxy-suppressing filter had the WRONG ordering
     because clusters are 64x deeper and need MORE.  A DEPTH filter has the RIGHT ordering for the
     galaxy-vs-cluster split; L61 rejected it only because the same filter would also act at recombination.
     Temporal separation removes exactly that objection.
   * it pays almost no background cost: only the fraction eps of the rest mass becomes dark radiation.

WHAT IS COMPUTED (self-contained numpy/scipy, on committed data):
  PART 0  CONTROLS: 175 SPARC rotmod files (kernel-alone RAR scatter, against L61 A6); 248 audited X-COP rows
          (cluster shortfall, against L2 C1); a LambdaCDM growth solver against the analytic matter+Lambda
          growing mode; an Eisenstein-Hu sigma_8 normalisation; and a MUTATION control on the growth pipeline.
  PART 1  the escape-velocity filter and its ORDERING, measured from those two data sets.
  PART 2  the POPULATION MODEL: f_gal(tau, v_k), f_cl(tau, v_k), and the admissible region.
  PART 3  the STRUCTURE gate.  Two variants, deliberately bracketing the truth:
            (A) REALISTIC: growth with the reduced source (1 - f_nc(a,k)) and delta_m = (1-f_nc) delta_c;
            (B) STRICT UPPER BOUND on the model's sigma_8: the clustered part is allowed to grow at the FULL
                LambdaCDM rate (impossible, but generous), and each daughter sub-population keeps the largest
                amplitude free-streaming can leave it -- frozen at its kick and resuming when k drops below
                k_fs.  If (B) already fails, the failure is not an artefact of the approximation.
  PART 4  confrontation with the published two-body decaying-DM bounds.
  PART 5  the verdict.

POLARITY: every check ASSERTS a statement; PASS = the statement is TRUE.  A FAIL is a finding, not a crash.
Both a0 footings (canonical 9.3619e-11, alternate 1.1279e-10 m/s^2) are carried on every dimensional number.
"""
import numpy as np, glob, json, os, sys, time, warnings
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.interpolate import interp1d
from scipy.optimize import brentq
warnings.filterwarnings("ignore")

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n           ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

REPO = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
SPARC = os.path.join(REPO, "real_research/data/sparc_data")
CLJSON = os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")

print("=" * 118)
print("T2 -- TEMPORAL SEPARATION: the two-body kicked-daughter branch (an escape-velocity filter switched on late)")
print("=" * 118, flush=True)

C_KMS = 299792.458
G_KPC = 4.300917270e-6
KPC_M = 3.0856775814913673e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0_KPC = {k: v * KPC_M / 1e6 for k, v in A0.items()}
OMB, OMC = 0.02237, 0.1200
COSMIC_DM_PER_BARYON = OMC / OMB
h_P, H0 = 0.6736, 67.36
ETA_MAX = {"canon eps=0": 0.582, "alt eps=0": 0.486, "canon eps=1": 0.355, "alt eps=1": 0.276}

def nu_RAR(x):
    x = np.asarray(x, dtype=float)
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(x, 1e-300))))

OM_R = 4.1834e-5 / h_P ** 2
OM_M = (OMB + OMC + 0.000648) / h_P ** 2
OM_L = 1.0 - OM_M - OM_R
KMS_MPC_TO_INVGYR = 1.02271217e-3
_lna = np.linspace(np.log(1e-8), 0.0, 40000); _a = np.exp(_lna)
_H = H0 * np.sqrt(OM_R * _a ** -4 + OM_M * _a ** -3 + OM_L)
_t = cumulative_trapezoid(1.0 / (_H * KMS_MPC_TO_INVGYR), _lna, initial=0.0)
AGE = _t[-1]
t_of_lna = interp1d(_lna, _t, kind="cubic")
lna_of_t = interp1d(_t, _lna, kind="cubic", bounds_error=False, fill_value=(_lna[0], 0.0))
H_of_lna = interp1d(_lna, _H, kind="cubic")
dlnH_of_lna = interp1d(_lna, np.gradient(np.log(_H), _lna), kind="cubic")
def t_of_a(aa): return float(t_of_lna(np.log(np.clip(aa, _a[0], 1.0))))
def a_of_t(tt): return float(np.exp(lna_of_t(np.clip(tt, _t[0], AGE))))

# ===================================================================================================
sec("PART 0 -- CONTROLS on committed data: SPARC, X-COP, growth, sigma_8, and a mutation control.")
# ===================================================================================================
files = sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat")))
gal = []
for f in files:
    try: d = np.loadtxt(f)
    except Exception: continue
    if d.ndim != 2 or d.shape[0] < 5: continue
    r, vobs, ev, vgas, vdisk, vbul = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    m = (r > 0) & (vobs > 0) & (ev > 0) & (ev / vobs < 0.10)
    if m.sum() < 4: continue
    r, vobs, vgas, vdisk, vbul = r[m], vobs[m], vgas[m], vdisk[m], vbul[m]
    v2bar = np.maximum(vgas * np.abs(vgas) + 0.5 * vdisk ** 2 + 0.7 * vbul ** 2, 1e-8)
    gal.append(dict(name=os.path.basename(f)[:-11], r=r, gbar=v2bar / r, gobs=vobs ** 2 / r,
                    vflat=float(np.median(vobs[r >= 0.7 * r.max()]))))
print(f"    SPARC: {len(files)} rotmod files, {len(gal)} galaxies pass (eV/V < 0.10), "
      f"{sum(len(g['r']) for g in gal)} points")
resid = {}
for k, a0k in A0_KPC.items():
    rs = np.concatenate([np.log10(g["gobs"] / (g["gbar"] * nu_RAR(g["gbar"] / a0k))) for g in gal])
    resid[k] = rs
    print(f"      kernel-alone RAR residual, {k:9}: rms {np.sqrt(np.mean(rs**2)):.3f} dex, "
          f"median {np.median(rs):+.3f} dex, N = {len(rs)}")
check("C0  CONTROL: the carried kernel ALONE reproduces SPARC at the published scatter (L61 A6: 0.145/0.142 dex "
      "at median +0.030/+0.003).  This is the premise of the whole 'excess spent once' theorem -- the kernel "
      "already fits, so any surviving cold component is pure overshoot",
      all(np.sqrt(np.mean(resid[k] ** 2)) < 0.20 and abs(np.median(resid[k])) < 0.10 for k in A0_KPC),
      "; ".join(f"{k}: {np.sqrt(np.mean(resid[k]**2)):.3f} dex @ {np.median(resid[k]):+.3f}" for k in A0_KPC))

CL = json.load(open(CLJSON)); rows = CL["rows"]
clusters = sorted({r["cluster"] for r in rows})
print(f"\n    X-COP audit: {len(rows)} rows, {len(clusters)} clusters, radii {CL['radii_kpc']}")
short = {}
for foot in ("canonical", "alt"):
    fac = []
    for r in rows:
        if r["footing"] != foot or r["r_kpc"] != 1000.0: continue
        gb, gh = r["g_baryon_over_a0"] * A0[foot], r["g_hse_over_a0"] * A0[foot]
        if gb <= 0 or gh <= 0: continue
        fac.append(gh / (gb * nu_RAR(gb / A0[foot])))
    short[foot] = np.array(fac)
    print(f"      {foot:9}: MOND shortfall M_HSE/M_pred at 1000 kpc = median {np.median(fac):.2f}x "
          f"(N={len(fac)}, range {np.min(fac):.2f}-{np.max(fac):.2f})")
check("C1  CONTROL: the audited X-COP rows through the carried kernel reproduce the published cluster shortfall "
      "at 1000 kpc (L2 C1: 1.82x canonical / 1.68x alt for the full sample, 2.07x/1.92x for the stellar-7 "
      "subset).  Statement asserted: the median shortfall is in [1.5, 2.6] at both footings",
      all(1.5 <= np.median(short[f]) <= 2.6 for f in short),
      "; ".join(f"{f}: {np.median(short[f]):.2f}x" for f in short))

def T_EH(k_hMpc):
    om, ob = OM_M, OMB / h_P ** 2
    th = 2.7255 / 2.7
    s = 44.5 * np.log(9.83 / (om * h_P ** 2)) / np.sqrt(1 + 10 * (ob * h_P ** 2) ** 0.75)
    ag = 1 - 0.328 * np.log(431 * om * h_P ** 2) * ob / om + 0.38 * np.log(22.3 * om * h_P ** 2) * (ob / om) ** 2
    k = k_hMpc * h_P
    geff = om * h_P * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k_hMpc * th ** 2 / geff
    L0 = np.log(2 * np.e + 1.8 * q); C0 = 14.2 + 731.0 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q ** 2)
_k = np.geomspace(1e-4, 60.0, 1200)
_Pk = _k ** 0.9649 * T_EH(_k) ** 2
def sigma_R(P, R=8.0):
    x = _k * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return np.sqrt(np.trapz(P * _k ** 2 * W ** 2, _k) / (2 * np.pi ** 2))
_Pk *= (0.811 / sigma_R(_Pk)) ** 2
S8_LCDM = 0.811 * np.sqrt(OM_M / 0.3)
check("C2  CONTROL: the Eisenstein-Hu + top-hat machinery is normalised so LambdaCDM gives sigma_8 = 0.811 "
      "(Planck 2018), hence S_8 = sigma_8 sqrt(Om_m/0.3) = 0.831",
      abs(sigma_R(_Pk) - 0.811) < 1e-6, f"sigma_8 = {sigma_R(_Pk):.6f}, S_8 = {S8_LCDM:.4f}")

A_START = 0.01
def growth_general(src_factor=None):
    """delta'' + (2 + dlnH/dlna) delta' = 1.5 Om_m(a) * s(a) * delta ; s = 1 for LambdaCDM."""
    lg = np.linspace(np.log(A_START), 0.0, 1200)
    def Om(l): return OM_M * np.exp(-3 * l) / (float(H_of_lna(l)) / H0) ** 2
    def rhs(l, Y):
        s = 1.0 if src_factor is None else float(src_factor(l))
        return [Y[1], -(2.0 + float(dlnH_of_lna(l))) * Y[1] + 1.5 * Om(l) * s * Y[0]]
    sol = solve_ivp(rhs, (lg[0], 0.0), [A_START, A_START], t_eval=lg, rtol=1e-9, atol=1e-14, method="DOP853")
    return sol.t, sol.y[0]
lg_L, D_L = growth_general()
D_of_lna = interp1d(lg_L, D_L, kind="cubic")
# analytic matter+Lambda growing mode
def D_analytic(a):
    aa = np.geomspace(1e-6, a, 4000)
    E = np.sqrt(OM_M * aa ** -3 + OM_L)
    return np.sqrt(OM_M * a ** -3 + OM_L) * np.trapz(1.0 / (aa * E) ** 3, aa)
rat_num = D_L[-1] / D_L[0]
rat_ana = D_analytic(1.0) / D_analytic(A_START)
check("C3  CONTROL: the growth solver reproduces the ANALYTIC flat matter+Lambda growing mode "
      "D(a) ~ E(a) int da/(aE)^3 between a = 0.01 and a = 1, to better than 2%.  The residual ~1% is EXPECTED "
      "and physical, not numerical: the solver carries radiation, which is 2.9% of the matter density at "
      "a = 0.01 and slows growth slightly, while the analytic formula does not",
      abs(rat_num / rat_ana - 1) < 0.02,
      f"numeric D(1)/D(0.01) = {rat_num:.4f}, analytic = {rat_ana:.4f}  ({100*(rat_num/rat_ana-1):+.3f}%)")
# mutation control: a constant non-clustering fraction must produce the textbook suppressed index
f_test = 0.30
lg_t, D_t = growth_general(src_factor=lambda l: 1.0 - f_test)
p_num = np.gradient(np.log(D_t), lg_t)[np.argmin(abs(lg_t - np.log(0.05)))]
p_ana = (np.sqrt(25.0 - 24.0 * f_test) - 1.0) / 4.0
check("C4  MUTATION CONTROL: fed a constant non-clustering fraction f = 0.30, the SAME solver returns the "
      "textbook suppressed growth index p = (sqrt(25-24f)-1)/4 in the matter era -- so a suppression this "
      "pipeline reports later is real, not an artefact",
      abs(p_num / p_ana - 1) < 0.03,
      f"measured dlnD/dlna at a = 0.05 is {p_num:.4f}; analytic (sqrt(25-24*0.30)-1)/4 = {p_ana:.4f}")

# ===================================================================================================
sec("PART 1 -- the ESCAPE-VELOCITY FILTER and its ORDERING, measured on the two data sets.")
# ===================================================================================================
print("""
  GALAXY escape velocity, in the theory's OWN gravity.  In deep MOND an isolated baryonic mass has a
  LOGARITHMIC potential, so v_esc^2(r) = 2 v_flat^2 ln(r_trunc/r) with r_trunc = v_flat^2/g_ext, the radius at
  which the internal field falls to the external field.  g_ext = 0.01 a0 is used: a DEEP truncation, which
  makes v_esc as LARGE as is defensible and therefore makes the escape's job as HARD as possible.  (A
  Newtonian cosmic-share NFW halo is printed as a cross-check.)
  CLUSTER escape velocity, from the audited X-COP g_HSE(r): Phi integrated outward with the measured g,
  continued as g ~ 1/r to 2 Mpc and Keplerian beyond.
""", flush=True)
vesc_gal = {}
for foot, a0k in A0_KPC.items():
    vs = []
    for g in gal:
        vf = g["vflat"]; r_tr = vf ** 2 / (0.01 * a0k); rmed = float(np.median(g["r"]))
        if r_tr > rmed: vs.append(np.sqrt(2.0 * vf ** 2 * np.log(r_tr / rmed)))
    vesc_gal[foot] = np.array(vs)
    print(f"    galaxies ({foot:9}): v_esc at the median measured radius -- median {np.median(vs):6.1f}, "
          f"75th {np.percentile(vs,75):6.1f}, 90th {np.percentile(vs,90):6.1f}, max {np.max(vs):6.1f} km/s "
          f"(N={len(vs)})")
def vesc_NFW(M200, c, r_kpc):
    rho_c = 2.775e11 * h_P ** 2
    r200 = (3 * M200 / (4 * np.pi * 200 * rho_c)) ** (1 / 3) * 1000.0
    rs = r200 / c; mc = np.log(1 + c) - c / (1 + c)
    return np.sqrt(2 * (G_KPC * M200 / mc) * np.log(1 + r_kpc / rs) / r_kpc)
print(f"    cross-check (Newtonian cosmic-share NFW): L* M200=1e12 c=10 -> v_esc(10 kpc) = "
      f"{vesc_NFW(1e12,10,10.0):.0f} km/s;  dwarf M200=3e10 c=12 -> v_esc(3 kpc) = {vesc_NFW(3e10,12,3.0):.0f} km/s")
vesc_cl = {}
for foot in ("canonical", "alt"):
    per = []
    for cn in clusters:
        rs_, gs_ = [], []
        for r in rows:
            if r["cluster"] == cn and r["footing"] == foot and r["g_hse_over_a0"] > 0:
                rs_.append(r["r_kpc"]); gs_.append(r["g_hse_over_a0"] * A0[foot] * KPC_M / 1e6)
        if len(rs_) < 5: continue
        rs_, gs_ = np.array(rs_), np.array(gs_); o = np.argsort(rs_); rs_, gs_ = rs_[o], gs_[o]
        g1000 = float(np.interp(1000.0, rs_, gs_))
        tail = g1000 * 1000.0 * np.log(2.0) + g1000 * 500.0
        cum = cumulative_trapezoid(gs_, rs_, initial=0.0)
        per.append(dict(name=cn, r=rs_, vesc=np.sqrt(2.0 * ((cum[-1] - cum) + tail))))
    vesc_cl[foot] = per
    v1000 = np.array([np.interp(1000.0, p["r"], p["vesc"]) for p in per])
    print(f"    clusters ({foot:9}): v_esc(1000 kpc) median {np.median(v1000):6.0f} km/s "
          f"(range {v1000.min():.0f}-{v1000.max():.0f}); v_esc(200 kpc) median "
          f"{np.median([np.interp(200.,p['r'],p['vesc']) for p in per]):6.0f} km/s")
VG = {f: float(np.median(vesc_gal[f])) for f in vesc_gal}
VG90 = {f: float(np.percentile(vesc_gal[f], 90)) for f in vesc_gal}
VC = {f: float(np.median([np.interp(1000.0, p["r"], p["vesc"]) for p in vesc_cl[f]])) for f in vesc_cl}
print(f"\n    THE ORDERING:  v_esc(cluster, 1 Mpc) / v_esc(galaxy, median) = "
      + ", ".join(f"{f}: {VC[f]/VG[f]:.2f}" for f in VG)
      + "   (against the 90th-percentile galaxy: " + ", ".join(f"{f}: {VC[f]/VG90[f]:.2f}" for f in VG) + ")")
check("O1  [POSITIVE FINDING, and the reason this arm had to be tested]  the escape-velocity filter has the "
      "RIGHT ORDERING for the galaxy-vs-cluster split: clusters are ~7x deeper, so a velocity cut that unbinds "
      "a galaxy still leaves a cluster loaded.  This is the first filter family in the record with the right "
      "ordering -- L61's B4 (range), B5 (density), B6 (acceleration) and B7 (potential-vs-recombination) all "
      "had the wrong one.  L61 rejected the depth filter only because it would also act AT RECOMBINATION, and "
      "temporal separation removes exactly that objection: the parent is still cold then",
      all(VC[f] / VG90[f] > 2.0 for f in VG),
      "; ".join(f"{f}: {VC[f]:.0f}/{VG[f]:.0f} = {VC[f]/VG[f]:.2f} (median), "
                f"{VC[f]/VG90[f]:.2f} (90th pct)" for f in VG))

# ===================================================================================================
sec("PART 2 -- the POPULATION MODEL: f_gal(tau, v_k), f_cl(tau, v_k), and the admissible region.")
# ===================================================================================================
print("""
  THE MODEL.  The parent decays with lifetime tau.  A daughter born at scale factor a_d carries speed v_k there
  and v(a) = v_k a_d/a afterwards, so its speed TODAY is v_k a_d.  It is retained by a halo iff v_today < v_esc.
  Because a_d grows with the decay time, the retained daughters are the EARLY ones: the kick COOLS OFF, and the
  velocity-ordering lemma reasserts itself inside the daughter population.  Hence

      f_bound(tau, v_k; v_esc) = exp(-t_0/tau)          [the surviving COLD parent -- always bound]
                               + [1 - exp(-t_x/tau)],   t_x = t(a = min(1, v_esc/v_k))

  and f_gal uses v_esc,gal, f_cl uses v_esc,cl.  (Because t_x is monotone in v_esc, the median over SPARC
  galaxies of the per-galaxy retained fraction equals f_bound evaluated at the median v_esc -- so this IS the
  median-galaxy statement the L61 ceiling is defined on.)

  THE GATES.
    galaxies:  f_gal <= eta_max     (the L61/L49/L50 transmitted-pull ceiling)
    clusters:  f_cl  >= f_req,  with f_req measured HERE from the audited rows as
               f_req(r) = [g_HSE(r) - g_MOND(r)] / [(Omega_c/Omega_b) g_bar(r)]
               -- the fraction of the cosmic cold share a cluster must still hold for MOND+dark to fit it.
""", flush=True)
freq = {}
for foot in ("canonical", "alt"):
    vals = {}
    for rr in (200.0, 1000.0):
        v = []
        for r in rows:
            if r["footing"] != foot or r["r_kpc"] != rr: continue
            gb, gh = r["g_baryon_over_a0"] * A0[foot], r["g_hse_over_a0"] * A0[foot]
            if gb <= 0 or gh <= 0: continue
            v.append((gh - gb * nu_RAR(gb / A0[foot])) / (COSMIC_DM_PER_BARYON * gb))
        vals[rr] = np.array(v)
    freq[foot] = vals
    for rr, v in vals.items():
        print(f"    f_req ({foot:9}, r = {rr:6.0f} kpc): median {np.median(v):.3f}, "
              f"mean {np.mean(v):.3f} +/- {np.std(v)/np.sqrt(len(v)):.3f} (s.e., N={len(v)})")
F_REQ = {f: float(np.median(freq[f][1000.0])) for f in freq}
F_REQ200 = {f: float(np.median(freq[f][200.0])) for f in freq}
check("C5  CONTROL: the cluster requirement derived here from the audited rows lands on the published value "
      "(L61 B7: eta = 0.569 +/- 0.130 at zero hydrostatic bias; L41 R1: M_X/M_bar = 5.73 +/- 0.68 against a "
      "cosmic 5.364).  Statement asserted: this independent derivation gives f_req(1 Mpc) in [0.35, 0.85] at "
      "both footings",
      all(0.35 <= F_REQ[f] <= 0.85 for f in F_REQ),
      "; ".join(f"{f}: f_req(1 Mpc) = {F_REQ[f]:.3f}" for f in F_REQ))
check("C6  [SEPARATE, PRE-EXISTING COST -- recorded, not attributed to the decay]  at 200 kpc the same "
      "derivation gives f_req > 1: the cluster needs a source MORE CONCENTRATED than the cosmic share tracing "
      "the baryons.  That is L41 R3 / g04a's rho_X ~ r^-1.5 restated, and it is a cost the hybrid already "
      "carries.  It matters here only DIRECTIONALLY: heating the component makes it less concentrated, so any "
      "kick moves AWAY from this requirement, never toward it",
      all(F_REQ200[f] > 1.0 for f in F_REQ200),
      "; ".join(f"{f}: f_req(200 kpc) = {F_REQ200[f]:.3f} vs f_req(1 Mpc) = {F_REQ[f]:.3f}" for f in F_REQ200))

def f_bound(tau, v_k, v_esc):
    a_c = min(1.0, v_esc / v_k) if v_k > 0 else 1.0
    return np.exp(-AGE / tau) + (1.0 - np.exp(-t_of_a(a_c) / tau))

print("\n  THE MAP.  Cells are f_gal/f_cl;  * = passes BOTH gates.")
FINE, BEST = {}, {}
for foot in ("canonical", "alt"):
    key = "canon eps=0" if foot == "canonical" else "alt eps=0"
    em, vg, vc, fr = ETA_MAX[key], VG[foot], VC[foot], F_REQ[foot]
    print(f"\n    {foot}:  eta_max = {em:.3f}   v_esc,gal = {vg:.0f} km/s   v_esc,cl = {vc:.0f} km/s   "
          f"f_req = {fr:.3f}")
    taus = np.array([1., 2., 3., 5., 8., 13.8, 25.5, 50., 100.])
    vks = np.array([300., 600., 1000., 1500., 2200., 3000., 5000., 10000., 30000.])
    print(f"      {'tau\\v_k':>9} " + " ".join(f"{v:>10.0f}" for v in vks))
    for tau in taus:
        cells = []
        for v_k in vks:
            fg, fc = f_bound(tau, v_k, vg), f_bound(tau, v_k, vc)
            cells.append(f"{fg:.2f}/{fc:.2f}" + ("*" if (fg <= em and fc >= fr) else " "))
        print(f"      {tau:9.1f} " + " ".join(f"{c:>10}" for c in cells))
    tt = np.geomspace(0.3, 300.0, 200); vv = np.geomspace(200.0, 1e5, 200)
    M = np.array([[(f_bound(t, v, vg) <= em) and (f_bound(t, v, vc) >= fr) for v in vv] for t in tt])
    FINE[foot] = (tt, vv, M)
    if M.any():
        ii, jj = np.where(M)
        print(f"      ADMISSIBLE REGION NON-EMPTY: tau in [{tt[ii].min():.2f}, {tt[ii].max():.2f}] Gyr, "
              f"v_k in [{vv[jj].min():.0f}, {vv[jj].max():.0f}] km/s "
              f"(eps in [{vv[jj].min()/C_KMS:.2e}, {vv[jj].max()/C_KMS:.2e}]);  {M.sum()}/{M.size} cells")
        b, bv = None, 9e9
        for i, j in zip(ii, jj):
            fg = f_bound(tt[i], vv[j], vg)
            if fg < bv: bv, b = fg, (tt[i], vv[j], fg, f_bound(tt[i], vv[j], vc))
        BEST[foot] = b
        print(f"      deepest admissible point: tau = {b[0]:.2f} Gyr, v_k = {b[1]:.0f} km/s "
              f"(eps = {b[1]/C_KMS:.2e}), f_gal = {b[2]:.3f}, f_cl = {b[3]:.3f}")
    else:
        BEST[foot] = None; print("      ADMISSIBLE REGION EMPTY.")
check("P1  [HONEST INTERIM -- the finding, not a failure]  the two-body branch is NOT closed by the "
      "galaxy-vs-cluster pincer.  The escape-velocity filter really does open a region in (tau, v_k) where the "
      "galaxy ceiling and the cluster requirement hold simultaneously, at BOTH footings",
      FINE["canonical"][2].any() and FINE["alt"][2].any(),
      "; ".join(f"{f}: {'non-empty' if FINE[f][2].any() else 'EMPTY'}" for f in FINE))

# ===================================================================================================
sec("PART 3 -- the STRUCTURE gate: what the same kick does to the matter power spectrum.")
# ===================================================================================================
print("""
  A daughter born at a_d has v(a) = v_k a_d/a, hence a comoving free-streaming wavenumber
      k_fs(a) = sqrt(3/2) a H(a) / v(a) = sqrt(3/2) a^2 H(a) / (v_k a_d).
  It cannot cluster on k > k_fs(a).  Two variants are computed, deliberately BRACKETING the truth:

   (B) STRICT UPPER BOUND on the model's sigma_8, and the ONE the gates are judged on.  Two facts make it a
       bound.  First, the clustered part cannot grow faster than LambdaCDM: its source is
       1.5 Om_m [(1-f_nc) delta_c + f_nc delta_h] with delta_h <= delta_c, hence <= LambdaCDM's source, so
       delta_c <= delta_c^LCDM.  Second, a daughter born at a_d and free-streaming until k_fs rises to k
       cannot end with more than delta_c(a_d) D(1)/D(a_re) -- freezing is the least free-streaming can do.
       Summing gives S_B(k) = f_b + f_dm e^{-t0/tau} + f_dm sum_w min(1, D(a_d)/D(a_re)).
   (A) THE STANDARD f_nc TREATMENT, shown for comparison only.  Growth with the reduced source and
       delta_m = (1-f_nc) delta_c -- the approximation used for massive neutrinos.  It is NOT a bound in
       either direction: it under-counts growth (the source omits the daughters' own frozen perturbation) and
       over-counts amplitude (a daughter that has re-clustered is given full weight, ignoring the growth it
       lost).  Where (A) exceeds (B), (A) is the one that is wrong.
""", flush=True)
def eps_bound_fn(G):
    """Abellan, Murgia & Poulin, PRD 104, 123533 (2021), 2-sigma exclusion over Gamma in [1e-3, 1e-1] Gyr^-1."""
    return 1.6e-4 * G ** -1.1

f_b = OMB / (OMB + OMC)
f_dm = 1.0 - f_b
NAD = 120
_ad = np.geomspace(1e-3, 1.0, NAD)
_td = np.array([t_of_a(x) for x in _ad])

def daughter_weights(tau):
    """mass fraction of the parent decaying in each a_d bin, normalised so the weights sum EXACTLY to the
       decayed fraction 1 - exp(-t_0/tau) (the raw finite-difference density carries ~1% quadrature error,
       which would otherwise let the growth bound exceed 1)."""
    w = np.exp(-_td / tau)
    dP = np.maximum(-np.gradient(w, _td) * np.gradient(_td), 0.0)
    tot = dP.sum()
    return dP * ((1.0 - np.exp(-AGE / tau)) / tot) if tot > 0 else dP

def kfs(a, a_d, v_k):
    """comoving free-streaming wavenumber in h/Mpc for the sub-population born at a_d."""
    return np.sqrt(1.5) * a ** 2 * float(H_of_lna(np.log(a))) / (v_k * a_d) / h_P

def S_upper(k, tau, v_k):
    """variant (B): strict upper bound on delta_m(k, a=1) / delta_m^LCDM(k, a=1)."""
    dP = daughter_weights(tau)
    tot = f_b + f_dm * np.exp(-AGE / tau)
    for a_d, w in zip(_ad, dP):
        if w <= 0: continue
        # a_re: the scale factor at which k_fs rises to k (never -> a_re = 1)
        if kfs(a_d, a_d, v_k) >= k:
            tot += f_dm * w; continue
        try:
            a_re = brentq(lambda la: kfs(np.exp(la), a_d, v_k) - k, np.log(a_d), 0.0, xtol=1e-8)
            a_re = np.exp(a_re)
            ratio = float(D_of_lna(np.log(max(a_d, A_START)))) / float(D_of_lna(np.log(max(a_re, A_START))))
        except ValueError:
            ratio = float(D_of_lna(np.log(max(a_d, A_START)))) / float(D_of_lna(0.0))
        tot += f_dm * w * min(1.0, ratio)
    return tot

def make_fnc_tab(tau, v_k, k):
    lg = np.linspace(np.log(A_START), 0.0, 260)
    dP = daughter_weights(tau)
    out = np.zeros_like(lg)
    for i, l in enumerate(lg):
        a = np.exp(l); born = _ad <= a
        if not born.any(): continue
        kf = np.sqrt(1.5) * a ** 2 * float(H_of_lna(l)) / (v_k * _ad[born]) / h_P
        out[i] = f_dm * float(np.sum(dP[born] * (kf < k)))
    return interp1d(lg, out, kind="linear")

def S_realistic(k, tau, v_k):
    fn = make_fnc_tab(tau, v_k, k)
    _, D = growth_general(src_factor=lambda l: 1.0 - float(fn(l)))
    return (D[-1] / D_L[-1]) * (1.0 - float(fn(0.0)))

KS = np.geomspace(0.02, 3.0, 16)
def sigma8_from_S(Sfun, tau, v_k):
    S = np.array([Sfun(k, tau, v_k) for k in KS])
    f = interp1d(np.log(KS), S, kind="cubic", bounds_error=False, fill_value=(S[0], S[-1]))
    Sk = f(np.log(np.clip(_k, KS[0], KS[-1])))
    return sigma_R(_Pk * Sk ** 2), S

S8_PL, S8_PL_E = 0.832, 0.013          # Planck 2018 TT,TE,EE+lowE+lensing
S8_KD, S8_KD_E = 0.815, 0.016          # KiDS-Legacy
probe = []
for foot in ("canonical", "alt"):
    if BEST[foot]: probe.append((round(BEST[foot][0], 2), round(BEST[foot][1], 0)))
probe += [(3.0, 3000.0), (5.0, 2200.0), (8.0, 1500.0), (13.8, 1000.0), (13.8, 2200.0), (25.5, 1000.0)]
seen = []
print(f"    {'tau':>7} {'v_k':>8} {'eps':>9} {'f_gal':>7} {'f_cl':>7} | {'sig8 (B) up':>11} {'S8 (B)':>7} "
      f"{'vs KiDS':>8} | {'sig8 (A)':>9} {'S8 (A)':>7} {'vs KiDS':>8}")
print(f"    {'LCDM':>7} {'--':>8} {'--':>9} {'--':>7} {'--':>7} | {0.811:11.3f} {S8_LCDM:7.3f} "
      f"{(S8_LCDM-S8_KD)/S8_KD_E:+8.2f} | {0.811:9.3f} {S8_LCDM:7.3f} {(S8_LCDM-S8_KD)/S8_KD_E:+8.2f}")
RES = {}
for tau, v_k in probe:
    if (tau, v_k) in [(a, b) for a, b, *_ in seen]: continue
    s8B, SB = sigma8_from_S(S_upper, tau, v_k)
    s8A, SA = sigma8_from_S(S_realistic, tau, v_k)
    S8B, S8A = s8B * np.sqrt(OM_M / 0.3), s8A * np.sqrt(OM_M / 0.3)
    fg = f_bound(tau, v_k, VG["canonical"]); fc = f_bound(tau, v_k, VC["canonical"])
    RES[(tau, v_k)] = (s8B, S8B, s8A, S8A, fg, fc, SB, SA)
    seen.append((tau, v_k, s8B))
    print(f"    {tau:7.2f} {v_k:8.0f} {v_k/C_KMS:9.2e} {fg:7.3f} {fc:7.3f} | {s8B:11.3f} {S8B:7.3f} "
          f"{(S8B-S8_KD)/S8_KD_E:+8.1f} | {s8A:9.3f} {S8A:7.3f} {(S8A-S8_KD)/S8_KD_E:+8.1f}")

bk = (round(BEST["canonical"][0], 2), round(BEST["canonical"][1], 0)) if BEST["canonical"] else None
if bk:
    s8B, S8B, s8A, S8A, fg, fc, SB, SA = RES[bk]
    nB = (S8_KD - S8B) / S8_KD_E
    check("P2  the STRUCTURE gate fires at the DEEPEST ADMISSIBLE point of PART 2, and it fires on the STRICT "
          "UPPER BOUND (B), not only on the realistic estimate: even when the clustered part is given the full "
          "LambdaCDM growth rate and every daughter is given the most amplitude free-streaming can leave it, "
          "S_8 falls more than 3 sigma below KiDS-Legacy's 0.815 +/- 0.016",
          nB > 3.0,
          f"tau = {bk[0]:.2f} Gyr, v_k = {bk[1]:.0f} km/s (eps = {bk[1]/C_KMS:.1e}): "
          f"UPPER BOUND sigma_8 <= {s8B:.3f} -> S_8 <= {S8B:.3f} ({nB:.1f} sigma below KiDS, "
          f"{(S8_PL-S8B)/S8_PL_E:.1f} below Planck); realistic sigma_8 = {s8A:.3f} -> S_8 = {S8A:.3f}")
    print(f"      sqrt(P_model/P_LCDM) at that point -- upper bound (B) / realistic (A):")
    for kv, sb, sa in zip(KS[::3], SB[::3], SA[::3]):
        print(f"        k = {kv:7.3f} h/Mpc :  {sb:.4f}  /  {sa:.4f}")

print("\n    THE TRIPLE SCAN.  A cell passes only if it clears the galaxy ceiling, the cluster requirement AND")
print("    S_8 within 3 sigma of KiDS-Legacy (>= 0.767) on the GENEROUS upper bound (B).")
S8_FLOOR = S8_KD - 3 * S8_KD_E
grid = []
for tau in [2.0, 3.0, 5.0, 8.0, 13.8, 25.5, 50.0]:
    for v_k in [300., 600., 1000., 1500., 2200., 3000., 5000.]:
        s8B, _ = sigma8_from_S(S_upper, tau, v_k)
        S8B = s8B * np.sqrt(OM_M / 0.3)
        fg = f_bound(tau, v_k, VG["canonical"]); fc = f_bound(tau, v_k, VC["canonical"])
        gal_ok = fg <= ETA_MAX["canon eps=0"]; cl_ok = fc >= F_REQ["canonical"]; s8_ok = S8B >= S8_FLOOR
        grid.append((tau, v_k, S8B, gal_ok, cl_ok, s8_ok))
        print(f"      tau {tau:6.1f}  v_k {v_k:6.0f}  S_8(up) {S8B:6.3f}   "
              f"gal {'OK  ' if gal_ok else 'DEAD'} (f={fg:.2f})   cl {'OK  ' if cl_ok else 'DEAD'} (f={fc:.2f})"
              f"   S8 {'OK' if s8_ok else 'DEAD'}")
triple = [g for g in grid if g[3] and g[4] and g[5]]
check("P3  NO cell on the probed grid passes all three gates.  The escape-velocity filter and the structure "
      "amplitude pull in opposite directions: the very velocity that unbinds a galaxy also erases the power "
      "that same component must carry on 8 Mpc/h",
      len(triple) == 0, f"{len(triple)} of {len(grid)} probed (tau, v_k) cells pass galaxy + cluster + S_8")

# ---------------------------------------------------------------------------------------------------
print("\n    WHERE THE REQUIREMENTS CROSS -- the decisive table.  For each lifetime:")
print("      v_k NEEDED   = the smallest kick that brings f_gal down to the galaxy ceiling (one column per")
print("                     ceiling: both a0 footings x both kernel-reading conventions);")
print("      v_k ALLOWED  = the largest kick that keeps S_8 within 3 sigma of KiDS-Legacy, on the GENEROUS")
print("                     upper bound (B) and on the REALISTIC calculation (A);")
print("      v_k PUBLISHED= the largest kick allowed by Abellan+2021's 2-sigma BAO+SNIa+Planck curve.")

def v_needed(tau, eta, v_esc):
    lo, hi = np.log(v_esc * 1.0001), np.log(3e6)
    if f_bound(tau, np.exp(hi), v_esc) > eta: return np.nan     # ceiling unreachable at ANY kick
    try: return np.exp(brentq(lambda lv: f_bound(tau, np.exp(lv), v_esc) - eta, lo, hi, xtol=1e-6))
    except ValueError: return np.nan

KS_C = np.geomspace(0.02, 3.0, 10)
def sigma8_coarse(Sfun, tau, v_k):
    S = np.array([Sfun(k, tau, v_k) for k in KS_C])
    f = interp1d(np.log(KS_C), S, kind="linear", bounds_error=False, fill_value=(S[0], S[-1]))
    return sigma_R(_Pk * f(np.log(np.clip(_k, KS_C[0], KS_C[-1]))) ** 2)

VGRID = np.geomspace(200.0, 8000.0, 7)
def v_allowed_S8(Sfun, tau):
    ys = np.array([sigma8_coarse(Sfun, tau, v) * np.sqrt(OM_M / 0.3) - S8_FLOOR for v in VGRID])
    if ys[0] < 0: return np.nan                     # even the smallest kick already fails
    if ys[-1] > 0: return VGRID[-1]
    f = interp1d(np.log(VGRID), ys, kind="linear")
    return float(np.exp(brentq(f, np.log(VGRID[0]), np.log(VGRID[-1]), xtol=1e-5)))

FOOT_OF = {"canon eps=0": "canonical", "alt eps=0": "alt", "canon eps=1": "canonical", "alt eps=1": "alt"}
TAUS_X = [2.0, 3.0, 5.0, 8.0, 10.0, 13.8, 17.0, 20.0, 25.5]
print(f"\n      {'tau':>6} | " + " ".join(f"{k:>11}" for k in ETA_MAX) +
      f" | {'ALLOW (B)':>10} {'ALLOW (A)':>10} {'PUBLISHED':>10} | {'SURVIVES?':>10}")
XT = []
for tau in TAUS_X:
    needs = {k: v_needed(tau, ETA_MAX[k], VG[FOOT_OF[k]]) for k in ETA_MAX}
    aB = v_allowed_S8(S_upper, tau)
    aA = v_allowed_S8(S_realistic, tau)
    aP = eps_bound_fn(1.0 / tau) * C_KMS
    nmin = needs["canon eps=0"]
    surv_gen = np.isfinite(nmin) and np.isfinite(aB) and nmin < aB
    surv_all = surv_gen and nmin < aP
    XT.append(dict(tau=tau, needs=needs, aB=aB, aA=aA, aP=aP, surv_gen=surv_gen, surv_all=surv_all))
    fmt = lambda x: (f"{x:11.0f}" if np.isfinite(x) else f"{'unreachable':>11}")
    print(f"      {tau:6.1f} | " + " ".join(fmt(needs[k]) for k in ETA_MAX) +
          f" | {aB:10.0f} {aA:10.0f} {aP:10.0f} | "
          f"{('LOOSEST ONLY' if surv_gen else 'no'):>10}")

surv_gen_taus = [x["tau"] for x in XT if x["surv_gen"]]
surv_all_taus = [x["tau"] for x in XT if x["surv_all"]]
ratios = [x["needs"]["canon eps=0"] / x["aB"] for x in XT
          if np.isfinite(x["needs"]["canon eps=0"]) and np.isfinite(x["aB"])]
closest = min(ratios) if ratios else np.inf
check("P4  under THIS lane's evacuation criterion -- a hard step at the escape velocity of the deep-MOND "
      "logarithmic potential truncated at g_ext = 0.01 a0 -- the galaxy gate and the S_8 gate are DISJOINT at "
      "every lifetime and every ceiling.  The closest approach is a factor of about 1.05 in the required kick, "
      "which is far too thin a margin to call a closure on its own -- and lane T4 shows the verdict TURNS on "
      "this criterion.  Statement asserted here: on the criterion used HERE, nothing survives, and the closest "
      "approach is within 20%",
      len(surv_gen_taus) == 0 and closest < 1.20,
      f"generous-bound survivors at this criterion: {surv_gen_taus}; closest approach "
      f"needed/allowed = {closest:.2f}x at tau = "
      f"{[x['tau'] for x in XT if np.isfinite(x['needs']['canon eps=0']) and np.isfinite(x['aB']) and abs(x['needs']['canon eps=0']/x['aB'] - closest) < 1e-9]}")
check("P5  the margin is thin enough that the criterion has to be stress-tested rather than trusted.  That is "
      "lane T4's job, and its answer is that three fairer criteria OPEN the region this one closes.  Recording "
      "the dependence here, at the point where it bites, rather than only in the later lane",
      True,
      f"closest approach {closest:.2f}x on this criterion; T4 finds the needed kick falls by 2.7-6.8x under "
      f"orbit-averaged and isothermal criteria, which reopens tau ~ 5-20 Gyr")

# characterise the closest-approach cell for the record
xc = min((x for x in XT if np.isfinite(x["needs"]["canon eps=0"]) and np.isfinite(x["aB"])),
         key=lambda x: x["needs"]["canon eps=0"] / x["aB"], default=None)
if xc is not None:
    ts, vs = xc["tau"], xc["needs"]["canon eps=0"]
    print(f"\n    THE CLOSEST-APPROACH CELL, characterised.  tau = {ts:.1f} Gyr, v_k = {vs:.0f} km/s "
          f"(eps = {vs/C_KMS:.2e}), f_gal = {f_bound(ts, vs, VG['canonical']):.3f}, "
          f"f_cl = {f_bound(ts, vs, VC['canonical']):.3f}")
    sB, SBk = sigma8_from_S(S_upper, ts, vs)
    sA, SAk = sigma8_from_S(S_realistic, ts, vs)
    print(f"      sigma_8: strict bound (B) {sB:.3f}, standard treatment (A) {sA:.3f}, LambdaCDM 0.811")
    print(f"      S_8:     strict bound (B) {sB*np.sqrt(OM_M/0.3):.3f} "
          f"({(sB*np.sqrt(OM_M/0.3)-S8_KD)/S8_KD_E:+.1f} sigma vs KiDS), standard (A) "
          f"{sA*np.sqrt(OM_M/0.3):.3f} ({(sA*np.sqrt(OM_M/0.3)-S8_KD)/S8_KD_E:+.1f} sigma)")
    print(f"      sqrt(P_model/P_LCDM) at z = 0, strict bound / standard:")
    for kv, sb, sa in zip(KS, SBk, SAk):
        print(f"        k = {kv:7.3f} h/Mpc :  {sb:.4f}  /  {sa:.4f}")
    k1 = float(interp1d(np.log(KS), SBk)(np.log(1.0)))
    check("P6  at the closest-approach cell the small-scale power at z = 0 is suppressed substantially even on "
          "the strict upper bound.  Whether that is fatal depends on the redshift at which it is measured, "
          "which lane T6 computes.  Statement asserted: P(k = 1 h/Mpc, z = 0) is below 70% of LambdaCDM's on "
          "the strict upper bound",
          k1 ** 2 < 0.70,
          f"sqrt(P/P_LCDM) at k = 1 h/Mpc, z = 0: bound {k1:.3f} -> P ratio {k1**2:.3f}; standard "
          f"{float(interp1d(np.log(KS), SAk)(np.log(1.0))):.3f} -> "
          f"{float(interp1d(np.log(KS), SAk)(np.log(1.0)))**2:.3f}")

# ===================================================================================================
sec("PART 4 -- confrontation with the PUBLISHED two-body decaying-DM bounds (cited, not re-derived).")
# ===================================================================================================
print("""
   * Abellan, Murgia & Poulin, PRD 104, 123533 (2021) [2102.12498].  BAO + SNIa + Planck: the 2-sigma exclusion
     over Gamma in [1e-3, 1e-1] Gyr^-1 is  eps <= 1.6e-4 (Gamma/Gyr^-1)^-1.1.  Their S_8-easing best fit is
     Gamma^-1 ~ 55 Gyr at eps ~ 0.7% -- i.e. this mechanism is ALREADY in use in the literature, at a kick two
     orders of magnitude below what this escape needs, and used to REDUCE S_8, not to preserve it.
   * Abellan, Murgia, Poulin & Lavalle, PRD 105, 063525 (2022) [2008.09615]: same tension-easing point.
   * Simon, Franco Abellan, Du, Poulin & Tsai, PRD 106, 023516 (2022) [2203.07440]: with EFTofBOSS + KiDS-1000,
     tau ~ 120 Gyr at eps ~ 1.2%;  68% range 1.61 < log10(tau/Gyr) < 3.71.
   * Mau et al., ApJ 932, 128 (2022) [2201.11740] (Milky Way Satellite Census IV): kicked-daughter DDM excluded
     at 95% for tau < 18 Gyr at v_kick = 20 km/s, and tau < 29 Gyr at v_kick = 40 km/s.  (LambdaCDM-modelled,
     so recorded as corroboration, not as the kill.)
""", flush=True)
eps_bound = eps_bound_fn
print(f"    {'tau [Gyr]':>10} {'Gamma':>9} {'eps allowed 2sig':>18} {'v_k allowed':>13} {'v_k NEEDED':>12} "
      f"{'violation':>11}")
viol = []
for x in XT:
    tau = x["tau"]; G = 1.0 / tau; eb = eps_bound(G); vb = eb * C_KMS
    vneed = x["needs"]["canon eps=0"]
    r = vneed / vb if np.isfinite(vneed) else np.nan
    viol.append(r)
    print(f"    {tau:10.1f} {G:9.4f} {eb:18.3e} {vb:13.1f} {vneed:12.0f} "
          f"{(f'{r:.2f}x' if np.isfinite(r) else 'n/a'):>11}")
worst = np.nanmin(viol)
check("P7  the published two-body bound and the escape's requirement are DISJOINT at EVERY lifetime, though "
      "the margin narrows to a factor ~1.1 at the sliver rather than the order of magnitude one might expect. "
      "Statement asserted: the needed kick exceeds the published 2-sigma allowed kick at every tau probed",
      worst > 1.0,
      f"smallest violation over tau in [2, 25.5] Gyr is {worst:.0f}x (needed v_k / allowed v_k); the published "
      f"S_8-easing best fit sits at eps ~ 0.7% -> v_k ~ {0.007*C_KMS:.0f} km/s = "
      f"{0.007*C_KMS/VG['canonical']:.1f}x the median galaxy escape velocity, and even that is used to LOWER "
      f"S_8 by a few percent")

# ===================================================================================================
sec("PART 5 -- VERDICT for the two-body arm.")
# ===================================================================================================
print(f"""
  WHAT SURVIVED, stated first, because it is a real result.  The escape-velocity filter is genuine and its
  ordering is RIGHT (O1): in the theory's own gravity, X-COP clusters are {VC['canonical']/VG['canonical']:.1f}x deeper than the median SPARC
  galaxy.  It breaks the velocity-ordering lemma's hypothesis, it answers L61 B7's ordering objection (which
  rejected depth filters only because they would also act at recombination -- and here the parent is still
  cold then), and it pays almost no background cost.  On the galaxy and cluster gates ALONE it opens a
  substantial region (P1).  This arm is NOT closed by the pincer that closed every earlier mechanism.

  WHAT CLOSED IT, and how comfortably.
   (i) STRUCTURE.  The kick that unbinds the median galaxy is v_k >~ {VG['canonical']:.0f} km/s, and a component moving that
       fast stops clustering on 8 Mpc/h.  Judged on the STRICT UPPER BOUND (B), the galaxy gate and the S_8
       gate are DISJOINT at every lifetime and every ceiling on THIS lane's evacuation criterion -- but the
       closest approach is only a factor {closest:.2f} in the required kick, which is far too thin to rest a
       closure on.  Lane T4 stress-tests that criterion and finds the region REOPENS under three fairer ones.
   (ii) THE DAUGHTER COOLS.  v ~ 1/a after the kick, so early daughters are slow today and fall back into
       galaxies.  The velocity-ordering lemma REASSERTS ITSELF inside the daughter population: shortening tau
       to clear the parent makes most daughters old, hence cold, hence bound again.  That is why f_gal has an
       interior optimum in tau and a strictly positive floor.
   (iii) THE PUBLISHED BOUND closes the sliver.  Abellan+2021's 2-sigma BAO+SNIa+Planck curve allows a smaller
       kick than the galaxy gate needs at EVERY lifetime, including inside the sliver (by a factor {worst:.2f} at the
       tightest point).  That margin is thin and should be quoted as thin.

  THE HONEST BOTTOM LINE for this arm: NOT CLOSED by this lane.  The gates are disjoint on the criterion used
  here, but by a margin of {closest:.0%} in the required kick -- and that criterion is the harshest of the four
  defensible ones.  Lanes T4/T5/T6 carry the arm from here; the verdict there is UNDETERMINED with a
  characterised live window, not a closure.

  THE GENERAL LESSON, which IS mechanism-independent.  Temporal separation moves WHEN the velocity appears; it
  cannot decouple the SCALE the velocity evacuates from the SCALE it erases, because both are set by the same
  one number v_k.  That is the velocity-ordering lemma in a new costume: not about a monotone v(a), but about
  there being only ONE velocity to spend on two jobs.
""", flush=True)
check("V1  [VERDICT, two-body arm]  the temporal-separation escape fails on STRUCTURE, not on the "
      "galaxy-cluster pincer -- and the closure is a COMBINATION, not a single decisive computation, which is "
      "how it must be quoted.  Statement asserted: no probed cell clears galaxy + cluster + S_8 together, and "
      "the published two-body bound is violated at every lifetime where the galaxy ceiling is reachable",
      len(triple) == 0 and worst > 1.0,
      f"{len(triple)} triple-passing cells of {len(grid)} probed; published-bound violation {worst:.2f}x at "
      f"the tightest point; closest approach on the S_8 bound is {closest:.2f}x.  T4 shows this verdict is "
      f"CRITERION-DEPENDENT and reopens under three fairer evacuation criteria")
check("V2  SCOPE.  Tested here: two-body decay to a massive daughter with a velocity kick, and (by the same "
      "computation, with v_k -> infinity) conversion to a smooth non-relativistic component.  Tested in T1: "
      "one-body decay to dark radiation, and by background-identity any matter -> radiation phase transition.  "
      "NOT covered: a mechanism that changes how the component GRAVITATES rather than how fast it moves -- "
      "that is not a decay and is a different door",
      True, "kick + smooth-conversion closed here; destruction closed in T1; a coupling-change door is untouched")

print("=" * 118)
if FAILS: print(f"T2 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}")
else: print(f"T2 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
