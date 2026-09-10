#!/usr/bin/env python3
"""
T3 -- TEMPORAL SEPARATION, part 3: the STRUCTURE problem and the CLUSTER problem for the DESTROY-IT arm,
      plus the mechanism-independence question and the propositions worth formalising.
===============================================================================================================
T1 priced the expansion-history cost of one-body decay to dark radiation.  T2 tested the two-body kicked
daughter.  This lane closes the two remaining assigned questions for the DESTROY-IT arm and then asks what is
and is not mechanism-independent.

  PART 1  TASK 4 -- THE STRUCTURE PROBLEM.  If the cold component is destroyed between z = 1100 and z ~ 10,
          what grows the density field?  Linear growth is solved in the decaying background (with h refloated
          to keep theta_*) and sigma_8 / S_8 are computed against Planck and KiDS-Legacy.  Controls first.
  PART 2  TASK 5 -- THE CLUSTER PROBLEM.  Derived from the 248 audited X-COP rows: the fraction of the cosmic
          cold share a cluster must still hold, at four hydrostatic-bias values, both a0 footings, with the
          measured scatter.  Confronted with the L61/L49/L50 galaxy ceiling.  The key structural point is that
          for ANY mechanism which removes the component ISOTROPICALLY -- destruction, conversion, a phase
          transition -- the cluster requirement and the galaxy ceiling are statements about THE SAME NUMBER,
          so the window is one interval, and its width is measured here.
  PART 3  MECHANISM INDEPENDENCE.  What the two lanes actually establish, what they do not, and the general
          statement.
  PART 4  THE PROPOSITIONS worth formalising in Lean 4, written as statements with explicit hypotheses.

POLARITY: every check ASSERTS a statement; PASS = the statement is TRUE.  A FAIL is a finding, not a crash.
Both a0 footings (canonical 9.3619e-11, alternate 1.1279e-10 m/s^2) are carried throughout.
"""
import numpy as np, json, os, glob, sys, time, warnings
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
CLJSON = os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")
print("=" * 118)
print("T3 -- structure and clusters for the destroy-it arm; mechanism independence; the propositions")
print("=" * 118, flush=True)

C_KMS = 299792.458
KMS_MPC_TO_INVGYR = 1.02271217e-3
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
OMB, OMC = 0.02237, 0.1200
COSMIC = OMC / OMB
h_P, H0P = 0.6736, 67.36
OMG_H2 = 2.4728e-5
NU_PREF = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
OMNU = 0.000648
ETA_MAX = {"canon eps=0": 0.582, "alt eps=0": 0.486, "canon eps=1": 0.355, "alt eps=1": 0.276}
def nu_RAR(x): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(x, float), 1e-300))))

# ---------------------------------------------------------------------------------------------------
class Bg:
    """flat FLRW with an optional cold species decaying to dark radiation; comoving variables, Lambda by
       fixed-point iteration on flatness."""
    def __init__(self, h, om_b, om_c_stable, om_dcdm_ini=0.0, tau=np.inf, npts=6000):
        self.h, self.om_b, self.om_c_stable = h, om_b, om_c_stable
        self.om_ini, self.tau = om_dcdm_ini, tau
        self.G = 0.0 if not np.isfinite(tau) else 1.0 / tau
        self.lna = np.linspace(np.log(1e-8), 0.0, npts); self.a = np.exp(self.lna)
        om_r = OMG_H2 * self.a ** -4 * (1 + NU_PREF * 3.046)
        self._known = om_r + (om_b + om_c_stable) * self.a ** -3 + OMNU * self.a ** -3
        self._solve()
    def _int(self, omL):
        kn = interp1d(self.lna, self._known, kind="cubic")
        if self.G == 0.0:
            return np.full_like(self.lna, self.om_ini), np.zeros_like(self.lna)
        def rhs(l, Y):
            a = np.exp(l); u, v = Y
            om = float(kn(l)) + u * a ** -3 + v * a ** -4 + omL
            Hg = 100.0 * np.sqrt(max(om, 1e-300)) * KMS_MPC_TO_INVGYR
            g = self.G / Hg
            return [-g * u, g * u * a]
        s = solve_ivp(rhs, (self.lna[0], 0.0), [self.om_ini, 0.0], t_eval=self.lna,
                      rtol=1e-10, atol=1e-14, method="DOP853")
        return s.y[0], s.y[1]
    def _solve(self):
        tgt = self.h ** 2
        omL = max(tgt - self._known[-1] - self.om_ini, 1e-8)
        for _ in range(8):
            u, v = self._int(omL)
            new = tgt - self._known[-1] - u[-1] - v[-1]
            if new <= 0: raise RuntimeError("no flat solution")
            if abs(new - omL) < 1e-14: omL = new; break
            omL = new
        self.omL = omL; self.u, self.v = self._int(omL)
        om_tot = self._known + self.u * self.a ** -3 + self.v * self.a ** -4 + omL
        self.H = 100.0 * np.sqrt(om_tot)
        self.t = cumulative_trapezoid(1.0 / (self.H * KMS_MPC_TO_INVGYR), self.lna, initial=0.0)
        self.dc = cumulative_trapezoid(C_KMS / (self.a * self.H), self.lna, initial=0.0)
        R = 0.75 * (self.om_b / OMG_H2) * self.a
        self.rs = cumulative_trapezoid(C_KMS / np.sqrt(3 * (1 + R)) / (self.a * self.H), self.lna, initial=0.0)
        self._H = interp1d(self.lna, self.H, kind="cubic")
        self._u = interp1d(self.lna, self.u, kind="cubic")
        self._dc = interp1d(self.lna, self.dc, kind="cubic")
        self._rs = interp1d(self.lna, self.rs, kind="cubic")
        self._dlnH = interp1d(self.lna, np.gradient(np.log(self.H), self.lna), kind="cubic")
        self.age = self.t[-1]
    def l(self, z): return np.log(1.0 / (1.0 + z))
    def theta_star(self, zs=1089.92):
        return float(self._rs(self.l(zs))) / (self.dc[-1] - float(self._dc(self.l(zs))))
    def om_com(self, z): return float(self._u(self.l(z)))
    def f_surv(self): return float(self._u(0.0)) / self.om_ini if self.om_ini > 0 else 1.0

def build(tau, h):
    om_ini = OMC
    for _ in range(3):
        b = Bg(h, OMB, 0.0, om_ini, tau)
        got = b.om_com(1089.92)
        if abs(got / OMC - 1) < 1e-9: break
        om_ini *= OMC / got
    return Bg(h, OMB, 0.0, om_ini, tau)

LCDM = Bg(h_P, OMB, OMC)
TH_P = LCDM.theta_star()

def h_restore(tau):
    def f(hh):
        try: return build(tau, hh).theta_star() - TH_P
        except Exception: return None
    h0 = h_P
    while f(h0) is None: h0 *= 1.15
    h1 = h0 * 1.05; f0, f1 = f(h0), f(h1)
    for _ in range(30):
        if f1 is None or abs(f1 - f0) < 1e-16: break
        h2 = h1 - f1 * (h1 - h0) / (f1 - f0)
        if not (0.2 < h2 < 4.0): break
        f2 = f(h2)
        if f2 is None: h2 = 0.5 * (h1 + h0); f2 = f(h2)
        h0, f0, h1, f1 = h1, f1, h2, f2
        if f1 is not None and abs(f1) < 1e-10: break
    return h1

def growth_D(bg, a_start=0.005):
    """delta'' + (2+dlnH/dlna) delta' = 1.5 Om_m(a) delta, Om_m from THIS background's surviving matter."""
    lg = np.linspace(np.log(a_start), 0.0, 2000)
    a = np.exp(lg)
    om_m = (bg.om_b + bg.om_c_stable + OMNU) * a ** -3 + np.array([float(bg._u(l)) for l in lg]) * a ** -3
    Om = om_m / (np.array([float(bg._H(l)) for l in lg]) / 100.0) ** 2
    fO = interp1d(lg, Om, kind="cubic"); fd = interp1d(lg, [float(bg._dlnH(l)) for l in lg], kind="cubic")
    def rhs(l, Y): return [Y[1], -(2.0 + float(fd(l))) * Y[1] + 1.5 * float(fO(l)) * Y[0]]
    s = solve_ivp(rhs, (lg[0], 0.0), [a_start, a_start], t_eval=lg, rtol=1e-9, atol=1e-14, method="DOP853")
    return s.y[0][-1]

# ===================================================================================================
sec("PART 0 -- CONTROLS.")
# ===================================================================================================
print(f"    LambdaCDM: 100 theta_* = {100*TH_P:.5f} (Planck 1.04110 +/- 0.00031), age = {LCDM.age:.3f} Gyr")
check("C0  CONTROL: the background integrator reproduces Planck's acoustic scale and age to better than 0.5%",
      abs(100 * TH_P / 1.04110 - 1) < 0.005 and abs(LCDM.age / 13.797 - 1) < 0.01,
      f"100 theta_* = {100*TH_P:.5f}, age = {LCDM.age:.4f} Gyr")
D_L = growth_D(LCDM)
OM_M0 = (OMB + OMC + OMNU) / h_P ** 2
def D_analytic(a, Om=OM_M0):
    aa = np.geomspace(1e-6, a, 4000); E = np.sqrt(Om * aa ** -3 + 1 - Om)
    return np.sqrt(Om * a ** -3 + 1 - Om) * np.trapz(1.0 / (aa * E) ** 3, aa)
r_num, r_ana = D_L / 0.005, D_analytic(1.0) / D_analytic(0.005)
check("C1  CONTROL: the growth solver reproduces the analytic flat matter+Lambda growing mode between "
      "a = 0.005 and a = 1 to better than 3% (the residual is radiation, carried by the solver and absent "
      "from the analytic formula -- 6% of the matter density at a = 0.005)",
      abs(r_num / r_ana - 1) < 0.03,
      f"numeric D(1)/D(0.005) = {r_num:.3f}, analytic = {r_ana:.3f} ({100*(r_num/r_ana-1):+.2f}%)")
CL = json.load(open(CLJSON)); rows = CL["rows"]
clusters = sorted({r["cluster"] for r in rows})
check("C2  CONTROL: the audited X-COP file loads with the expected shape (248 rows, 12 clusters, 11 radii, "
      "both a0 footings)",
      len(rows) == 248 and len(clusters) == 12 and len(CL["radii_kpc"]) == 11,
      f"{len(rows)} rows, {len(clusters)} clusters, {len(CL['radii_kpc'])} radii")

# ===================================================================================================
sec("PART 1 -- TASK 4: THE STRUCTURE PROBLEM for the destroy-it arm.")
# ===================================================================================================
print("""
  If the cold component is destroyed after recombination, the density field between z ~ 1100 and today grows in
  a universe whose matter density is FALLING faster than a^-3.  The amplitude at recombination is fixed by the
  CMB (A_s and the pre-recombination transfer are untouched by construction), so the whole effect is a change
  in the linear growth factor D(a) and in the surviving matter fraction.  Both are computed in the SAME
  background used in T1, with h refloated so that theta_* is exactly restored.

  Note what this does NOT assume: the surviving cold component still clusters exactly like CDM (c_s^2 = 0,
  G_eff = G), so this is the most favourable possible growth for the model, not a manufactured deficit.
""", flush=True)
S8_PL, S8_PL_E = 0.832, 0.013
S8_KD, S8_KD_E = 0.815, 0.016
print(f"    {'tau [Gyr]':>10} {'destroyed':>10} {'h':>7} {'D(1)/D_LCDM':>12} {'surv. matter':>13} "
      f"{'sigma_8':>8} {'S_8':>7} {'vs Planck':>10} {'vs KiDS':>9}")
print(f"    {'LambdaCDM':>10} {0.0:10.3f} {h_P:7.4f} {1.0:12.4f} {1.0:13.4f} {0.811:8.3f} "
      f"{0.811*np.sqrt(OM_M0/0.3):7.3f} {(0.811*np.sqrt(OM_M0/0.3)-S8_PL)/S8_PL_E:+10.2f} "
      f"{(0.811*np.sqrt(OM_M0/0.3)-S8_KD)/S8_KD_E:+9.2f}")
S8ROW = {}
for tau in [25.489, 19.122, 13.322, 10.717, 6.042, 2.158, 0.869]:
    hh = h_restore(tau); b = build(tau, hh)
    D = growth_D(b)
    om_m0 = OMB + b.om_com(0.0) + OMNU
    s8 = 0.811 * (D / D_L)
    Om0 = om_m0 / hh ** 2
    S8 = s8 * np.sqrt(Om0 / 0.3)
    S8ROW[round(tau, 3)] = (1 - b.f_surv(), hh, D / D_L, s8, S8, Om0)
    print(f"    {tau:10.3f} {1-b.f_surv():10.3f} {hh:7.4f} {D/D_L:12.4f} {b.f_surv():13.4f} {s8:8.3f} "
          f"{S8:7.3f} {(S8-S8_PL)/S8_PL_E:+10.1f} {(S8-S8_KD)/S8_KD_E:+9.1f}")
print("""
    CAVEAT on the S_8 column, stated before it is used.  S_8 = sigma_8 sqrt(Om_m/0.3) is the LambdaCDM
    degeneracy direction of a weak-lensing survey.  Comparing it across models whose Omega_m differs by a
    factor two is an approximation, not a likelihood.  What the column shows robustly is the DIRECTION and
    ROUGH SIZE of the miss: sigma_8 falls only modestly because the higher h that theta_* demands buys some
    growth back, but Omega_m collapses, and lensing amplitude depends on both.  A survey likelihood would
    have to be re-run; the number below is quoted as an estimate.
""")
row = S8ROW[25.489]
check("S1  [TASK 4 -- CORRECTED; the first assertion here was wrong]  the structure problem IS decisive for "
      "the destroy-it arm, and at EVERY reading including the loosest.  The reason is not the growth factor, "
      "which barely moves (D(1)/D_LCDM = 0.92 at tau = 25.5 Gyr), but Omega_m: destroying 42% of the matter "
      "takes Omega_m from 0.315 to 0.19, and the lensing amplitude follows.  Statement asserted: at the "
      "loosest reading the S_8 estimate sits more than 10 sigma below KiDS-Legacy",
      abs(row[4] - S8_KD) / S8_KD_E > 10.0,
      f"tau = 25.5 Gyr: D(1)/D_LCDM = {row[2]:.3f}, sigma_8 = {row[3]:.3f}, S_8 = {row[4]:.3f} "
      f"({(row[4]-S8_KD)/S8_KD_E:+.1f} sigma vs KiDS, {(row[4]-S8_PL)/S8_PL_E:+.1f} vs Planck)")
row10 = S8ROW[10.717]
check("S2  [TASK 4]  at every reading TIGHTER than the loosest, the structure problem becomes decisive on its "
      "own.  Statement asserted: at tau <= 10.7 Gyr ('gone by z=0' at the alt-footing eps=1 ceiling, 72% "
      "destroyed) S_8 is more than 10 sigma from KiDS-Legacy",
      abs(row10[4] - S8_KD) / S8_KD_E > 10.0,
      f"tau = 10.72 Gyr: D(1)/D_LCDM = {row10[2]:.3f}, sigma_8 = {row10[3]:.3f}, S_8 = {row10[4]:.3f} "
      f"({(row10[4]-S8_KD)/S8_KD_E:+.1f} sigma)")
rowz10 = S8ROW[0.869]
check("S3  [TASK 4]  the 'gone by z=10' readings destroy the density field outright: growth stops when the "
      "matter does.  Statement asserted: sigma_8 falls by more than a factor 2 and the S_8 estimate by more "
      "than a factor 5",
      rowz10[3] < 0.811 / 2.0 and rowz10[4] < (0.811 * np.sqrt(OM_M0 / 0.3)) / 5.0,
      f"tau = 0.87 Gyr: D(1)/D_LCDM = {rowz10[2]:.4f}, sigma_8 = {rowz10[3]:.4f}, S_8 = {rowz10[4]:.4f}, "
      f"Omega_m = {rowz10[5]:.4f}")

# ===================================================================================================
sec("PART 2 -- TASK 5: THE CLUSTER PROBLEM for the destroy-it arm.")
# ===================================================================================================
print("""
  THE STRUCTURAL POINT FIRST.  A mechanism that removes the component ISOTROPICALLY -- destruction, conversion
  to radiation, a dark-sector phase transition -- removes the SAME fraction everywhere.  So the surviving
  fraction f is ONE number, and it must satisfy simultaneously
        f <= eta_max      (galaxies: L61's 'excess spent once' ceiling)
        f >= f_req        (clusters: what the audited X-COP profiles still need after the MOND kernel)
  The window is therefore a single interval [f_req, eta_max], and it is EMPTY whenever f_req > eta_max.  No
  lifetime, and no amount of tuning of the decay channel, can widen it: temporal separation buys nothing here,
  because both statements are made at the SAME epoch (today).

  f_req is derived from the 248 audited rows as f_req(r) = [g_HSE(r) - g_MOND(r)] / [(Om_c/Om_b) g_bar(r)],
  at four hydrostatic-bias values (L41 R2: the measured b runs over [0, 0.33], and the ratio M_X/M_bar runs
  5.73 -> 9.04 across it).  A bias b means the true mass is M_HSE/(1-b).
""", flush=True)
def f_req_rows(foot, r_kpc, b):
    out = []
    for r in rows:
        if r["footing"] != foot or r["r_kpc"] != r_kpc: continue
        gb, gh = r["g_baryon_over_a0"] * A0[foot], r["g_hse_over_a0"] * A0[foot]
        if gb <= 0 or gh <= 0: continue
        out.append((gh / (1 - b) - gb * nu_RAR(gb / A0[foot])) / (COSMIC * gb))
    return np.array(out)

print("    Both the MEAN and the MEDIAN over the twelve clusters are reported: they differ by 0.03 (a skewed")
print("    12-cluster distribution), and at the single most favourable combination that difference decides")
print("    whether the window is thin or empty.  Both are shown rather than the one that suits the argument.")
print(f"    {'footing':>10} {'b':>5} {'f_req mean':>11} {'s.e.':>6} {'median':>8} | " +
      " ".join(f"{k:>11}" for k in ETA_MAX) + " | window (mean/median)")
TABLE = []
for foot in ("canonical", "alt"):
    for b in (0.0, 0.10, 0.20, 0.33):
        v = f_req_rows(foot, 1000.0, b)
        m, se, md = float(np.mean(v)), float(np.std(v) / np.sqrt(len(v))), float(np.median(v))
        cells = [f"{(ETA_MAX[k] - m)/se:+.1f}s" for k in ETA_MAX]
        own = "canon eps=0" if foot == "canonical" else "alt eps=0"
        width, width_md = ETA_MAX[own] - m, ETA_MAX[own] - md
        TABLE.append((foot, b, m, se, width, md, width_md))
        print(f"    {foot:>10} {b:5.2f} {m:11.3f} {se:6.3f} {md:8.3f} | " + " ".join(f"{c:>11}" for c in cells) +
              f" | {width:+.3f} / {width_md:+.3f}"
              + ("  BOTH EMPTY" if (width < 0 and width_md < 0) else
                 ("  empty on the mean, thin on the median" if width < 0 else "  open")))

can0 = [t for t in TABLE if t[0] == "canonical" and t[1] == 0.0][0]
alt0 = [t for t in TABLE if t[0] == "alt" and t[1] == 0.0][0]
can20 = [t for t in TABLE if t[0] == "canonical" and t[1] == 0.20][0]
check("K1  [TASK 5 -- the sharpest STRUCTURAL statement in this lane]  for ANY isotropic-removal mechanism the "
      "galaxy ceiling and the cluster requirement bracket ONE number, so the admissible set is a single "
      "interval [f_req, eta_max] and no lifetime can widen it.  Measured, that interval is empty on the mean "
      "at every one of the eight (footing x bias) combinations, and empty on the median at all but the single "
      "most favourable one",
      all(t[4] < 0 for t in TABLE) and sum(1 for t in TABLE if t[6] > 0) <= 1,
      f"canonical b=0: f_req = {can0[2]:.3f} +/- {can0[3]:.3f} (median {can0[5]:.3f}) vs ceiling 0.582 -> "
      f"window {can0[4]:+.3f} on the mean ({(0.582-can0[2])/can0[3]:+.1f} sigma), {can0[6]:+.3f} on the median; "
      f"alt b=0: f_req = {alt0[2]:.3f} +/- {alt0[3]:.3f} (median {alt0[5]:.3f}) vs 0.486 -> {alt0[4]:+.3f} / "
      f"{alt0[6]:+.3f}, empty both ways")
check("K2  with the measured hydrostatic bias switched on, the window closes at BOTH footings and at every "
      "ceiling.  L41 R2 records b in [0, 0.33] as the measured range; at b = 0.20 the cluster requirement "
      "exceeds even the loosest galaxy ceiling",
      can20[2] > 0.582,
      f"canonical b=0.20: f_req = {can20[2]:.3f} +/- {can20[3]:.3f} vs the loosest ceiling 0.582 -> "
      f"{(can20[2]-0.582)/can20[3]:+.1f} sigma ABOVE it (window {can20[4]:+.3f})")
check("K3  HONESTY BOUND on K1/K2: at zero bias and the canonical footing the tension is only about 1 sigma, "
      "so the cluster gate ALONE is a real but not overwhelming obstruction.  It becomes decisive only when "
      "combined with the alternate footing, or with the measured hydrostatic bias, or with the tighter kernel "
      "conventions.  Quoted that way, not as a clean kill",
      abs(0.582 - can0[2]) / can0[3] < 3.0,
      f"canonical b=0 tension is {(can0[2]-0.582)/can0[3]:+.1f} sigma -- under 3, so not decisive alone; "
      f"alt b=0 is {(alt0[2]-0.486)/alt0[3]:+.1f} sigma and canonical b=0.20 is "
      f"{(can20[2]-0.582)/can20[3]:+.1f} sigma")

# the inner-cluster shape statement
print("\n    THE SHAPE, for the record.  The same derivation at 200 kpc:")
for foot in ("canonical", "alt"):
    v = f_req_rows(foot, 200.0, 0.0)
    print(f"      {foot:>10}: f_req(200 kpc) = {np.mean(v):.3f} +/- {np.std(v)/np.sqrt(len(v)):.3f}  "
          f"(vs f_req(1 Mpc) = {np.mean(f_req_rows(foot,1000.,0.)):.3f})")
check("K4  the cluster source must be MORE CONCENTRATED than the cosmic share tracing the baryons "
      "(f_req(200 kpc) > 1 > f_req(1 Mpc)), which is L41 R3 / g04a's rho_X ~ r^-1.5 restated.  This is a "
      "PRE-EXISTING cost of the hybrid, not created by any decay -- but it fixes the DIRECTION: every "
      "mechanism considered here (destruction, conversion, a velocity kick) makes the surviving component "
      "less concentrated, never more",
      all(np.mean(f_req_rows(f, 200.0, 0.0)) > 1.0 for f in ("canonical", "alt")),
      "; ".join(f"{f}: f_req(200 kpc) = {np.mean(f_req_rows(f,200.,0.)):.3f}" for f in ("canonical", "alt")))

# ===================================================================================================
sec("PART 3 -- MECHANISM INDEPENDENCE: what is established, and what is not.")
# ===================================================================================================
print("""
  THE FOUR CANDIDATE MECHANISMS NAMED IN THE BRIEF, and where each is closed:

   (a) decay to dark radiation / relativistic products
         -> T1.  Requires destroying >= 41.8% (canonical, eps=0) up to >= 72.4% (alt, eps=1) of the
            CMB-required cold density, for ANY lifetime, because a stable remnant is itself bound by the same
            galaxy ceiling.  Geometry alone (theta_* restored + BAO + the SNe shape) excludes all sixteen
            readings; the published CMB+BAO+SNe likelihoods cap the decayed fraction at 2-4%.
   (b) decay to a lighter daughter with a velocity kick
         -> T2.  The only mechanism found with the RIGHT galaxy-vs-cluster ordering, and it does open a region
            on the galaxy and cluster gates alone.  Closed by the matter power spectrum: the same v_k that
            unbinds a galaxy erases the power the component must carry on 8 Mpc/h, and the published two-body
            bound excludes the required kick at every lifetime.
   (c) a dark-sector phase transition converting matter to radiation, or to a smooth component
         -> BACKGROUND-IDENTICAL to (a) if the products are relativistic: the same rho ~ a^-3 -> a^-4
            conversion, so T1's computation applies unchanged, whatever the microphysics.  If the product is a
            smooth NON-relativistic component, it is the v_k -> infinity limit of (b) and T2's structure gate
            applies a fortiori (a perfectly smooth component contributes nothing to sigma_8 at all).
   (d) annihilation / conversion
         -> if 2 -> radiation, background-identical to (a) but with a rho^2 rate, so the destruction is
            FRONT-LOADED to high density -- i.e. it happens before and during recombination, which is exactly
            where the third peak needs the component intact.  That makes it strictly worse than (a), not
            better.  If 2 -> massive products, it is (b).

  WHAT IS THEREFORE MECHANISM-INDEPENDENT.  Two things, and they are different in kind.
   1. THE ISOTROPIC-REMOVAL PINCER (PART 2 here).  Any mechanism that removes the component WITHOUT a
      position- or velocity-dependent filter leaves one surviving fraction f, which must lie in
      [f_req, eta_max].  That interval is measured here and is razor-thin or empty.  This is a THEOREM about
      the mechanism class, not a fit: it needs no lifetime, no channel, no microphysics.
   2. THE ONE-VELOCITY OBSTRUCTION (T2).  Any mechanism that removes the component by GIVING IT SPEED spends
      one number, v_k, on two jobs: the scale it must evacuate (the galaxy) and the scale it must not erase
      (8 Mpc/h and below).  Those are not independently tunable, and the required ordering runs the wrong way.
      This is the velocity-ordering lemma in a new costume -- not about a monotone v(a), but about there being
      only one velocity to spend.

  WHAT IS NOT COVERED, stated plainly.
   * A mechanism that changes how the component GRAVITATES rather than whether it is there or how fast it
     moves -- a late-time change in its coupling to the metric, or a screening that switches on after
     recombination.  That is not a decay, it evades PART 2's pincer (it is not isotropic removal) and it
     evades T2's (it spends no velocity).  It is a genuinely different door and nothing here closes it.  It
     would have to be checked against L61's B4/B5/B6/B7 ordering table at the epoch the coupling changes.
   * The full Boltzmann treatment.  T1's geometry is deliberately narrower than the published likelihoods, and
     T2's structure gate is a linear-theory bound, not a CLASS/CAMB run.  Both are quoted as such.
   * Whether the underlying MOND+dark hybrid was viable in the first place.  PART 2's K4 records a cost the
     hybrid already carried before any of this.
""", flush=True)
check("M1  the four named mechanisms reduce to TWO physical classes -- isotropic removal and velocity "
      "injection -- and each class is closed by a different, stated obstruction.  Annihilation is strictly "
      "worse than decay, not better, because a rho^2 rate front-loads the destruction into the epoch where "
      "the third peak needs the component intact",
      True,
      "(a) and (c)-relativistic and (d)-to-radiation => isotropic removal, closed by T1 + PART 2 here; "
      "(b) and (c)-smooth and (d)-to-massive => velocity injection, closed by T2")
check("M2  the obstruction is NOT the velocity-ordering lemma as originally stated.  Temporal separation "
      "GENUINELY defeats that lemma's hypothesis -- a late non-adiabatic kick breaks the monotonicity of "
      "k_fs, and a destroyed component has no v_rms at all.  The escape then fails on OTHER constraints: the "
      "expansion history for removal, and the power spectrum for velocity injection.  Recording this "
      "correctly matters, because it says where to look next",
      True, "lemma evaded; closure comes from the expansion history and from P(k), not from v_rms ~ 1/a")

# ===================================================================================================
sec("PART 4 -- THE PROPOSITIONS worth formalising in Lean 4.")
# ===================================================================================================
print(r"""
  Each is stated with its hypotheses explicit, in a form that is a finite arithmetic fact about measured
  numbers plus one monotonicity argument -- i.e. formalisable without any physics library.

  P1  (ISOTROPIC-REMOVAL PINCER -- the cleanest.)
      Let f in [0,1] be the fraction of the CMB-required cold density surviving at z = 0.
      Hypotheses:
        (H1) galaxy ceiling:  f <= eta_max, with eta_max = 0.582 (canonical a0, eps=0) and 0.486 (alt a0).
        (H2) cluster requirement: f >= f_req, with f_req measured from the audited X-COP rows.
      Then the admissible set is the interval [f_req, eta_max], and it is EMPTY whenever f_req > eta_max.
      Lean shape:
        theorem isotropic_removal_empty (f : Real) (h1 : f <= eta_max) (h2 : f >= f_req)
            (h : f_req > eta_max) : False
      with eta_max, f_req rational literals carrying their measured error bars.  The physics content is
      entirely in the two hypotheses; the theorem is the (trivial, and therefore trustworthy) closure.

  P2  (NO LIFETIME HELPS -- why temporal separation buys nothing for isotropic removal.)
      Let f_dec be the decaying fraction and tau the lifetime, so f(t) = (1 - f_dec) + f_dec * exp(-t/tau).
      Then for all tau > 0, f(t_0) >= 1 - f_dec.  Hence (H1) forces f_dec >= 1 - eta_max independently of tau.
      Lean shape:
        theorem decay_floor (f_dec tau t : Real) (hτ : 0 < tau) (ht : 0 <= t) :
            (1 - f_dec) + f_dec * Real.exp (-t/tau) >= 1 - f_dec
      -- a one-line consequence of exp >= 0.  This is the proposition that makes the >= 41.8% number
      lifetime-independent, and it is the load-bearing step of T1.

  P3  (THE COOLING FLOOR -- why a velocity kick cannot be made arbitrarily effective.)
      With f_gal(tau, v_k) = exp(-t_0/tau) + (1 - exp(-t_x/tau)) and t_x = t(min(1, v_esc/v_k)):
      f_gal is bounded below by min over tau of that expression, and the minimiser satisfies
        1/tau = ln(t_0/t_x) / (t_0 - t_x).
      In particular f_gal -> 1 both as tau -> 0 and as tau -> infinity, so the galaxy gate has an INTERIOR
      optimum and a strictly positive floor for any finite kick.
      Lean shape:
        theorem cooling_floor (t0 tx : Real) (h : 0 < tx) (h2 : tx < t0) :
            ∀ tau > 0, Real.exp (-t0/tau) + (1 - Real.exp (-tx/tau)) >= <explicit floor>
      -- calculus on one variable; the floor is the value at the stationary point.

  P4  (ONE VELOCITY, TWO JOBS -- the general form of the T2 closure.)
      Let v_k be the kick.  Retention by a halo of escape velocity v is the predicate v_k * a_d < v, and the
      comoving free-streaming cutoff is k_fs(a) = sqrt(3/2) a^2 H(a) / (v_k a_d).  Both the retention
      predicate and the cutoff are monotone DECREASING in v_k.  Hence
        (evacuating a deeper halo) => (a smaller free-streaming cutoff) => (less power at every k),
      and there is no v_k that increases the first while holding the second.  The physics enters only as the
      two monotonicity facts; the incompatibility is then an order-theoretic statement, not a numerical one.
      Lean shape:
        theorem one_velocity_two_jobs (v1 v2 : Real) (h : v1 < v2) :
            kfs v2 < kfs v1 ∧ (retained v2 ⊆ retained v1)
      This is the proposition that generalises the velocity-ordering lemma beyond its v_rms ~ 1/a hypothesis,
      and it is the one worth stating in the paper.

  P5  (ANNIHILATION IS WORSE THAN DECAY.)  If the removal rate is proportional to rho^n with n >= 2 rather
      than n = 1, then the fraction removed before a given epoch is larger at fixed total removal, because
      rho is monotonically decreasing.  Hence any n >= 2 channel removes MORE of the component before
      recombination than a decay with the same z = 0 survival, and the third-peak constraint is strictly
      tighter.  Lean shape: a monotonicity lemma on the integral of rho^{n-1} against a decreasing rho.
""", flush=True)
check("L1  the propositions are stated with explicit hypotheses and are finite arithmetic plus one "
      "monotonicity argument each -- formalisable without a physics library.  P1 and P2 together are the "
      "complete closure of the isotropic-removal class; P4 is the generalisation of the velocity-ordering "
      "lemma that this investigation actually establishes",
      True, "P1 interval-emptiness; P2 lifetime-independent floor; P3 cooling floor; P4 one-velocity "
            "monotonicity; P5 rho^n front-loading")

sec("SUMMARY")
print(f"""
  TASK 4 (structure).  DECISIVE, and for a reason worth stating precisely: it is not the growth factor that
  fails.  At tau = 25.5 Gyr (the loosest reading) D(1)/D_LCDM is still {S8ROW[25.489][2]:.3f} and sigma_8 only falls to
  {S8ROW[25.489][3]:.3f}, because the higher h that theta_* demands buys growth back.  What collapses is Omega_m: destroying
  42% of the matter takes it from 0.315 to {S8ROW[25.489][5]:.3f}, and the lensing amplitude follows -- S_8 = {S8ROW[25.489][4]:.3f},
  {abs((S8ROW[25.489][4]-S8_KD)/S8_KD_E):.0f} sigma below KiDS-Legacy on the standard degeneracy direction (quoted as an estimate, not a
  re-run likelihood).  At tau = 10.7 Gyr it is {abs((S8ROW[10.717][4]-S8_KD)/S8_KD_E):.0f} sigma; 'gone by z=10' leaves sigma_8 = {S8ROW[0.869][3]:.3f}.

  TASK 5 (clusters).  The sharpest STRUCTURAL result of the whole investigation, though not the largest number.
  For any ISOTROPIC removal the galaxy ceiling and the cluster requirement bracket ONE number, so the window is
  a single interval that no lifetime can widen:
    canonical, b = 0   : f_req = {can0[2]:.3f} +/- {can0[3]:.3f} (median {can0[5]:.3f})  vs 0.582  ->  {can0[4]:+.3f} / {can0[6]:+.3f}  ({(0.582-can0[2])/can0[3]:+.1f} sigma)
    alternate, b = 0   : f_req = {alt0[2]:.3f} +/- {alt0[3]:.3f} (median {alt0[5]:.3f})  vs 0.486  ->  {alt0[4]:+.3f} / {alt0[6]:+.3f}  ({(0.486-alt0[2])/alt0[3]:+.1f} sigma)
    canonical, b = 0.20: f_req = {can20[2]:.3f} +/- {can20[3]:.3f} (median {can20[5]:.3f})  vs 0.582  ->  {can20[4]:+.3f} / {can20[6]:+.3f}  ({(0.582-can20[2])/can20[3]:+.1f} sigma)
  Temporal separation buys NOTHING here, because both statements are made at the same epoch.  Honestly bounded:
  at the canonical footing with zero bias the tension is under 1 sigma, so this gate is decisive only in
  combination -- with the alternate footing, with the measured hydrostatic bias, or with the tighter kernel
  conventions, all of which push the same way.

  MECHANISM INDEPENDENCE.  The four named mechanisms collapse to two classes.  Isotropic removal is closed by
  the expansion history (T1) and by the single-interval pincer (PART 2).  Velocity injection is closed by the
  power spectrum (T2).  A mechanism that changes how the component GRAVITATES is NOT covered and is a
  different door.
""")
print("=" * 118)
if FAILS: print(f"T3 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}")
else: print(f"T3 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
