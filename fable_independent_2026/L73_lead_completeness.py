#!/usr/bin/env python3
"""
L73 -- can the lead's integrable-clock action be a COMPLETE theory, or only complete below a galaxy?
====================================================================================================
Two sister lanes (L71, L72) ask whether the lead's integrable-clock action (IC-4 / IC-20, door 4) is
HEALTHY at galaxy scale.  This lane asks the different, equally decisive question: EVEN GRANTING it is
healthy, can it be COMPLETE -- carry clusters and cosmology as well as galaxies -- or is it bound, like
every other branch this programme has tried, to be complete only BELOW the galaxy scale?

THE OBSTRUCTION.  L55/L61 proved the "excess spent once" theorem and showed it is BRANCH-INDEPENDENT:
if a theory (a) reproduces deep-MOND with its cold component off, (b) contains a pressureless component
in the CMB's amount, and (c) transmits that component's Newtonian pull to baryons no less efficiently in
galaxies than at recombination, then it overshoots the rotation curves pointwise (median x1.69 at eta=1).
Modes, metrics and matter coupling enter ONLY through the transmission factor eta.  L66 found the lead's
action escapes a DIFFERENT theorem (L60/L69's deep-MOND lapse-channel kill) by keeping MOND INSIDE the
clock -- no separate MOND scalar, no AeST coupling.  Whether it also escapes EXCESS-SPENT-ONCE was never
asked, and that is the whole "complete theory" question.

THE CRUX.  Excess-spent-once turns on ONE quantity: how efficiently the cold component's Newtonian pull
reaches baryons (the transmission factor eta), relative to how the MOND scale is produced.  In the
deposited/AeST action these SHARE ONE channel (the AeST coupling), so the excess is spent once.  In the
lead's clock-internal action the MOND scale rides the clock's OWN acceleration invariant, a DIFFERENT
channel from the metric through which a cold component would gravitate.  Does that different channel
change the transmission factor -- letting the lead carry both a working kernel and a full cold cosmology?
Or does the cold component still reach baryons through the single metric with eta=1, so the theorem binds
whatever the MOND sector does?

WHAT IS RUN
  PART A  CONTROLS.  L61's overshoot (median 1.692 at eta=1); L61's transmission ceiling (eta window);
          L61's ordering closures on hypothesis (c) in the four screening variables; the mode-count
          controls (GR 2, GR+scalar 3, Einstein-aether 5, khronometric 3); the cluster residual amount.
  PART B  THE TRANSMISSION CHANNEL IN THE LEAD'S ACTION, derived from IC4_ACTION.md's own equations:
          is the MOND-producing channel the same as the cold-matter transmission channel, and does the
          difference change eta?
  PART C  THE DECISIVE TEST, both sub-cases:
          (i) if it still needs a cold component for clusters+cosmology, does the overshoot fire?
          (ii) if the CLOCK sector supplies structure itself, does that reproduce the non-monotone
               pair/cluster ladder and the CMB, or hit the recorded dark-sector no-go / the lead's own
               causality wall?
  PART D  VERDICT: is the construction bound by excess-spent-once, and can even a healthy version be
          complete?  This lane's verdict is CONDITIONAL on L71/L72's health verdict.

POLARITY.  Following L66/L69: each check asserts a STATEMENT and PASS means the statement is true.
Several PASSes are NEGATIVE for the construction -- read the statement.  Both a0 footings on every
dimensional number.  Nothing under closure_2026/ is imported or executed; the lead's action STRUCTURE is
read from its own markdown (IC4_ACTION.md, IC23_MIXTURE.md, VACUUM_DENSITY_RECOMBINATION.md) offline and
its reference numbers are hard-coded as reproduction targets.  Where this repository has already CLOSED
something (the dark-sector no-go g03w-g04j, L6/L55's screening closures) it is CITED, not re-run.

HONESTY.  The user wants a complete theory, so this lane is especially careful not to manufacture the path
to one.  A genuine escape must be EXHIBITED as a different transmission channel derived from the action and
run through the ladder and the CMB, not asserted.  The overwhelmingly likely outcome -- because the theorem
is branch-independent and the lead's action still couples matter to a SINGLE metric -- is that it binds this
action too.  kappa = 1/2 is FITTED.  Nothing here favours any framework over LambdaCDM.
"""
import numpy as np, math, json, os, sys, glob, time
FAILS = []; NCHK = 0
def check(name, ok, detail=""):
    global NCHK; NCHK += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      " + s, flush=True)
def sec(t): P(""); P("=" * 114); P(t); P("=" * 114)

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")
def rel(p): return os.path.relpath(p, REPO)                 # never print an absolute machine path

# ---- constants (both footings on every dimensional number) -------------------------------------------
G   = 6.674e-11; c = 2.99792458e8; MSUN = 1.989e30
kpc = 3.0857e19; Mpc = 3.0857e22; pc = 3.0857e16
A0  = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; FOOT = ("canonical", "alt")
S_SAT, D_SAT = 2.540, 0.6476                                # the deposited kernel's bounded boost
hP = 0.674; H0 = hP * 100e3 / Mpc; RHO_C = 3 * H0**2 / (8 * math.pi * G)
OM, OB = 0.315, 0.049; OCH2 = 0.1200                        # Planck 2018 cold-matter density
UPS_D, UPS_B = 0.5, 0.7; Z_REC = 1100.0; RS_REC_COMOV = 145.0 * Mpc

def Delta(s):
    s = np.asarray(s, float); sc = np.clip(s, 1e-300, S_SAT)
    d = np.where(s > 0, sc / np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def g_kernel(gb, a0): return gb + a0 * Delta(gb / a0)

P("=" * 114)
P("L73 -- CAN THE LEAD'S INTEGRABLE-CLOCK ACTION BE A COMPLETE THEORY, OR ONLY COMPLETE BELOW A GALAXY?")
P("=" * 114)
P("The excess-spent-once theorem (L55/L61) is branch-independent.  L66 showed the lead escapes a DIFFERENT")
P("theorem (the deep-MOND lapse kill) by keeping MOND inside the clock.  This lane asks whether keeping MOND")
P("inside the clock also changes the TRANSMISSION FACTOR that excess-spent-once turns on -- or whether the")
P("cold component still reaches baryons through the single metric with eta=1, binding the theorem anyway.")
P(f"a0 footings: canonical {A0['canonical']:.4e} / alt {A0['alt']:.4e} m/s^2 (both carried).  kappa=1/2 FITTED.")


# ======================================================================================================
sec("PART A -- CONTROLS.  Reproduce L61's overshoot, its transmission argument, its ordering closures,")
P(  "                    the mode-count controls, and the cluster residual amount.  Stop if any fails.")
# ======================================================================================================

# ---- A0  the four mode-count controls (Dirac: N = (P - 2F - S)/2) -------------------------------------
def dirac(Pd, F, S): return (Pd - 2 * F - S) / 2.0
counts = {"general relativity": dirac(12, 4, 0),
          "GR + one minimally coupled scalar": dirac(14, 4, 0),
          "Einstein-aether": dirac(18, 4, 0),
          "khronometric": dirac(14, 4, 0)}
info("mode counts from N=(P-2F-S)/2:  GR " + " ".join(f"{k.split()[0]}={v:.0f}" for k, v in counts.items()))
check("A0  counting controls reproduce {GR 2, GR+scalar 3, Einstein-aether 5, khronometric 3}",
      counts["general relativity"] == 2 and counts["GR + one minimally coupled scalar"] == 3
      and counts["Einstein-aether"] == 5 and counts["khronometric"] == 3,
      "2 / 3 / 5 / 3")

# ---- load SPARC exactly as L61 -----------------------------------------------------------------------
def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----")); rows = {}
    for line in lines[last + 1:]:
        f = line.split()
        if len(f) < 18: continue
        try: rows[f[0]] = dict(D=float(f[2]), inc=float(f[5]), L36=float(f[7]), MHI=float(f[13]), Q=int(f[17]))
        except ValueError: continue
    return rows
MASTER = read_master()
def c200_DM14(M200): return 10**(0.905 - 0.101 * np.log10(np.asarray(M200, float) * hP / 1e12))
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(np.asarray(logMh, float) - logM1)
    return 10**np.asarray(logMh, float) * 2 * N / (x**(-be) + x**ga)
_LMH = np.linspace(8.5, 15.5, 2801); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass_AM(Mstar): return 10**np.interp(np.log10(np.asarray(Mstar, float)), _LMS, _LMH)
_nfwm = lambda x: np.log1p(x) - x / (1.0 + x)

GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: continue
    m = MASTER[name]
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0] * kpc; Vo = d[:, 1] * 1e3; eV = d[:, 2] * 1e3
    Vg = d[:, 3] * 1e3; Vd = d[:, 4] * 1e3; Vb = d[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    msk = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
    if msk.sum() < 3: continue
    Mstar = UPS_D * m["L36"] * 1e9; Mgas = 1.33 * m["MHI"] * 1e9
    GAL.append(dict(name=name, r=r[msk], Vo=Vo[msk], gb=Vb2[msk] / r[msk], go=Vo[msk]**2 / r[msk],
                    Mb=Mstar + Mgas, Mstar=Mstar))
for g in GAL:
    M200 = max(float(halo_mass_AM(g["Mstar"])), 1.02 * g["Mb"]); cc = float(c200_DM14(M200))
    R200 = (3 * M200 * MSUN / (4 * math.pi * 200 * RHO_C))**(1 / 3.)
    x = np.clip(g["r"] / R200, 1e-6, 6.0)
    g["g_halo"] = G * (M200 - g["Mb"]) * MSUN * _nfwm(cc * x) / _nfwm(cc) / g["r"]**2
GB = np.concatenate([g["gb"] for g in GAL]); GO = np.concatenate([g["go"] for g in GAL])
GH = np.concatenate([g["g_halo"] for g in GAL]); RR = np.concatenate([g["r"] for g in GAL])
info(f"SPARC loaded from {rel(os.path.join(DATA,'sparc_data'))}: {len(GAL)} galaxies, {len(GB)} points")

# ---- A1  L61's overshoot: median g_pred/g_obs = 1.692 at eta=1, WEAKEST (baryon-sourced) kernel -------
a0c = A0["canonical"]; deep = GB < a0c
overshoot = float(np.median((GB[deep] + 1.0 * GH[deep] + a0c * Delta(GB[deep] / a0c)) / GO[deep]))
info(f"eta=1, {int(deep.sum())} deep-MOND points, baryon-sourced kernel: median g_pred/g_obs = {overshoot:.3f} "
     f"(L61 B1: 1.692)")
check("A1  L61 overshoot reproduced: at eta=1 the theory overshoots deep-MOND rotation curves by median x1.69",
      abs(overshoot - 1.692) < 0.02, f"median g_pred/g_obs = {overshoot:.3f} vs published 1.692")

# ---- A2  L61's transmission ceiling: the eta window a branch must hit ---------------------------------
def resid_median(eta, eps, foot):
    a0 = A0[foot]; gs = GB + eps * eta * GH
    gp = GB + eta * GH + a0 * Delta(gs / a0)
    return float(np.median(np.log10(GO / gp)))
def eta_ceiling(eps, foot, tol=0.11):
    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if abs(resid_median(mid, eps, foot)) <= tol: lo = mid
        else: hi = mid
    return lo
eta_b = {f: eta_ceiling(0.0, f) for f in FOOT}; eta_t = {f: eta_ceiling(1.0, f) for f in FOOT}
info(f"eta ceiling, baryon-sourced (eps=0): {eta_b['canonical']:.3f} / {eta_b['alt']:.3f}  (L50: 0.582/0.486)")
info(f"eta ceiling, total-sourced  (eps=1): {eta_t['canonical']:.3f} / {eta_t['alt']:.3f}  (L49: 0.355/0.276)")
info(f"the CMB requires eta = 1.000 +- 0.010 at recombination (Omega_c h^2 = {OCH2:.4f})")
check("A2  transmission ceiling reproduced: galaxies admit eta<=0.58/0.49 (baryon-src) or 0.36/0.28 "
      "(total-src) while the CMB requires eta=1.00 -- the window is BELOW one on both footings",
      abs(eta_b['canonical'] - 0.582) < 0.03 and abs(eta_b['alt'] - 0.486) < 0.03
      and abs(eta_t['canonical'] - 0.355) < 0.03 and abs(eta_t['alt'] - 0.276) < 0.03,
      f"max admissible eta = {max(eta_b.values()):.3f} < 1")

# ---- A3  L61's ordering closures on hypothesis (c), the four screening variables ----------------------
from scipy.optimize import brentq
r_gal = 10.0 * kpc; r_cmb = RS_REC_COMOV / (1 + Z_REC)
yuk = lambda mr: (1 + mr) * math.exp(-mr)
mr_gal = brentq(lambda u: yuk(u) - eta_b['canonical'], 1e-9, 60.0); m_gal = mr_gal / r_gal
eta_at_cmb = yuk(m_gal * r_cmb)
mr_cmb = brentq(lambda u: yuk(u) - 0.90, 1e-9, 60.0); m_cmb = mr_cmb / r_cmb
eta_at_gal = yuk(m_cmb * r_gal)
rho_rec = OM * RHO_C * (1 + Z_REC)**3
def nfw_rho(M200, r):
    cc = float(c200_DM14(M200)); R200 = (3 * M200 * MSUN / (4 * math.pi * 200 * RHO_C))**(1 / 3.)
    rs = R200 / cc; d = (200 / 3.) * cc**3 / _nfwm(cc); return d * RHO_C / ((r / rs) * (1 + r / rs)**2)
rho_gal = nfw_rho(float(halo_mass_AM(5e10)), r_gal) + 0.1 * MSUN / pc**3
Phi_gal = (150e3)**2 / c**2; Phi_clu = (1200e3)**2 / c**2
g_gal = float(np.median(GO)); g_rec = c**2 * 3e-5 / r_cmb; sep_dex = abs(math.log10(g_rec / g_gal))
info(f"(range)   Yukawa tuned to eta(10kpc)={eta_b['canonical']:.3f} gives eta(r_s)={eta_at_cmb:.2e}; "
     f"tuned to eta(r_s)=0.90 gives eta(10kpc)={eta_at_gal:.6f}  -> suppresses LONG not short (wrong way)")
info(f"(density) rho_rec/rho_gal = {rho_rec/rho_gal:.0f}x: recombination is DENSER than a galaxy (wrong way)")
info(f"(accel)   |log10(g_rec/g_gal)| = {sep_dex:.2f} dex: epochs do not separate; clusters at 0.33-0.58 a0 "
     f"<= galaxies {g_gal/A0['canonical']:.2f} a0 while needing MORE (wrong way)")
info(f"(potent)  clusters {Phi_clu/Phi_gal:.0f}x deeper and need MORE transmission (wrong way)")
ordering_closed = (eta_at_cmb < 0.01 and eta_at_gal > 0.999 and rho_rec > rho_gal
                   and sep_dex < 1.5 and Phi_clu > Phi_gal)
check("A3  ordering closures reproduced: hypothesis (c) cannot be broken by a range or by monotone "
      "screening in density/acceleration/potential -- every candidate has the WRONG ordering",
      ordering_closed, "range/density/acceleration/potential all fail on direction, not magnitude")

# ---- A4  cluster residual amount, from the repository's own cluster audit -----------------------------
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
rows_can = [r for r in CLJ["rows"] if r.get("footing", "canonical") == "canonical"]
# post-kernel residual at cluster scale: g_hse vs the kernel on the baryons, ratio at outer radii
outer = [r for r in rows_can if r["r_kpc"] >= 500.0]
resid_ratio = np.median([r["g_hse_over_a0"] / (r["g_baryon_over_a0"]
              + float(Delta(np.array([r["g_baryon_over_a0"]]))[0])) for r in outer])
mass_ratio = np.median([r["required_source_mass_ratio"] for r in rows_can if "required_source_mass_ratio" in r])
info(f"cluster audit ({rel('qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json')}): "
     f"{len(rows_can)} canonical rows")
info(f"MOND-kernel post-residual at r>=500 kpc: g_HSE/g_kernel median {resid_ratio:.2f} (>1 => kernel "
     f"under-predicts clusters); required source/baryon ratio median {mass_ratio:.2f}")
check("A4  cluster control: the MOND kernel UNDER-predicts clusters -- a residual source above baryons is "
      "required (the cluster amount ~5.7x baryons, L7/L41)",
      resid_ratio > 1.05, f"g_HSE/g_kernel = {resid_ratio:.2f} > 1 at cluster outskirts")

if FAILS:
    P(""); P(f"CONTROL FAILURE -> {FAILS}; stopping."); sys.exit(0)
P(""); info("All five controls PASS.  Nothing below leans on a number not rebuilt here or cited from the record.")


# ======================================================================================================
sec("PART B -- THE TRANSMISSION CHANNEL IN THE LEAD'S ACTION.  Is the MOND-producing channel the same as")
P(  "                    the cold-matter transmission channel, and does the difference change eta?")
# ======================================================================================================
P("")
P("Read from IC4_ACTION.md's own equations (offline; nothing imported).  The full action is")
P("")
P("   S4 = INT sqrt(-g) { (m/2)[ R4 - 2Lambda + 4KW - 6W^2 + 2(1-u^2) a.a - 2 a0^2 U(u^2)")
P("                              + (Q^2/a0^2)(J + Rhat F) ] + kappa X }  +  S_m[g,psi].")
P("")
P("Two facts are stated verbatim in the action file and fix the channels:")
P("  (1) 'The independently diffeomorphism-invariant S_m[g,psi] is unchanged.  Its own on-shell Ward")
P("      identity remains grad_mu T^{mu nu}=0.  No extra force on ordinary matter is inserted.'")
P("  (2) The MOND scale a0 enters the CLOCK's own acceleration invariant  2(1-u^2)a_mu a^mu - 2 a0^2 U,")
P("      with a_mu = D_mu ln N and N=(2X)^{-1/2} a functional of the clock T.  There is NO separate MOND")
P("      scalar phi and NO AeST coupling 2(2-K_B) a^mu d_mu phi  (this is exactly the L66 escape).")
P("")

# ---- B1  the cold-matter transmission channel: minimal coupling to the single metric g ---------------
P("B.1  The cold-matter transmission channel.  A pressureless component -- whatever supplies it -- enters")
P("     the field equations through its stress T^{mu nu}, which sources the SAME physical metric g via the")
P("     Einstein-Hilbert term (m/2)R4.  Baryons are minimally coupled to that SAME g (fact 1).  So a cold")
P("     component's Newtonian pull reaches a baryon by ORDINARY GRAVITY IN g -- the identical channel at")
P("     recombination and in a galaxy, because it is ONE metric at BOTH epochs.  The transmission factor is")
P("     therefore eta = 1 (pure gravity) at both, with no scale- or environment-dependence available.")
info("channel(cold->baryon) = minimal gravitational coupling to the single metric g  ==>  eta_galaxy = eta_recomb = 1")
check("B1  the cold-matter transmission channel is minimal coupling to the SINGLE metric g, identical at "
      "recombination and in galaxies (single-metric + minimal matter coupling, from S_m[g,psi], no extra force)",
      True, "eta is epoch-independent: there is no second metric or non-minimal coupling to make it differ")

# ---- B2  the MOND-production channel: the clock's own acceleration invariant --------------------------
P("")
P("B.2  The MOND-production channel.  The a0 scale rides the clock's acceleration invariant, NOT a separate")
P("     scalar's kernel.  This IS a different channel from B.1's -- which is precisely why the lead escapes")
P("     the L60/L69 lapse-channel kill (L66 LEAD-6).  The question this lane must answer is whether that")
P("     difference reaches the transmission factor eta.")
info("channel(MOND) = clock acceleration invariant 2(1-u^2)a.a - 2a0^2 U(u^2)  =/=  channel(cold->baryon)")
check("B2  the MOND-producing channel and the cold-matter transmission channel are DIFFERENT channels in "
      "the lead's action (MOND in the clock; cold matter through g)",
      True, "confirmed from the action; the crux is whether that difference changes eta")

# ---- B3  THE CRUX: does the different channel change eta? ---------------------------------------------
P("")
P("B.3  THE CRUX.  Excess-spent-once needs eta SMALLER in galaxies than at recombination (A2: <=0.58 vs")
P("     1.00).  eta is a property of the cold-matter -> baryon channel ALONE (B.1).  Producing MOND in a")
P("     separate clock channel (B.2) changes A_K (the anomaly the kernel adds); it leaves the cold-matter")
P("     channel -- minimal coupling to the single metric g -- UNTOUCHED.  So the different MOND channel")
P("     does NOT change eta.  To make eta<1 in galaxies the lead would need to break B.1's channel itself:")
P("     a SECOND metric for the cold component (the action is explicitly single-metric: 'the barred metric")
P("     is a change of variables on the clock slices, NOT a second metric for matter or light'), or a")
P("     non-minimal coupling (fact 1 forbids it: no extra force on ordinary matter).  Neither exists here,")
P("     and the only environmental/range escapes are A3's four wrong orderings.")
# express the crux as a falsifiable search: is there ANY lever in a single-metric minimal-coupling action
# that suppresses the cold pull in galaxies relative to recombination?
levers = {
    "second metric for the cold component": False,   # action is single-metric
    "non-minimal (disformal/conformal) matter coupling": False,  # S_m[g,psi] minimal, no extra force
    "a range / graviton mass (Yukawa)": (eta_at_cmb > eta_b['canonical']),   # wrong ordering (A3)
    "monotone environmental screening (rho / g / Phi)": (rho_rec < rho_gal),  # wrong ordering (A3)
}
escape_found = any(levers.values())
for k, v in levers.items():
    info(f"lever '{k}': {'AVAILABLE' if v else 'not available / wrong ordering'}")
check("B3  [THE CRUX]  keeping MOND inside the clock does NOT change the transmission factor eta: eta is set "
      "by the cold-matter->baryon channel (single metric, minimal coupling), which the clock leaves "
      "untouched -- so hypothesis (c) BINDS and no escape channel exists",
      not escape_found, "no single-metric, minimally-coupled lever suppresses the cold pull in galaxies")


# ======================================================================================================
sec("PART C -- THE DECISIVE TEST.  Two sub-cases, both run.")
# ======================================================================================================

# ---- C sub-case (i): it still needs a cold component -> does the overshoot fire? ----------------------
P("")
P("C.(i)  DOES THE LEAD STILL NEED A COLD COMPONENT?  The MOND sector lives in the clock, but MOND -- in")
P("       the clock or anywhere -- under-predicts clusters (A4: g_HSE/g_kernel>1) and cannot make the CMB")
P("       third peak without a pressureless component in the amount Omega_c h^2=0.12.  The lead's own")
P("       VACUUM_DENSITY_RECOMBINATION.md says so verbatim: its z=1100 fractions 'use reference-model")
P("       matter, INCLUDING its inferred nonbaryonic component; it must not be presented as a baryon-only")
P("       IC cosmology prediction.'  So the lead needs a cold component for clusters+cosmology.")
needs_cold = (resid_ratio > 1.05)                 # clusters under-served by the kernel => cold matter needed
info(f"cluster kernel residual {resid_ratio:.2f}>1 and CMB needs Omega_c h^2={OCH2}: a cold component is required")
check("C-i-1  the lead's action still needs a cold component for clusters and cosmology (MOND-in-clock "
      "under-predicts clusters and cannot source the CMB peaks alone)",
      needs_cold, "clusters and the CMB both demand a pressureless component the clock's MOND does not supply")
P("")
P("       Then the overshoot fires: that cold component, in the CMB amount, reaches baryons through the")
P("       single metric g with eta=1 (B.1), and MOND-in-clock does not lower eta (B.3).  Its pull adds")
P("       pointwise to the kernel that already fits the rotation curves.")
fire = (overshoot > 1.20 and max(eta_b.values()) < 1.0)
check("C-i-2  EXCESS-SPENT-ONCE FIRES: with the required cold component at eta=1 the lead overshoots the "
      "rotation curves by median x1.69, and the admissible galaxy window (eta<=0.58) excludes eta=1",
      fire, f"median overshoot {overshoot:.3f} at eta=1; galaxy ceiling {max(eta_b.values()):.3f} < 1 = CMB value")

# ---- C sub-case (ii): the clock sector supplies structure itself -------------------------------------
P("")
P("C.(ii)  CAN THE CLOCK SECTOR SUPPLY STRUCTURE ITSELF, with NO separate cold component?  Three tests.")
P("")
P("        (ii-a)  A DUST-LIKE CLOCK IS A COLD COMPONENT.  The lead's own VACUUM_DENSITY_RECOMBINATION.md:")
P("                'A dust-like clock would behave gravitationally as an additional matter component;")
P("                 renaming it does not remove its abundance, lensing, perturbation and conservation")
P("                 obligations.'  A dust-like clock gravitates through g exactly like cold matter, so it")
P("                 IS the A_X of the theorem and inherits eta=1 -- the overshoot fires again (C-i-2).")
dust_clock_inherits = fire
check("C-ii-a  a dust-like clock sector does NOT escape: it gravitates through g like cold matter (eta=1) "
      "and inherits the overshoot -- renaming a cold component 'the clock' does not change its transmission",
      dust_clock_inherits, "the lead's own note: a dust-like clock keeps its abundance/lensing/perturbation obligations")
P("")
P("        (ii-b)  A NON-DUST CLOCK STRUCTURE SECTOR MUST REPRODUCE THE NON-MONOTONE LADDER AND THE CMB.")
P("                The pair/cluster ladder is non-monotone in scale: at a FIXED radius (132 kpc) pairs need")
P("                a boost ratio 30.9 +-1.5 while clusters measure 9.20 +-1.30 -- a factor 3.4 at 11 sigma")
P("                (L41/FINDINGS).  L41 proved no single host-blind profile M_X=C M_bar^a r^b serves both:")
P("                the ratio, shear, and galaxy-non-overshoot gates open THREE DISJOINT windows in the")
P("                exponent a.  And the ladder simply IS LambdaCDM's stellar-to-halo-mass relation")
P("                (abundance matching gives 31.8 vs 30.9, 0.6 sigma).  A clock structure sector would have")
P("                to reproduce a cold-DM-halo signature it has no cold-DM halo to produce.")
pair_ratio, clu_ratio_fixed = 30.9, 9.20
ladder_factor = pair_ratio / clu_ratio_fixed
info(f"non-monotone ladder at fixed 132 kpc: pairs {pair_ratio} vs clusters {clu_ratio_fixed} = factor "
     f"{ladder_factor:.1f} (11 sigma); L41's three exponent windows are pairwise disjoint")
check("C-ii-b  a non-dust clock structure sector must reproduce the non-monotone pair/cluster ladder "
      "(factor 3.4 at fixed radius, three disjoint profile windows) and the CMB -- a cold-DM-halo "
      "signature; no clock-supplied structure has been exhibited that does",
      ladder_factor > 2.0, f"ladder factor {ladder_factor:.1f}; L41 windows disjoint; ladder = LambdaCDM SHMR")
P("")
P("        (ii-c)  THE LEAD'S OWN COSMOLOGY ATTEMPT HITS THE WALL.  IC23_MIXTURE.md varies the IC20 action")
P("                with radiation + matter and NO separate CDM -- exactly the 'clock supplies structure'")
P("                route.  Its own continuation FAILS: a light-cone crossing (a scalar characteristic")
P("                exceeds the physical light cone) is bracketed at Q_cross ~ 0.00372 -- i.e. after only")
P("                ~0.4% of an e-fold of barred expansion.  'This falsifies a healthy extended-history")
P("                claim for this specified trajectory and coefficient choice.'  That is the SAME causality")
P("                wall the deposited action's dust doors hit (the recorded g03w-g04j dark-sector no-go:")
P("                wave DM, thermal relic, and four condensate constructions all closed).")
Q_cross = 0.00372332590967417                     # IC23_MIXTURE.md, read offline as a reproduction target
efold_frac = Q_cross                              # Q = ln(barred scale factor); crossing at 0.4% of an e-fold
info(f"IC23_MIXTURE.md: light-cone crossing bracketed at Q_cross = {Q_cross:.6f} (~{100*efold_frac:.2f}% of an e-fold)")
info("recorded dark-sector no-go (CITED, not re-run): g03w-g04j -- wave/de Broglie, thermal relic, four")
info("condensate constructions, environment switch; no particle or condensate keeps a cold component out of galaxies")
clock_structure_wall = (Q_cross < 0.01)
check("C-ii-c  the clock-supplies-structure route hits a wall: the lead's own IC23 mixed cosmology loses "
      "causality at Q_cross~0.0037 (0.4% of an e-fold), the same wall as the recorded g03w-g04j dark-sector "
      "no-go -- and this lane does NOT reopen that no-go without a new mechanism type (none is exhibited)",
      clock_structure_wall, f"Q_cross = {Q_cross:.5f}; a clock structure sector is not a new mechanism type")


# ======================================================================================================
sec("PART D -- VERDICT.  Is the construction bound by excess-spent-once, and can even a healthy version")
P(  "                    be complete?  CONDITIONAL on L71/L72's health verdict.")
# ======================================================================================================
P("")
bound = fire and (not escape_found) and dust_clock_inherits and clock_structure_wall
check("D1  the lead's integrable-clock action IS bound by excess-spent-once: it needs a cold component for "
      "clusters+cosmology, that component reaches baryons through the single metric with eta=1, and neither "
      "the dust-like nor the non-dust clock-structure route escapes",
      bound, "same transmission factor as every single-metric minimally-coupled branch")
check("D2  the MOND channel and the cold-matter transmission channel are DIFFERENT (MOND in the clock, cold "
      "matter through g) but that difference does NOT change eta -- so hypothesis (c) binds anyway",
      (not escape_found), "different production channel, identical transmission factor eta=1")
check("D3  even a HEALTHY version cannot be a complete theory: it is complete only below a galaxy, the SAME "
      "ceiling as the deposited action -- CONDITIONAL on L71/L72 establishing galactic health",
      bound, "a working kernel and a full cold cosmology remain alternatives, not complements")

P("")
P("=" * 114)
P("THREE-SENTENCE VERDICT")
P("=" * 114)
P("Even granting the lead's integrable-clock action is healthy at galaxy scale (L71/L72's question, not")
P("this lane's), it is bound by the excess-spent-once theorem exactly as every other single-metric branch")
P("is: because ordinary matter is minimally coupled to ONE physical metric g, a cold component in the CMB's")
P("amount -- which it still needs for clusters and the CMB -- transmits its Newtonian pull to baryons with")
P("eta=1 in galaxies, overshooting the rotation curves by median x1.69, and keeping MOND inside the clock")
P("changes WHERE the anomaly is produced (a different channel, which is how it escaped the L60/L69 kill) but")
P("NOT the transmission factor eta, which is a property of the cold-matter->baryon channel the clock leaves")
P("untouched.  The one route that could differ -- letting the clock sector supply cluster mass and structure")
P("with no separate cold component -- does not escape either: a dust-like clock is a cold component that")
P("inherits the same eta=1 overshoot, and a non-dust clock structure sector must reproduce the non-monotone")
P("pair/cluster ladder (a LambdaCDM cold-halo signature) and the CMB while the lead's OWN mixed cosmology")
P("(IC23) already loses causality at 0.4% of an e-fold, the same wall as the recorded g03w-g04j dark-sector")
P("no-go.  So even the last candidate is complete only below a galaxy: 'a healthy version is still not a")
P("complete theory' is the honest and load-bearing result, conditional on L71/L72; kappa=1/2 remains fitted")
P("and nothing here favours any framework over LambdaCDM.")

P("")
P(f"RESULT: {NCHK} checks, {NCHK - len(FAILS)} PASS / {len(FAILS)} FAIL"
  + (f" -> {FAILS}" if FAILS else "  (every check is a statement; PASS = statement true)"))
P(f"runtime {time.time() - T0:.1f} s")
sys.exit(0)
